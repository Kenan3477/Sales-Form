import asyncio
import json
from typing import Dict, List, Any, Optional
from flask import request, jsonify
import time
import threading

# Import the autonomous agency
try:
    from asis_autonomous_agency import ASISAutonomousAgency, Goal, GoalType, Priority
    AGENCY_AVAILABLE = True
except ImportError:
    AGENCY_AVAILABLE = False
    print("⚠️ Autonomous agency not available")

class ASISAutonomousIntegration:
    def __init__(self):
        if AGENCY_AVAILABLE:
            self.autonomous_agency = ASISAutonomousAgency()
            self.auto_agency_enabled = False
            self.agency_schedule = {
                'interval': 7200,  # 2 hours
                'last_run': 0,
                'max_goals_per_cycle': 3
            }
        else:
            self.autonomous_agency = None
        
        # Agency metrics and history
        self.agency_history = []
        self.performance_tracking = {
            'total_autonomous_cycles': 0,
            'successful_cycles': 0,
            'total_goals_achieved': 0,
            'total_decisions_made': 0,
            'average_cycle_duration': 0.0,
            'last_cycle_performance': None
        }
    
    async def get_agency_status(self) -> Dict[str, Any]:
        """Get comprehensive autonomous agency status"""
        if not self.autonomous_agency:
            return {'error': 'Autonomous agency not available'}
        
        try:
            status = self.autonomous_agency.get_agency_status()
            
            return {
                'status': 'success',
                'agency_available': True,
                'auto_mode_enabled': self.auto_agency_enabled,
                'agency_metrics': status['agency_metrics'],
                'active_goals': status['active_goals'],
                'active_plans': status['active_plans'],
                'resource_status': status['resource_status'],
                'agency_health': status['agency_health'],
                'performance_tracking': self.performance_tracking,
                'schedule': self.agency_schedule,
                'timestamp': time.time()
            }
        except Exception as e:
            return {'error': f'Agency status check failed: {str(e)}'}
    
    async def generate_goals(self, goal_count: int = 5) -> Dict[str, Any]:
        """Generate meaningful goals for ASIS"""
        if not self.autonomous_agency:
            return {'error': 'Autonomous agency not available'}
        
        try:
            goals = await self.autonomous_agency.generate_meaningful_goals()
            
            # Convert goals to serializable format
            goals_data = []
            for goal in goals[:goal_count]:
                goals_data.append({
                    'id': goal.id,
                    'title': goal.title,
                    'description': goal.description,
                    'goal_type': goal.goal_type.value,
                    'priority': goal.priority.value,
                    'success_criteria': goal.success_criteria,
                    'estimated_duration': goal.estimated_duration,
                    'created_at': goal.created_at,
                    'context': goal.context
                })
            
            return {
                'status': 'success',
                'goals': goals_data,
                'count': len(goals_data),
                'generation_timestamp': time.time()
            }
        except Exception as e:
            return {'error': f'Goal generation failed: {str(e)}'}
    
    async def execute_specific_goal(self, goal_data: Dict) -> Dict[str, Any]:
        """Execute a specific goal autonomously"""
        if not self.autonomous_agency:
            return {'error': 'Autonomous agency not available'}
        
        try:
            # Create Goal object from data
            goal = Goal(
                id=goal_data.get('id', f"manual_{int(time.time())}"),
                title=goal_data.get('title', 'Manual Goal'),
                description=goal_data.get('description', 'Manually specified goal'),
                goal_type=GoalType(goal_data.get('goal_type', 'enhancement')),
                priority=Priority(goal_data.get('priority', 2)),
                success_criteria=goal_data.get('success_criteria', ['Complete goal successfully']),
                estimated_duration=goal_data.get('estimated_duration', 1800),
                created_at=time.time(),
                context=goal_data.get('context', {})
            )
            
            print(f"🎯 Executing specific goal: {goal.title}")
            
            # Plan the goal
            plan = await self.autonomous_agency.plan_goal_achievement(goal)
            
            # Allocate resources
            allocation = await self.autonomous_agency.allocate_resources(plan)
            
            if not allocation['success']:
                return {
                    'status': 'failed',
                    'reason': 'Resource allocation failed',
                    'allocation_result': allocation
                }
            
            # Execute autonomously
            execution_result = await self.autonomous_agency.execute_autonomously(plan, allocation)
            
            # Learn from results
            learning_result = await self.autonomous_agency.evaluate_and_learn(goal, execution_result)
            
            # Release resources
            await self.autonomous_agency.resource_manager.release_resources(plan['plan_id'])
            
            return {
                'status': 'success',
                'goal': goal_data,
                'plan_id': plan['plan_id'],
                'execution_result': execution_result,
                'learning_result': learning_result,
                'execution_timestamp': time.time()
            }
            
        except Exception as e:
            return {'error': f'Goal execution failed: {str(e)}'}
    
    async def run_autonomous_cycle(self, max_goals: int = 3) -> Dict[str, Any]:
        """Run a complete autonomous agency cycle"""
        if not self.autonomous_agency:
            return {'error': 'Autonomous agency not available'}
        
        try:
            print(f"🤖 Starting autonomous cycle with max {max_goals} goals")
            
            cycle_result = await self.autonomous_agency.autonomous_cycle(max_goals)
            
            # Update performance tracking
            self.performance_tracking['total_autonomous_cycles'] += 1
            
            if cycle_result.get('success_rate', 0) > 0.5:
                self.performance_tracking['successful_cycles'] += 1
            
            self.performance_tracking['total_goals_achieved'] += cycle_result.get('successful_goals', 0)
            self.performance_tracking['total_decisions_made'] += cycle_result.get('total_decisions', 0)
            
            # Update average cycle duration
            if cycle_result.get('duration'):
                current_avg = self.performance_tracking['average_cycle_duration']
                total_cycles = self.performance_tracking['total_autonomous_cycles']
                new_avg = ((current_avg * (total_cycles - 1)) + cycle_result['duration']) / total_cycles
                self.performance_tracking['average_cycle_duration'] = new_avg
            
            self.performance_tracking['last_cycle_performance'] = {
                'success_rate': cycle_result.get('success_rate', 0),
                'goals_processed': cycle_result.get('goals_processed', 0),
                'duration': cycle_result.get('duration', 0),
                'timestamp': time.time()
            }
            
            # Store in history
            self.agency_history.append(cycle_result)
            
            # Keep only last 10 cycles in history
            if len(self.agency_history) > 10:
                self.agency_history = self.agency_history[-10:]
            
            return {
                'status': 'success',
                'cycle_result': cycle_result,
                'updated_metrics': self.performance_tracking
            }
            
        except Exception as e:
            return {'error': f'Autonomous cycle failed: {str(e)}'}
    
    async def enable_auto_agency(self, interval: int = 7200, max_goals: int = 3) -> Dict[str, Any]:
        """Enable automatic autonomous cycles"""
        if not self.autonomous_agency:
            return {'error': 'Autonomous agency not available'}
        
        self.auto_agency_enabled = True
        self.agency_schedule['interval'] = interval
        self.agency_schedule['max_goals_per_cycle'] = max_goals
        
        return {
            'status': 'enabled',
            'auto_agency_enabled': True,
            'interval': interval,
            'max_goals_per_cycle': max_goals,
            'next_run': time.time() + interval
        }
    
    async def disable_auto_agency(self) -> Dict[str, Any]:
        """Disable automatic autonomous cycles"""
        self.auto_agency_enabled = False
        
        return {
            'status': 'disabled',
            'auto_agency_enabled': False
        }
    
    async def get_goal_recommendations(self) -> Dict[str, Any]:
        """Get AI-recommended goals based on current state"""
        if not self.autonomous_agency:
            return {'error': 'Autonomous agency not available'}
        
        try:
            # Get current system state
            current_state = await self.autonomous_agency.evaluate_current_state()
            
            # Generate recommended goals
            goals = await self.autonomous_agency.generate_meaningful_goals()
            
            # Create recommendations with reasoning
            recommendations = []
            for goal in goals[:5]:
                recommendation = {
                    'goal': {
                        'title': goal.title,
                        'description': goal.description,
                        'goal_type': goal.goal_type.value,
                        'priority': goal.priority.value,
                        'estimated_duration': goal.estimated_duration
                    },
                    'reasoning': self._generate_goal_reasoning(goal, current_state),
                    'expected_benefits': self._generate_expected_benefits(goal),
                    'risk_assessment': self._assess_goal_risk(goal)
                }
                recommendations.append(recommendation)
            
            return {
                'status': 'success',
                'recommendations': recommendations,
                'current_state': current_state,
                'recommendation_timestamp': time.time()
            }
            
        except Exception as e:
            return {'error': f'Goal recommendation failed: {str(e)}'}
    
    def _generate_goal_reasoning(self, goal: Goal, current_state: Dict) -> str:
        """Generate reasoning for why this goal is recommended"""
        reasons = []
        
        if goal.goal_type == GoalType.OPTIMIZATION:
            system_health = current_state.get('system_health', 80)
            if system_health < 85:
                reasons.append(f"System health at {system_health:.1f}% indicates optimization opportunities")
            else:
                reasons.append("Proactive optimization to maintain high performance")
        
        elif goal.goal_type == GoalType.RESEARCH:
            reasons.append("Knowledge expansion to improve problem-solving capabilities")
        
        elif goal.goal_type == GoalType.MAINTENANCE:
            last_maintenance = current_state.get('last_maintenance', 0)
            hours_since = (time.time() - last_maintenance) / 3600
            if hours_since > 24:
                reasons.append(f"Maintenance overdue by {hours_since - 24:.1f} hours")
            else:
                reasons.append("Preventive maintenance to ensure system reliability")
        
        elif goal.goal_type == GoalType.ENHANCEMENT:
            reasons.append("Capability enhancement to expand functional range")
        
        elif goal.goal_type == GoalType.USER_SERVICE:
            user_requests = current_state.get('user_requests', 0)
            if user_requests > 0:
                reasons.append(f"{user_requests} pending user requests require attention")
            else:
                reasons.append("Proactive user experience improvement")
        
        return "; ".join(reasons) if reasons else "Strategic goal for overall system improvement"
    
    def _generate_expected_benefits(self, goal: Goal) -> List[str]:
        """Generate expected benefits from achieving this goal"""
        benefits = []
        
        if goal.goal_type == GoalType.OPTIMIZATION:
            benefits.extend([
                "Improved system performance and response times",
                "Reduced resource consumption",
                "Enhanced user experience"
            ])
        elif goal.goal_type == GoalType.RESEARCH:
            benefits.extend([
                "Expanded knowledge base",
                "Better problem-solving capabilities",
                "Improved decision-making accuracy"
            ])
        elif goal.goal_type == GoalType.MAINTENANCE:
            benefits.extend([
                "Increased system reliability",
                "Prevention of potential issues",
                "Optimized resource utilization"
            ])
        elif goal.goal_type == GoalType.ENHANCEMENT:
            benefits.extend([
                "New or improved capabilities",
                "Increased functional versatility",
                "Better service delivery"
            ])
        elif goal.goal_type == GoalType.USER_SERVICE:
            benefits.extend([
                "Improved user satisfaction",
                "Faster response to user needs",
                "Enhanced service quality"
            ])
        
        return benefits
    
    def _assess_goal_risk(self, goal: Goal) -> Dict[str, Any]:
        """Assess risk level for achieving this goal"""
        risk_factors = []
        risk_level = "low"
        
        # Assess based on goal type
        if goal.goal_type in [GoalType.OPTIMIZATION, GoalType.ENHANCEMENT]:
            risk_level = "medium"
            risk_factors.append("Implementation complexity")
        
        # Assess based on duration
        if goal.estimated_duration > 3600:  # > 1 hour
            risk_factors.append("Extended execution time")
            if risk_level == "low":
                risk_level = "medium"
        
        # Assess based on priority
        if goal.priority == Priority.CRITICAL:
            risk_factors.append("High priority pressure")
        
        return {
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'mitigation_strategies': [
                "Incremental implementation",
                "Resource monitoring",
                "Rollback planning"
            ]
        }
    
    async def check_auto_agency(self) -> Dict[str, Any]:
        """Check if auto agency should run and execute if needed"""
        if not self.auto_agency_enabled or not self.autonomous_agency:
            return {'should_run': False, 'reason': 'Auto agency disabled'}
        
        current_time = time.time()
        last_run = self.agency_schedule.get('last_run', 0)
        interval = self.agency_schedule.get('interval', 7200)
        
        if current_time - last_run >= interval:
            # Run auto agency cycle
            max_goals = self.agency_schedule.get('max_goals_per_cycle', 3)
            
            print(f"🤖 Running scheduled autonomous agency cycle")
            cycle_result = await self.run_autonomous_cycle(max_goals)
            
            self.agency_schedule['last_run'] = current_time
            
            return {
                'should_run': True,
                'executed': True,
                'result': cycle_result,
                'next_run': current_time + interval
            }
        
        return {
            'should_run': False,
            'reason': 'Not yet time for next cycle',
            'next_run': last_run + interval,
            'time_remaining': (last_run + interval) - current_time
        }
    
    def get_agency_history(self) -> Dict[str, Any]:
        """Get autonomous agency execution history"""
        return {
            'total_cycles': len(self.agency_history),
            'recent_cycles': self.agency_history[-5:] if self.agency_history else [],
            'performance_summary': self.performance_tracking,
            'success_rate': (
                self.performance_tracking['successful_cycles'] / 
                max(self.performance_tracking['total_autonomous_cycles'], 1)
            )
        }

# Global autonomous integration instance
asis_autonomous = ASISAutonomousIntegration()

# Flask route handlers for ASIS integration
def register_autonomous_routes(app):
    """Register autonomous agency routes with Flask app"""
    
    @app.route('/api/autonomous/status', methods=['GET'])
    async def autonomous_status():
        """Get autonomous agency status"""
        result = await asis_autonomous.get_agency_status()
        return jsonify(result)
    
    @app.route('/api/autonomous/goals/generate', methods=['POST'])
    async def generate_goals():
        """Generate meaningful goals"""
        data = request.get_json() or {}
        goal_count = data.get('count', 5)
        
        result = await asis_autonomous.generate_goals(goal_count)
        return jsonify(result)
    
    @app.route('/api/autonomous/goals/recommendations', methods=['GET'])
    async def get_goal_recommendations():
        """Get AI-recommended goals"""
        result = await asis_autonomous.get_goal_recommendations()
        return jsonify(result)
    
    @app.route('/api/autonomous/goals/execute', methods=['POST'])
    async def execute_goal():
        """Execute a specific goal"""
        goal_data = request.get_json()
        if not goal_data:
            return jsonify({'error': 'No goal data provided'}), 400
        
        result = await asis_autonomous.execute_specific_goal(goal_data)
        return jsonify(result)
    
    @app.route('/api/autonomous/cycle/run', methods=['POST'])
    async def run_autonomous_cycle():
        """Run autonomous agency cycle"""
        data = request.get_json() or {}
        max_goals = data.get('max_goals', 3)
        
        result = await asis_autonomous.run_autonomous_cycle(max_goals)
        return jsonify(result)
    
    @app.route('/api/autonomous/auto/enable', methods=['POST'])
    async def enable_auto_agency():
        """Enable automatic autonomous cycles"""
        data = request.get_json() or {}
        interval = data.get('interval', 7200)
        max_goals = data.get('max_goals', 3)
        
        result = await asis_autonomous.enable_auto_agency(interval, max_goals)
        return jsonify(result)
    
    @app.route('/api/autonomous/auto/disable', methods=['POST'])
    async def disable_auto_agency():
        """Disable automatic autonomous cycles"""
        result = await asis_autonomous.disable_auto_agency()
        return jsonify(result)
    
    @app.route('/api/autonomous/history', methods=['GET'])
    def get_agency_history():
        """Get autonomous agency history"""
        result = asis_autonomous.get_agency_history()
        return jsonify(result)
    
    print("✅ Autonomous agency routes registered")

# Background task for auto agency
async def autonomous_background_task():
    """Background task to check for scheduled autonomous cycles"""
    while True:
        try:
            await asis_autonomous.check_auto_agency()
            await asyncio.sleep(600)  # Check every 10 minutes
        except Exception as e:
            print(f"⚠️ Autonomous background task error: {str(e)}")
            await asyncio.sleep(600)

# Test function
async def test_autonomous_integration():
    """Test the autonomous integration"""
    print("🧪 Testing Autonomous Integration...")
    
    # Test status
    status = await asis_autonomous.get_agency_status()
    print(f"✅ Agency status: {status.get('agency_available', False)}")
    
    # Test goal generation
    goals = await asis_autonomous.generate_goals(3)
    print(f"✅ Goals generated: {goals.get('count', 0)}")
    
    # Test recommendations
    recommendations = await asis_autonomous.get_goal_recommendations()
    print(f"✅ Recommendations: {len(recommendations.get('recommendations', []))}")
    
    return asis_autonomous

if __name__ == "__main__":
    asyncio.run(test_autonomous_integration())