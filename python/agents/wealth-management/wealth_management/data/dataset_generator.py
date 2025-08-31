"""Generate realistic datasets for wealth management scenarios"""

import json
import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any
import numpy as np

class WealthDatasetGenerator:
    """Generate comprehensive wealth management datasets"""
    
    def __init__(self):
        self.client_data = []
        self.portfolio_data = []
        self.relationship_data = []
        self.market_data = []
        self.transaction_data = []
        
        # Reference data
        self.first_names = [
            "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
            "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
            "Thomas", "Sarah", "Christopher", "Karen", "Charles", "Nancy", "Daniel", "Lisa",
            "Matthew", "Betty", "Anthony", "Dorothy", "Mark", "Sandra", "Donald", "Donna",
            "Steven", "Carol", "Paul", "Ruth", "Andrew", "Sharon", "Joshua", "Michelle"
        ]
        
        self.last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
            "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
            "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
            "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"
        ]
        
        self.securities = [
            # Large Cap Stocks
            {"symbol": "AAPL", "name": "Apple Inc", "type": "equity", "sector": "Technology", "price": 175.43},
            {"symbol": "MSFT", "name": "Microsoft Corp", "type": "equity", "sector": "Technology", "price": 378.85},
            {"symbol": "GOOGL", "name": "Alphabet Inc", "type": "equity", "sector": "Technology", "price": 127.89},
            {"symbol": "AMZN", "name": "Amazon.com Inc", "type": "equity", "sector": "Consumer Discretionary", "price": 144.73},
            {"symbol": "TSLA", "name": "Tesla Inc", "type": "equity", "sector": "Consumer Discretionary", "price": 207.30},
            {"symbol": "JPM", "name": "JPMorgan Chase", "type": "equity", "sector": "Financial", "price": 158.42},
            {"symbol": "JNJ", "name": "Johnson & Johnson", "type": "equity", "sector": "Healthcare", "price": 162.35},
            {"symbol": "V", "name": "Visa Inc", "type": "equity", "sector": "Financial", "price": 262.77},
            {"symbol": "PG", "name": "Procter & Gamble", "type": "equity", "sector": "Consumer Staples", "price": 158.90},
            {"symbol": "UNH", "name": "UnitedHealth Group", "type": "equity", "sector": "Healthcare", "price": 542.18},
            
            # ETFs
            {"symbol": "SPY", "name": "SPDR S&P 500 ETF", "type": "etf", "sector": "Large Cap", "price": 441.07},
            {"symbol": "QQQ", "name": "Invesco QQQ Trust", "type": "etf", "sector": "Technology", "price": 381.94},
            {"symbol": "IWM", "name": "iShares Russell 2000", "type": "etf", "sector": "Small Cap", "price": 218.45},
            {"symbol": "VTI", "name": "Vanguard Total Stock Market", "type": "etf", "sector": "Total Market", "price": 237.89},
            {"symbol": "BND", "name": "Vanguard Total Bond Market", "type": "etf", "sector": "Bonds", "price": 78.92},
            
            # Bonds
            {"symbol": "AGG", "name": "iShares Core US Aggregate Bond", "type": "bond", "sector": "Government", "price": 104.23},
            {"symbol": "TLT", "name": "iShares 20+ Year Treasury Bond", "type": "bond", "sector": "Government", "price": 95.67},
            {"symbol": "HYG", "name": "iShares iBoxx High Yield Corporate", "type": "bond", "sector": "Corporate", "price": 82.45},
            
            # International
            {"symbol": "VEA", "name": "Vanguard FTSE Developed Markets", "type": "etf", "sector": "International", "price": 49.23},
            {"symbol": "VWO", "name": "Vanguard FTSE Emerging Markets", "type": "etf", "sector": "Emerging Markets", "price": 42.18}
        ]
        
        self.cities = [
            "New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", "Phoenix, AZ",
            "Philadelphia, PA", "San Antonio, TX", "San Diego, CA", "Dallas, TX", "San Jose, CA",
            "Austin, TX", "Jacksonville, FL", "Fort Worth, TX", "Columbus, OH", "Charlotte, NC",
            "San Francisco, CA", "Indianapolis, IN", "Seattle, WA", "Denver, CO", "Washington, DC",
            "Boston, MA", "El Paso, TX", "Detroit, MI", "Nashville, TN", "Portland, OR",
            "Memphis, TN", "Oklahoma City, OK", "Las Vegas, NV", "Louisville, KY", "Baltimore, MD"
        ]
        
        self.investment_goals = [
            "Retirement Planning", "Wealth Preservation", "Growth", "Income Generation",
            "Education Funding", "Estate Planning", "Tax Minimization", "Capital Appreciation",
            "Liquidity Preservation", "Risk Mitigation"
        ]
        
        self.risk_tolerances = ["Conservative", "Moderate Conservative", "Moderate", "Moderate Aggressive", "Aggressive"]
        
    def generate_clients(self, count: int = 1000) -> List[Dict[str, Any]]:
        """Generate realistic client profiles"""
        
        clients = []
        
        for i in range(count):
            client_id = f"WM{str(i+1).zfill(6)}"
            
            # Demographics
            first_name = random.choice(self.first_names)
            last_name = random.choice(self.last_names)
            age = random.randint(25, 85)
            
            # Wealth tier based on age and random distribution
            if age < 35:
                wealth_tier = random.choices(
                    ["Emerging", "Growing", "Established"], 
                    weights=[0.6, 0.3, 0.1]
                )[0]
            elif age < 50:
                wealth_tier = random.choices(
                    ["Growing", "Established", "High Net Worth"], 
                    weights=[0.4, 0.4, 0.2]
                )[0]
            elif age < 65:
                wealth_tier = random.choices(
                    ["Established", "High Net Worth", "Ultra High Net Worth"], 
                    weights=[0.3, 0.5, 0.2]
                )[0]
            else:
                wealth_tier = random.choices(
                    ["High Net Worth", "Ultra High Net Worth"], 
                    weights=[0.7, 0.3]
                )[0]
            
            # Assets based on wealth tier
            if wealth_tier == "Emerging":
                total_assets = random.randint(50000, 250000)
            elif wealth_tier == "Growing":
                total_assets = random.randint(250000, 1000000)
            elif wealth_tier == "Established":
                total_assets = random.randint(1000000, 5000000)
            elif wealth_tier == "High Net Worth":
                total_assets = random.randint(5000000, 25000000)
            else:  # Ultra High Net Worth
                total_assets = random.randint(25000000, 100000000)
            
            client = {
                "client_id": client_id,
                "first_name": first_name,
                "last_name": last_name,
                "full_name": f"{first_name} {last_name}",
                "age": age,
                "location": random.choice(self.cities),
                "wealth_tier": wealth_tier,
                "total_assets": total_assets,
                "risk_tolerance": random.choice(self.risk_tolerances),
                "primary_goal": random.choice(self.investment_goals),
                "secondary_goals": random.sample(self.investment_goals, random.randint(1, 3)),
                "onboarding_date": self._random_date(365*5),  # Within last 5 years
                "last_review_date": self._random_date(90),    # Within last 90 days
                "advisor_id": f"ADV{random.randint(1, 50):03d}",
                "relationship_manager_id": f"RM{random.randint(1, 25):03d}",
                "status": random.choices(
                    ["Active", "Prospect", "Inactive"], 
                    weights=[0.85, 0.10, 0.05]
                )[0],
                "kyc_completed": random.choice([True, False]),
                "accredited_investor": total_assets > 1000000,
                "contact_preferences": {
                    "email": True,
                    "phone": random.choice([True, False]),
                    "text": random.choice([True, False]),
                    "mail": random.choice([True, False])
                },
                "family_office": total_assets > 50000000
            }
            
            clients.append(client)
        
        self.client_data = clients
        return clients
    
    def generate_portfolios(self) -> List[Dict[str, Any]]:
        """Generate portfolio allocations for each client"""
        
        portfolios = []
        
        for client in self.client_data:
            portfolio_id = f"PF{client['client_id'][2:]}"
            
            # Determine allocation strategy based on risk tolerance and age
            if client['risk_tolerance'] == 'Conservative':
                equity_pct = max(0.2, 0.8 - (client['age'] - 30) * 0.01)
            elif client['risk_tolerance'] == 'Moderate Conservative':
                equity_pct = max(0.3, 0.9 - (client['age'] - 30) * 0.01)
            elif client['risk_tolerance'] == 'Moderate':
                equity_pct = max(0.4, 1.0 - (client['age'] - 30) * 0.01)
            elif client['risk_tolerance'] == 'Moderate Aggressive':
                equity_pct = max(0.5, 1.1 - (client['age'] - 30) * 0.01)
            else:  # Aggressive
                equity_pct = max(0.6, 1.2 - (client['age'] - 30) * 0.01)
            
            equity_pct = min(0.95, equity_pct)  # Cap at 95%
            bond_pct = max(0.05, 1.0 - equity_pct)
            
            # Generate holdings
            holdings = []
            remaining_value = client['total_assets']
            
            # Allocate to major asset classes
            equity_value = remaining_value * equity_pct
            bond_value = remaining_value * bond_pct
            
            # Generate equity holdings
            equity_securities = [s for s in self.securities if s['type'] in ['equity', 'etf'] and s['sector'] != 'Bonds']
            num_equity_holdings = min(random.randint(5, 15), len(equity_securities))
            selected_equities = random.sample(equity_securities, num_equity_holdings)
            
            equity_weights = np.random.dirichlet(np.ones(num_equity_holdings))
            
            for i, security in enumerate(selected_equities):
                holding_value = equity_value * equity_weights[i]
                shares = holding_value / security['price']
                
                holdings.append({
                    "security_id": security['symbol'],
                    "security_name": security['name'],
                    "security_type": security['type'],
                    "sector": security['sector'],
                    "shares": round(shares, 2),
                    "price": security['price'],
                    "market_value": round(holding_value, 2),
                    "weight": round(equity_weights[i] * equity_pct, 4),
                    "purchase_date": self._random_date(365*2)
                })
            
            # Generate bond holdings
            bond_securities = [s for s in self.securities if s['type'] == 'bond' or s['sector'] == 'Bonds']
            num_bond_holdings = min(random.randint(2, 5), len(bond_securities))
            selected_bonds = random.sample(bond_securities, num_bond_holdings)
            
            bond_weights = np.random.dirichlet(np.ones(num_bond_holdings))
            
            for i, security in enumerate(selected_bonds):
                holding_value = bond_value * bond_weights[i]
                shares = holding_value / security['price']
                
                holdings.append({
                    "security_id": security['symbol'],
                    "security_name": security['name'],
                    "security_type": security['type'],
                    "sector": security['sector'],
                    "shares": round(shares, 2),
                    "price": security['price'],
                    "market_value": round(holding_value, 2),
                    "weight": round(bond_weights[i] * bond_pct, 4),
                    "purchase_date": self._random_date(365*2)
                })
            
            # Add cash position
            cash_pct = random.uniform(0.02, 0.08)
            cash_value = remaining_value * cash_pct
            
            holdings.append({
                "security_id": "CASH",
                "security_name": "Cash and Cash Equivalents",
                "security_type": "cash",
                "sector": "Cash",
                "shares": 1,
                "price": cash_value,
                "market_value": cash_value,
                "weight": cash_pct,
                "purchase_date": datetime.now().strftime('%Y-%m-%d')
            })
            
            # Performance metrics
            ytd_return = random.uniform(-0.15, 0.25)
            one_year_return = random.uniform(-0.20, 0.30)
            three_year_return = random.uniform(-0.05, 0.15)
            
            portfolio = {
                "portfolio_id": portfolio_id,
                "client_id": client['client_id'],
                "portfolio_type": random.choice(["Taxable", "IRA", "401k", "Trust", "Joint"]),
                "total_value": client['total_assets'],
                "cash_value": cash_value,
                "equity_allocation": equity_pct,
                "bond_allocation": bond_pct,
                "cash_allocation": cash_pct,
                "holdings": holdings,
                "performance": {
                    "ytd_return": round(ytd_return, 4),
                    "one_year_return": round(one_year_return, 4),
                    "three_year_return": round(three_year_return, 4),
                    "inception_return": round(random.uniform(0.05, 0.12), 4)
                },
                "risk_metrics": {
                    "beta": round(random.uniform(0.6, 1.2), 2),
                    "standard_deviation": round(random.uniform(0.08, 0.18), 4),
                    "sharpe_ratio": round(random.uniform(0.5, 1.5), 2),
                    "max_drawdown": round(random.uniform(-0.25, -0.05), 4)
                },
                "last_rebalance_date": self._random_date(180),
                "next_rebalance_date": self._future_date(90)
            }
            
            portfolios.append(portfolio)
        
        self.portfolio_data = portfolios
        return portfolios
    
    def generate_relationships(self) -> List[Dict[str, Any]]:
        """Generate advisor-client relationships and team structures"""
        
        relationships = []
        
        # Generate advisor data
        advisors = {}
        for i in range(1, 51):
            advisor_id = f"ADV{i:03d}"
            advisors[advisor_id] = {
                "advisor_id": advisor_id,
                "first_name": random.choice(self.first_names),
                "last_name": random.choice(self.last_names),
                "years_experience": random.randint(3, 30),
                "specialization": random.choice([
                    "Retirement Planning", "Estate Planning", "Tax Planning", "Investment Management",
                    "Risk Management", "Family Office", "Corporate Benefits", "Alternative Investments"
                ]),
                "credentials": random.sample([
                    "CFP", "CFA", "ChFC", "CLU", "CIMA", "CPWA", "CPA", "JD"
                ], random.randint(1, 3)),
                "location": random.choice(self.cities),
                "client_capacity": random.randint(80, 150),
                "assets_under_management": 0  # Will calculate
            }
        
        # Generate relationship managers
        relationship_managers = {}
        for i in range(1, 26):
            rm_id = f"RM{i:03d}"
            relationship_managers[rm_id] = {
                "rm_id": rm_id,
                "first_name": random.choice(self.first_names),
                "last_name": random.choice(self.last_names),
                "years_experience": random.randint(5, 25),
                "territory": random.choice([
                    "Northeast", "Southeast", "Midwest", "Southwest", "West Coast", "Northwest"
                ]),
                "advisor_count": 0  # Will calculate
            }
        
        # Create client-advisor relationships
        for client in self.client_data:
            advisor = advisors[client['advisor_id']]
            rm = relationship_managers[client['relationship_manager_id']]
            
            # Update AUM
            advisor['assets_under_management'] += client['total_assets']
            
            relationship = {
                "client_id": client['client_id'],
                "advisor_id": client['advisor_id'],
                "rm_id": client['relationship_manager_id'],
                "relationship_start_date": client['onboarding_date'],
                "relationship_type": random.choice([
                    "Primary", "Joint", "Trust", "Corporate", "Family Office"
                ]),
                "service_model": random.choice([
                    "Full Service", "Advisory Only", "Discretionary", "Non-Discretionary"
                ]),
                "fee_structure": random.choice([
                    "Asset Based", "Hourly", "Project Based", "Retainer", "Performance Based"
                ]),
                "annual_fee": client['total_assets'] * random.uniform(0.005, 0.015),
                "meeting_frequency": random.choice([
                    "Monthly", "Quarterly", "Semi-Annual", "Annual", "As Needed"
                ]),
                "last_contact_date": self._random_date(30),
                "next_scheduled_contact": self._future_date(random.randint(30, 90)),
                "satisfaction_score": random.randint(7, 10),
                "referral_source": random.choice([
                    "Referral", "Cold Call", "Website", "Event", "Advertising", "Social Media"
                ])
            }
            
            relationships.append(relationship)
        
        # Calculate advisor counts for RMs
        for relationship in relationships:
            rm = relationship_managers[relationship['rm_id']]
            if relationship['advisor_id'] not in [r['advisor_id'] for r in relationships if r['rm_id'] == relationship['rm_id']][:rm['advisor_count']]:
                rm['advisor_count'] += 1
        
        # Store advisor and RM data
        self.advisor_data = list(advisors.values())
        self.rm_data = list(relationship_managers.values())
        self.relationship_data = relationships
        
        return relationships
    
    def generate_market_data(self) -> List[Dict[str, Any]]:
        """Generate market scenarios and events"""
        
        scenarios = []
        
        # Market volatility scenarios
        for i in range(50):
            scenario = {
                "scenario_id": f"MKT{i+1:03d}",
                "event_type": "market_volatility",
                "date": self._random_date(365),
                "severity": random.choice(["Low", "Medium", "High", "Extreme"]),
                "vix_level": random.uniform(12, 45),
                "market_decline": random.uniform(0, 0.25),
                "duration_days": random.randint(1, 30),
                "sectors_affected": random.sample([
                    "Technology", "Financial", "Healthcare", "Consumer Discretionary",
                    "Energy", "Materials", "Industrials", "Utilities", "Real Estate"
                ], random.randint(2, 6)),
                "client_impact_count": random.randint(50, 800),
                "advisor_actions_required": random.choice([True, False]),
                "communication_sent": random.choice([True, False])
            }
            scenarios.append(scenario)
        
        # Regulatory events
        for i in range(20):
            scenario = {
                "scenario_id": f"REG{i+1:03d}",
                "event_type": "regulatory_change",
                "date": self._random_date(730),
                "regulation": random.choice([
                    "DOL Fiduciary Rule", "SEC Best Interest", "State Regulations",
                    "Tax Law Changes", "Reporting Requirements"
                ]),
                "impact_level": random.choice(["Low", "Medium", "High"]),
                "compliance_deadline": self._future_date(random.randint(30, 365)),
                "affected_accounts": random.randint(100, 1000),
                "training_required": random.choice([True, False]),
                "system_changes_needed": random.choice([True, False])
            }
            scenarios.append(scenario)
        
        self.market_data = scenarios
        return scenarios
    
    def generate_transactions(self, days: int = 30) -> List[Dict[str, Any]]:
        """Generate transaction history"""
        
        transactions = []
        
        for _ in range(random.randint(500, 2000)):  # Generate 500-2000 transactions
            client = random.choice(self.client_data)
            portfolio = next((p for p in self.portfolio_data if p['client_id'] == client['client_id']), None)
            
            if not portfolio:
                continue
                
            holding = random.choice(portfolio['holdings'])
            
            transaction = {
                "transaction_id": str(uuid.uuid4()),
                "client_id": client['client_id'],
                "portfolio_id": portfolio['portfolio_id'],
                "security_id": holding['security_id'],
                "transaction_type": random.choices([
                    "Buy", "Sell", "Dividend", "Interest", "Fee", "Transfer"
                ], weights=[0.3, 0.2, 0.2, 0.1, 0.1, 0.1])[0],
                "transaction_date": self._random_date(days),
                "shares": round(random.uniform(1, 100), 2) if holding['security_id'] != 'CASH' else 1,
                "price": holding['price'] * random.uniform(0.95, 1.05),
                "amount": 0,  # Will calculate
                "fee": random.uniform(0, 25) if random.random() < 0.3 else 0,
                "advisor_id": client['advisor_id'],
                "trade_reason": random.choice([
                    "Rebalancing", "Client Request", "Market Opportunity", "Risk Management",
                    "Income Distribution", "Tax Loss Harvesting", "Asset Allocation"
                ]),
                "execution_venue": random.choice([
                    "NYSE", "NASDAQ", "Internal", "Third Party", "Dark Pool"
                ])
            }
            
            # Calculate amount
            if transaction['transaction_type'] in ['Buy', 'Sell']:
                transaction['amount'] = transaction['shares'] * transaction['price']
                if transaction['transaction_type'] == 'Sell':
                    transaction['amount'] *= -1
            elif transaction['transaction_type'] in ['Dividend', 'Interest']:
                transaction['amount'] = random.uniform(50, 1000)
            elif transaction['transaction_type'] == 'Fee':
                transaction['amount'] = -random.uniform(10, 100)
            else:  # Transfer
                transaction['amount'] = random.uniform(1000, 50000) * random.choice([1, -1])
            
            transactions.append(transaction)
        
        self.transaction_data = transactions
        return transactions
    
    def _random_date(self, days_back: int) -> str:
        """Generate random date within specified days back"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        random_date = start_date + timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds()))
        )
        return random_date.strftime('%Y-%m-%d')
    
    def _future_date(self, days_forward: int) -> str:
        """Generate future date within specified days forward"""
        start_date = datetime.now()
        future_date = start_date + timedelta(days=random.randint(1, days_forward))
        return future_date.strftime('%Y-%m-%d')
    
    def save_datasets(self, output_dir: str = "datasets"):
        """Save all generated datasets to JSON files"""
        import os
        
        os.makedirs(output_dir, exist_ok=True)
        
        datasets = {
            "clients": self.client_data,
            "portfolios": self.portfolio_data,
            "relationships": self.relationship_data,
            "advisors": getattr(self, 'advisor_data', []),
            "relationship_managers": getattr(self, 'rm_data', []),
            "market_scenarios": self.market_data,
            "transactions": self.transaction_data
        }
        
        for name, data in datasets.items():
            filepath = os.path.join(output_dir, f"{name}.json")
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        
        # Generate summary
        summary = {
            "generation_date": datetime.now().isoformat(),
            "total_clients": len(self.client_data),
            "total_portfolios": len(self.portfolio_data),
            "total_advisors": len(getattr(self, 'advisor_data', [])),
            "total_rms": len(getattr(self, 'rm_data', [])),
            "total_relationships": len(self.relationship_data),
            "total_transactions": len(self.transaction_data),
            "total_market_scenarios": len(self.market_data),
            "total_assets_under_management": sum(c['total_assets'] for c in self.client_data),
            "wealth_tier_distribution": self._calculate_wealth_distribution(),
            "risk_tolerance_distribution": self._calculate_risk_distribution()
        }
        
        with open(os.path.join(output_dir, "summary.json"), 'w') as f:
            json.dump(summary, f, indent=2)
            
        return summary
    
    def _calculate_wealth_distribution(self) -> Dict[str, int]:
        """Calculate distribution of clients by wealth tier"""
        distribution = {}
        for client in self.client_data:
            tier = client['wealth_tier']
            distribution[tier] = distribution.get(tier, 0) + 1
        return distribution
    
    def _calculate_risk_distribution(self) -> Dict[str, int]:
        """Calculate distribution of clients by risk tolerance"""
        distribution = {}
        for client in self.client_data:
            risk = client['risk_tolerance']
            distribution[risk] = distribution.get(risk, 0) + 1
        return distribution

def generate_complete_dataset(client_count: int = 1000) -> Dict[str, Any]:
    """Generate complete wealth management dataset"""
    
    generator = WealthDatasetGenerator()
    
    print(f"Generating {client_count} clients...")
    clients = generator.generate_clients(client_count)
    
    print("Generating portfolios...")
    portfolios = generator.generate_portfolios()
    
    print("Generating relationships...")
    relationships = generator.generate_relationships()
    
    print("Generating market scenarios...")
    market_data = generator.generate_market_data()
    
    print("Generating transactions...")
    transactions = generator.generate_transactions(90)  # 90 days of transactions
    
    print("Saving datasets...")
    summary = generator.save_datasets()
    
    print(f"\n✅ Dataset Generation Complete!")
    print(f"📊 Total Clients: {summary['total_clients']:,}")
    print(f"💰 Total AUM: ${summary['total_assets_under_management']:,}")
    print(f"📈 Portfolios: {summary['total_portfolios']:,}")
    print(f"🤝 Relationships: {summary['total_relationships']:,}")
    print(f"💼 Transactions: {summary['total_transactions']:,}")
    
    return summary

if __name__ == "__main__":
    generate_complete_dataset(1200)  # Generate 1200 clients for extra data