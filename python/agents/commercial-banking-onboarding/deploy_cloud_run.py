#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deploy Commercial Banking Onboarding Agent to Google Cloud Run."""

import os
import sys
import subprocess
import json
import argparse
from pathlib import Path

def run_command(command, description=""):
    """Run a shell command and return the result."""
    print(f"[*] {description}")
    print(f"Running: {command}")
    
    result = subprocess.run(
        command, 
        shell=True, 
        capture_output=True, 
        text=True
    )
    
    if result.returncode != 0:
        print(f"[ERROR] {result.stderr}")
        return False, result.stderr
    
    if result.stdout:
        print(f"[SUCCESS] {result.stdout.strip()}")
    
    return True, result.stdout

def check_prerequisites():
    """Check if required tools are installed."""
    print("[*] Checking prerequisites...")
    
    # Check gcloud
    success, _ = run_command("gcloud version", "Checking gcloud CLI")
    if not success:
        print("[ERROR] gcloud CLI is not installed. Please install it first.")
        return False
    
    # Check Docker
    success, _ = run_command("docker --version", "Checking Docker")
    if not success:
        print("[ERROR] Docker is not installed. Please install it first.")
        return False
    
    # Check if authenticated
    success, _ = run_command("gcloud auth list --filter=status:ACTIVE", "Checking authentication")
    if not success:
        print("[ERROR] Please authenticate with gcloud: gcloud auth login")
        return False
    
    print("[SUCCESS] All prerequisites met!")
    return True

def deploy_to_cloud_run(project_id, region="us-central1", service_name="commercial-banking-onboarding"):
    """Deploy the application to Cloud Run."""
    
    if not check_prerequisites():
        return False
    
    print(f"\n[*] Starting deployment to Cloud Run...")
    print(f"Project: {project_id}")
    print(f"Region: {region}")
    print(f"Service: {service_name}")
    
    # Set the project
    success, _ = run_command(
        f"gcloud config set project {project_id}",
        "Setting active project"
    )
    if not success:
        return False
    
    # Enable required APIs
    apis = [
        "run.googleapis.com",
        "cloudbuild.googleapis.com",
        "aiplatform.googleapis.com",
        "artifactregistry.googleapis.com"
    ]
    
    for api in apis:
        success, _ = run_command(
            f"gcloud services enable {api}",
            f"Enabling {api}"
        )
        if not success:
            print(f"[WARNING] Failed to enable {api}, continuing...")
    
    # Create Artifact Registry repository if it doesn't exist
    repo_name = "adk-agents"
    success, _ = run_command(
        f"gcloud artifacts repositories create {repo_name} --repository-format=docker --location={region} --description='ADK Agents Repository' || true",
        f"Creating Artifact Registry repository"
    )
    
    # Build and deploy to Cloud Run
    image_url = f"{region}-docker.pkg.dev/{project_id}/{repo_name}/{service_name}"
    
    deploy_command = f"""gcloud run deploy {service_name} \
        --source . \
        --platform managed \
        --region {region} \
        --allow-unauthenticated \
        --port 8080 \
        --memory 2Gi \
        --cpu 2 \
        --timeout 900 \
        --concurrency 10 \
        --max-instances 10 \
        --min-instances 0 \
        --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=1,GOOGLE_CLOUD_PROJECT={project_id},GOOGLE_CLOUD_LOCATION={region}" \
        --quiet"""
    
    success, output = run_command(
        deploy_command,
        "Building and deploying to Cloud Run"
    )
    
    if not success:
        print("[ERROR] Deployment failed!")
        return False
    
    # Extract the service URL from output
    service_url = None
    for line in output.split('\n'):
        if 'https://' in line and 'run.app' in line:
            service_url = line.strip()
            break
    
    if service_url:
        print(f"\n[SUCCESS] DEPLOYMENT SUCCESSFUL!")
        print(f"Service URL: {service_url}")
        print(f"\nService Details:")
        print(f"   Project ID: {project_id}")
        print(f"   Region: {region}")
        print(f"   Service Name: {service_name}")
        print(f"   Image: {image_url}")
        
        # Save deployment info
        deployment_info = {
            "service_url": service_url,
            "project_id": project_id,
            "region": region,
            "service_name": service_name,
            "image_url": image_url,
            "deployment_type": "cloud_run"
        }
        
        info_file = Path("deployment_info.json")
        with open(info_file, 'w') as f:
            json.dump(deployment_info, f, indent=2)
        
        print(f"[*] Deployment info saved to: {info_file}")
        
        print(f"\nYour Commercial Banking Onboarding system is now live!")
        print(f"Try asking questions like:")
        print(f"   • 'I want to open a business banking account'")
        print(f"   • 'Can you verify my company's identity for compliance?'")
        print(f"   • 'We need a $200,000 credit line for expansion'")
        print(f"   • 'What documents do I need for onboarding?'")
        
        return True
    else:
        print("[ERROR] Could not extract service URL from deployment output")
        return False

def main():
    """Main deployment function."""
    parser = argparse.ArgumentParser(description="Deploy Commercial Banking Onboarding Agent to Cloud Run")
    parser.add_argument("--project-id", required=True, help="Google Cloud project ID")
    parser.add_argument("--region", default="us-central1", help="Cloud Run region")
    parser.add_argument("--service-name", default="commercial-banking-onboarding", help="Cloud Run service name")
    
    args = parser.parse_args()
    
    print("COMMERCIAL BANKING ONBOARDING - CLOUD RUN DEPLOYMENT")
    print("=" * 70)
    
    # Deploy to Cloud Run
    success = deploy_to_cloud_run(
        project_id=args.project_id,
        region=args.region,
        service_name=args.service_name
    )
    
    if success:
        print("\n[SUCCESS] Deployment completed successfully!")
        sys.exit(0)
    else:
        print("\n[ERROR] Deployment failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()