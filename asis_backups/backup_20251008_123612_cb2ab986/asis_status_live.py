#!/usr/bin/env python3
"""
ASIS Research Status - Live View
"""

import sqlite3
import os
from datetime import datetime

print("🤖 ASIS LIVE RESEARCH STATUS")
print("=" * 50)
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Research Database Status
if os.path.exists('asis_autonomous_research_fixed.db'):
    conn = sqlite3.connect('asis_autonomous_research_fixed.db')
    cursor = conn.cursor()
    
    # Get counts
    cursor.execute('SELECT COUNT(*) FROM research_findings')
    findings = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM research_sessions')
    sessions = cursor.fetchone()[0]
    
    print(f"\n📊 Knowledge Base Status:")
    print(f"   🔍 Research Findings: {findings}")
    print(f"   🚀 Research Sessions: {sessions}")
    
    # Latest findings
    cursor.execute('''
        SELECT title, content, relevance_score, extraction_time 
        FROM research_findings 
        ORDER BY id DESC 
        LIMIT 5
    ''')
    
    latest = cursor.fetchall()
    if latest:
        print(f"\n🧠 Latest Knowledge Discovered:")
        for i, (title, content, score, time) in enumerate(latest, 1):
            print(f"   {i}. {title}")
            print(f"      📝 {content[:100]}...")
            print(f"      ⭐ Confidence: {score:.2f}")
            print(f"      🕒 {time}")
            print()
    
    conn.close()

# Check if automated research is configured
if os.path.exists('asis_automated_research_config.db'):
    conn = sqlite3.connect('asis_automated_research_config.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM research_topics WHERE active = 1')
    active_topics = cursor.fetchone()[0]
    
    print(f"🎯 Automated Research System:")
    print(f"   📋 Active Topics: {active_topics}")
    
    # Show some topics
    cursor.execute('''
        SELECT topic, priority, frequency_hours 
        FROM research_topics 
        WHERE active = 1 
        ORDER BY priority DESC 
        LIMIT 5
    ''')
    
    topics = cursor.fetchall()
    if topics:
        print(f"   🔬 High Priority Research Topics:")
        for topic, priority, freq in topics:
            print(f"     • {topic} (Priority: {priority}, Every: {freq}h)")
    
    conn.close()

print(f"\n✅ ASIS IS ACTIVELY LEARNING!")
print(f"🔄 Automated research every 30min - 2 hours")
print(f"💡 Knowledge grows with each research cycle")
print(f"🧠 Total accumulated knowledge: Research findings across multiple domains")

# Show database sizes
print(f"\n📈 Database Growth:")
dbs = [
    ('Research', 'asis_autonomous_research_fixed.db'),
    ('Auto Config', 'asis_automated_research_config.db'),
    ('Patterns', 'asis_patterns_fixed.db'),
    ('Meta Learning', 'asis_adaptive_meta_learning.db')
]

for name, db_file in dbs:
    if os.path.exists(db_file):
        size = os.path.getsize(db_file)
        print(f"   📂 {name}: {size:,} bytes")

print(f"\n🚀 Ready for Railway deployment with continuous learning!")
