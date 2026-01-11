# Research Assistant with SCOPE Integration

A LangGraph-based research assistant that automatically improves its search queries using [SCOPE](https://github.com/neural-loop/scope-optimizer) (Self-Correcting Optimal Prompt Evolution).

This project demonstrates how SCOPE can be integrated into a multi-agent system to continuously learn and optimize prompt quality, resulting in better search queries and more relevant research outputs.

## 🎯 What This Demonstrates

- **Automatic Prompt Optimization**: SCOPE observes search query generation and learns to improve prompts over time
- **Observable Learning**: See SCOPE learn in real-time as it analyzes query quality and generates improvement rules
- **Persistent Memory**: Strategic rules are saved and automatically applied to future runs
- **Measurable Impact**: Compare before/after results to see concrete improvements

## 🏗️ Architecture

```
Research Topic → Analyst Generation → Interviews → Report Writing
                                ↓
                        Search Queries (Web + Wikipedia)
                                ↓
                        SCOPE Observation & Learning
                                ↓
                        Strategic Rules Saved
                                ↓
                        Applied to Future Queries
```

**SCOPE Integration Points:**
- `search_web()` - Tavily web search query generation
- `search_wikipedia()` - Wikipedia search query generation

## 📦 Installation

### 1. Clone and Setup

```bash
git clone <repository-url>
cd evolving-prompt-researcher
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Or use the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```bash
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here  # Optional
ENABLE_SCOPE=true
SCOPE_DATA_PATH=./scope_data
```

**Get API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Tavily: https://tavily.com/ (for web search)
- LangSmith: https://smith.langchain.com/ (optional, for tracing)

## 🚀 Quick Start

### Two Demo Modes

This project includes **two complementary demos**:

#### 1. Simple Demo - Information Extraction (Recommended for learning)
```bash
python simple_demo.py
```

**Best for:**
- Understanding SCOPE fundamentals
- Seeing clear, predictable learning patterns
- Quick demonstrations (faster iterations)
- Teaching SCOPE concepts

#### 2. Research Assistant - Multi-Agent Research (Full complexity)
```bash
python main.py
```

**Best for:**
- Real-world application showcase
- Complex multi-agent scenarios
- Production-ready examples
- Comprehensive research tasks

Enter a research topic and watch the assistant:
1. Generate analyst perspectives
2. Conduct interviews with web/Wikipedia searches
3. Write a comprehensive report
4. **SCOPE learns from each search query!**

Look for `📚 SCOPE learned` messages during execution.

### Demo: See SCOPE's Impact Through Iterative Learning

**Two comparison modes available:**

#### Simple Demo Comparison (Recommended First)
```bash
# Quick test (5 iterations, ~10 minutes)
python simple_compare.py

# Medium demo (10 iterations, ~20 minutes)
python simple_compare.py --iterations 10

# Full presentation (15 iterations, ~30 minutes)
python simple_compare.py --iterations 15
```

**Why start here:**
- ✅ Faster iterations (~2 min each)
- ✅ Clearer learning patterns
- ✅ More predictable improvements
- ✅ Perfect for understanding SCOPE

**Generates:**
- `comparison_outputs/simple_results_summary.md` - Comparison table
- `comparison_outputs/simple_prompts/` - Evolved prompts per iteration
- `comparison_outputs/simple_rules_snapshots/` - Rules evolution

#### Research Demo Comparison (Full Complexity)
```bash
# Quick test (3 iterations, ~15 minutes)
python compare_scope_impact.py

# Medium demo (10 iterations, ~50 minutes)
python compare_scope_impact.py --iterations 10

# Full presentation (20 iterations, ~2 hours)
python compare_scope_impact.py --iterations 20
```

**Why use this:**
- 🎯 Real-world complexity
- 🎯 Production scenario
- 🎯 Impressive results
- 🎯 Shows SCOPE at scale

**Generates:**
- `comparison_outputs/results_summary.md` - Research comparison table
- `comparison_outputs/reports/` - Full research reports
- `comparison_outputs/rules_snapshots/` - SCOPE rules evolution

**Recommended workflow:**
1. Start with `simple_compare.py` to show SCOPE fundamentals
2. Then show `compare_scope_impact.py` for real-world application
3. Compare both results to highlight SCOPE's versatility

## 📊 How SCOPE Works

### 1. Observation Phase
```python
# After generating a search query
optimizer.on_step_complete(
    agent_name="search_query_generator_web",
    task="Generate search query for: AI trends",
    model_output="artificial intelligence 2024 trends",
    observations="Found 5 results, top result relevant...",
    current_system_prompt=search_instructions
)
```

### 2. Learning Phase
SCOPE analyzes:
- Query quality (verbose? missing keywords?)
- Result relevance
- Inefficiencies or patterns

Generates rules like:
- ✅ "Use concise and precise queries"
- ✅ "Include specific keywords to enhance search relevance"
- ✅ "Ensure query context aligns with task focus"

### 3. Application Phase
Strategic rules are:
- Saved to `scope_data/strategic_memory/global_rules.json`
- Automatically loaded on next run
- Applied to enhance prompts before query generation

## 📁 Project Structure

```
langchain-evolving-prompt-researcher/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── setup.sh                     # Quick setup script
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                      # MIT License
│
├── main.py                      # Research assistant entry point
├── simple_demo.py               # Simple extraction demo
├── graph.py                     # LangGraph workflow definition
├── nodes.py                     # Node functions (SCOPE integrated)
├── prompts.py                   # System prompts
├── models.py                    # Pydantic data models
├── config.py                    # Configuration loader
│
├── compare_scope_impact.py      # Research iterative comparison
├── simple_compare.py            # Simple demo iterative comparison
│
├── scope_data/                  # SCOPE learning storage
│   ├── strategic_memory/        # Persistent strategic rules
│   │   └── global_rules.json
│   └── prompt_updates/          # Learning history (JSONL)
│
└── comparison_outputs/          # Generated comparison results
    ├── results_summary.md       # Research demo results
    ├── simple_results_summary.md # Simple demo results
    ├── reports/                 # Research reports per iteration
    ├── simple_prompts/          # Evolved prompts per iteration
    └── *_rules_snapshots/       # Rules evolution tracking
```

## 🔍 Viewing SCOPE Results

### Check Strategic Rules

```bash
cat scope_data/strategic_memory/global_rules.json | python3 -m json.tool
```

### View Learning History

```bash
# Web search rules
cat scope_data/prompt_updates/search_query_generator_web.jsonl

# Wikipedia search rules
cat scope_data/prompt_updates/search_query_generator_wikipedia.jsonl
```

### Compare Reports

```bash
# After running compare_scope_impact.py
diff comparison_outputs/report_run1_baseline.txt comparison_outputs/report_run2_optimized.txt
```

## 💡 Example Topics to Try

Test with diverse topics to see different learning patterns:

- "artificial intelligence trends 2024"
- "climate change solutions"
- "quantum computing applications"
- "healthy Mediterranean diet"
- "sustainable energy technologies"

Each topic helps SCOPE learn different patterns and improve various aspects of query generation.

## 🛠️ Troubleshooting

### SCOPE folders are empty

**This is normal!** SCOPE learns from execution patterns:
- Good queries → No rules needed
- After 2-3 runs with diverse topics, rules should appear
- Strategic rules only saved when confidence is high

### No learning events showing

Check your `.env`:
```bash
ENABLE_SCOPE=true  # Make sure this is set
```

### API Errors

Verify your API keys:
```bash
# Test OpenAI
python -c "from openai import OpenAI; client = OpenAI(); print('✅ OpenAI connected')"

# Test Tavily
python -c "from tavily import TavilyClient; client = TavilyClient(); print('✅ Tavily connected')"
```

### Want to start fresh?

```bash
rm -rf scope_data
mkdir -p scope_data/prompt_updates scope_data/strategic_memory
```

## 🧪 Development

### Running Tests

```bash
# Test basic functionality
python main.py << EOF
Test topic
1

EOF

# Test SCOPE integration
python compare_scope_impact.py << EOF
Test topic
EOF
```

### Extending SCOPE Integration

SCOPE can be integrated into other nodes (answer generation, report writing, etc.). See `nodes.py` for the integration pattern:

```python
# 1. Get optimizer
optimizer = get_scope_optimizer()

# 2. Load strategic rules
if optimizer:
    strategic_rules = optimizer.get_strategic_rules_for_agent(agent_name)
    enhanced_prompt = base_prompt + strategic_rules

# 3. Execute task with enhanced prompt
result = llm.invoke([SystemMessage(content=enhanced_prompt)] + messages)

# 4. Let SCOPE observe and learn
_observe_with_scope(
    optimizer,
    agent_name=agent_name,
    agent_role="Role description",
    task="What the agent is doing",
    model_output=result,
    observations="Results of the action",
    current_prompt=enhanced_prompt,
    task_id=unique_task_id
)
```

## 📚 Resources

- **SCOPE Framework**: https://github.com/neural-loop/scope-optimizer
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **LangChain**: https://python.langchain.com/
- **Tavily Search**: https://tavily.com/

## 🤝 Contributing

This is an example project demonstrating SCOPE integration with LangGraph. Contributions are welcome:

- Improve search quality
- Add more SCOPE integration points
- Enhance reporting
- Add more agent types

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Built on [LangGraph](https://github.com/langchain-ai/langgraph) multi-agent framework
- Prompt optimization powered by [SCOPE](https://github.com/neural-loop/scope-optimizer)
- Based on LangChain Academy's [Research Assistant](https://github.com/langchain-ai/langchain-academy) example

---

**Questions?** Open an issue or check the [SCOPE documentation](https://github.com/neural-loop/scope-optimizer)
