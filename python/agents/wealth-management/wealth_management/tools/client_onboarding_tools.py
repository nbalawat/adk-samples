"""Tools for client onboarding agent"""

import json
import re
from typing import Dict, Any
from ..mock_apis import MockCRMAPI


def collect_kyc_information(client_data: Dict[str, Any]) -> dict:
    """
    Collect and validate Know Your Customer (KYC) information from new client.
    
    Args:
        client_data: Dictionary containing client's personal and financial information
        
    Returns:
        Dictionary with collection status and any validation messages
    """
    crm_api = MockCRMAPI()
    
    # Validate required KYC fields
    required_fields = [
        "first_name", "last_name", "date_of_birth", "ssn", 
        "address", "phone", "email", "employment_status",
        "annual_income", "net_worth", "investment_experience"
    ]
    
    missing_fields = []
    for field in required_fields:
        if field not in client_data or not client_data[field]:
            missing_fields.append(field)
    
    if missing_fields:
        return {
            "status": "INCOMPLETE",
            "message": f"Missing required KYC information: {', '.join(missing_fields)}",
            "missing_fields": missing_fields,
            "completed_fields": [f for f in required_fields if f not in missing_fields]
        }
    
    # Validate data quality (mock implementation)
    validation_errors = []
    warnings = []
    
    # Simple validation checks
    if client_data.get("ssn") and not re.match(r'^\d{3}-\d{2}-\d{4}$', client_data["ssn"]):
        validation_errors.append("Invalid SSN format")
    
    if client_data.get("email") and "@" not in client_data["email"]:
        validation_errors.append("Invalid email format")
    
    if client_data.get("annual_income", 0) <= 0:
        warnings.append("Annual income appears low or not specified")
    
    if validation_errors:
        return {
            "status": "VALIDATION_ERROR",
            "message": "KYC data validation failed",
            "validation_errors": validation_errors,
            "warnings": warnings
        }
    
    # Store KYC information in CRM
    try:
        crm_response = crm_api.create_client({
            "first_name": client_data["first_name"],
            "last_name": client_data["last_name"],
            "email": client_data["email"],
            "phone": client_data["phone"],
            "client_type": client_data.get("client_type", "INDIVIDUAL"),
            "risk_tolerance": client_data.get("risk_tolerance", "MODERATE"),
            "net_worth": client_data.get("net_worth", 0),
            "investment_goals": client_data.get("investment_goals", ["retirement"]),
            "advisor_id": "ADV001"
        })
        
        if crm_response.success:
            client_id = crm_response.data.get("client_id", "UNKNOWN")
            
            return {
                "status": "SUCCESS",
                "message": "KYC information collected and validated successfully",
                "client_id": client_id,
                "kyc_status": "COMPLETED",
                "next_step": "risk_tolerance_assessment"
            }
        else:
            return {
                "status": "ERROR",
                "message": f"Failed to store KYC information: {crm_response.error}"
            }
            
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Error processing KYC information: {str(e)}"
        }


def assess_risk_tolerance(questionnaire_responses: Dict[str, Any]) -> dict:
    """
    Assess client's risk tolerance based on questionnaire responses.
    
    Args:
        questionnaire_responses: Dictionary containing client's risk questionnaire answers
        
    Returns:
        Dictionary with risk tolerance assessment results
    """
    # Validate questionnaire responses
    required_questions = [
        "investment_timeline", "risk_comfort", "volatility_preference",
        "loss_tolerance", "investment_knowledge", "previous_losses"
    ]
    
    missing_questions = []
    for question in required_questions:
        if question not in questionnaire_responses:
            missing_questions.append(question)
    
    if missing_questions:
        return {
            "status": "INCOMPLETE",
            "message": f"Missing risk questionnaire responses: {', '.join(missing_questions)}",
            "missing_questions": missing_questions
        }
    
    # Calculate risk score (simplified algorithm)
    risk_score = 0
    
    # Investment timeline scoring
    timeline = questionnaire_responses.get("investment_timeline", "")
    if timeline in ["long_term", "10_plus_years"]:
        risk_score += 3
    elif timeline in ["medium_term", "5_10_years"]:
        risk_score += 2
    else:
        risk_score += 1
    
    # Risk comfort scoring  
    comfort = questionnaire_responses.get("risk_comfort", "")
    if comfort in ["high", "comfortable"]:
        risk_score += 3
    elif comfort in ["moderate", "somewhat_comfortable"]:
        risk_score += 2
    else:
        risk_score += 1
    
    # Volatility preference
    volatility = questionnaire_responses.get("volatility_preference", "")
    if volatility in ["high", "growth_focused"]:
        risk_score += 3
    elif volatility in ["moderate", "balanced"]:
        risk_score += 2
    else:
        risk_score += 1
    
    # Determine risk tolerance level
    if risk_score >= 8:
        risk_level = "AGGRESSIVE"
        risk_description = "High risk tolerance, suitable for growth-oriented investments"
    elif risk_score >= 6:
        risk_level = "MODERATE"
        risk_description = "Moderate risk tolerance, suitable for balanced investments"
    else:
        risk_level = "CONSERVATIVE"
        risk_description = "Low risk tolerance, suitable for capital preservation strategies"
    
    return {
        "status": "SUCCESS",
        "risk_tolerance": risk_level,
        "risk_score": risk_score,
        "risk_description": risk_description,
        "recommended_allocation": {
            "AGGRESSIVE": "80% Stocks, 15% Bonds, 5% Cash",
            "MODERATE": "60% Stocks, 35% Bonds, 5% Cash", 
            "CONSERVATIVE": "30% Stocks, 60% Bonds, 10% Cash"
        }[risk_level],
        "message": f"Risk tolerance assessed as {risk_level}"
    }


def set_investment_goals(goals_data: Dict[str, Any]) -> dict:
    """
    Set and prioritize client's investment goals.
    
    Args:
        goals_data: Dictionary containing client's investment goals and priorities
        
    Returns:
        Dictionary with goal setting results
    """
    # Validate goals data
    if "goals" not in goals_data or not isinstance(goals_data["goals"], list):
        return {
            "status": "VALIDATION_ERROR",
            "message": "Goals data must contain a 'goals' list"
        }
    
    goals = goals_data["goals"]
    client_id = goals_data.get("client_id", "UNKNOWN")
    
    if not goals:
        return {
            "status": "VALIDATION_ERROR", 
            "message": "At least one investment goal must be specified"
        }
    
    # Process each goal
    processed_goals = []
    for i, goal in enumerate(goals):
        goal_type = goal.get("type", "")
        target_amount = goal.get("target_amount", 0)
        timeline = goal.get("timeline_years", 0)
        priority = goal.get("priority", "MEDIUM")
        
        # Validate goal requirements
        if not goal_type or target_amount <= 0 or timeline <= 0:
            return {
                "status": "VALIDATION_ERROR",
                "message": f"Goal {i+1} missing required fields (type, target_amount, timeline_years)"
            }
        
        # Calculate required monthly savings (simplified)
        monthly_savings = target_amount / (timeline * 12)  # No interest assumed for simplicity
        
        processed_goal = {
            "goal_id": f"GOAL{i+1:03d}",
            "type": goal_type,
            "target_amount": f"${target_amount:,.2f}",
            "timeline_years": timeline,
            "priority": priority,
            "monthly_savings_required": f"${monthly_savings:.2f}",
            "status": "ACTIVE"
        }
        
        processed_goals.append(processed_goal)
    
    # Sort by priority (HIGH, MEDIUM, LOW)
    priority_order = {"HIGH": 1, "MEDIUM": 2, "LOW": 3}
    processed_goals.sort(key=lambda g: priority_order.get(g["priority"], 3))
    
    return {
        "status": "SUCCESS",
        "client_id": client_id,
        "num_goals": len(processed_goals),
        "goals": processed_goals,
        "message": f"Successfully set {len(processed_goals)} investment goals",
        "next_step": "create_investment_plan"
    }


def create_client_profile(profile_data: Dict[str, Any]) -> dict:
    """
    Create comprehensive client profile combining KYC, risk tolerance, and goals.
    
    Args:
        profile_data: Dictionary containing all client profile information
        
    Returns:
        Dictionary with client profile creation results
    """
    required_sections = ["kyc_data", "risk_assessment", "investment_goals"]
    missing_sections = [section for section in required_sections if section not in profile_data]
    
    if missing_sections:
        return {
            "status": "INCOMPLETE",
            "message": f"Missing profile sections: {', '.join(missing_sections)}",
            "required_sections": required_sections,
            "provided_sections": [k for k in profile_data.keys() if k in required_sections]
        }
    
    client_id = profile_data.get("client_id", f"CLIENT{hash(str(profile_data)) % 10000:04d}")
    
    # Compile comprehensive profile
    client_profile = {
        "client_id": client_id,
        "profile_status": "COMPLETE",
        "kyc_status": profile_data["kyc_data"].get("status", "UNKNOWN"),
        "risk_tolerance": profile_data["risk_assessment"].get("risk_tolerance", "UNKNOWN"),
        "num_goals": len(profile_data["investment_goals"].get("goals", [])),
        "onboarding_date": "2024-08-30",  # Mock date
        "profile_completeness": "100%",
        "ready_for_investment": True
    }
    
    # Store profile in CRM system
    crm_api = MockCRMAPI()
    try:
        storage_response = crm_api.create_client({
            "client_id": client_id,
            "profile_data": client_profile,
            "status": "ACTIVE"
        })
        
        if storage_response.success:
            return {
                "status": "SUCCESS", 
                "message": "Client profile created successfully",
                "client_profile": client_profile,
                "next_steps": [
                    "schedule_advisor_meeting",
                    "create_investment_plan", 
                    "open_investment_accounts"
                ]
            }
        else:
            return {
                "status": "ERROR",
                "message": f"Failed to store client profile: {storage_response.error}"
            }
            
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Error creating client profile: {str(e)}"
        }