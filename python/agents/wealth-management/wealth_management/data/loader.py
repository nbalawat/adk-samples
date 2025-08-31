"""Data loader utilities for accessing generated datasets"""

import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path

class WealthDataLoader:
    """Load and provide access to generated wealth management datasets"""
    
    def __init__(self, datasets_dir: str = "datasets"):
        self.datasets_dir = Path(datasets_dir)
        self._cache = {}
        
    def load_clients(self) -> List[Dict[str, Any]]:
        """Load client data"""
        return self._load_dataset("clients")
    
    def load_portfolios(self) -> List[Dict[str, Any]]:
        """Load portfolio data"""
        return self._load_dataset("portfolios")
    
    def load_relationships(self) -> List[Dict[str, Any]]:
        """Load relationship data"""
        return self._load_dataset("relationships")
    
    def load_advisors(self) -> List[Dict[str, Any]]:
        """Load advisor data"""
        return self._load_dataset("advisors")
    
    def load_relationship_managers(self) -> List[Dict[str, Any]]:
        """Load relationship manager data"""
        return self._load_dataset("relationship_managers")
    
    def load_market_scenarios(self) -> List[Dict[str, Any]]:
        """Load market scenario data"""
        return self._load_dataset("market_scenarios")
    
    def load_transactions(self) -> List[Dict[str, Any]]:
        """Load transaction data"""
        return self._load_dataset("transactions")
    
    def load_summary(self) -> Dict[str, Any]:
        """Load dataset summary"""
        return self._load_dataset("summary")
    
    def get_client_by_id(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Get specific client by ID"""
        clients = self.load_clients()
        return next((c for c in clients if c['client_id'] == client_id), None)
    
    def get_portfolio_by_client_id(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Get portfolio for specific client"""
        portfolios = self.load_portfolios()
        return next((p for p in portfolios if p['client_id'] == client_id), None)
    
    def get_clients_by_advisor(self, advisor_id: str) -> List[Dict[str, Any]]:
        """Get all clients for specific advisor"""
        relationships = self.load_relationships()
        client_ids = [r['client_id'] for r in relationships if r['advisor_id'] == advisor_id]
        clients = self.load_clients()
        return [c for c in clients if c['client_id'] in client_ids]
    
    def get_clients_by_wealth_tier(self, wealth_tier: str) -> List[Dict[str, Any]]:
        """Get clients by wealth tier"""
        clients = self.load_clients()
        return [c for c in clients if c['wealth_tier'] == wealth_tier]
    
    def get_clients_by_risk_tolerance(self, risk_tolerance: str) -> List[Dict[str, Any]]:
        """Get clients by risk tolerance"""
        clients = self.load_clients()
        return [c for c in clients if c['risk_tolerance'] == risk_tolerance]
    
    def get_high_volatility_scenarios(self) -> List[Dict[str, Any]]:
        """Get market scenarios with high volatility"""
        scenarios = self.load_market_scenarios()
        return [s for s in scenarios if s.get('severity') in ['High', 'Extreme']]
    
    def get_recent_transactions(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get transactions from last N days"""
        from datetime import datetime, timedelta
        
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        transactions = self.load_transactions()
        return [t for t in transactions if t['transaction_date'] >= cutoff_date]
    
    def get_portfolio_performance_summary(self) -> Dict[str, Any]:
        """Get aggregate portfolio performance metrics"""
        portfolios = self.load_portfolios()
        
        if not portfolios:
            return {}
        
        total_value = sum(p['total_value'] for p in portfolios)
        
        # Calculate weighted averages
        ytd_returns = []
        one_year_returns = []
        
        for portfolio in portfolios:
            weight = portfolio['total_value'] / total_value
            perf = portfolio['performance']
            ytd_returns.append(perf['ytd_return'] * weight)
            one_year_returns.append(perf['one_year_return'] * weight)
        
        return {
            "total_aum": total_value,
            "portfolio_count": len(portfolios),
            "weighted_ytd_return": sum(ytd_returns),
            "weighted_one_year_return": sum(one_year_returns),
            "average_portfolio_value": total_value / len(portfolios)
        }
    
    def search_clients(self, **criteria) -> List[Dict[str, Any]]:
        """Search clients by multiple criteria"""
        clients = self.load_clients()
        results = []
        
        for client in clients:
            match = True
            for key, value in criteria.items():
                if key not in client:
                    match = False
                    break
                
                # Handle different comparison types
                if isinstance(value, (list, tuple)):
                    if client[key] not in value:
                        match = False
                        break
                elif isinstance(value, dict):
                    # Range queries like {'min': 100000, 'max': 1000000}
                    if 'min' in value and client[key] < value['min']:
                        match = False
                        break
                    if 'max' in value and client[key] > value['max']:
                        match = False
                        break
                else:
                    if client[key] != value:
                        match = False
                        break
            
            if match:
                results.append(client)
        
        return results
    
    def get_workflow_test_data(self, workflow_type: str) -> Dict[str, Any]:
        """Get sample data for testing specific workflow types"""
        
        clients = self.load_clients()
        portfolios = self.load_portfolios()
        scenarios = self.load_market_scenarios()
        
        # Return relevant data based on workflow type
        if workflow_type == "crisis_response":
            return {
                "high_value_clients": [c for c in clients if c['total_assets'] > 10000000][:10],
                "volatile_scenarios": [s for s in scenarios if s.get('severity') == 'Extreme'][:5],
                "sample_portfolios": [p for p in portfolios if p['total_value'] > 5000000][:5]
            }
        
        elif workflow_type == "market_volatility":
            return {
                "affected_clients": clients[:50],  # Sample of clients
                "volatility_scenarios": [s for s in scenarios if s.get('event_type') == 'market_volatility'][:10],
                "portfolio_exposures": portfolios[:20]
            }
        
        elif workflow_type == "client_onboarding":
            return {
                "new_prospects": [c for c in clients if c['status'] == 'Prospect'][:10],
                "sample_portfolios": portfolios[:5],
                "advisor_assignments": self.load_relationships()[:10]
            }
        
        elif workflow_type == "portfolio_rebalancing":
            return {
                "rebalance_candidates": [p for p in portfolios if 
                                       abs(p['equity_allocation'] - 0.6) > 0.1][:15],
                "client_profiles": clients[:15],
                "market_conditions": scenarios[:5]
            }
        
        else:
            # Default test data
            return {
                "sample_clients": clients[:10],
                "sample_portfolios": portfolios[:10],
                "sample_scenarios": scenarios[:5],
                "sample_relationships": self.load_relationships()[:10]
            }
    
    def _load_dataset(self, dataset_name: str) -> Any:
        """Load dataset with caching"""
        if dataset_name in self._cache:
            return self._cache[dataset_name]
        
        filepath = self.datasets_dir / f"{dataset_name}.json"
        
        if not filepath.exists():
            raise FileNotFoundError(f"Dataset file not found: {filepath}")
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self._cache[dataset_name] = data
        return data
    
    def clear_cache(self):
        """Clear dataset cache"""
        self._cache.clear()
    
    def get_dataset_info(self) -> Dict[str, Any]:
        """Get information about available datasets"""
        info = {
            "datasets_directory": str(self.datasets_dir),
            "available_datasets": [],
            "total_size_mb": 0
        }
        
        if self.datasets_dir.exists():
            for file in self.datasets_dir.glob("*.json"):
                size_mb = file.stat().st_size / (1024 * 1024)
                info["available_datasets"].append({
                    "name": file.stem,
                    "size_mb": round(size_mb, 2)
                })
                info["total_size_mb"] += size_mb
        
        info["total_size_mb"] = round(info["total_size_mb"], 2)
        return info

# Global data loader instance
data_loader = WealthDataLoader()

# Convenience functions
def get_client(client_id: str) -> Optional[Dict[str, Any]]:
    """Get client by ID"""
    return data_loader.get_client_by_id(client_id)

def get_portfolio(client_id: str) -> Optional[Dict[str, Any]]:
    """Get portfolio by client ID"""
    return data_loader.get_portfolio_by_client_id(client_id)

def search_clients(**criteria) -> List[Dict[str, Any]]:
    """Search clients by criteria"""
    return data_loader.search_clients(**criteria)

def get_test_data(workflow_type: str) -> Dict[str, Any]:
    """Get test data for workflow"""
    return data_loader.get_workflow_test_data(workflow_type)