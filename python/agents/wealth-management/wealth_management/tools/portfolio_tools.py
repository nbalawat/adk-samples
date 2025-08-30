"""Tools for portfolio dashboard agent with context management"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from google.adk.tools import ToolContext
from ..mock_apis import MockCustodianAPI, MockMarketDataAPI
from ..shared_libraries import PortfolioAnalyzer, FinancialCalculator
from .memory_tools import get_current_account, remember_account


def get_portfolio_summary(account_id: Optional[str] = None, tool_context: ToolContext = None) -> dict:
    """
    Get comprehensive portfolio summary for client dashboard.
    Automatically uses remembered account if no account_id provided.
    
    Args:
        account_id: Optional account identifier (uses remembered account if not provided)
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary with portfolio summary information
    """
    # Use context-aware account resolution
    if not account_id and tool_context:
        account_context = get_current_account(tool_context)
        if account_context["status"] == "SUCCESS":
            account_id = account_context["account_id"]
        else:
            return {
                "status": "ERROR",
                "message": "No account specified and no account remembered. Please provide an account ID or say something like 'use account TEST001'.",
                "available_accounts": account_context.get("available_accounts", [])
            }
    
    # Remember this account for future use
    if account_id and tool_context:
        remember_account(account_id, tool_context)
    custodian_api = MockCustodianAPI()
    market_api = MockMarketDataAPI()
    
    # Get account information
    account_response = custodian_api.get_account_info(account_id)
    if not account_response.success:
        return {
            "status": "ERROR",
            "message": f"Failed to retrieve account information: {account_response.error}"
        }
    
    account_info = account_response.data
    
    # Get current positions
    positions_response = custodian_api.get_positions(account_id)
    if not positions_response.success:
        return {
            "status": "ERROR", 
            "message": f"Failed to retrieve positions: {positions_response.error}"
        }
    
    positions_data = positions_response.data
    positions = positions_data.get("positions", [])
    
    # Calculate portfolio metrics
    portfolio_performance = PortfolioAnalyzer.calculate_portfolio_performance(positions)
    
    # Get market context
    market_indices = market_api.get_market_indices()
    market_status = market_api.is_market_open()
    
    # Calculate daily change (mock calculation)
    total_value = portfolio_performance.get("total_market_value", 0)
    daily_change = total_value * 0.01  # Mock 1% daily change
    daily_change_pct = 1.0 if total_value > 0 else 0.0
    
    summary = {
        "account_id": account_id,
        "total_value": f"${total_value:,.2f}",
        "daily_change": f"${daily_change:+,.2f}",
        "daily_change_pct": f"{daily_change_pct:+.2f}%",
        "cash_balance": f"${account_info.get('cash_balance', 0):,.2f}" if account_info else "$0.00",
        "total_gain_loss": f"${portfolio_performance.get('total_gain_loss', 0):+,.2f}",
        "total_return_pct": f"{portfolio_performance.get('total_return', 0) * 100:+.2f}%",
        "num_positions": str(portfolio_performance.get("num_positions", 0)),
        "market_open": str(market_status.data.get("is_open", False)) if market_status.success else "unknown",
        "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }
    
    return {
        "status": "SUCCESS",
        "message": "Portfolio summary retrieved successfully",
        **summary
    }


def get_position_details(symbol: str, account_id: Optional[str] = None, tool_context: ToolContext = None) -> dict:
    """
    Get detailed information about a specific position.
    Automatically uses remembered account if no account_id provided.
    
    Args:
        symbol: Stock/security symbol
        account_id: Optional account identifier (uses remembered account if not provided)
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary with position details
    """
    # Use context-aware account resolution
    if not account_id and tool_context:
        account_context = get_current_account(tool_context)
        if account_context["status"] == "SUCCESS":
            account_id = account_context["account_id"]
        else:
            return {
                "status": "ERROR",
                "message": f"No account specified for {symbol} position lookup. Please provide an account ID.",
                "available_accounts": account_context.get("available_accounts", [])
            }
    # Get fresh positions data
    custodian_api = MockCustodianAPI()
    positions_response = custodian_api.get_positions(account_id)
    if not positions_response.success:
        return {
            "status": "ERROR",
            "message": f"Failed to retrieve positions: {positions_response.error}"
        }
    positions = positions_response.data.get("positions", [])
    
    # Find the specific position
    position = None
    for pos in positions:
        if pos.get("symbol") == symbol:
            position = pos
            break
    
    if not position:
        return {
            "status": "ERROR",
            "message": f"Position {symbol} not found in account {account_id}"
        }
    
    # Get current market data
    market_api = MockMarketDataAPI()
    quote_response = market_api.get_quote(symbol)
    current_price = 0
    daily_change = 0
    daily_change_pct = 0
    
    if quote_response.success:
        quote_data = quote_response.data
        current_price = quote_data.get("price", 0)
        daily_change = quote_data.get("change", 0)
        daily_change_pct = quote_data.get("change_percent", 0)
    
    # Calculate position metrics
    quantity = position.get("quantity", 0)
    market_value = position.get("market_value", 0)
    cost_basis = position.get("cost_basis", 0)
    unrealized_gain_loss = market_value - cost_basis
    unrealized_pct = (unrealized_gain_loss / cost_basis * 100) if cost_basis > 0 else 0
    avg_cost = cost_basis / quantity if quantity > 0 else 0
    
    return {
        "status": "SUCCESS",
        "symbol": symbol,
        "quantity": f"{quantity:,.0f}",
        "current_price": f"${current_price:.2f}",
        "market_value": f"${market_value:,.2f}",
        "cost_basis": f"${cost_basis:,.2f}",
        "avg_cost": f"${avg_cost:.2f}",
        "unrealized_gain_loss": f"${unrealized_gain_loss:+,.2f}",
        "unrealized_pct": f"{unrealized_pct:+.2f}%",
        "daily_change": f"${daily_change:+.2f}",
        "daily_change_pct": f"{daily_change_pct:+.2f}%",
        "message": f"Position details for {symbol} retrieved successfully"
    }


def calculate_performance_metrics(period: str = "1Y", account_id: Optional[str] = None, tool_context: ToolContext = None) -> dict:
    """
    Calculate portfolio performance metrics over specified period.
    Automatically uses remembered account if no account_id provided.
    
    Args:
        period: Time period for analysis (1M, 3M, 6M, 1Y, 3Y, 5Y)
        account_id: Optional account identifier (uses remembered account if not provided)
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary with performance metrics
    """
    # Use context-aware account resolution
    if not account_id and tool_context:
        account_context = get_current_account(tool_context)
        if account_context["status"] == "SUCCESS":
            account_id = account_context["account_id"]
        else:
            return {
                "status": "ERROR",
                "message": f"No account specified for {period} performance analysis. Please provide an account ID.",
                "available_accounts": account_context.get("available_accounts", [])
            }
    custodian_api = MockCustodianAPI()
    
    # Get account transactions for performance calculation
    try:
        transactions_response = custodian_api.get_transactions(account_id)
        if not transactions_response.success:
            return {
                "status": "ERROR",
                "message": f"Failed to retrieve transactions: {transactions_response.error}"
            }
        
        transactions = transactions_response.data.get("transactions", [])
        
        # Get current positions
        positions_response = custodian_api.get_positions(account_id)
        if not positions_response.success:
            return {
                "status": "ERROR",
                "message": f"Failed to retrieve positions: {positions_response.error}"
            }
        
        positions = positions_response.data.get("positions", [])
        
        # Mock performance metrics based on period (removed FinancialCalculator dependency)
        period_multiplier = {"1M": 1, "3M": 3, "6M": 6, "1Y": 12, "3Y": 36, "5Y": 60}.get(period, 12)
        
        # Mock calculations
        total_return = 0.08 * (period_multiplier / 12)  # 8% annualized
        volatility = 0.15
        sharpe_ratio = total_return / volatility if volatility > 0 else 0
        max_drawdown = -0.05 * (period_multiplier / 12)
        
        return {
            "status": "SUCCESS",
            "account_id": account_id,
            "period": period,
            "total_return": f"{total_return * 100:+.2f}%",
            "annualized_return": f"{(total_return / (period_multiplier / 12)) * 100:+.2f}%",
            "volatility": f"{volatility * 100:.2f}%",
            "sharpe_ratio": f"{sharpe_ratio:.2f}",
            "max_drawdown": f"{max_drawdown * 100:+.2f}%",
            "num_transactions": str(len(transactions)),
            "num_positions": str(len(positions)),
            "message": f"Performance metrics for {period} period calculated successfully"
        }
        
    except Exception as e:
        return {
            "status": "ERROR", 
            "message": f"Error calculating performance metrics: {str(e)}"
        }


def generate_allocation_charts(account_id: Optional[str] = None, tool_context: ToolContext = None) -> dict:
    """
    Generate asset allocation charts and analysis.
    Automatically uses remembered account if no account_id provided.
    
    Args:
        account_id: Optional account identifier (uses remembered account if not provided)
        tool_context: ADK tool context for state management
        
    Returns:
        Dictionary with allocation analysis
    """
    # Use context-aware account resolution
    if not account_id and tool_context:
        account_context = get_current_account(tool_context)
        if account_context["status"] == "SUCCESS":
            account_id = account_context["account_id"]
        else:
            return {
                "status": "ERROR",
                "message": "No account specified for allocation analysis. Please provide an account ID.",
                "available_accounts": account_context.get("available_accounts", [])
            }
    custodian_api = MockCustodianAPI()
    
    # Get current positions
    positions_response = custodian_api.get_positions(account_id)
    if not positions_response.success:
        return {
            "status": "ERROR",
            "message": f"Failed to retrieve positions: {positions_response.error}"
        }
    
    positions = positions_response.data.get("positions", [])
    
    if not positions:
        return {
            "status": "SUCCESS",
            "account_id": account_id,
            "message": "No positions found for allocation analysis",
            "allocations": []
        }
    
    # Calculate allocation percentages
    total_value = sum(pos.get("market_value", 0) for pos in positions)
    
    allocations = []
    for position in positions:
        market_value = position.get("market_value", 0)
        allocation_pct = (market_value / total_value * 100) if total_value > 0 else 0
        
        allocations.append({
            "symbol": position.get("symbol", ""),
            "market_value": f"${market_value:,.2f}",
            "allocation_pct": f"{allocation_pct:.2f}%"
        })
    
    # Sort by allocation percentage descending
    allocations.sort(key=lambda x: float(x["allocation_pct"].rstrip('%')), reverse=True)
    
    return {
        "status": "SUCCESS",
        "account_id": account_id,
        "total_portfolio_value": f"${total_value:,.2f}",
        "num_positions": str(len(positions)),
        "allocations": allocations,
        "message": "Asset allocation charts generated successfully"
    }