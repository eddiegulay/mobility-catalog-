"""JSON utilities for parsing and cleaning LLM outputs."""

import json
from typing import Any, Dict


def extract_json_from_text(text: str) -> str:
    """
    Extract JSON from text that might contain markdown or other content.
    
    Args:
        text: Raw text possibly containing JSON
        
    Returns:
        Extracted JSON string
    """
    text = text.strip()
    
    # Remove markdown code blocks
    if "```json" in text:
        # Extract content between ```json and ```
        start = text.find("```json") + 7
        end = text.find("```", start)
        if end != -1:
            text = text[start:end].strip()
    elif "```" in text:
        # Extract content between ``` and ```
        start = text.find("```") + 3
        end = text.find("```", start)
        if end != -1:
            text = text[start:end].strip()
    
    # Find JSON object boundaries
    if "{" in text and "}" in text:
        start = text.find("{")
        end = text.rfind("}") + 1
        text = text[start:end]
    
    return text.strip()


def safe_json_parse(text: str) -> tuple[Dict[str, Any], str]:
    """
    Safely parse JSON with comprehensive error handling.
    
    Args:
        text: JSON string to parse
        
    Returns:
        Tuple of (parsed_dict or {}, error_message or "")
    """
    try:
        cleaned = extract_json_from_text(text)
        parsed = json.loads(cleaned)
        
        if not isinstance(parsed, dict):
            return {}, "Parsed JSON is not a dictionary"
        
        return parsed, ""
        
    except json.JSONDecodeError as e:
        return {}, f"JSON parsing error at position {e.pos}: {e.msg}"
    except Exception as e:
        return {}, f"Unexpected error: {str(e)}"


def clean_json_output(text: str) -> str:
    """
    Clean and normalize JSON output.
    
    Args:
        text: Raw JSON text
        
    Returns:
        Cleaned JSON string
    """
    return extract_json_from_text(text)


def format_json_pretty(data: Dict[str, Any]) -> str:
    """
    Format dictionary as pretty-printed JSON.
    
    Args:
        data: Dictionary to format
        
    Returns:
        Pretty-printed JSON string
    """
    return json.dumps(data, indent=2, ensure_ascii=False)
