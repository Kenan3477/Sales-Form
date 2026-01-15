#!/usr/bin/env python3

print("🔍 Testing ASIS Agent Integration")
print("=" * 50)

try:
    # Test import
    print("Importing ASIS Interface...")
    from asis_interface import ASISInterface
    print("✅ Import successful")
    
    # Test initialization
    print("Initializing interface...")
    asis = ASISInterface()
    print("✅ Interface initialized")
    
    # Test agent system
    print("Checking agent system...")
    if hasattr(asis, 'agent_system') and asis.agent_system:
        print("✅ ChatGPT Agent system ACTIVE")
        print("🎯 INTEGRATION SUCCESS!")
    else:
        print("❌ Agent system not available")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\nTest complete!")
