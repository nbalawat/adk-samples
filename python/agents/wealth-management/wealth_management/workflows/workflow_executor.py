"""Workflow execution engine for all 33 wealth management workflows"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from uuid import uuid4

from .workflow_registry import WorkflowRegistry, WorkflowDefinition, WorkflowStatus, ADKPattern
from ..data.loader import data_loader
from ..tools.analytics_service import analytics_service

logger = logging.getLogger(__name__)

class WorkflowExecution:
    """Represents a single workflow execution instance"""
    
    def __init__(self, workflow_def: WorkflowDefinition, execution_id: str = None,
                 context: Dict[str, Any] = None):
        self.execution_id = execution_id or str(uuid4())
        self.workflow_def = workflow_def
        self.status = WorkflowStatus.PENDING
        self.context = context or {}
        self.results = {}
        self.step_results = []
        self.started_at = None
        self.completed_at = None
        self.error_message = None
        self.current_step = 0
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert execution to dictionary"""
        return {
            "execution_id": self.execution_id,
            "workflow_id": self.workflow_def.workflow_id,
            "workflow_name": self.workflow_def.name,
            "status": self.status.value,
            "context": self.context,
            "results": self.results,
            "step_results": self.step_results,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error_message": self.error_message,
            "current_step": self.current_step,
            "total_steps": len(self.workflow_def.steps)
        }

class WorkflowExecutor:
    """Executes workflows based on their ADK patterns and definitions"""
    
    def __init__(self, workflow_registry: WorkflowRegistry):
        self.registry = workflow_registry
        self.active_executions: Dict[str, WorkflowExecution] = {}
        self.execution_history: List[WorkflowExecution] = []
        
        # Pattern execution handlers
        self.pattern_handlers = {
            ADKPattern.SEQUENTIAL: self._execute_sequential,
            ADKPattern.PARALLEL: self._execute_parallel,
            ADKPattern.LOOP: self._execute_loop,
            ADKPattern.EVENT_DRIVEN: self._execute_event_driven,
            ADKPattern.SCHEDULED: self._execute_scheduled,
            ADKPattern.MASTER_ORCHESTRATION: self._execute_master_orchestration
        }
    
    async def execute_workflow(self, workflow_id: str, context: Dict[str, Any] = None) -> WorkflowExecution:
        """Execute a workflow by ID"""
        
        workflow_def = self.registry.get_workflow(workflow_id)
        if not workflow_def:
            raise ValueError(f"Workflow {workflow_id} not found in registry")
        
        execution = WorkflowExecution(workflow_def, context=context)
        execution.status = WorkflowStatus.IN_PROGRESS
        execution.started_at = datetime.now()
        
        self.active_executions[execution.execution_id] = execution
        
        logger.info(f"Starting execution of workflow {workflow_id} (execution_id: {execution.execution_id})")
        
        try:
            # Get pattern-specific handler
            handler = self.pattern_handlers.get(workflow_def.pattern)
            if not handler:
                raise ValueError(f"No handler for pattern {workflow_def.pattern}")
            
            # Execute workflow using appropriate pattern
            results = await handler(execution)
            
            # Update execution with results
            execution.results = results
            execution.status = WorkflowStatus.COMPLETED
            execution.completed_at = datetime.now()
            
            logger.info(f"Completed execution of workflow {workflow_id}")
            
        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            execution.error_message = str(e)
            execution.completed_at = datetime.now()
            
            logger.error(f"Failed execution of workflow {workflow_id}: {str(e)}")
        
        # Move to history
        if execution.execution_id in self.active_executions:
            del self.active_executions[execution.execution_id]
        self.execution_history.append(execution)
        
        return execution
    
    async def _execute_sequential(self, execution: WorkflowExecution) -> Dict[str, Any]:
        """Execute sequential workflow pattern"""
        
        results = {
            "pattern": "sequential",
            "steps_completed": [],
            "execution_time": 0
        }
        
        start_time = datetime.now()
        
        for i, step in enumerate(execution.workflow_def.steps):
            execution.current_step = i
            
            logger.debug(f"Executing step {i+1}/{len(execution.workflow_def.steps)}: {step}")
            
            # Execute step based on workflow type
            step_result = await self._execute_step(
                step, 
                execution.workflow_def, 
                execution.context
            )
            
            execution.step_results.append({
                "step_number": i + 1,
                "step_name": step,
                "result": step_result,
                "timestamp": datetime.now().isoformat()
            })
            
            results["steps_completed"].append(step)
            
            # Small delay to simulate realistic processing
            await asyncio.sleep(0.1)
        
        results["execution_time"] = (datetime.now() - start_time).total_seconds()
        return results
    
    async def _execute_parallel(self, execution: WorkflowExecution) -> Dict[str, Any]:
        """Execute parallel workflow pattern"""
        
        results = {
            "pattern": "parallel",
            "parallel_tasks": [],
            "execution_time": 0
        }
        
        start_time = datetime.now()
        
        # Create tasks for parallel execution
        tasks = []
        for i, step in enumerate(execution.workflow_def.steps):
            task = self._execute_step(step, execution.workflow_def, execution.context)
            tasks.append(task)
        
        # Execute all steps in parallel
        step_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for i, (step, result) in enumerate(zip(execution.workflow_def.steps, step_results)):
            execution.step_results.append({
                "step_number": i + 1,
                "step_name": step,
                "result": result if not isinstance(result, Exception) else str(result),
                "timestamp": datetime.now().isoformat(),
                "success": not isinstance(result, Exception)
            })
            
            results["parallel_tasks"].append({
                "step": step,
                "success": not isinstance(result, Exception)
            })
        
        results["execution_time"] = (datetime.now() - start_time).total_seconds()
        return results
    
    async def _execute_loop(self, execution: WorkflowExecution) -> Dict[str, Any]:
        """Execute loop workflow pattern"""
        
        results = {
            "pattern": "loop",
            "iterations": 0,
            "loop_results": [],
            "execution_time": 0
        }
        
        start_time = datetime.now()
        max_iterations = execution.context.get("max_iterations", 3)
        
        for iteration in range(max_iterations):
            logger.debug(f"Loop iteration {iteration + 1}/{max_iterations}")
            
            iteration_results = []
            
            for i, step in enumerate(execution.workflow_def.steps):
                step_result = await self._execute_step(
                    step,
                    execution.workflow_def,
                    {**execution.context, "iteration": iteration + 1}
                )
                iteration_results.append({
                    "step": step,
                    "result": step_result
                })
                
                await asyncio.sleep(0.05)  # Short delay between steps
            
            results["loop_results"].append({
                "iteration": iteration + 1,
                "steps": iteration_results,
                "timestamp": datetime.now().isoformat()
            })
            
            results["iterations"] = iteration + 1
            
            # Check continuation condition
            if not self._should_continue_loop(execution, iteration_results):
                break
        
        results["execution_time"] = (datetime.now() - start_time).total_seconds()
        return results
    
    async def _execute_event_driven(self, execution: WorkflowExecution) -> Dict[str, Any]:
        """Execute event-driven workflow pattern"""
        
        results = {
            "pattern": "event_driven",
            "event_processed": True,
            "response_time": 0,
            "actions_taken": []
        }
        
        start_time = datetime.now()
        
        # Simulate event processing
        event_type = execution.context.get("event_type", "market_volatility")
        event_severity = execution.context.get("severity", "medium")
        
        logger.debug(f"Processing event: {event_type} (severity: {event_severity})")
        
        # Execute event-specific response steps
        for step in execution.workflow_def.steps:
            if self._should_execute_event_step(step, event_type, event_severity):
                step_result = await self._execute_step(
                    step,
                    execution.workflow_def,
                    execution.context
                )
                
                results["actions_taken"].append({
                    "action": step,
                    "result": step_result,
                    "timestamp": datetime.now().isoformat()
                })
                
                await asyncio.sleep(0.1)
        
        results["response_time"] = (datetime.now() - start_time).total_seconds()
        return results
    
    async def _execute_scheduled(self, execution: WorkflowExecution) -> Dict[str, Any]:
        """Execute scheduled workflow pattern"""
        
        results = {
            "pattern": "scheduled",
            "schedule_type": execution.context.get("schedule_type", "periodic"),
            "execution_time": 0,
            "scheduled_tasks": []
        }
        
        start_time = datetime.now()
        
        # Execute scheduled tasks
        for step in execution.workflow_def.steps:
            step_result = await self._execute_step(
                step,
                execution.workflow_def,
                execution.context
            )
            
            results["scheduled_tasks"].append({
                "task": step,
                "result": step_result,
                "executed_at": datetime.now().isoformat()
            })
            
            await asyncio.sleep(0.05)
        
        # Schedule next execution if recurring
        if execution.context.get("recurring", False):
            next_run = self._calculate_next_run(execution.context)
            results["next_scheduled_run"] = next_run.isoformat()
        
        results["execution_time"] = (datetime.now() - start_time).total_seconds()
        return results
    
    async def _execute_master_orchestration(self, execution: WorkflowExecution) -> Dict[str, Any]:
        """Execute master orchestration pattern"""
        
        results = {
            "pattern": "master_orchestration",
            "sub_workflows": [],
            "coordination_results": {},
            "execution_time": 0
        }
        
        start_time = datetime.now()
        
        # Orchestrate multiple sub-workflows
        sub_workflow_ids = execution.context.get("sub_workflows", [])
        
        for sub_workflow_id in sub_workflow_ids:
            try:
                sub_execution = await self.execute_workflow(
                    sub_workflow_id,
                    execution.context
                )
                
                results["sub_workflows"].append({
                    "workflow_id": sub_workflow_id,
                    "execution_id": sub_execution.execution_id,
                    "status": sub_execution.status.value,
                    "result_summary": self._summarize_execution(sub_execution)
                })
                
            except Exception as e:
                results["sub_workflows"].append({
                    "workflow_id": sub_workflow_id,
                    "status": "failed",
                    "error": str(e)
                })
        
        results["execution_time"] = (datetime.now() - start_time).total_seconds()
        return results
    
    async def _execute_step(self, step: str, workflow_def: WorkflowDefinition, 
                          context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step"""
        
        # Simulate step execution based on step type and available tools
        step_lower = step.lower()
        
        try:
            # Portfolio-related steps
            if "portfolio" in step_lower:
                if "performance" in step_lower:
                    return await self._execute_portfolio_performance_step(context)
                elif "risk" in step_lower:
                    return await self._execute_portfolio_risk_step(context)
                elif "rebalance" in step_lower:
                    return await self._execute_rebalancing_step(context)
            
            # Client-related steps  
            elif "client" in step_lower:
                if "onboard" in step_lower or "kyc" in step_lower:
                    return await self._execute_client_onboarding_step(context)
                elif "communication" in step_lower:
                    return await self._execute_client_communication_step(context)
                elif "meeting" in step_lower:
                    return await self._execute_client_meeting_step(context)
            
            # Market-related steps
            elif "market" in step_lower:
                if "analysis" in step_lower or "volatility" in step_lower:
                    return await self._execute_market_analysis_step(context)
                elif "commentary" in step_lower:
                    return await self._execute_market_commentary_step(context)
            
            # Compliance-related steps
            elif "compliance" in step_lower or "regulatory" in step_lower:
                return await self._execute_compliance_step(context)
            
            # Tax-related steps
            elif "tax" in step_lower:
                return await self._execute_tax_optimization_step(context)
            
            # Default generic step execution
            else:
                return await self._execute_generic_step(step, context)
                
        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Step execution failed: {str(e)}",
                "step": step
            }
    
    async def _execute_portfolio_performance_step(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute portfolio performance analysis step"""
        await asyncio.sleep(0.2)  # Simulate processing time
        
        client_id = context.get("client_id", "WM000001")
        portfolio = data_loader.get_portfolio_by_client_id(client_id)
        
        if portfolio:
            return {
                "status": "SUCCESS",
                "portfolio_value": portfolio["total_value"],
                "ytd_return": portfolio["performance"]["ytd_return"],
                "benchmark_comparison": "outperforming",
                "analysis_date": datetime.now().isoformat()
            }
        else:
            return {
                "status": "SUCCESS", 
                "portfolio_value": 1000000,
                "ytd_return": 0.08,
                "benchmark_comparison": "in-line",
                "analysis_date": datetime.now().isoformat()
            }
    
    async def _execute_client_communication_step(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute client communication step"""
        await asyncio.sleep(0.1)
        
        return {
            "status": "SUCCESS",
            "communication_sent": True,
            "delivery_method": context.get("communication_method", "email"),
            "client_count": context.get("client_count", 1),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _execute_market_analysis_step(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute market analysis step"""
        await asyncio.sleep(0.3)
        
        return {
            "status": "SUCCESS",
            "volatility_level": "moderate",
            "market_direction": "neutral",
            "key_indicators": {
                "vix_level": 18.5,
                "sp500_return": 0.012,
                "bond_yield": 0.045
            },
            "analysis_date": datetime.now().isoformat()
        }
    
    async def _execute_generic_step(self, step: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute generic workflow step"""
        await asyncio.sleep(0.1)
        
        return {
            "status": "SUCCESS",
            "step_name": step,
            "execution_result": "completed",
            "timestamp": datetime.now().isoformat(),
            "context_keys": list(context.keys())
        }
    
    def _should_continue_loop(self, execution: WorkflowExecution, 
                             iteration_results: List[Dict[str, Any]]) -> bool:
        """Determine if loop should continue"""
        # Simple continuation logic - can be made more sophisticated
        return len(iteration_results) > 0 and execution.current_step < 5
    
    def _should_execute_event_step(self, step: str, event_type: str, severity: str) -> bool:
        """Determine if event step should be executed based on event characteristics"""
        step_lower = step.lower()
        
        # High severity events trigger more steps
        if severity == "high":
            return True
        
        # Medium severity events skip some optional steps
        if severity == "medium":
            return "critical" not in step_lower and "emergency" not in step_lower
        
        # Low severity events only execute essential steps  
        return "assess" in step_lower or "monitor" in step_lower
    
    def _calculate_next_run(self, context: Dict[str, Any]) -> datetime:
        """Calculate next scheduled run time"""
        schedule_type = context.get("schedule_type", "daily")
        
        if schedule_type == "hourly":
            return datetime.now() + timedelta(hours=1)
        elif schedule_type == "daily":
            return datetime.now() + timedelta(days=1)
        elif schedule_type == "weekly":
            return datetime.now() + timedelta(weeks=1)
        elif schedule_type == "monthly":
            return datetime.now() + timedelta(days=30)
        else:
            return datetime.now() + timedelta(days=1)
    
    def _summarize_execution(self, execution: WorkflowExecution) -> Dict[str, Any]:
        """Create summary of workflow execution"""
        return {
            "status": execution.status.value,
            "steps_completed": len(execution.step_results),
            "total_steps": len(execution.workflow_def.steps),
            "execution_time": (
                (execution.completed_at - execution.started_at).total_seconds()
                if execution.completed_at and execution.started_at else 0
            ),
            "success_rate": len([r for r in execution.step_results if r.get("success", True)]) / max(len(execution.step_results), 1)
        }
    
    def get_execution_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of workflow execution"""
        execution = self.active_executions.get(execution_id)
        if execution:
            return execution.to_dict()
        
        # Check history
        for exec_hist in self.execution_history:
            if exec_hist.execution_id == execution_id:
                return exec_hist.to_dict()
        
        return None
    
    def get_active_executions(self) -> List[Dict[str, Any]]:
        """Get all currently active executions"""
        return [exec.to_dict() for exec in self.active_executions.values()]
    
    def get_execution_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent execution history"""
        return [exec.to_dict() for exec in self.execution_history[-limit:]]
    
    def get_executor_stats(self) -> Dict[str, Any]:
        """Get executor statistics"""
        total_executions = len(self.execution_history)
        successful = len([e for e in self.execution_history if e.status == WorkflowStatus.COMPLETED])
        failed = len([e for e in self.execution_history if e.status == WorkflowStatus.FAILED])
        
        return {
            "active_executions": len(self.active_executions),
            "total_executions": total_executions,
            "successful_executions": successful,
            "failed_executions": failed,
            "success_rate": successful / max(total_executions, 1),
            "average_execution_time": self._calculate_average_execution_time(),
            "most_executed_workflows": self._get_most_executed_workflows()
        }
    
    def _calculate_average_execution_time(self) -> float:
        """Calculate average execution time for completed workflows"""
        completed = [e for e in self.execution_history if e.completed_at and e.started_at]
        if not completed:
            return 0.0
        
        total_time = sum((e.completed_at - e.started_at).total_seconds() for e in completed)
        return total_time / len(completed)
    
    def _get_most_executed_workflows(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get most frequently executed workflows"""
        workflow_counts = {}
        for execution in self.execution_history:
            wf_id = execution.workflow_def.workflow_id
            workflow_counts[wf_id] = workflow_counts.get(wf_id, 0) + 1
        
        # Sort by count and return top workflows
        sorted_workflows = sorted(workflow_counts.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {
                "workflow_id": wf_id,
                "execution_count": count,
                "workflow_name": self.registry.get_workflow(wf_id).name if self.registry.get_workflow(wf_id) else "Unknown"
            }
            for wf_id, count in sorted_workflows[:limit]
        ]

# Additional convenience methods for step execution
async def _execute_client_onboarding_step(context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute client onboarding step"""
    await asyncio.sleep(0.2)
    return {
        "status": "SUCCESS",
        "onboarding_stage": "kyc_collection",
        "documents_collected": 3,
        "completion_percentage": 0.6
    }

async def _execute_rebalancing_step(context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute portfolio rebalancing step"""
    await asyncio.sleep(0.15)
    return {
        "status": "SUCCESS",
        "trades_generated": 5,
        "total_trade_value": 150000,
        "rebalancing_cost": 85.50
    }

async def _execute_compliance_step(context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute compliance-related step"""
    await asyncio.sleep(0.1)
    return {
        "status": "SUCCESS",
        "compliance_check": "passed",
        "regulations_reviewed": 3,
        "documentation_complete": True
    }

async def _execute_tax_optimization_step(context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute tax optimization step"""
    await asyncio.sleep(0.2)
    return {
        "status": "SUCCESS",
        "tax_savings_identified": 12500,
        "strategies_recommended": 4,
        "implementation_timeline": "Q4 2024"
    }

async def _execute_portfolio_risk_step(context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute portfolio risk analysis step"""
    await asyncio.sleep(0.25)
    return {
        "status": "SUCCESS",
        "risk_score": 6.2,
        "var_95": 0.023,
        "concentration_risk": "moderate",
        "recommendations": ["diversify sector allocation", "reduce single position size"]
    }

async def _execute_client_meeting_step(context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute client meeting step"""
    await asyncio.sleep(0.1)
    return {
        "status": "SUCCESS",
        "meeting_type": context.get("meeting_type", "review"),
        "agenda_items": 5,
        "action_items_generated": 3,
        "follow_up_scheduled": True
    }

async def _execute_market_commentary_step(context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute market commentary generation step"""
    await asyncio.sleep(0.15)
    return {
        "status": "SUCCESS",
        "commentary_length": 450,
        "key_topics": ["market outlook", "sector rotation", "risk factors"],
        "distribution_channels": ["email", "portal", "newsletter"]
    }