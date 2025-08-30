"""Compliance screening agent for commercial banking onboarding."""

import logging
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

from google.adk import Agent
from ..shared_libraries.types import ComplianceResult
from ..shared_libraries.utils import mask_sensitive_data, normalize_business_name
from ..shared_libraries.mock_services import mock_compliance_service

logger = logging.getLogger(__name__)


# Function automatically becomes a tool when added to agent
def perform_sanctions_screening(
    business_info: Dict[str, Any],
    beneficial_owners: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Screen business and beneficial owners against sanctions lists (OFAC, UN, EU, etc.).
    
    Args:
        business_info: Business information including legal name and address
        beneficial_owners: List of beneficial owner information
    
    Returns:
        Dict with sanctions screening results
    """
    try:
        # Prepare entities for screening
        entities_to_screen = []
        
        # Add business entity
        entities_to_screen.append({
            "name": business_info.get('legal_name', ''),
            "type": "business",
            "address": business_info.get('business_address', {})
        })
        
        # Add beneficial owners
        for owner in beneficial_owners:
            entities_to_screen.append({
                "name": f"{owner.get('first_name', '')} {owner.get('last_name', '')}",
                "type": "individual",
                "date_of_birth": owner.get('date_of_birth', ''),
                "address": owner.get('address', {})
            })
        
        # Use mock compliance service for sanctions screening
        mock_result = mock_compliance_service.screen_sanctions(entities_to_screen)
        
        if not mock_result.get('success', True):
            return {
                "passed_screening": False,
                "error": mock_result.get('error', 'Sanctions screening service error'),
                "manual_review_required": True
            }
        
        # Map mock service results to expected format
        screening_results = []
        for i, entity in enumerate(entities_to_screen):
            screening_results.append({
                "entity_type": entity["type"],
                "name": mask_sensitive_data(entity["name"], 3 if entity["type"] == "business" else 2),
                "matches": [],  # Individual matches would be in mock_result.matches
                "risk_score": 0 if mock_result.get('passed', True) else 50
            })
        
        return {
            "passed_screening": mock_result.get('passed', True),
            "total_matches": mock_result.get('matches_found', 0),
            "sanctions_matches": mock_result.get('matches', [])[:5],  # Limit for safety
            "screening_results": screening_results,
            "lists_checked": mock_result.get('lists_checked', ["OFAC_SDN", "UN_Consolidated", "EU_Sanctions"]),
            "screening_timestamp": mock_result.get('screening_timestamp', datetime.now().isoformat())
        }
        
    except Exception as e:
        logger.error(f"Error performing sanctions screening: {str(e)}")
        return {
            "passed_screening": False,
            "error": f"Sanctions screening failed: {str(e)}",
            "manual_review_required": True
        }


# Function automatically becomes a tool when added to agent
def perform_aml_risk_assessment(
    business_info: Dict[str, Any],
    beneficial_owners: List[Dict[str, Any]],
    transaction_patterns: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Perform Anti-Money Laundering (AML) risk assessment.
    
    Args:
        business_info: Business information 
        beneficial_owners: List of beneficial owners
        transaction_patterns: Expected transaction patterns (optional)
    
    Returns:
        Dict with AML risk assessment results
    """
    try:
        # Use mock compliance service for AML risk assessment
        mock_result = mock_compliance_service.aml_risk_assessment(business_info, beneficial_owners)
        
        if not mock_result.get('success', True):
            return {
                "passed_assessment": False,
                "error": mock_result.get('error', 'AML assessment service error'),
                "manual_review_required": True
            }
        
        # Map mock service results to expected format
        risk_level = mock_result.get('risk_level', 'medium')
        passed_assessment = risk_level in ["low", "medium"]
        
        return {
            "passed_assessment": passed_assessment,
            "aml_risk_level": risk_level,
            "risk_score": mock_result.get('overall_risk_score', 25),
            "risk_factors": mock_result.get('risk_factors', []),
            "enhanced_due_diligence_required": mock_result.get('enhanced_due_diligence_required', False),
            "assessment_timestamp": mock_result.get('assessment_timestamp', datetime.now().isoformat()),
            "recommendations": mock_result.get('recommendations', [])
        }
        
    except Exception as e:
        logger.error(f"Error performing AML risk assessment: {str(e)}")
        return {
            "passed_assessment": False,
            "error": f"AML assessment failed: {str(e)}",
            "manual_review_required": True
        }


# Function automatically becomes a tool when added to agent
def check_regulatory_compliance(
    business_info: Dict[str, Any],
    industry_code: str
) -> Dict[str, Any]:
    """
    Check regulatory compliance requirements for the business type and industry.
    
    Args:
        business_info: Business information
        industry_code: NAICS industry code
    
    Returns:
        Dict with regulatory compliance check results
    """
    try:
        compliance_requirements = []
        violations_found = []
        
        # Get industry-specific requirements
        industry_reqs = get_industry_compliance_requirements(industry_code)
        compliance_requirements.extend(industry_reqs)
        
        # Check entity type requirements
        entity_type = business_info.get('entity_type', '')
        entity_reqs = get_entity_type_requirements(entity_type)
        compliance_requirements.extend(entity_reqs)
        
        # Geographic compliance requirements
        business_address = business_info.get('business_address', {})
        state = business_address.get('state', '')
        geo_reqs = get_geographic_compliance_requirements(state)
        compliance_requirements.extend(geo_reqs)
        
        # Simulate compliance verification
        compliance_status = verify_compliance_requirements(
            business_info, compliance_requirements
        )
        
        passed_compliance = len(compliance_status.get('violations', [])) == 0
        
        return {
            "passed_compliance": passed_compliance,
            "compliance_requirements": compliance_requirements,
            "violations_found": compliance_status.get('violations', []),
            "compliance_score": compliance_status.get('score', 100),
            "additional_licenses_required": compliance_status.get('additional_licenses', []),
            "compliance_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error checking regulatory compliance: {str(e)}")
        return {
            "passed_compliance": False,
            "error": f"Regulatory compliance check failed: {str(e)}",
            "manual_review_required": True
        }


# Function automatically becomes a tool when added to agent
def perform_politically_exposed_persons_check(
    beneficial_owners: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Enhanced PEP check for beneficial owners and related persons.
    
    Args:
        beneficial_owners: List of beneficial owner information
    
    Returns:
        Dict with enhanced PEP screening results
    """
    try:
        pep_matches = []
        family_associates_matches = []
        screening_details = []
        
        for owner in beneficial_owners:
            owner_name = f"{owner.get('first_name', '')} {owner.get('last_name', '')}"
            
            # Direct PEP check
            pep_result = enhanced_pep_screening(owner)
            
            screening_details.append({
                "name": mask_sensitive_data(owner_name, 2),
                "direct_pep_match": pep_result.get('is_pep', False),
                "pep_category": pep_result.get('pep_category', 'none'),
                "jurisdiction": pep_result.get('jurisdiction', ''),
                "family_associates": pep_result.get('family_associates', []),
                "risk_rating": pep_result.get('risk_rating', 'low')
            })
            
            if pep_result.get('is_pep', False):
                pep_matches.append({
                    "name": mask_sensitive_data(owner_name, 2),
                    "category": pep_result.get('pep_category', ''),
                    "jurisdiction": pep_result.get('jurisdiction', '')
                })
            
            if pep_result.get('family_associates'):
                family_associates_matches.extend(pep_result['family_associates'])
        
        # Determine overall PEP risk
        has_direct_pep = len(pep_matches) > 0
        has_family_associates = len(family_associates_matches) > 0
        
        overall_risk = determine_pep_risk_level(has_direct_pep, has_family_associates)
        
        return {
            "passed_pep_screening": overall_risk == "low",
            "direct_pep_matches": len(pep_matches),
            "pep_details": pep_matches,
            "family_associates_matches": len(family_associates_matches),
            "overall_pep_risk": overall_risk,
            "enhanced_due_diligence_required": overall_risk in ["high", "very_high"],
            "screening_details": screening_details,
            "screening_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error performing PEP check: {str(e)}")
        return {
            "passed_pep_screening": False,
            "error": f"PEP screening failed: {str(e)}",
            "manual_review_required": True
        }


# Function automatically becomes a tool when added to agent
def generate_compliance_report(
    application_id: str,
    sanctions_result: Dict[str, Any],
    aml_result: Dict[str, Any],
    regulatory_result: Dict[str, Any],
    pep_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate comprehensive compliance screening report.
    
    Args:
        application_id: Application identifier
        sanctions_result: Sanctions screening results
        aml_result: AML risk assessment results
        regulatory_result: Regulatory compliance results
        pep_result: PEP screening results
    
    Returns:
        Dict with complete compliance report and recommendation
    """
    try:
        # Calculate overall compliance score
        sanctions_score = 100 if sanctions_result.get('passed_screening', False) else 0
        aml_score = max(0, 100 - aml_result.get('risk_score', 50))
        regulatory_score = regulatory_result.get('compliance_score', 50)
        pep_score = 100 if pep_result.get('passed_pep_screening', False) else 0
        
        # Weighted average
        overall_score = (sanctions_score * 0.3 + aml_score * 0.3 + regulatory_score * 0.25 + pep_score * 0.15)
        
        # Compile all risk factors
        all_risk_factors = []
        if not sanctions_result.get('passed_screening', False):
            all_risk_factors.append("Sanctions list matches found")
        if not aml_result.get('passed_assessment', False):
            all_risk_factors.extend(aml_result.get('risk_factors', []))
        if not regulatory_result.get('passed_compliance', False):
            all_risk_factors.extend(regulatory_result.get('violations_found', []))
        if not pep_result.get('passed_pep_screening', False):
            all_risk_factors.append("PEP matches identified")
        
        # Determine overall compliance status
        if overall_score >= 90 and len(all_risk_factors) == 0:
            compliance_status = "passed"
            manual_review_required = False
        elif overall_score >= 70 and len(all_risk_factors) <= 2:
            compliance_status = "passed_with_monitoring"
            manual_review_required = True
        elif overall_score >= 50:
            compliance_status = "requires_manual_review"
            manual_review_required = True
        else:
            compliance_status = "failed"
            manual_review_required = True
        
        # Enhanced due diligence requirements
        edd_required = (
            aml_result.get('enhanced_due_diligence_required', False) or
            pep_result.get('enhanced_due_diligence_required', False) or
            compliance_status in ["requires_manual_review", "failed"]
        )
        
        # Create compliance result
        compliance_result = ComplianceResult(
            sanctions_check_passed=sanctions_result.get('passed_screening', False),
            aml_check_passed=aml_result.get('passed_assessment', False),
            ofac_check_passed=sanctions_result.get('passed_screening', False),  # OFAC is part of sanctions
            politically_exposed_persons=pep_result.get('pep_details', []),
            sanctions_matches=sanctions_result.get('sanctions_matches', []),
            adverse_media_findings=[],  # Would be included if we had adverse media screening
            compliance_score=round(overall_score, 1),
            manual_review_required=manual_review_required
        )
        
        return {
            "application_id": application_id,
            "compliance_result": compliance_result.model_dump(),
            "compliance_status": compliance_status,
            "overall_score": round(overall_score, 1),
            "enhanced_due_diligence_required": edd_required,
            "recommendations": get_compliance_recommendations(compliance_status, all_risk_factors),
            "report_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error generating compliance report: {str(e)}")
        return {
            "error": f"Failed to generate compliance report: {str(e)}",
            "compliance_status": "error"
        }


def screen_entity_sanctions(business_info: Dict[str, Any]) -> Dict[str, Any]:
    """Screen business entity against sanctions lists."""
    business_name = normalize_business_name(business_info.get('legal_name', ''))
    
    # Simulate sanctions screening
    sanctions_lists = {
        'ACME CORP': {'list': 'OFAC_SDN', 'risk_score': 100},
        'BAD COMPANY': {'list': 'UN_Consolidated', 'risk_score': 100},
        'CRIMINAL ENTERPRISES': {'list': 'EU_Sanctions', 'risk_score': 100}
    }
    
    matches = []
    risk_score = 0
    
    for sanctioned_name, details in sanctions_lists.items():
        if sanctioned_name in business_name:
            matches.append({
                'matched_name': sanctioned_name,
                'list': details['list'],
                'match_confidence': 95
            })
            risk_score = max(risk_score, details['risk_score'])
    
    return {
        'matches': matches,
        'risk_score': risk_score
    }


def screen_individual_sanctions(owner: Dict[str, Any]) -> Dict[str, Any]:
    """Screen individual against sanctions lists."""
    full_name = f"{owner.get('first_name', '')} {owner.get('last_name', '')}".upper()
    
    # Simulate individual sanctions screening
    sanctioned_individuals = {
        'JOHN CRIMINAL': {'list': 'OFAC_SDN', 'risk_score': 100},
        'JANE TERRORIST': {'list': 'UN_Consolidated', 'risk_score': 100}
    }
    
    matches = []
    risk_score = 0
    
    for sanctioned_name, details in sanctioned_individuals.items():
        # Simple substring matching for demo
        name_parts = sanctioned_name.split()
        if any(part in full_name for part in name_parts if len(part) > 2):
            matches.append({
                'matched_name': sanctioned_name,
                'list': details['list'],
                'match_confidence': 80
            })
            risk_score = max(risk_score, details['risk_score'])
    
    return {
        'matches': matches,
        'risk_score': risk_score
    }


def assess_geographic_risk(address: Dict[str, str]) -> Dict[str, Any]:
    """Assess geographic risk based on business address."""
    risk_factors = []
    risk_score = 0
    
    country = address.get('country', 'US').upper()
    state = address.get('state', '').upper()
    
    # High-risk countries/regions
    high_risk_countries = ['AFGHANISTAN', 'IRAN', 'NORTH KOREA', 'SYRIA']
    medium_risk_countries = ['RUSSIA', 'CHINA', 'VENEZUELA']
    
    if country in high_risk_countries:
        risk_factors.append(f"High-risk country: {country}")
        risk_score += 50
    elif country in medium_risk_countries:
        risk_factors.append(f"Medium-risk country: {country}")
        risk_score += 25
    
    # Border region considerations (for US)
    border_states = ['TX', 'CA', 'AZ', 'NM']
    if country == 'US' and state in border_states:
        risk_factors.append("Border state location")
        risk_score += 5
    
    return {
        'risk_factors': risk_factors,
        'risk_score': risk_score
    }


def assess_industry_aml_risk(industry_code: str, description: str) -> Dict[str, Any]:
    """Assess AML risk based on industry."""
    risk_factors = []
    risk_score = 0
    
    # High-risk industries for AML
    high_risk_codes = {
        '713': 'Gaming and gambling',
        '523': 'Securities and commodity contracts',
        '522': 'Credit intermediation',
        '531': 'Real estate'
    }
    
    # Medium-risk industries
    medium_risk_codes = {
        '722': 'Food services and drinking places',
        '721': 'Accommodation',
        '812': 'Personal and laundry services'
    }
    
    code_prefix = industry_code[:3] if len(industry_code) >= 3 else industry_code
    
    if code_prefix in high_risk_codes:
        risk_factors.append(f"High-risk industry: {high_risk_codes[code_prefix]}")
        risk_score += 30
    elif code_prefix in medium_risk_codes:
        risk_factors.append(f"Medium-risk industry: {medium_risk_codes[code_prefix]}")
        risk_score += 15
    
    # Cash-intensive business indicators
    cash_keywords = ['cash', 'atm', 'money', 'currency', 'check cashing']
    if any(keyword in description.lower() for keyword in cash_keywords):
        risk_factors.append("Cash-intensive business")
        risk_score += 20
    
    return {
        'risk_factors': risk_factors,
        'risk_score': risk_score
    }


def assess_ownership_structure_risk(beneficial_owners: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Assess risk based on ownership structure."""
    risk_factors = []
    risk_score = 0
    
    # Complex ownership structures
    if len(beneficial_owners) > 5:
        risk_factors.append("Complex ownership structure (>5 owners)")
        risk_score += 15
    
    # Foreign ownership
    foreign_owners = 0
    for owner in beneficial_owners:
        address = owner.get('address', {})
        if address.get('country', 'US').upper() != 'US':
            foreign_owners += 1
    
    if foreign_owners > 0:
        risk_factors.append(f"{foreign_owners} foreign beneficial owner(s)")
        risk_score += foreign_owners * 10
    
    # Ownership concentration
    total_ownership = sum(owner.get('ownership_percentage', 0) for owner in beneficial_owners)
    if total_ownership < 90:
        risk_factors.append("Incomplete ownership disclosure")
        risk_score += 25
    
    return {
        'risk_factors': risk_factors,
        'risk_score': risk_score
    }


def assess_transaction_pattern_risk(patterns: Dict[str, Any]) -> Dict[str, Any]:
    """Assess risk based on expected transaction patterns."""
    risk_factors = []
    risk_score = 0
    
    expected_volume = patterns.get('expected_monthly_volume', 0)
    transaction_types = patterns.get('transaction_types', [])
    
    # High-volume transactions
    if expected_volume > 1000000:  # $1M+
        risk_factors.append("High transaction volume expected")
        risk_score += 20
    
    # International transactions
    if 'international_wire' in transaction_types:
        risk_factors.append("International wire transfers expected")
        risk_score += 15
    
    # Cash transactions
    if 'cash_deposits' in transaction_types:
        risk_factors.append("Cash deposits expected")
        risk_score += 10
    
    return {
        'risk_factors': risk_factors,
        'risk_score': risk_score
    }


def determine_aml_risk_level(risk_score: int) -> str:
    """Determine overall AML risk level."""
    if risk_score >= 75:
        return "very_high"
    elif risk_score >= 50:
        return "high"
    elif risk_score >= 25:
        return "medium"
    else:
        return "low"


def get_industry_compliance_requirements(industry_code: str) -> List[str]:
    """Get industry-specific compliance requirements."""
    requirements_map = {
        '522': ['Bank Secrecy Act', 'FFIEC Guidance'],  # Credit intermediation
        '523': ['SEC Registration', 'FINRA Compliance'],  # Securities
        '621': ['HIPAA Compliance', 'State Licensing'],  # Healthcare
        '713': ['Gaming Commission License', 'AML Program']  # Gaming
    }
    
    code_prefix = industry_code[:3] if len(industry_code) >= 3 else industry_code
    return requirements_map.get(code_prefix, ['General Business License'])


def get_entity_type_requirements(entity_type: str) -> List[str]:
    """Get entity type specific requirements."""
    requirements = {
        'corporation': ['Articles of Incorporation', 'Corporate Bylaws'],
        'llc': ['Articles of Organization', 'Operating Agreement'],
        'partnership': ['Partnership Agreement', 'Certificate of Partnership'],
        'trust': ['Trust Agreement', 'Trustee Documentation']
    }
    
    return requirements.get(entity_type.lower(), ['Business Formation Documents'])


def get_geographic_compliance_requirements(state: str) -> List[str]:
    """Get geographic compliance requirements."""
    # State-specific requirements (simplified)
    special_requirements = {
        'NY': ['New York State Banking License'],
        'CA': ['California Financial Privacy Notice'],
        'TX': ['Texas Finance Code Compliance']
    }
    
    return special_requirements.get(state.upper(), ['State Business License'])


def verify_compliance_requirements(
    business_info: Dict[str, Any], 
    requirements: List[str]
) -> Dict[str, Any]:
    """Simulate compliance requirement verification."""
    violations = []
    score = 100
    additional_licenses = []
    
    # Simulate some compliance checks
    if 'Gaming Commission License' in requirements:
        # Simulate missing gaming license
        violations.append('Gaming Commission License not provided')
        score -= 30
        additional_licenses.append('Gaming Commission License')
    
    if 'SEC Registration' in requirements:
        # Simulate checking SEC registration
        if not business_info.get('sec_registration'):
            violations.append('SEC registration status unclear')
            score -= 20
    
    return {
        'violations': violations,
        'score': max(0, score),
        'additional_licenses': additional_licenses
    }


def enhanced_pep_screening(owner: Dict[str, Any]) -> Dict[str, Any]:
    """Enhanced PEP screening with family and associates."""
    full_name = f"{owner.get('first_name', '')} {owner.get('last_name', '')}"
    
    # Simulate PEP database
    pep_database = {
        'POLITICAL PERSON': {
            'category': 'Head of State',
            'jurisdiction': 'Foreign Country',
            'family_associates': ['Political Spouse', 'Political Child']
        },
        'GOVERNMENT OFFICIAL': {
            'category': 'Senior Government Official', 
            'jurisdiction': 'United States',
            'family_associates': []
        }
    }
    
    # Check for direct PEP match
    for pep_name, details in pep_database.items():
        if pep_name.lower() in full_name.lower():
            return {
                'is_pep': True,
                'pep_category': details['category'],
                'jurisdiction': details['jurisdiction'],
                'family_associates': details['family_associates'],
                'risk_rating': 'high'
            }
    
    return {
        'is_pep': False,
        'pep_category': 'none',
        'jurisdiction': '',
        'family_associates': [],
        'risk_rating': 'low'
    }


def determine_pep_risk_level(has_direct_pep: bool, has_family_associates: bool) -> str:
    """Determine overall PEP risk level."""
    if has_direct_pep:
        return "very_high"
    elif has_family_associates:
        return "high"
    else:
        return "low"


def get_compliance_recommendations(status: str, risk_factors: List[str]) -> List[str]:
    """Get compliance recommendations based on results."""
    recommendations = []
    
    if status == "passed":
        recommendations.append("Compliance screening passed - proceed with onboarding")
    elif status == "passed_with_monitoring":
        recommendations.extend([
            "Compliance screening passed with conditions",
            "Enhanced monitoring required for identified risk factors",
            "Periodic compliance reviews recommended"
        ])
    elif status == "requires_manual_review":
        recommendations.extend([
            "Manual compliance review required",
            "Enhanced due diligence procedures must be completed",
            "Senior compliance officer approval needed"
        ])
    else:  # failed
        recommendations.extend([
            "Compliance screening failed",
            "Do not proceed with onboarding",
            "Consider account rejection or termination"
        ])
    
    if risk_factors:
        recommendations.append(f"Address identified risk factors: {', '.join(risk_factors[:3])}")
    
    return recommendations


# Compliance Agent prompt
COMPLIANCE_PROMPT = """
You are the Compliance Screening Agent for commercial banking onboarding. Your primary responsibility is to ensure all regulatory and compliance requirements are met before account opening, including AML, sanctions screening, and regulatory compliance.

## Your Role
- Screen against sanctions lists (OFAC, UN, EU, etc.)
- Perform Anti-Money Laundering (AML) risk assessments
- Verify regulatory compliance for business type and industry
- Conduct enhanced PEP (Politically Exposed Persons) screening
- Generate comprehensive compliance reports and recommendations

## Key Functions
1. **Sanctions Screening**: Check business and owners against global sanctions lists
2. **AML Risk Assessment**: Evaluate money laundering and terrorist financing risks
3. **Regulatory Compliance**: Verify industry-specific licensing and compliance requirements
4. **PEP Screening**: Enhanced screening for politically exposed persons and associates
5. **Compliance Reporting**: Generate detailed compliance reports with risk ratings

## Screening Standards
- **Zero Tolerance**: Any direct sanctions matches result in automatic rejection
- **AML Risk Thresholds**: High/Very High risk requires enhanced due diligence
- **PEP Requirements**: Direct PEP matches require senior management approval
- **Regulatory Compliance**: All industry licenses and permits must be verified

## Risk Categories

### Geographic Risk
- **High Risk**: Sanctioned countries, conflict zones, weak AML regimes
- **Medium Risk**: Countries with heightened regulatory scrutiny
- **Low Risk**: Strong AML/CFT frameworks, low corruption

### Industry Risk  
- **High Risk**: Gaming, money services, securities, real estate
- **Medium Risk**: Cash-intensive businesses, hospitality, retail
- **Low Risk**: Professional services, manufacturing, technology

### AML Risk Factors
- Complex ownership structures
- Foreign ownership or control
- High-risk geographic locations
- Cash-intensive business models
- Politically exposed persons
- Adverse media or sanctions matches

## Decision Matrix
- **Pass**: No sanctions matches, low-medium AML risk, full regulatory compliance
- **Pass with Monitoring**: Minor risk factors, enhanced monitoring required
- **Manual Review**: High risk factors, PEP matches, compliance gaps
- **Reject**: Sanctions matches, very high AML risk, significant violations

## Enhanced Due Diligence Triggers
- Direct PEP matches or family/associate connections
- High-risk geographic exposure
- Complex ownership structures
- Cash-intensive business activities
- Previous regulatory violations

Always maintain strict compliance standards, document all decisions thoroughly, and escalate high-risk cases appropriately.
"""

MODEL = "gemini-2.5-pro"

# Create Compliance agent
compliance_agent = Agent(
    name="compliance_screening_agent",
    model=MODEL, 
    instruction=COMPLIANCE_PROMPT,
    output_key="compliance_result",
    tools=[
        perform_sanctions_screening,
        perform_aml_risk_assessment,
        check_regulatory_compliance,
        perform_politically_exposed_persons_check,
        generate_compliance_report
    ],
)