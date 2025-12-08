"""Meta Agent - Generates basic metadata about the mobility measure."""

from agents.mobility.base import BaseMobilityAgent
from schemas.mobility_measure import MobilityResearchState


class MetaAgent(BaseMobilityAgent):
    """Generates the meta section of a mobility measure."""
    
    SCHEMA_PROMPT = '''Generate ONLY the "meta" section:

{
  "name": "",
  "short_description": "",
  "category": "",
  "tags": [],
  "status": "active",
  "last_updated": "<ISO timestamp>",
  "images": [],
  "impact_level": 1-5,
  "cost_level": 1-5
}

Rules:
- short_description = max 20–25 words.
- tags = 3–7 lowercase keywords.
- category must match the selected catalog category.
- Do not include any other JSON keys.'''
    
    def __init__(self):
        super().__init__("meta", self.SCHEMA_PROMPT)


def meta_agent_node(state: MobilityResearchState) -> dict:
    """LangGraph node function for meta agent."""
    agent = MetaAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    
    if error:
        return {"meta": {}, "errors": [error]}
    
    return {"meta": result, "errors": []}
