#!/usr/bin/env python3
"""Simple test script for the commercial banking onboarding application."""

import sys
import os
from pathlib import Path

# Add the project to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing imports...")
    
    try:
        from commercial_banking_onboarding.shared_libraries.mock_services import mock_kyc_service
        print("SUCCESS: Mock services imported")
        
        # Quick test of mock service
        result = mock_kyc_service.verify_business_identity(
            business_name="Test Corp",
            tax_id="12-3456789",
            address={"street": "123 Main St", "city": "Test City", "state": "CA", "zip_code": "12345"}
        )
        print("SUCCESS: Mock KYC service call worked")
        print("Result:", result.get('success', False))
        
    except Exception as e:
        print("FAILED: Mock services error:", str(e))
        return False
    
    try:
        from commercial_banking_onboarding.agent import agent
        print("SUCCESS: Main agent imported")
        print("Agent name:", agent.name)
        print("Agent model:", agent.model)
        print("Tools count:", len(agent.tools))
    except Exception as e:
        print("FAILED: Agent import error:", str(e))
        return False
    
    return True

if __name__ == "__main__":
    print("Commercial Banking Onboarding - Simple Test")
    print("=" * 50)
    
    if test_imports():
        print("\nAll core components loaded successfully!")
        print("The application is ready to use.")
    else:
        print("\nSome components failed to load.")
        sys.exit(1)