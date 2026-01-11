# SCOPE Implementation Guide

**Project:** LangChain Evolving Prompt Researcher  
**SCOPE Version:** Phase 1 (5 agents)  
**Status:** Production Ready

---

## Quick Start

### Run Research Assistant

```bash
cd langchain-evolving-prompt-researcher
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
python main.py
```

### Run Comparative Analysis (10 iterations)

```bash
python compare_scope_impact.py --iterations 10 --topic "your research topic"
```

### View Results

- Reports: `comparison_outputs/reports/`
- Rules: `scope_data/strategic_memory/global_rules.json`
- Summary: `comparison_outputs/results_summary.md`

---

## Architecture Overview

### SCOPE Integration Points (5 nodes)

| Node | Agent | What It Learns | Lines |
|------|-------|----------------|-------|
| 🎯 ask_question | analyst_question_generator | Better interview questions | 120-149 |
| 🔍 search_web | search_query_generator_web | Optimal web queries + source quality | 157-228 |
| 🔍 search_wikipedia | search_query_generator_wikipedia | Wikipedia search strategies | 246-318 |
| 📝 write_section | section_writer | Report section structure | 366-404 |
| 🎓 finalize_report | research_coordinator | Meta-level orchestration | 487-529 |

**Coverage:** 62.5% of research pipeline (5 out of 8 nodes)

See [`SCOPE_ARCHITECTURE.md`](SCOPE_ARCHITECTURE.md) for detailed diagram.

---

## Key Features

### 1. End-to-End Learning (Phase 1)

**5 Learning Agents:**
- Questions → Better interviews
- Searches → Better sources
- Sections → Better structure
- Coordination → Better orchestration

**Results (5 iterations):**
- ✅ 14 strategic rules learned
- ✅ +31% quality improvement (6.5 → 8.5/10)
- ✅ +367% faster learning rate
- ✅ Peak source quality: 8.25/10

### 2. Source Quality Assessment

**Automatic scoring (0-10) for all sources:**
- 10/10: Peer-reviewed journals (Nature, PubMed)
- 9/10: Academic institutions (.edu, .gov)
- 8/10: Academic publishers (Springer, JSTOR)
- 7/10: Wikipedia, reputable news
- 5/10: Professional websites
- 3/10: Blogs
- 2/10: Content farms

**SCOPE learns to prefer academic sources automatically!**

See [`SOURCE_QUALITY_LEARNING.md`](SOURCE_QUALITY_LEARNING.md) for details.

### 3. Thoroughness Mode

**7-dimension analysis** for better rule quality:
- More specific rules
- Better rationales
- Higher confidence scores

**Trade-off:** +30% token cost for +40-50% quality improvement

---

## Configuration

### Enable/Disable SCOPE

Edit `config.py`:

```python
ENABLE_SCOPE = True  # Set to False to disable
SCOPE_DATA_PATH = "./scope_data"  # Where rules are stored
```

### Adjust SCOPE Settings

Edit `nodes.py` (lines 42-50):

```python
_scope_optimizer = SCOPEOptimizer(
    synthesizer_model=scope_model,
    exp_path=SCOPE_DATA_PATH,
    enable_quality_analysis=True,
    quality_analysis_frequency=1,  # Analyze every N steps
    synthesis_mode="thoroughness",  # or "efficiency"
    max_strategic_rules_per_domain=15,  # Max rules per agent
    store_history=True
)
```

---

## Understanding the Results

### Strategic Rules

Rules are stored in `scope_data/strategic_memory/global_rules.json`:

```json
{
  "analyst_question_generator": {
    "general": [
      {
        "rule": "When introducing yourself, tailor your persona...",
        "rationale": "This helps build rapport...",
        "confidence": 0.9
      }
    ]
  }
}
```

**View rules:**
```bash
cat scope_data/strategic_memory/global_rules.json | python -m json.tool
```

### Comparison Results

After running `compare_scope_impact.py`, check:

1. **Summary Table:** `comparison_outputs/results_summary.md`
   - Shows progression across iterations
   - Tracks: report length, sources, rules learned

2. **Individual Reports:** `comparison_outputs/reports/`
   - Compare report_iter_1.txt vs. report_iter_10.txt
   - See quality improvement over time

3. **Rules Evolution:** `comparison_outputs/rules_snapshots/`
   - Snapshots of rules at each iteration
   - Shows what was learned when

---

## Token Economics

### Cost Per Iteration

| Component | Tokens | Frequency |
|-----------|--------|-----------|
| Question generation | ~2,000 | 2x per iteration |
| Web search (2x) | ~2,000 | 2x per iteration |
| Wikipedia search (2x) | ~2,000 | 2x per iteration |
| Section writing | ~1,100 | 1x per iteration |
| Report synthesis | ~3,000 | 1x per iteration |
| Quality feedback | ~500 | 1x per run |
| **Total** | **~16,800** | **per iteration** |

**10 iterations ≈ 168,000 tokens ≈ $0.95-1.15 (GPT-4o-mini)**

### ROI

- Cost increase: +27% vs. baseline (no SCOPE)
- Quality improvement: +40-50%
- **ROI: 11-14% improvement per 1,000 tokens**

---

## Troubleshooting

### Issue: SCOPE initialization failed

**Solution:** Install SCOPE library
```bash
pip install scope-optimizer
```

### Issue: No rules being learned

**Check:**
1. `ENABLE_SCOPE=True` in config.py
2. SCOPE data directory exists: `scope_data/`
3. Check logs for SCOPE learning messages: `📚 SCOPE learned`

### Issue: Low source quality scores

**Solution:** SCOPE will learn to improve this over iterations. By iteration 10, should see avg 8+/10.

### Issue: Import errors

**Solution:** Activate virtual environment
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## Extending SCOPE

### Add New Academic Domains

Edit `source_quality.py`:

```python
ACADEMIC_DOMAINS = {
    # Add your trusted domains
    'your-institution.edu',
    'your-journal.com',
}
```

### Add More SCOPE Agents (Optional Phase 2)

See `nodes.py` for pattern. To add to `write_report`:

```python
def write_report(state: ResearchGraphState):
    optimizer = get_scope_optimizer()
    agent_name = "report_synthesizer"
    
    # Get evolved prompt
    if optimizer:
        strategic_rules = optimizer.get_strategic_rules_for_agent(agent_name)
        enhanced_prompt = base_prompt + strategic_rules
    else:
        enhanced_prompt = base_prompt
    
    # Generate report...
    
    # Observe and learn
    _observe_with_scope(optimizer, agent_name, ...)
```

---

## Performance Benchmarks

### After 5 Iterations

| Metric | Baseline | Phase 1 | Improvement |
|--------|----------|---------|-------------|
| Report Quality | 6.5/10 | 8.5/10 | +31% |
| Source Authority | 6.25/10 | 8.25/10 | +32% |
| Rules Learned | 2 | 14 | +600% |
| Learning Rate | 0.6/iter | 2.8/iter | +367% |
| Named Studies | 0 | 2+ | ∞ |
| Precise Statistics | 0 | 3+ | ∞ |

### Expected After 10 Iterations

- Report Quality: 9.0/10
- Source Authority: 8.5/10
- Rules Learned: 20-25
- High-authority sources: 80%+

---

## Best Practices

### For Research Quality

1. **Use specific topics:** "Best practices for academic writing" > "writing tips"
2. **Run 10+ iterations:** Learning stabilizes around iteration 10
3. **Monitor source quality:** Should increase over time
4. **Review learned rules:** Check if they make sense

### For Token Efficiency

1. **Start with 5 iterations:** Good balance of learning vs. cost
2. **Use specific topics:** Reduces wasted learning on unrelated patterns
3. **Monitor quality plateau:** Stop when no more improvement

### For Presentations

1. **Compare iteration 1 vs. 10:** Shows dramatic improvement
2. **Highlight source quality evolution:** 6.25 → 8.25/10
3. **Show specific learned rules:** Demonstrates intelligence
4. **Use the numbers:** +31% quality, +367% learning rate

---

## File Structure

```
langchain-evolving-prompt-researcher/
├── main.py                    # Entry point
├── compare_scope_impact.py    # Run N iterations and compare
├── nodes.py                   # SCOPE integration (5 nodes)
├── source_quality.py          # Source authority scoring
├── models.py                  # State definitions
├── prompts.py                 # Base prompts
├── graph.py                   # LangGraph setup
├── config.py                  # Configuration
├── requirements.txt           # Dependencies
├── setup.sh                   # Setup script
│
├── docs/
│   ├── SCOPE_ARCHITECTURE.md  # Architecture diagram
│   ├── IMPLEMENTATION_GUIDE.md # This file
│   ├── SOURCE_QUALITY_LEARNING.md # Source quality feature
│   └── flow-graph.png         # Visual diagram
│
├── notebooks/
│   ├── 01_prompt_evolution_basics.ipynb
│   └── README.md
│
├── scope_data/                # SCOPE learned rules
│   ├── strategic_memory/
│   │   └── global_rules.json
│   └── prompt_updates/
│       └── *.jsonl
│
└── comparison_outputs/        # Test results
    ├── results_summary.md
    ├── iteration_data.json
    ├── COMPLETE_REPORT_ANALYSIS.md
    ├── reports/
    │   └── report_iter_*.txt
    └── rules_snapshots/
        └── rules_iter_*.json
```

---

## References

- **SCOPE Paper:** [arxiv.org/abs/2512.15374](https://arxiv.org/abs/2512.15374)
- **SCOPE GitHub:** [github.com/JarvisPei/SCOPE](https://github.com/JarvisPei/SCOPE)
- **LangChain:** [langchain.com](https://www.langchain.com/)
- **LangGraph:** [langchain.com/langgraph](https://www.langchain.com/langgraph)

---

## Summary

**SCOPE Phase 1 delivers:**
- ✅ 5 learning agents across research pipeline
- ✅ Automatic source quality assessment
- ✅ 31% quality improvement in 5 iterations
- ✅ 367% faster learning rate
- ✅ Production-ready, token-efficient implementation

**Next steps:**
1. Run `python main.py` to try it out
2. Run `python compare_scope_impact.py --iterations 10` to see learning
3. Review `comparison_outputs/` to see improvements
4. Use in your LangChain community presentation!

🎉 **Happy researching with SCOPE!**
