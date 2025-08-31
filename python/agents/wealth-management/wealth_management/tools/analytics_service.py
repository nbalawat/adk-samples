"""Advanced analytics service following ADK best practices"""

import json
import logging
import random
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import os

from google.adk.tools import ToolContext
from ..data.loader import data_loader

# Setup logging
logger = logging.getLogger(__name__)

class AnalyticsServiceError(Exception):
    """Custom exception for analytics service errors"""
    pass

class AnalyticsService:
    """Analytics service for wealth management insights"""
    
    def __init__(self, enable_failures: bool = False, failure_rate: float = 0.05):
        self.enable_failures = enable_failures
        self.failure_rate = failure_rate
        self.api_key = os.getenv("ANALYTICS_API_KEY", "demo_key_12345")
    
    def _simulate_network_delay(self, min_ms: int = 200, max_ms: int = 1500):
        """Simulate realistic network latency."""
        delay = random.uniform(min_ms, max_ms) / 1000
        time.sleep(delay)
    
    def _should_fail(self) -> bool:
        """Determine if this call should simulate failure."""
        return self.enable_failures and random.random() < self.failure_rate
    
    def _validate_client_id(self, client_id: str) -> bool:
        """Validate client ID format."""
        return bool(client_id and (client_id.startswith('WM') or client_id.startswith('CLIENT')))
    
    def analyze_behavior(self, client_id: str, period: str) -> Dict[str, Any]:
        """Analyze client behavior patterns."""
        self._simulate_network_delay(300, 2000)
        
        if self._should_fail():
            raise AnalyticsServiceError("Analytics service temporarily unavailable")
        
        if not self._validate_client_id(client_id):
            raise AnalyticsServiceError(f"Invalid client ID format: {client_id}")
        
        # Try to get real client data if available
        client_data = data_loader.get_client_by_id(client_id)
        if client_data:
            risk_tolerance = client_data.get('risk_tolerance', 'Moderate')
            wealth_tier = client_data.get('wealth_tier', 'Growing')
        else:
            risk_tolerance = random.choice(['Conservative', 'Moderate', 'Aggressive'])
            wealth_tier = random.choice(['Emerging', 'Growing', 'Established'])
        
        # Generate behavior patterns based on client profile
        behavior_data = {
            "communication_preferences": {
                "preferred_channel": self._get_preferred_channel(wealth_tier),
                "response_time_avg_hours": self._get_response_time(risk_tolerance),
                "engagement_score": random.uniform(0.4, 0.95),
                "meeting_frequency": self._get_meeting_frequency(wealth_tier)
            },
            "investment_behavior": {
                "risk_appetite_trend": self._get_risk_trend(risk_tolerance),
                "trading_frequency": self._get_trading_frequency(wealth_tier),
                "rebalancing_tolerance": random.uniform(0.05, 0.25),
                "emotional_reaction_score": self._get_emotion_score(risk_tolerance)
            },
            "satisfaction_metrics": {
                "nps_score": random.randint(-20, 100),
                "service_satisfaction": random.uniform(7.0, 9.5),
                "advisor_relationship_strength": random.uniform(7.5, 9.8),
                "referral_likelihood": random.uniform(0.3, 0.9)
            }
        }
        
        return {
            "client_id": client_id,
            "analysis_period": period,
            "behavior_patterns": behavior_data,
            "confidence_score": random.uniform(0.75, 0.95),
            "last_updated": datetime.now().isoformat()
        }
    
    def predict_needs(self, client_id: str, horizon: str) -> Dict[str, Any]:
        """Predict future client needs."""
        self._simulate_network_delay(500, 3000)
        
        if self._should_fail():
            raise AnalyticsServiceError("Prediction service temporarily unavailable")
        
        # Get client context for more accurate predictions
        client_data = data_loader.get_client_by_id(client_id)
        age = client_data.get('age', 45) if client_data else random.randint(25, 75)
        total_assets = client_data.get('total_assets', 1000000) if client_data else random.randint(100000, 5000000)
        
        predictions = {
            "retirement_planning": {
                "probability": max(0.2, min(0.9, (age - 30) / 35)),
                "urgency": "high" if age > 55 else "medium" if age > 45 else "low",
                "estimated_gap": max(0, random.randint(100000, 2000000) - (total_assets * 0.1))
            },
            "estate_planning": {
                "probability": max(0.1, min(0.8, total_assets / 10000000)),
                "complexity": "high" if total_assets > 5000000 else "medium",
                "tax_efficiency_opportunity": random.uniform(0.05, 0.25)
            },
            "alternative_investments": {
                "suitability_score": min(0.9, max(0.1, total_assets / 1000000 * 0.3)),
                "recommended_allocation": min(0.25, max(0.02, total_assets / 5000000 * 0.15)),
                "risk_adjusted_return": random.uniform(0.06, 0.18)
            }
        }
        
        return {
            "client_id": client_id,
            "prediction_horizon": horizon,
            "predictions": predictions,
            "confidence_level": random.uniform(0.70, 0.92),
            "generated_at": datetime.now().isoformat()
        }
    
    def _get_preferred_channel(self, wealth_tier: str) -> str:
        """Get preferred communication channel based on wealth tier."""
        preferences = {
            "Ultra High Net Worth": ["phone", "in_person", "email"],
            "High Net Worth": ["email", "phone", "portal"],
            "Established": ["email", "portal", "phone"],
            "Growing": ["email", "portal", "text"],
            "Emerging": ["email", "text", "portal"]
        }
        return random.choice(preferences.get(wealth_tier, ["email", "phone"]))
    
    def _get_response_time(self, risk_tolerance: str) -> float:
        """Get expected response time based on risk tolerance."""
        times = {
            "Conservative": random.uniform(2, 12),
            "Moderate Conservative": random.uniform(4, 16),
            "Moderate": random.uniform(6, 24),
            "Moderate Aggressive": random.uniform(8, 36),
            "Aggressive": random.uniform(12, 48)
        }
        return times.get(risk_tolerance, random.uniform(4, 24))
    
    def _get_meeting_frequency(self, wealth_tier: str) -> str:
        """Get meeting frequency preference based on wealth tier."""
        frequencies = {
            "Ultra High Net Worth": ["monthly", "bi-weekly"],
            "High Net Worth": ["monthly", "quarterly"],
            "Established": ["quarterly", "bi-annual"],
            "Growing": ["quarterly", "bi-annual"],
            "Emerging": ["bi-annual", "annual"]
        }
        return random.choice(frequencies.get(wealth_tier, ["quarterly"]))
    
    def _get_risk_trend(self, risk_tolerance: str) -> str:
        """Get risk appetite trend based on current tolerance."""
        if risk_tolerance in ["Conservative", "Moderate Conservative"]:
            return random.choice(["stable", "stable", "increasing"])
        elif risk_tolerance == "Moderate":
            return random.choice(["stable", "increasing", "decreasing"])
        else:
            return random.choice(["stable", "decreasing", "increasing"])
    
    def _get_trading_frequency(self, wealth_tier: str) -> str:
        """Get trading frequency based on wealth tier."""
        if wealth_tier in ["Ultra High Net Worth", "High Net Worth"]:
            return random.choice(["moderate", "high"])
        else:
            return random.choice(["low", "moderate"])
    
    def _get_emotion_score(self, risk_tolerance: str) -> float:
        """Get emotional reaction score based on risk tolerance."""
        scores = {
            "Conservative": random.uniform(0.6, 0.9),
            "Moderate Conservative": random.uniform(0.4, 0.7),
            "Moderate": random.uniform(0.3, 0.6),
            "Moderate Aggressive": random.uniform(0.2, 0.5),
            "Aggressive": random.uniform(0.1, 0.4)
        }
        return scores.get(risk_tolerance, random.uniform(0.3, 0.6))

# Global service instance
analytics_service = AnalyticsService()

# ADK Tool Functions
def analyze_client_behavior(client_id: str, analysis_period: str = "6M", tool_context: ToolContext = None) -> dict:
    """
    Analyze client behavior patterns using advanced analytics.
    
    Args:
        client_id: The client identifier (format: WM123456 or CLIENT001)
        analysis_period: Analysis period (1M, 3M, 6M, 1Y, 2Y)
        tool_context: Tool execution context for state management
    
    Returns:
        dict: Analysis results with status, data, and message
    
    Example:
        result = analyze_client_behavior("WM123456", "6M")
        if result["status"] == "SUCCESS":
            behavior_data = result["data"]
    """
    
    logger.info(f"Starting behavior analysis for client {client_id} over period {analysis_period}")
    
    try:
        # Validate inputs
        valid_periods = ["1M", "3M", "6M", "1Y", "2Y"]
        if analysis_period not in valid_periods:
            return {
                "status": "ERROR",
                "message": f"Invalid analysis_period. Must be one of: {valid_periods}",
                "error_code": "INVALID_PERIOD"
            }
        
        # Call analytics service
        analysis_data = analytics_service.analyze_behavior(client_id, analysis_period)
        
        # Generate insights
        behavior = analysis_data["behavior_patterns"]
        insights = [
            f"Client prefers {behavior['communication_preferences']['preferred_channel']} communication",
            f"Risk appetite trend: {behavior['investment_behavior']['risk_appetite_trend']}",
            f"NPS Score: {behavior['satisfaction_metrics']['nps_score']}",
            f"Engagement score: {behavior['communication_preferences']['engagement_score']:.1%}"
        ]
        
        analysis_data["key_insights"] = insights
        analysis_data["recommended_actions"] = [
            "Review communication preferences",
            "Assess portfolio alignment with behavior",
            "Schedule relationship review meeting",
            "Consider service model adjustments"
        ]
        
        # Store in context for downstream tools
        if tool_context:
            tool_context.state[f"behavior_analysis_{client_id}"] = analysis_data
            logger.debug(f"Stored behavior analysis for {client_id} in tool context")
        
        logger.info(f"Behavior analysis completed successfully for client {client_id}")
        return {
            "status": "SUCCESS",
            "data": analysis_data,
            "message": f"Behavior analysis completed for client {client_id}",
            "execution_time_ms": random.randint(800, 2500)
        }
        
    except AnalyticsServiceError as e:
        error_msg = f"Analytics service error for client {client_id}: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "ERROR",
            "message": error_msg,
            "error_code": "SERVICE_ERROR",
            "retry_after": 300
        }
        
    except Exception as e:
        error_msg = f"Unexpected error analyzing behavior for client {client_id}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "status": "ERROR",
            "message": error_msg,
            "error_code": "INTERNAL_ERROR"
        }


def predict_client_needs(client_id: str, prediction_horizon: str = "12M", tool_context: ToolContext = None) -> dict:
    """
    Predict future client needs using predictive analytics.
    
    Args:
        client_id: The client identifier
        prediction_horizon: Prediction timeframe (3M, 6M, 12M, 24M, 36M)
        tool_context: Tool execution context for state management
    
    Returns:
        dict: Prediction results with status and data
    
    Example:
        result = predict_client_needs("WM123456", "12M")
        predictions = result["data"]["predictions"]
    """
    
    logger.info(f"Predicting client needs for {client_id} over {prediction_horizon}")
    
    try:
        # Validate inputs
        valid_horizons = ["3M", "6M", "12M", "24M", "36M"]
        if prediction_horizon not in valid_horizons:
            return {
                "status": "ERROR",
                "message": f"Invalid prediction_horizon. Must be one of: {valid_horizons}",
                "error_code": "INVALID_HORIZON"
            }
        
        # Call prediction service
        prediction_data = analytics_service.predict_needs(client_id, prediction_horizon)
        
        # Generate priority recommendations
        predictions = prediction_data["predictions"]
        priority_needs = []
        
        for need, details in predictions.items():
            if isinstance(details, dict) and details.get("probability", 0) > 0.6:
                priority_needs.append({
                    "need": need.replace("_", " ").title(),
                    "probability": details["probability"],
                    "urgency": details.get("urgency", "medium")
                })
        
        # Sort by probability
        priority_needs.sort(key=lambda x: x["probability"], reverse=True)
        prediction_data["priority_needs"] = priority_needs[:5]  # Top 5
        
        # Store in context
        if tool_context:
            tool_context.state[f"needs_prediction_{client_id}"] = prediction_data
            
        logger.info(f"Needs prediction completed for client {client_id}")
        return {
            "status": "SUCCESS", 
            "data": prediction_data,
            "message": f"Needs prediction completed for client {client_id}",
            "execution_time_ms": random.randint(1200, 3500)
        }
        
    except AnalyticsServiceError as e:
        error_msg = f"Prediction service error for client {client_id}: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "ERROR",
            "message": error_msg,
            "error_code": "PREDICTION_ERROR",
            "retry_after": 600
        }
        
    except Exception as e:
        error_msg = f"Unexpected error predicting needs for client {client_id}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "status": "ERROR",
            "message": error_msg,
            "error_code": "INTERNAL_ERROR"
        }


def generate_investment_research(topic: str, research_type: str = "market_analysis", tool_context: ToolContext = None) -> dict:
    """
    Generate investment research and market intelligence.
    
    Args:
        topic: Research topic or security symbol
        research_type: Type of research (market_analysis, security_analysis, sector_analysis, economic_outlook)
        tool_context: Tool execution context
    
    Returns:
        dict: Research report with status and data
    """
    
    logger.info(f"Generating investment research on topic: {topic}, type: {research_type}")
    
    try:
        # Validate inputs
        valid_types = ["market_analysis", "security_analysis", "sector_analysis", "economic_outlook"]
        if research_type not in valid_types:
            return {
                "status": "ERROR",
                "message": f"Invalid research_type. Must be one of: {valid_types}",
                "error_code": "INVALID_TYPE"
            }
        
        # Simulate research generation with realistic delay
        time.sleep(random.uniform(0.5, 2.0))
        
        research_data = {
            "topic": topic,
            "research_type": research_type,
            "publication_date": datetime.now().isoformat(),
            "analyst_rating": random.choice(["Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"]),
            "confidence_level": random.choice(["High", "Medium", "Low"]),
            "key_findings": [
                f"Current market conditions favor {random.choice(['growth', 'value', 'defensive'])} strategies",
                f"Expected volatility: {random.uniform(0.10, 0.25):.1%} over next 12 months",
                f"Key risk factors include {random.choice(['inflation', 'interest rates', 'geopolitical events'])}"
            ],
            "price_targets": {
                "current_price": round(random.uniform(50, 500), 2),
                "12_month_target": round(random.uniform(60, 600), 2),
                "support_level": round(random.uniform(40, 200), 2),
                "resistance_level": round(random.uniform(100, 800), 2)
            },
            "risk_rating": random.choice(["Low", "Medium", "High"]),
            "time_horizon": random.choice(["Short-term", "Medium-term", "Long-term"])
        }
        
        # Store in context
        if tool_context:
            tool_context.state[f"research_{topic}_{research_type}"] = research_data
        
        logger.info(f"Investment research completed for topic: {topic}")
        return {
            "status": "SUCCESS",
            "data": research_data,
            "message": f"Investment research generated for {topic}",
            "execution_time_ms": random.randint(800, 2200)
        }
        
    except Exception as e:
        error_msg = f"Failed to generate research for {topic}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "status": "ERROR",
            "message": error_msg,
            "error_code": "RESEARCH_FAILED"
        }