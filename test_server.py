#!/usr/bin/env python3
"""
Simple test server to verify functionality
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>ASIS Test</title>
    <style>
        body { font-family: Arial; background: #1a1a1a; color: white; padding: 20px; }
        .chat-container { max-width: 600px; margin: 0 auto; }
        .chat-input { width: 100%; padding: 10px; margin: 10px 0; }
        .chat-messages { height: 300px; border: 1px solid #333; padding: 10px; overflow-y: auto; }
        .message { margin: 10px 0; padding: 10px; background: #333; border-radius: 5px; }
        .test-btn { padding: 10px 20px; background: #0066cc; color: white; border: none; margin: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>ASIS Chat Test</h1>
    <div class="chat-container">
        <div id="messages" class="chat-messages"></div>
        <input type="text" id="chatInput" class="chat-input" placeholder="Type your message...">
        <button onclick="sendMessage()" class="test-btn">Send Message</button>
        <button onclick="testAnalytics()" class="test-btn">Test Analytics</button>
        <button onclick="testAgents()" class="test-btn">Test Agents</button>
    </div>

    <script>
        function addMessage(text) {
            const messages = document.getElementById('messages');
            const msg = document.createElement('div');
            msg.className = 'message';
            msg.textContent = text;
            messages.appendChild(msg);
            messages.scrollTop = messages.scrollHeight;
        }

        function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            if (!message) return;
            
            addMessage('You: ' + message);
            input.value = '';
            
            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                addMessage('ASIS: ' + data.response);
            })
            .catch(error => {
                addMessage('Error: ' + error.message);
            });
        }

        function testAnalytics() {
            fetch('/api/analytics')
            .then(response => response.json())
            .then(data => {
                addMessage('Analytics: ' + JSON.stringify(data));
            })
            .catch(error => {
                addMessage('Analytics Error: ' + error.message);
            });
        }

        function testAgents() {
            fetch('/api/agents', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ type: 'test' })
            })
            .then(response => response.json())
            .then(data => {
                addMessage('Agent Spawn: ' + JSON.stringify(data));
            })
            .catch(error => {
                addMessage('Agent Error: ' + error.message);
            });
        }

        // Enter key support
        document.getElementById('chatInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Initial message
        window.onload = function() {
            addMessage('ASIS Test Server Ready - Try typing a message!');
        };
    </script>
</body>
</html>'''

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get('message', '')
    
    # Simple AI response
    if 'hello' in message.lower():
        response = "Hello! I'm ASIS. How can I help you today?"
    elif 'test' in message.lower():
        response = "Test successful! All systems are working properly."
    elif 'help' in message.lower():
        response = "I can help you with coding, analysis, and development tasks. What do you need?"
    else:
        response = f"I received your message: '{message}'. I'm ASIS, your AI assistant. How can I help?"
    
    return {"response": response}

@app.get("/api/analytics")
async def analytics():
    return {
        "code_quality": 92,
        "active_agents": 3,
        "efficiency": 96,
        "status": "All systems operational"
    }

@app.post("/api/agents")
async def spawn_agent(request: Request):
    data = await request.json()
    agent_type = data.get('type', 'general')
    
    return {
        "success": True,
        "agent_id": f"agent_{agent_type}_123",
        "type": agent_type,
        "status": "spawned and active"
    }

if __name__ == "__main__":
    print("🚀 Starting ASIS Test Server on http://localhost:8001")
    uvicorn.run(app, host="localhost", port=8001)