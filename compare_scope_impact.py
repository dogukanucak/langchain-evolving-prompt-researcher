#!/usr/bin/env python3
"""
Script to demonstrate SCOPE's impact through iterative learning.

This script runs the research assistant N times with the same topic:
- Iteration 1: Clean slate (no SCOPE rules)
- Iterations 2-N: With accumulated learned rules from previous iterations

It captures metrics and generates a markdown table for presentation.
"""
import subprocess
import json
import os
import argparse
import re
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


def run_research(topic: str, num_analysts: int = 1, run_label: str = "Run"):
    """Run the research assistant and capture output."""
    print(f"{'='*70}")
    print(f"{run_label}: Researching '{topic}'")
    print(f"{'='*70}\n")

    input_data = f"{topic}\n{num_analysts}\n\n"

    result = subprocess.run(
        ["python", "main.py"],
        input=input_data,
        capture_output=True,
        text=True,
        cwd="."
    )

    return result.stdout, result.stderr


def extract_scope_messages(output: str):
    """Extract SCOPE learning messages from output."""
    lines = output.split('\n')
    scope_messages = [line for line in lines if '📚 SCOPE learned' in line]
    return scope_messages


def extract_final_report(output: str):
    """Extract the final report from output."""
    lines = output.split('\n')

    # Find the FINAL REPORT section
    start_idx = None
    for i, line in enumerate(lines):
        if 'FINAL REPORT' in line or 'Final Report' in line:
            start_idx = i
            break

    if start_idx is None:
        return None

    # Extract everything after FINAL REPORT header
    report_lines = []
    in_report = False
    for line in lines[start_idx:]:
        if '=' * 20 in line and not in_report:
            in_report = True
            continue
        if in_report:
            report_lines.append(line)

    return '\n'.join(report_lines).strip()


def count_sources_in_report(report: str):
    """Count number of sources cited in the report."""
    if not report:
        return 0

    # Look for common source patterns like [1], [2], etc. or URLs
    citation_patterns = [
        r'\[\d+\]',  # [1], [2], etc.
        r'https?://[^\s\)]+',  # URLs
    ]

    sources = set()
    for pattern in citation_patterns:
        matches = re.findall(pattern, report)
        sources.update(matches)

    return len(sources)


def save_report(report: str, filename: str):
    """Save report to file."""
    output_dir = Path("comparison_outputs")
    output_dir.mkdir(exist_ok=True)

    filepath = output_dir / filename
    with open(filepath, 'w') as f:
        f.write(report)

    return filepath


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


def print_rules_summary(rules: dict):
    """Print a summary of strategic rules."""
    if not rules:
        print("   No strategic rules yet")
        return

    total_rules = sum(len(agent_rules) for agent in rules.values()
                      for agent_rules in agent.values())
    print(f"   Total strategic rules: {total_rules}")

    for agent_name, domains in rules.items():
        print(f"\n   📌 {agent_name}:")
        for domain, rule_list in domains.items():
            for rule in rule_list:
                print(f"      • {rule['rule'][:80]}...")


def generate_markdown_table(iterations_data: list):
    """Generate markdown table from iterations data."""
    table = "## SCOPE Learning Progress\n\n"
    table += "| Iteration | Report Length (chars) | Sources Cited | Query Improvements | New Rules Learned | Total Rules | Gemini Score | Grok Score |\n"
    table += "|-----------|----------------------|---------------|-------------------|-------------------|-------------|--------------|------------|\n"

    for data in iterations_data:
        table += f"| {data['iteration']} | {data['report_length']:,} | {data['sources_cited']} | {data['query_improvements']} | {data['new_rules']} | {data['total_rules']} | TBD | TBD |\n"

    table += "\n### Notes\n"
    table += "- **Report Length**: Character count of the final research report\n"
    table += "- **Sources Cited**: Number of unique sources referenced in the report\n"
    table += "- **Query Improvements**: Number of SCOPE learning events (fewer = better queries)\n"
    table += "- **New Rules Learned**: Strategic rules learned in this iteration\n"
    table += "- **Total Rules**: Cumulative strategic rules across all iterations\n"
    table += "- **Gemini/Grok Scores**: To be filled after manual evaluation\n"

    return table


def save_iteration_data(iterations_data: list, output_dir: Path):
    """Save iteration data to JSON file."""
    json_file = output_dir / "iteration_data.json"
    with open(json_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'iterations': iterations_data
        }, f, indent=2)
    return json_file


def main():
    parser = argparse.ArgumentParser(
        description='Demonstrate SCOPE impact through iterative learning'
    )
    parser.add_argument(
        '--iterations', '-n',
        type=int,
        default=3,
        help='Number of iterations to run (default: 3, recommended: 5-20 for presentation)'
    )
    parser.add_argument(
        '--topic', '-t',
        type=str,
        default=None,
        help='Research topic (will prompt if not provided)'
    )

    args = parser.parse_args()

    num_iterations = args.iterations
    if num_iterations < 2:
        print("❌ Error: Number of iterations must be at least 2")
        return
    if num_iterations > 25:
        print("⚠️  Warning: Running more than 25 iterations may take a very long time")
        response = input("Continue anyway? (yes/no): ").strip().lower()
        if response != 'yes':
            return

    print("\n" + "="*70)
    print("SCOPE ITERATIVE LEARNING DEMONSTRATION")
    print("="*70)
    print(
        f"\nThis demo runs the research assistant {num_iterations} times with the same topic:")
    print("  • Iteration 1: Clean slate (no SCOPE rules)")
    print(f"  • Iterations 2-{num_iterations}: With accumulated learned rules")
    print("\nWe'll track improvements across iterations!\n")

    # Get topic from user
    topic = args.topic
    if not topic:
        topic = input(
            "Enter research topic (or press Enter for 'the healthiest foods to eat'): ").strip()
        if not topic:
            topic = "the healthiest foods to eat"

    print(f"\n📋 Research Topic: '{topic}'")
    print(f"🔄 Iterations: {num_iterations}")

    # Prepare output directory
    output_dir = Path("comparison_outputs")
    output_dir.mkdir(exist_ok=True)
    reports_dir = output_dir / "reports"
    reports_dir.mkdir(exist_ok=True)
    rules_dir = output_dir / "rules_snapshots"
    rules_dir.mkdir(exist_ok=True)

    # Clear SCOPE data for clean start
    print("\n" + "="*70)
    print("PREPARING: Clearing SCOPE data for clean baseline")
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

        # Run research
        stdout, stderr = run_research(
            topic,
            num_analysts=1,
            run_label=f"ITERATION {i}"
        )

        # Extract metrics
        scope_messages = extract_scope_messages(stdout)
        report = extract_final_report(stdout)
        rules = get_strategic_rules()

        # Calculate metrics
        total_rules = count_total_rules(rules)
        new_rules = total_rules - previous_rules_count
        report_length = len(report) if report else 0
        sources_cited = count_sources_in_report(report) if report else 0
        query_improvements = len(scope_messages)

        # Store iteration data
        iteration_data = {
            'iteration': i,
            'report_length': report_length,
            'sources_cited': sources_cited,
            'query_improvements': query_improvements,
            'new_rules': new_rules,
            'total_rules': total_rules
        }
        iterations_data.append(iteration_data)

        # Save report
        if report:
            report_file = reports_dir / f"report_iter_{i}.txt"
            with open(report_file, 'w') as f:
                f.write(report)

        # Save rules snapshot
        if rules:
            rules_file = rules_dir / f"rules_iter_{i}.json"
            with open(rules_file, 'w') as f:
                json.dump(rules, f, indent=2)

        # Print iteration summary
        print("\n" + "-"*70)
        print(f"ITERATION {i} SUMMARY:")
        print("-"*70)
        print(f"  📝 Report length: {report_length:,} characters")
        print(f"  📚 Sources cited: {sources_cited}")
        print(f"  🔍 Query improvement events: {query_improvements}")
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
    summary_file = output_dir / "results_summary.md"

    with open(summary_file, 'w') as f:
        f.write(f"# SCOPE Learning Progress Report\n\n")
        f.write(f"**Research Topic:** {topic}\n\n")
        f.write(
            f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total Iterations:** {num_iterations}\n\n")
        f.write("---\n\n")
        f.write(markdown_table)
        f.write("\n---\n\n")
        f.write("## Files Generated\n\n")
        f.write(
            f"- Reports: `comparison_outputs/reports/report_iter_[1-{num_iterations}].txt`\n")
        f.write(
            f"- Rules Snapshots: `comparison_outputs/rules_snapshots/rules_iter_[1-{num_iterations}].json`\n")
        f.write(f"- Raw Data: `comparison_outputs/iteration_data.json`\n\n")
        f.write("## Next Steps\n\n")
        f.write("1. Review each report in the `reports/` folder\n")
        f.write("2. Send each report to Gemini and Grok for scoring (1-10)\n")
        f.write("3. Update the Gemini Score and Grok Score columns in this table\n")
        f.write("4. Use this table in your LangChain community presentation\n")

    # Save JSON data
    json_file = save_iteration_data(iterations_data, output_dir)

    # Display results
    print(markdown_table)

    print("\n" + "="*70)
    print("DEMO COMPLETE!")
    print("="*70)
    print(f"\n✅ Successfully completed {num_iterations} iterations")
    print(f"\n📊 Results saved to:")
    print(f"   • Summary table: {summary_file}")
    print(f"   • Raw data: {json_file}")
    print(f"   • Reports: {reports_dir}/")
    print(f"   • Rules: {rules_dir}/")

    print("\n📋 Next steps for presentation:")
    print("   1. Review reports in comparison_outputs/reports/")
    print("   2. Send each report to Gemini for scoring")
    print("   3. Send each report to Grok for scoring")
    print("   4. Update results_summary.md with scores")
    print("   5. Use the markdown table in your presentation!")

    print(f"\n💡 Tip: To run more iterations, use:")
    print(f"   python compare_scope_impact.py --iterations 20")
    print(f"   python compare_scope_impact.py --iterations 10 --topic 'your topic here'")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
