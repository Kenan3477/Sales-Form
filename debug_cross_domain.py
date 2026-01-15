#!/usr/bin/env python3
"""
Debug Cross-Domain Test
=======================
Debug the cross-domain reasoning test execution
"""

print("🔍 Starting Cross-Domain Debug Test...")

try:
    print("1️⃣ Testing basic import...")
    from asis_cross_domain_reasoning_engine import CrossDomainReasoningEngine
    print("✅ Import successful")
    
    print("2️⃣ Testing engine creation...")
    engine = CrossDomainReasoningEngine()
    print("✅ Engine created")
    
    print("3️⃣ Testing method availability...")
    has_method = hasattr(engine, 'advanced_cross_domain_reasoning')
    print(f"Method available: {has_method}")
    
    if has_method:
        print("4️⃣ Testing async execution...")
        import asyncio
        
        async def test_async():
            try:
                result = await engine.advanced_cross_domain_reasoning(
                    source_domain="physics",
                    target_domain="economics", 
                    concept="conservation_of_energy",
                    problem="How to maintain value in economic transactions"
                )
                return result
            except Exception as e:
                print(f"❌ Async execution failed: {e}")
                import traceback
                traceback.print_exc()
                return None
        
        print("Running async test...")
        result = asyncio.run(test_async())
        
        if result:
            print("✅ Cross-domain reasoning successful!")
            print(f"Confidence: {result.get('confidence', 'N/A')}")
            print(f"Mappings: {len(result.get('analogical_mapping', {}))}")
        else:
            print("❌ Cross-domain reasoning failed")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()

print("🔍 Debug test complete")
