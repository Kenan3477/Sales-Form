#!/usr/bin/env python3
"""
Comprehensive Interface Fix Validation
"""

print("🔥 COMPREHENSIVE INTERFACE FIX VALIDATION")
print("=" * 60)

# Test 1: Import both engines
print("\n📦 Test 1: Engine Imports")
print("-" * 30)
try:
    from asis_ethical_reasoning_engine import EthicalReasoningEngine
    print("✅ Ethical Reasoning Engine imported")
    
    from asis_cross_domain_reasoning_engine import CrossDomainReasoningEngine
    print("✅ Cross-Domain Reasoning Engine imported")
    
    from advanced_ai_engine import AdvancedAIEngine
    print("✅ Advanced AI Engine imported")
    
except Exception as e:
    print(f"❌ Import failed: {e}")
    exit(1)

# Test 2: Initialize engines
print("\n🚀 Test 2: Engine Initialization")
print("-" * 30)
try:
    ethical_engine = EthicalReasoningEngine()
    print("✅ Ethical engine initialized")
    
    cross_domain_engine = CrossDomainReasoningEngine()
    print("✅ Cross-domain engine initialized")
    
    ai_engine = AdvancedAIEngine()
    print("✅ Advanced AI engine initialized")
    
except Exception as e:
    print(f"❌ Initialization failed: {e}")
    exit(1)

# Test 3: Check method signatures
print("\n🔍 Test 3: Method Signature Analysis")
print("-" * 30)
import inspect

try:
    # Check ethical reasoning interface
    ethical_sig = inspect.signature(ethical_engine.analyze_ethical_implications)
    print(f"✅ Ethical method signature: {ethical_sig}")
    
    # Check cross-domain reasoning interface
    cross_domain_sig = inspect.signature(cross_domain_engine.reason_across_domains)
    print(f"✅ Cross-domain method signature: {cross_domain_sig}")
    
except Exception as e:
    print(f"❌ Signature analysis failed: {e}")

# Test 4: Interface compatibility test (async)
print("\n⚡ Test 4: Async Interface Test")
print("-" * 30)

import asyncio

async def test_interfaces():
    try:
        # Test ethical interface with string scenario
        result = await ethical_engine.analyze_ethical_implications(
            "AI should prioritize efficiency over privacy",
            {"stakeholders": ["users", "companies", "society"]}
        )
        print(f"✅ Ethical string interface: Score {result.get('overall_ethical_score', 0):.2f}")
        
        # Test cross-domain interface with 4 arguments
        result = await cross_domain_engine.reason_across_domains(
            "computer_science", "biology", "optimization", "Apply evolution to AI"
        )
        print(f"✅ Cross-domain 4-arg interface: Confidence {result.get('reasoning_confidence', 0):.2f}")
        
        # Test cross-domain interface with 3 arguments
        result = await cross_domain_engine.reason_across_domains(
            "Apply neural networks to economics", "computer_science", "economics"
        )
        print(f"✅ Cross-domain 3-arg interface: Confidence {result.get('reasoning_confidence', 0):.2f}")
        
    except Exception as e:
        print(f"❌ Async interface test failed: {e}")
        import traceback
        traceback.print_exc()

# Run async test
asyncio.run(test_interfaces())

print("\n🎉 INTERFACE FIX VALIDATION COMPLETE")
print("=" * 60)
