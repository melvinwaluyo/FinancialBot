# Financial Bot CLI Runner
# Script untuk menjalankan bot dalam mode CLI untuk testing

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.bot_core import FinancialBotCore

def main():
    """CLI interface untuk testing bot tanpa Discord"""
    print("🤖 Financial Bot CLI Mode")
    print("="*40)
    print("Ketik 'exit' atau 'quit' untuk keluar")
    print("Ketik '!help' untuk melihat bantuan")
    print("="*40)
    
    # Initialize bot core
    bot_core = FinancialBotCore("financial_bot_cli.db")
    
    # Simulate user
    user_id = "cli_user"
    username = "CLI_User"
    
    try:
        while True:
            # Get user input
            user_input = input("\n👤 Anda: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("👋 Sampai jumpa!")
                break
            
            if not user_input:
                continue
            
            # Process message
            response = bot_core.process_message(user_id, username, user_input)
            
            # Display response
            print(f"🤖 Bot: {response}")
    
    except KeyboardInterrupt:
        print("\n\n👋 Sampai jumpa!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
