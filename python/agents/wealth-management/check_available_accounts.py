#!/usr/bin/env python3
"""Check what accounts are actually available in the mock APIs"""

from wealth_management.mock_apis import MockCustodianAPI

def check_available_accounts():
    """Check what accounts exist in the MockCustodianAPI"""
    
    api = MockCustodianAPI()
    
    print("🔍 Checking Available Accounts in MockCustodianAPI...")
    print("=" * 60)
    
    # Get all account IDs
    account_ids = list(api._accounts.keys())
    account_ids.sort()
    
    print(f"📊 Found {len(account_ids)} accounts:")
    print()
    
    for account_id in account_ids:
        account = api._accounts[account_id]
        positions = api._positions.get(account_id, [])
        total_value = sum(pos.market_value for pos in positions) if positions else 0
        
        print(f"🏦 {account_id:<12} | {account['account_type']:<12} | ${float(account['cash_balance']):>10,.0f} cash | ${float(total_value):>12,.0f} total")
    
    print("\n" + "=" * 60)
    print("💡 Use these account IDs in your queries:")
    for account_id in account_ids[:10]:  # Show first 10
        print(f"   • 'Show portfolio for {account_id}'")
    
    return account_ids

if __name__ == "__main__":
    accounts = check_available_accounts()
    print(f"\n🎉 Found {len(accounts)} working accounts!")