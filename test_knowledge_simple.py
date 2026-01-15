#!/usr/bin/env python3
"""
Simple Knowledge Expansion Test - Quick verification
"""

import sqlite3
import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🔍 Simple ASIS Knowledge Expansion Test")
print("=" * 50)

# Test 1: Check database files existence and sizes
databases = [
    'asis_autonomous_research_fixed.db',
    'asis_adaptive_meta_learning.db',
    'asis_builtin_knowledge.db',
    'asis_complete_memory.db'
]

print("\n📊 Database Status:")
for db in databases:
    if os.path.exists(db):
        size = os.path.getsize(db)
        print(f"  ✅ {db}: {size} bytes")
    else:
        print(f"  ❌ {db}: Not found")

# Test 2: Check research database content
print("\n🔬 Research Database Content:")
try:
    conn = sqlite3.connect('asis_autonomous_research_fixed.db')
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"  Tables found: {[t[0] for t in tables]}")
    
    # Check research sessions
    cursor.execute("SELECT COUNT(*) FROM research_sessions")
    sessions_count = cursor.fetchone()[0]
    print(f"  Research sessions: {sessions_count}")
    
    # Check findings
    cursor.execute("SELECT COUNT(*) FROM research_findings")
    findings_count = cursor.fetchone()[0]
    print(f"  Research findings: {findings_count}")
    
    # Check recent findings
    if findings_count > 0:
        cursor.execute("SELECT topic, summary, timestamp FROM research_findings ORDER BY timestamp DESC LIMIT 3")
        recent = cursor.fetchall()
        print("  Recent findings:")
        for topic, summary, timestamp in recent:
            print(f"    • {topic}: {summary[:50]}...")
    
    conn.close()
    
except Exception as e:
    print(f"  ❌ Error checking research database: {e}")

# Test 3: Quick autonomous research test
print("\n🚀 Testing Autonomous Research:")
try:
    from asis_autonomous_research_fixed import ASISAutonomousResearch
    
    research_system = ASISAutonomousResearch()
    
    # Check if research is active
    status = research_system.get_research_status()
    print(f"  Research Status: {status}")
    
    # Try to start a quick research session
    print("  Attempting forced research session...")
    result = research_system.force_research_session("AI technology trends", duration=5)
    print(f"  Research result: {result}")
    
    # Check knowledge summary
    summary = research_system.get_knowledge_summary()
    print(f"  Knowledge entries: {summary.get('total_entries', 0)}")
    
except Exception as e:
    print(f"  ❌ Error testing research system: {e}")

# Test 4: Meta-learning database
print("\n🧠 Meta-Learning Database:")
try:
    conn = sqlite3.connect('asis_adaptive_meta_learning.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"  Tables: {[t[0] for t in tables]}")
    
    if ('patterns',) in tables:
        cursor.execute("SELECT COUNT(*) FROM patterns")
        patterns_count = cursor.fetchone()[0]
        print(f"  Pattern count: {patterns_count}")
    
    conn.close()
    
except Exception as e:
    print(f"  ❌ Error checking meta-learning database: {e}")

print("\n✅ Simple knowledge expansion test completed!")
print("=" * 50)
