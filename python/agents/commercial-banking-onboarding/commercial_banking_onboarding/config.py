"""Configuration settings for commercial banking onboarding system."""

import os

# Model configuration
MODEL = "gemini-2.5-pro"

# Environment settings
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# API configuration
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# Mock API settings
MOCK_APIS_ENABLED = os.getenv("MOCK_APIS_ENABLED", "true").lower() == "true"
MOCK_API_DELAY_MS = int(os.getenv("MOCK_API_DELAY_MS", "200"))
MOCK_API_FAILURE_RATE = float(os.getenv("MOCK_API_FAILURE_RATE", "0.02"))

# Banking configuration
DEFAULT_CURRENCY = "USD"
DEFAULT_TIMEZONE = "America/New_York"

# Compliance settings
SANCTIONS_SCREENING_ENABLED = True
PEP_SCREENING_ENABLED = True
ENHANCED_DUE_DILIGENCE_THRESHOLD = 100000  # $100K

# Processing thresholds
PROCESSING_SLA_DAYS = 14
ESCALATION_THRESHOLD_HOURS = 24
HIGH_RISK_MANUAL_REVIEW = True

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"