"""Risk analytics library for wealth management"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from scipy import stats
from scipy.optimize import minimize


class RiskAnalyzer:
    """Comprehensive risk analytics for portfolios and investments"""
    
    @staticmethod
    def calculate_portfolio_risk_metrics(
        returns: List[float],
        weights: Optional[List[float]] = None,
        benchmark_returns: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """Calculate comprehensive risk metrics for a portfolio"""
        if not returns:
            return {}
        
        returns_array = np.array(returns)
        
        metrics = {
            "volatility": np.std(returns_array, ddof=1) * np.sqrt(252),  # Annualized
            "skewness": stats.skew(returns_array),
            "kurtosis": stats.kurtosis(returns_array),
            "var_95": np.percentile(returns_array, 5),
            "var_99": np.percentile(returns_array, 1),
            "cvar_95": RiskAnalyzer._conditional_var(returns_array, 0.05),
            "cvar_99": RiskAnalyzer._conditional_var(returns_array, 0.01),
            "max_drawdown": RiskAnalyzer._calculate_max_drawdown(returns_array)
        }
        
        # Add benchmark-relative metrics if provided
        if benchmark_returns and len(benchmark_returns) == len(returns):
            benchmark_array = np.array(benchmark_returns)
            excess_returns = returns_array - benchmark_array
            
            metrics.update({
                "tracking_error": np.std(excess_returns, ddof=1) * np.sqrt(252),
                "information_ratio": (np.mean(excess_returns) / np.std(excess_returns, ddof=1)) * np.sqrt(252) if np.std(excess_returns) > 0 else 0,
                "beta": RiskAnalyzer._calculate_beta(returns_array, benchmark_array),
                "correlation": np.corrcoef(returns_array, benchmark_array)[0, 1] if len(returns_array) > 1 else 0
            })
        
        return metrics
    
    @staticmethod
    def _conditional_var(returns: np.ndarray, confidence_level: float) -> float:
        """Calculate Conditional Value at Risk (Expected Shortfall)"""
        var = np.percentile(returns, confidence_level * 100)
        return np.mean(returns[returns <= var])
    
    @staticmethod
    def _calculate_max_drawdown(returns: np.ndarray) -> Dict[str, Any]:
        """Calculate maximum drawdown and related metrics"""
        cumulative = np.cumprod(1 + returns)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - running_max) / running_max
        
        max_dd = np.min(drawdown)
        max_dd_idx = np.argmin(drawdown)
        
        # Find the peak before max drawdown
        peak_idx = np.argmax(running_max[:max_dd_idx + 1])
        
        return {
            "max_drawdown": abs(max_dd),
            "max_dd_start": peak_idx,
            "max_dd_end": max_dd_idx,
            "max_dd_duration": max_dd_idx - peak_idx,
            "current_drawdown": abs(drawdown[-1]) if drawdown[-1] < 0 else 0
        }
    
    @staticmethod
    def _calculate_beta(asset_returns: np.ndarray, market_returns: np.ndarray) -> float:
        """Calculate beta coefficient"""
        if len(asset_returns) < 2:
            return 1.0
        
        covariance = np.cov(asset_returns, market_returns)[0][1]
        market_variance = np.var(market_returns, ddof=1)
        
        return covariance / market_variance if market_variance > 0 else 1.0
    
    @staticmethod
    def stress_test_portfolio(
        portfolio_returns: List[float],
        scenarios: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Run stress tests on portfolio under various scenarios"""
        if not portfolio_returns:
            return {}
        
        results = {}
        
        for scenario in scenarios:
            scenario_name = scenario.get("name", "Unnamed Scenario")
            market_shock = scenario.get("market_shock", 0)  # % decline in market
            volatility_increase = scenario.get("volatility_increase", 1)  # multiplier
            correlation_increase = scenario.get("correlation_increase", 1)  # multiplier
            
            # Simulate stressed returns
            stressed_returns = RiskAnalyzer._apply_stress_scenario(
                portfolio_returns, market_shock, volatility_increase
            )
            
            # Calculate metrics under stress
            stress_metrics = {
                "scenario_return": np.sum(stressed_returns),
                "scenario_volatility": np.std(stressed_returns, ddof=1) * np.sqrt(252),
                "scenario_var_95": np.percentile(stressed_returns, 5),
                "scenario_max_loss": np.min(stressed_returns),
                "days_to_recover": RiskAnalyzer._estimate_recovery_time(stressed_returns)
            }
            
            results[scenario_name] = stress_metrics
        
        return results
    
    @staticmethod
    def _apply_stress_scenario(
        returns: List[float], 
        market_shock: float, 
        volatility_increase: float
    ) -> np.ndarray:
        """Apply stress scenario to returns"""
        returns_array = np.array(returns)
        
        # Apply market shock (one-time decline)
        shocked_returns = returns_array.copy()
        if market_shock < 0:
            shocked_returns[0] += market_shock  # Apply shock to first period
        
        # Increase volatility
        if volatility_increase > 1:
            mean_return = np.mean(shocked_returns)
            shocked_returns = mean_return + (shocked_returns - mean_return) * volatility_increase
        
        return shocked_returns
    
    @staticmethod
    def _estimate_recovery_time(stressed_returns: np.ndarray) -> int:
        """Estimate time to recover from stress scenario"""
        cumulative = np.cumprod(1 + stressed_returns)
        min_value = np.min(cumulative)
        
        if min_value >= cumulative[0]:  # No recovery needed
            return 0
        
        # Find when it first recovers to initial value
        recovery_idx = np.where(cumulative >= cumulative[0])[0]
        return recovery_idx[0] if len(recovery_idx) > 0 else len(stressed_returns)
    
    @staticmethod
    def calculate_risk_attribution(
        portfolio_weights: List[float],
        asset_returns: List[List[float]],
        asset_names: List[str]
    ) -> Dict[str, Any]:
        """Calculate risk attribution by asset/factor"""
        if not portfolio_weights or not asset_returns:
            return {}
        
        weights = np.array(portfolio_weights)
        returns_matrix = np.array(asset_returns).T  # Transpose for proper shape
        
        # Calculate covariance matrix
        cov_matrix = np.cov(returns_matrix.T)
        
        # Portfolio variance
        portfolio_variance = np.dot(weights, np.dot(cov_matrix, weights))
        portfolio_volatility = np.sqrt(portfolio_variance * 252)
        
        # Risk contribution of each asset
        marginal_risk = np.dot(cov_matrix, weights) * 252
        risk_contribution = weights * marginal_risk
        
        # Component risk (risk contribution / portfolio variance)
        component_risk = risk_contribution / portfolio_variance if portfolio_variance > 0 else np.zeros_like(risk_contribution)
        
        attribution = {}
        for i, name in enumerate(asset_names):
            attribution[name] = {
                "weight": weights[i],
                "marginal_risk": marginal_risk[i],
                "risk_contribution": risk_contribution[i],
                "risk_percentage": component_risk[i] * 100,
                "volatility_contribution": np.sqrt(risk_contribution[i]) if risk_contribution[i] > 0 else 0
            }
        
        return {
            "portfolio_volatility": portfolio_volatility,
            "portfolio_variance": portfolio_variance,
            "risk_attribution": attribution,
            "diversification_ratio": sum(weights[i] * np.sqrt(cov_matrix[i, i] * 252) for i in range(len(weights))) / portfolio_volatility
        }
    
    @staticmethod
    def optimize_risk_parity_portfolio(
        expected_returns: List[float],
        covariance_matrix: List[List[float]],
        risk_budget: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """Optimize portfolio for risk parity"""
        n_assets = len(expected_returns)
        
        if risk_budget is None:
            risk_budget = [1/n_assets] * n_assets
        
        expected_returns = np.array(expected_returns)
        cov_matrix = np.array(covariance_matrix)
        risk_budget = np.array(risk_budget)
        
        # Initial guess - equal weights
        initial_weights = np.array([1/n_assets] * n_assets)
        
        # Constraints
        constraints = [
            {"type": "eq", "fun": lambda w: np.sum(w) - 1},  # Weights sum to 1
        ]
        
        # Bounds - long only
        bounds = [(0.0, 1.0) for _ in range(n_assets)]
        
        # Objective function - minimize squared deviations from risk budget
        def objective(weights):
            portfolio_vol = np.sqrt(np.dot(weights, np.dot(cov_matrix, weights)))
            marginal_contrib = np.dot(cov_matrix, weights) / portfolio_vol
            risk_contrib = weights * marginal_contrib / portfolio_vol
            
            return np.sum((risk_contrib - risk_budget) ** 2)
        
        # Optimize
        result = minimize(
            objective,
            initial_weights,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
            options={"maxiter": 1000}
        )
        
        if result.success:
            optimal_weights = result.x
            portfolio_vol = np.sqrt(np.dot(optimal_weights, np.dot(cov_matrix, optimal_weights)))
            expected_return = np.dot(optimal_weights, expected_returns)
            
            return {
                "success": True,
                "weights": optimal_weights.tolist(),
                "expected_return": expected_return,
                "portfolio_volatility": portfolio_vol,
                "sharpe_ratio": expected_return / portfolio_vol if portfolio_vol > 0 else 0,
                "optimization_result": result
            }
        else:
            return {
                "success": False,
                "error": result.message,
                "weights": initial_weights.tolist()
            }
    
    @staticmethod
    def calculate_var_models(
        returns: List[float],
        confidence_levels: List[float] = [0.01, 0.05, 0.10]
    ) -> Dict[str, Any]:
        """Calculate VaR using multiple models"""
        if not returns:
            return {}
        
        returns_array = np.array(returns)
        var_results = {}
        
        for confidence in confidence_levels:
            confidence_pct = int(confidence * 100)
            
            # Historical VaR
            historical_var = np.percentile(returns_array, confidence * 100)
            
            # Parametric VaR (assuming normal distribution)
            mean_return = np.mean(returns_array)
            std_return = np.std(returns_array, ddof=1)
            z_score = stats.norm.ppf(confidence)
            parametric_var = mean_return + z_score * std_return
            
            # Monte Carlo VaR
            np.random.seed(42)
            mc_returns = np.random.normal(mean_return, std_return, 10000)
            mc_var = np.percentile(mc_returns, confidence * 100)
            
            # Expected Shortfall for each method
            historical_es = np.mean(returns_array[returns_array <= historical_var])
            parametric_es = mean_return - std_return * stats.norm.pdf(z_score) / confidence
            mc_es = np.mean(mc_returns[mc_returns <= mc_var])
            
            var_results[f"var_{confidence_pct}"] = {
                "historical_var": historical_var,
                "parametric_var": parametric_var,
                "monte_carlo_var": mc_var,
                "historical_es": historical_es,
                "parametric_es": parametric_es,
                "monte_carlo_es": mc_es
            }
        
        return var_results
    
    @staticmethod
    def assess_concentration_risk(
        portfolio_weights: List[float],
        asset_names: List[str],
        sector_mappings: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Assess concentration risk in portfolio"""
        weights = np.array(portfolio_weights)
        
        # Asset concentration
        asset_concentration = {
            "max_weight": np.max(weights),
            "top_5_weight": np.sum(np.sort(weights)[-5:]) if len(weights) >= 5 else np.sum(weights),
            "herfindahl_index": np.sum(weights ** 2),
            "effective_num_assets": 1 / np.sum(weights ** 2),
            "concentration_ratio": np.sum(np.sort(weights)[-3:]) if len(weights) >= 3 else np.sum(weights)
        }
        
        # Sector concentration if mapping provided
        sector_concentration = {}
        if sector_mappings:
            sector_weights = {}
            for i, asset in enumerate(asset_names):
                sector = sector_mappings.get(asset, "Unknown")
                sector_weights[sector] = sector_weights.get(sector, 0) + weights[i]
            
            sector_weights_array = np.array(list(sector_weights.values()))
            sector_concentration = {
                "max_sector_weight": np.max(sector_weights_array),
                "num_sectors": len(sector_weights),
                "sector_hhi": np.sum(sector_weights_array ** 2),
                "sector_weights": sector_weights
            }
        
        # Risk warnings
        warnings = []
        if asset_concentration["max_weight"] > 0.1:
            warnings.append(f"Single asset concentration exceeds 10%: {asset_concentration['max_weight']:.1%}")
        
        if asset_concentration["top_5_weight"] > 0.6:
            warnings.append(f"Top 5 assets represent {asset_concentration['top_5_weight']:.1%} of portfolio")
        
        if sector_concentration and sector_concentration["max_sector_weight"] > 0.3:
            warnings.append(f"Single sector concentration exceeds 30%: {sector_concentration['max_sector_weight']:.1%}")
        
        return {
            "asset_concentration": asset_concentration,
            "sector_concentration": sector_concentration,
            "concentration_warnings": warnings,
            "overall_concentration_score": min(10, asset_concentration["herfindahl_index"] * 10)  # 0-10 scale
        }