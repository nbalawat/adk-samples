"""Portfolio Monitoring Loop Agent - Continuously monitors and analyzes portfolios."""

from google.adk import agents
from google.adk.agents import Agent
from google.adk.agents import callback_context as callback_context_module
from google.genai import types
from typing import Optional

from ..tools.portfolio_tools import (
    get_portfolio_summary,
    get_position_details,
    calculate_performance_metrics,
    generate_allocation_charts
)
from ..tools.goal_tracking_tools import (
    track_goal_progress,
    project_goal_timeline,
    suggest_goal_adjustments
)
from ..tools.memory_tools import (
    get_current_account,
    store_conversation_context
)

MODEL = "gemini-2.5-pro"

# Portfolio monitoring callback functions
def initialize_monitoring_loop(
    callback_context: callback_context_module.CallbackContext
) -> Optional[types.Content]:
    """Initialize monitoring loop state."""
    callback_context.state["monitoring_iteration"] = 0
    callback_context.state["portfolio_issues_found"] = []
    callback_context.state["goal_adjustments_needed"] = []
    return None

def check_monitoring_complete(
    callback_context: callback_context_module.CallbackContext
) -> Optional[types.Content]:
    """Check if monitoring cycle should continue."""
    iteration = callback_context.state.get("monitoring_iteration", 0)
    callback_context.state["monitoring_iteration"] = iteration + 1
    
    # Complete after thorough analysis
    issues_found = len(callback_context.state.get("portfolio_issues_found", []))
    if iteration >= 3 or issues_found == 0:  # Max 3 iterations or no issues
        callback_context.state["monitoring_complete"] = True
    
    return None

def update_monitoring_state(
    callback_context: callback_context_module.CallbackContext
) -> Optional[types.Content]:
    """Update monitoring state after each cycle."""
    callback_context.state["last_monitoring_update"] = "completed_cycle"
    return None

# Portfolio analysis agent (runs in loop)
portfolio_analysis_agent = Agent(
    name="portfolio_analysis_agent",
    model=MODEL,
    description="Comprehensive portfolio analysis including performance, allocation, and position details.",
    instruction="""You are a portfolio analyst. Your role is to:

1. Get portfolio summary using get_portfolio_summary tool
2. Calculate performance metrics using calculate_performance_metrics tool
3. Generate allocation charts using generate_allocation_charts tool
4. Identify any portfolio issues or opportunities
5. Store findings for goal tracking analysis

Conduct thorough analysis and identify areas needing attention.""",
    tools=[
        get_portfolio_summary,
        calculate_performance_metrics, 
        generate_allocation_charts,
        get_current_account,
        store_conversation_context,
    ],
    after_agent_callback=update_monitoring_state,
)

# Goal tracking agent (runs in loop)
goal_tracking_agent = Agent(
    name="goal_tracking_agent",
    model=MODEL,
    description="Tracks progress toward client goals and suggests adjustments as needed.",
    instruction="""You are a goal tracking specialist. Your role is to:

1. Track goal progress using track_goal_progress tool
2. Project goal timelines using project_goal_timeline tool  
3. Suggest goal adjustments using suggest_goal_adjustments tool if needed
4. Identify goals that may be at risk
5. Prepare recommendations for client discussions

Focus on proactive goal management and realistic timeline projections.""",
    tools=[
        track_goal_progress,
        project_goal_timeline,
        suggest_goal_adjustments,
        get_current_account,
        store_conversation_context,
    ],
)

# Sequential monitoring workflow (runs inside loop)
monitoring_workflow_agent = agents.SequentialAgent(
    name="portfolio_monitoring_workflow",
    description="Sequential workflow for portfolio analysis followed by goal tracking.",
    sub_agents=[
        portfolio_analysis_agent,
        goal_tracking_agent,
    ],
    after_agent_callback=check_monitoring_complete,
)

# Main loop agent for continuous portfolio monitoring
portfolio_monitoring_loop_agent = agents.LoopAgent(
    name="portfolio_monitoring_loop_agent", 
    description="Continuous monitoring loop for portfolio analysis and goal tracking with automatic completion.",
    sub_agents=[monitoring_workflow_agent],
    before_agent_callback=initialize_monitoring_loop,
    max_iterations=3,  # Reasonable limit for monitoring cycles
)