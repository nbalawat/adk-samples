"""Tools for the orchestrator agent to manage onboarding workflow."""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

# Tools are automatically converted when added to agent
from ..shared_libraries.types import (
    OnboardingApplication, OnboardingStatus, BusinessInfo, 
    BeneficialOwner, DocumentInfo, OnboardingDecision
)
from ..shared_libraries.utils import generate_application_id, create_audit_entry

logger = logging.getLogger(__name__)


# Function automatically becomes a tool when added to agent
def create_onboarding_application(
    business_info: Dict[str, Any],
    beneficial_owners: List[Dict[str, Any]],
    documents: List[Dict[str, Any]] = []
) -> Dict[str, Any]:
    """
    Create a new commercial banking onboarding application.
    
    Args:
        business_info: Business information including legal name, entity type, etc.
        beneficial_owners: List of beneficial owners with their information
        documents: List of uploaded documents (optional)
    
    Returns:
        Dict containing the created application with application ID
    """
    try:
        # Generate unique application ID
        app_id = generate_application_id()
        
        # Create application object
        application = OnboardingApplication(
            application_id=app_id,
            business_info=BusinessInfo(**business_info),
            beneficial_owners=[BeneficialOwner(**owner) for owner in beneficial_owners],
            documents=[DocumentInfo(**doc) for doc in documents],
            status=OnboardingStatus.INITIATED
        )
        
        # Log application creation
        audit_entry = create_audit_entry(
            action="application_created",
            user_id="system",
            details={
                "application_id": app_id,
                "business_name": business_info.get("legal_name"),
                "entity_type": business_info.get("entity_type")
            }
        )
        
        logger.info(f"Created onboarding application {app_id} for {business_info.get('legal_name')}")
        
        return {
            "application_id": app_id,
            "status": "created",
            "application": application.model_dump(),
            "audit_entry": audit_entry
        }
        
    except Exception as e:
        logger.error(f"Error creating onboarding application: {str(e)}")
        return {
            "error": f"Failed to create application: {str(e)}",
            "status": "failed"
        }


# Function automatically becomes a tool when added to agent
def update_application_status(
    application_id: str,
    new_status: str,
    notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update the status of an onboarding application.
    
    Args:
        application_id: Unique application identifier
        new_status: New status to set
        notes: Optional notes about the status change
    
    Returns:
        Dict with update confirmation
    """
    try:
        # Validate status
        valid_statuses = [status.value for status in OnboardingStatus]
        if new_status not in valid_statuses:
            return {
                "error": f"Invalid status: {new_status}. Valid statuses: {valid_statuses}",
                "status": "failed"
            }
        
        # Create audit entry
        audit_entry = create_audit_entry(
            action="status_updated",
            user_id="system", 
            details={
                "application_id": application_id,
                "new_status": new_status,
                "notes": notes
            }
        )
        
        logger.info(f"Updated application {application_id} status to {new_status}")
        
        return {
            "application_id": application_id,
            "status": "updated",
            "new_status": new_status,
            "timestamp": datetime.now().isoformat(),
            "audit_entry": audit_entry
        }
        
    except Exception as e:
        logger.error(f"Error updating application status: {str(e)}")
        return {
            "error": f"Failed to update status: {str(e)}",
            "status": "failed"
        }


# Function automatically becomes a tool when added to agent
def get_application_status(application_id: str) -> Dict[str, Any]:
    """
    Get the current status and details of an onboarding application.
    
    Args:
        application_id: Unique application identifier
    
    Returns:
        Dict with application status and progress information
    """
    try:
        # In a real implementation, this would query a database
        # For demo purposes, return a simulated status
        
        status_progression = [
            OnboardingStatus.INITIATED,
            OnboardingStatus.DOCUMENTS_RECEIVED,
            OnboardingStatus.KYC_IN_PROGRESS,
            OnboardingStatus.KYC_COMPLETED,
            OnboardingStatus.CREDIT_ASSESSMENT,
            OnboardingStatus.COMPLIANCE_SCREENING,
            OnboardingStatus.ACCOUNT_SETUP,
            OnboardingStatus.COMPLETED
        ]
        
        # Simulate current status (in real app, would be from database)
        import random
        current_status = random.choice(status_progression[:4])  # Random status for demo
        
        # Calculate progress percentage
        if current_status in status_progression:
            progress = (status_progression.index(current_status) + 1) / len(status_progression) * 100
        else:
            progress = 0
        
        return {
            "application_id": application_id,
            "current_status": current_status.value,
            "progress_percentage": round(progress, 1),
            "last_updated": datetime.now().isoformat(),
            "next_steps": get_next_steps(current_status),
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error getting application status: {str(e)}")
        return {
            "error": f"Failed to get status: {str(e)}",
            "status": "failed"
        }


# Function automatically becomes a tool when added to agent
def route_to_specialist_agent(
    application_id: str,
    agent_type: str,
    task_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Route task to appropriate specialist agent.
    
    Args:
        application_id: Unique application identifier
        agent_type: Type of agent (kyc, credit, compliance, document, account_setup)
        task_data: Data needed for the specialist agent
    
    Returns:
        Dict with routing confirmation and task ID
    """
    try:
        valid_agents = ["kyc", "credit", "compliance", "document", "account_setup"]
        
        if agent_type not in valid_agents:
            return {
                "error": f"Invalid agent type: {agent_type}. Valid types: {valid_agents}",
                "status": "failed"
            }
        
        # Generate task ID
        task_id = f"{agent_type}-{application_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create audit entry
        audit_entry = create_audit_entry(
            action="task_routed",
            user_id="system",
            details={
                "application_id": application_id,
                "agent_type": agent_type,
                "task_id": task_id
            }
        )
        
        logger.info(f"Routed task {task_id} to {agent_type} agent for application {application_id}")
        
        return {
            "task_id": task_id,
            "agent_type": agent_type,
            "application_id": application_id,
            "status": "routed",
            "estimated_completion": "2-4 hours",  # Simulated
            "audit_entry": audit_entry
        }
        
    except Exception as e:
        logger.error(f"Error routing to specialist agent: {str(e)}")
        return {
            "error": f"Failed to route task: {str(e)}",
            "status": "failed"
        }


# Function automatically becomes a tool when added to agent
def make_onboarding_decision(
    application_id: str,
    decision: str,
    decision_factors: List[str],
    conditions: List[str] = [],
    account_types: List[str] = []
) -> Dict[str, Any]:
    """
    Make final onboarding decision for an application.
    
    Args:
        application_id: Unique application identifier
        decision: Final decision (approved, rejected, manual_review)
        decision_factors: Key factors that influenced the decision
        conditions: Any conditions for approval
        account_types: Types of accounts to create if approved
    
    Returns:
        Dict with decision details and next steps
    """
    try:
        valid_decisions = ["approved", "rejected", "manual_review"]
        
        if decision not in valid_decisions:
            return {
                "error": f"Invalid decision: {decision}. Valid decisions: {valid_decisions}",
                "status": "failed"
            }
        
        # Create decision object
        onboarding_decision = OnboardingDecision(
            application_id=application_id,
            decision=decision,
            decision_factors=decision_factors,
            conditions=conditions
        )
        
        # If approved, generate account numbers
        if decision == "approved":
            from ..shared_libraries.utils import generate_account_number
            
            account_numbers = {}
            for account_type in account_types:
                account_numbers[account_type] = generate_account_number(account_type)
            
            onboarding_decision.account_numbers = account_numbers
        
        # Set next steps based on decision
        if decision == "approved":
            next_steps = [
                "Account setup in progress",
                "Welcome package will be sent",
                "Online banking credentials will be provided",
                "Relationship manager will contact within 2 business days"
            ]
        elif decision == "rejected":
            next_steps = [
                "Rejection notice will be sent",
                "Adverse action notice provided if applicable",
                "Customer can reapply after addressing issues"
            ]
        else:  # manual_review
            next_steps = [
                "Application escalated to manual review",
                "Additional documentation may be requested",
                "Decision expected within 5-7 business days"
            ]
        
        onboarding_decision.next_steps = next_steps
        
        # Create audit entry
        audit_entry = create_audit_entry(
            action="decision_made",
            user_id="system",
            details={
                "application_id": application_id,
                "decision": decision,
                "decision_factors": decision_factors
            }
        )
        
        logger.info(f"Made onboarding decision for application {application_id}: {decision}")
        
        return {
            "application_id": application_id,
            "decision": onboarding_decision.model_dump(),
            "status": "completed",
            "audit_entry": audit_entry
        }
        
    except Exception as e:
        logger.error(f"Error making onboarding decision: {str(e)}")
        return {
            "error": f"Failed to make decision: {str(e)}",
            "status": "failed"
        }


def get_next_steps(current_status: OnboardingStatus) -> List[str]:
    """Get next steps based on current status."""
    next_steps_map = {
        OnboardingStatus.INITIATED: [
            "Upload required business documents",
            "Provide beneficial ownership information",
            "Complete business information form"
        ],
        OnboardingStatus.DOCUMENTS_RECEIVED: [
            "Document processing and validation in progress",
            "KYC verification will begin shortly"
        ],
        OnboardingStatus.KYC_IN_PROGRESS: [
            "Identity verification in progress",
            "Background checks being performed"
        ],
        OnboardingStatus.KYC_COMPLETED: [
            "Credit assessment in progress",
            "Financial analysis being performed"
        ],
        OnboardingStatus.CREDIT_ASSESSMENT: [
            "Compliance screening in progress",
            "AML and sanctions checks being performed"
        ],
        OnboardingStatus.COMPLIANCE_SCREENING: [
            "Final review in progress",
            "Account setup preparation"
        ],
        OnboardingStatus.ACCOUNT_SETUP: [
            "Accounts being created",
            "Banking services being configured"
        ],
        OnboardingStatus.COMPLETED: [
            "Onboarding complete",
            "Welcome materials sent",
            "Relationship manager assigned"
        ]
    }
    
    return next_steps_map.get(current_status, ["Status update in progress"])