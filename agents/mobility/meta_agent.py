"""Meta Agent - Generates basic metadata about the mobility measure."""

from agents.mobility.base import BaseMobilityAgent
from schemas.mobility_measure import MobilityResearchState
from utils.logger import logger
from config.llm import anthropic_llm


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

Category Definitions:
- Active Mobility: Supports walking, cycling, e-bikes, and cargo bikes (safe infrastructure, secure parking, maintenance).
- Shared Mobility: Services where vehicles are collectively used (shared cars, shared bikes, cargo-bike pools).
- Public Transport: Strengthens access to buses, metro, trains, trams, or integrates housing with transit.
- Information & Nudging: Increases awareness, visibility, behavioural support, and real-time info.
- Logistics: Reduces private car need by simplifying tasks (delivery lockers, tool libraries, goods transport).

Rules:
- short_description = max 20–25 words.
- tags = 3–7 lowercase keywords.
- tags = 3–7 lowercase keywords.
- category must be one of: "Active Mobility", "Shared Mobility", "Public Transport", "Information & Nudging", "Logistics".
- Do not include any other JSON keys.'''
    
    def __init__(self, llm_instance=None):
        super().__init__("meta", self.SCHEMA_PROMPT, llm_instance)


def meta_agent_node(state: MobilityResearchState) -> dict:
    """LangGraph node function for meta agent."""
    from utils.image_search import search_mobility_images
    
    agent = MetaAgent(llm_instance=anthropic_llm)
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    
    if error:
        return {"meta": {}, "errors": [error]}
    
    # Add images automatically using Pexels API
    if result and "images" in result:
        try:
            images = search_mobility_images(state["measure_name"], count=3)
            result["images"] = images
            logger.info(f"Added {len(images)} images to meta section")
        except Exception as e:
            logger.error(f"Failed to fetch images: {e}")
            result["images"] = []
    
    return {"meta": result, "errors": []}
