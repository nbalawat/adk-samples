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
from .tools.analytics_service import (
    analyze_client_behavior,
    predict_client_needs,
    generate_investment_research
)
from .tools.regulatory_compliance_tools import (
    assess_fiduciary_compliance,
    generate_regulatory_report,
    monitor_regulatory_changes,
    conduct_aml_screening,
    generate_compliance_training
)
from .tools.client_experience_tools import (
    generate_personalized_communication,
    measure_client_satisfaction,
    orchestrate_client_journey,
    manage_client_events
)
from .tools.client_portfolio_analytics import (
    analyze_market_impact_across_clients,
    identify_enhancement_opportunities,
    analyze_client_help_desk_requests,
    generate_client_outreach_recommendations,
    suggest_personalized_materials
)

MODEL = "gemini-2.5-pro"

# Create the wealth management agent using standard ADK pattern
root_agent = Agent(
    name="wealth_management_agent",
    model=MODEL,
    description=(
        "Advanced wealth management agent supporting 33 specialized workflows across "
        "advisor, client, and operations use cases with comprehensive tool integration."
    ),
    instruction=prompt.ENHANCED_WEALTH_MANAGEMENT_PROMPT,
    tools=[
        # Portfolio tools
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
        
        # Memory tools
        remember_account,
        get_current_account,
        store_user_preference,
        get_user_preferences,
        store_conversation_context,
        get_conversation_context,
        initialize_user_session,
        get_session_summary,
        
        # Market intelligence tools
        analyze_market_volatility,
        generate_market_commentary,
        assess_portfolio_impact,
        create_comfort_call_scripts,
        trigger_proactive_outreach,
        
        # Crisis response tools
        initiate_emergency_protocol,
        provide_behavioral_coaching,
        prepare_scenario_analysis,
        coordinate_emergency_meeting,
        document_crisis_interaction,
        
        # Analytics service tools
        analyze_client_behavior,
        predict_client_needs,
        generate_investment_research,
        
        # Regulatory compliance tools
        assess_fiduciary_compliance,
        generate_regulatory_report,
        monitor_regulatory_changes,
        conduct_aml_screening,
        generate_compliance_training,
        
        # Client experience tools
        generate_personalized_communication,
        measure_client_satisfaction,
        orchestrate_client_journey,
        manage_client_events,
        
        # Client portfolio analytics tools
        analyze_market_impact_across_clients,
        identify_enhancement_opportunities,
        analyze_client_help_desk_requests,
        generate_client_outreach_recommendations,
        suggest_personalized_materials,
    ]
)