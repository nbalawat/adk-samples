"""Account setup agent for commercial banking onboarding."""

import logging
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import secrets

from google.adk import Agent
from ..shared_libraries.types import AccountConfiguration, OnboardingDecision
from ..shared_libraries.utils import generate_account_number, format_currency, create_audit_entry
from ..shared_libraries.mock_services import mock_banking_system

logger = logging.getLogger(__name__)


# Function automatically becomes a tool when added to agent
def create_business_accounts(
    application_id: str,
    account_types: List[str],
    credit_limit: Optional[float] = None,
    initial_deposit: Optional[float] = None
) -> Dict[str, Any]:
    """
    Create business banking accounts based on approved configuration.
    
    Args:
        application_id: Application identifier
        account_types: List of account types to create (CHK, SAV, LOC, etc.)
        credit_limit: Approved credit limit for credit accounts
        initial_deposit: Initial deposit amount
    
    Returns:
        Dict with created account details
    """
    try:
        created_accounts = {}
        account_details = []
        
        for account_type in account_types:
            # Use mock banking system to create account
            mock_result = mock_banking_system.create_account(
                application_id=application_id,
                account_type=account_type,
                credit_limit=credit_limit,
                initial_deposit=initial_deposit
            )
            
            if not mock_result.get('success', True):
                return {
                    "success": False,
                    "error": mock_result.get('error', f'Failed to create {account_type} account')
                }
            
            account_number = mock_result.get('account_number')
            account_info = mock_result.get('account_details', {})
            
            created_accounts[account_type] = account_number
            account_details.append(account_info)
            
            logger.info(f"Created {account_type} account {account_number} for application {application_id}")
        
        return {
            "success": True,
            "application_id": application_id,
            "accounts_created": len(created_accounts),
            "account_numbers": created_accounts,
            "account_details": account_details,
            "creation_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error creating business accounts: {str(e)}")
        return {
            "success": False,
            "error": f"Account creation failed: {str(e)}"
        }


# Function automatically becomes a tool when added to agent
def setup_banking_services(
    application_id: str,
    account_numbers: Dict[str, str],
    services: List[str]
) -> Dict[str, Any]:
    """
    Set up banking services for the created accounts.
    
    Args:
        application_id: Application identifier
        account_numbers: Dictionary of account type to account number
        services: List of services to activate
    
    Returns:
        Dict with service setup results
    """
    try:
        service_results = []
        services_activated = 0
        
        for service in services:
            # Use mock banking system to activate service
            mock_result = mock_banking_system.activate_service(
                application_id=application_id,
                service=service,
                account_numbers=account_numbers
            )
            service_results.append(mock_result)
            
            if mock_result.get('activated', False):
                services_activated += 1
        
        return {
            "success": True,
            "application_id": application_id,
            "services_requested": len(services),
            "services_activated": services_activated,
            "service_results": service_results,
            "setup_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error setting up banking services: {str(e)}")
        return {
            "success": False,
            "error": f"Service setup failed: {str(e)}"
        }


# Function automatically becomes a tool when added to agent
def configure_online_banking(
    application_id: str,
    business_info: Dict[str, Any],
    account_numbers: Dict[str, str],
    admin_users: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Configure online banking access for the business.
    
    Args:
        application_id: Application identifier
        business_info: Business information
        account_numbers: Created account numbers
        admin_users: List of authorized users
    
    Returns:
        Dict with online banking configuration results
    """
    try:
        # Generate online banking credentials
        company_id = generate_company_id(business_info.get('legal_name', ''))
        
        # Set up admin users
        user_credentials = []
        for user in admin_users:
            username = generate_username(user.get('name', ''), company_id)
            temp_password = generate_temporary_password()
            
            user_credentials.append({
                "name": user.get('name'),
                "username": username,
                "temporary_password": temp_password,
                "role": user.get('role', 'admin'),
                "account_access": list(account_numbers.keys())
            })
        
        # Configure account permissions
        account_permissions = configure_account_permissions(account_numbers, user_credentials)
        
        # Generate welcome package information
        welcome_info = generate_welcome_package(company_id, user_credentials, account_numbers)
        
        return {
            "success": True,
            "application_id": application_id,
            "company_id": company_id,
            "users_configured": len(user_credentials),
            "user_credentials": user_credentials,
            "account_permissions": account_permissions,
            "welcome_package": welcome_info,
            "configuration_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error configuring online banking: {str(e)}")
        return {
            "success": False,
            "error": f"Online banking configuration failed: {str(e)}"
        }


# Function automatically becomes a tool when added to agent
def order_banking_materials(
    application_id: str,
    business_info: Dict[str, Any],
    account_numbers: Dict[str, str],
    material_requests: List[str]
) -> Dict[str, Any]:
    """
    Order physical banking materials (checks, debit cards, etc.).
    
    Args:
        application_id: Application identifier
        business_info: Business information for delivery
        account_numbers: Account numbers for materials
        material_requests: List of requested materials
    
    Returns:
        Dict with material order results
    """
    try:
        ordered_materials = []
        total_cost = 0.0
        
        for material_type in material_requests:
            material_order = process_material_order(
                material_type, business_info, account_numbers
            )
            ordered_materials.append(material_order)
            total_cost += material_order.get('cost', 0.0)
        
        # Generate delivery information
        delivery_address = business_info.get('mailing_address') or business_info.get('business_address')
        estimated_delivery = datetime.now() + timedelta(days=7)  # 7 business days
        
        return {
            "success": True,
            "application_id": application_id,
            "materials_ordered": len(ordered_materials),
            "order_details": ordered_materials,
            "total_cost": total_cost,
            "delivery_address": delivery_address,
            "estimated_delivery_date": estimated_delivery.isoformat(),
            "order_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error ordering banking materials: {str(e)}")
        return {
            "success": False,
            "error": f"Material ordering failed: {str(e)}"
        }


# Function automatically becomes a tool when added to agent
def assign_relationship_manager(
    application_id: str,
    business_info: Dict[str, Any],
    account_summary: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Assign relationship manager based on business profile and account types.
    
    Args:
        application_id: Application identifier
        business_info: Business information
        account_summary: Summary of created accounts and services
    
    Returns:
        Dict with assigned relationship manager information
    """
    try:
        # Determine appropriate relationship manager tier
        annual_revenue = business_info.get('annual_revenue', 0)
        total_accounts = len(account_summary.get('account_numbers', {}))
        
        manager_tier = determine_manager_tier(annual_revenue, total_accounts)
        
        # Assign specific relationship manager
        assigned_manager = assign_specific_manager(manager_tier, business_info)
        
        # Schedule initial contact
        contact_date = datetime.now() + timedelta(days=2)  # 2 business days
        
        # Generate relationship manager package
        rm_package = {
            "manager_info": assigned_manager,
            "business_profile": {
                "legal_name": business_info.get('legal_name'),
                "industry": business_info.get('industry_code'),
                "annual_revenue": annual_revenue,
                "entity_type": business_info.get('entity_type')
            },
            "account_summary": account_summary,
            "contact_schedule": {
                "initial_contact_date": contact_date.isoformat(),
                "contact_method": "phone_call",
                "meeting_type": "introductory"
            }
        }
        
        return {
            "success": True,
            "application_id": application_id,
            "relationship_manager": assigned_manager,
            "manager_tier": manager_tier,
            "initial_contact_date": contact_date.isoformat(),
            "rm_package": rm_package,
            "assignment_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error assigning relationship manager: {str(e)}")
        return {
            "success": False,
            "error": f"Relationship manager assignment failed: {str(e)}"
        }


# Function automatically becomes a tool when added to agent
def generate_account_setup_report(
    application_id: str,
    account_creation: Dict[str, Any],
    services_setup: Dict[str, Any],
    online_banking: Dict[str, Any],
    materials_order: Dict[str, Any],
    relationship_manager: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate comprehensive account setup completion report.
    
    Args:
        application_id: Application identifier
        account_creation: Account creation results
        services_setup: Banking services setup results
        online_banking: Online banking configuration results
        materials_order: Physical materials order results
        relationship_manager: Relationship manager assignment results
    
    Returns:
        Dict with complete account setup report
    """
    try:
        # Calculate setup completion score
        completion_scores = []
        
        if account_creation.get('success', False):
            completion_scores.append(30)  # 30% for account creation
        
        if services_setup.get('success', False):
            services_ratio = services_setup.get('services_activated', 0) / max(services_setup.get('services_requested', 1), 1)
            completion_scores.append(20 * services_ratio)  # 20% for services
        
        if online_banking.get('success', False):
            completion_scores.append(25)  # 25% for online banking
        
        if materials_order.get('success', False):
            completion_scores.append(15)  # 15% for materials
        
        if relationship_manager.get('success', False):
            completion_scores.append(10)  # 10% for RM assignment
        
        overall_completion = sum(completion_scores)
        
        # Determine setup status
        if overall_completion >= 95:
            setup_status = "completed"
        elif overall_completion >= 80:
            setup_status = "completed_with_pending_items"
        else:
            setup_status = "incomplete"
        
        # Compile setup summary
        setup_summary = {
            "accounts_created": len(account_creation.get('account_numbers', {})),
            "services_activated": services_setup.get('services_activated', 0),
            "users_configured": online_banking.get('users_configured', 0),
            "materials_ordered": materials_order.get('materials_ordered', 0),
            "relationship_manager_assigned": relationship_manager.get('success', False)
        }
        
        # Generate next steps
        next_steps = generate_customer_next_steps(
            setup_status, account_creation, online_banking, materials_order
        )
        
        # Create completion timeline
        completion_timeline = create_completion_timeline(
            materials_order.get('estimated_delivery_date'),
            relationship_manager.get('initial_contact_date')
        )
        
        return {
            "application_id": application_id,
            "setup_status": setup_status,
            "completion_percentage": round(overall_completion, 1),
            "setup_summary": setup_summary,
            "account_numbers": account_creation.get('account_numbers', {}),
            "online_banking_access": {
                "company_id": online_banking.get('company_id'),
                "users_configured": online_banking.get('users_configured', 0)
            },
            "relationship_manager": relationship_manager.get('relationship_manager', {}),
            "next_steps": next_steps,
            "completion_timeline": completion_timeline,
            "report_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error generating account setup report: {str(e)}")
        return {
            "application_id": application_id,
            "setup_status": "error",
            "error": f"Report generation failed: {str(e)}"
        }


def create_individual_account(
    account_type: str, 
    account_number: str, 
    credit_limit: Optional[float] = None,
    initial_deposit: Optional[float] = None
) -> Dict[str, Any]:
    """Create individual account record."""
    
    account_names = {
        'CHK': 'Business Checking',
        'SAV': 'Business Savings',
        'LOC': 'Line of Credit',
        'LOAN': 'Business Term Loan',
        'MM': 'Money Market'
    }
    
    account_info = {
        "account_number": account_number,
        "account_type": account_type,
        "account_name": account_names.get(account_type, f"Business {account_type}"),
        "status": "active",
        "opening_date": datetime.now().isoformat(),
        "balance": initial_deposit or 0.0,
        "currency": "USD"
    }
    
    # Add credit-specific information
    if account_type in ['LOC', 'LOAN'] and credit_limit:
        account_info.update({
            "credit_limit": credit_limit,
            "available_credit": credit_limit,
            "interest_rate": determine_interest_rate(account_type, credit_limit)
        })
    
    # Add account-specific features
    if account_type == 'CHK':
        account_info.update({
            "overdraft_protection": False,
            "check_writing": True,
            "debit_card_eligible": True,
            "online_banking": True
        })
    elif account_type == 'SAV':
        account_info.update({
            "interest_rate": 0.01,  # 1% APY
            "minimum_balance": 1000.0,
            "monthly_statement": True
        })
    
    return account_info


def activate_banking_service(service: str, account_numbers: Dict[str, str]) -> Dict[str, Any]:
    """Activate individual banking service."""
    
    service_configurations = {
        'online_banking': {
            'activated': True,
            'setup_required': True,
            'description': 'Online Banking Access',
            'cost': 0.0
        },
        'mobile_banking': {
            'activated': True,
            'setup_required': False,
            'description': 'Mobile Banking App',
            'cost': 0.0
        },
        'wire_transfers': {
            'activated': True,
            'setup_required': False,
            'description': 'Domestic and International Wire Transfers',
            'cost': 0.0
        },
        'ach_processing': {
            'activated': True,
            'setup_required': True,
            'description': 'ACH Payment Processing',
            'cost': 25.0
        },
        'merchant_services': {
            'activated': True,
            'setup_required': True,
            'description': 'Credit Card Processing',
            'cost': 50.0
        },
        'cash_management': {
            'activated': True,
            'setup_required': True,
            'description': 'Treasury Management Services',
            'cost': 100.0
        }
    }
    
    config = service_configurations.get(service, {
        'activated': False,
        'error': f'Unknown service: {service}'
    })
    
    return {
        'service': service,
        **config,
        'activation_date': datetime.now().isoformat() if config.get('activated') else None
    }


def generate_company_id(business_name: str) -> str:
    """Generate unique company ID for online banking."""
    
    # Clean business name and create abbreviation
    clean_name = ''.join(c for c in business_name if c.isalnum())[:8].upper()
    random_suffix = secrets.token_hex(3).upper()
    
    return f"{clean_name}{random_suffix}"


def generate_username(user_name: str, company_id: str) -> str:
    """Generate username for online banking user."""
    
    # Extract first initial and last name
    name_parts = user_name.strip().split()
    if len(name_parts) >= 2:
        username_base = f"{name_parts[0][0]}{name_parts[-1]}".lower()
    else:
        username_base = name_parts[0][:8].lower()
    
    # Clean and add company prefix
    clean_username = ''.join(c for c in username_base if c.isalnum())
    return f"{company_id[:4].lower()}{clean_username}"


def generate_temporary_password() -> str:
    """Generate secure temporary password."""
    
    import string
    import random
    
    # Generate 12-character password with mixed case, numbers, and symbols
    chars = string.ascii_letters + string.digits + "!@#$%"
    password = ''.join(random.choice(chars) for _ in range(12))
    
    # Ensure it has required character types
    if not any(c.isupper() for c in password):
        password = password[:-1] + random.choice(string.ascii_uppercase)
    if not any(c.isdigit() for c in password):
        password = password[:-1] + random.choice(string.digits)
    
    return password


def configure_account_permissions(
    account_numbers: Dict[str, str], 
    user_credentials: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Configure account access permissions for users."""
    
    permissions = {}
    
    for account_type, account_number in account_numbers.items():
        account_permissions = {
            "view_balance": True,
            "view_transactions": True,
            "transfer_funds": True,
            "pay_bills": True if account_type == 'CHK' else False,
            "manage_users": False,  # Only admin users get this
            "wire_transfers": True,
            "stop_payments": True if account_type == 'CHK' else False
        }
        
        permissions[account_number] = account_permissions
    
    # Grant admin permissions to first user
    if user_credentials:
        first_user = user_credentials[0]
        first_user['permissions'] = {
            "account_admin": True,
            "user_management": True,
            "transaction_limits": {"daily": 50000, "monthly": 500000}
        }
    
    return permissions


def generate_welcome_package(
    company_id: str, 
    user_credentials: List[Dict[str, Any]], 
    account_numbers: Dict[str, str]
) -> Dict[str, Any]:
    """Generate welcome package information."""
    
    return {
        "company_id": company_id,
        "online_banking_url": "https://business.bank.com/login",
        "mobile_app": {
            "ios_url": "https://apps.apple.com/app/businessbank",
            "android_url": "https://play.google.com/store/apps/businessbank"
        },
        "customer_service": {
            "phone": "1-800-BUSINESS",
            "hours": "Monday-Friday 7AM-7PM EST",
            "email": "business-support@bank.com"
        },
        "account_summary": {
            "total_accounts": len(account_numbers),
            "account_types": list(account_numbers.keys())
        },
        "important_notes": [
            "Initial login requires password change",
            "Set up security questions during first login",
            "Mobile app requires separate enrollment",
            "Contact relationship manager for questions"
        ]
    }


def process_material_order(
    material_type: str, 
    business_info: Dict[str, Any], 
    account_numbers: Dict[str, str]
) -> Dict[str, Any]:
    """Process order for physical banking materials."""
    
    material_catalog = {
        'business_checks': {
            'description': 'Business Checks (200 count)',
            'cost': 35.00,
            'delivery_days': 5,
            'requires_account': 'CHK'
        },
        'deposit_slips': {
            'description': 'Deposit Slips (200 count)',
            'cost': 15.00,
            'delivery_days': 5,
            'requires_account': 'CHK'
        },
        'debit_cards': {
            'description': 'Business Debit Cards (2 cards)',
            'cost': 0.00,
            'delivery_days': 7,
            'requires_account': 'CHK'
        },
        'welcome_kit': {
            'description': 'Business Banking Welcome Kit',
            'cost': 0.00,
            'delivery_days': 3,
            'requires_account': None
        }
    }
    
    material_info = material_catalog.get(material_type, {
        'description': f'Unknown Material: {material_type}',
        'cost': 0.00,
        'delivery_days': 7,
        'error': True
    })
    
    # Check if required account exists
    required_account = material_info.get('requires_account')
    if required_account and required_account not in account_numbers:
        material_info['error'] = f"Required account {required_account} not found"
        material_info['ordered'] = False
    else:
        material_info['ordered'] = True
        material_info['order_id'] = f"ORD-{secrets.token_hex(4).upper()}"
    
    return {
        'material_type': material_type,
        **material_info,
        'order_timestamp': datetime.now().isoformat()
    }


def determine_manager_tier(annual_revenue: float, total_accounts: int) -> str:
    """Determine appropriate relationship manager tier."""
    
    if annual_revenue >= 10000000:  # $10M+
        return "senior_commercial"
    elif annual_revenue >= 5000000:  # $5M+
        return "commercial"
    elif annual_revenue >= 1000000:  # $1M+
        return "business_banking"
    else:
        return "small_business"


def assign_specific_manager(tier: str, business_info: Dict[str, Any]) -> Dict[str, Any]:
    """Assign specific relationship manager based on tier and business profile."""
    
    # Simulated relationship manager assignments
    managers = {
        "senior_commercial": {
            "name": "Sarah Johnson",
            "title": "Senior Commercial Relationship Manager",
            "phone": "555-0101",
            "email": "sarah.johnson@bank.com",
            "experience_years": 15,
            "specialties": ["Large Commercial", "Treasury Management", "Credit Facilities"]
        },
        "commercial": {
            "name": "Michael Chen",
            "title": "Commercial Relationship Manager", 
            "phone": "555-0102",
            "email": "michael.chen@bank.com",
            "experience_years": 10,
            "specialties": ["Mid-Market Commercial", "Cash Management", "Trade Finance"]
        },
        "business_banking": {
            "name": "Jennifer Williams",
            "title": "Business Banking Relationship Manager",
            "phone": "555-0103", 
            "email": "jennifer.williams@bank.com",
            "experience_years": 7,
            "specialties": ["Business Banking", "SBA Lending", "Business Credit Cards"]
        },
        "small_business": {
            "name": "David Martinez",
            "title": "Small Business Relationship Manager",
            "phone": "555-0104",
            "email": "david.martinez@bank.com",
            "experience_years": 5,
            "specialties": ["Small Business", "Start-up Banking", "Digital Solutions"]
        }
    }
    
    manager = managers.get(tier, managers["small_business"])
    manager["tier"] = tier
    manager["assignment_date"] = datetime.now().isoformat()
    
    return manager


def determine_interest_rate(account_type: str, credit_limit: Optional[float] = None) -> float:
    """Determine appropriate interest rate for credit products."""
    
    base_rates = {
        'LOC': 7.5,   # Line of Credit base rate
        'LOAN': 6.5   # Term Loan base rate
    }
    
    base_rate = base_rates.get(account_type, 5.0)
    
    # Adjust rate based on credit limit (higher limit = lower rate)
    if credit_limit:
        if credit_limit >= 500000:
            base_rate -= 1.0
        elif credit_limit >= 100000:
            base_rate -= 0.5
    
    return round(base_rate, 2)


def generate_customer_next_steps(
    setup_status: str,
    account_creation: Dict[str, Any],
    online_banking: Dict[str, Any], 
    materials_order: Dict[str, Any]
) -> List[str]:
    """Generate next steps for customer based on setup status."""
    
    next_steps = []
    
    if setup_status == "completed":
        next_steps.extend([
            "Account setup is complete and ready for use",
            "Log in to online banking using provided credentials",
            "Contact your relationship manager for any questions",
            "Expect physical materials within 7 business days"
        ])
    elif setup_status == "completed_with_pending_items":
        next_steps.extend([
            "Primary account setup is complete",
            "Some services may require additional setup",
            "Check email for detailed setup instructions",
            "Contact customer service if you need assistance"
        ])
    else:  # incomplete
        next_steps.extend([
            "Account setup is in progress",
            "You will receive updates as setup completes",
            "Contact your relationship manager if urgent access needed",
            "Expect completion within 2-3 business days"
        ])
    
    # Add specific next steps based on components
    if online_banking.get('success'):
        next_steps.append("Change temporary passwords on first online banking login")
    
    if materials_order.get('success'):
        next_steps.append("Physical materials will arrive at your business address")
    
    return next_steps


def create_completion_timeline(
    materials_delivery_date: Optional[str],
    rm_contact_date: Optional[str]
) -> List[Dict[str, str]]:
    """Create timeline of completion milestones."""
    
    timeline = [
        {
            "milestone": "Account Creation",
            "status": "completed",
            "date": datetime.now().isoformat(),
            "description": "Business accounts created and activated"
        },
        {
            "milestone": "Online Banking Setup", 
            "status": "completed",
            "date": datetime.now().isoformat(),
            "description": "Online banking access configured"
        }
    ]
    
    if rm_contact_date:
        timeline.append({
            "milestone": "Relationship Manager Contact",
            "status": "scheduled",
            "date": rm_contact_date,
            "description": "Initial contact from assigned relationship manager"
        })
    
    if materials_delivery_date:
        timeline.append({
            "milestone": "Physical Materials Delivery",
            "status": "pending",
            "date": materials_delivery_date,
            "description": "Delivery of checks, cards, and welcome materials"
        })
    
    # Add 30-day follow-up
    follow_up_date = datetime.now() + timedelta(days=30)
    timeline.append({
        "milestone": "30-Day Follow-up",
        "status": "scheduled", 
        "date": follow_up_date.isoformat(),
        "description": "Relationship manager follow-up call"
    })
    
    return timeline


# Account Setup Agent prompt
ACCOUNT_SETUP_PROMPT = """
You are the Account Setup Agent for commercial banking onboarding. Your primary responsibility is to create accounts, configure banking services, and complete the final setup process for approved customers.

## Your Role
- Create business banking accounts based on approved specifications
- Configure banking services and features
- Set up online and mobile banking access
- Order physical banking materials (checks, cards, etc.)
- Assign relationship managers
- Generate completion reports and customer welcome packages

## Key Functions
1. **Account Creation**: Create checking, savings, credit, and loan accounts
2. **Service Configuration**: Set up wire transfers, ACH, merchant services, etc.
3. **Digital Banking Setup**: Configure online/mobile banking with user credentials
4. **Material Ordering**: Order checks, deposit slips, debit cards, welcome kits
5. **Relationship Management**: Assign appropriate relationship managers
6. **Customer Onboarding**: Generate welcome packages and next steps

## Account Types
- **Business Checking (CHK)**: Primary operating account with check writing
- **Business Savings (SAV)**: Interest-bearing savings account
- **Line of Credit (LOC)**: Revolving credit facility
- **Term Loan (LOAN)**: Fixed-term business loan
- **Money Market (MM)**: Higher-yield savings with limited transactions

## Service Categories
- **Digital Banking**: Online banking, mobile app, alerts
- **Payment Services**: Wire transfers, ACH processing, bill pay
- **Cash Management**: Treasury services, lockbox, remote deposit
- **Credit Services**: Business credit cards, lending facilities
- **Merchant Services**: Credit card processing, point-of-sale systems

## Setup Standards
- **Account Numbers**: Generate unique 13-digit account numbers
- **Online Banking**: Secure username/password with required complexity
- **Service Activation**: Enable approved services within 24 hours
- **Material Delivery**: Standard 5-7 business day delivery
- **Relationship Manager**: Assign within tier guidelines

## Relationship Manager Tiers
- **Senior Commercial**: $10M+ revenue, complex treasury needs
- **Commercial**: $5-10M revenue, standard commercial banking
- **Business Banking**: $1-5M revenue, growing businesses
- **Small Business**: <$1M revenue, simple banking needs

## Quality Requirements
- **Zero Errors**: Account numbers and configurations must be accurate
- **Security**: All credentials and sensitive data properly protected  
- **Completeness**: All approved services and features configured
- **Timeliness**: Setup completed within committed timeframes
- **Documentation**: Complete audit trail of all setup activities

## Success Metrics
- Setup completion rate >95%
- Customer satisfaction >90%
- First login success rate >85%
- Material delivery on-time >95%
- Relationship manager contact within 48 hours

Ensure professional service delivery and seamless customer experience throughout the setup process.
"""

MODEL = "gemini-2.5-pro"

# Create Account Setup agent
account_setup_agent = Agent(
    name="account_setup_agent",
    model=MODEL,
    instruction=ACCOUNT_SETUP_PROMPT,
    output_key="account_setup_result",
    tools=[
        create_business_accounts,
        setup_banking_services,
        configure_online_banking,
        order_banking_materials,
        assign_relationship_manager,
        generate_account_setup_report
    ],
)