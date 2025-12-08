"""
Mobility Measure Research - Main Entry Point

Command-line interface for researching mobility measures using
the multi-agent orchestration system.

Usage:
    uv run python mobility_research.py "Electric bikes in new housings"
    uv run python mobility_research.py "Car-sharing service" --context "Urban area"
"""

import sys
import argparse
from pathlib import Path
from graphs.mobility_graph import mobility_graph
from utils.formatting import print_header
from utils.logger import logger
import json


def research_mobility_measure(measure_name: str, context: str = "") -> dict:
    """
    Research a mobility measure using the multi-agent system.
    
    Args:
        measure_name: Name of the mobility measure to research
        context: Additional context or requirements
        
    Returns:
        Final state with complete mobility measure
    """
    logger.info(f"Starting mobility research for: '{measure_name}'")
    
    # Initialize state
    initial_state = {
        "measure_name": measure_name,
        "context": context,
        
        # Initialize all section fields
        "meta": {},
        "overview": {},
        "context_data": {},
        "evidence": {},
        "impact": {},
        "requirements": {},
        "infrastructure": {},
        "operations": {},
        "costs": {},
        "risks": {},
        "monitoring": {},
        "checklist": {},
        "lifecycle": {},
        "roles": {},
        "financial": {},
        "compliance": {},
        "visibility": {},
        "selection": {},
        "scalability": {},
        
        # Output fields
        "complete_measure": {},
        "output_path": "",
        "errors": []
    }
    
    # Invoke the multi-agent graph
    try:
        print_header("🔬 Multi-Agent Mobility Research")
        print(f"\nMobility Measure: {measure_name}")
        if context:
            print(f"Context: {context}")
        print("\n" + "=" * 60)
        print("Executing 19 specialized agents in parallel...")
        print("=" * 60)
        
        final_state = mobility_graph.invoke(initial_state)
        
        return final_state
        
    except Exception as e:
        logger.error(f"Error during mobility research: {e}")
        raise


def display_results(state: dict):
    """
    Display research results.
    
    Args:
        state: Final state from the workflow
    """
    print("\n" + "=" * 60)
    
    if state["errors"]:
        print("❌ ERRORS ENCOUNTERED:")
        print("=" * 60)
        for error in state["errors"]:
            print(f"  • {error}")
        return
    
    print("✅ RESEARCH COMPLETE")
    print("=" * 60)
    
    # Show summary
    complete = state.get("complete_measure", {})
    meta = complete.get("meta", {})
    
    if meta:
        print(f"\n📋 Measure: {meta.get('name', 'Unknown')}")
        print(f"📝 Description: {meta.get('short_description', 'N/A')}")
        print(f"🏷️  Category: {meta.get('category', 'N/A')}")
        print(f"🏷️  Tags: {', '.join(meta.get('tags', []))}")
        print(f"📊 Impact Level: {meta.get('impact_level', 'N/A')}/5")
        print(f"💰 Cost Level: {meta.get('cost_level', 'N/A')}/5")
    
    # Show output file
    output_path = state.get("output_path", "")
    if output_path:
        print(f"\n💾 Saved to: {output_path}")
        
        # Show file size
        file_size = Path(output_path).stat().st_size
        print(f"📦 File size: {file_size:,} bytes")
        
        # Count sections
        print(f"📑 Sections: 19")
    
    print("\n" + "=" * 60)


def main():
    """Main entrypoint."""
    parser = argparse.ArgumentParser(
        description="Research mobility measures using multi-agent AI system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Electric bikes in new housings"
  %(prog)s "Car-sharing service" --context "High-density urban area"
  %(prog)s "E-scooter parking stations" -c "Train station proximity"
        """
    )
    
    parser.add_argument(
        "measure_name",
        nargs="?",
        help="Name of the mobility measure to research"
    )
    
    parser.add_argument(
        "-c", "--context",
        default="",
        help="Additional context for the research"
    )
    
    parser.add_argument(
        "--view",
        action="store_true",
        help="View the generated JSON in console"
    )
    
    args = parser.parse_args()
    
    # Get measure name
    if not args.measure_name:
        print("Mobility Measure Research System")
        print("=" * 60)
        measure_name = input("\n🔍 Enter mobility measure name: ").strip()
        
        if not measure_name:
            print("Error: No measure name provided.")
            sys.exit(1)
        
        context = input("📝 Additional context (optional): ").strip()
    else:
        measure_name = args.measure_name
        context = args.context
    
    try:
        # Run research
        result = research_mobility_measure(measure_name, context)
        
        # Display results
        display_results(result)
        
        # Optionally view JSON
        if args.view and result.get("complete_measure"):
            print("\n" + "=" * 60)
            print("JSON OUTPUT:")
            print("=" * 60)
            print(json.dumps(result["complete_measure"], indent=2))
        
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
