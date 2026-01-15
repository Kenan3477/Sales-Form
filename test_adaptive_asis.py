#!/usr/bin/env python3
"""
Test ASIS Adaptive Meta-Learning Integration
===========================================
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from asis_interface import ASISInterface
import time

def test_adaptive_asis():
    print("🚀 Testing ASIS with Adaptive Meta-Learning...")
    print("=" * 60)
    
    # Create interface (this initializes all systems including adaptive meta-learning)
    asis = ASISInterface()
    
    print("\n⚡ ASIS Interface Ready with Adaptive Meta-Learning!")
    print("\n🧠 Testing Adaptive Response System...")
    print("=" * 60)
    
    # Test queries that should trigger different adaptive responses
    test_queries = [
        ("Just give me a direct answer - are you learning?", "Testing direct answer preference"),
        ("Can you explain in detail with examples what you've learned?", "Testing detailed explanation preference"),  
        ("I need technical precision - show me exact evidence", "Testing technical precision preference"),
        ("Let's have a friendly chat about your learning", "Testing conversational style preference"),
        ("Show me proof and evidence of your learning", "Testing evidence-based preference")
    ]
    
    for query, description in test_queries:
        print(f"\n📝 {description}")
        print(f"👤 User: {query}")
        print("🤖 ASIS:", end=" ")
        
        # Get adaptive response from ASIS
        response = asis._generate_asis_response(query)
        print(response['content'])
        
        print(f"🎯 Style Applied: {response.get('recommended_style', 'default')}")
        print(f"🔧 Adaptation Applied: {response.get('adaptation_applied', False)}")
        print(f"📊 Confidence: {response.get('confidence_level', 0):.2f}")
        print("-" * 50)
        time.sleep(1)
    
    print("\n📊 Getting Adaptive Learning Report...")
    adaptation_report = asis.adaptive_meta_learning.get_adaptation_effectiveness_report()
    print(adaptation_report)
    
    print("\n✅ Adaptive Meta-Learning Integration Test Complete!")
    print("\n🎯 Key Features Demonstrated:")
    print("  • Adaptive response style based on user preferences")
    print("  • Meta-learning from interaction patterns") 
    print("  • Real-time learning adaptation")
    print("  • Verifiable learning evidence")
    print("  • Self-improving learning processes")

if __name__ == "__main__":
    test_adaptive_asis()
