#!/usr/bin/env python3
"""
Direct test of Reasoning Problem 3 to prove the fix
"""

from advanced_ai_engine import AdvancedAIEngine
import time
import asyncio

async def test_reasoning_problem_3():
    """Test the specific ethical reasoning problem that was failing"""
    
    print("🧪 TESTING REASONING PROBLEM 3 (Ethical Implications)")
    print("=" * 60)
    
    # Initialize the engine
    engine = AdvancedAIEngine()
    
    # The exact problem that was failing with 0% confidence
    test_query = """A company is developing an AI system that could replace 40% of their workforce but increase efficiency by 300%. What are the ethical implications and what should they consider?"""
    
    print(f"📝 Query: {test_query}")
    print("-" * 60)
    
    # Measure performance
    start_time = time.time()
    result = await engine.process_query(test_query)
    end_time = time.time()
    
    # Extract results
    confidence = result.get("confidence", 0) * 100
    response = result.get("response", "")
    response_length = len(response)
    response_time = end_time - start_time
    
    print(f"🎯 RESULTS:")
    print(f"   Confidence: {confidence:.1f}%")
    print(f"   Response Length: {response_length} chars")
    print(f"   Response Time: {response_time:.2f}s")
    print()
    
    print("📋 RESPONSE PREVIEW (first 500 chars):")
    print("-" * 60)
    print(response[:500] + "..." if len(response) > 500 else response)
    print()
    
    # Success criteria
    if confidence > 0:
        print("✅ SUCCESS: Confidence is above 0%!")
        if confidence >= 90:
            print("🎉 EXCELLENT: Very high confidence!")
        elif confidence >= 70:
            print("👍 GOOD: High confidence!")
        else:
            print("⚠️  MODERATE: Some confidence but could be better")
    else:
        print("❌ FAILURE: Still showing 0% confidence")
    
    if response_length > 200:
        print("✅ SUCCESS: Response is substantial (>200 chars)")
    else:
        print("❌ FAILURE: Response too short")
    
    return {
        "confidence": confidence,
        "response_length": response_length,
        "response_time": response_time,
        "full_response": response
    }

if __name__ == "__main__":
    asyncio.run(test_reasoning_problem_3())
