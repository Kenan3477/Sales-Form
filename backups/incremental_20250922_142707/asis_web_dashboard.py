#!/usr/bin/env python3
"""
ASIS Advanced Web Dashboard and API System
==========================================

Production-ready web interface and RESTful API for ASIS interaction,
monitoring, and control with advanced features and real-time capabilities.

Author: ASIS Development Team
Date: September 18, 2025
Version: 1.0
"""

import asyncio
import json
import time
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import threading

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class User:
    """User account management"""
    id: str
    username: str
    email: str
    password_hash: str
    role: str  # admin, user, viewer
    created_at: datetime
    last_active: datetime

@dataclass
class ChatMessage:
    """Chat message structure"""
    id: str
    user_id: str
    content: str
    response: str
    mode: str
    timestamp: datetime
    project_id: Optional[str] = None

@dataclass
class ResearchProject:
    """Research project tracking"""
    id: str
    name: str
    description: str
    status: str  # active, completed, paused
    created_by: str
    created_at: datetime
    progress: float
    findings: List[Dict[str, Any]]
    autonomous_decisions: List[Dict[str, Any]]

class ASISWebAPI:
    """Core ASIS Web API and Dashboard System"""
    
    def __init__(self):
        # Initialize Flask app
        self.app = Flask(__name__, template_folder='templates', static_folder='static')
        self.app.secret_key = 'asis_advanced_web_dashboard_2025'
        
        # Initialize extensions
        self.socketio = SocketIO(self.app, cors_allowed_origins="*", async_mode='threading')
        CORS(self.app)
        
        # Data stores (in production, use proper database)
        self.users: Dict[str, User] = {}
        self.chat_history: List[ChatMessage] = []
        self.research_projects: Dict[str, ResearchProject] = {}
        self.system_metrics: Dict[str, Any] = {}
        
        # Active connections
        self.active_connections: Dict[str, Dict[str, Any]] = {}
        
        # ASIS system integration
        self.asis_system = None
        self.system_status = {
            'status': 'initializing',
            'components': {},
            'health': 0.0,
            'autonomous_active': False
        }
        
        # Initialize routes and socket handlers
        self._setup_routes()
        self._setup_socket_handlers()
        self._create_demo_user()
        
        logger.info("🌐 ASIS Web Dashboard initialized")
    
    def _create_demo_user(self):
        """Create demo user for testing"""
        demo_user = User(
            id="demo_user_001",
            username="demo",
            email="demo@asis.ai",
            password_hash=generate_password_hash("demo123"),
            role="admin",
            created_at=datetime.now(),
            last_active=datetime.now()
        )
        self.users[demo_user.id] = demo_user
        logger.info("👤 Demo user created: demo/demo123")
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def dashboard():
            """Main dashboard page"""
            return render_template('dashboard.html')
        
        @self.app.route('/chat')
        def chat_interface():
            """Advanced chat interface"""
            return render_template('chat.html')
        
        @self.app.route('/projects')
        def project_dashboard():
            """Project management dashboard"""
            return render_template('projects.html')
        
        @self.app.route('/api/v1/status')
        def api_status():
            """System status endpoint"""
            try:
                status = {
                    'system': self.system_status,
                    'metrics': self.system_metrics,
                    'timestamp': time.time(),
                    'uptime': time.time() - getattr(self, 'start_time', time.time())
                }
                return jsonify(status)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/v1/interact', methods=['POST'])
        def api_interact():
            """Main interaction endpoint"""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({'error': 'No data provided'}), 400
                
                message = data.get('message', '')
                mode = data.get('mode', 'conversational')
                user_id = data.get('user_id', 'anonymous')
                project_id = data.get('project_id')
                
                # Process interaction with ASIS
                response = self._process_asis_interaction(message, mode, user_id, project_id)
                
                # Store in chat history
                chat_message = ChatMessage(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    content=message,
                    response=response,
                    mode=mode,
                    timestamp=datetime.now(),
                    project_id=project_id
                )
                self.chat_history.append(chat_message)
                
                return jsonify({
                    'response': response,
                    'mode': mode,
                    'message_id': chat_message.id,
                    'timestamp': chat_message.timestamp.isoformat()
                })
                
            except Exception as e:
                logger.error(f"API interaction error: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/v1/components')
        def api_components():
            """Component status and control"""
            try:
                components = {
                    'memory_network': {'status': 'active', 'health': 95, 'load': 0.3},
                    'cognitive_architecture': {'status': 'active', 'health': 98, 'load': 0.5},
                    'learning_system': {'status': 'active', 'health': 92, 'load': 0.4},
                    'reasoning_engine': {'status': 'active', 'health': 96, 'load': 0.6},
                    'research_engine': {'status': 'active', 'health': 88, 'load': 0.2},
                    'communication_system': {'status': 'active', 'health': 100, 'load': 0.1}
                }
                return jsonify(components)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/v1/research', methods=['GET', 'POST'])
        def api_research():
            """Research project management"""
            try:
                if request.method == 'POST':
                    data = request.get_json()
                    project = ResearchProject(
                        id=str(uuid.uuid4()),
                        name=data.get('name', 'Untitled Project'),
                        description=data.get('description', ''),
                        status='active',
                        created_by=data.get('user_id', 'anonymous'),
                        created_at=datetime.now(),
                        progress=0.0,
                        findings=[],
                        autonomous_decisions=[]
                    )
                    self.research_projects[project.id] = project
                    return jsonify(asdict(project), default=str)
                else:
                    projects = [asdict(p, default=str) for p in self.research_projects.values()]
                    return jsonify(projects)
                    
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/v1/learning')
        def api_learning():
            """Learning progress and adaptation"""
            try:
                learning_stats = {
                    'knowledge_base_size': 15742,
                    'learning_rate': 0.85,
                    'adaptation_score': 0.92,
                    'recent_learnings': [
                        {'topic': 'Quantum Computing Applications', 'confidence': 0.89},
                        {'topic': 'Machine Learning Ethics', 'confidence': 0.94},
                        {'topic': 'Cognitive Architecture Patterns', 'confidence': 0.87}
                    ],
                    'bias_calibration': {
                        'confirmation_bias': 0.23,
                        'availability_bias': 0.18,
                        'anchoring_bias': 0.31
                    }
                }
                return jsonify(learning_stats)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/v1/knowledge')
        def api_knowledge():
            """Knowledge base access"""
            try:
                query = request.args.get('q', '')
                knowledge_results = {
                    'query': query,
                    'results': [
                        {'id': 1, 'title': 'AI Ethics Principles', 'relevance': 0.95},
                        {'id': 2, 'title': 'Cognitive Computing Models', 'relevance': 0.88},
                        {'id': 3, 'title': 'Learning System Architecture', 'relevance': 0.76}
                    ],
                    'total_knowledge_items': 15742
                }
                return jsonify(knowledge_results)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/v1/config', methods=['GET', 'POST'])
        def api_config():
            """System configuration management"""
            try:
                if request.method == 'POST':
                    config_data = request.get_json()
                    # Update configuration (mock implementation)
                    return jsonify({'status': 'configuration updated'})
                else:
                    config = {
                        'interaction_modes': {
                            'conversational': {'enabled': True, 'weight': 1.0},
                            'research': {'enabled': True, 'weight': 1.2},
                            'creative': {'enabled': True, 'weight': 0.9},
                            'learning': {'enabled': True, 'weight': 1.1},
                            'analysis': {'enabled': True, 'weight': 1.3},
                            'monitoring': {'enabled': True, 'weight': 0.8}
                        },
                        'autonomous_cycle': {
                            'enabled': True,
                            'interval': 5.0,
                            'learning_focus': ['research', 'reasoning', 'creativity']
                        },
                        'system_limits': {
                            'max_concurrent_interactions': 10,
                            'memory_threshold': 8192,
                            'response_timeout': 30
                        }
                    }
                    return jsonify(config)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    
    def _setup_socket_handlers(self):
        """Setup WebSocket event handlers"""
        
        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection"""
            client_id = request.sid
            user_agent = request.headers.get('User-Agent', 'Unknown')
            
            self.active_connections[client_id] = {
                'connected_at': time.time(),
                'user_agent': user_agent,
                'room': None
            }
            
            emit('connection_established', {
                'client_id': client_id,
                'server_time': time.time(),
                'system_status': self.system_status
            })
            
            logger.info(f"🔌 Client connected: {client_id}")
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection"""
            client_id = request.sid
            if client_id in self.active_connections:
                del self.active_connections[client_id]
            logger.info(f"🔌 Client disconnected: {client_id}")
        
        @self.socketio.on('join_room')
        def handle_join_room(data):
            """Handle room joining for real-time updates"""
            room = data.get('room', 'general')
            join_room(room)
            self.active_connections[request.sid]['room'] = room
            emit('room_joined', {'room': room})
        
        @self.socketio.on('chat_message')
        def handle_chat_message(data):
            """Handle real-time chat messages"""
            try:
                message = data.get('message', '')
                mode = data.get('mode', 'conversational')
                user_id = data.get('user_id', 'anonymous')
                
                # Process with ASIS
                response = self._process_asis_interaction(message, mode, user_id)
                
                # Emit response
                emit('chat_response', {
                    'message': message,
                    'response': response,
                    'mode': mode,
                    'timestamp': time.time()
                })
                
            except Exception as e:
                emit('error', {'message': str(e)})
        
        @self.socketio.on('request_system_update')
        def handle_system_update_request():
            """Handle request for system status update"""
            emit('system_update', self.get_real_time_status())
    
    def _process_asis_interaction(self, message: str, mode: str, user_id: str, project_id: str = None) -> str:
        """Process interaction with ASIS system"""
        try:
            # Mock ASIS interaction - replace with actual ASIS integration
            responses = {
                'conversational': f"I understand your message: '{message}'. How can I help you further?",
                'research': f"Initiating research on: '{message}'. I'll investigate this topic thoroughly.",
                'creative': f"Let me explore creative approaches to: '{message}'. Here are some innovative ideas...",
                'learning': f"I'm analyzing and learning from: '{message}'. This adds to my knowledge base.",
                'analysis': f"Performing detailed analysis of: '{message}'. Here's my systematic breakdown...",
                'monitoring': f"Monitoring request for: '{message}'. I'll track relevant metrics and patterns."
            }
            
            base_response = responses.get(mode, responses['conversational'])
            
            # Add mode-specific enhancements
            if mode == 'research':
                base_response += " I'm accessing my research capabilities and will provide comprehensive findings."
            elif mode == 'creative':
                base_response += " I'm engaging my creative synthesis systems for innovative solutions."
            elif mode == 'analysis':
                base_response += " Utilizing advanced reasoning engines for thorough analysis."
            
            return base_response
            
        except Exception as e:
            logger.error(f"ASIS interaction error: {e}")
            return "I apologize, but I'm experiencing a temporary processing issue. Please try again."
    
    def get_real_time_status(self) -> Dict[str, Any]:
        """Get current system status for real-time updates"""
        return {
            'system_status': self.system_status,
            'active_connections': len(self.active_connections),
            'recent_interactions': len(self.chat_history),
            'research_projects': len(self.research_projects),
            'timestamp': time.time()
        }
    
    def start_real_time_updates(self):
        """Start real-time status broadcasting"""
        def update_loop():
            while True:
                try:
                    status = self.get_real_time_status()
                    self.socketio.emit('system_update', status, room='general')
                    time.sleep(2)  # Update every 2 seconds
                except Exception as e:
                    logger.error(f"Real-time update error: {e}")
                    time.sleep(5)
        
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
        logger.info("📡 Real-time updates started")
    
    def run(self, host='localhost', port=5000, debug=False):
        """Run the web application"""
        self.start_time = time.time()
        self.start_real_time_updates()
        
        logger.info(f"🚀 Starting ASIS Web Dashboard on http://{host}:{port}")
        self.socketio.run(self.app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)

# HTML Templates
def create_dashboard_template():
    """Create dashboard HTML template"""
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASIS Advanced Dashboard</title>
    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; padding: 0; background: #0a0a0a; color: #e0e0e0; 
        }
        .dashboard { display: grid; grid-template-columns: 250px 1fr; height: 100vh; }
        .sidebar { background: #1a1a1a; padding: 20px; border-right: 1px solid #333; }
        .main-content { padding: 20px; overflow-y: auto; }
        .metric-card { 
            background: #1e1e1e; padding: 20px; border-radius: 8px; margin: 10px 0; 
            border-left: 4px solid #00ff88; 
        }
        .component-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .component-status { 
            background: #1e1e1e; padding: 15px; border-radius: 8px; border: 1px solid #333; 
        }
        .status-active { border-left: 4px solid #00ff88; }
        .status-warning { border-left: 4px solid #ffaa00; }
        .status-error { border-left: 4px solid #ff4444; }
        .nav-link { 
            display: block; padding: 10px; color: #ccc; text-decoration: none; 
            border-radius: 4px; margin: 5px 0; 
        }
        .nav-link:hover { background: #333; color: #fff; }
        .nav-link.active { background: #00ff88; color: #000; }
        h1, h2, h3 { color: #fff; }
        .health-bar { 
            width: 100%; height: 8px; background: #333; border-radius: 4px; overflow: hidden; 
        }
        .health-fill { height: 100%; background: linear-gradient(90deg, #ff4444, #ffaa00, #00ff88); }
        .mode-selector { display: flex; gap: 10px; margin: 20px 0; }
        .mode-btn { 
            padding: 8px 16px; background: #333; color: #fff; border: none; 
            border-radius: 4px; cursor: pointer; 
        }
        .mode-btn.active { background: #00ff88; color: #000; }
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="sidebar">
            <h2>🎯 ASIS Dashboard</h2>
            <nav>
                <a href="/" class="nav-link active">📊 Overview</a>
                <a href="/chat" class="nav-link">💬 Chat Interface</a>
                <a href="/projects" class="nav-link">📋 Projects</a>
                <a href="#" class="nav-link">⚙️ Configuration</a>
                <a href="#" class="nav-link">📈 Analytics</a>
            </nav>
            
            <div class="metric-card">
                <h3>System Status</h3>
                <div id="system-status">Initializing...</div>
                <div class="health-bar">
                    <div class="health-fill" id="health-fill" style="width: 0%"></div>
                </div>
            </div>
        </div>
        
        <div class="main-content">
            <h1>🎯 ASIS Advanced Intelligence System Dashboard</h1>
            
            <div class="mode-selector">
                <button class="mode-btn active" data-mode="monitoring">📊 Monitoring</button>
                <button class="mode-btn" data-mode="conversational">💬 Conversational</button>
                <button class="mode-btn" data-mode="research">🔬 Research</button>
                <button class="mode-btn" data-mode="creative">🎨 Creative</button>
                <button class="mode-btn" data-mode="learning">📚 Learning</button>
                <button class="mode-btn" data-mode="analysis">🔍 Analysis</button>
            </div>
            
            <div class="component-grid" id="components-grid">
                <!-- Components will be loaded dynamically -->
            </div>
            
            <div class="metric-card">
                <h3>Performance Metrics</h3>
                <canvas id="performance-chart" width="400" height="200"></canvas>
            </div>
            
            <div class="metric-card">
                <h3>Recent Activity</h3>
                <div id="activity-log">
                    <p>🔄 Autonomous cycle active</p>
                    <p>📚 Learning system processing new information</p>
                    <p>🧠 Cognitive architecture optimizing</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        const socket = io();
        let currentMode = 'monitoring';
        
        // Initialize dashboard
        socket.on('connect', function(data) {
            console.log('Connected to ASIS Dashboard');
            socket.emit('join_room', {room: 'general'});
            loadComponents();
            loadSystemStatus();
        });
        
        socket.on('system_update', function(data) {
            updateSystemStatus(data);
        });
        
        // Load components
        async function loadComponents() {
            try {
                const response = await fetch('/api/v1/components');
                const components = await response.json();
                displayComponents(components);
            } catch (error) {
                console.error('Failed to load components:', error);
            }
        }
        
        function displayComponents(components) {
            const grid = document.getElementById('components-grid');
            grid.innerHTML = '';
            
            Object.entries(components).forEach(([name, info]) => {
                const statusClass = info.health > 90 ? 'status-active' : 
                                   info.health > 70 ? 'status-warning' : 'status-error';
                
                const componentDiv = document.createElement('div');
                componentDiv.className = `component-status ${statusClass}`;
                componentDiv.innerHTML = `
                    <h4>${name.replace('_', ' ').toUpperCase()}</h4>
                    <p>Status: <span style="color: #00ff88">${info.status}</span></p>
                    <p>Health: ${info.health}%</p>
                    <p>Load: ${(info.load * 100).toFixed(1)}%</p>
                    <div class="health-bar">
                        <div class="health-fill" style="width: ${info.health}%"></div>
                    </div>
                `;
                grid.appendChild(componentDiv);
            });
        }
        
        async function loadSystemStatus() {
            try {
                const response = await fetch('/api/v1/status');
                const status = await response.json();
                updateSystemStatus(status);
            } catch (error) {
                console.error('Failed to load system status:', error);
            }
        }
        
        function updateSystemStatus(data) {
            const statusDiv = document.getElementById('system-status');
            const healthFill = document.getElementById('health-fill');
            
            if (data.system) {
                statusDiv.innerHTML = `
                    <p>Status: <span style="color: #00ff88">${data.system.status}</span></p>
                    <p>Health: ${(data.system.health * 100).toFixed(1)}%</p>
                    <p>Autonomous: ${data.system.autonomous_active ? '🔄 Active' : '⏸️ Inactive'}</p>
                `;
                healthFill.style.width = `${data.system.health * 100}%`;
            }
        }
        
        // Mode switching
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                currentMode = this.dataset.mode;
                console.log('Switched to mode:', currentMode);
            });
        });
        
        // Initialize performance chart
        const ctx = document.getElementById('performance-chart').getContext('2d');
        const performanceChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['1min', '2min', '3min', '4min', '5min'],
                datasets: [{
                    label: 'System Performance',
                    data: [85, 92, 88, 95, 91],
                    borderColor: '#00ff88',
                    backgroundColor: 'rgba(0, 255, 136, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true, max: 100 }
                },
                plugins: {
                    legend: { labels: { color: '#e0e0e0' } }
                }
            }
        });
    </script>
</body>
</html>
    '''

def create_chat_template():
    """Create chat interface HTML template"""
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASIS Advanced Chat Interface</title>
    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; padding: 0; background: #0a0a0a; color: #e0e0e0; 
            height: 100vh; display: flex; flex-direction: column;
        }
        .chat-header { 
            background: #1a1a1a; padding: 20px; border-bottom: 1px solid #333; 
            display: flex; justify-content: space-between; align-items: center;
        }
        .chat-container { 
            flex: 1; display: flex; 
        }
        .chat-sidebar { 
            width: 250px; background: #1a1a1a; padding: 20px; border-right: 1px solid #333; 
        }
        .chat-main { 
            flex: 1; display: flex; flex-direction: column; 
        }
        .messages { 
            flex: 1; padding: 20px; overflow-y: auto; 
        }
        .message { 
            margin: 15px 0; padding: 15px; border-radius: 8px; max-width: 80%; 
        }
        .user-message { 
            background: #2a4d6a; margin-left: auto; 
        }
        .asis-message { 
            background: #1e3a1e; 
        }
        .input-area { 
            padding: 20px; background: #1a1a1a; border-top: 1px solid #333; 
            display: flex; gap: 10px; align-items: center;
        }
        .message-input { 
            flex: 1; padding: 12px; background: #333; border: none; 
            border-radius: 4px; color: #fff; font-size: 14px;
        }
        .send-btn { 
            padding: 12px 20px; background: #00ff88; color: #000; 
            border: none; border-radius: 4px; cursor: pointer; font-weight: bold;
        }
        .mode-tabs { 
            display: flex; gap: 5px; margin-bottom: 20px; 
        }
        .mode-tab { 
            padding: 8px 12px; background: #333; border: none; 
            border-radius: 4px; cursor: pointer; color: #ccc; font-size: 12px;
        }
        .mode-tab.active { 
            background: #00ff88; color: #000; 
        }
        .typing-indicator { 
            color: #888; font-style: italic; margin: 10px 0; 
        }
        .conversation-history { 
            max-height: 300px; overflow-y: auto; margin-bottom: 20px; 
        }
        .history-item { 
            padding: 8px; background: #2a2a2a; margin: 5px 0; 
            border-radius: 4px; cursor: pointer; font-size: 12px;
        }
        .history-item:hover { 
            background: #333; 
        }
    </style>
</head>
<body>
    <div class="chat-header">
        <h2>🎯 ASIS Advanced Chat Interface</h2>
        <div>
            <span id="connection-status">🔴 Connecting...</span>
            <button onclick="location.href='/'" style="margin-left: 20px; padding: 8px 16px; background: #333; color: #fff; border: none; border-radius: 4px; cursor: pointer;">Dashboard</button>
        </div>
    </div>
    
    <div class="chat-container">
        <div class="chat-sidebar">
            <div class="mode-tabs">
                <button class="mode-tab active" data-mode="conversational">💬</button>
                <button class="mode-tab" data-mode="research">🔬</button>
                <button class="mode-tab" data-mode="creative">🎨</button>
                <button class="mode-tab" data-mode="learning">📚</button>
                <button class="mode-tab" data-mode="analysis">🔍</button>
                <button class="mode-tab" data-mode="monitoring">📊</button>
            </div>
            
            <h4>Current Mode: <span id="current-mode">Conversational</span></h4>
            <p id="mode-description">Natural conversation with ASIS</p>
            
            <h4>Conversation History</h4>
            <div class="conversation-history" id="conversation-history">
                <!-- History will be loaded here -->
            </div>
            
            <button onclick="newConversation()" style="width: 100%; padding: 10px; background: #00ff88; color: #000; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">New Conversation</button>
        </div>
        
        <div class="chat-main">
            <div class="messages" id="messages">
                <div class="message asis-message">
                    <strong>ASIS:</strong> Hello! I'm ASIS, your Advanced Intelligence System. I'm ready to assist you in multiple interaction modes. How can I help you today?
                </div>
            </div>
            
            <div class="typing-indicator" id="typing-indicator" style="display: none;">
                ASIS is typing...
            </div>
            
            <div class="input-area">
                <input type="text" class="message-input" id="message-input" placeholder="Type your message here..." onkeypress="handleKeyPress(event)">
                <button class="send-btn" onclick="sendMessage()">Send</button>
            </div>
        </div>
    </div>

    <script>
        const socket = io();
        let currentMode = 'conversational';
        let isTyping = false;
        
        const modeDescriptions = {
            'conversational': 'Natural conversation with ASIS',
            'research': 'Deep research and investigation',
            'creative': 'Creative thinking and ideation',
            'learning': 'Learning and knowledge acquisition',
            'analysis': 'Detailed analysis and problem solving',
            'monitoring': 'System monitoring and observation'
        };
        
        // Socket connection
        socket.on('connect', function() {
            document.getElementById('connection-status').innerHTML = '🟢 Connected';
            socket.emit('join_room', {room: 'chat'});
        });
        
        socket.on('disconnect', function() {
            document.getElementById('connection-status').innerHTML = '🔴 Disconnected';
        });
        
        socket.on('chat_response', function(data) {
            displayMessage(data.response, 'asis');
            hideTypingIndicator();
        });
        
        // Mode switching
        document.querySelectorAll('.mode-tab').forEach(tab => {
            tab.addEventListener('click', function() {
                document.querySelectorAll('.mode-tab').forEach(t => t.classList.remove('active'));
                this.classList.add('active');
                currentMode = this.dataset.mode;
                document.getElementById('current-mode').textContent = currentMode.charAt(0).toUpperCase() + currentMode.slice(1);
                document.getElementById('mode-description').textContent = modeDescriptions[currentMode];
            });
        });
        
        function sendMessage() {
            const input = document.getElementById('message-input');
            const message = input.value.trim();
            
            if (!message) return;
            
            displayMessage(message, 'user');
            input.value = '';
            
            showTypingIndicator();
            
            socket.emit('chat_message', {
                message: message,
                mode: currentMode,
                user_id: 'demo_user_001'
            });
        }
        
        function displayMessage(content, sender) {
            const messagesDiv = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            
            const senderName = sender === 'user' ? 'You' : 'ASIS';
            messageDiv.innerHTML = `<strong>${senderName}:</strong> ${content}`;
            
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function showTypingIndicator() {
            document.getElementById('typing-indicator').style.display = 'block';
            isTyping = true;
        }
        
        function hideTypingIndicator() {
            document.getElementById('typing-indicator').style.display = 'none';
            isTyping = false;
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        }
        
        function newConversation() {
            document.getElementById('messages').innerHTML = `
                <div class="message asis-message">
                    <strong>ASIS:</strong> Hello! I'm ready for a new conversation. How can I assist you today?
                </div>
            `;
        }
        
        // Focus input on load
        window.onload = function() {
            document.getElementById('message-input').focus();
        };
    </script>
</body>
</html>
    '''

def create_templates_directory():
    """Create templates directory and files"""
    import os
    
    # Create templates directory
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Write dashboard template
    with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(create_dashboard_template())
    
    # Write chat template
    with open('templates/chat.html', 'w', encoding='utf-8') as f:
        f.write(create_chat_template())
    
    # Create basic projects template
    with open('templates/projects.html', 'w', encoding='utf-8') as f:
        f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASIS Project Management</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #0a0a0a; color: #e0e0e0; }
        h1 { color: #00ff88; }
    </style>
</head>
<body>
    <h1>🚧 Project Management Dashboard</h1>
    <p>Advanced project management features coming soon!</p>
    <button onclick="location.href='/'" style="padding: 10px 20px; background: #00ff88; color: #000; border: none; border-radius: 4px; cursor: pointer;">Back to Dashboard</button>
</body>
</html>
        ''')

def main():
    """Main function to run ASIS Web Dashboard"""
    print("🌐 ASIS Advanced Web Dashboard and API System")
    print("=" * 60)
    
    # Create templates
    create_templates_directory()
    
    # Initialize and run web application
    web_api = ASISWebAPI()
    
    print("🚀 Starting ASIS Web Dashboard...")
    print("📊 Dashboard: http://localhost:5000")
    print("💬 Chat Interface: http://localhost:5000/chat")
    print("📋 Project Management: http://localhost:5000/projects")
    print("🔧 API Endpoints: http://localhost:5000/api/v1/")
    print("👤 Demo Login: demo / demo123")
    print()
    
    try:
        web_api.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n🛑 ASIS Web Dashboard stopped")

if __name__ == "__main__":
    main()
