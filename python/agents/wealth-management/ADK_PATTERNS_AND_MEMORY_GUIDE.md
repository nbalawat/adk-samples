# ADK Patterns and Memory Management Guide

## Memory Usage and State Management

### ADK ToolContext State Management

The ADK provides persistent state management through `ToolContext.state` that maintains data across tool calls within a conversation session.

#### Key Memory Patterns

**1. Account Context Management**
```python
def remember_account(account_id: str, tool_context: ToolContext) -> dict:
    tool_context.state["primary_account_id"] = account_id
    tool_context.state["last_account_accessed"] = account_id
    return {"status": "SUCCESS", "account_id": account_id}

def get_current_account(tool_context: ToolContext) -> dict:
    current_account = tool_context.state.get("last_account_accessed")
    if current_account:
        return {"status": "SUCCESS", "account_id": current_account}
    else:
        return {"status": "NO_ACCOUNT", "available_accounts": [...]}
```

**2. User Preferences Storage**
```python
def store_user_preference(key: str, value: str, tool_context: ToolContext) -> dict:
    if "user_preferences" not in tool_context.state:
        tool_context.state["user_preferences"] = {}
    tool_context.state["user_preferences"][key] = value
```

**3. Conversation Context**
```python
def store_conversation_context(context_type: str, context_data: Dict[str, Any], tool_context: ToolContext) -> dict:
    if "conversation_context" not in tool_context.state:
        tool_context.state["conversation_context"] = {}
    tool_context.state["conversation_context"][context_type] = context_data
```

#### Memory Best Practices

**✅ DO:**
- Store frequently accessed data (account IDs, client preferences)
- Use structured keys for different data types
- Implement fallback behavior when memory is empty
- Clean up stale data to avoid memory bloat
- Use memory for context-aware tool behavior

**❌ DON'T:**
- Store large objects or binary data
- Assume memory will persist across different sessions
- Store sensitive information like passwords
- Use memory as primary data storage
- Ignore memory initialization in tools

### Context-Aware Tool Design

Every tool should handle the case where no context exists:

```python
def get_portfolio_summary(account_id: Optional[str] = None, tool_context: ToolContext = None) -> dict:
    # Use context-aware account resolution
    if not account_id and tool_context:
        account_context = get_current_account(tool_context)
        if account_context["status"] == "SUCCESS":
            account_id = account_context["account_id"]
        else:
            return {
                "status": "ERROR",
                "message": "No account specified and no account remembered. Please provide an account ID.",
                "available_accounts": account_context.get("available_accounts", [])
            }
    
    # Remember this account for future use
    if account_id and tool_context:
        remember_account(account_id, tool_context)
```

## Workflow Orchestration Patterns

### 1. Sequential Pattern

**Use Case**: Step-by-step workflows where each step depends on the previous
**Implementation**: `wealth_management/sub_agents/market_response_agent.py`

```python
class MarketResponseAgent(Agent):
    async def run_async(self, query: str) -> str:
        # Step 1: Analyze volatility
        analysis = await self._call_tool("analyze_market_volatility", {...})
        
        # Step 2: Generate commentary (depends on analysis)
        commentary = await self._call_tool("generate_market_commentary", {
            "event_type": analysis.get("event_type")
        })
        
        # Step 3: Assess impact (uses both previous results)
        impact = await self._call_tool("assess_portfolio_impact", {
            "market_event": analysis.get("severity")
        })
        
        # Step 4: Coordinate outreach (final step)
        outreach = await self._call_tool("trigger_proactive_outreach", {
            "severity": impact.get("overall_severity")
        })
```

**Key Considerations:**
- Each step must complete before the next begins
- Error handling at each step affects downstream steps
- Information flows sequentially through the pipeline
- Good for processes requiring validation at each step

### 2. Parallel Pattern

**Use Case**: Independent tasks that can run simultaneously
**Implementation**: `wealth_management/sub_agents/client_onboarding_agent.py`

```python
class ClientOnboardingAgent(Agent):
    async def run_async(self, query: str) -> str:
        # All tasks run in parallel
        results = await asyncio.gather(
            self._call_tool("collect_kyc_information", {...}),
            self._call_tool("assess_risk_tolerance", {...}),
            self._call_tool("set_investment_goals", {...}),
            self._call_tool("create_client_profile", {...}),
            return_exceptions=True
        )
```

**Key Considerations:**
- Tasks must be truly independent
- Handle partial failures gracefully
- Aggregate results from all parallel tasks
- 5x efficiency gain over sequential processing
- Resource contention if too many parallel tasks

### 3. Loop Pattern

**Use Case**: Continuous monitoring with intelligent termination
**Implementation**: `wealth_management/sub_agents/portfolio_monitoring_agent.py`

```python
class PortfolioMonitoringAgent(Agent):
    async def run_async(self, query: str) -> str:
        iteration = 1
        max_iterations = 5
        completion_criteria_met = False
        
        while iteration <= max_iterations and not completion_criteria_met:
            # Perform analysis iteration
            results = await self._call_tool("comprehensive_portfolio_analysis", {
                "iteration": iteration
            })
            
            # Check if we've found everything we need
            completion_criteria_met = self._check_completion_criteria(results)
            iteration += 1
        
        return f"Analysis complete after {iteration-1} iterations"
```

**Key Considerations:**
- Always have maximum iteration limits
- Define clear completion criteria
- Each iteration should add incremental value
- Avoid infinite loops with intelligent termination
- Log progress for debugging

### 4. Master Orchestration Pattern

**Use Case**: Complex scenarios requiring multiple coordinated workflows
**Implementation**: Main agent intelligently routing to sub-agents

```python
class WealthManagementAgent(Agent):
    async def analyze_scenario_and_route(self, query: str) -> str:
        # Analyze query complexity and requirements
        scenario_analysis = self._analyze_query_complexity(query)
        
        if scenario_analysis["requires_multiple_workflows"]:
            # Route to multiple specialized agents
            workflows = []
            
            if scenario_analysis["market_crisis"]:
                workflows.append("market_response_sequential")
            
            if scenario_analysis["client_panic"]:
                workflows.append("crisis_management_sequential")
            
            if scenario_analysis["new_client"]:
                workflows.append("client_onboarding_parallel")
            
            # Execute coordinated workflows
            return await self._execute_coordinated_workflows(workflows, query)
        else:
            # Route to single appropriate workflow
            return await self._route_to_single_workflow(query)
```

**Key Considerations:**
- Intelligent query analysis for routing decisions
- Coordinate information sharing between workflows
- Handle workflow dependencies and sequencing
- Provide unified response aggregation
- Monitor overall system resource usage

## Critical Things to Bear in Mind

### Memory Management
1. **Session Scope**: Memory persists only within a conversation session
2. **Size Limits**: Don't store large objects; use references to external data
3. **Privacy**: Never store sensitive data in memory
4. **Cleanup**: Implement memory cleanup for long-running sessions

### Workflow Design
1. **Error Resilience**: Design for partial failures in parallel patterns
2. **Resource Management**: Monitor concurrent operations to avoid overload
3. **Timeout Handling**: All async operations should have reasonable timeouts
4. **Progress Visibility**: Provide status updates for long-running workflows

### Performance Considerations
1. **Parallel vs Sequential**: Use parallel only for truly independent tasks
2. **Loop Termination**: Always have multiple exit conditions for loops
3. **Tool Call Efficiency**: Minimize redundant tool calls through caching
4. **State Sharing**: Use memory to avoid re-fetching the same data

### ADK Integration
1. **Tool Context**: Always handle None ToolContext gracefully
2. **Function Signatures**: ADK tools don't take ToolContext as parameters
3. **Error Format**: Return consistent error dictionaries with status fields
4. **Async Patterns**: Use proper async/await for tool calls in sub-agents

### Testing and Debugging
1. **Mock APIs**: Essential for testing without external dependencies
2. **State Inspection**: Log memory state for debugging context issues
3. **Workflow Tracing**: Track execution flow through complex patterns
4. **Error Propagation**: Ensure errors bubble up with context

This guide represents patterns learned from building a production-ready wealth management system with ADK, demonstrating how sophisticated AI orchestration can solve complex business problems efficiently.