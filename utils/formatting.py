"""JSON and text formatting utilities."""

import json
from typing import Any, Dict


def format_research_output(state: Dict[str, Any]) -> str:
    """
    Format research agent state into structured JSON output.
    
    Args:
        state: Research agent state dictionary
        
    Returns:
        JSON string with question, answer, and timestamp
    """
    from datetime import datetime
    
    output = {
        "question": state.get("query", ""),
        "answer": state.get("summary", ""),
        "time_date": datetime.now().isoformat()
    }
    
    return json.dumps(output, indent=2, ensure_ascii=False)


def validate_research_output(state: Dict[str, Any]) -> bool:
    """
    Validate that research output has required fields.
    
    Args:
        state: Research agent state dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ["query", "summary"]
    
    for field in required_fields:
        if field not in state:
            return False
        
        # Validate types
        if not isinstance(state[field], str):
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
