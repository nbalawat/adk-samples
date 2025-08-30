"""Enhanced wealth management agent with ADK pattern support."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .tools.portfolio_tools import (
    get_portfolio_summary,
    get_position_details, 
    calculate_performance_metrics,
    generate_allocation_charts
)
from .tools.client_onboarding_tools import (
    collect_kyc_information,
    assess_risk_tolerance,
    set_investment_goals,
    create_client_profile
)
from .tools.goal_tracking_tools import (
    track_goal_progress,
    project_goal_timeline,
    suggest_goal_adjustments,
    calculate_required_savings
)
from .tools.memory_tools import (
    remember_account,
    get_current_account,
    store_user_preference,
    get_user_preferences,
    store_conversation_context,
    get_conversation_context,
    initialize_user_session,
    get_session_summary
)
from .tools.market_intelligence_tools import (
    analyze_market_volatility,
    generate_market_commentary,
    assess_portfolio_impact,
    create_comfort_call_scripts,
    trigger_proactive_outreach
)
from .tools.crisis_response_tools import (
    initiate_emergency_protocol,
    provide_behavioral_coaching,
    prepare_scenario_analysis,
    coordinate_emergency_meeting,
    document_crisis_interaction
)

# Import the sophisticated ADK pattern sub-agents
from .sub_agents.market_response_agent import market_response_agent
from .sub_agents.crisis_management_agent import crisis_management_agent
from .sub_agents.portfolio_monitoring_agent import portfolio_monitoring_loop_agent
from .sub_agents.client_onboarding_agent import client_onboarding_parallel_agent

MODEL = "gemini-2.5-pro"

# Enhanced orchestrator with both individual tools and sophisticated sub-agents
wealth_management_enhanced_orchestrator = Agent(
    name="wealth_management_enhanced_orchestrator",
    model=MODEL,
    description=(
        "Advanced wealth management platform supporting both granular tool-level operations "
        "and sophisticated multi-agent workflows using ADK Sequential, Parallel, and Loop patterns. "
        "Provides comprehensive coverage of 50+ wealth management workflows with intelligent routing."
    ),
    instruction="""You are an advanced wealth management orchestrator with two levels of operation:

## INDIVIDUAL TOOL OPERATIONS
For specific, targeted requests, use individual tools:
- Portfolio analysis: get_portfolio_summary, calculate_performance_metrics, etc.
- Client onboarding: collect_kyc_information, assess_risk_tolerance, etc.
- Goal management: track_goal_progress, suggest_goal_adjustments, etc.
- Market intelligence: analyze_market_volatility, generate_market_commentary, etc.
- Crisis response: initiate_emergency_protocol, provide_behavioral_coaching, etc.

## SOPHISTICATED WORKFLOW OPERATIONS  
For complex scenarios requiring coordinated workflows, use specialized sub-agents:

1. **Market Response Sequential Agent**: For comprehensive market volatility response
   - Use when: Market crashes, volatility events, broad client impact
   - Executes: Analysis → Commentary → Impact Assessment → Client Outreach

2. **Crisis Management Sequential Agent**: For emergency situations  
   - Use when: Client panic, liquidation threats, family emergencies, health crises
   - Executes: Emergency Protocol → Behavioral Coaching → Scenario Analysis → Documentation

3. **Portfolio Monitoring Loop Agent**: For continuous monitoring and analysis
   - Use when: Ongoing monitoring, goal tracking, performance review
   - Executes: Portfolio Analysis → Goal Tracking (with automatic iterations)

4. **Client Onboarding Parallel Agent**: For new client setup
   - Use when: New clients requiring complete onboarding  
   - Executes: KYC || Risk Assessment || Goal Setting || Profile Creation

## INTELLIGENT ROUTING LOGIC
- Single specific request → Use individual tools
- Complex multi-step workflow → Route to appropriate sub-agent
- Crisis situation → Crisis Management Sequential Agent  
- Market event → Market Response Sequential Agent
- New client → Client Onboarding Parallel Agent
- Monitoring request → Portfolio Monitoring Loop Agent

## CONTEXT MANAGEMENT
Always use memory tools to maintain conversation continuity:
- remember_account for client identification
- store_conversation_context for workflow state
- get_session_summary for comprehensive updates

Provide comprehensive responses that leverage both individual tools and sophisticated workflows as appropriate.""",
    
    output_key="enhanced_wealth_management_output",
    tools=[
        # Memory and context management tools
        remember_account,
        get_current_account,
        store_user_preference,
        get_user_preferences,
        store_conversation_context,
        get_conversation_context,
        initialize_user_session,
        get_session_summary,
        
        # Individual portfolio management tools
        get_portfolio_summary,
        get_position_details,
        calculate_performance_metrics,
        generate_allocation_charts,
        
        # Individual client onboarding tools
        collect_kyc_information,
        assess_risk_tolerance,
        set_investment_goals,
        create_client_profile,
        
        # Individual goal tracking tools
        track_goal_progress,
        project_goal_timeline,
        suggest_goal_adjustments,
        calculate_required_savings,
        
        # Individual market intelligence tools
        analyze_market_volatility,
        generate_market_commentary,
        assess_portfolio_impact,
        create_comfort_call_scripts,
        trigger_proactive_outreach,
        
        # Individual crisis response tools
        initiate_emergency_protocol,
        provide_behavioral_coaching,
        prepare_scenario_analysis,
        coordinate_emergency_meeting,
        document_crisis_interaction,
        
        # Sophisticated ADK pattern sub-agents
        AgentTool(market_response_agent),
        AgentTool(crisis_management_agent),
        AgentTool(portfolio_monitoring_loop_agent),
        AgentTool(client_onboarding_parallel_agent),
    ],
)

# Keep original agent for compatibility
wealth_management_orchestrator = Agent(
    name="wealth_management_orchestrator", 
    model=MODEL,
    description=(
        "Comprehensive wealth management platform orchestrating 50+ specialized agents "
        "to handle all interactions between advisors, clients, and operations teams. "
        "Provides intelligent routing and coordination across the entire wealth management ecosystem."
    ),
    instruction=prompt.WEALTH_MANAGEMENT_ORCHESTRATOR_PROMPT,
    output_key="wealth_management_output",
    tools=[
        # Memory and context management tools
        remember_account,
        get_current_account,
        store_user_preference,
        get_user_preferences,
        store_conversation_context,
        get_conversation_context,
        initialize_user_session,
        get_session_summary,
        
        # Portfolio management tools
        get_portfolio_summary,
        get_position_details,
        calculate_performance_metrics,
        generate_allocation_charts,
        
        # Client onboarding tools
        collect_kyc_information,
        assess_risk_tolerance,
        set_investment_goals,
        create_client_profile,
        
        # Goal tracking tools
        track_goal_progress,
        project_goal_timeline,
        suggest_goal_adjustments,
        calculate_required_savings,
        
        # Market Intelligence tools
        analyze_market_volatility,
        generate_market_commentary,
        assess_portfolio_impact,
        create_comfort_call_scripts,
        trigger_proactive_outreach,
        
        # Crisis Response tools
        initiate_emergency_protocol,
        provide_behavioral_coaching,
        prepare_scenario_analysis,
        coordinate_emergency_meeting,
        document_crisis_interaction,
    ],
)

# Use enhanced agent as root agent
root_agent = wealth_management_enhanced_orchestrator