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

# Remove unnecessary files
RUN rm -rf .git deployment/ .pytest_cache/ __pycache__/ *.pyc

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV GOOGLE_GENAI_USE_VERTEXAI=1
ENV GOOGLE_CLOUD_PROJECT=agentic-experiments
ENV GOOGLE_CLOUD_LOCATION=us-central1

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "main.py"]