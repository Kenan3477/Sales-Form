import requests
import json

def test_railway():
    print("🔍 TESTING RAILWAY VERIFICATION ENDPOINT")
    print("=" * 50)
    
    url = "https://asis-production.up.railway.app/verification"
    
    try:
        response = requests.get(url, timeout=15)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS - /verification endpoint is working!")
            print(f"Overall Score: {data.get('overall_score', 'Unknown')}")
            print(f"Status: {data.get('status', 'Unknown')}")
            print(f"Verification Type: {data.get('verification_type', 'Unknown')}")
            
            if 'systems' in data:
                print("\nSystems:")
                for system, info in data['systems'].items():
                    print(f"  {system}: {info.get('score', 'N/A')} - {info.get('evidence', 'N/A')}")
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(f"Response: {response.text[:300]}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_railway()
