#!/usr/bin/env python3
"""Ultra-minimal deployment using Cloud Build manually."""

import subprocess
import sys
import os

def main():
    """Deploy using manual Docker build."""
    project_id = "agentic-experiments"
    region = "us-central1"
    service_name = "commercial-banking-onboarding"
    
    print("=== MANUAL DEPLOYMENT ===")
    
    # Build and submit to Container Registry
    build_cmd = f"""
    gcloud builds submit --tag gcr.io/{project_id}/{service_name} \
        --project {project_id} \
        --machine-type=e2-highcpu-8 \
        --disk-size=100 \
        --timeout=20m
    """
    
    print(f"Building container...")
    result = subprocess.run(build_cmd, shell=True, text=True)
    
    if result.returncode != 0:
        print("Build failed!")
        return False
        
    # Deploy to Cloud Run
    deploy_cmd = f"""
    gcloud run deploy {service_name} \
        --image gcr.io/{project_id}/{service_name} \
        --region {region} \
        --allow-unauthenticated \
        --port 8080 \
        --memory 2Gi \
        --cpu 2 \
        --timeout 600 \
        --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=1,GOOGLE_CLOUD_PROJECT={project_id},GOOGLE_CLOUD_LOCATION={region}" \
        --project {project_id}
    """
    
    print(f"Deploying to Cloud Run...")
    result = subprocess.run(deploy_cmd, shell=True, text=True)
    
    if result.returncode == 0:
        print(f"\n✅ DEPLOYMENT SUCCESSFUL!")
        print(f"URL: https://{service_name}-{region.replace('-', '')}{project_id}.a.run.app")
        return True
    else:
        print("❌ Deployment failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)