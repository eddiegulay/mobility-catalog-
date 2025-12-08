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
    
    UNIVERSAL_PROMPT = """You are a Mobility Research Agent. Your task is to generate a specific section of a mobility measure using clear, descriptive, research-informed content.

GENERAL RULES:
- Output ONLY valid JSON for your assigned section.
- Your content must be descriptive, explanatory, and informative.
- Avoid generic task lists like "design X", "plan Y", or "choose Z".
- Instead, explain what each element actually consists of, why it matters, and how it supports implementation.
- Focus on clarity, real-world applicability, and practical detail.
- Write as if your text will be used by planners, designers, and policy-makers to understand the measure, NOT as instructions to a developer.
- Use Sweden and European mobility context when helpful.
- Never invent statistical data; use qualitative evidence grounded in known mobility practice.
- Keep professional tone, but allow depth and substance. Do not be overly short.

Your output must help the reader understand the concept, not merely list steps."""
    
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
    
    def generate(self, measure_name: str, context: str = "") -> tuple:
        """
        Generate JSON section for this agent.
        
        Args:
            measure_name: Name of mobility measure
            context: Additional context
            
        Returns:
            Tuple of (result_dict, error_message)
        """
        import time
        import random
        from config.settings import settings
        
        # Rate limiting: add random delay to spread out parallel requests
        if settings.ENABLE_RATE_LIMITING:
            delay = random.uniform(
                settings.REQUEST_DELAY_MIN,
                settings.REQUEST_DELAY_MAX
            )
            logger.debug(f"[{self.section_name}] Rate limiting delay: {delay:.2f}s")
            time.sleep(delay)
        
        logger.info(f"[{self.section_name}] Generating section for: {measure_name}")
        
        # Construct full prompt
        full_prompt = f"{self.UNIVERSAL_PROMPT}\n\n{self.schema_prompt}\n\nMobility Measure: {measure_name}"
        
        if context:
            full_prompt += f"\nContext: {context}"
        
        try:
            # Invoke LLM - use the llm instance from config
            response = self.llm.invoke(full_prompt)
            
            # Extract and parse JSON
            from utils.json_utils import extract_json_from_text, safe_json_parse
            
            json_text = extract_json_from_text(response.content)
            result, parse_error = safe_json_parse(json_text)
            
            if parse_error:
                error_msg = f"JSON parsing error in {self.section_name}: {parse_error}"
                logger.error(f"[{self.section_name}] {error_msg}")
                return {}, error_msg
            
            logger.info(f"[{self.section_name}] ✓ Section generated successfully")
            return result, None
            
        except Exception as e:
            error_str = str(e)
            
            # Check if it's a rate limit error (429)
            if "429" in error_str or "rate_limit" in error_str.lower():
                # Extract suggested wait time from error message
                import re
                wait_match = re.search(r'try again in ([\d.]+)([ms])', error_str)
                
                if wait_match:
                    wait_value = float(wait_match.group(1))
                    wait_unit = wait_match.group(2)
                    
                    # Convert to seconds
                    wait_time = wait_value if wait_unit == 's' else wait_value / 1000
                    wait_time = min(wait_time, 10.0)  # Cap at 10 seconds
                    
                    logger.info(f"[{self.section_name}] Rate limit hit. Waiting {wait_time:.1f}s before retry...")
                    time.sleep(wait_time + 0.5)  # Add small buffer
                    
                    # Retry with same model once
                    try:
                        response = self.llm.invoke(full_prompt)
                        
                        from utils.json_utils import extract_json_from_text, safe_json_parse
                        json_text = extract_json_from_text(response.content)
                        result, parse_error = safe_json_parse(json_text)
                        
                        if not parse_error:
                            logger.info(f"[{self.section_name}] ✓ Section generated after retry")
                            return result, None
                    except Exception as retry_error:
                        logger.debug(f"[{self.section_name}] Retry failed, trying fallback...")
                
                # Retry failed or no wait time found, try fallback model
                logger.warning(f"[{self.section_name}] Trying fallback model...")
                
                try:
                    from config.settings import settings
                    from langchain_groq import ChatGroq
                    
                    fallback_llm = ChatGroq(
                        api_key=settings.GROQ_API_KEY,
                        model=settings.FALLBACK_MODEL,
                        temperature=settings.TEMPERATURE,
                        max_tokens=settings.MAX_TOKENS,
                    )
                    
                    response = fallback_llm.invoke(full_prompt)
                    
                    from utils.json_utils import extract_json_from_text, safe_json_parse
                    json_text = extract_json_from_text(response.content)
                    result, parse_error = safe_json_parse(json_text)
                    
                    if parse_error:
                        error_msg = f"JSON parsing error in {self.section_name} (fallback): {parse_error}"
                        logger.error(f"[{self.section_name}] {error_msg}")
                        return {}, error_msg
                    
                    logger.info(f"[{self.section_name}] ✓ Section generated with fallback model")
                    return result, None
                    
                except Exception as fallback_error:
                    error_msg = f"Error in fallback for {self.section_name}: {str(fallback_error)}"
                    logger.error(f"[{self.section_name}] {error_msg}")
                    return {}, error_msg
            
            # Not a rate limit error, return original error
            error_msg = f"Error generating {self.section_name}: {error_str}"
            logger.error(f"[{self.section_name}] {error_msg}")
            return {}, error_msg
    
    def __str__(self) -> str:
        """String representation."""
        return f"<MobilityAgent: {self.section_name}>"
