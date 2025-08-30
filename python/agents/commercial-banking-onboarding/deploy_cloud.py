#!/usr/bin/env python3
"""Cloud deployment with custom Dockerfile."""

import subprocess
import sys

def main():
    project_id = "agentic-experiments"
    region = "us-central1"
    service_name = "commercial-banking-onboarding"
    
    print("=== CLOUD DEPLOYMENT WITH CUSTOM DOCKERFILE ===")
    
    # Deploy with specific dockerfile
    deploy_cmd = f"""gcloud run deploy {service_name} \
        --source . \
        --dockerfile Dockerfile.cloud \
        --region {region} \
        --allow-unauthenticated \
        --port 8080 \
        --memory 2Gi \
        --cpu 2 \
        --timeout 600 \
        --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=1,GOOGLE_CLOUD_PROJECT={project_id},GOOGLE_CLOUD_LOCATION={region}" \
        --project {project_id} \
        --quiet"""
    
    print("Deploying with custom dockerfile...")
    result = subprocess.run(deploy_cmd, shell=True, text=True)
    
    if result.returncode == 0:
        print(f"\n✅ DEPLOYMENT SUCCESSFUL!")
        return True
    else:
        print("❌ Deployment failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)