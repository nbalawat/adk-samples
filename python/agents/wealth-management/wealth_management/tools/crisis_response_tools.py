"""Tools for Crisis Response Agent - Emergency management and client panic response"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
from google.adk.tools import ToolContext
from ..mock_apis import MockCustodianAPI, MockCRMAPI
from .memory_tools import get_current_account, remember_account, store_conversation_context


def initiate_emergency_protocol(crisis_type: str, client_id: Optional[str] = None, urgency_level: str = "high", tool_context: ToolContext = None) -> dict:
    """
    Initiate emergency response protocol for various crisis situations.
    
    Args:
        crisis_type: Type of crisis (panic_selling, market_crash, family_death, health_crisis, natural_disaster)
        client_id: Optional client identifier (uses remembered account if not provided)
        urgency_level: Urgency level (low, moderate, high, critical)
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary with emergency protocol activation details
    """
    # Resolve client context
    if not client_id and tool_context:
        account_context = get_current_account(tool_context)
        if account_context["status"] == "SUCCESS":
            client_id = account_context["account_id"]
        else:
            return {
                "status": "ERROR",
                "message": "No client specified for emergency protocol. Please provide client ID."
            }
    
    # Define emergency protocols by crisis type
    emergency_protocols = {
        "panic_selling": {
            "response_time": "IMMEDIATE",
            "required_actions": [
                "Contact client immediately to discuss concerns",
                "Provide behavioral coaching and market context", 
                "Prepare scenario analysis of liquidation impact",
                "Document emotional state and concerns",
                "Schedule follow-up meeting within 24 hours"
            ],
            "escalation_triggers": ["Threatens to leave firm", "Extreme distress", "Large liquidation request"],
            "team_involvement": ["Primary Advisor", "Senior Advisor", "Operations"]
        },
        "market_crash": {
            "response_time": "2_HOURS",
            "required_actions": [
                "Assess portfolio impact and protection strategies",
                "Prepare market context and historical perspective",
                "Review cash flow needs and liquidity",
                "Proactive client communication",
                "Coordinate with investment committee"
            ],
            "escalation_triggers": ["Portfolio loss >20%", "Client media interviews", "Regulatory inquiry"],
            "team_involvement": ["All Advisors", "Investment Committee", "Compliance"]
        },
        "family_death": {
            "response_time": "4_HOURS",
            "required_actions": [
                "Express condolences and provide support",
                "Coordinate with estate planning team",
                "Freeze joint accounts if necessary",
                "Assist with estate settlement process", 
                "Connect family with appropriate specialists"
            ],
            "escalation_triggers": ["Estate disputes", "Beneficiary conflicts", "Large estate value"],
            "team_involvement": ["Primary Advisor", "Estate Planning", "Operations", "Legal"]
        },
        "health_crisis": {
            "response_time": "SAME_DAY",
            "required_actions": [
                "Provide emotional and financial support",
                "Review healthcare financing options",
                "Coordinate with disability insurance providers",
                "Update medical directives and powers of attorney",
                "Plan for potential long-term care needs"
            ],
            "escalation_triggers": ["Terminal diagnosis", "Family financial hardship", "Insurance disputes"],
            "team_involvement": ["Primary Advisor", "Insurance Specialist", "Estate Planning"]
        },
        "natural_disaster": {
            "response_time": "IMMEDIATE",
            "required_actions": [
                "Verify client and family safety",
                "Expedite emergency fund access",
                "Coordinate with insurance companies",
                "Provide temporary financial assistance",
                "Plan financial recovery strategy"
            ],
            "escalation_triggers": ["Total property loss", "Family displacement", "Business destruction"],
            "team_involvement": ["Primary Advisor", "Operations", "Insurance Specialist", "Emergency Response"]
        }
    }
    
    protocol = emergency_protocols.get(crisis_type, emergency_protocols["panic_selling"])
    
    # Generate emergency response plan
    emergency_response = {
        "protocol_id": f"EMRG-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "crisis_type": crisis_type,
        "client_id": client_id,
        "urgency_level": urgency_level,
        "initiated_timestamp": datetime.now().isoformat(),
        "response_time_requirement": protocol["response_time"],
        "required_actions": protocol["required_actions"],
        "team_involvement": protocol["team_involvement"],
        "escalation_triggers": protocol["escalation_triggers"],
        "status": "INITIATED"
    }
    
    # Store emergency context
    if tool_context:
        if "active_emergencies" not in tool_context.state:
            tool_context.state["active_emergencies"] = {}
        
        tool_context.state["active_emergencies"][emergency_response["protocol_id"]] = emergency_response
        
        # Store conversation context
        store_conversation_context("emergency_response", {
            "crisis_type": crisis_type,
            "protocol_id": emergency_response["protocol_id"],
            "urgency": urgency_level
        }, tool_context)
    
    return {
        "status": "SUCCESS",
        "message": f"Emergency protocol initiated for {crisis_type}",
        "emergency_response": emergency_response,
        "immediate_next_steps": protocol["required_actions"][:3],
        "coordination_required": f"Notify: {', '.join(protocol['team_involvement'])}"
    }


def provide_behavioral_coaching(client_emotion: str, market_condition: str, tool_context: ToolContext = None) -> dict:
    """
    Provide behavioral coaching and emotional support during market stress.
    
    Args:
        client_emotion: Client emotional state (panic, fear, anxiety, anger, despair)
        market_condition: Current market conditions (volatile, declining, crashing)
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary with behavioral coaching strategy and talking points
    """
    # Define coaching strategies by emotional state
    coaching_strategies = {
        "panic": {
            "primary_objective": "Immediate calming and perspective",
            "approach": "ACKNOWLEDGE_AND_REDIRECT",
            "key_phrases": [
                "I understand this feels overwhelming right now",
                "Let's take a step back and look at your full financial picture",
                "Your feelings are completely normal and understandable"
            ],
            "techniques": [
                "Active listening and validation",
                "Focus on long-term goals and progress",
                "Provide concrete data and historical context",
                "Break down complex decisions into smaller steps"
            ],
            "avoid": ["Minimizing their concerns", "Making immediate major changes", "Providing market predictions"]
        },
        "fear": {
            "primary_objective": "Build confidence through information",
            "approach": "EDUCATE_AND_REASSURE",
            "key_phrases": [
                "Let me show you how your portfolio is designed to handle this",
                "We've prepared for situations exactly like this",
                "Your diversification is working as intended"
            ],
            "techniques": [
                "Review portfolio design rationale",
                "Show historical market recovery patterns",
                "Explain defensive positioning benefits",
                "Reinforce advisor availability and support"
            ],
            "avoid": ["Rushing decisions", "Comparing to other clients", "Providing false guarantees"]
        },
        "anxiety": {
            "primary_objective": "Reduce uncertainty through planning",
            "approach": "STRUCTURE_AND_CONTROL",
            "key_phrases": [
                "Let's create a clear plan for moving forward",
                "Here are the specific steps we can take",
                "You have more control over this situation than you think"
            ],
            "techniques": [
                "Create specific action plans",
                "Schedule regular check-ins",
                "Provide written summaries of discussions",
                "Focus on controllable factors"
            ],
            "avoid": ["Open-ended timelines", "Vague reassurances", "Too many options at once"]
        },
        "anger": {
            "primary_objective": "Channel energy constructively",
            "approach": "VALIDATE_AND_REDIRECT",
            "key_phrases": [
                "I can hear how frustrated you are about this situation",
                "Let's focus that energy on protecting and growing your wealth",
                "Your concerns are valid, now let's address them systematically"
            ],
            "techniques": [
                "Acknowledge their right to be upset",
                "Focus on problem-solving activities",
                "Provide factual analysis without defensiveness",
                "Channel anger into positive action"
            ],
            "avoid": ["Becoming defensive", "Arguing with their perspective", "Making excuses"]
        },
        "despair": {
            "primary_objective": "Restore hope and perspective",
            "approach": "SUPPORT_AND_REBUILD",
            "key_phrases": [
                "I know this feels devastating, but we can work through this together",
                "You've overcome challenges before, and you have the strength to do it again",
                "Let's focus on what we can rebuild and improve"
            ],
            "techniques": [
                "Provide unconditional support and availability",
                "Focus on small, achievable wins",
                "Connect with other support resources if needed",
                "Emphasize their past resilience and strength"
            ],
            "avoid": ["Rushing recovery timeline", "Providing unsolicited advice", "Comparing their situation"]
        }
    }
    
    # Get coaching strategy
    strategy = coaching_strategies.get(client_emotion, coaching_strategies["anxiety"])
    
    # Customize based on market condition
    market_context = {
        "volatile": "short-term market movement that's part of normal cycles",
        "declining": "market downturn that creates long-term opportunities",
        "crashing": "severe market stress that tests portfolio resilience"
    }
    
    context = market_context.get(market_condition, market_context["volatile"])
    
    # Generate coaching session plan
    coaching_plan = {
        "session_objective": strategy["primary_objective"],
        "coaching_approach": strategy["approach"],
        "opening_statements": strategy["key_phrases"],
        "techniques_to_use": strategy["techniques"],
        "things_to_avoid": strategy["avoid"],
        "market_context": context,
        "session_structure": [
            "Acknowledge and validate their emotional state",
            "Provide relevant context about the situation",
            "Review their specific portfolio positioning",
            "Discuss available options and next steps",
            "Schedule appropriate follow-up"
        ]
    }
    
    # Store coaching session context
    if tool_context:
        store_conversation_context("behavioral_coaching", {
            "client_emotion": client_emotion,
            "market_condition": market_condition,
            "coaching_approach": strategy["approach"],
            "session_timestamp": datetime.now().isoformat()
        }, tool_context)
    
    return {
        "status": "SUCCESS",
        "client_emotional_state": client_emotion,
        "market_conditions": market_condition,
        "coaching_strategy": coaching_plan,
        "session_goals": [
            "Stabilize emotional state",
            "Provide clear context and perspective", 
            "Maintain client relationship and trust",
            "Guide toward sound financial decisions"
        ],
        "success_indicators": [
            "Client expresses reduced anxiety",
            "Client asks thoughtful questions",
            "Client agrees to scheduled follow-up",
            "Client maintains confidence in strategy"
        ],
        "message": f"Behavioral coaching strategy prepared for {client_emotion} client during {market_condition} conditions"
    }


def prepare_scenario_analysis(withdrawal_amount: float, market_impact: str, client_account: Optional[str] = None, tool_context: ToolContext = None) -> dict:
    """
    Prepare scenario analysis for major portfolio changes during crisis.
    
    Args:
        withdrawal_amount: Amount client wants to withdraw
        market_impact: Expected market impact (mild, moderate, severe)
        client_account: Optional client account ID (uses remembered account if not provided)
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary with comprehensive scenario analysis
    """
    # Resolve account context
    if not client_account and tool_context:
        account_context = get_current_account(tool_context)
        if account_context["status"] == "SUCCESS":
            client_account = account_context["account_id"]
        else:
            return {
                "status": "ERROR", 
                "message": "No client account specified for scenario analysis"
            }
    
    custodian_api = MockCustodianAPI()
    
    # Get current portfolio data
    portfolio_response = custodian_api.get_positions(client_account)
    if not portfolio_response.success:
        return {
            "status": "ERROR",
            "message": f"Failed to retrieve portfolio data: {portfolio_response.error}"
        }
    
    portfolio_data = portfolio_response.data
    positions = portfolio_data.get("positions", [])
    total_portfolio_value = portfolio_data.get("total_market_value", 0)
    
    # Define market impact scenarios
    impact_multipliers = {
        "mild": {"stocks": -0.05, "bonds": -0.01, "recovery_months": 6},
        "moderate": {"stocks": -0.15, "bonds": -0.03, "recovery_months": 18}, 
        "severe": {"stocks": -0.30, "bonds": -0.08, "recovery_months": 36}
    }
    
    impact_data = impact_multipliers.get(market_impact, impact_multipliers["moderate"])
    
    # Calculate current scenario (immediate withdrawal)
    withdrawal_percentage = (withdrawal_amount / total_portfolio_value * 100) if total_portfolio_value > 0 else 0
    remaining_portfolio_value = total_portfolio_value - withdrawal_amount
    
    # Calculate projected scenarios
    scenarios = []
    
    # Scenario 1: Immediate withdrawal at current market
    current_scenario = {
        "scenario_name": "Immediate Withdrawal (Current Market)",
        "withdrawal_amount": f"${withdrawal_amount:,.2f}",
        "withdrawal_percentage": f"{withdrawal_percentage:.1f}%",
        "remaining_portfolio": f"${remaining_portfolio_value:,.2f}",
        "tax_implications": f"${withdrawal_amount * 0.15:,.2f}",  # Estimated 15% tax
        "opportunity_cost": "Immediate liquidity, no market timing risk",
        "pros": ["Immediate access to funds", "No further market risk on withdrawn amount"],
        "cons": ["May be selling at unfavorable prices", "Reduces long-term wealth building"]
    }
    scenarios.append(current_scenario)
    
    # Scenario 2: Partial withdrawal with market recovery wait
    partial_amount = withdrawal_amount * 0.5
    partial_scenario = {
        "scenario_name": "Partial Withdrawal + Wait Strategy",
        "withdrawal_amount": f"${partial_amount:,.2f}",
        "withdrawal_percentage": f"{partial_amount / total_portfolio_value * 100:.1f}%",
        "remaining_portfolio": f"${total_portfolio_value - partial_amount:,.2f}",
        "projected_recovery_value": f"${(total_portfolio_value - partial_amount) * 1.1:,.2f}",
        "recovery_timeline": f"{impact_data['recovery_months']} months",
        "pros": ["Reduced immediate market impact", "Preserves growth potential", "Staged approach"],
        "cons": ["May not meet immediate cash needs", "Still subject to market risk"]
    }
    scenarios.append(partial_scenario)
    
    # Scenario 3: Alternative funding sources
    alternative_scenario = {
        "scenario_name": "Alternative Funding Sources",
        "options": [
            f"Securities-based lending: ${withdrawal_amount * 0.7:,.2f} available",
            f"Home equity line: Potential access to additional funds",
            f"Cash flow optimization: Review expense reduction opportunities"
        ],
        "benefits": ["Preserves investment positions", "May offer tax advantages", "Maintains long-term strategy"],
        "considerations": ["Interest costs", "Qualification requirements", "Ongoing payments"]
    }
    scenarios.append(alternative_scenario)
    
    # Generate recommendations
    if withdrawal_percentage > 50:
        recommendation = "STRONGLY_DISCOURAGE - Consider alternative funding sources"
        risk_level = "VERY_HIGH"
    elif withdrawal_percentage > 25:
        recommendation = "CAUTION_ADVISED - Explore partial withdrawal or alternatives"
        risk_level = "HIGH"
    elif withdrawal_percentage > 10:
        recommendation = "PROCEED_WITH_CARE - Consider timing and tax implications"
        risk_level = "MODERATE"
    else:
        recommendation = "MANAGEABLE - Monitor impact on long-term goals"
        risk_level = "LOW"
    
    return {
        "status": "SUCCESS",
        "analysis_timestamp": datetime.now().isoformat(),
        "client_account": client_account,
        "current_portfolio_value": f"${total_portfolio_value:,.2f}",
        "requested_withdrawal": f"${withdrawal_amount:,.2f}",
        "market_impact_assumption": market_impact,
        "scenarios": scenarios,
        "recommendation": recommendation,
        "risk_level": risk_level,
        "key_considerations": [
            "Tax implications of withdrawal timing",
            "Impact on long-term financial goals",
            "Alternative funding source availability",
            "Market recovery potential and timeline"
        ],
        "message": f"Scenario analysis prepared for ${withdrawal_amount:,.2f} withdrawal ({withdrawal_percentage:.1f}% of portfolio)"
    }


def coordinate_emergency_meeting(urgency_level: str, stakeholders: Optional[List[str]] = None, tool_context: ToolContext = None) -> dict:
    """
    Coordinate emergency meetings based on crisis severity.
    
    Args:
        urgency_level: Meeting urgency (routine, urgent, critical, emergency)
        stakeholders: Required meeting participants
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary with meeting coordination details
    """
    if stakeholders is None:
        stakeholders = ["primary_advisor", "client"]
    
    # Define meeting parameters by urgency
    meeting_parameters = {
        "routine": {
            "timeline": "WITHIN_1_WEEK",
            "duration": "60_MINUTES",
            "format": "IN_PERSON_OR_VIDEO",
            "preparation_time": "2_DAYS"
        },
        "urgent": {
            "timeline": "WITHIN_24_HOURS", 
            "duration": "45_MINUTES",
            "format": "VIDEO_OR_PHONE",
            "preparation_time": "4_HOURS"
        },
        "critical": {
            "timeline": "WITHIN_4_HOURS",
            "duration": "30_MINUTES", 
            "format": "PHONE_CALL",
            "preparation_time": "1_HOUR"
        },
        "emergency": {
            "timeline": "IMMEDIATE",
            "duration": "AS_NEEDED",
            "format": "PHONE_CALL",
            "preparation_time": "MINIMAL"
        }
    }
    
    params = meeting_parameters.get(urgency_level, meeting_parameters["urgent"])
    
    # Generate meeting coordination plan
    meeting_id = f"MTG-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    coordination_plan = {
        "meeting_id": meeting_id,
        "urgency_level": urgency_level,
        "timeline_requirement": params["timeline"],
        "estimated_duration": params["duration"],
        "recommended_format": params["format"],
        "preparation_time_available": params["preparation_time"],
        "required_stakeholders": stakeholders,
        "coordination_tasks": [
            "Contact all stakeholders immediately",
            "Identify optimal meeting time within timeline",
            "Set up meeting technology/logistics",
            "Prepare relevant documents and materials",
            "Send meeting invitations with agenda"
        ]
    }
    
    # Add stakeholder-specific coordination
    stakeholder_actions = {}
    for stakeholder in stakeholders:
        if stakeholder == "client":
            stakeholder_actions["client"] = [
                "Contact via primary phone number",
                "Confirm emotional readiness for discussion",
                "Provide brief agenda overview",
                "Ensure private/comfortable setting"
            ]
        elif stakeholder == "primary_advisor":
            stakeholder_actions["primary_advisor"] = [
                "Review recent client interactions",
                "Prepare relevant portfolio/market data",
                "Plan discussion approach and objectives",
                "Coordinate with support team if needed"
            ]
        elif stakeholder == "senior_advisor":
            stakeholder_actions["senior_advisor"] = [
                "Brief on client situation and history",
                "Review escalation triggers and options",
                "Prepare advanced solutions and alternatives",
                "Plan post-meeting follow-up strategy"
            ]
    
    coordination_plan["stakeholder_specific_actions"] = stakeholder_actions
    
    # Store meeting coordination in context
    if tool_context:
        if "scheduled_meetings" not in tool_context.state:
            tool_context.state["scheduled_meetings"] = {}
        
        tool_context.state["scheduled_meetings"][meeting_id] = {
            "urgency": urgency_level,
            "stakeholders": stakeholders,
            "scheduled_timestamp": datetime.now().isoformat(),
            "status": "COORDINATING"
        }
    
    return {
        "status": "SUCCESS",
        "meeting_coordination": coordination_plan,
        "immediate_actions": [
            f"Contact stakeholders within timeline: {params['timeline']}",
            f"Set up {params['format']} meeting capability",
            f"Prepare materials with {params['preparation_time']} available"
        ],
        "success_criteria": [
            "All stakeholders contacted and available",
            "Meeting scheduled within timeline requirement",
            "Appropriate preparation completed",
            "Clear agenda and objectives established"
        ],
        "message": f"Emergency meeting coordination initiated for {urgency_level} situation with {len(stakeholders)} stakeholders"
    }


def document_crisis_interaction(incident_details: Dict[str, Any], resolution: str, tool_context: ToolContext = None) -> dict:
    """
    Document crisis interactions for compliance and follow-up.
    
    Args:
        incident_details: Details about the crisis incident
        resolution: Resolution or current status of the situation
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary with documentation details and follow-up requirements
    """
    # Generate documentation record
    documentation_id = f"DOC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    crisis_documentation = {
        "documentation_id": documentation_id,
        "incident_timestamp": datetime.now().isoformat(),
        "incident_type": incident_details.get("crisis_type", "UNSPECIFIED"),
        "client_id": incident_details.get("client_id", "UNKNOWN"),
        "urgency_level": incident_details.get("urgency_level", "MODERATE"),
        "incident_description": incident_details.get("description", "Crisis interaction documented"),
        "actions_taken": incident_details.get("actions_taken", []),
        "resolution_status": resolution,
        "stakeholders_involved": incident_details.get("stakeholders", []),
        "follow_up_required": incident_details.get("follow_up_needed", True),
        "regulatory_implications": incident_details.get("regulatory_notes", "None identified"),
        "documented_by": "Crisis Response System",
        "documentation_complete": True
    }
    
    # Determine follow-up requirements
    follow_up_requirements = []
    
    if "panic" in incident_details.get("crisis_type", "").lower():
        follow_up_requirements.extend([
            "Schedule 48-hour check-in call",
            "Monitor account for unusual activity", 
            "Document emotional state progression",
            "Consider behavioral coaching referral"
        ])
    
    if "liquidation" in resolution.lower() or "withdrawal" in resolution.lower():
        follow_up_requirements.extend([
            "Process withdrawal documentation",
            "Calculate tax implications",
            "Update financial plan projections",
            "Review portfolio rebalancing needs"
        ])
    
    if incident_details.get("urgency_level") in ["critical", "emergency"]:
        follow_up_requirements.extend([
            "Senior management notification required",
            "Compliance review of actions taken",
            "Client satisfaction survey",
            "Process improvement review"
        ])
    
    # Store documentation in context
    if tool_context:
        if "crisis_documentation" not in tool_context.state:
            tool_context.state["crisis_documentation"] = {}
        
        tool_context.state["crisis_documentation"][documentation_id] = crisis_documentation
    
    return {
        "status": "SUCCESS",
        "documentation_record": crisis_documentation,
        "follow_up_requirements": follow_up_requirements,
        "compliance_notes": [
            "Crisis interaction properly documented",
            "All required stakeholders notified",
            "Client welfare prioritized throughout process",
            "Professional standards maintained"
        ],
        "retention_requirements": {
            "minimum_retention_period": "7_YEARS",
            "regulatory_filing": "IF_REQUIRED",
            "client_access": "UPON_REQUEST"
        },
        "message": f"Crisis interaction documented with ID: {documentation_id}"
    }