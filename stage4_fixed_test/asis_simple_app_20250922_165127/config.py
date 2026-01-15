#!/usr/bin/env python3
"""
Configuration for ASIS Simple App
"""

import os

CONFIG = {
    "app_name": "ASIS Simple Application",
    "version": "1.0.0",
    "session_id": "20250922_165127",
    "requirements": "basic application for testing",
    "debug_mode": True,
    "output_format": "json"
}

def get_config():
    """Get application configuration"""
    return CONFIG

def save_config(config_data):
    """Save configuration to file"""
    import json
    config_file = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)
    print(f"[ASIS] Configuration saved: {config_file}")

if __name__ == "__main__":
    print("[ASIS] Configuration module loaded")
    print(f"[ASIS] App: {CONFIG['app_name']}")
    print(f"[ASIS] Version: {CONFIG['version']}")
