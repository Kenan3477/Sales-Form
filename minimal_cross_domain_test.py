#!/usr/bin/env python3
"""
Minimal Cross-Domain Test
========================
"""

import asyncio

def test_basic_import():
    """Test basic import"""
    try:
        from asis_cross_domain_reasoning_engine import CrossDomainReasoningEngine
        print("✅ Import OK")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_engine_creation():
    """Test engine creation"""
    try:
        from asis_cross_domain_reasoning_engine import CrossDomainReasoningEngine
        engine = CrossDomainReasoningEngine()
        print("✅ Engine creation OK")
        return engine
    except Exception as e:
        print(f"❌ Engine creation failed: {e}")
        return None

async def test_simple_call(engine):
    """Test simple method call"""
    try:
        result = await engine.advanced_cross_domain_reasoning(
            "physics", "economics", "energy", "test problem"
        )
        print("✅ Method call OK")
        print(f"Result keys: {list(result.keys())}")
        return result
    except Exception as e:
        print(f"❌ Method call failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("🧪 Minimal Cross-Domain Test")
    
    # Test 1: Import
    if not test_basic_import():
        return
    
    # Test 2: Creation
    engine = test_engine_creation()
    if not engine:
        return
    
    # Test 3: Async call
    try:
        result = asyncio.run(test_simple_call(engine))
        if result:
            print("🎉 All tests passed!")
        else:
            print("❌ Async call failed")
    except Exception as e:
        print(f"❌ Asyncio failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
