"""Portfolio analysis utilities for wealth management"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from scipy.optimize import minimize
import pandas as pd


class PortfolioAnalyzer:
    """Comprehensive portfolio analysis utilities"""
    
    @staticmethod
    def calculate_portfolio_performance(
        positions: List[Dict[str, Any]],
        benchmark_returns: Optional[List[float]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Calculate comprehensive portfolio performance metrics"""
        if not positions:
            return {}
        
        # Calculate portfolio values
        total_market_value = sum(pos.get("market_value", 0) for pos in positions)
        total_cost_basis = sum(pos.get("cost_basis", 0) for pos in positions)
        
        if total_cost_basis == 0:
            return {"error": "No cost basis data available"}
        
        # Basic performance metrics
        total_return = (total_market_value - total_cost_basis) / total_cost_basis
        
        performance = {
            "total_market_value": total_market_value,
            "total_cost_basis": total_cost_basis,
            "total_return": total_return,
            "total_gain_loss": total_market_value - total_cost_basis,
            "num_positions": len(positions),
            "cash_percentage": 0,  # Would come from cash positions
            "analysis_date": datetime.utcnow().isoformat()
        }
        
        # Position-level analysis
        position_analysis = []
        for pos in positions:
            market_value = pos.get("market_value", 0)
            cost_basis = pos.get("cost_basis", 0)
            symbol = pos.get("symbol", "Unknown")
            
            if cost_basis > 0:
                position_return = (market_value - cost_basis) / cost_basis
                weight = market_value / total_market_value if total_market_value > 0 else 0
                
                position_analysis.append({
                    "symbol": symbol,
                    "market_value": market_value,
                    "cost_basis": cost_basis,
                    "weight": weight,
                    "return": position_return,
                    "gain_loss": market_value - cost_basis,
                    "quantity": pos.get("quantity", 0)
                })
        
        performance["positions"] = position_analysis
        
        # Portfolio composition analysis
        if position_analysis:
            weights = [pos["weight"] for pos in position_analysis]
            returns = [pos["return"] for pos in position_analysis]
            
            performance.update({
                "largest_position": max(weights) if weights else 0,
                "smallest_position": min(weights) if weights else 0,
                "top_5_concentration": sum(sorted(weights, reverse=True)[:5]),
                "best_performer": max(returns) if returns else 0,
                "worst_performer": min(returns) if returns else 0,
                "positive_positions": len([r for r in returns if r > 0]),
                "negative_positions": len([r for r in returns if r < 0])
            })
        
        return performance
    
    @staticmethod
    def generate_asset_allocation_analysis(
        positions: List[Dict[str, Any]],
        asset_class_mapping: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Analyze portfolio asset allocation"""
        if not positions:
            return {}
        
        total_value = sum(pos.get("market_value", 0) for pos in positions)
        
        if total_value == 0:
            return {"error": "No market value data"}
        
        # Default asset class mapping
        if asset_class_mapping is None:
            asset_class_mapping = {
                "SPY": "US Equity", "QQQ": "US Equity", "AAPL": "US Equity", 
                "GOOGL": "US Equity", "MSFT": "US Equity", "TSLA": "US Equity",
                "BND": "Fixed Income", "TLT": "Fixed Income", "AGG": "Fixed Income",
                "VTI": "US Equity", "VXUS": "International Equity", "VEA": "International Equity",
                "GLD": "Commodities", "VNQ": "Real Estate"
            }
        
        # Calculate allocations
        asset_class_values = {}
        sector_values = {}
        
        for pos in positions:
            symbol = pos.get("symbol", "Unknown")
            market_value = pos.get("market_value", 0)
            
            # Asset class allocation
            asset_class = asset_class_mapping.get(symbol, "Other")
            asset_class_values[asset_class] = asset_class_values.get(asset_class, 0) + market_value
            
            # Simple sector mapping (mock)
            sector = PortfolioAnalyzer._get_sector_for_symbol(symbol)
            sector_values[sector] = sector_values.get(sector, 0) + market_value
        
        # Convert to percentages
        asset_allocation = {
            asset_class: {"value": value, "percentage": (value / total_value) * 100}
            for asset_class, value in asset_class_values.items()
        }
        
        sector_allocation = {
            sector: {"value": value, "percentage": (value / total_value) * 100}
            for sector, value in sector_values.items()
        }
        
        return {
            "total_portfolio_value": total_value,
            "asset_class_allocation": asset_allocation,
            "sector_allocation": sector_allocation,
            "diversification_metrics": PortfolioAnalyzer._calculate_diversification_metrics(
                list(asset_class_values.values()), total_value
            )
        }
    
    @staticmethod
    def _get_sector_for_symbol(symbol: str) -> str:
        """Simple sector mapping for common symbols"""
        sector_map = {
            "AAPL": "Technology", "GOOGL": "Technology", "MSFT": "Technology",
            "TSLA": "Consumer Discretionary", "NVDA": "Technology",
            "JPM": "Financial", "BAC": "Financial", "WFC": "Financial",
            "JNJ": "Healthcare", "PFE": "Healthcare", "UNH": "Healthcare",
            "XOM": "Energy", "CVX": "Energy", "COP": "Energy",
            "SPY": "Index Fund", "QQQ": "Index Fund", "VTI": "Index Fund",
            "BND": "Fixed Income", "TLT": "Fixed Income", "AGG": "Fixed Income"
        }
        return sector_map.get(symbol, "Other")
    
    @staticmethod
    def _calculate_diversification_metrics(values: List[float], total_value: float) -> Dict[str, Any]:
        """Calculate portfolio diversification metrics"""
        if not values or total_value == 0:
            return {}
        
        weights = [v / total_value for v in values]
        
        # Herfindahl-Hirschman Index
        hhi = sum(w ** 2 for w in weights)
        
        # Effective number of assets
        effective_assets = 1 / hhi if hhi > 0 else 0
        
        return {
            "herfindahl_index": hhi,
            "effective_number_of_positions": effective_assets,
            "concentration_score": min(10, hhi * 10),  # 0-10 scale
            "diversification_ratio": 1 - hhi
        }
    
    @staticmethod
    def suggest_rebalancing(
        current_positions: List[Dict[str, Any]],
        target_allocation: Dict[str, float],
        tolerance: float = 0.05
    ) -> Dict[str, Any]:
        """Suggest portfolio rebalancing actions"""
        current_total = sum(pos.get("market_value", 0) for pos in current_positions)
        
        if current_total == 0:
            return {"error": "No current portfolio value"}
        
        # Calculate current allocation
        current_allocation = {}
        for pos in current_positions:
            symbol = pos.get("symbol", "Unknown")
            weight = pos.get("market_value", 0) / current_total
            current_allocation[symbol] = weight
        
        # Find deviations from target
        rebalancing_actions = []
        for symbol, target_weight in target_allocation.items():
            current_weight = current_allocation.get(symbol, 0)
            deviation = current_weight - target_weight
            
            if abs(deviation) > tolerance:
                target_value = target_weight * current_total
                current_value = current_weight * current_total
                adjustment_value = target_value - current_value
                
                action_type = "REDUCE" if deviation > 0 else "INCREASE"
                
                rebalancing_actions.append({
                    "symbol": symbol,
                    "action": action_type,
                    "current_weight": current_weight,
                    "target_weight": target_weight,
                    "deviation": deviation,
                    "current_value": current_value,
                    "target_value": target_value,
                    "adjustment_value": adjustment_value,
                    "priority": "HIGH" if abs(deviation) > tolerance * 2 else "MEDIUM"
                })
        
        # Sort by deviation magnitude
        rebalancing_actions.sort(key=lambda x: abs(x["deviation"]), reverse=True)
        
        return {
            "total_portfolio_value": current_total,
            "rebalancing_needed": len(rebalancing_actions) > 0,
            "tolerance_threshold": tolerance,
            "actions_required": len(rebalancing_actions),
            "rebalancing_actions": rebalancing_actions,
            "estimated_trading_cost": len(rebalancing_actions) * 9.99  # Mock trading cost
        }
    
    @staticmethod
    def calculate_optimal_allocation(
        expected_returns: List[float],
        covariance_matrix: List[List[float]],
        risk_tolerance: str = "moderate",
        constraints: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Calculate optimal portfolio allocation using mean-variance optimization"""
        if not expected_returns or not covariance_matrix:
            return {"error": "Insufficient data for optimization"}
        
        expected_returns = np.array(expected_returns)
        cov_matrix = np.array(covariance_matrix)
        n_assets = len(expected_returns)
        
        # Risk aversion parameter based on risk tolerance
        risk_aversion_map = {
            "conservative": 10,
            "moderate": 5,
            "aggressive": 2
        }
        risk_aversion = risk_aversion_map.get(risk_tolerance.lower(), 5)
        
        # Initial guess
        initial_weights = np.array([1/n_assets] * n_assets)
        
        # Objective function (maximize utility: return - 0.5 * risk_aversion * variance)
        def objective(weights):
            portfolio_return = np.dot(weights, expected_returns)
            portfolio_variance = np.dot(weights, np.dot(cov_matrix, weights))
            return -(portfolio_return - 0.5 * risk_aversion * portfolio_variance)
        
        # Constraints
        constraints_list = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
        
        # Additional constraints if provided
        if constraints:
            if "max_weight" in constraints:
                for i in range(n_assets):
                    constraints_list.append({
                        "type": "ineq", 
                        "fun": lambda w, i=i: constraints["max_weight"] - w[i]
                    })
            
            if "min_weight" in constraints:
                for i in range(n_assets):
                    constraints_list.append({
                        "type": "ineq", 
                        "fun": lambda w, i=i: w[i] - constraints["min_weight"]
                    })
        
        # Bounds (long-only portfolio)
        bounds = [(0.0, 1.0) for _ in range(n_assets)]
        
        # Optimize
        result = minimize(
            objective,
            initial_weights,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints_list,
            options={"maxiter": 1000}
        )
        
        if result.success:
            optimal_weights = result.x
            portfolio_return = np.dot(optimal_weights, expected_returns)
            portfolio_variance = np.dot(optimal_weights, np.dot(cov_matrix, optimal_weights))
            portfolio_volatility = np.sqrt(portfolio_variance)
            sharpe_ratio = portfolio_return / portfolio_volatility if portfolio_volatility > 0 else 0
            
            return {
                "success": True,
                "optimal_weights": optimal_weights.tolist(),
                "expected_return": portfolio_return,
                "expected_volatility": portfolio_volatility,
                "sharpe_ratio": sharpe_ratio,
                "risk_tolerance": risk_tolerance,
                "optimization_result": {
                    "converged": result.success,
                    "iterations": result.nit,
                    "message": result.message
                }
            }
        else:
            return {
                "success": False,
                "error": result.message,
                "fallback_weights": initial_weights.tolist()
            }
    
    @staticmethod
    def generate_efficient_frontier(
        expected_returns: List[float],
        covariance_matrix: List[List[float]],
        num_portfolios: int = 50
    ) -> Dict[str, Any]:
        """Generate efficient frontier for portfolio optimization"""
        if not expected_returns or not covariance_matrix:
            return {"error": "Insufficient data for efficient frontier"}
        
        expected_returns = np.array(expected_returns)
        cov_matrix = np.array(covariance_matrix)
        n_assets = len(expected_returns)
        
        # Range of target returns
        min_return = np.min(expected_returns)
        max_return = np.max(expected_returns)
        target_returns = np.linspace(min_return, max_return, num_portfolios)
        
        efficient_portfolios = []
        
        for target_return in target_returns:
            # Minimize variance subject to target return constraint
            def objective(weights):
                return np.dot(weights, np.dot(cov_matrix, weights))
            
            constraints = [
                {"type": "eq", "fun": lambda w: np.sum(w) - 1},
                {"type": "eq", "fun": lambda w: np.dot(w, expected_returns) - target_return}
            ]
            
            bounds = [(0.0, 1.0) for _ in range(n_assets)]
            
            result = minimize(
                objective,
                np.array([1/n_assets] * n_assets),
                method="SLSQP",
                bounds=bounds,
                constraints=constraints
            )
            
            if result.success:
                weights = result.x
                portfolio_return = np.dot(weights, expected_returns)
                portfolio_variance = result.fun
                portfolio_volatility = np.sqrt(portfolio_variance)
                
                efficient_portfolios.append({
                    "return": portfolio_return,
                    "volatility": portfolio_volatility,
                    "weights": weights.tolist(),
                    "sharpe_ratio": portfolio_return / portfolio_volatility if portfolio_volatility > 0 else 0
                })
        
        # Find maximum Sharpe ratio portfolio
        if efficient_portfolios:
            max_sharpe_portfolio = max(efficient_portfolios, key=lambda x: x["sharpe_ratio"])
            min_vol_portfolio = min(efficient_portfolios, key=lambda x: x["volatility"])
            
            return {
                "efficient_portfolios": efficient_portfolios,
                "max_sharpe_portfolio": max_sharpe_portfolio,
                "min_volatility_portfolio": min_vol_portfolio,
                "num_portfolios": len(efficient_portfolios)
            }
        else:
            return {"error": "Could not generate efficient frontier"}
    
    @staticmethod
    def analyze_portfolio_drift(
        initial_allocation: Dict[str, float],
        current_positions: List[Dict[str, Any]],
        time_period_days: int
    ) -> Dict[str, Any]:
        """Analyze how portfolio allocation has drifted over time"""
        current_total = sum(pos.get("market_value", 0) for pos in current_positions)
        
        if current_total == 0:
            return {"error": "No current portfolio value"}
        
        # Calculate current allocation
        current_allocation = {}
        for pos in current_positions:
            symbol = pos.get("symbol", "Unknown")
            weight = pos.get("market_value", 0) / current_total
            current_allocation[symbol] = weight
        
        # Calculate drift metrics
        drift_analysis = []
        total_drift = 0
        
        for symbol, initial_weight in initial_allocation.items():
            current_weight = current_allocation.get(symbol, 0)
            drift = current_weight - initial_weight
            abs_drift = abs(drift)
            
            drift_analysis.append({
                "symbol": symbol,
                "initial_weight": initial_weight,
                "current_weight": current_weight,
                "drift": drift,
                "abs_drift": abs_drift,
                "drift_percentage": (abs_drift / initial_weight * 100) if initial_weight > 0 else 0
            })
            
            total_drift += abs_drift
        
        # Check for new positions not in initial allocation
        for symbol, current_weight in current_allocation.items():
            if symbol not in initial_allocation:
                drift_analysis.append({
                    "symbol": symbol,
                    "initial_weight": 0,
                    "current_weight": current_weight,
                    "drift": current_weight,
                    "abs_drift": current_weight,
                    "drift_percentage": float('inf'),
                    "new_position": True
                })
                total_drift += current_weight
        
        # Sort by absolute drift
        drift_analysis.sort(key=lambda x: x["abs_drift"], reverse=True)
        
        return {
            "time_period_days": time_period_days,
            "total_drift": total_drift,
            "average_daily_drift": total_drift / time_period_days if time_period_days > 0 else 0,
            "drift_by_position": drift_analysis,
            "rebalancing_urgency": "HIGH" if total_drift > 0.1 else "MEDIUM" if total_drift > 0.05 else "LOW",
            "positions_requiring_attention": len([d for d in drift_analysis if d["abs_drift"] > 0.02])
        }