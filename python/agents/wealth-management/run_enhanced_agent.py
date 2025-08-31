#!/usr/bin/env python3
"""
Quick script to run the Enhanced Wealth Management Agent
Usage: uv run python run_enhanced_agent.py
"""

import asyncio
from wealth_management.enhanced_agent import enhanced_wealth_management_agent

async def main():
    """Interactive enhanced agent runner"""
    
    print("🎯 Enhanced Wealth Management Agent")
    print("=" * 50)
    print("Type your queries naturally - the agent will automatically route to appropriate workflows.")
    print("Examples:")
    print("  • 'Analyze client WM123456 behavior and predict future needs'")
    print("  • 'Prepare for quarterly review with client WM789012'")
    print("  • 'Respond to market volatility - high severity event'")
    print("  • 'Run compliance check for all portfolios'")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            query = input("\n💬 Your Query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            if not query:
                continue
                
            print(f"\n🔄 Processing: {query}")
            print("-" * 40)
            
            # Run the enhanced agent
            response = await enhanced_wealth_management_agent.run_async(query)
            
            print(f"📋 Response:\n{response}")
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())