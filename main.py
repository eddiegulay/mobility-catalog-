"""Main entrypoint for the LangGraph research agent."""

import sys
from graphs.research_graph import research_graph
from utils.formatting import format_research_output, validate_research_output, print_header
from utils.logger import logger


def run_research(query: str) -> dict:
    """
    Run the research agent workflow with the given query.
    
    Args:
        query: The research question or topic
        
    Returns:
        Dictionary containing the research results
        
    Example:
        >>> result = run_research("What are the key benefits of LangGraph?")
        >>> print(result['summary'])
    """
    logger.info(f"Starting research workflow for query: '{query}'")
    
    # Initialize state
    initial_state = {
        "query": query,
        "summary": "",
        "key_points": [],
        "sources_consulted": [],
        "internal_notes": ""
    }
    
    # Invoke the graph
    try:
        final_state = research_graph.invoke(initial_state)
        
        # Validate output
        if not validate_research_output(final_state):
            logger.warning("Output validation failed - some fields may be missing")
        
        return final_state
        
    except Exception as e:
        logger.error(f"Error during research workflow: {e}")
        raise


def main():
    """Main function to run the research agent from command line."""
    print_header("🔬 LangGraph Research Agent")
    
    # Get query from command line or prompt user
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        print("Enter your research query:")
        query = input("> ").strip()
        
        if not query:
            print("Error: No query provided.")
            sys.exit(1)
    
    print(f"\n🔍 Researching: {query}\n")
    
    try:
        # Run the research workflow
        result = run_research(query)
        
        # Display results
        print_header("📊 Research Results")
        print(format_research_output(result))
        print()
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease ensure you have:")
        print("1. Created a .env file (copy from .env.example)")
        print("2. Added your GROQ_API_KEY to the .env file")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.exception("Full error details:")
        sys.exit(1)


if __name__ == "__main__":
    main()
