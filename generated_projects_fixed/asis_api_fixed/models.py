#!/usr/bin/env python3
"""
ASIS API Service Models
======================
"""

import json
import time
from typing import Dict, Any, Optional

class AsisApiModel:
    """Base model for API objects"""
    
    def __init__(self, data: Dict[str, Any] = None):
        self.data = data or {}
        self.created_at = time.time()
        self.updated_at = self.created_at
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            "data": self.data,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def to_json(self) -> str:
        """Convert model to JSON"""
        return json.dumps(self.to_dict())

class AsisDataModel(AsisApiModel):
    """Data model for API entries"""
    
    def __init__(self, key: str, value: Any):
        super().__init__()
        self.key = key
        self.value = value
    
    def update_value(self, new_value: Any) -> None:
        """Update the value"""
        self.value = new_value
        self.updated_at = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            "key": self.key,
            "value": self.value
        })
        return base_dict

class AsisRequestModel(AsisApiModel):
    """Model for API requests"""
    
    def __init__(self, method: str, endpoint: str, data: Dict[str, Any] = None):
        super().__init__(data)
        self.method = method
        self.endpoint = endpoint
        self.response_code = None
        self.processing_time = 0
    
    def set_response(self, code: int, processing_time: float) -> None:
        """Set response details"""
        self.response_code = code
        self.processing_time = processing_time
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            "method": self.method,
            "endpoint": self.endpoint,
            "response_code": self.response_code,
            "processing_time": self.processing_time
        })
        return base_dict
