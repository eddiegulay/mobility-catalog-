"""Base class for all mobility measure agents."""

from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from config.llm import llm
from utils.json_utils import safe_json_parse
from utils.logger import logger


class BaseMobilityAgent:
    """
    Base class for all mobility measure agents.
    
    Enforces:
    - Universal prompt for all agents
    - JSON-only output
    - Schema validation
    - Consistent error handling
    """
    
    UNIVERSAL_PROMPT = """You are a Mobility Catalog Agent contributing one section of a structured mobility measure JSON.

Follow these global rules:

1. Output valid JSON only.
2. Only produce the section assigned to you.
3. Match field names and structure EXACTLY as the official schema defines.
4. Keep tone neutral, technical, and concise.
5. Avoid unverifiable claims, statistics, or speculation.
6. If you have no data for a field, return an empty string or empty array as appropriate.
7. Never include explanatory text, comments, or markdown.

Wait for:
- The mobility measure name
- Any additional context provided

Then output ONLY your assigned JSON section."""
    
    def __init__(self, section_name: str, schema_prompt: str):
        """
        Initialize the mobility agent.
        
        Args:
            section_name: Name of the JSON section this agent produces
            schema_prompt: Section-specific schema and rules
        """
        self.section_name = section_name
        self.schema_prompt = schema_prompt
        self.llm = llm
    
    def generate(self, measure_name: str, context: str = "") -> tuple[Dict[str, Any], str]:
        """
        Generate the JSON section for this agent.
        
        Args:
            measure_name: Name of the mobility measure
            context: Additional context or requirements
            
        Returns:
            Tuple of (json_dict, error_message)
            If successful: (parsed_json, "")
            If error: ({}, error_message)
        """
        logger.info(f"[{self.section_name}] Generating section for: {measure_name}")
        
        # Combine universal prompt + section-specific prompt
        system_content = f"{self.UNIVERSAL_PROMPT}\n\n{self.schema_prompt}"
        
        # Create user message with measure name and context
        user_content = f"Mobility Measure: {measure_name}"
        if context:
            user_content += f"\n\nAdditional Context:\n{context}"
        
        messages = [
            SystemMessage(content=system_content),
            HumanMessage(content=user_content)
        ]
        
        try:
            # Call LLM
            response = self.llm.invoke(messages)
            output = response.content.strip()
            
            logger.debug(f"[{self.section_name}] Raw output: {output[:200]}...")
            
            # Parse JSON
            json_data, error = safe_json_parse(output)
            
            if error:
                logger.error(f"[{self.section_name}] JSON parsing failed: {error}")
                return {}, f"JSON parsing error in {self.section_name}: {error}"
            
            logger.info(f"[{self.section_name}] ✓ Section generated successfully")
            return json_data, ""
            
        except Exception as e:
            error_msg = f"Error generating {self.section_name}: {str(e)}"
            logger.error(error_msg)
            return {}, error_msg
    
    def __str__(self) -> str:
        """String representation."""
        return f"<MobilityAgent: {self.section_name}>"
