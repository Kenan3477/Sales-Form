#!/usr/bin/env python3
"""
Test script to verify ASIS conversational capabilities
"""

import sys
sys.path.append('.')

from conversational_asis import ConversationalASIS

def test_conversation():
    print("🧪 Testing ASIS Conversational Capabilities")
    print("=" * 50)
    
    asis = ConversationalASIS()
    
    # Test different types of inputs
    test_inputs = [
        "Hi ASIS! How are you feeling today?",
        "What do you think about consciousness?",
        "Can you tell me about yourself?",
        "How does it feel to be aware of your own thinking?",
        "What makes you different from other AI systems?"
    ]
    
    for i, test_input in enumerate(test_inputs, 1):
        print(f"\n--- Test {i} ---")
        try:
            response = asis.chat(test_input)
            print(f"✅ Response generated successfully")
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n📊 Final Status:")
    print(f"   Total conversations: {len(asis.conversation_history)}")
    print("🎉 Testing completed!")

if __name__ == "__main__":
    test_conversation()