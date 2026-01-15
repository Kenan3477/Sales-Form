#!/usr/bin/env python3
"""
Test Railway Endpoints - Verify the /verification endpoint works
"""

import requests
import json

def test_railway_endpoints():
    """Test Railway app endpoints"""
    
    base_url = "https://asis-production.up.railway.app"
    
    print("🔍 TESTING RAILWAY ENDPOINTS")
    print("=" * 50)
    
    endpoints = [
        "/",
        "/api/status", 
        "/verification",
        "/version"
    ]
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        print(f"\n📡 Testing: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ SUCCESS")
                if endpoint == "/verification":
                    data = response.json()
                    print(f"   🎯 Authenticity: {data.get('overall_score', 'Unknown')}")
                    print(f"   📊 Status: {data.get('status', 'Unknown')}")
                elif endpoint == "/version":
                    data = response.json()
                    print(f"   🔢 Version: {data.get('version', 'Unknown')}")
                    print(f"   📝 Description: {data.get('description', 'Unknown')}")
            else:
                print(f"   ❌ FAILED - {response.status_code}")
                if response.text:
                    print(f"   Error: {response.text[:100]}...")
                    
        except requests.exceptions.RequestException as e:
            print(f"   ❌ CONNECTION ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("🚀 If /verification shows 404, Railway is still deploying")
    print("🔄 Wait 2-3 minutes and try again")
    print("✅ When ready, /verification will show 90%+ authenticity")

if __name__ == "__main__":
    test_railway_endpoints()
