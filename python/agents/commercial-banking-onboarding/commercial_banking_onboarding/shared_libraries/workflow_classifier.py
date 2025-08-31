"""
Intelligent workflow classification system for commercial banking onboarding.
Analyzes requests to determine persona, urgency, complexity, and optimal routing.
"""

import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

class PersonaType(Enum):
    """Supported persona types"""
    OPERATIONS = "operations"
    CLIENT = "client" 
    COMPLIANCE = "compliance"
    LEGAL = "legal"
    MIXED = "mixed"

class UrgencyLevel(Enum):
    """Urgency classification levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ComplexityLevel(Enum):
    """Workflow complexity levels"""
    SIMPLE = "simple"
    COMPLEX = "complex"
    MULTI_STEP = "multi_step"
    ORCHESTRATION = "orchestration"

class WorkflowPattern(Enum):
    """ADK workflow patterns"""
    INDIVIDUAL_TOOLS = "individual_tools"
    SEQUENTIAL_AGENT = "sequential_agent"
    PARALLEL_AGENT = "parallel_agent"
    LOOP_AGENT = "loop_agent"
    MULTI_PERSONA_COORDINATION = "multi_persona_coordination"

@dataclass
class WorkflowClassification:
    """Complete workflow classification result"""
    persona: PersonaType
    urgency: UrgencyLevel
    complexity: ComplexityLevel
    trigger_type: str
    workflow_type: str
    recommended_pattern: WorkflowPattern
    agent_type: str
    priority_queue: str
    execution_mode: str
    confidence_score: float

class WorkflowClassifier:
    """
    Sophisticated workflow classification system for commercial banking onboarding.
    
    Analyzes incoming requests to determine:
    - Primary persona (Operations, Client, Compliance, Legal)
    - Urgency level (Critical, High, Medium, Low)
    - Complexity level (Simple, Complex, Multi-step, Orchestration)
    - Optimal ADK pattern (Individual, Sequential, Parallel, Loop, Multi-persona)
    """
    
    def __init__(self):
        self._initialize_classification_patterns()
    
    def _initialize_classification_patterns(self):
        """Initialize classification patterns and keywords"""
        
        # Persona identification patterns
        self.persona_keywords = {
            PersonaType.OPERATIONS: {
                "primary": [
                    "process", "workflow", "system", "processing", "operations", 
                    "efficiency", "metrics", "status", "coordination", "routing",
                    "queue", "processing time", "bottleneck", "optimization"
                ],
                "roles": [
                    "operations manager", "processor", "coordinator", "workflow manager",
                    "operations specialist", "process manager"
                ],
                "actions": [
                    "process application", "coordinate workflow", "track status",
                    "optimize process", "manage queue", "route request"
                ]
            },
            PersonaType.CLIENT: {
                "primary": [
                    "my business", "my company", "we need", "we want", "client",
                    "customer", "business owner", "CFO", "treasurer", "our account",
                    "business requirements", "service", "relationship", "experience"
                ],
                "roles": [
                    "business owner", "CEO", "CFO", "treasurer", "decision maker",
                    "business manager", "company representative"
                ],
                "actions": [
                    "open account", "need banking services", "want to apply",
                    "business banking", "commercial account", "banking relationship"
                ]
            },
            PersonaType.COMPLIANCE: {
                "primary": [
                    "compliance", "risk", "regulatory", "AML", "KYC", "sanctions",
                    "due diligence", "verification", "screening", "monitoring",
                    "BSA", "CRA", "OFAC", "beneficial ownership", "PEP"
                ],
                "roles": [
                    "compliance officer", "risk analyst", "AML officer", 
                    "regulatory specialist", "compliance analyst", "risk manager"
                ],
                "actions": [
                    "conduct screening", "assess risk", "verify compliance",
                    "perform due diligence", "monitor transactions", "review compliance"
                ]
            },
            PersonaType.LEGAL: {
                "primary": [
                    "legal", "documentation", "contract", "agreement", "filing",
                    "regulatory filing", "legal document", "terms", "conditions",
                    "signature", "execution", "legal review", "counsel"
                ],
                "roles": [
                    "legal counsel", "attorney", "legal specialist",
                    "documentation specialist", "regulatory affairs"
                ],
                "actions": [
                    "prepare documents", "legal review", "execute contract",
                    "file regulatory", "legal documentation", "contract management"
                ]
            }
        }
        
        # Urgency level patterns
        self.urgency_keywords = {
            UrgencyLevel.CRITICAL: [
                "emergency", "urgent", "critical", "immediately", "crisis",
                "panic", "escalate", "ASAP", "red flag", "violation",
                "regulatory violation", "compliance failure", "system down"
            ],
            UrgencyLevel.HIGH: [
                "important", "priority", "soon", "today", "this week",
                "high priority", "expedite", "fast track", "deadline",
                "time sensitive", "client escalation"
            ],
            UrgencyLevel.MEDIUM: [
                "review", "analyze", "update", "check", "moderate",
                "standard timeline", "normal processing", "routine"
            ],
            UrgencyLevel.LOW: [
                "when convenient", "sometime", "eventually", "minor",
                "low priority", "backlog", "future consideration"
            ]
        }
        
        # Complexity level patterns
        self.complexity_keywords = {
            ComplexityLevel.SIMPLE: [
                "show", "display", "get", "retrieve", "simple", "quick",
                "basic", "straightforward", "single", "one", "just"
            ],
            ComplexityLevel.COMPLEX: [
                "analyze", "calculate", "assess", "evaluate", "comprehensive",
                "detailed", "thorough", "complete", "full", "extensive"
            ],
            ComplexityLevel.MULTI_STEP: [
                "workflow", "process", "sequence", "step by step", "stages",
                "phases", "multiple steps", "end-to-end", "complete process"
            ],
            ComplexityLevel.ORCHESTRATION: [
                "multiple", "all", "everyone", "coordination", "crisis",
                "enterprise", "organization-wide", "cross-functional", "complex coordination"
            ]
        }
        
        # Workflow type patterns
        self.workflow_type_patterns = {
            "client_onboarding": [
                "new client", "onboard", "open account", "new business",
                "application", "business account", "commercial account"
            ],
            "compliance_review": [
                "compliance review", "risk assessment", "due diligence",
                "AML screening", "KYC verification", "sanctions check"
            ],
            "document_processing": [
                "document", "paperwork", "forms", "signature", "upload",
                "file", "documentation", "contracts", "agreements"
            ],
            "credit_assessment": [
                "credit", "loan", "financing", "creditworthiness", "financial analysis",
                "credit score", "risk rating", "lending", "credit facility"
            ],
            "account_management": [
                "account setup", "product configuration", "service activation",
                "account modification", "product selection", "banking products"
            ],
            "crisis_management": [
                "crisis", "emergency", "escalation", "complaint", "issue",
                "problem", "urgent matter", "critical situation"
            ],
            "monitoring": [
                "monitor", "track", "status", "progress", "ongoing",
                "continuous", "watch", "observe", "surveillance"
            ]
        }

    def classify_workflow(self, query: str) -> Dict[str, Any]:
        """
        Classify a query into workflow categories and determine routing strategy.
        
        Args:
            query: The input query/request to classify
            
        Returns:
            Dict containing classification results and routing recommendations
        """
        query_lower = query.lower()
        
        # Classify each dimension
        persona = self._classify_persona(query_lower)
        urgency = self._classify_urgency(query_lower)
        complexity = self._classify_complexity(query_lower)
        trigger_type = self._classify_trigger_type(query_lower)
        workflow_type = self._determine_workflow_type(query_lower)
        
        # Determine optimal ADK pattern
        recommended_pattern = self._get_recommended_pattern(workflow_type, complexity, urgency)
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(query_lower, persona, urgency, complexity)
        
        # Create classification result
        classification = WorkflowClassification(
            persona=persona,
            urgency=urgency,
            complexity=complexity,
            trigger_type=trigger_type,
            workflow_type=workflow_type,
            recommended_pattern=recommended_pattern,
            agent_type=self._get_agent_type(recommended_pattern, workflow_type),
            priority_queue=self._get_priority_queue(urgency),
            execution_mode=self._get_execution_mode(complexity, urgency),
            confidence_score=confidence_score
        )
        
        return {
            "classification": {
                "persona": classification.persona.value,
                "urgency": classification.urgency.value,
                "complexity": classification.complexity.value,
                "trigger_type": classification.trigger_type,
                "workflow_type": classification.workflow_type,
                "confidence_score": classification.confidence_score
            },
            "routing": {
                "recommended_pattern": classification.recommended_pattern.value,
                "agent_type": classification.agent_type,
                "priority_queue": classification.priority_queue,
                "execution_mode": classification.execution_mode
            }
        }

    def _classify_persona(self, query: str) -> PersonaType:
        """Classify the primary persona based on query content"""
        persona_scores = {}
        
        for persona, patterns in self.persona_keywords.items():
            score = 0
            
            # Check primary keywords
            for keyword in patterns["primary"]:
                if keyword in query:
                    score += 3
            
            # Check role keywords  
            for role in patterns["roles"]:
                if role in query:
                    score += 5
                    
            # Check action keywords
            for action in patterns["actions"]:
                if action in query:
                    score += 4
            
            persona_scores[persona] = score
        
        # Find highest scoring persona
        if not persona_scores or max(persona_scores.values()) == 0:
            return PersonaType.CLIENT  # Default to client
            
        max_persona = max(persona_scores, key=persona_scores.get)
        
        # Check for mixed persona scenarios
        top_scores = sorted(persona_scores.values(), reverse=True)
        if len(top_scores) > 1 and top_scores[1] > top_scores[0] * 0.7:
            return PersonaType.MIXED
            
        return max_persona

    def _classify_urgency(self, query: str) -> UrgencyLevel:
        """Classify urgency level based on query content"""
        for urgency, keywords in self.urgency_keywords.items():
            for keyword in keywords:
                if keyword in query:
                    return urgency
        return UrgencyLevel.MEDIUM  # Default urgency

    def _classify_complexity(self, query: str) -> ComplexityLevel:
        """Classify complexity level based on query content"""
        complexity_scores = {}
        
        for complexity, keywords in self.complexity_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query)
            complexity_scores[complexity] = score
        
        if not complexity_scores or max(complexity_scores.values()) == 0:
            return ComplexityLevel.SIMPLE  # Default complexity
            
        return max(complexity_scores, key=complexity_scores.get)

    def _classify_trigger_type(self, query: str) -> str:
        """Classify the trigger type of the request"""
        trigger_patterns = {
            "user_request": ["i want", "can you", "please", "help me", "i need"],
            "system_event": ["alert", "notification", "triggered", "detected", "system"],
            "scheduled": ["daily", "weekly", "monthly", "scheduled", "recurring"],
            "exception": ["error", "failed", "exception", "issue", "problem"],
            "escalation": ["escalate", "urgent", "critical", "emergency", "priority"]
        }
        
        for trigger_type, patterns in trigger_patterns.items():
            if any(pattern in query for pattern in patterns):
                return trigger_type
                
        return "user_request"  # Default trigger type

    def _determine_workflow_type(self, query: str) -> str:
        """Determine the primary workflow type"""
        workflow_scores = {}
        
        for workflow_type, patterns in self.workflow_type_patterns.items():
            score = sum(2 if pattern in query else 0 for pattern in patterns)
            workflow_scores[workflow_type] = score
        
        if not workflow_scores or max(workflow_scores.values()) == 0:
            return "general_inquiry"  # Default workflow type
            
        return max(workflow_scores, key=workflow_scores.get)

    def _get_recommended_pattern(self, workflow_type: str, complexity: ComplexityLevel, urgency: UrgencyLevel) -> WorkflowPattern:
        """Determine the recommended ADK pattern based on classification"""
        
        # Crisis scenarios use multi-persona coordination
        if urgency == UrgencyLevel.CRITICAL or workflow_type == "crisis_management":
            return WorkflowPattern.MULTI_PERSONA_COORDINATION
        
        # Monitoring workflows use loop pattern
        if workflow_type == "monitoring":
            return WorkflowPattern.LOOP_AGENT
            
        # Complex multi-step workflows
        if complexity == ComplexityLevel.ORCHESTRATION:
            return WorkflowPattern.MULTI_PERSONA_COORDINATION
        elif complexity == ComplexityLevel.MULTI_STEP:
            if workflow_type in ["compliance_review", "document_processing"]:
                return WorkflowPattern.SEQUENTIAL_AGENT
            else:
                return WorkflowPattern.PARALLEL_AGENT
        elif complexity == ComplexityLevel.COMPLEX:
            return WorkflowPattern.PARALLEL_AGENT
        else:
            return WorkflowPattern.INDIVIDUAL_TOOLS

    def _get_agent_type(self, pattern: WorkflowPattern, workflow_type: str) -> str:
        """Get the specific agent type based on pattern and workflow"""
        agent_mapping = {
            WorkflowPattern.INDIVIDUAL_TOOLS: f"individual_tools_{workflow_type}",
            WorkflowPattern.SEQUENTIAL_AGENT: "compliance_review_sequential_agent" if "compliance" in workflow_type else "sequential_processing_agent",
            WorkflowPattern.PARALLEL_AGENT: "business_onboarding_parallel_agent",
            WorkflowPattern.LOOP_AGENT: "application_monitoring_loop_agent",
            WorkflowPattern.MULTI_PERSONA_COORDINATION: "crisis_management_orchestrator"
        }
        
        return agent_mapping.get(pattern, "enhanced_commercial_banking_orchestrator")

    def _get_priority_queue(self, urgency: UrgencyLevel) -> str:
        """Get priority queue based on urgency"""
        queue_mapping = {
            UrgencyLevel.CRITICAL: "critical_queue",
            UrgencyLevel.HIGH: "high_priority_queue", 
            UrgencyLevel.MEDIUM: "standard_queue",
            UrgencyLevel.LOW: "low_priority_queue"
        }
        return queue_mapping[urgency]

    def _get_execution_mode(self, complexity: ComplexityLevel, urgency: UrgencyLevel) -> str:
        """Get execution mode based on complexity and urgency"""
        if urgency == UrgencyLevel.CRITICAL:
            return "immediate_execution"
        elif complexity in [ComplexityLevel.ORCHESTRATION, ComplexityLevel.MULTI_STEP]:
            return "coordinated_execution"
        elif complexity == ComplexityLevel.COMPLEX:
            return "parallel_execution"
        else:
            return "standard_execution"

    def _calculate_confidence_score(self, query: str, persona: PersonaType, urgency: UrgencyLevel, complexity: ComplexityLevel) -> float:
        """Calculate confidence score for the classification"""
        base_score = 0.5
        
        # Boost score for clear persona indicators
        persona_keywords_found = 0
        if persona != PersonaType.MIXED:
            for keyword in self.persona_keywords.get(persona, {}).get("primary", []):
                if keyword in query:
                    persona_keywords_found += 1
            
            persona_score = min(persona_keywords_found * 0.1, 0.3)
            base_score += persona_score
        
        # Boost score for clear urgency indicators
        urgency_found = any(keyword in query for keyword in self.urgency_keywords.get(urgency, []))
        if urgency_found:
            base_score += 0.1
            
        # Boost score for clear complexity indicators  
        complexity_found = any(keyword in query for keyword in self.complexity_keywords.get(complexity, []))
        if complexity_found:
            base_score += 0.1
            
        return min(base_score, 1.0)

    def get_classification_explanation(self, classification: Dict[str, Any]) -> str:
        """Generate human-readable explanation of classification"""
        persona = classification["classification"]["persona"]
        urgency = classification["classification"]["urgency"]
        complexity = classification["classification"]["complexity"]
        pattern = classification["routing"]["recommended_pattern"]
        confidence = classification["classification"]["confidence_score"]
        
        explanation = f"""
Workflow Classification Analysis:
- Primary Persona: {persona.title()}
- Urgency Level: {urgency.title()}
- Complexity: {complexity.title()}
- Recommended Pattern: {pattern.replace('_', ' ').title()}
- Confidence Score: {confidence:.2f}

This request will be routed using {pattern.replace('_', ' ')} pattern 
optimized for {persona} persona with {urgency} priority processing.
"""
        return explanation.strip()