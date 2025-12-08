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

Rules:
- description = 2–3 sentences max.
- behavioural_primary = one clear behavioural goal.
- behavioural_secondary = 2–4 supporting behaviours.'''
    
    def __init__(self):
        super().__init__("overview", self.SCHEMA_PROMPT)


def overview_agent_node(state: MobilityResearchState) -> dict:
    """LangGraph node function for overview agent."""
    agent = OverviewAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    
    if error:
        return {"overview": {}, "errors": [error]}
    
    return {"overview": result, "errors": []}
