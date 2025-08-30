"""Memory and context management tools for wealth management agent"""

from typing import Dict, Any, Optional
from google.adk.tools import ToolContext


def remember_account(account_id: str, tool_context: ToolContext) -> dict:
    """
    Remember the user's primary account ID for future interactions.
    
    Args:
        account_id: Account ID to remember
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary confirming account has been remembered
    """
    tool_context.state["primary_account_id"] = account_id
    tool_context.state["last_account_accessed"] = account_id
    
    return {
        "status": "SUCCESS",
        "message": f"I'll remember account {account_id} for our conversation",
        "account_id": account_id
    }


def get_current_account(tool_context: ToolContext) -> dict:
    """
    Get the currently active account ID from conversation context.
    
    Args:
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary with current account information
    """
    primary_account = tool_context.state.get("primary_account_id")
    last_account = tool_context.state.get("last_account_accessed")
    
    current_account = last_account or primary_account
    
    if current_account:
        return {
            "status": "SUCCESS",
            "account_id": current_account,
            "is_primary": current_account == primary_account,
            "message": f"Using account {current_account}"
        }
    else:
        return {
            "status": "NO_ACCOUNT",
            "message": "No account has been set. Please provide an account ID.",
            "available_accounts": ["TEST001", "DEMO001", "CLIENT001", "WM100001", "WM100002"]
        }


def store_user_preference(key: str, value: str, tool_context: ToolContext) -> dict:
    """
    Store user preferences in session state.
    
    Args:
        key: Preference key (e.g., "risk_tolerance", "communication_frequency")
        value: Preference value
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary confirming preference has been stored
    """
    if "user_preferences" not in tool_context.state:
        tool_context.state["user_preferences"] = {}
    
    tool_context.state["user_preferences"][key] = value
    
    return {
        "status": "SUCCESS",
        "message": f"Stored preference: {key} = {value}",
        "key": key,
        "value": value
    }


def get_user_preferences(tool_context: ToolContext) -> dict:
    """
    Get all stored user preferences.
    
    Args:
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary with all user preferences
    """
    preferences = tool_context.state.get("user_preferences", {})
    
    return {
        "status": "SUCCESS",
        "preferences": preferences,
        "count": len(preferences)
    }


def store_conversation_context(context_type: str, context_data: Dict[str, Any], tool_context: ToolContext) -> dict:
    """
    Store conversation context for seamless experience.
    
    Args:
        context_type: Type of context (e.g., "portfolio_analysis", "goal_discussion") 
        context_data: Context data to store
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary confirming context has been stored
    """
    if "conversation_context" not in tool_context.state:
        tool_context.state["conversation_context"] = {}
    
    tool_context.state["conversation_context"][context_type] = context_data
    
    return {
        "status": "SUCCESS",
        "message": f"Stored {context_type} context",
        "context_type": context_type
    }


def get_conversation_context(context_type: str, tool_context: ToolContext) -> dict:
    """
    Retrieve stored conversation context.
    
    Args:
        context_type: Type of context to retrieve
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary with stored context data
    """
    context_data = tool_context.state.get("conversation_context", {}).get(context_type)
    
    if context_data:
        return {
            "status": "SUCCESS",
            "context_type": context_type,
            "context_data": context_data
        }
    else:
        return {
            "status": "NOT_FOUND",
            "message": f"No {context_type} context found",
            "context_type": context_type
        }


def initialize_user_session(user_id: str, primary_account_id: Optional[str] = None, tool_context: ToolContext = None) -> dict:
    """
    Initialize a new user session with basic context.
    
    Args:
        user_id: User identifier
        primary_account_id: Optional primary account ID
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary confirming session initialization
    """
    tool_context.state["user_id"] = user_id
    tool_context.state["session_initialized"] = True
    
    if primary_account_id:
        tool_context.state["primary_account_id"] = primary_account_id
        tool_context.state["last_account_accessed"] = primary_account_id
    
    # Initialize empty containers
    tool_context.state["user_preferences"] = {}
    tool_context.state["conversation_context"] = {}
    
    return {
        "status": "SUCCESS",
        "message": f"Session initialized for user {user_id}",
        "user_id": user_id,
        "primary_account_id": primary_account_id
    }


def get_session_summary(tool_context: ToolContext) -> dict:
    """
    Get a summary of current session state.
    
    Args:
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary with session summary
    """
    return {
        "status": "SUCCESS",
        "session_data": {
            "user_id": tool_context.state.get("user_id"),
            "primary_account_id": tool_context.state.get("primary_account_id"),
            "last_account_accessed": tool_context.state.get("last_account_accessed"),
            "preferences_count": len(tool_context.state.get("user_preferences", {})),
            "context_types": list(tool_context.state.get("conversation_context", {}).keys()),
            "session_initialized": tool_context.state.get("session_initialized", False)
        }
    }