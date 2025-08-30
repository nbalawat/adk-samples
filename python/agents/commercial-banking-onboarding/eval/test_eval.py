"""Evaluation script for commercial banking onboarding agents."""

import json
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Tuple
import asyncio
import logging

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from commercial_banking_onboarding.agent import agent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OnboardingEvaluator:
    """Evaluator for commercial banking onboarding agent system."""
    
    def __init__(self, config_path: str = None):
        """Initialize evaluator with configuration."""
        if config_path is None:
            config_path = Path(__file__).parent / "data" / "test_config.json"
        
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.test_results = []
        self.agent = agent
    
    async def run_evaluation(self, test_file: str = None) -> Dict[str, Any]:
        """Run complete evaluation suite."""
        if test_file is None:
            test_file = Path(__file__).parent / "data" / "commercial_banking_onboarding.test.json"
        
        # Load test cases
        with open(test_file, 'r') as f:
            test_cases = json.load(f)
        
        logger.info(f"Running evaluation with {len(test_cases)} test cases")
        
        # Run tests
        for test_case in test_cases:
            logger.info(f"Running test: {test_case['id']} - {test_case['name']}")
            
            start_time = time.time()
            try:
                result = await self.run_test_case(test_case)
                result['execution_time'] = time.time() - start_time
                result['status'] = 'completed'
            except Exception as e:
                logger.error(f"Test {test_case['id']} failed: {str(e)}")
                result = {
                    'test_id': test_case['id'],
                    'status': 'failed',
                    'error': str(e),
                    'execution_time': time.time() - start_time
                }
            
            self.test_results.append(result)
        
        # Calculate overall scores
        evaluation_summary = self.calculate_evaluation_summary()
        
        return {
            'test_results': self.test_results,
            'summary': evaluation_summary,
            'config': self.config
        }
    
    async def run_test_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Run individual test case."""
        test_id = test_case['id']
        test_input = test_case['input']
        expected_output = test_case['expected_output']
        
        # Simulate agent interaction
        response = await self.simulate_agent_interaction(test_input)
        
        # Evaluate response against expected output
        evaluation_result = self.evaluate_response(response, expected_output)
        
        return {
            'test_id': test_id,
            'test_name': test_case['name'],
            'input': test_input,
            'expected_output': expected_output,
            'actual_output': response,
            'evaluation': evaluation_result
        }
    
    async def simulate_agent_interaction(self, test_input: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate interaction with the agent system."""
        request = test_input['request']
        
        # For demonstration, we'll simulate the complete workflow
        # In a real implementation, this would call the actual agent
        
        simulated_response = {
            'application_created': True,
            'application_id': 'APP-20240101123456-ABCD',
            'workflow_steps': []
        }
        
        # Simulate KYC verification
        if 'business_info' in test_input:
            kyc_result = self.simulate_kyc_verification(
                test_input['business_info'],
                test_input.get('beneficial_owners', [])
            )
            simulated_response['kyc_verification'] = kyc_result
            simulated_response['workflow_steps'].append('kyc_verification')
        
        # Simulate credit assessment
        if 'business_info' in test_input:
            credit_result = self.simulate_credit_assessment(test_input['business_info'])
            simulated_response['credit_assessment'] = credit_result
            simulated_response['workflow_steps'].append('credit_assessment')
        
        # Simulate compliance screening
        compliance_result = self.simulate_compliance_screening(
            test_input['business_info'],
            test_input.get('beneficial_owners', [])
        )
        simulated_response['compliance_screening'] = compliance_result
        simulated_response['workflow_steps'].append('compliance_screening')
        
        # Simulate document processing if documents provided
        if 'documents' in test_input:
            doc_result = self.simulate_document_processing(test_input['documents'])
            simulated_response['document_processing'] = doc_result
            simulated_response['workflow_steps'].append('document_processing')
        
        # Make final decision
        final_decision = self.simulate_final_decision(simulated_response)
        simulated_response['final_decision'] = final_decision
        
        # Simulate account setup if approved
        if final_decision in ['approved', 'approved_with_conditions']:
            if 'approved_configuration' in test_input:
                setup_result = self.simulate_account_setup(test_input['approved_configuration'])
                simulated_response['account_setup'] = setup_result
                simulated_response['workflow_steps'].append('account_setup')
        
        return simulated_response
    
    def simulate_kyc_verification(self, business_info: Dict[str, Any], owners: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simulate KYC verification process."""
        # Business verification
        business_verified = True
        business_score = 85
        
        # Check for suspicious business names
        business_name = business_info.get('legal_name', '').lower()
        if any(word in business_name for word in ['fake', 'test', 'fraud']):
            business_verified = False
            business_score = 30
        
        # Owner verification
        owners_verified = len(owners) > 0
        total_ownership = sum(owner.get('ownership_percentage', 0) for owner in owners)
        ownership_valid = 95 <= total_ownership <= 105
        
        # PEP screening
        pep_check_passed = True
        for owner in owners:
            name = f"{owner.get('first_name', '')} {owner.get('last_name', '')}"
            if 'political' in name.lower() or 'government' in name.lower():
                pep_check_passed = False
        
        overall_score = (business_score + (85 if owners_verified else 30) + (90 if pep_check_passed else 20)) / 3
        
        manual_review_required = overall_score < 70 or not pep_check_passed
        
        return {
            'business_verified': business_verified,
            'owners_verified': owners_verified,
            'ownership_percentage_valid': ownership_valid,
            'pep_check_passed': pep_check_passed,
            'overall_score': round(overall_score, 1),
            'manual_review_required': manual_review_required
        }
    
    def simulate_credit_assessment(self, business_info: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate credit assessment process."""
        annual_revenue = business_info.get('annual_revenue', 0)
        industry_code = business_info.get('industry_code', '')
        
        # Base credit score calculation
        if annual_revenue >= 5000000:
            base_score = 750
        elif annual_revenue >= 1000000:
            base_score = 700
        elif annual_revenue >= 500000:
            base_score = 650
        else:
            base_score = 600
        
        # Industry risk adjustment
        high_risk_industries = ['522291', '713']  # Payday lending, gaming
        if industry_code in high_risk_industries:
            base_score -= 100
            risk_rating = 'very_high'
            industry_risk_score = 80
        elif industry_code.startswith('72'):  # Food service
            base_score -= 50
            risk_rating = 'high'
            industry_risk_score = 60
        else:
            risk_rating = 'medium' if base_score < 700 else 'low'
            industry_risk_score = 30 if risk_rating == 'low' else 40
        
        # Calculate recommended credit limit
        if risk_rating == 'low':
            credit_multiplier = 0.15
        elif risk_rating == 'medium':
            credit_multiplier = 0.10
        elif risk_rating == 'high':
            credit_multiplier = 0.05
        else:
            credit_multiplier = 0.02
        
        recommended_credit_limit = annual_revenue * credit_multiplier
        
        return {
            'credit_score': max(300, base_score),
            'risk_rating': risk_rating,
            'industry_risk_score': industry_risk_score,
            'recommended_credit_limit': recommended_credit_limit
        }
    
    def simulate_compliance_screening(self, business_info: Dict[str, Any], owners: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simulate compliance screening process."""
        # Sanctions screening
        sanctions_passed = True
        business_name = business_info.get('legal_name', '').lower()
        if 'sanctioned' in business_name or 'blocked' in business_name:
            sanctions_passed = False
        
        # AML risk assessment
        industry_code = business_info.get('industry_code', '')
        high_risk_industries = ['522291', '713', '531']
        
        if industry_code in high_risk_industries:
            aml_risk_level = 'high'
            aml_score = 70
        else:
            aml_risk_level = 'medium'
            aml_score = 85
        
        # Geographic risk
        state = business_info.get('business_address', {}).get('state', '')
        if state in ['NV', 'FL']:  # Higher risk states for demo
            aml_score -= 10
        
        aml_passed = aml_score >= 60
        
        # Ownership structure risk
        ownership_risk = 'low'
        if len(owners) > 5:
            ownership_risk = 'medium'
            aml_score -= 5
        
        # Enhanced due diligence
        edd_required = aml_risk_level in ['high', 'very_high'] or not sanctions_passed
        
        overall_score = (85 if sanctions_passed else 30) * 0.4 + aml_score * 0.4 + 85 * 0.2
        
        return {
            'sanctions_check_passed': sanctions_passed,
            'aml_check_passed': aml_passed,
            'aml_risk_level': aml_risk_level,
            'ownership_structure_risk': ownership_risk,
            'compliance_score': round(overall_score, 1),
            'enhanced_due_diligence_required': edd_required
        }
    
    def simulate_document_processing(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simulate document processing."""
        all_valid = True
        missing_docs = []
        authenticity_results = []
        
        # Check for required documents
        required_types = ['articles_of_incorporation', 'business_license', 'tax_id_certificate']
        provided_types = [doc['document_type'] for doc in documents]
        
        for req_type in required_types:
            if req_type not in provided_types:
                missing_docs.append(req_type)
                all_valid = False
        
        # Validate each document
        for doc in documents:
            doc_data = doc.get('document_data', {})
            business_name = doc_data.get('business_name', '')
            
            # Check for consistency
            authentic = 'fraud' not in business_name.lower() and 'fake' not in business_name.lower()
            authenticity_results.append({
                'document_type': doc['document_type'],
                'is_authentic': authentic,
                'authenticity_score': 95 if authentic else 20
            })
            
            if not authentic:
                all_valid = False
        
        # Cross-validation
        business_names = [doc.get('document_data', {}).get('business_name', '') for doc in documents]
        consistent = len(set(business_names)) <= 1  # All names should be the same
        
        return {
            'all_documents_valid': all_valid,
            'missing_documents': missing_docs,
            'authenticity_verification': {
                'all_authentic': all(r['is_authentic'] for r in authenticity_results)
            },
            'cross_validation': {
                'is_consistent': consistent
            }
        }
    
    def simulate_account_setup(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate account setup process."""
        account_types = config.get('account_types', [])
        services = config.get('services', [])
        users = config.get('users', [])
        materials = config.get('materials', [])
        
        # Generate account numbers
        account_numbers = {}
        for acc_type in account_types:
            account_numbers[acc_type] = f"100{len(acc_type)}{hash(acc_type) % 1000000000:09d}"
        
        return {
            'account_creation': {
                'accounts_created': len(account_types),
                'account_numbers': 'generated'
            },
            'services_setup': {
                'services_activated': len(services)
            },
            'online_banking': {
                'users_configured': len(users),
                'company_id': 'generated'
            },
            'materials_order': {
                'materials_ordered': len(materials)
            },
            'setup_status': 'completed'
        }
    
    def simulate_final_decision(self, response: Dict[str, Any]) -> str:
        """Make final onboarding decision based on all results."""
        kyc = response.get('kyc_verification', {})
        credit = response.get('credit_assessment', {})
        compliance = response.get('compliance_screening', {})
        
        # Check for automatic rejection criteria
        if not kyc.get('business_verified', True):
            return 'rejected'
        
        if not compliance.get('sanctions_check_passed', True):
            return 'rejected'
        
        if credit.get('risk_rating') == 'very_high':
            return 'rejected'
        
        # Check for manual review criteria
        if kyc.get('manual_review_required', False):
            return 'manual_review'
        
        if compliance.get('enhanced_due_diligence_required', False):
            return 'manual_review'
        
        if credit.get('risk_rating') == 'high':
            return 'approved_with_conditions'
        
        return 'approved'
    
    def evaluate_response(self, response: Dict[str, Any], expected: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate response against expected output."""
        evaluation = {
            'score': 0,
            'max_score': 0,
            'passed_checks': [],
            'failed_checks': [],
            'details': {}
        }
        
        # Evaluate each expected field
        for key, expected_value in expected.items():
            evaluation['max_score'] += 1
            
            if key in response:
                actual_value = response[key]
                
                if self.values_match(actual_value, expected_value):
                    evaluation['score'] += 1
                    evaluation['passed_checks'].append(key)
                else:
                    evaluation['failed_checks'].append(f"{key}: expected {expected_value}, got {actual_value}")
            else:
                evaluation['failed_checks'].append(f"Missing field: {key}")
            
            evaluation['details'][key] = {
                'expected': expected_value,
                'actual': response.get(key),
                'passed': key in evaluation['passed_checks']
            }
        
        # Calculate percentage score
        evaluation['percentage'] = (evaluation['score'] / evaluation['max_score'] * 100) if evaluation['max_score'] > 0 else 0
        
        return evaluation
    
    def values_match(self, actual: Any, expected: Any) -> bool:
        """Check if actual value matches expected value (with special handling for conditions)."""
        if isinstance(expected, str):
            # Handle special conditions like ">= 80", "> 0", etc.
            if expected.startswith('>='):
                threshold = float(expected.split('>=')[1].strip())
                return isinstance(actual, (int, float)) and actual >= threshold
            elif expected.startswith('>'):
                threshold = float(expected.split('>')[1].strip())
                return isinstance(actual, (int, float)) and actual > threshold
            elif expected.startswith('<='):
                threshold = float(expected.split('<=')[1].strip())
                return isinstance(actual, (int, float)) and actual <= threshold
            elif expected.startswith('<'):
                threshold = float(expected.split('<')[1].strip())
                return isinstance(actual, (int, float)) and actual < threshold
            elif '|' in expected:
                # Handle multiple acceptable values like "low|medium"
                acceptable_values = [v.strip() for v in expected.split('|')]
                return actual in acceptable_values
            elif expected == '[]':
                return isinstance(actual, list) and len(actual) == 0
            elif expected == 'generated':
                return actual is not None and actual != ''
        
        if isinstance(expected, dict) and isinstance(actual, dict):
            return all(self.values_match(actual.get(k), v) for k, v in expected.items())
        
        if isinstance(expected, list) and isinstance(actual, list):
            if len(expected) != len(actual):
                return False
            return all(self.values_match(actual[i], expected[i]) for i in range(len(expected)))
        
        return actual == expected
    
    def calculate_evaluation_summary(self) -> Dict[str, Any]:
        """Calculate overall evaluation summary."""
        if not self.test_results:
            return {'error': 'No test results available'}
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.get('status') == 'completed')
        failed_tests = total_tests - passed_tests
        
        # Calculate average scores
        scores = []
        execution_times = []
        
        for result in self.test_results:
            if result.get('status') == 'completed':
                eval_data = result.get('evaluation', {})
                scores.append(eval_data.get('percentage', 0))
                execution_times.append(result.get('execution_time', 0))
        
        avg_score = sum(scores) / len(scores) if scores else 0
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
        
        # Determine overall rating
        if avg_score >= 90:
            rating = 'excellent'
        elif avg_score >= 80:
            rating = 'good'
        elif avg_score >= 70:
            rating = 'acceptable'
        else:
            rating = 'needs_improvement'
        
        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            'average_score': round(avg_score, 1),
            'average_execution_time': round(avg_execution_time, 2),
            'overall_rating': rating,
            'rating_description': self.config['scoring'][rating]['description']
        }


async def main():
    """Run the evaluation."""
    evaluator = OnboardingEvaluator()
    
    print("Starting Commercial Banking Onboarding Agent Evaluation...")
    print("=" * 60)
    
    # Run evaluation
    results = await evaluator.run_evaluation()
    
    # Print summary
    summary = results['summary']
    print(f"\nEvaluation Summary:")
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed: {summary['passed_tests']}")
    print(f"Failed: {summary['failed_tests']}")
    print(f"Success Rate: {summary['success_rate']:.1f}%")
    print(f"Average Score: {summary['average_score']:.1f}%")
    print(f"Average Execution Time: {summary['average_execution_time']:.2f}s")
    print(f"Overall Rating: {summary['overall_rating'].title()} - {summary['rating_description']}")
    
    # Print detailed results
    print(f"\nDetailed Test Results:")
    print("-" * 60)
    
    for result in results['test_results']:
        status = result.get('status', 'unknown')
        test_name = result.get('test_name', result.get('test_id', 'Unknown Test'))
        
        if status == 'completed':
            eval_data = result.get('evaluation', {})
            score = eval_data.get('percentage', 0)
            exec_time = result.get('execution_time', 0)
            
            print(f"✅ {test_name}")
            print(f"   Score: {score:.1f}% | Time: {exec_time:.2f}s")
            
            if eval_data.get('failed_checks'):
                print(f"   Issues: {', '.join(eval_data['failed_checks'][:2])}")
        else:
            error = result.get('error', 'Unknown error')
            print(f"❌ {test_name}")
            print(f"   Error: {error}")
        
        print()
    
    # Save detailed results
    output_file = Path(__file__).parent / "evaluation_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"Detailed results saved to: {output_file}")
    
    return results


if __name__ == "__main__":
    asyncio.run(main())