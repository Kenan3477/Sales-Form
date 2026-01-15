#!/usr/bin/env python3
"""
Create Manual Deployment Package
===============================
Creates a simple deployment package for manual upload
"""

import os
import shutil
import zipfile
from datetime import datetime

def create_manual_package():
    print("📦 Creating Manual Deployment Package...")
    
    package_name = "asis_dashboard_manual_deploy"
    
    # Create deployment directory
    if os.path.exists(package_name):
        shutil.rmtree(package_name)
    os.makedirs(package_name)
    os.makedirs(f"{package_name}/templates", exist_ok=True)
    
    # Files to include
    files_to_copy = [
        "asis_dashboard_enhancer.py",
        "dashboard_control.py", 
        "test_dashboard_integration.py",
        "deployment_requirements.txt"
    ]
    
    # Copy files
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, f"{package_name}/{file}")
            print(f"  ✅ Added: {file}")
    
    # Copy template
    if os.path.exists("templates/dashboard_control.html"):
        shutil.copy2("templates/dashboard_control.html", f"{package_name}/templates/")
        print(f"  ✅ Added: templates/dashboard_control.html")
    
    # Create installation script
    install_script = f'''#!/bin/bash
# ASIS Dashboard Enhancement Manual Installation
echo "🚀 Installing ASIS Dashboard Enhancements..."

# Install requirements
pip install -r deployment_requirements.txt

# Copy files (assuming you're in the ASIS directory)
cp asis_dashboard_enhancer.py ./
cp dashboard_control.py ./
mkdir -p templates
cp templates/dashboard_control.html templates/
cp test_dashboard_integration.py ./

# Test installation
python test_dashboard_integration.py

# Restart ASIS
pkill -f "python.*app.py" || true
nohup python app.py > asis.log 2>&1 &

echo "✅ Installation complete!"
echo "🌐 Access: http://81.134.136.242:5000/dashboard/control"
'''
    
    with open(f"{package_name}/install.sh", 'w', encoding='utf-8') as f:
        f.write(install_script)
    
    # Make install script executable
    os.chmod(f"{package_name}/install.sh", 0o755)
    print(f"  ✅ Added: install.sh")
    
    # Create instructions
    instructions = f'''# ASIS Dashboard Enhancement Manual Deployment
Created: {datetime.now().isoformat()}

## Files Included:
- asis_dashboard_enhancer.py
- dashboard_control.py
- templates/dashboard_control.html
- test_dashboard_integration.py
- deployment_requirements.txt
- install.sh

## Installation Steps:

1. Upload this entire folder to your ASIS server
2. On your server, navigate to your ASIS directory:
   cd /home/creator_kenandavies/ASIS

3. Copy the deployment files:
   cp /path/to/upload/asis_dashboard_manual_deploy/* ./
   cp /path/to/upload/asis_dashboard_manual_deploy/templates/* templates/

4. Run the installation:
   chmod +x install.sh
   ./install.sh

5. Access enhanced dashboard:
   http://81.134.136.242:5000/dashboard/control

## Manual Commands (if install.sh doesn't work):

pip install -r deployment_requirements.txt
python test_dashboard_integration.py
pkill -f "python.*app.py" || true
nohup python app.py > asis.log 2>&1 &
'''
    
    with open(f"{package_name}/INSTALL_INSTRUCTIONS.txt", 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"  ✅ Added: INSTALL_INSTRUCTIONS.txt")
    
    # Create zip file
    zip_name = f"{package_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_name):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_name)
                zipf.write(file_path, arcname)
    
    print(f"\n🎉 Manual deployment package created: {zip_name}")
    print(f"📁 Extract and follow INSTALL_INSTRUCTIONS.txt on your server")
    
    return zip_name

if __name__ == "__main__":
    create_manual_package()