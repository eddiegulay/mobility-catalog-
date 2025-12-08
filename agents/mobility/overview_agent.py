"""Overview Agent - Generates description and behavioural goals."""

from agents.mobility.base import BaseMobilityAgent
from schemas.mobility_measure import MobilityResearchState


class OverviewAgent(BaseMobilityAgent):
    """Generates the overview section of a mobility measure."""
    
    SCHEMA_PROMPT = '''Generate ONLY the "overview" section:

{
  "description": "",
  "behavioural_primary": "",
  "behavioural_secondary": []
}

Your content must provide meaningful explanation, not generic statements.
Describe what the mobility measure fundamentally is, how it works, and why it matters.
The behavioural fields must describe real behavioural dynamics, not vague goals.

Rules:
- description = 2–3 sentences providing substantive explanation of what this measure is and how it functions
- behavioural_primary = describe the main behavioural change this measure aims to influence and why
- behavioural_secondary = 2–4 supporting behavioural patterns, each explained clearly'''
    
    def __init__(self):
        super().__init__("overview", self.SCHEMA_PROMPT)


def overview_agent_node(state: MobilityResearchState) -> dict:
    """LangGraph node function for overview agent."""
    agent = OverviewAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    
    if error:
        return {"overview": {}, "errors": [error]}
    
    return {"overview": result, "errors": []}
