"""
Assembly Agent - Combines all 19 sections into complete mobility measure.

This is the final agent that collects outputs from all specialized agents,
validates them, and assembles the complete JSON document.
"""

import json
import os
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
        "roles_responsibilities_detailed": state.get("roles_responsibilities_detailed", {}),
        "financial_model": state.get("financial_model", {}),
        "compliance": state.get("compliance", {}),
        "visibility_and_communication_design": state.get("visibility_and_communication_design", {}),
        "selection_logic": state.get("selection_logic", {}),
        "future_scalability": state.get("future_scalability", {}),
    }
    
    # Check for missing sections
    missing_sections = [name for name, data in sections.items() if not data]
    
    if missing_sections:
        logger.warning(f"{len(missing_sections)} sections missing or empty: {', '.join(missing_sections)}")
        logger.warning("Saving partial result - users can manually complete missing sections later")
    
    # Merge all sections (including empty ones with placeholders)
    complete_measure = {}
    for name, data in sections.items():
        if data:
            complete_measure[name] = data
        else:
            # Add placeholder for missing section
            complete_measure[name] = {}
            
    # Add metadata about completeness
    if missing_sections:
        complete_measure["_metadata"] = {
            "incomplete": True,
            "missing_sections": missing_sections,
            "completion_percentage": round((19 - len(missing_sections)) / 19 * 100, 1),
            "generated_at": datetime.now().isoformat(timespec='seconds') + "Z"
        }
    
    # Validate complete document
    # With Haiku/smaller models, we want to be lenient and save even if validation fails
    try:
        from schemas.validators import validate_complete_measure
        is_valid, val_errors = validate_complete_measure(complete_measure)
        
        if not is_valid:
            logger.warning(f"Validation warnings: {val_errors}")
            # We add validation errors to metadata but STILL SAVE the file
            if "_metadata" not in complete_measure:
                complete_measure["_metadata"] = {}
                
            complete_measure["_metadata"]["validation_errors"] = val_errors
            complete_measure["_metadata"]["is_valid"] = False
        else:
            if "_metadata" not in complete_measure:
                complete_measure["_metadata"] = {}
            complete_measure["_metadata"]["is_valid"] = True
            
    except Exception as e:
        logger.warning(f"Validation skipped due to error: {e}")
    
    # Generate output filename
    measure_name = state.get("measure_name", "unknown")
    safe_name = measure_name.lower().replace(" ", "-").replace("/", "-")
    output_dir = "research_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Add '-partial' suffix if incomplete
    suffix = "-partial" if missing_sections else ""
    output_filename = f"{safe_name}-mobility-measure{suffix}.json"
    output_path = os.path.join(output_dir, output_filename)
    
    # Save JSON file
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(complete_measure, f, indent=2, ensure_ascii=False)
        
        file_size = os.path.getsize(output_path)
        completion_pct = round((19 - len(missing_sections)) / 19 * 100, 1)
        
        logger.info(f"✓ Saved to: {output_path}")
        logger.info(f"✓ File size: {file_size:,} bytes")
        logger.info(f"✓ Completion: {completion_pct}% ({19-len(missing_sections)}/19 sections)")
        
        if missing_sections:
            logger.warning(f"⚠ Partial result saved. Missing sections can be completed later.")
    
    except Exception as e:
        logger.error(f"Failed to save output: {e}")
        return {
            "complete_measure": complete_measure,
            "output_path": "",
            "errors": [f"Save error: {str(e)}"]
        }
    
    logger.info("=" * 60)
    logger.info("ASSEMBLY COMPLETE")
    logger.info("=" * 60)
    
    return {
        "complete_measure": complete_measure,
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
