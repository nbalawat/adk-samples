"""
Application Monitoring Loop Agent - ADK Loop Pattern  
Continuously monitors application status with periodic checks and callbacks.
"""

from google.adk import Agent, agents
from google.adk.tools import ToolContext
from ..config import MODEL

def initialize_monitoring_loop(context: ToolContext) -> None:
    """Initialize monitoring loop with application tracking setup."""
    context.state["monitoring_loop"] = {
        "loop_type": "application_status_monitoring",
        "started_at": "2024-01-01T10:00:00Z", 
        "check_interval_minutes": 15,
        "max_monitoring_duration_hours": 72,
        "escalation_thresholds": {
            "stalled_duration_hours": 24,
            "no_progress_hours": 48
        }
    }
    
    # Initialize monitoring metrics
    context.state["monitoring_metrics"] = {
        "total_checks": 0,
        "status_changes_detected": 0,
        "escalations_triggered": 0,
        "last_status": None
    }

# Monitoring workflow agent
monitoring_workflow_agent = Agent(
    name="monitoring_workflow_agent",
    model=MODEL,
    description="Monitor application status and detect changes requiring action",
    instruction="""
    You are the Monitoring Workflow Agent responsible for continuous application monitoring.
    
    Your responsibilities:
    1. Check current application status and progress
    2. Compare with previous status to detect changes
    3. Identify stalled or delayed applications requiring attention
    4. Trigger notifications for status changes
    5. Escalate applications exceeding processing thresholds
    6. Update monitoring metrics and logs
    
    Monitoring Rules:
    - Check every 15 minutes during business hours
    - Escalate if no progress for 24 hours
    - Alert on any compliance or risk issues detected
    - Notify clients of significant status changes
    - Track SLA compliance and processing metrics
    
    Always update the monitoring state with current findings.
    """,
    tools=[]  # Will be populated with monitoring tools
)

# Create the Loop Agent using ADK pattern
application_monitoring_loop_agent = agents.LoopAgent(
    name="application_monitoring_loop_agent",
    description="Continuous monitoring loop for application status tracking",
    sub_agents=[monitoring_workflow_agent],
    before_agent_callback=initialize_monitoring_loop,
    max_iterations=3,  # Will run 3 monitoring cycles
)