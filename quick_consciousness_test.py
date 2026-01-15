#!/usr/bin/env python3
"""
Quick consciousness system test
"""

import asis_consciousness
import time

print("🧠 Quick Consciousness Test")
print("-" * 30)

# Get the consciousness system
system = asis_consciousness.asis_consciousness

print(f"✅ System Active: {system.consciousness_active}")
print(f"✅ Consciousness Level: {system.consciousness_level:.2f}")

# Test the consciousness wrapper
@asis_consciousness.enable_consciousness_for_function("quick_test", {
    "complexity": 0.3,
    "importance": 0.5
})
def quick_test():
    return "Quick test successful"

print("\n🧪 Testing consciousness wrapper...")
result = quick_test()
print(f"✅ Result: {result}")

print("\n🎉 Test completed!")
