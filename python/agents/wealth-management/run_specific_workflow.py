#!/usr/bin/env python3
"""
Script to run specific workflows directly
Usage: uv run python run_specific_workflow.py
"""

import asyncio
import json
from wealth_management.workflows.workflow_registry import workflow_registry
from wealth_management.workflows.workflow_executor import WorkflowExecutor

async def main():
    """Interactive workflow executor"""
    
    print("🔧 Direct Workflow Execution")
    print("=" * 50)
    
    executor = WorkflowExecutor(workflow_registry)
    
    # Show available workflows
    print("\n📋 Available Workflows:")
    categories = ['advisor', 'client', 'operations']
    
    for category in categories:
        workflows = workflow_registry.get_workflows_by_category_name(category)
        print(f"\n{category.upper()} ({len(workflows)} workflows):")
        for workflow in workflows[:5]:  # Show first 5 of each category
            print(f"  • {workflow.workflow_id}: {workflow.name}")
        if len(workflows) > 5:
            print(f"  ... and {len(workflows) - 5} more")
    
    print("\n" + "=" * 50)
    print("Enter workflow ID and context (or 'list' to see all, 'quit' to exit)")
    
    while True:
        try:
            command = input("\n💬 Command: ").strip()
            
            if command.lower() in ['quit', 'exit', 'q']:
                break
                
            if command.lower() == 'list':
                # Show all workflows
                all_workflows = workflow_registry.get_all_workflows()
                print(f"\n📋 All {len(all_workflows)} Workflows:")
                for workflow in all_workflows:
                    print(f"  {workflow.workflow_id}: {workflow.name} ({workflow.pattern.value})")
                continue
                
            if not command:
                continue
            
            # Parse command (workflow_id or workflow_id:context)
            if ':' in command:
                workflow_id, context_str = command.split(':', 1)
                try:
                    context = json.loads(context_str)
                except:
                    context = {"query": context_str}
            else:
                workflow_id = command
                context = {"demo_mode": True}
            
            workflow_id = workflow_id.strip()
            
            # Get workflow info
            workflow_def = workflow_registry.get_workflow(workflow_id)
            if not workflow_def:
                print(f"❌ Workflow '{workflow_id}' not found. Type 'list' to see all workflows.")
                continue
            
            print(f"\n🔄 Executing: {workflow_def.name}")
            print(f"   Pattern: {workflow_def.pattern.value}")
            print(f"   Complexity: {workflow_def.complexity}")
            print(f"   Context: {json.dumps(context, indent=2)}")
            print("-" * 40)
            
            # Execute workflow
            execution = await executor.execute_workflow(workflow_id, context)
            
            print(f"✅ Status: {execution.status.value}")
            print(f"📋 Steps Completed: {len(execution.step_results)}")
            
            if execution.results:
                print(f"📊 Results Preview:")
                # Show key results based on pattern
                if workflow_def.pattern.value == 'sequential':
                    steps = execution.results.get('steps_completed', [])
                    print(f"   Sequential steps: {len(steps)}")
                elif workflow_def.pattern.value == 'parallel':
                    tasks = execution.results.get('parallel_tasks', [])
                    print(f"   Parallel tasks: {len(tasks)}")
                elif workflow_def.pattern.value == 'loop':
                    iterations = execution.results.get('iterations', 0)
                    print(f"   Loop iterations: {iterations}")
                elif workflow_def.pattern.value == 'event_driven':
                    response_time = execution.results.get('response_time', 0)
                    print(f"   Response time: {response_time:.2f}s")
                elif workflow_def.pattern.value == 'scheduled':
                    next_run = execution.results.get('next_scheduled_run')
                    print(f"   Next run: {next_run}")
            
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())