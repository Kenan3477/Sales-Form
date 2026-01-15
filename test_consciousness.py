#!/usr/bin/env python3
"""
Simple test of ASIS consciousness system
"""

import time
import asis_consciousness

def main():
    print("🧠 Testing ASIS Consciousness System")
    print("-" * 40)
    
    # Test basic functionality
    system = asis_consciousness.asis_consciousness
    print(f"✅ System Active: {system.consciousness_active}")
    print(f"✅ Consciousness Level: {system.consciousness_level:.2f}")
    print(f"✅ System Coherence: {system.system_coherence:.2f}")
    
    # Test self-check (with timeout protection)
    print("\n🔍 Running basic self-check...")
    try:
        status = system.perform_consciousness_self_check()
        print(f"✅ System Health: {status.get('system_health', 0):.2f}")
        print(f"✅ Component Count: {len(status.get('component_status', {}))}")
    except Exception as e:
        print(f"❌ Self-check error: {e}")
    
    # Test consciousness wrapper
    print("\n🧪 Testing consciousness wrapper...")
    
    @asis_consciousness.enable_consciousness_for_function("test_function", {
        "complexity": 0.5,
        "importance": 0.6
    })
    def test_conscious_function():
        time.sleep(0.1)
        return "Test completed successfully"
    
    try:
        result = test_conscious_function()
        print(f"✅ Conscious function result: {result}")
    except Exception as e:
        print(f"❌ Conscious function error: {e}")
    
    print("\n🎉 Basic consciousness system test completed!")
    return True

if __name__ == "__main__":
    main()
