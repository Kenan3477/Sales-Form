#!/usr/bin/env python3
"""
ASIS Logging Configuration
Enhanced by True Self-Modification Engine
"""

import logging
import sys
from datetime import datetime

def setup_asis_logging(level=logging.INFO):
    """Setup enhanced logging for ASIS"""
    
    # Create logger
    logger = logging.getLogger('ASIS')
    logger.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.FileHandler(f'asis_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

# Auto-configure on import
ASIS_LOGGER = setup_asis_logging()
