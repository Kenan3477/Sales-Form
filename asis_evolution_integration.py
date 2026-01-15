import asyncio
import json
from typing import Dict, List, Any
from flask import request, jsonify
import time

# Import the evolution framework
try:
    from asis_evolution_framework import ASISEvolutionFramework, ImprovementOpportunity
    EVOLUTION_AVAILABLE = True
except ImportError:
    EVOLUTION_AVAILABLE = False
    print("⚠️ Evolution framework not available")

class ASISEvolutionIntegration:
    def __init__(self):
        if EVOLUTION_AVAILABLE:
            self.evolution_framework = ASISEvolutionFramework()
            self.auto_evolution_enabled = False
            self.evolution_schedule = {
                'interval': 3600,  # 1 hour
                'last_run': 0,
                'max_improvements_per_cycle': 2
            }
        else:
            self.evolution_framework = None
        
        # Evolution metrics
        self.evolution_metrics = {
            'total_cycles': 0,
            'successful_improvements': 0,
            'failed_improvements': 0,
            'last_evolution': None,
            'framework_status': 'active' if EVOLUTION_AVAILABLE else 'unavailable'
        }
    
    async def get_system_capabilities(self) -> Dict[str, Any]:
        """Get current system capabilities analysis"""
        if not self.evolution_framework:
            return {'error': 'Evolution framework not available'}
        
        try:
            capabilities = await self.evolution_framework.analyze_own_capabilities()
            return {
                'status': 'success',
                'capabilities': capabilities,
                'analysis_timestamp': time.time()
            }
        except Exception as e:
            return {'error': f'Capability analysis failed: {str(e)}'}
    
    async def get_improvement_opportunities(self) -> Dict[str, Any]:
        """Get identified improvement opportunities"""
        if not self.evolution_framework:
            return {'error': 'Evolution framework not available'}
        
        try:
            opportunities = await self.evolution_framework.identify_improvement_opportunities()
            
            # Convert to serializable format
            opportunities_data = []
            for opp in opportunities:
                opportunities_data.append({
                    'capability': opp.capability,
                    'current_score': opp.current_score,
                    'target_score': opp.target_score,
                    'improvement_type': opp.improvement_type,
                    'estimated_impact': opp.estimated_impact,
                    'implementation_difficulty': opp.implementation_difficulty,
                    'safety_risk': opp.safety_risk
                })
            
            return {
                'status': 'success',
                'opportunities': opportunities_data,
                'count': len(opportunities_data),
                'analysis_timestamp': time.time()
            }
        except Exception as e:
            return {'error': f'Opportunity identification failed: {str(e)}'}
    
    async def trigger_evolution_cycle(self, max_improvements: int = 2) -> Dict[str, Any]:
        """Manually trigger an evolution cycle"""
        if not self.evolution_framework:
            return {'error': 'Evolution framework not available'}
        
        try:
            print(f"🧬 Triggering manual evolution cycle (max {max_improvements} improvements)")
            
            evolution_results = await self.evolution_framework.evolve_system(max_improvements)
            
            # Update metrics
            self.evolution_metrics['total_cycles'] += 1
            self.evolution_metrics['successful_improvements'] += evolution_results.get('improvements_successful', 0)
            self.evolution_metrics['failed_improvements'] += (
                evolution_results.get('improvements_attempted', 0) - 
                evolution_results.get('improvements_successful', 0)
            )
            self.evolution_metrics['last_evolution'] = time.time()
            
            return {
                'status': 'success',
                'evolution_results': evolution_results,
                'updated_metrics': self.evolution_metrics
            }
            
        except Exception as e:
            return {'error': f'Evolution cycle failed: {str(e)}'}
    
    async def test_specific_improvement(self, improvement_data: Dict) -> Dict[str, Any]:
        """Test a specific improvement without deploying"""
        if not self.evolution_framework:
            return {'error': 'Evolution framework not available'}
        
        try:
            # Create ImprovementOpportunity from data
            improvement = ImprovementOpportunity(
                capability=improvement_data.get('capability', 'test_improvement'),
                current_score=improvement_data.get('current_score', 0.0),
                target_score=improvement_data.get('target_score', 80.0),
                improvement_type=improvement_data.get('improvement_type', 'optimize'),
                estimated_impact=improvement_data.get('estimated_impact', 0.5),
                implementation_difficulty=improvement_data.get('implementation_difficulty', 'medium'),
                safety_risk=improvement_data.get('safety_risk', 'low')
            )
            
            # Generate and test code
            code = await self.evolution_framework.generate_enhancement_code(improvement)
            test_results = await self.evolution_framework.test_enhancement(code, improvement)
            
            return {
                'status': 'success',
                'improvement': improvement_data,
                'generated_code_length': len(code),
                'test_results': test_results,
                'ready_for_deployment': test_results.get('success', False)
            }
            
        except Exception as e:
            return {'error': f'Improvement testing failed: {str(e)}'}
    
    async def deploy_tested_improvement(self, improvement_data: Dict, force_deploy: bool = False) -> Dict[str, Any]:
        """Deploy a tested improvement"""
        if not self.evolution_framework:
            return {'error': 'Evolution framework not available'}
        
        try:
            # First test the improvement
            test_result = await self.test_specific_improvement(improvement_data)
            
            if test_result.get('error'):
                return test_result
            
            if not test_result.get('ready_for_deployment') and not force_deploy:
                return {
                    'status': 'failed',
                    'reason': 'Improvement failed safety tests',
                    'test_results': test_result.get('test_results')
                }
            
            # Create improvement object and generate code
            improvement = ImprovementOpportunity(
                capability=improvement_data.get('capability', 'manual_improvement'),
                current_score=improvement_data.get('current_score', 0.0),
                target_score=improvement_data.get('target_score', 80.0),
                improvement_type=improvement_data.get('improvement_type', 'optimize'),
                estimated_impact=improvement_data.get('estimated_impact', 0.5),
                implementation_difficulty=improvement_data.get('implementation_difficulty', 'medium'),
                safety_risk=improvement_data.get('safety_risk', 'low')
            )
            
            code = await self.evolution_framework.generate_enhancement_code(improvement)
            test_results = test_result.get('test_results', {})
            
            # Deploy the enhancement
            deployment_success = await self.evolution_framework.deploy_enhancement(code, test_results)
            
            if deployment_success:
                self.evolution_metrics['successful_improvements'] += 1
                return {
                    'status': 'success',
                    'deployed': True,
                    'improvement': improvement_data,
                    'deployment_timestamp': time.time()
                }
            else:
                self.evolution_metrics['failed_improvements'] += 1
                return {
                    'status': 'failed',
                    'deployed': False,
                    'reason': 'Deployment process failed'
                }
                
        except Exception as e:
            return {'error': f'Deployment failed: {str(e)}'}
    
    def get_evolution_status(self) -> Dict[str, Any]:
        """Get evolution framework status and metrics"""
        status = {
            'framework_available': EVOLUTION_AVAILABLE,
            'auto_evolution_enabled': getattr(self, 'auto_evolution_enabled', False),
            'evolution_metrics': self.evolution_metrics,
            'evolution_schedule': getattr(self, 'evolution_schedule', {}),
            'framework_status': self.evolution_framework.get_evolution_status() if self.evolution_framework else None
        }
        
        return status
    
    def enable_auto_evolution(self, interval: int = 3600, max_improvements: int = 2) -> Dict[str, Any]:
        """Enable automatic evolution cycles"""
        if not self.evolution_framework:
            return {'error': 'Evolution framework not available'}
        
        self.auto_evolution_enabled = True
        self.evolution_schedule['interval'] = interval
        self.evolution_schedule['max_improvements_per_cycle'] = max_improvements
        
        return {
            'status': 'enabled',
            'interval': interval,
            'max_improvements_per_cycle': max_improvements,
            'next_run': time.time() + interval
        }
    
    def disable_auto_evolution(self) -> Dict[str, Any]:
        """Disable automatic evolution cycles"""
        self.auto_evolution_enabled = False
        
        return {
            'status': 'disabled',
            'auto_evolution_enabled': False
        }
    
    async def check_auto_evolution(self) -> Dict[str, Any]:
        """Check if auto evolution should run"""
        if not self.auto_evolution_enabled or not self.evolution_framework:
            return {'should_run': False, 'reason': 'Auto evolution disabled'}
        
        current_time = time.time()
        last_run = self.evolution_schedule.get('last_run', 0)
        interval = self.evolution_schedule.get('interval', 3600)
        
        if current_time - last_run >= interval:
            # Run auto evolution
            max_improvements = self.evolution_schedule.get('max_improvements_per_cycle', 2)
            
            print(f"🤖 Running scheduled evolution cycle")
            evolution_result = await self.trigger_evolution_cycle(max_improvements)
            
            self.evolution_schedule['last_run'] = current_time
            
            return {
                'should_run': True,
                'executed': True,
                'result': evolution_result,
                'next_run': current_time + interval
            }
        
        return {
            'should_run': False,
            'reason': 'Not yet time for next cycle',
            'next_run': last_run + interval,
            'time_remaining': (last_run + interval) - current_time
        }

# Global evolution integration instance
asis_evolution = ASISEvolutionIntegration()

# Flask route handlers for ASIS integration
def register_evolution_routes(app):
    """Register evolution framework routes with Flask app"""
    
    @app.route('/api/evolution/status', methods=['GET'])
    def evolution_status():
        """Get evolution framework status"""
        return jsonify(asis_evolution.get_evolution_status())
    
    @app.route('/api/evolution/capabilities', methods=['GET'])
    async def get_capabilities():
        """Get system capabilities analysis"""
        result = await asis_evolution.get_system_capabilities()
        return jsonify(result)
    
    @app.route('/api/evolution/opportunities', methods=['GET'])
    async def get_opportunities():
        """Get improvement opportunities"""
        result = await asis_evolution.get_improvement_opportunities()
        return jsonify(result)
    
    @app.route('/api/evolution/evolve', methods=['POST'])
    async def trigger_evolution():
        """Trigger manual evolution cycle"""
        data = request.get_json() or {}
        max_improvements = data.get('max_improvements', 2)
        
        result = await asis_evolution.trigger_evolution_cycle(max_improvements)
        return jsonify(result)
    
    @app.route('/api/evolution/test', methods=['POST'])
    async def test_improvement():
        """Test a specific improvement"""
        improvement_data = request.get_json()
        if not improvement_data:
            return jsonify({'error': 'No improvement data provided'}), 400
        
        result = await asis_evolution.test_specific_improvement(improvement_data)
        return jsonify(result)
    
    @app.route('/api/evolution/deploy', methods=['POST'])
    async def deploy_improvement():
        """Deploy a tested improvement"""
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No improvement data provided'}), 400
        
        improvement_data = data.get('improvement', {})
        force_deploy = data.get('force_deploy', False)
        
        result = await asis_evolution.deploy_tested_improvement(improvement_data, force_deploy)
        return jsonify(result)
    
    @app.route('/api/evolution/auto/enable', methods=['POST'])
    def enable_auto_evolution():
        """Enable automatic evolution"""
        data = request.get_json() or {}
        interval = data.get('interval', 3600)
        max_improvements = data.get('max_improvements', 2)
        
        result = asis_evolution.enable_auto_evolution(interval, max_improvements)
        return jsonify(result)
    
    @app.route('/api/evolution/auto/disable', methods=['POST'])
    def disable_auto_evolution():
        """Disable automatic evolution"""
        result = asis_evolution.disable_auto_evolution()
        return jsonify(result)
    
    print("✅ Evolution framework routes registered")

# Background task for auto evolution
async def evolution_background_task():
    """Background task to check for scheduled evolution"""
    while True:
        try:
            await asis_evolution.check_auto_evolution()
            await asyncio.sleep(300)  # Check every 5 minutes
        except Exception as e:
            print(f"⚠️ Evolution background task error: {str(e)}")
            await asyncio.sleep(300)

# Test function
async def test_evolution_integration():
    """Test the evolution integration"""
    print("🧪 Testing Evolution Integration...")
    
    # Test status
    status = asis_evolution.get_evolution_status()
    print(f"✅ Evolution status: {status['framework_available']}")
    
    # Test capabilities analysis
    capabilities = await asis_evolution.get_system_capabilities()
    print(f"✅ Capabilities analysis: {capabilities.get('status', 'failed')}")
    
    # Test opportunity identification
    opportunities = await asis_evolution.get_improvement_opportunities()
    print(f"✅ Opportunities found: {opportunities.get('count', 0)}")
    
    return asis_evolution

if __name__ == "__main__":
    asyncio.run(test_evolution_integration())