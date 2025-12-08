"""Context Agent - Generates target users and suitability information."""

from agents.mobility.base import BaseMobilityAgent
from schemas.mobility_measure import MobilityResearchState


class ContextAgent(BaseMobilityAgent):
    """Generates the context section of a mobility measure."""
    
    SCHEMA_PROMPT = '''Generate ONLY the "context" section:

{
  "target_users": [],
  "suitable_strong": [],
  "suitable_weak": []
}

For each suitability item, describe conditions precisely.
Avoid vague labels like "urban" alone.
Focus on specific situational characteristics: density, land-use patterns, cycling culture, street design, and public transport integration.

Rules:
- target_users = specific user groups with meaningful descriptors
- suitable_strong = describe WHERE and WHY this measure works well (8-15 words per item)
- suitable_weak = describe conditions that limit effectiveness with reasoning (8-15 words per item)'''
    
    def __init__(self):
        super().__init__("context", self.SCHEMA_PROMPT)


def context_agent_node(state: MobilityResearchState) -> dict:
    """LangGraph node function for context agent."""
    agent = ContextAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    
    if error:
        return {"context_data": {}, "errors": [error]}
    
    # Note: using "context_data" in state to avoid conflict with "context" input field
    return {"context_data": result, "errors": []}
