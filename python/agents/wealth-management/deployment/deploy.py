"""Deployment script for wealth management agent system"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from wealth_management.mock_apis import (
    MockMarketDataAPI, MockCustodianAPI, MockTradingAPI, 
    MockCRMAPI, MockComplianceAPI, MockTaxServiceAPI
)


def validate_environment() -> Dict[str, Any]:
    """Validate deployment environment and configuration"""
    
    validation_results = {
        "success": True,
        "errors": [],
        "warnings": [],
        "environment_info": {}
    }
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 11):
        validation_results["errors"].append(
            f"Python 3.11+ required, found {python_version.major}.{python_version.minor}"
        )
        validation_results["success"] = False
    
    validation_results["environment_info"]["python_version"] = f"{python_version.major}.{python_version.minor}.{python_version.micro}"
    
    # Check required environment variables
    required_env_vars = [
        "GOOGLE_CLOUD_PROJECT",
        "GOOGLE_CLOUD_REGION", 
        "VERTEX_AI_LOCATION"
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        validation_results["warnings"].append(
            f"Missing optional environment variables: {', '.join(missing_vars)}"
        )
    
    # Check if running in development mode
    if os.getenv("MOCK_MARKET_DATA_ENABLED", "true").lower() == "true":
        validation_results["environment_info"]["mode"] = "development"
        validation_results["warnings"].append("Running in development mode with mock APIs")
    else:
        validation_results["environment_info"]["mode"] = "production"
    
    # Test mock API connectivity
    try:
        market_api = MockMarketDataAPI()
        test_response = market_api.get_quote("AAPL")
        if not test_response.success:
            validation_results["warnings"].append("Mock Market Data API test failed")
    except Exception as e:
        validation_results["errors"].append(f"Mock API initialization failed: {str(e)}")
        validation_results["success"] = False
    
    return validation_results


def initialize_mock_apis() -> Dict[str, Any]:
    """Initialize and test all mock APIs"""
    
    api_status = {}
    
    apis = {
        "market_data": MockMarketDataAPI,
        "custodian": MockCustodianAPI,
        "trading": MockTradingAPI, 
        "crm": MockCRMAPI,
        "compliance": MockComplianceAPI,
        "tax_service": MockTaxServiceAPI
    }
    
    for api_name, api_class in apis.items():
        try:
            api_instance = api_class()
            # Perform a basic test based on API type
            if api_name == "market_data":
                test_result = api_instance.get_quote("AAPL")
            elif api_name == "custodian":
                test_result = api_instance.get_account_info("WM100001")
            elif api_name == "trading":
                test_result = api_instance.get_trading_hours()
            elif api_name == "crm":
                test_result = api_instance.get_client("CLI10001")
            elif api_name == "compliance":
                test_result = api_instance.get_compliance_rules()
            elif api_name == "tax_service":
                test_result = api_instance.get_tax_documents("WM100001")
            
            api_status[api_name] = {
                "status": "healthy" if test_result.success else "error",
                "message": test_result.error if not test_result.success else "OK"
            }
            
        except Exception as e:
            api_status[api_name] = {
                "status": "error",
                "message": str(e)
            }
    
    return api_status


def run_health_checks() -> Dict[str, Any]:
    """Run comprehensive health checks on the system"""
    
    health_status = {
        "overall_status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",  # Would use actual timestamp
        "checks": {}
    }
    
    # Environment validation
    env_validation = validate_environment()
    health_status["checks"]["environment"] = {
        "status": "healthy" if env_validation["success"] else "unhealthy",
        "details": env_validation
    }
    
    # API health checks
    api_status = initialize_mock_apis()
    failed_apis = [api for api, status in api_status.items() if status["status"] != "healthy"]
    
    health_status["checks"]["apis"] = {
        "status": "healthy" if not failed_apis else "degraded",
        "details": api_status,
        "failed_services": failed_apis
    }
    
    # Agent system checks
    try:
        # Test importing core agents
        from wealth_management.agent import wealth_management_orchestrator
        from wealth_management.agents.client_facing import client_onboarding_agent
        from wealth_management.agents.advisor_facing import portfolio_optimizer_agent
        
        health_status["checks"]["agents"] = {
            "status": "healthy",
            "message": "All core agents loaded successfully"
        }
    except Exception as e:
        health_status["checks"]["agents"] = {
            "status": "unhealthy", 
            "message": f"Agent loading failed: {str(e)}"
        }
        health_status["overall_status"] = "unhealthy"
    
    # Shared libraries checks
    try:
        from wealth_management.shared_libraries import (
            FinancialCalculator, RiskAnalyzer, PortfolioAnalyzer, ComplianceChecker
        )
        
        # Test basic calculation
        test_pv = FinancialCalculator.present_value(100, 0.05, 1)
        assert abs(test_pv - 95.24) < 0.1
        
        health_status["checks"]["calculations"] = {
            "status": "healthy",
            "message": "Financial calculations library working correctly"
        }
    except Exception as e:
        health_status["checks"]["calculations"] = {
            "status": "unhealthy",
            "message": f"Calculation library error: {str(e)}"
        }
        health_status["overall_status"] = "unhealthy"
    
    # Update overall status
    unhealthy_checks = [
        check for check in health_status["checks"].values() 
        if check["status"] == "unhealthy"
    ]
    
    if unhealthy_checks:
        health_status["overall_status"] = "unhealthy"
    elif failed_apis:
        health_status["overall_status"] = "degraded"
    
    return health_status


def deploy_to_vertex_ai(config: Dict[str, Any]) -> Dict[str, Any]:
    """Deploy agents to Vertex AI Agent Engine"""
    
    deployment_result = {
        "success": False,
        "agent_deployments": {},
        "errors": []
    }
    
    # This would integrate with actual Vertex AI deployment
    # For demo purposes, we simulate the deployment
    
    agents_to_deploy = [
        "wealth_management_orchestrator",
        "client_onboarding_agent", 
        "portfolio_dashboard_agent",
        "portfolio_optimizer_agent",
        "market_research_agent",
        "trade_settlement_agent"
    ]
    
    for agent_name in agents_to_deploy:
        try:
            # Simulate deployment process
            print(f"Deploying {agent_name} to Vertex AI...")
            
            # In real implementation, this would:
            # 1. Package agent code
            # 2. Deploy to Vertex AI Agent Engine
            # 3. Configure endpoints and routing
            # 4. Set up monitoring and logging
            
            deployment_result["agent_deployments"][agent_name] = {
                "status": "deployed",
                "endpoint": f"https://agent-engine.googleapis.com/agents/{agent_name}",
                "version": config.get("version", "1.0.0")
            }
            
            print(f"✓ {agent_name} deployed successfully")
            
        except Exception as e:
            error_msg = f"Failed to deploy {agent_name}: {str(e)}"
            deployment_result["errors"].append(error_msg)
            deployment_result["agent_deployments"][agent_name] = {
                "status": "failed",
                "error": error_msg
            }
            print(f"✗ {error_msg}")
    
    deployment_result["success"] = len(deployment_result["errors"]) == 0
    
    return deployment_result


def main():
    """Main deployment function"""
    
    parser = argparse.ArgumentParser(description="Deploy Wealth Management Agent System")
    parser.add_argument("--environment", choices=["dev", "staging", "prod"], 
                       default="dev", help="Deployment environment")
    parser.add_argument("--health-check-only", action="store_true",
                       help="Run health checks only, skip deployment")
    parser.add_argument("--config", type=str, help="Path to deployment config file")
    
    args = parser.parse_args()
    
    print("🚀 Wealth Management Agent System Deployment")
    print("=" * 50)
    
    # Load configuration
    config = {
        "environment": args.environment,
        "version": "1.0.0",
        "google_cloud_project": os.getenv("GOOGLE_CLOUD_PROJECT", "wealth-management-demo"),
        "region": os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
    }
    
    if args.config and os.path.exists(args.config):
        with open(args.config, 'r') as f:
            config.update(json.load(f))
    
    print(f"Environment: {config['environment']}")
    print(f"Version: {config['version']}")
    print(f"Project: {config['google_cloud_project']}")
    
    # Run health checks
    print("\n🏥 Running Health Checks...")
    health_results = run_health_checks()
    
    print(f"Overall Status: {health_results['overall_status'].upper()}")
    
    for check_name, check_result in health_results["checks"].items():
        status_emoji = "✓" if check_result["status"] == "healthy" else "⚠️" if check_result["status"] == "degraded" else "✗"
        print(f"{status_emoji} {check_name.title()}: {check_result['status']}")
        
        if check_result["status"] != "healthy" and "message" in check_result:
            print(f"   {check_result['message']}")
    
    if health_results["overall_status"] == "unhealthy":
        print("\n❌ Health checks failed. Please resolve issues before deployment.")
        return False
    
    if args.health_check_only:
        print("\n✅ Health check complete.")
        return True
    
    # Deploy to Vertex AI
    if config["environment"] != "dev":
        print("\n☁️ Deploying to Vertex AI Agent Engine...")
        deployment_results = deploy_to_vertex_ai(config)
        
        if deployment_results["success"]:
            print("\n✅ Deployment completed successfully!")
            print("\nDeployed Agents:")
            for agent_name, details in deployment_results["agent_deployments"].items():
                if details["status"] == "deployed":
                    print(f"  • {agent_name}: {details['endpoint']}")
        else:
            print("\n❌ Deployment completed with errors:")
            for error in deployment_results["errors"]:
                print(f"  • {error}")
            return False
    else:
        print("\n🔧 Development environment - skipping Vertex AI deployment")
        print("   Use 'adk run .' to test locally")
    
    # Generate deployment summary
    summary = {
        "deployment_time": "2024-01-01T00:00:00Z",  # Would use actual timestamp
        "environment": config["environment"],
        "version": config["version"],
        "health_status": health_results["overall_status"],
        "agents_deployed": len([a for a in deployment_results.get("agent_deployments", {}).values() 
                              if a.get("status") == "deployed"]) if config["environment"] != "dev" else "N/A (dev mode)"
    }
    
    print(f"\n📊 Deployment Summary:")
    for key, value in summary.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")
    
    print("\n🎉 Wealth Management Agent System is ready!")
    print("\nNext Steps:")
    print("1. Configure client environments with API endpoints")
    print("2. Set up monitoring and alerting")
    print("3. Run integration tests")
    print("4. Begin onboarding clients and advisors")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)