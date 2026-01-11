# SCOPE Integration in LangGraph Research Assistant

## Architecture Diagram

```
                                 ┌─────────┐
                                 │  START  │
                                 └────┬────┘
                                      │
                                      ▼
                            ┌──────────────────┐
                            │ create_analysts  │
                            └────────┬─────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │ human_feedback   │
                            └────────┬─────────┘
                                     │
                                     ▼
        ╔════════════════════════════════════════════════════════════╗
        ║         INTERVIEW SUBGRAPH (per analyst)                   ║
        ║         Runs in parallel using Send API                    ║
        ╠════════════════════════════════════════════════════════════╣
        ║                                                             ║
        ║                    ┌──────────────┐                        ║
        ║                    │ask_question  │                        ║
        ║                    └──────┬───────┘                        ║
        ║                           │                                 ║
        ║              ┌────────────┴────────────┐                   ║
        ║              │                         │                   ║
        ║              ▼                         ▼                   ║
        ║    ╔═════════════════╗       ╔═════════════════════╗      ║
        ║    ║  search_web     ║       ║ search_wikipedia    ║      ║
        ║    ║                 ║       ║                     ║      ║
        ║    ║  🔍 SCOPE:      ║       ║  🔍 SCOPE:          ║      ║
        ║    ║  • Enhance      ║       ║  • Enhance          ║      ║
        ║    ║  • Execute      ║       ║  • Execute          ║      ║
        ║    ║  • Observe      ║       ║  • Observe          ║      ║
        ║    ║  • Learn        ║       ║  • Learn            ║      ║
        ║    ╚═════════┬═══════╝       ╚═════════┬═══════════╝      ║
        ║              │                         │                   ║
        ║              └────────────┬────────────┘                   ║
        ║                           ▼                                ║
        ║                  ┌─────────────────┐                       ║
        ║                  │ answer_question │                       ║
        ║                  └────────┬────────┘                       ║
        ║                           │                                ║
        ║                    ┌──────┴──────┐                         ║
        ║                    │ More Qs?    │                         ║
        ║                    └──┬──────┬───┘                         ║
        ║                       │      │                             ║
        ║                   Yes │      │ No                          ║
        ║          ┌────────────┘      └────────┐                    ║
        ║          │                            │                    ║
        ║          ▼                            ▼                    ║
        ║   (Loop back)              ┌──────────────────┐            ║
        ║                            │ save_interview   │            ║
        ║                            └────────┬─────────┘            ║
        ║                                     │                      ║
        ║                                     ▼                      ║
        ║                            ┌──────────────────┐            ║
        ║                            │ write_section    │            ║
        ║                            └────────┬─────────┘            ║
        ║                                     │                      ║
        ╚═════════════════════════════════════╪══════════════════════╝
                                              │
                         ┌────────────────────┼────────────────────┐
                         │                    │                    │
                         ▼                    ▼                    ▼
                  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐
                  │write_report │    │write_intro   │    │write_conclusion│
                  └──────┬──────┘    └──────┬───────┘    └──────┬───────┘
                         │                  │                    │
                         └──────────────────┼────────────────────┘
                                            ▼
                                  ┌───────────────────┐
                                  │ finalize_report   │
                                  └─────────┬─────────┘
                                            │
                                            ▼
                                        ┌───────┐
                                        │  END  │
                                        └───────┘
```

## Where SCOPE is Integrated

**Location:** Inside `search_web` and `search_wikipedia` nodes (lines 129-228 in `nodes.py`)

**Integration Points:**
1. **Before search**: SCOPE enhances the prompt with learned strategic rules
2. **After search**: SCOPE observes results and learns improvements

## Why This Integration Point?

### Strategic Reason:
Search query quality directly impacts research quality. By optimizing how we generate search queries, we improve:
- Result relevance
- Information retrieval
- Report quality

### Technical Reason:
- **Observable Outcome**: Search results provide clear feedback on query quality
- **Frequent Execution**: Search nodes run multiple times per research task
- **Learning Opportunity**: Each search provides data for SCOPE to learn from
- **Direct Impact**: Better queries = better results immediately

### Implementation Reason:
- **Minimal Refactoring**: Works within existing node structure
- **Non-Invasive**: Doesn't change graph topology
- **Transparent**: Can be enabled/disabled without graph changes
- **Reusable Pattern**: Same approach works for both web and Wikipedia search

## SCOPE Learning Cycle

```
┌─────────────────────────────────────────────────────────────┐
│                    SCOPE Learning Cycle                     │
└─────────────────────────────────────────────────────────────┘

    1. Analyst asks question
           ↓
    2. SCOPE retrieves learned rules
           ↓
    3. Prompt enhanced with rules
           ↓
    4. LLM generates better query
           ↓
    5. Search executed
           ↓
    6. SCOPE observes results quality
           ↓
    7. SCOPE learns new strategic rules
           ↓
    8. Rules saved for next iteration
           ↓
    (Cycle repeats with improved prompts)
```

## Key Insight

> **SCOPE doesn't change the graph structure.**  
> **It makes the existing nodes smarter over time.**

The graph remains clean and simple, while the search nodes become increasingly effective through continuous learning.

---

**For Visual Diagrams:** Use the ASCII above as a template. Highlight the double-boxed search nodes to show SCOPE integration points.
