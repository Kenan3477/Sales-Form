#!/usr/bin/env python3
"""
ASIS Research Database Status Checker
"""

import sqlite3
import os
from datetime import datetime

def check_database_status():
    print("🔍 ASIS RESEARCH DATABASE STATUS")
    print("=" * 50)
    
    # Check research databases
    research_dbs = [
        'asis_autonomous_research_fixed.db',
        'asis_automated_research_config.db', 
        'asis_research_knowledge.db',
        'asis_adaptive_meta_learning.db',
        'asis_realtime_learning.db',
        'asis_patterns_fixed.db'
    ]

    total_records = 0
    
    for db_name in research_dbs:
        if os.path.exists(db_name):
            print(f'\n📊 {db_name}:')
            try:
                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()
                
                # Get table names
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                
                db_total = 0
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
                    count = cursor.fetchone()[0]
                    print(f'  • {table_name}: {count} records')
                    db_total += count
                
                conn.close()
                total_records += db_total
                print(f'  📈 Database Total: {db_total} records')
                
            except Exception as e:
                print(f'  ❌ Error reading database: {e}')
        else:
            print(f'\n❌ {db_name}: File not found')
    
    print(f"\n🎯 OVERALL RESEARCH DATA STATUS:")
    print(f"  • Total Records Across All Databases: {total_records}")
    print(f"  • Research Active: {'YES' if total_records > 0 else 'NO'}")
    
    # Check for active patterns
    pattern_files = [
        'asis_patterns_fixed.db',
        'asis_adaptive_meta_learning.db'
    ]
    
    pattern_count = 0
    for pattern_file in pattern_files:
        if os.path.exists(pattern_file):
            try:
                conn = sqlite3.connect(pattern_file)
                cursor = conn.cursor()
                
                # Check for pattern-specific tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%pattern%'")
                pattern_tables = cursor.fetchall()
                
                for table in pattern_tables:
                    cursor.execute(f'SELECT COUNT(*) FROM {table[0]}')
                    count = cursor.fetchone()[0]
                    pattern_count += count
                
                conn.close()
            except:
                pass
    
    print(f"  • Pattern Data Available: {pattern_count} patterns")
    
    # Check recent research activity
    if os.path.exists('asis_autonomous_research_fixed.db'):
        try:
            conn = sqlite3.connect('asis_autonomous_research_fixed.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='research_sessions'")
            if cursor.fetchone():
                cursor.execute("SELECT COUNT(*) FROM research_sessions WHERE date(start_time) = date('now')")
                today_sessions = cursor.fetchone()[0]
                print(f"  • Research Sessions Today: {today_sessions}")
            
            conn.close()
        except:
            pass

if __name__ == "__main__":
    check_database_status()
