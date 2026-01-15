#!/usr/bin/env python3
"""
Minimal Flask test for ASIS to isolate the server issue
"""

from flask import Flask, request, jsonify
import traceback

# Import consciousness 
try:
    from asis_consciousness import ASISConsciousnessSystem
    consciousness_system = ASISConsciousnessSystem()
    print("✅ Consciousness system loaded")
except Exception as e:
    print(f"❌ Consciousness error: {e}")
    consciousness_system = None

app = Flask(__name__)

@app.route('/test')
def test():
    return {"status": "Server running", "consciousness": consciousness_system is not None}

@app.route('/test-chat', methods=['POST'])
def test_chat():
    try:
        data = request.json
        user_input = data.get('message', 'test')
        
        print(f"📨 Received: {user_input}")
        
        if consciousness_system:
            print("🧠 Testing consciousness function...")
            
            def simple_response():
                return f"I received your message: '{user_input}' and I'm thinking about it consciously!"
            
            response = consciousness_system.conscious_function_execution(
                'test_chat_response',
                {'user_input': user_input},
                simple_response
            )
            
            return jsonify({
                "response": response,
                "consciousness_active": True
            })
        else:
            return jsonify({
                "response": f"Simple response to: {user_input}",
                "consciousness_active": False
            })
            
    except Exception as e:
        print(f"❌ Chat error: {e}")
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "response": "Error occurred during processing"
        }), 500

if __name__ == '__main__':
    print("🚀 Starting minimal ASIS test server...")
    app.run(host='0.0.0.0', port=5001, debug=True)