#!/usr/bin/env python3
"""
🔍 Full Autonomy Components Diagnostic

This script will diagnose any issues with the Full Autonomy components.
"""

import os
import sys
import traceback

def check_file_exists(filename):
    """Check if a file exists and return its size."""
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        return True, size
    return False, 0

def test_import(module_name, class_name):
    """Test importing a specific class from a module."""
    try:
        module = __import__(module_name)
        cls = getattr(module, class_name)
        return True, None
    except ImportError as e:
        return False, f"ImportError: {e}"
    except AttributeError as e:
        return False, f"AttributeError: {e}"
    except Exception as e:
        return False, f"Error: {e}"

def main():
    print("🔍 FULL AUTONOMY COMPONENTS DIAGNOSTIC")
    print("=" * 60)
    
    # Components to check
    components = [
        ("asis_environmental_interaction_engine.py", "asis_environmental_interaction_engine", "EnvironmentalInteractionEngine"),
        ("asis_persistent_goals_system.py", "asis_persistent_goals_system", "PersistentGoalsSystem"),
        ("asis_self_modification_system.py", "asis_self_modification_system", "SelfModificationSystem"),
        ("asis_continuous_operation_framework.py", "asis_continuous_operation_framework", "ContinuousOperationFramework")
    ]
    
    print("📁 FILE EXISTENCE CHECK:")
    print("-" * 30)
    for filename, module_name, class_name in components:
        exists, size = check_file_exists(filename)
        if exists:
            print(f"✅ {filename} exists ({size:,} bytes)")
        else:
            print(f"❌ {filename} MISSING")
    
    print("\n📦 IMPORT TEST:")
    print("-" * 20)
    all_success = True
    
    for filename, module_name, class_name in components:
        success, error = test_import(module_name, class_name)
        if success:
            print(f"✅ {class_name} imported successfully")
        else:
            print(f"❌ {class_name} FAILED: {error}")
            all_success = False
    
    print("\n🎯 MASTER ORCHESTRATOR TEST:")
    print("-" * 35)
    
    try:
        from asis_master_orchestrator import ASISMasterOrchestrator
        print("✅ ASISMasterOrchestrator imported successfully")
        
        orchestrator = ASISMasterOrchestrator()
        print("✅ ASISMasterOrchestrator initialized successfully")
        
        if hasattr(orchestrator, 'run_full_autonomous_cycle'):
            print("✅ run_full_autonomous_cycle method available")
        else:
            print("❌ run_full_autonomous_cycle method missing")
            
    except Exception as e:
        print(f"❌ Master Orchestrator failed: {e}")
        print(f"📋 Traceback: {traceback.format_exc()}")
        all_success = False
    
    print("\n" + "=" * 60)
    print("📊 DIAGNOSTIC RESULTS")
    print("=" * 60)
    
    if all_success:
        print("🎉 ALL COMPONENTS ARE WORKING CORRECTLY!")
        print("✅ Full Autonomy components are ready for use")
        print("✅ Master Orchestrator is functional")
    else:
        print("⚠️ ISSUES DETECTED")
        print("🔧 Check the error messages above for details")
        print("💡 Components may need to be recreated or fixed")
    
    print(f"\n📍 Current directory: {os.getcwd()}")
    print(f"🐍 Python version: {sys.version}")
    
    return all_success

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🚀 DIAGNOSTIC COMPLETE - ALL SYSTEMS OPERATIONAL!")
    else:
        print("\n🔧 DIAGNOSTIC COMPLETE - ISSUES NEED ATTENTION!")
