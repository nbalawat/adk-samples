"""
Compliance Review Sequential Agent - ADK Sequential Pattern
Executes compliance checks in proper sequence for regulatory compliance.
"""

from google.adk import Agent, agents
from google.adk.tools import ToolContext
from ..config import MODEL

# Individual compliance step agents
entity_verification_agent = Agent(
    name="entity_verification_agent",
    model=MODEL,
    description="Verify business entity existence and registration",
    instruction="""
    You are the Entity Verification Agent. Your role is to verify that the business entity:
    1. Is properly registered with state/federal authorities
    2. Has valid tax identification numbers
    3. Matches provided business information
    4. Has appropriate business licenses
    
    Use mock entity verification services to check registration status.
    Report any discrepancies or red flags for compliance review.
    """,
    tools=[]  # Will be populated with entity verification tools
)

beneficial_ownership_agent = Agent(
    name="beneficial_ownership_agent", 
    model=MODEL,
    description="Analyze and verify beneficial ownership structure",
    instruction="""
    You are the Beneficial Ownership Agent. Your role is to:
    1. Identify all beneficial owners with 25%+ ownership
    2. Verify ownership percentages add up correctly
    3. Check for complex ownership structures
    4. Validate beneficial owner identity information
    5. Flag any ownership structure requiring additional review
    
    Ensure compliance with beneficial ownership regulations and CDD requirements.
    """,
    tools=[]  # Will be populated with beneficial ownership tools
)

sanctions_screening_agent = Agent(
    name="sanctions_screening_agent",
    model=MODEL, 
    description="Perform comprehensive sanctions and PEP screening",
    instruction="""
    You are the Sanctions Screening Agent. Your role is to:
    1. Screen business entity against OFAC and other sanctions lists
    2. Screen all beneficial owners and key personnel
    3. Check for PEP (Politically Exposed Person) status
    4. Review adverse media and negative news
    5. Assess geographic and jurisdictional risks
    
    Any matches or potential matches must be escalated immediately.
    Provide detailed screening results with confidence scores.
    """,
    tools=[]  # Will be populated with sanctions screening tools
)

risk_assessment_agent = Agent(
    name="risk_assessment_agent",
    model=MODEL,
    description="Conduct comprehensive risk assessment and rating",
    instruction="""
    You are the Risk Assessment Agent. Your role is to:
    1. Analyze all collected information for risk factors
    2. Assess industry, geographic, and customer risk
    3. Evaluate transaction patterns and expected activity
    4. Determine overall risk rating (Low/Medium/High)
    5. Recommend appropriate monitoring and controls
    
    Consider all compliance results in determining final risk rating.
    Provide detailed rationale for risk assessment decisions.
    """,
    tools=[]  # Will be populated with risk assessment tools
)

final_compliance_approval_agent = Agent(
    name="final_compliance_approval_agent",
    model=MODEL,
    description="Make final compliance approval decision",
    instruction="""
    You are the Final Compliance Approval Agent. Your role is to:
    1. Review all compliance screening results
    2. Assess overall compliance posture
    3. Make final approval/rejection/escalation decision
    4. Document compliance decision rationale
    5. Set ongoing monitoring requirements
    
    Only approve if all compliance requirements are fully satisfied.
    Escalate any borderline cases for human review.
    """,
    tools=[]  # Will be populated with approval decision tools
)

# Create the Sequential Agent using ADK pattern
compliance_review_sequential_agent = agents.SequentialAgent(
    name="compliance_review_sequential_agent", 
    description="Execute compliance review in proper regulatory sequence",
    sub_agents=[
        entity_verification_agent,           # Step 1: Verify entity
        beneficial_ownership_agent,          # Step 2: Analyze ownership  
        sanctions_screening_agent,           # Step 3: Screen for sanctions
        risk_assessment_agent,               # Step 4: Assess overall risk
        final_compliance_approval_agent,     # Step 5: Final approval decision
    ]
)