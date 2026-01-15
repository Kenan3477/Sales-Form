#!/bin/bash
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
