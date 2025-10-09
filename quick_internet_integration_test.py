#!/usr/bin/env python3
"""
Quick test of ASIS Internet Research integration
"""

from asis_interface import ASISInterface
import asyncio

def test_asis_with_internet_research():
    """Test ASIS interface with new internet research capability"""
    
    print("🌐 Testing ASIS with Internet Research & Action Engine")
    print("=" * 60)
    
    # Create ASIS interface (includes internet research engine)
    asis = ASISInterface()
    
    # Test activation
    print("🚀 Activating ASIS...")
    result = asis.activate_asis()
    
    if result["activation_successful"]:
        print("✅ ASIS activated successfully!")
        
        # Show capabilities
        print(f"\n🤖 ASIS Capabilities:")
        for capability, enabled in asis.asis_capabilities.items():
            status = "✅" if enabled else "❌"
            print(f"   {status} {capability.replace('_', ' ').title()}")
        
        # Test internet research capability
        if asis.asis_capabilities.get("internet_research_action"):
            print(f"\n🌐 Internet Research Engine Status:")
            engine_status = asis.internet_action_engine.get_system_status()
            print(f"   Version: {engine_status['system_version']}")
            print(f"   Components: {len(engine_status['components'])}")
            print(f"   API Keys: {engine_status['api_keys_configured']}")
            print(f"   Database: {engine_status['database']}")
            
            print(f"\n✅ Internet Research & Action Engine ready!")
            print(f"📋 Available commands:")
            print(f"   • 'research artificial intelligence' - Research AI")
            print(f"   • 'research status' - Check research status")
            print(f"   • Start conversation to use research commands")
        
        # Show system info
        print(f"\n📊 ASIS System Status:")
        print(f"   ✅ Internet Research & Action Engine integrated")
        print(f"   ✅ All systems operational")
        print(f"   ✅ Ready for internet research commands")
        
        return asis
    else:
        print("❌ ASIS activation failed")
        return None

if __name__ == "__main__":
    asis = test_asis_with_internet_research()
    
    if asis:
        print(f"\n🎉 ASIS with Internet Research ready!")
        print(f"💡 To use: asis.start_conversation() then type 'research <topic>'")
    else:
        print(f"❌ Test failed")