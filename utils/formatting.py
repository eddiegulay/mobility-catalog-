"""JSON and text formatting utilities."""

import json
from typing import Any, Dict


def format_research_output(state: Dict[str, Any]) -> str:
    """
    Format research agent state into pretty-printed JSON.
    
    Args:
        state: Research agent state dictionary
        
    Returns:
        Pretty-printed JSON string
    """
    output = {
        "query": state.get("query", ""),
        "summary": state.get("summary", ""),
        "key_points": state.get("key_points", []),
        "sources_consulted": state.get("sources_consulted", [])
    }
    
    return json.dumps(output, indent=2, ensure_ascii=False)


def validate_research_output(state: Dict[str, Any]) -> bool:
    """
    Validate that research output has all required fields.
    
    Args:
        state: Research agent state dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ["query", "summary", "key_points", "sources_consulted"]
    
    for field in required_fields:
        if field not in state:
            return False
        
        # Validate types
        if field == "query" and not isinstance(state[field], str):
            return False
        if field == "summary" and not isinstance(state[field], str):
            return False
        if field in ["key_points", "sources_consulted"] and not isinstance(state[field], list):
            return False
    
    return True


def print_header(text: str, width: int = 60) -> None:
    """
    Print a formatted header.
    
    Args:
        text: Header text
        width: Total width of the header
    """
    border = "=" * width
    print(f"\n{border}")
    print(f"{text.center(width)}")
    print(f"{border}\n")
