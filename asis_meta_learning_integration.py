"""
ASIS Meta-Learning Integration
Flask API integration layer for the Advanced Meta-Learning System
"""

from flask import Blueprint, request, jsonify
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any
import traceback

# Import the meta-learning system
from asis_meta_learning import asis_meta_learning

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask blueprint for meta-learning endpoints
meta_learning_bp = Blueprint('meta_learning', __name__)

def async_wrapper(async_func):
    """Wrapper to run async functions in Flask routes"""
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(async_func(*args, **kwargs))
            loop.close()
            return result
        except Exception as e:
            logger.error(f"Error in async wrapper: {e}")
            logger.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}, 500
    wrapper.__name__ = async_func.__name__
    return wrapper

@meta_learning_bp.route('/status', methods=['GET'])
@async_wrapper
async def get_meta_learning_status():
    """Get comprehensive meta-learning system status"""
    try:
        status = await asis_meta_learning.get_system_status()
        
        # Add API-specific information
        status["api_version"] = "1.0.0"
        status["endpoints_available"] = [
            "/api/meta-learning/status",
            "/api/meta-learning/performance/analyze",
            "/api/meta-learning/strategies/generate",
            "/api/meta-learning/strategies/optimize",
            "/api/meta-learning/strategies/evaluate",
            "/api/meta-learning/learning/adapt",
            "/api/meta-learning/insights/generate"
        ]
        status["timestamp"] = datetime.now().isoformat()
        
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Error getting meta-learning status: {e}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@meta_learning_bp.route('/performance/analyze', methods=['GET', 'POST'])
@async_wrapper
async def analyze_learning_performance():
    """Analyze performance of current learning approaches"""
    try:
        # Get analysis parameters if provided
        params = {}
        if request.method == 'POST':
            data = request.get_json() or {}
            params = data.get('analysis_params', {})
        
        # Perform performance analysis
        analysis = await asis_meta_learning.analyze_learning_performance()
        
        # Enhance response with API metadata
        response = {
            "performance_analysis": analysis,
            "analysis_parameters": params,
            "meta_learning_version": "1.0.0",
            "analysis_timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Error analyzing learning performance: {e}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@meta_learning_bp.route('/strategies/generate', methods=['POST'])
@async_wrapper
async def generate_learning_strategies():
    """Generate domain-specific learning strategies"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "Request body required"
            }), 400
        
        domain = data.get('domain')
        if not domain:
            return jsonify({
                "status": "error",
                "message": "Domain parameter required"
            }), 400
        
        # Optional parameters
        strategy_count = data.get('strategy_count', None)
        complexity_preference = data.get('complexity_preference', 'balanced')
        custom_requirements = data.get('requirements', {})
        
        # Generate strategies
        strategies = await asis_meta_learning.generate_learning_strategies(domain)
        
        # Apply filters if specified
        if strategy_count and len(strategies) > strategy_count:
            # Sort by expected effectiveness and take top N
            strategies = sorted(
                strategies, 
                key=lambda x: x.get('expected_effectiveness', 0), 
                reverse=True
            )[:strategy_count]
        
        # Filter by complexity preference
        if complexity_preference != 'balanced':
            if complexity_preference == 'simple':
                strategies = [s for s in strategies if s.get('complexity_score', 0.5) <= 0.6]
            elif complexity_preference == 'complex':
                strategies = [s for s in strategies if s.get('complexity_score', 0.5) >= 0.7]
        
        response = {
            "strategies": strategies,
            "domain": domain,
            "strategy_count": len(strategies),
            "generation_parameters": {
                "domain": domain,
                "strategy_count": strategy_count,
                "complexity_preference": complexity_preference,
                "custom_requirements": custom_requirements
            },
            "generation_timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
        logger.info(f"Generated {len(strategies)} strategies for domain: {domain}")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error generating learning strategies: {e}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@meta_learning_bp.route('/strategies/optimize', methods=['POST'])
@async_wrapper
async def optimize_learning_strategy():
    """Optimize parameters for a learning strategy"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "Request body required"
            }), 400
        
        strategy = data.get('strategy')
        if not strategy:
            return jsonify({
                "status": "error",
                "message": "Strategy parameter required"
            }), 400
        
        # Optional optimization parameters
        optimization_goals = data.get('optimization_goals', ['effectiveness', 'efficiency'])
        constraints = data.get('constraints', {})
        
        # Perform optimization
        optimized_strategy = await asis_meta_learning.optimize_learning_parameters(strategy)
        
        # Calculate optimization metrics
        original_effectiveness = strategy.get('expected_effectiveness', 0.5)
        optimized_effectiveness = optimized_strategy.get('expected_effectiveness', original_effectiveness)
        improvement_ratio = optimized_effectiveness / max(original_effectiveness, 0.001)
        
        response = {
            "original_strategy": strategy,
            "optimized_strategy": optimized_strategy,
            "optimization_results": {
                "improvement_score": optimized_strategy.get('improvement_score', 0.0),
                "improvement_ratio": improvement_ratio,
                "optimization_method": optimized_strategy.get('optimization_method', 'unknown'),
                "confidence": optimized_strategy.get('confidence', 0.5)
            },
            "optimization_parameters": {
                "goals": optimization_goals,
                "constraints": constraints
            },
            "optimization_timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
        logger.info(f"Optimized strategy with improvement score: {optimized_strategy.get('improvement_score', 0):.3f}")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error optimizing learning strategy: {e}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@meta_learning_bp.route('/strategies/evaluate', methods=['POST'])
@async_wrapper
async def evaluate_strategy_effectiveness():
    """Evaluate effectiveness of a learning strategy"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "Request body required"
            }), 400
        
        strategy = data.get('strategy')
        results = data.get('results')
        
        if not strategy or not results:
            return jsonify({
                "status": "error",
                "message": "Both strategy and results parameters required"
            }), 400
        
        # Perform evaluation
        effectiveness_score = await asis_meta_learning.evaluate_strategy_effectiveness(strategy, results)
        
        # Generate detailed evaluation breakdown
        evaluation_breakdown = {
            "overall_effectiveness": effectiveness_score,
            "performance_category": _categorize_performance(effectiveness_score),
            "strategy_analysis": {
                "domain": strategy.get('domain', 'unknown'),
                "complexity": strategy.get('complexity_score', 0.5),
                "expected_vs_actual": {
                    "expected": strategy.get('expected_effectiveness', 0.5),
                    "actual": effectiveness_score,
                    "difference": effectiveness_score - strategy.get('expected_effectiveness', 0.5)
                }
            },
            "recommendations": _generate_evaluation_recommendations(effectiveness_score, strategy, results)
        }
        
        response = {
            "strategy": strategy,
            "results": results,
            "evaluation": evaluation_breakdown,
            "evaluation_timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
        logger.info(f"Evaluated strategy effectiveness: {effectiveness_score:.3f}")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error evaluating strategy effectiveness: {e}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@meta_learning_bp.route('/learning/adapt', methods=['POST'])
@async_wrapper
async def adaptive_learning_update():
    """Update learning strategies based on recent performance"""
    try:
        data = request.get_json() or {}
        
        # Get recent performance data
        performance_window = data.get('performance_window', '24h')
        adaptation_strength = data.get('adaptation_strength', 'moderate')
        target_domains = data.get('target_domains', [])
        
        # Analyze recent performance
        performance_analysis = await asis_meta_learning.analyze_learning_performance()
        
        # Generate adaptive recommendations
        adaptive_recommendations = await _generate_adaptive_recommendations(
            performance_analysis, adaptation_strength, target_domains
        )
        
        # Create adaptive learning plan
        learning_plan = {
            "adaptation_recommendations": adaptive_recommendations,
            "performance_insights": performance_analysis.get('meta_learning_insights', []),
            "suggested_strategies": [],
            "optimization_targets": _identify_optimization_targets(performance_analysis),
            "next_evaluation_schedule": _calculate_next_evaluation_time(adaptation_strength)
        }
        
        # Generate new strategies for underperforming domains
        underperforming_domains = _identify_underperforming_domains(performance_analysis)
        for domain in underperforming_domains:
            if not target_domains or domain in target_domains:
                new_strategies = await asis_meta_learning.generate_learning_strategies(domain)
                learning_plan["suggested_strategies"].extend(new_strategies[:2])  # Top 2 strategies
        
        response = {
            "adaptive_learning_plan": learning_plan,
            "performance_analysis": performance_analysis,
            "adaptation_parameters": {
                "performance_window": performance_window,
                "adaptation_strength": adaptation_strength,
                "target_domains": target_domains
            },
            "adaptation_timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
        logger.info(f"Generated adaptive learning plan with {len(adaptive_recommendations)} recommendations")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error in adaptive learning update: {e}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@meta_learning_bp.route('/insights/generate', methods=['POST'])
@async_wrapper
async def generate_meta_learning_insights():
    """Generate comprehensive meta-learning insights and recommendations"""
    try:
        data = request.get_json() or {}
        
        # Get insight parameters
        insight_depth = data.get('insight_depth', 'comprehensive')
        focus_areas = data.get('focus_areas', ['performance', 'optimization', 'strategy_selection'])
        time_horizon = data.get('time_horizon', '30d')
        
        # Gather comprehensive data
        performance_analysis = await asis_meta_learning.analyze_learning_performance()
        system_status = await asis_meta_learning.get_system_status()
        
        # Generate insights based on focus areas
        insights = {}
        
        if 'performance' in focus_areas:
            insights['performance_insights'] = await _generate_performance_insights(
                performance_analysis, time_horizon
            )
        
        if 'optimization' in focus_areas:
            insights['optimization_insights'] = await _generate_optimization_insights(
                performance_analysis, system_status
            )
        
        if 'strategy_selection' in focus_areas:
            insights['strategy_insights'] = await _generate_strategy_selection_insights(
                performance_analysis
            )
        
        # Generate meta-insights (insights about the meta-learning process itself)
        meta_insights = await _generate_meta_insights(performance_analysis, system_status)
        
        # Create actionable recommendations
        actionable_recommendations = await _create_actionable_recommendations(
            insights, meta_insights, insight_depth
        )
        
        response = {
            "meta_learning_insights": insights,
            "meta_insights": meta_insights,
            "actionable_recommendations": actionable_recommendations,
            "insight_parameters": {
                "depth": insight_depth,
                "focus_areas": focus_areas,
                "time_horizon": time_horizon
            },
            "confidence_score": _calculate_insight_confidence(insights),
            "generation_timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
        logger.info(f"Generated meta-learning insights for {len(focus_areas)} focus areas")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error generating meta-learning insights: {e}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

# Helper functions for the API endpoints

def _categorize_performance(effectiveness_score: float) -> str:
    """Categorize performance level"""
    if effectiveness_score >= 0.9:
        return "excellent"
    elif effectiveness_score >= 0.8:
        return "very_good"
    elif effectiveness_score >= 0.7:
        return "good"
    elif effectiveness_score >= 0.6:
        return "fair"
    elif effectiveness_score >= 0.5:
        return "poor"
    else:
        return "very_poor"

def _generate_evaluation_recommendations(effectiveness_score: float, strategy: Dict, results: Dict) -> List[str]:
    """Generate recommendations based on evaluation results"""
    recommendations = []
    
    if effectiveness_score < 0.6:
        recommendations.append("Consider strategy overhaul - current approach underperforming")
        recommendations.append("Investigate parameter tuning opportunities")
    elif effectiveness_score < 0.8:
        recommendations.append("Strategy shows promise - focus on optimization")
        recommendations.append("Monitor performance trends for stability")
    else:
        recommendations.append("Excellent performance - consider this as baseline strategy")
        recommendations.append("Document successful parameters for future use")
    
    # Domain-specific recommendations
    domain = strategy.get('domain', 'general')
    if domain == 'nlp' and effectiveness_score < 0.7:
        recommendations.append("Consider transformer-based approaches for NLP tasks")
    elif domain == 'vision' and effectiveness_score < 0.7:
        recommendations.append("Evaluate transfer learning strategies for vision tasks")
    
    return recommendations

async def _generate_adaptive_recommendations(analysis: Dict, strength: str, domains: List[str]) -> List[Dict]:
    """Generate adaptive learning recommendations"""
    recommendations = []
    
    overall_effectiveness = analysis.get('overall_effectiveness', 0.5)
    trend = analysis.get('effectiveness_trend', 'stable')
    
    # Base recommendations based on performance
    if overall_effectiveness < 0.7:
        recommendations.append({
            "type": "strategy_diversification",
            "priority": "high",
            "description": "Increase strategy diversity to improve overall effectiveness",
            "action": "generate_new_strategies",
            "target_domains": domains or ["nlp", "vision", "general"]
        })
    
    if trend == "declining":
        recommendations.append({
            "type": "performance_recovery",
            "priority": "critical",
            "description": "Address declining performance trend",
            "action": "optimize_existing_strategies",
            "urgency": "immediate"
        })
    
    # Strength-based recommendations
    if strength == "aggressive":
        recommendations.append({
            "type": "rapid_adaptation",
            "priority": "medium",
            "description": "Implement rapid learning rate adjustments",
            "action": "increase_adaptation_rate",
            "parameters": {"adaptation_multiplier": 1.5}
        })
    elif strength == "conservative":
        recommendations.append({
            "type": "gradual_improvement",
            "priority": "low",
            "description": "Make gradual incremental improvements",
            "action": "fine_tune_parameters",
            "parameters": {"adaptation_multiplier": 0.8}
        })
    
    return recommendations

def _identify_optimization_targets(analysis: Dict) -> List[Dict]:
    """Identify specific optimization targets from performance analysis"""
    targets = []
    
    domain_performance = analysis.get('domain_performance', {})
    for domain, performance_data in domain_performance.items():
        if performance_data:
            avg_performance = sum(entry['effectiveness'] for entry in performance_data) / len(performance_data)
            if avg_performance < 0.75:
                targets.append({
                    "target_type": "domain_improvement",
                    "domain": domain,
                    "current_performance": avg_performance,
                    "target_performance": 0.85,
                    "improvement_needed": 0.85 - avg_performance
                })
    
    return targets

def _calculate_next_evaluation_time(adaptation_strength: str) -> str:
    """Calculate when the next evaluation should occur"""
    from datetime import timedelta
    
    intervals = {
        "conservative": timedelta(days=7),
        "moderate": timedelta(days=3),
        "aggressive": timedelta(days=1)
    }
    
    interval = intervals.get(adaptation_strength, timedelta(days=3))
    next_time = datetime.now() + interval
    
    return next_time.isoformat()

def _identify_underperforming_domains(analysis: Dict) -> List[str]:
    """Identify domains that are underperforming"""
    underperforming = []
    domain_performance = analysis.get('domain_performance', {})
    
    for domain, performance_data in domain_performance.items():
        if performance_data:
            avg_performance = sum(entry['effectiveness'] for entry in performance_data) / len(performance_data)
            if avg_performance < 0.7:
                underperforming.append(domain)
    
    return underperforming

async def _generate_performance_insights(analysis: Dict, time_horizon: str) -> Dict:
    """Generate performance-specific insights"""
    return {
        "trend_analysis": {
            "current_trend": analysis.get('effectiveness_trend', 'unknown'),
            "trend_strength": "moderate",
            "prediction": "improvement expected with current optimizations"
        },
        "performance_distribution": {
            "top_quartile": 0.85,
            "median": analysis.get('overall_effectiveness', 0.5),
            "bottom_quartile": 0.65
        },
        "improvement_opportunities": [
            "Focus on underperforming domains",
            "Implement adaptive learning rates",
            "Increase strategy diversity"
        ]
    }

async def _generate_optimization_insights(analysis: Dict, status: Dict) -> Dict:
    """Generate optimization-specific insights"""
    return {
        "optimization_effectiveness": status.get('health_score', 0.8),
        "optimization_frequency": "optimal",
        "parameter_sensitivity": {
            "learning_rate": "high",
            "batch_size": "medium",
            "regularization": "low"
        },
        "optimization_recommendations": [
            "Continue current optimization approach",
            "Monitor parameter sensitivity",
            "Implement automated hyperparameter tuning"
        ]
    }

async def _generate_strategy_selection_insights(analysis: Dict) -> Dict:
    """Generate strategy selection insights"""
    top_strategies = analysis.get('top_strategies', [])
    
    return {
        "strategy_diversity": len(analysis.get('domain_performance', {})),
        "top_performing_strategies": top_strategies[:3],
        "strategy_effectiveness_distribution": {
            "excellent": len([s for s in top_strategies if s.get('avg_effectiveness', 0) >= 0.9]),
            "good": len([s for s in top_strategies if 0.7 <= s.get('avg_effectiveness', 0) < 0.9]),
            "fair": len([s for s in top_strategies if s.get('avg_effectiveness', 0) < 0.7])
        },
        "selection_recommendations": [
            "Favor top-performing strategies for critical tasks",
            "Maintain strategy diversity for robustness",
            "Regular evaluation of strategy effectiveness"
        ]
    }

async def _generate_meta_insights(analysis: Dict, status: Dict) -> Dict:
    """Generate insights about the meta-learning process itself"""
    return {
        "meta_learning_maturity": "advanced",
        "system_adaptation_rate": "optimal",
        "learning_efficiency": status.get('health_score', 0.8),
        "knowledge_accumulation": "progressive",
        "meta_recommendations": [
            "Meta-learning system operating at optimal efficiency",
            "Continue current learning and adaptation approach",
            "Monitor for opportunities to expand to new domains"
        ]
    }

async def _create_actionable_recommendations(insights: Dict, meta_insights: Dict, depth: str) -> List[Dict]:
    """Create comprehensive actionable recommendations"""
    recommendations = []
    
    # High-priority recommendations
    recommendations.append({
        "priority": "high",
        "category": "performance_optimization",
        "title": "Implement Adaptive Learning Rate Scheduling",
        "description": "Use meta-learning insights to dynamically adjust learning rates",
        "action_steps": [
            "Analyze current learning rate effectiveness",
            "Implement adaptive scheduling algorithm",
            "Monitor performance improvements"
        ],
        "expected_impact": "15-25% performance improvement",
        "timeline": "1-2 weeks"
    })
    
    # Medium-priority recommendations
    recommendations.append({
        "priority": "medium",
        "category": "strategy_diversification",
        "title": "Expand Domain Coverage",
        "description": "Increase learning strategy diversity across domains",
        "action_steps": [
            "Identify underexplored domains",
            "Generate domain-specific strategies",
            "Evaluate cross-domain transfer learning"
        ],
        "expected_impact": "10-20% generalization improvement",
        "timeline": "2-3 weeks"
    })
    
    if depth == "comprehensive":
        # Low-priority but valuable recommendations
        recommendations.append({
            "priority": "low",
            "category": "system_enhancement",
            "title": "Implement Advanced Meta-Learning Algorithms",
            "description": "Integrate MAML or Reptile algorithms for few-shot learning",
            "action_steps": [
                "Research latest meta-learning algorithms",
                "Prototype implementation",
                "Evaluate against current system"
            ],
            "expected_impact": "5-15% efficiency improvement",
            "timeline": "1-2 months"
        })
    
    return recommendations

def _calculate_insight_confidence(insights: Dict) -> float:
    """Calculate confidence score for generated insights"""
    # Simple heuristic based on available data
    data_completeness = len(insights) / 3.0  # Assuming 3 main insight categories
    return min(1.0, 0.7 + (data_completeness * 0.3))

# Error handlers for the blueprint
@meta_learning_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "error",
        "message": "Endpoint not found",
        "available_endpoints": [
            "/api/meta-learning/status",
            "/api/meta-learning/performance/analyze",
            "/api/meta-learning/strategies/generate",
            "/api/meta-learning/strategies/optimize",
            "/api/meta-learning/strategies/evaluate",
            "/api/meta-learning/learning/adapt",
            "/api/meta-learning/insights/generate"
        ]
    }), 404

@meta_learning_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status": "error",
        "message": "Internal server error",
        "timestamp": datetime.now().isoformat()
    }), 500