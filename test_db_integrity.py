#!/usr/bin/env python3
"""
Database integrity checker for ASIS
"""
import sqlite3
import os

def test_database(db_path):
    """Test database integrity"""
    try:
        print(f"Testing {db_path}...")
        if not os.path.exists(db_path):
            print(f"❌ {db_path} does not exist")
            return False
            
        conn = sqlite3.connect(db_path)
        result = conn.execute("PRAGMA integrity_check;").fetchone()
        conn.close()
        
        if result[0] == 'ok':
            print(f"✅ {db_path} is OK")
            return True
        else:
            print(f"❌ {db_path} has issues: {result[0]}")
            return False
            
    except Exception as e:
        print(f"❌ {db_path} ERROR: {e}")
        return False

if __name__ == "__main__":
    databases = [
        "asis_consciousness.db",
        "asis_episodic_memory.db", 
        "asis_persistent_memory.db",
        "enhanced_memory.db"
    ]
    
    print("🔍 ASIS Database Integrity Check")
    print("=" * 40)
    
    for db in databases:
        test_database(db)
    
    print("\n✅ Database integrity check complete")