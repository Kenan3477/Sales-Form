#!/usr/bin/env python3
"""
Check ASIS Database Schemas
"""

import sqlite3
import os

def check_database_schemas():
    print("🔍 CHECKING ASIS DATABASE SCHEMAS")
    print("=" * 50)
    
    databases = [
        'asis_patterns_fixed.db',
        'asis_adaptive_meta_learning.db', 
        'asis_autonomous_research_fixed.db',
        'asis_realtime_learning.db'
    ]
    
    for db_name in databases:
        if os.path.exists(db_name):
            print(f"\n📊 {db_name}:")
            print("-" * 40)
            
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                print(f"\n🗂️  Table: {table_name}")
                
                # Get column info
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                for col in columns:
                    col_id, col_name, col_type, not_null, default, pk = col
                    print(f"   • {col_name} ({col_type})")
            
            conn.close()
        else:
            print(f"\n❌ {db_name}: Not found")

if __name__ == "__main__":
    check_database_schemas()
