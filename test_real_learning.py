#!/usr/bin/env python3
"""
Test Real Learning System Evidence
==================================
"""

from asis_real_learning_system import ASISRealLearningSystem
import time

def test_real_learning():
    print("🧪 Testing Real Learning System...")
    
    # Initialize system
    learning_system = ASISRealLearningSystem()
    learning_system.setup_real_learning_system()
    
    print("\n📊 Adding some test learning data...")
    
    # Analyze some conversations to generate real learning
    test_conversations = [
        ("Hello ASIS", "Hello! How can I help you?", 5),
        ("Are you learning?", "Yes, I am continuously learning from our interactions!", 4),
        ("Who created you?", "You did! This entire ASIS system is your project.", 5),
        ("What have you learned?", "I've learned to provide more direct, specific answers based on your feedback.", 4)
    ]
    
    for user_input, response, rating in test_conversations:
        learning_system.analyze_real_conversation(user_input, response, rating)
        time.sleep(0.1)  # Small delay to create different timestamps
    
    # Add some knowledge expansion
    learning_system.expand_knowledge_base(
        "User Preferences", 
        "User prefers direct, specific answers over generic responses",
        "conversation_analysis"
    )
    
    learning_system.implement_improvement(
        "response_style",
        "Generic conversational responses", 
        "Direct, specific answers with evidence",
        "User feedback about avoiding generic responses"
    )
    
    print("\n🔍 Getting Learning Status...")
    status = learning_system.get_learning_status()
    print(f"📈 Patterns Learned: {status['total_patterns_learned']}")
    print(f"✅ Verified Insights: {status['verified_insights']}")
    print(f"⚡ Learning Velocity: {status['learning_velocity']}")
    
    print("\n📝 Recent Insights:")
    insights = learning_system.get_recent_insights()
    for insight in insights[:3]:
        print(f"  • {insight['pattern']}")
        print(f"    Hash: {insight['verification_hash'][:8]}")
    
    print("\n📁 Evidence Files:")
    files = learning_system.get_verification_files()
    print(f"  Found {len(files)} evidence files")
    
    print("\n🎯 Full Evidence Report:")
    evidence = learning_system.get_verifiable_evidence()
    print(evidence)
    
    print("\n✅ Real Learning System Test Complete!")

if __name__ == "__main__":
    test_real_learning()
