#!/usr/bin/env python3
"""
Simple Demo Comparison Script - Iterative Learning Demonstration

Runs the simple information extraction demo N times to show SCOPE learning.
Generates markdown tables for presentation.
"""
import subprocess
import json
import argparse
from pathlib import Path
from datetime import datetime


def clear_scope_data():
    """Clear SCOPE data to start fresh."""
    scope_path = Path("scope_data")
    if scope_path.exists():
        import shutil
        shutil.rmtree(scope_path)
    scope_path.mkdir(exist_ok=True)
    (scope_path / "prompt_updates").mkdir(exist_ok=True)
    (scope_path / "strategic_memory").mkdir(exist_ok=True)
    print("✅ Cleared SCOPE data\n")


def run_simple_demo():
    """Run the simple demo and capture output."""
    result = subprocess.run(
        ["python", "simple_demo.py"],
        capture_output=True,
        text=True,
        cwd="."
    )
    return result.stdout, result.stderr


def extract_learning_events(output: str):
    """Extract SCOPE learning messages from output."""
    lines = output.split('\n')
    scope_messages = [line for line in lines if '📚 SCOPE learned' in line]
    return scope_messages


def extract_statistics(output: str):
    """Extract statistics from output."""
    lines = output.split('\n')
    
    stats = {
        'tasks_completed': 0,
        'learning_events': 0
    }
    
    for line in lines:
        if 'Tasks completed:' in line:
            try:
                stats['tasks_completed'] = int(line.split(':')[1].strip())
            except:
                pass
        elif 'Learning events:' in line:
            try:
                stats['learning_events'] = int(line.split(':')[1].strip())
            except:
                pass
    
    return stats


def get_strategic_rules():
    """Get current strategic rules."""
    rules_file = Path("scope_data/strategic_memory/global_rules.json")
    if not rules_file.exists():
        return {}
    
    with open(rules_file) as f:
        return json.load(f)


def count_total_rules(rules: dict):
    """Count total number of strategic rules."""
    if not rules:
        return 0
    total = 0
    for agent_name, domains in rules.items():
        for domain, rule_list in domains.items():
            total += len(rule_list)
    return total


def extract_evolved_prompt(output: str):
    """Extract the evolved prompt from output."""
    lines = output.split('\n')
    
    # Find EVOLVED PROMPT section
    start_idx = None
    end_idx = None
    
    for i, line in enumerate(lines):
        if 'EVOLVED PROMPT' in line and '=' in line:
            start_idx = i + 2  # Skip the header and separator
        elif start_idx is not None and '=' * 20 in line:
            end_idx = i
            break
    
    if start_idx and end_idx:
        prompt_lines = lines[start_idx:end_idx]
        return '\n'.join(prompt_lines).strip()
    
    return None


def save_prompt(prompt: str, filename: str, output_dir: Path):
    """Save evolved prompt to file."""
    prompt_file = output_dir / filename
    with open(prompt_file, 'w') as f:
        f.write(prompt)
    return prompt_file


def generate_markdown_table(iterations_data: list):
    """Generate markdown table from iterations data."""
    table = "## SCOPE Learning Progress - Simple Demo\n\n"
    table += "| Iteration | Tasks Completed | Learning Events | New Rules | Total Rules | Success Rate | Gemini Score | Grok Score |\n"
    table += "|-----------|----------------|-----------------|-----------|-------------|--------------|--------------|------------|\n"
    
    for data in iterations_data:
        success_rate = f"{(data['tasks_completed'] / 8 * 100):.0f}%" if data['tasks_completed'] > 0 else "0%"
        table += f"| {data['iteration']} | {data['tasks_completed']} | {data['learning_events']} | {data['new_rules']} | {data['total_rules']} | {success_rate} | TBD | TBD |\n"
    
    table += "\n### Notes\n"
    table += "- **Tasks Completed**: Number of extraction tasks completed (max: 8)\n"
    table += "- **Learning Events**: Number of SCOPE learning events (fewer = better)\n"
    table += "- **New Rules**: Strategic rules learned in this iteration\n"
    table += "- **Total Rules**: Cumulative strategic rules\n"
    table += "- **Success Rate**: Task completion rate\n"
    table += "- **Gemini/Grok Scores**: To be filled after manual evaluation\n"
    
    return table


def save_iteration_data(iterations_data: list, output_dir: Path, topic: str):
    """Save iteration data to JSON file."""
    json_file = output_dir / "simple_iteration_data.json"
    with open(json_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'demo_type': 'simple_extraction',
            'iterations': iterations_data
        }, f, indent=2)
    return json_file


def main():
    parser = argparse.ArgumentParser(
        description='Simple Demo - Iterative SCOPE Learning'
    )
    parser.add_argument(
        '--iterations', '-n',
        type=int,
        default=5,
        help='Number of iterations to run (default: 5, recommended: 10-15)'
    )
    
    args = parser.parse_args()
    num_iterations = args.iterations
    
    if num_iterations < 2:
        print("❌ Error: Number of iterations must be at least 2")
        return
    
    print("\n" + "="*70)
    print("SIMPLE DEMO: ITERATIVE SCOPE LEARNING")
    print("="*70)
    print(f"\nRunning information extraction demo {num_iterations} times")
    print("This simpler task shows clearer learning patterns than research.\n")
    
    # Prepare output directory
    output_dir = Path("comparison_outputs")
    output_dir.mkdir(exist_ok=True)
    prompts_dir = output_dir / "simple_prompts"
    prompts_dir.mkdir(exist_ok=True)
    rules_dir = output_dir / "simple_rules_snapshots"
    rules_dir.mkdir(exist_ok=True)
    
    # Clear SCOPE data for clean start
    print("="*70)
    print("PREPARING: Clearing SCOPE data")
    print("="*70 + "\n")
    clear_scope_data()
    
    iterations_data = []
    previous_rules_count = 0
    
    # Run iterations
    for i in range(1, num_iterations + 1):
        print("\n" + "="*70)
        print(f"ITERATION {i}/{num_iterations}")
        if i == 1:
            print("(Baseline - No SCOPE Rules)")
        else:
            print(f"(With {previous_rules_count} accumulated rules)")
        print("="*70 + "\n")
        
        # Run simple demo
        stdout, stderr = run_simple_demo()
        
        # Extract metrics
        learning_events = extract_learning_events(stdout)
        stats = extract_statistics(stdout)
        rules = get_strategic_rules()
        evolved_prompt = extract_evolved_prompt(stdout)
        
        # Calculate metrics
        total_rules = count_total_rules(rules)
        new_rules = total_rules - previous_rules_count
        
        # Store iteration data
        iteration_data = {
            'iteration': i,
            'tasks_completed': stats['tasks_completed'],
            'learning_events': len(learning_events),
            'new_rules': new_rules,
            'total_rules': total_rules
        }
        iterations_data.append(iteration_data)
        
        # Save evolved prompt
        if evolved_prompt:
            prompt_file = prompts_dir / f"prompt_iter_{i}.txt"
            save_prompt(evolved_prompt, f"prompt_iter_{i}.txt", prompts_dir)
        
        # Save rules snapshot
        if rules:
            rules_file = rules_dir / f"rules_iter_{i}.json"
            with open(rules_file, 'w') as f:
                json.dump(rules, f, indent=2)
        
        # Print iteration summary
        print("\n" + "-"*70)
        print(f"ITERATION {i} SUMMARY:")
        print("-"*70)
        print(f"  ✅ Tasks completed: {stats['tasks_completed']}/8")
        print(f"  📚 Learning events: {len(learning_events)}")
        print(f"  ➕ New rules learned: {new_rules}")
        print(f"  📊 Total accumulated rules: {total_rules}")
        
        if i < num_iterations:
            print(f"\n⏭️  Proceeding to iteration {i+1}...")
        
        previous_rules_count = total_rules
    
    # Generate summary
    print("\n" + "="*70)
    print("GENERATING RESULTS SUMMARY")
    print("="*70 + "\n")
    
    # Create markdown table
    markdown_table = generate_markdown_table(iterations_data)
    summary_file = output_dir / "simple_results_summary.md"
    
    with open(summary_file, 'w') as f:
        f.write(f"# SCOPE Learning Progress - Simple Demo\n\n")
        f.write(f"**Demo Type:** Information Extraction\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total Iterations:** {num_iterations}\n\n")
        f.write("---\n\n")
        f.write(markdown_table)
        f.write("\n---\n\n")
        f.write("## Comparison with Research Demo\n\n")
        f.write("**Simple Demo (Information Extraction):**\n")
        f.write("- ✅ Clearer learning patterns\n")
        f.write("- ✅ More predictable improvements\n")
        f.write("- ✅ Faster convergence\n")
        f.write("- ✅ Better for demonstrating SCOPE fundamentals\n\n")
        f.write("**Research Demo (Multi-Agent Research):**\n")
        f.write("- 🎯 More complex and realistic\n")
        f.write("- 🎯 Shows SCOPE in production scenario\n")
        f.write("- 🎯 Variable but impressive results\n")
        f.write("- 🎯 Better for showing real-world applications\n\n")
        f.write("## Files Generated\n\n")
        f.write(f"- Prompts: `comparison_outputs/simple_prompts/prompt_iter_[1-{num_iterations}].txt`\n")
        f.write(f"- Rules: `comparison_outputs/simple_rules_snapshots/rules_iter_[1-{num_iterations}].json`\n")
        f.write(f"- Data: `comparison_outputs/simple_iteration_data.json`\n\n")
        f.write("## Scoring Instructions\n\n")
        f.write("For each iteration, review the evolved prompt and score with Gemini/Grok:\n\n")
        f.write("**Prompt:** Rate this extraction prompt 1-10 on clarity, completeness, and effectiveness.\n\n")
        f.write("Then update the table above with the scores.\n")
    
    # Save JSON data
    json_file = save_iteration_data(iterations_data, output_dir, "information_extraction")
    
    # Display results
    print(markdown_table)
    
    print("\n" + "="*70)
    print("DEMO COMPLETE!")
    print("="*70)
    print(f"\n✅ Successfully completed {num_iterations} iterations")
    print(f"\n📊 Results saved to:")
    print(f"   • Summary table: {summary_file}")
    print(f"   • Raw data: {json_file}")
    print(f"   • Evolved prompts: {prompts_dir}/")
    print(f"   • Rules snapshots: {rules_dir}/")
    
    print("\n📋 Key Observations:")
    first_learning = iterations_data[0]['learning_events']
    last_learning = iterations_data[-1]['learning_events']
    if last_learning < first_learning:
        improvement = ((first_learning - last_learning) / first_learning * 100)
        print(f"   ✅ Learning events reduced by {improvement:.0f}% ({first_learning} → {last_learning})")
    
    first_rules = iterations_data[0]['total_rules']
    last_rules = iterations_data[-1]['total_rules']
    if last_rules > first_rules:
        print(f"   ✅ Strategic rules accumulated: {first_rules} → {last_rules}")
    
    print("\n💡 Next steps:")
    print("   1. Review evolved prompts in comparison_outputs/simple_prompts/")
    print("   2. Score prompts with Gemini and Grok")
    print("   3. Update simple_results_summary.md with scores")
    print("   4. Compare with research demo results")
    print("   5. Use both demos in your LangChain presentation!")
    
    print(f"\n🔄 To run more iterations:")
    print(f"   python simple_compare.py --iterations 15")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
