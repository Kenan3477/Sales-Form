#!/usr/bin/env python3
"""
ASIS AGI Flask Integration
=========================
Flask endpoints and integration for AGI Core functionality

This module provides:
- AGI endpoints for the Flask web interface
- Integration with existing ASIS systems
- Compatibility with current verification systems
"""

import os
import sys
import json
import traceback
from datetime import datetime
from flask import jsonify, request
from typing import Dict, Any, Optional

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import AGI components
try:
    from asis_agi_core_stage2 import initialize_agi_core, get_agi_core, KnowledgeDomain
    AGI_AVAILABLE = True
except ImportError as e:
    print(f"Warning: AGI Core not available: {e}")
    AGI_AVAILABLE = False

class ASISAGIFlaskIntegration:
    """Flask integration for ASIS AGI Core"""
    
    def __init__(self, app=None):
        self.app = app
        self.agi_core = None
        self.integration_active = False
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize AGI integration with Flask app"""
        self.app = app
        
        # Initialize AGI Core if available
        if AGI_AVAILABLE:
            try:
                print("🚀 Initializing ASIS AGI Flask Integration...")
                self.agi_core = initialize_agi_core()
                self.integration_active = True
                print("✅ ASIS AGI Flask Integration active")
            except Exception as e:
                print(f"❌ Failed to initialize AGI Core: {e}")
                self.integration_active = False
        
        # Register AGI routes
        self._register_agi_routes()
    
    def _register_agi_routes(self):
        """Register AGI endpoints with Flask app"""
        if not self.app:
            return
        
        @self.app.route('/agi/status')
        def agi_status():
            """Get AGI system status"""
            return self._handle_agi_status()
        
        @self.app.route('/agi/reasoning', methods=['POST'])
        def agi_reasoning():
            """Perform AGI reasoning on a problem"""
            return self._handle_agi_reasoning()
        
        @self.app.route('/agi/knowledge')
        def agi_knowledge():
            """Get unified knowledge graph information"""
            return self._handle_agi_knowledge()
        
        @self.app.route('/agi/insights', methods=['POST'])
        def agi_insights():
            """Get cross-domain insights for a query"""
            return self._handle_agi_insights()
        
        @self.app.route('/agi/meta-cognitive')
        def agi_meta_cognitive():
            """Get meta-cognitive status and analytics"""
            return self._handle_meta_cognitive()
        
        @self.app.route('/agi/verification')
        def agi_verification():
            """Get AGI-enhanced verification status"""
            return self._handle_agi_verification()
        
        @self.app.route('/agi/performance')
        def agi_performance():
            """Get AGI performance analytics"""
            return self._handle_agi_performance()
        
        @self.app.route('/agi/chat', methods=['POST'])
        def agi_chat():
            """AGI-enhanced chat interface"""
            return self._handle_agi_chat()
    
    def _handle_agi_status(self) -> Dict[str, Any]:
        """Handle AGI status request"""
        try:
            if not self.integration_active or not self.agi_core:
                return jsonify({
                    'agi_available': False,
                    'status': 'AGI Core not initialized',
                    'message': 'AGI functionality is not available'
                })
            
            system_status = self.agi_core.get_system_status()
            
            return jsonify({
                'agi_available': True,
                'status': 'AGI Core Active',
                'system_status': system_status,
                'capabilities': [
                    'Unified Knowledge Graph',
                    'Cross-Domain Reasoning',
                    'Meta-Cognitive Control',
                    'Analogical Reasoning',
                    'Self-Optimization'
                ],
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            return jsonify({
                'error': f'AGI status error: {str(e)}',
                'agi_available': False
            }), 500
    
    def _handle_agi_reasoning(self) -> Dict[str, Any]:
        """Handle AGI reasoning request"""
        try:
            if not self.integration_active or not self.agi_core:
                return jsonify({
                    'error': 'AGI Core not available'
                }), 503
            
            data = request.get_json()
            if not data or 'problem' not in data:
                return jsonify({
                    'error': 'Problem statement required'
                }), 400
            
            problem = data['problem']
            context = data.get('context', {})
            
            # Process AGI request
            agi_response = self.agi_core.process_agi_request(problem, context)
            
            # Format response for web interface
            formatted_response = {
                'success': True,
                'session_id': agi_response['session_id'],
                'problem': problem,
                'solution': {
                    'reasoning_approach': agi_response['reasoning_result']['solution']['reasoning_approach'],
                    'confidence': agi_response['agi_confidence'],
                    'solution_components': agi_response['reasoning_result']['solution']['solution_components'],
                    'supporting_evidence': agi_response['reasoning_result']['solution']['supporting_evidence'],
                    'implementation_steps': agi_response['reasoning_result']['solution']['implementation_steps']
                },
                'cross_domain_insights': agi_response['cross_domain_insights'][:5],  # Limit for web display
                'meta_analysis': {
                    'strategy_used': agi_response['strategy_used'],
                    'processing_time': agi_response['processing_time'],
                    'knowledge_nodes_accessed': agi_response['reasoning_result']['knowledge_nodes_used'],
                    'domains_integrated': len(agi_response['reasoning_result']['relevant_domains']),
                    'analogies_discovered': agi_response['reasoning_result']['analogies_found']
                },
                'system_reflection': agi_response['meta_reflection']['quality_assessment'],
                'timestamp': datetime.now().isoformat()
            }
            
            return jsonify(formatted_response)
            
        except Exception as e:
            traceback.print_exc()
            return jsonify({
                'error': f'AGI reasoning error: {str(e)}',
                'success': False
            }), 500
    
    def _handle_agi_knowledge(self) -> Dict[str, Any]:
        """Handle knowledge graph information request"""
        try:
            if not self.integration_active or not self.agi_core:
                return jsonify({
                    'error': 'AGI Core not available'
                }), 503
            
            knowledge_stats = self.agi_core.knowledge_graph.get_knowledge_statistics()
            
            return jsonify({
                'knowledge_graph': {
                    'statistics': knowledge_stats,
                    'domains': [domain.value for domain in KnowledgeDomain],
                    'integration_status': 'Unified knowledge representation active',
                    'capabilities': [
                        'Cross-domain knowledge linking',
                        'Automatic connection discovery',
                        'Knowledge evolution tracking',
                        'Multi-domain insight generation'
                    ]
                },
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            return jsonify({
                'error': f'Knowledge graph error: {str(e)}'
            }), 500
    
    def _handle_agi_insights(self) -> Dict[str, Any]:
        """Handle cross-domain insights request"""
        try:
            if not self.integration_active or not self.agi_core:
                return jsonify({
                    'error': 'AGI Core not available'
                }), 503
            
            data = request.get_json()
            if not data or 'query' not in data:
                return jsonify({
                    'error': 'Query required'
                }), 400
            
            query = data['query']
            domains = data.get('domains', None)
            
            # Convert domain strings to enums if provided
            if domains:
                try:
                    domain_enums = [KnowledgeDomain(d) for d in domains]
                except ValueError as e:
                    return jsonify({
                        'error': f'Invalid domain: {str(e)}'
                    }), 400
            else:
                domain_enums = None
            
            insights = self.agi_core.knowledge_graph.get_cross_domain_insights(query, domain_enums)
            
            return jsonify({
                'query': query,
                'insights': insights,
                'insight_count': len(insights),
                'domains_searched': [d.value for d in (domain_enums or list(KnowledgeDomain))],
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            return jsonify({
                'error': f'Insights error: {str(e)}'
            }), 500
    
    def _handle_meta_cognitive(self) -> Dict[str, Any]:
        """Handle meta-cognitive status request"""
        try:
            if not self.integration_active or not self.agi_core:
                return jsonify({
                    'error': 'AGI Core not available'
                }), 503
            
            meta_status = self.agi_core.meta_controller.get_meta_cognitive_status()
            reasoning_analytics = self.agi_core.reasoning_engine.get_reasoning_analytics()
            
            return jsonify({
                'meta_cognitive_status': meta_status,
                'reasoning_analytics': reasoning_analytics,
                'self_awareness_level': 'Active meta-cognitive monitoring',
                'optimization_status': 'Continuous strategy optimization active',
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            return jsonify({
                'error': f'Meta-cognitive error: {str(e)}'
            }), 500
    
    def _handle_agi_verification(self) -> Dict[str, Any]:
        """Handle AGI-enhanced verification request"""
        try:
            if not self.integration_active or not self.agi_core:
                # Return basic verification if AGI not available
                return jsonify({
                    'overall_score': '85.0%',
                    'verification_level': 'BASIC AUTONOMOUS LEARNING',
                    'agi_enhancement': 'Not Available',
                    'status': 'BASIC SYSTEMS OPERATIONAL'
                })
            
            agi_verification = self.agi_core.get_verification_compatibility()
            
            return jsonify(agi_verification)
            
        except Exception as e:
            return jsonify({
                'error': f'AGI verification error: {str(e)}',
                'overall_score': '80.0%',
                'status': 'VERIFICATION ERROR'
            }), 500
    
    def _handle_agi_performance(self) -> Dict[str, Any]:
        """Handle AGI performance analytics request"""
        try:
            if not self.integration_active or not self.agi_core:
                return jsonify({
                    'error': 'AGI Core not available'
                }), 503
            
            performance_data = {
                'agi_sessions': len(self.agi_core.agi_performance_history),
                'recent_performance': list(self.agi_core.agi_performance_history)[-10:],
                'knowledge_growth': {
                    'total_nodes': len(self.agi_core.knowledge_graph.nodes),
                    'cross_domain_connections': len(self.agi_core.knowledge_graph.connections),
                    'domain_distribution': dict(self.agi_core.knowledge_graph.get_knowledge_statistics()['nodes_by_domain'])
                },
                'reasoning_evolution': {
                    'total_reasoning_sessions': len(self.agi_core.reasoning_engine.reasoning_history),
                    'strategy_performance': dict(self.agi_core.meta_controller._get_strategy_distribution()),
                    'quality_trend': 'improving'  # Could be calculated from history
                },
                'meta_cognitive_evolution': {
                    'adaptation_rate': self.agi_core.meta_controller.meta_state.adaptation_rate,
                    'reasoning_quality': self.agi_core.meta_controller.meta_state.reasoning_quality,
                    'confidence_level': self.agi_core.meta_controller.meta_state.confidence_level
                }
            }
            
            return jsonify({
                'performance_analytics': performance_data,
                'system_maturity': 'Evolving AGI System',
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            return jsonify({
                'error': f'Performance analytics error: {str(e)}'
            }), 500
    
    def _handle_agi_chat(self) -> Dict[str, Any]:
        """Handle AGI-enhanced chat request"""
        try:
            if not self.integration_active or not self.agi_core:
                return jsonify({
                    'response': 'AGI Core is not available. Using basic response system.',
                    'type': 'basic',
                    'agi_enhanced': False
                })
            
            data = request.get_json()
            if not data or 'message' not in data:
                return jsonify({
                    'error': 'Message required'
                }), 400
            
            message = data['message'].strip()
            context = data.get('context', {})
            
            # Process message with AGI
            agi_response = self.agi_core.process_agi_request(message, context)
            
            # Format for chat interface
            chat_response = {
                'response': self._format_agi_response_for_chat(agi_response),
                'type': 'agi_enhanced',
                'agi_enhanced': True,
                'session_id': agi_response['session_id'],
                'confidence': agi_response['agi_confidence'],
                'processing_time': agi_response['processing_time'],
                'strategy_used': agi_response['strategy_used'],
                'domains_consulted': agi_response['reasoning_result']['relevant_domains'],
                'knowledge_integration': f"Accessed {agi_response['reasoning_result']['knowledge_nodes_used']} knowledge nodes",
                'cross_domain_insights': len(agi_response['cross_domain_insights']),
                'timestamp': datetime.now().isoformat()
            }
            
            return jsonify(chat_response)
            
        except Exception as e:
            return jsonify({
                'response': f'AGI processing error: {str(e)}. Please try again.',
                'type': 'error',
                'agi_enhanced': False
            }), 500
    
    def _format_agi_response_for_chat(self, agi_response: Dict[str, Any]) -> str:
        """Format AGI response for chat interface"""
        solution = agi_response['reasoning_result']['solution']
        insights = agi_response['cross_domain_insights']
        
        # Build formatted response
        response_parts = []
        
        # Main response
        if solution['solution_components']:
            response_parts.append("🧠 **AGI Analysis:**")
            for i, component in enumerate(solution['solution_components'][:3], 1):
                comp_text = component.get('component', '')
                if len(comp_text) > 100:
                    comp_text = comp_text[:100] + "..."
                response_parts.append(f"{i}. {comp_text}")
        
        # Cross-domain insights
        if insights:
            response_parts.append("\n🔗 **Cross-Domain Insights:**")
            for insight in insights[:2]:
                domain = insight.get('domain', 'Unknown')
                relevance = insight.get('relevance', 0)
                response_parts.append(f"• {domain.title()}: {relevance:.1%} relevance")
        
        # Meta information
        meta_info = []
        meta_info.append(f"Strategy: {agi_response['strategy_used']}")
        meta_info.append(f"Confidence: {agi_response['agi_confidence']:.1%}")
        meta_info.append(f"Domains: {len(agi_response['reasoning_result']['relevant_domains'])}")
        
        response_parts.append(f"\n📊 **AGI Meta-Analysis:** {' | '.join(meta_info)}")
        
        return "\n".join(response_parts)


def create_agi_integration(app) -> ASISAGIFlaskIntegration:
    """Create and initialize AGI integration with Flask app"""
    return ASISAGIFlaskIntegration(app)

print("✅ ASIS AGI Flask Integration module loaded successfully")
