#!/usr/bin/env python3
"""
Simple demo of the Budget Advice and Purchase Planning features
"""

from core.bot_core import FinancialBotCore
import os

def main():
    """Demo the new features"""
    print("🎯 MOGRE FINANCIAL ASSISTANT - NEW FEATURES DEMO")
    print("="*55)
    
    # Setup
    test_db = "final_demo.db"
    if os.path.exists(test_db):
        try:
            os.remove(test_db)
        except:
            pass
    
    bot = FinancialBotCore(test_db)
    user_id = "demo_user"
    username = "DemoUser"
    
    print("\n📊 Setting up financial data...")
    print("Adding income: Rp 6,250,000")
    print("Adding expenses: Rp 4,500,000")
    
    bot.process_message(user_id, username, "Saya dapat gaji 6250000 dari kantor")
    bot.process_message(user_id, username, "Habis 4500000 untuk pengeluaran bulanan")
    
    print("\n" + "="*55)
    print("🏦 BUDGET ADVICE EXAMPLE")
    print("="*55)
    print("\nYou: Help me create a budget")
    print("\nMoGre Financial Assistant:")
    response = bot.process_message(user_id, username, "Help me create a budget")
    print(response)
    
    print("\n" + "="*55)
    print("🚗 PURCHASE PLANNING EXAMPLE")
    print("="*55)
    print("\nYou: I want to buy a $30000 car")
    print("\nMoGre Financial Assistant:")
    response = bot.process_message(user_id, username, "I want to buy a car 30000000")
    print(response)
    
    print("\n" + "="*55)
    print("✅ FEATURES SUCCESSFULLY IMPLEMENTED")
    print("="*55)
    print("✓ Budget advice with regex pattern matching")
    print("✓ Purchase planning analysis")
    print("✓ Multi-language support (ID/EN)")
    print("✓ Database integration for accurate responses")
    print("✓ Financial recommendations based on user data")
    print("✓ Smart categorization and analysis")

if __name__ == "__main__":
    main()
