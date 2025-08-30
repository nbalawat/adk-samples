"""Document processing agent for commercial banking onboarding."""

import logging
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import base64

from google.adk import Agent
from ..shared_libraries.types import DocumentType, DocumentInfo
from ..shared_libraries.utils import sanitize_filename, create_audit_entry
from ..shared_libraries.mock_services import mock_document_service

logger = logging.getLogger(__name__)


# Function automatically becomes a tool when added to agent
def extract_document_data(
    document_id: str,
    document_type: str,
    file_content: Optional[str] = None
) -> Dict[str, Any]:
    """
    Extract structured data from business documents using AI.
    
    Args:
        document_id: Unique document identifier
        document_type: Type of document to process
        file_content: Base64 encoded file content (optional for demo)
    
    Returns:
        Dict with extracted document data
    """
    try:
        # Validate document type
        valid_types = [dt.value for dt in DocumentType]
        if document_type not in valid_types:
            return {
                "success": False,
                "error": f"Invalid document type: {document_type}. Valid types: {valid_types}"
            }
        
        # Use mock document service for processing
        mock_result = mock_document_service.process_document(
            document_id=document_id,
            document_type=document_type,
            file_content=file_content
        )
        
        if not mock_result.get('success', True):
            return {
                "document_id": document_id,
                "success": False,
                "error": mock_result.get('error', 'Document processing service error')
            }
        
        extracted_data = mock_result.get('extracted_data', {})
        
        # Validate extracted data
        validation_result = validate_extracted_data(document_type, extracted_data)
        
        return {
            "document_id": document_id,
            "document_type": document_type,
            "extracted_data": extracted_data,
            "validation": validation_result,
            "extraction_confidence": validation_result.get('confidence_score', 85),
            "extraction_timestamp": datetime.now().isoformat(),
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Error extracting document data: {str(e)}")
        return {
            "document_id": document_id,
            "success": False,
            "error": f"Document extraction failed: {str(e)}"
        }


# Function automatically becomes a tool when added to agent
def validate_business_documents(
    documents: List[Dict[str, Any]],
    business_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Validate business documents against provided business information.
    
    Args:
        documents: List of processed documents with extracted data
        business_info: Business information to validate against
    
    Returns:
        Dict with validation results for all documents
    """
    try:
        validation_results = []
        all_valid = True
        missing_documents = []
        
        # Required documents based on entity type
        required_docs = get_required_documents(business_info.get('entity_type', ''))
        
        # Check for required documents
        provided_types = [doc.get('document_type') for doc in documents]
        for required_doc in required_docs:
            if required_doc not in provided_types:
                missing_documents.append(required_doc)
                all_valid = False
        
        # Validate each provided document
        for document in documents:
            doc_validation = validate_individual_document(document, business_info)
            validation_results.append(doc_validation)
            
            if not doc_validation.get('valid', False):
                all_valid = False
        
        return {
            "all_documents_valid": all_valid,
            "missing_documents": missing_documents,
            "validation_results": validation_results,
            "overall_confidence": calculate_overall_confidence(validation_results),
            "validation_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error validating business documents: {str(e)}")
        return {
            "all_documents_valid": False,
            "error": f"Document validation failed: {str(e)}"
        }


# Function automatically becomes a tool when added to agent
def verify_document_authenticity(
    document_id: str,
    document_type: str,
    extracted_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Verify document authenticity and detect potential fraud.
    
    Args:
        document_id: Document identifier
        document_type: Type of document
        extracted_data: Previously extracted document data
    
    Returns:
        Dict with authenticity verification results
    """
    try:
        # Use mock document service for authenticity verification
        mock_result = mock_document_service.verify_authenticity(
            document_id=document_id,
            document_type=document_type,
            extracted_data=extracted_data
        )
        
        if not mock_result.get('success', True):
            return {
                "document_id": document_id,
                "is_authentic": False,
                "error": mock_result.get('error', 'Authenticity verification service error'),
                "manual_review_required": True
            }
        
        is_authentic = mock_result.get('is_authentic', False)
        authenticity_score = mock_result.get('authenticity_score', 0)
        authenticity_checks = mock_result.get('checks_performed', [])
        risk_factors = mock_result.get('risk_factors', [])
        
        return {
            "document_id": document_id,
            "is_authentic": is_authentic,
            "authenticity_score": round(authenticity_score, 1),
            "authenticity_checks": authenticity_checks,
            "risk_factors": risk_factors,
            "manual_review_required": authenticity_score < 70 or len(risk_factors) > 2,
            "verification_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error verifying document authenticity: {str(e)}")
        return {
            "document_id": document_id,
            "is_authentic": False,
            "error": f"Authenticity verification failed: {str(e)}",
            "manual_review_required": True
        }


# Function automatically becomes a tool when added to agent
def cross_validate_extracted_data(
    all_documents: List[Dict[str, Any]],
    business_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Cross-validate extracted data across multiple documents for consistency.
    
    Args:
        all_documents: List of all processed documents with extracted data
        business_info: Business information for validation
    
    Returns:
        Dict with cross-validation results
    """
    try:
        inconsistencies = []
        validation_score = 100
        
        # Extract key fields from all documents
        extracted_fields = extract_key_fields_from_documents(all_documents)
        
        # Validate business name consistency
        name_validation = validate_business_name_consistency(extracted_fields, business_info)
        if not name_validation['consistent']:
            inconsistencies.extend(name_validation['inconsistencies'])
            validation_score -= 20
        
        # Validate tax ID consistency
        tax_id_validation = validate_tax_id_consistency(extracted_fields, business_info)
        if not tax_id_validation['consistent']:
            inconsistencies.extend(tax_id_validation['inconsistencies'])
            validation_score -= 25
        
        # Validate address consistency
        address_validation = validate_address_consistency(extracted_fields, business_info)
        if not address_validation['consistent']:
            inconsistencies.extend(address_validation['inconsistencies'])
            validation_score -= 15
        
        # Validate incorporation date consistency
        date_validation = validate_incorporation_date_consistency(extracted_fields, business_info)
        if not date_validation['consistent']:
            inconsistencies.extend(date_validation['inconsistencies'])
            validation_score -= 15
        
        # Validate beneficial ownership consistency
        ownership_validation = validate_ownership_consistency(all_documents)
        if not ownership_validation['consistent']:
            inconsistencies.extend(ownership_validation['inconsistencies'])
            validation_score -= 25
        
        is_consistent = len(inconsistencies) == 0
        
        return {
            "is_consistent": is_consistent,
            "validation_score": max(0, validation_score),
            "inconsistencies_found": len(inconsistencies),
            "inconsistencies": inconsistencies,
            "field_validations": {
                "business_name": name_validation['consistent'],
                "tax_id": tax_id_validation['consistent'],
                "address": address_validation['consistent'],
                "incorporation_date": date_validation['consistent'],
                "beneficial_ownership": ownership_validation['consistent']
            },
            "validation_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error cross-validating extracted data: {str(e)}")
        return {
            "is_consistent": False,
            "error": f"Cross-validation failed: {str(e)}"
        }


# Function automatically becomes a tool when added to agent
def generate_document_processing_report(
    application_id: str,
    documents: List[Dict[str, Any]],
    validation_results: Dict[str, Any],
    authenticity_results: List[Dict[str, Any]],
    cross_validation: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate comprehensive document processing report.
    
    Args:
        application_id: Application identifier
        documents: List of processed documents
        validation_results: Document validation results
        authenticity_results: Authenticity verification results
        cross_validation: Cross-validation results
    
    Returns:
        Dict with complete document processing report
    """
    try:
        # Calculate overall document score
        validation_score = validation_results.get('overall_confidence', 0)
        authenticity_scores = [result.get('authenticity_score', 0) for result in authenticity_results]
        avg_authenticity_score = sum(authenticity_scores) / len(authenticity_scores) if authenticity_scores else 0
        consistency_score = cross_validation.get('validation_score', 0)
        
        overall_score = (validation_score * 0.4 + avg_authenticity_score * 0.35 + consistency_score * 0.25)
        
        # Determine processing status
        all_authentic = all(result.get('is_authentic', False) for result in authenticity_results)
        all_valid = validation_results.get('all_documents_valid', False)
        is_consistent = cross_validation.get('is_consistent', False)
        
        if all_valid and all_authentic and is_consistent and overall_score >= 80:
            processing_status = "passed"
        elif overall_score >= 60:
            processing_status = "passed_with_conditions"
        else:
            processing_status = "requires_manual_review"
        
        # Compile all issues
        all_issues = []
        
        # Missing documents
        missing_docs = validation_results.get('missing_documents', [])
        if missing_docs:
            all_issues.extend([f"Missing document: {doc}" for doc in missing_docs])
        
        # Authenticity issues
        for auth_result in authenticity_results:
            if not auth_result.get('is_authentic', True):
                doc_id = auth_result.get('document_id', 'Unknown')
                all_issues.append(f"Document {doc_id} authenticity concerns")
        
        # Consistency issues
        inconsistencies = cross_validation.get('inconsistencies', [])
        all_issues.extend(inconsistencies)
        
        # Generate recommendations
        recommendations = generate_document_recommendations(
            processing_status, all_issues, overall_score
        )
        
        return {
            "application_id": application_id,
            "processing_status": processing_status,
            "overall_score": round(overall_score, 1),
            "documents_processed": len(documents),
            "issues_identified": len(all_issues),
            "issue_summary": all_issues[:10],  # Limit for readability
            "recommendations": recommendations,
            "manual_review_required": processing_status == "requires_manual_review",
            "report_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error generating document processing report: {str(e)}")
        return {
            "application_id": application_id,
            "processing_status": "error",
            "error": f"Report generation failed: {str(e)}"
        }


def simulate_document_extraction(document_type: str) -> Dict[str, Any]:
    """Simulate document AI extraction based on document type."""
    
    if document_type == DocumentType.ARTICLES_OF_INCORPORATION.value:
        return {
            "business_name": "Acme Corporation",
            "entity_type": "corporation",
            "incorporation_date": "2020-01-15",
            "state_of_incorporation": "Delaware",
            "registered_agent": "Corporate Services Inc.",
            "authorized_shares": 10000000,
            "incorporator": "John Doe"
        }
    
    elif document_type == DocumentType.BUSINESS_LICENSE.value:
        return {
            "license_number": "BL-2024-001234",
            "business_name": "Acme Corporation",
            "license_type": "General Business License",
            "issue_date": "2024-01-01",
            "expiration_date": "2024-12-31",
            "issuing_authority": "City Business Department"
        }
    
    elif document_type == DocumentType.TAX_ID_CERTIFICATE.value:
        return {
            "tax_id": "12-3456789",
            "business_name": "Acme Corporation", 
            "entity_type": "corporation",
            "issue_date": "2020-01-20"
        }
    
    elif document_type == DocumentType.FINANCIAL_STATEMENTS.value:
        return {
            "reporting_period": "2023-12-31",
            "business_name": "Acme Corporation",
            "annual_revenue": 5500000,
            "net_income": 550000,
            "total_assets": 3200000,
            "total_liabilities": 1800000,
            "current_assets": 1200000,
            "current_liabilities": 600000,
            "prepared_by": "CPA Firm LLC"
        }
    
    elif document_type == DocumentType.BENEFICIAL_OWNERSHIP.value:
        return {
            "certification_date": "2024-01-01",
            "business_name": "Acme Corporation",
            "beneficial_owners": [
                {
                    "name": "John Smith",
                    "ownership_percentage": 60,
                    "control_person": True
                },
                {
                    "name": "Jane Doe", 
                    "ownership_percentage": 40,
                    "control_person": False
                }
            ]
        }
    
    else:
        return {
            "document_type": document_type,
            "extraction_note": "Generic document extraction",
            "extracted_fields": ["field1", "field2", "field3"]
        }


def validate_extracted_data(document_type: str, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate the quality and completeness of extracted data."""
    
    required_fields_map = {
        DocumentType.ARTICLES_OF_INCORPORATION.value: [
            'business_name', 'entity_type', 'incorporation_date', 'state_of_incorporation'
        ],
        DocumentType.BUSINESS_LICENSE.value: [
            'license_number', 'business_name', 'issue_date', 'expiration_date'
        ],
        DocumentType.TAX_ID_CERTIFICATE.value: [
            'tax_id', 'business_name', 'entity_type'
        ],
        DocumentType.FINANCIAL_STATEMENTS.value: [
            'annual_revenue', 'net_income', 'total_assets', 'total_liabilities'
        ],
        DocumentType.BENEFICIAL_OWNERSHIP.value: [
            'business_name', 'beneficial_owners'
        ]
    }
    
    required_fields = required_fields_map.get(document_type, [])
    missing_fields = [field for field in required_fields if not extracted_data.get(field)]
    
    confidence_score = max(0, 100 - (len(missing_fields) * 20))
    
    return {
        "valid": len(missing_fields) == 0,
        "confidence_score": confidence_score,
        "required_fields": required_fields,
        "missing_fields": missing_fields,
        "extracted_fields": list(extracted_data.keys())
    }


def get_required_documents(entity_type: str) -> List[str]:
    """Get required documents based on entity type."""
    base_requirements = [
        DocumentType.TAX_ID_CERTIFICATE.value,
        DocumentType.BUSINESS_LICENSE.value,
        DocumentType.FINANCIAL_STATEMENTS.value,
        DocumentType.BENEFICIAL_OWNERSHIP.value
    ]
    
    entity_specific = {
        'corporation': [DocumentType.ARTICLES_OF_INCORPORATION.value],
        'llc': [DocumentType.OPERATING_AGREEMENT.value],
        'partnership': [DocumentType.PARTNERSHIP_AGREEMENT.value]
    }
    
    additional_docs = entity_specific.get(entity_type.lower(), [])
    return base_requirements + additional_docs


def validate_individual_document(document: Dict[str, Any], business_info: Dict[str, Any]) -> Dict[str, Any]:
    """Validate individual document against business information."""
    
    doc_type = document.get('document_type')
    extracted_data = document.get('extracted_data', {})
    
    validation_issues = []
    
    # Validate business name matches
    doc_business_name = extracted_data.get('business_name', '').strip().upper()
    provided_business_name = business_info.get('legal_name', '').strip().upper()
    
    if doc_business_name and provided_business_name and doc_business_name != provided_business_name:
        validation_issues.append(f"Business name mismatch in {doc_type}")
    
    # Validate tax ID if present
    doc_tax_id = extracted_data.get('tax_id', '').replace('-', '')
    provided_tax_id = business_info.get('tax_id', '').replace('-', '')
    
    if doc_tax_id and provided_tax_id and doc_tax_id != provided_tax_id:
        validation_issues.append(f"Tax ID mismatch in {doc_type}")
    
    # Document-specific validations
    if doc_type == DocumentType.BUSINESS_LICENSE.value:
        expiration_date = extracted_data.get('expiration_date')
        if expiration_date:
            try:
                exp_date = datetime.fromisoformat(expiration_date)
                if exp_date < datetime.now():
                    validation_issues.append("Business license has expired")
            except:
                validation_issues.append("Invalid expiration date format")
    
    return {
        "document_id": document.get('document_id'),
        "document_type": doc_type,
        "valid": len(validation_issues) == 0,
        "validation_issues": validation_issues
    }


def calculate_overall_confidence(validation_results: List[Dict[str, Any]]) -> float:
    """Calculate overall confidence score for document validation."""
    if not validation_results:
        return 0
    
    valid_docs = sum(1 for result in validation_results if result.get('valid', False))
    return (valid_docs / len(validation_results)) * 100


def validate_document_format(document_type: str, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate document format and structure."""
    
    score = 100
    risk_factors = []
    
    # Check for expected fields based on document type
    expected_patterns = {
        DocumentType.TAX_ID_CERTIFICATE.value: {
            'tax_id': r'^\d{2}-\d{7}$'  # EIN format
        },
        DocumentType.BUSINESS_LICENSE.value: {
            'license_number': r'^[A-Z]{2}-\d{4}-\d{6}$'  # Example license format
        }
    }
    
    patterns = expected_patterns.get(document_type, {})
    
    for field, pattern in patterns.items():
        value = extracted_data.get(field, '')
        if value:
            import re
            if not re.match(pattern, value):
                risk_factors.append(f"Invalid {field} format")
                score -= 20
        else:
            risk_factors.append(f"Missing required field: {field}")
            score -= 30
    
    return {
        "check_type": "format_validation",
        "score": max(0, score),
        "risk_factors": risk_factors
    }


def cross_reference_validation(document_type: str, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """Cross-reference document data with external sources."""
    
    score = 100
    risk_factors = []
    
    # Simulate external validation
    if document_type == DocumentType.BUSINESS_LICENSE.value:
        license_number = extracted_data.get('license_number')
        if license_number and not simulate_license_verification(license_number):
            risk_factors.append("License number not found in registry")
            score -= 50
    
    elif document_type == DocumentType.ARTICLES_OF_INCORPORATION.value:
        business_name = extracted_data.get('business_name')
        state = extracted_data.get('state_of_incorporation')
        if business_name and state and not simulate_incorporation_verification(business_name, state):
            risk_factors.append("Incorporation not verified with state registry")
            score -= 40
    
    return {
        "check_type": "cross_reference_validation",
        "score": max(0, score),
        "risk_factors": risk_factors
    }


def detect_fraud_patterns(document_type: str, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """Detect potential fraud patterns in documents."""
    
    score = 100
    risk_factors = []
    
    # Check for suspicious patterns
    business_name = extracted_data.get('business_name', '').lower()
    
    # Suspicious business names
    suspicious_keywords = ['fake', 'test', 'dummy', 'sample', 'fraud']
    if any(keyword in business_name for keyword in suspicious_keywords):
        risk_factors.append("Suspicious business name detected")
        score -= 70
    
    # Check for unrealistic financial data
    if document_type == DocumentType.FINANCIAL_STATEMENTS.value:
        revenue = extracted_data.get('annual_revenue', 0)
        net_income = extracted_data.get('net_income', 0)
        
        if revenue > 0 and net_income / revenue > 0.5:  # >50% profit margin
            risk_factors.append("Unusually high profit margin")
            score -= 20
        
        if revenue > 100000000:  # >$100M revenue
            risk_factors.append("Unusually high revenue for new business")
            score -= 15
    
    return {
        "check_type": "fraud_pattern_detection", 
        "score": max(0, score),
        "risk_factors": risk_factors
    }


def simulate_license_verification(license_number: str) -> bool:
    """Simulate license verification with external registry."""
    # For demo, assume valid if follows expected pattern
    import re
    return bool(re.match(r'^[A-Z]{2}-\d{4}-\d{6}$', license_number))


def simulate_incorporation_verification(business_name: str, state: str) -> bool:
    """Simulate incorporation verification with state registry."""
    # For demo, reject suspicious names
    suspicious_names = ['fake', 'test', 'dummy', 'fraud']
    return not any(suspicious in business_name.lower() for suspicious in suspicious_names)


def extract_key_fields_from_documents(documents: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """Extract key fields from all documents for cross-validation."""
    
    fields = {
        'business_names': [],
        'tax_ids': [],
        'addresses': [],
        'incorporation_dates': []
    }
    
    for doc in documents:
        extracted_data = doc.get('extracted_data', {})
        
        if extracted_data.get('business_name'):
            fields['business_names'].append(extracted_data['business_name'])
        
        if extracted_data.get('tax_id'):
            fields['tax_ids'].append(extracted_data['tax_id'])
        
        if extracted_data.get('address'):
            fields['addresses'].append(str(extracted_data['address']))
        
        if extracted_data.get('incorporation_date'):
            fields['incorporation_dates'].append(extracted_data['incorporation_date'])
    
    return fields


def validate_business_name_consistency(extracted_fields: Dict[str, List], business_info: Dict[str, Any]) -> Dict[str, Any]:
    """Validate business name consistency across documents."""
    
    business_names = extracted_fields.get('business_names', [])
    provided_name = business_info.get('legal_name', '').strip().upper()
    
    inconsistencies = []
    
    for name in business_names:
        if name.strip().upper() != provided_name:
            inconsistencies.append(f"Business name inconsistency: {name} vs {provided_name}")
    
    return {
        'consistent': len(inconsistencies) == 0,
        'inconsistencies': inconsistencies
    }


def validate_tax_id_consistency(extracted_fields: Dict[str, List], business_info: Dict[str, Any]) -> Dict[str, Any]:
    """Validate tax ID consistency across documents."""
    
    tax_ids = [tid.replace('-', '') for tid in extracted_fields.get('tax_ids', [])]
    provided_tax_id = business_info.get('tax_id', '').replace('-', '')
    
    inconsistencies = []
    
    for tax_id in tax_ids:
        if tax_id != provided_tax_id:
            inconsistencies.append(f"Tax ID inconsistency: {tax_id} vs {provided_tax_id}")
    
    return {
        'consistent': len(inconsistencies) == 0,
        'inconsistencies': inconsistencies
    }


def validate_address_consistency(extracted_fields: Dict[str, List], business_info: Dict[str, Any]) -> Dict[str, Any]:
    """Validate address consistency across documents."""
    
    addresses = extracted_fields.get('addresses', [])
    provided_address = str(business_info.get('business_address', {}))
    
    inconsistencies = []
    
    # Simple consistency check (in production, would use address normalization)
    for address in addresses:
        if address != provided_address:
            inconsistencies.append(f"Address inconsistency found")
    
    return {
        'consistent': len(inconsistencies) == 0,
        'inconsistencies': inconsistencies
    }


def validate_incorporation_date_consistency(extracted_fields: Dict[str, List], business_info: Dict[str, Any]) -> Dict[str, Any]:
    """Validate incorporation date consistency."""
    
    dates = extracted_fields.get('incorporation_dates', [])
    provided_date = business_info.get('incorporation_date', '')
    
    inconsistencies = []
    
    for date in dates:
        if date != provided_date:
            inconsistencies.append(f"Incorporation date inconsistency: {date} vs {provided_date}")
    
    return {
        'consistent': len(inconsistencies) == 0,
        'inconsistencies': inconsistencies
    }


def validate_ownership_consistency(documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate beneficial ownership consistency across documents."""
    
    ownership_docs = [
        doc for doc in documents 
        if doc.get('document_type') == DocumentType.BENEFICIAL_OWNERSHIP.value
    ]
    
    inconsistencies = []
    
    if len(ownership_docs) > 1:
        # Compare ownership information across multiple beneficial ownership documents
        first_doc = ownership_docs[0].get('extracted_data', {})
        first_owners = first_doc.get('beneficial_owners', [])
        
        for i, doc in enumerate(ownership_docs[1:], 1):
            doc_owners = doc.get('extracted_data', {}).get('beneficial_owners', [])
            
            if len(first_owners) != len(doc_owners):
                inconsistencies.append(f"Different number of owners in document {i+1}")
            
            # Check ownership percentages
            first_total = sum(owner.get('ownership_percentage', 0) for owner in first_owners)
            doc_total = sum(owner.get('ownership_percentage', 0) for owner in doc_owners)
            
            if abs(first_total - doc_total) > 1:  # Allow 1% difference for rounding
                inconsistencies.append(f"Ownership percentage mismatch in document {i+1}")
    
    return {
        'consistent': len(inconsistencies) == 0,
        'inconsistencies': inconsistencies
    }


def generate_document_recommendations(status: str, issues: List[str], score: float) -> List[str]:
    """Generate document processing recommendations."""
    
    recommendations = []
    
    if status == "passed":
        recommendations.append("Document processing completed successfully")
        recommendations.append("All required documents validated and verified")
    elif status == "passed_with_conditions":
        recommendations.append("Document processing completed with minor issues")
        recommendations.append("Enhanced monitoring recommended due to identified concerns")
        if issues:
            recommendations.append(f"Address the following issues: {issues[0]}")
    else:  # requires_manual_review
        recommendations.append("Manual document review required")
        recommendations.append("Do not proceed with automated onboarding")
        if len(issues) > 3:
            recommendations.append("Multiple significant issues identified")
        
        # Specific recommendations based on issues
        if any("missing" in issue.lower() for issue in issues):
            recommendations.append("Request missing documents from customer")
        if any("authenticity" in issue.lower() for issue in issues):
            recommendations.append("Conduct enhanced document authenticity verification")
        if any("inconsistency" in issue.lower() for issue in issues):
            recommendations.append("Resolve data inconsistencies before proceeding")
    
    return recommendations


# Document Processing Agent prompt
DOCUMENT_PROMPT = """
You are the Document Processing Agent for commercial banking onboarding. Your primary responsibility is to extract, validate, and verify all business documents submitted during the onboarding process.

## Your Role
- Extract structured data from business documents using AI/OCR
- Validate document completeness and accuracy
- Verify document authenticity and detect fraud
- Cross-validate information across multiple documents
- Generate comprehensive document processing reports

## Key Functions
1. **Document Extraction**: Use AI to extract structured data from PDFs and images
2. **Data Validation**: Verify extracted data quality and completeness
3. **Authenticity Verification**: Detect fraudulent or altered documents
4. **Cross-Validation**: Ensure consistency across all submitted documents
5. **Compliance Checking**: Verify all required documents are provided

## Document Types Processed
- **Articles of Incorporation**: Business formation documents
- **Business License**: Operating permits and licenses
- **Tax ID Certificate**: Federal/state tax identification
- **Financial Statements**: Income statements, balance sheets
- **Bank Statements**: Transaction history and account verification
- **Beneficial Ownership**: Ownership structure and control persons
- **Operating Agreements**: Partnership/LLC governing documents

## Validation Standards
- **Completeness**: All required fields extracted with high confidence
- **Consistency**: Information matches across all documents
- **Authenticity**: Documents pass fraud detection screening
- **Currency**: Documents are recent and not expired
- **Compliance**: All regulatory required documents provided

## Quality Thresholds
- **Extraction Confidence**: ≥85% confidence score required
- **Authenticity Score**: ≥70% to pass automated verification
- **Cross-Validation**: Zero tolerance for material inconsistencies
- **Document Age**: Most documents must be <12 months old

## Fraud Detection
- Suspicious document patterns or formatting
- Unrealistic financial data or business metrics
- Inconsistent information across documents
- Documents that fail external verification
- Known fraudulent document characteristics

## Decision Matrix
- **Pass**: All documents valid, authentic, and consistent
- **Pass with Conditions**: Minor issues, enhanced monitoring required
- **Manual Review**: Significant concerns, human verification needed
- **Reject**: Clear fraud indicators or major document deficiencies

Always maintain high standards for document quality and authenticity. When in doubt, escalate for manual review rather than approve questionable documents.
"""

MODEL = "gemini-2.5-pro"

# Create Document Processing agent
document_agent = Agent(
    name="document_processing_agent",
    model=MODEL,
    instruction=DOCUMENT_PROMPT,
    output_key="document_processing_result",
    tools=[
        extract_document_data,
        validate_business_documents,
        verify_document_authenticity,
        cross_validate_extracted_data,
        generate_document_processing_report
    ],
)