"""
Enhanced orchestrator tools for comprehensive commercial banking onboarding.
"""

from typing import Dict, Any, Optional, List
from google.adk.tools import ToolContext
import json
import uuid
import datetime

def create_onboarding_application(
    business_name: str,
    entity_type: str, 
    tax_id: str,
    business_address: str,
    beneficial_owners: List[Dict[str, Any]],
    requested_products: Optional[List[str]] = None,
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """
    Create a new comprehensive onboarding application with enhanced tracking.
    
    Args:
        business_name: Legal business name
        entity_type: Business entity type (LLC, Corporation, Partnership, etc.)
        tax_id: Federal tax identification number
        business_address: Primary business address
        beneficial_owners: List of beneficial owners with 25%+ ownership
        requested_products: List of requested banking products
        tool_context: ADK tool context for state management
    
    Returns:
        Dict with application details and unique identifier
    """
    try:
        # Generate unique application ID
        application_id = f"CBO-{datetime.datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        # Validate required information
        if not all([business_name, entity_type, tax_id, business_address]):
            return {
                "status": "ERROR",
                "message": "Missing required business information",
                "required_fields": ["business_name", "entity_type", "tax_id", "business_address"]
            }
        
        if not beneficial_owners:
            return {
                "status": "ERROR", 
                "message": "At least one beneficial owner is required"
            }
        
        # Create comprehensive application record
        application_data = {
            "application_id": application_id,
            "business_information": {
                "legal_name": business_name,
                "entity_type": entity_type,
                "tax_id": tax_id,
                "address": business_address,
                "industry": "To be determined",
                "years_in_business": "To be determined"
            },
            "beneficial_owners": beneficial_owners,
            "requested_products": requested_products or ["business_checking"],
            "application_status": {
                "current_stage": "application_created",
                "progress_percentage": 10,
                "created_at": datetime.datetime.now().isoformat(),
                "last_updated": datetime.datetime.now().isoformat(),
                "estimated_completion": "10-14 business days"
            },
            "workflow_tracking": {
                "stages_completed": [],
                "current_assignee": "operations_team",
                "priority_level": "standard",
                "sla_deadline": (datetime.datetime.now() + datetime.timedelta(days=14)).isoformat()
            }
        }
        
        # Store in context for tracking
        if tool_context:
            if "applications" not in tool_context.state:
                tool_context.state["applications"] = {}
            
            tool_context.state["applications"][application_id] = application_data
            tool_context.state["primary_application_id"] = application_id
            tool_context.state["primary_business_name"] = business_name
        
        return {
            "status": "SUCCESS",
            "message": f"Application {application_id} created successfully for {business_name}",
            "application_id": application_id,
            "application_data": application_data,
            "next_steps": [
                "Document collection and validation",
                "KYC verification process", 
                "Credit assessment initiation",
                "Compliance screening"
            ]
        }
        
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Failed to create application: {str(e)}"
        }

def update_application_status(
    application_id: str,
    new_status: str,
    status_details: Optional[Dict[str, Any]] = None,
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """
    Update application status with detailed tracking and notifications.
    """
    try:
        if not tool_context or "applications" not in tool_context.state:
            return {
                "status": "ERROR",
                "message": "No applications found in context"
            }
        
        if application_id not in tool_context.state["applications"]:
            return {
                "status": "ERROR",
                "message": f"Application {application_id} not found"
            }
        
        # Update application status
        application = tool_context.state["applications"][application_id]
        previous_status = application["application_status"]["current_stage"]
        
        application["application_status"].update({
            "current_stage": new_status,
            "last_updated": datetime.datetime.now().isoformat(),
            "previous_stage": previous_status,
            "status_details": status_details or {}
        })
        
        # Update progress percentage based on stage
        stage_progress = {
            "application_created": 10,
            "document_collection": 25,
            "kyc_verification": 40,
            "credit_assessment": 55,
            "compliance_review": 70,
            "final_approval": 85,
            "account_setup": 95,
            "onboarding_complete": 100
        }
        
        application["application_status"]["progress_percentage"] = stage_progress.get(new_status, 50)
        
        # Add to workflow tracking
        if previous_status not in application["workflow_tracking"]["stages_completed"]:
            application["workflow_tracking"]["stages_completed"].append(previous_status)
        
        return {
            "status": "SUCCESS",
            "message": f"Application {application_id} updated to {new_status}",
            "application_id": application_id,
            "previous_status": previous_status,
            "new_status": new_status,
            "progress_percentage": application["application_status"]["progress_percentage"],
            "status_details": status_details
        }
        
    except Exception as e:
        return {
            "status": "ERROR", 
            "message": f"Failed to update application status: {str(e)}"
        }

def get_application_status(
    application_id: Optional[str] = None,
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """
    Retrieve comprehensive application status and progress information.
    """
    try:
        # Use primary application if no ID provided
        if not application_id and tool_context:
            application_id = tool_context.state.get("primary_application_id")
        
        if not application_id:
            return {
                "status": "ERROR",
                "message": "No application ID provided"
            }
        
        if not tool_context or "applications" not in tool_context.state:
            return {
                "status": "ERROR",
                "message": "No applications found in context"
            }
        
        if application_id not in tool_context.state["applications"]:
            return {
                "status": "ERROR",
                "message": f"Application {application_id} not found"
            }
        
        application = tool_context.state["applications"][application_id]
        
        # Calculate time metrics
        created_at = datetime.datetime.fromisoformat(application["application_status"]["created_at"].replace('Z', '+00:00'))
        current_time = datetime.datetime.now(created_at.tzinfo)
        processing_days = (current_time - created_at).days
        
        return {
            "status": "SUCCESS",
            "application_id": application_id,
            "business_name": application["business_information"]["legal_name"],
            "current_stage": application["application_status"]["current_stage"],
            "progress_percentage": application["application_status"]["progress_percentage"],
            "processing_days": processing_days,
            "stages_completed": application["workflow_tracking"]["stages_completed"],
            "estimated_completion": application["application_status"]["estimated_completion"],
            "sla_status": "On Track" if processing_days < 10 else "At Risk",
            "next_steps": _get_next_steps(application["application_status"]["current_stage"]),
            "last_updated": application["application_status"]["last_updated"]
        }
        
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Failed to retrieve application status: {str(e)}"
        }

def _get_next_steps(current_stage: str) -> List[str]:
    """Get next steps based on current stage."""
    next_steps_map = {
        "application_created": [
            "Collect required business documentation",
            "Schedule initial KYC verification",
            "Begin document validation process"
        ],
        "document_collection": [
            "Complete KYC verification",
            "Initiate credit assessment",
            "Begin compliance screening"
        ],
        "kyc_verification": [
            "Finalize credit analysis",
            "Complete compliance review",
            "Prepare for approval decision"
        ],
        "credit_assessment": [
            "Complete remaining compliance checks",
            "Prepare approval documentation",
            "Schedule final review"
        ],
        "compliance_review": [
            "Final approval decision",
            "Account setup preparation",
            "Client notification"
        ],
        "final_approval": [
            "Account and product setup",
            "Client onboarding coordination",
            "Service activation"
        ],
        "account_setup": [
            "Final testing and verification",
            "Client training and handoff",
            "Relationship manager introduction"
        ],
        "onboarding_complete": [
            "Ongoing relationship management",
            "Regular account reviews",
            "Service optimization"
        ]
    }
    
    return next_steps_map.get(current_stage, ["Contact your relationship manager for next steps"])

def route_to_specialist_agent(
    agent_type: str,
    task_description: str,
    application_id: Optional[str] = None,
    task_data: Optional[Dict[str, Any]] = None,
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """
    Route specific tasks to specialist agents with proper context.
    """
    try:
        # Validate agent type
        valid_agents = [
            "kyc_verification", "credit_assessment", "compliance_screening",
            "document_processing", "account_setup", "risk_analysis"
        ]
        
        if agent_type not in valid_agents:
            return {
                "status": "ERROR",
                "message": f"Invalid agent type. Must be one of: {valid_agents}"
            }
        
        # Prepare routing information
        routing_info = {
            "agent_type": agent_type,
            "task_description": task_description,
            "application_id": application_id or tool_context.state.get("primary_application_id"),
            "task_data": task_data or {},
            "routed_at": datetime.datetime.now().isoformat(),
            "routing_id": str(uuid.uuid4())[:8].upper(),
            "priority": "standard",
            "expected_completion": "2-3 business days"
        }
        
        # Store routing information in context
        if tool_context:
            if "routing_history" not in tool_context.state:
                tool_context.state["routing_history"] = []
            
            tool_context.state["routing_history"].append(routing_info)
        
        return {
            "status": "SUCCESS",
            "message": f"Task routed to {agent_type} agent successfully",
            "routing_info": routing_info,
            "next_steps": [
                f"{agent_type} agent will process the request",
                "Status updates will be provided as work progresses", 
                "Results will be integrated into the main workflow"
            ]
        }
        
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Failed to route to specialist agent: {str(e)}"
        }

def make_onboarding_decision(
    application_id: str,
    decision: str,
    decision_rationale: str,
    conditions: Optional[List[str]] = None,
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """
    Make final onboarding approval decision with comprehensive documentation.
    """
    try:
        valid_decisions = ["APPROVED", "REJECTED", "MANUAL_REVIEW", "CONDITIONAL_APPROVAL"]
        
        if decision not in valid_decisions:
            return {
                "status": "ERROR",
                "message": f"Invalid decision. Must be one of: {valid_decisions}"
            }
        
        if not application_id and tool_context:
            application_id = tool_context.state.get("primary_application_id")
        
        if not application_id:
            return {
                "status": "ERROR",
                "message": "No application ID provided"
            }
        
        # Create decision record
        decision_record = {
            "application_id": application_id,
            "decision": decision,
            "decision_rationale": decision_rationale,
            "conditions": conditions or [],
            "decided_at": datetime.datetime.now().isoformat(),
            "decided_by": "enhanced_commercial_banking_orchestrator",
            "decision_id": str(uuid.uuid4())[:8].upper()
        }
        
        # Update application status based on decision
        if decision == "APPROVED":
            new_status = "final_approval"
        elif decision == "REJECTED":
            new_status = "application_rejected"  
        elif decision == "MANUAL_REVIEW":
            new_status = "manual_review_required"
        else:  # CONDITIONAL_APPROVAL
            new_status = "conditional_approval"
        
        # Update application status
        status_update = update_application_status(
            application_id, new_status, 
            {"decision_record": decision_record}, 
            tool_context
        )
        
        # Store decision in context
        if tool_context:
            if "decisions" not in tool_context.state:
                tool_context.state["decisions"] = {}
            
            tool_context.state["decisions"][application_id] = decision_record
        
        return {
            "status": "SUCCESS",
            "message": f"Onboarding decision recorded: {decision}",
            "decision_record": decision_record,
            "status_update": status_update,
            "next_steps": _get_decision_next_steps(decision)
        }
        
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Failed to record onboarding decision: {str(e)}"
        }

def _get_decision_next_steps(decision: str) -> List[str]:
    """Get next steps based on decision."""
    steps_map = {
        "APPROVED": [
            "Begin account setup process",
            "Configure requested banking products",
            "Schedule client onboarding session",
            "Prepare welcome materials"
        ],
        "REJECTED": [
            "Prepare rejection notification",
            "Document rejection reasons",
            "Provide appeal process information",
            "Close application file"
        ],
        "MANUAL_REVIEW": [
            "Route to senior underwriter",
            "Schedule review committee meeting", 
            "Prepare comprehensive case analysis",
            "Set review timeline expectations"
        ],
        "CONDITIONAL_APPROVAL": [
            "Communicate approval conditions to client",
            "Set up condition tracking",
            "Begin conditional account setup",
            "Schedule condition review milestones"
        ]
    }
    
    return steps_map.get(decision, ["Contact operations team for guidance"])