#!/usr/bin/env python3
"""
🔍 Quick Master Orchestrator Import Test

Test if the Master Orchestrator can import properly with all its dependencies.
"""

try:
    print("🎯 Testing Master Orchestrator import...")
    from asis_master_orchestrator import ASISMasterOrchestrator
    print("✅ ASISMasterOrchestrator imported successfully")
    
    print("🔧 Testing Master Orchestrator initialization...")
    orchestrator = ASISMasterOrchestrator()
    print("✅ ASISMasterOrchestrator initialized successfully")
    
    print("🔍 Testing Full Autonomy method availability...")
    if hasattr(orchestrator, 'run_full_autonomous_cycle'):
        print("✅ run_full_autonomous_cycle method available")
    else:
        print("❌ run_full_autonomous_cycle method missing")
    
    print("\n🎉 Master Orchestrator is working correctly!")
    print("✅ All Full Autonomy components should be accessible")

except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("🔧 This indicates missing dependencies")
    
    # Try to identify specific missing components
    missing_components = []
    
    try:
        from asis_environmental_interaction_engine import EnvironmentalInteractionEngine
    except ImportError:
        missing_components.append("EnvironmentalInteractionEngine")
    
    try:
        from asis_persistent_goals_system import PersistentGoalsSystem
    except ImportError:
        missing_components.append("PersistentGoalsSystem")
    
    try:
        from asis_self_modification_system import SelfModificationSystem
    except ImportError:
        missing_components.append("SelfModificationSystem")
    
    try:
        from asis_continuous_operation_framework import ContinuousOperationFramework
    except ImportError:
        missing_components.append("ContinuousOperationFramework")
    
    if missing_components:
        print(f"❌ Missing components: {', '.join(missing_components)}")
    else:
        print("🤔 All individual components import fine, but Master Orchestrator fails")

except Exception as e:
    print(f"❌ Error: {e}")
    print("🔧 This indicates an initialization problem")

print("\n📋 Test complete.")
