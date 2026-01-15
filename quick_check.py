#!/usr/bin/env python3
"""
Quick Check - After Forced Docker Rebuild
=========================================
Simple test to see if the endpoints finally work
"""

import requests
import time

def quick_check():
    print("🔧 QUICK CHECK AFTER FORCED DOCKER REBUILD")
    print("="*50)
    print("✅ Configuration Fixed:")
    print("   - railway.json: DOCKERFILE builder")  
    print("   - Dockerfile: CMD python asis_100_percent_production.py")
    print("   - File has /verification and /version endpoints")
    print()
    
    base = "https://asis-production.up.railway.app"
    
    # Give Railway time to rebuild
    print("⏱️  Waiting for Railway to complete rebuild...")
    time.sleep(15)
    
    print("\n🔍 Testing critical endpoints:")
    
    for endpoint in ["/verification", "/version"]:
        url = f"{base}{endpoint}"
        print(f"\n📡 {endpoint}")
        
        try:
            r = requests.get(url, timeout=10)
            print(f"   Status: {r.status_code}")
            
            if r.status_code == 200:
                print("   ✅ SUCCESS! Endpoint now works!")
                try:
                    data = r.json()
                    if endpoint == "/verification":
                        print(f"   📊 Score: {data.get('overall_score', 'N/A')}")
                    elif endpoint == "/version":
                        print(f"   🔢 Version: {data.get('version', 'N/A')}")
                except:
                    print("   📄 Got response (may be HTML)")
            elif r.status_code == 404:
                print("   ❌ Still 404 - rebuild may need more time")
            else:
                print(f"   ⚠️  Status: {r.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n🔗 Manual test: {base}/verification")
    print(f"🔗 Manual test: {base}/version")

if __name__ == "__main__":
    quick_check()
