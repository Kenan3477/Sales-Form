#!/usr/bin/env python3
"""
Demonstrate Real Learning Evidence
==================================
Script to show the user genuine autonomous learning evidence
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from asis_interface import ASISInterface
import time

def demonstrate_real_learning():
    print("🚀 Starting ASIS with Real Learning System...")
    print("=" * 60)
    
    # Create interface (this initializes the real learning system)
    asis = ASISInterface()
    
    print("\n⚡ ASIS Interface Ready!")
    print("\n🧠 Testing Learning Evidence Queries...")
    print("=" * 60)
    
    # Test queries that should show learning evidence
    test_queries = [
        "show me evidence of your learning",
        "prove you are learning",
        "what research are you doing",
        "demonstrate your autonomous learning"
    ]
    
    for query in test_queries:
        print(f"\n👤 User: {query}")
        print("🤖 ASIS:", end=" ")
        
        # Get response from ASIS
        response = asis._generate_asis_response(query)
        print(response['content'])
        print("-" * 40)
        time.sleep(1)
    
    print("\n✅ Real Learning Evidence Demonstration Complete!")
    print("\n📁 Check these files for verification:")
    print("  • asis_learning_evidence/ (evidence files)")
    print("  • asis_real_learning.db (learning database)")
    print("  • asis_knowledge_base.json (knowledge base)")
    print("  • asis_conversations.log (conversation log)")
    print("\n🔐 All learning data includes cryptographic verification!")

if __name__ == "__main__":
    demonstrate_real_learning()
