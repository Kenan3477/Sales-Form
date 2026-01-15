#!/usr/bin/env python3
"""
Quick Server Deployment Script
=============================
Simplified deployment script for ASIS dashboard enhancements
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def main():
    print("🚀 ASIS Dashboard Enhancement Quick Deploy")
    print("=" * 50)
    
    # Check if config exists
    if not os.path.exists("deployment_config.json"):
        print("❌ deployment_config.json not found!")
        print("📝 Please run deploy_to_server.py first to create configuration")
        return False
    
    # Load config
    with open("deployment_config.json", 'r') as f:
        config = json.load(f)
    
    server_host = config["server"]["host"]
    server_user = config["server"]["username"]
    asis_path = config["server"]["asis_path"]
    
    if server_host == "YOUR_SERVER_IP":
        print("❌ Please configure your server details in deployment_config.json")
        return False
    
    print(f"🎯 Target Server: {server_user}@{server_host}")
    print(f"📍 ASIS Path: {asis_path}")
    
    # Check required files exist
    required_files = config["files"]["enhancement_files"]
    missing_files = []
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files found")
    
    # Create deployment commands
    deployment_commands = []
    
    # Upload files
    for file_path in required_files:
        remote_path = f"{asis_path}/{file_path}"
        remote_dir = os.path.dirname(remote_path)
        
        # Create directory on server if needed
        deployment_commands.append(f'ssh {server_user}@{server_host} "mkdir -p {remote_dir}"')
        
        # Upload file
        deployment_commands.append(f'scp {file_path} {server_user}@{server_host}:{remote_path}')
    
    # Install requirements
    deployment_commands.append(f'ssh {server_user}@{server_host} "cd {asis_path} && pip install -r deployment_requirements.txt"')
    
    # Test integration
    deployment_commands.append(f'ssh {server_user}@{server_host} "cd {asis_path} && python test_dashboard_integration.py"')
    
    # Restart ASIS (optional)
    if config["deployment"]["restart_asis_after_deploy"]:
        deployment_commands.extend([
            f'ssh {server_user}@{server_host} "pkill -f \'python.*app.py\' || true"',
            f'ssh {server_user}@{server_host} "cd {asis_path} && nohup python app.py > asis.log 2>&1 &"'
        ])
    
    print("\n🔧 Deployment Commands:")
    print("-" * 30)
    for i, cmd in enumerate(deployment_commands, 1):
        print(f"{i}. {cmd}")
    
    print(f"\n📋 Total commands: {len(deployment_commands)}")
    
    proceed = input("\n🚀 Execute deployment? (y/N): ").strip().lower()
    if proceed != 'y':
        print("❌ Deployment cancelled")
        return False
    
    # Execute deployment
    print("\n🚀 Starting deployment...")
    
    for i, cmd in enumerate(deployment_commands, 1):
        print(f"\n📤 [{i}/{len(deployment_commands)}] {cmd}")
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"  ✅ Success")
                if result.stdout.strip():
                    print(f"  📤 {result.stdout.strip()}")
            else:
                print(f"  ❌ Failed (exit code: {result.returncode})")
                if result.stderr.strip():
                    print(f"  ❌ {result.stderr.strip()}")
                
                if "test_dashboard_integration" not in cmd:  # Don't fail on test errors
                    proceed_anyway = input("  ⚠️  Continue despite error? (y/N): ").strip().lower()
                    if proceed_anyway != 'y':
                        print("❌ Deployment stopped")
                        return False
        
        except Exception as e:
            print(f"  ❌ Command failed: {e}")
            return False
    
    print("\n🎉 Deployment completed!")
    print("=" * 30)
    print(f"🌐 Enhanced Dashboard: http://{server_host}:5000/dashboard/control")
    print("🎯 Access your ASIS server and activate dashboard enhancement")
    print("📊 Enjoy real-time monitoring and enhanced features!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)