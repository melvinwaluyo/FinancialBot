#!/usr/bin/env python3
"""
Tests for budget advice and purchase planning features
"""

import unittest
import tempfile
import os
from core.bot_core import FinancialBotCore
from core.rules import FinancialRulesEngine

class TestNewFeatures(unittest.TestCase):
    """Test budget advice and purchase planning functionality"""
    
    def setUp(self):
        """Setup test database and bot"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.bot = FinancialBotCore(self.temp_db.name)
        self.rules = FinancialRulesEngine()
        self.user_id = "test_user_123"
        self.username = "TestUser"
    
    def tearDown(self):
        """Clean up test database"""
        # Close the database connection properly
        if hasattr(self.bot, 'db') and hasattr(self.bot.db, 'db_path'):
            del self.bot.db
        try:
            if os.path.exists(self.temp_db.name):
                os.unlink(self.temp_db.name)
        except PermissionError:
            # On Windows, sometimes the file is still locked
            pass
    
    def test_budget_advice_parsing(self):
        """Test budget advice command parsing"""
        test_cases = [
            "Help me create a budget",
            "bantuan budget saya",
            "buatkan budget",
            "saya mau budget advice",
            "tolong budget saya"
        ]
        
        for command in test_cases:
            with self.subTest(command=command):
                result = self.rules.parse_command(command)
                self.assertEqual(result['type'], 'budget_advice')
                self.assertEqual(result['original_text'], command)
    
    def test_purchase_planning_parsing(self):
        """Test purchase planning command parsing"""
        test_cases = [
            ("I want to buy a car 30000000", "car", 30000000.0),
            ("saya mau beli laptop 15000000", "laptop", 15000000.0),
            ("I want to buy a house 500000000", "house", 500000000.0),
            ("saya ingin beli motor 25000000", "motor", 25000000.0)
        ]
        
        for command, expected_item, expected_price in test_cases:
            with self.subTest(command=command):
                result = self.rules.parse_command(command)
                self.assertEqual(result['type'], 'purchase_planning')
                self.assertEqual(result['item'], expected_item)
                self.assertEqual(result['price'], expected_price)
    
    def test_budget_advice_without_data(self):
        """Test budget advice when user has no financial data"""
        response = self.bot.process_message(self.user_id, self.username, "Help me create a budget")
        self.assertIn("Budget Advice", response)
        self.assertIn("pemasukan Anda", response)
    
    def test_budget_advice_with_data(self):
        """Test budget advice with existing financial data"""
        # Add some financial data
        self.bot.process_message(self.user_id, self.username, "Saya dapat gaji 6250000 dari kantor")
        self.bot.process_message(self.user_id, self.username, "Habis 4500000 untuk pengeluaran")
        
        # Request budget advice
        response = self.bot.process_message(self.user_id, self.username, "Help me create a budget")
        
        # Check response content
        self.assertIn("Monthly Budget Breakdown", response)
        self.assertIn("Income", response)
        self.assertIn("Expenses", response)
        self.assertIn("Available", response)
        self.assertIn("Emergency Fund", response)
        self.assertIn("Retirement", response)
        self.assertIn("6,250,000", response)
        self.assertIn("4,500,000", response)
    
    def test_purchase_planning_without_data(self):
        """Test purchase planning when user has no financial data"""
        response = self.bot.process_message(self.user_id, self.username, "I want to buy a car 30000000")
        self.assertIn("Car Purchase Analysis", response)
        self.assertIn("30,000,000", response)
        self.assertIn("Alternatives to Consider", response)
    
    def test_purchase_planning_with_data(self):
        """Test purchase planning with existing financial data"""
        # Add some financial data
        self.bot.process_message(self.user_id, self.username, "Saya dapat gaji 6250000 dari kantor")
        self.bot.process_message(self.user_id, self.username, "Habis 4500000 untuk pengeluaran")
        
        # Request purchase planning
        response = self.bot.process_message(self.user_id, self.username, "I want to buy a car 30000000")
        
        # Check response content
        self.assertIn("Car Purchase Analysis", response)
        self.assertIn("Purchase Price", response)
        self.assertIn("30,000,000", response)
        self.assertIn("Monthly Income", response)
        self.assertIn("6,250,000", response)
        self.assertIn("Alternatives to Consider", response)
        self.assertIn("Recommendation", response)
    
    def test_purchase_planning_expensive_item(self):
        """Test purchase planning for expensive items relative to income"""
        # Add minimal financial data
        self.bot.process_message(self.user_id, self.username, "Saya dapat gaji 3000000 dari kantor")
        
        # Request expensive item
        response = self.bot.process_message(self.user_id, self.username, "I want to buy a house 500000000")
        
        # Should contain warnings about the expensive purchase
        self.assertIn("House Purchase Analysis", response)
        self.assertIn("500,000,000", response)
        self.assertIn("Lower Cost Alternative", response)
        self.assertIn("Wait & Save", response)
    
    def test_budget_advice_different_languages(self):
        """Test budget advice in both Indonesian and English"""
        # Add financial data
        self.bot.process_message(self.user_id, self.username, "income 5000000 gaji")
        self.bot.process_message(self.user_id, self.username, "expense 3000000 pengeluaran")
        
        # Test English
        response_en = self.bot.process_message(self.user_id, self.username, "Help me create a budget")
        self.assertIn("Budget Breakdown", response_en)
        
        # Test Indonesian
        response_id = self.bot.process_message(self.user_id, self.username, "bantuan budget saya")
        self.assertIn("Budget Breakdown", response_id)
        
        # Both should contain similar financial information
        self.assertIn("5,000,000", response_en)
        self.assertIn("5,000,000", response_id)
    
    def test_purchase_planning_different_languages(self):
        """Test purchase planning in both Indonesian and English"""
        # Add financial data
        self.bot.process_message(self.user_id, self.username, "income 4000000 gaji")
        
        # Test English
        response_en = self.bot.process_message(self.user_id, self.username, "I want to buy a laptop 10000000")
        self.assertIn("Laptop Purchase Analysis", response_en)
        
        # Test Indonesian  
        response_id = self.bot.process_message(self.user_id, self.username, "saya mau beli motor 20000000")
        self.assertIn("Motor Purchase Analysis", response_id)
        
        # Both should contain analysis
        self.assertIn("Recommendation", response_en)
        self.assertIn("Recommendation", response_id)

if __name__ == '__main__':
    unittest.main()
