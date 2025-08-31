"""Workflow management system for wealth management agent

This package provides a comprehensive workflow system that implements all 33 
wealth management workflows with proper ADK pattern support and testing framework.

Components:
- WorkflowRegistry: Central registry of all workflow definitions
- WorkflowExecutor: Executes workflows using appropriate ADK patterns  
- WorkflowTestFramework: Comprehensive testing for all workflows
"""

from .workflow_registry import (
    WorkflowRegistry, 
    WorkflowDefinition, 
    WorkflowStatus,
    WorkflowCategory,
    ADKPattern,
    workflow_registry
)

from .workflow_executor import (
    WorkflowExecutor,
    WorkflowExecution
)

from .test_framework import (
    WorkflowTestFramework,
    TestCase,
    TestResult,
    run_comprehensive_tests,
    run_regression_tests
)

# Initialize default components
default_executor = WorkflowExecutor(workflow_registry)
default_test_framework = WorkflowTestFramework(workflow_registry, default_executor)

__all__ = [
    # Registry components
    'WorkflowRegistry',
    'WorkflowDefinition', 
    'WorkflowStatus',
    'WorkflowCategory',
    'ADKPattern',
    'workflow_registry',
    
    # Executor components
    'WorkflowExecutor',
    'WorkflowExecution',
    'default_executor',
    
    # Testing components
    'WorkflowTestFramework',
    'TestCase',
    'TestResult',
    'default_test_framework',
    'run_comprehensive_tests',
    'run_regression_tests'
]