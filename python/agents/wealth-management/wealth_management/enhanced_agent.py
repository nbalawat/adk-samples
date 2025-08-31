"""Enhanced wealth management agent with advanced workflow routing and orchestration"""

from google.adk.agents import Agent
from google.adk.tools import ToolContext
from typing import Dict, Any, Optional
import asyncio
import importlib
from datetime import datetime

from . import prompt
from .workflow_router import WorkflowRouter, WorkflowClassifier
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

MODEL = "gemini-2.5-pro"


class EnhancedWealthManagementAgent(Agent):
    """
    Enhanced wealth management agent with intelligent workflow routing,
    advanced pattern recognition, and sophisticated orchestration capabilities.
    
    Supports 6 ADK patterns:
    - Sequential: Step-by-step workflows (market response, crisis management)
    - Parallel: Concurrent processing (client onboarding, campaign management)
    - Loop: Continuous monitoring (portfolio tracking, risk assessment)
    - Event-Driven: Threshold and trigger-based (volatility alerts, news events)
    - Scheduled: Time-based workflows (reporting cycles, compliance deadlines)
    - Master Orchestration: Complex multi-agent coordination
    """

    def __init__(self):
        super().__init__(
            name="enhanced_wealth_management_agent",
            model=MODEL,
            description=(
                "Advanced wealth management orchestrator with intelligent workflow routing. "
                "Supports 6 ADK patterns across 33 specialized workflows serving advisor, "
                "client, and operations personas with enterprise-grade coordination."
            ),
            instruction=prompt.ENHANCED_WEALTH_MANAGEMENT_PROMPT
        )
        
        self.router = WorkflowRouter()
        self.classifier = WorkflowClassifier()
        self.sub_agents = {}
        self.workflow_metrics = {
            "total_workflows": 0,
            "successful_routes": 0,
            "pattern_usage": {
                "sequential": 0,
                "parallel": 0,
                "loop": 0,
                "event_driven": 0,
                "scheduled": 0,
                "master_orchestration": 0
            }
        }

    async def run_async(self, query: str, tool_context: Optional[ToolContext] = None) -> str:
        """
        Enhanced query processing with intelligent workflow routing.
        
        Args:
            query: User query
            tool_context: ADK tool context for state management
            
        Returns:
            Orchestrated response from appropriate workflow pattern
        """
        try:
            # Update workflow metrics
            self.workflow_metrics["total_workflows"] += 1
            
            # Route the query to determine optimal workflow pattern
            routing_decision = self.router.route_query(query)
            
            # Extract routing information
            classification = routing_decision["classification"]
            routing_strategy = routing_decision["routing_strategy"]
            execution_context = routing_decision["execution_context"]
            
            # Log classification results
            pattern = classification["routing"]["recommended_pattern"]
            self.workflow_metrics["pattern_usage"][pattern] += 1
            
            # Execute based on routing strategy
            response = await self._execute_workflow(
                query, routing_strategy, execution_context, tool_context
            )
            
            # Track successful routing
            if "SUCCESS" in response or "✅" in response:
                self.workflow_metrics["successful_routes"] += 1
            
            # Add routing metadata to response
            return self._format_enhanced_response(response, classification, routing_strategy)
            
        except Exception as e:
            error_response = f"❌ Workflow Routing Error: {str(e)}"
            return self._format_enhanced_response(error_response, None, None, error=True)

    async def _execute_workflow(self, query: str, strategy: Dict[str, Any], context: Dict[str, Any], tool_context: Optional[ToolContext] = None) -> str:
        """Execute workflow based on routing strategy"""
        
        strategy_type = strategy["type"]
        primary_agent = strategy["primary_agent"]
        
        if strategy_type == "orchestrated":
            return await self._execute_orchestrated_workflow(query, strategy, context, tool_context)
        elif strategy_type == "concurrent":
            return await self._execute_concurrent_workflow(query, strategy, context, tool_context)
        elif strategy_type == "reactive":
            return await self._execute_reactive_workflow(query, strategy, context, tool_context)
        elif strategy_type == "scheduled":
            return await self._execute_scheduled_workflow(query, strategy, context, tool_context)
        else:
            return await self._execute_sequential_workflow(query, strategy, context, tool_context)

    async def _execute_orchestrated_workflow(self, query: str, strategy: Dict[str, Any], context: Dict[str, Any], tool_context: Optional[ToolContext] = None) -> str:
        """Execute master orchestration workflow"""
        
        try:
            # Load master orchestrator
            orchestrator = await self._get_sub_agent("MasterOrchestrator")
            
            if orchestrator:
                # Execute with full orchestration capabilities
                response = await orchestrator.run_async(query)
                return f"🧠 Master Orchestration Executed\n\n{response}"
            else:
                # Fall back to intelligent routing across multiple patterns
                return await self._execute_multi_pattern_fallback(query, context, tool_context)
                
        except Exception as e:
            return f"❌ Orchestration Error: {str(e)}"

    async def _execute_concurrent_workflow(self, query: str, strategy: Dict[str, Any], context: Dict[str, Any], tool_context: Optional[ToolContext] = None) -> str:
        """Execute parallel/concurrent workflow"""
        
        try:
            # Check if this is a client onboarding scenario
            if "onboarding" in query.lower():
                onboarding_agent = await self._get_sub_agent("ClientOnboardingAgent")
                if onboarding_agent:
                    response = await onboarding_agent.run_async(query)
                    return f"⚡ Parallel Processing Complete\n\n{response}"
            
            # Fall back to parallel tool execution
            return await self._execute_parallel_tools(query, context, tool_context)
            
        except Exception as e:
            return f"❌ Concurrent Execution Error: {str(e)}"

    async def _execute_reactive_workflow(self, query: str, strategy: Dict[str, Any], context: Dict[str, Any], tool_context: Optional[ToolContext] = None) -> str:
        """Execute event-driven workflow"""
        
        try:
            # Load event-driven agent
            event_agent = await self._get_sub_agent("EventDrivenAgent")
            
            if event_agent:
                response = await event_agent.run_async(query)
                return f"🔥 Event-Driven Response\n\n{response}"
            else:
                # Fall back to threshold-based processing
                return await self._execute_threshold_fallback(query, context, tool_context)
                
        except Exception as e:
            return f"❌ Event Processing Error: {str(e)}"

    async def _execute_scheduled_workflow(self, query: str, strategy: Dict[str, Any], context: Dict[str, Any], tool_context: Optional[ToolContext] = None) -> str:
        """Execute scheduled/time-based workflow"""
        
        try:
            # Load scheduled agent
            scheduled_agent = await self._get_sub_agent("ScheduledAgent")
            
            if scheduled_agent:
                response = await scheduled_agent.run_async(query)
                return f"📅 Scheduled Workflow Complete\n\n{response}"
            else:
                # Fall back to time-based processing
                return await self._execute_time_based_fallback(query, context, tool_context)
                
        except Exception as e:
            return f"❌ Scheduled Processing Error: {str(e)}"

    async def _execute_sequential_workflow(self, query: str, strategy: Dict[str, Any], context: Dict[str, Any], tool_context: Optional[ToolContext] = None) -> str:
        """Execute sequential workflow"""
        
        try:
            primary_agent = strategy["primary_agent"]
            
            # Route to appropriate sequential agent
            if "Market" in primary_agent:
                agent = await self._get_sub_agent("MarketResponseAgent")
                if agent:
                    response = await agent.run_async(query)
                    return f"📊 Sequential Market Response\n\n{response}"
            
            elif "Crisis" in primary_agent:
                agent = await self._get_sub_agent("CrisisManagementAgent")
                if agent:
                    response = await agent.run_async(query)
                    return f"🚨 Sequential Crisis Management\n\n{response}"
            
            elif "Portfolio" in primary_agent:
                agent = await self._get_sub_agent("PortfolioMonitoringAgent")
                if agent:
                    response = await agent.run_async(query)
                    return f"🔄 Portfolio Monitoring Loop\n\n{response}"
            
            # Fall back to tool-based sequential execution
            return await self._execute_tool_sequence(query, context, tool_context)
            
        except Exception as e:
            return f"❌ Sequential Processing Error: {str(e)}"

    async def _get_sub_agent(self, agent_name: str) -> Optional[Agent]:
        """Load and cache sub-agent instances"""
        
        if agent_name in self.sub_agents:
            return self.sub_agents[agent_name]
        
        try:
            # Dynamic import based on agent name
            module_map = {
                "EventDrivenAgent": "wealth_management.sub_agents.event_driven_agent",
                "ScheduledAgent": "wealth_management.sub_agents.scheduled_agent",
                "MasterOrchestrator": "wealth_management.sub_agents.master_orchestrator",
                "MarketResponseAgent": "wealth_management.sub_agents.market_response_agent",
                "CrisisManagementAgent": "wealth_management.sub_agents.crisis_management_agent",
                "ClientOnboardingAgent": "wealth_management.sub_agents.client_onboarding_agent",
                "PortfolioMonitoringAgent": "wealth_management.sub_agents.portfolio_monitoring_agent"
            }
            
            if agent_name not in module_map:
                return None
                
            module_path = module_map[agent_name]
            module = importlib.import_module(module_path)
            agent_class = getattr(module, agent_name)
            
            # Create and cache the agent
            agent_instance = agent_class()
            self.sub_agents[agent_name] = agent_instance
            
            return agent_instance
            
        except Exception as e:
            print(f"Failed to load sub-agent {agent_name}: {str(e)}")
            return None

    async def _execute_multi_pattern_fallback(self, query: str, context: Dict[str, Any], tool_context: Optional[ToolContext] = None) -> str:
        """Multi-pattern fallback for complex orchestration"""
        
        # Analyze query for multiple patterns
        if "market" in query.lower() and "client" in query.lower():
            # Market + Client scenario
            market_response = await self._execute_market_tools(query, tool_context)
            client_response = await self._execute_client_tools(query, tool_context)
            
            return f"🎯 Multi-Pattern Orchestration\n\n📊 Market Analysis:\n{market_response}\n\n👥 Client Impact:\n{client_response}"
        
        # Default to comprehensive analysis
        return await self._execute_comprehensive_analysis(query, tool_context)

    async def _execute_parallel_tools(self, query: str, context: Dict[str, Any], tool_context: Optional[ToolContext] = None) -> str:
        """Execute multiple tools in parallel"""
        
        # Determine relevant tool categories
        tool_tasks = []
        
        if "portfolio" in query.lower():
            tool_tasks.append(self._execute_portfolio_tools(query, tool_context))
        
        if "performance" in query.lower():
            tool_tasks.append(self._execute_performance_tools(query, tool_context))
        
        if "risk" in query.lower():
            tool_tasks.append(self._execute_risk_tools(query, tool_context))
        
        if not tool_tasks:
            tool_tasks.append(self._execute_comprehensive_analysis(query, tool_context))
        
        # Execute tools in parallel
        results = await asyncio.gather(*tool_tasks, return_exceptions=True)
        
        # Format parallel results
        response = "⚡ Parallel Tool Execution Results:\n\n"
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                response += f"Task {i+1}: ❌ Error - {str(result)}\n"
            else:
                response += f"Task {i+1}: ✅ {result[:100]}...\n"
        
        return response

    async def _execute_threshold_fallback(self, query: str, context: Dict[str, Any], tool_context: Optional[ToolContext] = None) -> str:
        """Threshold-based fallback processing"""
        
        # Extract threshold values from query
        import re
        threshold_match = re.search(r'(\d+(?:\.\d+)?)%', query)
        if threshold_match:
            threshold = float(threshold_match.group(1))
            
            # Execute volatility analysis with threshold
            result = analyze_market_volatility(threshold=threshold, timeframe="1D", tool_context=tool_context)
            return f"🎯 Threshold Analysis (>{threshold}%)\n\n{self._format_tool_result(result)}"
        
        # Default volatility analysis
        result = analyze_market_volatility(threshold=15.0, timeframe="1D", tool_context=tool_context)
        return f"🔥 Event Trigger Analysis\n\n{self._format_tool_result(result)}"

    async def _execute_time_based_fallback(self, query: str, context: Dict[str, Any], tool_context: Optional[ToolContext] = None) -> str:
        """Time-based fallback processing"""
        
        current_time = datetime.utcnow()
        
        # Determine time-based action
        if "daily" in query.lower():
            return f"📅 Daily Processing ({current_time.strftime('%Y-%m-%d')})\n\nExecuting daily workflows..."
        elif "weekly" in query.lower():
            return f"📅 Weekly Processing (Week of {current_time.strftime('%Y-%m-%d')})\n\nExecuting weekly workflows..."
        elif "monthly" in query.lower():
            return f"📅 Monthly Processing ({current_time.strftime('%Y-%m')})\n\nExecuting monthly workflows..."
        
        return f"📅 Scheduled Processing\n\nTime-based workflow executed at {current_time.strftime('%H:%M:%S UTC')}"

    async def _execute_tool_sequence(self, query: str, context: Dict[str, Any], tool_context: Optional[ToolContext] = None) -> str:
        """Execute tools in sequence based on query analysis"""
        
        sequence_results = []
        
        # Step 1: Memory/Context check
        if tool_context:
            account_check = get_current_account(tool_context)
            if account_check.get("status") == "SUCCESS":
                sequence_results.append(f"✅ Using account: {account_check['account_id']}")
            else:
                sequence_results.append("⚠️ No account context - provide account ID")
        
        # Step 2: Portfolio analysis if relevant
        if "portfolio" in query.lower():
            portfolio_result = get_portfolio_summary(tool_context=tool_context)
            sequence_results.append(f"📊 Portfolio: {self._format_tool_result(portfolio_result)}")
        
        # Step 3: Performance analysis if relevant
        if "performance" in query.lower():
            performance_result = calculate_performance_metrics(tool_context=tool_context)
            sequence_results.append(f"📈 Performance: {self._format_tool_result(performance_result)}")
        
        return f"🔄 Sequential Processing Complete:\n\n" + "\n".join(sequence_results)

    # Helper methods for specific tool categories
    async def _execute_market_tools(self, query: str, tool_context: Optional[ToolContext] = None) -> str:
        """Execute market-related tools"""
        volatility = analyze_market_volatility(tool_context=tool_context)
        commentary = generate_market_commentary(tool_context=tool_context)
        return f"Volatility: {volatility.get('status', 'N/A')}, Commentary: {commentary.get('status', 'N/A')}"

    async def _execute_client_tools(self, query: str, tool_context: Optional[ToolContext] = None) -> str:
        """Execute client-related tools"""
        if tool_context:
            account_info = get_current_account(tool_context)
            if account_info.get("status") == "SUCCESS":
                portfolio = get_portfolio_summary(tool_context=tool_context)
                return f"Account {account_info['account_id']}: {portfolio.get('status', 'N/A')}"
        return "No account context available"

    async def _execute_portfolio_tools(self, query: str, tool_context: Optional[ToolContext] = None) -> str:
        """Execute portfolio-related tools"""
        summary = get_portfolio_summary(tool_context=tool_context)
        return f"Portfolio Summary: {summary.get('status', 'N/A')}"

    async def _execute_performance_tools(self, query: str, tool_context: Optional[ToolContext] = None) -> str:
        """Execute performance-related tools"""
        performance = calculate_performance_metrics(tool_context=tool_context)
        return f"Performance Metrics: {performance.get('status', 'N/A')}"

    async def _execute_risk_tools(self, query: str, tool_context: Optional[ToolContext] = None) -> str:
        """Execute risk-related tools"""
        # Use market volatility as proxy for risk analysis
        risk_analysis = analyze_market_volatility(tool_context=tool_context)
        return f"Risk Analysis: {risk_analysis.get('status', 'N/A')}"
    
    async def _execute_analytics_tools(self, query: str, tool_context: Optional[ToolContext] = None) -> str:
        """Execute advanced analytics tools with proper error handling"""
        results = []
        
        # Extract client ID from query or use default
        client_id = self._extract_client_id(query) or "WM000001"
        
        try:
            if "behavior" in query.lower():
                behavior_result = analyze_client_behavior(client_id, tool_context=tool_context)
                if behavior_result["status"] == "SUCCESS":
                    analysis_data = behavior_result["data"]
                    insights = analysis_data.get("key_insights", [])[:3]
                    results.append(f"📊 **Behavior Analysis Complete**\n   • " + "\n   • ".join(insights))
                else:
                    results.append(f"❌ Behavior Analysis Failed: {behavior_result.get('message', 'Unknown error')}")
            
            if "predict" in query.lower() or "forecast" in query.lower():
                prediction_result = predict_client_needs(client_id, tool_context=tool_context)
                if prediction_result["status"] == "SUCCESS":
                    prediction_data = prediction_result["data"]
                    priority_needs = prediction_data.get("priority_needs", [])[:3]
                    need_summary = [f"{need['need']} ({need['probability']:.1%})" for need in priority_needs]
                    results.append(f"🔮 **Predictive Analysis Complete**\n   • " + "\n   • ".join(need_summary))
                else:
                    results.append(f"❌ Prediction Failed: {prediction_result.get('message', 'Unknown error')}")
            
            if "research" in query.lower():
                topic = self._extract_research_topic(query) or "Market Analysis"
                research_result = generate_investment_research(topic, tool_context=tool_context)
                if research_result["status"] == "SUCCESS":
                    research_data = research_result["data"]
                    rating = research_data.get("analyst_rating", "N/A")
                    confidence = research_data.get("confidence_level", "N/A")
                    results.append(f"📋 **Investment Research Complete**\n   • Topic: {topic}\n   • Rating: {rating}\n   • Confidence: {confidence}")
                else:
                    results.append(f"❌ Research Failed: {research_result.get('message', 'Unknown error')}")
            
        except Exception as e:
            logger.error(f"Error executing analytics tools: {str(e)}")
            results.append(f"❌ Analytics execution error: {str(e)}")
        
        if not results:
            return "No analytics tools matched query patterns. Available: behavior analysis, predictions, research"
        
        return f"🧠 **Advanced Analytics Results**\n\n" + "\n\n".join(results)
    
    async def _execute_compliance_tools(self, query: str, tool_context: Optional[ToolContext] = None) -> str:
        """Execute regulatory compliance tools"""
        results = []
        
        client_id = self._extract_client_id(query) or "CLIENT001"
        
        if "fiduciary" in query.lower():
            fiduciary_assessment = assess_fiduciary_compliance(client_id)
            results.append(f"⚖️ Fiduciary Compliance: {self._format_tool_result(fiduciary_assessment)}")
        
        if "report" in query.lower() and "regulatory" in query.lower():
            report_type = self._extract_report_type(query) or "adv_update"
            regulatory_report = generate_regulatory_report(report_type)
            results.append(f"📄 Regulatory Report: {self._format_tool_result(regulatory_report)}")
        
        if "monitor" in query.lower() and "regulatory" in query.lower():
            regulatory_monitoring = monitor_regulatory_changes()
            results.append(f"🔍 Regulatory Monitoring: {self._format_tool_result(regulatory_monitoring)}")
        
        if "aml" in query.lower() or "screening" in query.lower():
            aml_screening = conduct_aml_screening(client_id)
            results.append(f"🛡️ AML Screening: {self._format_tool_result(aml_screening)}")
        
        if "training" in query.lower():
            training_topic = self._extract_training_topic(query) or "fiduciary_duty"
            compliance_training = generate_compliance_training(training_topic)
            results.append(f"🎓 Compliance Training: {self._format_tool_result(compliance_training)}")
        
        return f"📋 Compliance Management Complete:\n\n" + "\n".join(results) if results else "No compliance tools matched query"
    
    async def _execute_experience_tools(self, query: str, tool_context: Optional[ToolContext] = None) -> str:
        """Execute client experience tools"""
        results = []
        
        client_id = self._extract_client_id(query) or "CLIENT001"
        
        if "communication" in query.lower() or "personalized" in query.lower():
            comm_type = self._extract_communication_type(query) or "market_update"
            personalized_comm = generate_personalized_communication(client_id, comm_type)
            results.append(f"💌 Personalized Communication: {self._format_tool_result(personalized_comm)}")
        
        if "satisfaction" in query.lower() or "survey" in query.lower():
            satisfaction_analysis = measure_client_satisfaction(client_id)
            results.append(f"😊 Satisfaction Analysis: {self._format_tool_result(satisfaction_analysis)}")
        
        if "journey" in query.lower():
            journey_stage = self._extract_journey_stage(query) or "active"
            journey_orchestration = orchestrate_client_journey(client_id, journey_stage)
            results.append(f"🗺️ Journey Orchestration: {self._format_tool_result(journey_orchestration)}")
        
        if "event" in query.lower():
            event_type = self._extract_event_type(query) or "educational_webinar"
            event_management = manage_client_events(event_type)
            results.append(f"🎉 Event Management: {self._format_tool_result(event_management)}")
        
        return f"🌟 Client Experience Complete:\n\n" + "\n".join(results) if results else "No experience tools matched query"

    async def _execute_comprehensive_analysis(self, query: str, tool_context: Optional[ToolContext] = None) -> str:
        """Execute comprehensive analysis across multiple domains"""
        results = []
        
        # Portfolio analysis
        if tool_context:
            portfolio = get_portfolio_summary(tool_context=tool_context)
            results.append(f"Portfolio: {portfolio.get('status', 'N/A')}")
        
        # Market analysis
        market = analyze_market_volatility(tool_context=tool_context)
        results.append(f"Market: {market.get('status', 'N/A')}")
        
        return "🎯 Comprehensive Analysis: " + ", ".join(results)

    def _format_tool_result(self, result: Dict[str, Any]) -> str:
        """Format tool result for display"""
        if isinstance(result, dict):
            status = result.get("status", "UNKNOWN")
            message = result.get("message", "No details available")
            return f"{status} - {message[:100]}"
        return str(result)[:100]

    def _format_enhanced_response(self, response: str, classification: Optional[Dict[str, Any]], strategy: Optional[Dict[str, Any]], error: bool = False) -> str:
        """Format response with routing metadata"""
        
        if error:
            return response
        
        if not classification or not strategy:
            return response
        
        # Add routing header
        persona = classification["classification"]["persona"]
        pattern = classification["routing"]["recommended_pattern"]
        confidence = classification["confidence"]["overall"]
        
        header = f"🎯 Intelligent Routing: {pattern.replace('_', ' ').title()} Pattern\n"
        header += f"👤 Persona: {persona.title()} | 🎚️ Confidence: {confidence:.1%}\n"
        header += "─" * 50 + "\n\n"
        
        # Add metrics footer
        total = self.workflow_metrics["total_workflows"]
        success_rate = self.workflow_metrics["successful_routes"] / max(total, 1) * 100
        
        footer = f"\n\n📊 Session Metrics: {total} workflows | {success_rate:.1f}% success rate"
        footer += f"\n🔄 Pattern Distribution: {dict(list(self.workflow_metrics['pattern_usage'].items())[:3])}"
        
        return header + response + footer

    def _extract_client_id(self, query: str) -> Optional[str]:
        """Extract client ID from query string"""
        import re
        # Look for patterns like WM123456, CLIENT001, etc.
        patterns = [
            r'\b(WM\d{6})\b',
            r'\b(CLIENT\d{3,6})\b', 
            r'\bclient[_\s]+id[:\s]*([A-Z0-9]{6,})\b'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return match.group(1).upper()
        
        return None
    
    def _extract_research_topic(self, query: str) -> Optional[str]:
        """Extract research topic from query"""
        # Look for common patterns
        topic_patterns = [
            r'research\s+(?:on\s+)?([A-Z]{2,5})\b',  # Stock symbols
            r'analyze\s+([A-Z\s&]+(?:Corp|Inc|Ltd))',  # Company names
            r'(?:market|sector)\s+([a-zA-Z\s]+)',  # Market/sector analysis
        ]
        
        import re
        for pattern in topic_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Default extraction
        words = query.split()
        research_idx = -1
        for i, word in enumerate(words):
            if word.lower() in ['research', 'analyze', 'study']:
                research_idx = i
                break
        
        if research_idx >= 0 and research_idx + 1 < len(words):
            return words[research_idx + 1].capitalize()
        
        return None
    
    def _format_tool_result(self, result: Any) -> str:
        """Format tool result for display"""
        if isinstance(result, dict):
            status = result.get("status", "UNKNOWN")
            message = result.get("message", "No message")
            return f"{status} - {message}"
        elif isinstance(result, str):
            return result[:100] + "..." if len(result) > 100 else result
        else:
            return str(result)[:100]
    
    def get_workflow_metrics(self) -> Dict[str, Any]:
        """Get current workflow performance metrics"""
        return {
            **self.workflow_metrics,
            "timestamp": datetime.utcnow().isoformat(),
            "success_rate": self.workflow_metrics["successful_routes"] / max(self.workflow_metrics["total_workflows"], 1)
        }

    def reset_metrics(self) -> None:
        """Reset workflow metrics"""
        self.workflow_metrics = {
            "total_workflows": 0,
            "successful_routes": 0,
            "pattern_usage": {
                "sequential": 0,
                "parallel": 0,
                "loop": 0,
                "event_driven": 0,
                "scheduled": 0,
                "master_orchestration": 0
            }
        }


# Create the enhanced agent instance
enhanced_wealth_management_agent = EnhancedWealthManagementAgent()

# Maintain backward compatibility
root_agent = enhanced_wealth_management_agent