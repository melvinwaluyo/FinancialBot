"""
Core bot logic untuk Financial Bot Discord
Menggabungkan rules engine, database, dan Discord integration
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
import discord
from discord.ext import commands

from .database import DatabaseManager
from .rules import FinancialRulesEngine

class FinancialBotCore:
    """Core logic untuk Financial Bot"""
    
    def __init__(self, db_path: str = "financial_bot.db"):
        self.db = DatabaseManager(db_path)
        self.rules_engine = FinancialRulesEngine()
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/bot.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('FinancialBot')
    
    def process_message(self, user_id: str, username: str, message: str) -> str:
        """Proses pesan dari user dan return response"""
        try:
            # Log incoming message
            self.logger.info(f"Processing message from {username} ({user_id}): {message}")
            
            # Parse command menggunakan rules engine
            command_result = self.rules_engine.parse_command(message)
            command_type = command_result.get('type')
            
            # Process berdasarkan tipe command
            if command_type == 'income':
                return self._handle_income(user_id, username, command_result)
            
            elif command_type == 'expense':
                return self._handle_expense(user_id, username, command_result)
            
            elif command_type == 'balance':
                return self._handle_balance(user_id, command_result)
            
            elif command_type == 'report':
                return self._handle_report(user_id, command_result)
            
            elif command_type == 'delete':
                return self._handle_delete(user_id, command_result)
            
            elif command_type == 'budget_advice':
                return self._handle_budget_advice(user_id, command_result)
            
            elif command_type == 'purchase_planning':
                return self._handle_purchase_planning(user_id, command_result)
            
            elif command_type == 'help':
                return self.rules_engine.generate_response(command_result)
            
            else:
                return self.rules_engine.generate_response(command_result)
        
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return "Maaf, terjadi kesalahan saat memproses perintah Anda. Silakan coba lagi."
    
    def _handle_income(self, user_id: str, username: str, command_result: Dict[str, Any]) -> str:
        """Handle perintah pemasukan"""
        amount = command_result['amount']
        category = command_result['category']
        description = command_result['description']
        
        if amount <= 0:
            return "❌ Jumlah pemasukan harus lebih dari 0."
        
        # Simpan ke database
        success = self.db.add_transaction(
            user_id=user_id,
            username=username,
            transaction_type='income',
            amount=amount,
            category=category,
            description=description
        )
        
        if success:
            self.logger.info(f"Income added: {username} - Rp {amount:,.0f} - {category}")
            
            # Get updated balance untuk response
            balance_info = self.db.get_user_balance(user_id)
            response = self.rules_engine.generate_response(command_result)
            response += f"\n💰 Saldo terbaru: Rp {balance_info['balance']:,.0f}"
            return response
        else:
            return "❌ Gagal menyimpan transaksi. Silakan coba lagi."
    
    def _handle_expense(self, user_id: str, username: str, command_result: Dict[str, Any]) -> str:
        """Handle perintah pengeluaran"""
        amount = command_result['amount']
        category = command_result['category']
        description = command_result['description']
        
        if amount <= 0:
            return "❌ Jumlah pengeluaran harus lebih dari 0."
        
        # Simpan ke database
        success = self.db.add_transaction(
            user_id=user_id,
            username=username,
            transaction_type='expense',
            amount=amount,
            category=category,
            description=description
        )
        
        if success:
            self.logger.info(f"Expense added: {username} - Rp {amount:,.0f} - {category}")
            
            # Get updated balance untuk response
            balance_info = self.db.get_user_balance(user_id)
            response = self.rules_engine.generate_response(command_result)
            response += f"\n💰 Saldo terbaru: Rp {balance_info['balance']:,.0f}"
            
            # Warning jika saldo negatif
            if balance_info['balance'] < 0:
                response += "\n⚠️ **Perhatian**: Saldo Anda sudah negatif!"
            
            return response
        else:
            return "❌ Gagal menyimpan transaksi. Silakan coba lagi."
    
    def _handle_balance(self, user_id: str, command_result: Dict[str, Any]) -> str:
        """Handle perintah saldo"""
        balance_info = self.db.get_user_balance(user_id)
        
        # Get recent transactions
        recent_transactions = self.db.get_user_transactions(user_id, limit=5)
        
        user_data = {
            'balance': balance_info,
            'recent_transactions': recent_transactions
        }
        
        response = self.rules_engine.generate_response(command_result, user_data)
        
        # Add recent transactions if available
        if recent_transactions:
            response += "\n\n📋 **5 Transaksi Terakhir:**"
            for idx, trans in enumerate(recent_transactions, 1):
                type_emoji = "💚" if trans['type'] == 'income' else "💸"
                response += f"\n{idx}. {type_emoji} Rp {trans['amount']:,.0f} - {trans['category']}"
                if trans['description']:
                    response += f" ({trans['description']})"
        
        return response
    
    def _handle_report(self, user_id: str, command_result: Dict[str, Any]) -> str:
        """Handle perintah laporan"""
        category_report = self.db.get_category_report(user_id)
        balance_info = self.db.get_user_balance(user_id)
        
        if not category_report:
            return "📊 Kamu belum memiliki transaksi untuk dilaporkan."
        
        response = "📊 **Laporan Keuangan per Kategori:**\n\n"
        
        # Summary
        response += f"💰 **Total Pemasukan**: Rp {balance_info['income']:,.0f}\n"
        response += f"💸 **Total Pengeluaran**: Rp {balance_info['expense']:,.0f}\n"
        response += f"📈 **Saldo**: Rp {balance_info['balance']:,.0f}\n\n"
        
        # Separate income and expense categories
        income_categories = {}
        expense_categories = {}
        
        for category, amounts in category_report.items():
            if amounts['income'] > 0:
                income_categories[category] = amounts['income']
            if amounts['expense'] > 0:
                expense_categories[category] = amounts['expense']
        
        # Display Income section
        if income_categories:
            response += "**💚 Pemasukan:**\n"
            # Sort by amount (highest first)
            sorted_income = sorted(income_categories.items(), key=lambda x: x[1], reverse=True)
            for category, amount in sorted_income:
                response += f"• {category.title()}: Rp {amount:,.0f}\n"
            response += "\n"
        
        # Display Expense section
        if expense_categories:
            response += "**💸 Pengeluaran:**\n"
            # Sort by amount (highest first)
            sorted_expense = sorted(expense_categories.items(), key=lambda x: x[1], reverse=True)
            for category, amount in sorted_expense:
                response += f"• {category.title()}: Rp {amount:,.0f}\n"
        
        return response
    
    def _handle_delete(self, user_id: str, command_result: Dict[str, Any]) -> str:
        """Handle perintah hapus transaksi"""
        transaction_id = command_result['transaction_id']
        
        # Get transaction details first untuk logging
        transactions = self.db.get_user_transactions(user_id, limit=100)
        target_transaction = None
        
        for trans in transactions:
            if trans['id'] == transaction_id:
                target_transaction = trans
                break
        
        if not target_transaction:
            return f"❌ Transaksi dengan ID {transaction_id} tidak ditemukan atau bukan milik Anda."
        
        # Delete transaction
        success = self.db.delete_transaction(user_id, transaction_id)
        
        if success:
            self.logger.info(f"Transaction deleted: {user_id} - ID {transaction_id}")
            return f"✅ Transaksi ID {transaction_id} berhasil dihapus."
        else:
            return f"❌ Gagal menghapus transaksi ID {transaction_id}."
    
    def _handle_budget_advice(self, user_id: str, command_result: Dict[str, Any]) -> str:
        """Handle budget advice request"""
        # Get comprehensive user financial data
        user_data = self._get_comprehensive_user_data(user_id)
        
        self.logger.info(f"Budget advice requested by {user_id}")
        return self.rules_engine.generate_response(command_result, user_data)
    
    def _handle_purchase_planning(self, user_id: str, command_result: Dict[str, Any]) -> str:
        """Handle purchase planning request"""
        # Get comprehensive user financial data
        user_data = self._get_comprehensive_user_data(user_id)
        
        item = command_result.get('item', 'item')
        price = command_result.get('price', 0)
        self.logger.info(f"Purchase planning requested by {user_id} for {item} at Rp {price:,.0f}")
        
        return self.rules_engine.generate_response(command_result, user_data)
    
    def _get_comprehensive_user_data(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user data for financial analysis"""
        balance_info = self.db.get_user_balance(user_id)
        recent_transactions = self.db.get_user_transactions(user_id, limit=50)
        category_report = self.db.get_category_report(user_id)
        
        # Calculate debt information from transactions
        debt_categories = ['tagihan', 'cicilan', 'hutang', 'debt', 'loan', 'credit']
        debt_transactions = []
        total_debt = 0
        
        for trans in recent_transactions:
            if trans['type'] == 'expense' and any(debt_cat in trans['category'].lower() or 
                                                  debt_cat in trans['description'].lower() 
                                                  for debt_cat in debt_categories):
                debt_transactions.append(trans)
                total_debt += trans['amount']
        
        # Estimate monthly income and expenses (using recent transaction patterns)
        monthly_income = 0
        monthly_expense = 0
        
        # Simple estimation: if we have transactions, estimate monthly based on recent data
        if recent_transactions:
            income_sum = sum(t['amount'] for t in recent_transactions if t['type'] == 'income')
            expense_sum = sum(t['amount'] for t in recent_transactions if t['type'] == 'expense')
            
            # If we have multiple transactions, try to estimate monthly values
            if len(recent_transactions) > 5:
                monthly_income = income_sum / max(1, len([t for t in recent_transactions if t['type'] == 'income'])) if income_sum > 0 else 0
                monthly_expense = expense_sum / max(1, len([t for t in recent_transactions if t['type'] == 'expense'])) if expense_sum > 0 else 0
            else:
                monthly_income = income_sum
                monthly_expense = expense_sum
        
        return {
            'balance': {
                'income': monthly_income or balance_info['income'],
                'expense': monthly_expense or balance_info['expense'],
                'balance': balance_info['balance']
            },
            'recent_transactions': recent_transactions,
            'category_report': category_report,
            'debt_info': {
                'debt_transactions': debt_transactions,
                'total_debt': total_debt
            },
            'transaction_count': len(recent_transactions)
        }
    
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get statistik lengkap user"""
        balance_info = self.db.get_user_balance(user_id)
        recent_transactions = self.db.get_user_transactions(user_id, limit=10)
        category_report = self.db.get_category_report(user_id)
        
        return {
            'balance': balance_info,
            'recent_transactions': recent_transactions,
            'category_report': category_report,
            'transaction_count': len(recent_transactions)
        }
