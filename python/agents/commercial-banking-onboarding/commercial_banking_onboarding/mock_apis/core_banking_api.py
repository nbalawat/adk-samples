"""
Core Banking API mock for commercial banking onboarding.
Handles account creation, product setup, and banking operations.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import random
import uuid

from .base_api import BaseMockAPI, APIResponse, MockDataGenerator

@dataclass
class BankAccount:
    """Bank account data structure"""
    account_number: str
    account_type: str
    product_code: str
    status: str
    opened_date: str
    balance: float
    currency: str = "USD"
    interest_rate: float = 0.0
    monthly_fee: float = 0.0
    minimum_balance: float = 0.0

@dataclass 
class BankingProduct:
    """Banking product data structure"""
    product_code: str
    product_name: str
    category: str
    description: str
    monthly_fee: float
    minimum_balance: float
    interest_rate: float
    features: List[str]
    eligibility_requirements: List[str]

class MockCoreBankingAPI(BaseMockAPI):
    """
    Mock Core Banking System API for account management and product operations.
    Simulates realistic banking system interactions for commercial clients.
    """
    
    def __init__(self):
        super().__init__("core_banking_api")
        self._accounts = {}
        self._products = {}
        self._transactions = {}
        self._initialize_banking_products()
    
    def _initialize_banking_products(self):
        """Initialize available banking products"""
        products = [
            BankingProduct(
                product_code="BUS_CHK_BASIC",
                product_name="Business Checking Basic",
                category="deposit",
                description="Basic business checking account with standard features",
                monthly_fee=15.00,
                minimum_balance=1000.00,
                interest_rate=0.01,
                features=["Online Banking", "Mobile App", "Debit Cards", "Check Writing"],
                eligibility_requirements=["Business registration", "Tax ID", "Minimum deposit $1000"]
            ),
            BankingProduct(
                product_code="BUS_CHK_PREMIUM",
                product_name="Business Checking Premium",
                category="deposit",
                description="Premium business checking with enhanced features",
                monthly_fee=45.00,
                minimum_balance=5000.00,
                interest_rate=0.15,
                features=["Online Banking", "Mobile App", "Debit Cards", "Check Writing", 
                         "Cash Management", "ACH Processing", "Wire Transfers"],
                eligibility_requirements=["Business registration", "Tax ID", "Minimum deposit $5000"]
            ),
            BankingProduct(
                product_code="BUS_SAV_HIGH_YIELD",
                product_name="Business High-Yield Savings",
                category="deposit",
                description="High-yield savings account for business reserves",
                monthly_fee=0.00,
                minimum_balance=10000.00,
                interest_rate=4.5,
                features=["High Interest Rate", "Online Banking", "Mobile App"],
                eligibility_requirements=["Business registration", "Minimum deposit $10000"]
            ),
            BankingProduct(
                product_code="BUS_CD_12M",
                product_name="Business Certificate of Deposit (12 Month)",
                category="deposit",
                description="12-month certificate of deposit with competitive rates",
                monthly_fee=0.00,
                minimum_balance=25000.00,
                interest_rate=5.25,
                features=["Guaranteed Return", "FDIC Insured", "Auto-renewal Option"],
                eligibility_requirements=["Minimum deposit $25000", "12-month commitment"]
            ),
            BankingProduct(
                product_code="BUS_LOC_SECURED",
                product_name="Secured Business Line of Credit",
                category="credit",
                description="Secured revolving credit line for working capital",
                monthly_fee=25.00,
                minimum_balance=0.00,
                interest_rate=8.75,
                features=["Revolving Credit", "Online Access", "Flexible Repayment"],
                eligibility_requirements=["Collateral required", "Credit approval", "Personal guarantee"]
            ),
            BankingProduct(
                product_code="BUS_MERCHANT",
                product_name="Merchant Services",
                category="payment",
                description="Credit card processing and payment solutions",
                monthly_fee=29.99,
                minimum_balance=0.00,
                interest_rate=0.00,
                features=["Credit Card Processing", "POS Systems", "Online Payments", "Mobile Payments"],
                eligibility_requirements=["Business registration", "Processing agreement"]
            )
        ]
        
        for product in products:
            self._products[product.product_code] = product
    
    def get_available_products(self, business_type: str = None, revenue_range: str = None) -> APIResponse:
        """
        Get available banking products based on business criteria.
        
        Args:
            business_type: Type of business (optional filter)
            revenue_range: Annual revenue range (optional filter)
        
        Returns:
            APIResponse with available products
        """
        availability_check = self._check_api_availability()
        if availability_check:
            return availability_check
        
        try:
            # Filter products based on criteria (simplified logic)
            available_products = list(self._products.values())
            
            # Apply basic filtering
            if revenue_range == "small":  # < $1M
                # Remove high-minimum products for small businesses
                available_products = [p for p in available_products if p.minimum_balance < 25000]
            
            product_data = [
                {
                    "product_code": p.product_code,
                    "product_name": p.product_name,
                    "category": p.category,
                    "description": p.description,
                    "monthly_fee": p.monthly_fee,
                    "minimum_balance": p.minimum_balance,
                    "interest_rate": p.interest_rate,
                    "features": p.features,
                    "eligibility_requirements": p.eligibility_requirements
                }
                for p in available_products
            ]
            
            return self._create_response(data={
                "products": product_data,
                "total_products": len(product_data),
                "filter_criteria": {
                    "business_type": business_type,
                    "revenue_range": revenue_range
                }
            })
            
        except Exception as e:
            return self._create_response(
                error=f"Failed to retrieve products: {str(e)}",
                error_code="PRODUCT_RETRIEVAL_ERROR"
            )
    
    def create_business_account(
        self,
        application_id: str,
        business_info: Dict[str, Any],
        product_codes: List[str],
        initial_deposit: float = 0.0
    ) -> APIResponse:
        """
        Create new business banking accounts.
        
        Args:
            application_id: Application identifier
            business_info: Business information dictionary
            product_codes: List of product codes to set up
            initial_deposit: Initial deposit amount
        
        Returns:
            APIResponse with created account information
        """
        availability_check = self._check_api_availability()
        if availability_check:
            return availability_check
        
        try:
            # Validate products exist
            invalid_products = [code for code in product_codes if code not in self._products]
            if invalid_products:
                return self._create_response(
                    error=f"Invalid product codes: {invalid_products}",
                    error_code="INVALID_PRODUCT_CODE"
                )
            
            created_accounts = []
            
            for product_code in product_codes:
                product = self._products[product_code]
                
                # Generate account number (realistic format)
                account_number = f"{random.randint(100000, 999999)}{random.randint(100, 999)}"
                
                # Check minimum deposit requirement
                if initial_deposit < product.minimum_balance:
                    return self._create_response(
                        error=f"Initial deposit ${initial_deposit} below minimum ${product.minimum_balance} for {product.product_name}",
                        error_code="INSUFFICIENT_INITIAL_DEPOSIT"
                    )
                
                # Create account
                account = BankAccount(
                    account_number=account_number,
                    account_type=product.category,
                    product_code=product_code,
                    status="PENDING_ACTIVATION",
                    opened_date=datetime.now().isoformat(),
                    balance=initial_deposit,
                    currency="USD",
                    interest_rate=product.interest_rate,
                    monthly_fee=product.monthly_fee,
                    minimum_balance=product.minimum_balance
                )
                
                self._accounts[account_number] = account
                created_accounts.append({
                    "account_number": account_number,
                    "product_name": product.product_name,
                    "product_code": product_code,
                    "status": account.status,
                    "opening_balance": initial_deposit,
                    "monthly_fee": product.monthly_fee,
                    "interest_rate": product.interest_rate
                })
            
            return self._create_response(data={
                "application_id": application_id,
                "accounts_created": created_accounts,
                "total_accounts": len(created_accounts),
                "next_steps": [
                    "Accounts pending activation",
                    "Initial deposit will be processed",
                    "Account materials will be prepared",
                    "Online banking access will be configured"
                ]
            })
            
        except Exception as e:
            return self._create_response(
                error=f"Failed to create accounts: {str(e)}",
                error_code="ACCOUNT_CREATION_ERROR"
            )
    
    def activate_accounts(self, account_numbers: List[str]) -> APIResponse:
        """
        Activate pending accounts after onboarding completion.
        
        Args:
            account_numbers: List of account numbers to activate
        
        Returns:
            APIResponse with activation results
        """
        availability_check = self._check_api_availability()
        if availability_check:
            return availability_check
        
        try:
            activation_results = []
            
            for account_number in account_numbers:
                if account_number not in self._accounts:
                    activation_results.append({
                        "account_number": account_number,
                        "status": "ERROR",
                        "message": "Account not found"
                    })
                    continue
                
                account = self._accounts[account_number]
                
                if account.status == "ACTIVE":
                    activation_results.append({
                        "account_number": account_number,
                        "status": "ALREADY_ACTIVE",
                        "message": "Account was already active"
                    })
                    continue
                
                # Activate the account
                account.status = "ACTIVE"
                activation_results.append({
                    "account_number": account_number,
                    "status": "ACTIVATED",
                    "message": "Account successfully activated",
                    "activation_date": datetime.now().isoformat()
                })
            
            successful_activations = len([r for r in activation_results if r["status"] == "ACTIVATED"])
            
            return self._create_response(data={
                "activation_results": activation_results,
                "successful_activations": successful_activations,
                "total_requested": len(account_numbers),
                "all_successful": successful_activations == len(account_numbers)
            })
            
        except Exception as e:
            return self._create_response(
                error=f"Failed to activate accounts: {str(e)}",
                error_code="ACTIVATION_ERROR"
            )
    
    def get_account_details(self, account_number: str) -> APIResponse:
        """
        Get detailed account information.
        
        Args:
            account_number: Account number to query
        
        Returns:
            APIResponse with account details
        """
        availability_check = self._check_api_availability()
        if availability_check:
            return availability_check
        
        try:
            if account_number not in self._accounts:
                return self._create_response(
                    error="Account not found",
                    error_code="ACCOUNT_NOT_FOUND"
                )
            
            account = self._accounts[account_number]
            product = self._products[account.product_code]
            
            return self._create_response(data={
                "account_number": account.account_number,
                "product_name": product.product_name,
                "account_type": account.account_type,
                "status": account.status,
                "current_balance": account.balance,
                "available_balance": account.balance,  # Simplified
                "currency": account.currency,
                "interest_rate": account.interest_rate,
                "monthly_fee": account.monthly_fee,
                "minimum_balance": account.minimum_balance,
                "opened_date": account.opened_date,
                "last_statement_date": (datetime.now() - timedelta(days=30)).isoformat(),
                "features": product.features
            })
            
        except Exception as e:
            return self._create_response(
                error=f"Failed to retrieve account details: {str(e)}",
                error_code="ACCOUNT_RETRIEVAL_ERROR"
            )
    
    def configure_online_banking(self, business_info: Dict[str, Any], account_numbers: List[str]) -> APIResponse:
        """
        Configure online banking access for business accounts.
        
        Args:
            business_info: Business information for setup
            account_numbers: List of account numbers to include
        
        Returns:
            APIResponse with online banking configuration
        """
        availability_check = self._check_api_availability()
        if availability_check:
            return availability_check
        
        try:
            # Generate online banking credentials
            user_id = f"BIZ{random.randint(100000, 999999)}"
            temp_password = f"Temp{random.randint(1000, 9999)}!"
            
            # Configure account access
            configured_accounts = []
            for account_number in account_numbers:
                if account_number in self._accounts:
                    account = self._accounts[account_number]
                    product = self._products[account.product_code]
                    
                    configured_accounts.append({
                        "account_number": account_number,
                        "nickname": f"{product.product_name} - {account_number[-4:]}",
                        "permissions": ["VIEW_BALANCE", "VIEW_TRANSACTIONS", "TRANSFER", "PAY_BILLS"]
                    })
            
            online_banking_config = {
                "user_id": user_id,
                "temporary_password": temp_password,
                "password_reset_required": True,
                "configured_accounts": configured_accounts,
                "access_url": "https://business.bank.com/login",
                "mobile_app": {
                    "ios_app": "Business Banking - App Store",
                    "android_app": "Business Banking - Google Play"
                },
                "features_enabled": [
                    "Account Management", "Transaction History", "Transfers",
                    "Bill Pay", "Mobile Deposit", "Account Alerts", 
                    "Statement Access", "Tax Document Access"
                ],
                "setup_instructions": [
                    f"Visit {business_info.get('legal_name', 'business')} online banking portal",
                    f"Log in with User ID: {user_id}",
                    "Use temporary password and create new secure password",
                    "Set up security questions and contact preferences",
                    "Review account access and permissions"
                ]
            }
            
            return self._create_response(data=online_banking_config)
            
        except Exception as e:
            return self._create_response(
                error=f"Failed to configure online banking: {str(e)}",
                error_code="ONLINE_BANKING_CONFIG_ERROR"
            )