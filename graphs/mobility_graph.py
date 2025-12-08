"""
Multi-agent orchestration graph for mobility measure research.

This graph coordinates execution of all 19 specialized agents in parallel,
then combines their outputs into a complete mobility measure JSON document.
"""

from langgraph.graph import StateGraph, START, END
from schemas.mobility_measure import MobilityResearchState
from agents.mobility.meta_agent import meta_agent_node
from agents.mobility.overview_agent import overview_agent_node
from agents.mobility.context_agent import context_agent_node
from agents.mobility.all_agents import (
    evidence_agent_node,
    impact_agent_node,
    requirements_agent_node,
    infrastructure_agent_node,
    operations_agent_node,
    costs_agent_node,
    risks_agent_node,
    monitoring_agent_node,
    checklist_agent_node,
    lifecycle_agent_node,
    roles_agent_node,
    financial_agent_node,
    compliance_agent_node,
    visibility_agent_node,
    selection_agent_node,
    scalability_agent_node,
)
from agents.mobility.assembly_agent import assembly_agent_node
from utils.logger import logger


def create_mobility_graph():
    """
    Create and compile the multi-agent mobility research workflow.
    
    Architecture:
    - All 19 agents execute in parallel from START
    - All agents feed their outputs to assembly_agent
    - Assembly validates, merges, and saves complete JSON
    - Workflow ends at END
    
    Returns:
        Compiled LangGraph workflow
    """
    logger.info("Building mobility research graph...")
    
    # Create workflow with MobilityResearchState schema
    workflow = StateGraph(MobilityResearchState)
    
    # Add all 19 specialized agent nodes
    workflow.add_node("meta_agent", meta_agent_node)
    workflow.add_node("overview_agent", overview_agent_node)
    workflow.add_node("context_agent", context_agent_node)
    workflow.add_node("evidence_agent", evidence_agent_node)
    workflow.add_node("impact_agent", impact_agent_node)
    workflow.add_node("requirements_agent", requirements_agent_node)
    workflow.add_node("infrastructure_agent", infrastructure_agent_node)
    workflow.add_node("operations_agent", operations_agent_node)
    workflow.add_node("costs_agent", costs_agent_node)
    workflow.add_node("risks_agent", risks_agent_node)
    workflow.add_node("monitoring_agent", monitoring_agent_node)
    workflow.add_node("checklist_agent", checklist_agent_node)
    workflow.add_node("lifecycle_agent", lifecycle_agent_node)
    workflow.add_node("roles_agent", roles_agent_node)
    workflow.add_node("financial_agent", financial_agent_node)
    workflow.add_node("compliance_agent", compliance_agent_node)
    workflow.add_node("visibility_agent", visibility_agent_node)
    workflow.add_node("selection_agent", selection_agent_node)
    workflow.add_node("scalability_agent", scalability_agent_node)
    
    # Add assembly node
    workflow.add_node("assembly", assembly_agent_node)
    
    # All agents execute in parallel from START
    agent_names = [
        "meta_agent", "overview_agent", "context_agent", "evidence_agent",
        "impact_agent", "requirements_agent", "infrastructure_agent",
        "operations_agent", "costs_agent", "risks_agent", "monitoring_agent",
        "checklist_agent", "lifecycle_agent", "roles_agent", "financial_agent",
        "compliance_agent", "visibility_agent", "selection_agent", "scalability_agent"
    ]
    
    for agent_name in agent_names:
        workflow.add_edge(START, agent_name)
    
    # All agents converge to assembly
    for agent_name in agent_names:
        workflow.add_edge(agent_name, "assembly")
    
    # Assembly to END
    workflow.add_edge("assembly", END)
    
    # Compile the graph
    graph = workflow.compile()
    
    logger.info(f"✓ Mobility graph compiled with {len(agent_names)} agents")
    logger.info("✓ Agents will execute in parallel")
    
    return graph


# Create the compiled graph instance
mobility_graph = create_mobility_graph()
