#!/usr/bin/env python3
"""
ASIS Knowledge Expansion Live Test - Real research attempt
"""

import sqlite3
import os
import sys
from datetime import datetime
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🔍 ASIS Knowledge Expansion LIVE TEST")
print("=" * 50)

def check_database_before_after(db_path, description):
    """Check database content before and after research"""
    
    if not os.path.exists(db_path):
        print(f"  ❌ {description} database not found!")
        return 0, 0
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT COUNT(*) FROM research_findings')
        findings_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM research_sessions')
        sessions_count = cursor.fetchone()[0]
        
        conn.close()
        return findings_count, sessions_count
        
    except Exception as e:
        print(f"  ❌ Error querying {description}: {e}")
        conn.close()
        return 0, 0

# Check initial state
print("\n📊 BEFORE Research Session:")
before_findings, before_sessions = check_database_before_after('asis_autonomous_research_fixed.db', 'Research')
print(f"  Findings: {before_findings}, Sessions: {before_sessions}")

# Attempt actual research
print("\n🚀 Starting REAL Research Session...")
try:
    from asis_autonomous_research_fixed import ASISAutonomousResearch
    
    research_system = ASISAutonomousResearch()
    
    # Force a research session with proper parameters
    print("  🔬 Researching: 'Artificial Intelligence trends 2024'")
    result = research_system.force_research_session(
        topic="AI trends 2024", 
        search_terms="artificial intelligence trends 2024 machine learning"
    )
    
    print(f"  Research result: {result}")
    
    # Wait a moment for processing
    time.sleep(2)
    
except Exception as e:
    print(f"  ❌ Error during research: {e}")
    import traceback
    traceback.print_exc()

# Check final state
print("\n📊 AFTER Research Session:")
after_findings, after_sessions = check_database_before_after('asis_autonomous_research_fixed.db', 'Research')
print(f"  Findings: {after_findings}, Sessions: {after_sessions}")

# Show the difference
findings_added = after_findings - before_findings
sessions_added = after_sessions - before_sessions

print(f"\n🎯 KNOWLEDGE EXPANSION RESULTS:")
print(f"  New Findings Added: {findings_added}")
print(f"  New Sessions Added: {sessions_added}")

if findings_added > 0:
    print("  ✅ SUCCESS: ASIS is actually storing research findings!")
    
    # Show recent findings
    conn = sqlite3.connect('asis_autonomous_research_fixed.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT topic, title, content, relevance_score, timestamp 
        FROM research_findings 
        ORDER BY timestamp DESC LIMIT 3
    ''')
    recent = cursor.fetchall()
    
    print("  Recent discoveries:")
    for topic, title, content, score, timestamp in recent:
        print(f"    • {topic}: {title}")
        print(f"      Content: {content[:100]}...")
        print(f"      Score: {score}, Time: {timestamp}")
    
    conn.close()
    
else:
    print("  ⚠️  WARNING: No new findings stored - research may not be working properly")

# Test interaction-based learning
print(f"\n🧠 Testing Interaction-Based Learning...")
try:
    # Simulate learning from this interaction
    if hasattr(research_system, 'learn_from_interaction'):
        learning_result = research_system.learn_from_interaction(
            "User asked about knowledge expansion capabilities",
            "verification_request",
            {"context": "deployment_testing", "priority": "high"}
        )
        print(f"  Learning result: {learning_result}")
    else:
        print("  ⚠️  No interaction learning method found")
        
except Exception as e:
    print(f"  ❌ Error testing interaction learning: {e}")

print("\n" + "=" * 50)
print("✅ Live Knowledge Expansion Test Complete!")
print("✅ This test shows if ASIS actually expands its knowledge autonomously!")
