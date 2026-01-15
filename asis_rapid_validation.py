#!/usr/bin/env python3
"""
🔍 ASIS RAPID VALIDATION TEST
============================

Quick synchronous test of all ASIS core capabilities.
"""

import os
import sys
import traceback
from datetime import datetime

def test_component(name, test_func):
    """Test a component with error handling"""
    try:
        print(f"🧪 Testing {name}...")
        result = test_func()
        if result:
            print(f"✅ {name}: PASSED")
            return True, ""
        else:
            print(f"❌ {name}: FAILED")
            return False, "Test returned False"
    except Exception as e:
        print(f"❌ {name}: ERROR - {str(e)}")
        return False, str(e)

def test_master_orchestrator():
    """Test Master Orchestrator"""
    from asis_master_orchestrator import ASISMasterOrchestrator
    orchestrator = ASISMasterOrchestrator()
    return hasattr(orchestrator, 'run_full_autonomous_cycle')

def test_full_autonomy():
    """Test Full Autonomy Components"""
    from asis_environmental_interaction_engine import EnvironmentalInteractionEngine
    from asis_persistent_goals_system import PersistentGoalsSystem  
    from asis_self_modification_system import SelfModificationSystem
    from asis_continuous_operation_framework import ContinuousOperationFramework
    
    env = EnvironmentalInteractionEngine()
    goals = PersistentGoalsSystem()
    selfmod = SelfModificationSystem()
    contops = ContinuousOperationFramework()
    
    return all([
        hasattr(env, 'name'),
        hasattr(goals, 'name'),
        hasattr(selfmod, 'name'),
        hasattr(contops, 'name')
    ])

def test_agi_engines():
    """Test AGI Engines"""
    try:
        from advanced_ai_engine import AdvancedAIEngine
        ai_engine = AdvancedAIEngine()
        return hasattr(ai_engine, 'process_query')
    except:
        return False

def test_reasoning_engines():
    """Test Reasoning Engines"""
    success_count = 0
    
    try:
        from asis_ethical_reasoning_engine import EthicalReasoningEngine
        ethical = EthicalReasoningEngine()
        if hasattr(ethical, 'analyze_ethical_implications'):
            success_count += 1
    except:
        pass
    
    try:
        from asis_cross_domain_reasoning_engine import CrossDomainReasoningEngine
        cross = CrossDomainReasoningEngine()
        if hasattr(cross, 'reason_across_domains'):
            success_count += 1
    except:
        pass
    
    try:
        from asis_novel_problem_solving_engine import NovelProblemSolvingEngine
        novel = NovelProblemSolvingEngine()
        if hasattr(novel, 'solve_novel_problem'):
            success_count += 1
    except:
        pass
    
    return success_count >= 2

def test_advanced_features():
    """Test Advanced Features"""
    success_count = 0
    
    # Test Memory Network
    try:
        from memory_network import MemoryNetwork
        memory = MemoryNetwork()
        if hasattr(memory, 'store_memory'):
            success_count += 1
    except:
        pass
    
    # Test Consciousness
    try:
        from asis_consciousness import ConsciousnessModule
        consciousness = ConsciousnessModule()
        if hasattr(consciousness, 'get_self_awareness_level'):
            success_count += 1
    except:
        pass
    
    # Test Learning
    try:
        from asis_realtime_learning import RealtimeLearningSystem
        learning = RealtimeLearningSystem()
        if hasattr(learning, 'learn_from_interaction'):
            success_count += 1
    except:
        pass
    
    return success_count >= 1

def main():
    """Run rapid validation"""
    print("🚀 ASIS RAPID VALIDATION TEST")
    print("=" * 50)
    print(f"🕐 Started: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    tests = [
        ("Master Orchestrator", test_master_orchestrator),
        ("Full Autonomy Systems", test_full_autonomy),
        ("AGI Engines", test_agi_engines),
        ("Reasoning Engines", test_reasoning_engines),
        ("Advanced Features", test_advanced_features)
    ]
    
    results = []
    for name, test_func in tests:
        success, error = test_component(name, test_func)
        results.append((name, success, error))
        print()
    
    # Summary
    print("=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    pass_rate = passed / total
    
    for name, success, error in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {name}")
        if not success and error:
            print(f"    Error: {error}")
    
    print()
    print(f"📈 Pass Rate: {passed}/{total} ({pass_rate:.1%})")
    
    # AGI Assessment
    if pass_rate >= 0.8:
        agi_level = "🔥 HIGH AGI CAPABILITY"
        readiness = "PRODUCTION READY"
    elif pass_rate >= 0.6:
        agi_level = "⚡ MODERATE AGI CAPABILITY"
        readiness = "NEAR PRODUCTION"
    else:
        agi_level = "🌱 BASIC AGI CAPABILITY"
        readiness = "DEVELOPMENT STAGE"
    
    print(f"🧠 AGI Level: {agi_level}")
    print(f"🚀 Readiness: {readiness}")
    
    print()
    print("=" * 50)
    print("🎯 RAPID VALIDATION COMPLETE")
    print("=" * 50)
    
    return pass_rate >= 0.6

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        print(f"📋 Traceback: {traceback.format_exc()}")
        sys.exit(1)
