#!/usr/bin/env python3
"""
Simple SCOPE Demo - Information Extraction

A straightforward example showing SCOPE's learning capabilities with
a simple information extraction task. Perfect for:
- Understanding SCOPE fundamentals
- Quick demonstrations (~2 min/run)
- Teaching prompt evolution concepts

Compare to main.py:
- Simple: Single-agent, information extraction
- Fast: ~2 minutes per run
- Clear: Easy to understand learning patterns
"""
import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# Load environment variables
load_dotenv()

# Check for SCOPE
try:
    from scope import SCOPEOptimizer
    from scope.models import create_openai_model
    SCOPE_AVAILABLE = True
except ImportError:
    print("⚠️  SCOPE not installed. Install with: pip install scope-optimizer")
    SCOPE_AVAILABLE = False
    exit(1)

# Base extraction prompt
BASE_PROMPT = """You are an information extraction specialist.
Your task is to extract requested information from text accurately.

## Core Instructions:
- Extract only the requested information
- Be accurate and precise
- If information is missing, state "Not found"
- Provide clean, structured output
"""

# Sample extraction tasks
EXTRACTION_TASKS = [
    {
        "instruction": "Extract the email address",
        "text": "Contact John Doe at john.doe@example.com for support"
    },
    {
        "instruction": "Parse and extract: name, age, and city",
        "text": "Name: Jane Smith, Age: 28, City: Boston"
    },
    {
        "instruction": "Extract the phone number",
        "text": "You can email us at support@company.com"
    },
    {
        "instruction": "Extract name, age, city, and phone",
        "text": "name:John|age:35|city:NYC|phone:555-0123"
    },
    {
        "instruction": "Extract all email addresses",
        "text": "Team: alice@test.com, Bob <bob@example.org>, charlie@mail.net"
    },
]


async def extract_with_scope(llm, optimizer, instruction, text, task_id):
    """Extract information and let SCOPE observe."""
    
    # Get current prompt with learned rules
    strategic_rules = optimizer.get_strategic_rules_for_agent("info_extractor")
    current_prompt = BASE_PROMPT
    if strategic_rules:
        current_prompt += f"\n\n## Strategic Guidelines (Learned):\n{strategic_rules}"
    
    # Create messages
    messages = [
        SystemMessage(content=current_prompt),
        HumanMessage(content=f"{instruction}\n\nText: {text}")
    ]
    
    # Get response
    response = llm.invoke(messages)
    output = response.content
    
    # Let SCOPE observe
    result = await optimizer.on_step_complete(
        agent_name="info_extractor",
        agent_role="Information Extraction Specialist",
        task=f"{instruction} | Text: {text}",
        model_output=output,
        observations=f"Extracted from: '{text[:50]}...'",
        error=None,
        current_system_prompt=current_prompt,
        task_id=task_id
    )
    
    return output, result


async def main():
    """Run simple extraction demo with SCOPE."""
    
    print("\n" + "=" * 70)
    print("SIMPLE SCOPE DEMO - Information Extraction")
    print("=" * 70)
    print("\nThis demo shows SCOPE learning to extract information better.\n")
    
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    print("✅ LangChain ChatOpenAI initialized (gpt-4o)")
    
    # Initialize SCOPE
    scope_model = create_openai_model(
        model="gpt-4o",
        api_key=os.environ["OPENAI_API_KEY"]
    )
    
    optimizer = SCOPEOptimizer(
        synthesizer_model=scope_model,
        exp_path="./scope_data",
        enable_quality_analysis=True,
        quality_analysis_frequency=1,
        synthesis_mode="efficiency",
        store_history=True
    )
    
    print("✅ SCOPE Optimizer initialized\n")
    
    # Run extraction tasks
    print("🚀 Running extraction tasks...\n")
    print("=" * 70)
    
    learning_events = []
    
    for i, task in enumerate(EXTRACTION_TASKS, 1):
        print(f"\n📝 Task {i}/{len(EXTRACTION_TASKS)}")
        print(f"   Instruction: {task['instruction']}")
        print(f"   Text: {task['text']}")
        
        output, learning_result = await extract_with_scope(
            llm,
            optimizer,
            task['instruction'],
            task['text'],
            f"task_{i}"
        )
        
        print(f"\n   ✓ Output: {output}")
        
        if learning_result:
            guideline, guideline_type = learning_result
            learning_events.append({
                "task": i,
                "type": guideline_type,
                "rule": guideline
            })
            print(f"\n   📚 SCOPE LEARNED ({guideline_type.upper()}):")
            print(f"      {guideline[:100]}...")
        
        print("\n" + "-" * 70)
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"\n✅ Completed {len(EXTRACTION_TASKS)} tasks")
    print(f"📚 SCOPE learning events: {len(learning_events)}")
    
    if learning_events:
        print("\n📋 What SCOPE Learned:\n")
        for event in learning_events:
            print(f"   • Task {event['task']}: {event['rule'][:80]}...")
    
    # Show evolved prompt
    strategic_rules = optimizer.get_strategic_rules_for_agent("info_extractor")
    if strategic_rules:
        print("\n" + "=" * 70)
        print("EVOLVED PROMPT")
        print("=" * 70)
        print(f"\n{BASE_PROMPT}")
        print("\n## Strategic Guidelines (Learned):")
        print(strategic_rules)
    
    print("\n💡 Tip: Run again to see if SCOPE learns more or stabilizes!")
    print("💡 Use simple_compare.py to see learning over multiple iterations.\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n❌ Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
