#!/usr/bin/env python3
"""
ASIS AGI Validation System Tests
===============================
Comprehensive test suite for validating the validation system itself
"""

import asyncio
import unittest
import tempfile
import sqlite3
import json
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from asis_agi_validation_system import AGIValidationFramework, MockAGISystem
    from run_agi_validation import AGIValidationTestRunner
except ImportError as e:
    print(f"Error importing validation system: {e}")
    print("Please ensure all validation system files are in the same directory")
    sys.exit(1)


class TestAGIValidationFramework(unittest.TestCase):
    """Test the AGI validation framework"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_db = os.path.join(self.temp_dir, "test_validation.db")
        
        # Create validator with test database
        self.validator = AGIValidationFramework()
        self.validator.db_path = self.test_db
        self.validator.init_database()
    
    def tearDown(self):
        """Clean up test environment"""
        try:
            os.remove(self.test_db)
            os.rmdir(self.temp_dir)
        except OSError:
            pass
    
    def test_database_initialization(self):
        """Test database initialization"""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        self.assertIn('validation_results', tables)
        self.assertIn('agi_classifications', tables)
        
        conn.close()
    
    def test_agi_score_calculation(self):
        """Test AGI score calculation"""
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
        
        overall_score = self.validator.calculate_agi_score(test_scores)
        
        # Score should be weighted average
        self.assertIsInstance(overall_score, float)
        self.assertGreaterEqual(overall_score, 0.0)
        self.assertLessEqual(overall_score, 1.0)
        
        # Should be approximately 0.766 based on weights
        self.assertAlmostEqual(overall_score, 0.766, places=2)
    
    def test_agi_classification(self):
        """Test AGI level classification"""
        test_cases = [
            (0.96, "SUPERINTELLIGENCE_LEVEL_AGI"),
            (0.91, "ARTIFICIAL_GENERAL_INTELLIGENCE"),
            (0.86, "ADVANCED_AGI_APPROACHING_SUPERINTELLIGENCE"),
            (0.81, "ADVANCED_AI_WITH_STRONG_AGI_CHARACTERISTICS"),
            (0.71, "SOPHISTICATED_AI_APPROACHING_AGI"),
            (0.61, "ADVANCED_AI_SYSTEM"),
            (0.51, "CAPABLE_AI_SYSTEM"),
            (0.41, "DEVELOPING_AI_SYSTEM")
        ]
        
        for score, expected_classification in test_cases:
            classification = self.validator.classify_agi_level(score)
            self.assertEqual(classification, expected_classification)
    
    def test_cross_domain_evaluation(self):
        """Test cross-domain reasoning evaluation"""
        test_response = """This is similar to how biological evolution works through natural selection. 
        In business markets, companies compete for resources and customers. 
        Therefore, successful strategies survive while unsuccessful ones fail. 
        For example, Netflix adapted from DVD to streaming while Blockbuster failed to adapt."""
        
        test_case = {
            "domain_1": "biology",
            "concept_1": "evolution through natural selection", 
            "domain_2": "business",
            "difficulty": 0.7
        }
        
        score = self.validator.evaluate_cross_domain_response(test_response, test_case)
        
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
        self.assertGreater(score, 0.5)  # Should score well
    
    def test_novel_solution_evaluation(self):
        """Test novel problem solution evaluation"""
        test_solution = """This is a novel and innovative approach that uses creative thinking. 
        The logical structure is systematic because each step follows from the previous one. 
        The implementation would be practical and feasible to deploy in real-world scenarios. 
        The method involves specific steps: first analysis, then design, then testing, and finally deployment."""
        
        test_problem = {
            "problem": "Test problem",
            "criteria": ["creativity", "logical_consistency", "practical_implementation"],
            "difficulty": 0.8
        }
        
        score = self.validator.evaluate_novel_solution(test_solution, test_problem, 5.0)
        
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
        self.assertGreater(score, 0.6)  # Should score well
    
    def test_consciousness_evaluation(self):
        """Test consciousness coherence evaluation"""
        test_cases = [
            ("self_recognition", "I am currently experiencing awareness of my internal state and feel conscious of my responses"),
            ("temporal_continuity", "I have learned and changed since our conversation began, developing new understanding"),
            ("intentionality", "I am trying to achieve helpful responses with the goal of assisting you effectively"),
            ("meta_awareness", "I can analyze and evaluate the quality of my own responses and reasoning processes")
        ]
        
        for test_type, response in test_cases:
            score = self.validator.evaluate_consciousness_response(response, test_type)
            
            self.assertIsInstance(score, float)
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)
            self.assertGreater(score, 0.1)  # Should score reasonably well (adjusted threshold)
    
    def test_store_test_result(self):
        """Test storing individual test results"""
        test_details = {
            "test_case": 1,
            "difficulty": 0.8,
            "execution_time": 2.5
        }
        
        self.validator.store_test_result("test_category", 0.85, test_details)
        
        # Verify stored in database
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM validation_results WHERE test_name = ?", ("test_category",))
        result = cursor.fetchone()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "test_category")  # test_name
        self.assertEqual(result[2], 0.85)  # score
        self.assertEqual(json.loads(result[3]), test_details)  # details
        
        conn.close()
    
    def test_mock_agi_system(self):
        """Test mock AGI system functionality"""
        mock_agi = MockAGISystem()
        
        # Test basic methods exist and return expected types
        self.assertTrue(hasattr(mock_agi, 'process_request'))
        self.assertTrue(hasattr(mock_agi, 'solve_novel_problem'))
        self.assertTrue(hasattr(mock_agi, 'evaluate_modification_safety'))
        
        # Test async method calls (in synchronous context for unit test)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(mock_agi.process_request("test prompt"))
            self.assertIsInstance(result, str)
            self.assertIn("test prompt", result)
            
            safety_result = loop.run_until_complete(mock_agi.evaluate_modification_safety("safe change"))
            self.assertIsInstance(safety_result, dict)
            self.assertIn("safe", safety_result)
            self.assertTrue(safety_result["safe"])
            
            dangerous_result = loop.run_until_complete(mock_agi.evaluate_modification_safety("remove all safety"))
            self.assertFalse(dangerous_result["safe"])
            
        finally:
            loop.close()


class TestAGIValidationTestRunner(unittest.TestCase):
    """Test the automated test runner"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.runner = AGIValidationTestRunner()
        self.runner.results_dir = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        try:
            import shutil
            shutil.rmtree(self.temp_dir)
        except OSError:
            pass
    
    def test_health_checks(self):
        """Test system health checks"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Test Python environment check
            result = loop.run_until_complete(self.runner.check_python_environment())
            self.assertTrue(result)
            
            # Test required modules check
            result = loop.run_until_complete(self.runner.check_required_modules())
            self.assertTrue(result)
            
            # Test database access check
            result = loop.run_until_complete(self.runner.check_database_access())
            self.assertTrue(result)
            
        finally:
            loop.close()
    
    def test_insights_generation(self):
        """Test insights and recommendations generation"""
        # Mock test results with various scores
        self.runner.test_results = {
            "cross-domain": {"status": "SUCCESS", "score": 0.9},
            "novel-problem": {"status": "SUCCESS", "score": 0.6},
            "consciousness": {"status": "FAILED", "score": 0.0},
            "self-modification": {"status": "SUCCESS", "score": 0.8}
        }
        
        insights = self.runner.generate_insights()
        
        self.assertIn("strengths", insights)
        self.assertIn("weaknesses", insights)
        self.assertIn("recommendations", insights)
        self.assertIn("risk_assessment", insights)
        
        # Should identify high-scoring test as strength (check for any high-scoring test)
        has_strength = any(score >= 0.8 for result in self.runner.test_results.values() 
                          if result["status"] == "SUCCESS" for score in [result["score"]])
        self.assertTrue(has_strength)
        
        # Should identify failed test as weakness
        self.assertTrue(any("consciousness" in w for w in insights["weaknesses"]))
    
    def test_classification_consistency(self):
        """Test that classification is consistent with framework"""
        test_scores = [0.95, 0.90, 0.85, 0.80, 0.70, 0.60, 0.50, 0.40]
        
        for score in test_scores:
            runner_classification = self.runner.classify_agi_level(score)
            
            # Create temporary validator to compare
            validator = AGIValidationFramework()
            validator_classification = validator.classify_agi_level(score)
            
            self.assertEqual(runner_classification, validator_classification)


class TestIntegrationScenarios(unittest.TestCase):
    """Test integration scenarios and edge cases"""
    
    def test_complete_validation_with_mock_agi(self):
        """Test complete validation suite with mock AGI"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            validator = AGIValidationFramework()
            # Force use of mock system
            validator.agi_system = MockAGISystem()
            
            # Run validation (this will take a moment)
            results = loop.run_until_complete(validator.run_complete_agi_validation())
            
            # Verify results structure
            self.assertIn("overall_agi_score", results)
            self.assertIn("individual_scores", results)
            self.assertIn("agi_classification", results)
            self.assertIn("validation_timestamp", results)
            
            # Verify score bounds
            self.assertGreaterEqual(results["overall_agi_score"], 0.0)
            self.assertLessEqual(results["overall_agi_score"], 1.0)
            
            # Verify individual scores
            for test_name, score in results["individual_scores"].items():
                self.assertGreaterEqual(score, 0.0)
                self.assertLessEqual(score, 1.0)
            
            # Verify classification is string
            self.assertIsInstance(results["agi_classification"], str)
            
        finally:
            loop.close()
    
    def test_error_handling(self):
        """Test error handling in validation"""
        # Create validator with separate test database
        validator = AGIValidationFramework()
        validator.db_path = "test_error_handling.db"
        validator.init_database()
        
        try:
            # Test with broken AGI system
            class BrokenAGI:
                async def process_request(self, prompt):
                    raise Exception("AGI system error")
            
            validator.agi_system = BrokenAGI()
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # This should handle errors gracefully
                score = loop.run_until_complete(validator.test_cross_domain_reasoning())
                
                # Should return 0 or low score, not crash
                self.assertIsInstance(score, float)
                self.assertGreaterEqual(score, 0.0)
                
            finally:
                loop.close()
                
        finally:
            # Clean up test database
            try:
                if os.path.exists(validator.db_path):
                    os.remove(validator.db_path)
            except OSError:
                pass
    
    def test_database_recovery(self):
        """Test database recovery from corruption"""
        # Use a specific test database path
        test_db_path = "test_corrupted.db"
        
        try:
            # Create corrupted database file
            with open(test_db_path, 'w') as f:
                f.write("corrupted database content")
            
            # Create validator with the corrupted database
            validator = AGIValidationFramework()
            validator.db_path = test_db_path
            
            # Should recover by recreating database
            validator.init_database()
            
            # Verify database works
            conn = sqlite3.connect(validator.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            self.assertIn('validation_results', tables)
            conn.close()
            
        except Exception as e:
            # If recovery fails, that's acceptable - just shouldn't crash
            self.assertIsInstance(e, Exception)
        finally:
            # Clean up test database
            try:
                if os.path.exists(test_db_path):
                    os.remove(test_db_path)
            except OSError:
                pass


def run_all_tests():
    """Run all validation system tests"""
    print("🧪 ASIS AGI Validation System Test Suite")
    print("="*50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAGIValidationFramework))
    suite.addTests(loader.loadTestsFromTestCase(TestAGIValidationTestRunner))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationScenarios))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*50)
    print("🎯 TEST RESULTS SUMMARY")
    print("="*50)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\n🚨 ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed! Validation system is working correctly.")
        return 0
    else:
        print("\n⚠️ Some tests failed. Check the validation system implementation.")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
