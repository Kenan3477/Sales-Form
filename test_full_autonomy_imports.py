#!/usr/bin/env python3
"""
🔍 Full Autonomy Components Import Test

Test each Full Autonomy component import individually to identify any issues.
"""

def test_imports():
    """Test each import individually with detailed error reporting."""
    
    print("🔍 TESTING FULL AUTONOMY COMPONENT IMPORTS")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Environmental Interaction Engine
    try:
        print("🌍 Testing EnvironmentalInteractionEngine import...")
        from asis_environmental_interaction_engine import EnvironmentalInteractionEngine
        print("✅ EnvironmentalInteractionEngine imported successfully")
        
        # Test instantiation
        engine = EnvironmentalInteractionEngine()
        print(f"✅ Engine initialized: {engine.name}")
        results['environmental'] = True
        
    except ImportError as e:
        print(f"❌ Import Error for EnvironmentalInteractionEngine: {e}")
        results['environmental'] = False
    except Exception as e:
        print(f"❌ Error with EnvironmentalInteractionEngine: {e}")
        results['environmental'] = False
    
    print()
    
    # Test 2: Persistent Goals System
    try:
        print("🎯 Testing PersistentGoalsSystem import...")
        from asis_persistent_goals_system import PersistentGoalsSystem
        print("✅ PersistentGoalsSystem imported successfully")
        
        # Test instantiation
        goals = PersistentGoalsSystem()
        print(f"✅ Goals system initialized: {goals.name}")
        results['goals'] = True
        
    except ImportError as e:
        print(f"❌ Import Error for PersistentGoalsSystem: {e}")
        results['goals'] = False
    except Exception as e:
        print(f"❌ Error with PersistentGoalsSystem: {e}")
        results['goals'] = False
    
    print()
    
    # Test 3: Self Modification System
    try:
        print("🔧 Testing SelfModificationSystem import...")
        from asis_self_modification_system import SelfModificationSystem
        print("✅ SelfModificationSystem imported successfully")
        
        # Test instantiation
        modifier = SelfModificationSystem()
        print(f"✅ Self-modification system initialized: {modifier.name}")
        results['self_modification'] = True
        
    except ImportError as e:
        print(f"❌ Import Error for SelfModificationSystem: {e}")
        results['self_modification'] = False
    except Exception as e:
        print(f"❌ Error with SelfModificationSystem: {e}")
        results['self_modification'] = False
    
    print()
    
    # Test 4: Continuous Operation Framework
    try:
        print("⚡ Testing ContinuousOperationFramework import...")
        from asis_continuous_operation_framework import ContinuousOperationFramework
        print("✅ ContinuousOperationFramework imported successfully")
        
        # Test instantiation
        framework = ContinuousOperationFramework()
        print(f"✅ Continuous operation framework initialized: {framework.name}")
        results['continuous'] = True
        
    except ImportError as e:
        print(f"❌ Import Error for ContinuousOperationFramework: {e}")
        results['continuous'] = False
    except Exception as e:
        print(f"❌ Error with ContinuousOperationFramework: {e}")
        results['continuous'] = False
    
    print()
    print("=" * 60)
    print("📊 IMPORT TEST RESULTS")
    print("=" * 60)
    
    for component, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{component.replace('_', ' ').title()}: {status}")
    
    success_count = sum(1 for success in results.values() if success)
    total_count = len(results)
    
    print(f"\n🎯 Overall Success Rate: {success_count}/{total_count} ({success_count/total_count:.1%})")
    
    if success_count == total_count:
        print("🎉 ALL COMPONENTS IMPORTED SUCCESSFULLY!")
        print("✅ Full Autonomy components are ready for use!")
        return True
    else:
        print("⚠️ Some components failed to import.")
        print("🔧 Check the error messages above for details.")
        return False

if __name__ == "__main__":
    success = test_imports()
    print(f"\n{'🚀 READY FOR FULL AUTONOMY!' if success else '🛠️ COMPONENTS NEED ATTENTION'}")
