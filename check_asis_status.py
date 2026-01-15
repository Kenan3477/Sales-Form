#!/usr/bin/env python3
"""
Quick ASIS Research Status Check
"""

import sqlite3
import os
from datetime import datetime

def show_live_status():
    print("🤖 ASIS CURRENT RESEARCH STATUS")
    print("=" * 50)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check research database
    if os.path.exists('asis_autonomous_research_fixed.db'):
        conn = sqlite3.connect('asis_autonomous_research_fixed.db')
        cursor = conn.cursor()
        
        # Total findings
        cursor.execute('SELECT COUNT(*) FROM research_findings')
        total_findings = cursor.fetchone()[0]
        
        # Total sessions
        cursor.execute('SELECT COUNT(*) FROM research_sessions')
        total_sessions = cursor.fetchone()[0]
        
        print(f"📊 Knowledge Base:")
        print(f"   • Research Findings: {total_findings}")
        print(f"   • Research Sessions: {total_sessions}")
        
        # Latest discoveries
        cursor.execute('''
            SELECT title, content, relevance_score, extraction_time 
            FROM research_findings 
            ORDER BY extraction_time DESC 
            LIMIT 3
        ''')
        
        findings = cursor.fetchall()
        if findings:
            print(f"\n🔍 Latest 3 Discoveries:")
            for i, (title, content, score, time) in enumerate(findings, 1):
                print(f"   {i}. {title}")
                print(f"      Content: {content[:80]}...")
                print(f"      Confidence: {score:.2f} | Time: {time}")
        
        # Recent sessions
        cursor.execute('''
            SELECT topic, start_time, status, findings_count 
            FROM research_sessions 
            ORDER BY start_time DESC 
            LIMIT 3
        ''')
        
        sessions = cursor.fetchall()
        if sessions:
            print(f"\n🚀 Latest 3 Research Sessions:")
            for i, (topic, start_time, status, findings_count) in enumerate(sessions, 1):
                status_icon = "✅" if status == "completed" else "🔄" if status == "active" else "⚠️"
                print(f"   {i}. {status_icon} {topic}")
                print(f"      Findings: {findings_count} | Time: {start_time}")
        
        conn.close()
    
    # Check automated topics
    if os.path.exists('asis_automated_research_config.db'):
        conn = sqlite3.connect('asis_automated_research_config.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM research_topics WHERE active = 1')
        active_topics = cursor.fetchone()[0]
        
        print(f"\n🎯 Automated Research Configuration:")
        print(f"   • Active Topics: {active_topics}")
        
        # Next ready topics
        cursor.execute('''
            SELECT topic, priority, last_researched
            FROM research_topics 
            WHERE active = 1 
            AND (last_researched IS NULL OR 
                 datetime(last_researched, '+' || frequency_hours || ' hours') <= datetime('now'))
            ORDER BY priority DESC 
            LIMIT 3
        ''')
        
        ready_topics = cursor.fetchall()
        if ready_topics:
            print(f"   • Next Topics Ready for Research:")
            for topic, priority, last_researched in ready_topics:
                last_time = "Never" if not last_researched else last_researched
                print(f"     - {topic} (Priority: {priority}, Last: {last_time})")
        
        conn.close()
    
    print(f"\n✅ ASIS is actively learning and expanding knowledge!")
    print(f"🔄 Research runs automatically every 30 minutes - 2 hours")

if __name__ == "__main__":
    show_live_status()
