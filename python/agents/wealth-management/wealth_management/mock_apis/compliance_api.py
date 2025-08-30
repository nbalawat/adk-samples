"""Mock Compliance API for regulatory checks and monitoring"""

import os
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from .base_api import BaseMockAPI, APIResponse

class ComplianceCheckType(Enum):
    SUITABILITY = "SUITABILITY"
    CONCENTRATION = "CONCENTRATION"
    LIQUIDITY = "LIQUIDITY"
    RISK_TOLERANCE = "RISK_TOLERANCE"
    REGULATORY_LIMIT = "REGULATORY_LIMIT"
    FIDUCIARY_DUTY = "FIDUCIARY_DUTY"

class ComplianceStatus(Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REQUIRES_REVIEW = "REQUIRES_REVIEW"
    CONDITIONAL_APPROVAL = "CONDITIONAL_APPROVAL"

@dataclass
class ComplianceRule:
    """Compliance rule structure"""
    rule_id: str
    rule_name: str
    description: str
    check_type: ComplianceCheckType
    is_active: bool
    severity: str  # HIGH, MEDIUM, LOW

class MockComplianceAPI(BaseMockAPI):
    """Mock compliance API for regulatory monitoring"""
    
    def __init__(self):
        super().__init__("compliance_api")
        self.fiduciary_enforcement = os.getenv("FIDUCIARY_RULE_ENFORCEMENT", "true").lower() == "true"
        self.suitability_checks = os.getenv("SUITABILITY_CHECKS_ENABLED", "true").lower() == "true"
        
        # Initialize compliance rules
        self._rules = self._initialize_compliance_rules()
        self._violations = {}
        self._check_history = {}
    
    def _initialize_compliance_rules(self) -> Dict[str, ComplianceRule]:
        """Initialize standard compliance rules"""
        rules = {
            "RULE_001": ComplianceRule(
                "RULE_001", "Single Position Concentration",
                "No single position should exceed 10% of portfolio",
                ComplianceCheckType.CONCENTRATION, True, "HIGH"
            ),
            "RULE_002": ComplianceRule(
                "RULE_002", "Sector Concentration",
                "No single sector should exceed 25% of portfolio",
                ComplianceCheckType.CONCENTRATION, True, "MEDIUM"
            ),
            "RULE_003": ComplianceRule(
                "RULE_003", "Risk Tolerance Alignment",
                "Investment risk must align with client risk tolerance",
                ComplianceCheckType.RISK_TOLERANCE, True, "HIGH"
            ),
            "RULE_004": ComplianceRule(
                "RULE_004", "Liquidity Requirements",
                "Portfolio must maintain minimum 5% cash position",
                ComplianceCheckType.LIQUIDITY, True, "MEDIUM"
            ),
            "RULE_005": ComplianceRule(
                "RULE_005", "Suitability Check",
                "All investments must be suitable for client profile",
                ComplianceCheckType.SUITABILITY, True, "HIGH"
            ),
            "RULE_006": ComplianceRule(
                "RULE_006", "Fiduciary Standard",
                "All recommendations must meet fiduciary standard",
                ComplianceCheckType.FIDUCIARY_DUTY, True, "HIGH"
            ),
            "RULE_007": ComplianceRule(
                "RULE_007", "Regulatory Position Limits",
                "Individual positions must comply with regulatory limits",
                ComplianceCheckType.REGULATORY_LIMIT, True, "HIGH"
            )
        }
        return rules
    
    def check_trade_compliance(self, trade_data: Dict[str, Any]) -> APIResponse:
        """Check if a proposed trade complies with regulations"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error="Compliance system temporarily unavailable")
        
        check_id = f"CHK{datetime.utcnow().strftime('%Y%m%d')}{random.randint(1000, 9999)}"
        violations = []
        warnings = []
        
        # Simulate various compliance checks
        account_id = trade_data.get("account_id")
        symbol = trade_data.get("symbol")
        quantity = float(trade_data.get("quantity", 0))
        trade_value = float(trade_data.get("trade_value", quantity * 100))
        
        # Position concentration check
        concentration_check = self._check_position_concentration(
            account_id, symbol, trade_value
        )
        if concentration_check["violation"]:
            violations.append({
                "rule_id": "RULE_001",
                "severity": "HIGH",
                "message": concentration_check["message"]
            })
        
        # Risk tolerance alignment (random simulation)
        if random.random() < 0.1:  # 10% chance of risk mismatch
            violations.append({
                "rule_id": "RULE_003",
                "severity": "HIGH",
                "message": "Investment risk level exceeds client risk tolerance"
            })
        
        # Suitability check
        if self.suitability_checks:
            suitability_check = self._check_investment_suitability(trade_data)
            if not suitability_check["suitable"]:
                violations.append({
                    "rule_id": "RULE_005",
                    "severity": "HIGH",
                    "message": suitability_check["message"]
                })
        
        # Liquidity requirements
        if random.random() < 0.05:  # 5% chance of liquidity issue
            warnings.append({
                "rule_id": "RULE_004",
                "severity": "MEDIUM",
                "message": "Trade may impact portfolio liquidity requirements"
            })
        
        # Determine overall status
        if violations:
            status = ComplianceStatus.REJECTED
        elif warnings:
            status = ComplianceStatus.REQUIRES_REVIEW
        else:
            status = ComplianceStatus.APPROVED
        
        # Store check history
        check_result = {
            "check_id": check_id,
            "account_id": account_id,
            "trade_data": trade_data,
            "status": status.value,
            "violations": violations,
            "warnings": warnings,
            "timestamp": datetime.utcnow().isoformat(),
            "reviewed_by": "AUTO_SYSTEM"
        }
        
        if account_id not in self._check_history:
            self._check_history[account_id] = []
        self._check_history[account_id].append(check_result)
        
        return self._create_response(data=check_result)
    
    def _check_position_concentration(
        self, 
        account_id: str, 
        symbol: str, 
        trade_value: float
    ) -> Dict[str, Any]:
        """Check position concentration limits"""
        # Simulate portfolio total value
        portfolio_value = random.uniform(100000, 5000000)
        
        # Simulate current position size
        current_position_value = random.uniform(0, portfolio_value * 0.15)
        new_position_value = current_position_value + trade_value
        
        concentration_pct = (new_position_value / portfolio_value) * 100
        
        if concentration_pct > 10:  # 10% concentration limit
            return {
                "violation": True,
                "message": f"Position in {symbol} would exceed 10% concentration limit ({concentration_pct:.1f}%)"
            }
        elif concentration_pct > 8:  # Warning threshold
            return {
                "violation": False,
                "message": f"Position in {symbol} approaching concentration limit ({concentration_pct:.1f}%)"
            }
        
        return {"violation": False, "message": "Position concentration within limits"}
    
    def _check_investment_suitability(self, trade_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check investment suitability for client"""
        symbol = trade_data.get("symbol", "")
        
        # Simulate unsuitable investments (random)
        risky_symbols = ["TSLA", "GME", "AMC", "SPCE", "COIN"]
        speculative_symbols = ["crypto", "penny", "OTC"]
        
        if symbol in risky_symbols and random.random() < 0.3:
            return {
                "suitable": False,
                "message": f"Investment in {symbol} may not be suitable based on client risk profile"
            }
        
        if any(spec in symbol.lower() for spec in speculative_symbols):
            return {
                "suitable": False,
                "message": f"Speculative investment {symbol} requires additional client approval"
            }
        
        return {"suitable": True, "message": "Investment suitable for client profile"}
    
    def check_portfolio_compliance(self, account_id: str) -> APIResponse:
        """Comprehensive portfolio compliance check"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error=f"Failed to check portfolio compliance for {account_id}")
        
        check_id = f"PFC{datetime.utcnow().strftime('%Y%m%d')}{random.randint(1000, 9999)}"
        
        # Simulate comprehensive portfolio analysis
        compliance_results = {
            "check_id": check_id,
            "account_id": account_id,
            "overall_status": "COMPLIANT",
            "checks_performed": [],
            "violations": [],
            "warnings": [],
            "recommendations": [],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Concentration checks
        concentration_result = self._simulate_concentration_analysis()
        compliance_results["checks_performed"].append("CONCENTRATION")
        if concentration_result["violations"]:
            compliance_results["violations"].extend(concentration_result["violations"])
            compliance_results["overall_status"] = "NON_COMPLIANT"
        
        # Risk alignment check
        risk_result = self._simulate_risk_alignment_check()
        compliance_results["checks_performed"].append("RISK_ALIGNMENT")
        if risk_result["warnings"]:
            compliance_results["warnings"].extend(risk_result["warnings"])
        
        # Liquidity check
        liquidity_result = self._simulate_liquidity_check()
        compliance_results["checks_performed"].append("LIQUIDITY")
        if liquidity_result["recommendations"]:
            compliance_results["recommendations"].extend(liquidity_result["recommendations"])
        
        return self._create_response(data=compliance_results)
    
    def _simulate_concentration_analysis(self) -> Dict[str, Any]:
        """Simulate portfolio concentration analysis"""
        violations = []
        
        if random.random() < 0.2:  # 20% chance of concentration violation
            violations.append({
                "rule_id": "RULE_001",
                "severity": "HIGH",
                "message": "AAPL position exceeds 10% concentration limit (12.5%)",
                "current_value": 12.5,
                "limit": 10.0
            })
        
        if random.random() < 0.15:  # 15% chance of sector concentration
            violations.append({
                "rule_id": "RULE_002",
                "severity": "MEDIUM",
                "message": "Technology sector exceeds 25% limit (28.3%)",
                "current_value": 28.3,
                "limit": 25.0
            })
        
        return {"violations": violations}
    
    def _simulate_risk_alignment_check(self) -> Dict[str, Any]:
        """Simulate risk tolerance alignment check"""
        warnings = []
        
        if random.random() < 0.1:  # 10% chance of risk misalignment
            warnings.append({
                "rule_id": "RULE_003",
                "severity": "MEDIUM",
                "message": "Portfolio risk level may be higher than client tolerance",
                "portfolio_risk": "MODERATE_AGGRESSIVE",
                "client_tolerance": "MODERATE"
            })
        
        return {"warnings": warnings}
    
    def _simulate_liquidity_check(self) -> Dict[str, Any]:
        """Simulate portfolio liquidity analysis"""
        recommendations = []
        
        if random.random() < 0.3:  # 30% chance of liquidity recommendation
            recommendations.append({
                "type": "LIQUIDITY_OPTIMIZATION",
                "message": "Consider increasing cash allocation to meet 5% minimum",
                "current_cash_pct": 3.2,
                "recommended_cash_pct": 5.0
            })
        
        return {"recommendations": recommendations}
    
    def get_compliance_rules(self) -> APIResponse:
        """Get all active compliance rules"""
        self._simulate_network_delay()
        
        rules_data = []
        for rule in self._rules.values():
            if rule.is_active:
                rules_data.append({
                    "rule_id": rule.rule_id,
                    "rule_name": rule.rule_name,
                    "description": rule.description,
                    "check_type": rule.check_type.value,
                    "severity": rule.severity
                })
        
        return self._create_response(data={
            "rules": rules_data,
            "total_active_rules": len(rules_data)
        })
    
    def get_compliance_history(self, account_id: str, days: int = 30) -> APIResponse:
        """Get compliance check history for an account"""
        self._simulate_network_delay()
        
        history = self._check_history.get(account_id, [])
        
        # Filter by date range
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        filtered_history = [
            check for check in history
            if datetime.fromisoformat(check["timestamp"]) >= cutoff_date
        ]
        
        return self._create_response(data={
            "account_id": account_id,
            "history": filtered_history,
            "total_checks": len(filtered_history),
            "date_range_days": days
        })