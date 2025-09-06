"""
Unit tests untuk Rules Engine
Testing regex patterns dan reflection kata ganti
"""

import unittest
import sys
import os

# Add parent directory to path untuk import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.rules import FinancialRulesEngine, ReflectionEngine

class TestReflectionEngine(unittest.TestCase):
    """Test reflection kata ganti"""
    
    def setUp(self):
        self.reflection_engine = ReflectionEngine()
    
    def test_pronoun_reflection_indonesian(self):
        """Test reflection kata ganti bahasa Indonesia"""
        # Test basic pronouns
        self.assertEqual(self.reflection_engine.reflect_text("saya punya uang"), "kamu punya uang")
        self.assertEqual(self.reflection_engine.reflect_text("aku mau nabung"), "kamu mau nabung")
        self.assertEqual(self.reflection_engine.reflect_text("kamu sudah bayar"), "saya sudah bayar")
        self.assertEqual(self.reflection_engine.reflect_text("anda sudah transfer"), "saya sudah transfer")

class TestFinancialRulesEngine(unittest.TestCase):
    """Test Financial Rules Engine"""
    
    def setUp(self):
        self.rules_engine = FinancialRulesEngine()
    
    def test_income_command_parsing(self):
        """Test parsing perintah pemasukan"""
        # Test command format
        result = self.rules_engine.parse_command("!income 5000000 gaji bonus akhir tahun")
        self.assertEqual(result['type'], 'income')
        self.assertEqual(result['amount'], 5000000.0)
        self.assertEqual(result['category'], 'gaji')
        self.assertEqual(result['description'], 'bonus akhir tahun')
        
        # Test natural language - Fixed pattern
        result = self.rules_engine.parse_command("saya dapat freelance 1000000 dari projek website")
        self.assertEqual(result['type'], 'income')
        self.assertEqual(result['amount'], 1000000.0)
        self.assertEqual(result['category'], 'freelance')
        
        # Test simple format
        result = self.rules_engine.parse_command("dapat 1000000 freelance")
        self.assertEqual(result['type'], 'income')
        self.assertEqual(result['amount'], 1000000.0)
        
        # Test with synonyms
        result = self.rules_engine.parse_command("saya meraih gaji 2000000")
        self.assertEqual(result['type'], 'income')
        self.assertEqual(result['amount'], 2000000.0)
    
    def test_expense_command_parsing(self):
        """Test parsing perintah pengeluaran"""
        # Test command format
        result = self.rules_engine.parse_command("!expense 50000 makanan lunch dengan teman")
        self.assertEqual(result['type'], 'expense')
        self.assertEqual(result['amount'], 50000.0)
        self.assertEqual(result['category'], 'makanan')
        self.assertEqual(result['description'], 'lunch dengan teman')
        
        # Test natural language
        result = self.rules_engine.parse_command("saya habis 75000 untuk transport")
        self.assertEqual(result['type'], 'expense')
        self.assertEqual(result['amount'], 75000.0)
        
        # Test alternative format: beli makanan 25000
        result = self.rules_engine.parse_command("beli makanan 25000")
        self.assertEqual(result['type'], 'expense')
        self.assertEqual(result['category'], 'makanan')
        self.assertEqual(result['amount'], 25000.0)
        
        # Test with synonyms
        result = self.rules_engine.parse_command("saya menghabiskan 100000 untuk hiburan")
        self.assertEqual(result['type'], 'expense')
        self.assertEqual(result['amount'], 100000.0)
        
        result = self.rules_engine.parse_command("saya belanja 200000 baju")
        self.assertEqual(result['type'], 'expense')
        self.assertEqual(result['amount'], 200000.0)
    
    def test_balance_command_parsing(self):
        """Test parsing perintah saldo"""
        # Test various balance queries - hanya bahasa Indonesia
        test_cases = [
            "!balance",
            "saldo saya",
            "cek saldo",
            "berapa uang saya",
            "saya punya berapa"
        ]
        
        for test_case in test_cases:
            result = self.rules_engine.parse_command(test_case)
            self.assertEqual(result['type'], 'balance', f"Failed for: {test_case}")
    
    def test_report_command_parsing(self):
        """Test parsing perintah laporan"""
        test_cases = [
            "!report",
            "laporan",
            "lihat laporan",
            "summary keuangan"
        ]
        
        for test_case in test_cases:
            result = self.rules_engine.parse_command(test_case)
            self.assertEqual(result['type'], 'report', f"Failed for: {test_case}")
    
    def test_help_command_parsing(self):
        """Test parsing perintah bantuan"""
        test_cases = [
            "!help",
            "help",
            "bantuan",
            "gimana cara",
            "apa perintah"
        ]
        
        for test_case in test_cases:
            result = self.rules_engine.parse_command(test_case)
            self.assertEqual(result['type'], 'help', f"Failed for: {test_case}")
    
    def test_about_command_parsing(self):
        """Test parsing pertanyaan tentang bot"""
        test_cases = [
            "siapa kamu",
            "apa nama kamu",
            "perkenalkan diri",
            "hai",
            "hello",
            "halo"
        ]
        
        for test_case in test_cases:
            result = self.rules_engine.parse_command(test_case)
            self.assertEqual(result['type'], 'about', f"Failed for: {test_case}")
    
    def test_capability_command_parsing(self):
        """Test parsing pertanyaan kemampuan bot"""
        test_cases = [
            "apa yang bisa kamu lakukan",
            "kamu bisa apa",
            "fungsi apa",
            "kemampuan kamu"
        ]
        
        for test_case in test_cases:
            result = self.rules_engine.parse_command(test_case)
            self.assertEqual(result['type'], 'capability', f"Failed for: {test_case}")
    
    def test_thanks_command_parsing(self):
        """Test parsing ucapan terima kasih"""
        test_cases = [
            "terima kasih",
            "makasih",
            "bagus",
            "mantap"
        ]
        
        for test_case in test_cases:
            result = self.rules_engine.parse_command(test_case)
            self.assertEqual(result['type'], 'thanks', f"Failed for: {test_case}")
    
    def test_goodbye_command_parsing(self):
        """Test parsing salam perpisahan"""
        test_cases = [
            "bye",
            "goodbye",
            "sampai jumpa",
            "dadah"
        ]
        
        for test_case in test_cases:
            result = self.rules_engine.parse_command(test_case)
            self.assertEqual(result['type'], 'goodbye', f"Failed for: {test_case}")
    
    def test_delete_command_parsing(self):
        """Test parsing perintah hapus"""
        # Test delete commands
        result = self.rules_engine.parse_command("!delete 123")
        self.assertEqual(result['type'], 'delete')
        self.assertEqual(result['transaction_id'], 123)
        
        result = self.rules_engine.parse_command("hapus transaksi 456")
        self.assertEqual(result['type'], 'delete')
        self.assertEqual(result['transaction_id'], 456)
    
    def test_automatic_categorization(self):
        """Test kategorisasi otomatis"""
        # Test income categorization
        category = self.rules_engine.categorize_automatically("gaji bulan ini", 5000000)
        self.assertEqual(category, 'gaji')
        
        category = self.rules_engine.categorize_automatically("projek freelance", 1000000)
        self.assertEqual(category, 'freelance')
        
        # Test expense categorization
        category = self.rules_engine.categorize_automatically("makan siang", 50000)
        self.assertEqual(category, 'makanan')
        
        category = self.rules_engine.categorize_automatically("bensin motor", 30000)
        self.assertEqual(category, 'transport')
        
        category = self.rules_engine.categorize_automatically("bayar listrik", 200000)
        self.assertEqual(category, 'tagihan')
        
        # Test with new synonyms
        category = self.rules_engine.categorize_automatically("lapar banget", 25000)
        self.assertEqual(category, 'makanan')
        
        category = self.rules_engine.categorize_automatically("pekerjaan kantor", 3000000)
        self.assertEqual(category, 'gaji')
    
    def test_amount_parsing(self):
        """Test parsing jumlah uang"""
        # Test various amount formats
        self.assertEqual(self.rules_engine.parse_amount("1000000"), 1000000.0)
        self.assertEqual(self.rules_engine.parse_amount("1,000,000"), 1000000.0)
        self.assertEqual(self.rules_engine.parse_amount("50000"), 50000.0)
        self.assertEqual(self.rules_engine.parse_amount("invalid"), 0.0)
    
    def test_unknown_command(self):
        """Test handling perintah tidak dikenal"""
        result = self.rules_engine.parse_command("hello world random text")
        self.assertEqual(result['type'], 'unknown')
        self.assertEqual(result['original_text'], 'hello world random text')
    
    def test_response_generation(self):
        """Test generation response"""
        # Test income response
        command_result = {
            'type': 'income',
            'amount': 1000000,
            'category': 'gaji',
            'description': 'gaji bulan ini'
        }
        response = self.rules_engine.generate_response(command_result)
        self.assertIn('Baik!', response)
        self.assertIn('1,000,000', response)
        self.assertIn('gaji', response)
        
        # Test expense response
        command_result = {
            'type': 'expense',
            'amount': 50000,
            'category': 'makanan',
            'description': 'lunch'
        }
        response = self.rules_engine.generate_response(command_result)
        self.assertIn('Oke!', response)
        self.assertIn('50,000', response)
        self.assertIn('makanan', response)
        
        # Test about response
        command_result = {'type': 'about'}
        response = self.rules_engine.generate_response(command_result)
        self.assertIn('Financial Bot', response)
        self.assertIn('asisten keuangan', response)
        
        # Test capability response
        command_result = {'type': 'capability'}
        response = self.rules_engine.generate_response(command_result)
        self.assertIn('Kemampuan Saya', response)
        self.assertIn('Manajemen Keuangan', response)
        
        # Test thanks response
        command_result = {'type': 'thanks'}
        response = self.rules_engine.generate_response(command_result)
        self.assertIn('Sama-sama', response)
        
        # Test goodbye response
        command_result = {'type': 'goodbye'}
        response = self.rules_engine.generate_response(command_result)
        self.assertIn('Sampai jumpa', response)
        
        # Test help response
        command_result = {'type': 'help'}
        response = self.rules_engine.generate_response(command_result)
        self.assertIn('Financial Bot', response)
        self.assertIn('!income', response)
        self.assertIn('!expense', response)

if __name__ == '__main__':
    unittest.main()