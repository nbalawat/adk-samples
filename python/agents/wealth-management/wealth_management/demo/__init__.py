"""Enterprise demo framework for wealth management workflows

This package provides a comprehensive enterprise demonstration framework
with role-based interfaces for showcasing all wealth management capabilities.

Components:
- EnterpriseDemo: Main demo orchestration class
- UserRole: Role-based access and perspectives
- DemoScenario: Structured demo scenarios
- Quick demo functions for immediate demonstrations
"""

from .enterprise_demo import (
    EnterpriseDemo,
    UserRole,
    DemoScenario,
    run_advisor_demo,
    run_client_demo,
    run_crisis_demo,
    get_demo_menu
)

# Create default demo instance
default_enterprise_demo = EnterpriseDemo()

__all__ = [
    'EnterpriseDemo',
    'UserRole', 
    'DemoScenario',
    'run_advisor_demo',
    'run_client_demo',
    'run_crisis_demo',
    'get_demo_menu',
    'default_enterprise_demo'
]