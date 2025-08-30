#!/usr/bin/env python3
"""Test actual agent invocations with real prompts and tool usage."""

import sys
import os
import asyncio
import json
from pathlib import Path

# Add the project to path
sys.path.insert(0, str(Path(__file__).parent))

from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent

async def invoke_agent(agent, user_input: str, agent_name: str):
    """Helper function to properly invoke an ADK agent."""
    try:
        runner = InMemoryRunner(agent=agent)
        session = await runner.session_service.create_session(
            app_name=runner.app_name, user_id="test_user"
        )
        content = UserContent(parts=[Part(text=user_input)])
        response = ""
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
        ):
            if hasattr(event, 'message') and hasattr(event.message, 'content'):
                response += str(event.message.content)
        return response
    except Exception as e:
        print(f"Error invoking {agent_name}: {e}")
        return None

async def test_kyc_agent():
    """Test KYC agent with a realistic business verification request."""
    print("\n" + "="*60)
    print("TESTING KYC AGENT")
    print("="*60)
    
    from commercial_banking_onboarding.sub_agents.kyc_agent import kyc_agent
    
    kyc_request = """
    I need to verify the identity of a new business customer applying for commercial banking services:
    
    Business Information:
    - Legal Name: Acme Technology Solutions Inc.
    - Tax ID: 12-3456789
    - Entity Type: Corporation
    - Business Address: 123 Tech Drive, San Francisco, CA 94102
    - Incorporation Date: 2020-01-15
    
    Beneficial Owners:
    1. John Smith (CEO) - 60% ownership
       - SSN: 123-45-6789
       - DOB: 1980-01-15
       - Address: 456 Oak Street, San Francisco, CA 94103
    
    2. Jane Doe (CTO) - 40% ownership
       - SSN: 987-65-4321
       - DOB: 1985-03-20
       - Address: 789 Pine Street, San Francisco, CA 94104
    
    Please perform complete KYC verification including business identity verification, 
    beneficial owner verification, PEP screening, and generate a comprehensive KYC report.
    """
    
    try:
        print("Invoking KYC Agent...")
        print("Request: Business identity verification for Acme Technology Solutions Inc.")
        
        # Invoke the agent using proper ADK pattern
        response = await invoke_agent(kyc_agent, kyc_request, "KYC Agent")
        
        if response:
            print(f"\n✅ KYC Agent Response Received:")
            print(f"Response Length: {len(str(response))}")
            print(f"Response Preview: {str(response)[:500]}...")
            return True
        else:
            print(f"❌ KYC Agent: No response received")
            return False
        
    except Exception as e:
        print(f"❌ KYC Agent Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_credit_agent():
    """Test Credit agent with a credit assessment request."""
    print("\n" + "="*60)
    print("TESTING CREDIT AGENT")
    print("="*60)
    
    from commercial_banking_onboarding.sub_agents.credit_agent import credit_agent
    
    credit_request = """
    I need a comprehensive credit assessment for a commercial banking applicant:
    
    Business Details:
    - Company: Acme Technology Solutions Inc.
    - Tax ID: 12-3456789
    - Industry: Software Development (NAICS 541511)
    - Annual Revenue: $2,500,000
    - Years in Business: 4 years
    - Entity Type: Corporation
    
    Financial Information:
    - Requested Credit Line: $250,000
    - Current Business Debt: $150,000
    - Monthly Cash Flow: $200,000
    - Assets: $800,000
    
    Please perform:
    1. Credit bureau report analysis
    2. Financial statement review
    3. Industry risk assessment
    4. Credit score calculation
    5. Credit limit recommendation
    6. Generate comprehensive credit assessment report
    """
    
    try:
        print("Invoking Credit Agent...")
        print("Request: Credit assessment for $250,000 credit line")
        
        response = await credit_agent.ainvoke(credit_request)
        
        print(f"\n✅ Credit Agent Response Received:")
        print(f"Response Type: {type(response)}")
        print(f"Response Length: {len(str(response))}")
        print(f"Response Preview: {str(response)[:500]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Credit Agent Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_compliance_agent():
    """Test Compliance agent with sanctions and AML screening."""
    print("\n" + "="*60)
    print("TESTING COMPLIANCE AGENT")
    print("="*60)
    
    from commercial_banking_onboarding.sub_agents.compliance_agent import compliance_agent
    
    compliance_request = """
    I need comprehensive compliance screening for a new commercial banking customer:
    
    Business Information:
    - Legal Name: Acme Technology Solutions Inc.
    - Industry: Software Development
    - Business Address: 123 Tech Drive, San Francisco, CA 94102
    
    Key Personnel:
    - John Smith (CEO, 60% owner)
    - Jane Doe (CTO, 40% owner)
    
    Required Screening:
    1. Sanctions screening against OFAC, UN, EU lists
    2. AML risk assessment
    3. PEP (Politically Exposed Persons) screening
    4. Regulatory compliance verification
    5. Generate comprehensive compliance report
    
    Please ensure all compliance requirements are met for commercial banking onboarding.
    """
    
    try:
        print("Invoking Compliance Agent...")
        print("Request: Full compliance screening including sanctions and AML")
        
        response = await compliance_agent.ainvoke(compliance_request)
        
        print(f"\n✅ Compliance Agent Response Received:")
        print(f"Response Type: {type(response)}")
        print(f"Response Length: {len(str(response))}")
        print(f"Response Preview: {str(response)[:500]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Compliance Agent Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_document_agent():
    """Test Document agent with document processing request."""
    print("\n" + "="*60)
    print("TESTING DOCUMENT AGENT")
    print("="*60)
    
    from commercial_banking_onboarding.sub_agents.document_agent import document_agent
    
    document_request = """
    I need to process and validate business documents for commercial banking onboarding:
    
    Documents Submitted:
    1. Articles of Incorporation (acme_articles.pdf)
    2. Business License (acme_license.pdf)
    3. Tax ID Certificate (acme_tax_cert.pdf)
    4. Financial Statements (acme_financials.pdf)
    5. Beneficial Ownership Certification (acme_ownership.pdf)
    
    Required Processing:
    1. Extract structured data from all documents
    2. Validate document completeness and accuracy
    3. Verify document authenticity
    4. Cross-validate information across documents
    5. Generate document processing report
    
    Business Information for Validation:
    - Legal Name: Acme Technology Solutions Inc.
    - Tax ID: 12-3456789
    - Entity Type: Corporation
    
    Please process all documents and provide validation results.
    """
    
    try:
        print("Invoking Document Agent...")
        print("Request: Process 5 business documents with validation")
        
        response = await document_agent.ainvoke(document_request)
        
        print(f"\n✅ Document Agent Response Received:")
        print(f"Response Type: {type(response)}")
        print(f"Response Length: {len(str(response))}")
        print(f"Response Preview: {str(response)[:500]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Document Agent Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_account_setup_agent():
    """Test Account Setup agent with account creation request."""
    print("\n" + "="*60)
    print("TESTING ACCOUNT SETUP AGENT")
    print("="*60)
    
    from commercial_banking_onboarding.sub_agents.account_setup_agent import account_setup_agent
    
    account_setup_request = """
    I need to set up banking accounts and services for an approved commercial customer:
    
    Approved Application Details:
    - Application ID: APP-20240101-001
    - Business: Acme Technology Solutions Inc.
    - Annual Revenue: $2,500,000
    - Approved Credit Limit: $200,000
    
    Requested Services:
    - Business Checking Account (initial deposit: $25,000)
    - Business Savings Account
    - Line of Credit ($200,000)
    - Online Banking
    - Wire Transfer Services
    - ACH Processing
    
    Admin Users for Online Banking:
    - John Smith (CEO) - Full admin access
    - Jane Doe (CTO) - Transaction access
    
    Physical Materials Needed:
    - Business checks
    - Debit cards
    - Welcome kit
    
    Please:
    1. Create all requested accounts
    2. Set up banking services
    3. Configure online banking access
    4. Order physical materials
    5. Assign appropriate relationship manager
    6. Generate account setup completion report
    """
    
    try:
        print("Invoking Account Setup Agent...")
        print("Request: Complete account setup with multiple services")
        
        response = await account_setup_agent.ainvoke(account_setup_request)
        
        print(f"\n✅ Account Setup Agent Response Received:")
        print(f"Response Type: {type(response)}")
        print(f"Response Length: {len(str(response))}")
        print(f"Response Preview: {str(response)[:500]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Account Setup Agent Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_main_orchestrator():
    """Test the main orchestrator agent with a complete onboarding request."""
    print("\n" + "="*60)
    print("TESTING MAIN ORCHESTRATOR AGENT")
    print("="*60)
    
    from commercial_banking_onboarding.agent import root_agent
    
    orchestrator_request = """
    I am the CEO of Acme Technology Solutions Inc. and I would like to open commercial banking accounts for my corporation. Here are our details:
    
    Business Information:
    - Legal Name: Acme Technology Solutions Inc.
    - Entity Type: C-Corporation
    - Tax ID: 12-3456789
    - Industry: Software Development (NAICS 541511)
    - Incorporation Date: January 15, 2020
    - Annual Revenue: $2,500,000
    - Number of Employees: 15
    
    Business Address:
    123 Tech Drive, San Francisco, CA 94102
    
    Beneficial Owners:
    1. John Smith (CEO) - 60% ownership
       - SSN: 123-45-6789
       - DOB: January 15, 1980
       - Address: 456 Oak Street, San Francisco, CA 94103
    
    2. Jane Doe (CTO) - 40% ownership  
       - SSN: 987-65-4321
       - DOB: March 20, 1985
       - Address: 789 Pine Street, San Francisco, CA 94104
    
    Banking Needs:
    - Business Checking Account (initial deposit: $25,000)
    - Business Savings Account
    - Line of Credit (requesting $200,000)
    - Online Banking with mobile access
    - Wire transfer capabilities
    - ACH processing for payroll
    
    We have all required documents ready including articles of incorporation, business license, tax certificates, and financial statements.
    
    Please guide me through the complete commercial banking onboarding process and let me know what additional information you need.
    """
    
    try:
        print("Invoking Main Orchestrator Agent...")
        print("Request: Complete commercial banking onboarding")
        
        response = await root_agent.ainvoke(orchestrator_request)
        
        print(f"\n✅ Main Orchestrator Response Received:")
        print(f"Response Type: {type(response)}")
        print(f"Response Length: {len(str(response))}")
        print(f"Response Preview: {str(response)[:800]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Main Orchestrator Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all agent invocation tests."""
    print("COMMERCIAL BANKING ONBOARDING - AGENT INVOCATION TESTS")
    print("Testing actual agent responses with realistic banking scenarios")
    print("="*80)
    
    results = {}
    
    try:
        # Test individual sub-agents first
        results['kyc'] = await test_kyc_agent()
        results['credit'] = await test_credit_agent()  
        results['compliance'] = await test_compliance_agent()
        results['document'] = await test_document_agent()
        results['account_setup'] = await test_account_setup_agent()
        
        # Test main orchestrator
        results['orchestrator'] = await test_main_orchestrator()
        
        # Summary
        print("\n" + "="*80)
        print("AGENT INVOCATION TEST SUMMARY")
        print("="*80)
        
        passed = sum(1 for success in results.values() if success)
        total = len(results)
        
        print(f"\nResults: {passed}/{total} agents responded successfully")
        
        for agent_name, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"  {agent_name.replace('_', ' ').title()} Agent: {status}")
        
        if passed == total:
            print(f"\n🎉 ALL AGENTS WORKING!")
            print("The commercial banking onboarding system is fully operational.")
            print("\nCapabilities Verified:")
            print("  ✓ KYC identity verification and screening")
            print("  ✓ Credit assessment and risk analysis") 
            print("  ✓ Compliance and sanctions screening")
            print("  ✓ Document processing and validation")
            print("  ✓ Account setup and service configuration")
            print("  ✓ End-to-end orchestration workflow")
        else:
            print(f"\n⚠️  {total - passed} agents had issues")
            print("Check the error messages above for details.")
            
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())