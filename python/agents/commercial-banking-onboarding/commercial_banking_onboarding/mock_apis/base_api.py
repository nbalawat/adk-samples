"""
Base mock API infrastructure for commercial banking onboarding.
Based on wealth management patterns with banking-specific adaptations.
"""

import os
import time
import random
import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResponseStatus(Enum):
    """API response status enumeration"""
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    MAINTENANCE = "maintenance"

@dataclass
class APIResponse:
    """Standard API response structure for all mock APIs"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    timestamp: Optional[datetime] = None
    response_time_ms: Optional[int] = None
    api_version: str = "v1.0"
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class BaseMockAPI:
    """
    Base class for all commercial banking mock APIs.
    Provides common functionality for realistic API simulation.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.enabled = os.getenv(f"MOCK_{name.upper()}_ENABLED", "true").lower() == "true"
        self.delay_ms = int(os.getenv(f"{name.upper()}_DELAY_MS", "200"))
        self.failure_rate = float(os.getenv(f"{name.upper()}_FAILURE_RATE", "0.02"))
        self.maintenance_mode = os.getenv(f"{name.upper()}_MAINTENANCE", "false").lower() == "true"
        
        # Initialize request tracking
        self.request_count = 0
        self.error_count = 0
        self.last_request_time = None
        
        logger.info(f"Initialized {name} mock API - Enabled: {self.enabled}, Delay: {self.delay_ms}ms")
    
    def _simulate_network_delay(self) -> None:
        """Simulate realistic network latency"""
        if self.delay_ms > 0:
            # Add some randomness to delay (±20%)
            actual_delay = self.delay_ms + random.randint(-self.delay_ms//5, self.delay_ms//5)
            time.sleep(max(actual_delay, 0) / 1000.0)
    
    def _simulate_occasional_failure(self, failure_rate: Optional[float] = None) -> bool:
        """Simulate occasional API failures based on failure rate"""
        rate = failure_rate or self.failure_rate
        return random.random() < rate
    
    def _simulate_rate_limiting(self) -> bool:
        """Simulate API rate limiting"""
        current_time = time.time()
        
        if self.last_request_time and (current_time - self.last_request_time) < 0.1:
            # Too many requests too quickly
            return True
            
        self.last_request_time = current_time
        return False
    
    def _create_response(
        self, 
        data: Optional[Dict[str, Any]] = None, 
        error: Optional[str] = None,
        error_code: Optional[str] = None
    ) -> APIResponse:
        """Create standardized API response"""
        start_time = time.time()
        self._simulate_network_delay()
        response_time = int((time.time() - start_time) * 1000)
        
        self.request_count += 1
        if error:
            self.error_count += 1
        
        return APIResponse(
            success=error is None,
            data=data,
            error=error,
            error_code=error_code,
            response_time_ms=response_time
        )
    
    def _check_api_availability(self) -> Optional[APIResponse]:
        """Check if API is available (not in maintenance, not rate limited, etc.)"""
        if not self.enabled:
            return self._create_response(
                error="API is disabled",
                error_code="API_DISABLED"
            )
        
        if self.maintenance_mode:
            return self._create_response(
                error="API is under maintenance",
                error_code="MAINTENANCE_MODE"
            )
        
        if self._simulate_rate_limiting():
            return self._create_response(
                error="Rate limit exceeded",
                error_code="RATE_LIMITED"
            )
        
        if self._simulate_occasional_failure():
            return self._create_response(
                error="Internal API error occurred",
                error_code="INTERNAL_ERROR"
            )
        
        return None  # API is available
    
    def get_api_stats(self) -> Dict[str, Any]:
        """Get API usage statistics"""
        return {
            "api_name": self.name,
            "enabled": self.enabled,
            "total_requests": self.request_count,
            "error_count": self.error_count,
            "success_rate": (self.request_count - self.error_count) / max(self.request_count, 1),
            "average_delay_ms": self.delay_ms,
            "maintenance_mode": self.maintenance_mode,
            "last_request_time": self.last_request_time
        }

class MockDataGenerator:
    """Utility class for generating realistic mock data"""
    
    # Common business entity types
    ENTITY_TYPES = [
        "LLC", "Corporation", "Partnership", "Sole Proprietorship", 
        "S-Corporation", "Limited Partnership", "Professional Corporation"
    ]
    
    # Common business industries
    INDUSTRIES = [
        "Technology", "Healthcare", "Manufacturing", "Retail", "Finance",
        "Real Estate", "Construction", "Professional Services", "Restaurant",
        "Transportation", "Agriculture", "Education", "Entertainment"
    ]
    
    # US states for address generation
    STATES = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
    ]
    
    # Risk rating levels
    RISK_LEVELS = ["Low", "Medium-Low", "Medium", "Medium-High", "High"]
    
    @staticmethod
    def generate_business_name() -> str:
        """Generate realistic business name"""
        prefixes = ["Advanced", "Global", "Premier", "Elite", "Strategic", "Dynamic", "Innovative"]
        business_types = ["Solutions", "Systems", "Technologies", "Services", "Consulting", "Group", "Partners"]
        suffixes = ["LLC", "Inc", "Corp", "Partners", "Associates"]
        
        prefix = random.choice(prefixes)
        business_type = random.choice(business_types)
        suffix = random.choice(suffixes)
        
        return f"{prefix} {business_type} {suffix}"
    
    @staticmethod
    def generate_tax_id() -> str:
        """Generate realistic EIN (Employer Identification Number)"""
        # Format: XX-XXXXXXX
        return f"{random.randint(10, 99)}-{random.randint(1000000, 9999999)}"
    
    @staticmethod
    def generate_address() -> Dict[str, str]:
        """Generate realistic business address"""
        street_numbers = range(100, 9999)
        street_names = ["Main St", "Oak Ave", "Park Blvd", "First St", "Market St", "Broadway", "Center Ave"]
        cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio"]
        
        return {
            "street": f"{random.choice(street_numbers)} {random.choice(street_names)}",
            "city": random.choice(cities),
            "state": random.choice(MockDataGenerator.STATES),
            "zip_code": f"{random.randint(10000, 99999)}"
        }
    
    @staticmethod
    def generate_credit_score() -> int:
        """Generate realistic business credit score"""
        # Business credit scores typically range from 0-100
        # Weight towards higher scores for approved applications
        weights = [0.05, 0.15, 0.3, 0.35, 0.15]  # Low to high score probability
        score_ranges = [(0, 20), (21, 40), (41, 60), (61, 80), (81, 100)]
        
        selected_range = random.choices(score_ranges, weights=weights)[0]
        return random.randint(selected_range[0], selected_range[1])
    
    @staticmethod
    def generate_financial_metrics() -> Dict[str, Any]:
        """Generate realistic financial metrics"""
        annual_revenue = random.randint(100000, 50000000)  # $100K to $50M
        
        return {
            "annual_revenue": annual_revenue,
            "monthly_revenue": annual_revenue // 12,
            "gross_margin_percent": random.randint(20, 60),
            "net_margin_percent": random.randint(5, 25),
            "current_ratio": round(random.uniform(1.0, 3.5), 2),
            "debt_to_equity_ratio": round(random.uniform(0.1, 2.0), 2),
            "cash_flow": random.randint(10000, annual_revenue // 10),
            "employees": random.randint(1, 500)
        }
    
    @staticmethod
    def generate_compliance_flags() -> List[Dict[str, Any]]:
        """Generate potential compliance flags for testing"""
        flag_types = [
            "sanctions_match", "pep_match", "adverse_media", "high_risk_jurisdiction",
            "unusual_ownership", "cash_intensive_business", "regulatory_action"
        ]
        
        flags = []
        # Most applications have no flags, some have 1-2
        if random.random() < 0.1:  # 10% chance of flags
            num_flags = random.choices([1, 2, 3], weights=[0.7, 0.2, 0.1])[0]
            
            for _ in range(num_flags):
                flag_type = random.choice(flag_types)
                flags.append({
                    "flag_type": flag_type,
                    "severity": random.choice(["Low", "Medium", "High"]),
                    "description": f"Potential {flag_type.replace('_', ' ')} detected",
                    "requires_review": flag_type in ["sanctions_match", "pep_match"],
                    "confidence_score": random.randint(60, 95)
                })
        
        return flags