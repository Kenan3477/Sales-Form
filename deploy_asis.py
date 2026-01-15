#!/usr/bin/env python3
"""
ASIS Deployment Script
======================
Automated deployment and configuration for ASIS system.
"""

import subprocess
import sys
import os
import json
from pathlib import Path

def check_python_version():
    """Check Python version compatibility"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def install_dependencies():
    """Install required Python packages"""
    requirements = [
        'flask>=2.0.0',
        'flask-socketio>=5.0.0',
        'flask-cors>=4.0.0',
        'werkzeug>=2.0.0',
        'psutil>=5.9.0'
    ]
    
    print("📦 Installing dependencies...")
    for req in requirements:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', req], 
                         check=True, capture_output=True)
            print(f"✅ {req}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {req}: {e}")
            return False
    
    return True

def setup_directories():
    """Create necessary directories"""
    directories = [
        'static/css',
        'static/js',
        'static/icons',
        'templates',
        'logs',
        'config',
        'data'
    ]
    
    print("📁 Creating directories...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ {directory}")

def create_config_file():
    """Create default configuration file"""
    config = {
        "host": "0.0.0.0",
        "port": 5000,
        "debug": False,
        "log_level": "INFO",
        "secret_key": "your-secret-key-here",
        "max_concurrent_users": 100,
        "response_timeout": 30,
        "memory_threshold_mb": 1024
    }
    
    config_path = Path('config/asis_config.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configuration created: {config_path}")

def run_system_check():
    """Run system compatibility check"""
    print("🔍 Running system check...")
    
    try:
        subprocess.run([sys.executable, 'asis_integration_system.py', '--check'], 
                      check=True, capture_output=True)
        print("✅ System check passed")
        return True
    except subprocess.CalledProcessError:
        print("❌ System check failed")
        return False

def main():
    """Main deployment function"""
    print("🚀 ASIS Deployment Script")
    print("=" * 30)
    
    if not check_python_version():
        sys.exit(1)
    
    setup_directories()
    
    if not install_dependencies():
        sys.exit(1)
    
    create_config_file()
    
    if not run_system_check():
        print("⚠️ Warning: System check failed, but continuing...")
    
    print("✅ ASIS deployment completed successfully!")
    print("📝 Next steps:")
    print("   1. Review config/asis_config.json")
    print("   2. Run: python asis_integration_system.py")
    print("   3. Open: http://localhost:5000")

if __name__ == "__main__":
    main()
