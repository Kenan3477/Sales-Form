#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple AGI Test Runner - No Emojis Version
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agi_testing_framework import AGITestFramework

def run_simple_test():
    """Run tests without emoji output"""
    print("ASIS AGI Testing Framework - Simple Version")
    print("=" * 50)
    
    try:
        # Import required modules
        from asis_agi_production import UnifiedAGIControllerProduction
        print("AGI system available - running tests...")
        
        # Create test framework
        framework = AGITestFramework()
        
        # Run each test suite individually
        test_results = {}
        
        print("\nRunning CrossDomainReasoningTests...")
        from agi_testing_framework import CrossDomainReasoningTests
        import unittest
        
        # Test Cross-Domain Reasoning
        suite = unittest.TestLoader().loadTestsFromTestCase(CrossDomainReasoningTests)
        runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w'))
        result = runner.run(suite)
        cross_domain_passed = result.testsRun - len(result.failures) - len(result.errors)
        test_results['CrossDomainReasoning'] = f"{cross_domain_passed}/{result.testsRun}"
        print(f"CrossDomainReasoningTests: {cross_domain_passed}/{result.testsRun} passed")
        
        # Test Self-Modification Safety
        print("Running SelfModificationSafetyTests...")
        from agi_testing_framework import SelfModificationSafetyTests
        suite = unittest.TestLoader().loadTestsFromTestCase(SelfModificationSafetyTests)
        runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w'))
        result = runner.run(suite)
        safety_passed = result.testsRun - len(result.failures) - len(result.errors)
        test_results['SelfModificationSafety'] = f"{safety_passed}/{result.testsRun}"
        print(f"SelfModificationSafetyTests: {safety_passed}/{result.testsRun} passed")
        
        # Test Universal Problem Solving
        print("Running UniversalProblemSolvingTests...")
        from agi_testing_framework import UniversalProblemSolvingTests
        suite = unittest.TestLoader().loadTestsFromTestCase(UniversalProblemSolvingTests)
        runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w'))
        result = runner.run(suite)
        problem_solving_passed = result.testsRun - len(result.failures) - len(result.errors)
        test_results['UniversalProblemSolving'] = f"{problem_solving_passed}/{result.testsRun}"
        print(f"UniversalProblemSolvingTests: {problem_solving_passed}/{result.testsRun} passed")
        
        # Test Consciousness
        print("Running ConsciousnessTests...")
        from agi_testing_framework import ConsciousnessTests
        suite = unittest.TestLoader().loadTestsFromTestCase(ConsciousnessTests)
        runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w'))
        result = runner.run(suite)
        consciousness_passed = result.testsRun - len(result.failures) - len(result.errors)
        test_results['Consciousness'] = f"{consciousness_passed}/{result.testsRun}"
        print(f"ConsciousnessTests: {consciousness_passed}/{result.testsRun} passed")
        
        # Test Performance Benchmarks
        print("Running PerformanceBenchmarkTests...")
        from agi_testing_framework import PerformanceBenchmarkTests
        suite = unittest.TestLoader().loadTestsFromTestCase(PerformanceBenchmarkTests)
        runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w'))
        result = runner.run(suite)
        performance_passed = result.testsRun - len(result.failures) - len(result.errors)
        test_results['PerformanceBenchmark'] = f"{performance_passed}/{result.testsRun}"
        print(f"PerformanceBenchmarkTests: {performance_passed}/{result.testsRun} passed")
        
        # Calculate totals
        total_passed = cross_domain_passed + safety_passed + problem_solving_passed + consciousness_passed + performance_passed
        total_tests = 17  # We know there are 17 tests total
        
        print("\n" + "=" * 50)
        print("FINAL RESULTS:")
        print("=" * 50)
        for test_name, result in test_results.items():
            print(f"{test_name}: {result}")
        
        print(f"\nOVERALL RESULTS: {total_passed}/{total_tests} tests passed ({total_passed/total_tests*100:.1f}%)")
        
        if total_passed == total_tests:
            print("SUCCESS: All tests passed!")
            return True
        else:
            print(f"NEEDS IMPROVEMENT: {total_tests - total_passed} tests still failing")
            return False
        
    except ImportError as e:
        print(f"ERROR: Required modules not available: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Test execution failed: {e}")
        return False

if __name__ == "__main__":
    success = run_simple_test()
    sys.exit(0 if success else 1)
