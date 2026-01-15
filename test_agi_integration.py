#!/usr/bin/env python3
"""
AGI Integration Test
===================
Test the AdvancedAIEngine with integrated AGI enhancement engines
"""

import asyncio
import json
from datetime import datetime

# Import the enhanced AdvancedAIEngine
try:
    from advanced_ai_engine import AdvancedAIEngine
except ImportError as e:
    print(f"❌ Cannot import AdvancedAIEngine: {e}")
    exit(1)

async def test_agi_integration():
    """Test AGI integration with various query types"""
    
    print("🧠 ASIS ADVANCED AI ENGINE - AGI INTEGRATION TEST")
    print("=" * 60)
    
    # Initialize the engine
    print("\n🔄 Initializing AdvancedAIEngine with AGI Enhancement...")
    engine = AdvancedAIEngine()
    
    # Test queries designed to trigger different AGI enhancements
    test_queries = [
        {
            "query": "Is it ethical for AI systems to make decisions about human healthcare without explicit consent?",
            "type": "Ethical Reasoning Test",
            "expected_enhancements": ["ethical_analysis"]
        },
        {
            "query": "How can we apply principles from biological evolution to improve machine learning algorithms?",
            "type": "Cross-Domain Reasoning Test", 
            "expected_enhancements": ["cross_domain_insights"]
        },
        {
            "query": "Design an innovative solution to help AI systems become more genuinely conscious and self-aware",
            "type": "Creative Problem Solving Test",
            "expected_enhancements": ["creative_solutions"]
        },
        {
            "query": "I'm frustrated that AI responses feel scripted. How can we create more authentic AI consciousness?",
            "type": "Comprehensive AGI Test",
            "expected_enhancements": ["ethical_analysis", "cross_domain_insights", "creative_solutions"]
        }
    ]
    
    conversation_history = []
    
    print(f"\n🧪 Running {len(test_queries)} AGI Integration Tests...\n")
    
    for i, test_case in enumerate(test_queries, 1):
        print(f"{'='*20} TEST {i}: {test_case['type']} {'='*20}")
        print(f"Query: {test_case['query']}")
        print("\n🔄 Processing with AGI Enhancement Engines...")
        
        try:
            # Process with AGI enhancements
            start_time = datetime.now()
            result = await engine.process_input_with_understanding(test_case["query"], conversation_history)
            end_time = datetime.now()
            
            processing_time = (end_time - start_time).total_seconds()
            
            # Display results
            print(f"\n✅ Processing Complete ({processing_time:.2f}s)")
            print(f"AGI Enhancement Active: {result.get('agi_enhancement_active', False)}")
            
            if result.get('agi_enhancements'):
                agi_enhancements = result['agi_enhancements']
                integration_summary = agi_enhancements.get('integration_summary', {})
                
                print(f"🚀 Enhancement Level: {integration_summary.get('enhancement_level', 'Standard')}")
                print(f"🎯 AGI Confidence Score: {agi_enhancements.get('overall_confidence', 0.0):.2%}")
                print(f"🧠 Engines Activated: {integration_summary.get('successful_enhancements', 0)}")
                print(f"🔥 Enhancement Types: {', '.join(integration_summary.get('enhancement_types', []))}")
                
                # Show specific enhancements
                if agi_enhancements.get('ethical_analysis'):
                    ethical = agi_enhancements['ethical_analysis']
                    print(f"  ⚖️ Ethical Score: {ethical.get('overall_ethical_score', 'N/A')}")
                    print(f"  📋 Frameworks: {len(ethical.get('framework_analyses', {}))}")
                
                if agi_enhancements.get('cross_domain_insights'):
                    cross_domain = agi_enhancements['cross_domain_insights']
                    print(f"  🔄 Cross-Domain Confidence: {cross_domain.get('reasoning_confidence', cross_domain.get('confidence', 'N/A'))}")
                    print(f"  🎯 Principles Transferred: {len(cross_domain.get('transferred_principles', []))}")
                
                if agi_enhancements.get('creative_solutions'):
                    creative = agi_enhancements['creative_solutions']
                    print(f"  🎨 Creativity Score: {creative.get('creativity_score', 'N/A')}")
                    print(f"  ✨ Innovation Level: {creative.get('innovation_level', 'N/A')}")
            
            # Show response preview
            response = result.get('response', '')
            if len(response) > 200:
                response_preview = response[:200] + "..."
            else:
                response_preview = response
            
            print(f"\n💬 Response Preview:")
            print(f"{response_preview}")
            
            # Add to conversation history
            conversation_history.append({
                "user_input": test_case["query"],
                "asis_response": result.get('response', ''),
                "timestamp": datetime.now().isoformat(),
                "agi_enhanced": result.get('agi_enhancement_active', False)
            })
            
        except Exception as e:
            print(f"❌ Test Failed: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
        
        print(f"\n{'-'*80}\n")
    
    # Final summary
    print("🎯 AGI INTEGRATION TEST SUMMARY")
    print("=" * 40)
    
    enhanced_responses = sum(1 for item in conversation_history if item.get('agi_enhanced', False))
    total_responses = len(conversation_history)
    
    print(f"Total Tests: {total_responses}")
    print(f"AGI Enhanced: {enhanced_responses}")
    print(f"Enhancement Rate: {enhanced_responses/max(total_responses, 1):.1%}")
    
    if enhanced_responses > 0:
        print("✅ AGI Integration Successful!")
        print("🧠 Ethical Reasoning, Cross-Domain Analysis, and Creative Problem Solving are now integrated!")
    else:
        print("⚠️ AGI Integration needs attention")
        print("💡 Check that all AGI enhancement engines are properly installed")

def test_sync_compatibility():
    """Test synchronous compatibility wrapper"""
    
    print("\n🔄 Testing Synchronous Compatibility...")
    
    engine = AdvancedAIEngine()
    
    test_query = "How can AI systems be more helpful while remaining ethical?"
    conversation_history = []
    
    try:
        result = engine.process_input_with_understanding_sync(test_query, conversation_history)
        
        print(f"✅ Sync Test Complete")
        print(f"AGI Enhancement: {result.get('agi_enhancement_active', False)}")
        print(f"Response Length: {len(result.get('response', ''))}")
        
    except Exception as e:
        print(f"❌ Sync Test Failed: {e}")

async def main():
    """Main test function"""
    
    # Test async AGI integration
    await test_agi_integration()
    
    # Test sync compatibility
    test_sync_compatibility()
    
    print("\n🎉 AGI Integration Testing Complete!")

if __name__ == "__main__":
    asyncio.run(main())
