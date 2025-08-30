"""Shared types and data models for commercial banking onboarding."""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class EntityType(str, Enum):
    CORPORATION = "corporation"
    LLC = "llc" 
    PARTNERSHIP = "partnership"
    SOLE_PROPRIETORSHIP = "sole_proprietorship"
    TRUST = "trust"
    NON_PROFIT = "non_profit"


class DocumentType(str, Enum):
    ARTICLES_OF_INCORPORATION = "articles_of_incorporation"
    BUSINESS_LICENSE = "business_license"
    TAX_ID_CERTIFICATE = "tax_id_certificate"
    FINANCIAL_STATEMENTS = "financial_statements"
    BANK_STATEMENTS = "bank_statements"
    BENEFICIAL_OWNERSHIP = "beneficial_ownership"
    OPERATING_AGREEMENT = "operating_agreement"
    PARTNERSHIP_AGREEMENT = "partnership_agreement"


class OnboardingStatus(str, Enum):
    INITIATED = "initiated"
    DOCUMENTS_RECEIVED = "documents_received"
    KYC_IN_PROGRESS = "kyc_in_progress"
    KYC_COMPLETED = "kyc_completed"
    CREDIT_ASSESSMENT = "credit_assessment"
    COMPLIANCE_SCREENING = "compliance_screening"
    ACCOUNT_SETUP = "account_setup"
    COMPLETED = "completed"
    REJECTED = "rejected"
    REQUIRES_MANUAL_REVIEW = "requires_manual_review"


class RiskRating(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class BusinessInfo(BaseModel):
    """Business information for onboarding."""
    legal_name: str = Field(..., description="Legal business name")
    dba_name: Optional[str] = Field(None, description="Doing business as name")
    entity_type: EntityType = Field(..., description="Type of business entity")
    tax_id: str = Field(..., description="Tax identification number")
    incorporation_date: datetime = Field(..., description="Date of incorporation")
    business_address: Dict[str, str] = Field(..., description="Business address")
    mailing_address: Optional[Dict[str, str]] = Field(None, description="Mailing address")
    industry_code: str = Field(..., description="NAICS industry code")
    description: str = Field(..., description="Business description")
    phone: str = Field(..., description="Business phone number")
    email: str = Field(..., description="Business email address")
    website: Optional[str] = Field(None, description="Business website")


class BeneficialOwner(BaseModel):
    """Information about beneficial owner."""
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    date_of_birth: datetime = Field(..., description="Date of birth")
    ssn: str = Field(..., description="Social Security Number")
    ownership_percentage: float = Field(..., description="Ownership percentage", ge=0, le=100)
    address: Dict[str, str] = Field(..., description="Home address")
    phone: str = Field(..., description="Phone number")
    email: str = Field(..., description="Email address")
    is_control_person: bool = Field(..., description="Has significant control")


class DocumentInfo(BaseModel):
    """Document information."""
    document_id: str = Field(..., description="Unique document identifier")
    document_type: DocumentType = Field(..., description="Type of document")
    file_name: str = Field(..., description="Original file name")
    file_size: int = Field(..., description="File size in bytes")
    mime_type: str = Field(..., description="MIME type")
    upload_timestamp: datetime = Field(..., description="Upload timestamp")
    extracted_data: Optional[Dict[str, Any]] = Field(None, description="Extracted document data")
    validation_status: str = Field("pending", description="Document validation status")


class KYCResult(BaseModel):
    """KYC verification result."""
    business_verified: bool = Field(..., description="Business identity verified")
    owners_verified: bool = Field(..., description="All owners verified")
    pep_check_passed: bool = Field(..., description="PEP screening passed")
    adverse_media_check_passed: bool = Field(..., description="Adverse media check passed")
    verification_score: float = Field(..., description="Verification confidence score", ge=0, le=100)
    risk_factors: List[str] = Field(default_factory=list, description="Identified risk factors")
    manual_review_required: bool = Field(..., description="Requires manual review")


class CreditAssessment(BaseModel):
    """Credit assessment result."""
    credit_score: Optional[int] = Field(None, description="Business credit score")
    risk_rating: RiskRating = Field(..., description="Overall risk rating")
    debt_to_income_ratio: Optional[float] = Field(None, description="Debt to income ratio")
    annual_revenue: Optional[float] = Field(None, description="Annual revenue")
    years_in_business: Optional[int] = Field(None, description="Years in business")
    credit_utilization: Optional[float] = Field(None, description="Credit utilization ratio")
    payment_history_score: Optional[int] = Field(None, description="Payment history score")
    recommended_credit_limit: Optional[float] = Field(None, description="Recommended credit limit")
    assessment_notes: List[str] = Field(default_factory=list, description="Assessment notes")


class ComplianceResult(BaseModel):
    """Compliance screening result."""
    sanctions_check_passed: bool = Field(..., description="Sanctions screening passed")
    aml_check_passed: bool = Field(..., description="AML screening passed")
    ofac_check_passed: bool = Field(..., description="OFAC screening passed")
    politically_exposed_persons: List[str] = Field(default_factory=list, description="PEP matches")
    sanctions_matches: List[str] = Field(default_factory=list, description="Sanctions matches")
    adverse_media_findings: List[str] = Field(default_factory=list, description="Adverse media")
    compliance_score: float = Field(..., description="Compliance score", ge=0, le=100)
    manual_review_required: bool = Field(..., description="Requires manual review")


class AccountConfiguration(BaseModel):
    """Account setup configuration."""
    account_types: List[str] = Field(..., description="Types of accounts to create")
    services: List[str] = Field(..., description="Banking services to activate")
    initial_deposit_amount: Optional[float] = Field(None, description="Initial deposit amount")
    overdraft_protection: bool = Field(False, description="Enable overdraft protection")
    online_banking: bool = Field(True, description="Enable online banking")
    mobile_banking: bool = Field(True, description="Enable mobile banking")
    debit_cards: int = Field(0, description="Number of debit cards")
    credit_limit: Optional[float] = Field(None, description="Credit limit if applicable")


class OnboardingApplication(BaseModel):
    """Complete onboarding application."""
    application_id: str = Field(..., description="Unique application identifier")
    status: OnboardingStatus = Field(OnboardingStatus.INITIATED, description="Current status")
    created_timestamp: datetime = Field(default_factory=datetime.now, description="Creation time")
    updated_timestamp: datetime = Field(default_factory=datetime.now, description="Last update")
    
    business_info: BusinessInfo = Field(..., description="Business information")
    beneficial_owners: List[BeneficialOwner] = Field(..., description="Beneficial owners")
    documents: List[DocumentInfo] = Field(default_factory=list, description="Uploaded documents")
    
    kyc_result: Optional[KYCResult] = Field(None, description="KYC verification result")
    credit_assessment: Optional[CreditAssessment] = Field(None, description="Credit assessment")
    compliance_result: Optional[ComplianceResult] = Field(None, description="Compliance result")
    account_config: Optional[AccountConfiguration] = Field(None, description="Account configuration")
    
    notes: List[str] = Field(default_factory=list, description="Processing notes")
    assigned_processor: Optional[str] = Field(None, description="Assigned processor ID")


class OnboardingDecision(BaseModel):
    """Final onboarding decision."""
    application_id: str = Field(..., description="Application identifier")
    decision: str = Field(..., description="Final decision (approved/rejected/manual_review)")
    decision_timestamp: datetime = Field(default_factory=datetime.now, description="Decision time")
    decision_factors: List[str] = Field(..., description="Key decision factors")
    conditions: List[str] = Field(default_factory=list, description="Approval conditions")
    account_numbers: Dict[str, str] = Field(default_factory=dict, description="Created account numbers")
    next_steps: List[str] = Field(default_factory=list, description="Next steps for customer")