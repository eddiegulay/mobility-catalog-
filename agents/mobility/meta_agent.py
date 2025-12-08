"""Meta Agent - Generates basic metadata about the mobility measure."""

from agents.mobility.base import BaseMobilityAgent
from schemas.mobility_measure import MobilityResearchState
from utils.logger import logger


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
    from utils.image_search import get_mobility_measure_images
    
    agent = MetaAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    
    if error:
        return {"meta": {}, "errors": [error]}
    
    # Add images automatically
    if result and "images" in result:
        try:
            images = get_mobility_measure_images(state["measure_name"], count=3)
            result["images"] = images
        except Exception as e:
            logger.error(f"Failed to fetch images: {e}")
            result["images"] = []
    
    return {"meta": result, "errors": []}
