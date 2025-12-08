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

Rules:
- Use general validated patterns, not fabricated claims.
- 1–3 lines per field.'''
    
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

Use qualitative or range-based values.'''
    
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
}'''
    
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
}'''
    
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
}'''
    
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

Values for upfront and operational must be qualitative ("low", "medium", "high").'''
    
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

No more than 3 risks.'''
    
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

Rules:
- 3–6 metrics max.
- Frequency should be "quarterly", "annual", etc.'''
    
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

Each list = 3–6 steps.'''
    
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

2–5 items per stage.'''
    
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
}'''
    
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

Rules:
- Use qualitative/semi-quantitative values.
- incentives: 1–3 items max.'''
    
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
}'''
    
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
}'''
    
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
}'''
    
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
}'''
    
    def __init__(self):
        super().__init__("scalability", self.SCHEMA_PROMPT)


def scalability_agent_node(state: MobilityResearchState) -> dict:
    agent = ScalabilityAgent()
    result, error = agent.generate(state["measure_name"], state.get("context", ""))
    return {"scalability": result, "errors": [error]} if error else {"scalability": result, "errors": []}
