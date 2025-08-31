#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple test of the Enhanced Commercial Banking Onboarding System.
Tests core functionality without complex dependencies.
"""

import sys
import os
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set environment
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "1"
os.environ["GOOGLE_CLOUD_PROJECT"] = "agentic-experiments"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

def test_workflow_classification():
    """Test the workflow classification system."""
    print("🧠 Testing Workflow Classification System...")
    
    try:
        from commercial_banking_onboarding.shared_libraries.workflow_classifier import WorkflowClassifier
        
        classifier = WorkflowClassifier()
        
        # Test different queries
        test_queries = [
            "I want to open a business account for my LLC",
            "We need to process application CBO-123 urgently", 
            "Conduct compliance review for high-risk client",
            "Prepare legal documents for account opening"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n   Test {i}: {query[:50]}...")
            classification = classifier.classify_workflow(query)
            
            print(f"   → Persona: {classification['classification']['persona']}")
            print(f"   → Complexity: {classification['classification']['complexity']}")
            print(f"   → Pattern: {classification['routing']['recommended_pattern']}")
            print(f"   → Confidence: {classification['classification']['confidence_score']:.2f}")
        
        print("   ✅ Workflow Classification: SUCCESS")
        return True
        
    except Exception as e:
        print(f"   ❌ Workflow Classification: FAILED - {e}")
        return False

def test_memory_tools():
    """Test memory and context management tools."""
    print("\n💾 Testing Memory and Context Tools...")
    
    try:
        from commercial_banking_onboarding.tools.memory_tools import (
            remember_application, store_business_context, update_workflow_progress
        )
        
        # Mock tool context
        class MockToolContext:
            def __init__(self):
                self.state = {}
        
        context = MockToolContext()
        
        # Test application memory
        result1 = remember_application("TEST-APP-001", "Test Business LLC", context)
        assert result1['status'] == 'SUCCESS', "Application memory failed"
        
        # Test business context  
        business_data = {"industry": "Technology", "revenue": 1000000}
        result2 = store_business_context("business_info", business_data, context)
        assert result2['status'] == 'SUCCESS', "Business context failed"
        
        # Test workflow progress
        result3 = update_workflow_progress("kyc_verification", {"status": "completed"}, context)
        assert result3['status'] == 'SUCCESS', "Workflow progress failed"
        
        print("   ✅ Memory Tools: SUCCESS")
        return True
        
    except Exception as e:
        print(f"   ❌ Memory Tools: FAILED - {e}")
        return False

def test_mock_apis():
    """Test mock API functionality."""
    print("\n🔗 Testing Mock APIs...")
    
    try:
        from commercial_banking_onboarding.mock_apis.core_banking_api import MockCoreBankingAPI
        
        api = MockCoreBankingAPI()
        
        # Test product retrieval
        products_response = api.get_available_products()
        assert products_response.success, f"Products API failed: {products_response.error}"
        assert len(products_response.data['products']) > 0, "No products returned"
        
        # Test account creation
        business_info = {"legal_name": "Test Corp", "tax_id": "12-3456789"}
        account_response = api.create_business_account(
            "TEST-APP", business_info, ["BUS_CHK_BASIC"], 5000.0
        )
        assert account_response.success, f"Account creation failed: {account_response.error}"
        
        print("   ✅ Mock APIs: SUCCESS")
        return True
        
    except Exception as e:
        print(f"   ❌ Mock APIs: FAILED - {e}")
        return False

def test_orchestrator_tools():
    """Test orchestrator tools."""
    print("\n🎼 Testing Orchestrator Tools...")
    
    try:
        from commercial_banking_onboarding.tools.enhanced_orchestrator_tools import (
            create_onboarding_application, update_application_status, get_application_status
        )
        
        # Mock tool context
        class MockToolContext:
            def __init__(self):
                self.state = {}
        
        context = MockToolContext()
        
        # Test application creation
        result = create_onboarding_application(
            business_name="Test Business LLC",
            entity_type="LLC",
            tax_id="12-3456789", 
            business_address="123 Main St, City, ST 12345",
            beneficial_owners=[{"name": "John Doe", "ownership": 100}],
            requested_products=["business_checking"],
            tool_context=context
        )
        
        assert result['status'] == 'SUCCESS', f"Application creation failed: {result['message']}"
        app_id = result['application_id']
        
        # Test status update
        update_result = update_application_status(app_id, "kyc_verification", tool_context=context)
        assert update_result['status'] == 'SUCCESS', "Status update failed"
        
        # Test status retrieval  
        status_result = get_application_status(app_id, tool_context=context)
        assert status_result['status'] == 'SUCCESS', "Status retrieval failed"
        
        print("   ✅ Orchestrator Tools: SUCCESS")
        return True
        
    except Exception as e:
        print(f"   ❌ Orchestrator Tools: FAILED - {e}")
        return False

def test_client_tools():
    """Test client experience tools."""
    print("\n🤝 Testing Client Experience Tools...")
    
    try:
        from commercial_banking_onboarding.tools.client_experience_tools import (
            create_client_portal_access, generate_client_dashboard
        )
        
        # Mock tool context with application data
        class MockToolContext:
            def __init__(self):
                self.state = {
                    "applications": {
                        "TEST-APP": {
                            "business_information": {"legal_name": "Test Corp"},
                            "application_status": {
                                "current_stage": "kyc_verification",
                                "progress_percentage": 45,
                                "created_at": "2024-01-01T10:00:00Z"
                            },
                            "workflow_tracking": {"stages_completed": ["application_created"]}
                        }
                    }
                }
        
        context = MockToolContext()
        
        # Test portal creation
        portal_result = create_client_portal_access(
            "TEST-APP", "Test Corp", "ceo@testcorp.com", "John Smith", context
        )
        assert portal_result['status'] == 'SUCCESS', "Portal creation failed"
        
        # Test dashboard generation
        dashboard_result = generate_client_dashboard("TEST-APP", context)
        assert dashboard_result['status'] == 'SUCCESS', "Dashboard generation failed"
        
        print("   ✅ Client Experience Tools: SUCCESS")
        return True
        
    except Exception as e:
        print(f"   ❌ Client Experience Tools: FAILED - {e}")
        return False

def main():
    """Run all tests."""
    print("🏦 ENHANCED COMMERCIAL BANKING ONBOARDING - COMPONENT TESTS")
    print("="*60)
    
    tests = [
        test_workflow_classification,
        test_memory_tools,
        test_mock_apis,
        test_orchestrator_tools,
        test_client_tools
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"   💥 Test failed with exception: {e}")
    
    print(f"\n📊 TEST RESULTS")
    print("="*30)
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {passed/total:.1%}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is working correctly.")
        print("\n✅ Ready for:")
        print("   • Full agent orchestration testing")
        print("   • Cloud deployment")
        print("   • Production pilot")
        return True
    else:
        print(f"\n⚠️  {total-passed} tests failed. Please review and fix issues.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n💥 Test suite failed: {e}")
        sys.exit(1)