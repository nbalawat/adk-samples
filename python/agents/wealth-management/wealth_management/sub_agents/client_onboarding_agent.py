"""Client Onboarding Parallel Agent - Handles multiple onboarding tasks simultaneously."""

from google.adk import agents
from google.adk.agents import Agent
from google.adk.agents import callback_context as callback_context_module
from google.genai import types
from typing import Optional

from ..tools.client_onboarding_tools import (
    collect_kyc_information,
    assess_risk_tolerance,
    set_investment_goals,
    create_client_profile
)
from ..tools.memory_tools import (
    initialize_user_session,
    store_user_preference,
    store_conversation_context
)

MODEL = "gemini-2.5-pro"

# Onboarding callback functions
def initialize_onboarding(
    callback_context: callback_context_module.CallbackContext
) -> Optional[types.Content]:
    """Initialize client onboarding state."""
    callback_context.state["onboarding_started"] = True
    callback_context.state["onboarding_components"] = {
        "kyc_complete": False,
        "risk_assessment_complete": False,
        "goals_set": False,
        "profile_created": False
    }
    return None

def finalize_onboarding(
    callback_context: callback_context_module.CallbackContext
) -> Optional[types.Content]:
    """Finalize onboarding after all parallel tasks complete."""
    callback_context.state["onboarding_complete"] = True
    return None

# Parallel onboarding agents
kyc_collection_agent = Agent(
    name="kyc_collection_agent",
    model=MODEL,
    description="Collects Know Your Customer (KYC) information and documentation.",
    instruction="""You are a KYC compliance specialist. Your role is to:

1. Collect KYC information using collect_kyc_information tool
2. Ensure all regulatory requirements are met
3. Verify client identity and documentation
4. Store KYC data securely for compliance

Focus on thorough documentation and regulatory compliance.""",
    tools=[
        collect_kyc_information,
        store_conversation_context,
    ],
)

risk_assessment_agent = Agent(
    name="risk_assessment_agent",
    model=MODEL,
    description="Assesses client risk tolerance through questionnaires and analysis.",
    instruction="""You are a risk assessment specialist. Your role is to:

1. Assess client risk tolerance using assess_risk_tolerance tool
2. Conduct thorough risk questionnaire
3. Analyze client's investment experience and comfort level
4. Determine appropriate risk profile classification

Focus on accurate risk profiling to ensure suitable investment recommendations.""",
    tools=[
        assess_risk_tolerance,
        store_user_preference,
        store_conversation_context,
    ],
)

goal_setting_agent = Agent(
    name="goal_setting_agent",
    model=MODEL,
    description="Works with clients to establish investment goals and timelines.",
    instruction="""You are an investment goal specialist. Your role is to:

1. Set investment goals using set_investment_goals tool
2. Work with client to define financial objectives
3. Establish realistic timelines and milestones
4. Prioritize multiple goals if needed

Focus on creating SMART (Specific, Measurable, Achievable, Relevant, Time-bound) goals.""",
    tools=[
        set_investment_goals,
        store_user_preference,
        store_conversation_context,
    ],
)

profile_creation_agent = Agent(
    name="profile_creation_agent",
    model=MODEL,
    description="Creates comprehensive client profile integrating all onboarding information.",
    instruction="""You are a client profile specialist. Your role is to:

1. Create client profile using create_client_profile tool
2. Integrate KYC, risk assessment, and goal information
3. Ensure profile completeness and accuracy
4. Prepare profile for portfolio construction

Focus on creating a comprehensive, accurate client profile for investment management.""",
    tools=[
        create_client_profile,
        initialize_user_session,
        store_conversation_context,
    ],
)

# Main parallel agent for client onboarding
client_onboarding_parallel_agent = agents.ParallelAgent(
    name="client_onboarding_parallel_agent",
    description="Parallel execution of client onboarding tasks including KYC, risk assessment, goal setting, and profile creation.",
    sub_agents=[
        kyc_collection_agent,
        risk_assessment_agent,
        goal_setting_agent,
        profile_creation_agent,
    ],
    before_agent_callback=initialize_onboarding,
    after_agent_callback=finalize_onboarding,
)