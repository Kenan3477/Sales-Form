#!/usr/bin/env python3
"""
Minimal Flask test to isolate the crash issue
"""

from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return {"status": "Flask server running", "timestamp": datetime.now().isoformat()}

@app.route('/health')
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.route('/api/minimal-chat', methods=['POST'])
def minimal_chat():
    try:
        print("📨 Minimal chat endpoint called")
        data = request.json
        user_input = data.get('message', 'No message')
        
        response = f"Hello! I received your message: '{user_input}'. I'm a minimal ASIS test without consciousness integration."
        
        return jsonify({
            "response": response,
            "status": "SUCCESS",
            "consciousness_active": False,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Minimal chat error: {e}")
        return jsonify({
            "response": "Error in minimal chat",
            "status": "ERROR",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting minimal Flask test server...")
    app.run(host='0.0.0.0', port=5002, debug=False)