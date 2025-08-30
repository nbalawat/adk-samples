"""Tools for Market Intelligence Agent - Market volatility and economic event response"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
from google.adk.tools import ToolContext
from ..mock_apis import MockMarketDataAPI, MockCustodianAPI
from .memory_tools import get_current_account, remember_account


def analyze_market_volatility(threshold: float = 5.0, timeframe: str = "1D", tool_context: ToolContext = None) -> dict:
    """
    Analyze current market volatility and assess client impact.
    
    Args:
        threshold: Volatility threshold percentage for alerts (default 5.0%)
        timeframe: Analysis timeframe (1D, 1W, 1M)
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary with volatility analysis and client impact assessment
    """
    market_api = MockMarketDataAPI()
    
    # Get current market conditions
    market_response = market_api.get_market_indices()
    
    if not market_response.success:
        return {
            "status": "ERROR",
            "message": f"Failed to retrieve market data: {market_response.error}"
        }
    
    market_data = market_response.data
    
    # Calculate volatility metrics
    volatility_events = []
    high_volatility_detected = False
    
    for index, data in market_data.items():
        daily_change = data.get("daily_change_percent", 0)
        if abs(daily_change) >= threshold:
            high_volatility_detected = True
            volatility_events.append({
                "index": index,
                "change_percent": daily_change,
                "current_price": data.get("current_price", 0),
                "volatility_level": "HIGH" if abs(daily_change) >= 10 else "ELEVATED"
            })
    
    # Determine overall market stress level
    if high_volatility_detected:
        if any(abs(event["change_percent"]) >= 10 for event in volatility_events):
            stress_level = "SEVERE"
            recommended_action = "IMMEDIATE_CLIENT_OUTREACH"
        elif any(abs(event["change_percent"]) >= 7 for event in volatility_events):
            stress_level = "HIGH"
            recommended_action = "PROACTIVE_COMMUNICATION"
        else:
            stress_level = "MODERATE"
            recommended_action = "MONITOR_AND_PREPARE"
    else:
        stress_level = "NORMAL"
        recommended_action = "ROUTINE_MONITORING"
    
    # Store market analysis in context
    if tool_context:
        tool_context.state["last_market_analysis"] = {
            "timestamp": datetime.now().isoformat(),
            "stress_level": stress_level,
            "volatility_events": volatility_events
        }
    
    return {
        "status": "SUCCESS",
        "analysis_timestamp": datetime.now().isoformat(),
        "timeframe": timeframe,
        "threshold_used": f"{threshold}%",
        "stress_level": stress_level,
        "high_volatility_detected": high_volatility_detected,
        "volatility_events": volatility_events,
        "recommended_action": recommended_action,
        "client_impact_assessment": "Market volatility may affect client portfolios. Review high-risk clients first.",
        "message": f"Market analysis complete. Stress level: {stress_level}, Events detected: {len(volatility_events)}"
    }


def generate_market_commentary(event_type: str, client_segments: Optional[List[str]] = None, tool_context: ToolContext = None) -> dict:
    """
    Generate market commentary for different client segments.
    
    Args:
        event_type: Type of market event (volatility, correction, crash, recession)
        client_segments: Target client segments (conservative, moderate, aggressive)
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary with customized market commentary for each segment
    """
    if client_segments is None:
        client_segments = ["conservative", "moderate", "aggressive"]
    
    # Get current market analysis if available
    last_analysis = {}
    if tool_context:
        last_analysis = tool_context.state.get("last_market_analysis", {})
    
    # Generate commentary templates based on event type
    commentary_templates = {
        "volatility": {
            "conservative": {
                "headline": "Market Volatility Update - Your Portfolio Remains Stable",
                "message": "While today's market movements may seem concerning, your conservative portfolio allocation is designed to weather these periods of volatility. Your bond and cash positions provide stability during uncertain times.",
                "action_items": ["Review your emergency fund adequacy", "Consider this an opportunity to discuss rebalancing", "Maintain long-term perspective"]
            },
            "moderate": {
                "headline": "Market Volatility - Staying the Course",
                "message": "Today's market volatility is a reminder of why we maintain a balanced approach to your investments. Your diversified portfolio is positioned to capture long-term growth while managing downside risk.",
                "action_items": ["Review portfolio allocation", "Consider tax-loss harvesting opportunities", "Maintain disciplined investment approach"]
            },
            "aggressive": {
                "headline": "Market Volatility Creates Opportunities",
                "message": "While market volatility can be unsettling, history shows these periods often present long-term investment opportunities. Your growth-focused strategy is built to capitalize on market cycles.",
                "action_items": ["Consider additional investment opportunities", "Review risk tolerance", "Focus on long-term wealth building goals"]
            }
        },
        "correction": {
            "conservative": {
                "headline": "Market Correction - Your Conservative Strategy Provides Protection",
                "message": "Market corrections are normal parts of market cycles. Your conservative allocation significantly limits your exposure to this downturn while preserving capital for future opportunities.",
                "action_items": ["Review cash flow needs", "Consider defensive positioning", "Prepare for potential rebalancing"]
            },
            "moderate": {
                "headline": "Navigating the Market Correction",
                "message": "Market corrections, while uncomfortable, are normal and expected events. Your balanced portfolio is designed to participate in recoveries while limiting downside exposure during corrections like this one.",
                "action_items": ["Stay disciplined with investment plan", "Consider rebalancing opportunities", "Review and reaffirm long-term goals"]
            },
            "aggressive": {
                "headline": "Market Correction Presents Long-Term Opportunities", 
                "message": "Market corrections often create excellent long-term investment opportunities. While short-term volatility is challenging, your growth strategy positions you to benefit from eventual market recovery.",
                "action_items": ["Consider increasing equity positions", "Review dollar-cost averaging opportunities", "Maintain focus on long-term wealth creation"]
            }
        }
    }
    
    # Get appropriate template
    event_templates = commentary_templates.get(event_type, commentary_templates["volatility"])
    
    # Generate commentary for each segment
    generated_commentary = {}
    for segment in client_segments:
        template = event_templates.get(segment, event_templates["moderate"])
        
        # Customize with current market data
        commentary = {
            "segment": segment,
            "headline": template["headline"],
            "message": template["message"],
            "action_items": template["action_items"],
            "market_context": last_analysis.get("stress_level", "UNKNOWN"),
            "generated_timestamp": datetime.now().isoformat()
        }
        
        generated_commentary[segment] = commentary
    
    return {
        "status": "SUCCESS",
        "event_type": event_type,
        "segments_covered": client_segments,
        "commentary": generated_commentary,
        "usage_instructions": "Use appropriate segment commentary for client communications",
        "message": f"Generated market commentary for {len(client_segments)} client segments"
    }


def assess_portfolio_impact(market_event: str, client_account: Optional[str] = None, tool_context: ToolContext = None) -> dict:
    """
    Assess the impact of market events on specific client portfolios.
    
    Args:
        market_event: Type of market event (volatility, correction, crash)
        client_account: Optional client account ID (uses remembered account if not provided)
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary with detailed portfolio impact analysis
    """
    # Resolve account context
    if not client_account and tool_context:
        account_context = get_current_account(tool_context)
        if account_context["status"] == "SUCCESS":
            client_account = account_context["account_id"]
        else:
            return {
                "status": "ERROR",
                "message": "No client account specified. Please provide an account ID.",
                "available_accounts": account_context.get("available_accounts", [])
            }
    
    custodian_api = MockCustodianAPI()
    market_api = MockMarketDataAPI()
    
    # Get portfolio data
    portfolio_response = custodian_api.get_positions(client_account)
    if not portfolio_response.success:
        return {
            "status": "ERROR",
            "message": f"Failed to retrieve portfolio data: {portfolio_response.error}"
        }
    
    portfolio_data = portfolio_response.data
    positions = portfolio_data.get("positions", [])
    
    # Calculate impact by position
    impact_analysis = []
    total_portfolio_value = 0
    total_estimated_impact = 0
    
    # Define impact factors by event type
    impact_factors = {
        "volatility": {"stocks": -0.02, "bonds": -0.005, "cash": 0.0},  # 2% stocks, 0.5% bonds
        "correction": {"stocks": -0.12, "bonds": -0.02, "cash": 0.0},   # 12% stocks, 2% bonds  
        "crash": {"stocks": -0.25, "bonds": -0.05, "cash": 0.0}        # 25% stocks, 5% bonds
    }
    
    event_factors = impact_factors.get(market_event, impact_factors["volatility"])
    
    for position in positions:
        symbol = position.get("symbol", "")
        market_value = position.get("market_value", 0)
        total_portfolio_value += market_value
        
        # Classify position type (simplified)
        if symbol in ["BND", "VGIT", "TLT"]:
            position_type = "bonds"
            impact_factor = event_factors["bonds"]
        elif symbol in ["CASH", "VMOT"]:
            position_type = "cash"
            impact_factor = event_factors["cash"]
        else:
            position_type = "stocks"
            impact_factor = event_factors["stocks"]
        
        estimated_impact = market_value * impact_factor
        total_estimated_impact += estimated_impact
        
        impact_analysis.append({
            "symbol": symbol,
            "position_type": position_type,
            "current_value": f"${market_value:,.2f}",
            "estimated_impact": f"${estimated_impact:+,.2f}",
            "impact_percentage": f"{impact_factor * 100:+.1f}%"
        })
    
    # Calculate overall impact metrics
    portfolio_impact_percent = (total_estimated_impact / total_portfolio_value * 100) if total_portfolio_value > 0 else 0
    
    # Determine risk level
    if abs(portfolio_impact_percent) >= 15:
        risk_level = "HIGH"
        recommended_action = "IMMEDIATE_CLIENT_CONTACT"
    elif abs(portfolio_impact_percent) >= 8:
        risk_level = "MODERATE"
        recommended_action = "PROACTIVE_OUTREACH"
    else:
        risk_level = "LOW"
        recommended_action = "ROUTINE_MONITORING"
    
    return {
        "status": "SUCCESS",
        "client_account": client_account,
        "market_event": market_event,
        "analysis_timestamp": datetime.now().isoformat(),
        "portfolio_summary": {
            "total_value": f"${total_portfolio_value:,.2f}",
            "estimated_impact": f"${total_estimated_impact:+,.2f}",
            "impact_percentage": f"{portfolio_impact_percent:+.2f}%"
        },
        "risk_level": risk_level,
        "recommended_action": recommended_action,
        "position_analysis": impact_analysis,
        "message": f"Portfolio impact analysis complete. Risk level: {risk_level}"
    }


def create_comfort_call_scripts(market_condition: str, risk_tolerance: str = "moderate", tool_context: ToolContext = None) -> dict:
    """
    Create customized scripts for comfort calls during market stress.
    
    Args:
        market_condition: Current market condition (volatile, correction, crash)
        risk_tolerance: Client risk tolerance level (conservative, moderate, aggressive)
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary with scripted talking points and coaching guidance
    """
    # Define comfort call scripts by condition and risk tolerance
    call_scripts = {
        "volatile": {
            "conservative": {
                "opening": "I'm calling to check in with you regarding today's market activity. I know you prefer a conservative approach, and I want to reassure you about your portfolio positioning.",
                "key_points": [
                    "Your portfolio is heavily weighted toward stable investments",
                    "Bond and cash positions are providing stability during this volatility", 
                    "This type of market movement is normal and expected",
                    "Your conservative allocation is protecting your capital"
                ],
                "behavioral_coaching": "Acknowledge their concerns and emphasize the protective nature of their conservative strategy.",
                "closing": "Remember, we built your portfolio specifically to weather periods like this. I'm here if you have any concerns."
            },
            "moderate": {
                "opening": "I wanted to reach out regarding today's market movements and discuss how your balanced portfolio is positioned during this volatility.",
                "key_points": [
                    "Your diversified approach is working as designed",
                    "Both growth and defensive positions are serving their purposes",
                    "Market volatility creates long-term opportunities",
                    "We may consider rebalancing if conditions persist"
                ],
                "behavioral_coaching": "Focus on the benefits of diversification and the long-term perspective.",
                "closing": "This is exactly why we maintain a balanced approach. Let's stay disciplined and focused on your long-term goals."
            },
            "aggressive": {
                "opening": "Given today's market activity, I wanted to discuss how this volatility might present opportunities for your growth-oriented strategy.",
                "key_points": [
                    "Volatility is often a precursor to strong returns",
                    "Your growth strategy is built for these market cycles",
                    "History shows patient investors are rewarded",
                    "We may have opportunities to add to positions"
                ],
                "behavioral_coaching": "Channel their risk appetite into productive long-term thinking.",
                "closing": "This is exactly the type of environment where growth strategies can excel. Let's stay focused on your wealth-building objectives."
            }
        },
        "correction": {
            "conservative": {
                "opening": "I'm calling about the recent market correction. I want to review how your conservative strategy is protecting your portfolio.",
                "key_points": [
                    "Market corrections are normal and expected events",
                    "Your allocation significantly limits downside exposure",
                    "Quality bonds and cash are providing stability",
                    "This validates our conservative approach"
                ],
                "behavioral_coaching": "Reinforce their wise choice of conservative positioning and provide historical context.",
                "closing": "Your conservative approach is doing exactly what we intended - protecting your wealth during uncertain times."
            },
            "moderate": {
                "opening": "I wanted to discuss the current market correction and how your balanced portfolio is navigating this environment.",
                "key_points": [
                    "Corrections are healthy parts of long-term market cycles", 
                    "Your diversification is limiting the impact",
                    "We're positioned for the eventual recovery",
                    "This may create rebalancing opportunities"
                ],
                "behavioral_coaching": "Emphasize the normalcy of corrections and the benefits of staying disciplined.",
                "closing": "Remember, corrections are often followed by strong recoveries. Your balanced approach positions you well for both."
            },
            "aggressive": {
                "opening": "I want to discuss the current market correction and the potential opportunities it's creating for your growth strategy.",
                "key_points": [
                    "Corrections often create the best long-term opportunities",
                    "Your growth allocation is built for these cycles",
                    "History shows corrections are temporary",
                    "We may consider adding to high-quality positions"
                ],
                "behavioral_coaching": "Help them see opportunity in volatility while maintaining long-term perspective.",
                "closing": "The best long-term returns often come from staying disciplined during corrections like this one."
            }
        }
    }
    
    # Get appropriate script
    condition_scripts = call_scripts.get(market_condition, call_scripts["volatile"])
    script = condition_scripts.get(risk_tolerance, condition_scripts["moderate"])
    
    # Add general coaching points
    general_coaching = {
        "do_emphasize": [
            "Long-term perspective and goals",
            "Portfolio design rationale", 
            "Historical market resilience",
            "Advisor availability for support"
        ],
        "do_not": [
            "Make predictions about market direction",
            "Recommend major strategy changes during stress",
            "Minimize client concerns",
            "Rush the conversation"
        ],
        "red_flags": [
            "Client wanting to liquidate everything",
            "Extreme emotional distress",
            "Mention of financial hardship",
            "Family pressure to make changes"
        ]
    }
    
    return {
        "status": "SUCCESS",
        "market_condition": market_condition,
        "risk_tolerance": risk_tolerance,
        "call_script": script,
        "coaching_guidance": general_coaching,
        "call_objectives": [
            "Provide reassurance and context",
            "Reinforce portfolio strategy",
            "Identify any immediate concerns",
            "Schedule follow-up if needed"
        ],
        "message": f"Comfort call script prepared for {risk_tolerance} risk tolerance client during {market_condition} conditions"
    }


def trigger_proactive_outreach(event_severity: str, client_segments: Optional[List[str]] = None, tool_context: ToolContext = None) -> dict:
    """
    Trigger and coordinate proactive client outreach during market events.
    
    Args:
        event_severity: Severity level (low, moderate, high, severe)
        client_segments: Target client segments for outreach
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary with outreach plan and execution details
    """
    if client_segments is None:
        client_segments = ["high_net_worth", "conservative", "moderate", "aggressive"]
    
    # Define outreach strategies by severity
    outreach_strategies = {
        "low": {
            "method": "EMAIL",
            "timeline": "24_HOURS",
            "priority": "STANDARD",
            "message_type": "INFORMATIONAL"
        },
        "moderate": {
            "method": "EMAIL_AND_PORTAL",
            "timeline": "4_HOURS", 
            "priority": "ELEVATED",
            "message_type": "REASSURANCE"
        },
        "high": {
            "method": "PHONE_AND_EMAIL",
            "timeline": "2_HOURS",
            "priority": "HIGH",
            "message_type": "COMFORT_CALL"
        },
        "severe": {
            "method": "IMMEDIATE_CONTACT",
            "timeline": "30_MINUTES",
            "priority": "URGENT",
            "message_type": "CRISIS_COMMUNICATION"
        }
    }
    
    strategy = outreach_strategies.get(event_severity, outreach_strategies["moderate"])
    
    # Generate outreach plan by segment
    outreach_plan = []
    for segment in client_segments:
        segment_plan = {
            "client_segment": segment,
            "outreach_method": strategy["method"],
            "timeline": strategy["timeline"],
            "priority_level": strategy["priority"],
            "message_type": strategy["message_type"],
            "estimated_clients": 25 if segment == "high_net_worth" else 75,  # Mock numbers
            "assigned_team": "Senior Advisor" if segment == "high_net_worth" else "Advisory Team"
        }
        outreach_plan.append(segment_plan)
    
    # Store outreach execution in context
    if tool_context:
        tool_context.state["active_outreach_campaign"] = {
            "timestamp": datetime.now().isoformat(),
            "event_severity": event_severity,
            "outreach_plan": outreach_plan,
            "status": "INITIATED"
        }
    
    # Calculate total outreach scope
    total_clients = sum(plan["estimated_clients"] for plan in outreach_plan)
    
    return {
        "status": "SUCCESS",
        "campaign_initiated": datetime.now().isoformat(),
        "event_severity": event_severity,
        "outreach_strategy": strategy,
        "outreach_plan": outreach_plan,
        "execution_summary": {
            "total_client_segments": len(client_segments),
            "estimated_total_clients": total_clients,
            "execution_timeline": strategy["timeline"],
            "priority_level": strategy["priority"]
        },
        "next_steps": [
            "Execute outreach according to timeline",
            "Monitor client responses and concerns",
            "Document all interactions",
            "Escalate urgent situations",
            "Report completion metrics"
        ],
        "message": f"Proactive outreach campaign initiated for {event_severity} severity event affecting {total_clients} estimated clients"
    }