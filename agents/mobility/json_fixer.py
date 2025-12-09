"""JSON Fixer Agent - specialized in repairing malformed JSON."""

from typing import Dict, Any, Optional, Tuple
from langchain_core.messages import SystemMessage, HumanMessage
from config.llm import llm
from utils.logger import logger
from utils.json_utils import extract_json_from_text, safe_json_parse

class JsonFixerAgent:
    """
    Specialized agent that uses an LLM to repair broken JSON strings.
    """
    
    SYSTEM_PROMPT = """You are a JSON Repair Expert. Your ONLY job is to fix malformed JSON.
    
    The user will provide:
    1. A broken JSON string
    2. An error message explaining what's wrong
    3. (Optional) The expected schema/context
    
    YOUR RULES:
    - You must return ONLY valid, parseable JSON.
    - Do not add any markdown formatting, no ```json blocks.
    - Do not add any conversational text.
    - Preserve the original data as much as possible.
    - Fix syntax errors (missing commas, unclosed quotes/braces).
    - Ensure all keys and string values are properly double-quoted.
    """

    def __init__(self):
        self.llm = llm

    def fix_json(self, broken_json: str, error_msg: str, context_prompt: str = "") -> Tuple[Dict[str, Any], Optional[str]]:
        """
        Attempt to fix a broken JSON string using the LLM.

        Args:
            broken_json: The malformed JSON string
            error_msg: The error message from the failed parse attempt
            context_prompt: The original schema/instruction prompt (to help the LLM understand expected structure)

        Returns:
            Tuple of (fixed_dict, error_message)
            If success: (dict, None)
            If failure: ({}, error_msg)
        """
        logger.info("🔧 JSON FIXER: Attempting to repair malformed JSON...")
        
        # Construct a targeted prompt for the fix
        fix_prompt = f"""I have some malformed JSON that failed to parse.
        
ERROR: {error_msg}

BROKEN JSON:
{broken_json}

EXPECTED SCHEMA/CONTEXT:
{context_prompt}

Please fix the JSON errors and return the valid JSON object.
"""
        
        # Retry logic for rate limits
        max_retries = 3
        
        import time
        import re
        
        for attempt in range(max_retries + 1):
            try:
                # We use the same LLM instance
                messages = [
                    SystemMessage(content=self.SYSTEM_PROMPT),
                    HumanMessage(content=fix_prompt)
                ]
                
                response = self.llm.invoke(messages)
                content = response.content
                
                # Clean and parse the result
                json_text = extract_json_from_text(content)
                result, parse_error = safe_json_parse(json_text)
                
                if parse_error:
                    msg = f"Fix attempts failed: {parse_error}"
                    logger.error(f"🔧 {msg}")
                    return {}, msg
                    
                logger.info("🔧 JSON FIXER: Successfully repaired JSON!")
                return result, None

            except Exception as e:
                error_str = str(e)
                
                # Check for rate limit
                if "429" in error_str or "rate_limit" in error_str.lower():
                    if attempt < max_retries:
                        # Extract wait time or default to exponential backoff
                        wait_match = re.search(r'try again in ([\d.]+)([ms])', error_str)
                        if wait_match:
                            wait_value = float(wait_match.group(1))
                            wait_unit = wait_match.group(2)
                            wait_time = wait_value if wait_unit == 's' else wait_value / 1000
                        else:
                            wait_time = 2 * (2 ** attempt)  # 2, 4, 8 seconds
                            
                        wait_time = min(wait_time, 15.0)
                        
                        logger.warning(f"🔧 JSON FIXER: Rate limit hit. Waiting {wait_time:.1f}s before retry {attempt+1}/{max_retries}...")
                        time.sleep(wait_time + 0.5)
                        continue
                
                # If legitimate error or out of retries
                msg = f"Error during JSON repair: {error_str}"
                logger.error(f"🔧 {msg}")
                return {}, msg
