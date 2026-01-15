#!/usr/bin/env python3
"""
Quick Deployment Verification
============================
Run this to verify what version you have locally and what should be deployed
"""

import subprocess
import os
import json
from datetime import datetime

def quick_verification():
    """Quick check of deployment readiness"""
    
    print("🔍 QUICK DEPLOYMENT VERIFICATION")
    print("=" * 40)
    
    # 1. Check current commit
    try:
        result = subprocess.run(['git', 'log', '-1', '--oneline'], 
                              capture_output=True, text=True, cwd='.')
        latest_commit = result.stdout.strip()
        print(f"📝 Latest Commit: {latest_commit}")
    except:
        print("❌ Cannot check git status")
    
    # 2. Check if railway.json exists and is correct
    if os.path.exists('railway.json'):
        with open('railway.json', 'r') as f:
            config = json.load(f)
        start_command = config.get('deploy', {}).get('startCommand', '')
        print(f"🚀 Railway Start Command: {start_command}")
        
        if start_command == "python asis_100_percent_production.py":
            print("✅ Railway configured correctly")
        else:
            print("⚠️  Railway start command may be wrong")
    else:
        print("❌ railway.json not found")
    
    # 3. Check if the production file exists
    if os.path.exists('asis_100_percent_production.py'):
        print("✅ Production file exists")
    else:
        print("❌ asis_100_percent_production.py not found")
    
    # 4. Check if verification fix files exist
    verification_files = [
        'asis_final_verification_fix.py',
        'ASIS_FINAL_REAL_VERIFICATION.json'
    ]
    
    for file in verification_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
    
    print("\n🎯 TO VERIFY YOUR DEPLOYMENT:")
    print("1. Go to your Railway dashboard")
    print("2. Check if your latest commit deployed successfully")
    print("3. Visit your Railway app URL")
    print("4. Look for these indicators of the correct version:")
    print("   - Shows '100% VERIFIED AUTONOMOUS' status")
    print("   - Pattern recognition shows 83+ patterns (not 0)")
    print("   - Learning velocity shows 1000+ events (not fake data)")
    print("   - Research module shows active sessions and findings")
    
    # 5. Create a version identifier
    version_info = {
        "version": "3.0.0-REAL-DATA-FIX",
        "description": "ASIS with real database verification - no fake data",
        "timestamp": datetime.now().isoformat(),
        "key_features": [
            "Real pattern recognition from asis_patterns_fixed.db",
            "Real learning data from asis_realtime_learning.db", 
            "Real adaptation data from asis_adaptive_meta_learning.db",
            "100% authentic verification results"
        ]
    }
    
    with open('VERSION_INFO.json', 'w') as f:
        json.dump(version_info, f, indent=2)
    
    print(f"\n✅ Created VERSION_INFO.json - this identifies your version")
    
    return version_info

if __name__ == "__main__":
    quick_verification()
