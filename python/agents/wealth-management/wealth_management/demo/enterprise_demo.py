"""Enterprise demo framework with role-based interfaces for wealth management workflows"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from enum import Enum
import random

from ..workflows import workflow_registry, default_executor, WorkflowCategory, ADKPattern
from ..data.loader import data_loader

class UserRole(Enum):
    """User roles in the wealth management system"""
    FINANCIAL_ADVISOR = "financial_advisor"
    PORTFOLIO_MANAGER = "portfolio_manager" 
    CLIENT_SERVICES = "client_services"
    OPERATIONS_MANAGER = "operations_manager"
    COMPLIANCE_OFFICER = "compliance_officer"
    SENIOR_ADVISOR = "senior_advisor"
    WEALTH_CLIENT = "wealth_client"
    RELATIONSHIP_MANAGER = "relationship_manager"

class DemoScenario:
    """Represents a demo scenario for specific user roles"""
    
    def __init__(self, scenario_id: str, name: str, description: str, 
                 target_roles: List[UserRole], workflows: List[str],
                 context: Dict[str, Any], duration_minutes: int = 15):
        self.scenario_id = scenario_id
        self.name = name
        self.description = description
        self.target_roles = target_roles
        self.workflows = workflows
        self.context = context
        self.duration_minutes = duration_minutes

class EnterpriseDemo:
    """Enterprise demonstration framework with role-based workflow showcases"""
    
    def __init__(self):
        self.scenarios: Dict[str, DemoScenario] = {}
        self.user_sessions: Dict[str, Dict[str, Any]] = {}
        self._create_demo_scenarios()
        
    def _create_demo_scenarios(self):
        """Create comprehensive demo scenarios for all user roles"""
        
        # Scenario 1: Market Volatility Crisis Response
        self.scenarios["crisis_response"] = DemoScenario(
            scenario_id="crisis_response",
            name="Market Crisis Response Workflow",
            description="Demonstrate how the system responds to market volatility with coordinated team response",
            target_roles=[UserRole.SENIOR_ADVISOR, UserRole.PORTFOLIO_MANAGER, UserRole.RELATIONSHIP_MANAGER],
            workflows=["ADV007", "ADV009", "ADV002", "ADV008"],
            context={
                "event_type": "market_crash",
                "severity": "extreme", 
                "affected_clients": ["WM123456", "WM789012", "WM345678"],
                "market_decline": 0.15,
                "vix_level": 45.5,
                "trigger_time": datetime.now().isoformat()
            },
            duration_minutes=20
        )
        
        # Scenario 2: New Client Onboarding Journey
        self.scenarios["client_onboarding"] = DemoScenario(
            scenario_id="client_onboarding", 
            name="Comprehensive Client Onboarding",
            description="Full client onboarding process from prospect to active client",
            target_roles=[UserRole.FINANCIAL_ADVISOR, UserRole.CLIENT_SERVICES, UserRole.COMPLIANCE_OFFICER],
            workflows=["ADV005", "CLI001", "CLI002", "OPS001"],
            context={
                "prospect_id": "PROSPECT_2024_001",
                "prospect_name": "Sarah Johnson",
                "initial_assets": 2500000,
                "risk_tolerance": "Moderate",
                "primary_goals": ["Retirement Planning", "Tax Optimization"],
                "referral_source": "Existing Client"
            },
            duration_minutes=25
        )
        
        # Scenario 3: Quarterly Portfolio Review Cycle
        self.scenarios["quarterly_review"] = DemoScenario(
            scenario_id="quarterly_review",
            name="Quarterly Portfolio Review Process", 
            description="Systematic quarterly review across client portfolio with reporting and follow-up",
            target_roles=[UserRole.PORTFOLIO_MANAGER, UserRole.FINANCIAL_ADVISOR],
            workflows=["ADV002", "ADV006", "CLI003", "ADV014"],
            context={
                "review_period": "Q3_2024",
                "client_segment": "High Net Worth",
                "portfolio_count": 150,
                "performance_benchmark": "S&P 500",
                "review_type": "comprehensive"
            },
            duration_minutes=18
        )
        
        # Scenario 4: Regulatory Compliance Audit
        self.scenarios["compliance_audit"] = DemoScenario(
            scenario_id="compliance_audit",
            name="Regulatory Compliance and Audit Response",
            description="Handle regulatory examination with documentation and process validation",
            target_roles=[UserRole.COMPLIANCE_OFFICER, UserRole.OPERATIONS_MANAGER],
            workflows=["ADV008", "OPS001", "OPS002"],
            context={
                "audit_type": "SEC Examination",
                "examination_scope": "Investment Advisory Operations",
                "client_sample_size": 50,
                "review_period": "2023-2024",
                "examiner_requests": 12
            },
            duration_minutes=22
        )
        
        # Scenario 5: Client-Driven Planning Session  
        self.scenarios["client_planning"] = DemoScenario(
            scenario_id="client_planning",
            name="Interactive Financial Planning Session",
            description="Client-initiated comprehensive financial planning with goal setting and strategy",
            target_roles=[UserRole.WEALTH_CLIENT, UserRole.FINANCIAL_ADVISOR],
            workflows=["CLI001", "CLI002", "ADV006", "ADV010"],
            context={
                "client_id": "WM456789", 
                "planning_trigger": "Major Life Event",
                "life_event": "Business Sale",
                "windfall_amount": 5000000,
                "new_goals": ["Estate Planning", "Charitable Giving", "Family Education"],
                "time_horizon": "15+ years"
            },
            duration_minutes=30
        )
        
        # Scenario 6: Operations Excellence Showcase
        self.scenarios["operations_excellence"] = DemoScenario(
            scenario_id="operations_excellence",
            name="Operations and Trade Management Excellence",
            description="Showcase operational efficiency in trade processing and account management",
            target_roles=[UserRole.OPERATIONS_MANAGER, UserRole.PORTFOLIO_MANAGER],
            workflows=["OPS002", "OPS001", "ADV013"],
            context={
                "rebalancing_cycle": "Monthly",
                "accounts_to_rebalance": 200,
                "trade_volume": 15000000,
                "efficiency_target": "99.5%",
                "automation_level": "High"
            },
            duration_minutes=15
        )
    
    async def run_scenario(self, scenario_id: str, user_role: UserRole, 
                          session_id: str = None) -> Dict[str, Any]:
        """Execute a demo scenario for a specific user role"""
        
        if scenario_id not in self.scenarios:
            raise ValueError(f"Scenario {scenario_id} not found")
        
        scenario = self.scenarios[scenario_id]
        
        # Check role authorization
        if user_role not in scenario.target_roles:
            return {
                "error": f"Role {user_role.value} not authorized for scenario {scenario_id}",
                "authorized_roles": [role.value for role in scenario.target_roles]
            }
        
        session_id = session_id or f"demo_{scenario_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"\n🎭 Starting Enterprise Demo Scenario")
        print(f"📋 Scenario: {scenario.name}")
        print(f"👤 User Role: {user_role.value.replace('_', ' ').title()}")
        print(f"🆔 Session ID: {session_id}")
        print(f"⏱️ Duration: ~{scenario.duration_minutes} minutes")
        print(f"📝 Description: {scenario.description}")
        print("="*60)
        
        # Initialize session
        session_start = datetime.now()
        session_data = {
            "session_id": session_id,
            "scenario_id": scenario_id,
            "user_role": user_role.value,
            "start_time": session_start.isoformat(),
            "workflow_executions": [],
            "role_specific_insights": [],
            "kpis": {}
        }
        
        self.user_sessions[session_id] = session_data
        
        try:
            # Execute scenario workflows with role-specific perspective
            for i, workflow_id in enumerate(scenario.workflows, 1):
                workflow_def = workflow_registry.get_workflow(workflow_id)
                if not workflow_def:
                    continue
                
                print(f"\n🔄 Step {i}/{len(scenario.workflows)}: {workflow_def.name}")
                print(f"   Pattern: {workflow_def.pattern.value}")
                print(f"   Category: {workflow_def.category.value}")
                
                # Add role-specific context
                execution_context = {
                    **scenario.context,
                    "user_role": user_role.value,
                    "session_id": session_id,
                    "demo_mode": True
                }
                
                # Execute workflow
                execution = await default_executor.execute_workflow(workflow_id, execution_context)
                
                # Record execution
                session_data["workflow_executions"].append({
                    "workflow_id": workflow_id,
                    "workflow_name": workflow_def.name,
                    "execution_id": execution.execution_id,
                    "status": execution.status.value,
                    "steps_completed": len(execution.step_results),
                    "execution_time": (
                        (execution.completed_at - execution.started_at).total_seconds()
                        if execution.completed_at and execution.started_at else 0
                    )
                })
                
                # Add role-specific insights
                insight = self._generate_role_insight(user_role, workflow_def, execution)
                if insight:
                    session_data["role_specific_insights"].append(insight)
                    print(f"   💡 {user_role.value.replace('_', ' ').title()} Insight: {insight}")
                
                print(f"   ✅ Status: {execution.status.value}")
                
                # Small delay for demo pacing
                await asyncio.sleep(0.5)
            
            # Calculate session KPIs
            session_data["kpis"] = self._calculate_session_kpis(scenario, session_data)
            
            # Session completion
            session_end = datetime.now()
            session_data["end_time"] = session_end.isoformat()
            session_data["total_duration"] = (session_end - session_start).total_seconds()
            
            # Generate role-specific summary
            summary = self._generate_role_summary(user_role, scenario, session_data)
            
            print(f"\n🎉 Scenario Complete!")
            print(f"⏱️ Total Duration: {session_data['total_duration']:.1f} seconds")
            print(f"✅ Workflows Executed: {len(session_data['workflow_executions'])}")
            print(f"📊 Success Rate: {session_data['kpis']['success_rate']:.1%}")
            
            return {
                "session_data": session_data,
                "summary": summary,
                "success": True
            }
            
        except Exception as e:
            session_data["error"] = str(e)
            session_data["end_time"] = datetime.now().isoformat()
            
            print(f"\n❌ Scenario Failed: {str(e)}")
            
            return {
                "session_data": session_data,
                "error": str(e),
                "success": False
            }
    
    def _generate_role_insight(self, user_role: UserRole, workflow_def, execution) -> Optional[str]:
        """Generate role-specific insights from workflow execution"""
        
        insights_by_role = {
            UserRole.FINANCIAL_ADVISOR: [
                f"Client impact assessment shows {random.choice(['positive', 'neutral', 'requires attention'])} status",
                f"Recommended follow-up: {random.choice(['Schedule meeting', 'Send update', 'Monitor closely'])}",
                f"Portfolio alignment score: {random.randint(75, 95)}%"
            ],
            UserRole.PORTFOLIO_MANAGER: [
                f"Risk-adjusted performance: {random.uniform(-0.05, 0.15):.2%}",
                f"Allocation drift detected: {random.uniform(0, 0.08):.1%}",
                f"Rebalancing {random.choice(['recommended', 'not required', 'scheduled'])}"
            ],
            UserRole.COMPLIANCE_OFFICER: [
                f"Regulatory compliance: {random.choice(['Fully compliant', 'Minor issues', 'Requires review'])}",
                f"Documentation status: {random.choice(['Complete', 'Pending items', 'Up to date'])}",
                f"Audit trail: {random.choice(['Comprehensive', 'Adequate', 'Enhanced needed'])}"
            ],
            UserRole.OPERATIONS_MANAGER: [
                f"Process efficiency: {random.randint(85, 99)}%",
                f"STP rate: {random.randint(90, 98)}%",
                f"Exception handling: {random.choice(['Automated', 'Manual review', 'Escalated'])}"
            ],
            UserRole.WEALTH_CLIENT: [
                f"Goal progress: {random.randint(65, 95)}% on track",
                f"Risk level: {random.choice(['Within tolerance', 'Slightly elevated', 'Conservative'])}",
                f"Next milestone: {random.choice(['6 months', '1 year', '2 years'])}"
            ]
        }
        
        role_insights = insights_by_role.get(user_role)
        if role_insights:
            return random.choice(role_insights)
        
        return None
    
    def _calculate_session_kpis(self, scenario: DemoScenario, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate KPIs for the demo session"""
        
        executions = session_data["workflow_executions"]
        
        successful = len([e for e in executions if e["status"] == "COMPLETED"])
        total = len(executions)
        
        kpis = {
            "success_rate": successful / max(total, 1),
            "total_workflows": total,
            "successful_workflows": successful,
            "failed_workflows": total - successful,
            "average_execution_time": sum(e["execution_time"] for e in executions) / max(total, 1),
            "total_steps": sum(e["steps_completed"] for e in executions),
            "scenario_completion": 100 if successful == total else (successful / total) * 100
        }
        
        return kpis
    
    def _generate_role_summary(self, user_role: UserRole, scenario: DemoScenario, 
                              session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate role-specific summary of the demo session"""
        
        kpis = session_data["kpis"]
        
        # Base summary
        summary = {
            "role": user_role.value,
            "scenario": scenario.name,
            "key_metrics": kpis,
            "insights": session_data["role_specific_insights"],
            "duration_minutes": session_data["total_duration"] / 60
        }
        
        # Role-specific additions
        if user_role == UserRole.FINANCIAL_ADVISOR:
            summary["client_outcomes"] = {
                "clients_reviewed": len(scenario.context.get("affected_clients", [1])),
                "meetings_scheduled": random.randint(2, 8),
                "action_items": random.randint(5, 15),
                "follow_up_required": random.choice([True, False])
            }
        
        elif user_role == UserRole.PORTFOLIO_MANAGER:
            summary["portfolio_metrics"] = {
                "portfolios_analyzed": random.randint(10, 100),
                "rebalancing_trades": random.randint(15, 50),
                "risk_adjustments": random.randint(3, 12),
                "performance_attribution": "completed"
            }
        
        elif user_role == UserRole.COMPLIANCE_OFFICER:
            summary["compliance_metrics"] = {
                "regulations_reviewed": random.randint(5, 15),
                "policies_updated": random.randint(2, 8),
                "training_sessions": random.randint(1, 4),
                "audit_readiness": random.choice(["Excellent", "Good", "Needs Improvement"])
            }
        
        elif user_role == UserRole.OPERATIONS_MANAGER:
            summary["operational_metrics"] = {
                "processes_optimized": random.randint(3, 10),
                "efficiency_gain": f"{random.uniform(5, 25):.1f}%",
                "error_reduction": f"{random.uniform(10, 40):.1f}%",
                "automation_opportunities": random.randint(2, 8)
            }
        
        return summary
    
    def get_available_scenarios(self, user_role: UserRole = None) -> List[Dict[str, Any]]:
        """Get list of available scenarios, optionally filtered by role"""
        
        scenarios = []
        for scenario_id, scenario in self.scenarios.items():
            if user_role is None or user_role in scenario.target_roles:
                scenarios.append({
                    "scenario_id": scenario_id,
                    "name": scenario.name,
                    "description": scenario.description,
                    "target_roles": [role.value for role in scenario.target_roles],
                    "workflow_count": len(scenario.workflows),
                    "duration_minutes": scenario.duration_minutes
                })
        
        return scenarios
    
    def get_role_dashboard(self, user_role: UserRole) -> Dict[str, Any]:
        """Generate role-specific dashboard showing relevant capabilities"""
        
        # Get workflows relevant to this role
        relevant_workflows = []
        role_keywords = {
            UserRole.FINANCIAL_ADVISOR: ["client", "meeting", "planning", "communication"],
            UserRole.PORTFOLIO_MANAGER: ["portfolio", "performance", "risk", "rebalancing"],
            UserRole.COMPLIANCE_OFFICER: ["compliance", "regulatory", "audit", "training"],
            UserRole.OPERATIONS_MANAGER: ["operation", "trade", "account", "process"],
            UserRole.WEALTH_CLIENT: ["planning", "goal", "review", "education"]
        }
        
        keywords = role_keywords.get(user_role, [])
        
        for workflow in workflow_registry.get_all_workflows():
            workflow_text = f"{workflow.name} {workflow.description}".lower()
            if any(keyword in workflow_text for keyword in keywords):
                relevant_workflows.append({
                    "workflow_id": workflow.workflow_id,
                    "name": workflow.name,
                    "pattern": workflow.pattern.value,
                    "complexity": workflow.complexity
                })
        
        # Available scenarios for this role
        available_scenarios = self.get_available_scenarios(user_role)
        
        dashboard = {
            "user_role": user_role.value,
            "role_name": user_role.value.replace('_', ' ').title(),
            "relevant_workflows": relevant_workflows,
            "available_scenarios": available_scenarios,
            "capabilities": {
                "workflow_access": len(relevant_workflows),
                "scenario_access": len(available_scenarios),
                "pattern_coverage": list(set(wf["pattern"] for wf in relevant_workflows))
            },
            "quick_actions": self._get_role_quick_actions(user_role)
        }
        
        return dashboard
    
    def _get_role_quick_actions(self, user_role: UserRole) -> List[str]:
        """Get quick actions available for each role"""
        
        quick_actions = {
            UserRole.FINANCIAL_ADVISOR: [
                "Schedule client meeting",
                "Review portfolio performance", 
                "Generate market commentary",
                "Create financial plan"
            ],
            UserRole.PORTFOLIO_MANAGER: [
                "Analyze portfolio risk",
                "Execute rebalancing",
                "Review performance attribution",
                "Generate investment research"
            ],
            UserRole.COMPLIANCE_OFFICER: [
                "Run compliance audit",
                "Review regulatory changes",
                "Generate compliance report",
                "Schedule training session"
            ],
            UserRole.OPERATIONS_MANAGER: [
                "Process trade settlements",
                "Review operational metrics",
                "Optimize workflows",
                "Manage account administration"
            ],
            UserRole.WEALTH_CLIENT: [
                "Review goal progress",
                "Schedule planning session",
                "View portfolio summary",
                "Access educational resources"
            ]
        }
        
        return quick_actions.get(user_role, [])
    
    def export_session_report(self, session_id: str) -> Dict[str, Any]:
        """Export detailed session report"""
        
        if session_id not in self.user_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.user_sessions[session_id]
        
        report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "session_id": session_id,
                "report_type": "enterprise_demo_session"
            },
            "session_summary": session,
            "workflow_details": [],
            "recommendations": []
        }
        
        # Add detailed workflow information
        for execution in session["workflow_executions"]:
            workflow_def = workflow_registry.get_workflow(execution["workflow_id"])
            if workflow_def:
                report["workflow_details"].append({
                    "workflow_id": execution["workflow_id"],
                    "name": execution["workflow_name"],
                    "category": workflow_def.category.value,
                    "pattern": workflow_def.pattern.value,
                    "complexity": workflow_def.complexity,
                    "execution_summary": execution
                })
        
        # Generate recommendations
        if session["kpis"]["success_rate"] < 0.9:
            report["recommendations"].append("Consider additional training on failed workflows")
        
        if session["total_duration"] > 30 * 60:  # 30 minutes
            report["recommendations"].append("Workflow optimization opportunities identified")
        
        report["recommendations"].append("Schedule follow-up demo for advanced features")
        
        return report

# Convenience functions for easy demo execution
async def run_advisor_demo(session_id: str = None) -> Dict[str, Any]:
    """Quick advisor role demo"""
    demo = EnterpriseDemo()
    return await demo.run_scenario("quarterly_review", UserRole.FINANCIAL_ADVISOR, session_id)

async def run_client_demo(session_id: str = None) -> Dict[str, Any]:
    """Quick client role demo"""
    demo = EnterpriseDemo()
    return await demo.run_scenario("client_planning", UserRole.WEALTH_CLIENT, session_id)

async def run_crisis_demo(session_id: str = None) -> Dict[str, Any]:
    """Quick crisis management demo"""
    demo = EnterpriseDemo()
    return await demo.run_scenario("crisis_response", UserRole.SENIOR_ADVISOR, session_id)

def get_demo_menu() -> Dict[str, Any]:
    """Get interactive demo menu"""
    demo = EnterpriseDemo()
    
    return {
        "available_roles": [role.value for role in UserRole],
        "scenarios": demo.get_available_scenarios(),
        "quick_demos": {
            "advisor_demo": "Quarterly review process demonstration",
            "client_demo": "Client financial planning experience", 
            "crisis_demo": "Market crisis response coordination"
        },
        "instructions": [
            "1. Choose a user role from available_roles",
            "2. Select a scenario from scenarios list",
            "3. Run: await demo.run_scenario(scenario_id, user_role)",
            "4. Or use quick demos for immediate experience"
        ]
    }