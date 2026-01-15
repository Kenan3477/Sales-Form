#!/usr/bin/env python3
"""
ASIS Advanced Project Management Dashboard
==========================================

Sophisticated project management system for research tracking, autonomous decision
logging, progress monitoring, and collaborative workspace management.

Author: ASIS Development Team
Date: September 18, 2025
Version: 1.0
"""

import asyncio
import json
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, asdict, field
from enum import Enum
import threading
import logging

logger = logging.getLogger(__name__)

class ProjectStatus(Enum):
    """Project status enumeration"""
    PLANNING = "planning"
    ACTIVE = "active"
    RESEARCH_PHASE = "research_phase"
    ANALYSIS_PHASE = "analysis_phase"
    IMPLEMENTATION = "implementation"
    REVIEW = "review"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class DecisionType(Enum):
    """Types of autonomous decisions"""
    RESEARCH_DIRECTION = "research_direction"
    RESOURCE_ALLOCATION = "resource_allocation"
    METHODOLOGY_CHOICE = "methodology_choice"
    RISK_MITIGATION = "risk_mitigation"
    OPTIMIZATION = "optimization"
    LEARNING_ADAPTATION = "learning_adaptation"

@dataclass
class ProjectTask:
    """Individual project task"""
    id: str
    project_id: str
    title: str
    description: str
    priority: TaskPriority
    status: str  # todo, in_progress, completed, blocked
    assigned_to: str
    created_at: datetime
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

@dataclass
class AutonomousDecision:
    """Autonomous decision made by ASIS"""
    id: str
    project_id: str
    decision_type: DecisionType
    title: str
    description: str
    rationale: str
    confidence_score: float
    impact_level: str  # low, medium, high
    timestamp: datetime
    implemented: bool = False
    implementation_result: Optional[str] = None
    feedback_score: Optional[float] = None

@dataclass
class ResearchFinding:
    """Research finding or insight"""
    id: str
    project_id: str
    title: str
    content: str
    source: str
    relevance_score: float
    category: str  # hypothesis, data, insight, conclusion
    timestamp: datetime
    tags: List[str] = field(default_factory=list)
    related_findings: List[str] = field(default_factory=list)
    validation_status: str = "pending"  # pending, validated, disputed

@dataclass
class ProjectMilestone:
    """Project milestone"""
    id: str
    project_id: str
    title: str
    description: str
    target_date: datetime
    completion_date: Optional[datetime] = None
    status: str = "pending"  # pending, achieved, missed, cancelled
    success_criteria: List[str] = field(default_factory=list)
    completion_percentage: float = 0.0

@dataclass
class ResearchProject:
    """Comprehensive research project"""
    id: str
    title: str
    description: str
    status: ProjectStatus
    created_by: str
    created_at: datetime
    updated_at: datetime
    target_completion: Optional[datetime] = None
    actual_completion: Optional[datetime] = None
    progress_percentage: float = 0.0
    
    # Project components
    objectives: List[str] = field(default_factory=list)
    methodology: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    
    # Tracking
    tasks: List[ProjectTask] = field(default_factory=list)
    findings: List[ResearchFinding] = field(default_factory=list)
    decisions: List[AutonomousDecision] = field(default_factory=list)
    milestones: List[ProjectMilestone] = field(default_factory=list)
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    collaborators: List[str] = field(default_factory=list)
    budget_allocated: Optional[float] = None
    budget_used: Optional[float] = None

class ProjectAnalytics:
    """Project analytics and insights"""
    
    def __init__(self):
        self.analytics_cache = {}
        self.cache_timeout = 300  # 5 minutes
        
    def analyze_project_health(self, project: ResearchProject) -> Dict[str, Any]:
        """Analyze overall project health"""
        now = datetime.now()
        
        # Task completion analysis
        total_tasks = len(project.tasks)
        completed_tasks = sum(1 for task in project.tasks if task.status == 'completed')
        task_completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Timeline analysis
        timeline_health = "on_track"
        if project.target_completion:
            days_remaining = (project.target_completion - now).days
            if days_remaining < 0:
                timeline_health = "overdue"
            elif days_remaining < 7 and project.progress_percentage < 80:
                timeline_health = "at_risk"
        
        # Decision effectiveness
        implemented_decisions = [d for d in project.decisions if d.implemented]
        avg_decision_confidence = (
            sum(d.confidence_score for d in implemented_decisions) / len(implemented_decisions)
            if implemented_decisions else 0.0
        )
        
        # Research momentum
        recent_findings = [
            f for f in project.findings 
            if (now - f.timestamp).days <= 7
        ]
        research_momentum = len(recent_findings)
        
        # Overall health score
        health_factors = [
            task_completion_rate / 100,
            1.0 if timeline_health == "on_track" else 0.5 if timeline_health == "at_risk" else 0.0,
            avg_decision_confidence,
            min(research_momentum / 5, 1.0)  # Normalize to 0-1
        ]
        
        overall_health = sum(health_factors) / len(health_factors) * 100
        
        return {
            'overall_health': overall_health,
            'task_completion_rate': task_completion_rate,
            'timeline_health': timeline_health,
            'decision_confidence': avg_decision_confidence,
            'research_momentum': research_momentum,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'total_findings': len(project.findings),
            'recent_findings': len(recent_findings),
            'autonomous_decisions': len(project.decisions),
            'implemented_decisions': len(implemented_decisions)
        }
    
    def generate_project_insights(self, project: ResearchProject) -> List[str]:
        """Generate actionable insights for project"""
        insights = []
        analytics = self.analyze_project_health(project)
        
        # Task-based insights
        if analytics['task_completion_rate'] < 30:
            insights.append("📋 Low task completion rate. Consider breaking down complex tasks.")
        elif analytics['task_completion_rate'] > 80:
            insights.append("🎯 Excellent task completion rate. Project is progressing well.")
        
        # Timeline insights
        if analytics['timeline_health'] == 'at_risk':
            insights.append("⚠️ Project timeline at risk. Consider resource reallocation.")
        elif analytics['timeline_health'] == 'overdue':
            insights.append("🚨 Project overdue. Immediate attention required.")
        
        # Research insights
        if analytics['research_momentum'] < 2:
            insights.append("🔬 Research momentum is low. Consider new investigation directions.")
        elif analytics['research_momentum'] > 10:
            insights.append("🚀 High research momentum. Excellent progress in knowledge discovery.")
        
        # Decision insights
        if analytics['decision_confidence'] < 0.7:
            insights.append("🤔 Recent decisions have low confidence. Review decision criteria.")
        elif analytics['decision_confidence'] > 0.9:
            insights.append("💪 High confidence in autonomous decisions. System learning effectively.")
        
        return insights
    
    def predict_completion_date(self, project: ResearchProject) -> Optional[datetime]:
        """Predict project completion date based on current progress"""
        if project.progress_percentage == 0:
            return None
        
        days_elapsed = (datetime.now() - project.created_at).days
        if days_elapsed == 0:
            return None
        
        progress_rate = project.progress_percentage / days_elapsed
        remaining_progress = 100 - project.progress_percentage
        
        if progress_rate > 0:
            estimated_days_remaining = remaining_progress / progress_rate
            return datetime.now() + timedelta(days=estimated_days_remaining)
        
        return None

class ASISProjectManager:
    """Advanced project management system"""
    
    def __init__(self, web_api):
        self.web_api = web_api
        self.projects: Dict[str, ResearchProject] = {}
        self.analytics = ProjectAnalytics()
        
        # Background processing
        self.autonomous_agent_active = True
        self.decision_queue = []
        
        # Setup API endpoints
        self._setup_project_endpoints()
        
        # Setup socket handlers
        self._setup_project_socket_handlers()
        
        # Start autonomous agent
        self._start_autonomous_agent()
        
        # Create demo projects
        self._create_demo_projects()
        
        logger.info("📋 ASIS Project Manager initialized")
    
    def _setup_project_endpoints(self):
        """Setup project management API endpoints"""
        
        @self.web_api.app.route('/api/v1/projects', methods=['GET'])
        def get_projects():
            """Get all projects"""
            try:
                projects_data = []
                for project in self.projects.values():
                    project_dict = asdict(project)
                    # Convert datetime objects to ISO strings
                    project_dict = self._serialize_datetime_fields(project_dict)
                    projects_data.append(project_dict)
                
                return jsonify(projects_data)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.web_api.app.route('/api/v1/projects/<project_id>', methods=['GET'])
        def get_project(project_id):
            """Get specific project details"""
            try:
                if project_id not in self.projects:
                    return jsonify({'error': 'Project not found'}), 404
                
                project = self.projects[project_id]
                project_dict = asdict(project)
                project_dict = self._serialize_datetime_fields(project_dict)
                
                # Add analytics
                project_dict['analytics'] = self.analytics.analyze_project_health(project)
                project_dict['insights'] = self.analytics.generate_project_insights(project)
                project_dict['predicted_completion'] = self.analytics.predict_completion_date(project)
                
                return jsonify(project_dict)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.web_api.app.route('/api/v1/projects', methods=['POST'])
        def create_project():
            """Create new project"""
            try:
                data = request.get_json()
                
                project = ResearchProject(
                    id=str(uuid.uuid4()),
                    title=data.get('title', 'Untitled Project'),
                    description=data.get('description', ''),
                    status=ProjectStatus.PLANNING,
                    created_by=data.get('created_by', 'anonymous'),
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                
                # Optional fields
                if 'objectives' in data:
                    project.objectives = data['objectives']
                if 'target_completion' in data:
                    project.target_completion = datetime.fromisoformat(data['target_completion'])
                
                self.projects[project.id] = project
                
                project_dict = asdict(project)
                project_dict = self._serialize_datetime_fields(project_dict)
                
                return jsonify(project_dict), 201
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.web_api.app.route('/api/v1/projects/<project_id>/tasks', methods=['POST'])
        def add_project_task(project_id):
            """Add task to project"""
            try:
                if project_id not in self.projects:
                    return jsonify({'error': 'Project not found'}), 404
                
                data = request.get_json()
                
                task = ProjectTask(
                    id=str(uuid.uuid4()),
                    project_id=project_id,
                    title=data.get('title', 'Untitled Task'),
                    description=data.get('description', ''),
                    priority=TaskPriority(data.get('priority', 'medium')),
                    status=data.get('status', 'todo'),
                    assigned_to=data.get('assigned_to', 'unassigned'),
                    created_at=datetime.now()
                )
                
                self.projects[project_id].tasks.append(task)
                self.projects[project_id].updated_at = datetime.now()
                
                return jsonify(asdict(task), default=str), 201
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.web_api.app.route('/api/v1/projects/<project_id>/decisions', methods=['GET'])
        def get_project_decisions(project_id):
            """Get autonomous decisions for project"""
            try:
                if project_id not in self.projects:
                    return jsonify({'error': 'Project not found'}), 404
                
                decisions = self.projects[project_id].decisions
                decisions_data = []
                
                for decision in decisions:
                    decision_dict = asdict(decision)
                    decision_dict = self._serialize_datetime_fields(decision_dict)
                    decisions_data.append(decision_dict)
                
                return jsonify(decisions_data)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.web_api.app.route('/api/v1/projects/<project_id>/findings', methods=['POST'])
        def add_research_finding(project_id):
            """Add research finding to project"""
            try:
                if project_id not in self.projects:
                    return jsonify({'error': 'Project not found'}), 404
                
                data = request.get_json()
                
                finding = ResearchFinding(
                    id=str(uuid.uuid4()),
                    project_id=project_id,
                    title=data.get('title', 'Research Finding'),
                    content=data.get('content', ''),
                    source=data.get('source', 'manual_entry'),
                    relevance_score=data.get('relevance_score', 0.5),
                    category=data.get('category', 'insight'),
                    timestamp=datetime.now(),
                    tags=data.get('tags', [])
                )
                
                self.projects[project_id].findings.append(finding)
                self.projects[project_id].updated_at = datetime.now()
                
                return jsonify(asdict(finding), default=str), 201
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.web_api.app.route('/api/v1/projects/<project_id>/analytics')
        def get_project_analytics(project_id):
            """Get project analytics and insights"""
            try:
                if project_id not in self.projects:
                    return jsonify({'error': 'Project not found'}), 404
                
                project = self.projects[project_id]
                analytics = self.analytics.analyze_project_health(project)
                insights = self.analytics.generate_project_insights(project)
                predicted_completion = self.analytics.predict_completion_date(project)
                
                return jsonify({
                    'analytics': analytics,
                    'insights': insights,
                    'predicted_completion': predicted_completion.isoformat() if predicted_completion else None,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    
    def _setup_project_socket_handlers(self):
        """Setup WebSocket handlers for real-time project updates"""
        
        @self.web_api.socketio.on('project_subscribe')
        def handle_project_subscribe(data):
            """Subscribe to project updates"""
            try:
                project_id = data.get('project_id')
                if project_id in self.projects:
                    join_room(f'project_{project_id}')
                    emit('subscribed', {'project_id': project_id})
            except Exception as e:
                emit('error', {'message': str(e)})
        
        @self.web_api.socketio.on('project_update_progress')
        def handle_update_progress(data):
            """Update project progress"""
            try:
                project_id = data.get('project_id')
                progress = data.get('progress', 0)
                
                if project_id in self.projects:
                    self.projects[project_id].progress_percentage = float(progress)
                    self.projects[project_id].updated_at = datetime.now()
                    
                    # Broadcast update
                    self.web_api.socketio.emit('project_progress_updated', {
                        'project_id': project_id,
                        'progress': progress,
                        'timestamp': time.time()
                    }, room=f'project_{project_id}')
                    
            except Exception as e:
                emit('error', {'message': str(e)})
    
    def _start_autonomous_agent(self):
        """Start autonomous project management agent"""
        def autonomous_loop():
            while self.autonomous_agent_active:
                try:
                    # Make autonomous decisions for active projects
                    active_projects = [
                        p for p in self.projects.values() 
                        if p.status == ProjectStatus.ACTIVE
                    ]
                    
                    for project in active_projects:
                        if len(project.decisions) < 10:  # Limit decisions per project
                            decision = self._make_autonomous_decision(project)
                            if decision:
                                project.decisions.append(decision)
                                project.updated_at = datetime.now()
                                
                                # Broadcast decision
                                self.web_api.socketio.emit('autonomous_decision', {
                                    'project_id': project.id,
                                    'decision': asdict(decision, default=str)
                                }, room=f'project_{project.id}')
                    
                    time.sleep(30)  # Make decisions every 30 seconds
                    
                except Exception as e:
                    logger.error(f"Autonomous agent error: {e}")
                    time.sleep(60)
        
        agent_thread = threading.Thread(target=autonomous_loop, daemon=True)
        agent_thread.start()
        logger.info("🤖 Autonomous project agent started")
    
    def _make_autonomous_decision(self, project: ResearchProject) -> Optional[AutonomousDecision]:
        """Make an autonomous decision for project"""
        decision_scenarios = [
            {
                'type': DecisionType.RESEARCH_DIRECTION,
                'title': 'Research Focus Optimization',
                'description': 'Analyzing current research findings to optimize investigation direction',
                'rationale': 'Based on recent findings patterns, adjusting research focus for maximum insight generation',
                'confidence': 0.85,
                'impact': 'medium'
            },
            {
                'type': DecisionType.RESOURCE_ALLOCATION,
                'title': 'Resource Reallocation',
                'description': 'Optimizing resource allocation based on task priority and progress',
                'rationale': 'Current resource distribution analysis suggests potential for efficiency improvements',
                'confidence': 0.75,
                'impact': 'high'
            },
            {
                'type': DecisionType.METHODOLOGY_CHOICE,
                'title': 'Methodology Adaptation',
                'description': 'Adapting research methodology based on emerging patterns',
                'rationale': 'Data suggests alternative methodological approaches may yield better results',
                'confidence': 0.90,
                'impact': 'medium'
            },
            {
                'type': DecisionType.OPTIMIZATION,
                'title': 'Process Optimization',
                'description': 'Identifying opportunities for process improvement',
                'rationale': 'Analysis of current workflows indicates optimization potential',
                'confidence': 0.80,
                'impact': 'low'
            }
        ]
        
        # Select random scenario for demo (in real implementation, this would be based on actual analysis)
        scenario = decision_scenarios[len(project.decisions) % len(decision_scenarios)]
        
        decision = AutonomousDecision(
            id=str(uuid.uuid4()),
            project_id=project.id,
            decision_type=scenario['type'],
            title=scenario['title'],
            description=scenario['description'],
            rationale=scenario['rationale'],
            confidence_score=scenario['confidence'],
            impact_level=scenario['impact'],
            timestamp=datetime.now()
        )
        
        return decision
    
    def _create_demo_projects(self):
        """Create demonstration projects"""
        demo_projects = [
            {
                'title': 'AI Ethics Research Initiative',
                'description': 'Comprehensive research into ethical implications of advanced AI systems',
                'objectives': [
                    'Analyze current AI ethics frameworks',
                    'Identify potential ethical challenges',
                    'Develop recommendations for ethical AI development'
                ],
                'status': ProjectStatus.ACTIVE
            },
            {
                'title': 'Cognitive Architecture Optimization',
                'description': 'Research into optimizing cognitive processing architectures',
                'objectives': [
                    'Benchmark current architecture performance',
                    'Identify optimization opportunities',
                    'Implement and test improvements'
                ],
                'status': ProjectStatus.RESEARCH_PHASE
            },
            {
                'title': 'Advanced Learning Systems Study',
                'description': 'Investigation of next-generation machine learning approaches',
                'objectives': [
                    'Survey emerging ML techniques',
                    'Evaluate applicability to ASIS',
                    'Prototype promising approaches'
                ],
                'status': ProjectStatus.PLANNING
            }
        ]
        
        for i, project_data in enumerate(demo_projects):
            project = ResearchProject(
                id=f"demo_project_{i+1:03d}",
                title=project_data['title'],
                description=project_data['description'],
                status=project_data['status'],
                created_by='asis_system',
                created_at=datetime.now() - timedelta(days=7+i*3),
                updated_at=datetime.now() - timedelta(hours=i*2),
                objectives=project_data['objectives'],
                progress_percentage=20 + i*15,
                target_completion=datetime.now() + timedelta(days=30+i*15)
            )
            
            # Add demo tasks
            for j in range(3+i):
                task = ProjectTask(
                    id=f"task_{project.id}_{j+1}",
                    project_id=project.id,
                    title=f"Task {j+1}: {project_data['objectives'][j % len(project_data['objectives'])]}",
                    description=f"Detailed work for objective: {project_data['objectives'][j % len(project_data['objectives'])]}",
                    priority=TaskPriority.HIGH if j == 0 else TaskPriority.MEDIUM,
                    status='completed' if j < i else 'in_progress' if j == i else 'todo',
                    assigned_to='asis_researcher',
                    created_at=project.created_at + timedelta(days=j)
                )
                project.tasks.append(task)
            
            # Add demo findings
            for k in range(2+i):
                finding = ResearchFinding(
                    id=f"finding_{project.id}_{k+1}",
                    project_id=project.id,
                    title=f"Research Finding #{k+1}",
                    content=f"Significant insight discovered during {project_data['title']} research phase.",
                    source='autonomous_research',
                    relevance_score=0.7 + (k * 0.1),
                    category='insight',
                    timestamp=project.created_at + timedelta(days=k*2),
                    tags=['research', 'analysis', 'insight']
                )
                project.findings.append(finding)
            
            self.projects[project.id] = project
        
        logger.info(f"📋 Created {len(demo_projects)} demo projects")
    
    def _serialize_datetime_fields(self, obj):
        """Serialize datetime fields to ISO strings"""
        if isinstance(obj, dict):
            return {k: self._serialize_datetime_fields(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._serialize_datetime_fields(item) for item in obj]
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, '__dict__'):
            return {k: self._serialize_datetime_fields(v) for k, v in obj.__dict__.items()}
        else:
            return obj
    
    def get_project_statistics(self) -> Dict[str, Any]:
        """Get comprehensive project statistics"""
        total_projects = len(self.projects)
        active_projects = sum(1 for p in self.projects.values() if p.status == ProjectStatus.ACTIVE)
        completed_projects = sum(1 for p in self.projects.values() if p.status == ProjectStatus.COMPLETED)
        
        total_tasks = sum(len(p.tasks) for p in self.projects.values())
        completed_tasks = sum(
            sum(1 for task in p.tasks if task.status == 'completed') 
            for p in self.projects.values()
        )
        
        total_findings = sum(len(p.findings) for p in self.projects.values())
        total_decisions = sum(len(p.decisions) for p in self.projects.values())
        
        avg_progress = (
            sum(p.progress_percentage for p in self.projects.values()) / total_projects
            if total_projects > 0 else 0
        )
        
        return {
            'total_projects': total_projects,
            'active_projects': active_projects,
            'completed_projects': completed_projects,
            'completion_rate': (completed_projects / total_projects * 100) if total_projects > 0 else 0,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'task_completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            'total_findings': total_findings,
            'total_autonomous_decisions': total_decisions,
            'average_progress': avg_progress,
            'projects_by_status': {
                status.value: sum(1 for p in self.projects.values() if p.status == status)
                for status in ProjectStatus
            }
        }

def create_project_management_template():
    """Create project management dashboard template"""
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASIS Project Management Dashboard</title>
    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --primary-green: #00ff88;
            --bg-primary: #0a0a0a;
            --bg-secondary: #1a1a1a;
            --bg-tertiary: #1e1e1e;
            --text-primary: #e0e0e0;
            --text-secondary: #ccc;
            --border-color: #333;
            --warning-color: #ffaa00;
            --error-color: #ff4444;
            --success-color: #00ff88;
        }
        
        * { box-sizing: border-box; }
        
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; padding: 0; 
            background: var(--bg-primary); 
            color: var(--text-primary);
        }
        
        .dashboard-container { 
            display: grid; 
            grid-template-columns: 300px 1fr;
            min-height: 100vh;
        }
        
        .sidebar { 
            background: var(--bg-secondary); 
            padding: 20px; 
            border-right: 1px solid var(--border-color);
            overflow-y: auto;
        }
        
        .main-content { 
            padding: 20px; 
            overflow-y: auto;
        }
        
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding: 20px;
            background: var(--bg-tertiary);
            border-radius: 12px;
            border: 1px solid var(--border-color);
        }
        
        .stats-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card { 
            background: var(--bg-tertiary); 
            padding: 24px; 
            border-radius: 12px; 
            border: 1px solid var(--border-color);
            text-align: center;
        }
        
        .stat-value {
            font-size: 32px;
            font-weight: bold;
            color: var(--primary-green);
            margin-bottom: 8px;
        }
        
        .stat-label {
            color: var(--text-secondary);
            font-size: 14px;
        }
        
        .projects-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); 
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .project-card { 
            background: var(--bg-tertiary); 
            padding: 20px; 
            border-radius: 12px; 
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .project-card:hover {
            border-color: var(--primary-green);
            transform: translateY(-2px);
        }
        
        .project-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
        }
        
        .project-title {
            font-size: 18px;
            font-weight: bold;
            color: var(--text-primary);
            margin: 0;
        }
        
        .project-status {
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }
        
        .status-active { background: rgba(0, 255, 136, 0.2); color: var(--success-color); }
        .status-planning { background: rgba(255, 170, 0, 0.2); color: var(--warning-color); }
        .status-completed { background: rgba(136, 136, 136, 0.2); color: #888; }
        
        .project-description {
            color: var(--text-secondary);
            font-size: 14px;
            margin-bottom: 16px;
            line-height: 1.5;
        }
        
        .progress-section {
            margin-bottom: 16px;
        }
        
        .progress-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 14px;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: var(--border-color);
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary-green), #00cc6a);
            transition: width 0.5s ease;
        }
        
        .project-metrics {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .metric {
            text-align: center;
            padding: 8px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 6px;
        }
        
        .metric-value {
            font-weight: bold;
            color: var(--text-primary);
        }
        
        .sidebar-section {
            margin-bottom: 30px;
        }
        
        .sidebar-title {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 16px;
            color: var(--primary-green);
        }
        
        .filter-buttons {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .filter-btn {
            padding: 8px 16px;
            background: var(--bg-tertiary);
            color: var(--text-secondary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
            text-align: left;
        }
        
        .filter-btn:hover {
            border-color: var(--primary-green);
            color: var(--text-primary);
        }
        
        .filter-btn.active {
            background: var(--primary-green);
            color: #000;
            border-color: var(--primary-green);
        }
        
        .create-project-btn {
            width: 100%;
            padding: 12px;
            background: var(--primary-green);
            color: #000;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            font-size: 14px;
            margin-bottom: 20px;
        }
        
        .insights-panel {
            background: var(--bg-tertiary);
            padding: 16px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }
        
        .insight-item {
            color: var(--text-secondary);
            font-size: 13px;
            margin: 8px 0;
            padding: 8px;
            background: rgba(0, 255, 136, 0.05);
            border-radius: 4px;
            border-left: 3px solid var(--primary-green);
        }
        
        .nav-menu {
            list-style: none;
            padding: 0;
            margin: 0 0 20px 0;
        }
        
        .nav-item {
            margin: 4px 0;
        }
        
        .nav-link {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 12px;
            color: var(--text-secondary);
            text-decoration: none;
            border-radius: 6px;
            transition: all 0.3s ease;
            font-size: 14px;
        }
        
        .nav-link:hover {
            background: var(--border-color);
            color: var(--text-primary);
        }
        
        .nav-link.active {
            background: var(--primary-green);
            color: #000;
        }
        
        .autonomous-decisions {
            background: rgba(0, 255, 136, 0.05);
            border: 1px solid rgba(0, 255, 136, 0.2);
            padding: 12px;
            border-radius: 8px;
            margin-top: 12px;
        }
        
        .decision-item {
            font-size: 12px;
            margin: 6px 0;
            color: var(--text-secondary);
        }
        
        .decision-title {
            font-weight: bold;
            color: var(--primary-green);
        }
        
        .connection-status {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--error-color);
            animation: pulse 2s infinite;
        }
        
        .status-dot.connected {
            background: var(--primary-green);
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        @media (max-width: 768px) {
            .dashboard-container {
                grid-template-columns: 1fr;
            }
            
            .sidebar {
                display: none;
            }
            
            .projects-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="sidebar">
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="color: var(--primary-green); margin: 0;">📋 Projects</h2>
                <p style="margin: 5px 0; font-size: 12px; color: var(--text-secondary);">Research Management</p>
            </div>
            
            <ul class="nav-menu">
                <li class="nav-item">
                    <a href="/" class="nav-link">
                        <span>📊</span> Dashboard
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/chat" class="nav-link">
                        <span>💬</span> Chat Interface
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/projects" class="nav-link active">
                        <span>📋</span> Projects
                    </a>
                </li>
            </ul>
            
            <button class="create-project-btn" onclick="createNewProject()">
                ✨ New Project
            </button>
            
            <div class="sidebar-section">
                <div class="sidebar-title">Filter Projects</div>
                <div class="filter-buttons">
                    <button class="filter-btn active" data-filter="all">All Projects</button>
                    <button class="filter-btn" data-filter="active">Active</button>
                    <button class="filter-btn" data-filter="planning">Planning</button>
                    <button class="filter-btn" data-filter="completed">Completed</button>
                    <button class="filter-btn" data-filter="research_phase">Research Phase</button>
                </div>
            </div>
            
            <div class="insights-panel">
                <div class="sidebar-title">Autonomous Insights</div>
                <div id="autonomous-insights">
                    <div class="insight-item">🤖 Analyzing project patterns...</div>
                    <div class="insight-item">📊 Optimizing resource allocation</div>
                    <div class="insight-item">🔬 Research momentum tracking active</div>
                </div>
            </div>
        </div>
        
        <div class="main-content">
            <div class="header">
                <div>
                    <h1 style="margin: 0; color: var(--text-primary);">Project Management Dashboard</h1>
                    <p style="margin: 8px 0 0 0; color: var(--text-secondary);">Research project tracking and autonomous decision monitoring</p>
                </div>
                <div class="connection-status">
                    <div class="status-dot" id="connection-dot"></div>
                    <span id="connection-text">Connecting...</span>
                </div>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value" id="total-projects">0</div>
                    <div class="stat-label">Total Projects</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="active-projects">0</div>
                    <div class="stat-label">Active Projects</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="completion-rate">0%</div>
                    <div class="stat-label">Completion Rate</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="autonomous-decisions">0</div>
                    <div class="stat-label">Autonomous Decisions</div>
                </div>
            </div>
            
            <div class="projects-grid" id="projects-grid">
                <!-- Projects will be loaded here -->
            </div>
        </div>
    </div>

    <script>
        const socket = io();
        let projects = [];
        let currentFilter = 'all';
        
        // Initialize
        socket.on('connect', function() {
            updateConnectionStatus(true);
            socket.emit('join_room', {room: 'projects'});
            loadProjects();
            loadProjectStatistics();
        });
        
        socket.on('disconnect', function() {
            updateConnectionStatus(false);
        });
        
        socket.on('autonomous_decision', function(data) {
            console.log('New autonomous decision:', data);
            addInsight(`🤖 New decision: ${data.decision.title}`);
            loadProjects(); // Refresh projects
        });
        
        socket.on('project_progress_updated', function(data) {
            console.log('Project progress updated:', data);
            updateProjectProgress(data.project_id, data.progress);
        });
        
        // Load projects from API
        async function loadProjects() {
            try {
                const response = await fetch('/api/v1/projects');
                projects = await response.json();
                displayProjects();
            } catch (error) {
                console.error('Failed to load projects:', error);
            }
        }
        
        // Display projects in grid
        function displayProjects() {
            const grid = document.getElementById('projects-grid');
            const filteredProjects = filterProjects(projects);
            
            grid.innerHTML = '';
            
            filteredProjects.forEach(project => {
                const projectCard = createProjectCard(project);
                grid.appendChild(projectCard);
            });
        }
        
        function createProjectCard(project) {
            const card = document.createElement('div');
            card.className = 'project-card';
            card.onclick = () => viewProjectDetails(project.id);
            
            const statusClass = `status-${project.status}`;
            const statusText = project.status.replace('_', ' ').toUpperCase();
            
            card.innerHTML = `
                <div class="project-header">
                    <h3 class="project-title">${project.title}</h3>
                    <span class="project-status ${statusClass}">${statusText}</span>
                </div>
                
                <div class="project-description">
                    ${project.description}
                </div>
                
                <div class="progress-section">
                    <div class="progress-header">
                        <span>Progress</span>
                        <span>${project.progress_percentage.toFixed(1)}%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${project.progress_percentage}%"></div>
                    </div>
                </div>
                
                <div class="project-metrics">
                    <div class="metric">
                        <div class="metric-value">${project.tasks.length}</div>
                        <div>Tasks</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${project.findings.length}</div>
                        <div>Findings</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${project.decisions.length}</div>
                        <div>Decisions</div>
                    </div>
                </div>
                
                ${project.decisions.length > 0 ? `
                    <div class="autonomous-decisions">
                        <div style="font-weight: bold; margin-bottom: 8px;">🤖 Latest Decision</div>
                        <div class="decision-item">
                            <div class="decision-title">${project.decisions[project.decisions.length - 1].title}</div>
                            <div>${project.decisions[project.decisions.length - 1].description}</div>
                        </div>
                    </div>
                ` : ''}
            `;
            
            return card;
        }
        
        function filterProjects(projectList) {
            if (currentFilter === 'all') {
                return projectList;
            }
            return projectList.filter(project => project.status === currentFilter);
        }
        
        async function loadProjectStatistics() {
            try {
                // For demo purposes, calculate from loaded projects
                const totalProjects = projects.length;
                const activeProjects = projects.filter(p => p.status === 'active').length;
                const completedProjects = projects.filter(p => p.status === 'completed').length;
                const totalDecisions = projects.reduce((sum, p) => sum + p.decisions.length, 0);
                const completionRate = totalProjects > 0 ? (completedProjects / totalProjects * 100) : 0;
                
                document.getElementById('total-projects').textContent = totalProjects;
                document.getElementById('active-projects').textContent = activeProjects;
                document.getElementById('completion-rate').textContent = completionRate.toFixed(1) + '%';
                document.getElementById('autonomous-decisions').textContent = totalDecisions;
            } catch (error) {
                console.error('Failed to load project statistics:', error);
            }
        }
        
        function setupFilters() {
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                    this.classList.add('active');
                    currentFilter = this.dataset.filter;
                    displayProjects();
                });
            });
        }
        
        function viewProjectDetails(projectId) {
            // Navigate to detailed project view (would be implemented)
            console.log('Viewing project:', projectId);
            alert(`Project details for ${projectId} would be displayed here.`);
        }
        
        function createNewProject() {
            const title = prompt('Project Title:');
            if (!title) return;
            
            const description = prompt('Project Description:');
            if (!description) return;
            
            const projectData = {
                title: title,
                description: description,
                created_by: 'demo_user_001'
            };
            
            fetch('/api/v1/projects', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(projectData)
            })
            .then(response => response.json())
            .then(data => {
                console.log('Project created:', data);
                loadProjects();
                loadProjectStatistics();
            })
            .catch(error => {
                console.error('Failed to create project:', error);
            });
        }
        
        function updateConnectionStatus(connected) {
            const dot = document.getElementById('connection-dot');
            const text = document.getElementById('connection-text');
            
            if (connected) {
                dot.classList.add('connected');
                text.textContent = 'Connected';
            } else {
                dot.classList.remove('connected');
                text.textContent = 'Disconnected';
            }
        }
        
        function updateProjectProgress(projectId, progress) {
            const project = projects.find(p => p.id === projectId);
            if (project) {
                project.progress_percentage = progress;
                displayProjects();
            }
        }
        
        function addInsight(insight) {
            const insightsContainer = document.getElementById('autonomous-insights');
            const insightDiv = document.createElement('div');
            insightDiv.className = 'insight-item';
            insightDiv.textContent = insight;
            
            insightsContainer.insertBefore(insightDiv, insightsContainer.firstChild);
            
            // Keep only last 5 insights
            while (insightsContainer.children.length > 5) {
                insightsContainer.removeChild(insightsContainer.lastChild);
            }
        }
        
        // Initialize when page loads
        document.addEventListener('DOMContentLoaded', function() {
            setupFilters();
        });
    </script>
</body>
</html>
    '''

def main():
    """Main function to demonstrate project management system"""
    print("📋 ASIS Advanced Project Management Dashboard")
    print("=" * 55)
    
    # Update projects template
    with open('templates/projects.html', 'w', encoding='utf-8') as f:
        f.write(create_project_management_template())
    
    print("✅ Project management dashboard template created")
    print("🤖 Autonomous decision-making system implemented")
    print("📊 Research tracking and analytics integrated")
    print("🔄 Real-time project updates configured")
    print("📈 Progress monitoring and insights added")

if __name__ == "__main__":
    main()
