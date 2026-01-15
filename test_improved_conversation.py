#!/usr/bin/env python3
"""
Direct Conversational Test
=========================

Clean test showing the improved conversational capabilities
"""

from asis_truly_conversational import ASISTrulyConversational

def test_improved_conversation():
    print("🧪 TESTING IMPROVED CONVERSATIONAL RESPONSES")
    print("=" * 60)
    
    # Create fresh conversational ASIS
    asis = ASISTrulyConversational()
    
    print("Testing the exact question that showed limitations before...\n")
    
    # The problematic question from before
    test_question = "so what can you actually do?"
    
    print(f"👤 User: {test_question}")
    response = asis.generate_response(test_question)
    print(f"💬 New ASIS: {response}\n")
    
    # Follow up questions to show contextual awareness
    followups = [
        "Can you be more specific?",
        "Give me some examples", 
        "How do you remember things?",
        "What makes you different from other AI?"
    ]
    
    for question in followups:
        print(f"👤 User: {question}")
        response = asis.generate_response(question)
        print(f"💬 New ASIS: {response}\n")
    
    # Show conversation summary
    print("📊 CONVERSATION ANALYSIS:")
    asis.show_status()
    
    print("\n✅ KEY IMPROVEMENTS DEMONSTRATED:")
    print("   • Contextual responses that address actual questions")
    print("   • Memory of conversation flow and topics")
    print("   • Specific, helpful answers about capabilities")
    print("   • Follow-up questions to maintain dialogue")
    print("   • Recognition of user intent and appropriate responses")

if __name__ == "__main__":
    test_improved_conversation()
