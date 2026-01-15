#!/usr/bin/env python3
"""
ASIS Data Processor
Purpose: data analysis and processing tool  
"""

import json
from datetime import datetime

class DataProcessor:
    """Data processing utility"""
    
    def __init__(self):
        self.session_id = "20250922_165701"
        print("[ASIS] Data Processor initialized")
    
    def process_json_data(self, data):
        """Process JSON data"""
        if isinstance(data, dict):
            processed = {k: str(v).upper() if isinstance(v, str) else v for k, v in data.items()}
        elif isinstance(data, list):
            processed = [str(item).upper() if isinstance(item, str) else item for item in data]
        else:
            processed = str(data).upper()
        
        return processed
    
    def generate_summary(self, data):
        """Generate data summary"""
        return {
            "total_items": len(data) if hasattr(data, '__len__') else 1,
            "data_type": type(data).__name__,
            "processed_at": datetime.now().isoformat(),
            "session_id": self.session_id
        }

def main():
    """Test data processor"""
    processor = DataProcessor()
    
    test_data = [
        {"name": "test1", "value": 100},
        {"name": "test2", "value": 200}
    ]
    
    processed = processor.process_json_data(test_data)
    summary = processor.generate_summary(test_data)
    
    print(f"[ASIS] Processed: {processed}")
    print(f"[ASIS] Summary: {summary}")
    print("[ASIS] Data processing completed successfully")

if __name__ == "__main__":
    main()
