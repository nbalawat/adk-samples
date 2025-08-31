"""Workflow classification and routing system for wealth management agents"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import re


class WorkflowClassifier:
    """
    Sophisticated workflow classification system that analyzes queries and routes them
    to the appropriate ADK patterns and specialized agents based on:
    - Persona (Advisor, Client, Operations)
    - Urgency (Critical, High, Medium, Low)  
    - Complexity (Simple, Complex, Multi-step, Orchestration)
    - Trigger Type (Event-driven, Scheduled, Manual, Threshold)
    """

    def __init__(self):
        self.persona_keywords = {
            "advisor": ["advisor", "adviser", "meeting", "client call", "review", "analysis", "recommendation"],
            "client": ["client", "customer", "my portfolio", "my account", "i want", "help me", "show me"],
            "operations": ["operations", "ops", "compliance", "trade", "settlement", "processing", "system"]
        }
        
        self.urgency_keywords = {
            "critical": ["emergency", "urgent", "critical", "immediately", "crisis", "panic", "breaking"],
            "high": ["important", "priority", "asap", "soon", "today", "now", "significant"],
            "medium": ["review", "analyze", "update", "check", "moderate"],
            "low": ["when convenient", "sometime", "eventually", "minor", "optional"]
        }
        
        self.complexity_keywords = {
            "simple": ["show", "display", "get", "retrieve", "simple", "quick", "basic"],
            "complex": ["analyze", "calculate", "assess", "evaluate", "comprehensive", "detailed"],
            "multi_step": ["workflow", "process", "sequence", "step by step", "orchestrate", "coordinate"],
            "orchestration": ["multiple", "all", "everyone", "coordination", "crisis", "company-wide"]
        }
        
        self.trigger_keywords = {
            "event_driven": ["threshold", "alert", "trigger", "breach", "exceed", "volatility", "news", "event"],
            "scheduled": ["daily", "weekly", "monthly", "quarterly", "annual", "recurring", "scheduled"],
            "manual": ["request", "please", "can you", "help", "i need", "manual"],
            "threshold": ["above", "below", "over", "under", "limit", "boundary", "range"]
        }

        # Workflow pattern mappings from the CSV
        self.workflow_patterns = {
            # Sequential patterns
            "client_meeting_prep": "sequential",
            "market_response": "sequential", 
            "crisis_management": "sequential",
            "regulatory_response": "sequential",
            "transaction_processing": "sequential",
            
            # Parallel patterns
            "client_onboarding": "parallel",
            "campaign_management": "parallel",
            "performance_reporting": "parallel",
            "compliance_scanning": "parallel",
            "multi_client_outreach": "parallel",
            
            # Loop patterns
            "portfolio_monitoring": "loop",
            "risk_assessment": "loop",
            "market_monitoring": "loop",
            "continuous_compliance": "loop",
            
            # Event-driven patterns
            "market_volatility": "event_driven",
            "risk_breach": "event_driven",
            "news_impact": "event_driven",
            "threshold_alerts": "event_driven",
            
            # Scheduled patterns
            "reporting_cycle": "scheduled",
            "planning_process": "scheduled",
            "review_meetings": "scheduled",
            "compliance_deadlines": "scheduled",
            
            # Master orchestration
            "multi_persona_crisis": "master_orchestration",
            "business_continuity": "master_orchestration",
            "system_implementation": "master_orchestration",
            "annual_planning": "master_orchestration"
        }

    def classify_workflow(self, query: str) -> Dict[str, Any]:
        """
        Classify a query into workflow categories and determine routing strategy.
        
        Args:
            query: User input query
            
        Returns:
            Classification results with routing recommendations
        """
        
        # Analyze query characteristics
        persona = self._classify_persona(query)
        urgency = self._classify_urgency(query)
        complexity = self._classify_complexity(query)
        trigger_type = self._classify_trigger_type(query)
        
        # Determine specific workflow type
        workflow_type = self._determine_workflow_type(query, persona, urgency, complexity, trigger_type)
        
        # Get recommended pattern
        recommended_pattern = self._get_recommended_pattern(workflow_type, complexity, urgency)
        
        # Calculate confidence scores
        confidence = self._calculate_confidence_score(query, persona, urgency, complexity, trigger_type)
        
        # Generate routing recommendations
        routing = self._generate_routing_recommendations(
            recommended_pattern, persona, urgency, complexity, workflow_type
        )
        
        return {
            "classification": {
                "persona": persona,
                "urgency": urgency, 
                "complexity": complexity,
                "trigger_type": trigger_type,
                "workflow_type": workflow_type
            },
            "routing": {
                "recommended_pattern": recommended_pattern,
                "agent_type": routing["agent_type"],
                "priority_queue": routing["priority_queue"],
                "execution_mode": routing["execution_mode"]
            },
            "confidence": confidence,
            "metadata": {
                "classified_at": datetime.utcnow().isoformat(),
                "query_length": len(query),
                "keywords_matched": self._get_matched_keywords(query)
            }
        }

    def _classify_persona(self, query: str) -> str:
        """Classify the primary persona for the query"""
        query_lower = query.lower()
        persona_scores = {}
        
        for persona, keywords in self.persona_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                persona_scores[persona] = score
        
        if not persona_scores:
            # Default classification based on query patterns
            if any(word in query_lower for word in ["my", "i", "help me", "show me"]):
                return "client"
            elif any(word in query_lower for word in ["client", "review", "analyze"]):
                return "advisor"
            else:
                return "operations"
        
        return max(persona_scores, key=persona_scores.get)

    def _classify_urgency(self, query: str) -> str:
        """Classify the urgency level of the query"""
        query_lower = query.lower()
        urgency_scores = {}
        
        for urgency, keywords in self.urgency_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                urgency_scores[urgency] = score
        
        if not urgency_scores:
            return "medium"  # Default urgency
        
        return max(urgency_scores, key=urgency_scores.get)

    def _classify_complexity(self, query: str) -> str:
        """Classify the complexity level of the query"""
        query_lower = query.lower()
        complexity_scores = {}
        
        for complexity, keywords in self.complexity_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                complexity_scores[complexity] = score
        
        # Additional complexity indicators
        if len(query.split()) > 20:  # Long queries often indicate complexity
            complexity_scores["complex"] = complexity_scores.get("complex", 0) + 1
        
        if "and" in query_lower and query_lower.count("and") > 2:  # Multiple requirements
            complexity_scores["multi_step"] = complexity_scores.get("multi_step", 0) + 1
        
        if not complexity_scores:
            return "simple"  # Default complexity
        
        return max(complexity_scores, key=complexity_scores.get)

    def _classify_trigger_type(self, query: str) -> str:
        """Classify the trigger type for the query"""
        query_lower = query.lower()
        trigger_scores = {}
        
        for trigger, keywords in self.trigger_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                trigger_scores[trigger] = score
        
        if not trigger_scores:
            return "manual"  # Default trigger type
        
        return max(trigger_scores, key=trigger_scores.get)

    def _determine_workflow_type(self, query: str, persona: str, urgency: str, complexity: str, trigger_type: str) -> str:
        """Determine the specific workflow type based on classification"""
        query_lower = query.lower()
        
        # Market-related workflows
        if any(word in query_lower for word in ["market", "volatility", "crash", "s&p", "dow", "nasdaq"]):
            if urgency in ["critical", "high"]:
                return "market_response"
            else:
                return "market_monitoring"
        
        # Client-related workflows  
        if "onboarding" in query_lower or "new client" in query_lower:
            return "client_onboarding"
        elif "meeting" in query_lower or "review" in query_lower:
            return "client_meeting_prep"
        
        # Crisis-related workflows
        if any(word in query_lower for word in ["crisis", "panic", "emergency", "urgent"]):
            if complexity in ["multi_step", "orchestration"]:
                return "multi_persona_crisis"
            else:
                return "crisis_management"
        
        # Portfolio-related workflows
        if any(word in query_lower for word in ["portfolio", "performance", "allocation", "rebalancing"]):
            if trigger_type == "scheduled":
                return "performance_reporting"
            else:
                return "portfolio_monitoring"
        
        # Compliance-related workflows
        if "compliance" in query_lower or "regulatory" in query_lower:
            if trigger_type == "scheduled":
                return "compliance_deadlines"
            else:
                return "continuous_compliance"
        
        # Risk-related workflows
        if "risk" in query_lower:
            if "breach" in query_lower or "exceed" in query_lower:
                return "risk_breach"
            else:
                return "risk_assessment"
        
        # Reporting workflows
        if any(word in query_lower for word in ["report", "daily", "weekly", "monthly", "quarterly"]):
            return "reporting_cycle"
        
        # Campaign workflows
        if any(word in query_lower for word in ["campaign", "marketing", "outreach", "communication"]):
            return "campaign_management"
        
        # Transaction workflows
        if any(word in query_lower for word in ["trade", "transaction", "buy", "sell", "order"]):
            return "transaction_processing"
        
        # Default workflow type
        if persona == "client":
            return "client_service"
        elif persona == "advisor":
            return "advisor_support"
        else:
            return "operations_support"

    def _get_recommended_pattern(self, workflow_type: str, complexity: str, urgency: str) -> str:
        """Get the recommended ADK pattern for the workflow"""
        
        # Check if workflow type has a specific pattern mapping
        if workflow_type in self.workflow_patterns:
            return self.workflow_patterns[workflow_type]
        
        # Fall back to complexity-based pattern selection
        if complexity == "orchestration":
            return "master_orchestration"
        elif complexity == "multi_step":
            return "sequential"
        elif urgency in ["critical", "high"] and complexity == "complex":
            return "parallel"
        else:
            return "sequential"  # Default pattern

    def _generate_routing_recommendations(self, pattern: str, persona: str, urgency: str, complexity: str, workflow_type: str) -> Dict[str, str]:
        """Generate routing recommendations based on classification"""
        
        # Determine agent type
        if pattern == "event_driven":
            agent_type = "EventDrivenAgent"
        elif pattern == "scheduled":
            agent_type = "ScheduledAgent"
        elif pattern == "master_orchestration":
            agent_type = "MasterOrchestrator"
        elif pattern == "parallel":
            agent_type = "ClientOnboardingAgent"  # Best parallel example
        elif pattern == "loop":
            agent_type = "PortfolioMonitoringAgent"
        else:
            # Sequential patterns
            if "market" in workflow_type:
                agent_type = "MarketResponseAgent"
            elif "crisis" in workflow_type:
                agent_type = "CrisisManagementAgent"
            else:
                agent_type = "SequentialAgent"
        
        # Determine priority queue
        priority_queue = {
            "critical": "immediate",
            "high": "priority",
            "medium": "standard", 
            "low": "batch"
        }.get(urgency, "standard")
        
        # Determine execution mode
        if complexity == "orchestration":
            execution_mode = "orchestrated"
        elif urgency in ["critical", "high"]:
            execution_mode = "expedited"
        elif pattern == "parallel":
            execution_mode = "concurrent"
        else:
            execution_mode = "standard"
        
        return {
            "agent_type": agent_type,
            "priority_queue": priority_queue,
            "execution_mode": execution_mode
        }

    def _calculate_confidence_score(self, query: str, persona: str, urgency: str, complexity: str, trigger_type: str) -> Dict[str, float]:
        """Calculate confidence scores for each classification"""
        
        query_lower = query.lower()
        
        # Calculate persona confidence
        persona_matches = sum(1 for keyword in self.persona_keywords[persona] if keyword in query_lower)
        persona_confidence = min(persona_matches / 3.0, 1.0)  # Normalize to 0-1
        
        # Calculate urgency confidence
        urgency_matches = sum(1 for keyword in self.urgency_keywords[urgency] if keyword in query_lower)
        urgency_confidence = min(urgency_matches / 2.0, 1.0)
        
        # Calculate complexity confidence
        complexity_matches = sum(1 for keyword in self.complexity_keywords[complexity] if keyword in query_lower)
        complexity_confidence = min(complexity_matches / 2.0, 1.0)
        
        # Calculate trigger confidence  
        trigger_matches = sum(1 for keyword in self.trigger_keywords[trigger_type] if keyword in query_lower)
        trigger_confidence = min(trigger_matches / 2.0, 1.0)
        
        # Overall confidence
        overall_confidence = (persona_confidence + urgency_confidence + complexity_confidence + trigger_confidence) / 4.0
        
        return {
            "overall": round(overall_confidence, 3),
            "persona": round(persona_confidence, 3),
            "urgency": round(urgency_confidence, 3), 
            "complexity": round(complexity_confidence, 3),
            "trigger_type": round(trigger_confidence, 3)
        }

    def _get_matched_keywords(self, query: str) -> Dict[str, List[str]]:
        """Get all matched keywords by category"""
        query_lower = query.lower()
        matched = {}
        
        # Persona keywords
        matched["persona"] = [kw for kw_list in self.persona_keywords.values() for kw in kw_list if kw in query_lower]
        
        # Urgency keywords  
        matched["urgency"] = [kw for kw_list in self.urgency_keywords.values() for kw in kw_list if kw in query_lower]
        
        # Complexity keywords
        matched["complexity"] = [kw for kw_list in self.complexity_keywords.values() for kw in kw_list if kw in query_lower]
        
        # Trigger keywords
        matched["trigger"] = [kw for kw_list in self.trigger_keywords.values() for kw in kw_list if kw in query_lower]
        
        return matched


class WorkflowRouter:
    """
    Advanced workflow router that uses classification results to route queries
    to the appropriate agents and execution patterns.
    """
    
    def __init__(self):
        self.classifier = WorkflowClassifier()
        self.agent_registry = {
            "EventDrivenAgent": "wealth_management.sub_agents.event_driven_agent.EventDrivenAgent",
            "ScheduledAgent": "wealth_management.sub_agents.scheduled_agent.ScheduledAgent", 
            "MasterOrchestrator": "wealth_management.sub_agents.master_orchestrator.MasterOrchestrator",
            "MarketResponseAgent": "wealth_management.sub_agents.market_response_agent.MarketResponseAgent",
            "CrisisManagementAgent": "wealth_management.sub_agents.crisis_management_agent.CrisisManagementAgent",
            "ClientOnboardingAgent": "wealth_management.sub_agents.client_onboarding_agent.ClientOnboardingAgent",
            "PortfolioMonitoringAgent": "wealth_management.sub_agents.portfolio_monitoring_agent.PortfolioMonitoringAgent"
        }
        
    def route_query(self, query: str) -> Dict[str, Any]:
        """
        Route a query to the appropriate agent based on classification.
        
        Args:
            query: User input query
            
        Returns:
            Routing decision with agent selection and execution parameters
        """
        
        # Classify the workflow
        classification = self.classifier.classify_workflow(query)
        
        # Determine routing strategy
        routing_strategy = self._determine_routing_strategy(classification)
        
        # Prepare execution context
        execution_context = self._prepare_execution_context(classification, query)
        
        return {
            "classification": classification,
            "routing_strategy": routing_strategy,
            "execution_context": execution_context,
            "routed_at": datetime.utcnow().isoformat()
        }
    
    def _determine_routing_strategy(self, classification: Dict[str, Any]) -> Dict[str, Any]:
        """Determine the optimal routing strategy"""
        
        routing = classification["routing"]
        recommended_pattern = routing["recommended_pattern"]
        
        # Advanced routing logic based on pattern
        if recommended_pattern == "master_orchestration":
            strategy = {
                "type": "orchestrated",
                "primary_agent": routing["agent_type"],
                "coordination_required": True,
                "sub_agents": ["market_response", "crisis_management", "client_onboarding"],
                "execution_order": "intelligent_routing"
            }
        elif recommended_pattern == "parallel":
            strategy = {
                "type": "concurrent",
                "primary_agent": routing["agent_type"], 
                "parallel_execution": True,
                "max_concurrency": 4,
                "execution_order": "simultaneous"
            }
        elif recommended_pattern == "event_driven":
            strategy = {
                "type": "reactive",
                "primary_agent": routing["agent_type"],
                "trigger_based": True,
                "monitoring_required": True,
                "execution_order": "immediate"
            }
        elif recommended_pattern == "scheduled":
            strategy = {
                "type": "scheduled",
                "primary_agent": routing["agent_type"],
                "time_based": True,
                "recurring": True,
                "execution_order": "scheduled"
            }
        else:
            # Sequential or loop patterns
            strategy = {
                "type": "sequential",
                "primary_agent": routing["agent_type"],
                "step_by_step": True,
                "validation_required": True,
                "execution_order": "ordered"
            }
        
        return strategy
    
    def _prepare_execution_context(self, classification: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Prepare execution context for the routed workflow"""
        
        persona = classification["classification"]["persona"]
        urgency = classification["classification"]["urgency"]
        complexity = classification["classification"]["complexity"]
        
        return {
            "query": query,
            "persona": persona,
            "urgency_level": urgency,
            "complexity_level": complexity,
            "priority": self._calculate_priority(urgency, complexity),
            "timeout": self._calculate_timeout(complexity),
            "retry_policy": self._get_retry_policy(urgency),
            "logging_level": "DEBUG" if complexity in ["multi_step", "orchestration"] else "INFO",
            "monitoring_enabled": urgency in ["critical", "high"]
        }
    
    def _calculate_priority(self, urgency: str, complexity: str) -> int:
        """Calculate numeric priority score"""
        urgency_scores = {"critical": 100, "high": 75, "medium": 50, "low": 25}
        complexity_bonus = {"orchestration": 20, "multi_step": 15, "complex": 10, "simple": 0}
        
        base_score = urgency_scores.get(urgency, 50)
        bonus = complexity_bonus.get(complexity, 0)
        
        return min(base_score + bonus, 100)
    
    def _calculate_timeout(self, complexity: str) -> int:
        """Calculate timeout in seconds based on complexity"""
        timeout_map = {
            "simple": 30,
            "complex": 120, 
            "multi_step": 300,
            "orchestration": 600
        }
        
        return timeout_map.get(complexity, 60)
    
    def _get_retry_policy(self, urgency: str) -> Dict[str, Any]:
        """Get retry policy based on urgency"""
        if urgency == "critical":
            return {"max_retries": 3, "backoff_factor": 1.0, "timeout_multiplier": 1.5}
        elif urgency == "high":
            return {"max_retries": 2, "backoff_factor": 1.5, "timeout_multiplier": 1.2}
        else:
            return {"max_retries": 1, "backoff_factor": 2.0, "timeout_multiplier": 1.0}