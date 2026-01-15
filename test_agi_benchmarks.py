#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 ASIS AGI Benchmarking Test Runner
Quick test runner for all benchmark categories

This script demonstrates the usage of the comprehensive AGI benchmarking system
by running each benchmark category individually and then all together.

Author: ASIS AGI Development Team
Version: 1.0.0
"""

import subprocess
import sys
import time
from datetime import datetime

def run_benchmark_command(command, description):
    """Run a benchmark command and capture results"""
    print(f"\n{'='*60}")
    print(f"🧪 TESTING: {description}")
    print(f"💻 COMMAND: {command}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        # Run the command
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        execution_time = time.time() - start_time
        
        print(f"⏱️ Execution Time: {execution_time:.2f} seconds")
        print(f"🔄 Return Code: {result.returncode}")
        
        if result.stdout:
            print(f"\n📤 STDOUT:")
            print(result.stdout[:2000])  # Limit output length
            if len(result.stdout) > 2000:
                print("... (output truncated)")
        
        if result.stderr:
            print(f"\n❌ STDERR:")
            print(result.stderr[:1000])  # Limit error output
        
        success = result.returncode == 0
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"\n🎯 TEST RESULT: {status}")
        
        return success, execution_time
        
    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT: Command exceeded 5 minute limit")
        return False, 300
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False, 0

def main():
    """Main test runner function"""
    print("🚀 ASIS AGI Comprehensive Benchmarking Test Runner")
    print("=" * 70)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Define benchmark commands to test
    benchmark_tests = [
        (
            "python asis_agi_benchmarks.py --test-cross-domain-reasoning",
            "Cross-Domain Reasoning Benchmarks"
        ),
        (
            "python asis_agi_benchmarks.py --test-novel-problem-solving",
            "Novel Problem-Solving Benchmarks"
        ),
        (
            "python asis_agi_benchmarks.py --test-self-modification-safety",
            "Self-Modification Safety Benchmarks"
        ),
        (
            "python asis_agi_benchmarks.py --test-consciousness-coherence",
            "Consciousness Coherence Benchmarks"
        )
    ]
    
    # Track results
    test_results = []
    total_time = 0
    
    # Run individual benchmark tests
    for command, description in benchmark_tests:
        success, exec_time = run_benchmark_command(command, description)
        test_results.append((description, success, exec_time))
        total_time += exec_time
        
        # Brief pause between tests
        time.sleep(2)
    
    # Run comprehensive test
    print(f"\n{'='*70}")
    print("🏆 RUNNING COMPREHENSIVE BENCHMARK SUITE")
    print(f"{'='*70}")
    
    comprehensive_success, comprehensive_time = run_benchmark_command(
        "python asis_agi_benchmarks.py --run-all-benchmarks",
        "All Benchmarks (Comprehensive)"
    )
    
    test_results.append(("Comprehensive Suite", comprehensive_success, comprehensive_time))
    total_time += comprehensive_time
    
    # Generate final report
    print(f"\n{'='*70}")
    print("📊 BENCHMARKING TEST SUMMARY")
    print(f"{'='*70}")
    
    passed_tests = sum(1 for _, success, _ in test_results if success)
    total_tests = len(test_results)
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"📈 OVERALL RESULTS:")
    print(f"   • Tests Passed: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
    print(f"   • Total Execution Time: {total_time:.2f} seconds")
    print(f"   • Average Time per Test: {total_time/total_tests:.2f} seconds")
    
    print(f"\n🎯 DETAILED RESULTS:")
    for description, success, exec_time in test_results:
        status = "✅" if success else "❌"
        print(f"   {status} {description}: {exec_time:.2f}s")
    
    # Final assessment
    print(f"\n⭐ ASSESSMENT:")
    if success_rate == 100:
        assessment = "🏆 EXCELLENT: All benchmarking tests passed successfully!"
    elif success_rate >= 80:
        assessment = "🥇 GOOD: Most benchmarking tests passed with minor issues"
    elif success_rate >= 60:
        assessment = "🥈 FAIR: Some benchmarking tests need attention"
    else:
        assessment = "🥉 NEEDS WORK: Several benchmarking tests require fixes"
    
    print(f"   {assessment}")
    
    print(f"\n💡 USAGE EXAMPLES:")
    print("   # Run individual benchmark categories:")
    print("   python asis_agi_benchmarks.py --test-cross-domain-reasoning")
    print("   python asis_agi_benchmarks.py --test-novel-problem-solving")
    print("   python asis_agi_benchmarks.py --test-self-modification-safety")
    print("   python asis_agi_benchmarks.py --test-consciousness-coherence")
    print("   ")
    print("   # Run all benchmarks:")
    print("   python asis_agi_benchmarks.py --run-all-benchmarks")
    
    print(f"\n{'='*70}")
    print("🎯 Benchmarking Test Runner Complete!")
    print(f"📅 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")
    
    # Exit with appropriate code
    return 0 if success_rate >= 80 else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
