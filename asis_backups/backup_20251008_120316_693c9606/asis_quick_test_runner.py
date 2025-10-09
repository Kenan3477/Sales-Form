#!/usr/bin/env python3
"""
ASIS Quick Test Runner
=====================

A streamlined interface for running ASIS capability tests with focused scenarios.
Designed for rapid validation and demonstration of key capabilities.

Author: ASIS Development Team
Date: September 18, 2025
Version: 1.0
"""

import asyncio
import time
from asis_comprehensive_test_scenarios import ASISTestFramework, TestCategory

class ASISQuickTester:
    """Streamlined test runner for key ASIS capabilities"""
    
    def __init__(self):
        self.framework = ASISTestFramework()
        self.selected_tests = self._select_representative_tests()
    
    def _select_representative_tests(self):
        """Select representative tests from each category"""
        representative = []
        
        # Get one test from each category for quick validation
        categories_seen = set()
        for scenario in self.framework.test_scenarios:
            if scenario.category not in categories_seen:
                representative.append(scenario)
                categories_seen.add(scenario.category)
                
                # Stop when we have one from each category
                if len(categories_seen) >= 5:  # 5 categories
                    break
        
        return representative
    
    async def run_quick_tests(self):
        """Run representative tests quickly"""
        print("🚀 ASIS Quick Capability Validation")
        print("=" * 50)
        print(f"Running {len(self.selected_tests)} representative tests...")
        print()
        
        results = []
        for scenario in self.selected_tests:
            print(f"🔍 Testing: {scenario.category.value.replace('_', ' ').title()}")
            result = await self.framework.run_test_scenario(scenario)
            results.append(result)
            
            status = "✅ PASS" if result.success else "❌ FAIL"
            print(f"   {status} - Score: {result.score:.1f}/100 ({result.execution_time:.1f}s)")
            print()
        
        # Quick summary
        total_score = sum(r.score for r in results)
        max_score = sum(r.max_score for r in results)
        percentage = (total_score / max_score) * 100
        
        passed = sum(1 for r in results if r.success)
        
        print("📊 QUICK TEST SUMMARY")
        print("-" * 30)
        print(f"Overall Score: {total_score:.1f}/{max_score:.1f} ({percentage:.1f}%)")
        print(f"Tests Passed: {passed}/{len(results)}")
        print()
        
        # Capability assessment
        if percentage >= 90:
            print("🌟 EXCELLENT: ASIS demonstrates exceptional capabilities across all areas")
        elif percentage >= 80:
            print("✅ STRONG: ASIS shows solid performance in most capability areas")
        elif percentage >= 70:
            print("⚡ GOOD: ASIS has competent capabilities with room for improvement")
        elif percentage >= 60:
            print("⚠️ ADEQUATE: ASIS shows basic capabilities but needs enhancement")
        else:
            print("🔧 NEEDS WORK: ASIS capabilities require significant development")
        
        return results

async def main():
    """Run quick ASIS capability tests"""
    tester = ASISQuickTester()
    await tester.run_quick_tests()
    
    print("\n" + "=" * 50)
    print("For comprehensive testing, run: python asis_comprehensive_test_scenarios.py")

if __name__ == "__main__":
    asyncio.run(main())
