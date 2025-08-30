"""Mock Market Data API for realistic financial data simulation"""

import os
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from .base_api import BaseMockAPI, APIResponse

class Quote:
    """Market data quote structure"""
    def __init__(self, symbol, price, bid, ask, volume, change, change_percent, timestamp):
        self.symbol = symbol
        self.price = price
        self.bid = bid
        self.ask = ask
        self.volume = volume
        self.change = change
        self.change_percent = change_percent
        self.timestamp = timestamp

class MockMarketDataAPI(BaseMockAPI):
    """Mock market data API providing realistic financial data"""
    
    def __init__(self):
        super().__init__("market_data")
        self.volatility_factor = float(os.getenv("MARKET_VOLATILITY_FACTOR", "0.02"))
        self.simulate_market_hours = os.getenv("SIMULATE_MARKET_HOURS", "true").lower() == "true"
        
        # Initialize mock price cache
        self._price_cache = {
            "AAPL": 175.50, "GOOGL": 2800.00, "MSFT": 410.25, "AMZN": 3200.00,
            "TSLA": 220.00, "NVDA": 850.00, "META": 325.00, "BRK-B": 350.00,
            "JNJ": 160.00, "V": 250.00, "SPY": 450.00, "QQQ": 380.00,
            "VTI": 240.00, "BND": 80.00, "GLD": 185.00, "TLT": 95.00
        }
    
    def get_quote(self, symbol):
        """Get real-time quote for a symbol"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error="Failed to fetch quote for " + symbol)
        
        if symbol not in self._price_cache:
            return self._create_response(error="Symbol " + symbol + " not found")
        
        current_price = self._price_cache[symbol]
        new_price = self._generate_realistic_price_movement(current_price, self.volatility_factor)
        self._price_cache[symbol] = new_price
        
        # Calculate bid/ask spread (typically 0.01-0.05%)
        spread_pct = random.uniform(0.0001, 0.0005)
        spread = new_price * spread_pct
        bid = new_price - spread/2
        ask = new_price + spread/2
        
        change = new_price - current_price
        change_percent = (change / current_price) * 100
        
        quote_data = {
            "symbol": symbol,
            "price": round(new_price, 2),
            "bid": round(bid, 2),
            "ask": round(ask, 2),
            "volume": random.randint(100000, 10000000),
            "change": round(change, 2),
            "change_percent": round(change_percent, 2),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return self._create_response(data=quote_data)
    
    def get_historical_data(self, symbol, start_date, end_date, interval="daily"):
        """Get historical price data"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error=f"Failed to fetch historical data for {symbol}")
        
        if symbol not in self._price_cache:
            return self._create_response(error=f"Symbol {symbol} not found")
        
        # Generate realistic historical data
        current_date = start_date
        data_points = []
        base_price = self._price_cache[symbol]
        
        while current_date <= end_date:
            # Random walk for historical simulation
            base_price = self._generate_realistic_price_movement(base_price, self.volatility_factor)
            
            data_points.append({
                "date": current_date.isoformat(),
                "open": round(base_price * random.uniform(0.995, 1.005), 2),
                "high": round(base_price * random.uniform(1.002, 1.015), 2),
                "low": round(base_price * random.uniform(0.985, 0.998), 2),
                "close": round(base_price, 2),
                "volume": random.randint(1000000, 50000000),
                "adj_close": round(base_price, 2)
            })
            
            current_date += timedelta(days=1)
        
        return self._create_response(data={
            "symbol": symbol,
            "interval": interval,
            "data": data_points
        })
    
    def get_market_indices(self) -> APIResponse:
        """Get major market indices"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error="Failed to fetch market indices")
        
        indices = {}
        for symbol in ["SPY", "QQQ", "DIA", "IWM"]:
            quote_response = self.get_quote(symbol)
            if quote_response.success:
                indices[symbol] = quote_response.data
        
        return self._create_response(data=indices)
    
    def get_sector_performance(self) -> APIResponse:
        """Get sector performance data"""
        self._simulate_network_delay()
        
        sectors = [
            "Technology", "Healthcare", "Financial", "Consumer Discretionary",
            "Communication Services", "Industrials", "Consumer Staples",
            "Energy", "Utilities", "Real Estate", "Materials"
        ]
        
        sector_data = []
        for sector in sectors:
            performance = random.uniform(-3.0, 3.0)  # Daily performance %
            sector_data.append({
                "sector": sector,
                "performance": round(performance, 2),
                "market_cap": random.randint(500000, 5000000),  # in millions
                "timestamp": datetime.utcnow().isoformat()
            })
        
        return self._create_response(data={"sectors": sector_data})
    
    def is_market_open(self) -> APIResponse:
        """Check if market is currently open"""
        if not self.simulate_market_hours:
            return self._create_response(data={"is_open": True, "next_open": None, "next_close": None})
        
        now = datetime.utcnow()
        # Simulate US market hours (9:30 AM - 4:00 PM ET)
        market_open = now.replace(hour=14, minute=30, second=0, microsecond=0)  # 9:30 AM ET in UTC
        market_close = now.replace(hour=21, minute=0, second=0, microsecond=0)  # 4:00 PM ET in UTC
        
        # Weekend check
        is_weekend = now.weekday() >= 5
        is_open = not is_weekend and market_open <= now <= market_close
        
        return self._create_response(data={
            "is_open": is_open,
            "next_open": market_open.isoformat() if not is_open else None,
            "next_close": market_close.isoformat() if is_open else None,
            "timezone": "UTC"
        })