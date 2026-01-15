#!/usr/bin/env python3
"""
ASIS Advanced AI Engine Method Validation
=========================================
Test the new process_query method interface fix
"""

import asyncio
import json
from datetime import datetime

def test_advanced_ai_engine_method_interface():
    """Test if Advanced AI Engine now has the required process_query method"""
    
    print("🔥 TESTING ADVANCED AI ENGINE METHOD INTERFACE FIX")
    print("=" * 60)
    
    try:
        # Import the Advanced AI Engine
        from advanced_ai_engine import AdvancedAIEngine
        
        # Initialize the engine
        print("✅ Initializing Advanced AI Engine...")
        engine = AdvancedAIEngine()
        
        # Check if process_query method exists
        if hasattr(engine, 'process_query'):
            print("✅ process_query method found!")
            
            # Test the method interface
            async def test_method():
                try:
                    # Test with a simple query
                    test_query = "What is consciousness?"
                    test_context = {
                        'conversation_history': [
                            {"user_input": "Hello", "asis_response": "Hello! How can I help you?"}
                        ]
                    }
                    
                    print(f"🧠 Testing query: '{test_query}'")
                    result = await engine.process_query(test_query, test_context)
                    
                    # Validate the result format
                    required_fields = ["response", "confidence", "reasoning", "analysis", "engine_type"]
                    missing_fields = [field for field in required_fields if field not in result]
                    
                    if missing_fields:
                        print(f"❌ Missing required fields: {missing_fields}")
                        return False
                    else:
                        print("✅ All required fields present in response!")
                        print(f"   - Response: {result['response'][:100]}...")
                        print(f"   - Confidence: {result['confidence']}")
                        print(f"   - Engine Type: {result['engine_type']}")
                        print(f"   - Analysis Keys: {list(result['analysis'].keys())}")
                        print(f"   - Processing Time: {result['processing_time']}")
                        return True
                        
                except Exception as e:
                    print(f"❌ Error testing process_query method: {e}")
                    return False
            
            # Run the async test
            test_success = asyncio.run(test_method())
            
            if test_success:
                print("\n🎉 ADVANCED AI ENGINE METHOD INTERFACE FIX: SUCCESS!")
                print("✅ process_query method working correctly")
                print("✅ Returns proper AGI-compatible format")
                print("✅ Integrates with existing AGI enhancements")
                return True
            else:
                print("\n❌ ADVANCED AI ENGINE METHOD INTERFACE FIX: FAILED!")
                return False
                
        else:
            print("❌ process_query method NOT found!")
            print("Available methods:", [method for method in dir(engine) if not method.startswith('_')])
            return False
            
    except Exception as e:
        print(f"❌ Failed to test Advanced AI Engine: {e}")
        return False

def test_integration_with_agi_capability_assessment():
    """Test if the fix resolves the AGI capability assessment issue"""
    
    print("\n🚀 TESTING INTEGRATION WITH AGI CAPABILITY ASSESSMENT")
    print("=" * 60)
    
    try:
        # Import the AGI capability assessment
        from asis_agi_capability_assessment import test_agi_reasoning_engines
        
        print("✅ Running AGI reasoning engine test...")
        
        # Run the test that was failing before
        result = asyncio.run(test_agi_reasoning_engines())
        
        if result.get("advanced_ai_score", 0) > 0:
            print("✅ Advanced AI Engine now working in AGI tests!")
            print(f"   - Score: {result.get('advanced_ai_score', 0):.2f}")
            print(f"   - Response Time: {result.get('advanced_ai_time', 0):.2f}s")
            return True
        else:
            print("❌ Advanced AI Engine still failing in AGI tests")
            return False
            
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔥 ASIS ADVANCED AI ENGINE METHOD INTERFACE FIX VALIDATION")
    print("=" * 70)
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test 1: Method interface fix
    fix_success = test_advanced_ai_engine_method_interface()
    
    # Test 2: Integration with AGI assessment
    integration_success = test_integration_with_agi_capability_assessment()
    
    # Final results
    print("\n" + "=" * 70)
    print("🎯 FINAL VALIDATION RESULTS")
    print("=" * 70)
    
    if fix_success and integration_success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Advanced AI Engine method interface fixed")
        print("✅ AGI capability assessment integration working")
        print("🚀 Ready for full AGI validation run")
    elif fix_success:
        print("⚠️ PARTIAL SUCCESS")
        print("✅ Method interface fixed")
        print("❌ Integration needs work")
    else:
        print("❌ FIX FAILED")
        print("❌ Method interface still broken")
        
    print(f"\nValidation completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
