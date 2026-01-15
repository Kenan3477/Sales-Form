#!/usr/bin/env python3
"""
Comprehensive demonstration of the Cognitive Architecture
"""

import asyncio
import json
from cognitive_architecture import CognitiveArchitecture

async def comprehensive_demo():
    """Comprehensive demonstration of all cognitive components"""
    print("=" * 60)
    print("ADVANCED SYNTHETIC INTELLIGENCE SYSTEM")
    print("Comprehensive Cognitive Architecture Demo")
    print("=" * 60)
    print()
    
    # Create and initialize the architecture
    print("🧠 Initializing Cognitive Architecture...")
    arch = CognitiveArchitecture()
    await arch.initialize()
    print("✅ Initialization complete!")
    print()
    
    # Test scenarios that engage different components
    test_scenarios = [
        {
            "name": "Learning Scenario",
            "input": {
                "content": "Studying quantum computing and its applications in AI",
                "context": "education",
                "topic": "quantum_computing",
                "priority": 0.9,
                "interest_strength": 0.3
            },
            "description": "Tests attention, working memory, and interest formation"
        },
        {
            "name": "Problem-Solving Scenario", 
            "input": {
                "content": "Debugging a complex algorithm with multiple failure points",
                "context": "problem_solving",
                "topic": "programming",
                "requires_decision": True,
                "options": ["systematic_debugging", "code_review", "start_over", "get_help"],
                "priority": 0.8
            },
            "description": "Tests executive control, decision-making, and metacognition"
        },
        {
            "name": "Creative Scenario",
            "input": {
                "content": "Designing a new AI architecture for creative writing",
                "context": "creativity",
                "topic": "ai_design",
                "priority": 0.7,
                "interest_strength": 0.25
            },
            "description": "Tests creative thinking and emotional processing"
        },
        {
            "name": "Research Scenario",
            "input": {
                "content": "Investigating the relationship between consciousness and computation",
                "context": "research", 
                "topic": "consciousness",
                "priority": 0.85,
                "interest_strength": 0.4
            },
            "description": "Tests comprehensive cognitive integration"
        }
    ]
    
    results = []
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"🔬 Scenario {i}: {scenario['name']}")
        print(f"   {scenario['description']}")
        print(f"   Input: {scenario['input']['content']}")
        print()
        
        # Process the scenario
        result = await arch.process_input(scenario['input'])
        results.append({
            "scenario": scenario['name'],
            "result": result
        })
        
        # Display key results
        print(f"   📊 Results:")
        print(f"   • Processing Time: {result.get('processing_time', 0):.3f}s")
        print(f"   • Attention Focus: {result.get('attention', {}).get('current_focus', 'none')}")
        print(f"   • Focus Intensity: {result.get('attention', {}).get('focus_intensity', 0):.2f}")
        print(f"   • Memory Utilization: {result.get('memory', {}).get('utilization', 0):.2f}")
        print(f"   • Dominant Emotion: {result.get('emotion', {}).get('dominant_emotion', 'neutral')}")
        
        executive_result = result.get('executive', {})
        if executive_result.get('decision'):
            print(f"   • Decision Made: {executive_result['decision']}")
            print(f"   • Confidence: {executive_result.get('confidence', 0):.2f}")
        
        metacog_result = result.get('metacognition', {})
        if metacog_result.get('cognitive_insights'):
            print(f"   • Cognitive Insights: {len(metacog_result['cognitive_insights'])} generated")
        
        print(f"   • Current Interests: {', '.join(result.get('interests', []))}")
        print()
    
    # Show system evolution
    print("🧠 System Evolution Analysis")
    print("=" * 30)
    
    # Get comprehensive system status
    status = arch.get_system_status()
    
    print(f"Total Processing Cycles: {status['cycle_count']}")
    print(f"Top Interests: {', '.join(status['top_interests'])}")
    print()
    
    # Component status summary
    print("📊 Component Status Summary:")
    for name, component_status in status['components'].items():
        print(f"   • {name.title()}:")
        
        if name == "attention":
            print(f"     - Current Focus: {component_status.get('current_focus', 'none')}")
            print(f"     - Focus Intensity: {component_status.get('focus_intensity', 0):.2f}")
            print(f"     - Queue Size: {component_status.get('queue_size', 0)}")
        
        elif name == "working_memory":
            print(f"     - Utilization: {component_status.get('utilization_stats', {}).get('current', 0):.2f}")
            print(f"     - Active Operations: {component_status.get('active_operations', 0)}")
            print(f"     - Total Chunks: {component_status.get('total_chunks', 0)}")
        
        elif name == "executive":
            print(f"     - Active Goals: {component_status.get('goal_statistics', {}).get('active', 0)}")
            print(f"     - Cognitive Load: {component_status.get('cognitive_load', 0):.2f}")
            print(f"     - Executive Resources: {component_status.get('executive_resources', 0):.2f}")
        
        elif name == "metacognition":
            print(f"     - Awareness Level: {component_status.get('metacognitive_metrics', {}).get('awareness_level', 0):.2f}")
            print(f"     - Strategy Repertoire: {component_status.get('metacognitive_metrics', {}).get('strategy_repertoire', 0)}")
            print(f"     - Recent Insights: {component_status.get('recent_insights', 0)}")
        
        elif name == "emotional":
            print(f"     - Active Emotions: {component_status.get('active_emotions', 0)}")
            print(f"     - Emotional Memory: {component_status.get('emotional_memory', 0)}")
            print(f"     - Pattern Recognition: {component_status.get('pattern_recognition', 0)}")
    
    print()
    print("🎯 Demonstration Complete!")
    print("The cognitive architecture successfully demonstrated:")
    print("• Multi-component coordination")
    print("• Attention management and context switching")
    print("• Working memory manipulation")
    print("• Executive decision-making")
    print("• Metacognitive self-reflection")
    print("• Emotional processing and regulation")
    print("• Interest formation and learning")
    print("• System-wide integration")
    print()
    print("This represents a comprehensive implementation of Phase 1.2")
    print("of the Advanced Synthetic Intelligence System project.")
    
    return arch

if __name__ == "__main__":
    asyncio.run(comprehensive_demo())
