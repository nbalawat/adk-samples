#!/usr/bin/env python3
"""Simple test to verify agent invocation works."""

import sys
import asyncio
from pathlib import Path

# Add the project to path
sys.path.insert(0, str(Path(__file__).parent))

from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent

async def test_kyc_agent():
    """Test KYC agent with a simple request."""
    print("Testing KYC Agent Invocation...")
    
    from commercial_banking_onboarding.sub_agents.kyc_agent import kyc_agent
    
    simple_request = """
    Please verify the identity of a business:
    
    Business Name: Acme Corp
    Tax ID: 12-3456789
    Address: 123 Main St, San Francisco, CA 94102
    
    Please perform basic business identity verification and provide a summary.
    """
    
    try:
        runner = InMemoryRunner(agent=kyc_agent)
        session = await runner.session_service.create_session(
            app_name=runner.app_name, user_id="test_user"
        )
        content = UserContent(parts=[Part(text=simple_request)])
        
        print("Sending request to KYC agent...")
        response_text = ""
        
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
        ):
            print(f"Event type: {type(event)}")
            if hasattr(event, 'message'):
                print(f"Message: {event.message}")
                if hasattr(event.message, 'content'):
                    response_text += str(event.message.content)
        
        if response_text:
            print(f"\n✅ SUCCESS: KYC Agent responded!")
            print(f"Response length: {len(response_text)}")
            print(f"Response: {response_text[:300]}...")
        else:
            print("❌ No response received")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run the simple agent test."""
    print("SIMPLE AGENT INVOCATION TEST")
    print("="*50)
    
    success = await test_kyc_agent()
    
    if success:
        print("\n🎉 Agent invocation working!")
    else:
        print("\n❌ Agent invocation failed")

if __name__ == "__main__":
    asyncio.run(main())