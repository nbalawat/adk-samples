#!/usr/bin/env python3
"""
KICK-ASS DEMO SHOWCASE for ADK Wealth Management Platform
One-click demos that show off each sophisticated workflow pattern
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass

@dataclass 
class DemoScenario:
    name: str
    pattern: str
    description: str
    setup_prompt: str
    demo_prompts: List[str]
    expected_flow: List[str]
    wow_factor: str

# KICK-ASS DEMO SCENARIOS
DEMO_SCENARIOS = [
    DemoScenario(
        name="🚨 MARKET CRASH RESPONSE",
        pattern="Sequential Agent",
        description="Shows Sequential workflow handling market crisis from analysis to client outreach",
        setup_prompt="Remember account DEMO001 for our demo client.",
        demo_prompts=[
            "BREAKING: S&P 500 crashed 18% today! Execute complete market response workflow.",
            "I need comprehensive market analysis, commentary, portfolio impact assessment, and client outreach coordination."
        ],
        expected_flow=[
            "1️⃣ Market Analysis Agent: Analyzes 18% crash, identifies volatility events",
            "2️⃣ Market Commentary Agent: Creates client communications", 
            "3️⃣ Portfolio Impact Agent: Assesses client portfolio damage",
            "4️⃣ Client Outreach Agent: Coordinates proactive client contact"
        ],
        wow_factor="Shows systematic crisis response in 4 coordinated steps"
    ),
    
    DemoScenario(
        name="🆘 CLIENT PANIC MANAGEMENT", 
        pattern="Sequential Agent",
        description="Shows Crisis Management workflow handling client emotional crisis",
        setup_prompt="Client DEMO001 is our high-net-worth demonstration client with $3M portfolio.",
        demo_prompts=[
            "URGENT: Client is in full panic mode threatening to liquidate everything immediately!",
            "They're extremely emotional and irrational. Execute complete crisis management protocol."
        ],
        expected_flow=[
            "1️⃣ Emergency Protocol Agent: Activates crisis response procedures",
            "2️⃣ Behavioral Coaching Agent: Provides psychological intervention strategies",
            "3️⃣ Scenario Analysis Agent: Models liquidation consequences", 
            "4️⃣ Crisis Documentation Agent: Records everything + coordinates emergency meeting"
        ],
        wow_factor="Demonstrates professional crisis intervention with behavioral psychology"
    ),
    
    DemoScenario(
        name="👥 NEW CLIENT ONBOARDING",
        pattern="Parallel Agent", 
        description="Shows Parallel workflow processing multiple onboarding tasks simultaneously",
        setup_prompt="We have a new high-net-worth prospect ready for complete onboarding.",
        demo_prompts=[
            "New client wants comprehensive onboarding TODAY. Process everything simultaneously!",
            "Handle KYC documentation, risk assessment, investment goals, and profile creation in parallel."
        ],
        expected_flow=[
            "🔄 KYC Collection Agent || Risk Assessment Agent || Goal Setting Agent || Profile Creation Agent",
            "All 4 processes running simultaneously rather than sequentially",
            "Dramatic time savings through parallel processing",
            "Complete client profile ready in one coordinated workflow"
        ],
        wow_factor="Shows dramatic efficiency gains through parallel processing vs sequential"
    ),
    
    DemoScenario(
        name="🔄 PORTFOLIO MONITORING LOOP",
        pattern="Loop Agent",
        description="Shows Loop workflow with continuous monitoring until completion",
        setup_prompt="Account DEMO001 needs thorough ongoing analysis and monitoring.",
        demo_prompts=[
            "Start continuous portfolio monitoring for DEMO001. Keep analyzing until you find everything.",
            "Don't stop until you've completed a comprehensive assessment of portfolio and goals."
        ],
        expected_flow=[
            "🔄 Iteration 1: Portfolio Analysis → Goal Tracking",
            "🔄 Iteration 2: Deeper analysis → Goal progress assessment", 
            "🔄 Iteration 3: Final comprehensive review",
            "✅ Auto-termination when thorough analysis complete"
        ],
        wow_factor="Demonstrates intelligent looping with automatic completion logic"
    ),
    
    DemoScenario(
        name="🧠 MASTER ORCHESTRATION",
        pattern="Intelligent Routing",
        description="Shows Master Orchestrator routing complex scenarios to multiple workflows",
        setup_prompt="We have a complex situation requiring multiple coordinated responses.",
        demo_prompts=[
            "CRISIS SITUATION: Market crashed 20%, multiple clients panicking, and we have a new client wanting to onboard despite the chaos!",
            "I need comprehensive help with everything - market analysis, crisis management, client communications, AND new client onboarding."
        ],
        expected_flow=[
            "🧠 Master Orchestrator analyzes complex multi-faceted request",
            "🎯 Routes to Market Response Sequential Agent first",
            "🎯 Then triggers Crisis Management Sequential Agent", 
            "🎯 Coordinates with Client Onboarding Parallel Agent",
            "🔄 Intelligent workflow coordination and context management"
        ],
        wow_factor="Shows AI reasoning routing complex scenarios to multiple specialized workflows"
    )
]

def generate_demo_script():
    """Generate a comprehensive demo script."""
    
    script = f"""
# 🎬 KICK-ASS ADK WEALTH MANAGEMENT DEMO SCRIPT

## 🚀 PRE-DEMO SETUP (30 seconds)
1. Open terminal: `uv run adk web . --port 8080`
2. Open browser: http://localhost:8080/dev-ui/
3. Select "wealth-management" agent
4. Start new session
5. **READY TO ROCK!** 🎸

---

## 🎯 DEMO FLOW (5 minutes each scenario)

"""
    
    for i, scenario in enumerate(DEMO_SCENARIOS, 1):
        script += f"""
### DEMO {i}: {scenario.name}
**Pattern:** {scenario.pattern}
**Wow Factor:** {scenario.wow_factor}

**Setup** (say this first):
"{scenario.setup_prompt}"

**Demo Prompts** (paste these in order):
```
{scenario.demo_prompts[0]}
```

**Expected Flow to Highlight:**
{chr(10).join(scenario.expected_flow)}

**Key Points to Emphasize:**
- This is a {scenario.pattern} pattern in action
- Notice the {scenario.pattern.lower()} execution
- {scenario.wow_factor}

---
"""
    
    script += f"""
## 🎤 DEMO TALKING POINTS

### Opening Hook
"What you're about to see is a sophisticated AI agent system using Google's ADK with Sequential, Parallel, Loop, and Master Orchestration patterns to handle complex wealth management workflows."

### For Each Demo
- **Pattern Recognition**: "Notice how this uses [pattern] to..."
- **Professional Application**: "In real wealth management, this would..."
- **Technical Excellence**: "The AI is intelligently routing between..."

### Closing Impact
"This demonstrates enterprise-level AI orchestration solving real-world financial challenges with multiple coordinated agents working together."

## 🔥 BACKUP DEMOS (if something breaks)

### Quick Tool Demo
"Let me show you individual tools working..."
- "Remember account TEST001"
- "Get portfolio summary for this account" 
- "Analyze market volatility with 5% threshold"

### Pattern Explanation
"Each workflow uses different ADK patterns:
- **Sequential**: Step-by-step coordinated execution
- **Parallel**: Simultaneous task processing  
- **Loop**: Continuous monitoring with auto-completion
- **Orchestration**: Intelligent routing between workflows"

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    return script

def generate_demo_prompts():
    """Generate clean demo prompts for easy copy-paste."""
    
    prompts = {
        "setup_prompts": {},
        "demo_prompts": {}
    }
    
    for scenario in DEMO_SCENARIOS:
        key = scenario.name.replace("🚨 ", "").replace("🆘 ", "").replace("👥 ", "").replace("🔄 ", "").replace("🧠 ", "")
        prompts["setup_prompts"][key] = scenario.setup_prompt
        prompts["demo_prompts"][key] = scenario.demo_prompts
        
    return prompts

def create_demo_cheatsheet():
    """Create a demo cheatsheet for quick reference."""
    
    cheatsheet = f"""
# 🎯 DEMO CHEATSHEET - Quick Reference

## 🚀 ONE-LINER SETUP
```bash
uv run adk web . --port 8080
# Then: http://localhost:8080/dev-ui/ → wealth-management → new session
```

## 🎬 DEMO PROMPTS (Copy-Paste Ready)

### 1️⃣ MARKET CRASH (Sequential)
Setup: `Remember account DEMO001 for our demo client.`
Demo: `BREAKING: S&P 500 crashed 18% today! Execute complete market response workflow.`

### 2️⃣ CLIENT PANIC (Sequential)  
Setup: `Client DEMO001 is our high-net-worth demonstration client with $3M portfolio.`
Demo: `URGENT: Client is in full panic mode threatening to liquidate everything immediately!`

### 3️⃣ ONBOARDING (Parallel)
Setup: `We have a new high-net-worth prospect ready for complete onboarding.`
Demo: `New client wants comprehensive onboarding TODAY. Process everything simultaneously!`

### 4️⃣ MONITORING (Loop)
Setup: `Account DEMO001 needs thorough ongoing analysis and monitoring.`
Demo: `Start continuous portfolio monitoring for DEMO001. Keep analyzing until you find everything.`

### 5️⃣ ORCHESTRATION (Master)
Setup: `We have a complex situation requiring multiple coordinated responses.`
Demo: `CRISIS SITUATION: Market crashed 20%, multiple clients panicking, and we have a new client wanting to onboard despite the chaos!`

## 🎤 TALKING POINTS
- "Sequential agents execute steps in coordinated order"
- "Parallel agents process multiple tasks simultaneously" 
- "Loop agents continue until completion criteria met"
- "Master orchestrator routes intelligently between workflows"
- "This solves real wealth management challenges at scale"

## 🔧 BACKUP PLAN
If anything breaks, show individual tools:
- `Remember account TEST001`
- `Get portfolio summary for this account`
- `Analyze market volatility with 8% threshold`

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    return cheatsheet

def main():
    """Create kick-ass demo materials."""
    
    print("🎬 CREATING KICK-ASS DEMO MATERIALS")
    
    # Generate demo script
    demo_script = generate_demo_script()
    
    # Generate demo prompts
    demo_prompts = generate_demo_prompts()
    
    # Create demo cheatsheet
    demo_cheatsheet = create_demo_cheatsheet()
    
    # Save files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    script_file = f"demo_script_{timestamp}.md"
    with open(script_file, 'w') as f:
        f.write(demo_script)
    
    prompts_file = f"demo_prompts_{timestamp}.json"  
    with open(prompts_file, 'w') as f:
        json.dump(demo_prompts, f, indent=2)
    
    cheatsheet_file = f"demo_cheatsheet_{timestamp}.md"
    with open(cheatsheet_file, 'w') as f:
        f.write(demo_cheatsheet)
    
    print(f"✅ Demo script created: {script_file}")
    print(f"✅ Demo prompts created: {prompts_file}")
    print(f"✅ Demo cheatsheet created: {cheatsheet_file}")
    
    print(f"\n🎯 DEMO SUMMARY:")
    print(f"Total Demo Scenarios: {len(DEMO_SCENARIOS)}")
    print("1️⃣ Market Crash Response (Sequential)")
    print("2️⃣ Client Panic Management (Sequential)")  
    print("3️⃣ New Client Onboarding (Parallel)")
    print("4️⃣ Portfolio Monitoring Loop (Loop)")
    print("5️⃣ Master Orchestration (Intelligent Routing)")
    
    print(f"\n🚀 READY TO DEMO!")
    print("1. Start: uv run adk web . --port 8080")
    print("2. Navigate: http://localhost:8080/dev-ui/")
    print("3. Follow the cheatsheet for copy-paste prompts")
    print("4. Each demo takes ~2-3 minutes")
    print("5. Total demo time: ~15 minutes for all patterns")
    
    print(f"\n🎤 DEMO SELLING POINTS:")
    print("✅ Shows 4 different ADK patterns in action")
    print("✅ Realistic wealth management scenarios")  
    print("✅ Professional-grade AI orchestration")
    print("✅ Copy-paste prompts for smooth demo flow")
    print("✅ Backup options if anything breaks")
    print("✅ Clear talking points for technical audience")

if __name__ == "__main__":
    main()