#!/usr/bin/env python3
"""
ASIS Generated API Service
==========================
"""

import json
import sqlite3
import os
from typing import Dict, List, Any, Optional

class AsisApiService:
    """ASIS Generated REST API Service"""
    
    def __init__(self):
        self.database_path = "api_service.db"
        self.request_count = 0
        self.active_sessions = {}
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize the service database"""
        
        with sqlite3.connect(self.database_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS api_requests (
                    id INTEGER PRIMARY KEY,
                    endpoint TEXT,
                    method TEXT,
                    timestamp REAL,
                    response_code INTEGER
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS api_data (
                    id INTEGER PRIMARY KEY,
                    key TEXT UNIQUE,
                    value TEXT,
                    created_at REAL,
                    updated_at REAL
                )
            """)
    
    def handle_get_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle GET requests"""
        
        self.request_count += 1
        
        if endpoint == "/status":
            return self._get_service_status()
        elif endpoint == "/data":
            return self._get_all_data()
        elif endpoint.startswith("/data/"):
            key = endpoint.split("/")[-1]
            return self._get_data_by_key(key)
        else:
            return {"error": "Endpoint not found", "code": 404}
    
    def handle_post_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle POST requests"""
        
        self.request_count += 1
        
        if endpoint == "/data":
            return self._create_data_entry(data)
        elif endpoint == "/process":
            return self._process_data(data)
        else:
            return {"error": "Endpoint not found", "code": 404}
    
    def _get_service_status(self) -> Dict[str, Any]:
        """Get service status"""
        
        return {
            "status": "active",
            "requests_handled": self.request_count,
            "active_sessions": len(self.active_sessions),
            "database_connected": os.path.exists(self.database_path)
        }
    
    def _get_all_data(self) -> Dict[str, Any]:
        """Get all stored data"""
        
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.execute("SELECT key, value FROM api_data")
                data = {row[0]: json.loads(row[1]) for row in cursor.fetchall()}
                return {"data": data, "count": len(data)}
        except Exception as e:
            return {"error": str(e), "code": 500}
    
    def _get_data_by_key(self, key: str) -> Dict[str, Any]:
        """Get data by key"""
        
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.execute("SELECT value FROM api_data WHERE key = ?", (key,))
                row = cursor.fetchone()
                
                if row:
                    return {"data": json.loads(row[0])}
                else:
                    return {"error": "Key not found", "code": 404}
        except Exception as e:
            return {"error": str(e), "code": 500}
    
    def _create_data_entry(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new data entry"""
        
        try:
            key = data.get("key")
            value = data.get("value")
            
            if not key or not value:
                return {"error": "Missing key or value", "code": 400}
            
            with sqlite3.connect(self.database_path) as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO api_data (key, value, created_at, updated_at) VALUES (?, ?, ?, ?)",
                    (key, json.dumps(value), self.request_count, self.request_count)
                )
                
            return {"success": True, "key": key}
        except Exception as e:
            return {"error": str(e), "code": 500}
    
    def _process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process submitted data"""
        
        processed_data = {
            "input_keys": len(data.keys()),
            "processed_at": self.request_count,
            "result": "processed",
            "data_size": len(str(data))
        }
        
        return {"processed_data": processed_data}

def main():
    """Main entry point"""
    api = AsisApiService()
    
    # Test the API
    print("Testing API Service...")
    
    # Test GET status
    status = api.handle_get_request("/status")
    print(f"Status: {status}")
    
    # Test POST data
    test_data = {"key": "test", "value": {"message": "Hello ASIS"}}
    create_result = api.handle_post_request("/data", test_data)
    print(f"Create: {create_result}")
    
    # Test GET data
    get_result = api.handle_get_request("/data/test")
    print(f"Get: {get_result}")
    
    return True

if __name__ == "__main__":
    main()
