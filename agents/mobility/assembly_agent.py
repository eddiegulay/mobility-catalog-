"""
Assembly Agent - Combines all 19 sections into complete mobility measure.

This is the final agent that collects outputs from all specialized agents,
validates them, and assembles the complete JSON document.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from schemas.mobility_measure import MobilityResearchState, CompleteMobilityMeasure
from schemas.validators import validate_complete_measure, merge_sections
from utils.logger import logger


def assembly_agent_node(state: MobilityResearchState) -> dict:
    """
    Final assembly node that combines all agent outputs.
    
    Collects all 19 sections from state, validates them, merges into
    complete document, and saves to file.
    
    Args:
        state: Current workflow state with all agent outputs
        
    Returns:
        Updated state with complete_measure and output_path
    """
    logger.info("=" * 60)
    logger.info("ASSEMBLY AGENT: Combining all sections")
    logger.info("=" * 60)
    
    # Collect all sections
    sections = {
        "meta": state.get("meta", {}),
        "overview": state.get("overview", {}),
        "context": state.get("context_data", {}),  # Note: context_data due to naming conflict
        "evidence": state.get("evidence", {}),
        "impact": state.get("impact", {}),
        "requirements": state.get("requirements", {}),
        "infrastructure": state.get("infrastructure", {}),
        "operations": state.get("operations", {}),
        "costs": state.get("costs", {}),
        "risks": state.get("risks", {}),
        "monitoring": state.get("monitoring", {}),
        "checklist": state.get("checklist", {}),
        "lifecycle": state.get("lifecycle", {}),
        "roles": state.get("roles", {}),
        "financial": state.get("financial", {}),
        "compliance": state.get("compliance", {}),
        "visibility": state.get("visibility", {}),
        "selection": state.get("selection", {}),
        "scalability": state.get("scalability", {}),
    }
    
    # Check for missing sections
    missing = [name for name, data in sections.items() if not data]
    
    if missing:
        error_msg = f"Missing or empty sections: {', '.join(missing)}"
        logger.error(error_msg)
        return {
            "complete_measure": {},
            "output_path": "",
            "errors": [error_msg]
        }
    
    logger.info(f"✓ All {len(sections)} sections collected")
    
    # Merge sections
    complete = merge_sections(sections)
    
    # Validate complete document
    is_valid, validation_errors = validate_complete_measure(complete)
    
    if not is_valid:
        error_msg = f"Validation failed: {'; '.join(validation_errors)}"
        logger.error(error_msg)
        return {
            "complete_measure": {},
            "output_path": "",
            "errors": [error_msg]
        }
    
    logger.info("✓ Complete document validated")
    
    # Save to file
    output_path = save_mobility_measure(complete, state["measure_name"])
    
    logger.info(f"✓ Saved to: {output_path}")
    logger.info("=" * 60)
    logger.info("ASSEMBLY COMPLETE")
    logger.info("=" * 60)
    
    return {
        "complete_measure": complete,
        "output_path": output_path,
        "errors": []
    }


def save_mobility_measure(data: Dict[str, Any], measure_name: str) -> str:
    """
    Save mobility measure JSON to research_output directory.
    
    Args:
        data: Complete mobility measure data
        measure_name: Name of the mobility measure
        
    Returns:
        Absolute path to saved file
    """
    # Create research_output directory
    output_dir = Path("research_output")
    output_dir.mkdir(exist_ok=True)
    
    # Generate filename: name-mobility-measure.json
    # Clean measure_name for filesystem
    clean_name = measure_name.lower().replace(" ", "-").replace("/", "-")
    filename = f"{clean_name}-mobility-measure.json"
    
    output_path = output_dir / filename
    
    # Save with pretty printing
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return str(output_path.absolute())
