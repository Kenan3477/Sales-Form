#!/usr/bin/env python3
"""
ASIS Dashboard Enhancement Remote Deployment
==========================================
Deploy dashboard enhancements to remote ASIS server

Author: ASIS Development Team
Version: 1.0
"""

import os
import sys
import json
import shutil
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path
import paramiko
from scp import SCPClient
import time

class ASISServerDeployment:
    """Remote deployment manager for ASIS dashboard enhancements"""
    
    def __init__(self, config_file="deployment_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.deployment_files = []
        self.backup_created = False
        
        print("🚀 ASIS Dashboard Enhancement Deployment")
        print("=" * 50)
    
    def load_config(self):
        """Load deployment configuration"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                print(f"✅ Loaded configuration from {self.config_file}")
                return config
            else:
                # Create default config
                default_config = {
                    "server": {
                        "host": "YOUR_SERVER_IP",
                        "port": 22,
                        "username": "YOUR_USERNAME",
                        "password": "YOUR_PASSWORD",
                        "key_file": None,
                        "asis_path": "/path/to/asis"
                    },
                    "deployment": {
                        "backup_before_deploy": True,
                        "restart_asis_after_deploy": True,
                        "validate_deployment": True,
                        "deployment_method": "ssh"  # ssh, ftp, or manual
                    },
                    "files": {
                        "enhancement_files": [
                            "asis_dashboard_enhancer.py",
                            "dashboard_control.py",
                            "templates/dashboard_control.html",
                            "test_dashboard_integration.py"
                        ],
                        "backup_files": [
                            "app.py",
                            "templates/dashboard.html"
                        ]
                    }
                }
                
                with open(self.config_file, 'w') as f:
                    json.dump(default_config, f, indent=2)
                
                print(f"📝 Created default configuration: {self.config_file}")
                print("⚠️  Please edit the configuration file with your server details!")
                return default_config
                
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            sys.exit(1)
    
    def validate_config(self):
        """Validate deployment configuration"""
        print("🔍 Validating configuration...")
        
        required_fields = [
            "server.host",
            "server.username", 
            "server.asis_path"
        ]
        
        missing_fields = []
        for field in required_fields:
            keys = field.split('.')
            value = self.config
            try:
                for key in keys:
                    value = value[key]
                if not value or value == f"YOUR_{key.upper()}":
                    missing_fields.append(field)
            except KeyError:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ Missing required configuration fields: {missing_fields}")
            print("📝 Please edit deployment_config.json with your server details")
            return False
        
        print("✅ Configuration validated")
        return True
    
    def create_deployment_package(self):
        """Create deployment package with all enhancement files"""
        print("📦 Creating deployment package...")
        
        package_dir = "asis_dashboard_enhancement_package"
        if os.path.exists(package_dir):
            shutil.rmtree(package_dir)
        os.makedirs(package_dir)
        
        # Create subdirectories
        os.makedirs(f"{package_dir}/templates", exist_ok=True)
        os.makedirs(f"{package_dir}/backup", exist_ok=True)
        
        deployment_files = []
        
        # Copy enhancement files
        for file_path in self.config["files"]["enhancement_files"]:
            if os.path.exists(file_path):
                dest_path = f"{package_dir}/{file_path}"
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(file_path, dest_path)
                deployment_files.append(file_path)
                print(f"  ✅ Added: {file_path}")
            else:
                print(f"  ⚠️  File not found: {file_path}")
        
        # Create deployment manifest
        manifest = {
            "deployment_info": {
                "created_at": datetime.now().isoformat(),
                "version": "1.0",
                "description": "ASIS Dashboard Enhancement Package"
            },
            "files": deployment_files,
            "installation_steps": [
                "1. Backup existing ASIS files",
                "2. Stop ASIS service (if running)",
                "3. Copy enhancement files to ASIS directory",
                "4. Install required Python packages",
                "5. Restart ASIS service",
                "6. Validate deployment"
            ]
        }
        
        with open(f"{package_dir}/deployment_manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)
        
        # Create deployment archive
        archive_name = f"asis_enhancement_deployment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(package_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, package_dir)
                    zipf.write(file_path, arcname)
        
        print(f"📦 Created deployment package: {archive_name}")
        self.deployment_package = archive_name
        self.deployment_files = deployment_files
        
        return archive_name
    
    def create_server_installation_script(self):
        """Create server-side installation script"""
        print("📜 Creating server installation script...")
        
        script_content = f'''#!/bin/bash
# ASIS Dashboard Enhancement Installation Script
# Generated: {datetime.now().isoformat()}

set -e

ASIS_PATH="{self.config["server"]["asis_path"]}"
BACKUP_DIR="$ASIS_PATH/backup_$(date +%Y%m%d_%H%M%S)"
DEPLOYMENT_DIR="$(pwd)"

echo "🚀 ASIS Dashboard Enhancement Installation"
echo "============================================"

# Function to print status
print_status() {{
    echo "📍 $1"
}}

# Function to handle errors
handle_error() {{
    echo "❌ Error: $1"
    echo "🔄 Rolling back changes..."
    if [ -d "$BACKUP_DIR" ]; then
        cp -r "$BACKUP_DIR"/* "$ASIS_PATH/"
        echo "✅ Rollback completed"
    fi
    exit 1
}}

# Check if ASIS directory exists
if [ ! -d "$ASIS_PATH" ]; then
    echo "❌ ASIS directory not found: $ASIS_PATH"
    exit 1
fi

print_status "Creating backup directory: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

# Backup existing files
print_status "Backing up existing ASIS files..."
if [ -f "$ASIS_PATH/app.py" ]; then
    cp "$ASIS_PATH/app.py" "$BACKUP_DIR/"
fi
if [ -f "$ASIS_PATH/templates/dashboard.html" ]; then
    cp "$ASIS_PATH/templates/dashboard.html" "$BACKUP_DIR/"
fi

# Stop ASIS if running
print_status "Checking for running ASIS processes..."
ASIS_PID=$(pgrep -f "python.*app.py" || true)
if [ ! -z "$ASIS_PID" ]; then
    print_status "Stopping ASIS service (PID: $ASIS_PID)..."
    kill $ASIS_PID || true
    sleep 3
fi

# Install Python requirements
print_status "Installing Python requirements..."
if [ -f "$DEPLOYMENT_DIR/requirements.txt" ]; then
    pip install -r "$DEPLOYMENT_DIR/requirements.txt" || handle_error "Failed to install requirements"
else
    # Install essential packages
    pip install psutil flask-socketio paramiko scp || handle_error "Failed to install essential packages"
fi

# Copy enhancement files
print_status "Installing dashboard enhancement files..."
cp "$DEPLOYMENT_DIR/asis_dashboard_enhancer.py" "$ASIS_PATH/" || handle_error "Failed to copy dashboard enhancer"
cp "$DEPLOYMENT_DIR/dashboard_control.py" "$ASIS_PATH/" || handle_error "Failed to copy dashboard control"

# Create templates directory if it doesn't exist
mkdir -p "$ASIS_PATH/templates"
if [ -f "$DEPLOYMENT_DIR/templates/dashboard_control.html" ]; then
    cp "$DEPLOYMENT_DIR/templates/dashboard_control.html" "$ASIS_PATH/templates/" || handle_error "Failed to copy dashboard control template"
fi

# Copy test file
if [ -f "$DEPLOYMENT_DIR/test_dashboard_integration.py" ]; then
    cp "$DEPLOYMENT_DIR/test_dashboard_integration.py" "$ASIS_PATH/"
fi

# Set permissions
print_status "Setting file permissions..."
chmod +x "$ASIS_PATH/asis_dashboard_enhancer.py"
chmod +x "$ASIS_PATH/dashboard_control.py"

# Update app.py with dashboard integration (if not already integrated)
print_status "Checking app.py integration..."
if ! grep -q "dashboard_control" "$ASIS_PATH/app.py"; then
    print_status "Adding dashboard integration to app.py..."
    # This would need the actual integration code
    echo "⚠️  Manual integration required for app.py"
fi

# Restart ASIS
if [ "{self.config["deployment"]["restart_asis_after_deploy"]}" = "True" ]; then
    print_status "Starting ASIS service..."
    cd "$ASIS_PATH"
    nohup python app.py > asis.log 2>&1 &
    sleep 5
    
    # Check if ASIS started successfully
    if pgrep -f "python.*app.py" > /dev/null; then
        print_status "✅ ASIS service started successfully"
    else
        handle_error "Failed to start ASIS service"
    fi
fi

# Validate deployment
if [ "{self.config["deployment"]["validate_deployment"]}" = "True" ]; then
    print_status "Validating deployment..."
    cd "$ASIS_PATH"
    if python -c "import asis_dashboard_enhancer; print('Dashboard enhancer imported successfully')"; then
        print_status "✅ Dashboard enhancer validation passed"
    else
        handle_error "Dashboard enhancer validation failed"
    fi
fi

print_status "🎉 Dashboard enhancement deployment completed successfully!"
print_status "📊 Access enhanced dashboard at: http://your-server:5000/dashboard/control"
print_status "📋 Backup created at: $BACKUP_DIR"

echo ""
echo "🚀 Next Steps:"
echo "1. Test the enhanced dashboard interface"
echo "2. Activate dashboard enhancement via control panel"
echo "3. Monitor system health and performance"
echo "4. Review logs for any issues"
'''
        
        script_path = "install_dashboard_enhancement.sh"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make script executable
        os.chmod(script_path, 0o755)
        
        print(f"📜 Created installation script: {script_path}")
        return script_path
    
    def deploy_via_ssh(self):
        """Deploy to server via SSH/SCP"""
        print("🌐 Deploying via SSH...")
        
        try:
            # Create SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Connect to server
            print(f"🔗 Connecting to {self.config['server']['host']}...")
            
            if self.config['server'].get('key_file'):
                ssh.connect(
                    hostname=self.config['server']['host'],
                    port=self.config['server']['port'],
                    username=self.config['server']['username'],
                    key_filename=self.config['server']['key_file']
                )
            else:
                ssh.connect(
                    hostname=self.config['server']['host'],
                    port=self.config['server']['port'],
                    username=self.config['server']['username'],
                    password=self.config['server']['password']
                )
            
            print("✅ SSH connection established")
            
            # Create deployment directory on server
            deployment_dir = f"/tmp/asis_deployment_{int(time.time())}"
            ssh.exec_command(f"mkdir -p {deployment_dir}")
            
            # Upload deployment package
            with SCPClient(ssh.get_transport()) as scp:
                print(f"📤 Uploading deployment package...")
                scp.put(self.deployment_package, f"{deployment_dir}/")
                
                # Upload installation script
                scp.put("install_dashboard_enhancement.sh", f"{deployment_dir}/")
            
            print("✅ Files uploaded successfully")
            
            # Extract and install on server
            commands = [
                f"cd {deployment_dir}",
                f"unzip -q {os.path.basename(self.deployment_package)}",
                f"chmod +x install_dashboard_enhancement.sh",
                f"./install_dashboard_enhancement.sh"
            ]
            
            for cmd in commands:
                print(f"🔧 Executing: {cmd}")
                stdin, stdout, stderr = ssh.exec_command(cmd)
                
                # Print output in real-time
                for line in stdout:
                    print(f"  📤 {line.strip()}")
                
                # Check for errors
                error_output = stderr.read().decode()
                if error_output:
                    print(f"  ⚠️  {error_output.strip()}")
            
            # Cleanup deployment directory
            ssh.exec_command(f"rm -rf {deployment_dir}")
            
            ssh.close()
            print("🎉 Remote deployment completed successfully!")
            
        except Exception as e:
            print(f"❌ SSH deployment failed: {e}")
            return False
        
        return True
    
    def deploy_manual(self):
        """Generate manual deployment instructions"""
        print("📋 Generating manual deployment instructions...")
        
        instructions = f"""
# ASIS Dashboard Enhancement Manual Deployment
Generated: {datetime.now().isoformat()}

## Files to Upload to Server:
{chr(10).join(f"  • {file}" for file in self.deployment_files)}
  • install_dashboard_enhancement.sh
  • {self.deployment_package}

## Server Information:
  • Host: {self.config['server']['host']}
  • ASIS Path: {self.config['server']['asis_path']}

## Manual Deployment Steps:

1. **Upload Files to Server:**
   scp {self.deployment_package} {self.config['server']['username']}@{self.config['server']['host']}:/tmp/
   scp install_dashboard_enhancement.sh {self.config['server']['username']}@{self.config['server']['host']}:/tmp/

2. **Connect to Server:**
   ssh {self.config['server']['username']}@{self.config['server']['host']}

3. **Extract and Install:**
   cd /tmp
   unzip {self.deployment_package}
   chmod +x install_dashboard_enhancement.sh
   ./install_dashboard_enhancement.sh

4. **Verify Deployment:**
   cd {self.config['server']['asis_path']}
   python test_dashboard_integration.py

5. **Access Enhanced Dashboard:**
   http://{self.config['server']['host']}:5000/dashboard/control

## Rollback Instructions (if needed):
   cd {self.config['server']['asis_path']}
   cp backup_*/app.py ./
   cp backup_*/dashboard.html templates/
   python app.py

## Support:
   • Review deployment logs for any issues
   • Check ASIS logs: tail -f {self.config['server']['asis_path']}/asis.log
   • Test integration: python test_dashboard_integration.py
"""
        
        with open("MANUAL_DEPLOYMENT_INSTRUCTIONS.md", 'w') as f:
            f.write(instructions)
        
        print("📋 Manual deployment instructions created: MANUAL_DEPLOYMENT_INSTRUCTIONS.md")
        return True
    
    def deploy(self):
        """Main deployment function"""
        if not self.validate_config():
            return False
        
        # Create deployment package
        self.create_deployment_package()
        
        # Create installation script
        self.create_server_installation_script()
        
        # Deploy based on method
        deployment_method = self.config["deployment"]["deployment_method"]
        
        if deployment_method == "ssh":
            success = self.deploy_via_ssh()
        elif deployment_method == "manual":
            success = self.deploy_manual()
        else:
            print(f"❌ Unknown deployment method: {deployment_method}")
            success = False
        
        if success:
            print("\n🎉 Deployment Summary:")
            print("=" * 30)
            print(f"✅ Files deployed: {len(self.deployment_files)}")
            print(f"📦 Package created: {self.deployment_package}")
            print(f"🌐 Server: {self.config['server']['host']}")
            print(f"📍 ASIS Path: {self.config['server']['asis_path']}")
            print(f"🎯 Enhanced Dashboard: http://{self.config['server']['host']}:5000/dashboard/control")
            
            print("\n🚀 Next Steps:")
            print("1. Access the enhanced dashboard control interface")
            print("2. Activate dashboard enhancement")
            print("3. Monitor real-time system metrics")
            print("4. Enjoy the enhanced ASIS experience!")
        
        return success

def main():
    """Main deployment entry point"""
    deployment = ASISServerDeployment()
    
    print("Dashboard Enhancement Deployment Options:")
    print("1. Full automated deployment (SSH)")
    print("2. Generate manual deployment package")
    print("3. Configure deployment settings")
    
    try:
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            deployment.config["deployment"]["deployment_method"] = "ssh"
            success = deployment.deploy()
        elif choice == "2":
            deployment.config["deployment"]["deployment_method"] = "manual"
            success = deployment.deploy()
        elif choice == "3":
            print(f"📝 Edit configuration file: {deployment.config_file}")
            success = True
        else:
            print("❌ Invalid option")
            success = False
            
    except KeyboardInterrupt:
        print("\n👋 Deployment cancelled")
        success = False
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        success = False
    
    if success:
        print("\n🎉 Deployment process completed successfully!")
    else:
        print("\n❌ Deployment process failed")
    
    return success

if __name__ == "__main__":
    main()