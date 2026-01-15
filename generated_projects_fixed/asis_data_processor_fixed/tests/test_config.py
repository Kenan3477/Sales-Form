#!/usr/bin/env python3
"""
ASIS Generated Tests for config.py
===================================
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestConfig(unittest.TestCase):
    """Test cases for config module"""
    
    def test_module_imports(self):
        """Test that the module can be imported"""
        try:
            if "config" == "data_processor":
                from data_processor import AsisDataProcessor
                processor = AsisDataProcessor()
                self.assertIsNotNone(processor)
            elif "config" == "automation_tool":
                from automation_tool import AsisAutomationTool
                tool = AsisAutomationTool()
                self.assertIsNotNone(tool)
            elif "config" == "api_service":
                from api_service import AsisApiService
                service = AsisApiService()
                self.assertIsNotNone(service)
        except ImportError as e:
            self.fail(f"Failed to import config: {e}")

if __name__ == "__main__":
    unittest.main()