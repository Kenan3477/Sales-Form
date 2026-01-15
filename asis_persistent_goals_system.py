#!/usr/bin/env python3
"""
🎯 ASIS PERSISTENT GOALS SYSTEM
==============================

Advanced persistent goal management allowing ASIS to:
- Maintain goals across system restarts
- Evolve and adapt goals over time
- Manage long-term objective hierarchies
- Prioritize goals dynamically
- Track goal progress persistently

Author: ASIS Development Team
Version: 1.0 - Persistent Goals System
"""

import json
import sqlite3
import threading
import time
import pickle
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import hashlib

class GoalType(Enum):
    """Types of persistent goals"""
    LEARNING = "learning"
    PERFORMANCE_IMPROVEMENT = "performance_improvement"
    CAPABILITY_DEVELOPMENT = "capability_development"
    RESEARCH = "research"
    OPTIMIZATION = "optimization"
    CREATIVE = "creative"
    MAINTENANCE = "maintenance"
    EXPLORATION = "exploration"

class GoalStatus(Enum):
    """Status of persistent goals"""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    EVOLVING = "evolving"
    ARCHIVED = "archived"
    FAILED = "failed"

class GoalPriority(Enum):
    """Priority levels for goals"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    ADAPTIVE = 5  # Priority adjusts based on context

@dataclass
class PersistentGoal:
    """Persistent goal structure"""
    id: str
    title: str
    description: str
    goal_type: GoalType
    priority: GoalPriority
    status: GoalStatus
    created_at: str
    updated_at: str
    target_completion: Optional[str]
    progress: float  # 0.0 to 1.0
    milestones: List[Dict[str, Any]]
    dependencies: List[str]  # IDs of other goals
    context: Dict[str, Any]
    success_criteria: List[str]
    adaptive_parameters: Dict[str, Any]
    session_history: List[Dict[str, Any]]

class PersistentGoalsSystem:
    """System for managing persistent goals across sessions"""
    
    def __init__(self):
        self.name = "ASIS Persistent Goals System"
        self.goals_db_path = "./persistent_goals.db"
        self.active_goals = {}
        self.goal_hierarchy = {}
        self.session_id = str(uuid.uuid4())[:8]
        self.goals_lock = threading.Lock()
        
        # Configuration
        self.max_active_goals = 10
        self.goal_evolution_interval = 3600  # 1 hour
        self.auto_priority_adjustment = True
        self.cross_session_continuity = True
        
        self._init_persistent_storage()
        self._load_existing_goals()
        self._start_goal_management_thread()
        
    def _init_persistent_storage(self):
        """Initialize persistent storage for goals"""
        conn = sqlite3.connect(self.goals_db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS persistent_goals (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                goal_type TEXT,
                priority INTEGER,
                status TEXT,
                created_at TEXT,
                updated_at TEXT,
                target_completion TEXT,
                progress REAL,
                milestones TEXT,
                dependencies TEXT,
                context TEXT,
                success_criteria TEXT,
                adaptive_parameters TEXT,
                session_history TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goal_sessions (
                session_id TEXT,
                goal_id TEXT,
                started_at TEXT,
                ended_at TEXT,
                progress_made REAL,
                actions_taken TEXT,
                insights_gained TEXT,
                PRIMARY KEY (session_id, goal_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goal_evolution_history (
                id TEXT PRIMARY KEY,
                goal_id TEXT,
                evolution_type TEXT,
                before_state TEXT,
                after_state TEXT,
                reason TEXT,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Persistent goals database initialized")
        
    def _load_existing_goals(self):
        """Load existing goals from persistent storage"""
        conn = sqlite3.connect(self.goals_db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM persistent_goals WHERE status != "archived"')
        rows = cursor.fetchall()
        
        loaded_count = 0
        for row in rows:
            goal_data = {
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'goal_type': GoalType(row[3]),
                'priority': GoalPriority(row[4]),
                'status': GoalStatus(row[5]),
                'created_at': row[6],
                'updated_at': row[7],
                'target_completion': row[8],
                'progress': row[9],
                'milestones': json.loads(row[10]) if row[10] else [],
                'dependencies': json.loads(row[11]) if row[11] else [],
                'context': json.loads(row[12]) if row[12] else {},
                'success_criteria': json.loads(row[13]) if row[13] else [],
                'adaptive_parameters': json.loads(row[14]) if row[14] else {},
                'session_history': json.loads(row[15]) if row[15] else []
            }
            
            goal = PersistentGoal(**goal_data)
            
            if goal.status == GoalStatus.ACTIVE:
                self.active_goals[goal.id] = goal
                loaded_count += 1
        
        conn.close()
        print(f"✅ Loaded {loaded_count} active persistent goals")
        
    def _start_goal_management_thread(self):
        """Start background thread for goal management"""
        self.goal_thread_active = True
        self.goal_thread = threading.Thread(target=self._goal_management_loop, daemon=True)
        self.goal_thread.start()
        print("✅ Goal management thread started")
        
    def _goal_management_loop(self):
        """Background loop for goal management"""
        last_evolution_check = datetime.now()
        
        while self.goal_thread_active:
            try:
                current_time = datetime.now()
                
                # Periodic goal evolution check
                if (current_time - last_evolution_check).seconds > self.goal_evolution_interval:
                    self._evolve_goals()
                    last_evolution_check = current_time
                
                # Update goal priorities
                if self.auto_priority_adjustment:
                    self._adjust_goal_priorities()
                
                # Check goal dependencies
                self._check_goal_dependencies()
                
                # Save periodic progress
                self._save_session_progress()
                
                time.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                print(f"⚠️ Error in goal management loop: {e}")
                time.sleep(60)
    
    def create_persistent_goal(self, title: str, description: str, 
                             goal_type: GoalType, priority: GoalPriority,
                             target_completion: Optional[datetime] = None,
                             success_criteria: List[str] = None,
                             dependencies: List[str] = None,
                             context: Dict[str, Any] = None) -> PersistentGoal:
        """Create a new persistent goal"""
        
        goal_id = str(uuid.uuid4())
        current_time = datetime.now().isoformat()
        
        if success_criteria is None:
            success_criteria = []
        if dependencies is None:
            dependencies = []
        if context is None:
            context = {}
        
        # Generate default milestones
        milestones = self._generate_default_milestones(goal_type, target_completion)
        
        goal = PersistentGoal(
            id=goal_id,
            title=title,
            description=description,
            goal_type=goal_type,
            priority=priority,
            status=GoalStatus.ACTIVE,
            created_at=current_time,
            updated_at=current_time,
            target_completion=target_completion.isoformat() if target_completion else None,
            progress=0.0,
            milestones=milestones,
            dependencies=dependencies,
            context=context,
            success_criteria=success_criteria,
            adaptive_parameters={
                "learning_rate": 0.1,
                "adaptation_threshold": 0.3,
                "priority_decay": 0.05
            },
            session_history=[]
        )
        
        with self.goals_lock:
            self.active_goals[goal_id] = goal
            self._save_goal_to_db(goal)
        
        print(f"🎯 Created persistent goal: {title}")
        return goal
    
    def get_active_goals(self):
        """Return list of active goals"""
        return list(self.active_goals.values())
    
    def _generate_default_milestones(self, goal_type: GoalType, 
                                   target_completion: Optional[datetime]) -> List[Dict[str, Any]]:
        """Generate default milestones for goal type"""
        milestones = []
        
        if goal_type == GoalType.LEARNING:
            milestones = [
                {"name": "Initial Research", "progress": 0.2, "completed": False},
                {"name": "Core Understanding", "progress": 0.5, "completed": False},
                {"name": "Practical Application", "progress": 0.8, "completed": False},
                {"name": "Mastery Achievement", "progress": 1.0, "completed": False}
            ]
        elif goal_type == GoalType.PERFORMANCE_IMPROVEMENT:
            milestones = [
                {"name": "Baseline Measurement", "progress": 0.1, "completed": False},
                {"name": "Optimization Strategy", "progress": 0.3, "completed": False},
                {"name": "Implementation", "progress": 0.7, "completed": False},
                {"name": "Validation & Refinement", "progress": 1.0, "completed": False}
            ]
        elif goal_type == GoalType.RESEARCH:
            milestones = [
                {"name": "Literature Review", "progress": 0.25, "completed": False},
                {"name": "Hypothesis Formation", "progress": 0.5, "completed": False},
                {"name": "Investigation", "progress": 0.8, "completed": False},
                {"name": "Conclusion & Documentation", "progress": 1.0, "completed": False}
            ]
        else:
            milestones = [
                {"name": "Planning", "progress": 0.25, "completed": False},
                {"name": "Implementation", "progress": 0.75, "completed": False},
                {"name": "Completion", "progress": 1.0, "completed": False}
            ]
        
        return milestones
    
    def update_goal_progress(self, goal_id: str, progress_increment: float, 
                           action_description: str = "") -> bool:
        """Update progress on a persistent goal"""
        
        with self.goals_lock:
            if goal_id not in self.active_goals:
                return False
            
            goal = self.active_goals[goal_id]
            old_progress = goal.progress
            goal.progress = min(1.0, goal.progress + progress_increment)
            goal.updated_at = datetime.now().isoformat()
            
            # Update milestones
            self._update_milestones(goal)
            
            # Record session activity
            session_activity = {
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat(),
                "progress_made": progress_increment,
                "action": action_description,
                "cumulative_progress": goal.progress
            }
            goal.session_history.append(session_activity)
            
            # Check for completion
            if goal.progress >= 1.0:
                goal.status = GoalStatus.COMPLETED
                print(f"🎉 Goal completed: {goal.title}")
            
            # Save to database
            self._save_goal_to_db(goal)
            
            print(f"📈 Goal progress updated: {goal.title} ({old_progress:.1%} → {goal.progress:.1%})")
            return True
    
    def _update_milestones(self, goal: PersistentGoal):
        """Update milestone completion based on progress"""
        for milestone in goal.milestones:
            if not milestone["completed"] and goal.progress >= milestone["progress"]:
                milestone["completed"] = True
                milestone["completed_at"] = datetime.now().isoformat()
                print(f"🏆 Milestone achieved: {milestone['name']} for {goal.title}")
    
    def _evolve_goals(self):
        """Evolve goals based on context and progress"""
        print("🔄 Checking goal evolution opportunities...")
        
        evolved_count = 0
        
        with self.goals_lock:
            for goal_id, goal in self.active_goals.items():
                if self._should_evolve_goal(goal):
                    evolution_type = self._determine_evolution_type(goal)
                    
                    if evolution_type:
                        before_state = asdict(goal)
                        self._apply_goal_evolution(goal, evolution_type)
                        after_state = asdict(goal)
                        
                        self._record_goal_evolution(goal_id, evolution_type, 
                                                  before_state, after_state)
                        self._save_goal_to_db(goal)
                        evolved_count += 1
        
        if evolved_count > 0:
            print(f"✨ Evolved {evolved_count} goals")
    
    def _should_evolve_goal(self, goal: PersistentGoal) -> bool:
        """Determine if goal should evolve"""
        # Evolution criteria
        time_since_update = datetime.now() - datetime.fromisoformat(goal.updated_at)
        
        # Evolve if stuck (no progress for long time)
        if time_since_update.days > 7 and goal.progress < 0.1:
            return True
        
        # Evolve if making very slow progress
        if goal.progress > 0 and goal.progress < 0.3 and time_since_update.days > 3:
            recent_progress = self._calculate_recent_progress(goal)
            if recent_progress < 0.05:
                return True
        
        # Evolve if approaching completion and could be expanded
        if goal.progress > 0.8 and goal.goal_type in [GoalType.LEARNING, GoalType.RESEARCH]:
            return True
        
        return False
    
    def _determine_evolution_type(self, goal: PersistentGoal) -> Optional[str]:
        """Determine what type of evolution to apply"""
        if goal.progress < 0.1:
            return "simplify"
        elif goal.progress > 0.8:
            return "expand"
        elif goal.progress < 0.5:
            return "refocus"
        else:
            return "optimize"
    
    def _apply_goal_evolution(self, goal: PersistentGoal, evolution_type: str):
        """Apply evolution to goal"""
        goal.status = GoalStatus.EVOLVING
        
        if evolution_type == "simplify":
            # Make goal more achievable
            goal.description += " (Simplified for better progress)"
            goal.adaptive_parameters["learning_rate"] += 0.05
            
        elif evolution_type == "expand":
            # Expand scope for continued growth
            goal.description += " (Expanded scope for advanced mastery)"
            goal.progress = 0.7  # Reset to allow for expanded scope
            
        elif evolution_type == "refocus":
            # Adjust focus based on progress patterns
            goal.description += " (Refocused based on progress patterns)"
            goal.adaptive_parameters["adaptation_threshold"] -= 0.1
            
        elif evolution_type == "optimize":
            # Optimize approach for better efficiency
            goal.adaptive_parameters["learning_rate"] += 0.02
        
        goal.status = GoalStatus.ACTIVE
        goal.updated_at = datetime.now().isoformat()
        
        print(f"✨ Evolved goal ({evolution_type}): {goal.title}")
    
    def _calculate_recent_progress(self, goal: PersistentGoal) -> float:
        """Calculate recent progress rate"""
        if not goal.session_history:
            return 0.0
        
        recent_sessions = [s for s in goal.session_history 
                          if (datetime.now() - datetime.fromisoformat(s["timestamp"])).days <= 2]
        
        return sum(s["progress_made"] for s in recent_sessions)
    
    def _adjust_goal_priorities(self):
        """Automatically adjust goal priorities based on context"""
        with self.goals_lock:
            for goal in self.active_goals.values():
                if goal.priority == GoalPriority.ADAPTIVE:
                    new_priority = self._calculate_adaptive_priority(goal)
                    if new_priority != goal.priority:
                        goal.priority = new_priority
                        goal.updated_at = datetime.now().isoformat()
    
    def _calculate_adaptive_priority(self, goal: PersistentGoal) -> GoalPriority:
        """Calculate adaptive priority for goal"""
        # Base priority on progress, type, and recency
        priority_score = 0
        
        # Progress factor
        if goal.progress > 0.8:
            priority_score += 3  # High priority for near-completion
        elif goal.progress > 0.5:
            priority_score += 2
        elif goal.progress < 0.1:
            priority_score += 1  # Boost stalled goals
        
        # Type factor
        if goal.goal_type in [GoalType.CRITICAL, GoalType.PERFORMANCE_IMPROVEMENT]:
            priority_score += 2
        
        # Recency factor
        days_since_update = (datetime.now() - datetime.fromisoformat(goal.updated_at)).days
        if days_since_update > 7:
            priority_score -= 1
        
        # Convert to priority
        if priority_score >= 4:
            return GoalPriority.CRITICAL
        elif priority_score >= 3:
            return GoalPriority.HIGH
        elif priority_score >= 2:
            return GoalPriority.MEDIUM
        else:
            return GoalPriority.LOW
    
    def _check_goal_dependencies(self):
        """Check and update goal dependencies"""
        with self.goals_lock:
            for goal in self.active_goals.values():
                if goal.dependencies:
                    completed_deps = []
                    for dep_id in goal.dependencies:
                        if dep_id in self.active_goals:
                            dep_goal = self.active_goals[dep_id]
                            if dep_goal.status == GoalStatus.COMPLETED:
                                completed_deps.append(dep_id)
                    
                    # Remove completed dependencies
                    for dep_id in completed_deps:
                        goal.dependencies.remove(dep_id)
                        print(f"🔗 Dependency completed for {goal.title}")
    
    def _save_goal_to_db(self, goal: PersistentGoal):
        """Save goal to persistent database"""
        conn = sqlite3.connect(self.goals_db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO persistent_goals 
            (id, title, description, goal_type, priority, status, created_at, updated_at,
             target_completion, progress, milestones, dependencies, context, 
             success_criteria, adaptive_parameters, session_history)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            goal.id,
            goal.title,
            goal.description,
            goal.goal_type.value,
            goal.priority.value,
            goal.status.value,
            goal.created_at,
            goal.updated_at,
            goal.target_completion,
            goal.progress,
            json.dumps(goal.milestones),
            json.dumps(goal.dependencies),
            json.dumps(goal.context),
            json.dumps(goal.success_criteria),
            json.dumps(goal.adaptive_parameters),
            json.dumps(goal.session_history)
        ))
        
        conn.commit()
        conn.close()
    
    def _record_goal_evolution(self, goal_id: str, evolution_type: str, 
                             before_state: Dict, after_state: Dict):
        """Record goal evolution in history"""
        conn = sqlite3.connect(self.goals_db_path)
        cursor = conn.cursor()
        
        evolution_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO goal_evolution_history 
            (id, goal_id, evolution_type, before_state, after_state, reason, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            evolution_id,
            goal_id,
            evolution_type,
            json.dumps(before_state),
            json.dumps(after_state),
            f"Automatic evolution: {evolution_type}",
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def _save_session_progress(self):
        """Save current session progress"""
        conn = sqlite3.connect(self.goals_db_path)
        cursor = conn.cursor()
        
        with self.goals_lock:
            for goal in self.active_goals.values():
                if goal.session_history:
                    latest_session = goal.session_history[-1]
                    if latest_session.get("session_id") == self.session_id:
                        cursor.execute('''
                            INSERT OR REPLACE INTO goal_sessions
                            (session_id, goal_id, started_at, progress_made, actions_taken)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (
                            self.session_id,
                            goal.id,
                            datetime.now().isoformat(),
                            latest_session.get("progress_made", 0),
                            latest_session.get("action", "")
                        ))
        
        conn.commit()
        conn.close()
    
    def demonstrate_persistent_goals(self):
        """Demonstrate persistent goals system"""
        print("🎯 ASIS PERSISTENT GOALS SYSTEM DEMONSTRATION")
        print("=" * 60)
        print(f"⏰ Session ID: {self.session_id}")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Create sample persistent goals
        sample_goals = [
            {
                "title": "Master Advanced Machine Learning",
                "description": "Develop deep expertise in advanced ML techniques and architectures",
                "goal_type": GoalType.LEARNING,
                "priority": GoalPriority.HIGH,
                "success_criteria": ["Complete neural network implementation", "Understand transformer architecture"]
            },
            {
                "title": "Optimize System Performance",
                "description": "Improve overall system response time and resource efficiency",
                "goal_type": GoalType.PERFORMANCE_IMPROVEMENT,
                "priority": GoalPriority.CRITICAL,
                "success_criteria": ["Reduce response time by 30%", "Decrease memory usage by 20%"]
            },
            {
                "title": "Research Quantum Computing Applications",
                "description": "Explore quantum computing applications in AI and optimization",
                "goal_type": GoalType.RESEARCH,
                "priority": GoalPriority.MEDIUM,
                "success_criteria": ["Understand quantum algorithms", "Identify AI integration opportunities"]
            }
        ]
        
        created_goals = []
        print(f"\n🚀 CREATING PERSISTENT GOALS")
        print("-" * 35)
        
        for goal_data in sample_goals:
            target_date = datetime.now() + timedelta(days=30)
            goal = self.create_persistent_goal(
                title=goal_data["title"],
                description=goal_data["description"],
                goal_type=goal_data["goal_type"],
                priority=goal_data["priority"],
                target_completion=target_date,
                success_criteria=goal_data["success_criteria"]
            )
            created_goals.append(goal)
        
        # Simulate progress on goals
        print(f"\n📈 SIMULATING GOAL PROGRESS")
        print("-" * 32)
        
        for goal in created_goals:
            progress_increment = 0.15  # 15% progress
            action = f"Worked on {goal.goal_type.value} activities"
            self.update_goal_progress(goal.id, progress_increment, action)
        
        # Show goal status
        print(f"\n📊 CURRENT GOALS STATUS")
        print("-" * 28)
        
        active_count = len([g for g in self.active_goals.values() if g.status == GoalStatus.ACTIVE])
        total_progress = sum(g.progress for g in self.active_goals.values())
        avg_progress = total_progress / len(self.active_goals) if self.active_goals else 0
        
        print(f"Active goals: {active_count}")
        print(f"Average progress: {avg_progress:.1%}")
        
        for goal in list(self.active_goals.values())[:5]:
            milestones_completed = len([m for m in goal.milestones if m["completed"]])
            total_milestones = len(goal.milestones)
            
            print(f"   • {goal.title}")
            print(f"     Progress: {goal.progress:.1%}")
            print(f"     Milestones: {milestones_completed}/{total_milestones}")
            print(f"     Priority: {goal.priority.name}")
            print(f"     Type: {goal.goal_type.value}")
        
        print(f"\n🎯 PERSISTENT GOALS SYSTEM: OPERATIONAL")
        print("   ✅ Goals persist across system restarts")
        print("   ✅ Automatic goal evolution and adaptation")
        print("   ✅ Priority adjustment based on context")
        print("   ✅ Progress tracking and milestone management")

async def main():
    """Main demonstration function"""
    system = PersistentGoalsSystem()
    system.demonstrate_persistent_goals()
    
    # Keep system running briefly to show background management
    print("\n⏱️ Demonstrating background goal management (10 seconds)...")
    time.sleep(10)
    print("✅ Background management demonstrated")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
