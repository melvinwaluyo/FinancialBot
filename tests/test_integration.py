"""
Integration tests untuk Bot Core
Testing end-to-end functionality
"""

import unittest
import os
import tempfile
import sys
import gc
import sqlite3

# Add parent directory to path untuk import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.bot_core import FinancialBotCore

class TestBotCoreIntegration(unittest.TestCase):
    """Test integrasi bot core dengan semua komponen"""
    
    def setUp(self):
        """Setup test environment"""
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        # Initialize bot core dengan test database
        self.bot = FinancialBotCore(self.temp_db.name)
        
        # Test user data
        self.test_user_id = "test_user_123"
        self.test_username = "TestUser"
    
    def tearDown(self):
        """Cleanup"""
        # Properly close database connections
        if hasattr(self.bot, 'db'):
            del self.bot.db
        del self.bot
        gc.collect()
        
        # Try to remove file (ignore if locked on Windows)
        try:
            if os.path.exists(self.temp_db.name):
                os.unlink(self.temp_db.name)
        except (PermissionError, OSError):
            pass  # Ignore Windows file locking issues
    
    def test_complete_income_flow(self):
        """Test complete flow untuk pemasukan"""
        # Test berbagai format perintah income
        test_messages = [
            "!income 5000000 gaji bonus akhir tahun",
            "saya dapat gaji 1000000 dari projek website",
            "dapat 500000 investasi",
            "income 250000 hadiah dari keluarga"
        ]
        
        for message in test_messages:
            response = self.bot.process_message(self.test_user_id, self.test_username, message)
            self.assertIn("Baik!", response)
            self.assertIn("pemasukan", response)
            self.assertIn("Saldo terbaru", response)
        
        # Check final balance
        stats = self.bot.get_user_stats(self.test_user_id)
        expected_total = 5000000 + 1000000 + 500000 + 250000
        self.assertEqual(stats['balance']['income'], expected_total)
        self.assertEqual(stats['balance']['balance'], expected_total)
    
    def test_complete_expense_flow(self):
        """Test complete flow untuk pengeluaran"""
        # Add some income first
        self.bot.process_message(self.test_user_id, self.test_username, "!income 1000000 gaji")
        
        # Test berbagai format expense
        test_messages = [
            "!expense 200000 makanan groceries bulanan",
            "saya habis 50000 untuk transport",
            "beli hiburan 100000",
            "bayar tagihan 150000"
        ]
        
        for message in test_messages:
            response = self.bot.process_message(self.test_user_id, self.test_username, message)
            self.assertIn("Oke!", response)
            self.assertIn("pengeluaran", response)
            self.assertIn("Saldo terbaru", response)
        
        # Check balance
        stats = self.bot.get_user_stats(self.test_user_id)
        expected_expense = 200000 + 50000 + 100000 + 150000
        self.assertEqual(stats['balance']['expense'], expected_expense)
        self.assertEqual(stats['balance']['balance'], 1000000 - expected_expense)
    
    def test_balance_query_variations(self):
        """Test berbagai variasi query balance"""
        # Add some transactions
        self.bot.process_message(self.test_user_id, self.test_username, "!income 1000000 gaji")
        self.bot.process_message(self.test_user_id, self.test_username, "!expense 300000 makanan")
        
        balance_queries = [
            "!balance",
            "saldo saya",
            "cek saldo",
            "berapa uang saya",
            "balance"
        ]
        
        for query in balance_queries:
            response = self.bot.process_message(self.test_user_id, self.test_username, query)
            self.assertIn("Ringkasan Keuangan", response)
            self.assertIn("1,000,000", response)  # Income
            self.assertIn("300,000", response)    # Expense
            self.assertIn("700,000", response)    # Balance
    
    def test_report_generation(self):
        """Test generation laporan"""
        # Add various transactions
        transactions = [
            ("!income 5000000 gaji", "salary"),
            ("!income 1000000 freelance", "project"),
            ("!expense 200000 makanan", "food"),
            ("!expense 150000 makanan", "snacks"),
            ("!expense 100000 transport", "fuel"),
            ("!expense 50000 hiburan", "movie")
        ]
        
        for message, desc in transactions:
            self.bot.process_message(self.test_user_id, self.test_username, message)
        
        # Generate report
        response = self.bot.process_message(self.test_user_id, self.test_username, "!report")
        
        # Check report content
        self.assertIn("Laporan Keuangan", response)
        self.assertIn("6,000,000", response)  # Total income
        self.assertIn("500,000", response)    # Total expense
        self.assertIn("5,500,000", response)  # Balance
        self.assertIn("Makanan", response)    # Category
        self.assertIn("350,000", response)    # Makanan total expense
    
    def test_help_command(self):
        """Test help command"""
        help_queries = [
            "!help",
            "help",
            "bantuan",
            "gimana cara pakai"
        ]
        
        for query in help_queries:
            response = self.bot.process_message(self.test_user_id, self.test_username, query)
            self.assertIn("Financial Bot", response)
            self.assertIn("!income", response)
            self.assertIn("!expense", response)
            self.assertIn("!balance", response)
    
    def test_automatic_categorization(self):
        """Test automatic categorization dalam context"""
        # Test messages with proper format that can be parsed
        test_cases = [
            ("!income 5000000 gaji bulan ini", "gaji"),
            ("!expense 50000 makanan siang", "makanan"),
            ("!expense 30000 transport bensin motor", "transport"),
            ("!expense 200000 tagihan listrik", "tagihan")
        ]
        
        for message, expected_category in test_cases:
            response = self.bot.process_message(self.test_user_id, self.test_username, message)
            # Check that the response mentions the expected category
            self.assertIn(expected_category, response.lower())
    
    def test_negative_balance_warning(self):
        """Test warning ketika saldo negatif"""
        # Start with small income
        self.bot.process_message(self.test_user_id, self.test_username, "!income 100000 gaji")
        
        # Make expense that exceeds income
        response = self.bot.process_message(self.test_user_id, self.test_username, "!expense 150000 makanan")
        
        # Should have warning
        self.assertIn("Perhatian", response)
        self.assertIn("negatif", response)
    
    def test_invalid_amounts(self):
        """Test handling invalid amounts"""
        # Test zero amount - proper command format
        response = self.bot.process_message(self.test_user_id, self.test_username, "!income 0 gaji")
        self.assertIn("harus lebih dari 0", response)
        
        # Test invalid format that won't be recognized
        response = self.bot.process_message(self.test_user_id, self.test_username, "random invalid text")
        self.assertIn("tidak mengerti", response)
    
    def test_large_numbers(self):
        """Test handling angka besar"""
        # Test dengan angka miliaran
        response = self.bot.process_message(
            self.test_user_id, 
            self.test_username, 
            "!income 1000000000 investasi"
        )
        self.assertIn("1,000,000,000", response)
        
        # Verify in balance
        balance_response = self.bot.process_message(self.test_user_id, self.test_username, "!balance")
        self.assertIn("1,000,000,000", balance_response)
    
    def test_unknown_command_handling(self):
        """Test handling perintah tidak dikenal"""
        unknown_messages = [
            "hello world",
            "what is the weather",
            "random text here",
            "!invalidcommand"
        ]
        
        for message in unknown_messages:
            response = self.bot.process_message(self.test_user_id, self.test_username, message)
            self.assertIn("tidak mengerti", response)
            self.assertIn("!help", response)
    
    def test_user_isolation(self):
        """Test bahwa data antar user terpisah"""
        user1_id = "user1_123"
        user2_id = "user2_456"
        
        # Add different transactions for each user
        self.bot.process_message(user1_id, "User1", "!income 1000000 gaji")
        self.bot.process_message(user2_id, "User2", "!expense 50000 makanan")
        
        # Check balances separately
        stats1 = self.bot.get_user_stats(user1_id)
        stats2 = self.bot.get_user_stats(user2_id)
        
        self.assertEqual(stats1['balance']['income'], 1000000)
        self.assertEqual(stats1['balance']['expense'], 0)
        
        self.assertEqual(stats2['balance']['income'], 0)
        self.assertEqual(stats2['balance']['expense'], 50000)

if __name__ == '__main__':
    unittest.main()