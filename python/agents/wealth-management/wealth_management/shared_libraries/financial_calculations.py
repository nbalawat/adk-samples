"""Financial calculations library for wealth management agents"""

import math
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from decimal import Decimal
from datetime import datetime, timedelta


class FinancialCalculator:
    """Comprehensive financial calculations for wealth management"""
    
    @staticmethod
    def present_value(future_value: float, rate: float, periods: int) -> float:
        """Calculate present value of future cash flows"""
        if rate == 0:
            return future_value / periods
        return future_value / ((1 + rate) ** periods)
    
    @staticmethod
    def future_value(present_value: float, rate: float, periods: int) -> float:
        """Calculate future value of current investment"""
        return present_value * ((1 + rate) ** periods)
    
    @staticmethod
    def compound_annual_growth_rate(beginning_value: float, ending_value: float, periods: int) -> float:
        """Calculate CAGR between two values"""
        if beginning_value <= 0 or ending_value <= 0 or periods <= 0:
            return 0.0
        return ((ending_value / beginning_value) ** (1 / periods)) - 1
    
    @staticmethod
    def net_present_value(cash_flows: List[float], discount_rate: float) -> float:
        """Calculate NPV of cash flow series"""
        npv = 0.0
        for i, cash_flow in enumerate(cash_flows):
            npv += cash_flow / ((1 + discount_rate) ** i)
        return npv
    
    @staticmethod
    def internal_rate_of_return(cash_flows: List[float], initial_guess: float = 0.1) -> Optional[float]:
        """Calculate IRR using Newton-Raphson method"""
        if len(cash_flows) < 2:
            return None
        
        # Newton-Raphson method for IRR
        rate = initial_guess
        max_iterations = 100
        tolerance = 1e-6
        
        for _ in range(max_iterations):
            # Calculate NPV and its derivative
            npv = 0.0
            dnpv = 0.0
            
            for i, cash_flow in enumerate(cash_flows):
                if i == 0:
                    npv += cash_flow
                else:
                    factor = (1 + rate) ** i
                    npv += cash_flow / factor
                    dnpv -= i * cash_flow / (factor * (1 + rate))
            
            if abs(npv) < tolerance:
                return rate
            
            if abs(dnpv) < tolerance:
                break
            
            rate = rate - npv / dnpv
        
        return rate if abs(npv) < 0.01 else None
    
    @staticmethod
    def sharpe_ratio(returns: List[float], risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio for return series"""
        if not returns or len(returns) < 2:
            return 0.0
        
        excess_returns = [r - risk_free_rate/252 for r in returns]  # Daily risk-free rate
        mean_excess = np.mean(excess_returns)
        std_excess = np.std(excess_returns, ddof=1)
        
        return (mean_excess / std_excess) * np.sqrt(252) if std_excess != 0 else 0.0
    
    @staticmethod
    def sortino_ratio(returns: List[float], risk_free_rate: float = 0.02, target_return: Optional[float] = None) -> float:
        """Calculate Sortino ratio focusing on downside deviation"""
        if not returns or len(returns) < 2:
            return 0.0
        
        if target_return is None:
            target_return = risk_free_rate / 252
        
        excess_returns = [r - target_return for r in returns]
        mean_excess = np.mean(excess_returns)
        
        # Calculate downside deviation
        downside_returns = [min(0, r) for r in excess_returns]
        downside_deviation = np.std(downside_returns, ddof=1)
        
        return (mean_excess / downside_deviation) * np.sqrt(252) if downside_deviation != 0 else 0.0
    
    @staticmethod
    def maximum_drawdown(values: List[float]) -> Tuple[float, int, int]:
        """Calculate maximum drawdown and its duration"""
        if not values or len(values) < 2:
            return 0.0, 0, 0
        
        peak = values[0]
        max_dd = 0.0
        max_dd_start = 0
        max_dd_end = 0
        current_dd_start = 0
        
        for i, value in enumerate(values):
            if value > peak:
                peak = value
                current_dd_start = i
            else:
                dd = (peak - value) / peak
                if dd > max_dd:
                    max_dd = dd
                    max_dd_start = current_dd_start
                    max_dd_end = i
        
        return max_dd, max_dd_start, max_dd_end
    
    @staticmethod
    def value_at_risk(returns: List[float], confidence_level: float = 0.05) -> float:
        """Calculate Value at Risk at given confidence level"""
        if not returns:
            return 0.0
        
        return np.percentile(returns, confidence_level * 100)
    
    @staticmethod
    def conditional_value_at_risk(returns: List[float], confidence_level: float = 0.05) -> float:
        """Calculate Conditional VaR (Expected Shortfall)"""
        if not returns:
            return 0.0
        
        var = FinancialCalculator.value_at_risk(returns, confidence_level)
        tail_returns = [r for r in returns if r <= var]
        
        return np.mean(tail_returns) if tail_returns else 0.0
    
    @staticmethod
    def beta(asset_returns: List[float], market_returns: List[float]) -> float:
        """Calculate beta relative to market"""
        if len(asset_returns) != len(market_returns) or len(asset_returns) < 2:
            return 1.0
        
        covariance = np.cov(asset_returns, market_returns)[0][1]
        market_variance = np.var(market_returns, ddof=1)
        
        return covariance / market_variance if market_variance != 0 else 1.0
    
    @staticmethod
    def alpha(asset_returns: List[float], market_returns: List[float], risk_free_rate: float = 0.02) -> float:
        """Calculate Jensen's alpha"""
        if len(asset_returns) != len(market_returns) or len(asset_returns) < 2:
            return 0.0
        
        beta = FinancialCalculator.beta(asset_returns, market_returns)
        asset_mean = np.mean(asset_returns)
        market_mean = np.mean(market_returns)
        rf_daily = risk_free_rate / 252
        
        expected_return = rf_daily + beta * (market_mean - rf_daily)
        return (asset_mean - expected_return) * 252  # Annualized alpha
    
    @staticmethod
    def information_ratio(portfolio_returns: List[float], benchmark_returns: List[float]) -> float:
        """Calculate information ratio vs benchmark"""
        if len(portfolio_returns) != len(benchmark_returns) or len(portfolio_returns) < 2:
            return 0.0
        
        excess_returns = [p - b for p, b in zip(portfolio_returns, benchmark_returns)]
        mean_excess = np.mean(excess_returns)
        tracking_error = np.std(excess_returns, ddof=1)
        
        return (mean_excess / tracking_error) * np.sqrt(252) if tracking_error != 0 else 0.0
    
    @staticmethod
    def treynor_ratio(returns: List[float], market_returns: List[float], risk_free_rate: float = 0.02) -> float:
        """Calculate Treynor ratio"""
        if not returns or len(returns) < 2:
            return 0.0
        
        beta = FinancialCalculator.beta(returns, market_returns)
        mean_return = np.mean(returns)
        rf_daily = risk_free_rate / 252
        
        return ((mean_return - rf_daily) / beta) * 252 if beta != 0 else 0.0
    
    @staticmethod
    def calmar_ratio(returns: List[float]) -> float:
        """Calculate Calmar ratio (annual return / max drawdown)"""
        if not returns or len(returns) < 2:
            return 0.0
        
        annual_return = np.mean(returns) * 252
        cumulative_returns = np.cumprod(1 + np.array(returns))
        max_dd, _, _ = FinancialCalculator.maximum_drawdown(cumulative_returns.tolist())
        
        return annual_return / max_dd if max_dd != 0 else 0.0
    
    @staticmethod
    def calculate_required_return(goal_amount: float, current_amount: float, years: int) -> float:
        """Calculate required annual return to reach financial goal"""
        if current_amount <= 0 or years <= 0:
            return 0.0
        
        return ((goal_amount / current_amount) ** (1 / years)) - 1
    
    @staticmethod
    def monte_carlo_simulation(
        initial_value: float,
        expected_return: float,
        volatility: float,
        years: int,
        simulations: int = 1000
    ) -> Dict[str, Any]:
        """Run Monte Carlo simulation for portfolio projections"""
        np.random.seed(42)  # For reproducible results
        
        final_values = []
        
        for _ in range(simulations):
            value = initial_value
            
            for _ in range(years * 252):  # Daily simulation
                daily_return = np.random.normal(
                    expected_return / 252, 
                    volatility / np.sqrt(252)
                )
                value *= (1 + daily_return)
            
            final_values.append(value)
        
        final_values = np.array(final_values)
        
        return {
            "mean_final_value": np.mean(final_values),
            "median_final_value": np.median(final_values),
            "std_final_value": np.std(final_values),
            "percentile_5": np.percentile(final_values, 5),
            "percentile_25": np.percentile(final_values, 25),
            "percentile_75": np.percentile(final_values, 75),
            "percentile_95": np.percentile(final_values, 95),
            "probability_of_loss": np.mean(final_values < initial_value),
            "probability_of_doubling": np.mean(final_values >= initial_value * 2)
        }
    
    @staticmethod
    def calculate_retirement_savings(
        current_age: int,
        retirement_age: int,
        current_savings: float,
        annual_contribution: float,
        expected_return: float,
        inflation_rate: float = 0.03
    ) -> Dict[str, Any]:
        """Calculate retirement savings projections"""
        years_to_retirement = retirement_age - current_age
        
        if years_to_retirement <= 0:
            return {
                "years_to_retirement": 0,
                "projected_balance": current_savings,
                "real_purchasing_power": current_savings,
                "total_contributions": 0
            }
        
        # Calculate future value with regular contributions
        fv_current = FinancialCalculator.future_value(current_savings, expected_return, years_to_retirement)
        
        # Future value of annuity (regular contributions)
        if expected_return == 0:
            fv_contributions = annual_contribution * years_to_retirement
        else:
            fv_contributions = annual_contribution * (((1 + expected_return) ** years_to_retirement - 1) / expected_return)
        
        total_balance = fv_current + fv_contributions
        real_purchasing_power = total_balance / ((1 + inflation_rate) ** years_to_retirement)
        
        return {
            "years_to_retirement": years_to_retirement,
            "projected_balance": total_balance,
            "real_purchasing_power": real_purchasing_power,
            "total_contributions": annual_contribution * years_to_retirement,
            "growth_from_current_savings": fv_current - current_savings,
            "growth_from_contributions": fv_contributions - (annual_contribution * years_to_retirement)
        }