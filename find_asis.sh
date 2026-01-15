#!/bin/bash
# ASIS Directory Finder Script
# Run this on your server to locate ASIS installation

echo "🔍 ASIS Directory Finder"
echo "======================="

echo ""
echo "📍 Checking for running ASIS processes..."
ASIS_PROC=$(ps aux | grep -E "(app_enhanced|asis)" | grep -v grep)
if [ ! -z "$ASIS_PROC" ]; then
    echo "✅ Found running ASIS process:"
    echo "$ASIS_PROC"
else
    echo "❌ No ASIS processes currently running"
fi

echo ""
echo "🔍 Searching for ASIS files..."

# Find app_enhanced.py
APP_ENHANCED=$(find / -name "app_enhanced.py" 2>/dev/null | head -1)
if [ ! -z "$APP_ENHANCED" ]; then
    ASIS_DIR=$(dirname "$APP_ENHANCED")
    echo "✅ Found ASIS directory: $ASIS_DIR"
    echo "📁 Contents:"
    ls -la "$ASIS_DIR" | head -10
    
    echo ""
    echo "🔧 Setting up git repository..."
    cd "$ASIS_DIR"
    
    if [ -d ".git" ]; then
        echo "✅ Git repository already exists"
        git status
    else
        echo "⚠️ No git repository found - setting up..."
        git init
        git remote add origin https://github.com/Kenan3477/ASIS.git
        git fetch origin
        git checkout main
        echo "✅ Git repository set up successfully"
    fi
    
    echo ""
    echo "🎯 ASIS Directory: $ASIS_DIR"
    echo "🚀 To deploy meta-learning system:"
    echo "   cd $ASIS_DIR"
    echo "   git pull origin main"
    echo "   pkill -f 'python3 app_enhanced.py'"
    echo "   pip3 install --upgrade numpy scikit-learn matplotlib seaborn"
    echo "   nohup python3 app_enhanced.py &"
    
else
    echo "❌ app_enhanced.py not found"
    echo ""
    echo "🔍 Checking common directories..."
    
    for dir in "/root" "/home" "/opt" "/var/www"; do
        if [ -d "$dir" ]; then
            echo "📁 Checking $dir..."
            find "$dir" -name "*.py" -path "*asis*" 2>/dev/null | head -5
        fi
    done
    
    echo ""
    echo "💡 ASIS installation not found. To set up fresh:"
    echo "   cd /root"
    echo "   git clone https://github.com/Kenan3477/ASIS.git"
    echo "   cd ASIS"
    echo "   pip3 install flask flask-socketio requests beautifulsoup4"
    echo "   pip3 install numpy scikit-learn matplotlib seaborn"
    echo "   nohup python3 app_enhanced.py &"
fi

echo ""
echo "🏁 Directory finder complete!"