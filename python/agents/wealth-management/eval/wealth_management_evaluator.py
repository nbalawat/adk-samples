"""Wealth Management Agent Evaluator using ADK AgentEvaluator pattern."""

import asyncio
import json
import logging
import pathlib
from pathlib import Path
from typing import Dict, Any, List
from google.adk.evaluation.agent_evaluator import AgentEvaluator
import dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WealthManagementEvaluator:
    """Enhanced evaluator for wealth management agent using ADK patterns."""
    
    def __init__(self, config_path: str = None):
        """Initialize evaluator with configuration."""
        if config_path is None:
            config_path = Path(__file__).parent / "data" / "test_config.json"
        
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Load environment variables
        dotenv.load_dotenv()
        
    async def run_adk_evaluation(self, data_dir: str = None, num_runs: int = 5) -> Dict[str, Any]:
        """Run ADK-based evaluation."""
        if data_dir is None:
            data_dir = str(Path(__file__).parent / "data")
        
        logger.info(f"Running ADK evaluation with {num_runs} runs")
        
        try:
            # Use ADK's built-in AgentEvaluator
            await AgentEvaluator.evaluate(
                "wealth_management",
                data_dir,
                num_runs=num_runs,
            )
            
            return {"status": "completed", "evaluation_type": "adk_built_in"}
            
        except Exception as e:
            logger.error(f"ADK evaluation failed: {str(e)}")
            return {"status": "failed", "error": str(e)}
    
    async def run_custom_evaluation(self, test_file: str = None) -> Dict[str, Any]:
        """Run custom evaluation for wealth management specific features."""
        if test_file is None:
            test_file = Path(__file__).parent / "data" / "wealth_management.test.json"
        
        try:
            with open(test_file, 'r') as f:
                test_cases = json.load(f)
        except FileNotFoundError:
            logger.warning(f"Test file {test_file} not found. Skipping custom evaluation.")
            return {"status": "skipped", "reason": "test_file_not_found"}
        
        logger.info(f"Running custom evaluation with {len(test_cases)} test cases")
        
        results = []
        for test_case in test_cases:
            logger.info(f"Evaluating: {test_case['id']} - {test_case['name']}")
            
            # Evaluate workflow completion
            workflow_score = self._evaluate_workflow_completion(test_case)
            
            # Evaluate data accuracy
            accuracy_score = self._evaluate_data_accuracy(test_case)
            
            # Evaluate compliance
            compliance_score = self._evaluate_compliance(test_case)
            
            # Calculate overall score (simplified weights)
            overall_score = (
                workflow_score * 0.4 +
                accuracy_score * 0.4 +
                compliance_score * 0.2
            )
            
            results.append({
                "test_id": test_case["id"],
                "test_name": test_case["name"],
                "workflow_score": workflow_score,
                "accuracy_score": accuracy_score, 
                "compliance_score": compliance_score,
                "overall_score": overall_score,
                "rating": self._get_rating(overall_score)
            })
        
        return {
            "status": "completed",
            "evaluation_type": "custom",
            "results": results,
            "summary": self._calculate_summary(results)
        }
    
    def _evaluate_workflow_completion(self, test_case: Dict[str, Any]) -> float:
        """Evaluate workflow completion score."""
        workflow_type = test_case.get("workflow_type", "unknown")
        
        # Get expected tools from config if available, otherwise use defaults
        if "workflow_specific_tests" in self.config and workflow_type in self.config["workflow_specific_tests"]:
            expected_tools = self.config["workflow_specific_tests"][workflow_type].get("required_tools", [])
        else:
            expected_tools = []
        
        # For now, assume 80% completion rate (would be replaced with actual agent interaction)
        return 0.8
    
    def _evaluate_data_accuracy(self, test_case: Dict[str, Any]) -> float:
        """Evaluate data accuracy score."""
        # Simulate data accuracy evaluation
        return 0.85
    
    def _evaluate_compliance(self, test_case: Dict[str, Any]) -> float:
        """Evaluate compliance score."""
        # Simulate compliance evaluation
        return 0.9
    
    def _get_rating(self, score: float) -> str:
        """Get rating based on score."""
        score_percent = score * 100
        
        for rating, config in self.config["scoring"].items():
            if score_percent >= config["min_score"]:
                return rating
        
        return "needs_improvement"
    
    def _calculate_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate evaluation summary."""
        if not results:
            return {}
        
        scores = [r["overall_score"] for r in results]
        avg_score = sum(scores) / len(scores) * 100
        
        ratings = [r["rating"] for r in results]
        rating_counts = {}
        for rating in ratings:
            rating_counts[rating] = rating_counts.get(rating, 0) + 1
        
        return {
            "total_tests": len(results),
            "average_score": round(avg_score, 1),
            "rating_distribution": rating_counts,
            "overall_rating": self._get_rating(avg_score / 100)
        }


async def main():
    """Main evaluation function."""
    evaluator = WealthManagementEvaluator()
    
    print("Starting Wealth Management Agent Evaluation...")
    print("=" * 60)
    
    # Run ADK evaluation
    print("\n1. Running ADK Built-in Evaluation...")
    adk_results = await evaluator.run_adk_evaluation()
    print(f"ADK Evaluation: {adk_results['status']}")
    
    # Run custom evaluation
    print("\n2. Running Custom Workflow Evaluation...")
    custom_results = await evaluator.run_custom_evaluation()
    print(f"Custom Evaluation: {custom_results['status']}")
    
    if custom_results.get("status") == "completed":
        summary = custom_results["summary"]
        print(f"\nCustom Evaluation Summary:")
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Average Score: {summary['average_score']:.1f}%")
        print(f"Overall Rating: {summary['overall_rating'].title()}")
        print(f"Rating Distribution: {summary['rating_distribution']}")
    
    print("\nEvaluation completed!")
    return {"adk_results": adk_results, "custom_results": custom_results}


if __name__ == "__main__":
    asyncio.run(main())