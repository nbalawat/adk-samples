"""Main wealth management orchestrator agent"""

from google.adk.agents import Agent

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

MODEL = "gemini-2.5-pro"

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

root_agent = wealth_management_orchestrator