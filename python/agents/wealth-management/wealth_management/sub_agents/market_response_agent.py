"""Market Response Sequential Agent - Handles market volatility workflows systematically."""

from google.adk import agents
from google.adk.agents import Agent
from google.adk.agents import callback_context as callback_context_module
from google.genai import types
from typing import Optional

from ..tools.market_intelligence_tools import (
    analyze_market_volatility,
    generate_market_commentary,
    assess_portfolio_impact,
    create_comfort_call_scripts,
    trigger_proactive_outreach
)
from ..tools.memory_tools import (
    remember_account,
    get_current_account,
    store_conversation_context
)

MODEL = "gemini-2.5-pro"

# Sequential workflow for market response
def prepare_market_analysis(
    callback_context: callback_context_module.CallbackContext
) -> Optional[types.Content]:
    """Prepare market analysis state before sequential execution."""
    if "market_event_severity" not in callback_context.state:
        callback_context.state["market_event_severity"] = "moderate"
    if "client_segments_affected" not in callback_context.state:
        callback_context.state["client_segments_affected"] = ["conservative", "moderate"]
    return None

def store_analysis_results(
    callback_context: callback_context_module.CallbackContext
) -> Optional[types.Content]:
    """Store analysis results for next agent in sequence."""
    # Results automatically stored in state by tools
    callback_context.state["market_analysis_complete"] = True
    return None

def store_commentary_results(
    callback_context: callback_context_module.CallbackContext
) -> Optional[types.Content]:
    """Store commentary results for next agent in sequence."""
    callback_context.state["commentary_generated"] = True
    return None

def store_impact_results(
    callback_context: callback_context_module.CallbackContext
) -> Optional[types.Content]:
    """Store impact assessment results."""
    callback_context.state["impact_assessment_complete"] = True
    return None

def finalize_market_response(
    callback_context: callback_context_module.CallbackContext
) -> Optional[types.Content]:
    """Finalize market response workflow."""
    callback_context.state["market_response_workflow_complete"] = True
    return None

# Individual agents in the sequence
market_analysis_agent = Agent(
    name="market_analysis_agent",
    model=MODEL,
    description="Analyzes current market volatility and identifies key risk factors affecting client portfolios.",
    instruction="""You are a market volatility analyst. Your role is to:

1. Analyze current market conditions using the analyze_market_volatility tool
2. Identify volatility events and risk levels
3. Assess which client segments are most affected
4. Prepare context for portfolio impact assessment

Use the analyze_market_volatility tool with appropriate thresholds based on current market conditions.
Store findings in your analysis for the next agent in the workflow.""",
    tools=[
        analyze_market_volatility,
        store_conversation_context,
    ],
    before_agent_callback=prepare_market_analysis,
    after_agent_callback=store_analysis_results,
)

market_commentary_agent = Agent(
    name="market_commentary_agent", 
    model=MODEL,
    description="Generates customized market commentary and client communications based on market analysis.",
    instruction="""You are a market communications specialist. Your role is to:

1. Use market analysis results from the previous agent
2. Generate appropriate market commentary using generate_market_commentary tool
3. Create client-appropriate messaging based on volatility levels
4. Prepare communications for different client segments

Focus on clear, reassuring communication that addresses client concerns while maintaining professional credibility.""",
    tools=[
        generate_market_commentary,
        store_conversation_context,
    ],
    after_agent_callback=store_commentary_results,
)

portfolio_impact_agent = Agent(
    name="portfolio_impact_agent",
    model=MODEL,
    description="Assesses portfolio-specific impacts and creates action plans for client protection.",
    instruction="""You are a portfolio risk analyst. Your role is to:

1. Use market analysis to assess portfolio impacts using assess_portfolio_impact tool
2. Determine which clients need immediate attention
3. Identify portfolio adjustments or protective measures needed
4. Prepare data for client outreach coordination

Focus on quantifying risks and recommending specific protective actions.""",
    tools=[
        assess_portfolio_impact,
        get_current_account,
        store_conversation_context,
    ],
    after_agent_callback=store_impact_results,
)

client_outreach_agent = Agent(
    name="client_outreach_agent",
    model=MODEL, 
    description="Coordinates proactive client outreach and creates comfort call scripts.",
    instruction="""You are a client relationship coordinator. Your role is to:

1. Based on previous analysis, trigger proactive outreach using trigger_proactive_outreach tool
2. Create comfort call scripts using create_comfort_call_scripts tool
3. Coordinate timing and prioritization of client communications
4. Ensure all affected clients receive appropriate contact

Focus on maintaining client confidence and providing clear next steps.""",
    tools=[
        trigger_proactive_outreach,
        create_comfort_call_scripts,
        store_conversation_context,
    ],
    after_agent_callback=finalize_market_response,
)

# Main sequential agent that orchestrates the market response workflow
market_response_agent = agents.SequentialAgent(
    name="market_response_sequential_agent",
    description="Complete market response workflow handling volatility analysis, communication, and client outreach in sequence.",
    sub_agents=[
        market_analysis_agent,
        market_commentary_agent,
        portfolio_impact_agent,
        client_outreach_agent,
    ],
)