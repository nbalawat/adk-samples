"""Mock Custodian API for account positions and transaction data"""

import os
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from decimal import Decimal

from .base_api import BaseMockAPI, APIResponse

@dataclass
class Position:
    """Account position structure"""
    symbol: str
    quantity: Decimal
    market_value: Decimal
    cost_basis: Decimal
    unrealized_gain_loss: Decimal
    last_updated: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Transaction:
    """Transaction structure"""
    transaction_id: str
    account_id: str
    symbol: str
    transaction_type: str  # BUY, SELL, DIVIDEND, INTEREST, FEE
    quantity: Decimal
    price: Decimal
    amount: Decimal
    settlement_date: datetime
    trade_date: datetime
    description: str

class MockCustodianAPI(BaseMockAPI):
    """Mock custodian API for account and position management"""
    
    def __init__(self):
        super().__init__("custodian_api")
        
        # Initialize mock account data
        self._accounts = {}
        self._positions = {}
        self._transactions = {}
        self._initialize_mock_accounts()
    
    def _initialize_mock_accounts(self):
        """Initialize some mock accounts with positions"""
        sample_accounts = [
            f"WM{str(i).zfill(6)}" for i in range(100001, 100021)
        ]
        # Add common test account IDs for easy testing
        sample_accounts.extend(["TEST001", "DEMO001", "CLIENT001"])
        
        sample_symbols = ["AAPL", "GOOGL", "MSFT", "SPY", "BND", "VTI", "QQQ"]
        
        for account_id in sample_accounts:
            self._accounts[account_id] = {
                "account_id": account_id,
                "account_type": random.choice(["INDIVIDUAL", "JOINT", "IRA", "ROTH_IRA", "401K"]),
                "status": "ACTIVE",
                "cash_balance": Decimal(str(random.randint(1000, 100000))),
                "total_value": Decimal("0"),
                "created_date": datetime.utcnow() - timedelta(days=random.randint(30, 1000))
            }
            
            # Create random positions
            num_positions = random.randint(3, 8)
            account_positions = []
            
            for _ in range(num_positions):
                symbol = random.choice(sample_symbols)
                quantity = Decimal(str(random.randint(10, 1000)))
                cost_basis = Decimal(str(random.uniform(50.0, 500.0)))
                market_value = cost_basis * Decimal(str(random.uniform(0.8, 1.5)))
                
                position = Position(
                    symbol=symbol,
                    quantity=quantity,
                    market_value=market_value * quantity,
                    cost_basis=cost_basis * quantity,
                    unrealized_gain_loss=(market_value - cost_basis) * quantity
                )
                account_positions.append(position)
            
            self._positions[account_id] = account_positions
            
            # Update total account value
            total_positions_value = sum(pos.market_value for pos in account_positions)
            self._accounts[account_id]["total_value"] = (
                self._accounts[account_id]["cash_balance"] + total_positions_value
            )
    
    def get_account_info(self, account_id: str) -> APIResponse:
        """Get account information"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error=f"Failed to fetch account info for {account_id}")
        
        if account_id not in self._accounts:
            return self._create_response(error=f"Account {account_id} not found")
        
        account_data = self._accounts[account_id].copy()
        account_data["cash_balance"] = float(account_data["cash_balance"])
        account_data["total_value"] = float(account_data["total_value"])
        
        return self._create_response(data=account_data)
    
    def get_positions(self, account_id: str) -> APIResponse:
        """Get account positions"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error=f"Failed to fetch positions for {account_id}")
        
        if account_id not in self._positions:
            return self._create_response(error=f"Account {account_id} not found")
        
        positions_data = []
        for position in self._positions[account_id]:
            positions_data.append({
                "symbol": position.symbol,
                "quantity": float(position.quantity),
                "market_value": float(position.market_value),
                "cost_basis": float(position.cost_basis),
                "unrealized_gain_loss": float(position.unrealized_gain_loss),
                "last_updated": position.last_updated.isoformat()
            })
        
        return self._create_response(data={
            "account_id": account_id,
            "positions": positions_data,
            "total_market_value": sum(float(pos.market_value) for pos in self._positions[account_id]),
            "as_of_date": datetime.utcnow().isoformat()
        })
    
    def get_transactions(
        self, 
        account_id: str, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        transaction_type: Optional[str] = None
    ) -> APIResponse:
        """Get account transactions"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error=f"Failed to fetch transactions for {account_id}")
        
        if account_id not in self._accounts:
            return self._create_response(error=f"Account {account_id} not found")
        
        # Generate mock transactions
        if account_id not in self._transactions:
            self._transactions[account_id] = self._generate_mock_transactions(account_id)
        
        transactions = self._transactions[account_id]
        
        # Apply filters
        if start_date:
            transactions = [t for t in transactions if t.trade_date >= start_date]
        if end_date:
            transactions = [t for t in transactions if t.trade_date <= end_date]
        if transaction_type:
            transactions = [t for t in transactions if t.transaction_type == transaction_type]
        
        # Convert to dict format
        transactions_data = []
        for txn in transactions:
            transactions_data.append({
                "transaction_id": txn.transaction_id,
                "account_id": txn.account_id,
                "symbol": txn.symbol,
                "transaction_type": txn.transaction_type,
                "quantity": float(txn.quantity),
                "price": float(txn.price),
                "amount": float(txn.amount),
                "settlement_date": txn.settlement_date.isoformat(),
                "trade_date": txn.trade_date.isoformat(),
                "description": txn.description
            })
        
        return self._create_response(data={
            "account_id": account_id,
            "transactions": transactions_data,
            "count": len(transactions_data)
        })
    
    def _generate_mock_transactions(self, account_id: str) -> List[Transaction]:
        """Generate realistic mock transactions for an account"""
        transactions = []
        num_transactions = random.randint(20, 100)
        
        for i in range(num_transactions):
            trade_date = datetime.utcnow() - timedelta(days=random.randint(1, 365))
            settlement_date = trade_date + timedelta(days=2)  # T+2 settlement
            
            transaction_type = random.choice(["BUY", "SELL", "DIVIDEND", "INTEREST", "FEE"])
            symbol = random.choice(["AAPL", "GOOGL", "MSFT", "SPY", "BND", "VTI", "QQQ", "CASH"])
            
            if transaction_type in ["BUY", "SELL"]:
                quantity = Decimal(str(random.randint(1, 100)))
                price = Decimal(str(random.uniform(50.0, 500.0)))
                amount = quantity * price * (-1 if transaction_type == "BUY" else 1)
                description = f"{transaction_type} {quantity} shares of {symbol}"
            elif transaction_type == "DIVIDEND":
                quantity = Decimal("0")
                price = Decimal("0")
                amount = Decimal(str(random.uniform(10.0, 1000.0)))
                description = f"Dividend payment from {symbol}"
            elif transaction_type == "INTEREST":
                quantity = Decimal("0")
                price = Decimal("0")
                amount = Decimal(str(random.uniform(1.0, 100.0)))
                description = "Interest payment"
            else:  # FEE
                quantity = Decimal("0")
                price = Decimal("0")
                amount = Decimal(str(random.uniform(-50.0, -5.0)))
                description = "Management fee"
            
            transaction = Transaction(
                transaction_id=self._generate_mock_transaction_id(),
                account_id=account_id,
                symbol=symbol,
                transaction_type=transaction_type,
                quantity=quantity,
                price=price,
                amount=amount,
                settlement_date=settlement_date,
                trade_date=trade_date,
                description=description
            )
            transactions.append(transaction)
        
        return sorted(transactions, key=lambda x: x.trade_date, reverse=True)
    
    def create_account(self, account_data: Dict[str, Any]) -> APIResponse:
        """Create a new account"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error="Failed to create account")
        
        account_id = self._generate_mock_account_id()
        
        self._accounts[account_id] = {
            "account_id": account_id,
            "account_type": account_data.get("account_type", "INDIVIDUAL"),
            "status": "ACTIVE",
            "cash_balance": Decimal("0"),
            "total_value": Decimal("0"),
            "created_date": datetime.utcnow()
        }
        
        self._positions[account_id] = []
        
        return self._create_response(data={"account_id": account_id, "status": "created"})