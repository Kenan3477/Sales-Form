#!/usr/bin/env python3
"""
Simple test for Cross-Domain Reasoning Engine Interface Fix
"""

import asyncio
from asis_cross_domain_reasoning_engine import CrossDomainReasoningEngine

async def test_simple():
    print("🧪 Testing Cross-Domain Interface Fix")
    
    engine = CrossDomainReasoningEngine()
    
    # Test the exact signature from the error message
    try:
        # This is what the error wants:
        # async def reason_across_domains(self, problem: str, source_domain: str = None, target_domain: str = None)
        result = await engine.reason_across_domains(
            "How to apply biological principles to AI optimization?", 
            "biology", 
            "computer_science"
        )
        
        print("✅ SUCCESS: Interface fix works!")
        print(f"Confidence: {result.get('reasoning_confidence', 0):.2f}")
        print(f"Domains: {result.get('domains_analyzed', [])}")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(test_simple())
