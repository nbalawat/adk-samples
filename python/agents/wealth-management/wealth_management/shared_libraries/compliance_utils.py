"""Compliance utilities for wealth management"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import re


class ComplianceLevel(Enum):
    """Compliance violation severity levels"""
    INFO = "INFO"
    WARNING = "WARNING"
    VIOLATION = "VIOLATION"
    CRITICAL = "CRITICAL"


class ComplianceChecker:
    """Utilities for compliance checking and monitoring"""
    
    # Standard concentration limits
    CONCENTRATION_LIMITS = {
        "single_position": 0.10,  # 10%
        "single_sector": 0.25,    # 25%
        "top_5_positions": 0.60,  # 60%
        "cash_minimum": 0.02      # 2%
    }
    
    # Suitability risk mappings
    RISK_SUITABILITY = {
        "CONSERVATIVE": ["Investment Grade Bonds", "Government Bonds", "CDs", "Money Market"],
        "MODERATE": ["Large Cap Stocks", "Dividend Stocks", "Balanced Funds", "REITs"],
        "AGGRESSIVE": ["Small Cap Stocks", "Growth Stocks", "Sector ETFs", "International Stocks"],
        "SPECULATIVE": ["Options", "Futures", "Crypto", "Penny Stocks", "Leveraged ETFs"]
    }
    
    @staticmethod
    def check_position_concentration(
        positions: List[Dict[str, Any]],
        limits: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """Check portfolio concentration limits"""
        if not positions:
            return {"compliant": True, "violations": [], "warnings": []}
        
        limits = limits or ComplianceChecker.CONCENTRATION_LIMITS
        total_value = sum(pos.get("market_value", 0) for pos in positions)
        
        if total_value == 0:
            return {"compliant": True, "violations": [], "warnings": []}
        
        violations = []
        warnings = []
        
        # Check individual position concentration
        for pos in positions:
            symbol = pos.get("symbol", "Unknown")
            market_value = pos.get("market_value", 0)
            weight = market_value / total_value
            
            if weight > limits["single_position"]:
                violations.append({
                    "type": "POSITION_CONCENTRATION",
                    "level": ComplianceLevel.VIOLATION,
                    "symbol": symbol,
                    "current_weight": weight,
                    "limit": limits["single_position"],
                    "excess": weight - limits["single_position"],
                    "message": f"{symbol} exceeds single position limit: {weight:.1%} > {limits['single_position']:.1%}"
                })
            elif weight > limits["single_position"] * 0.8:  # 80% of limit
                warnings.append({
                    "type": "POSITION_CONCENTRATION",
                    "level": ComplianceLevel.WARNING,
                    "symbol": symbol,
                    "current_weight": weight,
                    "limit": limits["single_position"],
                    "message": f"{symbol} approaching single position limit: {weight:.1%}"
                })
        
        # Check top 5 concentration
        weights = [pos.get("market_value", 0) / total_value for pos in positions]
        top_5_weight = sum(sorted(weights, reverse=True)[:5])
        
        if top_5_weight > limits["top_5_positions"]:
            violations.append({
                "type": "TOP_5_CONCENTRATION",
                "level": ComplianceLevel.VIOLATION,
                "current_weight": top_5_weight,
                "limit": limits["top_5_positions"],
                "excess": top_5_weight - limits["top_5_positions"],
                "message": f"Top 5 positions exceed limit: {top_5_weight:.1%} > {limits['top_5_positions']:.1%}"
            })
        
        # Check sector concentration (mock implementation)
        sector_weights = ComplianceChecker._calculate_sector_weights(positions)
        for sector, weight in sector_weights.items():
            if weight > limits["single_sector"]:
                violations.append({
                    "type": "SECTOR_CONCENTRATION",
                    "level": ComplianceLevel.VIOLATION,
                    "sector": sector,
                    "current_weight": weight,
                    "limit": limits["single_sector"],
                    "excess": weight - limits["single_sector"],
                    "message": f"{sector} sector exceeds limit: {weight:.1%} > {limits['single_sector']:.1%}"
                })
        
        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "warnings": warnings,
            "total_positions": len(positions),
            "concentration_metrics": {
                "max_position_weight": max(weights) if weights else 0,
                "top_5_weight": top_5_weight,
                "herfindahl_index": sum(w**2 for w in weights)
            }
        }
    
    @staticmethod
    def _calculate_sector_weights(positions: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate sector weights (mock implementation)"""
        total_value = sum(pos.get("market_value", 0) for pos in positions)
        
        if total_value == 0:
            return {}
        
        # Simple sector mapping
        sector_map = {
            "AAPL": "Technology", "GOOGL": "Technology", "MSFT": "Technology",
            "TSLA": "Consumer Discretionary", "NVDA": "Technology",
            "JPM": "Financial", "BAC": "Financial", "WFC": "Financial",
            "JNJ": "Healthcare", "PFE": "Healthcare", "UNH": "Healthcare",
            "XOM": "Energy", "CVX": "Energy", "COP": "Energy"
        }
        
        sector_values = {}
        for pos in positions:
            symbol = pos.get("symbol", "Unknown")
            sector = sector_map.get(symbol, "Other")
            market_value = pos.get("market_value", 0)
            sector_values[sector] = sector_values.get(sector, 0) + market_value
        
        return {sector: value / total_value for sector, value in sector_values.items()}
    
    @staticmethod
    def check_suitability(
        client_risk_tolerance: str,
        proposed_investments: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Check investment suitability against client risk profile"""
        if not proposed_investments:
            return {"suitable": True, "violations": [], "warnings": []}
        
        violations = []
        warnings = []
        
        client_tolerance_upper = client_risk_tolerance.upper()
        suitable_categories = ComplianceChecker.RISK_SUITABILITY.get(client_tolerance_upper, [])
        
        # Allow investments up to one level higher than client tolerance
        risk_hierarchy = ["CONSERVATIVE", "MODERATE", "AGGRESSIVE", "SPECULATIVE"]
        client_index = risk_hierarchy.index(client_tolerance_upper) if client_tolerance_upper in risk_hierarchy else 1
        
        allowed_categories = []
        for i in range(min(client_index + 2, len(risk_hierarchy))):
            allowed_categories.extend(ComplianceChecker.RISK_SUITABILITY.get(risk_hierarchy[i], []))
        
        for investment in proposed_investments:
            symbol = investment.get("symbol", "Unknown")
            investment_type = investment.get("investment_type", "Unknown")
            amount = investment.get("amount", 0)
            
            # Check if investment type is suitable
            if investment_type not in allowed_categories:
                # Determine severity based on risk level
                if investment_type in ComplianceChecker.RISK_SUITABILITY.get("SPECULATIVE", []):
                    level = ComplianceLevel.CRITICAL
                elif investment_type in ComplianceChecker.RISK_SUITABILITY.get("AGGRESSIVE", []):
                    level = ComplianceLevel.VIOLATION if client_tolerance_upper in ["CONSERVATIVE"] else ComplianceLevel.WARNING
                else:
                    level = ComplianceLevel.WARNING
                
                violation_item = {
                    "type": "SUITABILITY_MISMATCH",
                    "level": level,
                    "symbol": symbol,
                    "investment_type": investment_type,
                    "client_risk_tolerance": client_risk_tolerance,
                    "amount": amount,
                    "message": f"{symbol} ({investment_type}) may not be suitable for {client_risk_tolerance} risk tolerance"
                }
                
                if level in [ComplianceLevel.VIOLATION, ComplianceLevel.CRITICAL]:
                    violations.append(violation_item)
                else:
                    warnings.append(violation_item)
        
        return {
            "suitable": len(violations) == 0,
            "violations": violations,
            "warnings": warnings,
            "client_risk_tolerance": client_risk_tolerance,
            "investments_reviewed": len(proposed_investments)
        }
    
    @staticmethod
    def check_liquidity_requirements(
        positions: List[Dict[str, Any]],
        cash_balance: float,
        minimum_liquidity: float = 0.05  # 5%
    ) -> Dict[str, Any]:
        """Check portfolio liquidity requirements"""
        total_value = sum(pos.get("market_value", 0) for pos in positions) + cash_balance
        
        if total_value == 0:
            return {"compliant": True, "violations": [], "warnings": []}
        
        violations = []
        warnings = []
        
        # Check cash percentage
        cash_percentage = cash_balance / total_value
        
        if cash_percentage < minimum_liquidity:
            violations.append({
                "type": "INSUFFICIENT_LIQUIDITY",
                "level": ComplianceLevel.VIOLATION,
                "current_cash_percentage": cash_percentage,
                "minimum_required": minimum_liquidity,
                "shortfall": minimum_liquidity - cash_percentage,
                "message": f"Cash position below minimum: {cash_percentage:.1%} < {minimum_liquidity:.1%}"
            })
        elif cash_percentage < minimum_liquidity * 1.5:  # 150% of minimum
            warnings.append({
                "type": "LOW_LIQUIDITY",
                "level": ComplianceLevel.WARNING,
                "current_cash_percentage": cash_percentage,
                "minimum_required": minimum_liquidity,
                "message": f"Cash position approaching minimum: {cash_percentage:.1%}"
            })
        
        # Check for illiquid positions
        illiquid_symbols = ["OTC", "PRIVATE", "RESTRICTED"]  # Mock illiquid identifiers
        illiquid_value = 0
        
        for pos in positions:
            symbol = pos.get("symbol", "")
            if any(illiquid in symbol for illiquid in illiquid_symbols):
                illiquid_value += pos.get("market_value", 0)
        
        illiquid_percentage = illiquid_value / total_value
        
        if illiquid_percentage > 0.20:  # 20% maximum illiquid
            violations.append({
                "type": "EXCESSIVE_ILLIQUID_HOLDINGS",
                "level": ComplianceLevel.VIOLATION,
                "illiquid_percentage": illiquid_percentage,
                "maximum_allowed": 0.20,
                "excess": illiquid_percentage - 0.20,
                "message": f"Illiquid holdings exceed 20% limit: {illiquid_percentage:.1%}"
            })
        
        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "warnings": warnings,
            "liquidity_metrics": {
                "cash_percentage": cash_percentage,
                "illiquid_percentage": illiquid_percentage,
                "liquid_percentage": 1 - illiquid_percentage
            }
        }
    
    @staticmethod
    def check_regulatory_limits(
        account_type: str,
        positions: List[Dict[str, Any]],
        client_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Check regulatory limits based on account type"""
        violations = []
        warnings = []
        
        # IRA contribution limits (mock for current year)
        if account_type.upper() in ["IRA", "ROTH_IRA"]:
            annual_contribution_limit = 6500  # Mock 2024 limit
            age = client_info.get("age", 50)
            
            if age >= 50:
                annual_contribution_limit += 1000  # Catch-up contribution
            
            # Check if recent contributions exceed limits (mock check)
            recent_contributions = client_info.get("annual_contributions", 0)
            
            if recent_contributions > annual_contribution_limit:
                violations.append({
                    "type": "IRA_CONTRIBUTION_EXCESS",
                    "level": ComplianceLevel.VIOLATION,
                    "contributions": recent_contributions,
                    "limit": annual_contribution_limit,
                    "excess": recent_contributions - annual_contribution_limit,
                    "message": f"IRA contributions exceed annual limit: ${recent_contributions:,.2f} > ${annual_contribution_limit:,.2f}"
                })
        
        # 401k limits
        if account_type.upper() == "401K":
            annual_limit = 23000  # Mock 2024 limit
            age = client_info.get("age", 50)
            
            if age >= 50:
                annual_limit += 7500  # Catch-up contribution
            
            recent_contributions = client_info.get("annual_contributions", 0)
            
            if recent_contributions > annual_limit:
                violations.append({
                    "type": "401K_CONTRIBUTION_EXCESS",
                    "level": ComplianceLevel.VIOLATION,
                    "contributions": recent_contributions,
                    "limit": annual_limit,
                    "excess": recent_contributions - annual_limit,
                    "message": f"401k contributions exceed annual limit: ${recent_contributions:,.2f} > ${annual_limit:,.2f}"
                })
        
        # Pattern Day Trader rule (mock)
        if account_type.upper() in ["INDIVIDUAL", "JOINT"]:
            account_value = sum(pos.get("market_value", 0) for pos in positions)
            day_trades = client_info.get("day_trades_count", 0)
            
            if day_trades >= 4 and account_value < 25000:
                violations.append({
                    "type": "PDT_RULE_VIOLATION",
                    "level": ComplianceLevel.CRITICAL,
                    "day_trades": day_trades,
                    "account_value": account_value,
                    "minimum_required": 25000,
                    "message": f"Pattern Day Trader rule violation: {day_trades} day trades with account value ${account_value:,.2f} < $25,000"
                })
        
        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "warnings": warnings,
            "account_type": account_type,
            "regulatory_framework": "US_SECURITIES"
        }
    
    @staticmethod
    def generate_compliance_report(
        account_id: str,
        positions: List[Dict[str, Any]],
        client_info: Dict[str, Any],
        cash_balance: float = 0
    ) -> Dict[str, Any]:
        """Generate comprehensive compliance report"""
        
        # Run all compliance checks
        concentration_check = ComplianceChecker.check_position_concentration(positions)
        suitability_check = ComplianceChecker.check_suitability(
            client_info.get("risk_tolerance", "MODERATE"),
            positions
        )
        liquidity_check = ComplianceChecker.check_liquidity_requirements(positions, cash_balance)
        regulatory_check = ComplianceChecker.check_regulatory_limits(
            client_info.get("account_type", "INDIVIDUAL"),
            positions,
            client_info
        )
        
        # Aggregate results
        all_violations = (
            concentration_check.get("violations", []) +
            suitability_check.get("violations", []) +
            liquidity_check.get("violations", []) +
            regulatory_check.get("violations", [])
        )
        
        all_warnings = (
            concentration_check.get("warnings", []) +
            suitability_check.get("warnings", []) +
            liquidity_check.get("warnings", []) +
            regulatory_check.get("warnings", [])
        )
        
        # Determine overall compliance status
        overall_status = "COMPLIANT"
        if any(v.get("level") == ComplianceLevel.CRITICAL for v in all_violations):
            overall_status = "CRITICAL_VIOLATIONS"
        elif all_violations:
            overall_status = "VIOLATIONS_FOUND"
        elif all_warnings:
            overall_status = "WARNINGS_ONLY"
        
        return {
            "account_id": account_id,
            "report_date": datetime.utcnow().isoformat(),
            "overall_status": overall_status,
            "compliant": len(all_violations) == 0,
            "summary": {
                "total_violations": len(all_violations),
                "total_warnings": len(all_warnings),
                "critical_violations": len([v for v in all_violations if v.get("level") == ComplianceLevel.CRITICAL]),
                "checks_performed": ["CONCENTRATION", "SUITABILITY", "LIQUIDITY", "REGULATORY"]
            },
            "detailed_results": {
                "concentration_check": concentration_check,
                "suitability_check": suitability_check,
                "liquidity_check": liquidity_check,
                "regulatory_check": regulatory_check
            },
            "violations": all_violations,
            "warnings": all_warnings,
            "recommended_actions": ComplianceChecker._generate_recommendations(all_violations, all_warnings)
        }
    
    @staticmethod
    def _generate_recommendations(violations: List[Dict], warnings: List[Dict]) -> List[str]:
        """Generate compliance recommendations"""
        recommendations = []
        
        # Process violations
        for violation in violations:
            violation_type = violation.get("type")
            
            if violation_type == "POSITION_CONCENTRATION":
                recommendations.append(f"Reduce position in {violation.get('symbol')} to below {violation.get('limit'):.1%}")
            elif violation_type == "SECTOR_CONCENTRATION":
                recommendations.append(f"Diversify away from {violation.get('sector')} sector")
            elif violation_type == "SUITABILITY_MISMATCH":
                recommendations.append(f"Review suitability of {violation.get('symbol')} for client risk profile")
            elif violation_type == "INSUFFICIENT_LIQUIDITY":
                recommendations.append(f"Increase cash position to at least {violation.get('minimum_required'):.1%}")
            elif violation_type == "PDT_RULE_VIOLATION":
                recommendations.append("Reduce day trading activity or increase account value above $25,000")
        
        # Process warnings
        for warning in warnings:
            if warning.get("type") == "LOW_LIQUIDITY":
                recommendations.append("Consider increasing cash allocation for liquidity buffer")
        
        return recommendations