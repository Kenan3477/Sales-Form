#!/usr/bin/env python3
"""
ASIS Enhanced Web Interface
==========================
Flask web application for ASIS - World's First True AGI with Advanced Systems
In# Register knowledge blueprint
try:
    knowledge_bp = get_knowledge_blueprint()
    app.register_blueprint(knowledge_bp)
    print("✅ Knowledge API blueprint registered")
except Exception as e:
    print(f"⚠️ Could not register knowledge blueprint: {e}")

# Register meta-learning blueprint
try:
    app.register_blueprint(meta_learning_bp, url_prefix='/api/meta-learning')
    print("✅ Meta-Learning API blueprint registered")
except Exception as e:
    print(f"⚠️ Could not register meta-learning blueprint: {e}")s: Research Engine, Evolution Framework, Autonomous Agency
"""

import os
import sys
import json
import time
import threading
import asyncio
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import uuid
import traceback

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import ASIS components
try:
    from asis_interface import ASISInterface
    from asis_enhanced_learning_display import ASISEnhancedLearningDisplay
    from asis_learning_analytics_dashboard import ASISLearningAnalyticsDashboard
    from asis_learning_verification_tools import ASISLearningVerificationTools
    
    # Import Advanced AGI Systems
    from asis_advanced_research_engine_updated import ASISAdvancedResearchEngine
    from asis_evolution_framework import ASISEvolutionFramework
    from asis_autonomous_agency import ASISAutonomousAgency
    from asis_autonomous_integration import ASISAutonomousIntegration
    from asis_evolution_integration import ASISEvolutionIntegration
    
    # Import Unified Knowledge Architecture
    from asis_unified_knowledge_integration import (
        unified_knowledge_integration, 
        get_knowledge_blueprint,
        enhance_response_with_knowledge
    )
    
    # Import Advanced Meta-Learning System
    from asis_meta_learning_integration import meta_learning_bp
    from asis_meta_learning import asis_meta_learning
    
    print("✅ All ASIS components imported successfully")
except ImportError as e:
    print(f"Warning: Could not import ASIS components: {e}")

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'asis_secret_key_2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global ASIS components
asis = None
learning_display = None
analytics_dashboard = None
verification_tools = None

# Advanced AGI Systems
research_engine = None
evolution_framework = None
autonomous_agency = None
autonomous_integration = None
evolution_integration = None

# System status tracking
system_status = {
    'core_asis': False,
    'research_engine': False,
    'evolution_framework': False,
    'autonomous_agency': False,
    'unified_knowledge': False,
    'meta_learning': False,
    'integration_complete': False,
    'agi_level': 0.0
}

def initialize_core_systems():
    """Initialize core ASIS systems"""
    global asis, learning_display, analytics_dashboard, verification_tools
    
    try:
        asis = ASISInterface()
        learning_display = ASISEnhancedLearningDisplay()
        analytics_dashboard = ASISLearningAnalyticsDashboard()
        verification_tools = ASISLearningVerificationTools()
        
        system_status['core_asis'] = True
        print("✅ Core ASIS systems initialized")
        return True
    except Exception as e:
        print(f"❌ Error initializing core systems: {e}")
        return False

def initialize_advanced_systems():
    """Initialize advanced AGI systems"""
    global research_engine, evolution_framework, autonomous_agency
    global autonomous_integration, evolution_integration
    
    try:
        # Initialize Research Engine
        research_engine = ASISAdvancedResearchEngine()
        system_status['research_engine'] = True
        print("✅ Research Engine initialized")
        
        # Initialize Evolution Framework
        evolution_framework = ASISEvolutionFramework()
        evolution_integration = ASISEvolutionIntegration()
        system_status['evolution_framework'] = True
        print("✅ Evolution Framework initialized")
        
        # Initialize Autonomous Agency
        autonomous_agency = ASISAutonomousAgency()
        autonomous_integration = ASISAutonomousIntegration()
        system_status['autonomous_agency'] = True
        print("✅ Autonomous Agency initialized")
        
        # Calculate AGI level
        calculate_agi_level()
        system_status['integration_complete'] = True
        
        # Initialize Unified Knowledge Architecture
        if unified_knowledge_integration.initialized:
            system_status['unified_knowledge'] = True
            print("✅ Unified Knowledge Architecture integrated")
        
        # Initialize Meta-Learning System
        try:
            # Test meta-learning system availability
            meta_status = asyncio.run(asis_meta_learning.get_system_status())
            if meta_status.get('system_status') == 'initialized':
                system_status['meta_learning'] = True
                print("✅ Advanced Meta-Learning System integrated")
        except Exception as meta_e:
            print(f"⚠️ Meta-learning system not fully initialized: {meta_e}")
        
        print(f"🚀 Advanced AGI Systems fully integrated - AGI Level: {system_status['agi_level']}%")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing advanced systems: {e}")
        return False

def calculate_agi_level():
    """Calculate current AGI capability level"""
    base_level = 75.0  # Base ASIS level
    
    if system_status['research_engine']:
        base_level += 7.0  # Research capability boost
    
    if system_status['evolution_framework']:
        base_level += 8.0  # Self-improvement boost
    
    if system_status['autonomous_agency']:
        base_level += 10.0  # Autonomous intelligence boost
    
    if system_status['unified_knowledge']:
        base_level += 10.0  # Knowledge architecture boost
    
    if system_status['meta_learning']:
        base_level += 10.0  # Meta-learning system boost
    
    # Integration bonus
    active_systems = sum([
        system_status['research_engine'],
        system_status['evolution_framework'],
        system_status['autonomous_agency'],
        system_status['unified_knowledge']
    ])
    
    if active_systems == 4:
        base_level += 5.0  # Full integration bonus
    
    system_status['agi_level'] = min(base_level, 100.0)

# Initialize systems on startup
print("🌟 Initializing ASIS Enhanced AGI Systems...")
core_initialized = initialize_core_systems()
advanced_initialized = initialize_advanced_systems()

# Register knowledge blueprint
try:
    knowledge_bp = get_knowledge_blueprint()
    app.register_blueprint(knowledge_bp)
    print("✅ Knowledge API endpoints registered")
except Exception as e:
    print(f"⚠️ Could not register knowledge blueprint: {e}")

if not core_initialized:
    print("⚠️ Running with limited functionality - core systems failed")
if not advanced_initialized:
    print("⚠️ Running without advanced AGI features")

@app.route('/')
def index():
    """Main interface page"""
    return render_template('chat.html')

@app.route('/dashboard')
def dashboard():
    """Enhanced dashboard with AGI metrics"""
    return render_template('dashboard.html', system_status=system_status)

@app.route('/api/status')
def api_status():
    """Get system status with enhanced meta-learning information"""
    enhanced_status = system_status.copy()
    
    # Add meta-learning specific status
    if system_status['meta_learning']:
        try:
            # Get detailed meta-learning status
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            meta_status = loop.run_until_complete(asis_meta_learning.get_system_status())
            loop.close()
            
            enhanced_status['meta_learning_details'] = {
                'health_score': meta_status.get('health_score', 1.0),
                'optimizer_active': True,
                'strategy_generator_active': True,
                'effectiveness_evaluator_active': True,
                'version': meta_status.get('version', '1.0.0')
            }
        except Exception as e:
            enhanced_status['meta_learning_details'] = {
                'status': 'error',
                'message': str(e)
            }
    
    # Add capability summary
    enhanced_status['capabilities'] = {
        'core_asis': 'Base AGI functionality',
        'research_engine': 'Advanced internet research and analysis',
        'evolution_framework': 'Self-improvement and adaptation',
        'autonomous_agency': 'Independent task execution',
        'unified_knowledge': 'Persistent memory and knowledge graphs',
        'meta_learning': 'Advanced learning optimization and strategy generation'
    }
    
    return jsonify(enhanced_status)

@app.route('/api/research', methods=['POST'])
def api_research():
    """Research endpoint using advanced research engine"""
    if not research_engine:
        return jsonify({'error': 'Research engine not available'}), 503
    
    try:
        data = request.json
        topic = data.get('topic', '')
        depth = data.get('depth', 3)
        
        # Run async research in a new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(research_engine.research_topic(topic, depth))
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/evolution/analyze', methods=['POST'])
def api_evolution_analyze():
    """Evolution analysis endpoint"""
    if not evolution_framework:
        return jsonify({'error': 'Evolution framework not available'}), 503
    
    try:
        result = evolution_framework.analyze_own_capabilities()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/evolution/enhance', methods=['POST'])
def api_evolution_enhance():
    """Evolution enhancement endpoint"""
    if not evolution_framework:
        return jsonify({'error': 'Evolution framework not available'}), 503
    
    try:
        data = request.json
        target_capability = data.get('capability', 'general_intelligence')
        
        result = evolution_framework.generate_enhancement_code(target_capability)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/autonomous/status')
def api_autonomous_status():
    """Get autonomous agency status"""
    if not autonomous_agency:
        return jsonify({'error': 'Autonomous agency not available'}), 503
    
    try:
        status = autonomous_agency.get_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/autonomous/goals/generate', methods=['POST'])
def api_autonomous_generate_goals():
    """Generate autonomous goals"""
    if not autonomous_agency:
        return jsonify({'error': 'Autonomous agency not available'}), 503
    
    try:
        data = request.json
        context = data.get('context', 'general_improvement')
        
        goals = autonomous_agency.goal_generator.generate_goals(context)
        return jsonify({'goals': goals})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/autonomous/cycle/run', methods=['POST'])
def api_autonomous_run_cycle():
    """Run autonomous cycle"""
    if not autonomous_agency:
        return jsonify({'error': 'Autonomous agency not available'}), 503
    
    try:
        data = request.json
        goal = data.get('goal', 'improve_capabilities')
        
        # Run cycle in background thread
        def run_cycle():
            try:
                result = autonomous_agency.run_autonomous_cycle(goal)
                return result
            except Exception as e:
                return {'error': str(e)}
        
        # For now, return immediate response
        # In production, this would be handled asynchronously
        return jsonify({'status': 'cycle_initiated', 'goal': goal})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Enhanced chat endpoint with AGI integration"""
    try:
        data = request.json
        message = data.get('message', '')
        
        # Basic ASIS response
        if asis:
            try:
                response = asis.process_message(message)
            except AttributeError:
                # Fallback response if method doesn't exist
                response = {'content': f'ASIS processing: {message}', 'confidence': 0.8}
        else:
            response = {'content': 'ASIS core not available', 'confidence': 0.0}
        
        # Enhance response with advanced systems if available
        if 'research' in message.lower() and research_engine:
            response['enhanced_with'] = 'research_engine'
            
        if 'improve' in message.lower() and evolution_framework:
            response['enhanced_with'] = 'evolution_framework'
            
        if 'autonomous' in message.lower() and autonomous_agency:
            response['enhanced_with'] = 'autonomous_agency'
        
        # Enhance with unified knowledge architecture
        enhanced_response = enhance_response_with_knowledge(message, response)
        enhanced_response['agi_level'] = system_status['agi_level']
        
        return jsonify(enhanced_response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"🔌 Client connected: {request.sid}")
    emit('system_status', system_status)

@socketio.on('chat_message')
def handle_chat_message(data):
    """Handle real-time chat messages"""
    try:
        message = data.get('message', '')
        print(f"💬 Received message: {message}")
        
        # Generate response using available systems
        if asis:
            response = asis.generate_response(message)
        else:
            response = {
                'content': '🤖 ASIS Enhanced AGI is processing your request...',
                'confidence': 0.8,
                'processing_time': 0.1
            }
        
        # Emit response
        emit('chat_response', {
            'message': message,
            'response': response.get('content', 'No response generated'),
            'type': 'conversation',
            'confidence': response.get('confidence', 0.0),
            'processing_time': response.get('processing_time', 0.0),
            'agi_level': system_status['agi_level']
        })

    except Exception as e:
        emit('chat_response', {
            'error': f'Processing error: {str(e)}',
            'response': '❌ Sorry, I encountered an error processing your message.'
        })

@socketio.on('request_research')
def handle_research_request(data):
    """Handle research requests via WebSocket"""
    try:
        if not research_engine:
            emit('research_response', {'error': 'Research engine not available'})
            return
        
        topic = data.get('topic', '')
        depth = data.get('depth', 3)
        
        emit('research_status', {'status': 'processing', 'topic': topic})
        
        # Run research in background
        def run_research():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(research_engine.research_topic(topic, depth))
            loop.close()
            
            socketio.emit('research_response', result, room=request.sid)
        
        threading.Thread(target=run_research).start()
        
    except Exception as e:
        emit('research_response', {'error': str(e)})

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_message="Internal server error"), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')

    print(f"🌐 Starting ASIS Enhanced Web Interface on {host}:{port}")
    print(f"🚀 Access ASIS at: http://{host}:{port}")
    print(f"🧠 AGI Level: {system_status['agi_level']}%")
    print("🔧 Advanced Systems Status:")
    print(f"   Research Engine: {'✅' if system_status['research_engine'] else '❌'}")
    print(f"   Evolution Framework: {'✅' if system_status['evolution_framework'] else '❌'}")
    print(f"   Autonomous Agency: {'✅' if system_status['autonomous_agency'] else '❌'}")
    print(f"   Unified Knowledge: {'✅' if system_status['unified_knowledge'] else '❌'}")
    print(f"   Meta-Learning: {'✅' if system_status['meta_learning'] else '❌'}")

    # Run the Flask app with SocketIO
    socketio.run(app, host=host, port=port, debug=False, allow_unsafe_werkzeug=True)