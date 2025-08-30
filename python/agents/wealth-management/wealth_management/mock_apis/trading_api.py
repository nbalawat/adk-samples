"""Mock Trading API for order management and execution simulation"""

import os
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal

from .base_api import BaseMockAPI, APIResponse

class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"

class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderStatus(Enum):
    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"
    PARTIAL_FILL = "PARTIAL_FILL"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"

@dataclass
class Order:
    """Trading order structure"""
    order_id: str
    account_id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: Decimal
    price: Optional[Decimal]
    stop_price: Optional[Decimal]
    status: OrderStatus
    filled_quantity: Decimal
    avg_fill_price: Decimal
    submitted_time: datetime
    last_update_time: datetime
    expiration_time: Optional[datetime]

class MockTradingAPI(BaseMockAPI):
    """Mock trading API for order management and execution"""
    
    def __init__(self):
        super().__init__("trading_api")
        self.execution_delay_ms = int(os.getenv("TRADE_EXECUTION_DELAY_MS", "500"))
        self.simulate_slippage = os.getenv("SIMULATE_SLIPPAGE", "true").lower() == "true"
        self.max_order_size = int(os.getenv("MAX_ORDER_SIZE", "1000000"))
        
        # Initialize order storage
        self._orders = {}
        self._next_order_id = 1000001
    
    def submit_order(self, order_data: Dict[str, Any]) -> APIResponse:
        """Submit a new trading order"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error="Trading system temporarily unavailable")
        
        # Validate order data
        validation_error = self._validate_order_data(order_data)
        if validation_error:
            return self._create_response(error=validation_error)
        
        order_id = f"ORD{self._next_order_id}"
        self._next_order_id += 1
        
        order = Order(
            order_id=order_id,
            account_id=order_data["account_id"],
            symbol=order_data["symbol"],
            side=OrderSide(order_data["side"]),
            order_type=OrderType(order_data["order_type"]),
            quantity=Decimal(str(order_data["quantity"])),
            price=Decimal(str(order_data.get("price", 0))) if order_data.get("price") else None,
            stop_price=Decimal(str(order_data.get("stop_price", 0))) if order_data.get("stop_price") else None,
            status=OrderStatus.SUBMITTED,
            filled_quantity=Decimal("0"),
            avg_fill_price=Decimal("0"),
            submitted_time=datetime.utcnow(),
            last_update_time=datetime.utcnow(),
            expiration_time=None
        )
        
        # Set expiration for day orders
        if order_data.get("time_in_force") == "DAY":
            order.expiration_time = datetime.utcnow().replace(hour=21, minute=0, second=0)  # 4 PM ET
        
        self._orders[order_id] = order
        
        # Simulate order processing in background
        self._process_order_async(order_id)
        
        return self._create_response(data={
            "order_id": order_id,
            "status": order.status.value,
            "message": f"Order {order_id} submitted successfully"
        })
    
    def get_order_status(self, order_id: str) -> APIResponse:
        """Get status of a specific order"""
        self._simulate_network_delay()
        
        if order_id not in self._orders:
            return self._create_response(error=f"Order {order_id} not found")
        
        order = self._orders[order_id]
        
        return self._create_response(data={
            "order_id": order.order_id,
            "account_id": order.account_id,
            "symbol": order.symbol,
            "side": order.side.value,
            "order_type": order.order_type.value,
            "quantity": float(order.quantity),
            "price": float(order.price) if order.price else None,
            "stop_price": float(order.stop_price) if order.stop_price else None,
            "status": order.status.value,
            "filled_quantity": float(order.filled_quantity),
            "avg_fill_price": float(order.avg_fill_price),
            "submitted_time": order.submitted_time.isoformat(),
            "last_update_time": order.last_update_time.isoformat(),
            "expiration_time": order.expiration_time.isoformat() if order.expiration_time else None
        })
    
    def cancel_order(self, order_id: str) -> APIResponse:
        """Cancel a pending order"""
        self._simulate_network_delay()
        
        if order_id not in self._orders:
            return self._create_response(error=f"Order {order_id} not found")
        
        order = self._orders[order_id]
        
        if order.status in [OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.REJECTED]:
            return self._create_response(error=f"Cannot cancel order {order_id} with status {order.status.value}")
        
        order.status = OrderStatus.CANCELLED
        order.last_update_time = datetime.utcnow()
        
        return self._create_response(data={
            "order_id": order_id,
            "status": order.status.value,
            "message": f"Order {order_id} cancelled successfully"
        })
    
    def get_account_orders(self, account_id: str, status_filter: Optional[str] = None) -> APIResponse:
        """Get all orders for an account"""
        self._simulate_network_delay()
        
        account_orders = [
            order for order in self._orders.values() 
            if order.account_id == account_id
        ]
        
        if status_filter:
            account_orders = [
                order for order in account_orders 
                if order.status.value == status_filter
            ]
        
        orders_data = []
        for order in account_orders:
            orders_data.append({
                "order_id": order.order_id,
                "symbol": order.symbol,
                "side": order.side.value,
                "order_type": order.order_type.value,
                "quantity": float(order.quantity),
                "price": float(order.price) if order.price else None,
                "status": order.status.value,
                "filled_quantity": float(order.filled_quantity),
                "avg_fill_price": float(order.avg_fill_price),
                "submitted_time": order.submitted_time.isoformat()
            })
        
        return self._create_response(data={
            "account_id": account_id,
            "orders": orders_data,
            "count": len(orders_data)
        })
    
    def _validate_order_data(self, order_data: Dict[str, Any]) -> Optional[str]:
        """Validate order data"""
        required_fields = ["account_id", "symbol", "side", "order_type", "quantity"]
        
        for field in required_fields:
            if field not in order_data:
                return f"Missing required field: {field}"
        
        try:
            side = OrderSide(order_data["side"])
            order_type = OrderType(order_data["order_type"])
            quantity = Decimal(str(order_data["quantity"]))
        except (ValueError, KeyError) as e:
            return f"Invalid order data: {e}"
        
        if quantity <= 0:
            return "Quantity must be positive"
        
        if float(quantity) > self.max_order_size:
            return f"Order size exceeds maximum limit of {self.max_order_size}"
        
        # Validate price for limit orders
        if order_type in [OrderType.LIMIT, OrderType.STOP_LIMIT]:
            if "price" not in order_data or not order_data["price"]:
                return "Price required for limit orders"
            
            try:
                price = Decimal(str(order_data["price"]))
                if price <= 0:
                    return "Price must be positive"
            except ValueError:
                return "Invalid price format"
        
        # Validate stop price for stop orders
        if order_type in [OrderType.STOP, OrderType.STOP_LIMIT]:
            if "stop_price" not in order_data or not order_data["stop_price"]:
                return "Stop price required for stop orders"
            
            try:
                stop_price = Decimal(str(order_data["stop_price"]))
                if stop_price <= 0:
                    return "Stop price must be positive"
            except ValueError:
                return "Invalid stop price format"
        
        return None
    
    def _process_order_async(self, order_id: str) -> None:
        """Simulate asynchronous order processing"""
        order = self._orders[order_id]
        
        # Simulate processing delay
        processing_delay = random.uniform(0.1, 2.0)  # 100ms to 2 seconds
        
        # Determine if order should be filled (95% fill rate for market orders)
        fill_probability = 0.95 if order.order_type == OrderType.MARKET else 0.85
        
        if random.random() < fill_probability:
            # Simulate full fill
            order.status = OrderStatus.FILLED
            order.filled_quantity = order.quantity
            
            # Calculate fill price with potential slippage
            if order.order_type == OrderType.MARKET:
                # Market order - use current market price with slippage
                base_price = self._get_mock_market_price(order.symbol)
                if self.simulate_slippage:
                    slippage_factor = random.uniform(0.9995, 1.0005)  # ±0.05% slippage
                    if order.side == OrderSide.BUY:
                        order.avg_fill_price = base_price * Decimal(str(slippage_factor))
                    else:  # SELL
                        order.avg_fill_price = base_price * Decimal(str(2 - slippage_factor))
                else:
                    order.avg_fill_price = base_price
            else:
                # Limit order - fill at limit price or better
                order.avg_fill_price = order.price
        else:
            # Order not filled (e.g., limit price not reached)
            if order.order_type != OrderType.MARKET:
                order.status = OrderStatus.PENDING
            else:
                order.status = OrderStatus.REJECTED
        
        order.last_update_time = datetime.utcnow()
    
    def _get_mock_market_price(self, symbol: str) -> Decimal:
        """Get mock current market price for a symbol"""
        # Simple mock prices - in real implementation would call market data API
        mock_prices = {
            "AAPL": 175.50, "GOOGL": 2800.00, "MSFT": 410.25, "AMZN": 3200.00,
            "TSLA": 220.00, "NVDA": 850.00, "META": 325.00, "SPY": 450.00
        }
        
        base_price = mock_prices.get(symbol, 100.0)
        # Add some random movement
        movement = random.uniform(0.995, 1.005)
        return Decimal(str(base_price * movement))
    
    def get_trading_hours(self) -> APIResponse:
        """Get current trading hours status"""
        self._simulate_network_delay()
        
        now = datetime.utcnow()
        market_open = now.replace(hour=14, minute=30, second=0, microsecond=0)  # 9:30 AM ET
        market_close = now.replace(hour=21, minute=0, second=0, microsecond=0)  # 4:00 PM ET
        
        is_weekend = now.weekday() >= 5
        is_open = not is_weekend and market_open <= now <= market_close
        
        return self._create_response(data={
            "is_open": is_open,
            "market_open": market_open.isoformat(),
            "market_close": market_close.isoformat(),
            "timezone": "UTC",
            "session": "REGULAR" if is_open else "CLOSED"
        })