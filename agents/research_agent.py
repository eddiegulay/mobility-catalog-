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
            "You are a research synthesizer. Create a comprehensive, well-structured answer "
            "that synthesizes all the research findings. The answer should be clear, informative, "
            "and directly address the user's question. Include key insights and important details."
        )),
        HumanMessage(content=(
            f"Query: {state['query']}\n\n"
            f"Research Notes:\n{state.get('internal_notes', '')}\n\n"
            "Provide a comprehensive answer to this query based on the research."
        ))
    ]
    
    response = llm.invoke(messages)
    answer = response.content.strip()
    
    logger.info("Synthesis complete!")
    
    return {
        **state,
        "summary": answer,  # Store the answer in summary field
        "key_points": [],   # Keep for backward compatibility
        "sources_consulted": ["LLM Synthesis Engine"]
    }
