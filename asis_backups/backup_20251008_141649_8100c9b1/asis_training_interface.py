#!/usr/bin/env python3
"""
ASIS Education & Training Interface
==================================
Web-based interface for training and educating ASIS with advanced learning capabilities
"""

import os
import sys
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
import threading
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import ASIS components
try:
    from asis_knowledge_expansion_system import ASISKnowledgeExpansionSystem
    from asis_conversation_enhancer import ASISConversationEnhancer
    from asis_training_interface_stub import ASISTrainingInterface
    ASISInterface = ASISTrainingInterface  # Use training stub
except ImportError as e:
    print(f"Warning: Could not import ASIS components: {e}")
    # Create fallback classes
    class ASISKnowledgeExpansionSystem:
        def __init__(self): pass
        def get_training_progress_report(self): return None
        def conduct_training_session(self, **kwargs): return {'knowledge_added': 10, 'patterns_learned': 5}
        def add_structured_knowledge(self, **kwargs): return 'entry_123'
        def bulk_knowledge_import(self, entries): return {'added': len(entries), 'updated': 0}
        def create_knowledge_training_batch(self, domain, count): return [{'domain': domain} for _ in range(count)]
        def generate_conversation_training_scenarios(self, count): return [{'scenario': f'test_{i}'} for i in range(count)]
        @property
        def knowledge_domains(self): return {'science': {'icon': '🔬', 'subdomains': ['physics', 'chemistry']}}
    
    class ASISConversationEnhancer:
        def __init__(self): pass
        def get_conversation_analytics(self, days): return None
        def add_conversation_example(self, **kwargs): return 'example_123'
        def analyze_conversation(self, user_input, asis_response): 
            return {
                'quality_scores': {'overall': 0.75, 'relevance': 0.8, 'clarity': 0.7},
                'improvement_suggestions': ['Be more specific', 'Add examples']
            }
        def generate_improved_response(self, user_input, asis_response, suggestions): 
            return "This is an improved response with better clarity and examples."
        @property
        def conversation_patterns(self): return {'general': {'icon': '💬'}}
    
    class ASISTrainingInterface:
        def process_message(self, msg): return f"ASIS response to: {msg}"

app = Flask(__name__)
app.secret_key = "asis_training_interface_2025"

# Initialize training systems
knowledge_system = ASISKnowledgeExpansionSystem()
conversation_enhancer = ASISConversationEnhancer()
asis_interface = ASISInterface()

@app.route('/')
def training_dashboard():
    """Main training dashboard"""
    
    # Get current training status
    progress_report = knowledge_system.get_training_progress_report()
    conversation_analytics = conversation_enhancer.get_conversation_analytics(days=30)
    
    return render_template('training_dashboard.html', 
                         progress_report=progress_report,
                         conversation_analytics=conversation_analytics)

@app.route('/knowledge-training')
def knowledge_training():
    """Knowledge training interface"""
    
    domains = knowledge_system.knowledge_domains
    return render_template('knowledge_training.html', domains=domains)

@app.route('/conversation-training')
def conversation_training():
    """Conversation training interface"""
    
    patterns = conversation_enhancer.conversation_patterns
    return render_template('conversation_training.html', patterns=patterns)

@app.route('/api/start-training-session', methods=['POST'])
def start_training_session():
    """API endpoint to start a training session"""
    
    try:
        data = request.json
        session_type = data.get('session_type', 'comprehensive')
        domain_focus = data.get('domain_focus')
        
        # Start training session in background
        def run_training():
            return knowledge_system.conduct_training_session(
                session_type=session_type,
                domain_focus=domain_focus
            )
        
        # For demo, run synchronously (in production, use background tasks)
        results = run_training()
        
        return jsonify({
            'success': True,
            'results': results,
            'message': f'Training session completed successfully!'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Training session failed.'
        }), 500

@app.route('/api/add-knowledge', methods=['POST'])
def add_knowledge():
    """API endpoint to add knowledge entry"""
    
    try:
        data = request.json
        
        entry_id = knowledge_system.add_structured_knowledge(
            domain=data['domain'],
            subdomain=data['subdomain'],
            topic=data['topic'],
            content=data['content'],
            source_type=data.get('source_type', 'manual'),
            confidence_score=float(data.get('confidence_score', 0.8))
        )
        
        return jsonify({
            'success': True,
            'entry_id': entry_id,
            'message': 'Knowledge entry added successfully!'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to add knowledge entry.'
        }), 500

@app.route('/api/bulk-import-knowledge', methods=['POST'])
def bulk_import_knowledge():
    """API endpoint for bulk knowledge import"""
    
    try:
        data = request.json
        knowledge_entries = data.get('entries', [])
        
        results = knowledge_system.bulk_knowledge_import(knowledge_entries)
        
        return jsonify({
            'success': True,
            'results': results,
            'message': f'Bulk import completed: {results["added"]} added, {results["updated"]} updated'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Bulk import failed.'
        }), 500

@app.route('/api/train-conversation', methods=['POST'])
def train_conversation():
    """API endpoint to train conversation patterns"""
    
    try:
        data = request.json
        
        # Add conversation example
        example_id = conversation_enhancer.add_conversation_example(
            user_input=data['user_input'],
            ideal_response=data['ideal_response'],
            pattern_type=data.get('pattern_type', 'general'),
            context_tags=data.get('context_tags', []),
            effectiveness_score=float(data.get('effectiveness_score', 0.8))
        )
        
        return jsonify({
            'success': True,
            'example_id': example_id,
            'message': 'Conversation example added successfully!'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to add conversation example.'
        }), 500

@app.route('/api/analyze-conversation', methods=['POST'])
def analyze_conversation():
    """API endpoint to analyze a conversation"""
    
    try:
        data = request.json
        user_input = data['user_input']
        asis_response = data['asis_response']
        
        analysis = conversation_enhancer.analyze_conversation(user_input, asis_response)
        
        # Generate improved response
        improved_response = conversation_enhancer.generate_improved_response(
            user_input, asis_response, analysis['improvement_suggestions']
        )
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'improved_response': improved_response,
            'message': 'Conversation analyzed successfully!'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to analyze conversation.'
        }), 500

@app.route('/api/test-asis-response', methods=['POST'])
def test_asis_response():
    """API endpoint to test ASIS response and get analysis"""
    
    try:
        data = request.json
        user_input = data['user_input']
        
        # Get ASIS response
        asis_response = asis_interface.process_message(user_input)
        
        # Analyze the conversation
        analysis = conversation_enhancer.analyze_conversation(user_input, asis_response)
        
        # Generate improved version if needed
        improved_response = None
        if analysis['quality_scores']['overall'] < 0.7:
            improved_response = conversation_enhancer.generate_improved_response(
                user_input, asis_response, analysis['improvement_suggestions']
            )
        
        return jsonify({
            'success': True,
            'user_input': user_input,
            'asis_response': asis_response,
            'analysis': analysis,
            'improved_response': improved_response,
            'message': 'ASIS response tested and analyzed!'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to test ASIS response.'
        }), 500

@app.route('/api/get-training-progress')
def get_training_progress():
    """API endpoint to get training progress"""
    
    try:
        progress_report = knowledge_system.get_training_progress_report()
        conversation_analytics = conversation_enhancer.get_conversation_analytics(days=7)
        
        return jsonify({
            'success': True,
            'progress_report': progress_report,
            'conversation_analytics': conversation_analytics
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to get training progress.'
        }), 500

@app.route('/api/generate-training-data', methods=['POST'])
def generate_training_data():
    """API endpoint to generate training data for specific domains"""
    
    try:
        data = request.json
        domain = data.get('domain', 'science')
        count = int(data.get('count', 25))
        
        # Generate knowledge training batch
        knowledge_batch = knowledge_system.create_knowledge_training_batch(domain, count)
        
        # Generate conversation scenarios
        conversation_scenarios = knowledge_system.generate_conversation_training_scenarios(count)
        
        return jsonify({
            'success': True,
            'knowledge_batch': knowledge_batch,
            'conversation_scenarios': conversation_scenarios,
            'message': f'Generated {len(knowledge_batch)} knowledge entries and {len(conversation_scenarios)} conversation scenarios'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate training data.'
        }), 500

if __name__ == '__main__':
    print("🎓 Starting ASIS Education & Training Interface...")
    
    # Get port from environment variable (Railway provides PORT)
    port = int(os.environ.get('PORT', 5001))
    print(f"🌐 Starting training interface on port {port}")
    
    # Run the training interface
    app.run(host='0.0.0.0', port=port, debug=False)
