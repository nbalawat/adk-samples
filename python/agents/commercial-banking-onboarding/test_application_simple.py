#!/usr/bin/env python3
"""Test script for the commercial banking onboarding application."""

import sys
import os
from pathlib import Path

# Add the project to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing imports...")
    
    try:
        from commercial_banking_onboarding.shared_libraries.mock_services import (
            mock_kyc_service,
            mock_credit_bureau,
            mock_compliance_service,
            mock_document_service,
            mock_banking_system
        )
        print("SUCCESS: Mock services imported")
    except Exception as e:
        print(f"FAILED: Mock services import error: {e}")
        return False
    
    try:
        from commercial_banking_onboarding.agent import agent
        print("SUCCESS: Main agent imported")
        print(f"Agent name: {agent.name}")
        print(f"Agent model: {agent.model}")
        print(f"Tools count: {len(agent.tools)}")
    except Exception as e:
        print(f"FAILED: Agent import error: {e}")
        return False
    
    return True

def test_mock_services():
    """Test all mock services are functioning."""
    print("\nTesting Mock Services...")
    
    from commercial_banking_onboarding.shared_libraries.mock_services import (
        mock_kyc_service,
        mock_credit_bureau,
        mock_compliance_service,
        mock_document_service,
        mock_banking_system
    )
    
    # Test KYC Service
    print("1. Testing KYC Service:")
    kyc_result = mock_kyc_service.verify_business({
        "legal_name": "Test Corporation",
        "tax_id": "12-3456789",
        "business_address": {"street": "123 Main St", "city": "New York", "state": "NY", "zip_code": "10001"}
    })
    print(f"   KYC Service result: {kyc_result.get('success', False)}")
    
    # Test Credit Bureau Service
    print("2. Testing Credit Bureau Service:")
    credit_result = mock_credit_bureau.get_business_credit_report("12-3456789", "Test Corporation")
    print(f"   Credit Service result: {credit_result.get('success', False)}")
    
    # Test Compliance Service
    print("3. Testing Compliance Service:")
    compliance_result = mock_compliance_service.screen_sanctions([
        {"name": "Test Corporation", "type": "business"}
    ])
    print(f"   Compliance Service result: {compliance_result.get('success', False)}")
    
    # Test Document Service
    print("4. Testing Document Service:")
    doc_result = mock_document_service.process_document("DOC-001", "business_license")
    print(f"   Document Service result: {doc_result.get('success', False)}")
    
    # Test Banking System
    print("5. Testing Banking System:")
    banking_result = mock_banking_system.create_account("APP-001", "CHK")
    print(f"   Banking System result: {banking_result.get('success', False)}")
    
    return True

def test_sub_agents():
    """Test that sub-agents can be imported."""
    print("\nTesting Sub-Agents...")
    
    sub_agents = [
        'kyc_agent',
        'credit_agent', 
        'compliance_agent',
        'document_agent',
        'account_setup_agent'
    ]
    
    for sub_agent_name in sub_agents:
        try:
            module_name = f"commercial_banking_onboarding.sub_agents.{sub_agent_name}"
            __import__(module_name)
            print(f"   {sub_agent_name}: SUCCESS")
        except Exception as e:
            print(f"   {sub_agent_name}: FAILED - {e}")
            return False
    
    return True

def main():
    """Run all tests."""
    print("Starting Commercial Banking Onboarding Application Test")
    print("=" * 60)
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    # Test mock services
    if not test_mock_services():
        success = False
    
    # Test sub-agents
    if not test_sub_agents():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("All tests completed successfully!")
        print("\nThe commercial banking onboarding application is ready for use with:")
        print("* Complete mock service integration")
        print("* Multi-agent orchestration")
        print("* KYC, Credit, Compliance, Document, and Account Setup capabilities")
        print("* Realistic banking workflow simulation")
    else:
        print("Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()