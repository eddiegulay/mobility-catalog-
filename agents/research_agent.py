"""Research agent implementation following LangGraph patterns."""

from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, SystemMessage
from config.llm import llm
from utils.logger import logger
import operator


# Define the state schema for the research agent
class ResearchState(TypedDict):
    """State schema for the research workflow."""
    query: str
    summary: str
    key_points: Annotated[list[str], operator.add]
    sources_consulted: Annotated[list[str], operator.add]
    internal_notes: str  # For intermediate processing


def analyze_query_node(state: ResearchState) -> ResearchState:
    """
    Analyze the user's query to understand research requirements.
    
    Args:
        state: Current research state
        
    Returns:
        Updated state with internal notes
    """
    logger.info(f"Analyzing query: {state['query']}")
    
    messages = [
        SystemMessage(content=(
            "You are a research assistant. Analyze the given query and provide "
            "insights about what kind of information would be needed to answer it thoroughly."
        )),
        HumanMessage(content=f"Query: {state['query']}\n\nWhat are the key aspects to research?")
    ]
    
    response = llm.invoke(messages)
    
    return {
        **state,
        "internal_notes": response.content,
        "sources_consulted": ["LLM Query Analysis"]
    }


def research_node(state: ResearchState) -> ResearchState:
    """
    Perform research using the LLM to gather information.
    
    Args:
        state: Current research state with query and analysis
        
    Returns:
        Updated state with research findings
    """
    logger.info("Conducting research...")
    
    messages = [
        SystemMessage(content=(
            "You are an expert researcher. Based on the query and analysis notes, "
            "provide detailed research findings. Include key points and insights."
        )),
        HumanMessage(content=(
            f"Query: {state['query']}\n\n"
            f"Analysis: {state.get('internal_notes', '')}\n\n"
            "Provide comprehensive research findings with specific insights and key points."
        ))
    ]
    
    response = llm.invoke(messages)
    
    return {
        **state,
        "internal_notes": state.get("internal_notes", "") + f"\n\nResearch findings: {response.content}",
        "sources_consulted": ["LLM Research Database"]
    }


def synthesize_node(state: ResearchState) -> ResearchState:
    """
    Synthesize research findings into structured output.
    
    Args:
        state: Current research state with findings
        
    Returns:
        Final state with summary and key points
    """
    logger.info("Synthesizing results...")
    
    messages = [
        SystemMessage(content=(
            "You are a research synthesizer. Create a concise summary and extract "
            "3-5 key points from the research findings. Format your response as:\n"
            "SUMMARY: [brief 2-3 sentence summary]\n"
            "KEY_POINTS:\n- [point 1]\n- [point 2]\n- [point 3]\n..."
        )),
        HumanMessage(content=(
            f"Query: {state['query']}\n\n"
            f"Research Notes:\n{state.get('internal_notes', '')}\n\n"
            "Synthesize this into a summary and key points."
        ))
    ]
    
    response = llm.invoke(messages)
    content = response.content
    
    # Parse the response
    summary = ""
    key_points = []
    
    if "SUMMARY:" in content:
        summary_part = content.split("SUMMARY:")[1].split("KEY_POINTS:")[0].strip()
        summary = summary_part
    
    if "KEY_POINTS:" in content:
        points_part = content.split("KEY_POINTS:")[1].strip()
        key_points = [
            line.strip("- ").strip() 
            for line in points_part.split("\n") 
            if line.strip().startswith("-")
        ]
    
    # Fallback if parsing fails
    if not summary:
        summary = content[:200] + "..." if len(content) > 200 else content
    if not key_points:
        key_points = ["Research completed - see summary for details"]
    
    logger.info("Synthesis complete!")
    
    return {
        **state,
        "summary": summary,
        "key_points": key_points,
        "sources_consulted": ["LLM Synthesis Engine"]
    }
