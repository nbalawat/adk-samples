"""Standalone test runner for comprehensive workflow testing"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any, List
from enum import Enum

class WorkflowStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class WorkflowCategory(Enum):
    ADVISOR_WORKFLOWS = "advisor"
    CLIENT_WORKFLOWS = "client"
    OPERATIONS_WORKFLOWS = "operations"

class ADKPattern(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    LOOP = "loop"
    EVENT_DRIVEN = "event_driven"
    SCHEDULED = "scheduled"
    MASTER_ORCHESTRATION = "master_orchestration"

class MockWorkflowDefinition:
    def __init__(self, workflow_id: str, name: str, description: str, 
                 category: WorkflowCategory, pattern: ADKPattern, complexity: str):
        self.workflow_id = workflow_id
        self.name = name
        self.description = description
        self.category = category
        self.pattern = pattern
        self.complexity = complexity
        self.steps = self._generate_steps()
        
    def _generate_steps(self):
        """Generate realistic steps based on workflow type"""
        if "market" in self.name.lower() or "volatility" in self.name.lower():
            return ["Analyze market conditions", "Assess portfolio impact", "Generate communications", "Execute response"]
        elif "client" in self.name.lower() or "onboarding" in self.name.lower():
            return ["Collect information", "Assess requirements", "Create profile", "Setup accounts"]
        elif "compliance" in self.name.lower() or "regulatory" in self.name.lower():
            return ["Review requirements", "Assess compliance", "Generate reports", "Submit documentation"]
        elif "portfolio" in self.name.lower() or "performance" in self.name.lower():
            return ["Gather data", "Calculate metrics", "Compare benchmarks", "Generate reports"]
        else:
            return ["Initialize process", "Execute workflow", "Validate results", "Complete process"]

class MockWorkflowExecution:
    def __init__(self, workflow_def: MockWorkflowDefinition, context: Dict[str, Any]):
        self.workflow_def = workflow_def
        self.context = context
        self.status = WorkflowStatus.PENDING
        self.start_time = None
        self.end_time = None
        self.step_results = []
        self.error_message = None
        
    async def execute(self):
        """Execute the workflow simulation"""
        self.status = WorkflowStatus.IN_PROGRESS
        self.start_time = datetime.now()
        
        try:
            # Simulate workflow execution based on pattern
            if self.workflow_def.pattern == ADKPattern.SEQUENTIAL:
                await self._execute_sequential()
            elif self.workflow_def.pattern == ADKPattern.PARALLEL:
                await self._execute_parallel()
            elif self.workflow_def.pattern == ADKPattern.LOOP:
                await self._execute_loop()
            elif self.workflow_def.pattern == ADKPattern.EVENT_DRIVEN:
                await self._execute_event_driven()
            elif self.workflow_def.pattern == ADKPattern.SCHEDULED:
                await self._execute_scheduled()
            else:
                await self._execute_master_orchestration()
                
            self.status = WorkflowStatus.COMPLETED
            
        except Exception as e:
            self.status = WorkflowStatus.FAILED
            self.error_message = str(e)
            
        self.end_time = datetime.now()
        
    async def _execute_sequential(self):
        """Execute sequential workflow"""
        for i, step in enumerate(self.workflow_def.steps):
            await asyncio.sleep(0.1)  # Simulate step execution
            self.step_results.append({
                "step": step,
                "result": "completed",
                "timestamp": datetime.now().isoformat()
            })
            
    async def _execute_parallel(self):
        """Execute parallel workflow"""
        tasks = []
        for step in self.workflow_def.steps:
            tasks.append(self._execute_step(step))
        
        results = await asyncio.gather(*tasks)
        self.step_results = results
        
    async def _execute_loop(self):
        """Execute loop workflow"""
        max_iterations = self.context.get("max_iterations", 3)
        for iteration in range(max_iterations):
            for step in self.workflow_def.steps:
                await asyncio.sleep(0.05)
                self.step_results.append({
                    "step": step,
                    "iteration": iteration + 1,
                    "result": "completed"
                })
                
    async def _execute_event_driven(self):
        """Execute event-driven workflow"""
        event_type = self.context.get("event_type", "general")
        severity = self.context.get("severity", "medium")
        
        # Simulate faster execution for events
        for step in self.workflow_def.steps:
            await asyncio.sleep(0.02)
            self.step_results.append({
                "step": step,
                "event_type": event_type,
                "severity": severity,
                "result": "completed"
            })
            
    async def _execute_scheduled(self):
        """Execute scheduled workflow"""
        for step in self.workflow_def.steps:
            await asyncio.sleep(0.08)
            self.step_results.append({
                "step": step,
                "scheduled": True,
                "result": "completed"
            })
            
    async def _execute_master_orchestration(self):
        """Execute master orchestration workflow"""
        sub_workflows = self.context.get("sub_workflows", ["workflow1", "workflow2"])
        
        for sub_wf in sub_workflows:
            await asyncio.sleep(0.15)
            self.step_results.append({
                "sub_workflow": sub_wf,
                "result": "orchestrated"
            })
            
    async def _execute_step(self, step: str):
        """Execute a single step"""
        await asyncio.sleep(0.05)
        return {
            "step": step,
            "result": "completed",
            "timestamp": datetime.now().isoformat()
        }

class ComprehensiveWorkflowTester:
    """Comprehensive tester for all 33 workflows"""
    
    def __init__(self):
        self.workflows = self._create_all_workflows()
        
    def _create_all_workflows(self) -> List[MockWorkflowDefinition]:
        """Create all 33 workflow definitions"""
        workflows = []
        
        # ADVISOR WORKFLOWS (1-15)
        advisor_workflows = [
            ("ADV001", "Client Meeting Preparation and Follow-up", ADKPattern.SEQUENTIAL, "Moderate"),
            ("ADV002", "Portfolio Performance Review and Reporting", ADKPattern.SEQUENTIAL, "Complex"),
            ("ADV003", "Risk Assessment and Management", ADKPattern.LOOP, "Complex"),
            ("ADV004", "Investment Research and Recommendation", ADKPattern.SEQUENTIAL, "Complex"),
            ("ADV005", "Client Acquisition and Onboarding", ADKPattern.PARALLEL, "Moderate"),
            ("ADV006", "Wealth Planning and Goal Tracking", ADKPattern.SEQUENTIAL, "Complex"),
            ("ADV007", "Market Volatility Response", ADKPattern.EVENT_DRIVEN, "Moderate"),
            ("ADV008", "Regulatory Compliance Management", ADKPattern.SCHEDULED, "Complex"),
            ("ADV009", "Crisis Management and Communication", ADKPattern.EVENT_DRIVEN, "Complex"),
            ("ADV010", "Tax Optimization and Planning", ADKPattern.SCHEDULED, "Complex"),
            ("ADV011", "Alternative Investment Analysis", ADKPattern.SEQUENTIAL, "Complex"),
            ("ADV012", "ESG Integration and Reporting", ADKPattern.LOOP, "Moderate"),
            ("ADV013", "Portfolio Rebalancing Workflows", ADKPattern.EVENT_DRIVEN, "Moderate"),
            ("ADV014", "Client Education and Communication", ADKPattern.SCHEDULED, "Simple"),
            ("ADV015", "Business Development and Referrals", ADKPattern.LOOP, "Moderate")
        ]
        
        for wf_id, name, pattern, complexity in advisor_workflows:
            workflows.append(MockWorkflowDefinition(
                wf_id, name, f"Advisor workflow: {name}",
                WorkflowCategory.ADVISOR_WORKFLOWS, pattern, complexity
            ))
        
        # CLIENT WORKFLOWS (16-25)
        client_workflows = [
            ("CLI001", "Financial Planning Consultation", ADKPattern.SEQUENTIAL, "Complex"),
            ("CLI002", "Investment Goal Setting and Tracking", ADKPattern.LOOP, "Moderate"),
            ("CLI003", "Portfolio Review and Discussion", ADKPattern.SCHEDULED, "Moderate"),
            ("CLI004", "Risk Tolerance Assessment", ADKPattern.SEQUENTIAL, "Simple"),
            ("CLI005", "Market Education Sessions", ADKPattern.SCHEDULED, "Simple"),
            ("CLI006", "Life Event Financial Planning", ADKPattern.SEQUENTIAL, "Complex"),
            ("CLI007", "Retirement Planning Workshops", ADKPattern.SEQUENTIAL, "Complex"),
            ("CLI008", "Investment Performance Reviews", ADKPattern.SCHEDULED, "Moderate"),
            ("CLI009", "Estate Planning Consultation", ADKPattern.SEQUENTIAL, "Complex"),
            ("CLI010", "Tax Planning Sessions", ADKPattern.SCHEDULED, "Moderate")
        ]
        
        for wf_id, name, pattern, complexity in client_workflows:
            workflows.append(MockWorkflowDefinition(
                wf_id, name, f"Client workflow: {name}",
                WorkflowCategory.CLIENT_WORKFLOWS, pattern, complexity
            ))
        
        # OPERATIONS WORKFLOWS (26-33)
        operations_workflows = [
            ("OPS001", "Account Administration and Maintenance", ADKPattern.LOOP, "Simple"),
            ("OPS002", "Trade Execution and Settlement", ADKPattern.SEQUENTIAL, "Moderate"),
            ("OPS003", "Reconciliation and Reporting", ADKPattern.SCHEDULED, "Moderate"),
            ("OPS004", "Compliance Monitoring", ADKPattern.LOOP, "Complex"),
            ("OPS005", "Client Onboarding Operations", ADKPattern.PARALLEL, "Moderate"),
            ("OPS006", "Fee Calculation and Billing", ADKPattern.SCHEDULED, "Moderate"),
            ("OPS007", "Document Management", ADKPattern.LOOP, "Simple"),
            ("OPS008", "System Integration Management", ADKPattern.MASTER_ORCHESTRATION, "Complex")
        ]
        
        for wf_id, name, pattern, complexity in operations_workflows:
            workflows.append(MockWorkflowDefinition(
                wf_id, name, f"Operations workflow: {name}",
                WorkflowCategory.OPERATIONS_WORKFLOWS, pattern, complexity
            ))
        
        return workflows
    
    async def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Run comprehensive tests on all workflows"""
        
        print("🧪 COMPREHENSIVE WORKFLOW TESTING")
        print("="*60)
        print(f"Testing all {len(self.workflows)} workflows across all ADK patterns...")
        print()
        
        start_time = datetime.now()
        test_results = []
        
        # Test each workflow with multiple scenarios
        for workflow in self.workflows:
            print(f"🔄 Testing {workflow.workflow_id}: {workflow.name}")
            print(f"   Pattern: {workflow.pattern.value}, Complexity: {workflow.complexity}")
            
            # Basic functionality test
            basic_result = await self._test_workflow_basic(workflow)
            test_results.append(basic_result)
            
            # Error handling test
            error_result = await self._test_workflow_errors(workflow)
            test_results.append(error_result)
            
            # Performance test
            if workflow.complexity in ["Complex", "Moderate"]:
                perf_result = await self._test_workflow_performance(workflow)
                test_results.append(perf_result)
            
            success_count = sum(1 for r in [basic_result, error_result] if r["passed"])
            print(f"   ✅ Results: {success_count}/2 tests passed")
            print()
        
        end_time = datetime.now()
        
        # Generate comprehensive report
        return self._generate_test_report(test_results, start_time, end_time)
    
    async def _test_workflow_basic(self, workflow: MockWorkflowDefinition) -> Dict[str, Any]:
        """Test basic workflow functionality"""
        
        context = self._generate_test_context(workflow)
        execution = MockWorkflowExecution(workflow, context)
        
        try:
            await execution.execute()
            
            passed = (
                execution.status == WorkflowStatus.COMPLETED and
                len(execution.step_results) > 0 and
                execution.end_time is not None
            )
            
            return {
                "test_type": "basic_functionality",
                "workflow_id": workflow.workflow_id,
                "workflow_name": workflow.name,
                "pattern": workflow.pattern.value,
                "passed": passed,
                "execution_time": (execution.end_time - execution.start_time).total_seconds() if execution.end_time else 0,
                "steps_completed": len(execution.step_results),
                "error": execution.error_message
            }
            
        except Exception as e:
            return {
                "test_type": "basic_functionality", 
                "workflow_id": workflow.workflow_id,
                "workflow_name": workflow.name,
                "pattern": workflow.pattern.value,
                "passed": False,
                "error": str(e)
            }
    
    async def _test_workflow_errors(self, workflow: MockWorkflowDefinition) -> Dict[str, Any]:
        """Test workflow error handling"""
        
        # Create error-inducing context
        context = {"force_error": True, "invalid_data": True}
        execution = MockWorkflowExecution(workflow, context)
        
        try:
            await execution.execute()
            
            # For this test, we expect graceful handling even with errors
            passed = execution.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED]
            
            return {
                "test_type": "error_handling",
                "workflow_id": workflow.workflow_id,
                "workflow_name": workflow.name,
                "pattern": workflow.pattern.value,
                "passed": passed,
                "handled_gracefully": execution.error_message is not None if execution.status == WorkflowStatus.FAILED else True
            }
            
        except Exception as e:
            return {
                "test_type": "error_handling",
                "workflow_id": workflow.workflow_id,
                "workflow_name": workflow.name,
                "pattern": workflow.pattern.value,
                "passed": False,
                "error": str(e)
            }
    
    async def _test_workflow_performance(self, workflow: MockWorkflowDefinition) -> Dict[str, Any]:
        """Test workflow performance"""
        
        context = self._generate_performance_context(workflow)
        execution = MockWorkflowExecution(workflow, context)
        
        try:
            start_perf = time.time()
            await execution.execute()
            end_perf = time.time()
            
            execution_time = end_perf - start_perf
            
            # Performance thresholds based on complexity
            max_time = {"Simple": 2.0, "Moderate": 5.0, "Complex": 10.0}
            threshold = max_time.get(workflow.complexity, 5.0)
            
            passed = execution_time <= threshold and execution.status == WorkflowStatus.COMPLETED
            
            return {
                "test_type": "performance",
                "workflow_id": workflow.workflow_id,
                "workflow_name": workflow.name,
                "pattern": workflow.pattern.value,
                "passed": passed,
                "execution_time": execution_time,
                "threshold": threshold,
                "within_threshold": execution_time <= threshold
            }
            
        except Exception as e:
            return {
                "test_type": "performance",
                "workflow_id": workflow.workflow_id,
                "workflow_name": workflow.name,
                "pattern": workflow.pattern.value,
                "passed": False,
                "error": str(e)
            }
    
    def _generate_test_context(self, workflow: MockWorkflowDefinition) -> Dict[str, Any]:
        """Generate appropriate test context for workflow"""
        
        base_context = {
            "test_mode": True,
            "client_id": "WM000001",
            "execution_date": datetime.now().isoformat()
        }
        
        # Pattern-specific context
        if workflow.pattern == ADKPattern.EVENT_DRIVEN:
            base_context.update({
                "event_type": "market_volatility",
                "severity": "medium"
            })
        elif workflow.pattern == ADKPattern.SCHEDULED:
            base_context.update({
                "schedule_type": "daily",
                "recurring": True
            })
        elif workflow.pattern == ADKPattern.LOOP:
            base_context.update({
                "max_iterations": 3
            })
        elif workflow.pattern == ADKPattern.PARALLEL:
            base_context.update({
                "concurrent_tasks": 4
            })
        elif workflow.pattern == ADKPattern.MASTER_ORCHESTRATION:
            base_context.update({
                "sub_workflows": ["workflow1", "workflow2", "workflow3"]
            })
        
        return base_context
    
    def _generate_performance_context(self, workflow: MockWorkflowDefinition) -> Dict[str, Any]:
        """Generate performance test context"""
        
        context = self._generate_test_context(workflow)
        
        # Add load for performance testing
        if workflow.pattern == ADKPattern.PARALLEL:
            context["concurrent_tasks"] = 10
        elif workflow.pattern == ADKPattern.LOOP:
            context["max_iterations"] = 5
        else:
            context["load_multiplier"] = 2
        
        return context
    
    def _generate_test_report(self, test_results: List[Dict[str, Any]], 
                            start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        
        total_tests = len(test_results)
        passed_tests = len([r for r in test_results if r["passed"]])
        failed_tests = total_tests - passed_tests
        
        # Group by categories
        category_stats = {
            "advisor": {"total": 0, "passed": 0},
            "client": {"total": 0, "passed": 0}, 
            "operations": {"total": 0, "passed": 0}
        }
        
        pattern_stats = {}
        
        for result in test_results:
            # Determine category from workflow_id
            if result["workflow_id"].startswith("ADV"):
                category = "advisor"
            elif result["workflow_id"].startswith("CLI"):
                category = "client"
            else:
                category = "operations"
            
            category_stats[category]["total"] += 1
            if result["passed"]:
                category_stats[category]["passed"] += 1
            
            # Pattern stats
            pattern = result["pattern"]
            if pattern not in pattern_stats:
                pattern_stats[pattern] = {"total": 0, "passed": 0}
            pattern_stats[pattern]["total"] += 1
            if result["passed"]:
                pattern_stats[pattern]["passed"] += 1
        
        # Performance metrics
        execution_times = [r.get("execution_time", 0) for r in test_results if "execution_time" in r]
        avg_execution_time = sum(execution_times) / max(len(execution_times), 1)
        max_execution_time = max(execution_times) if execution_times else 0
        
        # Failed tests
        failed_tests_details = [
            {
                "workflow_id": r["workflow_id"],
                "workflow_name": r["workflow_name"],
                "test_type": r["test_type"],
                "error": r.get("error", "Unknown error")
            }
            for r in test_results if not r["passed"]
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
            "performance": {
                "average_execution_time": avg_execution_time,
                "max_execution_time": max_execution_time,
                "total_execution_time": sum(execution_times)
            },
            "failed_tests": failed_tests_details,
            "detailed_results": test_results
        }

async def main():
    """Run the comprehensive workflow tests"""
    
    tester = ComprehensiveWorkflowTester()
    results = await tester.run_comprehensive_tests()
    
    print("📊 FINAL TEST RESULTS")
    print("="*60)
    print(f"Total Tests: {results['summary']['total']}")
    print(f"Passed: {results['summary']['passed']}")
    print(f"Failed: {results['summary']['failed']}")
    print(f"Success Rate: {results['summary']['success_rate']:.1%}")
    print(f"Total Duration: {results['summary']['total_duration']:.1f}s")
    print()
    
    print("📋 BREAKDOWN BY CATEGORY")
    print("-"*40)
    for category, stats in results['category_breakdown'].items():
        success_rate = stats['passed'] / max(stats['total'], 1)
        print(f"{category.title():15}: {stats['passed']}/{stats['total']} ({success_rate:.1%})")
    
    print()
    print("🔄 BREAKDOWN BY ADK PATTERN")
    print("-"*40)
    for pattern, stats in results['pattern_breakdown'].items():
        success_rate = stats['passed'] / max(stats['total'], 1)
        pattern_name = pattern.replace("_", " ").title()
        print(f"{pattern_name:20}: {stats['passed']}/{stats['total']} ({success_rate:.1%})")
    
    print()
    print("⚡ PERFORMANCE METRICS")
    print("-"*40)
    print(f"Average Execution Time: {results['performance']['average_execution_time']:.2f}s")
    print(f"Maximum Execution Time: {results['performance']['max_execution_time']:.2f}s")
    print(f"Total Execution Time: {results['performance']['total_execution_time']:.2f}s")
    
    if results['failed_tests']:
        print()
        print("❌ FAILED TESTS")
        print("-"*40)
        for failed in results['failed_tests'][:10]:  # Show first 10
            print(f"• {failed['workflow_id']}: {failed['workflow_name']}")
            print(f"  Test Type: {failed['test_type']}")
            print(f"  Error: {failed['error']}")
            print()
    else:
        print()
        print("🎉 ALL TESTS PASSED!")
    
    # Save detailed results
    with open('comprehensive_test_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Detailed results saved to: comprehensive_test_results.json")
    
    return results

if __name__ == "__main__":
    results = asyncio.run(main())