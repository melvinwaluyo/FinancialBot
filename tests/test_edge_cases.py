"""
Test edge cases and error handling for Financial Bot
"""
import unittest
import tempfile
import os
from core.bot_core import FinancialBotCore
from core.database import DatabaseManager


class TestEdgeCases(unittest.TestCase):
    
    def setUp(self):
        """Setup test environment with temporary database"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.bot = FinancialBotCore(db_path=self.temp_db.name)
        self.test_user_id = "test_user_edge"
        self.test_username = "EdgeTester"
    
    def tearDown(self):
        """Clean up temporary database"""
        try:
            self.bot.close_database()
            self.bot = None
        except:
            pass
        
        try:
            import time
            time.sleep(0.1)
            if os.path.exists(self.temp_db.name):
                os.unlink(self.temp_db.name)
        except (PermissionError, FileNotFoundError):
            pass
    
    def test_empty_message(self):
        """Test handling of empty messages"""
        response = self.bot.process_message(self.test_user_id, self.test_username, "")
        self.assertIn("tidak mengerti", response.lower())
    
    def test_whitespace_only_message(self):
        """Test handling of whitespace-only messages"""
        response = self.bot.process_message(self.test_user_id, self.test_username, "   \n\t  ")
        self.assertIn("tidak mengerti", response.lower())
    
    def test_very_large_amount(self):
        """Test handling of very large amounts"""
        large_amount = "999999999999999"
        response = self.bot.process_message(
            self.test_user_id, 
            self.test_username, 
            f"saya dapat gaji {large_amount} dari kantor"
        )
        self.assertIn("Rp 999,999,999,999,999", response)
    
    def test_zero_amount(self):
        """Test handling of zero amounts"""
        response = self.bot.process_message(
            self.test_user_id, 
            self.test_username, 
            "saya dapat gaji 0 dari kantor"
        )
        self.assertIn("harus lebih dari 0", response)
    
    def test_negative_amount(self):
        """Test handling of negative amounts"""
        response = self.bot.process_message(
            self.test_user_id, 
            self.test_username, 
            "saya dapat gaji -5000000 dari kantor"
        )
        self.assertIn("tidak mengerti", response.lower())
    
    def test_invalid_amount_format(self):
        """Test handling of invalid amount formats"""
        test_cases = [
            "saya dapat gaji abc dari kantor",
            "saya dapat gaji 50.000.000 dari kantor",  # Indonesian number format
            "saya dapat gaji 5,000,000 dari kantor",   # English number format
            "saya dapat gaji 5e6 dari kantor",         # Scientific notation
        ]
        
        for message in test_cases:
            response = self.bot.process_message(self.test_user_id, self.test_username, message)
            # Should either parse correctly or show error
            self.assertTrue(
                "tidak mengerti" in response.lower() or "mencatat" in response.lower(),
                f"Unexpected response for: {message}"
            )
    
    def test_extremely_long_description(self):
        """Test handling of very long descriptions"""
        long_desc = "a" * 1000  # 1000 character description
        response = self.bot.process_message(
            self.test_user_id, 
            self.test_username, 
            f"saya dapat gaji 5000000 {long_desc}"
        )
        # Should still process but might truncate description
        self.assertIn("mencatat", response.lower())
    
    def test_special_characters_in_description(self):
        """Test handling of special characters in descriptions"""
        special_chars = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        response = self.bot.process_message(
            self.test_user_id, 
            self.test_username, 
            f"saya dapat gaji 5000000 {special_chars}"
        )
        self.assertIn("mencatat", response.lower())
    
    def test_unicode_characters(self):
        """Test handling of Unicode characters"""
        unicode_text = "dari perusahaan 😀 🎉 café naïve résumé"
        response = self.bot.process_message(
            self.test_user_id, 
            self.test_username, 
            f"saya dapat gaji 5000000 {unicode_text}"
        )
        self.assertIn("mencatat", response.lower())
    
    def test_budget_advice_no_income(self):
        """Test budget advice when user has no income data"""
        response = self.bot.process_message(
            self.test_user_id, 
            self.test_username, 
            "bantuan anggaran saya"
        )
        self.assertIn("belum melihat pemasukan", response)
    
    def test_purchase_analysis_no_income(self):
        """Test purchase analysis when user has no income data"""
        response = self.bot.process_message(
            self.test_user_id, 
            self.test_username, 
            "saya mau beli laptop 15000000"
        )
        # Should still provide analysis even without income data
        self.assertIn("Analisis Beli", response)
    
    def test_balance_query_no_transactions(self):
        """Test balance query when user has no transactions"""
        response = self.bot.process_message(
            self.test_user_id, 
            self.test_username, 
            "berapa saldo saya"
        )
        # System should show balance even if 0
        self.assertIn("Saldo: Rp 0", response)
    
    def test_report_query_no_transactions(self):
        """Test report query when user has no transactions"""
        response = self.bot.process_message(
            self.test_user_id, 
            self.test_username, 
            "buatkan laporan keuangan"
        )
        # Report command is not recognized, should get help message
        self.assertIn("tidak mengerti", response)
    
    def test_multiple_amounts_in_message(self):
        """Test handling messages with multiple numbers"""
        response = self.bot.process_message(
            self.test_user_id, 
            self.test_username, 
            "saya dapat gaji 5000000 dan bonus 1000000 total 6000000"
        )
        # Should pick the first amount (5000000)
        self.assertIn("5,000,000", response)
    
    def test_case_insensitive_commands(self):
        """Test case insensitivity of commands"""
        test_cases = [
            "BANTUAN ANGGARAN SAYA",
            "Bantuan Anggaran Saya", 
            "bantuan anggaran saya",
            "BANTUAN anggaran SAYA"
        ]
        
        # Add some income first
        self.bot.process_message(self.test_user_id, self.test_username, "saya dapat gaji 5000000")
        
        for message in test_cases:
            response = self.bot.process_message(self.test_user_id, self.test_username, message)
            self.assertIn("Saran Penggunaan", response)
    
    def test_mixed_language_rejection(self):
        """Test that mixed Indonesian-English is handled appropriately"""
        mixed_messages = [
            "help me with budget saya",
            "saya want to buy laptop 15000000",
            "create budget untuk saya",
        ]
        
        for message in mixed_messages:
            response = self.bot.process_message(self.test_user_id, self.test_username, message)
            # Should either not understand or give Indonesian response
            self.assertTrue(
                "tidak mengerti" in response.lower() or 
                all(word not in response.lower() for word in ['help', 'create', 'budget advice'])
            )
    
    def test_rapid_successive_requests(self):
        """Test handling of rapid successive identical requests"""
        message = "bantuan anggaran saya"
        responses = []
        
        # Send same message 5 times rapidly
        for _ in range(5):
            response = self.bot.process_message(self.test_user_id, self.test_username, message)
            responses.append(response)
        
        # All responses should be consistent
        for response in responses:
            self.assertIn("belum melihat pemasukan", response)
    
    def test_database_corruption_recovery(self):
        """Test graceful handling of database issues"""
        # This is a more advanced test that would require mocking database failures
        # For now, just test that the bot can handle a fresh database
        self.assertIsNotNone(self.bot.db)
        self.assertIsInstance(self.bot.db, DatabaseManager)


if __name__ == '__main__':
    unittest.main()
