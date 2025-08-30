"""Mock Tax Service API for tax planning and calculations"""

import os
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from decimal import Decimal

from .base_api import BaseMockAPI, APIResponse

@dataclass
class TaxLot:
    """Tax lot information for cost basis tracking"""
    symbol: str
    quantity: Decimal
    purchase_date: datetime
    purchase_price: Decimal
    cost_basis: Decimal

@dataclass
class TaxDocument:
    """Tax document structure"""
    document_id: str
    document_type: str  # 1099-DIV, 1099-INT, 1099-B, etc.
    tax_year: int
    account_id: str
    data: Dict[str, Any]
    generated_date: datetime

class MockTaxServiceAPI(BaseMockAPI):
    """Mock tax service API for tax calculations and document generation"""
    
    def __init__(self):
        super().__init__("tax_service_api")
        
        # Tax rates (simplified for simulation)
        self.tax_rates = {
            "ordinary_income": {
                "brackets": [
                    (10275, 0.10), (41775, 0.12), (89450, 0.22),
                    (190750, 0.24), (364200, 0.32), (462550, 0.35), (float('inf'), 0.37)
                ]
            },
            "long_term_capital_gains": {
                "brackets": [
                    (41675, 0.0), (459750, 0.15), (float('inf'), 0.20)
                ]
            },
            "short_term_capital_gains": "ordinary_income"
        }
        
        # Initialize tax lot tracking
        self._tax_lots = {}
        self._tax_documents = {}
        self._initialize_mock_tax_lots()
    
    def _initialize_mock_tax_lots(self):
        """Initialize mock tax lots for sample accounts"""
        sample_accounts = [f"WM{str(i).zfill(6)}" for i in range(100001, 100021)]
        sample_symbols = ["AAPL", "GOOGL", "MSFT", "SPY", "BND", "VTI"]
        
        for account_id in sample_accounts:
            account_lots = []
            
            for symbol in random.sample(sample_symbols, k=random.randint(2, 5)):
                # Create multiple tax lots for each symbol
                num_lots = random.randint(1, 4)
                
                for _ in range(num_lots):
                    purchase_date = datetime.utcnow() - timedelta(days=random.randint(30, 1000))
                    quantity = Decimal(str(random.randint(10, 500)))
                    purchase_price = Decimal(str(random.uniform(50.0, 400.0)))
                    
                    tax_lot = TaxLot(
                        symbol=symbol,
                        quantity=quantity,
                        purchase_date=purchase_date,
                        purchase_price=purchase_price,
                        cost_basis=quantity * purchase_price
                    )
                    account_lots.append(tax_lot)
            
            self._tax_lots[account_id] = account_lots
    
    def calculate_capital_gains(
        self,
        account_id: str,
        symbol: str,
        quantity: Decimal,
        sale_price: Decimal,
        sale_date: Optional[datetime] = None
    ) -> APIResponse:
        """Calculate capital gains for a proposed sale"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error="Tax calculation service unavailable")
        
        if sale_date is None:
            sale_date = datetime.utcnow()
        
        if account_id not in self._tax_lots:
            return self._create_response(error=f"No tax lots found for account {account_id}")
        
        # Find tax lots for the symbol
        symbol_lots = [lot for lot in self._tax_lots[account_id] if lot.symbol == symbol]
        
        if not symbol_lots:
            return self._create_response(error=f"No tax lots found for symbol {symbol}")
        
        # Sort by purchase date (FIFO method)
        symbol_lots.sort(key=lambda x: x.purchase_date)
        
        remaining_quantity = quantity
        gains_losses = []
        total_cost_basis = Decimal("0")
        total_proceeds = quantity * sale_price
        
        for lot in symbol_lots:
            if remaining_quantity <= 0:
                break
            
            lot_quantity_used = min(remaining_quantity, lot.quantity)
            lot_cost_basis = (lot_quantity_used / lot.quantity) * lot.cost_basis
            lot_proceeds = lot_quantity_used * sale_price
            
            # Calculate holding period
            holding_days = (sale_date - lot.purchase_date).days
            is_long_term = holding_days > 365
            
            gain_loss = lot_proceeds - lot_cost_basis
            
            gains_losses.append({
                "lot_id": f"{lot.symbol}_{lot.purchase_date.strftime('%Y%m%d')}",
                "purchase_date": lot.purchase_date.isoformat(),
                "purchase_price": float(lot.purchase_price),
                "quantity_sold": float(lot_quantity_used),
                "cost_basis": float(lot_cost_basis),
                "proceeds": float(lot_proceeds),
                "gain_loss": float(gain_loss),
                "holding_period_days": holding_days,
                "term": "LONG" if is_long_term else "SHORT"
            })
            
            total_cost_basis += lot_cost_basis
            remaining_quantity -= lot_quantity_used
        
        total_gain_loss = total_proceeds - total_cost_basis
        
        # Calculate tax implications
        long_term_gain = sum(gl["gain_loss"] for gl in gains_losses if gl["term"] == "LONG")
        short_term_gain = sum(gl["gain_loss"] for gl in gains_losses if gl["term"] == "SHORT")
        
        return self._create_response(data={
            "account_id": account_id,
            "symbol": symbol,
            "quantity_sold": float(quantity),
            "sale_price": float(sale_price),
            "sale_date": sale_date.isoformat(),
            "total_proceeds": float(total_proceeds),
            "total_cost_basis": float(total_cost_basis),
            "total_gain_loss": float(total_gain_loss),
            "long_term_gain_loss": long_term_gain,
            "short_term_gain_loss": short_term_gain,
            "lot_details": gains_losses,
            "calculation_method": "FIFO"
        })
    
    def calculate_tax_liability(self, income_data: Dict[str, Any]) -> APIResponse:
        """Calculate estimated tax liability"""
        self._simulate_network_delay()
        
        ordinary_income = float(income_data.get("ordinary_income", 0))
        long_term_gains = float(income_data.get("long_term_capital_gains", 0))
        short_term_gains = float(income_data.get("short_term_capital_gains", 0))
        qualified_dividends = float(income_data.get("qualified_dividends", 0))
        filing_status = income_data.get("filing_status", "single")
        
        # Calculate ordinary income tax
        total_ordinary = ordinary_income + short_term_gains
        ordinary_tax = self._calculate_progressive_tax(
            total_ordinary, 
            self.tax_rates["ordinary_income"]["brackets"]
        )
        
        # Calculate capital gains tax
        capital_gains_income = long_term_gains + qualified_dividends
        capital_gains_tax = self._calculate_progressive_tax(
            capital_gains_income,
            self.tax_rates["long_term_capital_gains"]["brackets"]
        )
        
        total_tax = ordinary_tax + capital_gains_tax
        
        # Add state tax estimate (simplified)
        state_tax_rate = random.uniform(0.0, 0.13)  # 0-13% state tax
        estimated_state_tax = (total_ordinary + capital_gains_income) * state_tax_rate
        
        return self._create_response(data={
            "income_summary": {
                "ordinary_income": ordinary_income,
                "short_term_capital_gains": short_term_gains,
                "long_term_capital_gains": long_term_gains,
                "qualified_dividends": qualified_dividends,
                "total_income": ordinary_income + short_term_gains + long_term_gains + qualified_dividends
            },
            "tax_calculation": {
                "federal_ordinary_tax": ordinary_tax,
                "federal_capital_gains_tax": capital_gains_tax,
                "total_federal_tax": total_tax,
                "estimated_state_tax": estimated_state_tax,
                "total_estimated_tax": total_tax + estimated_state_tax,
                "effective_tax_rate": ((total_tax + estimated_state_tax) / 
                                     (ordinary_income + short_term_gains + long_term_gains + qualified_dividends)) * 100
            },
            "filing_status": filing_status,
            "calculation_date": datetime.utcnow().isoformat()
        })
    
    def _calculate_progressive_tax(self, income: float, brackets: List[tuple]) -> float:
        """Calculate tax using progressive brackets"""
        total_tax = 0.0
        remaining_income = income
        previous_bracket = 0
        
        for bracket_limit, rate in brackets:
            if remaining_income <= 0:
                break
            
            taxable_in_bracket = min(remaining_income, bracket_limit - previous_bracket)
            total_tax += taxable_in_bracket * rate
            remaining_income -= taxable_in_bracket
            previous_bracket = bracket_limit
            
            if remaining_income <= 0:
                break
        
        return total_tax
    
    def generate_tax_loss_harvest_opportunities(self, account_id: str) -> APIResponse:
        """Identify tax loss harvesting opportunities"""
        self._simulate_network_delay()
        
        if account_id not in self._tax_lots:
            return self._create_response(error=f"No tax lots found for account {account_id}")
        
        opportunities = []
        
        # Get current market prices (simulated)
        current_prices = {
            "AAPL": 175.50, "GOOGL": 2800.00, "MSFT": 410.25,
            "SPY": 450.00, "BND": 80.00, "VTI": 240.00
        }
        
        for lot in self._tax_lots[account_id]:
            current_price = current_prices.get(lot.symbol, float(lot.purchase_price) * 1.1)
            current_value = lot.quantity * Decimal(str(current_price))
            unrealized_gain_loss = current_value - lot.cost_basis
            
            # Look for losses
            if unrealized_gain_loss < 0:
                holding_days = (datetime.utcnow() - lot.purchase_date).days
                
                opportunities.append({
                    "symbol": lot.symbol,
                    "lot_id": f"{lot.symbol}_{lot.purchase_date.strftime('%Y%m%d')}",
                    "purchase_date": lot.purchase_date.isoformat(),
                    "purchase_price": float(lot.purchase_price),
                    "current_price": current_price,
                    "quantity": float(lot.quantity),
                    "cost_basis": float(lot.cost_basis),
                    "current_value": float(current_value),
                    "unrealized_loss": float(abs(unrealized_gain_loss)),
                    "holding_period_days": holding_days,
                    "term": "LONG" if holding_days > 365 else "SHORT",
                    "wash_sale_risk": holding_days < 30  # Simplified wash sale check
                })
        
        # Sort by largest losses first
        opportunities.sort(key=lambda x: x["unrealized_loss"], reverse=True)
        
        total_harvestable_losses = sum(opp["unrealized_loss"] for opp in opportunities 
                                     if not opp["wash_sale_risk"])
        
        return self._create_response(data={
            "account_id": account_id,
            "opportunities": opportunities,
            "total_opportunities": len(opportunities),
            "total_harvestable_losses": total_harvestable_losses,
            "analysis_date": datetime.utcnow().isoformat()
        })
    
    def generate_tax_document(self, account_id: str, document_type: str, tax_year: int) -> APIResponse:
        """Generate mock tax documents"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error=f"Failed to generate {document_type} for {tax_year}")
        
        document_id = f"{document_type}_{account_id}_{tax_year}"
        
        # Generate mock document data based on type
        if document_type == "1099-DIV":
            document_data = {
                "total_dividends": random.uniform(500.0, 5000.0),
                "qualified_dividends": random.uniform(400.0, 4000.0),
                "capital_gains_distributions": random.uniform(0.0, 1000.0)
            }
        elif document_type == "1099-INT":
            document_data = {
                "interest_income": random.uniform(50.0, 500.0),
                "tax_exempt_interest": random.uniform(0.0, 200.0)
            }
        elif document_type == "1099-B":
            document_data = {
                "proceeds": random.uniform(10000.0, 100000.0),
                "cost_basis": random.uniform(8000.0, 95000.0),
                "wash_sale_adjustments": random.uniform(0.0, 1000.0)
            }
        else:
            document_data = {"message": f"Document type {document_type} not implemented"}
        
        tax_document = TaxDocument(
            document_id=document_id,
            document_type=document_type,
            tax_year=tax_year,
            account_id=account_id,
            data=document_data,
            generated_date=datetime.utcnow()
        )
        
        # Store document
        if account_id not in self._tax_documents:
            self._tax_documents[account_id] = []
        self._tax_documents[account_id].append(tax_document)
        
        return self._create_response(data={
            "document_id": document_id,
            "document_type": document_type,
            "tax_year": tax_year,
            "account_id": account_id,
            "data": document_data,
            "generated_date": tax_document.generated_date.isoformat(),
            "status": "generated"
        })
    
    def get_tax_documents(self, account_id: str, tax_year: Optional[int] = None) -> APIResponse:
        """Get tax documents for an account"""
        self._simulate_network_delay()
        
        if account_id not in self._tax_documents:
            return self._create_response(data={
                "account_id": account_id,
                "documents": [],
                "count": 0
            })
        
        documents = self._tax_documents[account_id]
        
        if tax_year:
            documents = [doc for doc in documents if doc.tax_year == tax_year]
        
        documents_data = []
        for doc in documents:
            documents_data.append({
                "document_id": doc.document_id,
                "document_type": doc.document_type,
                "tax_year": doc.tax_year,
                "data": doc.data,
                "generated_date": doc.generated_date.isoformat()
            })
        
        return self._create_response(data={
            "account_id": account_id,
            "documents": documents_data,
            "count": len(documents_data),
            "tax_year_filter": tax_year
        })