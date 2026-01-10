import config
from graph import build_research_graph


def print_analysts(analysts):
    """Print analyst information"""
    for analyst in analysts:
        print(f"Name: {analyst.name}")
        print(f"Affiliation: {analyst.affiliation}")
        print(f"Role: {analyst.role}")
        print(f"Description: {analyst.description}")
        print("-" * 50)


def run_research_assistant(topic: str, max_analysts: int = 3, thread_id: str = "1"):
    """Run the research assistant"""
    graph = build_research_graph()
    thread = {"configurable": {"thread_id": thread_id}}
    
    # Initial run - generate analysts
    print("\n=== Generating Analysts ===\n")
    for event in graph.stream({
        "topic": topic,
        "max_analysts": max_analysts
    }, thread, stream_mode="values"):
        analysts = event.get('analysts', '')
        if analysts:
            print_analysts(analysts)
    
    # Get feedback
    print("\n=== Waiting for Human Feedback ===")
    print("Current state:", graph.get_state(thread).next)
    
    feedback = input("\nEnter feedback (press Enter to continue without feedback): ").strip()
    
    if feedback:
        graph.update_state(
            thread,
            {"human_analyst_feedback": feedback},
            as_node="human_feedback"
        )
        
        # Regenerate analysts with feedback
        print("\n=== Regenerating Analysts with Feedback ===\n")
        for event in graph.stream(None, thread, stream_mode="values"):
            analysts = event.get('analysts', '')
            if analysts:
                print_analysts(analysts)
        
        # Confirm satisfaction
        confirm = input("\nAre you satisfied? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Process stopped. Run again with different inputs.")
            return None
    
    # Confirm to proceed
    graph.update_state(
        thread,
        {"human_analyst_feedback": None},
        as_node="human_feedback"
    )
    
    # Continue with interviews and report generation
    print("\n=== Conducting Interviews and Generating Report ===\n")
    for event in graph.stream(None, thread, stream_mode="updates"):
        node_name = next(iter(event.keys()))
        print(f"Processing: {node_name}")
    
    # Get final report
    final_state = graph.get_state(thread)
    report = final_state.values.get('final_report')
    
    print("\n" + "=" * 80)
    print("FINAL REPORT")
    print("=" * 80 + "\n")
    print(report)
    
    return report


def main():
    """Main entry point"""
    print("=== Research Assistant ===\n")
    
    topic = input("Enter research topic: ").strip()
    if not topic:
        topic = "The benefits of adopting LangGraph as an agent framework"
        print(f"Using default topic: {topic}")
    
    max_analysts_input = input("Enter number of analysts (default 3): ").strip()
    max_analysts = int(max_analysts_input) if max_analysts_input else 3
    
    run_research_assistant(topic, max_analysts)


if __name__ == "__main__":
    main()
