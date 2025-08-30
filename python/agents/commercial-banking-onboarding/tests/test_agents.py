"""Unit tests for commercial banking onboarding agents."""

import pytest
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from commercial_banking_onboarding.shared_libraries.types import (
    BusinessInfo, BeneficialOwner, EntityType, OnboardingApplication
)
from commercial_banking_onboarding.shared_libraries.utils import (
    generate_application_id, validate_tax_id, validate_email,
    calculate_business_age, normalize_business_name
)
from commercial_banking_onboarding.tools.orchestrator_tools import (
    create_onboarding_application, update_application_status
)


class TestSharedLibraries:
    """Test shared libraries and utilities."""
    
    def test_generate_application_id(self):
        """Test application ID generation."""
        app_id = generate_application_id()
        
        assert app_id.startswith("APP-")
        assert len(app_id) == 25  # APP-YYYYMMDDHHMMSS-XXXX format
        assert "-" in app_id
    
    def test_validate_tax_id(self):
        """Test tax ID validation."""
        # Valid EIN format
        assert validate_tax_id("12-3456789")
        
        # Valid SSN format  
        assert validate_tax_id("123-45-6789")
        
        # Invalid formats
        assert not validate_tax_id("123456789")
        assert not validate_tax_id("12-34567")
        assert not validate_tax_id("invalid")
    
    def test_validate_email(self):
        """Test email validation."""
        # Valid emails
        assert validate_email("test@example.com")
        assert validate_email("user.name@domain.co.uk")
        
        # Invalid emails
        assert not validate_email("invalid-email")
        assert not validate_email("@domain.com")
        assert not validate_email("user@")
    
    def test_calculate_business_age(self):
        """Test business age calculation."""
        # 2 years old
        incorporation_date = datetime(2022, 1, 1)
        age = calculate_business_age(incorporation_date)
        assert age >= 2
        
        # Brand new business
        incorporation_date = datetime.now()
        age = calculate_business_age(incorporation_date)
        assert age == 0
    
    def test_normalize_business_name(self):
        """Test business name normalization."""
        # Test suffix removal
        assert normalize_business_name("Acme Corp Inc") == "ACME CORP"
        assert normalize_business_name("Test Company LLC") == "TEST COMPANY"
        
        # Test special character removal
        assert normalize_business_name("ABC & Co.") == "ABC CO"
        assert normalize_business_name("XYZ-Corp") == "XYZCORP"


class TestBusinessInfo:
    """Test BusinessInfo data model."""
    
    def test_business_info_creation(self):
        """Test creating BusinessInfo object."""
        business_info = BusinessInfo(
            legal_name="Test Corp",
            entity_type=EntityType.CORPORATION,
            tax_id="12-3456789",
            incorporation_date=datetime(2020, 1, 1),
            business_address={
                "street": "123 Main St",
                "city": "Austin",
                "state": "TX",
                "zip_code": "78701"
            },
            industry_code="541511",
            description="Software development",
            phone="512-555-0100",
            email="info@testcorp.com"
        )
        
        assert business_info.legal_name == "Test Corp"
        assert business_info.entity_type == EntityType.CORPORATION
        assert business_info.tax_id == "12-3456789"


class TestBeneficialOwner:
    """Test BeneficialOwner data model."""
    
    def test_beneficial_owner_creation(self):
        """Test creating BeneficialOwner object."""
        owner = BeneficialOwner(
            first_name="John",
            last_name="Smith",
            date_of_birth=datetime(1980, 5, 15),
            ssn="123-45-6789",
            ownership_percentage=100.0,
            address={
                "street": "456 Oak St",
                "city": "Austin",
                "state": "TX",
                "zip_code": "78702"
            },
            phone="512-555-0101",
            email="john@example.com",
            is_control_person=True
        )
        
        assert owner.first_name == "John"
        assert owner.last_name == "Smith"
        assert owner.ownership_percentage == 100.0
        assert owner.is_control_person is True


class TestOrchestratorTools:
    """Test orchestrator agent tools."""
    
    def test_create_onboarding_application_success(self):
        """Test successful application creation."""
        business_info = {
            "legal_name": "Test Corp",
            "entity_type": "corporation",
            "tax_id": "12-3456789",
            "incorporation_date": "2020-01-01T00:00:00",
            "business_address": {
                "street": "123 Main St",
                "city": "Austin",
                "state": "TX",
                "zip_code": "78701"
            },
            "industry_code": "541511",
            "description": "Software development",
            "phone": "512-555-0100",
            "email": "info@testcorp.com"
        }
        
        beneficial_owners = [{
            "first_name": "John",
            "last_name": "Smith",
            "date_of_birth": "1980-05-15T00:00:00",
            "ssn": "123-45-6789",
            "ownership_percentage": 100.0,
            "address": {
                "street": "456 Oak St",
                "city": "Austin",
                "state": "TX",
                "zip_code": "78702"
            },
            "phone": "512-555-0101",
            "email": "john@example.com",
            "is_control_person": True
        }]
        
        result = create_onboarding_application(business_info, beneficial_owners)
        
        assert result["status"] == "created"
        assert "application_id" in result
        assert result["application_id"].startswith("APP-")
        assert "application" in result
        assert "audit_entry" in result
    
    def test_update_application_status_success(self):
        """Test successful status update."""
        app_id = "APP-20240101123456-ABCD"
        new_status = "kyc_completed"
        
        result = update_application_status(app_id, new_status, "KYC verification completed")
        
        assert result["status"] == "updated"
        assert result["application_id"] == app_id
        assert result["new_status"] == new_status
        assert "timestamp" in result
        assert "audit_entry" in result
    
    def test_update_application_status_invalid_status(self):
        """Test status update with invalid status."""
        app_id = "APP-20240101123456-ABCD"
        invalid_status = "invalid_status"
        
        result = update_application_status(app_id, invalid_status)
        
        assert result["status"] == "failed"
        assert "error" in result
        assert "Invalid status" in result["error"]


class TestKYCAgent:
    """Test KYC agent functionality."""
    
    @patch('commercial_banking_onboarding.sub_agents.kyc_agent.requests.post')
    def test_verify_business_identity_success(self, mock_post):
        """Test successful business identity verification."""
        # Import here to avoid circular imports
        from commercial_banking_onboarding.sub_agents.kyc_agent import verify_business_identity
        
        business_info = {
            "legal_name": "Test Corp",
            "tax_id": "12-3456789",
            "business_address": {
                "street": "123 Main St",
                "city": "Austin",
                "state": "TX",
                "zip_code": "78701"
            },
            "entity_type": "corporation"
        }
        
        # Mock API response
        mock_post.return_value.json.return_value = {"verified": True, "confidence": 90}
        mock_post.return_value.status_code = 200
        
        result = verify_business_identity(business_info)
        
        assert "verified" in result
        assert "confidence_score" in result
        assert result["verification_timestamp"]
    
    def test_verify_business_identity_missing_fields(self):
        """Test business verification with missing required fields."""
        from commercial_banking_onboarding.sub_agents.kyc_agent import verify_business_identity
        
        incomplete_info = {
            "legal_name": "Test Corp"
            # Missing tax_id and business_address
        }
        
        result = verify_business_identity(incomplete_info)
        
        assert result["verified"] is False
        assert "error" in result
        assert "Missing required fields" in result["error"]


class TestCreditAgent:
    """Test Credit agent functionality."""
    
    def test_analyze_financial_statements(self):
        """Test financial statement analysis."""
        from commercial_banking_onboarding.sub_agents.credit_agent import analyze_financial_statements
        
        financial_data = {
            "annual_revenue": 2500000,
            "total_assets": 2000000,
            "total_liabilities": 1200000,
            "net_income": 300000,
            "current_assets": 800000,
            "current_liabilities": 400000,
            "annual_debt_payments": 150000
        }
        
        result = analyze_financial_statements(financial_data)
        
        assert result["success"] is True
        assert "financial_ratios" in result
        assert "financial_health" in result
        
        ratios = result["financial_ratios"]
        assert "current_ratio" in ratios
        assert "debt_to_assets" in ratios
        assert "profit_margin" in ratios
        
        # Verify ratio calculations
        assert ratios["current_ratio"] == 2.0  # 800k / 400k
        assert ratios["debt_to_assets"] == 0.6  # 1.2M / 2M


class TestComplianceAgent:
    """Test Compliance agent functionality."""
    
    def test_perform_sanctions_screening_clean(self):
        """Test sanctions screening with clean results."""
        from commercial_banking_onboarding.sub_agents.compliance_agent import perform_sanctions_screening
        
        business_info = {
            "legal_name": "Clean Corp",
            "business_address": {
                "city": "Austin",
                "state": "TX",
                "country": "US"
            }
        }
        
        beneficial_owners = [{
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1980-01-01T00:00:00"
        }]
        
        result = perform_sanctions_screening(business_info, beneficial_owners)
        
        assert "passed_screening" in result
        assert "screening_results" in result
        assert "screening_timestamp" in result
    
    def test_assess_geographic_risk(self):
        """Test geographic risk assessment."""
        from commercial_banking_onboarding.sub_agents.compliance_agent import assess_geographic_risk
        
        # Test high-risk country
        high_risk_address = {"country": "IRAN", "state": ""}
        result = assess_geographic_risk(high_risk_address)
        
        assert result["risk_score"] > 0
        assert len(result["risk_factors"]) > 0
        assert "High-risk country" in result["risk_factors"][0]
        
        # Test low-risk address
        low_risk_address = {"country": "US", "state": "TX"}
        result = assess_geographic_risk(low_risk_address)
        
        assert result["risk_score"] < 20  # Should be low risk


class TestDocumentAgent:
    """Test Document agent functionality."""
    
    def test_simulate_document_extraction(self):
        """Test document data extraction simulation."""
        from commercial_banking_onboarding.sub_agents.document_agent import simulate_document_extraction
        
        # Test articles of incorporation
        result = simulate_document_extraction("articles_of_incorporation")
        
        assert "business_name" in result
        assert "entity_type" in result
        assert "incorporation_date" in result
        assert "state_of_incorporation" in result
    
    def test_validate_extracted_data(self):
        """Test extracted data validation."""
        from commercial_banking_onboarding.sub_agents.document_agent import validate_extracted_data
        
        # Complete data
        complete_data = {
            "business_name": "Test Corp",
            "entity_type": "corporation",
            "incorporation_date": "2020-01-01",
            "state_of_incorporation": "Delaware"
        }
        
        result = validate_extracted_data("articles_of_incorporation", complete_data)
        
        assert result["valid"] is True
        assert result["confidence_score"] == 100
        assert len(result["missing_fields"]) == 0
        
        # Incomplete data
        incomplete_data = {
            "business_name": "Test Corp"
        }
        
        result = validate_extracted_data("articles_of_incorporation", incomplete_data)
        
        assert result["valid"] is False
        assert result["confidence_score"] < 100
        assert len(result["missing_fields"]) > 0


class TestAccountSetupAgent:
    """Test Account Setup agent functionality."""
    
    def test_create_business_accounts(self):
        """Test business account creation."""
        from commercial_banking_onboarding.sub_agents.account_setup_agent import create_business_accounts
        
        app_id = "APP-20240101123456-ABCD"
        account_types = ["CHK", "SAV", "LOC"]
        credit_limit = 100000.0
        
        result = create_business_accounts(app_id, account_types, credit_limit)
        
        assert result["success"] is True
        assert result["accounts_created"] == 3
        assert len(result["account_numbers"]) == 3
        assert "CHK" in result["account_numbers"]
        assert "SAV" in result["account_numbers"]
        assert "LOC" in result["account_numbers"]
    
    def test_generate_company_id(self):
        """Test company ID generation."""
        from commercial_banking_onboarding.sub_agents.account_setup_agent import generate_company_id
        
        business_name = "TechStart Corporation"
        company_id = generate_company_id(business_name)
        
        assert len(company_id) == 14  # 8 chars + 6 hex chars
        assert company_id.startswith("TECHSTAR")
        assert company_id.isupper()
    
    def test_determine_manager_tier(self):
        """Test relationship manager tier determination."""
        from commercial_banking_onboarding.sub_agents.account_setup_agent import determine_manager_tier
        
        # Test different revenue levels
        assert determine_manager_tier(15000000, 5) == "senior_commercial"
        assert determine_manager_tier(7500000, 3) == "commercial"
        assert determine_manager_tier(2000000, 2) == "business_banking"
        assert determine_manager_tier(500000, 1) == "small_business"


@pytest.fixture
def sample_business_info():
    """Fixture providing sample business information."""
    return {
        "legal_name": "Test Corporation",
        "entity_type": "corporation",
        "tax_id": "12-3456789",
        "incorporation_date": "2020-01-01T00:00:00",
        "business_address": {
            "street": "123 Main St",
            "city": "Austin",
            "state": "TX",
            "zip_code": "78701",
            "country": "US"
        },
        "industry_code": "541511",
        "description": "Software development services",
        "phone": "512-555-0100",
        "email": "info@testcorp.com",
        "annual_revenue": 2500000
    }


@pytest.fixture
def sample_beneficial_owners():
    """Fixture providing sample beneficial owners."""
    return [{
        "first_name": "John",
        "last_name": "Smith",
        "date_of_birth": "1980-05-15T00:00:00",
        "ssn": "123-45-6789",
        "ownership_percentage": 100.0,
        "address": {
            "street": "456 Oak St",
            "city": "Austin",
            "state": "TX",
            "zip_code": "78702",
            "country": "US"
        },
        "phone": "512-555-0101",
        "email": "john@example.com",
        "is_control_person": True
    }]


class TestIntegration:
    """Integration tests for the complete onboarding workflow."""
    
    def test_complete_workflow_simulation(self, sample_business_info, sample_beneficial_owners):
        """Test complete onboarding workflow."""
        # Create application
        result = create_onboarding_application(sample_business_info, sample_beneficial_owners)
        assert result["status"] == "created"
        
        app_id = result["application_id"]
        
        # Update status through workflow
        statuses = ["documents_received", "kyc_in_progress", "kyc_completed", 
                   "credit_assessment", "compliance_screening", "account_setup"]
        
        for status in statuses:
            result = update_application_status(app_id, status)
            assert result["status"] == "updated"
            assert result["new_status"] == status


if __name__ == "__main__":
    pytest.main([__file__, "-v"])