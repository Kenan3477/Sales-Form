#!/usr/bin/env python3
"""
Test the Cross-Domain Reasoning Engine Interface Fix
"""

import asyncio
from asis_cross_domain_reasoning_engine import CrossDomainReasoningEngine

async def test_cross_domain_interface():
    """Test both interface formats for the cross-domain reasoning engine"""
    
    print("🧪 TESTING CROSS-DOMAIN REASONING ENGINE INTERFACE")
    print("=" * 60)
    
    engine = CrossDomainReasoningEngine()
    
    # Test 1: Original interface format (currently working)
    print("\n📝 Test 1: Original Interface Format")
    print("-" * 40)
    
    try:
        source_domain = "computer_science"
        target_domain = "biology"
        concept = "optimization"
        problem = "How can biological evolution principles improve AI algorithms?"
        
        result = await engine.reason_across_domains(source_domain, target_domain, concept, problem)
        
        print(f"✅ SUCCESS: Original interface works!")
        print(f"   Reasoning Confidence: {result.get('reasoning_confidence', 0):.2f}")
        print(f"   Domains Analyzed: {len(result.get('domains_analyzed', []))}")
        print(f"   Transferred Principles: {len(result.get('transferred_principles', []))}")
        
    except Exception as e:
        print(f"❌ FAILED: Original interface error: {e}")
    
    # Test 2: Simple interface format (the one that was failing)
    print("\n📝 Test 2: Simple Interface Format (Expected by Error)")
    print("-" * 40)
    
    try:
        # Check if method exists with expected signature
        if hasattr(engine, 'reason_across_domains_simple'):
            problem = "How can we apply network theory to understand social dynamics?"
            source_domain = "computer_science"
            target_domain = "psychology"
            
            result = await engine.reason_across_domains_simple(problem, source_domain, target_domain)
            
            print(f"✅ SUCCESS: Simple interface works!")
            print(f"   Reasoning Confidence: {result.get('reasoning_confidence', 0):.2f}")
            print(f"   Cross-domain Connections: {len(result.get('cross_domain_connections', []))}")
        else:
            print("⚠️  Simple interface method not found")
    except Exception as e:
        print(f"❌ FAILED: Simple interface error: {e}")
    
    # Test 3: Check method signature compatibility
    print("\n📝 Test 3: Method Signature Analysis")
    print("-" * 40)
    
    import inspect
    sig = inspect.signature(engine.reason_across_domains)
    params = list(sig.parameters.keys())
    print(f"Current signature parameters: {params}")
    
    # Try to call with positional args only (problem first)
    try:
        # This is the format expected by the error message
        problem = "Apply physics concepts to economics"
        result = await engine.reason_across_domains("computer_science", "economics", "optimization", problem)
        print(f"✅ SUCCESS: Can call with 4 positional args")
    except Exception as e:
        print(f"❌ FAILED: 4 positional args error: {e}")
    
    print("\n🎯 INTERFACE ANALYSIS COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_cross_domain_interface())
