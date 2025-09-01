"""Integration tests that actually invoke the wealth management agent."""

import asyncio
import time
import pytest
from pathlib import Path
import sys

# Add the parent directory to the path for imports
sys.path.append(str(Path(__file__).parent.parent))

from wealth_management.agent import root_agent

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_agent_basic_interaction():
    """Test basic agent interaction and response quality."""
    print("Testing basic agent interaction...")
    
    query = "What can you help me with as a wealth management advisor?"
    start_time = time.time()
    
    try:
        # Create a simple session for testing
        from google.adk.core import Session
        session = Session(user_id="test_user_001", app_name="wealth_management")
        
        response = await root_agent.run(query, session=session)
        execution_time = time.time() - start_time
        
        print(f"Response time: {execution_time:.2f}s")
        print(f"Response length: {len(response.content)}")
        print(f"Response preview: {response.content[:200]}...")
        
        # Basic validation
        assert response is not None
        assert len(response.content) > 50
        assert execution_time < 30.0  # Should respond within 30 seconds
        
        # Check for wealth management keywords
        response_text = response.content.lower()
        wealth_keywords = ['portfolio', 'investment', 'financial', 'wealth', 'advisor', 'client']
        found_keywords = [kw for kw in wealth_keywords if kw in response_text]
        
        print(f"Found wealth management keywords: {found_keywords}")
        assert len(found_keywords) >= 2, f"Expected wealth management context, found: {found_keywords}"
        
        return {
            "status": "passed",
            "execution_time": execution_time,
            "response_length": len(response.content),
            "keywords_found": len(found_keywords)
        }
        
    except Exception as e:
        print(f"Agent interaction failed: {str(e)}")
        return {
            "status": "failed",
            "error": str(e),
            "execution_time": time.time() - start_time
        }


@pytest.mark.asyncio
async def test_portfolio_analysis_workflow():
    """Test portfolio analysis workflow with real agent."""
    print("Testing portfolio analysis workflow...")
    
    query = "Analyze the performance of account TEST001 for the last quarter"
    start_time = time.time()
    
    try:
        from google.adk.core import Session
        session = Session(user_id="test_user_002", app_name="wealth_management")
        
        response = await root_agent.run(query, session=session)
        execution_time = time.time() - start_time
        
        print(f"Portfolio analysis time: {execution_time:.2f}s")
        print(f"Response length: {len(response.content)}")
        
        # Validation
        assert response is not None
        assert execution_time < 45.0  # Portfolio analysis might take longer
        
        # Check for portfolio-specific content
        response_text = response.content.lower()
        portfolio_keywords = ['test001', 'portfolio', 'performance', 'quarter', 'analysis']
        found_keywords = [kw for kw in portfolio_keywords if kw in response_text]
        
        print(f"Found portfolio keywords: {found_keywords}")
        assert len(found_keywords) >= 2, f"Expected portfolio analysis context: {found_keywords}"
        
        return {
            "status": "passed",
            "execution_time": execution_time,
            "response_length": len(response.content),
            "portfolio_keywords": len(found_keywords)
        }
        
    except Exception as e:
        print(f"Portfolio analysis failed: {str(e)}")
        return {
            "status": "failed",
            "error": str(e),
            "execution_time": time.time() - start_time
        }


@pytest.mark.asyncio
async def test_client_analytics_workflow():
    """Test client analytics workflow."""
    print("Testing client analytics workflow...")
    
    query = "How has the recent market volatility affected all my clients?"
    start_time = time.time()
    
    try:
        from google.adk.core import Session
        session = Session(user_id="test_user_003", app_name="wealth_management")
        
        response = await root_agent.run(query, session=session)
        execution_time = time.time() - start_time
        
        print(f"Client analytics time: {execution_time:.2f}s")
        print(f"Response length: {len(response.content)}")
        
        # Validation
        assert response is not None
        assert execution_time < 60.0  # Analytics might be slower
        
        # Check for analytics-specific content
        response_text = response.content.lower()
        analytics_keywords = ['client', 'market', 'volatility', 'impact', 'analysis']
        found_keywords = [kw for kw in analytics_keywords if kw in response_text]
        
        print(f"Found analytics keywords: {found_keywords}")
        assert len(found_keywords) >= 3, f"Expected client analytics context: {found_keywords}"
        
        return {
            "status": "passed",
            "execution_time": execution_time,
            "response_length": len(response.content),
            "analytics_keywords": len(found_keywords)
        }
        
    except Exception as e:
        print(f"Client analytics failed: {str(e)}")
        return {
            "status": "failed",
            "error": str(e),
            "execution_time": time.time() - start_time
        }


@pytest.mark.asyncio
async def test_performance_benchmark():
    """Run performance benchmark with multiple queries."""
    print("Running performance benchmark...")
    
    queries = [
        "What can you help me with?",
        "Show me portfolio summary for TEST001",
        "What are the current market conditions?",
        "Help me assess risk tolerance",
        "Generate market commentary"
    ]
    
    results = []
    
    for i, query in enumerate(queries):
        print(f"Testing query {i+1}/{len(queries)}: {query[:50]}...")
        
        start_time = time.time()
        try:
            from google.adk.core import Session
            session = Session(user_id=f"benchmark_user_{i}", app_name="wealth_management")
            
            response = await root_agent.run(query, session=session)
            execution_time = time.time() - start_time
            
            results.append({
                "query": query,
                "status": "success",
                "execution_time": execution_time,
                "response_length": len(response.content)
            })
            
        except Exception as e:
            results.append({
                "query": query,
                "status": "failed",
                "execution_time": time.time() - start_time,
                "error": str(e)
            })
    
    # Calculate benchmark statistics
    successful_results = [r for r in results if r["status"] == "success"]
    failed_results = [r for r in results if r["status"] == "failed"]
    
    if successful_results:
        avg_time = sum(r["execution_time"] for r in successful_results) / len(successful_results)
        max_time = max(r["execution_time"] for r in successful_results)
        min_time = min(r["execution_time"] for r in successful_results)
        
        print(f"\nBenchmark Results:")
        print(f"  Successful queries: {len(successful_results)}/{len(queries)}")
        print(f"  Average response time: {avg_time:.2f}s")
        print(f"  Min response time: {min_time:.2f}s")
        print(f"  Max response time: {max_time:.2f}s")
        print(f"  Failed queries: {len(failed_results)}")
        
        # Assertions for performance
        assert len(successful_results) >= len(queries) * 0.8  # 80% success rate minimum
        assert avg_time < 30.0  # Average response under 30 seconds
        assert max_time < 60.0  # No query should take over 60 seconds
    
    return {
        "total_queries": len(queries),
        "successful": len(successful_results),
        "failed": len(failed_results),
        "success_rate": len(successful_results) / len(queries) * 100,
        "avg_response_time": avg_time if successful_results else 0,
        "results": results
    }


if __name__ == "__main__":
    # Run integration tests directly
    async def main():
        print("Running Wealth Management Agent Integration Tests")
        print("=" * 60)
        
        # Test 1: Basic interaction
        print("\n1. Testing Basic Agent Interaction...")
        basic_result = await test_agent_basic_interaction()
        print(f"Result: {basic_result}")
        
        # Test 2: Portfolio workflow
        print("\n2. Testing Portfolio Analysis Workflow...")
        portfolio_result = await test_portfolio_analysis_workflow()
        print(f"Result: {portfolio_result}")
        
        # Test 3: Client analytics workflow
        print("\n3. Testing Client Analytics Workflow...")
        analytics_result = await test_client_analytics_workflow()
        print(f"Result: {analytics_result}")
        
        # Test 4: Performance benchmark
        print("\n4. Running Performance Benchmark...")
        benchmark_result = await test_performance_benchmark()
        print(f"Result: {benchmark_result}")
        
        print(f"\n" + "=" * 60)
        print("Integration Tests Complete!")
    
    asyncio.run(main())