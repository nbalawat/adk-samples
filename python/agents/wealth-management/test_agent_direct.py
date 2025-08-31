#!/usr/bin/env python3
"""
Direct test of the wealth management agent
"""

import asyncio
from wealth_management.agent import root_agent

async def test_agent():
    """Test the agent directly"""
    
    print("🧪 Testing Wealth Management Agent directly...")
    
    try:
        # Test basic portfolio query
        print("Sending query: 'Can you show me a portfolio summary for client WM123456?'")
        
        response_parts = []
        async for event in root_agent.run_async("Can you show me a portfolio summary for client WM123456?"):
            print(f"Event type: {type(event)}")
            response_parts.append(str(event))
            
        print("✅ Agent Response:")
        print("\n".join(response_parts[-5:]))  # Show last 5 parts
        return True
        
    except Exception as e:
        print(f"❌ Agent Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_agent())
    if success:
        print("\n🎉 Agent is working properly!")
    else:
        print("\n💥 Agent has issues!")