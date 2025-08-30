"""Utility functions for commercial banking onboarding."""

import re
import hashlib
import secrets
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import logging
from cryptography.fernet import Fernet
import os

logger = logging.getLogger(__name__)


def generate_application_id() -> str:
    """Generate unique application identifier."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = secrets.token_hex(4).upper()
    return f"APP-{timestamp}-{random_suffix}"


def generate_account_number(account_type: str = "CHK") -> str:
    """Generate account number."""
    prefix_map = {
        "CHK": "1001",  # Checking
        "SAV": "2001",  # Savings  
        "LOC": "3001",  # Line of Credit
        "LOAN": "4001", # Business Loan
        "MM": "5001"    # Money Market
    }
    
    prefix = prefix_map.get(account_type, "1001")
    suffix = secrets.randbelow(999999999)
    return f"{prefix}{suffix:09d}"


def validate_tax_id(tax_id: str) -> bool:
    """Validate tax identification number format."""
    # EIN format: XX-XXXXXXX
    ein_pattern = r'^\d{2}-\d{7}$'
    # SSN format for sole proprietorships: XXX-XX-XXXX
    ssn_pattern = r'^\d{3}-\d{2}-\d{4}$'
    
    return bool(re.match(ein_pattern, tax_id) or re.match(ssn_pattern, tax_id))


def validate_email(email: str) -> bool:
    """Validate email address format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """Validate phone number format."""
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    # US phone number should be 10 or 11 digits
    return len(digits) in [10, 11]


def mask_sensitive_data(data: str, visible_chars: int = 4) -> str:
    """Mask sensitive data showing only last N characters."""
    if len(data) <= visible_chars:
        return '*' * len(data)
    
    masked_part = '*' * (len(data) - visible_chars)
    visible_part = data[-visible_chars:]
    return f"{masked_part}{visible_part}"


def encrypt_sensitive_data(data: str) -> str:
    """Encrypt sensitive data using Fernet encryption."""
    key = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
    if isinstance(key, str):
        key = key.encode()
    
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data.decode()


def decrypt_sensitive_data(encrypted_data: str) -> str:
    """Decrypt sensitive data."""
    key = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
    if isinstance(key, str):
        key = key.encode()
    
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data.encode())
    return decrypted_data.decode()


def calculate_business_age(incorporation_date: datetime) -> int:
    """Calculate business age in years."""
    today = datetime.now()
    age = today - incorporation_date
    return age.days // 365


def normalize_business_name(name: str) -> str:
    """Normalize business name for comparison."""
    # Remove common suffixes and normalize
    suffixes = ['INC', 'INCORPORATED', 'LLC', 'LTD', 'LIMITED', 'CORP', 'CORPORATION', 'LP', 'LLP']
    normalized = name.upper().strip()
    
    for suffix in suffixes:
        if normalized.endswith(f' {suffix}'):
            normalized = normalized[:-len(f' {suffix}')]
            break
    
    # Remove special characters and extra spaces
    normalized = re.sub(r'[^\w\s]', '', normalized)
    normalized = ' '.join(normalized.split())
    
    return normalized


def calculate_risk_score(factors: Dict[str, Any]) -> float:
    """Calculate composite risk score from various factors."""
    weights = {
        'credit_score': 0.3,
        'business_age': 0.2,
        'industry_risk': 0.15,
        'ownership_complexity': 0.1,
        'geographic_risk': 0.1,
        'kyc_issues': 0.15
    }
    
    score = 0.0
    total_weight = 0.0
    
    for factor, value in factors.items():
        if factor in weights and value is not None:
            normalized_value = normalize_risk_factor(factor, value)
            score += weights[factor] * normalized_value
            total_weight += weights[factor]
    
    if total_weight > 0:
        return (score / total_weight) * 100
    
    return 50.0  # Default medium risk


def normalize_risk_factor(factor: str, value: Any) -> float:
    """Normalize risk factor to 0-1 scale (0 = low risk, 1 = high risk)."""
    if factor == 'credit_score':
        # Higher credit score = lower risk
        if value >= 750:
            return 0.1
        elif value >= 650:
            return 0.3
        elif value >= 550:
            return 0.6
        else:
            return 0.9
    
    elif factor == 'business_age':
        # Older business = lower risk
        if value >= 10:
            return 0.1
        elif value >= 5:
            return 0.3
        elif value >= 2:
            return 0.6
        else:
            return 0.9
    
    elif factor == 'industry_risk':
        # Industry-specific risk mapping
        high_risk_industries = ['gambling', 'cryptocurrency', 'adult_entertainment']
        medium_risk_industries = ['restaurant', 'retail', 'construction']
        
        if value.lower() in high_risk_industries:
            return 0.9
        elif value.lower() in medium_risk_industries:
            return 0.5
        else:
            return 0.2
    
    elif factor == 'ownership_complexity':
        # More complex ownership = higher risk
        if value > 5:
            return 0.8
        elif value > 2:
            return 0.5
        else:
            return 0.2
    
    elif factor == 'kyc_issues':
        # Boolean: issues = high risk
        return 0.9 if value else 0.1
    
    else:
        return 0.5  # Default medium risk


def format_currency(amount: float) -> str:
    """Format amount as currency."""
    return f"${amount:,.2f}"


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage."""
    # Remove or replace unsafe characters
    sanitized = re.sub(r'[^\w\s.-]', '', filename)
    sanitized = re.sub(r'\s+', '_', sanitized)
    return sanitized.strip('._')


def create_audit_entry(action: str, user_id: str, details: Dict[str, Any]) -> Dict[str, Any]:
    """Create audit log entry."""
    return {
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'user_id': user_id,
        'details': details,
        'ip_address': 'system',  # In real implementation, get from request
        'session_id': secrets.token_hex(16)
    }


def validate_address(address: Dict[str, str]) -> bool:
    """Validate address completeness."""
    required_fields = ['street', 'city', 'state', 'zip_code']
    return all(field in address and address[field].strip() for field in required_fields)


def get_industry_risk_level(naics_code: str) -> str:
    """Determine industry risk level from NAICS code."""
    # High-risk industries
    high_risk_codes = ['713', '722', '531', '523']  # Entertainment, Food Service, Real Estate, Securities
    
    # Medium-risk industries  
    medium_risk_codes = ['236', '441', '452', '444']  # Construction, Auto, General Retail, Building Materials
    
    code_prefix = naics_code[:3]
    
    if code_prefix in high_risk_codes:
        return 'high'
    elif code_prefix in medium_risk_codes:
        return 'medium'
    else:
        return 'low'


def calculate_debt_service_coverage(net_income: float, debt_payments: float) -> Optional[float]:
    """Calculate debt service coverage ratio."""
    if debt_payments <= 0:
        return None
    
    return net_income / debt_payments