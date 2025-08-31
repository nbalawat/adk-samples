"""Comprehensive testing framework for all 33 wealth management workflows"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict

from .workflow_registry import WorkflowRegistry, ADKPattern, WorkflowCategory
from .workflow_executor import WorkflowExecutor, WorkflowExecution, WorkflowStatus
from ..data.loader import data_loader

logger = logging.getLogger(__name__)

@dataclass
class TestCase:
    """Individual test case for workflow testing"""
    test_id: str
    workflow_id: str
    test_name: str
    description: str
    input_context: Dict[str, Any]
    expected_outcomes: Dict[str, Any]
    test_category: str
    priority: str  # high, medium, low
    timeout_seconds: int = 30

@dataclass 
class TestResult:
    """Result of a single test execution"""
    test_case: TestCase
    execution: Optional[WorkflowExecution]
    passed: bool
    error_message: Optional[str]
    execution_time: float
    performance_metrics: Dict[str, Any]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self.test_case),
            "execution_id": self.execution.execution_id if self.execution else None,
            "passed": self.passed,
            "error_message": self.error_message,
            "execution_time": self.execution_time,
            "performance_metrics": self.performance_metrics,
            "timestamp": self.timestamp.isoformat()
        }

class WorkflowTestFramework:
    """Comprehensive testing framework for workflow validation"""
    
    def __init__(self, workflow_registry: WorkflowRegistry, workflow_executor: WorkflowExecutor):
        self.registry = workflow_registry
        self.executor = workflow_executor
        self.test_cases: Dict[str, TestCase] = {}
        self.test_results: List[TestResult] = []
        
        # Initialize test cases
        self._create_test_cases()
    
    def _create_test_cases(self):
        """Create comprehensive test cases for all workflows"""
        
        # Generate test cases for each workflow in registry
        for workflow in self.registry.get_all_workflows():
            self._create_workflow_test_cases(workflow)
    
    def _create_workflow_test_cases(self, workflow_def):
        """Create test cases for a specific workflow"""
        
        workflow_id = workflow_def.workflow_id
        
        # Basic functionality test
        basic_test = TestCase(
            test_id=f"{workflow_id}_BASIC",
            workflow_id=workflow_id,
            test_name=f"{workflow_def.name} - Basic Functionality",
            description=f"Test basic execution of {workflow_def.name} workflow",
            input_context=self._generate_basic_context(workflow_def),
            expected_outcomes={
                "status": "COMPLETED",
                "steps_completed": len(workflow_def.steps),
                "execution_time_max": 30.0
            },
            test_category="functionality",
            priority="high"
        )
        self.test_cases[basic_test.test_id] = basic_test
        
        # Error handling test
        error_test = TestCase(
            test_id=f"{workflow_id}_ERROR",
            workflow_id=workflow_id,
            test_name=f"{workflow_def.name} - Error Handling",
            description=f"Test error handling in {workflow_def.name} workflow",
            input_context=self._generate_error_context(workflow_def),
            expected_outcomes={
                "handles_errors": True,
                "graceful_degradation": True
            },
            test_category="error_handling",
            priority="high"
        )
        self.test_cases[error_test.test_id] = error_test
        
        # Performance test
        performance_test = TestCase(
            test_id=f"{workflow_id}_PERF",
            workflow_id=workflow_id,
            test_name=f"{workflow_def.name} - Performance",
            description=f"Test performance characteristics of {workflow_def.name}",
            input_context=self._generate_performance_context(workflow_def),
            expected_outcomes={
                "execution_time_max": self._get_performance_threshold(workflow_def),
                "memory_usage_reasonable": True,
                "resource_cleanup": True
            },
            test_category="performance",
            priority="medium"
        )
        self.test_cases[performance_test.test_id] = performance_test
        
        # Integration test (if workflow uses external data)
        if self._requires_integration_testing(workflow_def):
            integration_test = TestCase(
                test_id=f"{workflow_id}_INTEGRATION",
                workflow_id=workflow_id,
                test_name=f"{workflow_def.name} - Integration",
                description=f"Test integration with external systems for {workflow_def.name}",
                input_context=self._generate_integration_context(workflow_def),
                expected_outcomes={
                    "external_data_access": True,
                    "data_consistency": True,
                    "transaction_integrity": True
                },
                test_category="integration",
                priority="medium"
            )
            self.test_cases[integration_test.test_id] = integration_test
        
        # Pattern-specific tests
        pattern_test = self._create_pattern_specific_test(workflow_def)
        if pattern_test:
            self.test_cases[pattern_test.test_id] = pattern_test
    
    def _generate_basic_context(self, workflow_def) -> Dict[str, Any]:
        """Generate basic context for workflow testing"""
        
        base_context = {
            "test_mode": True,
            "client_id": "WM000001",
            "execution_date": datetime.now().isoformat()
        }
        
        # Add workflow-specific context
        if workflow_def.category == WorkflowCategory.ADVISOR_WORKFLOWS:
            base_context.update({
                "advisor_id": "ADV001",
                "client_count": 1,
                "meeting_type": "review"
            })
        elif workflow_def.category == WorkflowCategory.CLIENT_WORKFLOWS:
            base_context.update({
                "client_id": "WM000001",
                "session_type": "planning",
                "goal_type": "retirement"
            })
        else:  # Operations
            base_context.update({
                "operation_type": "account_maintenance",
                "batch_size": 10,
                "priority": "standard"
            })
        
        # Pattern-specific context
        if workflow_def.pattern == ADKPattern.EVENT_DRIVEN:
            base_context.update({
                "event_type": "market_volatility",
                "severity": "medium",
                "trigger_threshold": 15.0
            })
        elif workflow_def.pattern == ADKPattern.SCHEDULED:
            base_context.update({
                "schedule_type": "daily",
                "recurring": True,
                "next_run": (datetime.now()).isoformat()
            })
        elif workflow_def.pattern == ADKPattern.LOOP:
            base_context.update({
                "max_iterations": 3,
                "convergence_threshold": 0.01
            })
        elif workflow_def.pattern == ADKPattern.PARALLEL:
            base_context.update({
                "max_concurrent_tasks": 5,
                "task_timeout": 10
            })
        
        return base_context
    
    def _generate_error_context(self, workflow_def) -> Dict[str, Any]:
        """Generate context that should trigger error handling"""
        
        error_context = self._generate_basic_context(workflow_def)
        error_context.update({
            "force_error": True,
            "invalid_client_id": "INVALID_ID",
            "missing_required_field": None,
            "timeout_simulation": True
        })
        
        return error_context
    
    def _generate_performance_context(self, workflow_def) -> Dict[str, Any]:
        """Generate context for performance testing"""
        
        perf_context = self._generate_basic_context(workflow_def)
        
        # Add load for performance testing
        if workflow_def.pattern == ADKPattern.PARALLEL:
            perf_context.update({
                "client_count": 100,
                "concurrent_operations": 10
            })
        elif workflow_def.pattern == ADKPattern.LOOP:
            perf_context.update({
                "max_iterations": 10,
                "large_dataset": True
            })
        else:
            perf_context.update({
                "client_count": 50,
                "data_volume": "large"
            })
        
        return perf_context
    
    def _generate_integration_context(self, workflow_def) -> Dict[str, Any]:
        """Generate context for integration testing"""
        
        integration_context = self._generate_basic_context(workflow_def)
        integration_context.update({
            "use_real_data": True,
            "client_id": "WM000001",  # Use actual test data
            "validate_external_apis": True,
            "check_data_consistency": True
        })
        
        return integration_context
    
    def _create_pattern_specific_test(self, workflow_def) -> Optional[TestCase]:
        """Create pattern-specific test cases"""
        
        if workflow_def.pattern == ADKPattern.EVENT_DRIVEN:
            return TestCase(
                test_id=f"{workflow_def.workflow_id}_EVENT_RESPONSE",
                workflow_id=workflow_def.workflow_id,
                test_name=f"{workflow_def.name} - Event Response Time",
                description="Test event-driven pattern response characteristics",
                input_context={
                    **self._generate_basic_context(workflow_def),
                    "event_type": "market_volatility",
                    "severity": "high",
                    "measure_response_time": True
                },
                expected_outcomes={
                    "response_time_max": 2.0,
                    "event_processed": True,
                    "appropriate_actions": True
                },
                test_category="pattern_specific",
                priority="high"
            )
        
        elif workflow_def.pattern == ADKPattern.SCHEDULED:
            return TestCase(
                test_id=f"{workflow_def.workflow_id}_SCHEDULE",
                workflow_id=workflow_def.workflow_id, 
                test_name=f"{workflow_def.name} - Schedule Execution",
                description="Test scheduled pattern timing and reliability",
                input_context={
                    **self._generate_basic_context(workflow_def),
                    "schedule_type": "hourly",
                    "recurring": True,
                    "validate_timing": True
                },
                expected_outcomes={
                    "executes_on_schedule": True,
                    "timing_accuracy": 0.95,
                    "handles_missed_runs": True
                },
                test_category="pattern_specific",
                priority="medium"
            )
        
        elif workflow_def.pattern == ADKPattern.PARALLEL:
            return TestCase(
                test_id=f"{workflow_def.workflow_id}_CONCURRENCY",
                workflow_id=workflow_def.workflow_id,
                test_name=f"{workflow_def.name} - Concurrency",
                description="Test parallel execution and resource management",
                input_context={
                    **self._generate_basic_context(workflow_def),
                    "max_concurrent_tasks": 10,
                    "validate_concurrency": True
                },
                expected_outcomes={
                    "concurrent_execution": True,
                    "no_race_conditions": True,
                    "proper_resource_sharing": True
                },
                test_category="pattern_specific",
                priority="high"
            )
        
        return None
    
    def _get_performance_threshold(self, workflow_def) -> float:
        """Get performance threshold based on workflow complexity"""
        
        complexity_thresholds = {
            "Simple": 5.0,
            "Moderate": 15.0, 
            "Complex": 30.0
        }
        
        return complexity_thresholds.get(workflow_def.complexity, 15.0)
    
    def _requires_integration_testing(self, workflow_def) -> bool:
        """Determine if workflow requires integration testing"""
        
        integration_indicators = [
            "portfolio", "market", "client", "account", 
            "compliance", "regulatory", "kyc"
        ]
        
        description_lower = workflow_def.description.lower()
        return any(indicator in description_lower for indicator in integration_indicators)
    
    async def run_test_suite(self, test_categories: List[str] = None, 
                           priority_filter: List[str] = None) -> Dict[str, Any]:
        """Run comprehensive test suite"""
        
        logger.info("Starting comprehensive workflow test suite")
        start_time = datetime.now()
        
        # Filter test cases
        filtered_tests = self._filter_test_cases(test_categories, priority_filter)
        
        logger.info(f"Running {len(filtered_tests)} test cases")
        
        # Execute tests
        test_results = []
        for test_case in filtered_tests:
            result = await self._execute_test_case(test_case)
            test_results.append(result)
            self.test_results.append(result)
        
        end_time = datetime.now()
        
        # Generate test report
        report = self._generate_test_report(test_results, start_time, end_time)
        
        logger.info(f"Test suite completed. {report['summary']['passed']}/{report['summary']['total']} tests passed")
        
        return report
    
    def _filter_test_cases(self, categories: List[str] = None, 
                          priorities: List[str] = None) -> List[TestCase]:
        """Filter test cases based on criteria"""
        
        filtered = list(self.test_cases.values())
        
        if categories:
            filtered = [t for t in filtered if t.test_category in categories]
        
        if priorities:
            filtered = [t for t in filtered if t.priority in priorities]
        
        return filtered
    
    async def _execute_test_case(self, test_case: TestCase) -> TestResult:
        """Execute a single test case"""
        
        logger.debug(f"Executing test case: {test_case.test_id}")
        
        start_time = datetime.now()
        execution = None
        error_message = None
        passed = False
        
        try:
            # Execute workflow
            execution = await asyncio.wait_for(
                self.executor.execute_workflow(
                    test_case.workflow_id,
                    test_case.input_context
                ),
                timeout=test_case.timeout_seconds
            )
            
            # Evaluate test results
            passed, error_message = self._evaluate_test_results(test_case, execution)
            
        except asyncio.TimeoutError:
            error_message = f"Test timed out after {test_case.timeout_seconds} seconds"
        except Exception as e:
            error_message = f"Test execution failed: {str(e)}"
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        # Calculate performance metrics
        performance_metrics = self._calculate_performance_metrics(execution, execution_time)
        
        return TestResult(
            test_case=test_case,
            execution=execution,
            passed=passed,
            error_message=error_message,
            execution_time=execution_time,
            performance_metrics=performance_metrics,
            timestamp=end_time
        )
    
    def _evaluate_test_results(self, test_case: TestCase, 
                              execution: WorkflowExecution) -> Tuple[bool, Optional[str]]:
        """Evaluate if test case passed based on execution results"""
        
        try:
            expected = test_case.expected_outcomes
            
            # Check basic status
            if "status" in expected:
                if execution.status.value != expected["status"]:
                    return False, f"Expected status {expected['status']}, got {execution.status.value}"
            
            # Check steps completed
            if "steps_completed" in expected:
                actual_steps = len(execution.step_results)
                if actual_steps != expected["steps_completed"]:
                    return False, f"Expected {expected['steps_completed']} steps, completed {actual_steps}"
            
            # Check execution time
            if "execution_time_max" in expected and execution.started_at and execution.completed_at:
                actual_time = (execution.completed_at - execution.started_at).total_seconds()
                if actual_time > expected["execution_time_max"]:
                    return False, f"Execution took {actual_time}s, max allowed {expected['execution_time_max']}s"
            
            # Pattern-specific validations
            if execution.workflow_def.pattern == ADKPattern.EVENT_DRIVEN:
                if "response_time_max" in expected:
                    response_time = execution.results.get("response_time", float('inf'))
                    if response_time > expected["response_time_max"]:
                        return False, f"Response time {response_time}s exceeded max {expected['response_time_max']}s"
            
            if execution.workflow_def.pattern == ADKPattern.PARALLEL:
                if "concurrent_execution" in expected and expected["concurrent_execution"]:
                    if not execution.results.get("parallel_tasks"):
                        return False, "Parallel execution not detected"
            
            # Check for successful completion
            if execution.status == WorkflowStatus.COMPLETED:
                return True, None
            else:
                return False, f"Workflow failed to complete: {execution.error_message}"
                
        except Exception as e:
            return False, f"Test evaluation failed: {str(e)}"
    
    def _calculate_performance_metrics(self, execution: Optional[WorkflowExecution], 
                                     execution_time: float) -> Dict[str, Any]:
        """Calculate performance metrics for test result"""
        
        metrics = {
            "execution_time": execution_time,
            "timeout_occurred": False,
            "steps_per_second": 0,
            "pattern_efficiency": "unknown"
        }
        
        if execution and execution.step_results:
            metrics["steps_per_second"] = len(execution.step_results) / max(execution_time, 0.001)
            
            # Pattern-specific metrics
            if execution.workflow_def.pattern == ADKPattern.PARALLEL:
                parallel_tasks = execution.results.get("parallel_tasks", [])
                metrics["parallel_efficiency"] = len(parallel_tasks) / max(execution_time, 0.001)
                
            elif execution.workflow_def.pattern == ADKPattern.EVENT_DRIVEN:
                metrics["response_time"] = execution.results.get("response_time", execution_time)
                
            elif execution.workflow_def.pattern == ADKPattern.LOOP:
                iterations = execution.results.get("iterations", 0)
                metrics["iterations_completed"] = iterations
                metrics["iteration_rate"] = iterations / max(execution_time, 0.001)
        
        return metrics
    
    def _generate_test_report(self, test_results: List[TestResult], 
                            start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        
        total_tests = len(test_results)
        passed_tests = len([r for r in test_results if r.passed])
        failed_tests = total_tests - passed_tests
        
        # Categorize results
        category_stats = {}
        pattern_stats = {}
        priority_stats = {}
        
        for result in test_results:
            # By category
            category = result.test_case.test_category
            if category not in category_stats:
                category_stats[category] = {"total": 0, "passed": 0}
            category_stats[category]["total"] += 1
            if result.passed:
                category_stats[category]["passed"] += 1
            
            # By ADK pattern
            if result.execution:
                pattern = result.execution.workflow_def.pattern.value
                if pattern not in pattern_stats:
                    pattern_stats[pattern] = {"total": 0, "passed": 0}
                pattern_stats[pattern]["total"] += 1
                if result.passed:
                    pattern_stats[pattern]["passed"] += 1
            
            # By priority
            priority = result.test_case.priority
            if priority not in priority_stats:
                priority_stats[priority] = {"total": 0, "passed": 0}
            priority_stats[priority]["total"] += 1
            if result.passed:
                priority_stats[priority]["passed"] += 1
        
        # Performance analysis
        execution_times = [r.execution_time for r in test_results]
        avg_execution_time = sum(execution_times) / max(len(execution_times), 1)
        max_execution_time = max(execution_times) if execution_times else 0
        
        # Failed tests details
        failed_test_details = [
            {
                "test_id": r.test_case.test_id,
                "test_name": r.test_case.test_name,
                "error_message": r.error_message,
                "execution_time": r.execution_time
            }
            for r in test_results if not r.passed
        ]
        
        return {
            "summary": {
                "total": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": passed_tests / max(total_tests, 1),
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "total_duration": (end_time - start_time).total_seconds()
            },
            "category_breakdown": category_stats,
            "pattern_breakdown": pattern_stats,
            "priority_breakdown": priority_stats,
            "performance": {
                "average_execution_time": avg_execution_time,
                "max_execution_time": max_execution_time,
                "total_execution_time": sum(execution_times)
            },
            "failed_tests": failed_test_details,
            "detailed_results": [r.to_dict() for r in test_results]
        }
    
    async def run_smoke_tests(self) -> Dict[str, Any]:
        """Run basic smoke tests for all workflows"""
        
        logger.info("Running smoke tests for all workflows")
        
        basic_tests = [t for t in self.test_cases.values() 
                      if t.test_category == "functionality" and t.priority == "high"]
        
        return await self.run_test_suite(test_categories=["functionality"], priority_filter=["high"])
    
    async def run_performance_tests(self) -> Dict[str, Any]:
        """Run performance-focused tests"""
        
        logger.info("Running performance tests")
        
        return await self.run_test_suite(test_categories=["performance"])
    
    async def run_pattern_tests(self, pattern: ADKPattern) -> Dict[str, Any]:
        """Run tests for specific ADK pattern"""
        
        logger.info(f"Running tests for {pattern.value} pattern")
        
        pattern_workflows = self.registry.get_workflows_by_pattern(pattern)
        pattern_test_ids = []
        
        for workflow in pattern_workflows:
            pattern_test_ids.extend([
                t.test_id for t in self.test_cases.values() 
                if t.workflow_id == workflow.workflow_id
            ])
        
        filtered_tests = [t for t in self.test_cases.values() 
                         if t.test_id in pattern_test_ids]
        
        test_results = []
        for test_case in filtered_tests:
            result = await self._execute_test_case(test_case)
            test_results.append(result)
        
        return self._generate_test_report(test_results, datetime.now(), datetime.now())
    
    def get_test_coverage(self) -> Dict[str, Any]:
        """Get test coverage statistics"""
        
        total_workflows = len(self.registry.get_all_workflows())
        workflows_with_tests = len(set(t.workflow_id for t in self.test_cases.values()))
        
        coverage_by_category = {}
        for category in WorkflowCategory:
            category_workflows = self.registry.get_workflows_by_category(category)
            category_tested = len([w for w in category_workflows 
                                 if any(t.workflow_id == w.workflow_id for t in self.test_cases.values())])
            coverage_by_category[category.value] = {
                "total": len(category_workflows),
                "tested": category_tested,
                "coverage": category_tested / max(len(category_workflows), 1)
            }
        
        return {
            "overall_coverage": workflows_with_tests / max(total_workflows, 1),
            "workflows_total": total_workflows,
            "workflows_tested": workflows_with_tests,
            "coverage_by_category": coverage_by_category,
            "total_test_cases": len(self.test_cases),
            "test_categories": list(set(t.test_category for t in self.test_cases.values()))
        }

# Usage example and convenience functions
async def run_comprehensive_tests(registry: WorkflowRegistry, executor: WorkflowExecutor) -> Dict[str, Any]:
    """Run comprehensive test suite on all workflows"""
    
    test_framework = WorkflowTestFramework(registry, executor)
    
    logger.info("Starting comprehensive workflow testing")
    
    # Run all test categories
    full_results = await test_framework.run_test_suite()
    
    # Additional analysis
    coverage = test_framework.get_test_coverage()
    full_results["test_coverage"] = coverage
    
    return full_results

async def run_regression_tests(registry: WorkflowRegistry, executor: WorkflowExecutor) -> Dict[str, Any]:
    """Run regression tests focusing on critical functionality"""
    
    test_framework = WorkflowTestFramework(registry, executor)
    
    # Focus on high-priority functionality and error handling tests
    return await test_framework.run_test_suite(
        test_categories=["functionality", "error_handling"],
        priority_filter=["high"]
    )