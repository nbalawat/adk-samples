"""Mock Economic Data API for market intelligence and economic indicators"""

import os
import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from decimal import Decimal

from .base_api import BaseMockAPI, APIResponse

@dataclass
class EconomicIndicator:
    """Economic indicator data structure"""
    name: str
    current_value: float
    previous_value: float
    change_percent: float
    release_date: datetime
    next_release: datetime
    impact_level: str  # HIGH, MEDIUM, LOW
    trend: str  # IMPROVING, DECLINING, STABLE

@dataclass
class MarketEvent:
    """Market event structure"""
    event_id: str
    event_type: str  # VOLATILITY, CORRECTION, CRASH, RECOVERY
    severity: str    # LOW, MODERATE, HIGH, SEVERE
    start_time: datetime
    description: str
    affected_sectors: List[str]
    client_impact_level: str

class MockEconomicDataAPI(BaseMockAPI):
    """Mock economic data API for market intelligence"""
    
    def __init__(self):
        super().__init__("economic_data_api")
        self._initialize_economic_data()
        self._initialize_market_events()
    
    def _initialize_economic_data(self):
        """Initialize mock economic indicators"""
        self._economic_indicators = {
            "GDP_GROWTH": EconomicIndicator(
                name="GDP Growth Rate",
                current_value=2.4,
                previous_value=2.1,
                change_percent=14.3,
                release_date=datetime.now() - timedelta(days=30),
                next_release=datetime.now() + timedelta(days=60),
                impact_level="HIGH",
                trend="IMPROVING"
            ),
            "UNEMPLOYMENT": EconomicIndicator(
                name="Unemployment Rate",
                current_value=3.7,
                previous_value=3.9,
                change_percent=-5.1,
                release_date=datetime.now() - timedelta(days=7),
                next_release=datetime.now() + timedelta(days=23),
                impact_level="HIGH",
                trend="IMPROVING"
            ),
            "INFLATION_CPI": EconomicIndicator(
                name="Consumer Price Index",
                current_value=3.2,
                previous_value=3.7,
                change_percent=-13.5,
                release_date=datetime.now() - timedelta(days=14),
                next_release=datetime.now() + timedelta(days=16),
                impact_level="HIGH",
                trend="IMPROVING"
            ),
            "FED_FUNDS_RATE": EconomicIndicator(
                name="Federal Funds Rate",
                current_value=5.25,
                previous_value=5.0,
                change_percent=5.0,
                release_date=datetime.now() - timedelta(days=45),
                next_release=datetime.now() + timedelta(days=15),
                impact_level="HIGH",
                trend="STABLE"
            ),
            "CONSUMER_CONFIDENCE": EconomicIndicator(
                name="Consumer Confidence Index",
                current_value=102.6,
                previous_value=99.1,
                change_percent=3.5,
                release_date=datetime.now() - timedelta(days=5),
                next_release=datetime.now() + timedelta(days=25),
                impact_level="MEDIUM",
                trend="IMPROVING"
            ),
            "HOUSING_STARTS": EconomicIndicator(
                name="Housing Starts",
                current_value=1340000,
                previous_value=1290000,
                change_percent=3.9,
                release_date=datetime.now() - timedelta(days=10),
                next_release=datetime.now() + timedelta(days=20),
                impact_level="MEDIUM",
                trend="IMPROVING"
            )
        }
    
    def _initialize_market_events(self):
        """Initialize mock market events"""
        self._recent_events = [
            MarketEvent(
                event_id="EVT001",
                event_type="VOLATILITY",
                severity="MODERATE",
                start_time=datetime.now() - timedelta(hours=2),
                description="Increased volatility following Fed commentary on interest rates",
                affected_sectors=["Technology", "Real Estate", "Utilities"],
                client_impact_level="LOW"
            ),
            MarketEvent(
                event_id="EVT002", 
                event_type="CORRECTION",
                severity="HIGH",
                start_time=datetime.now() - timedelta(days=5),
                description="Market correction triggered by inflation concerns",
                affected_sectors=["Growth Stocks", "Technology", "Consumer Discretionary"],
                client_impact_level="MODERATE"
            )
        ]
    
    def get_economic_indicators(self, indicators: Optional[List[str]] = None) -> APIResponse:
        """Get current economic indicators"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error="Failed to retrieve economic indicators")
        
        if indicators is None:
            indicators = list(self._economic_indicators.keys())
        
        indicator_data = {}
        for indicator in indicators:
            if indicator in self._economic_indicators:
                ind = self._economic_indicators[indicator]
                indicator_data[indicator] = {
                    "name": ind.name,
                    "current_value": ind.current_value,
                    "previous_value": ind.previous_value,
                    "change_percent": ind.change_percent,
                    "release_date": ind.release_date.isoformat(),
                    "next_release": ind.next_release.isoformat(),
                    "impact_level": ind.impact_level,
                    "trend": ind.trend
                }
        
        return self._create_response(data={
            "indicators": indicator_data,
            "last_updated": datetime.now().isoformat(),
            "data_source": "Mock Economic Data Provider"
        })
    
    def get_market_stress_indicators(self) -> APIResponse:
        """Get market stress and volatility indicators"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error="Failed to retrieve market stress indicators")
        
        # Generate mock stress indicators
        stress_indicators = {
            "vix_level": round(random.uniform(15.0, 35.0), 2),
            "credit_spreads": round(random.uniform(0.8, 2.5), 2),
            "yield_curve_slope": round(random.uniform(-0.5, 2.0), 2),
            "dollar_strength": round(random.uniform(95.0, 110.0), 2),
            "commodity_volatility": round(random.uniform(20.0, 45.0), 2)
        }
        
        # Calculate overall stress level
        vix = stress_indicators["vix_level"]
        if vix > 30:
            overall_stress = "HIGH"
        elif vix > 20:
            overall_stress = "MODERATE" 
        else:
            overall_stress = "LOW"
        
        return self._create_response(data={
            "overall_stress_level": overall_stress,
            "stress_indicators": stress_indicators,
            "assessment_timestamp": datetime.now().isoformat(),
            "risk_factors": [
                "Interest rate uncertainty" if stress_indicators["yield_curve_slope"] < 0.5 else None,
                "High volatility environment" if vix > 25 else None,
                "Credit market stress" if stress_indicators["credit_spreads"] > 2.0 else None
            ]
        })
    
    def get_recent_market_events(self, days_back: int = 7) -> APIResponse:
        """Get recent market events and their impacts"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error="Failed to retrieve market events")
        
        cutoff_date = datetime.now() - timedelta(days=days_back)
        recent_events = [
            event for event in self._recent_events 
            if event.start_time >= cutoff_date
        ]
        
        events_data = []
        for event in recent_events:
            events_data.append({
                "event_id": event.event_id,
                "event_type": event.event_type,
                "severity": event.severity,
                "start_time": event.start_time.isoformat(),
                "description": event.description,
                "affected_sectors": event.affected_sectors,
                "client_impact_level": event.client_impact_level
            })
        
        return self._create_response(data={
            "events": events_data,
            "query_period_days": days_back,
            "total_events": len(events_data),
            "last_updated": datetime.now().isoformat()
        })
    
    def simulate_market_event(self, event_type: str, severity: str) -> APIResponse:
        """Simulate a market event for testing purposes"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error="Failed to simulate market event")
        
        # Generate new market event
        event_id = f"SIM{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        event_descriptions = {
            "VOLATILITY": "Simulated market volatility event for testing",
            "CORRECTION": "Simulated market correction for crisis response testing",
            "CRASH": "Simulated market crash for emergency protocol testing",
            "RECOVERY": "Simulated market recovery for positive sentiment testing"
        }
        
        sector_impacts = {
            "VOLATILITY": ["Technology", "Growth Stocks"],
            "CORRECTION": ["All Sectors", "High Beta Stocks"],
            "CRASH": ["All Sectors", "Equities", "Risk Assets"],
            "RECOVERY": ["Cyclical Sectors", "Small Cap"]
        }
        
        new_event = MarketEvent(
            event_id=event_id,
            event_type=event_type,
            severity=severity,
            start_time=datetime.now(),
            description=event_descriptions.get(event_type, "Simulated market event"),
            affected_sectors=sector_impacts.get(event_type, ["General Market"]),
            client_impact_level=severity.upper() if severity in ["LOW", "MODERATE", "HIGH"] else "MODERATE"
        )
        
        # Add to recent events
        self._recent_events.insert(0, new_event)
        
        return self._create_response(data={
            "simulated_event": {
                "event_id": new_event.event_id,
                "event_type": new_event.event_type,
                "severity": new_event.severity,
                "start_time": new_event.start_time.isoformat(),
                "description": new_event.description,
                "affected_sectors": new_event.affected_sectors,
                "client_impact_level": new_event.client_impact_level
            },
            "simulation_timestamp": datetime.now().isoformat(),
            "testing_note": "This is a simulated event for testing purposes"
        })
    
    def get_sector_performance(self, time_period: str = "1D") -> APIResponse:
        """Get sector performance data"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error="Failed to retrieve sector performance")
        
        # Mock sector performance data
        sectors = [
            "Technology", "Healthcare", "Financial Services", "Consumer Discretionary",
            "Consumer Staples", "Energy", "Materials", "Industrials", 
            "Real Estate", "Utilities", "Communication Services"
        ]
        
        sector_data = {}
        for sector in sectors:
            # Generate realistic performance based on time period
            if time_period == "1D":
                performance = round(random.uniform(-3.0, 3.0), 2)
            elif time_period == "1W":
                performance = round(random.uniform(-8.0, 8.0), 2)
            elif time_period == "1M":
                performance = round(random.uniform(-15.0, 15.0), 2)
            else:
                performance = round(random.uniform(-25.0, 25.0), 2)
            
            sector_data[sector] = {
                "performance_percent": performance,
                "volatility": round(random.uniform(10.0, 30.0), 2),
                "market_cap_billions": round(random.uniform(500.0, 8000.0), 0),
                "relative_strength": "STRONG" if performance > 2 else "WEAK" if performance < -2 else "NEUTRAL"
            }
        
        return self._create_response(data={
            "sector_performance": sector_data,
            "time_period": time_period,
            "analysis_timestamp": datetime.now().isoformat(),
            "benchmark": "S&P 500 Sector Indices"
        })