"""Tools for investment goal tracker agent with context management"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from google.adk.tools import ToolContext
from ..shared_libraries import FinancialCalculator
from .memory_tools import get_current_account, remember_account


def track_goal_progress(goal_id: str, account_id: Optional[str] = None, tool_context: ToolContext = None) -> dict:
    """
    Track progress toward a specific investment goal.
    Automatically uses remembered account if no account_id provided.
    
    Args:
        goal_id: Specific goal identifier
        account_id: Optional account identifier (uses remembered account if not provided)
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary with goal progress information
    """
    # Use context-aware account resolution
    if not account_id and tool_context:
        account_context = get_current_account(tool_context)
        if account_context["status"] == "SUCCESS":
            account_id = account_context["account_id"]
        else:
            return {
                "status": "ERROR",
                "message": f"No account specified for goal {goal_id} tracking. Please provide an account ID.",
                "available_accounts": account_context.get("available_accounts", [])
            }
    # Mock goal data - in real implementation would come from database
    mock_goals = {
        "retirement_401k": {
            "name": "Retirement Savings",
            "target_amount": 1000000,
            "target_date": "2040-01-01",
            "current_amount": 275000,
            "monthly_contribution": 1500,
            "expected_return": 0.07
        },
        "GOAL001": {
            "name": "Emergency Fund",
            "target_amount": 50000,
            "target_date": "2025-12-31", 
            "current_amount": 35000,
            "monthly_contribution": 1000,
            "expected_return": 0.03
        },
        "house_down_payment": {
            "name": "House Down Payment",
            "target_amount": 100000,
            "target_date": "2027-06-01",
            "current_amount": 45000,
            "monthly_contribution": 2000,
            "expected_return": 0.05
        }
    }
    
    # Use goal_id or fallback to first goal for demo
    goal = mock_goals.get(goal_id, mock_goals.get("GOAL001", list(mock_goals.values())[0]))
    
    # Calculate progress metrics
    progress_percentage = (goal["current_amount"] / goal["target_amount"]) * 100
    remaining_amount = goal["target_amount"] - goal["current_amount"]
    
    # Calculate time metrics
    target_date = datetime.strptime(goal["target_date"], "%Y-%m-%d")
    current_date = datetime.now()
    months_remaining = max(1, (target_date - current_date).days / 30.44)
    
    # Calculate if on track
    calculator = FinancialCalculator()
    monthly_needed = calculator.calculate_required_savings(
        remaining_amount, goal["expected_return"] / 12, int(months_remaining)
    )
    
    on_track = goal["monthly_contribution"] >= monthly_needed * 0.95  # 5% tolerance
    
    return {
        "status": "SUCCESS",
        "goal_id": goal_id,
        "goal_name": goal["name"],
        "target_amount": f"${goal['target_amount']:,.2f}",
        "current_amount": f"${goal['current_amount']:,.2f}",
        "progress_percentage": f"{progress_percentage:.1f}%",
        "remaining_amount": f"${remaining_amount:,.2f}",
        "target_date": goal["target_date"],
        "months_remaining": f"{months_remaining:.1f}",
        "monthly_contribution": f"${goal['monthly_contribution']:,.2f}",
        "monthly_needed": f"${monthly_needed:.2f}",
        "on_track": str(on_track),
        "message": f"Goal progress: {progress_percentage:.1f}% complete"
    }


def project_goal_timeline(client_id: str, goal_data: Dict[str, Any]) -> dict:
    """
    Project timeline and milestones for achieving investment goal.
    
    Args:
        client_id: Client account identifier
        goal_data: Goal parameters and assumptions
        
    Returns:
        Dictionary with projected timeline and milestones
    """
    target_amount = goal_data.get("target_amount", 100000)
    current_amount = goal_data.get("current_amount", 0) 
    monthly_contribution = goal_data.get("monthly_contribution", 1000)
    expected_return = goal_data.get("expected_return", 0.07)
    
    # Calculate timeline using financial calculator
    calculator = FinancialCalculator()
    
    # Calculate months needed to reach goal
    if monthly_contribution <= 0:
        return {
            "status": "ERROR",
            "message": "Monthly contribution must be greater than 0"
        }
    
    remaining_amount = target_amount - current_amount
    monthly_rate = expected_return / 12
    
    # Simplified calculation for demo
    if monthly_rate > 0:
        months_needed = calculator.calculate_time_to_goal(
            remaining_amount, monthly_contribution, monthly_rate
        )
    else:
        months_needed = remaining_amount / monthly_contribution
    
    # Create milestone projections
    milestones = []
    milestone_percentages = [25, 50, 75, 100]
    
    for pct in milestone_percentages:
        milestone_amount = target_amount * (pct / 100)
        milestone_months = months_needed * (pct / 100)
        milestone_date = datetime.now() + timedelta(days=milestone_months * 30.44)
        
        milestones.append({
            "percentage": f"{pct}%",
            "amount": f"${milestone_amount:,.2f}",
            "projected_date": milestone_date.strftime("%Y-%m-%d"),
            "months_from_now": f"{milestone_months:.1f}"
        })
    
    completion_date = datetime.now() + timedelta(days=months_needed * 30.44)
    
    return {
        "status": "SUCCESS",
        "client_id": client_id,
        "target_amount": f"${target_amount:,.2f}",
        "current_amount": f"${current_amount:,.2f}",
        "monthly_contribution": f"${monthly_contribution:,.2f}",
        "expected_return": f"{expected_return * 100:.1f}%",
        "months_needed": f"{months_needed:.1f}",
        "completion_date": completion_date.strftime("%Y-%m-%d"),
        "milestones": milestones,
        "message": f"Goal projected to be achieved in {months_needed:.1f} months"
    }


def suggest_goal_adjustments(goal_id: str, client_id: Optional[str] = None, tool_context: ToolContext = None) -> dict:
    """
    Suggest adjustments to improve goal achievement probability.
    Automatically uses remembered account if no client_id provided.
    
    Args:
        goal_id: Specific goal identifier
        client_id: Optional client account identifier (uses remembered account if not provided)
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary with adjustment suggestions
    """
    # Use context-aware account resolution
    if not client_id and tool_context:
        account_context = get_current_account(tool_context)
        if account_context["status"] == "SUCCESS":
            client_id = account_context["account_id"]
        else:
            return {
                "status": "ERROR",
                "message": f"No account specified for goal {goal_id} adjustment suggestions. Please provide an account ID.",
                "available_accounts": account_context.get("available_accounts", [])
            }
    # Get current goal progress first
    progress_data = track_goal_progress(client_id, goal_id)
    
    if progress_data["status"] != "SUCCESS":
        return {
            "status": "ERROR",
            "message": "Unable to retrieve goal progress for analysis"
        }
    
    # Parse current values
    on_track = progress_data["on_track"] == "True"
    current_contribution = float(progress_data["monthly_contribution"].replace("$", "").replace(",", ""))
    needed_contribution = float(progress_data["monthly_needed"].replace("$", "").replace(",", ""))
    
    suggestions = []
    
    if not on_track:
        contribution_gap = needed_contribution - current_contribution
        
        suggestions.extend([
            {
                "type": "INCREASE_CONTRIBUTION",
                "description": f"Increase monthly contribution by ${contribution_gap:.2f}",
                "impact": "Ensures goal stays on track",
                "difficulty": "MEDIUM"
            },
            {
                "type": "EXTEND_TIMELINE", 
                "description": "Consider extending target date by 6-12 months",
                "impact": "Reduces required monthly contribution",
                "difficulty": "LOW"
            },
            {
                "type": "REDUCE_TARGET",
                "description": "Consider reducing target amount by 10-20%",
                "impact": "Makes goal more achievable",
                "difficulty": "LOW"
            }
        ])
    else:
        suggestions.extend([
            {
                "type": "ACCELERATE_GOAL",
                "description": "Goal is on track - consider increasing contributions to finish early",
                "impact": "Achieve goal ahead of schedule",
                "difficulty": "LOW"
            },
            {
                "type": "ADD_STRETCH_GOAL",
                "description": "Add a stretch target of 10% above current goal",
                "impact": "Build additional financial cushion", 
                "difficulty": "MEDIUM"
            }
        ])
    
    return {
        "status": "SUCCESS",
        "goal_id": goal_id,
        "on_track": str(on_track),
        "current_status": "ON_TRACK" if on_track else "BEHIND",
        "num_suggestions": len(suggestions),
        "suggestions": suggestions,
        "message": f"Generated {len(suggestions)} adjustment suggestions"
    }


def calculate_required_savings(goal_amount: float, years: int, client_id: Optional[str] = None, tool_context: ToolContext = None) -> dict:
    """
    Calculate required monthly savings to reach a financial goal.
    Automatically uses remembered account if no client_id provided.
    
    Args:
        goal_amount: Target amount to save
        years: Time horizon in years
        client_id: Optional client account identifier (uses remembered account if not provided)
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary with savings calculations
    """
    # Use context-aware account resolution
    if not client_id and tool_context:
        account_context = get_current_account(tool_context)
        if account_context["status"] == "SUCCESS":
            client_id = account_context["account_id"]
        else:
            return {
                "status": "ERROR",
                "message": f"No account specified for savings calculation. Please provide an account ID.",
                "available_accounts": account_context.get("available_accounts", [])
            }
    if goal_amount <= 0 or years <= 0:
        return {
            "status": "VALIDATION_ERROR",
            "message": "Goal amount and years must be positive numbers"
        }
    
    # Use different return assumptions based on time horizon
    if years >= 10:
        expected_return = 0.07  # Long-term stock market return
    elif years >= 5:
        expected_return = 0.05  # Moderate growth
    else:
        expected_return = 0.03  # Conservative/short-term
    
    calculator = FinancialCalculator()
    
    # Calculate required monthly savings with compound interest
    monthly_rate = expected_return / 12
    months = years * 12
    
    if monthly_rate > 0:
        # PMT calculation for annuity
        monthly_payment = goal_amount * monthly_rate / ((1 + monthly_rate) ** months - 1)
    else:
        # Simple division if no interest
        monthly_payment = goal_amount / months
    
    # Calculate different scenarios
    scenarios = []
    return_rates = [0.03, 0.05, 0.07, 0.10]  # 3%, 5%, 7%, 10%
    
    for rate in return_rates:
        monthly_rate_scenario = rate / 12
        if monthly_rate_scenario > 0:
            payment = goal_amount * monthly_rate_scenario / ((1 + monthly_rate_scenario) ** months - 1)
        else:
            payment = goal_amount / months
            
        scenarios.append({
            "return_rate": f"{rate * 100:.1f}%",
            "monthly_savings": f"${payment:.2f}",
            "total_contributions": f"${payment * months:,.2f}",
            "growth": f"${goal_amount - (payment * months):,.2f}"
        })
    
    return {
        "status": "SUCCESS",
        "client_id": client_id,
        "goal_amount": f"${goal_amount:,.2f}",
        "time_horizon": f"{years} years ({months} months)",
        "recommended_monthly_savings": f"${monthly_payment:.2f}",
        "expected_return": f"{expected_return * 100:.1f}%",
        "total_contributions": f"${monthly_payment * months:,.2f}",
        "projected_growth": f"${goal_amount - (monthly_payment * months):,.2f}",
        "scenarios": scenarios,
        "message": f"Monthly savings of ${monthly_payment:.2f} required to reach ${goal_amount:,.2f} goal"
    }