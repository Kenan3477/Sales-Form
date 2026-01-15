#!/usr/bin/env python3
"""
ASIS All Method Interface Fixes Test
===================================
Test all AGI engine method interface fixes
"""

import asyncio
from datetime import datetime

async def test_all_agi_methods():
    """Test all AGI engine method interfaces"""
    
    print("🔥 TESTING ALL AGI ENGINE METHOD INTERFACES")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Advanced AI Engine
    print("1. 🧠 Testing Advanced AI Engine...")
    try:
        from advanced_ai_engine import AdvancedAIEngine
        engine = AdvancedAIEngine()
        
        if hasattr(engine, 'process_query'):
            test_result = await engine.process_query("Test query", {"conversation_history": []})
            if isinstance(test_result, dict) and "response" in test_result:
                print("   ✅ process_query method: WORKING")
                results["advanced_ai"] = True
            else:
                print("   ❌ process_query method: INVALID RESPONSE")
                results["advanced_ai"] = False
        else:
            print("   ❌ process_query method: NOT FOUND")
            results["advanced_ai"] = False
    except Exception as e:
        print(f"   ❌ Advanced AI Engine error: {e}")
        results["advanced_ai"] = False
    
    # Test 2: Ethical Reasoning Engine
    print("\n2. ⚖️ Testing Ethical Reasoning Engine...")
    try:
        from asis_ethical_reasoning_engine import EthicalReasoningEngine
        engine = EthicalReasoningEngine()
        
        if hasattr(engine, 'analyze_ethical_implications'):
            test_situation = {"scenario": "test", "context": {}}
            test_result = await engine.analyze_ethical_implications(test_situation)
            if isinstance(test_result, dict) and "overall_ethical_score" in test_result:
                print("   ✅ analyze_ethical_implications method: WORKING")
                results["ethical_reasoning"] = True
            else:
                print("   ❌ analyze_ethical_implications method: INVALID RESPONSE")
                results["ethical_reasoning"] = False
        else:
            print("   ❌ analyze_ethical_implications method: NOT FOUND")
            results["ethical_reasoning"] = False
    except Exception as e:
        print(f"   ❌ Ethical Reasoning Engine error: {e}")
        results["ethical_reasoning"] = False
    
    # Test 3: Cross-Domain Reasoning Engine
    print("\n3. 🔄 Testing Cross-Domain Reasoning Engine...")
    try:
        from asis_cross_domain_reasoning_engine import CrossDomainReasoningEngine
        engine = CrossDomainReasoningEngine()
        
        if hasattr(engine, 'reason_across_domains'):
            test_result = await engine.reason_across_domains("biology", "technology", "adaptation")
            if isinstance(test_result, dict) and "reasoning_confidence" in test_result:
                print("   ✅ reason_across_domains method: WORKING")
                results["cross_domain"] = True
            else:
                print("   ❌ reason_across_domains method: INVALID RESPONSE")
                results["cross_domain"] = False
        else:
            print("   ❌ reason_across_domains method: NOT FOUND")
            results["cross_domain"] = False
    except Exception as e:
        print(f"   ❌ Cross-Domain Reasoning Engine error: {e}")
        results["cross_domain"] = False
    
    # Test 4: Novel Problem Solving Engine
    print("\n4. 🧩 Testing Novel Problem Solving Engine...")
    try:
        from asis_novel_problem_solving_engine import NovelProblemSolvingEngine
        engine = NovelProblemSolvingEngine()
        
        if hasattr(engine, 'solve_novel_problem'):
            test_result = await engine.solve_novel_problem("test problem", {})
            if isinstance(test_result, dict):
                print("   ✅ solve_novel_problem method: WORKING")
                results["novel_solving"] = True
            else:
                print("   ❌ solve_novel_problem method: INVALID RESPONSE")
                results["novel_solving"] = False
        else:
            print("   ❌ solve_novel_problem method: NOT FOUND")
            results["novel_solving"] = False
    except Exception as e:
        print(f"   ❌ Novel Problem Solving Engine error: {e}")
        results["novel_solving"] = False
    
    return results

async def main():
    print("🔥 ASIS ALL AGI ENGINE METHOD INTERFACE FIXES VALIDATION")
    print("=" * 70)
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all tests
    results = await test_all_agi_methods()
    
    # Summary
    print("\n" + "=" * 70)
    print("🎯 FINAL RESULTS")
    print("=" * 70)
    
    total_engines = len(results)
    working_engines = sum(results.values())
    
    print(f"AGI Engines Tested: {total_engines}")
    print(f"Methods Working: {working_engines}/{total_engines}")
    print(f"Success Rate: {working_engines/total_engines*100:.1f}%")
    
    print("\nDetailed Results:")
    for engine, working in results.items():
        status = "✅ WORKING" if working else "❌ FAILED"
        print(f"  - {engine}: {status}")
    
    if working_engines == total_engines:
        print("\n🎉 ALL METHOD INTERFACE FIXES SUCCESSFUL!")
        print("✅ All AGI engines have required methods")
        print("✅ All methods execute without errors")
        print("🚀 READY FOR FULL AGI CAPABILITY ASSESSMENT!")
        
        print("\n📋 Applied Fixes:")
        print("  ✅ Added process_query method to Advanced AI Engine")
        print("  ✅ Added analyze_ethical_implications method to Ethical Reasoning Engine")
        print("  ✅ Added reason_across_domains method to Cross-Domain Reasoning Engine")
        print("  ✅ Verified solve_novel_problem method in Novel Problem Solving Engine")
        
    elif working_engines > 0:
        print(f"\n⚠️ PARTIAL SUCCESS - {working_engines}/{total_engines} engines working")
        failed_engines = [engine for engine, working in results.items() if not working]
        print(f"Still need fixes: {', '.join(failed_engines)}")
        
    else:
        print("\n❌ ALL FIXES FAILED")
    
    print(f"\nValidation completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    asyncio.run(main())
