#!/usr/bin/env python3
"""
ASIS Data Processor Utilities
=============================
"""

import os
import json
from typing import Any, Dict

class AsisUtils:
    """Utility functions"""
    
    @staticmethod
    def validate_file(file_path: str) -> bool:
        """Validate if file exists and is readable"""
        return os.path.exists(file_path) and os.path.isfile(file_path)
    
    @staticmethod
    def safe_json_load(file_path: str) -> Dict[str, Any]:
        """Safely load JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return json.load(f)
        except Exception:
            return {}
    
    @staticmethod
    def format_size(size_bytes: int) -> str:
        """Format file size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f}TB"
