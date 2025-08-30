#!/usr/bin/env python3
"""Interactive session for Commercial Banking Onboarding application."""

import sys
import asyncio
import os
from pathlib import Path

# Add the project to path
sys.path.insert(0, str(Path(__file__).parent))

# Set up Vertex AI environment variables
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = '1'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'agentic-experiments'  
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'

from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent

class BankingChatSession:
    def __init__(self):
        self.session = None
        self.runner = None
        self.conversation_history = []
        
    async def initialize(self):
        """Initialize the banking application session."""
        print("🏦 COMMERCIAL BANKING ONBOARDING APPLICATION")
        print("="*60)
        print("Powered by Google ADK + Vertex AI")
        print("="*60)
        
        try:
            # Import the main orchestrator
            from commercial_banking_onboarding.agent import root_agent
            
            print("✅ Loading Commercial Banking Orchestrator...")
            print(f"   Agent: {root_agent.name}")
            print(f"   Model: {root_agent.model}")
            print(f"   Capabilities: {len(root_agent.tools)} banking tools available")
            
            # Setup session
            self.runner = InMemoryRunner(agent=root_agent)
            self.session = await self.runner.session_service.create_session(
                app_name=self.runner.app_name, 
                user_id="interactive_user"
            )
            
            print("✅ Session initialized successfully!")
            print("\n🎯 Available Services:")
            print("   🔍 KYC Identity Verification")
            print("   💰 Credit Assessment & Analysis")
            print("   ⚖️ Compliance & Sanctions Screening")
            print("   📄 Document Processing & Validation")
            print("   🏦 Account Creation & Setup")
            print("   🎭 Complete Onboarding Orchestration")
            
            print(f"\n💡 You can ask about:")
            print("   • Opening business accounts")
            print("   • Credit line applications")
            print("   • Account verification processes")
            print("   • Banking services setup")
            print("   • Compliance requirements")
            print("   • Document requirements")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize: {e}")
            return False
    
    async def send_message(self, message: str):
        """Send a message to the banking agent and get response."""
        if not self.session or not self.runner:
            print("❌ Session not initialized. Please restart the application.")
            return
        
        try:
            print(f"\n{'='*60}")
            print(f"🗣️  YOU: {message}")
            print(f"{'='*60}")
            
            content = UserContent(parts=[Part(text=message)])
            self.conversation_history.append(("User", message))
            
            print("🤖 Banking Agent is processing your request...")
            print("   (This may take 20-30 seconds for complex requests)")
            
            # Collect all response parts
            response_parts = []
            function_calls = []
            events_count = 0
            
            async for event in self.runner.run_async(
                user_id=self.session.user_id,
                session_id=self.session.id,
                new_message=content,
            ):
                events_count += 1
                print(f"   Processing... (Event {events_count})")
                
                if hasattr(event, 'message') and hasattr(event.message, 'content'):
                    for part in event.message.content.parts:
                        if hasattr(part, 'text') and part.text:
                            response_parts.append(part.text)
                        elif hasattr(part, 'function_call'):
                            function_calls.append(part.function_call.name)
                            print(f"   🔧 Executing: {part.function_call.name}")
                        elif hasattr(part, 'function_response'):
                            print(f"   ✅ Completed: {part.function_response.name}")
            
            # Display response
            if response_parts:
                full_response = "\n".join(response_parts)
                print(f"\n🏦 BANKING AGENT RESPONSE:")
                print("-" * 60)
                print(full_response)
                print("-" * 60)
                self.conversation_history.append(("Agent", full_response))
            else:
                print(f"\n🔧 AGENT ACTIVITY DETECTED:")
                print(f"   Events processed: {events_count}")
                print(f"   Functions executed: {len(function_calls)}")
                if function_calls:
                    print(f"   Tools used: {', '.join(set(function_calls))}")
                print(f"   ✅ Your request was processed by the banking system")
                print(f"   💡 The agent executed banking operations but didn't return text")
                print(f"   📞 In a real system, you'd receive confirmation via other channels")
        
        except Exception as e:
            print(f"❌ Error processing message: {e}")
    
    def show_conversation_history(self):
        """Display the conversation history."""
        if not self.conversation_history:
            print("📝 No conversation history yet.")
            return
            
        print(f"\n📝 CONVERSATION HISTORY:")
        print("="*50)
        for i, (speaker, message) in enumerate(self.conversation_history, 1):
            print(f"{i}. {speaker}: {message[:100]}{'...' if len(message) > 100 else ''}")
        print("="*50)
    
    def show_help(self):
        """Display help information."""
        print(f"\n💡 HELP - Available Commands:")
        print("="*40)
        print("📝 Just type your banking questions naturally!")
        print()
        print("🎯 Example questions you can ask:")
        print("   • 'I want to open a business account'")
        print("   • 'What documents do I need for onboarding?'")
        print("   • 'Can you verify my business identity?'")
        print("   • 'I need a $100,000 credit line'")
        print("   • 'Help me set up online banking'")
        print("   • 'What are your compliance requirements?'")
        print()
        print("🔧 Special commands:")
        print("   • 'help' - Show this help")
        print("   • 'history' - Show conversation history")
        print("   • 'quit' or 'exit' - End session")
        print("="*40)

async def run_interactive_session():
    """Run the interactive banking session."""
    
    banking_session = BankingChatSession()
    
    # Initialize
    if not await banking_session.initialize():
        print("Failed to start banking session. Please check your configuration.")
        return
    
    print(f"\n🚀 READY FOR QUESTIONS!")
    print("Type your banking questions below (or 'help' for guidance)")
    print("="*60)
    
    # Interactive loop
    while True:
        try:
            print(f"\n💬 Your message (or 'quit' to exit):")
            user_input = input("🗣️  ").strip()
            
            if not user_input:
                print("💡 Please enter a message or question.")
                continue
            
            # Handle special commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print(f"\n👋 Thank you for using Commercial Banking Onboarding!")
                print("Have a great day!")
                break
            elif user_input.lower() == 'help':
                banking_session.show_help()
                continue
            elif user_input.lower() == 'history':
                banking_session.show_conversation_history()
                continue
            
            # Send to banking agent
            await banking_session.send_message(user_input)
            
        except KeyboardInterrupt:
            print(f"\n\n👋 Session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Please try again or type 'quit' to exit.")

def main():
    """Main entry point."""
    print("Starting Commercial Banking Onboarding Interactive Session...")
    
    # Check environment
    required_vars = ['GOOGLE_APPLICATION_CREDENTIALS']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set up authentication before running.")
        return
    
    print("✅ Environment configured")
    
    # Run the session
    try:
        asyncio.run(run_interactive_session())
    except Exception as e:
        print(f"❌ Application error: {e}")
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    main()