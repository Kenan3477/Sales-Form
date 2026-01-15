#!/usr/bin/env python3
"""
ASIS API Database Manager
=========================
"""

import sqlite3
import json
import time
from typing import Dict, List, Any, Optional

class AsisDatabase:
    """Database manager for API service"""
    
    def __init__(self, db_path: str = "asis_api.db"):
        self.db_path = db_path
        self.connection = None
        self._initialize_schema()
    
    def _initialize_schema(self):
        """Initialize database schema"""
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS api_keys (
                    id INTEGER PRIMARY KEY,
                    key_name TEXT UNIQUE,
                    key_value TEXT,
                    permissions TEXT,
                    created_at REAL,
                    active BOOLEAN DEFAULT 1
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS request_logs (
                    id INTEGER PRIMARY KEY,
                    timestamp REAL,
                    method TEXT,
                    endpoint TEXT,
                    ip_address TEXT,
                    response_code INTEGER,
                    processing_time REAL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cached_responses (
                    id INTEGER PRIMARY KEY,
                    request_hash TEXT UNIQUE,
                    response_data TEXT,
                    created_at REAL,
                    expires_at REAL
                )
            """)
    
    def log_request(self, method: str, endpoint: str, ip: str, response_code: int, processing_time: float) -> bool:
        """Log API request"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO request_logs (timestamp, method, endpoint, ip_address, response_code, processing_time) VALUES (?, ?, ?, ?, ?, ?)",
                    (time.time(), method, endpoint, ip, response_code, processing_time)
                )
            return True
        except Exception:
            return False
    
    def create_api_key(self, key_name: str, permissions: List[str]) -> Optional[str]:
        """Create new API key"""
        
        try:
            key_value = f"asis_key_{int(time.time())}"
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO api_keys (key_name, key_value, permissions, created_at) VALUES (?, ?, ?, ?)",
                    (key_name, key_value, json.dumps(permissions), time.time())
                )
            
            return key_value
        except Exception:
            return None
    
    def validate_api_key(self, key_value: str) -> Optional[Dict[str, Any]]:
        """Validate API key"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT key_name, permissions, active FROM api_keys WHERE key_value = ?",
                    (key_value,)
                )
                row = cursor.fetchone()
                
                if row and row[2]:  # active
                    return {
                        "key_name": row[0],
                        "permissions": json.loads(row[1]),
                        "active": bool(row[2])
                    }
        except Exception:
            pass
        
        return None
    
    def get_request_stats(self) -> Dict[str, Any]:
        """Get request statistics"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT COUNT(*), AVG(processing_time) FROM request_logs")
                count, avg_time = cursor.fetchone()
                
                cursor = conn.execute("SELECT response_code, COUNT(*) FROM request_logs GROUP BY response_code")
                status_codes = dict(cursor.fetchall())
                
                return {
                    "total_requests": count or 0,
                    "average_processing_time": avg_time or 0,
                    "status_codes": status_codes
                }
        except Exception:
            return {"total_requests": 0, "average_processing_time": 0, "status_codes": {}}
