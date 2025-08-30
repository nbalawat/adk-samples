# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the Agent Development Kit (ADK) Samples repository containing ready-to-use agents built on top of Google's Agent Development Kit for both Python and Java. The repository demonstrates a range of agent complexities from simple conversational bots to complex multi-agent workflows.

## Repository Structure

- `python/` - Python ADK samples with 18+ agent examples
- `java/` - Java ADK samples (2 agents currently)
- Each agent has its own directory with specific setup instructions

## Common Development Tasks

### Python Agents

**Prerequisites:**
- Python ADK installed and configured
- Python 3.9+ for most agents, 3.11+ for some newer agents
- Poetry or uv for dependency management (agents use different tools)

**Agent Development Workflow:**
1. Navigate to specific agent directory: `cd python/agents/<agent-name>`
2. Copy `.env.example` to `.env` and configure environment variables
3. Install dependencies:
   - Poetry-based agents: `poetry install`
   - uv-based agents: `uv sync`
4. Run agent locally:
   - CLI: `adk run .` (from core agent directory)
   - Dev UI: `adk web .` (from main agent directory)

**Testing:**
- Unit tests: `pytest` (from agent directory)
- Evaluations: `python eval/test_eval.py` (if eval/ directory exists)

**Deployment:**
- Most agents support Vertex AI Agent Engine deployment
- Use scripts in `deployment/` directory (typically `python deployment/deploy.py`)

**Special Cases:**
- `gemini-fullstack` uses Makefile: `make install`, `make dev`, `make lint`
- `data-science` uses uv instead of Poetry
- Some agents use both Poetry and uv in different configurations

### Java Agents

**Prerequisites:**
- Java ADK installed and configured
- JDK 17+ required
- Maven or Gradle build tools

**Agent Development Workflow:**
1. Navigate to agent directory: `cd java/agents/<agent-name>`
2. Copy example configuration files and fill in required variables
3. Build project:
   - Maven: `mvn clean install`
   - Gradle: `gradle build`
4. Run agent:
   - Executable JAR: `java -jar target/<agent-name>.jar`
   - Maven: `mvn exec:java`
   - ADK Dev UI: `mvn compile exec:java -Dexec.args="--server.port=8080 --adk.agents.source-dir=src/main/java/..."`

**Testing:**
- Unit tests: `mvn test` or `gradle test`

## Agent Architecture Patterns

### Python Agent Structure
```
agent-name/
├── agent_name/                 # Core logic (underscores)
│   ├── agent.py               # Main agent definition
│   ├── prompt.py              # Agent prompts
│   ├── tools/                 # Custom tools
│   ├── sub_agents/            # Multi-agent patterns
│   └── shared_libraries/      # Common utilities
├── deployment/                # Deployment scripts
├── eval/                      # Evaluation framework
├── tests/                     # Unit tests
├── .env.example              # Environment template
└── pyproject.toml            # Dependencies
```

### Java Agent Structure
```
agent-name/
├── src/main/java/com/google/adk/samples/agent/
│   ├── Agent.java            # Core agent logic
│   ├── tools/                # Custom tools
│   └── services/             # Business logic
├── deployment/               # Deployment configs
├── src/test/java/            # Tests
└── pom.xml                   # Maven config
```

## Key Technologies

**Python Agents:**
- Google ADK Python (google-adk package)
- Poetry or uv for dependency management
- Vertex AI and Google Cloud services
- BigQuery for data agents
- Various AI/ML libraries

**Java Agents:**
- Google ADK Java
- Maven build system
- Spring Boot (some agents)
- Vertex AI integration

## Environment Setup

All agents require:
- Google Cloud project with enabled APIs
- Vertex AI access
- Environment variables for API keys, project IDs, and regions
- Some agents require additional services (BigQuery, Dataform, etc.)

## Testing and Evaluation

- Most agents include evaluation frameworks in `eval/` directories
- Python agents typically use pytest for unit testing
- Java agents use JUnit/Maven for testing
- Evaluation data is provided in `.test.json` format
- Some agents include integration tests with external services

## Deployment

- Primary deployment target: Vertex AI Agent Engine
- Alternative deployments: Google Cloud Run, local development servers
- Deployment scripts handle Google Cloud configuration automatically
- Some agents include Docker configurations for containerized deployment
- Always consult the documentation for ADK while building agents - https://google.github.io/adk-docs/api-reference/python/
- Ensure that you consult other examples in the repository and the official API reference for google ADK