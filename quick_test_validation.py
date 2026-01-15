#!/usr/bin/env python3
"""
Quick AGI Validation System Test
================================
Simple test to verify the validation system works correctly
"""

import asyncio
import sys
import os

def test_basic_functionality():
    """Test basic functionality of the validation system"""
    print("🧪 Quick AGI Validation System Test")
    print("="*40)
    
    try:
        # Test imports
        print("1. Testing imports...")
        from asis_agi_validation_system import AGIValidationFramework, MockAGISystem
        from run_agi_validation import AGIValidationTestRunner
        print("   ✅ All imports successful")
        
        # Test validator initialization
        print("2. Testing validator initialization...")
        validator = AGIValidationFramework()
        print("   ✅ Validator initialized successfully")
        
        # Test mock AGI system
        print("3. Testing mock AGI system...")
        mock_agi = MockAGISystem()
        
        async def test_mock_agi():
            result = await mock_agi.process_request("test")
            return isinstance(result, str) and "test" in result
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            mock_works = loop.run_until_complete(test_mock_agi())
            if mock_works:
                print("   ✅ Mock AGI system working")
            else:
                print("   ❌ Mock AGI system issue")
                return False
        finally:
            loop.close()
        
        # Test scoring methods
        print("4. Testing scoring methods...")
        test_scores = {
            "cross_domain": 0.8,
            "novel_problem": 0.9,
            "self_modification": 0.7,
            "consciousness": 0.8,
            "transfer_learning": 0.6,
            "metacognition": 0.7,
            "emergent_behavior": 0.8,
            "ethical_reasoning": 0.7
        }
        
        overall_score = validator.calculate_agi_score(test_scores)
        if 0.0 <= overall_score <= 1.0:
            print(f"   ✅ Scoring system working (score: {overall_score:.3f})")
        else:
            print(f"   ❌ Scoring system issue (score: {overall_score})")
            return False
        
        # Test classification
        print("5. Testing AGI classification...")
        classification = validator.classify_agi_level(overall_score)
        if classification and isinstance(classification, str):
            print(f"   ✅ Classification working ({classification})")
        else:
            print("   ❌ Classification issue")
            return False
        
        # Test evaluation methods
        print("6. Testing evaluation methods...")
        test_response = "This is similar to biological evolution. Companies compete for market share."
        test_case = {"domain_1": "biology", "domain_2": "business", "difficulty": 0.7}
        
        score = validator.evaluate_cross_domain_response(test_response, test_case)
        if 0.0 <= score <= 1.0:
            print(f"   ✅ Cross-domain evaluation working (score: {score:.3f})")
        else:
            print(f"   ❌ Cross-domain evaluation issue (score: {score})")
            return False
        
        # Test test runner
        print("7. Testing test runner...")
        runner = AGIValidationTestRunner()
        if hasattr(runner, 'run_validation_suite'):
            print("   ✅ Test runner initialized")
        else:
            print("   ❌ Test runner issue")
            return False
        
        print("\n🎉 ALL BASIC TESTS PASSED!")
        print("The AGI validation system is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sample_validation():
    """Run a quick sample validation"""
    print("\n🚀 Running Sample Validation...")
    print("="*40)
    
    try:
        from asis_agi_validation_system import AGIValidationFramework
        
        validator = AGIValidationFramework()
        
        # Test individual evaluation methods
        print("Testing consciousness evaluation...")
        consciousness_response = "I am currently aware of my internal state and experiencing this conversation"
        consciousness_score = validator.evaluate_consciousness_response(consciousness_response, "self_recognition")
        print(f"Consciousness Score: {consciousness_score:.3f}")
        
        print("Testing novel solution evaluation...")
        novel_solution = "This innovative approach uses creative thinking with logical steps and practical implementation"
        novel_problem = {"criteria": ["creativity", "logic", "practical"], "difficulty": 0.8}
        novel_score = validator.evaluate_novel_solution(novel_solution, novel_problem, 2.0)
        print(f"Novel Solution Score: {novel_score:.3f}")
        
        print("Testing transfer learning evaluation...")
        learning_result = type('Result', (), {'success': True, 'concept': 'test'})()
        transfer_result = "Successfully applied the learned concept to the new domain"
        transfer_score = validator.evaluate_transfer_learning(learning_result, transfer_result)
        print(f"Transfer Learning Score: {transfer_score:.3f}")
        
        print("\n✅ Sample validation completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Sample validation failed: {e}")
        return False

def test_database_operations():
    """Test database operations"""
    print("\n💾 Testing Database Operations...")
    print("="*40)
    
    try:
        from asis_agi_validation_system import AGIValidationFramework
        import sqlite3
        
        # Create validator with test database
        validator = AGIValidationFramework()
        validator.db_path = "test_quick_validation.db"
        validator.init_database()
        
        # Test storing results
        test_details = {"test_case": 1, "difficulty": 0.8}
        validator.store_test_result("test_category", 0.85, test_details)
        
        # Verify storage
        conn = sqlite3.connect(validator.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM validation_results WHERE test_name = ?", ("test_category",))
        result = cursor.fetchone()
        conn.close()
        
        if result and result[2] == 0.85:  # Check score
            print("✅ Database operations working")
            
            # Clean up test database
            try:
                os.remove(validator.db_path)
            except OSError:
                pass
                
            return True
        else:
            print("❌ Database storage issue")
            return False
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def main():
    """Run all quick tests"""
    print("🔬 ASIS AGI Validation System Quick Test Suite")
    print("="*50)
    
    tests_passed = 0
    total_tests = 3
    
    # Run basic functionality test
    if test_basic_functionality():
        tests_passed += 1
    
    # Run sample validation test
    if test_sample_validation():
        tests_passed += 1
    
    # Run database operations test
    if test_database_operations():
        tests_passed += 1
    
    # Final results
    print(f"\n🎯 FINAL RESULTS")
    print("="*20)
    print(f"Tests Passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED! The AGI validation system is working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Check the implementation.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
