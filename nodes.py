from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.messages import get_buffer_string
from langchain_tavily import TavilySearch
from langchain_community.document_loaders import WikipediaLoader
import time
import asyncio

from models import (
    GenerateAnalystsState, InterviewState, ResearchGraphState,
    Perspectives, SearchQuery, Analyst
)
from prompts import (
    analyst_instructions, question_instructions, search_instructions,
    answer_instructions, section_writer_instructions, report_writer_instructions,
    intro_conclusion_instructions
)
from config import SCOPE_DATA_PATH, ENABLE_SCOPE

llm = ChatOpenAI(model="gpt-4o", temperature=0)
tavily_search = TavilySearch(max_results=3)

# SCOPE optimizer (lazy initialization)
_scope_optimizer = None


def get_scope_optimizer():
    """Get or create SCOPE optimizer instance."""
    global _scope_optimizer
    if _scope_optimizer is None and ENABLE_SCOPE:
        try:
            from scope import SCOPEOptimizer
            from scope.models import create_openai_model
            from config import OPENAI_API_KEY

            # Create SCOPE-compatible model
            scope_model = create_openai_model(
                model="gpt-4o",
                api_key=OPENAI_API_KEY
            )

            _scope_optimizer = SCOPEOptimizer(
                synthesizer_model=scope_model,
                exp_path=SCOPE_DATA_PATH,
                enable_quality_analysis=True,
                quality_analysis_frequency=1,  # Analyze every step
                synthesis_mode="efficiency",
                store_history=True
            )
        except Exception as e:
            # SCOPE initialization failed, continue without it
            print(f"⚠️  SCOPE initialization failed: {e}")
            return None
    return _scope_optimizer


def _observe_with_scope(optimizer, agent_name, agent_role, task, model_output, observations, current_prompt, task_id):
    """Helper to observe with SCOPE - bridges sync/async boundary."""
    if optimizer is None:
        return
    
    try:
        # Bridge sync→async: SCOPE is async, LangGraph nodes are sync
        result = asyncio.run(
            optimizer.on_step_complete(
                agent_name=agent_name,
                agent_role=agent_role,
                task=task,
                model_output=model_output,
                observations=observations,
                error=None,
                current_system_prompt=current_prompt,
                task_id=task_id
            )
        )
        if result:
            guideline, guideline_type = result
            print(f"📚 SCOPE learned ({guideline_type}): {guideline[:100]}...")
    except Exception as e:
        # Silently skip if SCOPE observation fails
        pass


def create_analysts(state: GenerateAnalystsState):
    """Create analysts based on topic and feedback"""
    topic = state['topic']
    max_analysts = state['max_analysts']
    human_analyst_feedback = state.get('human_analyst_feedback', '')

    structured_llm = llm.with_structured_output(Perspectives)
    system_message = analyst_instructions.format(
        topic=topic,
        human_analyst_feedback=human_analyst_feedback,
        max_analysts=max_analysts
    )

    analysts = structured_llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content="Generate the set of analysts.")
    ])

    return {"analysts": analysts.analysts}


def human_feedback(state: GenerateAnalystsState):
    """No-op node that should be interrupted on"""
    pass


def should_continue(state: GenerateAnalystsState):
    """Return the next node to execute"""
    human_analyst_feedback = state.get('human_analyst_feedback', None)
    if human_analyst_feedback:
        return "create_analysts"
    return "__end__"


def generate_question(state: InterviewState):
    """Node to generate a question"""
    analyst = state["analyst"]
    messages = state["messages"]

    system_message = question_instructions.format(goals=analyst.persona)
    question = llm.invoke([SystemMessage(content=system_message)] + messages)

    return {"messages": [question]}


def search_web(state: InterviewState):
    """Retrieve docs from web search with SCOPE optimization"""
    optimizer = get_scope_optimizer()
    agent_name = "search_query_generator_web"
    
    # Get evolved prompt from SCOPE if available
    if optimizer:
        strategic_rules = optimizer.get_strategic_rules_for_agent(agent_name)
        enhanced_prompt = search_instructions + strategic_rules
    else:
        enhanced_prompt = search_instructions
    
    # Generate search query with evolved prompt
    structured_llm = llm.with_structured_output(SearchQuery)
    search_query = structured_llm.invoke([
        SystemMessage(content=enhanced_prompt)
    ] + state['messages'])
    
    query_text = search_query.search_query
    
    # Execute search
    data = tavily_search.invoke({"query": query_text})
    search_docs = data.get("results", data)
    
    # Format results summary for SCOPE
    results_summary = f"Found {len(search_docs)} results"
    if search_docs:
        results_summary += f"\nTop result: {search_docs[0].get('url', 'N/A')}"
        results_summary += f"\nPreview: {search_docs[0].get('content', '')[:100]}..."
    
    # Let SCOPE observe and learn (with observations)
    _observe_with_scope(
        optimizer,
        agent_name=agent_name,
        agent_role="Generate effective web search queries",
        task=f"Generate query for: {state['messages'][-1].content[:150]}",
        model_output=query_text,
        observations=results_summary,
        current_prompt=enhanced_prompt,
        task_id=f"web_search_{int(time.time()*1000)}"
    )
    
    formatted_search_docs = "\n\n---\n\n".join([
        f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
        for doc in search_docs
    ])
    
    return {"context": [formatted_search_docs]}


def search_wikipedia(state: InterviewState):
    """Retrieve docs from wikipedia with SCOPE optimization"""
    optimizer = get_scope_optimizer()
    agent_name = "search_query_generator_wikipedia"
    
    # Get evolved prompt from SCOPE if available
    if optimizer:
        strategic_rules = optimizer.get_strategic_rules_for_agent(agent_name)
        enhanced_prompt = search_instructions + strategic_rules
    else:
        enhanced_prompt = search_instructions
    
    # Generate search query with evolved prompt
    structured_llm = llm.with_structured_output(SearchQuery)
    search_query = structured_llm.invoke([
        SystemMessage(content=enhanced_prompt)
    ] + state['messages'])
    
    query_text = search_query.search_query
    
    # Execute search
    search_docs = WikipediaLoader(
        query=query_text,
        load_max_docs=2
    ).load()
    
    # Format results summary for SCOPE
    results_summary = f"Found {len(search_docs)} Wikipedia articles"
    if search_docs:
        results_summary += f"\nTop article: {search_docs[0].metadata.get('source', 'N/A')}"
        results_summary += f"\nPreview: {search_docs[0].page_content[:100]}..."
    
    # Let SCOPE observe and learn (with observations)
    _observe_with_scope(
        optimizer,
        agent_name=agent_name,
        agent_role="Generate effective Wikipedia search queries",
        task=f"Generate query for: {state['messages'][-1].content[:150]}",
        model_output=query_text,
        observations=results_summary,
        current_prompt=enhanced_prompt,
        task_id=f"wiki_search_{int(time.time()*1000)}"
    )
    
    formatted_search_docs = "\n\n---\n\n".join([
        f'<Document source="{doc.metadata["source"]}" page="{doc.metadata.get("page", "")}"/>\n{doc.page_content}\n</Document>'
        for doc in search_docs
    ])
    
    return {"context": [formatted_search_docs]}


def generate_answer(state: InterviewState):
    """Node to answer a question"""
    analyst = state["analyst"]
    messages = state["messages"]
    context = state["context"]

    system_message = answer_instructions.format(
        goals=analyst.persona,
        context=context
    )
    answer = llm.invoke([SystemMessage(content=system_message)] + messages)
    answer.name = "expert"

    return {"messages": [answer]}


def save_interview(state: InterviewState):
    """Save interviews"""
    messages = state["messages"]
    interview = get_buffer_string(messages)
    return {"interview": interview}


def route_messages(state: InterviewState, name: str = "expert"):
    """Route between question and answer"""
    messages = state["messages"]
    max_num_turns = state.get('max_num_turns', 2)

    num_responses = len([
        m for m in messages
        if isinstance(m, AIMessage) and m.name == name
    ])

    if num_responses >= max_num_turns:
        return 'save_interview'

    last_question = messages[-2]
    if "Thank you so much for your help" in last_question.content:
        return 'save_interview'

    return "ask_question"


def write_section(state: InterviewState):
    """Write a section based on interview"""
    interview = state["interview"]
    context = state["context"]
    analyst = state["analyst"]

    system_message = section_writer_instructions.format(
        focus=analyst.description)
    section = llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(
            content=f"Use this source to write your section: {context}")
    ])

    return {"sections": [section.content]}


def write_report(state: ResearchGraphState):
    """Write final report from sections"""
    sections = state["sections"]
    topic = state["topic"]

    formatted_str_sections = "\n\n".join(
        [f"{section}" for section in sections])
    system_message = report_writer_instructions.format(
        topic=topic,
        context=formatted_str_sections
    )

    report = llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content="Write a report based upon these memos.")
    ])

    return {"content": report.content}


def write_introduction(state: ResearchGraphState):
    """Write introduction for report"""
    sections = state["sections"]
    topic = state["topic"]

    formatted_str_sections = "\n\n".join(
        [f"{section}" for section in sections])
    instructions = intro_conclusion_instructions.format(
        topic=topic,
        formatted_str_sections=formatted_str_sections
    )

    intro = llm.invoke([
        instructions,
        HumanMessage(content="Write the report introduction")
    ])

    return {"introduction": intro.content}


def write_conclusion(state: ResearchGraphState):
    """Write conclusion for report"""
    sections = state["sections"]
    topic = state["topic"]

    formatted_str_sections = "\n\n".join(
        [f"{section}" for section in sections])
    instructions = intro_conclusion_instructions.format(
        topic=topic,
        formatted_str_sections=formatted_str_sections
    )

    conclusion = llm.invoke([
        instructions,
        HumanMessage(content="Write the report conclusion")
    ])

    return {"conclusion": conclusion.content}


def finalize_report(state: ResearchGraphState):
    """Finalize the report by combining all sections"""
    content = state["content"]

    if content.startswith("## Insights"):
        content = content.strip("## Insights")

    if "## Sources" in content:
        try:
            content, sources = content.split("\n## Sources\n")
        except:
            sources = None
    else:
        sources = None

    final_report = (
        state["introduction"] + "\n\n---\n\n" +
        content + "\n\n---\n\n" +
        state["conclusion"]
    )

    if sources is not None:
        final_report += "\n\n## Sources\n" + sources

    return {"final_report": final_report}
