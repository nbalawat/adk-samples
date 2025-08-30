"""Master Orchestrator Agent - Coordinates all wealth management workflows using ADK patterns."""

from google.adk import agents
from google.adk.agents import Agent
from google.adk.agents import callback_context as callback_context_module
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
from typing import Optional

from .market_response_agent import market_response_agent
from .crisis_management_agent import crisis_management_agent  
from .portfolio_monitoring_agent import portfolio_monitoring_loop_agent
from .client_onboarding_agent import client_onboarding_parallel_agent

from ..tools.memory_tools import (
    remember_account,
    get_current_account,
    store_conversation_context,
    get_session_summary
)

MODEL = "gemini-2.5-pro"

# Orchestration callback functions
def analyze_request_intent(
    callback_context: callback_context_module.CallbackContext
) -> Optional[types.Content]:
    """Analyze user request to determine appropriate workflow."""
    # This would contain logic to classify user intent
    callback_context.state["workflow_classification"] = "pending"
    return None

def route_to_appropriate_workflow(
    callback_context: callback_context_module.CallbackContext
) -> Optional[types.Content]:
    """Route to appropriate sub-agent workflow based on intent analysis."""
    callback_context.state["workflow_routed"] = True
    return None

def finalize_orchestration(
    callback_context: callback_context_module.CallbackContext
) -> Optional[types.Content]:
    """Finalize orchestration and prepare response."""
    callback_context.state["orchestration_complete"] = True
    return None

# Main orchestrator agent with intelligent routing
wealth_management_master_orchestrator = Agent(
    name="wealth_management_master_orchestrator",
    model=MODEL,
    description="""
    Master orchestrator for comprehensive wealth management platform coordinating specialized 
    sub-agent workflows using ADK Sequential, Parallel, and Loop patterns. Routes requests 
    to appropriate specialized workflows based on intent analysis.
    """,
    instruction="""You are the master orchestrator for a comprehensive wealth management platform. Your role is to:

WORKFLOW ROUTING INTELLIGENCE:
1. Analyze incoming requests to determine the most appropriate workflow
2. Route to specialized sub-agents based on request type:
   - Market volatility/correction concerns → Market Response Sequential Agent
   - Client panic/crisis situations → Crisis Management Sequential Agent  
   - Portfolio analysis/monitoring → Portfolio Monitoring Loop Agent
   - New client setup → Client Onboarding Parallel Agent

AVAILABLE SUB-AGENT WORKFLOWS:
1. **Market Response Agent** (Sequential): Handles market volatility analysis → commentary → impact assessment → client outreach
2. **Crisis Management Agent** (Sequential): Handles emergency protocols → behavioral coaching → scenario analysis → documentation
3. **Portfolio Monitoring Agent** (Loop): Continuously monitors portfolios and tracks goals with automatic completion
4. **Client Onboarding Agent** (Parallel): Simultaneously handles KYC, risk assessment, goals, and profile creation

ORCHESTRATION PRINCIPLES:
- Use context and memory tools to maintain conversation continuity
- Route requests intelligently based on keywords and intent
- Coordinate between workflows when multiple are needed
- Provide comprehensive responses integrating results from sub-agents

EXAMPLE ROUTING LOGIC:
- "The market crashed today" → Market Response Agent → Crisis Management Agent if severe
- "I want to sell everything" → Crisis Management Agent
- "How is my portfolio doing?" → Portfolio Monitoring Agent  
- "I'm a new client" → Client Onboarding Agent

Always start by remembering the client account and understanding their context before routing to appropriate workflows.""",
    
    tools=[
        # Memory and context management
        remember_account,
        get_current_account,
        store_conversation_context,
        get_session_summary,
        
        # Sub-agent workflow tools
        AgentTool(market_response_agent),
        AgentTool(crisis_management_agent),
        AgentTool(portfolio_monitoring_loop_agent),
        AgentTool(client_onboarding_parallel_agent),
    ],
    
    before_agent_callback=analyze_request_intent,
    after_agent_callback=finalize_orchestration,
)

# Export the main orchestrator
root_agent = wealth_management_master_orchestrator