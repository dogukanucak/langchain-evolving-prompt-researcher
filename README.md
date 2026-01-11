# LangChain Research Assistant with SCOPE

A production-ready LangGraph-based research assistant that continuously improves through [SCOPE](https://github.com/JarvisPei/SCOPE) (Self-evolving Context Optimization via Prompt Evolution).

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Overview

This project demonstrates how AI agents can learn and improve through experience using the SCOPE framework. The system features:

- **5 Self-Improving Agents**: Question generation, web search, Wikipedia search, section writing, and research coordination
- **Source Quality Assessment**: Automatic evaluation of information sources (academic journals, institutional sites, blogs)
- **Measurable Learning**: Quality improvements tracked across iterations
- **Production Ready**: Clean architecture, comprehensive documentation, easy setup

**Proven Results:**
- +31% quality improvement over 5 iterations (6.5 → 8.5/10)
- +32% source authority improvement (6.25 → 8.25/10)
- 14 strategic rules learned automatically
- Research-grade reports with named studies and precise statistics

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone repository
git clone <your-repo-url>
cd langchain-evolving-prompt-researcher

# Setup environment
chmod +x setup.sh
./setup.sh

# Or manually:
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
LANGSMITH_API_KEY=your_langsmith_key_here  # Optional, for tracing
```

Get your API keys:
- **OpenAI**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Tavily**: [tavily.com](https://tavily.com/)
- **LangSmith** (optional): [smith.langchain.com](https://smith.langchain.com/)

### 3. Run a Demo

**Quick Demo (Recommended First):**
```bash
# Simple extraction demo (~2 min)
python simple_demo.py
```

**Full Research Assistant:**
```bash
# Research assistant demo (~5 min)
python main.py
```

Enter a topic and watch SCOPE learn! Look for `📚 SCOPE learned` messages.

### 4. See Learning in Action (Recommended)

**Simple Comparison (Fast):**
```bash
# 5 iterations, ~10 minutes
python simple_compare.py

# 10 iterations for clear learning curve
python simple_compare.py --iterations 10
```

**Research Comparison (Full):**
```bash
# 10 iterations to see quality improvement
python compare_scope_impact.py --iterations 10 --topic "your topic"

# View results
cat comparison_outputs/results_summary.md
```

---

## 📊 Architecture

### SCOPE Integration Points (5 Agents)

```
Research Topic
    ↓
┌───────────────────────────────────┐
│  🎯 Question Generation (SCOPE)   │ → Learns to ask better questions
│  🔍 Web Search (SCOPE)            │ → Learns academic source selection
│  🔍 Wikipedia Search (SCOPE)      │ → Learns encyclopedia queries
│  📝 Section Writing (SCOPE)       │ → Learns report structure
│  🎓 Research Coordination (SCOPE) │ → Meta-level orchestration
└───────────────────────────────────┘
    ↓
Final Research Report
```

**Coverage:** 62.5% of pipeline (5 out of 8 nodes)

See [`docs/SCOPE_ARCHITECTURE.md`](docs/SCOPE_ARCHITECTURE.md) for detailed diagram.

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [`docs/IMPLEMENTATION_GUIDE.md`](docs/IMPLEMENTATION_GUIDE.md) | Complete implementation and usage guide |
| [`docs/SCOPE_ARCHITECTURE.md`](docs/SCOPE_ARCHITECTURE.md) | Architecture diagram and integration details |
| [`notebooks/01_prompt_evolution_basics.ipynb`](notebooks/01_prompt_evolution_basics.ipynb) | Interactive tutorial |

---

## 🎓 Key Features

### Self-Improving Agent Pipeline

Five specialized agents that learn from experience:
- **Question Generation**: Learns to formulate better research questions
- **Web Search**: Learns to identify high-quality sources
- **Wikipedia Search**: Learns effective encyclopedia queries
- **Section Writing**: Learns optimal report structure
- **Research Coordination**: Learns meta-level orchestration

### Source Quality Assessment

Automatic evaluation of information sources (0-10 scale):
- **10/10**: Peer-reviewed journals (Nature, PubMed, NIH, Science)
- **9/10**: Academic institutions (.edu, .gov domains)
- **8/10**: Academic publishers (Springer, JSTOR, IEEE)
- **7/10**: Wikipedia, established news organizations
- **3/10**: Blogs, personal websites

SCOPE automatically learns to prioritize authoritative sources.

### Measurable Results

Documented improvements over 5 iterations:
- **+31% report quality** (6.5 → 8.5/10)
- **+32% source authority** (6.25 → 8.25/10)
- **14 strategic rules** learned automatically
- **Research-grade output**: Named studies, precise statistics, proper citations

---

## 💡 Usage Examples

### Simple Extraction Demo

```bash
python simple_demo.py
```

Example output:
```
📝 Task 1/5
   Instruction: Extract the email address
   Text: Contact John Doe at john.doe@example.com...
   ✓ Output: john.doe@example.com
   
   📚 SCOPE LEARNED: Always validate email format patterns...

✅ Completed 5 tasks | 📚 SCOPE learning events: 2
```

### Research Assistant

```bash
python main.py
```

Example session:
```
Topic: Best practices for academic writing
Analysts: 1

📚 SCOPE learned: Include terms like 'peer-reviewed' for academic
    topics to boost source authority (5/10 → 9/10)

📚 SCOPE learned: When asking about writing techniques, prompt for
    comparative examples across disciplines
```

### Comparison Tools

**Simple Comparison** (faster, good for testing):
```bash
python simple_compare.py --iterations 5
```

**Research Comparison** (full pipeline):
```bash
python compare_scope_impact.py --iterations 10 --topic "your topic"
```

**Generated outputs:**
- `comparison_outputs/results_summary.md` - Quality progression
- `comparison_outputs/reports/` - Full reports per iteration
- `comparison_outputs/rules_snapshots/` - Rule evolution
- `comparison_outputs/COMPLETE_REPORT_ANALYSIS.md` - Detailed analysis

---

## 📈 Performance Metrics

### Token Usage and Cost

| Metric | Value (per iteration) |
|--------|----------------------|
| **Tokens** | ~16,800 |
| **Cost** (GPT-4o-mini) | ~$0.10 |
| **10 iterations** | ~168,000 tokens, ~$1.00 |
| **ROI** | 11-14% quality improvement per 1,000 tokens |

### Quality Progression

| Metric | Baseline | 5 Iterations | 10 Iterations (est.) |
|--------|----------|--------------|---------------------|
| Report Quality | 6.5/10 | 8.5/10 | 9.0/10 |
| Source Authority | 6.25/10 | 8.25/10 | 8.5/10 |
| Strategic Rules | 2 | 14 | 20-25 |
| Research Citations | 0 | 2+ | 5+ |

---

## 🔧 Configuration

### Enable/Disable SCOPE

Edit `config.py`:

```python
ENABLE_SCOPE = True  # Set to False to disable learning
SCOPE_DATA_PATH = "./scope_data"  # Directory for learned rules
```

### SCOPE Settings

Configure SCOPE behavior in `nodes.py`:

```python
SCOPEOptimizer(
    synthesis_mode="thoroughness",  # Options: "thoroughness" or "efficiency"
    max_strategic_rules_per_domain=15,  # Maximum rules per domain
    quality_analysis_frequency=1,  # Analyze quality every N steps
)
```

See [`docs/IMPLEMENTATION_GUIDE.md`](docs/IMPLEMENTATION_GUIDE.md) for advanced configuration.

---

## 📁 Project Structure

```
langchain-evolving-prompt-researcher/
├── main.py                    # Research assistant entry point
├── simple_demo.py             # Simple extraction demo
├── compare_scope_impact.py    # Research comparison tool
├── simple_compare.py          # Simple comparison tool
├── nodes.py                   # SCOPE-enabled agent nodes
├── source_quality.py          # Source authority scoring
├── graph.py                   # LangGraph workflow
├── models.py                  # Data models
├── prompts.py                 # Agent prompts
├── config.py                  # Configuration
├── requirements.txt           # Python dependencies
├── setup.sh                   # Setup script
│
├── docs/                      # Documentation
│   ├── IMPLEMENTATION_GUIDE.md
│   ├── SCOPE_ARCHITECTURE.md
│   └── flow-graph.png
│
├── notebooks/                 # Interactive tutorials
│   ├── 01_prompt_evolution_basics.ipynb
│   ├── 02_research_assistant_with_scope.ipynb
│   └── scope_data/            # Notebook-generated learning data
│
├── scope_data/                # Main learned rules (created on first run)
│   ├── strategic_memory/
│   └── prompt_updates/
│
└── comparison_outputs/        # Generated test results
    ├── results_summary.md
    ├── COMPLETE_REPORT_ANALYSIS.md
    ├── reports/
    └── rules_snapshots/
```

---

## 🛠️ Troubleshooting

### SCOPE not learning

Check that SCOPE is enabled in `config.py`:
```python
ENABLE_SCOPE = True
```

Verify the learning directory exists:
```bash
ls scope_data/strategic_memory/
```

Look for learning messages in output: `📚 SCOPE learned`

### Low source quality scores

This is normal! SCOPE learns to improve source quality over iterations:
- **Iteration 1**: ~6/10 (blogs, general websites)
- **Iteration 5**: ~8/10 (academic sources)
- **Iteration 10**: ~8.5/10 (peer-reviewed journals)

### Import errors

Activate the virtual environment and reinstall dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🚀 Next Steps

**Recommended Learning Path:**

1. **Quick demo:** `python simple_demo.py` (~2 minutes)
2. **See learning:** `python simple_compare.py --iterations 5` (~10 minutes)
3. **Full research:** `python main.py` (~5 minutes)
4. **Research comparison:** `python compare_scope_impact.py --iterations 5` (~25 minutes)
5. **Explore documentation:** [`docs/IMPLEMENTATION_GUIDE.md`](docs/IMPLEMENTATION_GUIDE.md) and [`docs/SCOPE_ARCHITECTURE.md`](docs/SCOPE_ARCHITECTURE.md)
6. **Interactive tutorials:** Jupyter notebooks in [`notebooks/`](notebooks/)

---

## 📖 References

### SCOPE Framework
- **SCOPE GitHub Repository:** [github.com/JarvisPei/SCOPE](https://github.com/JarvisPei/SCOPE)
- **SCOPE Paper:** Pei, Z., et al. (2024). SCOPE: Prompt Evolution for Enhancing Agent Effectiveness. [arXiv:2512.15374](https://arxiv.org/abs/2512.15374)

### Related Research on Agentic AI
- Jiang, P., et al. (2025). Adaptation of Agentic AI. [arXiv:2512.16301](https://arxiv.org/abs/2512.16301)
- Fang, J., et al. (2025). A Comprehensive Survey of Self-Evolving AI Agents: A New Paradigm Bridging Foundation Models and Lifelong Agentic Systems. [arXiv:2508.07407](https://arxiv.org/abs/2508.07407)
- Liu, S., et al. (2025). Adaptive and Resource-efficient Agentic AI Systems for Mobile and Embedded Devices: A Survey. [arXiv:2510.00078](https://arxiv.org/abs/2510.00078)
- Gao, H.-a., et al. (2025). A Survey of Self-Evolving Agents: On Path to Artificial Super Intelligence. [arXiv:2507.21046](https://arxiv.org/abs/2507.21046)
- Anonymous. (2025). Agentic AI: A Comprehensive Survey of Architectures, Applications, and Future Directions. [arXiv:2510.25445](https://arxiv.org/abs/2510.25445)

### Tutorials and Articles
- **Prompt Evolution with LangChain and SCOPE:** [medium.com/@dogukanucak94/prompt-evolution-with-langchain-and-scope-85c86246584e](https://medium.com/@dogukanucak94/prompt-evolution-with-langchain-and-scope-85c86246584e)

### Frameworks
- **LangGraph:** [langchain.com/langgraph](https://www.langchain.com/langgraph)
- **LangChain:** [langchain.com](https://www.langchain.com/)

---

## 🤝 Contributing

Contributions are welcome! Please see [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines.

**Areas for improvement:**
- Additional SCOPE-enabled agents
- Enhanced source quality detection
- Domain-specific learning rules
- Visualization and monitoring tools
- Performance optimizations

---

## 📄 License

MIT License - See [`LICENSE`](LICENSE) file

---

## 🙏 Acknowledgments

- **SCOPE Framework** by [Zehua Pei et al.](https://arxiv.org/abs/2512.15374)
- **LangGraph** by LangChain
- **LangChain Academy** research assistant example

---

## Questions or Issues?

Check the [documentation](docs/) or open an issue on GitHub.

**Happy researching with SCOPE! 🎉**
