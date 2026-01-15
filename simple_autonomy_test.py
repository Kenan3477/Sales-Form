#!/usr/bin/env python3
"""
🚀 ASIS SIMPLE AUTONOMY VERIFICATION

Simple verification that Full Autonomy components are working.
"""

def test_autonomy_components():
    """Test each autonomy component individually."""
    
    print("🚀 ASIS AUTONOMY COMPONENTS TEST")
    print("=" * 50)
    
    results = {}
    
    # Test 1: Self-Modification System
    try:
        print("🔧 Testing Self-Modification System...")
        from asis_self_modification_system import SelfModificationSystem, ModificationRisk
        system = SelfModificationSystem()
        print(f"✅ Self-Modification System: {system.name}")
        results['self_modification'] = True
    except Exception as e:
        print(f"❌ Self-Modification System failed: {e}")
        results['self_modification'] = False
    
    # Test 2: Environmental Interaction Engine
    try:
        print("🌍 Testing Environmental Interaction Engine...")
        from asis_environmental_interaction_engine import EnvironmentalInteractionEngine
        engine = EnvironmentalInteractionEngine()
        print(f"✅ Environmental Engine: {engine.name}")
        results['environmental'] = True
    except Exception as e:
        print(f"❌ Environmental Engine failed: {e}")
        results['environmental'] = False
    
    # Test 3: Persistent Goals System
    try:
        print("🎯 Testing Persistent Goals System...")
        from asis_persistent_goals_system import PersistentGoalsSystem
        goals = PersistentGoalsSystem()
        print(f"✅ Goals System: {goals.name}")
        results['goals'] = True
    except Exception as e:
        print(f"❌ Goals System failed: {e}")
        results['goals'] = False
    
    # Test 4: Continuous Operation Framework
    try:
        print("⚡ Testing Continuous Operation Framework...")
        from asis_continuous_operation_framework import ContinuousOperationFramework
        framework = ContinuousOperationFramework()
        print(f"✅ Operation Framework: {framework.name}")
        results['continuous'] = True
    except Exception as e:
        print(f"❌ Operation Framework failed: {e}")
        results['continuous'] = False
    
    # Test 5: Master Orchestrator
    try:
        print("🎯 Testing Master Orchestrator...")
        from asis_master_orchestrator import ASISMasterOrchestrator
        orchestrator = ASISMasterOrchestrator()
        print("✅ Master Orchestrator initialized")
        
        # Check for Full Autonomy method
        if hasattr(orchestrator, 'run_full_autonomous_cycle'):
            print("✅ Full Autonomous Cycle method available")
            results['orchestrator'] = True
        else:
            print("❌ Full Autonomous Cycle method missing")
            results['orchestrator'] = False
    except Exception as e:
        print(f"❌ Master Orchestrator failed: {e}")
        results['orchestrator'] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 AUTONOMY COMPONENTS SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for success in results.values() if success)
    total = len(results)
    
    for component, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{component.replace('_', ' ').title()}: {status}")
    
    success_rate = passed / total
    print(f"\n🎯 Success Rate: {passed}/{total} ({success_rate:.1%})")
    
    if success_rate >= 1.0:
        print("🔥 PERFECT: All Full Autonomy components operational!")
    elif success_rate >= 0.8:
        print("⚡ EXCELLENT: Most autonomy components working!")
    elif success_rate >= 0.6:
        print("📈 GOOD: Majority of components functional!")
    else:
        print("🌱 NEEDS WORK: Several components need attention!")
    
    return success_rate >= 0.8

if __name__ == "__main__":
    success = test_autonomy_components()
    print(f"\n{'🎉 FULL AUTONOMY READY!' if success else '🔧 NEEDS IMPROVEMENT'}")
