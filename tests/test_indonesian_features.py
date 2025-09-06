#!/usr/bin/env python3
"""
Simple test for Indonesian budget and purchase planning features
"""

import unittest
from core.rules import FinancialRulesEngine

class TestIndonesianFeatures(unittest.TestCase):
    """Test Indonesian budget advice and purchase planning"""
    
    def setUp(self):
        """Setup rules engine"""
        self.rules = FinancialRulesEngine()
    
    def test_indonesian_budget_patterns(self):
        """Test Indonesian budget advice patterns"""
        test_cases = [
            "bantuan anggaran saya",
            "buatkan anggaran", 
            "saya mau anggaran",
            "konsultasi anggaran",
            "analisis anggaran saya"
        ]
        
        for command in test_cases:
            with self.subTest(command=command):
                result = self.rules.parse_command(command)
                self.assertEqual(result['type'], 'budget_advice')
    
    def test_indonesian_purchase_patterns(self):
        """Test Indonesian purchase planning patterns"""
        test_cases = [
            ("saya mau beli mobil 50000000", "mobil", 50000000.0),
            ("mau beli laptop 15000000", "laptop", 15000000.0),
            ("rencana beli motor 25000000", "motor", 25000000.0),
            ("analisis beli rumah 500000000", "rumah", 500000000.0),
            ("konsultasi beli handphone 10000000", "handphone", 10000000.0)
        ]
        
        for command, expected_item, expected_price in test_cases:
            with self.subTest(command=command):
                result = self.rules.parse_command(command)
                self.assertEqual(result['type'], 'purchase_planning')
                self.assertEqual(result['item'], expected_item)
                self.assertEqual(result['price'], expected_price)
    
    def test_budget_response_without_data(self):
        """Test budget response when no data is available"""
        result = self.rules._generate_budget_advice_response(None)
        self.assertIn("Saran Anggaran", result)
        self.assertIn("data keuangan kamu dulu", result)
        self.assertIn("Mulai dengan", result)
    
    def test_budget_response_with_data(self):
        """Test budget response with financial data"""
        user_data = {
            'balance': {
                'income': 6250000,
                'expense': 4500000,
                'balance': 1750000
            }
        }
        
        result = self.rules._generate_budget_advice_response(user_data)
        self.assertIn("Ringkasan Keuangan Bulanan", result)
        self.assertIn("Pemasukan", result)
        self.assertIn("Pengeluaran", result)
        self.assertIn("Dana Darurat", result)
        self.assertIn("Tabungan", result)
        self.assertIn("6,250,000", result)
        self.assertIn("4,500,000", result)
    
    def test_purchase_response_without_data(self):
        """Test purchase response when no data is available"""
        command_result = {'item': 'mobil', 'price': 30000000}
        result = self.rules._generate_purchase_planning_response(command_result, None)
        self.assertIn("Analisis Pembelian", result)
        self.assertIn("30,000,000", result)
        self.assertIn("data keuangan kamu", result)
    
    def test_purchase_response_with_data(self):
        """Test purchase response with financial data"""
        command_result = {'item': 'mobil', 'price': 30000000}
        user_data = {
            'balance': {
                'income': 6250000,
                'expense': 4500000,
                'balance': 1750000
            }
        }
        
        result = self.rules._generate_purchase_planning_response(command_result, user_data)
        self.assertIn("Analisis Beli Mobil", result)
        self.assertIn("Harga Barang", result)
        self.assertIn("30,000,000", result)
        self.assertIn("Gaji Bulanan", result)
        self.assertIn("6,250,000", result)
        self.assertIn("Pilihan untuk Kamu", result)
        self.assertIn("Saran Saya", result)
    
    def test_no_english_in_responses(self):
        """Test that responses are purely in Indonesian"""
        # Test budget response
        user_data = {
            'balance': {
                'income': 5000000,
                'expense': 3000000,
                'balance': 2000000
            }
        }
        budget_response = self.rules._generate_budget_advice_response(user_data)
        
        # Test purchase response
        command_result = {'item': 'laptop', 'price': 15000000}
        purchase_response = self.rules._generate_purchase_planning_response(command_result, user_data)
        
        # Check for common English words that should not appear
        english_words = ['Budget', 'Breakdown', 'Income', 'Expenses', 'Available', 
                        'Emergency', 'Fund', 'Retirement', 'Purchase', 'Analysis',
                        'Option', 'Alternative', 'Recommendation', 'Concerns']
        
        for word in english_words:
            self.assertNotIn(word, budget_response, f"English word '{word}' found in budget response")
            self.assertNotIn(word, purchase_response, f"English word '{word}' found in purchase response")

if __name__ == '__main__':
    unittest.main()
