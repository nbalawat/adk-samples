#!/usr/bin/env python3
"""Test agents with proper Vertex AI initialization."""

import sys
import asyncio
import os
from pathlib import Path

# Add the project to path
sys.path.insert(0, str(Path(__file__).parent))

import vertexai
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent

async def test_agent_with_vertexai():
    """Test agent with proper Vertex AI setup."""
    print("COMMERCIAL BANKING AGENTS - VERTEX AI TEST")
    print("="*60)
    
    # Initialize Vertex AI
    project_id = "agentic-experiments"
    location = "us-central1"
    
    print(f"Initializing Vertex AI...")
    print(f"Project: {project_id}")
    print(f"Location: {location}")
    
    vertexai.init(project=project_id, location=location)
    
    # Test KYC Agent
    print(f"\nTesting KYC Agent...")
    
    from commercial_banking_onboarding.sub_agents.kyc_agent import kyc_agent
    
    kyc_request = """
    Please verify this business:
    - Business Name: Acme Technology Solutions Inc
    - Tax ID: 12-3456789
    - Address: 123 Tech Drive, San Francisco, CA 94102
    
    Perform basic identity verification and provide a brief summary.
    """
    
    try:
        runner = InMemoryRunner(agent=kyc_agent)
        session = await runner.session_service.create_session(
            app_name=runner.app_name, user_id="test_user"
        )
        content = UserContent(parts=[Part(text=kyc_request)])
        
        response_text = ""
        message_count = 0
        
        print("Sending request to KYC agent...")
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
        ):
            message_count += 1
            print(f"Event #{message_count}: {type(event).__name__}")
            
            # Try to extract response content
            if hasattr(event, 'message') and hasattr(event.message, 'content'):
                content_str = str(event.message.content)
                response_text += content_str
                print(f"Content: {content_str[:100]}...")
            elif hasattr(event, 'content'):
                content_str = str(event.content)
                response_text += content_str
                print(f"Content: {content_str[:100]}...")
        
        print(f"\n✅ KYC Agent Test Results:")
        print(f"Events received: {message_count}")
        print(f"Response length: {len(response_text)}")
        
        if response_text.strip():
            print(f"Response preview:")
            print("-" * 40)
            print(response_text[:800])
            print("-" * 40)
            return True
        else:
            print("No response content extracted")
            return False
            
    except Exception as e:
        print(f"❌ KYC Agent Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run the agent test."""
    success = await test_agent_with_vertexai()
    
    if success:
        print(f"\n🎉 SUCCESS! Agent responded successfully!")
        print("The commercial banking agents are working with Vertex AI.")
    else:
        print(f"\n❌ Test failed - see error details above")

if __name__ == "__main__":
    asyncio.run(main())