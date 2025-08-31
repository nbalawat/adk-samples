#!/usr/bin/env python3
"""Deploy Wealth Management Agent to Google Cloud Run with all data included"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

def check_prerequisites() -> bool:
    """Check if all required tools are installed"""
    required_tools = ['gcloud', 'docker']
    missing_tools = []
    
    for tool in required_tools:
        try:
            subprocess.run([tool, '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"❌ Missing required tools: {', '.join(missing_tools)}")
        print("Please install them and try again.")
        return False
    
    print("✅ All required tools are available")
    return True

def validate_gcp_config() -> Dict[str, str]:
    """Validate and get GCP configuration"""
    try:
        # Get current project
        result = subprocess.run(
            ['gcloud', 'config', 'get', 'project'], 
            capture_output=True, text=True, check=True
        )
        project_id = result.stdout.strip()
        
        if not project_id:
            raise ValueError("No default project set")
        
        # Get current region (fallback to us-central1)
        try:
            result = subprocess.run(
                ['gcloud', 'config', 'get', 'run/region'], 
                capture_output=True, text=True, check=True
            )
            region = result.stdout.strip() or 'us-central1'
        except subprocess.CalledProcessError:
            region = 'us-central1'
        
        config = {
            'project_id': project_id,
            'region': region
        }
        
        print(f"✅ GCP Configuration:")
        print(f"   Project: {config['project_id']}")
        print(f"   Region: {config['region']}")
        
        return config
        
    except (subprocess.CalledProcessError, ValueError) as e:
        print(f"❌ GCP configuration error: {e}")
        print("Please run 'gcloud auth login' and 'gcloud config set project YOUR_PROJECT_ID'")
        sys.exit(1)

def enable_required_apis(project_id: str) -> bool:
    """Enable required Google Cloud APIs"""
    required_apis = [
        'run.googleapis.com',
        'cloudbuild.googleapis.com', 
        'artifactregistry.googleapis.com',
        'aiplatform.googleapis.com'
    ]
    
    print("🔧 Enabling required Google Cloud APIs...")
    
    for api in required_apis:
        try:
            print(f"   Enabling {api}...")
            subprocess.run([
                'gcloud', 'services', 'enable', api, 
                '--project', project_id
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Failed to enable {api}: {e}")
            return False
    
    print("✅ All required APIs enabled")
    return True

def build_and_push_image(project_id: str, service_name: str) -> str:
    """Build and push Docker image to Google Container Registry"""
    
    # Use Artifact Registry instead of GCR
    image_name = f"{project_id}/{service_name}"
    image_uri = f"gcr.io/{image_name}:latest"
    
    print(f"🔨 Building Docker image...")
    print(f"   Image: {image_uri}")
    
    # Build image with Cloud Build for better reliability
    try:
        subprocess.run([
            'gcloud', 'builds', 'submit', 
            '--tag', image_uri,
            '--project', project_id,
            '.'  # Current directory
        ], check=True)
        
        print(f"✅ Image built and pushed successfully")
        return image_uri
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build image: {e}")
        sys.exit(1)

def deploy_to_cloud_run(
    image_uri: str, 
    service_name: str, 
    project_id: str, 
    region: str,
    env_vars: Dict[str, str]
) -> Dict[str, Any]:
    """Deploy the image to Cloud Run"""
    
    print(f"🚀 Deploying to Cloud Run...")
    print(f"   Service: {service_name}")
    print(f"   Region: {region}")
    
    # Prepare deployment command
    cmd = [
        'gcloud', 'run', 'deploy', service_name,
        '--image', image_uri,
        '--project', project_id,
        '--region', region,
        '--platform', 'managed',
        '--allow-unauthenticated',
        '--memory', '2Gi',
        '--cpu', '2',
        '--max-instances', '10',
        '--port', '8080',
        '--timeout', '900'  # 15 minutes timeout
    ]
    
    # Add environment variables
    if env_vars:
        for key, value in env_vars.items():
            cmd.extend(['--set-env-vars', f'{key}={value}'])
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # Extract service URL from output
        output_lines = result.stderr.split('\n')
        service_url = None
        
        for line in output_lines:
            if 'Service URL:' in line:
                service_url = line.split('Service URL:')[1].strip()
                break
        
        if not service_url:
            # Try to get URL using describe command
            result = subprocess.run([
                'gcloud', 'run', 'services', 'describe', service_name,
                '--project', project_id,
                '--region', region,
                '--format', 'value(status.url)'
            ], capture_output=True, text=True, check=True)
            service_url = result.stdout.strip()
        
        print(f"✅ Deployment successful!")
        print(f"   Service URL: {service_url}")
        
        return {
            'success': True,
            'service_name': service_name,
            'service_url': service_url,
            'region': region,
            'project_id': project_id
        }
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr.decode()}")
        sys.exit(1)

def create_env_file():
    """Create .env file with deployment settings"""
    env_content = '''# Wealth Management Agent Configuration
GOOGLE_GENAI_USE_VERTEXAI=true
SERVE_WEB_INTERFACE=true
MOCK_MARKET_DATA_ENABLED=true
MOCK_CUSTODIAN_API_ENABLED=true
MOCK_TRADING_API_ENABLED=true
MOCK_CRM_API_ENABLED=true
MOCK_COMPLIANCE_API_ENABLED=true
MOCK_TAX_SERVICE_API_ENABLED=true

# Optional: Set these for production
# GOOGLE_CLOUD_PROJECT=your-project-id
# VERTEX_AI_LOCATION=us-central1
# SESSION_SERVICE_URI=your-session-service-uri
'''
    
    env_path = Path('.env')
    if not env_path.exists():
        with open(env_path, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with default configuration")
    else:
        print("ℹ️  .env file already exists, skipping creation")

def test_deployment(service_url: str) -> bool:
    """Test the deployed service"""
    import requests
    import time
    
    print("🧪 Testing deployed service...")
    
    # Wait a moment for service to be ready
    time.sleep(10)
    
    try:
        # Test the health endpoint
        response = requests.get(f"{service_url}/health", timeout=30)
        
        if response.status_code == 200:
            print("✅ Service is responding correctly")
            return True
        else:
            print(f"⚠️  Service responded with status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Service test failed: {e}")
        print("   The service may still be starting up. Please test manually.")
        return False

def main():
    """Main deployment function"""
    parser = argparse.ArgumentParser(description="Deploy Wealth Management Agent to Cloud Run")
    parser.add_argument("--service-name", default="wealth-management-agent",
                       help="Cloud Run service name")
    parser.add_argument("--skip-build", action="store_true",
                       help="Skip building new image (use existing)")
    parser.add_argument("--skip-test", action="store_true",
                       help="Skip testing deployed service")
    
    args = parser.parse_args()
    
    print("🚀 Wealth Management Agent - Cloud Run Deployment")
    print("=" * 55)
    
    # Change to the project root directory
    os.chdir(Path(__file__).parent.parent)
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Validate GCP configuration
    gcp_config = validate_gcp_config()
    
    # Enable required APIs
    if not enable_required_apis(gcp_config['project_id']):
        print("⚠️  Some APIs couldn't be enabled, but continuing...")
    
    # Create .env file if it doesn't exist
    create_env_file()
    
    # Environment variables for the service
    env_vars = {
        'GOOGLE_GENAI_USE_VERTEXAI': 'true',
        'SERVE_WEB_INTERFACE': 'true',
        'MOCK_MARKET_DATA_ENABLED': 'true',
        'GOOGLE_CLOUD_PROJECT': gcp_config['project_id'],
        'VERTEX_AI_LOCATION': gcp_config['region']
    }
    
    # Build and push image (unless skipped)
    if not args.skip_build:
        image_uri = build_and_push_image(gcp_config['project_id'], args.service_name)
    else:
        image_uri = f"gcr.io/{gcp_config['project_id']}/{args.service_name}:latest"
        print(f"ℹ️  Skipping build, using existing image: {image_uri}")
    
    # Deploy to Cloud Run
    deployment_result = deploy_to_cloud_run(
        image_uri, 
        args.service_name,
        gcp_config['project_id'],
        gcp_config['region'],
        env_vars
    )
    
    if deployment_result['success']:
        service_url = deployment_result['service_url']
        
        print("\n🎉 Deployment Complete!")
        print("=" * 25)
        print(f"Service URL: {service_url}")
        print(f"Project: {gcp_config['project_id']}")
        print(f"Region: {gcp_config['region']}")
        print(f"Service: {args.service_name}")
        
        # Test deployment (unless skipped)
        if not args.skip_test:
            test_deployment(service_url)
        
        print(f"\n📚 Available Endpoints:")
        print(f"   Web Interface: {service_url}/dev-ui/")
        print(f"   API Docs: {service_url}/docs")
        print(f"   Health Check: {service_url}/health")
        
        print(f"\n🧪 Test the agent with these sample queries:")
        print(f"   • 'Show me portfolio summary for client TEST001'")
        print(f"   • 'Conduct risk assessment for client WM100004'")
        print(f"   • 'Generate investment research for WM100006'")
        
        print(f"\n📊 The following data is included in the deployment:")
        print(f"   • 23 working client accounts (TEST001, DEMO001, CLIENT001, WM100001-WM100020)")
        print(f"   • Complete portfolio positions and transaction history")
        print(f"   • 33 wealth management workflows across all categories")
        print(f"   • All mock APIs with realistic financial data")
        
        # Generate deployment info file
        deployment_info = {
            'service_url': service_url,
            'service_name': args.service_name,
            'project_id': gcp_config['project_id'],
            'region': gcp_config['region'],
            'image_uri': image_uri,
            'deployed_at': '2024-01-01T00:00:00Z',  # Would use actual timestamp
            'features': [
                '33 wealth management workflows',
                '23 client accounts with realistic data',
                'Complete mock API ecosystem',
                'ADK web interface included',
                'All test documentation included'
            ]
        }
        
        with open('deployment_info.json', 'w') as f:
            json.dump(deployment_info, f, indent=2)
        
        print(f"\nℹ️  Deployment info saved to: deployment_info.json")
        
    else:
        print("\n❌ Deployment failed")
        sys.exit(1)

if __name__ == "__main__":
    main()