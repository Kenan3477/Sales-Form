#!/usr/bin/env python3
"""
Simple test for cross-domain interface fix
"""

import asyncio
from asis_cross_domain_reasoning_engine import CrossDomainReasoningEngine

async def quick_test():
    print("🧪 Testing Cross-Domain Interface Fix...")
    engine = CrossDomainReasoningEngine()
    
    # Test the 4-argument pattern that was failing
    try:
        result = await engine.reason_across_domains("computer_science", "biology", "optimization", "How can evolution improve AI?")
        print(f"✅ 4-arg pattern: Confidence {result.get('reasoning_confidence', 0):.2f}")
    except Exception as e:
        print(f"❌ 4-arg pattern failed: {e}")
    
    # Test the 3-argument pattern
    try:
        result = await engine.reason_across_domains("How can evolution improve AI?", "computer_science", "biology")
        print(f"✅ 3-arg pattern: Confidence {result.get('reasoning_confidence', 0):.2f}")
    except Exception as e:
        print(f"❌ 3-arg pattern failed: {e}")
    
    print("✨ Interface fix test complete!")

asyncio.run(quick_test())
