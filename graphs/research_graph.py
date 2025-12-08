"""LangGraph workflow definition for research agent."""

from langgraph.graph import StateGraph, START, END
from agents.research_agent import (
    ResearchState,
    analyze_query_node,
    research_node,
    synthesize_node
)
from utils.logger import logger


def create_research_graph() -> StateGraph:
    """
    Create and compile the research agent workflow graph.
    
    Returns:
        Compiled StateGraph ready for invocation
    """
    logger.info("Building research graph...")
    
    # Initialize the graph with our state schema
    workflow = StateGraph(ResearchState)
    
    # Add nodes to the graph
    workflow.add_node("analyze_query", analyze_query_node)
    workflow.add_node("research", research_node)
    workflow.add_node("synthesize", synthesize_node)
    
    # Define the workflow edges
    workflow.add_edge(START, "analyze_query")
    workflow.add_edge("analyze_query", "research")
    workflow.add_edge("research", "synthesize")
    workflow.add_edge("synthesize", END)
    
    # Compile the graph
    graph = workflow.compile()
    
    logger.info("Research graph compiled successfully!")
    
    return graph


# Create the compiled graph instance
research_graph = create_research_graph()
