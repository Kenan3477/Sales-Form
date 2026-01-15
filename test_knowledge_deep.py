#!/usr/bin/env python3
"""
ASIS Knowledge Expansion Deep Test
=================================
Check if ASIS actually stores and expands knowledge during interactions
"""

print("🔍 Deep Testing ASIS Knowledge Expansion...")
print("=" * 60)

try:
    from asis_autonomous_research_fixed import ASISAutonomousResearch
    from asis_complete_training_interface import asis_interface
    
    research = ASISAutonomousResearch()
    
    print("1. 📊 Current Knowledge State:")
    knowledge = research.get_knowledge_summary()
    print(f"   Total Entries: {knowledge['total_entries']}")
    print(f"   Recent Activity: {knowledge['recent_activity_7days']}")
    print(f"   Knowledge Growth Active: {knowledge['knowledge_growth_active']}")
    
    print("\n2. 🔬 Force Research Session (Manual Knowledge Expansion):")
    # Force a research session to see if it actually adds knowledge
    research_result = research.force_research_session("artificial intelligence", "AI machine learning")
    print(f"   Forced Session: {research_result['session_id']}")
    print(f"   Findings: {research_result.get('findings_count', 0)}")
    
    print("\n3. 📊 Knowledge After Forced Research:")
    knowledge_after = research.get_knowledge_summary()
    print(f"   Total Entries: {knowledge_after['total_entries']}")
    print(f"   Knowledge Growth: {knowledge_after['total_entries'] - knowledge['total_entries']} new entries")
    
    print("\n4. 🤖 Test ASIS Response Learning:")
    # Test if ASIS learns from interactions
    print("   Processing user input to see if ASIS stores patterns...")
    response1 = asis_interface.process_user_input("What is machine learning?")
    print(f"   Response generated (patterns recognized: {response1['patterns_recognized']})")
    
    response2 = asis_interface.process_user_input("Tell me about artificial intelligence")
    print(f"   Response generated (patterns recognized: {response2['patterns_recognized']})")
    
    print("\n5. 📈 Learning Effectiveness Analysis:")
    learning_analysis = research.analyze_learning_effectiveness()
    print(f"   Effectiveness Score: {learning_analysis['effectiveness_score']:.1%}")
    print(f"   Knowledge Expanding: {learning_analysis['knowledge_expanding']}")
    print(f"   Learning Trend: {learning_analysis['learning_trend']}")
    
    print("\n6. 🎯 FINAL ASSESSMENT:")
    if knowledge_after['total_entries'] > knowledge['total_entries']:
        print("✅ ASIS IS expanding its knowledge base!")
        print("✅ Forced research sessions add new knowledge")
        print("✅ Knowledge storage system is functional")
    else:
        print("⚠️  Knowledge base is not expanding automatically")
        print("⚠️  Research system may need activation")
    
    if response1['patterns_recognized'] > 0 or response2['patterns_recognized'] > 0:
        print("✅ ASIS IS recognizing and learning from patterns")
        print("✅ Interaction-based learning is active")
    else:
        print("⚠️  Pattern recognition may be limited")
    
    print(f"\n🔍 AUTONOMOUS RESEARCH STATUS:")
    print(f"   Database Size: {knowledge_after['total_entries']} entries")
    print(f"   Last 7 Days Activity: {knowledge_after['recent_activity_7days']} entries")
    
    # Check if threads would start with active research
    print("\n7. 🚀 Testing Background Research Activation:")
    import threading
    active_threads = threading.active_count()
    research.start_autonomous_research()
    new_active_threads = threading.active_count()
    
    print(f"   Threads before: {active_threads}")
    print(f"   Threads after: {new_active_threads}")
    print(f"   New research threads: {new_active_threads - active_threads}")
    
    if new_active_threads > active_threads:
        print("✅ Background research threads are starting!")
        print("✅ Continuous knowledge expansion should be active")
    else:
        print("⚠️  Background research threads may not be starting")
        print("⚠️  Manual research sessions still work")
    
except Exception as e:
    print(f"❌ Error during deep testing: {e}")
    import traceback
    traceback.print_exc()
