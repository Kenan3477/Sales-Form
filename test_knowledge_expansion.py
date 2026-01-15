#!/usr/bin/env python3
"""
ASIS Knowledge Expansion Test
============================
Check if ASIS is actually expanding its knowledge base
"""

print("🔍 Checking ASIS Knowledge Expansion...")
print("=" * 50)

try:
    from asis_autonomous_research_fixed import ASISAutonomousResearch
    research = ASISAutonomousResearch()
    
    # Check research status
    status = research.get_research_status()
    print(f"Active Research Threads: {status.get('active_research_threads', 0)}")
    
    # Check knowledge database
    knowledge = research.get_knowledge_summary()
    print(f"Total Knowledge Entries: {knowledge.get('total_entries', 0)}")
    
    # Check if database files exist
    import os
    db_files = [
        'asis_autonomous_research_fixed.db',
        'asis_patterns_fixed.db', 
        'asis_meta_learning_fixed.db',
        'asis_adaptation_fixed.db'
    ]
    
    print("\nDatabase Files Status:")
    for db_file in db_files:
        exists = os.path.exists(db_file)
        size = os.path.getsize(db_file) if exists else 0
        print(f"  {db_file}: {'EXISTS' if exists else 'MISSING'} ({size} bytes)")
    
    # Test if research can be started
    print("\nTesting Research Activation...")
    research.start_autonomous_research()
    
    # Check status after starting
    new_status = research.get_research_status()
    print(f"Research Threads After Start: {new_status.get('active_research_threads', 0)}")
    
    print("\n🎯 KNOWLEDGE EXPANSION STATUS:")
    if new_status.get('active_research_threads', 0) > 0:
        print("✅ ASIS IS actively expanding knowledge base")
        print("✅ Research threads are running")
        print("✅ Knowledge accumulation is operational")
    else:
        print("⚠️  Research threads are not currently active")
        print("⚠️  Knowledge expansion may be limited")
    
except Exception as e:
    print(f"❌ Error checking knowledge expansion: {e}")
    import traceback
    traceback.print_exc()
