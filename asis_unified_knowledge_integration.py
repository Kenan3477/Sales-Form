#!/usr/bin/env python3
"""
ASIS Unified Knowledge Integration
=================================
Flask API integration for unified memory and knowledge architecture
"""

import asyncio
import json
from flask import Blueprint, request, jsonify
from typing import Dict, Any

# Import the unified knowledge system
try:
    from asis_unified_knowledge import ASISUnifiedKnowledge
    UNIFIED_KNOWLEDGE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Unified Knowledge not available: {e}")
    UNIFIED_KNOWLEDGE_AVAILABLE = False

class ASISUnifiedKnowledgeIntegration:
    """Integration layer for unified knowledge system"""
    
    def __init__(self):
        if UNIFIED_KNOWLEDGE_AVAILABLE:
            self.knowledge_system = ASISUnifiedKnowledge()
            self.initialized = True
            print("✅ Unified Knowledge Integration initialized")
        else:
            self.knowledge_system = None
            self.initialized = False
            print("❌ Unified Knowledge Integration failed - module not available")
    
    def create_blueprint(self) -> Blueprint:
        """Create Flask blueprint for knowledge API endpoints"""
        knowledge_bp = Blueprint('knowledge', __name__, url_prefix='/api/knowledge')
        
        @knowledge_bp.route('/status', methods=['GET'])
        def get_status():
            """Get knowledge system status"""
            if not self.initialized:
                return jsonify({'error': 'Knowledge system not initialized'}), 503
            
            try:
                stats = self.knowledge_system.get_system_stats()
                return jsonify({
                    'status': 'operational',
                    'initialized': True,
                    'stats': stats
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @knowledge_bp.route('/experience/store', methods=['POST'])
        def store_experience():
            """Store episodic experience"""
            if not self.initialized:
                return jsonify({'error': 'Knowledge system not initialized'}), 503
            
            try:
                data = request.json
                experience = data.get('experience', {})
                
                # Run async function
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                memory_id = loop.run_until_complete(
                    self.knowledge_system.store_experience(experience)
                )
                loop.close()
                
                return jsonify({
                    'success': True,
                    'memory_id': memory_id,
                    'stored_experience': experience
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @knowledge_bp.route('/concept/integrate', methods=['POST'])
        def integrate_concept():
            """Integrate new conceptual knowledge"""
            if not self.initialized:
                return jsonify({'error': 'Knowledge system not initialized'}), 503
            
            try:
                data = request.json
                concept = data.get('concept', '')
                definition = data.get('definition', {})
                relations = data.get('relations', [])
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    self.knowledge_system.integrate_concept(concept, definition, relations)
                )
                loop.close()
                
                return jsonify({
                    'success': result,
                    'concept': concept,
                    'integrated': result
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @knowledge_bp.route('/procedure/learn', methods=['POST'])
        def learn_procedure():
            """Learn procedural knowledge"""
            if not self.initialized:
                return jsonify({'error': 'Knowledge system not initialized'}), 503
            
            try:
                data = request.json
                task = data.get('task', '')
                procedure = data.get('procedure', [])
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    self.knowledge_system.learn_procedure(task, procedure)
                )
                loop.close()
                
                return jsonify({
                    'success': result,
                    'task': task,
                    'learned': result
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @knowledge_bp.route('/query', methods=['POST'])
        def query_knowledge():
            """Query knowledge graph"""
            if not self.initialized:
                return jsonify({'error': 'Knowledge system not initialized'}), 503
            
            try:
                data = request.json
                query = data.get('query', {})
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    self.knowledge_system.query_knowledge(query)
                )
                loop.close()
                
                return jsonify({
                    'success': True,
                    'query': query,
                    'result': result
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @knowledge_bp.route('/reasoning', methods=['POST'])
        def perform_reasoning():
            """Perform complex reasoning"""
            if not self.initialized:
                return jsonify({'error': 'Knowledge system not initialized'}), 503
            
            try:
                data = request.json
                reasoning_query = data.get('reasoning_query', {})
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    self.knowledge_system.reason_over_knowledge(reasoning_query)
                )
                loop.close()
                
                return jsonify({
                    'success': True,
                    'reasoning_query': reasoning_query,
                    'result': result
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @knowledge_bp.route('/search', methods=['POST'])
        def comprehensive_search():
            """Perform comprehensive knowledge search"""
            if not self.initialized:
                return jsonify({'error': 'Knowledge system not initialized'}), 503
            
            try:
                data = request.json
                search_query = data.get('query', '')
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    self.knowledge_system.comprehensive_search(search_query)
                )
                loop.close()
                
                return jsonify({
                    'success': True,
                    'search_query': search_query,
                    'results': result
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        return knowledge_bp
    
    async def enhance_chat_response(self, message: str, base_response: Dict) -> Dict:
        """Enhance chat response with knowledge integration"""
        if not self.initialized:
            return base_response
        
        try:
            # Search for relevant knowledge
            search_results = await self.knowledge_system.comprehensive_search(message)
            
            # Add knowledge context to response
            enhanced_response = base_response.copy()
            enhanced_response['knowledge_context'] = {
                'relevant_experiences': len(search_results.get('episodic_memories', [])),
                'related_concepts': len(search_results.get('related_concepts', [])),
                'knowledge_connections': search_results.get('knowledge_connections', {}),
                'enhanced_with_knowledge': True
            }
            
            # Store this interaction as experience
            experience = {
                'context': {'type': 'chat', 'message': message},
                'actions': ['process_message', 'generate_response'],
                'outcomes': {'success': True, 'enhanced': True},
                'importance': 0.6
            }
            
            await self.knowledge_system.store_experience(experience)
            
            return enhanced_response
            
        except Exception as e:
            print(f"⚠️ Error enhancing chat response: {e}")
            return base_response
    
    def get_integration_status(self) -> Dict:
        """Get integration status"""
        return {
            'unified_knowledge_available': UNIFIED_KNOWLEDGE_AVAILABLE,
            'initialized': self.initialized,
            'integration_version': '1.0.0',
            'features': [
                'episodic_memory',
                'semantic_network', 
                'procedural_knowledge',
                'knowledge_graph',
                'complex_reasoning',
                'comprehensive_search'
            ] if self.initialized else []
        }

# Global integration instance
unified_knowledge_integration = ASISUnifiedKnowledgeIntegration()

def get_knowledge_blueprint():
    """Get the knowledge API blueprint"""
    return unified_knowledge_integration.create_blueprint()

def enhance_response_with_knowledge(message: str, response: Dict) -> Dict:
    """Enhance response with knowledge (sync wrapper)"""
    if not unified_knowledge_integration.initialized:
        return response
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        enhanced = loop.run_until_complete(
            unified_knowledge_integration.enhance_chat_response(message, response)
        )
        loop.close()
        return enhanced
    except Exception as e:
        print(f"⚠️ Error in knowledge enhancement: {e}")
        return response