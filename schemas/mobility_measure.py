"""
Complete JSON schema definitions for mobility measures.

This module defines the TypedDict schemas for all sections of a mobility measure.
Each section corresponds to one specialized agent's output.
"""

from typing import TypedDict, List, Literal, Annotated
from datetime import datetime
import operator


# ============================================================================
# SECTION SCHEMAS (Each corresponds to one agent)
# ============================================================================

class MobilityMeasureMeta(TypedDict):
    """Meta information about the mobility measure."""
    name: str
    short_description: str  # Max 20-25 words
    category: str
    tags: List[str]  # 3-7 lowercase keywords
    status: Literal["active", "draft", "archived"]
    last_updated: str  # ISO 8601 timestamp
    images: List[str]  # URLs or paths
    impact_level: int  # 1-5
    cost_level: int  # 1-5


class MobilityMeasureOverview(TypedDict):
    """Overview and behavioural goals."""
    description: str  # 2-3 sentences max
    behavioural_primary: str  # One clear behavioural goal
    behavioural_secondary: List[str]  # 2-4 supporting behaviours


class MobilityMeasureContext(TypedDict):
    """Context and applicability."""
    target_users: List[str]  # Short descriptors (max 8 words each)
    suitable_strong: List[str]  # Where it works well
    suitable_weak: List[str]  # Where it doesn't work well


class MobilityMeasureEvidence(TypedDict):
    """Evidence and research support."""
    sweden: List[str]  # Swedish examples
    europe: List[str]  # European examples
    research: List[str]  # Research findings
    behavioural: List[str]  # Behavioural insights


class MobilityMeasureImpact(TypedDict):
    """Expected impacts."""
    car_ownership_reduction: str
    modal_shift: str
    parking_reduction: str
    satisfaction: str
    congestion_reduction: str
    long_distance_support: str
    other: str


class MobilityMeasureRequirements(TypedDict):
    """Requirements for implementation."""
    security: List[str]
    infrastructure: List[str]
    charging: List[str]
    accessibility: List[str]
    information: List[str]
    quality_standards: List[str]


class MobilityMeasureInfrastructure(TypedDict):
    """Infrastructure specifications."""
    key_requirements: List[str]
    power_requirements: List[str]
    weather_protection: List[str]
    placement_rules: List[str]
    notes: str


class MobilityMeasureOperations(TypedDict):
    """Operations and phases."""
    developer: List[str]
    housing_association: List[str]
    mobility_provider: List[str]
    city: List[str]
    operations_phases: "OperationsPhases"


class OperationsPhases(TypedDict):
    """Detailed operations phases."""
    installation: List[str]
    maintenance: List[str]
    data_reporting: List[str]
    upgrades: List[str]


class MobilityMeasureCosts(TypedDict):
    """Cost information."""
    upfront: str  # Qualitative: "low", "medium", "high"
    operational: str  # Qualitative: "low", "medium", "high"
    benefits: List[str]


class MobilityMeasureRisks(TypedDict):
    """Top risks (max 3)."""
    risk_1: str
    risk_2: str
    risk_3: str


class MobilityMeasureMonitoring(TypedDict):
    """Monitoring approach."""
    metrics: List[str]  # 3-6 metrics
    frequency: str  # "quarterly", "annual", etc.


class MobilityMeasureChecklist(TypedDict):
    """Implementation checklist."""
    before_move_in: List[str]  # 3-6 steps
    at_move_in: List[str]  # 3-6 steps
    after_move_in: List[str]  # 3-6 steps


class MobilityMeasureLifecycle(TypedDict):
    """Development lifecycle stages."""
    stage_1_land_allocation: List[str]  # 2-5 items
    stage_2_detailed_planning: List[str]  # 2-5 items
    stage_3_construction: List[str]  # 2-5 items
    stage_4_pre_occupancy: List[str]  # 2-5 items
    stage_5_operation_year_1: List[str]  # 2-5 items
    stage_6_long_term: List[str]  # 2-5 items


class StakeholderRole(TypedDict):
    """Role definition for a stakeholder."""
    financial: List[str]
    technical: List[str]
    handover: List[str]


class HousingAssociationRole(TypedDict):
    """Housing association responsibilities."""
    financial: List[str]
    operation: List[str]
    issue_resolution: List[str]


class MobilityProviderRole(TypedDict):
    """Mobility provider responsibilities."""
    service_level: List[str]
    data: List[str]
    support: List[str]


class CityRole(TypedDict):
    """City/municipality responsibilities."""
    regulation: List[str]
    monitoring: List[str]


class MobilityMeasureRolesResponsibilitiesDetailed(TypedDict):
    """Roles and responsibilities."""
    developer: StakeholderRole
    housing_association: HousingAssociationRole
    mobility_provider: MobilityProviderRole
    city: CityRole


class CostDistribution(TypedDict):
    """Cost distribution by stakeholder."""
    developer: List[str]
    mobility_provider: List[str]
    housing_association: List[str]
    city: List[str]


class EstimatedCosts(TypedDict):
    """Estimated cost breakdowns."""
    installation_cost: str
    annual_maintenance: str
    electricity_cost: str


class Savings(TypedDict):
    """Potential savings."""
    parking_construction_reduction: str
    reduced_need_for_family_car_ownership: str


class MobilityMeasureFinancialModel(TypedDict):
    """Financial model."""
    cost_distribution: CostDistribution
    estimated_costs: EstimatedCosts
    savings: Savings
    incentives: List[str]  # 1-3 items max


class MobilityMeasureCompliance(TypedDict):
    """Compliance requirements."""
    minimum_requirements: List[str]
    documentation_required: List[str]
    approval_process: List[str]
    non_compliance_actions: List[str]


class MobilityMeasureVisibilityAndCommunicationDesign(TypedDict):
    """Visibility and communication."""
    signage: List[str]
    digital: List[str]
    physical_touchpoints: List[str]


class MobilityMeasureSelectionLogic(TypedDict):
    """Selection logic and recommendations."""
    requires: List[str]
    not_recommended_if: List[str]
    recommended_combination: List[str]


class MobilityMeasureFutureScalability(TypedDict):
    """Future scalability."""
    conditions_for_expansion: List[str]
    extensions: List[str]


# ============================================================================
# COMPLETE MOBILITY MEASURE
# ============================================================================

class CompleteMobilityMeasure(TypedDict):
    """
    Complete mobility measure document combining all sections.
    This is the final output from the assembly agent.
    """
    meta: MobilityMeasureMeta
    overview: MobilityMeasureOverview
    context: MobilityMeasureContext
    evidence: MobilityMeasureEvidence
    impact: MobilityMeasureImpact
    requirements: MobilityMeasureRequirements
    infrastructure: MobilityMeasureInfrastructure
    operations: MobilityMeasureOperations
    costs: MobilityMeasureCosts
    risks: MobilityMeasureRisks
    monitoring: MobilityMeasureMonitoring
    checklist: MobilityMeasureChecklist
    lifecycle: MobilityMeasureLifecycle
    roles_responsibilities_detailed: MobilityMeasureRolesResponsibilitiesDetailed
    financial_model: MobilityMeasureFinancialModel
    compliance: MobilityMeasureCompliance
    visibility_and_communication_design: MobilityMeasureVisibilityAndCommunicationDesign
    selection_logic: MobilityMeasureSelectionLogic
    future_scalability: MobilityMeasureFutureScalability


# ============================================================================
# LANGGRAPH STATE (for multi-agent workflow)
# ============================================================================

class MobilityResearchState(TypedDict):
    """
    State for the LangGraph multi-agent workflow.
    
    Workflow:
    1. User provides measure_name and optional context
    2. All 19 agents execute in parallel
    3. Assembly agent combines results
    4. Output saved to research_output/{name}-mobility-measure.json
    """
    # Input
    measure_name: str
    context: str
    
    # Agent results (19 sections)
    meta: MobilityMeasureMeta
    overview: MobilityMeasureOverview
    context_data: MobilityMeasureContext
    evidence: MobilityMeasureEvidence
    impact: MobilityMeasureImpact
    requirements: MobilityMeasureRequirements
    infrastructure: MobilityMeasureInfrastructure
    operations: MobilityMeasureOperations
    costs: MobilityMeasureCosts
    risks: MobilityMeasureRisks
    monitoring: MobilityMeasureMonitoring
    checklist: MobilityMeasureChecklist
    lifecycle: MobilityMeasureLifecycle
    roles_responsibilities_detailed: MobilityMeasureRolesResponsibilitiesDetailed
    financial_model: MobilityMeasureFinancialModel
    compliance: MobilityMeasureCompliance
    visibility_and_communication_design: MobilityMeasureVisibilityAndCommunicationDesign
    selection_logic: MobilityMeasureSelectionLogic
    future_scalability: MobilityMeasureFutureScalability
    
    # Final output
    complete_measure: CompleteMobilityMeasure
    output_path: str  # Path to saved JSON file
    errors: Annotated[List[str], operator.add]  # Collect errors from all agents
