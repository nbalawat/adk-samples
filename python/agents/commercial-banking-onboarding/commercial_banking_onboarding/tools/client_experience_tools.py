"""
Client experience tools for enhanced commercial banking onboarding.
Focused on client-facing interactions, communication, and service delivery.
"""

from typing import Dict, Any, Optional, List
from google.adk.tools import ToolContext
import datetime
import json

def create_client_portal_access(
    application_id: str,
    business_name: str,
    primary_contact_email: str,
    contact_name: str,
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    Create secure client portal access for application tracking and communication.
    
    Args:
        application_id: Unique application identifier
        business_name: Legal business name
        primary_contact_email: Primary contact email address
        contact_name: Name of primary contact person
        tool_context: ADK tool context for state management
    
    Returns:
        Dict with portal access information and credentials
    """
    try:
        # Generate secure portal credentials (in production, use proper auth)
        portal_access = {
            "portal_id": f"PORTAL-{application_id}",
            "business_name": business_name,
            "primary_contact": {
                "name": contact_name,
                "email": primary_contact_email
            },
            "access_credentials": {
                "username": primary_contact_email,
                "temporary_password": "TempPass123!",  # In production, generate secure password
                "password_reset_required": True
            },
            "portal_features": [
                "Application status tracking",
                "Document upload and management", 
                "Direct messaging with banking team",
                "Appointment scheduling",
                "Product information and rates"
            ],
            "portal_url": f"https://business-portal.bank.com/applications/{application_id}",
            "created_at": datetime.datetime.now().isoformat(),
            "expires_at": (datetime.datetime.now() + datetime.timedelta(days=90)).isoformat()
        }
        
        # Store portal information
        if tool_context:
            if "client_portals" not in tool_context.state:
                tool_context.state["client_portals"] = {}
            
            tool_context.state["client_portals"][application_id] = portal_access
        
        return {
            "status": "SUCCESS",
            "message": f"Client portal access created for {business_name}",
            "portal_access": portal_access,
            "setup_instructions": [
                f"Access portal at: {portal_access['portal_url']}",
                f"Username: {primary_contact_email}",
                "Use temporary password and reset on first login",
                "Complete profile setup for full access",
                "Enable notifications for status updates"
            ],
            "next_steps": [
                "Send portal access email to client",
                "Schedule portal walkthrough session",
                "Configure notification preferences"
            ]
        }
        
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Failed to create client portal access: {str(e)}"
        }

def schedule_client_meeting(
    application_id: str,
    meeting_type: str,
    preferred_dates: List[str],
    meeting_purpose: str,
    attendees: Optional[List[Dict[str, str]]] = None,
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    Schedule client meeting with banking team members.
    
    Args:
        application_id: Application identifier
        meeting_type: Type of meeting (kickoff, review, approval, etc.)
        preferred_dates: List of preferred meeting dates
        meeting_purpose: Purpose and agenda for the meeting
        attendees: List of attendees with names and roles
        tool_context: ADK tool context
    
    Returns:
        Dict with meeting scheduling information
    """
    try:
        # Validate meeting type
        valid_meeting_types = [
            "application_kickoff", "document_review", "credit_discussion",
            "compliance_clarification", "approval_meeting", "account_setup",
            "onboarding_completion", "relationship_introduction"
        ]
        
        if meeting_type not in valid_meeting_types:
            return {
                "status": "ERROR", 
                "message": f"Invalid meeting type. Must be one of: {valid_meeting_types}"
            }
        
        # Create meeting record
        meeting_info = {
            "meeting_id": f"MTG-{application_id}-{datetime.datetime.now().strftime('%Y%m%d%H%M')}",
            "application_id": application_id,
            "meeting_type": meeting_type,
            "purpose": meeting_purpose,
            "preferred_dates": preferred_dates,
            "attendees": attendees or [],
            "scheduling_details": {
                "duration_minutes": _get_meeting_duration(meeting_type),
                "meeting_format": "In-person or video conference",
                "location": "Bank branch or virtual",
                "preparation_required": _get_meeting_prep(meeting_type)
            },
            "scheduled_date": None,  # To be confirmed
            "status": "scheduling_in_progress",
            "created_at": datetime.datetime.now().isoformat()
        }
        
        # Store meeting information
        if tool_context:
            if "scheduled_meetings" not in tool_context.state:
                tool_context.state["scheduled_meetings"] = {}
            
            tool_context.state["scheduled_meetings"][meeting_info["meeting_id"]] = meeting_info
        
        return {
            "status": "SUCCESS",
            "message": f"Meeting scheduling initiated for {meeting_type}",
            "meeting_info": meeting_info,
            "next_steps": [
                "Coordinate calendars with all attendees",
                "Send calendar invitations",
                "Prepare meeting materials",
                "Confirm meeting logistics"
            ]
        }
        
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Failed to schedule client meeting: {str(e)}"
        }

def send_status_notification(
    application_id: str,
    notification_type: str,
    message_content: str,
    recipients: List[str],
    urgency_level: str = "normal",
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    Send status notification to client with appropriate messaging.
    """
    try:
        # Validate notification type and urgency
        valid_notification_types = [
            "status_update", "document_request", "approval_notification",
            "rejection_notification", "meeting_reminder", "completion_notice"
        ]
        
        valid_urgency_levels = ["low", "normal", "high", "critical"]
        
        if notification_type not in valid_notification_types:
            return {
                "status": "ERROR",
                "message": f"Invalid notification type. Must be one of: {valid_notification_types}"
            }
        
        if urgency_level not in valid_urgency_levels:
            urgency_level = "normal"
        
        # Create notification record
        notification = {
            "notification_id": f"NOT-{application_id}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            "application_id": application_id,
            "type": notification_type,
            "urgency": urgency_level,
            "content": {
                "subject": _generate_notification_subject(notification_type, application_id),
                "message": message_content,
                "sender": "Commercial Banking Onboarding Team",
                "reply_to": "onboarding@bank.com"
            },
            "recipients": recipients,
            "delivery_channels": _get_delivery_channels(urgency_level),
            "sent_at": datetime.datetime.now().isoformat(),
            "delivery_status": "sent"
        }
        
        # Store notification history
        if tool_context:
            if "notifications_sent" not in tool_context.state:
                tool_context.state["notifications_sent"] = []
            
            tool_context.state["notifications_sent"].append(notification)
        
        return {
            "status": "SUCCESS",
            "message": f"Notification sent successfully to {len(recipients)} recipient(s)",
            "notification": notification,
            "delivery_confirmation": {
                "sent_via": notification["delivery_channels"],
                "expected_delivery": "Within 5 minutes",
                "tracking_available": True
            }
        }
        
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Failed to send status notification: {str(e)}"
        }

def collect_client_feedback(
    application_id: str,
    feedback_type: str = "satisfaction_survey",
    custom_questions: Optional[List[str]] = None,
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    Collect client feedback on the onboarding experience.
    """
    try:
        # Generate feedback survey
        feedback_survey = {
            "survey_id": f"FEEDBACK-{application_id}-{datetime.datetime.now().strftime('%Y%m%d')}",
            "application_id": application_id,
            "survey_type": feedback_type,
            "questions": custom_questions or _get_standard_feedback_questions(),
            "response_method": ["Online survey", "Phone interview", "Email response"],
            "survey_url": f"https://feedback.bank.com/onboarding/{application_id}",
            "created_at": datetime.datetime.now().isoformat(),
            "expires_at": (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat()
        }
        
        # Mock feedback responses (in production, would collect real responses)
        mock_feedback = {
            "overall_satisfaction": "4.5/5.0",
            "process_clarity": "4.2/5.0", 
            "communication_quality": "4.7/5.0",
            "processing_speed": "4.0/5.0",
            "staff_helpfulness": "4.8/5.0",
            "recommendations": [
                "Process was thorough and professional",
                "Appreciate the regular status updates",
                "Portal was very helpful for tracking"
            ],
            "areas_for_improvement": [
                "Document upload process could be simplified",
                "More clarity on timeline expectations"
            ]
        }
        
        # Store feedback information
        if tool_context:
            if "client_feedback" not in tool_context.state:
                tool_context.state["client_feedback"] = {}
            
            tool_context.state["client_feedback"][application_id] = {
                "survey": feedback_survey,
                "responses": mock_feedback
            }
        
        return {
            "status": "SUCCESS",
            "message": "Client feedback collection initiated",
            "feedback_survey": feedback_survey,
            "mock_responses": mock_feedback,  # In production, would be actual responses
            "next_steps": [
                "Send survey invitation to client",
                "Follow up on survey completion",
                "Analyze feedback for process improvements"
            ]
        }
        
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Failed to collect client feedback: {str(e)}"
        }

def generate_client_dashboard(
    application_id: str,
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    Generate comprehensive client dashboard with application status and insights.
    """
    try:
        # Retrieve application information
        if not tool_context or "applications" not in tool_context.state:
            return {
                "status": "ERROR",
                "message": "No application data available"
            }
        
        application = tool_context.state["applications"].get(application_id)
        if not application:
            return {
                "status": "ERROR",
                "message": f"Application {application_id} not found"
            }
        
        # Generate dashboard data
        dashboard = {
            "dashboard_id": f"DASH-{application_id}",
            "generated_at": datetime.datetime.now().isoformat(),
            "application_overview": {
                "application_id": application_id,
                "business_name": application["business_information"]["legal_name"],
                "current_stage": application["application_status"]["current_stage"],
                "progress_percentage": application["application_status"]["progress_percentage"],
                "days_in_process": _calculate_processing_days(application["application_status"]["created_at"])
            },
            "progress_timeline": _generate_progress_timeline(application),
            "required_actions": _get_client_required_actions(application),
            "contact_information": {
                "relationship_manager": "Sarah Johnson",
                "phone": "(555) 123-4567",
                "email": "sarah.johnson@bank.com",
                "office_hours": "Monday-Friday 8:00 AM - 6:00 PM EST"
            },
            "resources": [
                {"title": "Document Upload Portal", "url": f"https://portal.bank.com/upload/{application_id}"},
                {"title": "FAQs", "url": "https://bank.com/business-onboarding-faq"},
                {"title": "Product Information", "url": "https://bank.com/business-banking-products"}
            ]
        }
        
        return {
            "status": "SUCCESS",
            "message": "Client dashboard generated successfully",
            "dashboard": dashboard
        }
        
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Failed to generate client dashboard: {str(e)}"
        }

# Helper functions

def _get_meeting_duration(meeting_type: str) -> int:
    """Get meeting duration in minutes based on type."""
    duration_map = {
        "application_kickoff": 60,
        "document_review": 45,
        "credit_discussion": 90,
        "compliance_clarification": 30,
        "approval_meeting": 45,
        "account_setup": 60,
        "onboarding_completion": 45,
        "relationship_introduction": 30
    }
    return duration_map.get(meeting_type, 45)

def _get_meeting_prep(meeting_type: str) -> List[str]:
    """Get preparation requirements for meeting type."""
    prep_map = {
        "application_kickoff": ["Review application", "Prepare questions", "Bring identification"],
        "document_review": ["Gather requested documents", "Review completeness"],
        "credit_discussion": ["Prepare financial statements", "Review credit questions"],
        "compliance_clarification": ["Prepare compliance documentation"],
        "approval_meeting": ["Review terms and conditions"],
        "account_setup": ["Bring authorized signers", "Review product selections"],
        "onboarding_completion": ["Review account access", "Prepare questions"],
        "relationship_introduction": ["Prepare business goals and needs"]
    }
    return prep_map.get(meeting_type, ["Review relevant materials"])

def _generate_notification_subject(notification_type: str, application_id: str) -> str:
    """Generate appropriate subject line for notification type."""
    subject_map = {
        "status_update": f"Application Status Update - {application_id}",
        "document_request": f"Document Request - Application {application_id}",
        "approval_notification": f"Application Approved - {application_id}",
        "rejection_notification": f"Application Status - {application_id}",
        "meeting_reminder": f"Meeting Reminder - Application {application_id}",
        "completion_notice": f"Onboarding Complete - Welcome to Business Banking!"
    }
    return subject_map.get(notification_type, f"Application Update - {application_id}")

def _get_delivery_channels(urgency_level: str) -> List[str]:
    """Get delivery channels based on urgency."""
    channel_map = {
        "low": ["Email"],
        "normal": ["Email", "Portal notification"],
        "high": ["Email", "Portal notification", "SMS"],
        "critical": ["Email", "Portal notification", "SMS", "Phone call"]
    }
    return channel_map.get(urgency_level, ["Email"])

def _get_standard_feedback_questions() -> List[str]:
    """Get standard feedback survey questions."""
    return [
        "How would you rate your overall onboarding experience? (1-5)",
        "Was the application process clear and easy to understand?",
        "How satisfied were you with the communication throughout the process?",
        "Did the process take longer or shorter than you expected?",
        "How helpful was our staff in addressing your questions?",
        "What could we improve about the onboarding experience?",
        "Would you recommend our business banking services to others?",
        "Any additional comments or suggestions?"
    ]

def _calculate_processing_days(created_at: str) -> int:
    """Calculate number of days in processing."""
    created_date = datetime.datetime.fromisoformat(created_at.replace('Z', '+00:00'))
    current_date = datetime.datetime.now(created_date.tzinfo)
    return (current_date - created_date).days

def _generate_progress_timeline(application: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate progress timeline for dashboard."""
    stages = [
        {"stage": "Application Created", "status": "completed", "date": application["application_status"]["created_at"]},
        {"stage": "Document Collection", "status": "in_progress", "date": None},
        {"stage": "KYC Verification", "status": "pending", "date": None},
        {"stage": "Credit Assessment", "status": "pending", "date": None},
        {"stage": "Compliance Review", "status": "pending", "date": None},
        {"stage": "Final Approval", "status": "pending", "date": None},
        {"stage": "Account Setup", "status": "pending", "date": None},
        {"stage": "Onboarding Complete", "status": "pending", "date": None}
    ]
    return stages

def _get_client_required_actions(application: Dict[str, Any]) -> List[Dict[str, str]]:
    """Get required actions for client based on current stage."""
    current_stage = application["application_status"]["current_stage"]
    
    action_map = {
        "application_created": [
            {"action": "Upload business documents", "priority": "high", "due_date": "3 business days"},
            {"action": "Schedule kickoff meeting", "priority": "medium", "due_date": "5 business days"}
        ],
        "document_collection": [
            {"action": "Complete KYC forms", "priority": "high", "due_date": "2 business days"},
            {"action": "Provide beneficial owner information", "priority": "high", "due_date": "2 business days"}
        ]
    }
    
    return action_map.get(current_stage, [])