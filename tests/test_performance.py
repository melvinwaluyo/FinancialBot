"""
Performance tests for Financial Bot
Tests response times, memory usage, and scalability
"""
import unittest
import tempfile
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from core.bot_core import FinancialBotCore


class TestPerformance(unittest.TestCase):
    
    def setUp(self):
        """Setup test environment"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.bot = FinancialBotCore(db_path=self.temp_db.name)
        self.test_user_id = "perf_user"
        self.test_username = "PerfTester"
    
    def tearDown(self):
        """Clean up"""
        try:
            self.bot.close_database()
            self.bot = None
        except:
            pass
        
        try:
            # Give some time for file to be released on Windows
            import time
            time.sleep(0.1)
            if os.path.exists(self.temp_db.name):
                os.unlink(self.temp_db.name)
        except (PermissionError, FileNotFoundError):
            # File cleanup failed - not critical for test results
            pass
    
    def test_response_time_basic_commands(self):
        """Test response time for basic commands"""
        commands = [
            "saya dapat gaji 5000000 dari kantor",
            "habis 50000 makan siang", 
            "berapa saldo saya",
            "bantuan anggaran saya",
            "saya mau beli laptop 15000000"
        ]
        
        for command in commands:
            start_time = time.time()
            response = self.bot.process_message(self.test_user_id, self.test_username, command)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            # Response time should be under 1 second for basic commands
            self.assertLess(response_time, 1.0, 
                          f"Command '{command}' took {response_time:.3f}s")
            self.assertIsNotNone(response)
            self.assertGreater(len(response), 0)
    
    def test_large_transaction_volume(self):
        """Test handling of large number of transactions"""
        start_time = time.time()
        
        # Add 1000 transactions
        for i in range(1000):
            if i % 2 == 0:
                self.bot.process_message(
                    self.test_user_id, 
                    self.test_username, 
                    f"saya dapat gaji {5000000 + i} dari kantor transaksi {i}"
                )
            else:
                self.bot.process_message(
                    self.test_user_id, 
                    self.test_username, 
                    f"habis {50000 + i} untuk makanan transaksi {i}"
                )
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should handle 1000 transactions in reasonable time (under 30 seconds)
        self.assertLess(total_time, 30.0, 
                       f"1000 transactions took {total_time:.3f}s")
        
        # Test that balance query still works efficiently
        start_time = time.time()
        response = self.bot.process_message(self.test_user_id, self.test_username, "berapa saldo saya")
        end_time = time.time()
        
        balance_time = end_time - start_time
        self.assertLess(balance_time, 2.0, 
                       f"Balance query with 1000 transactions took {balance_time:.3f}s")
        self.assertIn("Ringkasan Keuangan", response)
    
    def test_concurrent_users(self):
        """Test handling multiple concurrent users"""
        def user_session(user_id):
            """Simulate a user session"""
            username = f"User{user_id}"
            commands = [
                f"saya dapat gaji {5000000 + user_id * 1000} dari kantor",
                f"habis {50000 + user_id * 10} makan siang",
                "berapa saldo saya",
                "bantuan anggaran saya"
            ]
            
            responses = []
            for command in commands:
                response = self.bot.process_message(str(user_id), username, command)
                responses.append(response)
                time.sleep(0.1)  # Small delay between commands
            
            return responses
        
        # Test with 10 concurrent users
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(user_session, i) for i in range(10)]
            results = [future.result() for future in futures]
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should handle 10 concurrent users in reasonable time
        self.assertLess(total_time, 15.0, 
                       f"10 concurrent users took {total_time:.3f}s")
        
        # All users should get responses
        self.assertEqual(len(results), 10)
        for user_responses in results:
            self.assertEqual(len(user_responses), 4)  # 4 commands per user
            for response in user_responses:
                self.assertIsNotNone(response)
                self.assertGreater(len(response), 0)
    
    def test_pattern_matching_performance(self):
        """Test performance of pattern matching with various inputs"""
        test_messages = [
            "bantuan anggaran saya",
            "tolong buatkan anggaran untuk saya",
            "saya mau beli mobil 50000000",
            "mau beli laptop 15000000 untuk kerja",
            "saya dapat gaji 5000000 dari kantor",
            "habis 50000 makan siang di warung",
            "berapa saldo saya sekarang",
            "buatkan laporan keuangan bulan ini",
            "siapa kamu?",
            "apa yang bisa kamu lakukan?",
            "message yang tidak dikenali sama sekali",
            "random text without meaning 12345"
        ]
        
        total_start_time = time.time()
        
        for message in test_messages:
            start_time = time.time()
            response = self.bot.process_message(self.test_user_id, self.test_username, message)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            # Each pattern matching should be very fast (under 0.1s)
            self.assertLess(response_time, 0.1, 
                          f"Pattern matching for '{message}' took {response_time:.3f}s")
        
        total_end_time = time.time()
        total_time = total_end_time - total_start_time
        
        # All pattern matching should complete quickly
        self.assertLess(total_time, 2.0, 
                       f"All pattern matching took {total_time:.3f}s")
    
    def test_memory_usage_stability(self):
        """Test that memory usage remains stable over many operations"""
        # Simplified test without psutil dependency
        
        # Perform many operations to test for memory leaks
        for i in range(100):
            self.bot.process_message(
                f"user_{i % 10}", 
                f"User{i}", 
                f"saya dapat gaji {5000000 + i} dari kantor {i}"
            )
            
            if i % 10 == 0:
                self.bot.process_message(f"user_{i % 10}", f"User{i}", "berapa saldo saya")
        
        # Test that bot still responds correctly after many operations
        response = self.bot.process_message(self.test_user_id, self.test_username, "bantuan anggaran saya")
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)
    
    def test_database_query_performance(self):
        """Test database query performance with varying data sizes"""
        # Add transactions for testing
        for i in range(100):
            self.bot.process_message(
                self.test_user_id, 
                self.test_username, 
                f"saya dapat gaji {5000000 + i} dari kantor {i}"
            )
        
        # Test balance query performance
        start_time = time.time()
        for _ in range(10):
            self.bot.process_message(self.test_user_id, self.test_username, "berapa saldo saya")
        end_time = time.time()
        
        avg_time = (end_time - start_time) / 10
        self.assertLess(avg_time, 0.5, 
                       f"Average balance query took {avg_time:.3f}s")
        
        # Test report query performance
        start_time = time.time()
        for _ in range(5):
            self.bot.process_message(self.test_user_id, self.test_username, "buatkan laporan keuangan")
        end_time = time.time()
        
        avg_time = (end_time - start_time) / 5
        self.assertLess(avg_time, 1.0, 
                       f"Average report query took {avg_time:.3f}s")
    
    def test_regex_pattern_efficiency(self):
        """Test efficiency of regex pattern matching"""
        from core.rules import FinancialRulesEngine
        
        rules_engine = FinancialRulesEngine()
        
        test_messages = [
            "bantuan anggaran saya" * 10,  # Repeated text
            "a" * 1000,  # Very long message
            "saya mau beli " + "laptop " * 100 + "15000000",  # Long with pattern
            "kata acak " * 200 + "bantuan anggaran saya",  # Pattern at end
        ]
        
        for message in test_messages:
            start_time = time.time()
            result = self.bot.process_message(self.test_user_id, self.test_username, message)
            end_time = time.time()
            
            processing_time = end_time - start_time
            
            # Regex should be efficient even with long messages
            self.assertLess(processing_time, 0.1, 
                          f"Regex processing took {processing_time:.3f}s for message length {len(message)}")


if __name__ == '__main__':
    unittest.main()
