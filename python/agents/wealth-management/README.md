# Wealth Management Agent System

A comprehensive wealth management agent system built on Google Agent Development Kit (ADK) demonstrating sophisticated multi-agent orchestration patterns.

## Quick Start

```bash
# Install dependencies
uv sync

# Run the ADK web interface
uv run adk web . --port 8080

# Access demo at: http://localhost:8080/dev-ui/
```

## Demo Scenarios

### Sequential Workflow Pattern
```
BREAKING: S&P 500 crashed 18% today! Execute complete market response workflow.
```

### Parallel Workflow Pattern  
```
New client wants comprehensive onboarding TODAY. Process everything simultaneously!
```

### Loop Workflow Pattern
```
Start continuous portfolio monitoring for DEMO001. Keep analyzing until you find everything.
```

### Master Orchestration Pattern
```
CRISIS SITUATION: Market crashed 20%, multiple clients panicking, and we have a new client wanting to onboard despite the chaos!
```

## System Architecture

- **Main Agent**: `wealth_management/agent.py` - Master orchestrator with 25+ tools
- **Sub-Agents**: Specialized agents for sequential, parallel, and loop patterns
- **Mock APIs**: 8 realistic financial APIs for custodian, market data, CRM, etc.
- **Memory Tools**: Context-aware state management using ADK ToolContext

## Key Features

- ✅ 4 ADK orchestration patterns (Sequential, Parallel, Loop, Master)
- ✅ 25+ specialized financial tools
- ✅ Context retention and memory management
- ✅ Professional-grade outputs with realistic financial data
- ✅ Error handling and graceful degradation

## Environment Variables

Copy `.env.example` to `.env` and configure:
- `GOOGLE_APPLICATION_CREDENTIALS`
- `GOOGLE_CLOUD_PROJECT`
- `GOOGLE_CLOUD_REGION`

## Deployment

```bash
python deployment/deploy.py
```

Built with Google Agent Development Kit - demonstrating enterprise-level AI orchestration for wealth management.