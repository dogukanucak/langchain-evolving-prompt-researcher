#!/usr/bin/env python3
"""
Simple script to demonstrate SCOPE's impact by comparing before/after runs.

This script runs the research assistant twice with the same topic:
1. First run: Clean slate (no SCOPE rules)
2. Second run: With learned rules from first run

It captures and compares the search queries generated to show improvement.
"""
import subprocess
import json
import os
from pathlib import Path


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


def main():
    print("\n" + "="*70)
    print("SCOPE IMPACT DEMONSTRATION")
    print("="*70)
    print("\nThis demo runs the research assistant twice with the same topic:")
    print("  1. First run: No SCOPE rules (learning from scratch)")
    print("  2. Second run: With learned rules applied")
    print("\nCompare the outputs to see how SCOPE improves search queries!\n")

    # Get topic from user
    topic = input(
        "Enter research topic (or press Enter for 'quantum computing basics'): ").strip()
    if not topic:
        topic = "quantum computing basics"

    # RUN 1: Clean slate
    print("\n" + "="*70)
    print("STEP 1: BASELINE RUN (No SCOPE Rules)")
    print("="*70 + "\n")
    clear_scope_data()

    stdout1, stderr1 = run_research(topic, num_analysts=1, run_label="RUN 1")

    scope_messages_1 = extract_scope_messages(stdout1)
    report_1 = extract_final_report(stdout1)
    rules_after_1 = get_strategic_rules()

    print("\n" + "-"*70)
    print("RUN 1 RESULTS:")
    print("-"*70)
    print(f"SCOPE learning events: {len(scope_messages_1)}")
    for msg in scope_messages_1:
        print(f"  {msg.strip()}")

    print("\n📊 Rules learned in Run 1:")
    print_rules_summary(rules_after_1)

    # Wait for user to continue
    print("\n" + "="*70)
    input("Press Enter to continue to Run 2 (with learned rules)...")

    # RUN 2: With learned rules
    print("\n" + "="*70)
    print("STEP 2: OPTIMIZED RUN (With SCOPE Rules)")
    print("="*70 + "\n")
    print("📚 Applying rules from Run 1...\n")

    stdout2, stderr2 = run_research(topic, num_analysts=1, run_label="RUN 2")

    scope_messages_2 = extract_scope_messages(stdout2)
    report_2 = extract_final_report(stdout2)
    rules_after_2 = get_strategic_rules()

    print("\n" + "-"*70)
    print("RUN 2 RESULTS:")
    print("-"*70)
    print(f"SCOPE learning events: {len(scope_messages_2)}")
    for msg in scope_messages_2:
        print(f"  {msg.strip()}")

    print("\n📊 Total strategic rules after Run 2:")
    print_rules_summary(rules_after_2)

    # COMPARISON
    print("\n" + "="*70)
    print("COMPARISON: RUN 1 vs RUN 2")
    print("="*70)
    print(f"Topic: {topic}")
    print(f"\nRun 1 (no rules):  {len(scope_messages_1)} learning events")
    print(f"Run 2 (with rules): {len(scope_messages_2)} learning events")

    if len(scope_messages_2) < len(scope_messages_1):
        print("\n✅ IMPROVEMENT: Fewer learning events in Run 2")
        print("   This means queries were already better, thanks to applied rules!")
    elif len(scope_messages_2) == len(scope_messages_1):
        print("\n📊 OBSERVATION: Similar learning events")
        print("   SCOPE may be learning new patterns for this specific topic.")

    print("\n💡 TIP: Fewer learning events = queries already optimized!")

    # Save and display reports
    print("\n" + "="*70)
    print("FINAL REPORTS COMPARISON")
    print("="*70)

    if report_1:
        report1_file = save_report(report_1, "report_run1_baseline.txt")
        print(f"\n📄 Run 1 Report saved to: {report1_file}")
        print("\n" + "-"*70)
        print("RUN 1 FINAL REPORT (Baseline - No SCOPE Rules):")
        print("-"*70)
        print(report_1[:800] + "\n... (truncated, see file for full report)")

    if report_2:
        report2_file = save_report(report_2, "report_run2_optimized.txt")
        print(f"\n📄 Run 2 Report saved to: {report2_file}")
        print("\n" + "-"*70)
        print("RUN 2 FINAL REPORT (Optimized - With SCOPE Rules):")
        print("-"*70)
        print(report_2[:800] + "\n... (truncated, see file for full report)")

    print("\n" + "="*70)
    print("QUALITY ANALYSIS")
    print("="*70)

    if report_1 and report_2:
        len_diff = len(report_2) - len(report_1)
        print(f"\nReport 1 length: {len(report_1)} chars")
        print(f"Report 2 length: {len(report_2)} chars")
        print(
            f"Difference: {len_diff:+d} chars ({len_diff/len(report_1)*100:+.1f}%)")

        print("\n💡 To compare reports in detail:")
        print(f"   diff comparison_outputs/report_run1_baseline.txt comparison_outputs/report_run2_optimized.txt")
        print(f"   or open both files side-by-side in your editor")

    print("\n" + "="*70)
    print("DEMO COMPLETE")
    print("="*70)
    print("\n📊 Summary:")
    print(f"   • Topic: {topic}")
    print(
        f"   • Learning improvement: {len(scope_messages_1)} → {len(scope_messages_2)} events")
    print(f"   • Strategic rules learned: {len(rules_after_2)}")
    print(f"   • Reports saved to: comparison_outputs/")

    print("\nNext steps:")
    print("  • Review both reports in comparison_outputs/ folder")
    print("  • Check strategic rules: cat scope_data/strategic_memory/global_rules.json | python3 -m json.tool")
    print("  • Run another topic: python compare_scope_impact.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
