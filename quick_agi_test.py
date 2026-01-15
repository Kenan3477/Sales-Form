#!/usr/bin/env python3
"""
Quick AGI Method Test
====================
"""

def quick_test():
    print("🔥 QUICK AGI ENGINE METHOD TEST")
    print("=" * 40)
    
    results = []
    
    # Test Advanced AI Engine
    try:
        from advanced_ai_engine import AdvancedAIEngine
        engine = AdvancedAIEngine()
        if hasattr(engine, 'process_query'):
            results.append("✅ Advanced AI Engine: process_query")
        else:
            results.append("❌ Advanced AI Engine: missing process_query")
    except Exception as e:
        results.append(f"❌ Advanced AI Engine: {e}")
    
    # Test Ethical Reasoning Engine
    try:
        from asis_ethical_reasoning_engine import EthicalReasoningEngine
        engine = EthicalReasoningEngine()
        if hasattr(engine, 'analyze_ethical_implications'):
            results.append("✅ Ethical Engine: analyze_ethical_implications")
        else:
            results.append("❌ Ethical Engine: missing analyze_ethical_implications")
    except Exception as e:
        results.append(f"❌ Ethical Engine: {e}")
    
    # Test Cross-Domain Reasoning Engine
    try:
        from asis_cross_domain_reasoning_engine import CrossDomainReasoningEngine
        engine = CrossDomainReasoningEngine()
        if hasattr(engine, 'reason_across_domains'):
            results.append("✅ Cross-Domain Engine: reason_across_domains")
        else:
            results.append("❌ Cross-Domain Engine: missing reason_across_domains")
    except Exception as e:
        results.append(f"❌ Cross-Domain Engine: {e}")
    
    # Test Novel Problem Solving Engine
    try:
        from asis_novel_problem_solving_engine import NovelProblemSolvingEngine
        engine = NovelProblemSolvingEngine()
        if hasattr(engine, 'solve_novel_problem'):
            results.append("✅ Novel Solving Engine: solve_novel_problem")
        else:
            results.append("❌ Novel Solving Engine: missing solve_novel_problem")
    except Exception as e:
        results.append(f"❌ Novel Solving Engine: {e}")
    
    # Show results
    for result in results:
        print(result)
    
    success_count = sum(1 for r in results if r.startswith("✅"))
    print(f"\n🎯 RESULT: {success_count}/4 engines have required methods")
    
    if success_count == 4:
        print("🎉 ALL METHOD INTERFACE FIXES SUCCESSFUL!")
    elif success_count > 0:
        print("⚠️ PARTIAL SUCCESS - Some fixes still needed")
    else:
        print("❌ ALL FIXES FAILED")

if __name__ == "__main__":
    quick_test()
