"""Advisor-facing agents for wealth management"""

from .client_relationship_manager_agent import client_relationship_manager_agent
from .portfolio_optimizer_agent import portfolio_optimizer_agent
from .market_research_agent import market_research_agent

__all__ = [
    "client_relationship_manager_agent",
    "portfolio_optimizer_agent",
    "market_research_agent"
]