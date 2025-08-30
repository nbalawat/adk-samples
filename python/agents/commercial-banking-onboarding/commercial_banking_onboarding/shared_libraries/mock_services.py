"""Mock services to simulate external API calls for commercial banking onboarding."""

import json
import random
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import hashlib
import logging

logger = logging.getLogger(__name__)


class MockServiceBase:
    """Base class for mock services."""
    
    def __init__(self, enable_failures: bool = False, failure_rate: float = 0.1):
        """Initialize mock service.
        
        Args:
            enable_failures: Whether to simulate random failures
            failure_rate: Probability of failure (0.0 to 1.0)
        """
        self.enable_failures = enable_failures
        self.failure_rate = failure_rate
        self.call_count = 0
    
    def _simulate_network_delay(self, min_ms: int = 100, max_ms: int = 2000):
        """Simulate network latency."""
        delay = random.uniform(min_ms, max_ms) / 1000
        time.sleep(delay)
    
    def _should_fail(self) -> bool:
        """Determine if this call should fail."""
        return self.enable_failures and random.random() < self.failure_rate
    
    def _log_api_call(self, service_name: str, method: str, params: Dict[str, Any]):
        """Log API call for debugging."""
        self.call_count += 1
        logger.info(f"Mock {service_name} API call #{self.call_count}: {method} - {params}")


class MockKYCService(MockServiceBase):
    """Mock KYC verification service."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Mock database of known entities
        self.business_database = {
            "ACME CORPORATION": {
                "verified": True,
                "confidence": 95,
                "incorporation_date": "2020-01-15",
                "status": "active"
            },
            "TEST COMPANY LLC": {
                "verified": True,
                "confidence": 88,
                "incorporation_date": "2021-03-10",
                "status": "active"
            },
            "FRAUDULENT CORP": {
                "verified": False,
                "confidence": 15,
                "flags": ["suspicious_activity", "potential_fraud"]
            },
            "SANCTIONED BUSINESS": {
                "verified": False,
                "confidence": 0,
                "flags": ["sanctions_match"]
            }
        }
        
        self.individual_database = {
            "JOHN SMITH": {
                "verified": True,
                "confidence": 92,
                "ssn_verified": True,
                "address_verified": True
            },
            "JANE DOE": {
                "verified": True,
                "confidence": 89,
                "ssn_verified": True,
                "address_verified": True
            },
            "CRIMINAL PERSON": {
                "verified": False,
                "confidence": 20,
                "flags": ["criminal_record", "high_risk"]
            }
        }
    
    def verify_business_identity(self, business_name: str, tax_id: str, address: Dict[str, Any]) -> Dict[str, Any]:
        """Mock business identity verification."""
        self._log_api_call("KYC", "verify_business_identity", {
            "business_name": business_name, "tax_id": tax_id[-4:]
        })
        self._simulate_network_delay(500, 3000)
        
        if self._should_fail():
            return {
                "success": False,
                "error": "KYC service temporarily unavailable",
                "retry_after": 300
            }
        
        business_key = business_name.upper().strip()
        business_data = self.business_database.get(business_key, {
            "verified": True,
            "confidence": random.randint(70, 95),
            "status": "active"
        })
        
        # Add some variability to mock responses
        confidence_variance = random.randint(-5, 5)
        final_confidence = max(0, min(100, business_data.get("confidence", 85) + confidence_variance))
        
        result = {
            "success": True,
            "business_name": business_name,
            "tax_id_last_4": tax_id[-4:] if tax_id else "****",
            "verified": business_data.get("verified", True),
            "confidence_score": final_confidence,
            "verification_method": "document_cross_reference",
            "status": business_data.get("status", "active"),
            "flags": business_data.get("flags", []),
            "verified_fields": ["business_name", "tax_id", "address"],
            "verification_timestamp": datetime.now().isoformat()
        }
        
        return result
    
    def verify_individual(self, first_name: str, last_name: str, ssn: str, 
                         date_of_birth: str, address: Dict[str, Any]) -> Dict[str, Any]:
        """Mock individual identity verification."""
        full_name = f"{first_name} {last_name}"
        self._log_api_call("KYC", "verify_individual", {
            "name": full_name, "ssn": "***-**-" + ssn[-4:] if ssn else "****"
        })
        self._simulate_network_delay(300, 2000)
        
        if self._should_fail():
            return {
                "success": False,
                "error": "Identity verification service unavailable"
            }
        
        person_key = full_name.upper().strip()
        person_data = self.individual_database.get(person_key, {
            "verified": True,
            "confidence": random.randint(75, 95),
            "ssn_verified": True,
            "address_verified": True
        })
        
        return {
            "success": True,
            "name": full_name,
            "ssn_last_4": ssn[-4:] if ssn else "****",
            "verified": person_data.get("verified", True),
            "confidence_score": person_data.get("confidence", 85),
            "ssn_verified": person_data.get("ssn_verified", True),
            "address_verified": person_data.get("address_verified", True),
            "flags": person_data.get("flags", []),
            "verification_timestamp": datetime.now().isoformat()
        }
    
    def screen_pep(self, full_name: str, date_of_birth: str) -> Dict[str, Any]:
        """Mock PEP (Politically Exposed Persons) screening."""
        self._log_api_call("KYC", "screen_pep", {"name": full_name})
        self._simulate_network_delay(200, 1500)
        
        if self._should_fail():
            return {
                "success": False,
                "error": "PEP screening service unavailable"
            }
        
        # Mock PEP matches
        pep_names = [
            "POLITICAL PERSON",
            "GOVERNMENT OFFICIAL", 
            "FOREIGN MINISTER",
            "SENATOR SMITH"
        ]
        
        is_pep = any(pep_name in full_name.upper() for pep_name in pep_names)
        
        result = {
            "success": True,
            "name": full_name,
            "is_pep": is_pep,
            "confidence_score": 95 if is_pep else 2,
            "matches": [],
            "risk_level": "high" if is_pep else "low"
        }
        
        if is_pep:
            result["matches"] = [{
                "name": full_name,
                "position": "Government Official",
                "country": "Various",
                "match_confidence": 95,
                "last_updated": "2024-01-01"
            }]
        
        return result


class MockCreditBureauService(MockServiceBase):
    """Mock credit bureau service."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Mock credit profiles
        self.credit_profiles = {
            "12-3456789": {
                "business_name": "Acme Corporation",
                "credit_score": 750,
                "payment_history_score": 85,
                "credit_utilization": 0.35,
                "years_on_file": 4,
                "total_tradelines": 6,
                "bankruptcies": 0,
                "liens": 0,
                "judgments": 0
            },
            "98-7654321": {
                "business_name": "High Risk LLC",
                "credit_score": 520,
                "payment_history_score": 45,
                "credit_utilization": 0.85,
                "years_on_file": 1,
                "total_tradelines": 2,
                "bankruptcies": 0,
                "liens": 1,
                "judgments": 0
            }
        }
    
    def get_credit_report(self, tax_id: str, business_name: str) -> Dict[str, Any]:
        """Mock credit bureau report."""
        self._log_api_call("CreditBureau", "get_credit_report", {
            "tax_id": tax_id[-4:], "business_name": business_name
        })
        self._simulate_network_delay(1000, 5000)
        
        if self._should_fail():
            return {
                "success": False,
                "error": "Credit bureau service temporarily unavailable",
                "retry_after": 600
            }
        
        # Get profile or create random one
        profile = self.credit_profiles.get(tax_id, self._generate_random_credit_profile(business_name))
        
        return {
            "success": True,
            "report_id": f"CR-{datetime.now().strftime('%Y%m%d')}-{hash(tax_id) % 10000:04d}",
            "business_name": profile["business_name"],
            "tax_id_last_4": tax_id[-4:],
            "credit_score": profile["credit_score"],
            "credit_score_range": "300-850",
            "score_factors": self._get_score_factors(profile["credit_score"]),
            "payment_history": {
                "score": profile["payment_history_score"],
                "rating": self._get_payment_rating(profile["payment_history_score"]),
                "late_payments_12mo": random.randint(0, 3),
                "missed_payments_12mo": random.randint(0, 1)
            },
            "credit_utilization": {
                "ratio": profile["credit_utilization"],
                "total_credit_limit": random.randint(50000, 500000),
                "total_balance": int(random.randint(50000, 500000) * profile["credit_utilization"])
            },
            "trade_lines": {
                "total": profile["total_tradelines"],
                "open": profile["total_tradelines"] - random.randint(0, 1),
                "closed": random.randint(0, 1)
            },
            "public_records": {
                "bankruptcies": profile["bankruptcies"],
                "liens": profile["liens"], 
                "judgments": profile["judgments"]
            },
            "years_on_file": profile["years_on_file"],
            "inquiries_12mo": random.randint(1, 5),
            "report_date": datetime.now().isoformat()
        }
    
    def _generate_random_credit_profile(self, business_name: str) -> Dict[str, Any]:
        """Generate random credit profile for unknown businesses."""
        base_score = random.randint(550, 780)
        
        return {
            "business_name": business_name,
            "credit_score": base_score,
            "payment_history_score": max(30, base_score - random.randint(0, 100)),
            "credit_utilization": random.uniform(0.1, 0.7),
            "years_on_file": random.randint(1, 10),
            "total_tradelines": random.randint(2, 12),
            "bankruptcies": 0 if base_score > 600 else random.randint(0, 1),
            "liens": random.randint(0, 2) if base_score < 650 else 0,
            "judgments": random.randint(0, 1) if base_score < 600 else 0
        }
    
    def _get_score_factors(self, score: int) -> List[str]:
        """Get factors affecting credit score."""
        factors = []
        
        if score >= 750:
            factors = ["Strong payment history", "Low credit utilization", "Established credit history"]
        elif score >= 650:
            factors = ["Good payment history", "Moderate credit utilization"]
        elif score >= 550:
            factors = ["Some late payments", "High credit utilization", "Limited credit history"]
        else:
            factors = ["Poor payment history", "Very high utilization", "Public records"]
        
        return factors
    
    def _get_payment_rating(self, score: int) -> str:
        """Get payment history rating."""
        if score >= 80:
            return "excellent"
        elif score >= 60:
            return "good"
        elif score >= 40:
            return "fair"
        else:
            return "poor"


class MockComplianceService(MockServiceBase):
    """Mock compliance screening service."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Mock sanctions lists
        self.sanctions_list = [
            "SANCTIONED CORPORATION",
            "BLOCKED ENTITY LLC",
            "PROHIBITED BUSINESS",
            "CRIMINAL ENTERPRISES"
        ]
        
        self.pep_list = [
            "POLITICAL FIGURE",
            "GOVERNMENT MINISTER",
            "FOREIGN OFFICIAL"
        ]
    
    def screen_sanctions(self, entities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Mock sanctions screening."""
        self._log_api_call("Compliance", "screen_sanctions", {
            "entities": len(entities)
        })
        self._simulate_network_delay(800, 3000)
        
        if self._should_fail():
            return {
                "success": False,
                "error": "Sanctions screening service unavailable"
            }
        
        matches = []
        
        for entity in entities:
            entity_name = entity.get("name", "").upper()
            entity_type = entity.get("type", "unknown")
            
            # Check for sanctions matches
            for sanctioned_name in self.sanctions_list:
                if sanctioned_name in entity_name or entity_name in sanctioned_name:
                    matches.append({
                        "entity_name": entity.get("name"),
                        "entity_type": entity_type,
                        "matched_name": sanctioned_name,
                        "list": "OFAC_SDN",
                        "match_confidence": random.randint(85, 99),
                        "risk_level": "high"
                    })
        
        return {
            "success": True,
            "screening_id": f"SAN-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "entities_screened": len(entities),
            "matches_found": len(matches),
            "matches": matches,
            "lists_checked": ["OFAC_SDN", "UN_Consolidated", "EU_Sanctions"],
            "screening_timestamp": datetime.now().isoformat(),
            "passed": len(matches) == 0
        }
    
    def aml_risk_assessment(self, business_info: Dict[str, Any], 
                          owners: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Mock AML risk assessment."""
        self._log_api_call("Compliance", "aml_risk_assessment", {
            "business": business_info.get("legal_name"), 
            "owners": len(owners)
        })
        self._simulate_network_delay(1500, 4000)
        
        if self._should_fail():
            return {
                "success": False,
                "error": "AML assessment service unavailable"
            }
        
        risk_score = 0
        risk_factors = []
        
        # Industry risk
        industry_code = business_info.get("industry_code", "")
        high_risk_industries = ["522291", "713", "531"]  # MSB, Gaming, Real Estate
        
        if industry_code in high_risk_industries:
            risk_score += 30
            risk_factors.append(f"High-risk industry: {industry_code}")
        
        # Geographic risk
        address = business_info.get("business_address", {})
        high_risk_states = ["NV", "FL"]  # High-risk jurisdictions
        if address.get("state") in high_risk_states:
            risk_score += 15
            risk_factors.append("High-risk geographic location")
        
        # Ownership complexity
        if len(owners) > 5:
            risk_score += 10
            risk_factors.append("Complex ownership structure")
        
        # Foreign ownership
        foreign_owners = sum(1 for owner in owners 
                           if owner.get("address", {}).get("country", "US") != "US")
        if foreign_owners > 0:
            risk_score += foreign_owners * 5
            risk_factors.append(f"{foreign_owners} foreign beneficial owner(s)")
        
        # Cash-intensive indicators
        business_desc = business_info.get("description", "").lower()
        cash_keywords = ["cash", "atm", "money", "currency"]
        if any(keyword in business_desc for keyword in cash_keywords):
            risk_score += 20
            risk_factors.append("Cash-intensive business model")
        
        # Determine risk level
        if risk_score >= 60:
            risk_level = "very_high"
        elif risk_score >= 40:
            risk_level = "high"
        elif risk_score >= 20:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "success": True,
            "assessment_id": f"AML-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "overall_risk_score": risk_score,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "enhanced_due_diligence_required": risk_level in ["high", "very_high"],
            "assessment_timestamp": datetime.now().isoformat(),
            "recommendations": self._get_aml_recommendations(risk_level)
        }
    
    def _get_aml_recommendations(self, risk_level: str) -> List[str]:
        """Get AML recommendations based on risk level."""
        recommendations = {
            "low": ["Standard monitoring procedures", "Annual review"],
            "medium": ["Enhanced monitoring", "Quarterly review", "Transaction monitoring"],
            "high": ["Enhanced due diligence", "Monthly review", "Senior management approval"],
            "very_high": ["Extensive due diligence", "Weekly monitoring", "Regulatory notification"]
        }
        return recommendations.get(risk_level, [])


class MockDocumentProcessingService(MockServiceBase):
    """Mock document processing/AI service."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def extract_document_data(self, document_type: str, file_content: bytes = None,
                            file_name: str = None) -> Dict[str, Any]:
        """Mock document data extraction using AI/OCR."""
        self._log_api_call("DocumentAI", "extract_document_data", {
            "document_type": document_type, "file_name": file_name
        })
        self._simulate_network_delay(2000, 8000)  # Document processing takes longer
        
        if self._should_fail():
            return {
                "success": False,
                "error": "Document processing service unavailable"
            }
        
        # Mock extracted data based on document type
        extracted_data = self._get_mock_extracted_data(document_type, file_name)
        
        # Add some realistic extraction confidence
        confidence = random.uniform(85, 99)
        
        return {
            "success": True,
            "document_type": document_type,
            "file_name": file_name,
            "extraction_confidence": confidence,
            "extracted_data": extracted_data,
            "processing_time_ms": random.randint(1000, 5000),
            "pages_processed": random.randint(1, 3),
            "extraction_timestamp": datetime.now().isoformat()
        }
    
    def _get_mock_extracted_data(self, doc_type: str, file_name: str = None) -> Dict[str, Any]:
        """Generate mock extracted data based on document type."""
        base_business_name = "Sample Business Corp"
        if file_name:
            # Try to infer business name from filename
            name_parts = file_name.replace("_", " ").replace("-", " ").split()
            if len(name_parts) > 1:
                base_business_name = " ".join(name_parts[:2]).title() + " Corp"
        
        mock_data = {
            "articles_of_incorporation": {
                "business_name": base_business_name,
                "entity_type": "corporation",
                "incorporation_date": "2020-01-15",
                "state_of_incorporation": "Delaware",
                "registered_agent": "Corporate Services Inc.",
                "authorized_shares": 10000000,
                "incorporator_name": "John Smith",
                "incorporation_number": f"DE-{random.randint(1000000, 9999999)}"
            },
            "business_license": {
                "license_number": f"BL-2024-{random.randint(100000, 999999)}",
                "business_name": base_business_name,
                "license_type": "General Business License", 
                "issue_date": "2024-01-01",
                "expiration_date": "2024-12-31",
                "issuing_authority": "City Business Department",
                "license_status": "active"
            },
            "tax_id_certificate": {
                "tax_id": f"{random.randint(10, 99)}-{random.randint(1000000, 9999999)}",
                "business_name": base_business_name,
                "entity_type": "corporation",
                "issue_date": "2020-01-20",
                "issuing_authority": "Internal Revenue Service"
            },
            "financial_statements": {
                "reporting_period": "2023-12-31",
                "business_name": base_business_name,
                "annual_revenue": random.randint(500000, 10000000),
                "net_income": random.randint(50000, 1000000),
                "total_assets": random.randint(1000000, 5000000),
                "total_liabilities": random.randint(500000, 3000000),
                "current_assets": random.randint(200000, 2000000),
                "current_liabilities": random.randint(100000, 1000000),
                "prepared_by": "CPA Firm LLC",
                "audit_opinion": "unqualified"
            },
            "beneficial_ownership": {
                "certification_date": "2024-01-01",
                "business_name": base_business_name,
                "beneficial_owners": [
                    {
                        "name": "John Smith",
                        "ownership_percentage": 60,
                        "control_person": True,
                        "address": "123 Main St, City, ST 12345"
                    },
                    {
                        "name": "Jane Doe",
                        "ownership_percentage": 40, 
                        "control_person": False,
                        "address": "456 Oak Ave, City, ST 12345"
                    }
                ],
                "certifying_individual": "John Smith",
                "certification_title": "CEO"
            }
        }
        
        return mock_data.get(doc_type, {
            "document_type": doc_type,
            "extraction_note": f"Generic extraction for {doc_type}",
            "raw_text_sample": "Sample extracted text content..."
        })


class MockBankingSystemService(MockServiceBase):
    """Mock internal banking system API."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.created_accounts = {}
        self.user_credentials = {}
    
    def create_account(self, account_type: str, account_config: Dict[str, Any]) -> Dict[str, Any]:
        """Mock account creation in banking system."""
        self._log_api_call("BankingSystem", "create_account", {
            "account_type": account_type
        })
        self._simulate_network_delay(500, 2000)
        
        if self._should_fail():
            return {
                "success": False,
                "error": "Banking system temporarily unavailable"
            }
        
        # Generate account number
        account_number = self._generate_account_number(account_type)
        
        account_info = {
            "account_number": account_number,
            "account_type": account_type,
            "status": "active",
            "opening_date": datetime.now().isoformat(),
            "balance": account_config.get("initial_deposit", 0),
            "currency": "USD",
            "routing_number": "123456789",
            "account_title": account_config.get("account_title", "Business Account")
        }
        
        # Add account-specific features
        if account_type == "CHK":
            account_info.update({
                "check_writing_enabled": True,
                "debit_card_eligible": True,
                "overdraft_protection": account_config.get("overdraft_protection", False)
            })
        elif account_type in ["LOC", "LOAN"]:
            account_info.update({
                "credit_limit": account_config.get("credit_limit", 0),
                "available_credit": account_config.get("credit_limit", 0),
                "interest_rate": account_config.get("interest_rate", 6.5)
            })
        
        self.created_accounts[account_number] = account_info
        
        return {
            "success": True,
            "account_number": account_number,
            "account_info": account_info,
            "creation_timestamp": datetime.now().isoformat()
        }
    
    def setup_online_banking(self, business_name: str, users: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Mock online banking setup."""
        self._log_api_call("BankingSystem", "setup_online_banking", {
            "business_name": business_name, "users": len(users)
        })
        self._simulate_network_delay(1000, 3000)
        
        if self._should_fail():
            return {
                "success": False,
                "error": "Online banking system unavailable"
            }
        
        company_id = self._generate_company_id(business_name)
        user_credentials = []
        
        for user in users:
            username = self._generate_username(user.get("name", ""), company_id)
            temp_password = self._generate_temp_password()
            
            user_cred = {
                "user_id": f"U{random.randint(100000, 999999)}",
                "username": username,
                "temporary_password": temp_password,
                "name": user.get("name"),
                "email": user.get("email"),
                "role": user.get("role", "user"),
                "status": "active",
                "password_change_required": True,
                "setup_timestamp": datetime.now().isoformat()
            }
            
            user_credentials.append(user_cred)
            self.user_credentials[username] = user_cred
        
        return {
            "success": True,
            "company_id": company_id,
            "online_banking_url": "https://business.mockbank.com/login",
            "user_credentials": user_credentials,
            "setup_complete": True
        }
    
    def order_materials(self, account_numbers: List[str], materials: List[str],
                       delivery_address: Dict[str, Any]) -> Dict[str, Any]:
        """Mock banking materials order."""
        self._log_api_call("BankingSystem", "order_materials", {
            "accounts": len(account_numbers), "materials": materials
        })
        self._simulate_network_delay(300, 1000)
        
        if self._should_fail():
            return {
                "success": False,
                "error": "Materials ordering system unavailable"
            }
        
        order_id = f"ORD-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        estimated_delivery = datetime.now() + timedelta(days=random.randint(5, 10))
        
        material_details = []
        total_cost = 0
        
        for material in materials:
            cost = self._get_material_cost(material)
            material_details.append({
                "item": material,
                "quantity": 1,
                "cost": cost,
                "estimated_delivery": estimated_delivery.isoformat()
            })
            total_cost += cost
        
        return {
            "success": True,
            "order_id": order_id,
            "materials": material_details,
            "total_cost": total_cost,
            "delivery_address": delivery_address,
            "estimated_delivery_date": estimated_delivery.isoformat(),
            "tracking_number": f"TRK{random.randint(1000000000, 9999999999)}",
            "order_timestamp": datetime.now().isoformat()
        }
    
    def _generate_account_number(self, account_type: str) -> str:
        """Generate mock account number."""
        prefixes = {
            "CHK": "1001",
            "SAV": "2001", 
            "LOC": "3001",
            "LOAN": "4001",
            "MM": "5001"
        }
        prefix = prefixes.get(account_type, "1001")
        suffix = random.randint(100000000, 999999999)
        return f"{prefix}{suffix}"
    
    def _generate_company_id(self, business_name: str) -> str:
        """Generate company ID for online banking."""
        clean_name = ''.join(c for c in business_name if c.isalnum())[:8].upper()
        random_suffix = f"{random.randint(100, 999)}"
        return f"{clean_name}{random_suffix}"
    
    def _generate_username(self, full_name: str, company_id: str) -> str:
        """Generate username for online banking."""
        name_parts = full_name.strip().split()
        if len(name_parts) >= 2:
            username_base = f"{name_parts[0][0]}{name_parts[-1]}".lower()
        else:
            username_base = name_parts[0][:8].lower()
        
        return f"{company_id[:4].lower()}{username_base}{random.randint(10, 99)}"
    
    def _generate_temp_password(self) -> str:
        """Generate temporary password."""
        import string
        chars = string.ascii_letters + string.digits + "!@#$%"
        return ''.join(random.choice(chars) for _ in range(12))
    
    def _get_material_cost(self, material: str) -> float:
        """Get cost for banking materials."""
        costs = {
            "business_checks": 35.00,
            "deposit_slips": 15.00,
            "debit_cards": 0.00,
            "welcome_kit": 0.00,
            "starter_kit": 25.00
        }
        return costs.get(material, 10.00)


# Global mock service instances
mock_kyc_service = MockKYCService()
mock_credit_bureau = MockCreditBureauService()
mock_compliance_service = MockComplianceService()
mock_document_service = MockDocumentProcessingService()
mock_banking_system = MockBankingSystemService()