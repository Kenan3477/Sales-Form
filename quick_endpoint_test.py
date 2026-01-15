import requests

def quick_test():
    base = "https://asis-production.up.railway.app"
    
    endpoints = ["/", "/api/status", "/verification", "/version"]
    
    for endpoint in endpoints:
        try:
            r = requests.get(f"{base}{endpoint}", timeout=5)
            print(f"{endpoint}: {r.status_code}")
            if r.status_code == 200 and endpoint in ["/verification", "/version"]:
                data = r.json()
                if endpoint == "/verification":
                    print(f"  Score: {data.get('overall_score', 'N/A')}")
                elif endpoint == "/version":
                    print(f"  Version: {data.get('version', 'N/A')}")
        except Exception as e:
            print(f"{endpoint}: ERROR - {e}")

if __name__ == "__main__":
    quick_test()
