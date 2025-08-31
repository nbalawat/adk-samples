"""
Comprehensive Client Portfolio Analytics Tools
Provides insights across all managed clients for relationship managers
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from google.adk.tools import ToolContext
from ..mock_apis.custodian_api import MockCustodianAPI
from ..mock_apis.market_data_api import MockMarketDataAPI  
from ..mock_apis.crm_api import MockCRMAPI

# Simple utility classes for analytics
class PortfolioAnalyzer:
    """Simple portfolio analysis utilities"""
    
    @staticmethod
    def calculate_return(initial_value: float, current_value: float) -> float:
        if initial_value == 0:
            return 0.0
        return ((current_value - initial_value) / initial_value) * 100
    
    @staticmethod
    def calculate_volatility(returns: List[float]) -> float:
        if len(returns) < 2:
            return 0.0
        import statistics
        return statistics.stdev(returns)

class FinancialCalculator:
    """Simple financial calculation utilities"""
    
    @staticmethod
    def present_value(future_value: float, rate: float, periods: float) -> float:
        return future_value / ((1 + rate) ** periods)
    
    @staticmethod
    def future_value(present_value: float, rate: float, periods: float) -> float:
        return present_value * ((1 + rate) ** periods)


def analyze_market_impact_across_clients(
    advisor_id: Optional[str] = None,
    time_period: str = "3M",
    tool_context: ToolContext = None
) -> dict:
    """
    Analyze how recent market movements have impacted all clients under management.
    
    Args:
        advisor_id: Advisor/RM identifier (optional, can be inferred from context)
        time_period: Analysis period (1M, 3M, 6M, 1Y)
        tool_context: ADK tool context
        
    Returns:
        Comprehensive market impact analysis across client portfolio
    """
    custodian_api = MockCustodianAPI()
    market_api = MockMarketDataAPI()
    crm_api = MockCRMAPI()
    
    # Get all client accounts (simulated - in reality would come from advisor assignment)
    client_accounts = [
        "TEST001", "DEMO001", "CLIENT001", 
        "WM100001", "WM100002", "WM100003", "WM100004", "WM100005",
        "WM100006", "WM100007", "WM100008", "WM100009", "WM100010"
    ]
    
    market_impact_analysis = {
        "analysis_period": time_period,
        "analysis_date": datetime.utcnow().isoformat(),
        "total_clients_analyzed": len(client_accounts),
        "market_conditions": {
            "market_trend": "volatile_decline",
            "volatility_level": "high",
            "key_drivers": ["inflation_concerns", "geopolitical_tensions", "interest_rate_changes"]
        },
        "aggregate_impact": {
            "total_aum_analyzed": 0,
            "total_unrealized_loss": 0,
            "average_portfolio_decline": 0,
            "clients_with_significant_losses": 0
        },
        "client_impact_details": [],
        "sector_analysis": {},
        "risk_alerts": [],
        "opportunity_recommendations": []
    }
    
    total_aum = 0
    total_loss = 0
    client_details = []
    
    for account_id in client_accounts:
        # Get account positions
        positions_response = custodian_api.get_positions(account_id)
        if not positions_response.success:
            continue
            
        positions = positions_response.data.get("positions", [])
        portfolio_value = sum(pos.get("market_value", 0) for pos in positions)
        portfolio_loss = sum(pos.get("unrealized_gain_loss", 0) for pos in positions if pos.get("unrealized_gain_loss", 0) < 0)
        
        # Calculate impact severity
        if portfolio_value > 0:
            loss_percentage = (portfolio_loss / portfolio_value) * 100
        else:
            loss_percentage = 0
            
        impact_severity = "low"
        if loss_percentage < -10:
            impact_severity = "high"
        elif loss_percentage < -5:
            impact_severity = "medium"
        
        client_impact = {
            "account_id": account_id,
            "portfolio_value": f"${portfolio_value:,.2f}",
            "unrealized_loss": f"${portfolio_loss:,.2f}",
            "loss_percentage": f"{loss_percentage:.2f}%",
            "impact_severity": impact_severity,
            "top_losing_positions": [],
            "recommended_actions": []
        }
        
        # Analyze top losing positions
        losing_positions = [pos for pos in positions if pos.get("unrealized_gain_loss", 0) < 0]
        losing_positions.sort(key=lambda x: x.get("unrealized_gain_loss", 0))
        
        for pos in losing_positions[:3]:  # Top 3 losers
            client_impact["top_losing_positions"].append({
                "symbol": pos.get("symbol", ""),
                "loss": f"${pos.get('unrealized_gain_loss', 0):,.2f}",
                "loss_pct": f"{(pos.get('unrealized_gain_loss', 0) / pos.get('cost_basis', 1)) * 100:.1f}%"
            })
        
        # Generate recommendations based on impact
        if impact_severity == "high":
            client_impact["recommended_actions"] = [
                "Schedule urgent portfolio review meeting",
                "Consider defensive rebalancing",
                "Review risk tolerance and investment objectives",
                "Implement tax-loss harvesting if appropriate"
            ]
        elif impact_severity == "medium":
            client_impact["recommended_actions"] = [
                "Schedule portfolio review within 2 weeks",
                "Assess rebalancing opportunities",
                "Review sector allocation"
            ]
        else:
            client_impact["recommended_actions"] = [
                "Monitor closely",
                "Consider opportunistic investments"
            ]
        
        client_details.append(client_impact)
        total_aum += portfolio_value
        total_loss += abs(portfolio_loss)
        
        if impact_severity in ["high", "medium"]:
            market_impact_analysis["aggregate_impact"]["clients_with_significant_losses"] += 1
    
    # Update aggregate metrics
    market_impact_analysis["aggregate_impact"]["total_aum_analyzed"] = f"${total_aum:,.2f}"
    market_impact_analysis["aggregate_impact"]["total_unrealized_loss"] = f"${total_loss:,.2f}"
    if total_aum > 0:
        market_impact_analysis["aggregate_impact"]["average_portfolio_decline"] = f"{(total_loss / total_aum) * 100:.2f}%"
    
    market_impact_analysis["client_impact_details"] = client_details
    
    # Add sector analysis (simplified)
    market_impact_analysis["sector_analysis"] = {
        "technology": {"impact": "-12.5%", "clients_affected": 8},
        "financials": {"impact": "-8.3%", "clients_affected": 6},
        "healthcare": {"impact": "-4.2%", "clients_affected": 4},
        "utilities": {"impact": "+2.1%", "clients_affected": 3}
    }
    
    # Risk alerts
    high_impact_clients = [c for c in client_details if c["impact_severity"] == "high"]
    if high_impact_clients:
        market_impact_analysis["risk_alerts"].append({
            "alert_type": "high_portfolio_losses",
            "affected_clients": len(high_impact_clients),
            "recommended_action": "Immediate client outreach required"
        })
    
    return {
        "status": "SUCCESS",
        "message": f"Market impact analysis completed for {len(client_accounts)} clients",
        **market_impact_analysis
    }


def identify_enhancement_opportunities(
    focus_area: str = "all",  # "performance", "risk", "allocation", "tax", "all"
    minimum_aum: float = 100000,
    tool_context: ToolContext = None
) -> dict:
    """
    Identify opportunities to enhance client portfolios and relationships.
    
    Args:
        focus_area: Area to focus analysis on
        minimum_aum: Minimum AUM threshold for analysis
        tool_context: ADK tool context
        
    Returns:
        Enhancement opportunities across client base
    """
    custodian_api = MockCustodianAPI()
    
    client_accounts = [
        "TEST001", "DEMO001", "CLIENT001", 
        "WM100001", "WM100002", "WM100003", "WM100004", "WM100005",
        "WM100006", "WM100007", "WM100008", "WM100009", "WM100010"
    ]
    
    opportunities = {
        "analysis_date": datetime.utcnow().isoformat(),
        "focus_area": focus_area,
        "minimum_aum_threshold": f"${minimum_aum:,.2f}",
        "total_opportunities_identified": 0,
        "potential_additional_revenue": 0,
        "opportunities_by_category": {
            "portfolio_optimization": [],
            "risk_management": [],
            "tax_efficiency": [],
            "product_expansion": [],
            "fee_optimization": []
        },
        "priority_clients": [],
        "recommended_actions": []
    }
    
    total_revenue_opportunity = 0
    
    for account_id in client_accounts:
        # Get account info and positions
        account_response = custodian_api.get_account_info(account_id)
        positions_response = custodian_api.get_positions(account_id)
        
        if not (account_response.success and positions_response.success):
            continue
            
        account_info = account_response.data
        positions = positions_response.data.get("positions", [])
        portfolio_value = sum(pos.get("market_value", 0) for pos in positions)
        
        if portfolio_value < minimum_aum:
            continue
        
        client_opportunities = {
            "account_id": account_id,
            "portfolio_value": f"${portfolio_value:,.2f}",
            "opportunities": []
        }
        
        # Portfolio Optimization Opportunities
        cash_balance = account_info.get("cash_balance", 0)
        if cash_balance > portfolio_value * 0.1:  # More than 10% cash
            opportunity = {
                "type": "cash_drag_optimization",
                "description": f"High cash balance (${cash_balance:,.2f}) reducing returns",
                "potential_benefit": f"${cash_balance * 0.05:,.2f} additional annual return",
                "recommended_action": "Deploy excess cash into strategic allocations",
                "priority": "medium"
            }
            client_opportunities["opportunities"].append(opportunity)
            opportunities["opportunities_by_category"]["portfolio_optimization"].append({
                "client": account_id,
                **opportunity
            })
        
        # Risk Management - Concentration Risk
        if positions:
            largest_position = max(positions, key=lambda x: x.get("market_value", 0))
            largest_position_pct = (largest_position.get("market_value", 0) / portfolio_value) * 100
            
            if largest_position_pct > 25:  # Concentration risk
                opportunity = {
                    "type": "concentration_risk",
                    "description": f"Concentrated position in {largest_position.get('symbol', 'unknown')} ({largest_position_pct:.1f}%)",
                    "potential_benefit": "Improved risk-adjusted returns",
                    "recommended_action": "Gradual diversification strategy",
                    "priority": "high" if largest_position_pct > 40 else "medium"
                }
                client_opportunities["opportunities"].append(opportunity)
                opportunities["opportunities_by_category"]["risk_management"].append({
                    "client": account_id,
                    **opportunity
                })
        
        # Tax Efficiency - Tax Loss Harvesting
        losing_positions = [pos for pos in positions if pos.get("unrealized_gain_loss", 0) < 0]
        if losing_positions:
            total_losses = sum(abs(pos.get("unrealized_gain_loss", 0)) for pos in losing_positions)
            if total_losses > 5000:  # Significant tax loss harvesting opportunity
                opportunity = {
                    "type": "tax_loss_harvesting",
                    "description": f"${total_losses:,.2f} in unrealized losses available for harvesting",
                    "potential_benefit": f"${total_losses * 0.25:,.2f} potential tax savings",
                    "recommended_action": "Implement systematic tax loss harvesting",
                    "priority": "medium"
                }
                client_opportunities["opportunities"].append(opportunity)
                opportunities["opportunities_by_category"]["tax_efficiency"].append({
                    "client": account_id,
                    **opportunity
                })
        
        # Product Expansion - Alternative Investments
        if portfolio_value > 500000:  # High net worth threshold
            has_alternatives = any(pos.get("symbol", "").startswith(("REIT", "PRIV", "HEDGE")) for pos in positions)
            if not has_alternatives:
                opportunity = {
                    "type": "alternative_investments",
                    "description": "No alternative investments for diversification",
                    "potential_benefit": "Enhanced risk-adjusted returns and diversification",
                    "recommended_action": "Consider REITs, private equity, or hedge fund allocations",
                    "priority": "low"
                }
                client_opportunities["opportunities"].append(opportunity)
                opportunities["opportunities_by_category"]["product_expansion"].append({
                    "client": account_id,
                    **opportunity
                })
        
        # Fee Optimization
        estimated_fees = portfolio_value * 0.01  # Assume 1% fee
        if portfolio_value > 1000000 and estimated_fees > 10000:  # High-value client
            opportunity = {
                "type": "fee_optimization",
                "description": f"Potential for tiered pricing on ${portfolio_value:,.2f} portfolio",
                "potential_benefit": f"${estimated_fees * 0.15:,.2f} annual fee savings opportunity",
                "recommended_action": "Review fee structure and provide value-added services",
                "priority": "low"
            }
            client_opportunities["opportunities"].append(opportunity)
            opportunities["opportunities_by_category"]["fee_optimization"].append({
                "client": account_id,
                **opportunity
            })
        
        if client_opportunities["opportunities"]:
            opportunities["priority_clients"].append(client_opportunities)
            # Calculate revenue opportunity (simplified)
            revenue_opp = portfolio_value * 0.002  # 0.2% additional revenue opportunity
            total_revenue_opportunity += revenue_opp
    
    opportunities["total_opportunities_identified"] = sum(
        len(cat) for cat in opportunities["opportunities_by_category"].values()
    )
    opportunities["potential_additional_revenue"] = f"${total_revenue_opportunity:,.2f}"
    
    # Generate recommended actions
    opportunities["recommended_actions"] = [
        {
            "action": "Schedule quarterly portfolio reviews",
            "clients_affected": len(opportunities["priority_clients"]),
            "timeline": "Next 30 days"
        },
        {
            "action": "Implement systematic rebalancing program",
            "clients_affected": len([c for c in opportunities["priority_clients"] if any(o["type"] == "concentration_risk" for o in c["opportunities"])]),
            "timeline": "Next 60 days"
        },
        {
            "action": "Launch tax optimization campaign",
            "clients_affected": len(opportunities["opportunities_by_category"]["tax_efficiency"]),
            "timeline": "Before year-end"
        }
    ]
    
    return {
        "status": "SUCCESS",
        "message": f"Enhancement opportunities identified for {len(opportunities['priority_clients'])} clients",
        **opportunities
    }


def analyze_client_help_desk_requests(
    time_period: str = "3M",
    request_category: str = "all",
    tool_context: ToolContext = None
) -> dict:
    """
    Analyze client help desk requests to identify patterns and issues.
    
    Args:
        time_period: Analysis period (1M, 3M, 6M, 1Y)
        request_category: Category filter ("technical", "account", "investment", "all")
        tool_context: ADK tool context
        
    Returns:
        Analysis of client help desk interactions and trends
    """
    crm_api = MockCRMAPI()
    
    # Mock help desk data (in reality, would come from CRM/ticketing system)
    help_desk_analysis = {
        "analysis_period": time_period,
        "analysis_date": datetime.utcnow().isoformat(),
        "total_requests": 247,
        "avg_requests_per_day": 2.7,
        "resolution_metrics": {
            "avg_resolution_time": "4.2 hours",
            "first_contact_resolution": "68%",
            "customer_satisfaction": "4.3/5.0"
        },
        "request_categories": {
            "account_access": {"count": 89, "percentage": "36%", "avg_resolution": "2.1 hours"},
            "investment_questions": {"count": 67, "percentage": "27%", "avg_resolution": "6.4 hours"},
            "technical_issues": {"count": 45, "percentage": "18%", "avg_resolution": "3.8 hours"},
            "fee_inquiries": {"count": 28, "percentage": "11%", "avg_resolution": "1.9 hours"},
            "document_requests": {"count": 18, "percentage": "8%", "avg_resolution": "24.2 hours"}
        },
        "trending_issues": [
            {
                "issue": "Mobile app login difficulties",
                "requests": 34,
                "trend": "increasing",
                "impact": "high",
                "recommended_action": "Update mobile app authentication flow"
            },
            {
                "issue": "Market volatility concerns",
                "requests": 28,
                "trend": "stable",
                "impact": "medium",
                "recommended_action": "Proactive market education campaign"
            },
            {
                "issue": "ESG investment options requests",
                "requests": 22,
                "trend": "increasing",
                "impact": "medium",
                "recommended_action": "Expand ESG product offerings"
            }
        ],
        "client_specific_patterns": [],
        "proactive_recommendations": []
    }
    
    # Client-specific patterns (mock data)
    client_patterns = [
        {
            "pattern": "High-net-worth clients requesting alternative investments",
            "affected_clients": 12,
            "avg_requests_per_client": 3.2,
            "recommendation": "Develop alternative investment educational materials"
        },
        {
            "pattern": "Retirees asking about income generation strategies",
            "affected_clients": 18,
            "avg_requests_per_client": 2.8,
            "recommendation": "Create retirement income planning workshops"
        },
        {
            "pattern": "Younger clients inquiring about robo-advisor integration",
            "affected_clients": 8,
            "avg_requests_per_client": 4.1,
            "recommendation": "Evaluate digital investment platform integration"
        }
    ]
    
    help_desk_analysis["client_specific_patterns"] = client_patterns
    
    # Proactive recommendations
    help_desk_analysis["proactive_recommendations"] = [
        {
            "recommendation": "Implement chatbot for common account access issues",
            "potential_impact": "Reduce 40% of account access requests",
            "implementation_timeline": "2-3 months"
        },
        {
            "recommendation": "Create video library for investment education",
            "potential_impact": "Reduce investment question call volume by 25%",
            "implementation_timeline": "1-2 months"
        },
        {
            "recommendation": "Proactive client communication during market volatility",
            "potential_impact": "Reduce anxiety-driven calls by 35%",
            "implementation_timeline": "Immediate"
        }
    ]
    
    return {
        "status": "SUCCESS",
        "message": f"Help desk analysis completed for {time_period} period",
        **help_desk_analysis
    }


def generate_client_outreach_recommendations(
    outreach_type: str = "all",  # "proactive", "reactive", "retention", "all"
    priority_level: str = "medium",  # "low", "medium", "high", "all"
    tool_context: ToolContext = None
) -> dict:
    """
    Generate personalized outreach recommendations based on client interactions and portfolio status.
    
    Args:
        outreach_type: Type of outreach to focus on
        priority_level: Priority filter for recommendations
        tool_context: ADK tool context
        
    Returns:
        Personalized outreach recommendations for clients
    """
    custodian_api = MockCustodianAPI()
    crm_api = MockCRMAPI()
    
    client_accounts = [
        "TEST001", "DEMO001", "CLIENT001", 
        "WM100001", "WM100002", "WM100003", "WM100004", "WM100005",
        "WM100006", "WM100007", "WM100008", "WM100009", "WM100010"
    ]
    
    outreach_analysis = {
        "analysis_date": datetime.utcnow().isoformat(),
        "outreach_type_filter": outreach_type,
        "priority_filter": priority_level,
        "total_outreach_recommendations": 0,
        "client_outreach_plan": [],
        "communication_templates": {},
        "scheduling_recommendations": {
            "immediate_calls": [],
            "this_week_meetings": [],
            "this_month_reviews": []
        }
    }
    
    for account_id in client_accounts:
        # Get client portfolio and interaction history
        account_response = custodian_api.get_account_info(account_id)
        positions_response = custodian_api.get_positions(account_id)
        
        if not (account_response.success and positions_response.success):
            continue
        
        positions = positions_response.data.get("positions", [])
        portfolio_value = sum(pos.get("market_value", 0) for pos in positions)
        
        # Analyze client situation
        client_outreach = {
            "account_id": account_id,
            "portfolio_value": f"${portfolio_value:,.2f}",
            "last_contact": "2024-01-15",  # Mock data
            "outreach_recommendations": []
        }
        
        # Market Impact Outreach
        portfolio_loss = sum(pos.get("unrealized_gain_loss", 0) for pos in positions if pos.get("unrealized_gain_loss", 0) < 0)
        if portfolio_value > 0:
            loss_percentage = abs(portfolio_loss / portfolio_value) * 100
        else:
            loss_percentage = 0
        
        if loss_percentage > 10:  # Significant losses
            client_outreach["outreach_recommendations"].append({
                "type": "market_volatility_comfort_call",
                "priority": "high",
                "reason": f"Portfolio down {loss_percentage:.1f}% - client may need reassurance",
                "recommended_message": "Market volatility discussion and portfolio review",
                "timeline": "Within 24 hours",
                "communication_channel": "phone_call"
            })
            outreach_analysis["scheduling_recommendations"]["immediate_calls"].append(account_id)
        
        # Opportunity-Based Outreach
        cash_balance = account_response.data.get("cash_balance", 0)
        if cash_balance > portfolio_value * 0.15:  # High cash balance
            client_outreach["outreach_recommendations"].append({
                "type": "investment_opportunity",
                "priority": "medium",
                "reason": f"High cash balance (${cash_balance:,.2f}) - deployment opportunities",
                "recommended_message": "Investment opportunities in current market",
                "timeline": "This week",
                "communication_channel": "scheduled_call"
            })
            outreach_analysis["scheduling_recommendations"]["this_week_meetings"].append(account_id)
        
        # Relationship Maintenance
        # Mock: assume some clients haven't been contacted recently
        days_since_contact = 45  # Mock calculation
        if days_since_contact > 90:  # No contact in 3 months
            client_outreach["outreach_recommendations"].append({
                "type": "relationship_maintenance",
                "priority": "medium",
                "reason": f"No contact in {days_since_contact} days",
                "recommended_message": "Quarterly portfolio review and relationship check-in",
                "timeline": "This month",
                "communication_channel": "meeting"
            })
            outreach_analysis["scheduling_recommendations"]["this_month_reviews"].append(account_id)
        
        # Product Cross-sell Opportunities
        if portfolio_value > 500000:  # High net worth
            has_estate_planning = False  # Mock - would check actual services
            if not has_estate_planning:
                client_outreach["outreach_recommendations"].append({
                    "type": "service_expansion",
                    "priority": "low",
                    "reason": "Eligible for estate planning services",
                    "recommended_message": "Estate planning and wealth transfer strategies",
                    "timeline": "Next quarter",
                    "communication_channel": "email_then_call"
                })
        
        if client_outreach["outreach_recommendations"]:
            outreach_analysis["client_outreach_plan"].append(client_outreach)
    
    # Generate communication templates
    outreach_analysis["communication_templates"] = {
        "market_volatility_comfort_call": {
            "subject": "Portfolio Review - Navigating Market Volatility",
            "opening": "I wanted to reach out personally regarding the recent market movements and their impact on your portfolio...",
            "key_points": [
                "Current market conditions context",
                "Your portfolio's defensive positioning",
                "Long-term investment perspective",
                "Any questions or concerns you might have"
            ],
            "call_to_action": "Would you like to schedule a brief call this week to discuss?"
        },
        "investment_opportunity": {
            "subject": "Investment Opportunities in Current Market Environment",
            "opening": "Given the current market conditions, I've identified some strategic opportunities that align with your investment objectives...",
            "key_points": [
                "Cash deployment strategies",
                "Attractive entry points in quality securities",
                "Rebalancing opportunities",
                "Tax-efficient investment approaches"
            ],
            "call_to_action": "Let's schedule a call to review these opportunities together"
        },
        "relationship_maintenance": {
            "subject": "Quarterly Portfolio Review - Let's Connect",
            "opening": "I hope you're doing well. It's been a while since we last spoke, and I'd love to catch up and review your portfolio performance...",
            "key_points": [
                "Portfolio performance update",
                "Any changes in your financial situation",
                "Upcoming financial planning opportunities",
                "Market outlook and strategy adjustments"
            ],
            "call_to_action": "Would next week work for a portfolio review meeting?"
        }
    }
    
    outreach_analysis["total_outreach_recommendations"] = sum(
        len(client["outreach_recommendations"]) 
        for client in outreach_analysis["client_outreach_plan"]
    )
    
    return {
        "status": "SUCCESS",
        "message": f"Outreach recommendations generated for {len(outreach_analysis['client_outreach_plan'])} clients",
        **outreach_analysis
    }


def suggest_personalized_materials(
    client_id: Optional[str] = None,
    content_type: str = "all",  # "educational", "market_updates", "planning_tools", "all"
    tool_context: ToolContext = None
) -> dict:
    """
    Suggest personalized materials and resources for clients based on their profile and current needs.
    
    Args:
        client_id: Specific client ID (optional, will analyze all if not provided)
        content_type: Type of content to suggest
        tool_context: ADK tool context
        
    Returns:
        Personalized content suggestions for clients
    """
    custodian_api = MockCustodianAPI()
    
    if client_id:
        client_accounts = [client_id]
    else:
        client_accounts = [
            "TEST001", "DEMO001", "CLIENT001", 
            "WM100001", "WM100002", "WM100003", "WM100004", "WM100005"
        ]
    
    content_suggestions = {
        "analysis_date": datetime.utcnow().isoformat(),
        "content_type_filter": content_type,
        "client_content_recommendations": [],
        "trending_content": [
            {
                "title": "Navigating Market Volatility: A Long-term Perspective",
                "type": "market_commentary",
                "relevance": "All clients experiencing portfolio declines",
                "format": "PDF report + video explanation"
            },
            {
                "title": "Tax Loss Harvesting Strategies for 2024",
                "type": "tax_planning",
                "relevance": "Clients with unrealized losses",
                "format": "Interactive calculator + guide"
            },
            {
                "title": "ESG Investing: Aligning Values with Returns",
                "type": "investment_education",
                "relevance": "Clients interested in sustainable investing",
                "format": "Webinar series + fact sheets"
            }
        ],
        "content_library": {
            "educational_materials": [],
            "planning_tools": [],
            "market_insights": []
        }
    }
    
    for account_id in client_accounts:
        # Get client profile
        account_response = custodian_api.get_account_info(account_id)
        positions_response = custodian_api.get_positions(account_id)
        
        if not (account_response.success and positions_response.success):
            continue
        
        account_info = account_response.data
        positions = positions_response.data.get("positions", [])
        portfolio_value = sum(pos.get("market_value", 0) for pos in positions)
        
        client_suggestions = {
            "account_id": account_id,
            "portfolio_value": f"${portfolio_value:,.2f}",
            "account_type": account_info.get("account_type", "INDIVIDUAL"),
            "personalized_content": []
        }
        
        # Age-based content (mock - would come from client profile)
        client_age = 45  # Mock age
        if client_age < 40:
            client_suggestions["personalized_content"].append({
                "category": "long_term_planning",
                "title": "Building Wealth in Your 30s and 40s",
                "description": "Strategies for accumulating wealth during peak earning years",
                "format": "E-book + planning worksheets",
                "priority": "medium"
            })
        elif client_age > 55:
            client_suggestions["personalized_content"].append({
                "category": "retirement_planning",
                "title": "Pre-Retirement Checklist: 10 Years to Go",
                "description": "Essential steps to prepare for retirement",
                "format": "Checklist + retirement calculator",
                "priority": "high"
            })
        
        # Portfolio-based suggestions
        portfolio_loss = sum(pos.get("unrealized_gain_loss", 0) for pos in positions if pos.get("unrealized_gain_loss", 0) < 0)
        if abs(portfolio_loss) > portfolio_value * 0.05:  # Significant losses
            client_suggestions["personalized_content"].append({
                "category": "market_education",
                "title": "Understanding Market Cycles and Your Portfolio",
                "description": "Historical context and coping strategies for market downturns",
                "format": "Video series + historical data charts",
                "priority": "high"
            })
        
        # Cash balance suggestions
        cash_balance = account_info.get("cash_balance", 0)
        if cash_balance > portfolio_value * 0.1:
            client_suggestions["personalized_content"].append({
                "category": "investment_strategy",
                "title": "Smart Cash Deployment Strategies",
                "description": "Techniques for putting excess cash to work efficiently",
                "format": "Interactive guide + opportunity scanner",
                "priority": "medium"
            })
        
        # Account type specific content
        if account_info.get("account_type") == "IRA":
            client_suggestions["personalized_content"].append({
                "category": "tax_planning",
                "title": "IRA Optimization Strategies",
                "description": "Maximizing tax advantages and planning distributions",
                "format": "Tax calculator + strategy guide",
                "priority": "medium"
            })
        
        # High net worth content
        if portfolio_value > 1000000:
            client_suggestions["personalized_content"].append({
                "category": "advanced_planning",
                "title": "High Net Worth Planning Strategies",
                "description": "Estate planning, tax optimization, and philanthropic giving",
                "format": "Comprehensive planning guide + case studies",
                "priority": "medium"
            })
            client_suggestions["personalized_content"].append({
                "category": "alternative_investments",
                "title": "Alternative Investment Opportunities",
                "description": "Private equity, hedge funds, and real estate investments",
                "format": "Market analysis + due diligence framework",
                "priority": "low"
            })
        
        if client_suggestions["personalized_content"]:
            content_suggestions["client_content_recommendations"].append(client_suggestions)
    
    # Build content library structure
    content_suggestions["content_library"] = {
        "educational_materials": [
            "Investment Basics Series",
            "Risk Management Fundamentals", 
            "Market Analysis Training",
            "Financial Planning 101"
        ],
        "planning_tools": [
            "Retirement Planning Calculator",
            "Risk Assessment Questionnaire",
            "Tax Loss Harvesting Optimizer",
            "Asset Allocation Modeler"
        ],
        "market_insights": [
            "Weekly Market Commentary",
            "Quarterly Economic Outlook", 
            "Sector Analysis Reports",
            "Fed Policy Impact Analysis"
        ]
    }
    
    total_suggestions = sum(
        len(client["personalized_content"]) 
        for client in content_suggestions["client_content_recommendations"]
    )
    
    return {
        "status": "SUCCESS",
        "message": f"Content suggestions generated: {total_suggestions} personalized recommendations for {len(client_accounts)} clients",
        **content_suggestions
    }