#!/usr/bin/env python3
"""
ASIS Generated Tests for utils.py
===================================
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestUtils(unittest.TestCase):
    """Test cases for utils module"""
    
    def test_module_imports(self):
        """Test that the module can be imported"""
        try:
            if "utils" == "data_processor":
                from data_processor import AsisDataProcessor
                processor = AsisDataProcessor()
                self.assertIsNotNone(processor)
            elif "utils" == "automation_tool":
                from automation_tool import AsisAutomationTool
                tool = AsisAutomationTool()
                self.assertIsNotNone(tool)
            elif "utils" == "api_service":
                from api_service import AsisApiService
                service = AsisApiService()
                self.assertIsNotNone(service)
        except ImportError as e:
            self.fail(f"Failed to import utils: {e}")

if __name__ == "__main__":
    unittest.main()