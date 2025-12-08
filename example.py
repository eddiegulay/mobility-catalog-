"""
Example script demonstrating the structured JSON output format.

This shows how to use the research agent programmatically and get
structured JSON output with question, answer, and timestamp.
"""

from graphs.research_graph import research_graph
from utils.formatting import format_research_output
import json


def run_example():
    """Run a simple example query and display the JSON output."""
    
    # Define a query
    query = "What are the main components of LangGraph?"
    
    # Initialize state
    initial_state = {
        "query": query,
        "summary": "",
        "key_points": [],
        "sources_consulted": [],
        "internal_notes": ""
    }
    
    print(f"Query: {query}\n")
    print("Processing...\n")
    
    # Invoke the graph
    result = research_graph.invoke(initial_state)
    
    # Format as JSON
    json_output = format_research_output(result)
    
    print("=" * 60)
    print("STRUCTURED JSON OUTPUT:")
    print("=" * 60)
    print(json_output)
    print("\n")
    
    # Parse and display structure
    parsed = json.loads(json_output)
    print("=" * 60)
    print("OUTPUT STRUCTURE:")
    print("=" * 60)
    print(f"✓ question: string ({len(parsed['question'])} chars)")
    print(f"✓ answer: string ({len(parsed['answer'])} chars)")
    print(f"✓ time_date: ISO 8601 timestamp")
    print("=" * 60)


if __name__ == "__main__":
    run_example()
