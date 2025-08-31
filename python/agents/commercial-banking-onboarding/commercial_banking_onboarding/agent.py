"""Commercial banking onboarding orchestrator agent."""

import logging
from .enhanced_agent import enhanced_commercial_banking_orchestrator

logger = logging.getLogger(__name__)

# Use the enhanced agent system as the main orchestrator
commercial_banking_orchestrator = enhanced_commercial_banking_orchestrator

# Standard pattern: root_agent points to main orchestrator  
root_agent = enhanced_commercial_banking_orchestrator
agent = enhanced_commercial_banking_orchestrator  # Keep backward compatibility