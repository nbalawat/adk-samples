#!/usr/bin/env python3
"""
Script to run the standard ADK Web UI for wealth management
Usage: uv run python run_adk_ui.py
"""

import subprocess
import sys
import os

def main():
    """Run the ADK Web UI"""
    
    print("🌐 Starting ADK Web UI for Wealth Management")
    print("=" * 50)
    print("This will start the standard ADK development interface")
    print("Navigate to the URL shown to interact with the agent")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Change to the wealth_management directory 
        os.chdir('wealth_management')
        
        # Run ADK web interface
        subprocess.run(['adk', 'web', '.'], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running ADK web: {e}")
        print("\n💡 Alternative: Try running directly with:")
        print("   cd wealth_management")  
        print("   adk web .")
    except KeyboardInterrupt:
        print("\n👋 ADK Web UI stopped")
    except FileNotFoundError:
        print("❌ ADK command not found. Make sure ADK is installed:")
        print("   pip install google-adk")

if __name__ == "__main__":
    main()