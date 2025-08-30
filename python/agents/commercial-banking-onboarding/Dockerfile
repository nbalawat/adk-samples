# Simple Dockerfile without uv complexity
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY commercial_banking_onboarding/ ./commercial_banking_onboarding/
COPY main.py .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV GOOGLE_GENAI_USE_VERTEXAI=1

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "main.py"]