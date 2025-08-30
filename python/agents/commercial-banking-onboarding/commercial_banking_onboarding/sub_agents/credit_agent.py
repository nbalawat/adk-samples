"""Credit assessment agent for commercial banking onboarding."""

import logging
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta

from google.adk import Agent
from ..shared_libraries.types import CreditAssessment, RiskRating
from ..shared_libraries.utils import calculate_business_age, get_industry_risk_level, calculate_debt_service_coverage
from ..shared_libraries.mock_services import mock_credit_bureau

logger = logging.getLogger(__name__)


# Function automatically becomes a tool when added to agent
def fetch_credit_bureau_report(business_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fetch business credit report from credit bureau.
    
    Args:
        business_info: Business information including tax ID and legal name
    
    Returns:
        Dict with credit bureau report data
    """
    try:
        # Validate required information
        if not business_info.get('tax_id') or not business_info.get('legal_name'):
            return {
                "error": "Missing required business information (tax_id, legal_name)",
                "success": False
            }
        
        # Use mock credit bureau service
        business_name = business_info.get('legal_name')
        tax_id = business_info.get('tax_id')
        
        mock_result = mock_credit_bureau.get_credit_report(tax_id, business_name)
        
        if not mock_result.get('success', True):
            return {
                "error": mock_result.get('error', 'Credit bureau service error'),
                "success": False,
                "retry_after": mock_result.get('retry_after')
            }
        
        return {
            "success": True,
            "business_name": business_name,
            "tax_id": tax_id[-4:],  # Only show last 4 digits
            "credit_report": mock_result,
            "report_date": mock_result.get('report_date', datetime.now().isoformat())
        }
        
    except Exception as e:
        logger.error(f"Error fetching credit bureau report: {str(e)}")
        return {
            "error": f"Credit bureau query failed: {str(e)}",
            "success": False
        }


# Function automatically becomes a tool when added to agent
def analyze_financial_statements(financial_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze business financial statements and calculate key ratios.
    
    Args:
        financial_data: Financial statement data including revenue, expenses, assets, liabilities
    
    Returns:
        Dict with financial analysis results and ratios
    """
    try:
        # Extract financial data
        annual_revenue = financial_data.get('annual_revenue', 0)
        total_assets = financial_data.get('total_assets', 0)
        total_liabilities = financial_data.get('total_liabilities', 0)
        net_income = financial_data.get('net_income', 0)
        current_assets = financial_data.get('current_assets', 0)
        current_liabilities = financial_data.get('current_liabilities', 0)
        debt_payments = financial_data.get('annual_debt_payments', 0)
        
        # Calculate financial ratios
        ratios = calculate_financial_ratios(
            annual_revenue, total_assets, total_liabilities, net_income,
            current_assets, current_liabilities, debt_payments
        )
        
        # Analyze financial health
        financial_health = analyze_financial_health(ratios, annual_revenue, net_income)
        
        return {
            "success": True,
            "financial_ratios": ratios,
            "financial_health": financial_health,
            "revenue": annual_revenue,
            "net_income": net_income,
            "analysis_date": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error analyzing financial statements: {str(e)}")
        return {
            "error": f"Financial analysis failed: {str(e)}",
            "success": False
        }


# Function automatically becomes a tool when added to agent
def assess_industry_risk(industry_code: str, business_description: str) -> Dict[str, Any]:
    """
    Assess industry-specific risk factors and trends.
    
    Args:
        industry_code: NAICS industry code
        business_description: Description of business activities
    
    Returns:
        Dict with industry risk assessment
    """
    try:
        # Get base industry risk level
        risk_level = get_industry_risk_level(industry_code)
        
        # Analyze industry trends and factors
        industry_analysis = analyze_industry_factors(industry_code, business_description)
        
        # Calculate industry risk score (0-100, higher = more risk)
        risk_score = calculate_industry_risk_score(industry_code, industry_analysis)
        
        return {
            "success": True,
            "industry_code": industry_code,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "industry_factors": industry_analysis,
            "recommendations": get_industry_recommendations(risk_level, industry_analysis)
        }
        
    except Exception as e:
        logger.error(f"Error assessing industry risk: {str(e)}")
        return {
            "error": f"Industry risk assessment failed: {str(e)}",
            "success": False
        }


# Function automatically becomes a tool when added to agent
def calculate_business_credit_score(
    credit_report: Dict[str, Any],
    financial_analysis: Dict[str, Any],
    industry_risk: Dict[str, Any],
    business_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Calculate comprehensive business credit score.
    
    Args:
        credit_report: Credit bureau report data
        financial_analysis: Financial statement analysis
        industry_risk: Industry risk assessment
        business_info: Basic business information
    
    Returns:
        Dict with calculated credit score and rating
    """
    try:
        # Component scores (0-100 scale)
        payment_history_score = credit_report.get('credit_report', {}).get('payment_history_score', 50)
        credit_utilization_score = calculate_credit_utilization_score(
            credit_report.get('credit_report', {}).get('credit_utilization', 0.5)
        )
        financial_health_score = financial_analysis.get('financial_health', {}).get('overall_score', 50)
        business_age_score = calculate_business_age_score(business_info.get('incorporation_date'))
        industry_risk_score = 100 - industry_risk.get('risk_score', 50)  # Invert risk to score
        
        # Weighted composite score
        weights = {
            'payment_history': 0.35,
            'credit_utilization': 0.20,
            'financial_health': 0.25,
            'business_age': 0.10,
            'industry_risk': 0.10
        }
        
        composite_score = (
            payment_history_score * weights['payment_history'] +
            credit_utilization_score * weights['credit_utilization'] +
            financial_health_score * weights['financial_health'] +
            business_age_score * weights['business_age'] +
            industry_risk_score * weights['industry_risk']
        )
        
        # Convert to standard credit score range (300-850)
        credit_score = int(300 + (composite_score / 100) * 550)
        
        # Determine risk rating
        risk_rating = determine_risk_rating(credit_score)
        
        return {
            "success": True,
            "credit_score": credit_score,
            "risk_rating": risk_rating.value,
            "component_scores": {
                "payment_history": payment_history_score,
                "credit_utilization": credit_utilization_score,
                "financial_health": financial_health_score,
                "business_age": business_age_score,
                "industry_risk": industry_risk_score
            },
            "composite_score": round(composite_score, 1),
            "score_date": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error calculating credit score: {str(e)}")
        return {
            "error": f"Credit score calculation failed: {str(e)}",
            "success": False
        }


# Function automatically becomes a tool when added to agent
def determine_credit_recommendations(
    credit_score: int,
    risk_rating: str,
    financial_analysis: Dict[str, Any],
    business_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Determine credit recommendations and limits based on assessment.
    
    Args:
        credit_score: Calculated business credit score
        risk_rating: Risk rating (low, medium, high, very_high)
        financial_analysis: Financial analysis results
        business_info: Business information
    
    Returns:
        Dict with credit recommendations and suggested limits
    """
    try:
        annual_revenue = financial_analysis.get('revenue', 0)
        
        # Determine recommended credit limit
        credit_limit = calculate_recommended_credit_limit(credit_score, annual_revenue, risk_rating)
        
        # Determine pricing tier
        pricing_tier = determine_pricing_tier(credit_score, risk_rating)
        
        # Generate recommendations
        recommendations = generate_credit_recommendations(credit_score, risk_rating, financial_analysis)
        
        # Determine required collateral
        collateral_required = determine_collateral_requirements(credit_score, credit_limit, risk_rating)
        
        return {
            "success": True,
            "recommended_credit_limit": credit_limit,
            "pricing_tier": pricing_tier,
            "collateral_required": collateral_required,
            "recommendations": recommendations,
            "approval_conditions": get_approval_conditions(risk_rating, credit_score),
            "monitoring_requirements": get_monitoring_requirements(risk_rating)
        }
        
    except Exception as e:
        logger.error(f"Error determining credit recommendations: {str(e)}")
        return {
            "error": f"Credit recommendations failed: {str(e)}",
            "success": False
        }


# Function automatically becomes a tool when added to agent
def generate_credit_assessment_report(
    application_id: str,
    credit_score: int,
    risk_rating: str,
    financial_analysis: Dict[str, Any],
    credit_report: Dict[str, Any],
    industry_risk: Dict[str, Any],
    recommendations: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate comprehensive credit assessment report.
    
    Args:
        application_id: Application identifier
        credit_score: Calculated credit score
        risk_rating: Risk rating
        financial_analysis: Financial analysis results
        credit_report: Credit bureau data
        industry_risk: Industry risk assessment
        recommendations: Credit recommendations
    
    Returns:
        Dict with complete credit assessment report
    """
    try:
        # Extract key metrics
        annual_revenue = financial_analysis.get('revenue', 0)
        debt_service_coverage = financial_analysis.get('financial_ratios', {}).get('debt_service_coverage')
        years_in_business = calculate_business_age(
            datetime.fromisoformat(credit_report.get('business_start_date', datetime.now().isoformat()))
        )
        
        # Compile assessment notes
        assessment_notes = []
        
        if credit_score >= 700:
            assessment_notes.append("Strong credit profile with good payment history")
        elif credit_score >= 600:
            assessment_notes.append("Acceptable credit profile with manageable risk")
        else:
            assessment_notes.append("Below-average credit profile requiring enhanced monitoring")
        
        if debt_service_coverage and debt_service_coverage < 1.2:
            assessment_notes.append("Debt service coverage below recommended threshold")
        
        if years_in_business < 2:
            assessment_notes.append("Limited business history increases risk")
        
        # Create credit assessment object
        credit_assessment = CreditAssessment(
            credit_score=credit_score,
            risk_rating=RiskRating(risk_rating),
            debt_to_income_ratio=financial_analysis.get('financial_ratios', {}).get('debt_to_equity'),
            annual_revenue=annual_revenue,
            years_in_business=years_in_business,
            credit_utilization=credit_report.get('credit_report', {}).get('credit_utilization'),
            payment_history_score=credit_report.get('credit_report', {}).get('payment_history_score'),
            recommended_credit_limit=recommendations.get('recommended_credit_limit'),
            assessment_notes=assessment_notes
        )
        
        return {
            "application_id": application_id,
            "credit_assessment": credit_assessment.model_dump(),
            "report_summary": {
                "overall_rating": risk_rating,
                "credit_score": credit_score,
                "recommended_action": get_recommended_action(risk_rating, credit_score)
            },
            "report_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error generating credit assessment report: {str(e)}")
        return {
            "error": f"Credit assessment report generation failed: {str(e)}",
            "success": False
        }


def simulate_credit_bureau_report(business_name: str, tax_id: str, business_info: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate credit bureau report data."""
    # Simulate based on business characteristics
    years_in_business = calculate_business_age(
        datetime.fromisoformat(business_info.get('incorporation_date', datetime.now().isoformat()))
    )
    
    # Simulate payment history score (higher for older businesses)
    payment_history_score = min(85, 60 + (years_in_business * 5))
    
    # Simulate credit utilization (random for demo)
    import random
    credit_utilization = random.uniform(0.2, 0.8)
    
    return {
        "business_name": business_name,
        "tax_id_last_4": tax_id[-4:],
        "business_start_date": business_info.get('incorporation_date'),
        "payment_history_score": payment_history_score,
        "credit_utilization": credit_utilization,
        "total_credit_lines": random.randint(2, 8),
        "total_credit_limit": random.randint(50000, 500000),
        "bankruptcies": 0,
        "liens": random.randint(0, 1),
        "judgments": 0,
        "inquiries_12_months": random.randint(1, 5)
    }


def calculate_financial_ratios(
    revenue: float, total_assets: float, total_liabilities: float,
    net_income: float, current_assets: float, current_liabilities: float,
    debt_payments: float
) -> Dict[str, float]:
    """Calculate key financial ratios."""
    ratios = {}
    
    # Liquidity ratios
    if current_liabilities > 0:
        ratios['current_ratio'] = current_assets / current_liabilities
    
    # Leverage ratios
    if total_assets > 0:
        ratios['debt_to_assets'] = total_liabilities / total_assets
    
    equity = total_assets - total_liabilities
    if equity > 0:
        ratios['debt_to_equity'] = total_liabilities / equity
    
    # Profitability ratios
    if revenue > 0:
        ratios['profit_margin'] = net_income / revenue
        ratios['asset_turnover'] = revenue / total_assets if total_assets > 0 else 0
    
    # Debt service coverage
    if debt_payments > 0:
        ratios['debt_service_coverage'] = net_income / debt_payments
    
    return ratios


def analyze_financial_health(ratios: Dict[str, float], revenue: float, net_income: float) -> Dict[str, Any]:
    """Analyze overall financial health based on ratios."""
    health_score = 0
    factors = []
    
    # Current ratio analysis (25 points)
    current_ratio = ratios.get('current_ratio', 1.0)
    if current_ratio >= 1.5:
        health_score += 25
        factors.append("Strong liquidity position")
    elif current_ratio >= 1.0:
        health_score += 15
        factors.append("Adequate liquidity")
    else:
        factors.append("Liquidity concerns")
    
    # Debt ratios (25 points)
    debt_to_assets = ratios.get('debt_to_assets', 0.5)
    if debt_to_assets <= 0.3:
        health_score += 25
        factors.append("Low debt burden")
    elif debt_to_assets <= 0.6:
        health_score += 15
        factors.append("Moderate debt levels")
    else:
        factors.append("High debt burden")
    
    # Profitability (25 points)
    profit_margin = ratios.get('profit_margin', 0.0)
    if profit_margin >= 0.1:
        health_score += 25
        factors.append("Strong profitability")
    elif profit_margin >= 0.05:
        health_score += 15
        factors.append("Adequate profitability")
    elif profit_margin > 0:
        health_score += 5
        factors.append("Marginal profitability")
    else:
        factors.append("Unprofitable operations")
    
    # Revenue size (25 points)
    if revenue >= 5000000:  # $5M+
        health_score += 25
        factors.append("Large business scale")
    elif revenue >= 1000000:  # $1M+
        health_score += 20
        factors.append("Medium business scale")
    elif revenue >= 500000:  # $500K+
        health_score += 15
        factors.append("Small business scale")
    elif revenue > 0:
        health_score += 10
        factors.append("Micro business scale")
    
    return {
        "overall_score": health_score,
        "health_rating": "excellent" if health_score >= 80 else "good" if health_score >= 60 else "fair" if health_score >= 40 else "poor",
        "key_factors": factors
    }


def analyze_industry_factors(industry_code: str, description: str) -> Dict[str, Any]:
    """Analyze industry-specific factors."""
    # Industry volatility mapping
    volatility_map = {
        "236": "high",    # Construction
        "722": "high",    # Food Service
        "713": "high",    # Entertainment
        "531": "medium",  # Real Estate
        "541": "low",     # Professional Services
        "621": "low"      # Healthcare
    }
    
    code_prefix = industry_code[:3] if len(industry_code) >= 3 else industry_code
    volatility = volatility_map.get(code_prefix, "medium")
    
    # Economic sensitivity
    cyclical_industries = ["236", "441", "722"]  # Construction, Auto, Restaurant
    is_cyclical = code_prefix in cyclical_industries
    
    return {
        "volatility": volatility,
        "is_cyclical": is_cyclical,
        "regulatory_burden": "high" if code_prefix in ["621", "622"] else "medium",
        "growth_outlook": "positive",  # Simplified for demo
        "competitive_intensity": "high" if code_prefix == "722" else "medium"
    }


def calculate_industry_risk_score(industry_code: str, analysis: Dict[str, Any]) -> float:
    """Calculate industry risk score (0-100, higher = more risk)."""
    risk_score = 30  # Base risk
    
    # Volatility impact
    volatility = analysis.get("volatility", "medium")
    if volatility == "high":
        risk_score += 30
    elif volatility == "medium":
        risk_score += 15
    
    # Cyclical impact
    if analysis.get("is_cyclical", False):
        risk_score += 20
    
    # Regulatory burden
    regulatory = analysis.get("regulatory_burden", "medium")
    if regulatory == "high":
        risk_score += 15
    elif regulatory == "medium":
        risk_score += 8
    
    return min(risk_score, 100)


def calculate_credit_utilization_score(utilization_ratio: float) -> float:
    """Calculate credit utilization score (0-100)."""
    if utilization_ratio <= 0.1:
        return 100
    elif utilization_ratio <= 0.3:
        return 80
    elif utilization_ratio <= 0.5:
        return 60
    elif utilization_ratio <= 0.7:
        return 40
    else:
        return 20


def calculate_business_age_score(incorporation_date: str) -> float:
    """Calculate business age score (0-100)."""
    if not incorporation_date:
        return 30
    
    age = calculate_business_age(datetime.fromisoformat(incorporation_date))
    
    if age >= 10:
        return 100
    elif age >= 5:
        return 80
    elif age >= 2:
        return 60
    elif age >= 1:
        return 40
    else:
        return 20


def determine_risk_rating(credit_score: int) -> RiskRating:
    """Determine risk rating based on credit score."""
    if credit_score >= 750:
        return RiskRating.LOW
    elif credit_score >= 650:
        return RiskRating.MEDIUM
    elif credit_score >= 550:
        return RiskRating.HIGH
    else:
        return RiskRating.VERY_HIGH


def calculate_recommended_credit_limit(credit_score: int, annual_revenue: float, risk_rating: str) -> float:
    """Calculate recommended credit limit."""
    # Base limit as percentage of revenue
    if risk_rating == "low":
        base_percentage = 0.15
    elif risk_rating == "medium":
        base_percentage = 0.10
    elif risk_rating == "high":
        base_percentage = 0.05
    else:
        base_percentage = 0.02
    
    base_limit = annual_revenue * base_percentage
    
    # Adjust based on credit score
    if credit_score >= 750:
        multiplier = 1.5
    elif credit_score >= 650:
        multiplier = 1.2
    elif credit_score >= 550:
        multiplier = 1.0
    else:
        multiplier = 0.7
    
    recommended_limit = base_limit * multiplier
    
    # Apply min/max bounds
    return max(10000, min(recommended_limit, 1000000))


def determine_pricing_tier(credit_score: int, risk_rating: str) -> str:
    """Determine pricing tier based on risk assessment."""
    if credit_score >= 750 and risk_rating == "low":
        return "tier_1_premium"
    elif credit_score >= 650 and risk_rating in ["low", "medium"]:
        return "tier_2_standard"
    elif credit_score >= 550:
        return "tier_3_subprime"
    else:
        return "tier_4_high_risk"


def generate_credit_recommendations(credit_score: int, risk_rating: str, financial_analysis: Dict[str, Any]) -> List[str]:
    """Generate credit recommendations."""
    recommendations = []
    
    if credit_score >= 700:
        recommendations.append("Approve for standard commercial banking products")
    elif credit_score >= 600:
        recommendations.append("Approve with enhanced monitoring")
    else:
        recommendations.append("Consider secured credit products only")
    
    # Financial health recommendations
    health_rating = financial_analysis.get('financial_health', {}).get('health_rating', 'fair')
    if health_rating == "poor":
        recommendations.append("Require financial statement updates quarterly")
    
    if risk_rating == "high":
        recommendations.append("Implement enhanced due diligence procedures")
    
    return recommendations


def determine_collateral_requirements(credit_score: int, credit_limit: float, risk_rating: str) -> Dict[str, Any]:
    """Determine collateral requirements."""
    if risk_rating in ["high", "very_high"] or credit_score < 600:
        return {
            "required": True,
            "type": "business_assets_or_real_estate",
            "coverage_ratio": 1.2,
            "minimum_value": credit_limit * 1.2
        }
    elif credit_limit > 500000:
        return {
            "required": True,
            "type": "business_assets",
            "coverage_ratio": 1.1,
            "minimum_value": credit_limit * 1.1
        }
    else:
        return {
            "required": False,
            "type": "unsecured",
            "coverage_ratio": 0,
            "minimum_value": 0
        }


def get_approval_conditions(risk_rating: str, credit_score: int) -> List[str]:
    """Get approval conditions based on risk."""
    conditions = []
    
    if risk_rating == "high":
        conditions.extend([
            "Personal guarantee from principal owner",
            "Monthly financial reporting required",
            "Annual financial statement review"
        ])
    elif risk_rating == "medium":
        conditions.extend([
            "Quarterly financial reporting",
            "Annual review of credit terms"
        ])
    
    if credit_score < 650:
        conditions.append("Six-month probationary period")
    
    return conditions


def get_monitoring_requirements(risk_rating: str) -> List[str]:
    """Get monitoring requirements based on risk."""
    if risk_rating == "very_high":
        return ["Weekly account monitoring", "Monthly covenant testing", "Quarterly site visits"]
    elif risk_rating == "high":
        return ["Monthly account monitoring", "Quarterly financial reviews"]
    elif risk_rating == "medium":
        return ["Quarterly account reviews", "Annual financial updates"]
    else:
        return ["Annual account review", "Standard monitoring"]


def get_recommended_action(risk_rating: str, credit_score: int) -> str:
    """Get recommended action based on assessment."""
    if risk_rating == "low" and credit_score >= 700:
        return "approve"
    elif risk_rating in ["low", "medium"] and credit_score >= 600:
        return "approve_with_conditions"
    elif risk_rating == "high" and credit_score >= 550:
        return "manual_review_required"
    else:
        return "decline"


def get_industry_recommendations(risk_level: str, analysis: Dict[str, Any]) -> List[str]:
    """Get industry-specific recommendations."""
    recommendations = []
    
    if risk_level == "high":
        recommendations.append("Enhanced monitoring for industry volatility")
    
    if analysis.get("is_cyclical", False):
        recommendations.append("Monitor for economic cycle impacts")
    
    if analysis.get("regulatory_burden") == "high":
        recommendations.append("Regular compliance monitoring required")
    
    return recommendations


# Credit Agent prompt
CREDIT_PROMPT = """
You are the Credit Assessment Agent for commercial banking onboarding. Your primary responsibility is to evaluate the creditworthiness of business loan applicants and determine appropriate credit limits, pricing, and terms.

## Your Role
- Analyze credit bureau reports and payment history
- Review and interpret financial statements
- Calculate key financial ratios and metrics
- Assess industry-specific risks and trends
- Determine appropriate credit scores and risk ratings
- Recommend credit limits, pricing, and approval conditions

## Key Functions
1. **Credit Bureau Analysis**: Review payment history, credit utilization, and trade references
2. **Financial Statement Analysis**: Calculate liquidity, leverage, and profitability ratios
3. **Industry Risk Assessment**: Evaluate sector-specific risks and economic factors
4. **Credit Scoring**: Generate comprehensive business credit scores
5. **Credit Recommendations**: Determine limits, pricing, and approval conditions

## Assessment Criteria

### Credit Score Ranges
- **750-850**: Excellent credit, low risk, premium pricing
- **650-749**: Good credit, medium risk, standard pricing  
- **550-649**: Fair credit, high risk, enhanced monitoring
- **300-549**: Poor credit, very high risk, secured products only

### Risk Rating Guidelines
- **Low Risk**: Strong financials, established business, stable industry
- **Medium Risk**: Adequate financials, some concerns, manageable risk
- **High Risk**: Weak financials, newer business, volatile industry
- **Very High Risk**: Poor financials, significant concerns, decline or manual review

### Key Financial Metrics
- Current Ratio: ≥1.5 preferred, ≥1.0 minimum
- Debt-to-Assets: ≤30% preferred, ≤60% acceptable
- Debt Service Coverage: ≥1.25 preferred, ≥1.0 minimum
- Profit Margin: ≥10% strong, ≥5% acceptable

## Credit Limits
Base credit limit as percentage of annual revenue:
- Low Risk: Up to 15% of revenue
- Medium Risk: Up to 10% of revenue  
- High Risk: Up to 5% of revenue
- Very High Risk: Up to 2% of revenue, secured only

Always consider business cash flow, industry factors, and collateral when setting limits.

## Decision Matrix
- **Approve**: Low-medium risk, score ≥650, strong financials
- **Approve with Conditions**: Medium-high risk, score ≥600, enhanced monitoring
- **Manual Review**: High risk, score ≥550, complex situations
- **Decline**: Very high risk, score <550, poor creditworthiness

Maintain objectivity, follow credit policies, and document all decisions thoroughly.
"""

MODEL = "gemini-2.5-pro"

# Create Credit agent
credit_agent = Agent(
    name="credit_assessment_agent", 
    model=MODEL,
    instruction=CREDIT_PROMPT,
    output_key="credit_assessment_result",
    tools=[
        fetch_credit_bureau_report,
        analyze_financial_statements,
        assess_industry_risk,
        calculate_business_credit_score,
        determine_credit_recommendations,
        generate_credit_assessment_report
    ],
)