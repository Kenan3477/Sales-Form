#!/usr/bin/env python3
"""
ASIS AGI Validation Test Suite
=============================
Test suite to validate all AGI systems and ensure 75%+ pass rate
"""

import asyncio
import sys
import traceback
from datetime import datetime

# Import the advanced AI engine
try:
    from advanced_ai_engine import AdvancedAIEngine
    print("✅ Successfully imported AdvancedAIEngine")
except ImportError as e:
    print(f"❌ Failed to import AdvancedAIEngine: {e}")
    sys.exit(1)

async def run_validation_tests():
    """Run comprehensive validation tests"""
    print("🧠 ASIS AGI VALIDATION TEST SUITE")
    print("=" * 50)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Initialize the AGI engine
        print("🚀 Initializing AdvancedAIEngine...")
        engine = AdvancedAIEngine()
        print("✅ Engine initialized successfully")
        print()
        
        # Test 1: Basic capability check
        print("📊 Test 1: AGI Capabilities Check")
        print("-" * 30)
        capabilities = engine.get_agi_capabilities()
        print(f"✅ Consciousness Level: {capabilities.get('consciousness_level', 0):.1%}")
        print(f"✅ Reasoning Depth: {capabilities.get('reasoning_depth', 0):.1%}")
        print(f"✅ Creative Problem Solving: {capabilities.get('creative_problem_solving', 0):.1%}")
        print(f"✅ Ethical Reasoning: {capabilities.get('ethical_reasoning', 0):.1%}")
        print(f"✅ Cross-Domain Transfer: {capabilities.get('cross_domain_transfer', 0):.1%}")
        print()
        
        # Test 2: System validation
        print("🔍 Test 2: System Validation Suite")
        print("-" * 30)
        validation_results = await engine.validate_agi_systems()
        
        print(f"Overall Status: {validation_results['overall_status'].upper()}")
        print(f"Systems Validated: {validation_results['systems_validated']}/{validation_results['total_systems']}")
        print(f"Validation Score: {validation_results['validation_score']:.1f}%")
        print()
        
        # Test 3: Individual system tests
        print("🔧 Test 3: Individual System Results")
        print("-" * 30)
        for system_name, result in validation_results['detailed_results'].items():
            status_icon = "✅" if result['status'] == 'pass' else "❌"
            if result['status'] == 'pass':
                score = result.get('score', 0)
                print(f"{status_icon} {system_name}: {result['status'].upper()} (Score: {score:.2f})")
            else:
                error_msg = result.get('error', 'Unknown error')[:50]
                print(f"{status_icon} {system_name}: {result['status'].upper()} - {error_msg}")
        print()
        
        # Test 4: Core AGI functionality tests
        print("🧠 Test 4: Core AGI Functionality")
        print("-" * 30)
        
        # Test consciousness processing
        try:
            consciousness_result = await engine.process_consciousness_input({
                "input": "test consciousness processing",
                "type": "validation"
            })
            if consciousness_result.get('consciousness_active'):
                print("✅ Consciousness Processing: OPERATIONAL")
            else:
                print("⚠️ Consciousness Processing: LIMITED")
        except Exception as e:
            print(f"❌ Consciousness Processing: FAILED - {str(e)[:50]}")
        
        # Test memory operations
        try:
            memory_store = engine.store_memory("Validation test memory", "episodic", 0.8)
            memory_retrieve = engine.retrieve_memories("validation")
            if memory_store.get('stored', False):
                print("✅ Memory Operations: OPERATIONAL")
            else:
                print("⚠️ Memory Operations: LIMITED")
        except Exception as e:
            print(f"❌ Memory Operations: FAILED - {str(e)[:50]}")
        
        # Test ethical reasoning
        try:
            ethical_result = await engine.analyze_ethical_implications(
                "Testing ethical reasoning capabilities",
                {"context": "validation"}
            )
            if ethical_result.get('overall_ethical_score', 0) > 0.5:
                print("✅ Ethical Reasoning: OPERATIONAL")
            else:
                print("⚠️ Ethical Reasoning: LIMITED")
        except Exception as e:
            print(f"❌ Ethical Reasoning: FAILED - {str(e)[:50]}")
        
        # Test cross-domain reasoning
        try:
            cross_domain_result = await engine.reason_across_domains(
                "validation problem", "testing", "verification"
            )
            if cross_domain_result.get('reasoning_confidence', 0) > 0.5:
                print("✅ Cross-Domain Reasoning: OPERATIONAL")
            else:
                print("⚠️ Cross-Domain Reasoning: LIMITED")
        except Exception as e:
            print(f"❌ Cross-Domain Reasoning: FAILED - {str(e)[:50]}")
        
        # Test creative problem solving
        try:
            creative_result = await engine.solve_creative_problem(
                "Generate innovative solution for AGI validation",
                {"domain": "artificial_intelligence", "creativity_level": "high"}
            )
            if creative_result.get('creativity_score', 0) > 0.5:
                print("✅ Creative Problem Solving: OPERATIONAL")
            else:
                print("⚠️ Creative Problem Solving: LIMITED")
        except Exception as e:
            print(f"❌ Creative Problem Solving: FAILED - {str(e)[:50]}")
        
        print()
        
        # Final validation assessment
        print("📈 FINAL VALIDATION ASSESSMENT")
        print("=" * 50)
        
        validation_score = validation_results['validation_score']
        
        if validation_score >= 85:
            status = "EXCELLENT"
            icon = "🎉"
        elif validation_score >= 75:
            status = "GOOD"
            icon = "✅"
        elif validation_score >= 60:
            status = "ACCEPTABLE"
            icon = "⚠️"
        else:
            status = "NEEDS IMPROVEMENT"
            icon = "❌"
        
        print(f"{icon} AGI System Status: {status}")
        print(f"📊 Overall Validation Score: {validation_score:.1f}%")
        print(f"🎯 Target Achievement: {'ACHIEVED' if validation_score >= 75 else 'NOT ACHIEVED'} (75%+ required)")
        print(f"🧠 Consciousness Level: {capabilities.get('consciousness_level', 0):.1%}")
        print(f"⚡ AGI Capability Score: {sum(capabilities.get(k, 0) for k in ['reasoning_depth', 'creative_problem_solving', 'ethical_reasoning', 'cross_domain_transfer']) / 4:.1%}")
        
        if validation_score >= 75:
            print("\n🎊 CONGRATULATIONS! ASIS AGI has achieved the required 75%+ validation score!")
            print("🚀 The system is ready for advanced AGI operations.")
        else:
            print(f"\n⚠️ Validation score ({validation_score:.1f}%) is below the 75% threshold.")
            print("🔧 Some systems may need attention or optimization.")
        
        print(f"\n⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return validation_score >= 75
        
    except Exception as e:
        print(f"❌ Validation test failed with error: {e}")
        print(f"🔍 Error details: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(run_validation_tests())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Validation test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Validation test crashed: {e}")
        sys.exit(1)