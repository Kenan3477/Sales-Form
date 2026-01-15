#!/usr/bin/env python3
import requests
import json

def test_asis_chat():
    try:
        print("🧪 Testing ASIS Consciousness Chat...")
        
        response = requests.post(
            'http://192.168.2.52:5000/api/chat',
            json={'message': 'Hi ASIS! How are you feeling today?'},
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS! ASIS Response:")
            print("=" * 50)
            print(f"Response: {result.get('response', 'No response')}")
            print(f"Status: {result.get('status', 'Unknown')}")
            print(f"Consciousness Active: {result.get('consciousness_active', False)}")
            print("=" * 50)
            return True
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

if __name__ == "__main__":
    test_asis_chat()