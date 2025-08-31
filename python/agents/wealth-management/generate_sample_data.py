#!/usr/bin/env python3
"""Generate sample client IDs and basic data for testing"""

from wealth_management.data.dataset_generator import WealthDatasetGenerator

def generate_sample_clients():
    """Generate a small sample of clients for testing"""
    
    generator = WealthDatasetGenerator()
    
    # Generate 50 sample clients
    print("🎯 Generating 50 sample clients...")
    clients = generator.generate_clients(50)
    
    print("\n📋 Sample Client IDs and Info:")
    print("=" * 60)
    
    for i, client in enumerate(clients[:20]):  # Show first 20
        print(f"{client['client_id']:>8} | {client['first_name']} {client['last_name']:12} | {client['wealth_tier']:12} | ${client['total_assets']:>12,}")
    
    if len(clients) > 20:
        print(f"... and {len(clients) - 20} more clients")
    
    print("\n" + "=" * 60)
    print("💡 You can use any of these client IDs in your queries:")
    print("   Examples:")
    for client in clients[:10]:
        print(f"   • 'Show portfolio for client {client['client_id']}'")
    
    # Show wealth tier distribution
    wealth_tiers = {}
    for client in clients:
        tier = client['wealth_tier']
        wealth_tiers[tier] = wealth_tiers.get(tier, 0) + 1
    
    print(f"\n📊 Wealth Tier Distribution:")
    for tier, count in wealth_tiers.items():
        print(f"   {tier:15}: {count:2d} clients")
    
    return clients

if __name__ == "__main__":
    clients = generate_sample_clients()
    print(f"\n🎉 Generated {len(clients)} sample clients for testing!")