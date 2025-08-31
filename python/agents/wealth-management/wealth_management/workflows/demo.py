"""Demonstration of all 33 wealth management workflows"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any

from .workflow_registry import workflow_registry, ADKPattern, WorkflowCategory
from .workflow_executor import WorkflowExecutor
from .test_framework import WorkflowTestFramework

async def demo_all_workflows():
    """Demonstrate all 33 workflows with sample executions"""
    
    print("🎯 Wealth Management Workflow System Demo")
    print("=" * 50)
    
    # Initialize components
    executor = WorkflowExecutor(workflow_registry)
    test_framework = WorkflowTestFramework(workflow_registry, executor)
    
    # Show registry statistics
    stats = workflow_registry.get_registry_stats()
    print(f"\n📊 Workflow Registry Statistics:")
    print(f"   Total Workflows: {stats['total_workflows']}")
    print(f"   By Category: {stats['by_category']}")
    print(f"   By Pattern: {stats['by_pattern']}")
    print(f"   By Complexity: {stats['by_complexity']}")
    
    print("\n" + "="*50)
    print("🚀 Executing Sample Workflows by Category")
    print("="*50)
    
    # Demo workflows by category
    await demo_advisor_workflows(executor)
    await demo_client_workflows(executor)
    await demo_operations_workflows(executor)
    
    print("\n" + "="*50)
    print("🧪 Running Comprehensive Tests")
    print("="*50)
    
    # Run smoke tests
    smoke_results = await test_framework.run_smoke_tests()
    print(f"\n✅ Smoke Tests Results:")
    print(f"   Passed: {smoke_results['summary']['passed']}/{smoke_results['summary']['total']}")
    print(f"   Success Rate: {smoke_results['summary']['success_rate']:.1%}")
    
    # Show pattern-specific results
    print(f"\n🔄 ADK Pattern Performance:")
    for pattern, stats in smoke_results['pattern_breakdown'].items():
        success_rate = stats['passed'] / max(stats['total'], 1)
        print(f"   {pattern.replace('_', ' ').title()}: {stats['passed']}/{stats['total']} ({success_rate:.1%})")
    
    print("\n" + "="*50)
    print("📈 Performance Analytics")
    print("="*50)
    
    perf = smoke_results['performance']
    print(f"   Average Execution Time: {perf['average_execution_time']:.2f}s")
    print(f"   Maximum Execution Time: {perf['max_execution_time']:.2f}s")
    print(f"   Total Test Duration: {perf['total_execution_time']:.2f}s")
    
    # Show failed tests if any
    if smoke_results['failed_tests']:
        print(f"\n❌ Failed Tests ({len(smoke_results['failed_tests'])}):")
        for failed in smoke_results['failed_tests'][:5]:  # Show first 5
            print(f"   • {failed['test_name']}: {failed['error_message']}")
    
    print(f"\n🎉 Demo Complete! All {stats['total_workflows']} workflows demonstrated.")
    
    return {
        "total_workflows": stats['total_workflows'],
        "test_results": smoke_results,
        "execution_summary": executor.get_executor_stats()
    }

async def demo_advisor_workflows(executor: WorkflowExecutor):
    """Demonstrate key advisor workflows"""
    
    print("\n👨‍💼 ADVISOR WORKFLOWS")
    print("-" * 30)
    
    advisor_workflows = [
        ("ADV001", {"client_id": "WM123456", "meeting_type": "quarterly_review"}),
        ("ADV002", {"client_id": "WM123456", "period": "Q3_2024"}),
        ("ADV007", {"event_type": "market_volatility", "severity": "high"}),
        ("ADV009", {"event_type": "market_crash", "severity": "extreme"})
    ]
    
    for workflow_id, context in advisor_workflows:
        workflow_def = workflow_registry.get_workflow(workflow_id)
        if workflow_def:
            print(f"\n🔄 Executing: {workflow_def.name}")
            print(f"   Pattern: {workflow_def.pattern.value}")
            print(f"   Complexity: {workflow_def.complexity}")
            
            try:
                execution = await executor.execute_workflow(workflow_id, context)
                print(f"   ✅ Status: {execution.status.value}")
                print(f"   ⏱️ Duration: {execution.execution_time if hasattr(execution, 'execution_time') else 'N/A'}")
                print(f"   📋 Steps: {len(execution.step_results)}/{len(execution.workflow_def.steps)}")
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")

async def demo_client_workflows(executor: WorkflowExecutor):
    """Demonstrate key client workflows"""
    
    print("\n👤 CLIENT WORKFLOWS") 
    print("-" * 30)
    
    client_workflows = [
        ("CLI001", {"client_id": "WM789012", "planning_type": "comprehensive"}),
        ("CLI002", {"client_id": "WM789012", "goal_type": "retirement", "target_amount": 2000000}),
        ("CLI003", {"client_id": "WM789012", "review_type": "quarterly"})
    ]
    
    for workflow_id, context in client_workflows:
        workflow_def = workflow_registry.get_workflow(workflow_id)
        if workflow_def:
            print(f"\n🔄 Executing: {workflow_def.name}")
            print(f"   Pattern: {workflow_def.pattern.value}")
            
            try:
                execution = await executor.execute_workflow(workflow_id, context)
                print(f"   ✅ Status: {execution.status.value}")
                print(f"   📋 Steps: {len(execution.step_results)}")
                
                # Show some results
                if execution.results:
                    if execution.workflow_def.pattern == ADKPattern.SEQUENTIAL:
                        print(f"   🔄 Steps Completed: {len(execution.results.get('steps_completed', []))}")
                    elif execution.workflow_def.pattern == ADKPattern.PARALLEL:
                        print(f"   ⚡ Parallel Tasks: {len(execution.results.get('parallel_tasks', []))}")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")

async def demo_operations_workflows(executor: WorkflowExecutor):
    """Demonstrate key operations workflows"""
    
    print("\n⚙️ OPERATIONS WORKFLOWS")
    print("-" * 30)
    
    operations_workflows = [
        ("OPS001", {"operation_type": "account_update", "batch_size": 25}),
        ("OPS002", {"trade_type": "rebalancing", "account_count": 15})
    ]
    
    for workflow_id, context in operations_workflows:
        workflow_def = workflow_registry.get_workflow(workflow_id)
        if workflow_def:
            print(f"\n🔄 Executing: {workflow_def.name}")
            print(f"   Pattern: {workflow_def.pattern.value}")
            
            try:
                execution = await executor.execute_workflow(workflow_id, context)
                print(f"   ✅ Status: {execution.status.value}")
                print(f"   📋 Steps: {len(execution.step_results)}")
                
                # Show pattern-specific results
                if execution.workflow_def.pattern == ADKPattern.LOOP:
                    iterations = execution.results.get('iterations', 0)
                    print(f"   🔄 Iterations: {iterations}")
                elif execution.workflow_def.pattern == ADKPattern.SCHEDULED:
                    next_run = execution.results.get('next_scheduled_run')
                    if next_run:
                        print(f"   📅 Next Run: {next_run}")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")

async def demo_pattern_showcase():
    """Showcase each ADK pattern with specific examples"""
    
    print("\n🎭 ADK PATTERN SHOWCASE")
    print("-" * 30)
    
    executor = WorkflowExecutor(workflow_registry)
    
    # Sequential Pattern
    print("\n1️⃣ SEQUENTIAL PATTERN")
    sequential_workflow = workflow_registry.get_workflows_by_pattern(ADKPattern.SEQUENTIAL)[0]
    execution = await executor.execute_workflow(
        sequential_workflow.workflow_id, 
        {"client_id": "WM999999", "demo_mode": True}
    )
    print(f"   ✅ {sequential_workflow.name}: {execution.status.value}")
    print(f"   🔄 Sequential Steps: {len(execution.step_results)}")
    
    # Parallel Pattern  
    print("\n2️⃣ PARALLEL PATTERN")
    parallel_workflow = workflow_registry.get_workflows_by_pattern(ADKPattern.PARALLEL)[0]
    execution = await executor.execute_workflow(
        parallel_workflow.workflow_id,
        {"client_id": "WM999999", "concurrent_tasks": 5}
    )
    print(f"   ✅ {parallel_workflow.name}: {execution.status.value}")
    parallel_tasks = execution.results.get('parallel_tasks', [])
    print(f"   ⚡ Parallel Tasks: {len(parallel_tasks)}")
    
    # Event-Driven Pattern
    print("\n3️⃣ EVENT-DRIVEN PATTERN") 
    event_workflow = workflow_registry.get_workflows_by_pattern(ADKPattern.EVENT_DRIVEN)[0]
    execution = await executor.execute_workflow(
        event_workflow.workflow_id,
        {"event_type": "market_volatility", "severity": "high"}
    )
    print(f"   ✅ {event_workflow.name}: {execution.status.value}")
    response_time = execution.results.get('response_time', 0)
    print(f"   ⚡ Response Time: {response_time:.2f}s")
    
    # Loop Pattern
    print("\n4️⃣ LOOP PATTERN")
    loop_workflow = workflow_registry.get_workflows_by_pattern(ADKPattern.LOOP)[0]
    execution = await executor.execute_workflow(
        loop_workflow.workflow_id,
        {"max_iterations": 3, "client_id": "WM999999"}
    )
    print(f"   ✅ {loop_workflow.name}: {execution.status.value}")
    iterations = execution.results.get('iterations', 0)
    print(f"   🔄 Iterations Completed: {iterations}")
    
    # Scheduled Pattern
    print("\n5️⃣ SCHEDULED PATTERN")
    scheduled_workflow = workflow_registry.get_workflows_by_pattern(ADKPattern.SCHEDULED)[0]
    execution = await executor.execute_workflow(
        scheduled_workflow.workflow_id,
        {"schedule_type": "daily", "recurring": True}
    )
    print(f"   ✅ {scheduled_workflow.name}: {execution.status.value}")
    scheduled_tasks = execution.results.get('scheduled_tasks', [])
    print(f"   📅 Scheduled Tasks: {len(scheduled_tasks)}")

def generate_workflow_documentation():
    """Generate documentation for all workflows"""
    
    print("\n📚 WORKFLOW DOCUMENTATION")
    print("=" * 50)
    
    # Group by category
    for category in WorkflowCategory:
        workflows = workflow_registry.get_workflows_by_category(category)
        print(f"\n{category.value.upper()} WORKFLOWS ({len(workflows)})")
        print("-" * 40)
        
        for i, workflow in enumerate(workflows, 1):
            print(f"\n{i}. {workflow.name} ({workflow.workflow_id})")
            print(f"   📝 {workflow.description}")
            print(f"   🔄 Pattern: {workflow.pattern.value}")
            print(f"   ⚡ Complexity: {workflow.complexity}")
            print(f"   👥 Personas: {', '.join(workflow.personas)}")
            print(f"   🎯 Triggers: {', '.join(workflow.triggers[:3])}")  # First 3 triggers
            print(f"   📋 Steps: {len(workflow.steps)} steps")
            print(f"   🛠️ Tools: {len(workflow.tools_required)} tools required")

async def run_performance_benchmarks():
    """Run performance benchmarks across all patterns"""
    
    print("\n⚡ PERFORMANCE BENCHMARKS")
    print("=" * 50)
    
    executor = WorkflowExecutor(workflow_registry)
    test_framework = WorkflowTestFramework(workflow_registry, executor)
    
    # Benchmark each pattern
    pattern_benchmarks = {}
    
    for pattern in ADKPattern:
        print(f"\n🔄 Benchmarking {pattern.value.replace('_', ' ').title()} Pattern...")
        
        try:
            results = await test_framework.run_pattern_tests(pattern)
            
            if results['summary']['total'] > 0:
                pattern_benchmarks[pattern.value] = {
                    "tests_run": results['summary']['total'],
                    "success_rate": results['summary']['success_rate'],
                    "avg_execution_time": results['performance']['average_execution_time'],
                    "max_execution_time": results['performance']['max_execution_time']
                }
                
                print(f"   ✅ Tests: {results['summary']['passed']}/{results['summary']['total']}")
                print(f"   ⏱️ Avg Time: {results['performance']['average_execution_time']:.2f}s")
                print(f"   🎯 Success Rate: {results['summary']['success_rate']:.1%}")
            else:
                print(f"   ⚠️ No tests found for {pattern.value}")
                
        except Exception as e:
            print(f"   ❌ Benchmark failed: {str(e)}")
    
    # Summary
    print(f"\n📊 BENCHMARK SUMMARY")
    print("-" * 30)
    
    if pattern_benchmarks:
        fastest_pattern = min(pattern_benchmarks.items(), 
                            key=lambda x: x[1]['avg_execution_time'])
        most_reliable = max(pattern_benchmarks.items(),
                          key=lambda x: x[1]['success_rate'])
        
        print(f"⚡ Fastest Pattern: {fastest_pattern[0]} ({fastest_pattern[1]['avg_execution_time']:.2f}s)")
        print(f"🎯 Most Reliable: {most_reliable[0]} ({most_reliable[1]['success_rate']:.1%})")
    
    return pattern_benchmarks

# Main demo function
async def main():
    """Run the complete workflow system demonstration"""
    
    print("🎯 COMPREHENSIVE WEALTH MANAGEMENT WORKFLOW SYSTEM")
    print("=" * 60)
    print(f"📅 Demo Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Main demo
    demo_results = await demo_all_workflows()
    
    # Pattern showcase
    await demo_pattern_showcase()
    
    # Generate documentation
    generate_workflow_documentation()
    
    # Performance benchmarks
    benchmark_results = await run_performance_benchmarks()
    
    print(f"\n🎉 DEMO COMPLETE!")
    print(f"   Total Workflows: {demo_results['total_workflows']}")
    print(f"   Test Success Rate: {demo_results['test_results']['summary']['success_rate']:.1%}")
    print(f"   Total Executions: {demo_results['execution_summary']['total_executions']}")
    
    # Save detailed results
    results_summary = {
        "demo_timestamp": datetime.now().isoformat(),
        "workflow_count": demo_results['total_workflows'],
        "test_results": demo_results['test_results'],
        "benchmark_results": benchmark_results,
        "executor_stats": demo_results['execution_summary']
    }
    
    with open('workflow_demo_results.json', 'w') as f:
        json.dump(results_summary, f, indent=2)
    
    print(f"   📄 Detailed results saved to: workflow_demo_results.json")
    
    return results_summary

if __name__ == "__main__":
    # Run the demo
    results = asyncio.run(main())