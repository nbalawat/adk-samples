"""Crisis Management Sequential Agent - Handles emergency situations with systematic response."""

from google.adk import agents
from google.adk.agents import Agent
from google.adk.agents import callback_context as callback_context_module
from google.genai import types
from typing import Optional

from ..tools.crisis_response_tools import (
    initiate_emergency_protocol,
    provide_behavioral_coaching,
    prepare_scenario_analysis,
    coordinate_emergency_meeting,
    document_crisis_interaction
)
from ..tools.memory_tools import (
    get_current_account,
    store_conversation_context
)

MODEL = "gemini-2.5-pro"

# Crisis management callback functions
def initialize_crisis_state(
    callback_context: callback_context_module.CallbackContext
) -> Optional[types.Content]:
    """Initialize crisis management state."""
    if "crisis_severity" not in callback_context.state:
        callback_context.state["crisis_severity"] = "high"
    if "crisis_type" not in callback_context.state:
        callback_context.state["crisis_type"] = "market_crash"
    callback_context.state["crisis_response_started"] = True
    return None

def escalate_if_needed(
    callback_context: callback_context_module.CallbackContext
) -> Optional[types.Content]:
    """Check if crisis needs escalation after protocol initiation."""
    # Logic to determine if escalation is needed
    callback_context.state["protocol_initiated"] = True
    return None

def prepare_coaching_context(
    callback_context: callback_context_module.CallbackContext
) -> Optional[types.Content]:
    """Prepare context for behavioral coaching."""
    callback_context.state["coaching_prepared"] = True
    return None

def prepare_scenario_context(
    callback_context: callback_context_module.CallbackContext
) -> Optional[types.Content]:
    """Prepare context for scenario analysis."""
    callback_context.state["scenario_analysis_ready"] = True
    return None

def finalize_crisis_response(
    callback_context: callback_context_module.CallbackContext
) -> Optional[types.Content]:
    """Finalize crisis response workflow."""
    callback_context.state["crisis_response_complete"] = True
    return None

# Crisis management sub-agents
emergency_protocol_agent = Agent(
    name="emergency_protocol_agent",
    model=MODEL,
    description="Initiates emergency protocols based on crisis type and severity.",
    instruction="""You are an emergency response coordinator. Your role is to:

1. Assess the crisis situation and determine appropriate response level
2. Initiate emergency protocol using initiate_emergency_protocol tool
3. Identify required immediate actions and stakeholders
4. Set up framework for coordinated response

Focus on speed and accuracy in crisis assessment and protocol activation.""",
    tools=[
        initiate_emergency_protocol,
        store_conversation_context,
    ],
    before_agent_callback=initialize_crisis_state,
    after_agent_callback=escalate_if_needed,
)

behavioral_coaching_agent = Agent(
    name="behavioral_coaching_agent",
    model=MODEL,
    description="Provides behavioral coaching strategies for managing client emotional responses during crisis.",
    instruction="""You are a behavioral finance specialist. Your role is to:

1. Analyze client emotional state and market conditions
2. Provide behavioral coaching using provide_behavioral_coaching tool
3. Develop strategies to prevent panic-driven decisions
4. Prepare guidance for advisor-client interactions

Focus on evidence-based psychological techniques to maintain client stability.""",
    tools=[
        provide_behavioral_coaching,
        store_conversation_context,
    ],
    before_agent_callback=prepare_coaching_context,
)

scenario_analysis_agent = Agent(
    name="scenario_analysis_agent", 
    model=MODEL,
    description="Prepares detailed scenario analysis for different crisis outcomes and client decisions.",
    instruction="""You are a scenario modeling specialist. Your role is to:

1. Model different crisis scenarios and outcomes
2. Prepare scenario analysis using prepare_scenario_analysis tool
3. Quantify impacts of various client decisions
4. Provide data-driven insights for crisis management

Focus on helping clients understand consequences of different actions.""",
    tools=[
        prepare_scenario_analysis,
        get_current_account,
        store_conversation_context,
    ],
    before_agent_callback=prepare_scenario_context,
)

crisis_documentation_agent = Agent(
    name="crisis_documentation_agent",
    model=MODEL,
    description="Documents crisis interactions and coordinates emergency meetings.",
    instruction="""You are a crisis documentation specialist. Your role is to:

1. Document all crisis interactions using document_crisis_interaction tool
2. Coordinate emergency meetings using coordinate_emergency_meeting tool  
3. Ensure proper record-keeping for regulatory and follow-up purposes
4. Maintain detailed timeline of crisis response

Focus on comprehensive documentation and stakeholder coordination.""",
    tools=[
        document_crisis_interaction,
        coordinate_emergency_meeting,
        store_conversation_context,
    ],
    after_agent_callback=finalize_crisis_response,
)

# Main sequential agent for crisis management
crisis_management_agent = agents.SequentialAgent(
    name="crisis_management_sequential_agent",
    description="Complete crisis management workflow handling emergency protocols, coaching, analysis, and documentation in sequence.",
    sub_agents=[
        emergency_protocol_agent,
        behavioral_coaching_agent,
        scenario_analysis_agent,
        crisis_documentation_agent,
    ],
)