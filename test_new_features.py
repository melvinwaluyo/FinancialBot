#!/usr/bin/env python3
"""
Test script for new budget advice and purchase planning features
"""

from core.bot_core import FinancialBotCore
from core.database import DatabaseManager
import os

def test_new_features():
    # Use test database
    test_db = "test_new_features.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    bot = FinancialBotCore(test_db)
    user_id = "test_user_123"
    username = "TestUser"
    
    print("🧪 Testing New Financial Bot Features")
    print("=" * 50)
    
    # Step 1: Add some financial data
    print("\n📊 Step 1: Adding financial data...")
    
    # Add income
    response = bot.process_message(user_id, username, "Saya dapat gaji 6250000 dari kantor")
    print(f"Income: {response}")
    
    # Add expenses
    expenses = [
        "Habis 2000000 untuk tagihan rumah",
        "Keluar 500000 untuk makanan",
        "Bayar 300000 transport",
        "Habis 200000 hiburan", 
        "Belanja baju 1500000"
    ]
    
    for expense in expenses:
        response = bot.process_message(user_id, username, expense)
        print(f"Expense: {response}")
    
    # Step 2: Test budget advice
    print("\n💰 Step 2: Testing Budget Advice...")
    budget_commands = [
        "Help me create a budget",
        "bantuan budget saya",
        "buatkan budget"
    ]
    
    for cmd in budget_commands:
        print(f"\nCommand: {cmd}")
        response = bot.process_message(user_id, username, cmd)
        print(f"Response: {response}")
        print("-" * 40)
    
    # Step 3: Test purchase planning
    print("\n🛍️ Step 3: Testing Purchase Planning...")
    purchase_commands = [
        "I want to buy a 30000000 car",
        "saya mau beli laptop 15000000",
        "I want to buy a house 500000000"
    ]
    
    for cmd in purchase_commands:
        print(f"\nCommand: {cmd}")
        response = bot.process_message(user_id, username, cmd)
        print(f"Response: {response}")
        print("-" * 40)
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    test_new_features()
