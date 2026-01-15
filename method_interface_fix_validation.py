#!/usr/bin/env python3
"""
ASIS Method Interface Fix Validation
===================================
Test all AGI engine method interface fixes
"""

import asyncio
import json
from datetime import datetime
import traceback

def test_advanced_ai_engine():
    """Test Advanced AI Engine process_query method"""
    print("🔥 Testing Advanced AI Engine...")
    
    try:
        from advanced_ai_engine import AdvancedAIEngine
        engine = AdvancedAIEngine()
        
        if hasattr(engine, 'process_query'):
            print("   ✅ process_query method found")
            return True, "process_query method available"
        else:
            print("   ❌ process_query method missing")
            return False, "process_query method not found"
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False, str(e)

def test_ethical_reasoning_engine():
    """Test Ethical Reasoning Engine analyze_ethical_implications method"""
    print("⚖️ Testing Ethical Reasoning Engine...")
    
    try:
        from asis_ethical_reasoning_engine import EthicalReasoningEngine
        engine = EthicalReasoningEngine()
        
        if hasattr(engine, 'analyze_ethical_implications'):
            print("   ✅ analyze_ethical_implications method found")
            return True, "analyze_ethical_implications method available"
        else:
            print("   ❌ analyze_ethical_implications method missing")
            return False, "analyze_ethical_implications method not found"
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False, str(e)

def test_cross_domain_reasoning_engine():
    """Test Cross-Domain Reasoning Engine reason_across_domains method"""
    print("🔄 Testing Cross-Domain Reasoning Engine...")
    
    try:
        from asis_cross_domain_reasoning_engine import CrossDomainReasoningEngine
        engine = CrossDomainReasoningEngine()
        
        if hasattr(engine, 'reason_across_domains'):
            print("   ✅ reason_across_domains method found")
            return True, "reason_across_domains method available"
        else:
            print("   ❌ reason_across_domains method missing")
            return False, "reason_across_domains method not found"
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False, str(e)

def test_novel_problem_solving_engine():
    """Test Novel Problem Solving Engine solve_novel_problem method"""
    print("🧩 Testing Novel Problem Solving Engine...")
    
    try:
        from asis_novel_problem_solving_engine import NovelProblemSolvingEngine
        engine = NovelProblemSolvingEngine()
        
        if hasattr(engine, 'solve_novel_problem'):
            print("   ✅ solve_novel_problem method found")
            return True, "solve_novel_problem method available"
        else:
            print("   ❌ solve_novel_problem method missing")
            return False, "solve_novel_problem method not found"
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False, str(e)

async def test_method_execution():
    """Test actual method execution for all engines"""
    print("\n🚀 Testing Method Execution...")
    
    results = {}
    
    # Test Advanced AI Engine
    try:
        from advanced_ai_engine import AdvancedAIEngine
        engine = AdvancedAIEngine()
        
        if hasattr(engine, 'process_query'):
            result = await engine.process_query("Test query", {"conversation_history": []})
            if isinstance(result, dict) and "response" in result:
                print("   ✅ Advanced AI Engine: process_query execution successful")
                results["advanced_ai"] = True
            else:
                print("   ❌ Advanced AI Engine: process_query returned invalid format")
                results["advanced_ai"] = False
        else:
            results["advanced_ai"] = False
    except Exception as e:
        print(f"   ❌ Advanced AI Engine execution error: {e}")
        results["advanced_ai"] = False
    
    # Test Ethical Reasoning Engine
    try:
        from asis_ethical_reasoning_engine import EthicalReasoningEngine
        engine = EthicalReasoningEngine()
        
        if hasattr(engine, 'analyze_ethical_implications'):
            test_situation = {"scenario": "test", "context": {}}
            result = await engine.analyze_ethical_implications(test_situation)
            if isinstance(result, dict):
                print("   ✅ Ethical Reasoning Engine: analyze_ethical_implications execution successful")
                results["ethical"] = True
            else:
                print("   ❌ Ethical Reasoning Engine: analyze_ethical_implications returned invalid format")
                results["ethical"] = False
        else:
            results["ethical"] = False
    except Exception as e:
        print(f"   ❌ Ethical Reasoning Engine execution error: {e}")
        results["ethical"] = False
    
    # Test Cross-Domain Reasoning Engine
    try:
        from asis_cross_domain_reasoning_engine import CrossDomainReasoningEngine
        engine = CrossDomainReasoningEngine()
        
        if hasattr(engine, 'reason_across_domains'):
            result = await engine.reason_across_domains("source", "target", "concept")
            if isinstance(result, dict):
                print("   ✅ Cross-Domain Reasoning Engine: reason_across_domains execution successful")
                results["cross_domain"] = True
            else:
                print("   ❌ Cross-Domain Reasoning Engine: reason_across_domains returned invalid format")
                results["cross_domain"] = False
        else:
            results["cross_domain"] = False
    except Exception as e:
        print(f"   ❌ Cross-Domain Reasoning Engine execution error: {e}")
        results["cross_domain"] = False
    
    # Test Novel Problem Solving Engine
    try:
        from asis_novel_problem_solving_engine import NovelProblemSolvingEngine
        engine = NovelProblemSolvingEngine()
        
        if hasattr(engine, 'solve_novel_problem'):
            result = await engine.solve_novel_problem("test problem", {})
            if isinstance(result, dict):
                print("   ✅ Novel Problem Solving Engine: solve_novel_problem execution successful")
                results["novel_solving"] = True
            else:
                print("   ❌ Novel Problem Solving Engine: solve_novel_problem returned invalid format")
                results["novel_solving"] = False
        else:
            results["novel_solving"] = False
    except Exception as e:
        print(f"   ❌ Novel Problem Solving Engine execution error: {e}")
        results["novel_solving"] = False
    
    return results

def main():
    print("🔥 ASIS METHOD INTERFACE FIX VALIDATION")
    print("=" * 60)
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test method availability
    print("📋 TESTING METHOD AVAILABILITY")
    print("-" * 40)
    
    test_results = {}
    
    # Test each engine
    engines = [
        ("Advanced AI Engine", test_advanced_ai_engine),
        ("Ethical Reasoning Engine", test_ethical_reasoning_engine),
        ("Cross-Domain Reasoning Engine", test_cross_domain_reasoning_engine),
        ("Novel Problem Solving Engine", test_novel_problem_solving_engine),
    ]
    
    for engine_name, test_func in engines:
        success, message = test_func()
        test_results[engine_name] = success
    
    # Test method execution
    print("\n⚡ TESTING METHOD EXECUTION")
    print("-" * 40)
    
    execution_results = asyncio.run(test_method_execution())
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎯 VALIDATION SUMMARY")
    print("=" * 60)
    
    method_success_count = sum(test_results.values())
    execution_success_count = sum(execution_results.values())
    
    print(f"Method Availability: {method_success_count}/{len(test_results)} engines have required methods")
    print(f"Method Execution: {execution_success_count}/{len(execution_results)} engines execute successfully")
    
    if method_success_count == len(test_results) and execution_success_count == len(execution_results):
        print("\n🎉 ALL METHOD INTERFACE FIXES SUCCESSFUL!")
        print("✅ All AGI engines have required methods")
        print("✅ All methods execute without errors")
        print("🚀 Ready for full AGI capability assessment")
        
        # Save successful results
        results = {
            "validation_date": datetime.now().isoformat(),
            "method_availability": test_results,
            "method_execution": execution_results,
            "overall_success": True,
            "fixes_applied": [
                "Added process_query method to Advanced AI Engine",
                "Verified analyze_ethical_implications in Ethical Reasoning Engine",
                "Verified reason_across_domains in Cross-Domain Reasoning Engine",
                "Verified solve_novel_problem in Novel Problem Solving Engine"
            ]
        }
        
        with open("method_interface_fix_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Results saved to: method_interface_fix_results.json")
        
    elif method_success_count > 0:
        print(f"\n⚠️ PARTIAL SUCCESS - {method_success_count}/{len(test_results)} methods available")
        
        # Show which engines still need fixes
        for engine_name, success in test_results.items():
            if not success:
                print(f"❌ {engine_name}: Still needs method interface fix")
        
    else:
        print("\n❌ ALL FIXES FAILED")
        print("❌ No AGI engines have proper method interfaces")
    
    print(f"\nValidation completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
