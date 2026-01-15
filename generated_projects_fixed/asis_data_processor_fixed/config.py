#!/usr/bin/env python3
"""
ASIS Data Processor Configuration
=================================
"""

class AsisConfig:
    """Configuration settings"""
    
    # Processing settings
    BATCH_SIZE = 1000
    MAX_FILE_SIZE = 1024 * 1024 * 10  # 10MB
    SUPPORTED_FORMATS = ['json', 'csv', 'txt']
    
    # Output settings
    OUTPUT_FORMAT = 'json'
    INCLUDE_METADATA = True
    
    # Performance settings
    ENABLE_CACHING = True
    MAX_CACHE_SIZE = 100
    TIMEOUT_SECONDS = 30

CONFIG = AsisConfig()
