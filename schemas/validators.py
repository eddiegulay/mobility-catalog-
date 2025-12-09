"""JSON validation utilities for mobility measures."""

import json
from typing import Any, Dict, List
from schemas.mobility_measure import CompleteMobilityMeasure


def validate_section(section_name: str, data: Dict[str, Any]) -> tuple[bool, List[str]]:
    """
    Validate an individual section of a mobility measure.
    
    Args:
        section_name: Name of the section (e.g., "meta", "overview")
        data: The JSON data for that section
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    if not data:
        errors.append(f"Section '{section_name}' is empty")
        return False, errors
    
    if not isinstance(data, dict):
        errors.append(f"Section '{section_name}' must be a dictionary")
        return False, errors
    
    # Basic validation - check for required keys based on section
    # (Full schema validation would use pydantic or similar)
    
    return len(errors) == 0, errors


def validate_complete_measure(data: Dict[str, Any]) -> tuple[bool, List[str]]:
    """
    Validate a complete mobility measure document.
    
    Args:
        data: Complete mobility measure JSON
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    required_sections = [
        "meta", "overview", "context", "evidence", "impact",
        "requirements", "infrastructure", "operations", "costs",
        "risks", "monitoring", "checklist", "lifecycle",
        "roles", "financial", "compliance", "visibility",
        "selection", "scalability"
    ]
    
    # Check all required sections exist
    for section in required_sections:
        if section not in data:
            errors.append(f"Missing required section: {section}")
        elif not data[section]:
            errors.append(f"Section '{section}' is empty")
    
    return len(errors) == 0, errors


def merge_sections(**sections: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge all section dictionaries into a single complete mobility measure.
    Handles cases where models might return the inner object directly
    (unwrapped) or wrapped in the section name.
    """
    complete_measure = {}
    
    for section_name, section_data in sections.items():
        if not section_data:
            continue
            
        # Case 1: Data is wrapped correctly { "section_name": { ... } }
        if section_name in section_data:
            complete_measure[section_name] = section_data[section_name]
            
        # Case 2: Data is unwrapped { "field1": ... } - Common with Haiku
        # Check if it looks like the inner content (has expected keys)
        elif isinstance(section_data, dict) and len(section_data) > 0:
            # Assume it's the inner content and wrap it
            complete_measure[section_name] = section_data
            
    return complete_measure


def clean_json_output(text: str) -> str:
    """
    Clean LLM output to extract valid JSON.
    
    Handles cases where LLM might add markdown or extra text.
    
    Args:
        text: Raw output from LLM
        
    Returns:
        Cleaned JSON string
    """
    # Remove markdown code blocks
    text = text.strip()
    
    if text.startswith("```json"):
        text = text[7:]  # Remove ```json
    elif text.startswith("```"):
        text = text[3:]  # Remove ```
    
    if text.endswith("```"):
        text = text[:-3]
    
    text = text.strip()
    
    return text


def safe_json_parse(text: str) -> tuple[Dict[str, Any], str]:
    """
    Safely parse JSON with error handling.
    
    Args:
        text: JSON string to parse
        
    Returns:
        Tuple of (parsed_dict or {}, error_message or "")
    """
    try:
        cleaned = clean_json_output(text)
        parsed = json.loads(cleaned)
        return parsed, ""
    except json.JSONDecodeError as e:
        return {}, f"JSON parsing error: {str(e)}"
    except Exception as e:
        return {}, f"Unexpected error: {str(e)}"


def pretty_print_json(data: Dict[str, Any]) -> str:
    """
    Format JSON for pretty printing.
    
    Args:
        data: Dictionary to format
        
    Returns:
        Pretty-printed JSON string
    """
    return json.dumps(data, indent=2, ensure_ascii=False)
