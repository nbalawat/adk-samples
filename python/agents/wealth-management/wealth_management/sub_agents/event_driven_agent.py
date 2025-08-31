"""Event-driven agent for threshold-based and trigger workflows"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from google.adk.agents import Agent


class EventDrivenAgent(Agent):
    """
    Event-driven agent that responds to market events, threshold breaches,
    and trigger conditions across the wealth management platform.
    
    Handles workflows like:
    - Market volatility threshold alerts
    - Risk exposure breaches
    - Client lifecycle events
    - Regulatory deadline triggers
    """

    def __init__(self):
        super().__init__(
            name="EventDrivenAgent",
            description="Responds to real-time events and threshold-based triggers in wealth management workflows"
        )
        self.active_monitors = {}
        self.event_handlers = {
            "market_volatility": self._handle_market_volatility,
            "risk_breach": self._handle_risk_breach,
            "client_lifecycle": self._handle_client_lifecycle,
            "regulatory_deadline": self._handle_regulatory_deadline,
            "portfolio_threshold": self._handle_portfolio_threshold,
            "news_event": self._handle_news_event,
            "transaction_anomaly": self._handle_transaction_anomaly,
            "compliance_alert": self._handle_compliance_alert
        }

    async def run_async(self, query: str) -> str:
        """
        Process event-driven workflows based on trigger conditions.
        
        Args:
            query: Event description and parameters
            
        Returns:
            Workflow execution results
        """
        try:
            # Parse event type and parameters
            event_info = await self._parse_event_query(query)
            event_type = event_info.get("event_type")
            parameters = event_info.get("parameters", {})
            
            if event_type not in self.event_handlers:
                return await self._handle_unknown_event(event_type, parameters)
            
            # Execute event-specific handler
            handler = self.event_handlers[event_type]
            result = await handler(parameters)
            
            return self._format_event_response(event_type, result)
            
        except Exception as e:
            return f"Event processing error: {str(e)}"

    async def _parse_event_query(self, query: str) -> Dict[str, Any]:
        """Parse query to extract event type and parameters"""
        
        # Market volatility patterns
        if "volatility" in query.lower() or "vix" in query.lower():
            return {
                "event_type": "market_volatility",
                "parameters": await self._extract_volatility_params(query)
            }
        
        # Risk breach patterns
        if "risk" in query.lower() and ("breach" in query.lower() or "exceed" in query.lower()):
            return {
                "event_type": "risk_breach",
                "parameters": await self._extract_risk_params(query)
            }
        
        # Portfolio threshold patterns
        if "portfolio" in query.lower() and ("threshold" in query.lower() or "limit" in query.lower()):
            return {
                "event_type": "portfolio_threshold",
                "parameters": await self._extract_portfolio_params(query)
            }
        
        # News event patterns
        if "news" in query.lower() or "announcement" in query.lower() or "earnings" in query.lower():
            return {
                "event_type": "news_event",
                "parameters": await self._extract_news_params(query)
            }
        
        # Default to market volatility for broad market events
        return {
            "event_type": "market_volatility",
            "parameters": {"severity": "moderate", "source": query}
        }

    async def _handle_market_volatility(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle market volatility events"""
        
        severity = params.get("severity", "moderate")
        threshold = params.get("threshold", 20.0)
        
        # Trigger market response workflow
        market_analysis = await self._call_tool("analyze_market_volatility", {
            "threshold": threshold,
            "timeframe": "1D"
        })
        
        if market_analysis.get("status") == "SUCCESS":
            # Generate immediate client communications
            communications = await self._call_tool("trigger_proactive_outreach", {
                "event_type": "market_volatility",
                "severity": severity,
                "urgency": "high" if threshold > 15 else "medium"
            })
            
            # Alert advisor team
            advisor_alerts = await self._call_tool("notify_advisor_team", {
                "event": "market_volatility",
                "analysis": market_analysis,
                "recommended_actions": [
                    "Review client portfolios for exposure",
                    "Prepare talking points for client calls",
                    "Monitor for additional market developments"
                ]
            })
            
            return {
                "status": "SUCCESS",
                "event_type": "market_volatility",
                "actions_taken": [
                    "Market analysis completed",
                    "Client communications triggered",
                    "Advisor team alerted"
                ],
                "market_analysis": market_analysis,
                "communications": communications,
                "advisor_alerts": advisor_alerts
            }
        
        return {"status": "ERROR", "message": "Failed to analyze market volatility"}

    async def _handle_risk_breach(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle risk threshold breaches"""
        
        account_id = params.get("account_id", "UNKNOWN")
        risk_type = params.get("risk_type", "concentration")
        severity = params.get("severity", "medium")
        
        # Assess portfolio impact
        risk_assessment = await self._call_tool("assess_portfolio_risk", {
            "account_id": account_id,
            "focus_area": risk_type
        })
        
        # Generate rebalancing recommendations
        rebalancing = await self._call_tool("generate_rebalancing_recommendation", {
            "account_id": account_id,
            "risk_constraint": risk_type,
            "urgency": severity
        })
        
        # Create compliance documentation
        compliance_doc = await self._call_tool("document_risk_event", {
            "account_id": account_id,
            "risk_type": risk_type,
            "severity": severity,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return {
            "status": "SUCCESS",
            "event_type": "risk_breach",
            "account_id": account_id,
            "risk_type": risk_type,
            "actions_taken": [
                "Risk assessment completed",
                "Rebalancing recommendations generated",
                "Compliance documentation created"
            ],
            "risk_assessment": risk_assessment,
            "rebalancing": rebalancing,
            "compliance_doc": compliance_doc
        }

    async def _handle_client_lifecycle(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle client lifecycle events (retirement, inheritance, etc.)"""
        
        client_id = params.get("client_id", "UNKNOWN")
        event_type = params.get("lifecycle_event", "retirement")
        
        # Update client profile
        profile_update = await self._call_tool("update_client_profile", {
            "client_id": client_id,
            "lifecycle_event": event_type,
            "update_timestamp": datetime.utcnow().isoformat()
        })
        
        # Reassess investment strategy
        strategy_review = await self._call_tool("reassess_investment_strategy", {
            "client_id": client_id,
            "trigger_event": event_type
        })
        
        # Schedule advisor meeting
        meeting_scheduled = await self._call_tool("schedule_advisor_meeting", {
            "client_id": client_id,
            "meeting_type": "lifecycle_review",
            "priority": "high",
            "suggested_agenda": [
                f"Review {event_type} implications",
                "Update investment strategy",
                "Adjust risk tolerance",
                "Review beneficiary information"
            ]
        })
        
        return {
            "status": "SUCCESS",
            "event_type": "client_lifecycle",
            "client_id": client_id,
            "lifecycle_event": event_type,
            "actions_taken": [
                "Client profile updated",
                "Investment strategy reassessed",
                "Advisor meeting scheduled"
            ],
            "profile_update": profile_update,
            "strategy_review": strategy_review,
            "meeting_scheduled": meeting_scheduled
        }

    async def _handle_portfolio_threshold(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle portfolio threshold breaches (allocation, concentration, etc.)"""
        
        account_id = params.get("account_id", "UNKNOWN")
        threshold_type = params.get("threshold_type", "allocation")
        current_value = params.get("current_value", 0)
        threshold_value = params.get("threshold_value", 0)
        
        # Generate alert for advisor
        advisor_alert = await self._call_tool("generate_advisor_alert", {
            "account_id": account_id,
            "alert_type": "portfolio_threshold",
            "threshold_type": threshold_type,
            "current_value": current_value,
            "threshold_value": threshold_value,
            "severity": "high" if abs(current_value - threshold_value) > threshold_value * 0.1 else "medium"
        })
        
        # Calculate rebalancing options
        rebalancing_options = await self._call_tool("calculate_rebalancing_options", {
            "account_id": account_id,
            "constraint_type": threshold_type,
            "target_value": threshold_value
        })
        
        return {
            "status": "SUCCESS",
            "event_type": "portfolio_threshold",
            "account_id": account_id,
            "threshold_breach": {
                "type": threshold_type,
                "current": current_value,
                "threshold": threshold_value,
                "deviation": current_value - threshold_value
            },
            "actions_taken": [
                "Advisor alert generated",
                "Rebalancing options calculated"
            ],
            "advisor_alert": advisor_alert,
            "rebalancing_options": rebalancing_options
        }

    async def _handle_news_event(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle news events affecting client portfolios"""
        
        news_type = params.get("news_type", "earnings")
        affected_symbols = params.get("symbols", [])
        impact_level = params.get("impact", "medium")
        
        # Analyze portfolio exposure
        exposure_analysis = await self._call_tool("analyze_portfolio_exposure", {
            "symbols": affected_symbols,
            "news_type": news_type,
            "impact_level": impact_level
        })
        
        # Generate client communications if high impact
        if impact_level == "high":
            client_communications = await self._call_tool("prepare_client_communications", {
                "event_type": "news_impact",
                "affected_positions": affected_symbols,
                "communication_urgency": "immediate"
            })
        else:
            client_communications = {"status": "SKIPPED", "reason": "Low impact event"}
        
        return {
            "status": "SUCCESS",
            "event_type": "news_event",
            "news_type": news_type,
            "affected_symbols": affected_symbols,
            "impact_level": impact_level,
            "actions_taken": [
                "Portfolio exposure analyzed",
                "Client communications prepared" if impact_level == "high" else "No communications needed"
            ],
            "exposure_analysis": exposure_analysis,
            "client_communications": client_communications
        }

    async def _handle_transaction_anomaly(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle unusual transaction patterns or anomalies"""
        
        account_id = params.get("account_id", "UNKNOWN")
        anomaly_type = params.get("anomaly_type", "unusual_volume")
        
        # Flag for compliance review
        compliance_flag = await self._call_tool("flag_for_compliance_review", {
            "account_id": account_id,
            "anomaly_type": anomaly_type,
            "review_priority": "high",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Alert operations team
        operations_alert = await self._call_tool("alert_operations_team", {
            "alert_type": "transaction_anomaly",
            "account_id": account_id,
            "details": params
        })
        
        return {
            "status": "SUCCESS",
            "event_type": "transaction_anomaly",
            "account_id": account_id,
            "anomaly_type": anomaly_type,
            "actions_taken": [
                "Flagged for compliance review",
                "Operations team alerted"
            ],
            "compliance_flag": compliance_flag,
            "operations_alert": operations_alert
        }

    async def _handle_compliance_alert(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle compliance alerts and regulatory issues"""
        
        alert_type = params.get("alert_type", "regulatory_change")
        severity = params.get("severity", "medium")
        affected_accounts = params.get("affected_accounts", [])
        
        # Assess impact across client base
        impact_assessment = await self._call_tool("assess_compliance_impact", {
            "alert_type": alert_type,
            "affected_accounts": affected_accounts,
            "severity": severity
        })
        
        # Generate remediation plan
        remediation_plan = await self._call_tool("generate_remediation_plan", {
            "compliance_issue": alert_type,
            "impact_assessment": impact_assessment,
            "timeline": "immediate" if severity == "high" else "standard"
        })
        
        return {
            "status": "SUCCESS",
            "event_type": "compliance_alert",
            "alert_type": alert_type,
            "severity": severity,
            "affected_accounts_count": len(affected_accounts),
            "actions_taken": [
                "Impact assessment completed",
                "Remediation plan generated"
            ],
            "impact_assessment": impact_assessment,
            "remediation_plan": remediation_plan
        }

    async def _handle_unknown_event(self, event_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle unknown event types with generic response"""
        
        return {
            "status": "WARNING",
            "event_type": "unknown",
            "original_event_type": event_type,
            "message": f"Unknown event type '{event_type}' - routed to generic handler",
            "actions_taken": [
                "Event logged for review",
                "Default monitoring activated"
            ],
            "parameters": params
        }

    def _format_event_response(self, event_type: str, result: Dict[str, Any]) -> str:
        """Format event processing results for display"""
        
        if result.get("status") == "SUCCESS":
            actions = result.get("actions_taken", [])
            action_summary = ", ".join(actions)
            
            response = f"✅ Event-Driven Workflow Complete: {event_type.replace('_', ' ').title()}\n\n"
            response += f"🔄 Actions Executed: {action_summary}\n"
            
            if "account_id" in result:
                response += f"📊 Account: {result['account_id']}\n"
            
            if "affected_symbols" in result:
                symbols = result["affected_symbols"]
                response += f"📈 Affected Securities: {', '.join(symbols[:5])}\n"
            
            if "severity" in result:
                response += f"⚠️ Severity Level: {result['severity']}\n"
            
            response += f"\n📋 Event Details: {len(result)} data points processed"
            response += f"\n⏰ Processing Time: {datetime.utcnow().strftime('%H:%M:%S UTC')}"
            
            return response
        
        else:
            return f"❌ Event Processing Failed: {result.get('message', 'Unknown error')}"

    async def _extract_volatility_params(self, query: str) -> Dict[str, Any]:
        """Extract volatility-related parameters from query"""
        params = {"severity": "moderate"}
        
        if "extreme" in query.lower() or "severe" in query.lower():
            params["severity"] = "high"
        elif "mild" in query.lower() or "minor" in query.lower():
            params["severity"] = "low"
        
        # Extract percentage if mentioned
        import re
        pct_match = re.search(r'(\d+(?:\.\d+)?)%', query)
        if pct_match:
            params["threshold"] = float(pct_match.group(1))
        
        return params

    async def _extract_risk_params(self, query: str) -> Dict[str, Any]:
        """Extract risk-related parameters from query"""
        params = {"risk_type": "concentration"}
        
        if "liquidity" in query.lower():
            params["risk_type"] = "liquidity"
        elif "credit" in query.lower():
            params["risk_type"] = "credit"
        elif "market" in query.lower():
            params["risk_type"] = "market"
        
        # Extract account if mentioned
        import re
        account_match = re.search(r'(TEST\d+|DEMO\d+|CLIENT\d+|WM\d+)', query, re.IGNORECASE)
        if account_match:
            params["account_id"] = account_match.group(1).upper()
        
        return params

    async def _extract_portfolio_params(self, query: str) -> Dict[str, Any]:
        """Extract portfolio threshold parameters from query"""
        params = {"threshold_type": "allocation"}
        
        if "concentration" in query.lower():
            params["threshold_type"] = "concentration"
        elif "cash" in query.lower():
            params["threshold_type"] = "cash"
        elif "sector" in query.lower():
            params["threshold_type"] = "sector"
        
        return params

    async def _extract_news_params(self, query: str) -> Dict[str, Any]:
        """Extract news event parameters from query"""
        params = {"news_type": "general", "impact": "medium"}
        
        if "earnings" in query.lower():
            params["news_type"] = "earnings"
        elif "merger" in query.lower() or "acquisition" in query.lower():
            params["news_type"] = "ma"
        elif "dividend" in query.lower():
            params["news_type"] = "dividend"
        
        if "major" in query.lower() or "significant" in query.lower():
            params["impact"] = "high"
        
        return params