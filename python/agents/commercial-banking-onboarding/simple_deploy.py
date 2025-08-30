#!/usr/bin/env python3
"""Simple deployment script based on working ADK sample patterns."""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n[INFO] {description}")
    print(f"[CMD] {cmd}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"[SUCCESS] {description}")
        if result.stdout:
            print(result.stdout.strip())
        return True
    else:
        print(f"[ERROR] {description} failed")
        if result.stderr:
            print(result.stderr.strip())
        return False

def main():
    """Main deployment function."""
    project_id = "agentic-experiments"
    region = "us-central1"
    service_name = "commercial-banking-onboarding"
    
    print("=" * 70)
    print("COMMERCIAL BANKING ONBOARDING - SIMPLE DEPLOYMENT")
    print("=" * 70)
    
    # Check prerequisites
    if not run_command("gcloud version", "Checking gcloud CLI"):
        return False
        
    if not run_command("docker --version", "Checking Docker"):
        return False
    
    # Set project
    if not run_command(f"gcloud config set project {project_id}", "Setting project"):
        return False
    
    # Enable APIs
    apis = ["run.googleapis.com", "cloudbuild.googleapis.com"]
    for api in apis:
        run_command(f"gcloud services enable {api}", f"Enabling {api}")
    
    # Simple deployment with minimal config
    deploy_cmd = f"""gcloud run deploy {service_name} \
        --source . \
        --region {region} \
        --allow-unauthenticated \
        --port 8080 \
        --memory 1Gi \
        --cpu 1 \
        --timeout 600 \
        --min-instances 0 \
        --max-instances 5 \
        --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=1,GOOGLE_CLOUD_PROJECT={project_id},GOOGLE_CLOUD_LOCATION={region},SERVE_WEB_INTERFACE=true" \
        --quiet"""
    
    if run_command(deploy_cmd, "Deploying to Cloud Run"):
        print(f"\n{'='*70}")
        print("DEPLOYMENT SUCCESSFUL!")
        print(f"{'='*70}")
        print(f"Your Commercial Banking system should be available at:")
        print(f"https://{service_name}-{region.replace('-', '')}-{project_id}.run.app")
        return True
    else:
        print(f"\n{'='*70}")
        print("DEPLOYMENT FAILED!")
        print(f"{'='*70}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)