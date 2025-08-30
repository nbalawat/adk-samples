"""Mock CRM API for client relationship management"""

import os
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from .base_api import BaseMockAPI, APIResponse

class ClientType(Enum):
    INDIVIDUAL = "INDIVIDUAL"
    JOINT = "JOINT"
    CORPORATE = "CORPORATE"
    TRUST = "TRUST"

class RiskTolerance(Enum):
    CONSERVATIVE = "CONSERVATIVE"
    MODERATE = "MODERATE"
    AGGRESSIVE = "AGGRESSIVE"

@dataclass
class Client:
    """Client information structure"""
    client_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    client_type: ClientType
    risk_tolerance: RiskTolerance
    net_worth: float
    investment_goals: List[str]
    advisor_id: str
    created_date: datetime
    last_contact_date: datetime
    notes: str

class MockCRMAPI(BaseMockAPI):
    """Mock CRM API for client relationship management"""
    
    def __init__(self):
        super().__init__("crm_api")
        
        # Initialize mock client data
        self._clients = {}
        self._advisors = {}
        self._interactions = {}
        self._initialize_mock_data()
    
    def _initialize_mock_data(self):
        """Initialize mock client and advisor data"""
        # Create mock advisors
        advisor_names = [
            ("John", "Smith"), ("Sarah", "Johnson"), ("Michael", "Brown"),
            ("Lisa", "Davis"), ("Robert", "Wilson"), ("Emily", "Taylor")
        ]
        
        for i, (first, last) in enumerate(advisor_names, 1):
            advisor_id = f"ADV{str(i).zfill(4)}"
            self._advisors[advisor_id] = {
                "advisor_id": advisor_id,
                "first_name": first,
                "last_name": last,
                "email": f"{first.lower()}.{last.lower()}@wealthfirm.com",
                "phone": f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                "specialties": random.sample([
                    "Retirement Planning", "Estate Planning", "Tax Planning",
                    "Investment Management", "Insurance Planning", "Education Planning"
                ], k=random.randint(2, 4)),
                "clients_count": 0,
                "assets_under_management": 0.0
            }
        
        # Create mock clients
        first_names = ["Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona", "George", "Helen"]
        last_names = ["Anderson", "Baker", "Clark", "Davis", "Evans", "Foster", "Green", "Harris"]
        
        for i in range(50):
            client_id = f"CLI{str(i + 10001).zfill(5)}"
            first = random.choice(first_names)
            last = random.choice(last_names)
            advisor_id = random.choice(list(self._advisors.keys()))
            
            client = Client(
                client_id=client_id,
                first_name=first,
                last_name=last,
                email=f"{first.lower()}.{last.lower()}@email.com",
                phone=f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                client_type=random.choice(list(ClientType)),
                risk_tolerance=random.choice(list(RiskTolerance)),
                net_worth=random.uniform(100000, 10000000),
                investment_goals=random.sample([
                    "Retirement", "Education", "Home Purchase", "Wealth Preservation",
                    "Tax Optimization", "Estate Planning", "Income Generation"
                ], k=random.randint(1, 3)),
                advisor_id=advisor_id,
                created_date=datetime.utcnow() - timedelta(days=random.randint(30, 1000)),
                last_contact_date=datetime.utcnow() - timedelta(days=random.randint(1, 90)),
                notes=f"Client since {datetime.utcnow().year - random.randint(1, 5)}"
            )
            
            self._clients[client_id] = client
            self._advisors[advisor_id]["clients_count"] += 1
            self._advisors[advisor_id]["assets_under_management"] += client.net_worth * 0.7  # 70% AUM ratio
    
    def get_client(self, client_id: str) -> APIResponse:
        """Get client information"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error=f"Failed to fetch client {client_id}")
        
        if client_id not in self._clients:
            return self._create_response(error=f"Client {client_id} not found")
        
        client = self._clients[client_id]
        
        return self._create_response(data={
            "client_id": client.client_id,
            "first_name": client.first_name,
            "last_name": client.last_name,
            "email": client.email,
            "phone": client.phone,
            "client_type": client.client_type.value,
            "risk_tolerance": client.risk_tolerance.value,
            "net_worth": client.net_worth,
            "investment_goals": client.investment_goals,
            "advisor_id": client.advisor_id,
            "created_date": client.created_date.isoformat(),
            "last_contact_date": client.last_contact_date.isoformat(),
            "notes": client.notes
        })
    
    def get_advisor_clients(self, advisor_id: str) -> APIResponse:
        """Get all clients for an advisor"""
        self._simulate_network_delay()
        
        if advisor_id not in self._advisors:
            return self._create_response(error=f"Advisor {advisor_id} not found")
        
        advisor_clients = [
            client for client in self._clients.values()
            if client.advisor_id == advisor_id
        ]
        
        clients_data = []
        for client in advisor_clients:
            clients_data.append({
                "client_id": client.client_id,
                "first_name": client.first_name,
                "last_name": client.last_name,
                "email": client.email,
                "client_type": client.client_type.value,
                "risk_tolerance": client.risk_tolerance.value,
                "net_worth": client.net_worth,
                "last_contact_date": client.last_contact_date.isoformat()
            })
        
        return self._create_response(data={
            "advisor_id": advisor_id,
            "clients": clients_data,
            "total_clients": len(clients_data),
            "total_aum": sum(client.net_worth * 0.7 for client in advisor_clients)
        })
    
    def update_client(self, client_id: str, update_data: Dict[str, Any]) -> APIResponse:
        """Update client information"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error=f"Failed to update client {client_id}")
        
        if client_id not in self._clients:
            return self._create_response(error=f"Client {client_id} not found")
        
        client = self._clients[client_id]
        
        # Update allowed fields
        updateable_fields = [
            "first_name", "last_name", "email", "phone", "risk_tolerance",
            "net_worth", "investment_goals", "notes"
        ]
        
        for field, value in update_data.items():
            if field in updateable_fields:
                if field == "risk_tolerance":
                    client.risk_tolerance = RiskTolerance(value)
                elif field == "investment_goals" and isinstance(value, list):
                    client.investment_goals = value
                else:
                    setattr(client, field, value)
        
        return self._create_response(data={
            "client_id": client_id,
            "status": "updated",
            "updated_fields": list(update_data.keys())
        })
    
    def create_client(self, client_data: Dict[str, Any]) -> APIResponse:
        """Create a new client"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error="Failed to create client")
        
        # Generate new client ID
        existing_ids = [int(cid[3:]) for cid in self._clients.keys()]
        new_id = max(existing_ids) + 1 if existing_ids else 10001
        client_id = f"CLI{str(new_id).zfill(5)}"
        
        # Create client object
        client = Client(
            client_id=client_id,
            first_name=client_data["first_name"],
            last_name=client_data["last_name"],
            email=client_data["email"],
            phone=client_data.get("phone", ""),
            client_type=ClientType(client_data.get("client_type", "INDIVIDUAL")),
            risk_tolerance=RiskTolerance(client_data.get("risk_tolerance", "MODERATE")),
            net_worth=client_data.get("net_worth", 0.0),
            investment_goals=client_data.get("investment_goals", []),
            advisor_id=client_data["advisor_id"],
            created_date=datetime.utcnow(),
            last_contact_date=datetime.utcnow(),
            notes=client_data.get("notes", "")
        )
        
        self._clients[client_id] = client
        
        # Update advisor client count
        if client.advisor_id in self._advisors:
            self._advisors[client.advisor_id]["clients_count"] += 1
            self._advisors[client.advisor_id]["assets_under_management"] += client.net_worth * 0.7
        
        return self._create_response(data={
            "client_id": client_id,
            "status": "created",
            "message": f"Client {client_id} created successfully"
        })
    
    def log_interaction(self, interaction_data: Dict[str, Any]) -> APIResponse:
        """Log a client interaction"""
        self._simulate_network_delay()
        
        client_id = interaction_data["client_id"]
        
        if client_id not in self._clients:
            return self._create_response(error=f"Client {client_id} not found")
        
        interaction_id = f"INT{datetime.utcnow().strftime('%Y%m%d')}{random.randint(1000, 9999)}"
        
        interaction = {
            "interaction_id": interaction_id,
            "client_id": client_id,
            "advisor_id": interaction_data.get("advisor_id", self._clients[client_id].advisor_id),
            "interaction_type": interaction_data.get("type", "MEETING"),
            "subject": interaction_data.get("subject", ""),
            "notes": interaction_data.get("notes", ""),
            "date": interaction_data.get("date", datetime.utcnow().isoformat()),
            "duration_minutes": interaction_data.get("duration_minutes", 30),
            "outcome": interaction_data.get("outcome", "")
        }
        
        if client_id not in self._interactions:
            self._interactions[client_id] = []
        
        self._interactions[client_id].append(interaction)
        
        # Update last contact date
        self._clients[client_id].last_contact_date = datetime.utcnow()
        
        return self._create_response(data={
            "interaction_id": interaction_id,
            "status": "logged",
            "message": "Interaction logged successfully"
        })
    
    def get_client_interactions(self, client_id: str, limit: int = 50) -> APIResponse:
        """Get client interaction history"""
        self._simulate_network_delay()
        
        if client_id not in self._clients:
            return self._create_response(error=f"Client {client_id} not found")
        
        interactions = self._interactions.get(client_id, [])
        
        # Sort by date (most recent first) and limit
        sorted_interactions = sorted(
            interactions, 
            key=lambda x: datetime.fromisoformat(x["date"]), 
            reverse=True
        )[:limit]
        
        return self._create_response(data={
            "client_id": client_id,
            "interactions": sorted_interactions,
            "total_count": len(interactions)
        })