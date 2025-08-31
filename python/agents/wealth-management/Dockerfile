# Dockerfile for Wealth Management Agent
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy application code and all supporting files
COPY . .

# Copy service account key
COPY service-account-key.json /app/service-account-key.json

# Remove unnecessary files
RUN rm -rf .git deployment/ .pytest_cache/ __pycache__/ *.pyc

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV GOOGLE_GENAI_USE_VERTEXAI=1
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/service-account-key.json
ENV GOOGLE_CLOUD_PROJECT=agentic-experiments
ENV VERTEX_AI_LOCATION=us-central1

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "main.py"]