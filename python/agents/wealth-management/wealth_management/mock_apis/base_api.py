"""Base class for mock APIs with common functionality"""

import random
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import os
import logging

logger = logging.getLogger(__name__)

@dataclass
class APIResponse:
    """Standard API response structure"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

class BaseMockAPI:
    """Base class for all mock APIs with common functionality"""
    
    def __init__(self, name: str):
        self.name = name
        self.enabled = os.getenv(f"MOCK_{name.upper()}_ENABLED", "true").lower() == "true"
        self.delay_ms = int(os.getenv(f"{name.upper()}_DELAY_MS", "100"))
        logger.info(f"Initialized {name} mock API (enabled: {self.enabled})")
    
    def _simulate_network_delay(self) -> None:
        """Simulate network latency"""
        if self.delay_ms > 0:
            time.sleep(self.delay_ms / 1000.0)
    
    def _simulate_occasional_failure(self, failure_rate: float = 0.02) -> bool:
        """Simulate occasional API failures"""
        return random.random() < failure_rate
    
    def _create_response(
        self, 
        data: Optional[Dict[str, Any]] = None, 
        error: Optional[str] = None
    ) -> APIResponse:
        """Create standardized API response"""
        return APIResponse(
            success=error is None,
            data=data,
            error=error
        )
    
    def _generate_realistic_price_movement(
        self, 
        current_price: float, 
        volatility: float = 0.02
    ) -> float:
        """Generate realistic price movements using random walk"""
        change = random.gauss(0, volatility * current_price)
        return max(0.01, current_price + change)  # Ensure positive prices
    
    def _generate_mock_account_id(self) -> str:
        """Generate realistic account ID"""
        return f"WM{random.randint(100000, 999999)}"
    
    def _generate_mock_transaction_id(self) -> str:
        """Generate realistic transaction ID"""
        return f"TXN{datetime.utcnow().strftime('%Y%m%d')}{random.randint(1000, 9999)}"