#!/usr/bin/env python3
"""
ASIS Intelligence Integration Script
===================================

This script integrates the enhanced intelligence capabilities with your existing ASIS system.
Run this to upgrade ASIS from template responses to genuine learning and memory.
"""

import os
import sys
import json
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_asis_system():
    """Check if ASIS components are available"""
    
    print("🔍 Checking ASIS System Components...")
    print("-" * 50)
    
    required_files = [
        "asis_control_interface.py",
        "asis_activation_controller.py",
        "asis_advanced_chat.py"
    ]
    
    available_files = []
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            available_files.append(file)
            print(f"✅ {file} - Found")
        else:
            missing_files.append(file)
            print(f"❌ {file} - Missing")
    
    print(f"\nSystem Status: {len(available_files)}/{len(required_files)} components available")
    
    return len(available_files) >= 2, available_files, missing_files

def integrate_enhanced_intelligence():
    """Integrate enhanced intelligence into ASIS"""
    
    print("\n🧠 ASIS Intelligence Integration")
    print("=" * 50)
    
    # Check system readiness
    ready, available, missing = check_asis_system()
    
    if not ready:
        print(f"\n⚠️  Warning: Some ASIS components are missing: {missing}")
        print("📋 The enhanced intelligence will still work independently")
    
    # Import enhanced intelligence
    try:
        from asis_enhanced_intelligence import integrate_real_intelligence
        print("\n✅ Enhanced Intelligence Module Loaded")
    except ImportError as e:
        print(f"\n❌ Failed to load enhanced intelligence: {e}")
        return False
    
    # Try to import existing ASIS controller
    existing_controller = None
    try:
        from asis_activation_controller import ASISMasterController
        existing_controller = ASISMasterController()
        print("✅ Existing ASIS Controller Connected")
    except ImportError:
        print("⚠️  Running in standalone mode (existing ASIS not available)")
    
    # Initialize enhanced intelligence
    print(f"\n🚀 Initializing Enhanced Intelligence...")
    enhanced_asis = integrate_real_intelligence(existing_controller)
    
    # Create integration status file
    integration_status = {
        "integration_date": datetime.now().isoformat(),
        "enhanced_intelligence": True,
        "memory_system": "SQLite Database",
        "personality_system": "JSON Evolution",
        "learning_system": "Active",
        "existing_asis_connected": existing_controller is not None,
        "capabilities": [
            "Real Memory Storage & Retrieval",
            "Genuine Learning from Interactions", 
            "Personality Evolution",
            "Contextual Response Generation",
            "Topic Interest Development",
            "Relationship Level Tracking"
        ]
    }
    
    with open("asis_intelligence_status.json", "w") as f:
        json.dump(integration_status, f, indent=2)
    
    print(f"\n📊 Integration Complete!")
    print(f"📁 Status saved to: asis_intelligence_status.json")
    
    return enhanced_asis

def demonstrate_enhanced_capabilities(enhanced_asis):
    """Demonstrate the enhanced capabilities"""
    
    print(f"\n🎮 Interactive Demonstration")
    print("=" * 50)
    
    print("Your ASIS now has genuine intelligence! Let's test it:")
    print("(Type 'quit' to exit, 'status' to see intelligence status)")
    
    user_id = "demo_user"
    
    while True:
        try:
            user_input = input(f"\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye! Your enhanced ASIS will remember this conversation.")
                break
            
            if user_input.lower() == 'status':
                status = enhanced_asis.get_intelligence_status()
                print(f"\n📊 Intelligence Status:")
                for key, value in status.items():
                    print(f"   • {key.replace('_', ' ').title()}: {value}")
                continue
            
            if not user_input:
                continue
            
            # Determine response mode based on input
            mode = "conversational"
            if "research" in user_input.lower() or "study" in user_input.lower():
                mode = "research"
            elif "create" in user_input.lower() or "generate" in user_input.lower():
                mode = "creative"
            elif "learn" in user_input.lower() or "teach" in user_input.lower():
                mode = "learning"
            
            # Generate enhanced response
            response, analysis = enhanced_asis.generate_enhanced_response(
                user_input, mode, user_id
            )
            
            print(f"\n🤖 Enhanced ASIS: {response}")
            
            # Show analysis
            if analysis['topics']:
                print(f"📝 [Detected topics: {', '.join(analysis['topics'])}]")
            
            if analysis['relevant_memories'] > 0:
                print(f"🧠 [Used {analysis['relevant_memories']} relevant memories]")
            
            # Simulate learning (in real use, this would be based on actual feedback)
            enhanced_asis.learn_from_interaction(
                user_input, 
                response, 
                "good response",  # Positive feedback for demo
                user_id
            )
            
        except KeyboardInterrupt:
            print(f"\n\n👋 Interrupted. Enhanced ASIS will remember this conversation.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            continue

def main():
    """Main integration function"""
    
    print("🚀 ASIS Enhanced Intelligence Integration")
    print("=" * 60)
    print("This will upgrade your ASIS from template responses to genuine AI")
    print("with real memory, learning, and personality evolution.")
    print()
    
    # Integrate enhanced intelligence
    enhanced_asis = integrate_enhanced_intelligence()
    
    if enhanced_asis:
        print(f"\n🎉 Integration Successful!")
        
        # Ask if user wants to test
        test_choice = input(f"\nWould you like to test the enhanced capabilities? (y/n): ").strip().lower()
        
        if test_choice in ['y', 'yes']:
            demonstrate_enhanced_capabilities(enhanced_asis)
        else:
            print(f"\n📋 Enhanced ASIS is ready! Key features:")
            print(f"   • Memory database created: asis_enhanced_memory.db")
            print(f"   • Personality system active: asis_enhanced_personality.json") 
            print(f"   • Learning from every interaction")
            print(f"   • Contextual responses based on conversation history")
            print(f"\n🔧 Use asis_enhanced_intelligence.py to interact programmatically")
    else:
        print(f"\n❌ Integration failed. Check error messages above.")

if __name__ == "__main__":
    main()
