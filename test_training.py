#!/usr/bin/env python3
"""
Test ASIS Training System
=========================
Quick test of the training system's matching capabilities
"""

from asis_training_system import ASISTrainingSystem

def test_training_system():
    """Test the training system with various inputs"""
    
    training_system = ASISTrainingSystem()
    
    test_cases = [
        "what are you doing",
        "do you have interests",
        "how are you",
        "what do you like",
        "your responses are generic",
        "do you understand me"
    ]
    
    print("Testing ASIS Training System")
    print("=" * 50)
    
    for user_input in test_cases:
        print(f"\n🔍 Testing: '{user_input}'")
        
        # Find similar examples
        similar_examples = training_system.find_similar_training_examples(
            user_input, {}
        )
        
        if similar_examples:
            best_match = similar_examples[0]
            print(f"✅ Best match: '{best_match['input_text']}'")
            print(f"📊 Similarity: {best_match['similarity_score']:.3f}")
            
            if best_match['similarity_score'] > 0.3:
                print(f"🎯 Would use training response:")
                print(f"   {best_match['appropriate_response'][:100]}...")
            else:
                print("❌ Similarity too low for training response")
        else:
            print("❌ No similar examples found")

if __name__ == "__main__":
    test_training_system()
