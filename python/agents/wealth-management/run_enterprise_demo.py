#!/usr/bin/env python3
"""
Script to run the Enterprise Demo System
Usage: uv run python run_enterprise_demo.py
"""

import asyncio
from wealth_management.demo import (
    run_advisor_demo,
    run_client_demo, 
    run_crisis_demo,
    get_demo_menu,
    default_enterprise_demo
)

async def main():
    """Interactive enterprise demo runner"""
    
    print("🎭 Enterprise Demo System")
    print("=" * 50)
    print("Experience wealth management workflows from different user perspectives")
    
    while True:
        try:
            # Show demo menu
            menu = get_demo_menu()
            print("\n" + menu)
            
            choice = input("\n🎯 Select Demo (1-8 or 'quit'): ").strip()
            
            if choice.lower() in ['quit', 'exit', 'q']:
                break
                
            print(f"\n🚀 Starting Demo {choice}...")
            print("-" * 40)
            
            # Run selected demo
            if choice == '1':
                result = await run_advisor_demo()
            elif choice == '2':
                result = await run_client_demo()
            elif choice == '3':
                result = await run_crisis_demo()
            elif choice == '4':
                # Custom demo - let user choose role and scenario
                print("Available Roles: advisor, client, operations, compliance")
                role = input("Choose role: ").strip()
                print("Available Scenarios: market_crisis, client_onboarding, quarterly_review, compliance_audit, planning_session, operations")
                scenario = input("Choose scenario: ").strip()
                result = await default_enterprise_demo.run_demo(role, scenario)
            elif choice == '5':
                # Show all workflows demo
                from wealth_management.workflows.demo import demo_all_workflows
                result = await demo_all_workflows()
            elif choice == '6':
                # Pattern showcase
                from wealth_management.workflows.demo import demo_pattern_showcase
                result = await demo_pattern_showcase()
            elif choice == '7':
                # Performance benchmarks
                from wealth_management.workflows.demo import run_performance_benchmarks
                result = await run_performance_benchmarks()
            elif choice == '8':
                # Interactive workflow browser
                await interactive_workflow_browser()
                continue
            else:
                print("❌ Invalid choice. Please select 1-8.")
                continue
            
            print(f"\n✅ Demo Complete!")
            if isinstance(result, dict) and 'summary' in result:
                print(f"📊 Summary: {result['summary']}")
            
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

async def interactive_workflow_browser():
    """Browse and execute workflows interactively"""
    from wealth_management.workflows.workflow_registry import workflow_registry
    from wealth_management.workflows.workflow_executor import WorkflowExecutor
    
    print("\n🔍 Interactive Workflow Browser")
    print("=" * 40)
    
    executor = WorkflowExecutor(workflow_registry)
    
    # Show categories
    print("\nCategories:")
    print("1. Advisor Workflows (15)")
    print("2. Client Workflows (10)")  
    print("3. Operations Workflows (8)")
    print("4. All Workflows (33)")
    
    cat_choice = input("\nSelect category (1-4): ").strip()
    
    if cat_choice == '1':
        workflows = workflow_registry.get_workflows_by_category_name('advisor')
    elif cat_choice == '2':
        workflows = workflow_registry.get_workflows_by_category_name('client')
    elif cat_choice == '3':
        workflows = workflow_registry.get_workflows_by_category_name('operations')
    else:
        workflows = workflow_registry.get_all_workflows()
    
    print(f"\n📋 Available Workflows ({len(workflows)}):")
    for i, workflow in enumerate(workflows, 1):
        print(f"{i:2d}. {workflow.workflow_id}: {workflow.name}")
        print(f"     Pattern: {workflow.pattern.value}, Complexity: {workflow.complexity}")
    
    try:
        wf_choice = int(input(f"\nSelect workflow (1-{len(workflows)}): ").strip())
        selected = workflows[wf_choice - 1]
        
        print(f"\n🔄 Executing: {selected.name}")
        
        # Use sample context
        context = {
            "client_id": "WM123456",
            "demo_mode": True,
            "interactive": True
        }
        
        execution = await executor.execute_workflow(selected.workflow_id, context)
        print(f"✅ Status: {execution.status.value}")
        print(f"📋 Steps: {len(execution.step_results)}")
        
    except (ValueError, IndexError):
        print("❌ Invalid selection")

if __name__ == "__main__":
    asyncio.run(main())