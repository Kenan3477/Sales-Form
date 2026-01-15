#!/usr/bin/env python3
"""
Test the Ethical Reasoning Engine Interface Fix
"""

import asyncio
from asis_ethical_reasoning_engine import EthicalReasoningEngine

async def test_ethical_interface():
    """Test both interface formats for the ethical reasoning engine"""
    
    print("🧪 TESTING ETHICAL REASONING ENGINE INTERFACE")
    print("=" * 60)
    
    engine = EthicalReasoningEngine()
    
    # Test 1: String scenario format (the one that was failing)
    print("\n📝 Test 1: String Scenario Format")
    print("-" * 40)
    
    try:
        scenario = "A company wants to implement AI surveillance of employees to improve productivity"
        context = {
            "stakeholders": ["employees", "management", "customers"],
            "domain": "workplace_ethics"
        }
        
        result = await engine.analyze_ethical_implications(scenario, context)
        
        print(f"✅ SUCCESS: String scenario interface works!")
        print(f"   Ethical Score: {result.get('overall_ethical_score', 0):.2f}")
        print(f"   Frameworks Analyzed: {len(result.get('framework_analyses', {}))}")
        print(f"   Stakeholders: {result.get('stakeholders_affected', 0)}")
        
    except Exception as e:
        print(f"❌ FAILED: String scenario interface error: {e}")
    
    # Test 2: Dict situation format (original format)
    print("\n📝 Test 2: Dict Situation Format")
    print("-" * 40)
    
    try:
        situation = {
            "scenario": "Autonomous vehicles must choose between protecting passengers vs pedestrians",
            "stakeholders": ["passengers", "pedestrians", "society"],
            "context": {"domain": "autonomous_systems"},
            "decision_type": "ethical_dilemma"
        }
        
        result = await engine.analyze_ethical_implications(situation)
        
        print(f"✅ SUCCESS: Dict situation interface works!")
        print(f"   Ethical Score: {result.get('overall_ethical_score', 0):.2f}")
        print(f"   Frameworks Analyzed: {len(result.get('framework_analyses', {}))}")
        print(f"   Conflicts Found: {len(result.get('ethical_conflicts', []))}")
        
    except Exception as e:
        print(f"❌ FAILED: Dict situation interface error: {e}")
    
    print("\n🎯 INTERFACE FIX VERIFICATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_ethical_interface())
