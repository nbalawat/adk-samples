"""
Memory and context management tools for commercial banking onboarding.
Based on wealth management patterns for maintaining conversation continuity.
"""

from typing import Dict, Any, Optional, List
from google.adk.tools import ToolContext
import json
import datetime

def remember_application(application_id: str, business_name: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Remember the primary application ID and business name for future interactions.
    
    Args:
        application_id: Unique application identifier
        business_name: Legal business name
        tool_context: ADK tool context for state management
    
    Returns:
        Dict with success status and stored information
    """
    try:
        # Store primary application context
        tool_context.state["primary_application_id"] = application_id
        tool_context.state["primary_business_name"] = business_name
        tool_context.state["last_application_accessed"] = application_id
        tool_context.state["context_timestamp"] = datetime.datetime.now().isoformat()
        
        # Initialize application memory if not exists
        if "application_memory" not in tool_context.state:
            tool_context.state["application_memory"] = {}
        
        tool_context.state["application_memory"][application_id] = {
            "business_name": business_name,
            "first_accessed": datetime.datetime.now().isoformat(),
            "access_count": 1,
            "context_type": "primary_application"
        }
        
        return {
            "status": "SUCCESS",
            "message": f"I'll remember application {application_id} for {business_name} throughout our conversation",
            "application_id": application_id,
            "business_name": business_name,
            "stored_context": ["application_id", "business_name", "access_timestamp"]
        }
        
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Failed to store application context: {str(e)}"
        }

def store_business_context(context_type: str, context_data: Dict[str, Any], tool_context: ToolContext) -> Dict[str, Any]:
    """
    Store business-specific context for seamless experience across interactions.
    
    Args:
        context_type: Type of context (entity_info, beneficial_owners, documents, etc.)
        context_data: The context data to store
        tool_context: ADK tool context for state management
    
    Returns:
        Dict with success status and context information
    """
    try:
        # Initialize business context storage
        if "business_context" not in tool_context.state:
            tool_context.state["business_context"] = {}
        
        # Store the context with timestamp
        tool_context.state["business_context"][context_type] = {
            "data": context_data,
            "timestamp": datetime.datetime.now().isoformat(),
            "context_version": 1
        }
        
        # Update context summary
        if "context_summary" not in tool_context.state:
            tool_context.state["context_summary"] = []
            
        tool_context.state["context_summary"].append({
            "type": context_type,
            "stored_at": datetime.datetime.now().isoformat(),
            "data_keys": list(context_data.keys()) if isinstance(context_data, dict) else ["non_dict_data"]
        })
        
        return {
            "status": "SUCCESS",
            "message": f"Stored {context_type} context with {len(context_data)} data elements" if isinstance(context_data, dict) else f"Stored {context_type} context",
            "context_type": context_type,
            "data_elements": len(context_data) if isinstance(context_data, dict) else 1,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "ERROR", 
            "message": f"Failed to store business context: {str(e)}"
        }

def retrieve_application_status(application_id: Optional[str] = None, tool_context: ToolContext = None) -> Dict[str, Any]:
    """
    Retrieve current application status and context without re-processing.
    
    Args:
        application_id: Optional specific application ID (uses remembered ID if not provided)
        tool_context: ADK tool context for state access
    
    Returns:
        Dict with application status and context information
    """
    try:
        # Use remembered application ID if not provided
        if not application_id:
            application_id = tool_context.state.get("primary_application_id")
            
        if not application_id:
            return {
                "status": "ERROR",
                "message": "No application ID provided or remembered"
            }
        
        # Retrieve application memory
        application_memory = tool_context.state.get("application_memory", {})
        business_context = tool_context.state.get("business_context", {})
        
        if application_id not in application_memory:
            return {
                "status": "ERROR",
                "message": f"No memory found for application {application_id}"
            }
        
        # Build comprehensive status response
        app_info = application_memory[application_id]
        
        # Mock current status (in real implementation, would query actual status)
        current_status = {
            "application_id": application_id,
            "business_name": app_info["business_name"],
            "current_stage": "document_collection",
            "progress_percentage": 45,
            "next_steps": ["Complete beneficial owner information", "Submit financial statements"],
            "estimated_completion": "5-7 business days",
            "last_update": datetime.datetime.now().isoformat()
        }
        
        # Include available context
        available_context = list(business_context.keys())
        
        return {
            "status": "SUCCESS",
            "application_status": current_status,
            "available_context": available_context,
            "memory_info": {
                "first_accessed": app_info["first_accessed"],
                "access_count": app_info.get("access_count", 1),
                "context_elements": len(available_context)
            }
        }
        
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Failed to retrieve application status: {str(e)}"
        }

def update_workflow_progress(stage: str, progress_data: Dict[str, Any], tool_context: ToolContext) -> Dict[str, Any]:
    """
    Update workflow progress and maintain state for ongoing coordination.
    
    Args:
        stage: Current workflow stage
        progress_data: Progress information and next steps
        tool_context: ADK tool context for state management
    
    Returns:
        Dict with updated progress information
    """
    try:
        # Initialize workflow progress tracking
        if "workflow_progress" not in tool_context.state:
            tool_context.state["workflow_progress"] = {
                "stages_completed": [],
                "current_stage": None,
                "progress_history": [],
                "estimated_completion": None
            }
        
        # Update current stage
        previous_stage = tool_context.state["workflow_progress"]["current_stage"]
        tool_context.state["workflow_progress"]["current_stage"] = stage
        
        # Add to completed stages if moving forward
        if previous_stage and previous_stage not in tool_context.state["workflow_progress"]["stages_completed"]:
            tool_context.state["workflow_progress"]["stages_completed"].append(previous_stage)
        
        # Add progress history entry
        progress_entry = {
            "stage": stage,
            "timestamp": datetime.datetime.now().isoformat(),
            "progress_data": progress_data,
            "previous_stage": previous_stage
        }
        
        tool_context.state["workflow_progress"]["progress_history"].append(progress_entry)
        
        # Calculate overall progress
        stage_order = [
            "application_created", "document_collection", "kyc_verification", 
            "credit_assessment", "compliance_review", "final_approval", 
            "account_setup", "onboarding_complete"
        ]
        
        try:
            current_index = stage_order.index(stage)
            overall_progress = ((current_index + 1) / len(stage_order)) * 100
        except ValueError:
            overall_progress = 50  # Default if stage not in standard order
        
        return {
            "status": "SUCCESS",
            "current_stage": stage,
            "previous_stage": previous_stage,
            "overall_progress": overall_progress,
            "stages_completed": tool_context.state["workflow_progress"]["stages_completed"],
            "progress_data": progress_data,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Failed to update workflow progress: {str(e)}"
        }

def get_conversation_context(context_type: Optional[str] = None, tool_context: ToolContext = None) -> Dict[str, Any]:
    """
    Retrieve conversation context for continuity across interactions.
    
    Args:
        context_type: Specific type of context to retrieve (optional, returns all if None)
        tool_context: ADK tool context for state access
    
    Returns:
        Dict with requested context information
    """
    try:
        if context_type:
            # Return specific context type
            business_context = tool_context.state.get("business_context", {})
            if context_type in business_context:
                return {
                    "status": "SUCCESS",
                    "context_type": context_type,
                    "context_data": business_context[context_type]["data"],
                    "timestamp": business_context[context_type]["timestamp"]
                }
            else:
                return {
                    "status": "NOT_FOUND",
                    "message": f"No context found for type: {context_type}",
                    "available_types": list(business_context.keys())
                }
        else:
            # Return all available context
            return {
                "status": "SUCCESS",
                "primary_application": tool_context.state.get("primary_application_id"),
                "business_name": tool_context.state.get("primary_business_name"),
                "business_context": tool_context.state.get("business_context", {}),
                "workflow_progress": tool_context.state.get("workflow_progress", {}),
                "context_summary": tool_context.state.get("context_summary", [])
            }
            
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Failed to retrieve conversation context: {str(e)}"
        }

def clear_application_context(application_id: Optional[str] = None, tool_context: ToolContext = None) -> Dict[str, Any]:
    """
    Clear application context (typically used when application is completed).
    
    Args:
        application_id: Specific application to clear (clears primary if None)
        tool_context: ADK tool context for state management
    
    Returns:
        Dict with success status and cleared information
    """
    try:
        if not application_id:
            application_id = tool_context.state.get("primary_application_id")
            
        if not application_id:
            return {
                "status": "ERROR",
                "message": "No application ID provided or remembered"
            }
        
        # Clear application memory
        application_memory = tool_context.state.get("application_memory", {})
        if application_id in application_memory:
            del application_memory[application_id]
        
        # Clear primary application if it matches
        if tool_context.state.get("primary_application_id") == application_id:
            tool_context.state.pop("primary_application_id", None)
            tool_context.state.pop("primary_business_name", None)
            tool_context.state.pop("business_context", None)
            tool_context.state.pop("workflow_progress", None)
        
        return {
            "status": "SUCCESS",
            "message": f"Cleared context for application {application_id}",
            "application_id": application_id,
            "cleared_timestamp": datetime.datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Failed to clear application context: {str(e)}"
        }