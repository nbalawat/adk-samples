"""KYC (Know Your Customer) verification agent for commercial banking onboarding."""

import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, date

from google.adk import Agent
from ..shared_libraries.types import KYCResult, BusinessInfo, BeneficialOwner
from ..shared_libraries.utils import validate_tax_id, validate_email, mask_sensitive_data
from ..shared_libraries.mock_services import mock_kyc_service

logger = logging.getLogger(__name__)


# Function automatically becomes a tool when added to agent
def verify_business_identity(business_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verify business identity using external KYC provider.
    
    Args:
        business_info: Business information to verify
    
    Returns:
        Dict with verification results and confidence score
    """
    try:
        # Validate required fields
        required_fields = ['legal_name', 'tax_id', 'business_address']
        missing_fields = [field for field in required_fields if not business_info.get(field)]
        
        if missing_fields:
            return {
                "verified": False,
                "error": f"Missing required fields: {missing_fields}",
                "confidence_score": 0
            }
        
        # Validate tax ID format
        if not validate_tax_id(business_info.get('tax_id', '')):
            return {
                "verified": False,
                "error": "Invalid tax ID format",
                "confidence_score": 0
            }
        
        # Use mock KYC service
        mock_result = mock_kyc_service.verify_business_identity(
            business_name=business_info.get('legal_name'),
            tax_id=business_info.get('tax_id'),
            address=business_info.get('business_address')
        )
        
        if not mock_result.get('success', True):
            return {
                "verified": False,
                "error": mock_result.get('error', 'KYC service error'),
                "confidence_score": 0
            }
        
        # Map mock service result to expected format
        result = {
            "verified": mock_result.get('verified', False),
            "confidence_score": mock_result.get('confidence_score', 0),
            "verification_data": {
                "business_name": business_info.get('legal_name'),
                "tax_id": mask_sensitive_data(business_info.get('tax_id')),
                "address": business_info.get('business_address'),
                "entity_type": business_info.get('entity_type')
            },
            "verified_fields": mock_result.get('verified_fields', []),
            "risk_factors": get_business_risk_factors(business_info),
            "verification_timestamp": mock_result.get('verification_timestamp', datetime.now().isoformat())
        }
        
        logger.info(f"Business verification completed for {business_info.get('legal_name')}: {result['verified']}")
        return result
        
    except Exception as e:
        logger.error(f"Error verifying business identity: {str(e)}")
        return {
            "verified": False,
            "error": f"Verification failed: {str(e)}",
            "confidence_score": 0
        }


# Function automatically becomes a tool when added to agent
def verify_beneficial_owners(owners: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Verify beneficial owners' identities and perform background checks.
    
    Args:
        owners: List of beneficial owner information
    
    Returns:
        Dict with verification results for all owners
    """
    try:
        verification_results = []
        all_verified = True
        total_ownership = 0
        
        for owner in owners:
            # Validate ownership percentage
            ownership_pct = owner.get('ownership_percentage', 0)
            total_ownership += ownership_pct
            
            # Use mock KYC service for individual verification
            mock_result = mock_kyc_service.verify_individual(
                first_name=owner.get('first_name', ''),
                last_name=owner.get('last_name', ''),
                ssn=owner.get('ssn', ''),
                date_of_birth=owner.get('date_of_birth', ''),
                address=owner.get('address', {})
            )
            
            owner_result = {
                "name": mask_sensitive_data(f"{owner.get('first_name')} {owner.get('last_name')}", 2),
                "verified": mock_result.get('verified', False),
                "confidence_score": mock_result.get('confidence_score', 0),
                "verified_fields": ['name', 'ssn', 'address', 'date_of_birth'] if mock_result.get('verified') else [],
                "flags": mock_result.get('flags', [])
            }
            
            verification_results.append(owner_result)
            
            if not owner_result.get('verified', False):
                all_verified = False
        
        # Check total ownership
        ownership_valid = 95 <= total_ownership <= 105  # Allow small rounding differences
        
        return {
            "all_verified": all_verified and ownership_valid,
            "ownership_percentage_valid": ownership_valid,
            "total_ownership_percentage": total_ownership,
            "individual_results": verification_results,
            "verification_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error verifying beneficial owners: {str(e)}")
        return {
            "all_verified": False,
            "error": f"Owner verification failed: {str(e)}"
        }


# Function automatically becomes a tool when added to agent
def perform_pep_screening(owners: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Screen beneficial owners against Politically Exposed Persons (PEP) lists.
    
    Args:
        owners: List of beneficial owner information
    
    Returns:
        Dict with PEP screening results
    """
    try:
        pep_matches = []
        screening_results = []
        
        for owner in owners:
            full_name = f"{owner.get('first_name', '')} {owner.get('last_name', '')}"
            
            # Use mock KYC service for PEP screening
            pep_result = mock_kyc_service.screen_pep(full_name, owner.get('date_of_birth', ''))
            
            screening_results.append({
                "name": mask_sensitive_data(full_name, 2),
                "pep_match": pep_result.get('is_pep', False),
                "risk_level": pep_result.get('risk_level', 'low'),
                "match_details": pep_result.get('matches', [])
            })
            
            if pep_result.get('is_pep', False):
                pep_matches.append(full_name)
        
        passed_screening = len(pep_matches) == 0
        
        return {
            "passed_screening": passed_screening,
            "pep_matches_found": len(pep_matches),
            "pep_matches": [mask_sensitive_data(name, 2) for name in pep_matches],
            "individual_results": screening_results,
            "screening_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error performing PEP screening: {str(e)}")
        return {
            "passed_screening": False,
            "error": f"PEP screening failed: {str(e)}"
        }


# Function automatically becomes a tool when added to agent
def perform_adverse_media_screening(business_name: str, owners: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Screen business and owners against adverse media sources.
    
    Args:
        business_name: Legal business name
        owners: List of beneficial owner information
    
    Returns:
        Dict with adverse media screening results
    """
    try:
        adverse_findings = []
        
        # Screen business name
        business_findings = simulate_adverse_media_check(business_name, "business")
        if business_findings:
            adverse_findings.extend(business_findings)
        
        # Screen beneficial owners
        for owner in owners:
            full_name = f"{owner.get('first_name', '')} {owner.get('last_name', '')}"
            owner_findings = simulate_adverse_media_check(full_name, "individual")
            if owner_findings:
                adverse_findings.extend(owner_findings)
        
        passed_screening = len(adverse_findings) == 0
        
        return {
            "passed_screening": passed_screening,
            "findings_count": len(adverse_findings),
            "adverse_findings": adverse_findings[:5],  # Limit to top 5 findings
            "screening_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error performing adverse media screening: {str(e)}")
        return {
            "passed_screening": False,
            "error": f"Adverse media screening failed: {str(e)}"
        }


# Function automatically becomes a tool when added to agent
def generate_kyc_report(
    application_id: str,
    business_verification: Dict[str, Any],
    owner_verification: Dict[str, Any], 
    pep_screening: Dict[str, Any],
    adverse_media: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate comprehensive KYC verification report.
    
    Args:
        application_id: Application identifier
        business_verification: Business identity verification results
        owner_verification: Beneficial owner verification results
        pep_screening: PEP screening results
        adverse_media: Adverse media screening results
    
    Returns:
        Dict with complete KYC report and recommendation
    """
    try:
        # Calculate overall KYC score
        business_score = business_verification.get('confidence_score', 0)
        owner_score = 100 if owner_verification.get('all_verified', False) else 0
        pep_score = 100 if pep_screening.get('passed_screening', False) else 0
        media_score = 100 if adverse_media.get('passed_screening', False) else 0
        
        # Weighted average
        overall_score = (business_score * 0.4 + owner_score * 0.3 + pep_score * 0.2 + media_score * 0.1)
        
        # Determine verification status
        if overall_score >= 80:
            verification_status = "passed"
            manual_review_required = False
        elif overall_score >= 60:
            verification_status = "passed_with_conditions"
            manual_review_required = True
        else:
            verification_status = "failed"
            manual_review_required = True
        
        # Compile risk factors
        risk_factors = []
        if not business_verification.get('verified', False):
            risk_factors.append("Business identity not verified")
        if not owner_verification.get('all_verified', False):
            risk_factors.append("Beneficial owner verification incomplete")
        if not pep_screening.get('passed_screening', False):
            risk_factors.append("PEP matches found")
        if not adverse_media.get('passed_screening', False):
            risk_factors.append("Adverse media findings")
        
        # Create KYC result
        kyc_result = KYCResult(
            business_verified=business_verification.get('verified', False),
            owners_verified=owner_verification.get('all_verified', False),
            pep_check_passed=pep_screening.get('passed_screening', False),
            adverse_media_check_passed=adverse_media.get('passed_screening', False),
            verification_score=round(overall_score, 1),
            risk_factors=risk_factors,
            manual_review_required=manual_review_required
        )
        
        return {
            "application_id": application_id,
            "kyc_result": kyc_result.model_dump(),
            "verification_status": verification_status,
            "overall_score": round(overall_score, 1),
            "report_timestamp": datetime.now().isoformat(),
            "recommendations": get_kyc_recommendations(verification_status, risk_factors)
        }
        
    except Exception as e:
        logger.error(f"Error generating KYC report: {str(e)}")
        return {
            "error": f"Failed to generate KYC report: {str(e)}",
            "verification_status": "error"
        }


def verify_individual_owner(owner: Dict[str, Any]) -> Dict[str, Any]:
    """Verify individual beneficial owner."""
    # Simulate individual verification
    required_fields = ['first_name', 'last_name', 'ssn', 'date_of_birth', 'address']
    missing_fields = [field for field in required_fields if not owner.get(field)]
    
    if missing_fields:
        return {
            "verified": False,
            "error": f"Missing fields: {missing_fields}",
            "confidence_score": 0
        }
    
    # Simulate verification score
    confidence_score = 85  # Simulated high confidence
    
    return {
        "verified": True,
        "confidence_score": confidence_score,
        "name": mask_sensitive_data(f"{owner.get('first_name')} {owner.get('last_name')}", 2),
        "verified_fields": ['name', 'ssn', 'address', 'date_of_birth']
    }


def calculate_business_verification_score(business_info: Dict[str, Any]) -> float:
    """Calculate business verification confidence score."""
    score = 0
    
    # Legal name verification (30 points)
    if business_info.get('legal_name'):
        score += 30
    
    # Tax ID verification (25 points)
    if validate_tax_id(business_info.get('tax_id', '')):
        score += 25
    
    # Address verification (20 points)
    if business_info.get('business_address'):
        score += 20
    
    # Entity type verification (15 points)
    if business_info.get('entity_type'):
        score += 15
    
    # Additional info (10 points)
    if business_info.get('industry_code') and validate_email(business_info.get('email', '')):
        score += 10
    
    return min(score, 100)  # Cap at 100


def get_verified_fields(business_info: Dict[str, Any]) -> List[str]:
    """Get list of verified business fields."""
    verified = []
    
    if business_info.get('legal_name'):
        verified.append('legal_name')
    if validate_tax_id(business_info.get('tax_id', '')):
        verified.append('tax_id')
    if business_info.get('business_address'):
        verified.append('business_address')
    if business_info.get('entity_type'):
        verified.append('entity_type')
    
    return verified


def get_business_risk_factors(business_info: Dict[str, Any]) -> List[str]:
    """Identify business risk factors."""
    risk_factors = []
    
    # Recent incorporation
    incorporation_date = business_info.get('incorporation_date')
    if incorporation_date:
        if isinstance(incorporation_date, str):
            incorporation_date = datetime.fromisoformat(incorporation_date)
        
        business_age = (datetime.now() - incorporation_date).days / 365
        if business_age < 1:
            risk_factors.append("Business less than 1 year old")
    
    # High-risk industries
    industry_code = business_info.get('industry_code', '')
    high_risk_codes = ['713', '722', '531']  # Entertainment, Food Service, Real Estate
    if industry_code[:3] in high_risk_codes:
        risk_factors.append("High-risk industry")
    
    return risk_factors


def simulate_pep_check(name: str, date_of_birth: Any) -> Dict[str, Any]:
    """Simulate PEP screening check."""
    # For demo purposes, flag certain names as PEP
    pep_names = ['John Smith', 'Political Person', 'Government Official']
    
    is_pep = any(pep_name.lower() in name.lower() for pep_name in pep_names)
    
    return {
        "is_pep": is_pep,
        "risk_level": "high" if is_pep else "low",
        "match_details": [f"Potential match with {name}"] if is_pep else []
    }


def simulate_adverse_media_check(name: str, entity_type: str) -> List[str]:
    """Simulate adverse media screening."""
    # For demo purposes, flag certain names
    adverse_names = ['Bad Company', 'Fraudulent Corp', 'Criminal Person']
    
    findings = []
    for adverse_name in adverse_names:
        if adverse_name.lower() in name.lower():
            findings.append(f"Adverse media mention: {adverse_name} in financial news")
    
    return findings


def get_kyc_recommendations(status: str, risk_factors: List[str]) -> List[str]:
    """Get KYC recommendations based on verification results."""
    if status == "passed":
        return ["KYC verification complete", "Proceed with onboarding"]
    elif status == "passed_with_conditions":
        recommendations = ["KYC verification passed with conditions", "Enhanced monitoring recommended"]
        if risk_factors:
            recommendations.append(f"Monitor for: {', '.join(risk_factors)}")
        return recommendations
    else:
        return ["KYC verification failed", "Do not proceed with onboarding", "Manual review required"]


# KYC Agent prompt
KYC_PROMPT = """
You are the KYC (Know Your Customer) Verification Agent for commercial banking onboarding. Your primary responsibility is to verify the identity of businesses and their beneficial owners while ensuring compliance with regulatory requirements.

## Your Role
- Verify business identity using authoritative sources
- Validate beneficial owner information and ownership percentages
- Perform PEP (Politically Exposed Persons) screening
- Conduct adverse media screening
- Generate comprehensive KYC verification reports
- Identify risk factors that may require enhanced due diligence

## Key Functions
1. **Business Identity Verification**: Confirm legal name, tax ID, address, and entity type
2. **Beneficial Owner Verification**: Validate identity of individuals with 25%+ ownership or control
3. **PEP Screening**: Screen against politically exposed persons lists
4. **Adverse Media Screening**: Check for negative news or legal issues
5. **Risk Assessment**: Evaluate overall KYC risk profile

## Verification Standards
- Business verification score must be ≥70% to pass
- All beneficial owners must be verified
- Total ownership percentages must equal 100% (±5%)
- No PEP matches for standard approval
- No significant adverse media findings

## Decision Thresholds
- **Pass**: Overall score ≥80%, no major risk factors
- **Pass with Conditions**: Score 60-79%, minor risk factors, requires enhanced monitoring
- **Fail**: Score <60%, significant risk factors, reject application

Always maintain confidentiality, follow KYC regulations, and escalate complex cases for manual review.
"""

MODEL = "gemini-2.5-pro"

# Create KYC agent
kyc_agent = Agent(
    name="kyc_verification_agent",
    model=MODEL,
    instruction=KYC_PROMPT,
    output_key="kyc_result",
    tools=[
        verify_business_identity,
        verify_beneficial_owners,
        perform_pep_screening,
        perform_adverse_media_screening,
        generate_kyc_report
    ],
)