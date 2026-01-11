#!/usr/bin/env python3
"""
Simple SCOPE Comparison Tool

Runs information extraction demo multiple times to demonstrate SCOPE's
learning curve. Generates comparison reports showing improvement.

Perfect for:
- Quick demonstrations (~2 min/iteration vs ~5 min for research)
- Teaching SCOPE fundamentals with clear patterns
- Presentations requiring fast, measurable results

Usage:
    python simple_compare.py                    # 5 iterations (default)
    python simple_compare.py --iterations 10    # 10 iterations
    python simple_compare.py --iterations 15    # Full demo
"""
import asyncio
import argparse
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# Load environment
load_dotenv()

# Check for SCOPE
try:
    from scope import SCOPEOptimizer
    from scope.models import create_openai_model
    SCOPE_AVAILABLE = True
except ImportError:
    print("⚠️  SCOPE not installed. Install with: pip install scope-optimizer")
    exit(1)

# Base prompt
BASE_PROMPT = """You are an information extraction specialist.
Your task is to extract requested information from text accurately.

## Core Instructions:
- Extract only the requested information
- Be accurate and precise
- If information is missing, state "Not found"
- Provide clean, structured output
"""

# Extraction tasks
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
    
    strategic_rules = optimizer.get_strategic_rules_for_agent("info_extractor")
    current_prompt = BASE_PROMPT
    if strategic_rules:
        current_prompt += f"\n\n## Strategic Guidelines (Learned):\n{strategic_rules}"
    
    messages = [
        SystemMessage(content=current_prompt),
        HumanMessage(content=f"{instruction}\n\nText: {text}")
    ]
    
    response = llm.invoke(messages)
    output = response.content
    
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


async def run_iteration(iteration_num: int):
    """Run one complete iteration."""
    
    print(f"\n{'='*70}")
    print(f"ITERATION {iteration_num}")
    print(f"{'='*70}\n")
    
    # Initialize
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
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
    
    # Get current rules count
    strategic_rules = optimizer.get_strategic_rules_for_agent("info_extractor")
    initial_rules = len(strategic_rules.split('\n')) if strategic_rules else 0
    
    # Run tasks
    learning_events = []
    outputs = []
    
    for i, task in enumerate(EXTRACTION_TASKS, 1):
        print(f"Task {i}/{len(EXTRACTION_TASKS)}: {task['instruction'][:50]}...", end=" ")
        
        output, learning_result = await extract_with_scope(
            llm,
            optimizer,
            task['instruction'],
            task['text'],
            f"iter{iteration_num}_task{i}"
        )
        
        outputs.append(output)
        
        if learning_result:
            guideline, guideline_type = learning_result
            learning_events.append({
                "type": guideline_type,
                "rule": guideline
            })
            print(f"✓ [LEARNED {guideline_type}]")
        else:
            print("✓")
    
    # Get final rules count
    final_rules_text = optimizer.get_strategic_rules_for_agent("info_extractor")
    final_rules = len(final_rules_text.split('\n')) if final_rules_text else 0
    
    # Calculate metrics
    avg_output_length = sum(len(o) for o in outputs) / len(outputs)
    
    results = {
        "iteration": iteration_num,
        "tasks_completed": len(EXTRACTION_TASKS),
        "learning_events": len(learning_events),
        "strategic_rules": final_rules - initial_rules,
        "total_rules": final_rules,
        "avg_output_length": int(avg_output_length),
        "learned_this_iter": [e["rule"][:100] for e in learning_events]
    }
    
    print(f"\n✅ Iteration {iteration_num} complete:")
    print(f"   • Learning events: {len(learning_events)}")
    print(f"   • New rules: {results['strategic_rules']}")
    print(f"   • Total rules: {results['total_rules']}")
    
    return results, final_rules_text


def save_results(all_results, output_dir):
    """Save comparison results."""
    
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Save iteration data
    iteration_file = output_dir / "simple_iteration_data.json"
    with open(iteration_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Generate summary markdown
    summary_file = output_dir / "simple_results_summary.md"
    
    with open(summary_file, 'w') as f:
        f.write("# Simple Demo - SCOPE Learning Progression\n\n")
        f.write(f"**Task:** Information Extraction\n")
        f.write(f"**Total Iterations:** {len(all_results)}\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Iteration Summary\n\n")
        f.write("| Iter | Tasks | Learning Events | New Rules | Total Rules | Avg Output Length |\n")
        f.write("|------|-------|----------------|-----------|-------------|-------------------|\n")
        
        for r in all_results:
            f.write(f"| {r['iteration']} | {r['tasks_completed']} | "
                   f"{r['learning_events']} | {r['strategic_rules']} | "
                   f"{r['total_rules']} | {r['avg_output_length']} |\n")
        
        f.write("\n## Key Metrics\n\n")
        
        if len(all_results) > 1:
            first = all_results[0]
            last = all_results[-1]
            
            learning_change = ((last['learning_events'] - first['learning_events']) / 
                             max(first['learning_events'], 1) * 100)
            
            f.write(f"- **Initial Learning Events:** {first['learning_events']}\n")
            f.write(f"- **Final Learning Events:** {last['learning_events']}\n")
            f.write(f"- **Learning Event Change:** {learning_change:+.0f}%\n")
            f.write(f"- **Total Rules Accumulated:** {last['total_rules']}\n\n")
        
        f.write("## What This Shows\n\n")
        f.write("**Decreasing learning events = Better prompts!**\n\n")
        f.write("As SCOPE learns, it finds fewer issues with outputs, meaning the ")
        f.write("prompt is becoming more optimized.\n\n")
        
        f.write("## Learning Examples\n\n")
        for r in all_results[:5]:  # First 5 iterations
            if r['learned_this_iter']:
                f.write(f"### Iteration {r['iteration']}\n\n")
                for rule in r['learned_this_iter'][:3]:  # Top 3 rules
                    f.write(f"- {rule}...\n")
                f.write("\n")
    
    print(f"\n📊 Results saved:")
    print(f"   • Summary: {summary_file}")
    print(f"   • Data: {iteration_file}")


async def main():
    """Run multiple iterations and compare."""
    
    parser = argparse.ArgumentParser(description="Simple SCOPE comparison tool")
    parser.add_argument('--iterations', type=int, default=5,
                       help='Number of iterations to run (default: 5)')
    parser.add_argument('--output-dir', default='./comparison_outputs',
                       help='Output directory (default: ./comparison_outputs)')
    
    args = parser.parse_args()
    
    print("\n" + "=" * 70)
    print("SIMPLE SCOPE COMPARISON")
    print("=" * 70)
    print(f"\nTask: Information Extraction")
    print(f"Iterations: {args.iterations}")
    print(f"Tasks per iteration: {len(EXTRACTION_TASKS)}")
    print(f"Estimated time: ~{args.iterations * 2} minutes")
    print("\nThis will clear existing SCOPE data to show learning from scratch.\n")
    
    # Clear SCOPE data
    if Path("./scope_data").exists():
        response = input("Clear existing SCOPE data? [Y/n]: ").strip().lower()
        if response != 'n':
            shutil.rmtree("./scope_data")
            print("✅ SCOPE data cleared")
    
    # Run iterations
    all_results = []
    
    for i in range(1, args.iterations + 1):
        try:
            results, final_prompt = await run_iteration(i)
            all_results.append(results)
            
            # Save prompt snapshot
            output_dir = Path(args.output_dir) / "simple_prompts"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            prompt_file = output_dir / f"prompt_iter_{i}.txt"
            with open(prompt_file, 'w') as f:
                f.write(BASE_PROMPT)
                if final_prompt:
                    f.write("\n\n## Strategic Guidelines (Learned):\n")
                    f.write(final_prompt)
            
        except Exception as e:
            print(f"\n❌ Error in iteration {i}: {e}")
            import traceback
            traceback.print_exc()
            break
    
    # Save results
    if all_results:
        save_results(all_results, args.output_dir)
        
        print("\n" + "=" * 70)
        print("COMPARISON COMPLETE")
        print("=" * 70)
        print(f"\n✅ Completed {len(all_results)} iterations")
        print(f"\n📊 View results:")
        print(f"   cat {args.output_dir}/simple_results_summary.md")
        print("\n💡 Compare with research demo:")
        print("   python compare_scope_impact.py --iterations 5")
        print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n❌ Comparison interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
