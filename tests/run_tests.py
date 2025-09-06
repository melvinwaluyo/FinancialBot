"""
Comprehensive test runner for Financial Bot
Runs all test suitesif __name__ == "__main__":
    success = discover_and_run_tests()
    sys.exit(0 if success else 1)nd generates detailed reports
"""

import unittest
import sys
import os
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def discover_and_run_tests():
    """Discover and run all test files automatically"""
    print("🚀 Financial Bot - Comprehensive Test Suite")
    print(f"Python {sys.version}")
    print(f"Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Discover all test files
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Print comprehensive summary
    print(f"\n{'='*60}")
    print("🏁 COMPREHENSIVE TEST SUMMARY")
    print(f"{'='*60}")
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped) if hasattr(result, 'skipped') else 0
    passed = total_tests - failures - errors - skipped
    
    print(f"📊 Results:")
    print(f"   Total Tests: {total_tests}")
    print(f"   ✅ Passed:   {passed}")
    print(f"   ❌ Failed:   {failures}")
    print(f"   🚫 Errors:   {errors}")
    print(f"   ⏭️  Skipped:  {skipped}")
    print(f"   ⏱️  Time:     {end_time - start_time:.2f}s")
    print(f"   📈 Success:  {(passed / total_tests * 100):.1f}%")
    
    # Show details of failures
    if result.failures:
        print(f"\n❌ FAILURES ({len(result.failures)}):")
        for i, (test, traceback) in enumerate(result.failures, 1):
            print(f"   {i}. {test}")
    
    # Show details of errors  
    if result.errors:
        print(f"\n🚫 ERRORS ({len(result.errors)}):")
        for i, (test, traceback) in enumerate(result.errors, 1):
            print(f"   {i}. {test}")
    
    # Final status
    if failures + errors == 0:
        print(f"\n🎉 ALL TESTS PASSED! Financial Bot is ready.")
        return True
    else:
        print(f"\n⚠️  SOME TESTS FAILED. Review failures above.")
        return False

if __name__ == '__main__':
    success = discover_and_run_tests()
    sys.exit(0 if success else 1)
