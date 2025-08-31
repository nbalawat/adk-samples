#!/usr/bin/env python3
"""Test script for the new client portfolio analytics capabilities"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from wealth_management.tools.client_portfolio_analytics import (
    analyze_market_impact_across_clients,
    identify_enhancement_opportunities,
    analyze_client_help_desk_requests,
    generate_client_outreach_recommendations,
    suggest_personalized_materials
)

def test_client_analytics():
    """Test all client portfolio analytics functions"""
    
    print("🧪 Testing Client Portfolio Analytics System")
    print("=" * 60)
    
    # Test 1: Market Impact Analysis
    print("\n1️⃣ Testing Market Impact Analysis...")
    market_impact = analyze_market_impact_across_clients(time_period="3M")
    if market_impact["status"] == "SUCCESS":
        print(f"✅ Analyzed {market_impact['total_clients_analyzed']} clients")
        print(f"   Total AUM: {market_impact['aggregate_impact']['total_aum_analyzed']}")
        print(f"   Clients with significant losses: {market_impact['aggregate_impact']['clients_with_significant_losses']}")
        print(f"   Average decline: {market_impact['aggregate_impact']['average_portfolio_decline']}")
    else:
        print("❌ Market impact analysis failed")
    
    # Test 2: Enhancement Opportunities
    print("\n2️⃣ Testing Enhancement Opportunities...")
    opportunities = identify_enhancement_opportunities(focus_area="all")
    if opportunities["status"] == "SUCCESS":
        print(f"✅ Found {opportunities['total_opportunities_identified']} opportunities")
        print(f"   Potential additional revenue: {opportunities['potential_additional_revenue']}")
        print(f"   Priority clients: {len(opportunities['priority_clients'])}")
        
        # Show categories
        for category, items in opportunities["opportunities_by_category"].items():
            if items:
                print(f"   - {category.replace('_', ' ').title()}: {len(items)} opportunities")
    else:
        print("❌ Enhancement opportunities analysis failed")
    
    # Test 3: Help Desk Analysis
    print("\n3️⃣ Testing Help Desk Analysis...")
    help_desk = analyze_client_help_desk_requests(time_period="3M")
    if help_desk["status"] == "SUCCESS":
        print(f"✅ Analyzed {help_desk['total_requests']} help desk requests")
        print(f"   Average resolution time: {help_desk['resolution_metrics']['avg_resolution_time']}")
        print(f"   Customer satisfaction: {help_desk['resolution_metrics']['customer_satisfaction']}")
        print(f"   Trending issues: {len(help_desk['trending_issues'])} identified")
    else:
        print("❌ Help desk analysis failed")
    
    # Test 4: Outreach Recommendations
    print("\n4️⃣ Testing Outreach Recommendations...")
    outreach = generate_client_outreach_recommendations(outreach_type="all")
    if outreach["status"] == "SUCCESS":
        print(f"✅ Generated {outreach['total_outreach_recommendations']} outreach recommendations")
        print(f"   Clients requiring outreach: {len(outreach['client_outreach_plan'])}")
        print(f"   Immediate calls needed: {len(outreach['scheduling_recommendations']['immediate_calls'])}")
        print(f"   This week meetings: {len(outreach['scheduling_recommendations']['this_week_meetings'])}")
    else:
        print("❌ Outreach recommendations failed")
    
    # Test 5: Personalized Materials
    print("\n5️⃣ Testing Personalized Materials...")
    materials = suggest_personalized_materials(content_type="all")
    if materials["status"] == "SUCCESS":
        total_suggestions = sum(len(client["personalized_content"]) for client in materials["client_content_recommendations"])
        print(f"✅ Generated {total_suggestions} content suggestions")
        print(f"   Clients with recommendations: {len(materials['client_content_recommendations'])}")
        print(f"   Trending content pieces: {len(materials['trending_content'])}")
    else:
        print("❌ Personalized materials failed")
    
    print("\n" + "=" * 60)
    print("🎉 Client Portfolio Analytics System Testing Complete!")
    
    # Summary of capabilities
    print("\n📊 New Capabilities Available:")
    print("   a) Market impact analysis across all managed clients")
    print("   b) Enhancement opportunities identification")
    print("   c) Help desk request pattern analysis")
    print("   d) Personalized client outreach recommendations")
    print("   e) Tailored content and material suggestions")
    
    print("\n🎯 Sample Queries You Can Now Use:")
    print("   • 'How has the recent market volatility impacted my clients?'")
    print("   • 'What opportunities exist to enhance my client relationships?'")
    print("   • 'What are the common issues clients are contacting us about?'")
    print("   • 'Who should I reach out to this week and why?'")
    print("   • 'What educational materials would be most relevant for each client?'")


if __name__ == "__main__":
    test_client_analytics()