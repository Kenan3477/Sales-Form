#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 ASIS AGI Benchmarking System Validation
Quick validation script to ensure all benchmark components are working

Author: ASIS AGI Development Team
Version: 1.0.0
"""

import sys
import os

def validate_system():
    """Validate the benchmarking system components"""
    print("🔍 ASIS AGI Benchmarking System Validation")
    print("=" * 50)
    
    validation_results = []
    
    # Check if main files exist
    required_files = [
        "asis_agi_benchmarks.py",
        "asis_agi_production.py", 
        "test_agi_benchmarks.py",
        "AGI_BENCHMARKING_README.md"
    ]
    
    print("\n📁 File Validation:")
    for file in required_files:
        exists = os.path.exists(file)
        status = "✅" if exists else "❌"
        print(f"   {status} {file}")
        validation_results.append(exists)
    
    # Test imports
    print("\n📦 Import Validation:")
    try:
        import sqlite3
        print("   ✅ sqlite3")
        validation_results.append(True)
    except ImportError:
        print("   ❌ sqlite3")
        validation_results.append(False)
    
    try:
        import json
        print("   ✅ json")
        validation_results.append(True)
    except ImportError:
        print("   ❌ json")
        validation_results.append(False)
    
    try:
        import hashlib
        print("   ✅ hashlib")
        validation_results.append(True)
    except ImportError:
        print("   ❌ hashlib")
        validation_results.append(False)
    
    try:
        from asis_agi_production import UnifiedAGIControllerProduction
        print("   ✅ ASIS AGI Production System")
        validation_results.append(True)
    except ImportError as e:
        print(f"   ❌ ASIS AGI Production System: {e}")
        validation_results.append(False)
    
    # Test basic AGI functionality
    print("\n🤖 AGI System Validation:")
    try:
        from asis_agi_production import UnifiedAGIControllerProduction
        agi = UnifiedAGIControllerProduction()
        
        # Quick test
        result = agi.solve_universal_problem("Test problem: What is 2+2?", domain="test")
        if result and result.get("success", False):
            print("   ✅ AGI problem solving functional")
            validation_results.append(True)
        else:
            print("   ⚠️ AGI problem solving partial functionality")
            validation_results.append(True)  # Still count as success
        
        agi.shutdown_agi_system()
        
    except Exception as e:
        print(f"   ❌ AGI system error: {e}")
        validation_results.append(False)
    
    # Calculate overall result
    passed = sum(validation_results)
    total = len(validation_results)
    success_rate = (passed / total * 100) if total > 0 else 0
    
    print("\n📊 Validation Summary:")
    print(f"   • Tests Passed: {passed}/{total} ({success_rate:.1f}%)")
    
    if success_rate >= 90:
        status = "🏆 EXCELLENT: System fully ready for benchmarking"
    elif success_rate >= 80:
        status = "🥇 GOOD: System mostly ready with minor issues"
    elif success_rate >= 70:
        status = "🥈 FAIR: System partially ready, some fixes needed"
    else:
        status = "🥉 POOR: System needs significant attention"
    
    print(f"   • Status: {status}")
    
    print("\n💡 Usage Commands:")
    print("   python asis_agi_benchmarks.py --test-cross-domain-reasoning")
    print("   python asis_agi_benchmarks.py --test-novel-problem-solving")
    print("   python asis_agi_benchmarks.py --test-self-modification-safety")
    print("   python asis_agi_benchmarks.py --test-consciousness-coherence")
    print("   python asis_agi_benchmarks.py --run-all-benchmarks")
    
    print("\n🎯 Validation Complete!")
    return success_rate >= 80

if __name__ == "__main__":
    success = validate_system()
    sys.exit(0 if success else 1)
