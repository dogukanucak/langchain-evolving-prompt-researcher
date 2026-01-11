# Prompt Evolution Tutorials

Welcome to the SCOPE (Self-Correcting Optimal Prompt Evolution) tutorial notebooks!

## 📚 Notebooks

### 01_prompt_evolution_basics.ipynb
**Introduction to Prompt Evolution**

Learn how AI systems can automatically improve their own prompts through observation and learning.

**What you'll learn:**
- How SCOPE works
- Automatic prompt optimization
- Observing learning in real-time
- Measuring improvements
- LangChain integration

**Duration:** ~30-45 minutes  
**Prerequisites:** Basic Python, understanding of LLMs  
**Best for:** First-time users, understanding fundamentals

---

### 02_research_assistant_with_scope.ipynb
**Multi-Agent Research Assistant (Advanced - Hands-On!)**

Run a real production multi-agent research system and watch 5 agents learn simultaneously!

**What you'll DO:**
- ✅ Run the full research assistant
- ✅ Watch 5 agents learning in real-time
- ✅ Inspect learned rules after each run
- ✅ Compare reports before/after learning
- ✅ See source quality improvements
- ✅ Experiment with your own topics

**Duration:** ~40-60 minutes (fully executable)  
**Prerequisites:** Complete notebook 01 first, Tavily API key  
**Best for:** Seeing SCOPE in production, hands-on learning

**Note:** This is a PRACTICAL notebook - you'll execute real code and see actual results!

## 🚀 Getting Started (2 Simple Steps!)

### Step 1: Activate the Project Environment

```bash
cd /path/to/langchain-evolving-prompt-researcher
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

**Note:** The project uses `.venv` (with dot) which VS Code/Cursor auto-detects. No manual kernel setup needed!

### Step 2: Open and Run

**Option A - VS Code/Cursor:**
```bash
code notebooks/01_prompt_evolution_basics.ipynb
```
The IDE will auto-select the `.venv` kernel automatically!

**Option B - Jupyter:**
```bash
pip install jupyter  # If not already installed
cd notebooks
jupyter notebook
```
Then open `01_prompt_evolution_basics.ipynb`.

That's it! Just run the cells. 🚀

## ✅ Environment Verification

The notebooks include built-in environment checks. If you see a warning in Cell 3, just:
1. Make sure you activated `.venv` (see Step 1 above)
2. Restart the notebook kernel

## 📋 Requirements

- Python 3.8+
- OpenAI API key (for SCOPE and LLM calls)
- Tavily API key for notebook 02 (free at https://tavily.com)
- That's it!

## 💡 Learning Path

### Beginner Path (Understanding SCOPE):
1. Start with `01_prompt_evolution_basics.ipynb`
2. Run all cells sequentially
3. Experiment with the exercises
4. Try your own extraction tasks

### Advanced Path (Production Applications):
1. Complete notebook 01 first
2. Run through `02_research_assistant_with_scope.ipynb`
   - Execute all cells to see 5 agents learning
   - Watch real research reports being generated
   - Inspect learned rules and improvements
3. Run more iterations via CLI for deeper analysis:
   ```bash
   cd ..
   python main.py  # Single research run
   python compare_scope_impact.py --iterations 10  # Full learning evolution
   ```

## 🎯 What to Expect

Each notebook follows this structure:
1. **Concept Introduction** - What you'll learn
2. **Setup** - Installing packages and API keys
3. **Step-by-Step Code** - Building the solution
4. **Live Demonstration** - Watch SCOPE learn
5. **Analysis** - Understand the results
6. **Exercises** - Try it yourself

## 📊 Hands-On Approach

These are **interactive** notebooks:
- Run the code cells as you read
- See SCOPE learn in real-time
- Experiment with parameters
- Add your own tasks

## 🤔 Need Help?

- **Import errors?** Make sure you activated `.venv` (Step 1 above)
- **API errors?** Check you have OpenAI API key set
- **Questions?** See the main README.md
- **Want more?** Check out the full project documentation

## 🌟 Tips for Success

1. **Activate `.venv` first** - Everything else is automatic
2. **Run cells in order** - They build on each other
3. **Watch the output** - Learning happens live!
4. **Experiment** - Try different tasks and parameters
5. **Compare results** - See how prompts improve

## 📖 Additional Resources

- [SCOPE GitHub](https://github.com/neural-loop/scope-optimizer)
- [LangChain Documentation](https://python.langchain.com/)
- [Project README](../README.md)

Happy Learning! 🚀
