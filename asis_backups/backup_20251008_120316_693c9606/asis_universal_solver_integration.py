#!/usr/bin/env python3
"""
ASIS Universal Solver Flask Integration
======================================
Integrates the Universal Problem-Solving System with Flask web application
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from flask import request, jsonify

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from asis_universal_solver import ASISUniversalSolver
except ImportError:
    print("Warning: ASIS Universal Solver not found, integration disabled")
    ASISUniversalSolver = None

class UniversalSolverIntegration:
    """Integration class for Universal Solver with Flask"""
    
    def __init__(self):
        self.solver = ASISUniversalSolver() if ASISUniversalSolver else None
        self.integration_status = "active" if self.solver else "disabled"
    
    def integrate_with_flask_app(self, app):
        """Integrate Universal Solver endpoints with Flask app"""
        if not self.solver:
            print("❌ Universal Solver not available for integration")
            return False
        
        try:
            # Universal problem solving endpoint
            @app.route('/api/universal-solver/solve', methods=['POST'])
            def solve_universal_problem():
                """Solve any type of problem using the universal solver"""
                try:
                    data = request.get_json()
                    problem_text = data.get('problem_text', '').strip()
                    
                    if not problem_text:
                        return jsonify({
                            'error': 'Problem text is required'
                        }), 400
                    
                    session_id = data.get('session_id')
                    
                    # Solve the problem
                    result = self.solver.solve_problem(problem_text, session_id)
                    
                    return jsonify({
                        'success': True,
                        'data': result,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    return jsonify({
                        'success': False,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    }), 500
            
            # Get solution details endpoint
            @app.route('/api/universal-solver/solution/<session_id>/<solution_id>', methods=['GET'])
            def get_solution_details(session_id, solution_id):
                """Get detailed information about a specific solution"""
                try:
                    details = self.solver.get_solution_details(session_id, solution_id)
                    
                    return jsonify({
                        'success': True,
                        'data': details,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    return jsonify({
                        'success': False,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    }), 500
            
            # Solver statistics endpoint
            @app.route('/api/universal-solver/stats', methods=['GET'])
            def get_solver_statistics():
                """Get universal solver performance statistics"""
                try:
                    stats = self.solver.get_solver_statistics()
                    
                    return jsonify({
                        'success': True,
                        'data': stats,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    return jsonify({
                        'success': False,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    }), 500
            
            # Problem analysis endpoint
            @app.route('/api/universal-solver/analyze', methods=['POST'])
            def analyze_problem_structure():
                """Analyze problem structure without generating solutions"""
                try:
                    data = request.get_json()
                    problem_text = data.get('problem_text', '').strip()
                    
                    if not problem_text:
                        return jsonify({
                            'error': 'Problem text is required'
                        }), 400
                    
                    # Analyze problem structure
                    structure = self.solver.structure_analyzer.analyze_problem_structure(problem_text)
                    
                    return jsonify({
                        'success': True,
                        'data': {
                            'problem_id': structure.problem_id,
                            'problem_type': structure.problem_type.value,
                            'domain': structure.domain,
                            'complexity_score': structure.complexity_score,
                            'key_components': structure.key_components,
                            'relationships': structure.relationships,
                            'constraints': structure.constraints,
                            'objectives': structure.objectives,
                            'keywords': structure.keywords,
                            'structural_patterns': structure.structural_patterns
                        },
                        'timestamp': datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    return jsonify({
                        'success': False,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    }), 500
            
            # Pattern matching endpoint
            @app.route('/api/universal-solver/patterns', methods=['POST'])
            def find_cross_domain_patterns():
                """Find cross-domain pattern matches for a problem"""
                try:
                    data = request.get_json()
                    problem_text = data.get('problem_text', '').strip()
                    
                    if not problem_text:
                        return jsonify({
                            'error': 'Problem text is required'
                        }), 400
                    
                    # Analyze problem and find patterns
                    structure = self.solver.structure_analyzer.analyze_problem_structure(problem_text)
                    patterns = self.solver.pattern_matcher.find_cross_domain_matches(structure)
                    
                    return jsonify({
                        'success': True,
                        'data': {
                            'problem_analysis': {
                                'problem_type': structure.problem_type.value,
                                'domain': structure.domain,
                                'complexity_score': structure.complexity_score
                            },
                            'pattern_matches': patterns
                        },
                        'timestamp': datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    return jsonify({
                        'success': False,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    }), 500
            
            # Solution feedback endpoint
            @app.route('/api/universal-solver/feedback', methods=['POST'])
            def record_solution_feedback():
                """Record feedback about solution implementation"""
                try:
                    data = request.get_json()
                    solution_id = data.get('solution_id')
                    problem_id = data.get('problem_id')
                    feedback = data.get('feedback', {})
                    
                    if not solution_id or not problem_id:
                        return jsonify({
                            'error': 'Solution ID and Problem ID are required'
                        }), 400
                    
                    # Record feedback
                    success = self.solver.learning_system.record_solution_feedback(
                        solution_id, problem_id, feedback
                    )
                    
                    return jsonify({
                        'success': success,
                        'message': 'Feedback recorded successfully' if success else 'Failed to record feedback',
                        'timestamp': datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    return jsonify({
                        'success': False,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    }), 500
            
            # Learning insights endpoint
            @app.route('/api/universal-solver/insights', methods=['GET'])
            def get_learning_insights():
                """Get extracted learning insights from recent solutions"""
                try:
                    # This would typically query recent solutions
                    # For now, return a placeholder response
                    insights = []
                    
                    return jsonify({
                        'success': True,
                        'data': {
                            'insights': insights,
                            'insight_count': len(insights)
                        },
                        'timestamp': datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    return jsonify({
                        'success': False,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    }), 500
            
            print("✅ Universal Solver endpoints integrated with Flask")
            return True
            
        except Exception as e:
            print(f"❌ Universal Solver Flask integration error: {e}")
            return False
    
    def create_universal_solver_endpoints(self, app):
        """Create Universal Solver specific endpoints"""
        if not self.solver:
            return False
        
        try:
            # Multi-strategy generation endpoint
            @app.route('/api/universal-solver/strategies', methods=['POST'])
            def generate_multiple_strategies():
                """Generate multiple solution strategies"""
                try:
                    data = request.get_json()
                    problem_text = data.get('problem_text', '').strip()
                    
                    if not problem_text:
                        return jsonify({
                            'error': 'Problem text is required'
                        }), 400
                    
                    # Analyze problem and generate strategies
                    structure = self.solver.structure_analyzer.analyze_problem_structure(problem_text)
                    patterns = self.solver.pattern_matcher.find_cross_domain_matches(structure)
                    solutions = self.solver.solution_generator.generate_multiple_solutions(structure, patterns)
                    
                    return jsonify({
                        'success': True,
                        'data': {
                            'total_strategies': len(solutions),
                            'strategies': [
                                {
                                    'strategy_id': sol.approach_id,
                                    'strategy_name': sol.strategy.value,
                                    'description': sol.description,
                                    'confidence_score': sol.confidence_score,
                                    'estimated_time': sol.estimated_time,
                                    'risk_level': sol.risk_level,
                                    'success_probability': sol.success_probability
                                }
                                for sol in solutions
                            ]
                        },
                        'timestamp': datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    return jsonify({
                        'success': False,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    }), 500
            
            # Problem complexity assessment endpoint
            @app.route('/api/universal-solver/complexity', methods=['POST'])
            def assess_problem_complexity():
                """Assess problem complexity and provide recommendations"""
                try:
                    data = request.get_json()
                    problem_text = data.get('problem_text', '').strip()
                    
                    if not problem_text:
                        return jsonify({
                            'error': 'Problem text is required'
                        }), 400
                    
                    # Analyze problem complexity
                    structure = self.solver.structure_analyzer.analyze_problem_structure(problem_text)
                    
                    # Generate complexity recommendations
                    recommendations = []
                    if structure.complexity_score > 0.8:
                        recommendations.extend([
                            "Consider breaking down into smaller sub-problems",
                            "Plan for extended timeline and additional resources",
                            "Consider collaborative approach with domain experts",
                            "Implement iterative solution development"
                        ])
                    elif structure.complexity_score > 0.5:
                        recommendations.extend([
                            "Plan systematic approach with clear milestones",
                            "Prepare contingency strategies",
                            "Document assumptions and dependencies"
                        ])
                    else:
                        recommendations.extend([
                            "Straightforward analytical approach should work",
                            "Standard resources and timeline sufficient"
                        ])
                    
                    return jsonify({
                        'success': True,
                        'data': {
                            'complexity_score': structure.complexity_score,
                            'complexity_level': (
                                'HIGH' if structure.complexity_score > 0.7 else
                                'MEDIUM' if structure.complexity_score > 0.4 else 'LOW'
                            ),
                            'key_complexity_factors': {
                                'component_count': len(structure.key_components),
                                'relationship_count': len(structure.relationships),
                                'constraint_count': len(structure.constraints),
                                'domain_specificity': structure.domain
                            },
                            'recommendations': recommendations
                        },
                        'timestamp': datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    return jsonify({
                        'success': False,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    }), 500
            
            return True
            
        except Exception as e:
            print(f"Universal Solver endpoint creation error: {e}")
            return False
    
    def enhance_production_system_with_universal_solver(self, app):
        """Enhance existing production system with universal solver capabilities"""
        if not self.solver:
            return False
        
        try:
            # Add universal solver status to system info
            @app.route('/api/system/universal-solver-status', methods=['GET'])
            def get_universal_solver_status():
                """Get universal solver system status"""
                try:
                    stats = self.solver.get_solver_statistics()
                    
                    return jsonify({
                        'success': True,
                        'data': {
                            'status': self.integration_status,
                            'solver_available': self.solver is not None,
                            'statistics': stats,
                            'capabilities': [
                                'Problem Structure Analysis',
                                'Cross-Domain Pattern Matching',
                                'Multi-Strategy Solution Generation',
                                'Learning Integration',
                                'Universal Problem Solving'
                            ]
                        },
                        'timestamp': datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    return jsonify({
                        'success': False,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    }), 500
            
            print("✅ Production system enhanced with Universal Solver capabilities")
            return True
            
        except Exception as e:
            print(f"Production system enhancement error: {e}")
            return False

def integrate_universal_solver_system():
    """Main integration function"""
    try:
        # Initialize integration
        integration = UniversalSolverIntegration()
        
        # Import Flask app
        try:
            from app import app
            flask_app = app
        except ImportError:
            try:
                from asis_100_percent_production_agi import app
                flask_app = app
            except ImportError:
                print("❌ Flask app not found for Universal Solver integration")
                return False
        
        # Integrate with Flask
        success = integration.integrate_with_flask_app(flask_app)
        if success:
            integration.create_universal_solver_endpoints(flask_app)
            integration.enhance_production_system_with_universal_solver(flask_app)
        
        return success
        
    except Exception as e:
        print(f"❌ Universal Solver integration error: {e}")
        return False

if __name__ == "__main__":
    print("🌟 ASIS Universal Solver Flask Integration")
    print("=" * 50)
    
    success = integrate_universal_solver_system()
    
    if success:
        print("✅ Universal Solver successfully integrated with Flask")
    else:
        print("❌ Universal Solver integration failed")
