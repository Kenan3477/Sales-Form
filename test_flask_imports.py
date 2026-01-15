#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick test to verify Flask AGI imports work correctly
"""

def test_flask_imports():
    """Test that Flask AGI imports work"""
    print("🧪 Testing Flask AGI Import Fixes...")
    
    try:
        # Test the production AGI import
        from asis_agi_production import UnifiedAGIControllerProduction
        print("✅ Production AGI import successful")
        
        # Test initialization
        agi = UnifiedAGIControllerProduction()
        print("✅ Production AGI initialization successful")
        
        # Test basic functionality
        status = agi.get_agi_system_status()
        if "error" not in status:
            print("✅ AGI system status check successful")
            print(f"   • Consciousness Level: {status['system_status']['consciousness_level']:.2f}")
        
        # Clean shutdown
        agi.shutdown_agi_system()
        print("✅ AGI system shutdown successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Flask AGI import test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_flask_imports()
    if success:
        print("\n🎉 Flask AGI imports are now fixed and ready!")
        print("You can now run: python asis_agi_flask_enhanced.py")
    else:
        print("\n❌ Import issues still exist")
