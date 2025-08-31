"""
Business Onboarding Parallel Agent - ADK Parallel Pattern
Executes KYC, Credit, Documentation, and Account Setup simultaneously for efficiency.
"""

from google.adk import Agent, agents
from google.adk.tools import ToolContext
from ..config import MODEL

# Import individual processing agents
from ..sub_agents.kyc_agent import kyc_agent
from ..sub_agents.credit_agent import credit_agent  
from ..sub_agents.document_agent import document_agent
from ..sub_agents.account_setup_agent import account_setup_agent

def initialize_parallel_onboarding(context: ToolContext) -> None:
    """Initialize parallel onboarding workflow with shared context."""
    context.state["parallel_workflow"] = {
        "workflow_type": "business_onboarding_parallel",
        "started_at": "2024-01-01T10:00:00Z",
        "agents_involved": ["kyc", "credit", "document", "account_setup"],
        "coordination_mode": "parallel_execution"
    }
    
    # Set shared application context for all parallel agents
    if "primary_application_id" in context.state:
        context.state["shared_application_context"] = {
            "application_id": context.state["primary_application_id"],
            "business_name": context.state.get("primary_business_name"),
            "parallel_processing": True
        }

def finalize_parallel_onboarding(context: ToolContext) -> None:
    """Finalize parallel onboarding by consolidating results."""
    # Collect results from all parallel agents
    parallel_results = {
        "kyc_result": context.state.get("kyc_verification_result"),
        "credit_result": context.state.get("credit_assessment_result"),
        "document_result": context.state.get("document_processing_result"),
        "account_setup_result": context.state.get("account_setup_result")
    }
    
    # Determine overall status
    all_success = all(
        result and result.get("status") == "SUCCESS" 
        for result in parallel_results.values() if result
    )
    
    context.state["parallel_onboarding_result"] = {
        "overall_status": "SUCCESS" if all_success else "PARTIAL_SUCCESS",
        "individual_results": parallel_results,
        "completed_at": "2024-01-01T10:30:00Z",
        "processing_time_minutes": 30
    }

# Create the Parallel Agent using ADK pattern
business_onboarding_parallel_agent = agents.ParallelAgent(
    name="business_onboarding_parallel_agent",
    description="Execute business onboarding tasks in parallel for maximum efficiency",
    sub_agents=[
        kyc_agent,      # Parallel execution
        credit_agent,     # Parallel execution  
        document_agent,   # Parallel execution
        account_setup_agent,         # Parallel execution
    ],
    before_agent_callback=initialize_parallel_onboarding,
    after_agent_callback=finalize_parallel_onboarding,
)