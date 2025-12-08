"""
All remaining mobility agents (4-19).

This file contains the remaining 16 specialized agents to keep implementation efficient.
Each agent follows the same pattern as the first 3 agents.
"""

from agents.mobility.base import BaseMobilityAgent
from schemas.mobility_measure import MobilityResearchState


# ============================================================================
# AGENT 4: EVIDENCE
# ============================================================================

class EvidenceAgent(BaseMobilityAgent):
    SCHEMA_PROMPT = '''Generate ONLY the "evidence" section:

{
  "sweden": [],
  "europe": [],
  "research": [],
  "behavioural": []
}

Provide descriptive, research-aligned insights.
Each bullet must convey an actual finding or pattern.
Avoid clichés like "this increases sustainability".
Base statements on known mobility principles (secure parking improves cycling rates, proximity increases mode choice likelihood, etc.)

Rules:
- Each item should be a meaningful insight, not a generic claim
- Reference real mobility patterns and principles
- 1–3 substantive points per field'''
    
    def __init__(self):
        super().__init__("evidence", self.SCHEMA_PROMPT)


def evidence_agent_node(state: MobilityResearchState) -> dict:
    agent = EvidenceAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    return {"evidence": result, "errors": [error]} if error else {"evidence": result, "errors": []}


# ============================================================================
# AGENT 5: IMPACT
# ============================================================================

class ImpactAgent(BaseMobilityAgent):
    SCHEMA_PROMPT = '''Generate ONLY:

{
  "car_ownership_reduction": "",
  "modal_shift": "",
  "parking_reduction": "",
  "satisfaction": "",
  "congestion_reduction": "",
  "long_distance_support": "",
  "other": ""
}

Describe expected impacts in meaningful qualitative ranges.
Avoid single words like "high" unless paired with detail (e.g., "high, especially in dense districts where cycling is common").

Rules:
- Provide context and reasoning for each impact level
- Use qualitative ranges with explanation when possible
- Connect impacts to specific conditions or user groups'''
    
    def __init__(self):
        super().__init__("impact", self.SCHEMA_PROMPT)


def impact_agent_node(state: MobilityResearchState) -> dict:
    agent = ImpactAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    return {"impact": result, "errors": [error]} if error else {"impact": result, "errors": []}


# ============================================================================
# AGENT 6: REQUIREMENTS
# ============================================================================

class RequirementsAgent(BaseMobilityAgent):
    SCHEMA_PROMPT = '''Generate ONLY:

{
  "security": [],
  "infrastructure": [],
  "charging": [],
  "accessibility": [],
  "information": [],
  "quality_standards": []
}

Each requirement must be descriptive and concrete.
Avoid terms like "secure bike parking" alone.
Instead describe what security means (locking points, CCTV, lighting, enclosure quality).

Rules:
- Explain WHAT each requirement consists of
- Describe WHY it matters for implementation
- Provide specific, actionable detail'''
    
    def __init__(self):
        super().__init__("requirements", self.SCHEMA_PROMPT)


def requirements_agent_node(state: MobilityResearchState) -> dict:
    agent = RequirementsAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    return {"requirements": result, "errors": [error]} if error else {"requirements": result, "errors": []}


# ============================================================================
# AGENT 7: INFRASTRUCTURE
# ============================================================================

class InfrastructureAgent(BaseMobilityAgent):
    SCHEMA_PROMPT = '''Generate ONLY:

{
  "key_requirements": [],
  "power_requirements": [],
  "weather_protection": [],
  "placement_rules": [],
  "notes": ""
}

For each item, describe physical characteristics, spatial standards, dimensions, environmental considerations, and user experience.
Avoid simple nouns; provide meaningful explanation.

Rules:
- Describe WHAT the infrastructure consists of physically
- Include relevant dimensions, materials, or technical specs when applicable
- Explain HOW placement or design affects functionality'''
    
    def __init__(self):
        super().__init__("infrastructure", self.SCHEMA_PROMPT)


def infrastructure_agent_node(state: MobilityResearchState) -> dict:
    agent = InfrastructureAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    return {"infrastructure": result, "errors": [error]} if error else {"infrastructure": result, "errors": []}


# ============================================================================
# AGENT 8: OPERATIONS
# ============================================================================

class OperationsAgent(BaseMobilityAgent):
    SCHEMA_PROMPT = '''Generate ONLY:

{
  "developer": [],
  "housing_association": [],
  "mobility_provider": [],
  "city": [],
  "operations_phases": {
    "installation": [],
    "maintenance": [],
    "data_reporting": [],
    "upgrades": []
  }
}

Instead of listing actors, describe their operational role in a meaningful way:
- What the developer maintains during construction
- What housing associations oversee day-to-day
- What mobility providers are responsible for regarding service reliability

Rules:
- Describe WHAT each actor actually does operationally
- Explain responsibilities with context
- For phases, describe activities with operational or planning detail'''
    
    def __init__(self):
        super().__init__("operations", self.SCHEMA_PROMPT)


def operations_agent_node(state: MobilityResearchState) -> dict:
    agent = OperationsAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    return {"operations": result, "errors": [error]} if error else {"operations": result, "errors": []}


# ============================================================================
# AGENT 9: COSTS
# ============================================================================

class CostsAgent(BaseMobilityAgent):
    SCHEMA_PROMPT = '''Generate ONLY:

{
  "upfront": "",
  "operational": "",
  "benefits": []
}

Provide qualitative ranges AND explanation.
Example: "Upfront cost: medium — typically involves shelter installation, structural anchoring, and durable fixtures."

Rules:
- Use qualitative levels (low/medium/high) with reasoning
- Explain WHAT drives costs
- Describe benefits with specific detail'''
    
    def __init__(self):
        super().__init__("costs", self.SCHEMA_PROMPT)


def costs_agent_node(state: MobilityResearchState) -> dict:
    agent = CostsAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    return {"costs": result, "errors": [error]} if error else {"costs": result, "errors": []}


# ============================================================================
# AGENT 10: RISKS
# ============================================================================

class RisksAgent(BaseMobilityAgent):
    SCHEMA_PROMPT = '''Generate ONLY:

{
  "risk_1": "",
  "risk_2": "",
  "risk_3": ""
}

Each risk must describe WHY the risk occurs and HOW it affects implementation or adoption.
Avoid generic phrasing.

Rules:
- Explain the risk mechanism, not just naming it
- Describe impact on implementation or user adoption
- Provide context on likelihood or severity
- Maximum 3 most significant risks'''
    
    def __init__(self):
        super().__init__("risks", self.SCHEMA_PROMPT)


def risks_agent_node(state: MobilityResearchState) -> dict:
    agent = RisksAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    return {"risks": result, "errors": [error]} if error else {"risks": result, "errors": []}


# ============================================================================
# AGENT 11: MONITORING
# ============================================================================

class MonitoringAgent(BaseMobilityAgent):
    SCHEMA_PROMPT = '''Generate ONLY:

{
  "metrics": [],
  "frequency": ""
}

Metrics must be measurable and meaningful.
Describe what each metric actually captures.

Rules:
- 3–6 specific, measurable metrics
- Explain WHAT each metric measures and WHY it matters
- Frequency should include reasoning (e.g., "Quarterly to capture seasonal patterns")'''
    
    def __init__(self):
        super().__init__("monitoring", self.SCHEMA_PROMPT)


def monitoring_agent_node(state: MobilityResearchState) -> dict:
    agent = MonitoringAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    return {"monitoring": result, "errors": [error]} if error else {"monitoring": result, "errors": []}


# ============================================================================
# AGENT 12: CHECKLIST
# ============================================================================

class ChecklistAgent(BaseMobilityAgent):
    SCHEMA_PROMPT = '''Generate ONLY:

{
  "before_move_in": [],
  "at_move_in": [],
  "after_move_in": []
}

Checklists must describe the intention behind each step.
For example: "Assess evening visibility to ensure safe access during winter months."

Rules:
- Each item = 3–6 steps per phase
- Describe WHAT to verify/do and WHY it matters
- Provide actionable detail, not generic tasks
- Include context on timing, conditions, or stakeholders involved'''
    
    def __init__(self):
        super().__init__("checklist", self.SCHEMA_PROMPT)


def checklist_agent_node(state: MobilityResearchState) -> dict:
    agent = ChecklistAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    return {"checklist": result, "errors": [error]} if error else {"checklist": result, "errors": []}


# ============================================================================
# AGENT 13: LIFECYCLE
# ============================================================================

class LifecycleAgent(BaseMobilityAgent):
    SCHEMA_PROMPT = '''Generate ONLY:

{
  "stage_1_land_allocation": [],
  "stage_2_detailed_planning": [],
  "stage_3_construction": [],
  "stage_4_pre_occupancy": [],
  "stage_5_operation_year_1": [],
  "stage_6_long_term": []
}

Each lifecycle item must describe activities with operational or planning detail.
Avoid listing 'design' or 'choose'.
Include considerations, dependencies, or planning context.

Rules:
- 2–5 items per stage
- Describe WHAT happens and WHY it's important at this stage
- Include dependencies, stakeholder coordination, or critical decisions
- Provide planning context, not just action verbs'''
    
    def __init__(self):
        super().__init__("lifecycle", self.SCHEMA_PROMPT)


def lifecycle_agent_node(state: MobilityResearchState) -> dict:
    agent = LifecycleAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    return {"lifecycle": result, "errors": [error]} if error else {"lifecycle": result, "errors": []}


# ============================================================================
# AGENT 14: ROLES & RESPONSIBILITIES
# ============================================================================

class RolesAgent(BaseMobilityAgent):
    SCHEMA_PROMPT = '''Generate ONLY:

{
  "developer": {
    "financial": [],
    "technical": [],
    "handover": []
  },
  "housing_association": {
    "financial": [],
    "operation": [],
    "issue_resolution": []
  },
  "mobility_provider": {
    "service_level": [],
    "data": [],
    "support": []
  },
  "city": {
    "regulation": [],
    "monitoring": []
  }
}

Each responsibility must state what the actor actually DOES and WHY their role matters.
Avoid simple labels like "maintenance".

Rules:
- Describe concrete responsibilities with context
- Explain HOW each role contributes to measure success
- Provide operational detail on what tasks involve'''
    
    def __init__(self):
        super().__init__("roles", self.SCHEMA_PROMPT)


def roles_agent_node(state: MobilityResearchState) -> dict:
    agent = RolesAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    return {"roles": result, "errors": [error]} if error else {"roles": result, "errors": []}


# ============================================================================
# AGENT 15: FINANCIAL MODEL
# ============================================================================

class FinancialAgent(BaseMobilityAgent):
    SCHEMA_PROMPT = '''Generate ONLY:

{
  "cost_distribution": {
    "developer": [],
    "mobility_provider": [],
    "housing_association": [],
    "city": []
  },
  "estimated_costs": {
    "installation_cost": "",
    "annual_maintenance": "",
    "electricity_cost": ""
  },
  "savings": {
    "parking_construction_reduction": "",
    "reduced_need_for_family_car_ownership": ""
  },
  "incentives": []
}

Costs and savings must include reasoning and context.
Avoid generic terms without explanation.

Rules:
- Use qualitative/semi-quantitative values with explanation
- Describe WHAT drives each cost component
- Explain HOW savings materialize
- incentives: 1–3 items with specific detail on requirements or mechanisms'''
    
    def __init__(self):
        super().__init__("financial", self.SCHEMA_PROMPT)


def financial_agent_node(state: MobilityResearchState) -> dict:
    agent = FinancialAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    return {"financial": result, "errors": [error]} if error else {"financial": result, "errors": []}


# ============================================================================
# AGENT 16: COMPLIANCE
# ============================================================================

class ComplianceAgent(BaseMobilityAgent):
    SCHEMA_PROMPT = '''Generate ONLY:

{
  "minimum_requirements": [],
  "documentation_required": [],
  "approval_process": [],
  "non_compliance_actions": []
}

Explain compliance expectations clearly.
Documentation items should describe what they validate.

Rules:
- Describe WHAT each requirement ensures
- Explain WHY documentation is needed
- Detail approval steps with stakeholders involved
- Describe consequences and remediation for non-compliance'''
    
    def __init__(self):
        super().__init__("compliance", self.SCHEMA_PROMPT)


def compliance_agent_node(state: MobilityResearchState) -> dict:
    agent = ComplianceAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    return {"compliance": result, "errors": [error]} if error else {"compliance": result, "errors": []}


# ============================================================================
# AGENT 17: VISIBILITY & COMMUNICATION
# ============================================================================

class VisibilityAgent(BaseMobilityAgent):
    SCHEMA_PROMPT = '''Generate ONLY:

{
  "signage": [],
  "digital": [],
  "physical_touchpoints": []
}

Describe what signage or communication elements actually convey and how they support adoption.

Rules:
- Explain WHAT information each element communicates
- Describe WHERE and WHEN users encounter it
- Explain HOW it supports awareness or usage'''
    
    def __init__(self):
        super().__init__("visibility", self.SCHEMA_PROMPT)


def visibility_agent_node(state: MobilityResearchState) -> dict:
    agent = VisibilityAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    return {"visibility": result, "errors": [error]} if error else {"visibility": result, "errors": []}


# ============================================================================
# AGENT 18: SELECTION LOGIC
# ============================================================================

class SelectionAgent(BaseMobilityAgent):
    SCHEMA_PROMPT = '''Generate ONLY:

{
  "requires": [],
  "not_recommended_if": [],
  "recommended_combination": []
}

Provide meaningful context for suitability decisions.
Avoid simple yes/no phrases.

Rules:
- Describe prerequisites with reasoning
- Explain WHY certain conditions make this unsuitable
- Suggest combinations that enhance effectiveness with explanation'''
    
    def __init__(self):
        super().__init__("selection", self.SCHEMA_PROMPT)


def selection_agent_node(state: MobilityResearchState) -> dict:
    agent = SelectionAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    return {"selection": result, "errors": [error]} if error else {"selection": result, "errors": []}


# ============================================================================
# AGENT 19: FUTURE SCALABILITY
# ============================================================================

class ScalabilityAgent(BaseMobilityAgent):
    SCHEMA_PROMPT = '''Generate ONLY:

{
  "conditions_for_expansion": [],
  "extensions": []
}

Explain what conditions signal demand growth or operational expansion.
Give realistic extensions.

Rules:
- Describe indicators that would justify expansion
- Explain HOW extensions would build on initial implementation
- Provide context on timing, demand thresholds, or enabling factors'''
    
    def __init__(self):
        super().__init__("scalability", self.SCHEMA_PROMPT)


def scalability_agent_node(state: MobilityResearchState) -> dict:
    agent = ScalabilityAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    return {"scalability": result, "errors": [error]} if error else {"scalability": result, "errors": []}
