#!/usr/bin/env python3
"""
Comprehensive demo of the new Budget Advice and Purchase Planning features
This demonstrates the exact functionality requested in the user prompt.
"""

from core.bot_core import FinancialBotCore
import os

def demo_budgeting_advice():
    """Demo the budgeting advice functionality with example from user prompt"""
    print("🏦 " + "="*50)
    print("   BUDGETING ADVICE DEMONSTRATION")
    print("="*52)
    
    # Setup
    test_db = "demo_budget.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    bot = FinancialBotCore(test_db)
    user_id = "user_demo"
    username = "DemoUser"
    
    # Add the financial data to match the example
    print("\n📊 Setting up financial data...")
    bot.process_message(user_id, username, "Saya dapat gaji 6250000 dari kantor")
    bot.process_message(user_id, username, "Habis 4500000 untuk pengeluaran bulanan")
    
    print("\n🤖 User: Help me create a budget")
    print("MoGre Financial Assistant:", end=" ")
    response = bot.process_message(user_id, username, "Help me create a budget")
    print(response)
    
    # Cleanup
    if os.path.exists(test_db):
        os.remove(test_db)

def demo_purchase_planning():
    """Demo the purchase planning functionality with example from user prompt"""
    print("\n🚗 " + "="*50)
    print("   PURCHASE PLANNING DEMONSTRATION")
    print("="*52)
    
    # Setup
    test_db = "demo_purchase.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    bot = FinancialBotCore(test_db)
    user_id = "user_demo"
    username = "DemoUser"
    
    # Add financial data including some debt
    print("\n📊 Setting up financial data with existing debt...")
    bot.process_message(user_id, username, "Saya dapat gaji 6250000 dari kantor")
    bot.process_message(user_id, username, "Habis 4500000 untuk pengeluaran bulanan")
    bot.process_message(user_id, username, "Bayar 25000000 untuk cicilan rumah")
    bot.process_message(user_id, username, "Bayar 45000000 untuk hutang kredit")
    
    print("\n🤖 User: I want to buy a $30000 car")
    print("MoGre Financial Assistant:", end=" ")
    response = bot.process_message(user_id, username, "I want to buy a car 30000000")
    print(response)
    
    # Cleanup
    if os.path.exists(test_db):
        os.remove(test_db)

def demo_additional_features():
    """Demo additional variations of the new features"""
    print("\n🔧 " + "="*50)
    print("   ADDITIONAL FEATURE VARIATIONS")
    print("="*52)
    
    # Setup
    test_db = "demo_additional.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    bot = FinancialBotCore(test_db)
    user_id = "user_demo"
    username = "DemoUser"
    
    # Add some basic financial data
    bot.process_message(user_id, username, "income 5000000 gaji")
    bot.process_message(user_id, username, "expense 3000000 pengeluaran")
    
    print("\n1. Indonesian Budget Request:")
    print("🤖 User: bantuan budget saya")
    response = bot.process_message(user_id, username, "bantuan budget saya")
    print("Response:", response[:200] + "..." if len(response) > 200 else response)
    
    print("\n2. Indonesian Purchase Planning:")
    print("🤖 User: saya mau beli laptop 15000000")
    response = bot.process_message(user_id, username, "saya mau beli laptop 15000000")
    print("Response:", response[:200] + "..." if len(response) > 200 else response)
    
    print("\n3. Expensive Purchase Analysis:")
    print("🤖 User: I want to buy a house 500000000")
    response = bot.process_message(user_id, username, "I want to buy a house 500000000")
    print("Response:", response[:300] + "..." if len(response) > 300 else response)
    
    # Cleanup
    if os.path.exists(test_db):
        os.remove(test_db)

def main():
    """Run the complete demonstration"""
    print("🎯 MOGRE FINANCIAL ASSISTANT - NEW FEATURES DEMO")
    print("Demonstrating Budget Advice and Purchase Planning Analysis")
    print("Based on user requirements with regex pattern recognition")
    
    demo_budgeting_advice()
    demo_purchase_planning()
    demo_additional_features()
    
    print("\n✅ " + "="*50)
    print("   DEMONSTRATION COMPLETE")
    print("="*52)
    print("\n🎉 New features successfully implemented:")
    print("   ✓ Budget Advice with 50/30/20 allocation recommendations")
    print("   ✓ Purchase Planning Analysis with debt consideration")
    print("   ✓ Multi-language support (Indonesian & English)")
    print("   ✓ Smart regex pattern matching")
    print("   ✓ Integration with existing database system")
    print("   ✓ Comprehensive financial recommendations")

if __name__ == "__main__":
    main()
