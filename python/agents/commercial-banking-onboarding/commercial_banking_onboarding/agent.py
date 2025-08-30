"""Commercial banking onboarding orchestrator agent."""

import logging
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from .prompt import ORCHESTRATOR_PROMPT
from .tools.orchestrator_tools import (
    create_onboarding_application,
    update_application_status,
    get_application_status,
    route_to_specialist_agent,
    make_onboarding_decision
)

# Import sub-agents
from .sub_agents.kyc_agent import kyc_agent
from .sub_agents.credit_agent import credit_agent
from .sub_agents.compliance_agent import compliance_agent
from .sub_agents.document_agent import document_agent
from .sub_agents.account_setup_agent import account_setup_agent

logger = logging.getLogger(__name__)

MODEL = "gemini-2.5-pro"

# Create the orchestrator agent
commercial_banking_orchestrator = LlmAgent(
    name="commercial_banking_orchestrator",
    model=MODEL,
    description="Multi-agent system for automating commercial banking customer onboarding",
    instruction=ORCHESTRATOR_PROMPT,
    output_key="onboarding_result",
    tools=[
        create_onboarding_application,
        update_application_status, 
        get_application_status,
        route_to_specialist_agent,
        make_onboarding_decision,
        # Wrap sub-agents with AgentTool
        AgentTool(agent=kyc_agent),
        AgentTool(agent=credit_agent),
        AgentTool(agent=compliance_agent),
        AgentTool(agent=document_agent),
        AgentTool(agent=account_setup_agent),
    ],
)

# Standard pattern: root_agent points to main orchestrator
root_agent = commercial_banking_orchestrator
agent = commercial_banking_orchestrator  # Keep backward compatibility