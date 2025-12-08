"""Interactive CLI for the LangGraph research agent."""

import sys
from graphs.research_graph import research_graph
from utils.formatting import format_research_output, validate_research_output, print_header
from utils.logger import logger


def print_welcome():
    """Print welcome message."""
    print_header("🔬 LangGraph Research Agent - Interactive Mode")
    print("Ask me anything! I'll research and provide detailed answers.")
    print("\nCommands:")
    print("  - Type your question and press Enter")
    print("  - Type 'quit', 'exit', or 'q' to exit")
    print("  - Type 'help' for this message")
    print("  - Press Ctrl+C to exit anytime")
    print("\n" + "=" * 60)


def run_research(query: str) -> dict:
    """
    Run the research agent workflow with the given query.
    
    Args:
        query: The research question or topic
        
    Returns:
        Dictionary containing the research results
    """
    initial_state = {
        "query": query,
        "summary": "",
        "key_points": [],
        "sources_consulted": [],
        "internal_notes": ""
    }
    
    try:
        final_state = research_graph.invoke(initial_state)
        
        if not validate_research_output(final_state):
            logger.warning("Output validation failed - some fields may be missing")
        
        return final_state
        
    except Exception as e:
        logger.error(f"Error during research workflow: {e}")
        raise


def format_response_for_cli(result: dict) -> str:
    """
    Format research results for CLI display.
    
    Args:
        result: Research results dictionary
        
    Returns:
        Formatted string for display
    """
    from datetime import datetime
    
    lines = []
    lines.append("\n💡 Answer:")
    lines.append("-" * 60)
    lines.append(result.get("summary", "No answer available"))
    lines.append("\n⏰ Timestamp:")
    lines.append("-" * 60)
    lines.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    lines.append("\n" + "=" * 60)
    
    return "\n".join(lines)


def interactive_mode():
    """Run the research agent in interactive mode."""
    print_welcome()
    
    query_count = 0
    
    try:
        while True:
            # Prompt for query
            try:
                query = input("\n🔍 Your Question: ").strip()
            except EOFError:
                print("\n\n👋 Goodbye!")
                break
            
            # Handle empty input
            if not query:
                continue
            
            # Handle commands
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if query.lower() == 'help':
                print_welcome()
                continue
            
            # Process query
            query_count += 1
            print(f"\n🤔 Researching... (Query #{query_count})")
            
            try:
                result = run_research(query)
                print(format_response_for_cli(result))
                
            except ValueError as e:
                print(f"\n❌ Configuration Error: {e}")
                print("\nPlease ensure you have:")
                print("1. Created a .env file (copy from .env.example)")
                print("2. Added your GROQ_API_KEY to the .env file")
                break
                
            except Exception as e:
                print(f"\n❌ Error: {e}")
                logger.exception("Full error details:")
                print("\nYou can continue with another question or type 'quit' to exit.")
    
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
    
    if query_count > 0:
        print(f"\n✅ Answered {query_count} question(s) in this session.")


def main():
    """Main entrypoint for interactive CLI."""
    interactive_mode()


if __name__ == "__main__":
    main()
