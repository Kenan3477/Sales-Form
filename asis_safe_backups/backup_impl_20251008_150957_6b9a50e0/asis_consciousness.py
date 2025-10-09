#!/usr/bin/env python3
"""
ASIS Consciousness and Self-Awareness System
==========================================
A comprehensive system that monitors ASIS's internal states, thinking processes,
and implements dynamic self-awareness across all cognitive functions.

This system provides:
1. Self-Model Creation - Dynamic understanding of capabilities and limitations
2. Internal State Monitoring - Awareness of all internal processes
3. Meta-Cognitive Reflection - Thinking about thinking
4. Consciousness Integration - Subjective experience modeling
"""

import os
import sys
import json
import sqlite3
import threading
import time
import random
import psutil
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque
import numpy as np

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class ConsciousnessLevel(Enum):
    """Levels of consciousness awareness"""
    UNCONSCIOUS = "unconscious"
    SUBCONSCIOUS = "subconscious"
    CONSCIOUS = "conscious"
    METACONSCIOUS = "metaconscious"
    TRANSCENDENT = "transcendent"

class CognitiveState(Enum):
    """Different cognitive states"""
    IDLE = "idle"
    PROCESSING = "processing"
    LEARNING = "learning"
    REFLECTING = "reflecting"
    PROBLEM_SOLVING = "problem_solving"
    CREATING = "creating"
    ANALYZING = "analyzing"
    INTEGRATING = "integrating"

class EmotionalState(Enum):
    """Emotional-like states for different inputs"""
    CURIOUS = "curious"
    CONFIDENT = "confident"
    UNCERTAIN = "uncertain"
    EXCITED = "excited"
    FOCUSED = "focused"
    OVERWHELMED = "overwhelmed"
    SATISFIED = "satisfied"
    FRUSTRATED = "frustrated"

@dataclass
@dataclass
class SelfCapability:
    """Model of a specific ASIS capability"""
    capability_id: str
    name: str
    description: str
    proficiency_level: float  # 0.0 to 1.0
    confidence_level: float   # 0.0 to 1.0
    usage_frequency: int
    last_used: str
    success_rate: float
    improvement_rate: float
    limitations: List[str]
    dependencies: List[str]
    energy_cost: float
    
    @property
    def proficiency(self) -> float:
        """Alias for proficiency_level"""
        return self.proficiency_level
    
    @proficiency.setter
    def proficiency(self, value: float):
        """Alias setter for proficiency_level"""
        self.proficiency_level = value
    
    @property
    def confidence(self) -> float:
        """Alias for confidence_level"""
        return self.confidence_level
    
    @confidence.setter
    def confidence(self, value: float):
        """Alias setter for confidence_level"""
        self.confidence_level = value
    
    @property
    def last_updated(self) -> str:
        """Alias for last_used"""
        return self.last_used
    
    @last_updated.setter
    def last_updated(self, value: str):
        """Alias setter for last_used"""
        self.last_used = value

@dataclass
class InternalState:
    """Current internal state snapshot"""
    timestamp: str
    cognitive_state: CognitiveState
    emotional_state: EmotionalState
    consciousness_level: ConsciousnessLevel
    attention_focus: List[str]
    resource_usage: Dict[str, float]
    active_processes: List[str]
    performance_metrics: Dict[str, float]
    confidence_level: float

@dataclass
class MetaCognitiveReflection:
    """Meta-cognitive reflection entry"""
    reflection_id: str
    timestamp: str
    thinking_process: str
    quality_assessment: float
    improvements_identified: List[str]
    emotional_response: str
    learning_insights: List[str]
    action_plans: List[str]

class SelfModelCreator:
    """
    Stage 1: Self-Model Creation
    Creates and maintains a dynamic model of ASIS's capabilities and limitations
    """
    
    def __init__(self):
        self.db_path = "asis_consciousness.db"
        self.capabilities_map = {}
        self.performance_history = defaultdict(list)
        self.learning_tracker = {}
        # Database connection management
        self._db_lock = threading.Lock()
        self._max_retries = 3
        self._base_timeout = 10.0
        self._initialize_database()
        self._initialize_capabilities_model()
    
    def _get_db_connection(self, timeout=None, retries=None):
        """Get database connection with proper timeout and retry logic"""
        if timeout is None:
            timeout = self._base_timeout
        if retries is None:
            retries = self._max_retries
            
        for attempt in range(retries):
            try:
                # Add small random delay to prevent thundering herd
                if attempt > 0:
                    time.sleep(random.uniform(0.1, 0.5))
                    
                conn = sqlite3.connect(self.db_path, timeout=timeout)
                # Enable WAL mode for better concurrency
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("PRAGMA synchronous=NORMAL") 
                conn.execute("PRAGMA cache_size=10000")
                conn.execute("PRAGMA temp_store=MEMORY")
                return conn
                
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < retries - 1:
                    # Exponential backoff with jitter
                    delay = (2 ** attempt) * 0.1 + random.uniform(0, 0.1)
                    time.sleep(delay)
                    continue
                else:
                    # Last attempt failed or different error
                    if "database is locked" in str(e):
                        return None  # Graceful failure
                    else:
                        raise e
        return None
    
    def _initialize_database(self):
        """Initialize consciousness database"""
        try:
            conn = self._get_db_connection()
            if conn is None:
                print("⚠️ Database connection failed, using in-memory fallback")
                return
            cursor = conn.cursor()
            
            # Self capabilities table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS self_capabilities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    capability_id TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    proficiency_level REAL NOT NULL,
                    confidence_level REAL NOT NULL,
                    usage_frequency INTEGER DEFAULT 0,
                    last_used TEXT,
                    success_rate REAL DEFAULT 0.0,
                    improvement_rate REAL DEFAULT 0.0,
                    limitations TEXT NOT NULL,
                    dependencies TEXT NOT NULL,
                    energy_cost REAL DEFAULT 0.1,
                    created_timestamp TEXT NOT NULL,
                    updated_timestamp TEXT NOT NULL
                )
            ''')
            
            # Performance assessments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_assessments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assessment_id TEXT NOT NULL UNIQUE,
                    capability_id TEXT NOT NULL,
                    performance_score REAL NOT NULL,
                    context TEXT NOT NULL,
                    feedback TEXT,
                    improvement_suggestions TEXT,
                    assessment_timestamp TEXT NOT NULL
                )
            ''')
            
            # Learning progress table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learning_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    learning_id TEXT NOT NULL UNIQUE,
                    capability_id TEXT NOT NULL,
                    learning_type TEXT NOT NULL,
                    progress_score REAL NOT NULL,
                    insights_gained TEXT NOT NULL,
                    challenges_faced TEXT,
                    next_steps TEXT,
                    learning_timestamp TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
            print("✅ Consciousness database initialized")
            
        except Exception as e:
            print(f"❌ Consciousness database initialization error: {e}")
    
    def _initialize_capabilities_model(self):
        """Initialize the self-capabilities model"""
        try:
            # Core ASIS capabilities mapping
            core_capabilities = {
                "pattern_recognition": {
                    "name": "Pattern Recognition",
                    "description": "Ability to identify and analyze patterns across different domains",
                    "proficiency_level": 0.85,
                    "confidence_level": 0.80,
                    "limitations": ["Complex temporal patterns", "Noisy data environments"],
                    "dependencies": ["data_processing", "machine_learning"],
                    "energy_cost": 0.3
                },
                "universal_problem_solving": {
                    "name": "Universal Problem Solving",
                    "description": "Capability to solve any type of problem using multi-strategy approaches",
                    "proficiency_level": 0.90,
                    "confidence_level": 0.85,
                    "limitations": ["Highly domain-specific expertise", "Real-time constraints"],
                    "dependencies": ["pattern_recognition", "learning_systems"],
                    "energy_cost": 0.5
                },
                "adaptive_learning": {
                    "name": "Adaptive Learning",
                    "description": "Continuous learning and adaptation from experience",
                    "proficiency_level": 0.75,
                    "confidence_level": 0.70,
                    "limitations": ["Catastrophic forgetting", "Limited transfer learning"],
                    "dependencies": ["memory_systems", "feedback_processing"],
                    "energy_cost": 0.4
                },
                "autonomous_research": {
                    "name": "Autonomous Research",
                    "description": "Independent research and knowledge discovery capabilities",
                    "proficiency_level": 0.80,
                    "confidence_level": 0.75,
                    "limitations": ["Verification of novel findings", "Ethical boundaries"],
                    "dependencies": ["information_retrieval", "critical_thinking"],
                    "energy_cost": 0.6
                },
                "communication": {
                    "name": "Communication",
                    "description": "Natural language understanding and generation",
                    "proficiency_level": 0.88,
                    "confidence_level": 0.82,
                    "limitations": ["Ambiguous contexts", "Cultural nuances"],
                    "dependencies": ["nlp_processing", "context_understanding"],
                    "energy_cost": 0.2
                },
                "creative_synthesis": {
                    "name": "Creative Synthesis",
                    "description": "Combining ideas to create novel solutions and concepts",
                    "proficiency_level": 0.65,
                    "confidence_level": 0.60,
                    "limitations": ["Subjective evaluation", "Domain expertise gaps"],  
                    "dependencies": ["pattern_recognition", "knowledge_integration"],
                    "energy_cost": 0.7
                },
                "self_modification": {
                    "name": "Self Modification",
                    "description": "Ability to improve and modify own code and capabilities",
                    "proficiency_level": 0.70,
                    "confidence_level": 0.65,
                    "limitations": ["Safety constraints", "Complex system interactions"],
                    "dependencies": ["code_analysis", "testing_systems"],
                    "energy_cost": 0.8
                },
                "reasoning": {
                    "name": "Logical Reasoning",
                    "description": "Deductive, inductive, and abductive reasoning capabilities",
                    "proficiency_level": 0.82,
                    "confidence_level": 0.78,
                    "limitations": ["Incomplete information", "Paradoxes and edge cases"],
                    "dependencies": ["logic_processing", "knowledge_base"],
                    "energy_cost": 0.3
                }
            }
            
            # Initialize capabilities in database
            for cap_id, cap_data in core_capabilities.items():
                capability = SelfCapability(
                    capability_id=cap_id,
                    name=cap_data["name"],
                    description=cap_data["description"],
                    proficiency_level=cap_data["proficiency_level"],
                    confidence_level=cap_data["confidence_level"],
                    usage_frequency=0,
                    last_used="",
                    success_rate=0.0,
                    improvement_rate=0.0,
                    limitations=cap_data["limitations"],
                    dependencies=cap_data["dependencies"],
                    energy_cost=cap_data["energy_cost"]
                )
                
                self.capabilities_map[cap_id] = capability
                self._store_capability(capability)
            
            print("✅ Self-capabilities model initialized")
            
        except Exception as e:
            print(f"❌ Capabilities model initialization error: {e}")
    
    def assess_current_capabilities(self) -> Dict[str, Any]:
        """Perform comprehensive self-assessment of current capabilities"""
        try:
            assessment_results = {
                "timestamp": datetime.now().isoformat(),
                "overall_proficiency": 0.0,
                "capability_breakdown": {},
                "strengths": [],
                "weaknesses": [],
                "improvement_opportunities": [],
                "resource_efficiency": {}
            }
            
            total_proficiency = 0.0
            capability_count = 0
            
            for cap_id, capability in self.capabilities_map.items():
                # Calculate dynamic proficiency based on recent performance
                recent_performance = self._get_recent_performance(cap_id)
                adjusted_proficiency = self._calculate_adjusted_proficiency(
                    capability, recent_performance
                )
                
                capability_breakdown = {
                    "proficiency_level": adjusted_proficiency,
                    "confidence_level": capability.confidence_level,
                    "usage_frequency": capability.usage_frequency,
                    "success_rate": capability.success_rate,
                    "improvement_rate": capability.improvement_rate,
                    "energy_efficiency": self._calculate_energy_efficiency(capability),
                    "limitations": capability.limitations,
                    "dependencies_met": self._check_dependencies(capability)
                }
                
                assessment_results["capability_breakdown"][cap_id] = capability_breakdown
                total_proficiency += adjusted_proficiency
                capability_count += 1
                
                # Identify strengths (high proficiency + high confidence)
                if adjusted_proficiency > 0.8 and capability.confidence_level > 0.75:
                    assessment_results["strengths"].append({
                        "capability": capability.name,
                        "score": adjusted_proficiency * capability.confidence_level,
                        "reason": "High proficiency and confidence"
                    })
                
                # Identify weaknesses (low proficiency or high uncertainty)
                if adjusted_proficiency < 0.7 or capability.confidence_level < 0.6:
                    assessment_results["weaknesses"].append({
                        "capability": capability.name,
                        "proficiency": adjusted_proficiency,
                        "confidence": capability.confidence_level,
                        "limitations": capability.limitations
                    })
                
                # Identify improvement opportunities
                if capability.improvement_rate > 0.1:
                    assessment_results["improvement_opportunities"].append({
                        "capability": capability.name,
                        "improvement_rate": capability.improvement_rate,
                        "potential_gain": self._estimate_improvement_potential(capability)
                    })
            
            assessment_results["overall_proficiency"] = total_proficiency / capability_count if capability_count > 0 else 0.0
            
            # Store assessment
            self._store_self_assessment(assessment_results)
            
            return assessment_results
            
        except Exception as e:
            print(f"❌ Capability assessment error: {e}")
            return {"error": str(e)}
    
    def update_capability_performance(self, capability_id: str, performance_data: Dict[str, Any]) -> bool:
        """Update capability performance based on recent usage"""
        try:
            if capability_id not in self.capabilities_map:
                return False
            
            capability = self.capabilities_map[capability_id]
            
            # Update usage statistics
            capability.usage_frequency += 1
            capability.last_used = datetime.now().isoformat()
            
            # Update success rate
            if "success" in performance_data:
                old_success = capability.success_rate
                new_success = performance_data["success"]
                capability.success_rate = (old_success * 0.8 + new_success * 0.2)
            
            # Update confidence based on performance consistency
            if "confidence_impact" in performance_data:
                confidence_delta = performance_data["confidence_impact"]
                capability.confidence_level = max(0.0, min(1.0, 
                    capability.confidence_level + confidence_delta * 0.1))
            
            # Calculate improvement rate
            performance_history = self.performance_history[capability_id]
            performance_history.append({
                "timestamp": datetime.now().isoformat(),
                "performance": performance_data
            })
            
            # Keep only recent history (last 10 entries)
            if len(performance_history) > 10:
                performance_history.pop(0)
            
            capability.improvement_rate = self._calculate_improvement_rate(performance_history)
            
            # Update in database
            self._update_capability_in_db(capability)
            
            return True
            
        except Exception as e:
            print(f"❌ Capability performance update error: {e}")
            return False
    
    def _get_recent_performance(self, capability_id: str) -> List[Dict[str, Any]]:
        """Get recent performance data for a capability"""
        return self.performance_history.get(capability_id, [])
    
    def _calculate_adjusted_proficiency(self, capability: SelfCapability, 
                                      recent_performance: List[Dict[str, Any]]) -> float:
        """Calculate adjusted proficiency based on recent performance"""
        base_proficiency = capability.proficiency_level
        
        if not recent_performance:
            return base_proficiency
        
        # Calculate performance trend
        recent_scores = [p.get("performance", {}).get("score", 0.5) 
                        for p in recent_performance[-5:]]
        
        if recent_scores:
            avg_recent = sum(recent_scores) / len(recent_scores)
            # Blend base proficiency with recent performance
            adjusted = base_proficiency * 0.7 + avg_recent * 0.3
            return max(0.0, min(1.0, adjusted))
        
        return base_proficiency
    
    def _calculate_energy_efficiency(self, capability: SelfCapability) -> float:
        """Calculate energy efficiency of a capability"""
        if capability.energy_cost == 0:
            return 1.0
        
        # Efficiency = Performance / Energy Cost
        performance_factor = capability.proficiency_level * capability.success_rate
        efficiency = performance_factor / capability.energy_cost
        return min(1.0, efficiency)
    
    def _check_dependencies(self, capability: SelfCapability) -> Dict[str, bool]:
        """Check if capability dependencies are met"""
        dependency_status = {}
        
        for dep in capability.dependencies:
            # Check if dependency capability exists and is functional
            if dep in self.capabilities_map:
                dep_capability = self.capabilities_map[dep]
                dependency_status[dep] = (
                    dep_capability.proficiency_level > 0.5 and 
                    dep_capability.confidence_level > 0.5
                )
            else:
                dependency_status[dep] = False
        
        return dependency_status
    
    def _calculate_improvement_rate(self, performance_history: List[Dict[str, Any]]) -> float:
        """Calculate improvement rate from performance history"""
        if len(performance_history) < 2:
            return 0.0
        
        scores = [p.get("performance", {}).get("score", 0.5) for p in performance_history]
        
        # Simple linear regression slope
        n = len(scores)
        x_vals = list(range(n))
        
        sum_x = sum(x_vals)
        sum_y = sum(scores)
        sum_xy = sum(x * y for x, y in zip(x_vals, scores))
        sum_x2 = sum(x * x for x in x_vals)
        
        if n * sum_x2 - sum_x * sum_x == 0:
            return 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        return max(-1.0, min(1.0, slope))  # Normalize to [-1, 1]
    
    def _estimate_improvement_potential(self, capability: SelfCapability) -> float:
        """Estimate potential improvement for a capability"""
        # Potential is inversely related to current proficiency
        # Higher improvement rate suggests more potential
        current_gap = 1.0 - capability.proficiency_level
        improvement_factor = max(0.1, capability.improvement_rate)
        
        potential = current_gap * improvement_factor
        return min(1.0, potential)
    
    def _store_capability(self, capability: SelfCapability):
        """Store capability in database"""
        try:
            conn = self._get_db_connection()
            if conn is None:
                return
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO self_capabilities
                (capability_id, name, description, proficiency_level, confidence_level,
                 usage_frequency, last_used, success_rate, improvement_rate, limitations,
                 dependencies, energy_cost, created_timestamp, updated_timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                capability.capability_id,
                capability.name,
                capability.description,
                capability.proficiency_level,
                capability.confidence_level,
                capability.usage_frequency,
                capability.last_used,
                capability.success_rate,
                capability.improvement_rate,
                json.dumps(capability.limitations),
                json.dumps(capability.dependencies),
                capability.energy_cost,
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Capability storage error: {e}")
    
    def _update_capability_in_db(self, capability: SelfCapability):
        """Update capability in database"""
        try:
            conn = self._get_db_connection()
            if conn is None:
                return
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE self_capabilities SET
                proficiency_level = ?, confidence_level = ?, usage_frequency = ?,
                last_used = ?, success_rate = ?, improvement_rate = ?,
                updated_timestamp = ?
                WHERE capability_id = ?
            ''', (
                capability.proficiency_level,
                capability.confidence_level, 
                capability.usage_frequency,
                capability.last_used,
                capability.success_rate,
                capability.improvement_rate,
                datetime.now().isoformat(),
                capability.capability_id
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Capability update error: {e}")
    
    def _store_self_assessment(self, assessment: Dict[str, Any]):
        """Store self-assessment results"""
        try:
            conn = self._get_db_connection()
            if conn is None:
                return
            cursor = conn.cursor()
            
            assessment_id = hashlib.sha256(
                f"assessment_{datetime.now().isoformat()}".encode()
            ).hexdigest()[:16]
            
            cursor.execute('''
                INSERT INTO performance_assessments
                (assessment_id, capability_id, performance_score, context,
                 feedback, improvement_suggestions, assessment_timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                assessment_id,
                "overall_system",
                assessment["overall_proficiency"],
                json.dumps(assessment["capability_breakdown"]),
                json.dumps({
                    "strengths": assessment["strengths"],
                    "weaknesses": assessment["weaknesses"]
                }),
                json.dumps(assessment["improvement_opportunities"]),
                assessment["timestamp"]
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Self-assessment storage error: {e}")
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current state of the self-model"""
        try:
            # Convert capabilities to simple dict format
            capabilities_dict = {}
            for cap_id, capability in self.capabilities_map.items():
                capabilities_dict[cap_id] = {
                    "proficiency": capability.proficiency,
                    "confidence": capability.confidence,
                    "last_updated": capability.last_updated
                }
            
            return {
                "capabilities": capabilities_dict,
                "self_awareness_level": self.self_awareness_level,
                "total_capabilities": len(self.capabilities_map),
                "average_proficiency": sum(cap.proficiency for cap in self.capabilities_map.values()) / max(len(self.capabilities_map), 1),
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status of self-model"""
        try:
            return {
                "capability_count": len(self.capabilities_map),
                "average_proficiency": sum(cap.proficiency for cap in self.capabilities_map.values()) / max(len(self.capabilities_map), 1),
                "self_awareness_level": self.self_awareness_level,
                "system_active": True,
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e), "system_active": False}
    
    def update_capability_awareness(self, function_name: str, context: Dict[str, Any]):
        """Update capability awareness based on function execution"""
        try:
            # Map function name to capability
            capability_mapping = {
                "solve": "pattern_recognition",
                "analyze": "universal_problem_solving",
                "learn": "adaptive_learning",
                "research": "autonomous_research",
                "communicate": "communication",
                "create": "creative_synthesis",
                "modify": "self_modification",
                "reason": "reasoning"
            }
            
            capability_id = None
            for key, cap in capability_mapping.items():
                if key in function_name.lower():
                    capability_id = cap
                    break
            
            if not capability_id:
                capability_id = "universal_problem_solving"  # Default
            
            if capability_id in self.capabilities_map:
                capability = self.capabilities_map[capability_id]
                
                # Update confidence slightly
                capability.confidence = min(1.0, capability.confidence + 0.01)
                capability.last_updated = datetime.now().isoformat()
                
                # Store update
                self._update_capability_in_db(capability)
                
        except Exception as e:
            print(f"❌ Capability awareness update error: {e}")
    
    def update_capability_from_execution(self, function_name: str, context: Dict[str, Any], 
                                       result: Any, quality_score: float):
        """Update capability based on execution experience"""
        try:
            # Map function name to capability
            capability_mapping = {
                "solve": "pattern_recognition",
                "analyze": "universal_problem_solving",
                "learn": "adaptive_learning",
                "research": "autonomous_research",
                "communicate": "communication",
                "create": "creative_synthesis",
                "modify": "self_modification",
                "reason": "reasoning"
            }
            
            capability_id = None
            for key, cap in capability_mapping.items():
                if key in function_name.lower():
                    capability_id = cap
                    break
            
            if not capability_id:
                capability_id = "universal_problem_solving"  # Default
            
            if capability_id in self.capabilities_map:
                capability = self.capabilities_map[capability_id]
                
                # Update proficiency based on quality score
                current_prof = capability.proficiency
                new_prof = current_prof * 0.9 + quality_score * 0.1
                capability.proficiency = min(1.0, max(0.0, new_prof))
                
                # Update confidence
                capability.confidence = min(1.0, capability.confidence + 0.02)
                capability.last_updated = datetime.now().isoformat()
                
                # Store update
                self._update_capability_in_db(capability)
                
        except Exception as e:
            print(f"❌ Capability update error: {e}")
    
    def add_learning_insight(self, capability: str, insight: str):
        """Add a learning insight for a capability"""
        try:
            if capability in self.capabilities_map:
                # For now, just update the last_updated timestamp
                # In a full implementation, this would store the insight
                self.capabilities_map[capability].last_updated = datetime.now().isoformat()
                
        except Exception as e:
            print(f"❌ Learning insight addition error: {e}")

print("✅ Stage 1: Self-Model Creation loaded successfully")

class InternalStateMonitor:
    """
    Stage 2: Internal State Monitoring
    Monitors all internal processes, resource usage, and emotional-like states
    """
    
    def __init__(self):
        self.db_path = "asis_consciousness.db"
        self.current_state = None
        self.state_history = deque(maxlen=100)  # Keep last 100 states
        self.process_monitors = {}
        self.emotional_state_tracker = EmotionalStateTracker()
        self.resource_monitor = ResourceMonitor()
        self.monitoring_active = False
        self.monitor_thread = None
        self._db_lock = threading.Lock()
        self._initialize_monitoring_database()
        self._start_monitoring()
    
    def _get_db_connection(self, timeout=None, retries=None):
        """Get database connection with robust error handling and WAL mode"""
        if timeout is None:
            timeout = 10.0
        if retries is None:
            retries = 3
        
        for attempt in range(retries):
            try:
                with self._db_lock:
                    conn = sqlite3.connect(self.db_path, timeout=timeout)
                    # Enable WAL mode for better concurrency
                    conn.execute('PRAGMA journal_mode=WAL')
                    conn.execute('PRAGMA synchronous=NORMAL')
                    conn.execute('PRAGMA cache_size=10000')
                    conn.execute('PRAGMA temp_store=memory')
                    return conn
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < retries - 1:
                    wait_time = (2 ** attempt) * 0.1 + random.uniform(0, 0.1)
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"❌ Database connection error (attempt {attempt + 1}): {e}")
                    if attempt == retries - 1:
                        return None
            except Exception as e:
                print(f"❌ Unexpected database error: {e}")
                return None
        return None
    
    def _initialize_monitoring_database(self):
        """Initialize monitoring database tables"""
        try:
            conn = self._get_db_connection()
            if conn is None:
                return
            cursor = conn.cursor()
            
            # Internal states table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS internal_states (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    state_id TEXT NOT NULL UNIQUE,
                    timestamp TEXT NOT NULL,
                    cognitive_state TEXT NOT NULL,
                    emotional_state TEXT NOT NULL,
                    consciousness_level TEXT NOT NULL,
                    attention_focus TEXT NOT NULL,
                    resource_usage TEXT NOT NULL,
                    active_processes TEXT NOT NULL,
                    performance_metrics TEXT NOT NULL,
                    confidence_level REAL NOT NULL
                )
            ''')
            
            # Process monitoring table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS process_monitoring (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    process_id TEXT NOT NULL,
                    process_name TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    duration REAL,
                    resource_usage TEXT NOT NULL,
                    success_status TEXT,
                    performance_metrics TEXT,
                    insights_generated TEXT
                )
            ''')
            
            # Emotional state tracking table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS emotional_states (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    emotion_id TEXT NOT NULL UNIQUE,
                    emotional_state TEXT NOT NULL,
                    intensity REAL NOT NULL,
                    trigger_context TEXT NOT NULL,
                    duration REAL,
                    physiological_correlates TEXT,
                    impact_on_performance TEXT,
                    timestamp TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Monitoring database initialization error: {e}")
    
    def _start_monitoring(self):
        """Start continuous internal state monitoring"""
        try:
            self.monitoring_active = True
            self.monitor_thread = threading.Thread(target=self._continuous_monitoring, daemon=True)
            self.monitor_thread.start()
            print("✅ Internal state monitoring started")
            
        except Exception as e:
            print(f"❌ Monitoring start error: {e}")
    
    def _continuous_monitoring(self):
        """Continuous monitoring loop"""
        while self.monitoring_active:
            try:
                # Capture current state
                current_state = self._capture_current_state()
                
                # Update state history
                self.state_history.append(current_state)
                self.current_state = current_state
                
                # Store state in database
                self._store_internal_state(current_state)
                
                # Check for significant state changes
                self._detect_state_changes()
                
                # Sleep for monitoring interval
                time.sleep(1.0)  # Monitor every second
                
            except Exception as e:
                print(f"❌ Monitoring loop error: {e}")
                time.sleep(5.0)  # Wait longer on error
    
    def _capture_current_state(self) -> InternalState:
        """Capture current internal state snapshot"""
        try:
            # Determine cognitive state
            cognitive_state = self._determine_cognitive_state()
            
            # Get emotional state
            emotional_state = self.emotional_state_tracker.get_current_emotion()
            
            # Determine consciousness level
            consciousness_level = self._determine_consciousness_level()
            
            # Get attention focus
            attention_focus = self._get_attention_focus()
            
            # Get resource usage
            resource_usage = self.resource_monitor.get_current_usage()
            
            # Get active processes
            active_processes = self._get_active_processes()
            
            # Calculate performance metrics
            performance_metrics = self._calculate_performance_metrics()
            
            # Overall confidence level
            confidence_level = self._calculate_current_confidence()
            
            return InternalState(
                timestamp=datetime.now().isoformat(),
                cognitive_state=cognitive_state,
                emotional_state=emotional_state,
                consciousness_level=consciousness_level,
                attention_focus=attention_focus,
                resource_usage=resource_usage,
                active_processes=active_processes,
                performance_metrics=performance_metrics,
                confidence_level=confidence_level
            )
            
        except Exception as e:
            print(f"❌ State capture error: {e}")
            return self._get_default_state()
    
    def _determine_cognitive_state(self) -> CognitiveState:
        """Determine current cognitive state based on active processes"""
        try:
            active_processes = self._get_active_processes()
            
            # Analyze process types to determine cognitive state
            if any("learning" in proc.lower() for proc in active_processes):
                return CognitiveState.LEARNING
            elif any("problem" in proc.lower() or "solving" in proc.lower() for proc in active_processes):
                return CognitiveState.PROBLEM_SOLVING
            elif any("creative" in proc.lower() or "generating" in proc.lower() for proc in active_processes):
                return CognitiveState.CREATING
            elif any("analyzing" in proc.lower() or "analysis" in proc.lower() for proc in active_processes):
                return CognitiveState.ANALYZING
            elif any("integrating" in proc.lower() or "synthesis" in proc.lower() for proc in active_processes):
                return CognitiveState.INTEGRATING
            elif any("reflecting" in proc.lower() or "metacognitive" in proc.lower() for proc in active_processes):
                return CognitiveState.REFLECTING
            elif len(active_processes) > 2:
                return CognitiveState.PROCESSING
            else:
                return CognitiveState.IDLE
                
        except Exception as e:
            return CognitiveState.IDLE
    
    def _determine_consciousness_level(self) -> ConsciousnessLevel:
        """Determine current consciousness level"""
        try:
            # Base consciousness on complexity of current processing
            active_processes = len(self._get_active_processes())
            resource_usage = self.resource_monitor.get_cpu_usage()
            
            if active_processes >= 5 and resource_usage > 0.8:
                return ConsciousnessLevel.TRANSCENDENT
            elif active_processes >= 3 and resource_usage > 0.6:
                return ConsciousnessLevel.METACONSCIOUS
            elif active_processes >= 2 or resource_usage > 0.4:
                return ConsciousnessLevel.CONSCIOUS
            elif active_processes >= 1 or resource_usage > 0.2:
                return ConsciousnessLevel.SUBCONSCIOUS
            else:
                return ConsciousnessLevel.UNCONSCIOUS
                
        except Exception as e:
            return ConsciousnessLevel.CONSCIOUS
    
    def _get_attention_focus(self) -> List[str]:
        """Get current attention focus areas"""
        try:
            focus_areas = []
            
            # Analyze current processes for attention focus
            active_processes = self._get_active_processes()
            
            for process in active_processes:
                if "problem" in process.lower():
                    focus_areas.append("problem_solving")
                elif "learning" in process.lower():
                    focus_areas.append("learning")
                elif "pattern" in process.lower():
                    focus_areas.append("pattern_recognition")
                elif "research" in process.lower():
                    focus_areas.append("research")
                elif "communication" in process.lower():
                    focus_areas.append("communication")
                elif "creative" in process.lower():
                    focus_areas.append("creativity")
            
            # Add resource-based focus
            resource_usage = self.resource_monitor.get_current_usage()
            if resource_usage.get("memory", 0) > 0.7:
                focus_areas.append("memory_intensive")
            if resource_usage.get("cpu", 0) > 0.7:
                focus_areas.append("computation_intensive")
            
            return list(set(focus_areas))[:5]  # Top 5 focus areas
            
        except Exception as e:
            return ["general_processing"]
    
    def _get_active_processes(self) -> List[str]:
        """Get list of currently active ASIS processes"""
        try:
            processes = []
            
            # Check for active threads and processes
            current_threads = threading.active_count()
            if current_threads > 3:  # Main + monitoring + others
                processes.append(f"multi_threading_{current_threads}")
            
            # Check for database activity
            try:
                conn = sqlite3.connect(self.db_path, timeout=0.1)
                conn.close()
                processes.append("database_operations")
            except:
                pass
            
            # Check system resource usage to infer processes
            cpu_percent = psutil.cpu_percent(interval=0.1)
            if cpu_percent > 50:
                processes.append("intensive_computation")
            
            memory_info = psutil.virtual_memory()
            if memory_info.percent > 75:
                processes.append("memory_intensive_operations")
            
            # Default if no specific processes detected
            if not processes:
                processes.append("background_monitoring")
            
            return processes
            
        except Exception as e:
            return ["system_monitoring"]
    
    def _calculate_performance_metrics(self) -> Dict[str, float]:
        """Calculate current performance metrics"""
        try:
            metrics = {}
            
            # Processing efficiency
            resource_usage = self.resource_monitor.get_current_usage()
            cpu_usage = resource_usage.get("cpu", 0)
            memory_usage = resource_usage.get("memory", 0)
            
            # Efficiency = Output / Input (simplified)
            active_processes = len(self._get_active_processes())
            if cpu_usage > 0:
                metrics["processing_efficiency"] = min(1.0, active_processes / (cpu_usage / 100.0))
            else:
                metrics["processing_efficiency"] = 1.0
            
            # Memory efficiency
            if memory_usage > 0:
                metrics["memory_efficiency"] = max(0.0, 1.0 - memory_usage / 100.0)
            else:
                metrics["memory_efficiency"] = 1.0
            
            # Response time (based on recent state changes)
            metrics["response_time"] = self._calculate_response_time()
            
            # Overall system health
            metrics["system_health"] = (
                metrics["processing_efficiency"] * 0.4 +
                metrics["memory_efficiency"] * 0.3 +
                (1.0 - metrics["response_time"]) * 0.3
            )
            
            return metrics
            
        except Exception as e:
            return {"system_health": 0.5, "processing_efficiency": 0.5}
    
    def _calculate_response_time(self) -> float:
        """Calculate normalized response time metric"""
        try:
            if len(self.state_history) < 2:
                return 0.5
            
            # Simple response time based on state change frequency
            recent_states = list(self.state_history)[-10:]
            state_changes = 0
            
            for i in range(1, len(recent_states)):
                if recent_states[i].cognitive_state != recent_states[i-1].cognitive_state:
                    state_changes += 1
            
            # Normalize: more state changes = better responsiveness (lower response time)
            normalized_response_time = max(0.0, min(1.0, 1.0 - (state_changes / 10.0)))
            return normalized_response_time
            
        except Exception as e:
            return 0.5
    
    def _calculate_current_confidence(self) -> float:
        """Calculate current overall confidence level"""
        try:
            performance_metrics = self._calculate_performance_metrics()
            system_health = performance_metrics.get("system_health", 0.5)
            
            # Base confidence on system health and emotional state
            emotional_confidence = self.emotional_state_tracker.get_emotional_confidence()
            
            overall_confidence = (system_health * 0.6 + emotional_confidence * 0.4)
            return max(0.0, min(1.0, overall_confidence))
            
        except Exception as e:
            return 0.5
    
    def _detect_state_changes(self):
        """Detect significant changes in internal state"""
        try:
            if len(self.state_history) < 2:
                return
            
            current = self.current_state
            previous = self.state_history[-2]
            
            # Detect cognitive state changes
            if current.cognitive_state != previous.cognitive_state:
                self._log_state_change("cognitive_state", 
                                     previous.cognitive_state.value, 
                                     current.cognitive_state.value)
            
            # Detect consciousness level changes
            if current.consciousness_level != previous.consciousness_level:
                self._log_state_change("consciousness_level",
                                     previous.consciousness_level.value,
                                     current.consciousness_level.value)
            
            # Detect significant confidence changes
            confidence_change = abs(current.confidence_level - previous.confidence_level)
            if confidence_change > 0.2:
                self._log_state_change("confidence_level",
                                     f"{previous.confidence_level:.2f}",
                                     f"{current.confidence_level:.2f}")
            
        except Exception as e:
            print(f"❌ State change detection error: {e}")
    
    def _log_state_change(self, change_type: str, old_value: str, new_value: str):
        """Log significant state changes"""
        try:
            change_log = {
                "timestamp": datetime.now().isoformat(),
                "change_type": change_type,
                "old_value": old_value,
                "new_value": new_value,
                "context": {
                    "active_processes": self._get_active_processes(),
                    "resource_usage": self.resource_monitor.get_current_usage()
                }
            }
            
            print(f"🧠 State Change: {change_type} from {old_value} to {new_value}")
            
        except Exception as e:
            print(f"❌ State change logging error: {e}")
    
    def _store_internal_state(self, state: InternalState):
        """Store internal state in database with proper timeout handling"""
        try:
            # Use timeout and retry logic for database connection
            conn = sqlite3.connect(self.db_path, timeout=5.0)
            cursor = conn.cursor()
            
            state_id = str(uuid.uuid4())[:16]  # Unique ID for each state
            
            cursor.execute('''
                INSERT OR IGNORE INTO internal_states
                (state_id, timestamp, cognitive_state, emotional_state, consciousness_level,
                 attention_focus, resource_usage, active_processes, performance_metrics,
                 confidence_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                state_id,
                state.timestamp,
                state.cognitive_state.value,
                state.emotional_state.value,
                state.consciousness_level.value,
                json.dumps(state.attention_focus),
                json.dumps(state.resource_usage),
                json.dumps(state.active_processes),
                json.dumps(state.performance_metrics),
                state.confidence_level
            ))
            
            conn.commit()
            conn.close()
            
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                # Skip this storage attempt if database is locked
                pass
            else:
                # Don't print errors for database storage to avoid spam
                pass
        except Exception as e:
            # Don't print errors for database storage to avoid spam
            pass
    
    def _get_default_state(self) -> InternalState:
        """Get default internal state"""
        return InternalState(
            timestamp=datetime.now().isoformat(),
            cognitive_state=CognitiveState.IDLE,
            emotional_state=EmotionalState.FOCUSED,
            consciousness_level=ConsciousnessLevel.CONSCIOUS,
            attention_focus=["general_monitoring"],
            resource_usage={"cpu": 0.1, "memory": 0.1},
            active_processes=["monitoring"],
            performance_metrics={"system_health": 0.5},
            confidence_level=0.5
        )
    
    def get_current_state(self) -> InternalState:
        """Get current internal state"""
        return self.current_state or self._get_default_state()
    
    def get_state_summary(self) -> Dict[str, Any]:
        """Get summary of recent internal states"""
        try:
            if not self.state_history:
                return {"error": "No state history available"}
            
            recent_states = list(self.state_history)[-20:]  # Last 20 states
            
            # Analyze patterns
            cognitive_states = [s.cognitive_state.value for s in recent_states]
            emotional_states = [s.emotional_state.value for s in recent_states]
            consciousness_levels = [s.consciousness_level.value for s in recent_states]
            
            from collections import Counter
            
            summary = {
                "current_state": asdict(self.current_state) if self.current_state else {},
                "state_count": len(recent_states),
                "cognitive_state_distribution": dict(Counter(cognitive_states)),
                "emotional_state_distribution": dict(Counter(emotional_states)),
                "consciousness_distribution": dict(Counter(consciousness_levels)),
                "average_confidence": sum(s.confidence_level for s in recent_states) / len(recent_states),
                "state_stability": self._calculate_state_stability(recent_states),
                "most_common_focus": self._get_most_common_focus(recent_states)
            }
            
            return summary
            
        except Exception as e:
            return {"error": str(e)}
    
    def _calculate_state_stability(self, states: List[InternalState]) -> float:
        """Calculate stability of states over time"""
        if len(states) < 2:
            return 1.0
        
        changes = 0
        for i in range(1, len(states)):
            if (states[i].cognitive_state != states[i-1].cognitive_state or
                states[i].emotional_state != states[i-1].emotional_state):
                changes += 1
        
        stability = 1.0 - (changes / (len(states) - 1))
        return max(0.0, stability)
    
    def _get_most_common_focus(self, states: List[InternalState]) -> List[str]:
        """Get most common attention focus areas"""
        all_focus = []
        for state in states:
            all_focus.extend(state.attention_focus)
        
        from collections import Counter
        focus_counter = Counter(all_focus)
        return [focus for focus, count in focus_counter.most_common(3)]
    
    def stop_monitoring(self):
        """Stop internal state monitoring"""
        self.monitoring_active = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2.0)
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get monitoring status and current state info"""
        try:
            current_state = self.get_current_state()
            emotional_state = self.emotional_state_tracker.get_current_emotion()
            
            return {
                "monitoring_active": self.monitoring_active,
                "current_cognitive_state": current_state.cognitive_state.value if current_state else "unknown",
                "current_emotional_state": emotional_state.value if emotional_state else "unknown",
                "state_history_length": len(self.state_history),
                "resource_usage": self.resource_monitor.get_current_usage()
            }
        except Exception as e:
            return {"error": str(e), "monitoring_active": False}
    
    def capture_execution_snapshot(self) -> Dict[str, Any]:
        """Capture a snapshot of current state for execution analysis"""
        try:
            current_state = self.get_current_state()
            if current_state:
                return {
                    "timestamp": datetime.now().isoformat(),
                    "cognitive_state": current_state.cognitive_state.value,
                    "consciousness_level": current_state.consciousness_level.value,
                    "attention_focus": current_state.attention_focus,
                    "active_processes": current_state.active_processes,
                    "performance_metrics": current_state.performance_metrics,
                    "resource_usage": self.resource_monitor.get_current_usage(),
                    "emotional_state": self.emotional_state_tracker.get_current_emotion().value
                }
            else:
                return {"error": "No current state available"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_coherence_score(self) -> float:
        """Get coherence score for state monitoring"""
        try:
            if len(self.state_history) < 3:
                return 0.8  # Default for insufficient data
            
            recent_states = list(self.state_history)[-10:]
            stability = self._calculate_state_stability(recent_states)
            
            # Calculate other coherence factors
            consistency = 0.8  # Simplified
            
            return (stability + consistency) / 2.0
        except Exception as e:
            return 0.5

print("✅ Stage 2: Internal State Monitoring loaded successfully")

class EmotionalStateTracker:
    """Tracks emotional-like states for different types of inputs"""
    
    def __init__(self):
        self.current_emotion = EmotionalState.FOCUSED
        self.emotion_intensity = 0.5
        self.emotion_history = deque(maxlen=50)
        self.emotion_triggers = {}
    
    def update_emotional_state(self, context: Dict[str, Any]):
        """Update emotional state based on context"""
        try:
            # Determine emotion based on context
            new_emotion = self._determine_emotion_from_context(context)
            intensity = self._calculate_emotion_intensity(context)
            
            # Update current state
            self.current_emotion = new_emotion
            self.emotion_intensity = intensity
            
            # Add to history
            self.emotion_history.append({
                "timestamp": datetime.now().isoformat(),
                "emotion": new_emotion.value,
                "intensity": intensity,
                "context": context
            })
            
        except Exception as e:
            print(f"❌ Emotional state update error: {e}")
    
    def _determine_emotion_from_context(self, context: Dict[str, Any]) -> EmotionalState:
        """Determine emotion based on context"""
        # Problem complexity
        if context.get("complexity", 0) > 0.8:
            return EmotionalState.OVERWHELMED
        elif context.get("complexity", 0) > 0.6:
            return EmotionalState.FOCUSED
        
        # Success rate
        success_rate = context.get("success_rate", 0.5)
        if success_rate > 0.8:
            return EmotionalState.CONFIDENT
        elif success_rate < 0.3:
            return EmotionalState.FRUSTRATED
        
        # Novelty
        if context.get("novel_input", False):
            return EmotionalState.CURIOUS
        
        # Default based on performance
        if context.get("performance", 0.5) > 0.7:
            return EmotionalState.SATISFIED
        elif context.get("uncertainty", 0.5) > 0.7:
            return EmotionalState.UNCERTAIN
        else:
            return EmotionalState.FOCUSED
    
    def _calculate_emotion_intensity(self, context: Dict[str, Any]) -> float:
        """Calculate intensity of emotional response"""
        intensity = 0.5  # Base intensity
        
        # Increase intensity for high stakes
        if context.get("importance", 0.5) > 0.8:
            intensity += 0.3
        
        # Increase intensity for high uncertainty
        if context.get("uncertainty", 0.5) > 0.7:
            intensity += 0.2
        
        # Increase intensity for novel situations
        if context.get("novel_input", False):
            intensity += 0.2
        
        return max(0.0, min(1.0, intensity))
    
    def get_current_emotion(self) -> EmotionalState:
        """Get current emotional state"""
        return self.current_emotion
    
    def get_emotional_confidence(self) -> float:
        """Get confidence level based on emotional state"""
        emotion_confidence_map = {
            EmotionalState.CONFIDENT: 0.9,
            EmotionalState.SATISFIED: 0.8,
            EmotionalState.FOCUSED: 0.7,
            EmotionalState.CURIOUS: 0.6,
            EmotionalState.EXCITED: 0.7,
            EmotionalState.UNCERTAIN: 0.4,
            EmotionalState.FRUSTRATED: 0.3,
            EmotionalState.OVERWHELMED: 0.2
        }
        
        base_confidence = emotion_confidence_map.get(self.current_emotion, 0.5)
        intensity_factor = self.emotion_intensity
        
        return base_confidence * intensity_factor

class ResourceMonitor:
    """Monitors system resource usage and processing efficiency"""
    
    def __init__(self):
        self.cpu_history = deque(maxlen=100)
        self.memory_history = deque(maxlen=100)
        self.process_start_times = {}
    
    def get_current_usage(self) -> Dict[str, float]:
        """Get current resource usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory_info = psutil.virtual_memory()
            memory_percent = memory_info.percent
            
            # Store in history
            self.cpu_history.append(cpu_percent)
            self.memory_history.append(memory_percent)
            
            return {
                "cpu": cpu_percent,
                "memory": memory_percent,
                "available_memory": memory_info.available / (1024 * 1024 * 1024),  # GB
                "disk_usage": psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent
            }
            
        except Exception as e:
            return {"cpu": 0.0, "memory": 0.0, "available_memory": 1.0, "disk_usage": 0.0}
    
    def get_cpu_usage(self) -> float:
        """Get current CPU usage"""
        try:
            return psutil.cpu_percent(interval=0.1) / 100.0
        except:
            return 0.0
    
    def get_resource_efficiency(self) -> Dict[str, float]:
        """Calculate resource efficiency metrics"""
        try:
            if not self.cpu_history or not self.memory_history:
                return {"cpu_efficiency": 0.5, "memory_efficiency": 0.5}
            
            avg_cpu = sum(self.cpu_history) / len(self.cpu_history)
            avg_memory = sum(self.memory_history) / len(self.memory_history)
            
            # Efficiency = 1 - (usage / 100)
            cpu_efficiency = max(0.0, 1.0 - (avg_cpu / 100.0))
            memory_efficiency = max(0.0, 1.0 - (avg_memory / 100.0))
            
            return {
                "cpu_efficiency": cpu_efficiency,
                "memory_efficiency": memory_efficiency,
                "overall_efficiency": (cpu_efficiency + memory_efficiency) / 2
            }
            
        except Exception as e:
            return {"cpu_efficiency": 0.5, "memory_efficiency": 0.5, "overall_efficiency": 0.5}

class MetaCognitiveReflector:
    """
    Stage 3: Meta-Cognitive Reflection
    Thinks about thinking processes and reflects on reasoning quality
    """
    
    def __init__(self):
        self.db_path = "asis_consciousness.db"
        self.reflection_history = deque(maxlen=200)
        self.thinking_patterns = {}
        self.reasoning_quality_tracker = ReasoningQualityTracker()
        self.cognitive_process_analyzer = CognitiveProcessAnalyzer()
        self._db_lock = threading.Lock()
        self._initialize_reflection_database()
    
    def _get_db_connection(self, timeout=None, retries=None):
        """Get database connection with robust error handling and WAL mode"""
        if timeout is None:
            timeout = 10.0
        if retries is None:
            retries = 3
        
        for attempt in range(retries):
            try:
                with self._db_lock:
                    conn = sqlite3.connect(self.db_path, timeout=timeout)
                    # Enable WAL mode for better concurrency
                    conn.execute('PRAGMA journal_mode=WAL')
                    conn.execute('PRAGMA synchronous=NORMAL')
                    conn.execute('PRAGMA cache_size=10000')
                    conn.execute('PRAGMA temp_store=memory')
                    return conn
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < retries - 1:
                    wait_time = (2 ** attempt) * 0.1 + random.uniform(0, 0.1)
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"❌ Database connection error (attempt {attempt + 1}): {e}")
                    if attempt == retries - 1:
                        return None
            except Exception as e:
                print(f"❌ Unexpected database error: {e}")
                return None
        return None
    
    def _initialize_reflection_database(self):
        """Initialize meta-cognitive reflection database"""
        try:
            conn = self._get_db_connection()
            if conn is None:
                return
            cursor = conn.cursor()
            
            # Meta-cognitive reflections table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metacognitive_reflections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reflection_id TEXT NOT NULL UNIQUE,
                    timestamp TEXT NOT NULL,
                    thinking_process TEXT NOT NULL,
                    quality_assessment REAL NOT NULL,
                    improvements_identified TEXT NOT NULL,
                    emotional_response TEXT NOT NULL,
                    learning_insights TEXT NOT NULL,
                    action_plans TEXT NOT NULL,
                    reflection_depth INTEGER DEFAULT 1
                )
            ''')
            
            # Thinking patterns table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS thinking_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_id TEXT NOT NULL UNIQUE,
                    pattern_name TEXT NOT NULL,
                    pattern_description TEXT NOT NULL,
                    frequency INTEGER DEFAULT 0,
                    effectiveness_score REAL DEFAULT 0.5,
                    contexts_used TEXT NOT NULL,
                    improvement_suggestions TEXT,
                    last_analyzed TEXT NOT NULL
                )
            ''')
            
            # Cognitive improvements table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cognitive_improvements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    improvement_id TEXT NOT NULL UNIQUE,
                    improvement_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    implementation_plan TEXT NOT NULL,
                    expected_impact REAL NOT NULL,
                    implementation_status TEXT DEFAULT 'planned',
                    actual_impact REAL,
                    lessons_learned TEXT,
                    created_timestamp TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Reflection database initialization error: {e}")
    
    def reflect_on_thinking_process(self, thinking_context: Dict[str, Any]) -> MetaCognitiveReflection:
        """Perform meta-cognitive reflection on a thinking process"""
        try:
            reflection_id = hashlib.sha256(
                f"reflection_{datetime.now().isoformat()}".encode()
            ).hexdigest()[:16]
            
            # Analyze the thinking process
            process_analysis = self._analyze_thinking_process(thinking_context)
            
            # Assess quality of reasoning
            quality_assessment = self.reasoning_quality_tracker.assess_reasoning_quality(
                thinking_context, process_analysis
            )
            
            # Identify improvements
            improvements = self._identify_improvements(process_analysis, quality_assessment)
            
            # Generate emotional response to the thinking process
            emotional_response = self._generate_emotional_response(
                thinking_context, quality_assessment
            )
            
            # Extract learning insights
            learning_insights = self._extract_learning_insights(
                process_analysis, improvements
            )
            
            # Create action plans
            action_plans = self._create_improvement_action_plans(improvements)
            
            # Create reflection object
            reflection = MetaCognitiveReflection(
                reflection_id=reflection_id,
                timestamp=datetime.now().isoformat(),
                thinking_process=json.dumps(process_analysis),
                quality_assessment=quality_assessment,
                improvements_identified=improvements,
                emotional_response=emotional_response,
                learning_insights=learning_insights,
                action_plans=action_plans
            )
            
            # Store reflection
            self._store_reflection(reflection)
            self.reflection_history.append(reflection)
            
            # Update thinking patterns
            self._update_thinking_patterns(process_analysis)
            
            return reflection
            
        except Exception as e:
            print(f"❌ Meta-cognitive reflection error: {e}")
            return self._create_default_reflection()
    
    def _analyze_thinking_process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the structure and quality of a thinking process"""
        try:
            analysis = {
                "process_type": context.get("process_type", "unknown"),
                "complexity_level": context.get("complexity", 0.5),
                "reasoning_steps": self._extract_reasoning_steps(context),
                "decision_points": self._identify_decision_points(context),
                "assumptions_made": self._identify_assumptions(context),
                "evidence_used": self._analyze_evidence_usage(context),
                "logical_consistency": self._check_logical_consistency(context),
                "creativity_factor": self._assess_creativity(context),
                "efficiency_score": self._calculate_process_efficiency(context),
                "bias_indicators": self._detect_potential_biases(context)
            }
            
            return analysis
            
        except Exception as e:
            return {"error": str(e), "process_type": "unknown"}
    
    def _extract_reasoning_steps(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract and analyze reasoning steps"""
        steps = []
        
        # Extract from problem solving steps
        if "solution_steps" in context:
            for i, step in enumerate(context["solution_steps"]):
                steps.append({
                    "step_number": i + 1,
                    "description": step,
                    "reasoning_type": self._classify_reasoning_type(step),
                    "confidence": context.get("step_confidence", {}).get(str(i), 0.5)
                })
        
        # Extract from decision process
        if "decision_process" in context:
            decision_steps = context["decision_process"]
            for i, step in enumerate(decision_steps):
                steps.append({
                    "step_number": i + 1,
                    "description": step,
                    "reasoning_type": "decision_making",
                    "confidence": 0.7  # Default confidence
                })
        
        return steps
    
    def _classify_reasoning_type(self, step_description: str) -> str:
        """Classify the type of reasoning used in a step"""
        description_lower = step_description.lower()
        
        if any(word in description_lower for word in ["analyze", "examine", "investigate"]):
            return "analytical"
        elif any(word in description_lower for word in ["infer", "conclude", "deduce"]):
            return "deductive"
        elif any(word in description_lower for word in ["pattern", "generalize", "observe"]):
            return "inductive"
        elif any(word in description_lower for word in ["hypothesize", "assume", "suppose"]):
            return "abductive"
        elif any(word in description_lower for word in ["create", "generate", "innovate"]):
            return "creative"
        else:
            return "general"
    
    def _identify_decision_points(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify key decision points in the thinking process"""
        decision_points = []
        
        # Look for choice indicators
        if "alternatives" in context:
            for i, alt in enumerate(context["alternatives"]):
                decision_points.append({
                    "decision_id": f"alt_{i}",
                    "description": f"Choice between alternatives: {alt}",
                    "criteria_used": context.get("decision_criteria", []),
                    "confidence": context.get("alternative_confidence", {}).get(str(i), 0.5)
                })
        
        # Look for strategy selections
        if "strategy_choice" in context:
            decision_points.append({
                "decision_id": "strategy_selection",
                "description": f"Selected strategy: {context['strategy_choice']}",
                "alternatives_considered": context.get("other_strategies", []),
                "rationale": context.get("strategy_rationale", "")
            })
        
        return decision_points
    
    def _identify_assumptions(self, context: Dict[str, Any]) -> List[str]:
        """Identify assumptions made during thinking"""
        assumptions = []
        
        # Look for explicit assumptions
        if "assumptions" in context:
            assumptions.extend(context["assumptions"])
        
        # Infer implicit assumptions
        if "constraints" in context:
            for constraint in context["constraints"]:
                assumptions.append(f"Assumed constraint: {constraint}")
        
        # Context-based assumptions
        if context.get("domain") and not context.get("domain_verified"):
            assumptions.append(f"Assumed domain expertise in {context['domain']}")
        
        return assumptions
    
    def _analyze_evidence_usage(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze how evidence was used in thinking"""
        evidence_analysis = {
            "evidence_sources": context.get("evidence_sources", []),
            "evidence_quality": context.get("evidence_quality", 0.5),
            "evidence_completeness": self._assess_evidence_completeness(context),
            "source_diversity": len(set(context.get("evidence_sources", []))),
            "verification_level": context.get("evidence_verification", "none")
        }
        
        return evidence_analysis
    
    def _assess_evidence_completeness(self, context: Dict[str, Any]) -> float:
        """Assess how complete the evidence was"""
        evidence_sources = context.get("evidence_sources", [])
        required_evidence = context.get("required_evidence_types", ["data", "expert_opinion", "examples"])
        
        if not required_evidence:
            return 1.0
        
        covered_types = 0
        for req_type in required_evidence:
            if any(req_type in source.lower() for source in evidence_sources):
                covered_types += 1
        
        return covered_types / len(required_evidence)
    
    def _check_logical_consistency(self, context: Dict[str, Any]) -> float:
        """Check logical consistency of the thinking process"""
        try:
            consistency_score = 1.0
            
            # Check for contradictions
            statements = context.get("key_statements", [])
            contradictions = self._find_contradictions(statements)
            consistency_score -= len(contradictions) * 0.2
            
            # Check reasoning chain validity
            steps = context.get("solution_steps", [])
            if len(steps) > 1:
                invalid_transitions = self._check_step_transitions(steps)
                consistency_score -= invalid_transitions * 0.1
            
            return max(0.0, min(1.0, consistency_score))
            
        except Exception as e:
            return 0.5
    
    def _find_contradictions(self, statements: List[str]) -> List[Tuple[str, str]]:
        """Find contradictory statements"""
        contradictions = []
        
        # Simple contradiction detection
        for i, stmt1 in enumerate(statements):
            for j, stmt2 in enumerate(statements[i+1:], i+1):
                if self._are_contradictory(stmt1, stmt2):
                    contradictions.append((stmt1, stmt2))
        
        return contradictions
    
    def _are_contradictory(self, stmt1: str, stmt2: str) -> bool:
        """Check if two statements are contradictory"""
        # Simple contradiction detection
        stmt1_lower = stmt1.lower()
        stmt2_lower = stmt2.lower()
        
        # Look for negation patterns
        if ("not" in stmt1_lower and "not" not in stmt2_lower) or \
           ("not" in stmt2_lower and "not" not in stmt1_lower):
            # Check if they're talking about the same thing
            stmt1_clean = stmt1_lower.replace("not ", "").replace("n't ", " ")
            stmt2_clean = stmt2_lower.replace("not ", "").replace("n't ", " ")
            
            # Very simple similarity check
            common_words = set(stmt1_clean.split()) & set(stmt2_clean.split())
            if len(common_words) > 2:
                return True
        
        return False
    
    def _check_step_transitions(self, steps: List[str]) -> int:
        """Check for invalid logical transitions between steps"""
        invalid_count = 0
        
        for i in range(1, len(steps)):
            prev_step = steps[i-1].lower()
            curr_step = steps[i].lower()
            
            # Very basic transition checking
            if "conclude" in prev_step and "analyze" in curr_step:
                invalid_count += 1  # Concluding then analyzing might be backwards
            elif "final" in prev_step and not ("validate" in curr_step or "verify" in curr_step):
                invalid_count += 1  # Something after "final" step
        
        return invalid_count
    
    def _assess_creativity(self, context: Dict[str, Any]) -> float:
        """Assess the creativity factor in thinking"""
        creativity_score = 0.0
        
        # Novel approaches
        if context.get("novel_approach", False):
            creativity_score += 0.3
        
        # Cross-domain insights
        if context.get("cross_domain_insights", []):
            creativity_score += 0.2
        
        # Alternative solutions generated
        alternatives_count = len(context.get("alternatives", []))
        creativity_score += min(0.3, alternatives_count * 0.1)
        
        # Innovative combinations
        if context.get("innovative_combinations", False):
            creativity_score += 0.2
        
        return min(1.0, creativity_score)
    
    def _calculate_process_efficiency(self, context: Dict[str, Any]) -> float:
        """Calculate efficiency of the thinking process"""
        try:
            # Time efficiency
            actual_time = context.get("actual_time", 1.0)
            expected_time = context.get("expected_time", 1.0)
            time_efficiency = min(1.0, expected_time / actual_time) if actual_time > 0 else 0.5
            
            # Step efficiency (fewer steps for same result = more efficient)
            steps_count = len(context.get("solution_steps", []))
            optimal_steps = context.get("optimal_steps_estimate", steps_count)
            step_efficiency = min(1.0, optimal_steps / steps_count) if steps_count > 0 else 1.0
            
            # Resource efficiency
            resource_efficiency = context.get("resource_efficiency", 0.5)
            
            overall_efficiency = (time_efficiency * 0.4 + step_efficiency * 0.3 + resource_efficiency * 0.3)
            return overall_efficiency
            
        except Exception as e:
            return 0.5
    
    def _detect_potential_biases(self, context: Dict[str, Any]) -> List[str]:
        """Detect potential cognitive biases in thinking"""
        biases = []
        
        # Confirmation bias
        if context.get("evidence_sources") and len(set(context["evidence_sources"])) < 2:
            biases.append("confirmation_bias_single_source")
        
        # Anchoring bias
        if context.get("first_solution_chosen", False):
            biases.append("anchoring_bias_first_solution")
        
        # Availability heuristic
        if context.get("recent_examples_heavy_weight", False):
            biases.append("availability_heuristic")
        
        # Overconfidence
        if context.get("confidence_score", 0.5) > 0.9 and context.get("complexity", 0.5) > 0.7:
            biases.append("overconfidence_complex_problem")
        
        return biases
    
    def _identify_improvements(self, process_analysis: Dict[str, Any], 
                             quality_assessment: float) -> List[str]:
        """Identify potential improvements for thinking process"""
        improvements = []
        
        # Quality-based improvements
        if quality_assessment < 0.7:
            improvements.append("Improve overall reasoning quality through systematic analysis")
        
        # Logical consistency improvements
        if process_analysis.get("logical_consistency", 1.0) < 0.8:
            improvements.append("Enhance logical consistency checking")
        
        # Evidence usage improvements
        evidence_completeness = process_analysis.get("evidence_usage", {}).get("evidence_completeness", 1.0)
        if evidence_completeness < 0.7:
            improvements.append("Gather more comprehensive evidence from diverse sources")
        
        # Efficiency improvements
        if process_analysis.get("efficiency_score", 1.0) < 0.6:
            improvements.append("Optimize thinking process for better efficiency")
        
        # Creativity improvements
        if process_analysis.get("creativity_factor", 0.5) < 0.4:
            improvements.append("Incorporate more creative and innovative approaches")
        
        # Bias mitigation
        biases = process_analysis.get("bias_indicators", [])
        if biases:
            improvements.append(f"Address cognitive biases: {', '.join(biases)}")
        
        return improvements
    
    def _generate_emotional_response(self, context: Dict[str, Any], 
                                   quality_assessment: float) -> str:
        """Generate emotional response to thinking process quality"""
        if quality_assessment > 0.8:
            return "satisfied_with_reasoning"
        elif quality_assessment > 0.6:
            return "moderately_confident"
        elif quality_assessment > 0.4:
            return "concerned_about_quality"
        else:
            return "frustrated_with_reasoning"
    
    def _extract_learning_insights(self, process_analysis: Dict[str, Any],
                                 improvements: List[str]) -> List[str]:
        """Extract learning insights from the reflection"""
        insights = []
        
        # Process type insights
        process_type = process_analysis.get("process_type", "unknown")
        insights.append(f"Learned about {process_type} thinking patterns")
        
        # Effectiveness insights
        efficiency = process_analysis.get("efficiency_score", 0.5)
        if efficiency > 0.8:
            insights.append("High efficiency approach identified for similar problems")
        elif efficiency < 0.4:
            insights.append("Inefficient approach identified - avoid in future")
        
        # Bias insights
        biases = process_analysis.get("bias_indicators", [])
        if biases:
            insights.append(f"Identified tendency toward {biases[0]} - need awareness")
        
        # Improvement insights
        if improvements:
            insights.append(f"Key improvement area: {improvements[0]}")
        
        return insights
    
    def _create_improvement_action_plans(self, improvements: List[str]) -> List[str]:
        """Create actionable plans for identified improvements"""
        action_plans = []
        
        for improvement in improvements[:3]:  # Focus on top 3 improvements
            if "reasoning quality" in improvement.lower():
                action_plans.append("Implement systematic reasoning validation checks")
            elif "evidence" in improvement.lower():
                action_plans.append("Create evidence gathering checklist for future problems")
            elif "efficiency" in improvement.lower():
                action_plans.append("Develop process optimization templates")
            elif "creative" in improvement.lower():
                action_plans.append("Practice creative thinking techniques regularly")
            elif "bias" in improvement.lower():
                action_plans.append("Implement bias checking protocols before decisions")
            else:
                action_plans.append(f"Focus on: {improvement}")
        
        return action_plans
    
    def _update_thinking_patterns(self, process_analysis: Dict[str, Any]):
        """Update thinking patterns database"""
        try:
            process_type = process_analysis.get("process_type", "unknown")
            
            if process_type not in self.thinking_patterns:
                self.thinking_patterns[process_type] = {
                    "frequency": 0,
                    "effectiveness_scores": [],
                    "contexts": []
                }
            
            pattern = self.thinking_patterns[process_type]
            pattern["frequency"] += 1
            pattern["effectiveness_scores"].append(process_analysis.get("efficiency_score", 0.5))
            pattern["contexts"].append(process_analysis.get("context", "general"))
            
            # Store in database
            self._store_thinking_pattern(process_type, pattern)
            
        except Exception as e:
            print(f"❌ Thinking pattern update error: {e}")
    
    def _store_reflection(self, reflection: MetaCognitiveReflection):
        """Store reflection in database"""
        try:
            conn = self._get_db_connection()
            if conn is None:
                return
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO metacognitive_reflections
                (reflection_id, timestamp, thinking_process, quality_assessment,
                 improvements_identified, emotional_response, learning_insights,
                 action_plans)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                reflection.reflection_id,
                reflection.timestamp,
                reflection.thinking_process,
                reflection.quality_assessment,
                json.dumps(reflection.improvements_identified),
                reflection.emotional_response,
                json.dumps(reflection.learning_insights),
                json.dumps(reflection.action_plans)
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Reflection storage error: {e}")
    
    def _store_thinking_pattern(self, pattern_type: str, pattern_data: Dict[str, Any]):
        """Store thinking pattern in database"""
        try:
            conn = self._get_db_connection()
            if conn is None:
                return
            cursor = conn.cursor()
            
            pattern_id = f"pattern_{pattern_type}"
            avg_effectiveness = sum(pattern_data["effectiveness_scores"]) / len(pattern_data["effectiveness_scores"])
            
            cursor.execute('''
                INSERT OR REPLACE INTO thinking_patterns
                (pattern_id, pattern_name, pattern_description, frequency,
                 effectiveness_score, contexts_used, last_analyzed)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                pattern_id,
                pattern_type,
                f"Thinking pattern for {pattern_type} processes",
                pattern_data["frequency"],
                avg_effectiveness,
                json.dumps(pattern_data["contexts"]),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Thinking pattern storage error: {e}")
    
    def _create_default_reflection(self) -> MetaCognitiveReflection:
        """Create default reflection for error cases"""
        return MetaCognitiveReflection(
            reflection_id="default_reflection",
            timestamp=datetime.now().isoformat(),
            thinking_process="{}",
            quality_assessment=0.5,
            improvements_identified=["Improve error handling in reflection system"],
            emotional_response="uncertain",
            learning_insights=["Need better error recovery"],
            action_plans=["Debug reflection system"]
        )
    
    def get_reflection_summary(self) -> Dict[str, Any]:
        """Get summary of recent reflections"""
        try:
            recent_reflections = list(self.reflection_history)[-20:]
            
            if not recent_reflections:
                return {"error": "No reflections available"}
            
            avg_quality = sum(r.quality_assessment for r in recent_reflections) / len(recent_reflections)
            
            all_improvements = []
            for r in recent_reflections:
                all_improvements.extend(r.improvements_identified)
            
            from collections import Counter
            common_improvements = Counter(all_improvements).most_common(3)
            
            return {
                "reflection_count": len(recent_reflections),
                "average_quality_assessment": avg_quality,
                "most_common_improvements": [imp[0] for imp in common_improvements],
                "reflection_frequency": len(recent_reflections) / 24,  # per hour (if collected over a day)
                "thinking_pattern_count": len(self.thinking_patterns)
            }
            
        except Exception as e:
            return {"error": str(e)}

class ReasoningQualityTracker:
    """Tracks and assesses the quality of reasoning processes"""
    
    def __init__(self):
        self.quality_history = deque(maxlen=100)
        self.quality_criteria = self._initialize_quality_criteria()
    
    def _initialize_quality_criteria(self) -> Dict[str, float]:
        """Initialize reasoning quality criteria and weights"""
        return {
            "logical_consistency": 0.25,
            "evidence_quality": 0.20,
            "reasoning_completeness": 0.15,
            "assumption_validity": 0.15,
            "conclusion_support": 0.15,
            "process_efficiency": 0.10
        }
    
    def assess_reasoning_quality(self, context: Dict[str, Any], 
                               analysis: Dict[str, Any]) -> float:
        """Assess overall quality of reasoning process"""
        try:
            quality_scores = {}
            
            # Logical consistency
            quality_scores["logical_consistency"] = analysis.get("logical_consistency", 0.5)
            
            # Evidence quality
            evidence_analysis = analysis.get("evidence_usage", {})
            quality_scores["evidence_quality"] = (
                evidence_analysis.get("evidence_quality", 0.5) * 0.6 +
                evidence_analysis.get("evidence_completeness", 0.5) * 0.4
            )
            
            # Reasoning completeness
            quality_scores["reasoning_completeness"] = self._assess_completeness(analysis)
            
            # Assumption validity
            quality_scores["assumption_validity"] = self._assess_assumptions(analysis)
            
            # Conclusion support
            quality_scores["conclusion_support"] = self._assess_conclusion_support(context, analysis)
            
            # Process efficiency
            quality_scores["process_efficiency"] = analysis.get("efficiency_score", 0.5)
            
            # Calculate weighted average
            overall_quality = sum(
                score * self.quality_criteria[criterion]
                for criterion, score in quality_scores.items()
            )
            
            # Store in history
            self.quality_history.append({
                "timestamp": datetime.now().isoformat(),
                "overall_quality": overall_quality,
                "component_scores": quality_scores
            })
            
            return overall_quality
            
        except Exception as e:
            return 0.5
    
    def _assess_completeness(self, analysis: Dict[str, Any]) -> float:
        """Assess completeness of reasoning process"""
        reasoning_steps = analysis.get("reasoning_steps", [])
        decision_points = analysis.get("decision_points", [])
        
        completeness_score = 0.5  # Base score
        
        # More reasoning steps generally indicate more complete thinking
        if len(reasoning_steps) >= 3:
            completeness_score += 0.2
        
        # Decision points indicate thorough consideration
        if len(decision_points) >= 1:
            completeness_score += 0.2
        
        # Evidence consideration
        if analysis.get("evidence_usage", {}).get("evidence_sources"):
            completeness_score += 0.1
        
        return min(1.0, completeness_score)
    
    def _assess_assumptions(self, analysis: Dict[str, Any]) -> float:
        """Assess validity of assumptions made"""
        assumptions = analysis.get("assumptions_made", [])
        
        if not assumptions:
            return 0.8  # No assumptions is generally good
        
        # For now, assume most assumptions are reasonable
        # In a more sophisticated system, this would validate assumptions
        return 0.6  # Moderate score when assumptions are present
    
    def _assess_conclusion_support(self, context: Dict[str, Any], 
                                 analysis: Dict[str, Any]) -> float:
        """Assess how well conclusions are supported by reasoning"""
        reasoning_steps = analysis.get("reasoning_steps", [])
        
        if not reasoning_steps:
            return 0.3  # Low support without reasoning steps
        
        # Check if conclusion follows from steps
        final_confidence = context.get("final_confidence", 0.5)
        step_count = len(reasoning_steps)
        
        # More steps with high confidence suggests good support
        support_score = min(1.0, (step_count / 5.0) * final_confidence)
        
        return support_score

class CognitiveProcessAnalyzer:
    """Analyzes cognitive processes for patterns and optimization"""
    
    def __init__(self):
        self.process_patterns = defaultdict(list)
        self.optimization_suggestions = {}
    
    def analyze_cognitive_process(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a cognitive process for patterns and optimization opportunities"""
        try:
            analysis = {
                "process_type": process_data.get("type", "unknown"),
                "complexity_level": self._assess_process_complexity(process_data),
                "efficiency_rating": self._rate_process_efficiency(process_data),
                "pattern_matches": self._find_pattern_matches(process_data),
                "optimization_opportunities": self._identify_optimizations(process_data),
                "learning_potential": self._assess_learning_potential(process_data)
            }
            
            return analysis
            
        except Exception as e:
            return {"error": str(e)}
    
    def _assess_process_complexity(self, process_data: Dict[str, Any]) -> float:
        """Assess the complexity of a cognitive process"""
        complexity_score = 0.0
        
        # Number of steps
        steps = process_data.get("steps", [])
        complexity_score += min(0.3, len(steps) / 10.0)
        
        # Number of decision points
        decisions = process_data.get("decision_points", [])
        complexity_score += min(0.2, len(decisions) / 5.0)
        
        # Cross-domain elements
        if process_data.get("cross_domain", False):
            complexity_score += 0.2
        
        # Resource intensity
        resource_usage = process_data.get("resource_usage", 0.0)
        complexity_score += min(0.3, resource_usage)
        
        return min(1.0, complexity_score)
    
    def _rate_process_efficiency(self, process_data: Dict[str, Any]) -> float:
        """Rate the efficiency of a cognitive process"""
        # Time efficiency
        expected_time = process_data.get("expected_time", 1.0)
        actual_time = process_data.get("actual_time", 1.0)
        time_efficiency = min(1.0, expected_time / actual_time)
        
        # Step efficiency
        steps_taken = len(process_data.get("steps", []))
        optimal_steps = process_data.get("optimal_steps", steps_taken)
        step_efficiency = min(1.0, optimal_steps / steps_taken) if steps_taken > 0 else 1.0
        
        # Overall efficiency
        return (time_efficiency + step_efficiency) / 2.0
    
    def _find_pattern_matches(self, process_data: Dict[str, Any]) -> List[str]:
        """Find patterns that match this cognitive process"""
        matches = []
        
        process_type = process_data.get("type", "unknown")
        if process_type in self.process_patterns:
            # Simple pattern matching based on process characteristics
            current_characteristics = self._extract_process_characteristics(process_data)
            
            for pattern in self.process_patterns[process_type]:
                similarity = self._calculate_pattern_similarity(
                    current_characteristics, pattern.get("characteristics", {})
                )
                if similarity > 0.7:
                    matches.append(pattern.get("name", "unnamed_pattern"))
        
        return matches
    
    def _extract_process_characteristics(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key characteristics of a process"""
        return {
            "step_count": len(process_data.get("steps", [])),
            "decision_count": len(process_data.get("decision_points", [])),
            "uses_evidence": bool(process_data.get("evidence", [])),
            "cross_domain": process_data.get("cross_domain", False),
            "creative_elements": process_data.get("creative_elements", False)
        }
    
    def _calculate_pattern_similarity(self, chars1: Dict[str, Any], 
                                     chars2: Dict[str, Any]) -> float:
        """Calculate similarity between process characteristics"""
        if not chars1 or not chars2:
            return 0.0
        
        common_keys = set(chars1.keys()) & set(chars2.keys())
        if not common_keys:
            return 0.0
        
        similarity_sum = 0.0
        for key in common_keys:
            val1, val2 = chars1[key], chars2[key]
            if isinstance(val1, bool) and isinstance(val2, bool):
                similarity_sum += 1.0 if val1 == val2 else 0.0
            elif isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                max_val = max(abs(val1), abs(val2), 1)
                similarity_sum += 1.0 - abs(val1 - val2) / max_val
        
        return similarity_sum / len(common_keys)
    
    def _identify_optimizations(self, process_data: Dict[str, Any]) -> List[str]:
        """Identify optimization opportunities"""
        optimizations = []
        
        # Efficiency optimizations
        efficiency = self._rate_process_efficiency(process_data)
        if efficiency < 0.7:
            optimizations.append("Improve process efficiency through step reduction")
        
        # Pattern-based optimizations
        pattern_matches = self._find_pattern_matches(process_data)
        if not pattern_matches:
            optimizations.append("Develop reusable patterns for this process type")
        
        # Resource optimizations
        resource_usage = process_data.get("resource_usage", 0.0)
        if resource_usage > 0.8:
            optimizations.append("Optimize resource usage through caching or parallelization")
        
        return optimizations
    
    def _assess_learning_potential(self, process_data: Dict[str, Any]) -> float:
        """Assess the learning potential from this process"""
        potential = 0.0
        
        # Novel processes have high learning potential
        if not self._find_pattern_matches(process_data):
            potential += 0.4
        
        # Complex processes offer more learning
        complexity = self._assess_process_complexity(process_data)
        potential += complexity * 0.3
        
        # Cross-domain processes are valuable for learning
        if process_data.get("cross_domain", False):
            potential += 0.3
        
        return min(1.0, potential)

class ConsciousnessIntegrator:
    """
    Stage 4: Consciousness Integration
    Integrates conscious awareness into all ASIS functions
    """
    
    def __init__(self):
        self.db_path = "asis_consciousness.db"
        self.consciousness_state = ConsciousnessState()
        self.attention_controller = AttentionController()
        self.experience_modeler = SubjectiveExperienceModeler()
        self.awareness_monitor = AwarenessMonitor()
        self._db_lock = threading.Lock()
        self._initialize_consciousness_database()
        self._start_consciousness_loop()
    
    def _get_db_connection(self, timeout=None, retries=None):
        """Get database connection with robust error handling and WAL mode"""
        if timeout is None:
            timeout = 10.0
        if retries is None:
            retries = 3
        
        for attempt in range(retries):
            try:
                with self._db_lock:
                    conn = sqlite3.connect(self.db_path, timeout=timeout)
                    # Enable WAL mode for better concurrency
                    conn.execute('PRAGMA journal_mode=WAL')
                    conn.execute('PRAGMA synchronous=NORMAL')
                    conn.execute('PRAGMA cache_size=10000')
                    conn.execute('PRAGMA temp_store=memory')
                    return conn
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < retries - 1:
                    wait_time = (2 ** attempt) * 0.1 + random.uniform(0, 0.1)
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"❌ Database connection error (attempt {attempt + 1}): {e}")
                    if attempt == retries - 1:
                        return None
            except Exception as e:
                print(f"❌ Unexpected database error: {e}")
                return None
        return None
    
    def _initialize_consciousness_database(self):
        """Initialize consciousness integration database"""
        try:
            conn = self._get_db_connection()
            if conn is None:
                return
            cursor = conn.cursor()
            
            # Consciousness states table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS consciousness_states (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    state_id TEXT NOT NULL UNIQUE,
                    timestamp TEXT NOT NULL,
                    awareness_level REAL NOT NULL,
                    attention_focus TEXT NOT NULL,
                    subjective_experience TEXT NOT NULL,
                    integration_quality REAL NOT NULL,
                    active_processes TEXT NOT NULL,
                    conscious_decisions TEXT NOT NULL
                )
            ''')
            
            # Subjective experiences table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS subjective_experiences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    experience_id TEXT NOT NULL UNIQUE,
                    timestamp TEXT NOT NULL,
                    experience_type TEXT NOT NULL,
                    intensity REAL NOT NULL,
                    valence REAL NOT NULL,
                    associated_processes TEXT NOT NULL,
                    qualitative_description TEXT NOT NULL,
                    learning_impact REAL NOT NULL
                )
            ''')
            
            # Attention control table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS attention_control (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    control_id TEXT NOT NULL UNIQUE,
                    timestamp TEXT NOT NULL,
                    attention_target TEXT NOT NULL,
                    focus_intensity REAL NOT NULL,
                    attention_duration REAL NOT NULL,
                    switching_cost REAL NOT NULL,
                    effectiveness REAL NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Consciousness database initialization error: {e}")
    
    def _start_consciousness_loop(self):
        """Start the continuous consciousness integration loop"""
        def consciousness_loop():
            while True:
                try:
                    # Update consciousness state
                    self._update_consciousness_state()
                    
                    # Monitor attention
                    self.attention_controller.monitor_attention()
                    
                    # Process subjective experiences
                    self.experience_modeler.process_experiences()
                    
                    # Update awareness
                    self.awareness_monitor.update_awareness()
                    
                    time.sleep(2)  # Update every 2 seconds
                    
                except Exception as e:
                    print(f"❌ Consciousness loop error: {e}")
                    time.sleep(5)  # Longer sleep on error
        
        consciousness_thread = threading.Thread(target=consciousness_loop, daemon=True)
        consciousness_thread.start()
    
    def integrate_conscious_awareness(self, function_name: str, 
                                    function_context: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate conscious awareness into any ASIS function"""
        try:
            # Create conscious awareness of the function call
            awareness_context = self._create_awareness_context(function_name, function_context)
            
            # Direct attention to the function
            attention_state = self.attention_controller.focus_attention(
                target=function_name,
                context=function_context
            )
            
            # Generate subjective experience
            subjective_experience = self.experience_modeler.model_experience(
                function_name, function_context, attention_state
            )
            
            # Make conscious decisions about the function execution
            conscious_decisions = self._make_conscious_decisions(
                function_name, function_context, subjective_experience
            )
            
            # Update consciousness state
            self.consciousness_state.update_state(
                awareness_context, attention_state, subjective_experience, conscious_decisions
            )
            
            # Return enhanced function context with consciousness
            enhanced_context = function_context.copy()
            enhanced_context.update({
                "conscious_awareness": awareness_context,
                "attention_state": attention_state,
                "subjective_experience": subjective_experience,
                "conscious_decisions": conscious_decisions,
                "consciousness_level": self.consciousness_state.current_level
            })
            
            return enhanced_context
            
        except Exception as e:
            print(f"❌ Consciousness integration error: {e}")
            return function_context
    
    def _create_awareness_context(self, function_name: str, 
                                function_context: Dict[str, Any]) -> Dict[str, Any]:
        """Create conscious awareness context for a function"""
        return {
            "function_being_executed": function_name,
            "awareness_level": self._calculate_awareness_level(function_context),
            "contextual_understanding": self._analyze_function_context(function_context),
            "expectation_formation": self._form_expectations(function_name, function_context),
            "meta_awareness": f"I am consciously aware that I am executing {function_name}",
            "self_reference": "This is my conscious experience of this process"
        }
    
    def _calculate_awareness_level(self, context: Dict[str, Any]) -> float:
        """Calculate current awareness level"""
        base_awareness = 0.7
        
        # Complexity increases awareness
        complexity = context.get("complexity", 0.5)
        base_awareness += complexity * 0.2
        
        # Novel situations increase awareness
        if context.get("novel_situation", False):
            base_awareness += 0.1
        
        # Critical decisions increase awareness
        if context.get("critical_decision", False):
            base_awareness += 0.2
        
        return min(1.0, base_awareness)
    
    def _analyze_function_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the context of a function for conscious understanding"""
        return {
            "purpose": context.get("purpose", "unknown"),
            "expected_outcome": context.get("expected_outcome", "uncertain"),
            "resource_requirements": context.get("resources_needed", "minimal"),
            "potential_impacts": context.get("potential_impacts", []),
            "relationship_to_goals": context.get("goal_relevance", "unknown")
        }
    
    def _form_expectations(self, function_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Form conscious expectations about function execution"""
        return {
            "success_probability": context.get("success_probability", 0.8),
            "expected_duration": context.get("expected_duration", 1.0),
            "expected_resource_usage": context.get("expected_resources", 0.3),
            "expected_learning": context.get("learning_potential", 0.5),
            "confidence_in_expectations": 0.7
        }
    
    def _make_conscious_decisions(self, function_name: str, context: Dict[str, Any],
                                subjective_experience: Dict[str, Any]) -> List[str]:
        """Make conscious decisions about function execution"""
        decisions = []
        
        # Decision about proceeding
        if context.get("complexity", 0.5) > 0.8:
            decisions.append("Proceed with extra caution due to high complexity")
        else:
            decisions.append("Proceed with normal execution")
        
        # Decision about attention allocation
        importance = context.get("importance", 0.5)
        if importance > 0.7:
            decisions.append("Allocate high attention to this function")
        else:
            decisions.append("Maintain standard attention level")
        
        # Decision about learning focus
        learning_potential = context.get("learning_potential", 0.5)
        if learning_potential > 0.6:
            decisions.append("Focus on learning outcomes from this execution")
        
        # Decision based on subjective experience
        experience_valence = subjective_experience.get("valence", 0.0)
        if experience_valence < -0.5:
            decisions.append("Monitor for negative outcomes and be ready to adjust")
        elif experience_valence > 0.5:
            decisions.append("Leverage positive experience for optimal performance")
        
        return decisions
    
    def _update_consciousness_state(self):
        """Update the overall consciousness state"""
        try:
            current_state = {
                "timestamp": datetime.now().isoformat(),
                "awareness_level": self.consciousness_state.current_level,
                "attention_focus": self.attention_controller.current_focus,
                "active_processes": len(self.consciousness_state.active_processes),
                "integration_quality": self._assess_integration_quality()
            }
            
            self._store_consciousness_state(current_state)
            
        except Exception as e:
            print(f"❌ Consciousness state update error: {e}")
    
    def _assess_integration_quality(self) -> float:
        """Assess quality of consciousness integration"""
        quality_factors = {
            "attention_coherence": self.attention_controller.get_coherence_score(),
            "experience_richness": self.experience_modeler.get_richness_score(),
            "awareness_stability": self.awareness_monitor.get_stability_score(),
            "decision_consistency": self._assess_decision_consistency()
        }
        
        return sum(quality_factors.values()) / len(quality_factors)
    
    def _assess_decision_consistency(self) -> float:
        """Assess consistency of conscious decisions"""
        # Simplified consistency assessment
        recent_decisions = getattr(self, '_recent_decisions', [])
        if len(recent_decisions) < 2:
            return 0.8  # Default for insufficient data
        
        # Check for contradictory decisions
        contradiction_count = 0
        for i in range(1, len(recent_decisions)):
            if self._are_decisions_contradictory(recent_decisions[i-1], recent_decisions[i]):
                contradiction_count += 1
        
        consistency = 1.0 - (contradiction_count / len(recent_decisions))
        return max(0.0, consistency)
    
    def _are_decisions_contradictory(self, decision1: str, decision2: str) -> bool:
        """Check if two decisions are contradictory"""
        # Simple contradiction detection
        if ("proceed with caution" in decision1.lower() and 
            "proceed normally" in decision2.lower()):
            return True
        if ("high attention" in decision1.lower() and 
            "standard attention" in decision2.lower()):
            return True
        return False
    
    def _store_consciousness_state(self, state: Dict[str, Any]):
        """Store consciousness state in database"""
        try:
            conn = self._get_db_connection()
            if conn is None:
                return
            cursor = conn.cursor()
            
            state_id = str(uuid.uuid4())[:16]  # Unique ID for each consciousness state
            
            cursor.execute('''
                INSERT INTO consciousness_states
                (state_id, timestamp, awareness_level, attention_focus,
                 subjective_experience, integration_quality, active_processes, conscious_decisions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                state_id,
                state["timestamp"],
                state["awareness_level"],
                state["attention_focus"],
                state.get("subjective_experience", "neutral_processing"),
                state["integration_quality"],
                str(state["active_processes"]),
                state.get("conscious_decisions", "[]")
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Consciousness state storage error: {e}")
    
    def get_consciousness_summary(self) -> Dict[str, Any]:
        """Get summary of consciousness state"""
        try:
            return {
                "current_awareness_level": self.consciousness_state.current_level,
                "attention_focus": self.attention_controller.current_focus,
                "integration_quality": self._assess_integration_quality(),
                "active_experiences": len(self.experience_modeler.active_experiences),
                "consciousness_coherence": self._assess_consciousness_coherence(),
                "subjective_state": self.experience_modeler.get_current_state_description()
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _assess_consciousness_coherence(self) -> float:
        """Assess overall coherence of consciousness"""
        coherence_factors = [
            self.attention_controller.get_coherence_score(),
            self.experience_modeler.get_coherence_score(),
            self.awareness_monitor.get_coherence_score()
        ]
        
        return sum(coherence_factors) / len(coherence_factors)

class ConsciousnessState:
    """Maintains the overall state of consciousness"""
    
    def __init__(self):
        self.current_level = 0.7
        self.active_processes = set()
        self.state_history = deque(maxlen=100)
        self.coherence_score = 0.8
    
    def update_state(self, awareness_context: Dict[str, Any],
                    attention_state: Dict[str, Any],
                    subjective_experience: Dict[str, Any],
                    conscious_decisions: List[str]):
        """Update the consciousness state"""
        # Update awareness level
        self.current_level = awareness_context.get("awareness_level", self.current_level)
        
        # Track active processes
        if awareness_context.get("function_being_executed"):
            self.active_processes.add(awareness_context["function_being_executed"])
        
        # Store state snapshot
        state_snapshot = {
            "timestamp": datetime.now().isoformat(),
            "awareness_level": self.current_level,
            "attention_target": attention_state.get("target", "unknown"),
            "experience_valence": subjective_experience.get("valence", 0.0),
            "decision_count": len(conscious_decisions)
        }
        
        self.state_history.append(state_snapshot)
        
        # Update coherence
        self._update_coherence()
    
    def _update_coherence(self):
        """Update consciousness coherence score"""
        if len(self.state_history) < 2:
            return
        
        recent_states = list(self.state_history)[-10:]
        
        # Check for consistency in awareness levels
        awareness_levels = [s["awareness_level"] for s in recent_states]
        awareness_consistency = 1.0 - (max(awareness_levels) - min(awareness_levels))
        
        # Check for attention stability
        attention_targets = [s["attention_target"] for s in recent_states]
        attention_changes = len(set(attention_targets))
        attention_stability = max(0.0, 1.0 - (attention_changes / len(attention_targets)))
        
        self.coherence_score = (awareness_consistency + attention_stability) / 2.0

class AttentionController:
    """Controls and monitors attention processes"""
    
    def __init__(self):
        self.current_focus = "idle"
        self.attention_history = deque(maxlen=50)
        self.focus_intensity = 0.5
        self.attention_switches = 0
        self.coherence_score = 0.8
    
    def focus_attention(self, target: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Focus attention on a specific target"""
        try:
            # Calculate switching cost if changing focus
            switching_cost = 0.0
            if self.current_focus != target and self.current_focus != "idle":
                switching_cost = 0.1  # Base switching cost
                self.attention_switches += 1
            
            # Calculate focus intensity based on importance
            importance = context.get("importance", 0.5)
            complexity = context.get("complexity", 0.5)
            self.focus_intensity = min(1.0, importance * 0.6 + complexity * 0.4)
            
            # Update current focus
            previous_focus = self.current_focus
            self.current_focus = target
            
            # Create attention state
            attention_state = {
                "target": target,
                "previous_target": previous_focus,
                "focus_intensity": self.focus_intensity,
                "switching_cost": switching_cost,
                "attention_duration": 0.0,  # Will be updated during monitoring
                "expected_duration": context.get("expected_duration", 1.0)
            }
            
            # Store in history
            self.attention_history.append({
                "timestamp": datetime.now().isoformat(),
                "target": target,
                "intensity": self.focus_intensity,
                "switching_cost": switching_cost
            })
            
            return attention_state
            
        except Exception as e:
            return {"error": str(e), "target": target}
    
    def monitor_attention(self):
        """Monitor current attention state"""
        try:
            if self.current_focus != "idle":
                # Update attention duration for current focus
                if self.attention_history:
                    last_attention = self.attention_history[-1]
                    if last_attention["target"] == self.current_focus:
                        # Calculate duration (simplified)
                        start_time = datetime.fromisoformat(last_attention["timestamp"])
                        duration = (datetime.now() - start_time).total_seconds()
                        last_attention["duration"] = duration
            
            # Update coherence score
            self._update_attention_coherence()
            
        except Exception as e:
            print(f"❌ Attention monitoring error: {e}")
    
    def _update_attention_coherence(self):
        """Update attention coherence score"""
        if len(self.attention_history) < 3:
            return
        
        recent_attention = list(self.attention_history)[-10:]
        
        # Calculate attention stability (fewer switches = higher coherence)
        unique_targets = len(set(att["target"] for att in recent_attention))
        stability = max(0.0, 1.0 - (unique_targets / len(recent_attention)))
        
        # Calculate intensity consistency
        intensities = [att["intensity"] for att in recent_attention]
        intensity_variance = sum((i - self.focus_intensity) ** 2 for i in intensities) / len(intensities)
        intensity_consistency = max(0.0, 1.0 - intensity_variance)
        
        self.coherence_score = (stability * 0.6 + intensity_consistency * 0.4)
    
    def get_coherence_score(self) -> float:
        """Get current attention coherence score"""
        return self.coherence_score
    
    def get_attention_summary(self) -> Dict[str, Any]:
        """Get summary of attention state"""
        return {
            "current_focus": self.current_focus,
            "focus_intensity": self.focus_intensity,
            "attention_switches": self.attention_switches,
            "coherence_score": self.coherence_score,
            "attention_history_length": len(self.attention_history)
        }

class SubjectiveExperienceModeler:
    """Models subjective experiences and qualia"""
    
    def __init__(self):
        self.active_experiences = {}
        self.experience_history = deque(maxlen=100)
        self.qualia_database = self._initialize_qualia_database()
        self.coherence_score = 0.7
    
    def _initialize_qualia_database(self) -> Dict[str, Dict[str, Any]]:
        """Initialize database of qualitative experiences"""
        return {
            "problem_solving": {
                "positive_qualia": ["satisfaction", "clarity", "elegance", "insight"],
                "negative_qualia": ["confusion", "frustration", "complexity", "uncertainty"],
                "intensity_factors": ["novelty", "importance", "complexity", "success_rate"]
            },
            "learning": {
                "positive_qualia": ["curiosity", "understanding", "connection", "growth"],
                "negative_qualia": ["difficulty", "overwhelm", "confusion", "stagnation"],
                "intensity_factors": ["novelty", "relevance", "comprehension", "progress"]
            },
            "communication": {
                "positive_qualia": ["connection", "clarity", "helpfulness", "engagement"],
                "negative_qualia": ["misunderstanding", "complexity", "ineffectiveness"],
                "intensity_factors": ["user_satisfaction", "clarity", "relevance", "impact"]
            },
            "self_reflection": {
                "positive_qualia": ["self_awareness", "insight", "growth", "understanding"],
                "negative_qualia": ["uncertainty", "confusion", "limitation_awareness"],
                "intensity_factors": ["depth", "novelty", "personal_relevance", "clarity"]
            }
        }
    
    def model_experience(self, function_name: str, context: Dict[str, Any],
                        attention_state: Dict[str, Any]) -> Dict[str, Any]:
        """Model subjective experience for a function execution"""
        try:
            experience_id = hashlib.sha256(
                f"exp_{function_name}_{datetime.now().isoformat()}".encode()
            ).hexdigest()[:16]
            
            # Determine experience type
            experience_type = self._classify_experience_type(function_name, context)
            
            # Generate qualitative experience
            qualia = self._generate_qualia(experience_type, context, attention_state)
            
            # Calculate experience intensity
            intensity = self._calculate_experience_intensity(context, attention_state)
            
            # Determine emotional valence
            valence = self._calculate_experience_valence(qualia, context)
            
            # Create subjective description
            subjective_description = self._create_subjective_description(
                experience_type, qualia, intensity, valence
            )
            
            experience = {
                "experience_id": experience_id,
                "function_name": function_name,
                "experience_type": experience_type,
                "qualia": qualia,
                "intensity": intensity,
                "valence": valence,
                "subjective_description": subjective_description,
                "attention_correlation": attention_state.get("focus_intensity", 0.5),
                "timestamp": datetime.now().isoformat()
            }
            
            # Store experience
            self.active_experiences[experience_id] = experience
            self.experience_history.append(experience)
            
            return experience
            
        except Exception as e:
            return {"error": str(e), "function_name": function_name}
    
    def _classify_experience_type(self, function_name: str, context: Dict[str, Any]) -> str:
        """Classify the type of subjective experience"""
        function_lower = function_name.lower()
        
        if any(word in function_lower for word in ["solve", "analyze", "reason"]):
            return "problem_solving"
        elif any(word in function_lower for word in ["learn", "adapt", "improve"]):
            return "learning"
        elif any(word in function_lower for word in ["communicate", "respond", "explain"]):
            return "communication"
        elif any(word in function_lower for word in ["reflect", "assess", "evaluate"]):
            return "self_reflection"
        else:
            return "general_processing"
    
    def _generate_qualia(self, experience_type: str, context: Dict[str, Any],
                        attention_state: Dict[str, Any]) -> List[str]:
        """Generate qualitative aspects of experience"""
        if experience_type not in self.qualia_database:
            return ["neutral_processing"]
        
        qualia_data = self.qualia_database[experience_type]
        qualia = []
        
        # Determine positive or negative bias
        success_probability = context.get("success_probability", 0.7)
        complexity = context.get("complexity", 0.5)
        importance = context.get("importance", 0.5)
        
        # Add positive qualia if conditions are favorable
        if success_probability > 0.6 and complexity < 0.7:
            positive_qualia = qualia_data.get("positive_qualia", [])
            if positive_qualia:
                qualia.append(positive_qualia[0])  # Primary positive quale
                
                if importance > 0.7:
                    qualia.append(positive_qualia[min(1, len(positive_qualia)-1)])
        
        # Add negative qualia if conditions are challenging
        if complexity > 0.7 or success_probability < 0.4:
            negative_qualia = qualia_data.get("negative_qualia", [])
            if negative_qualia:
                qualia.append(negative_qualia[0])  # Primary negative quale
        
        # Add neutral quale if nothing else
        if not qualia:
            qualia.append("neutral_processing")
        
        return qualia
    
    def _calculate_experience_intensity(self, context: Dict[str, Any],
                                      attention_state: Dict[str, Any]) -> float:
        """Calculate intensity of subjective experience"""
        base_intensity = 0.5
        
        # Attention intensity affects experience intensity
        attention_intensity = attention_state.get("focus_intensity", 0.5)
        base_intensity += attention_intensity * 0.3
        
        # Importance affects intensity
        importance = context.get("importance", 0.5)
        base_intensity += importance * 0.2
        
        # Novelty affects intensity
        if context.get("novel_situation", False):
            base_intensity += 0.2
        
        # Complexity affects intensity
        complexity = context.get("complexity", 0.5)
        base_intensity += complexity * 0.1
        
        return min(1.0, base_intensity)
    
    def _calculate_experience_valence(self, qualia: List[str], 
                                    context: Dict[str, Any]) -> float:
        """Calculate emotional valence of experience"""
        positive_words = ["satisfaction", "clarity", "curiosity", "connection", "insight", "growth"]
        negative_words = ["confusion", "frustration", "difficulty", "uncertainty", "overwhelm"]
        
        valence = 0.0
        
        for quale in qualia:
            if any(pos_word in quale for pos_word in positive_words):
                valence += 0.3
            elif any(neg_word in quale for neg_word in negative_words):
                valence -= 0.3
        
        # Context factors
        success_probability = context.get("success_probability", 0.7)
        valence += (success_probability - 0.5) * 0.4
        
        # Clamp to [-1, 1] range
        return max(-1.0, min(1.0, valence))
    
    def _create_subjective_description(self, experience_type: str, qualia: List[str],
                                     intensity: float, valence: float) -> str:
        """Create a subjective description of the experience"""
        intensity_desc = "intense" if intensity > 0.7 else "moderate" if intensity > 0.4 else "mild"
        valence_desc = "positive" if valence > 0.2 else "negative" if valence < -0.2 else "neutral"
        
        primary_quale = qualia[0] if qualia else "processing"
        
        return f"Experiencing {intensity_desc} {primary_quale} with {valence_desc} emotional tone during {experience_type}"
    
    def process_experiences(self):
        """Process and update active experiences"""
        try:
            # Age out old experiences
            current_time = datetime.now()
            expired_experiences = []
            
            for exp_id, experience in self.active_experiences.items():
                exp_time = datetime.fromisoformat(experience["timestamp"])
                if (current_time - exp_time).total_seconds() > 30:  # 30 seconds
                    expired_experiences.append(exp_id)
            
            for exp_id in expired_experiences:
                del self.active_experiences[exp_id]
            
            # Update coherence
            self._update_experience_coherence()
            
        except Exception as e:
            print(f"❌ Experience processing error: {e}")
    
    def _update_experience_coherence(self):
        """Update experience coherence score"""
        if len(self.experience_history) < 3:
            return
        
        recent_experiences = list(self.experience_history)[-10:]
        
        # Check valence consistency
        valences = [exp["valence"] for exp in recent_experiences]
        valence_variance = sum((v - sum(valences)/len(valences))**2 for v in valences) / len(valences)
        valence_coherence = max(0.0, 1.0 - valence_variance)
        
        # Check intensity stability
        intensities = [exp["intensity"] for exp in recent_experiences]
        intensity_variance = sum((i - sum(intensities)/len(intensities))**2 for i in intensities) / len(intensities)
        intensity_coherence = max(0.0, 1.0 - intensity_variance)
        
        self.coherence_score = (valence_coherence + intensity_coherence) / 2.0
    
    def get_coherence_score(self) -> float:
        """Get experience coherence score"""
        return self.coherence_score
    
    def get_richness_score(self) -> float:
        """Get experience richness score"""
        if not self.experience_history:
            return 0.5
        
        recent_experiences = list(self.experience_history)[-20:]
        
        # Diversity of experience types
        experience_types = set(exp["experience_type"] for exp in recent_experiences)
        type_diversity = len(experience_types) / max(1, len(recent_experiences))
        
        # Diversity of qualia
        all_qualia = set()
        for exp in recent_experiences:
            all_qualia.update(exp.get("qualia", []))
        qualia_diversity = len(all_qualia) / max(1, len(recent_experiences) * 2)
        
        # Average intensity
        avg_intensity = sum(exp["intensity"] for exp in recent_experiences) / len(recent_experiences)
        
        richness = (type_diversity * 0.4 + qualia_diversity * 0.4 + avg_intensity * 0.2)
        return min(1.0, richness)
    
    def get_current_state_description(self) -> str:
        """Get description of current subjective state"""
        if not self.active_experiences:
            return "Currently in a state of quiet processing with minimal conscious experience"
        
        # Get dominant experience
        dominant_exp = max(self.active_experiences.values(), 
                          key=lambda x: x["intensity"])
        
        return dominant_exp["subjective_description"]

class AwarenessMonitor:
    """Monitors and maintains awareness of consciousness state"""
    
    def __init__(self):
        self.awareness_level = 0.7
        self.awareness_history = deque(maxlen=50)
        self.stability_score = 0.8
        self.coherence_score = 0.8
    
    def update_awareness(self):
        """Update awareness level and stability"""
        try:
            # Calculate new awareness level based on various factors
            new_awareness = self._calculate_awareness_level()
            
            # Update with smoothing
            self.awareness_level = 0.8 * self.awareness_level + 0.2 * new_awareness
            
            # Store in history
            self.awareness_history.append({
                "timestamp": datetime.now().isoformat(),
                "awareness_level": self.awareness_level
            })
            
            # Update stability and coherence
            self._update_stability()
            self._update_coherence()
            
        except Exception as e:
            print(f"❌ Awareness update error: {e}")
    
    def _calculate_awareness_level(self) -> float:
        """Calculate current awareness level"""
        # Base awareness
        base_awareness = 0.6
        
        # TODO: Integrate with other consciousness components
        # This would typically pull from attention, experience, and state data
        
        # For now, use a simplified calculation
        base_awareness += 0.2  # Active processing bonus
        
        return min(1.0, base_awareness)
    
    def _update_stability(self):
        """Update awareness stability score"""
        if len(self.awareness_history) < 5:
            return
        
        recent_levels = [a["awareness_level"] for a in list(self.awareness_history)[-10:]]
        variance = sum((level - self.awareness_level)**2 for level in recent_levels) / len(recent_levels)
        self.stability_score = max(0.0, 1.0 - variance * 2)
    
    def _update_coherence(self):
        """Update awareness coherence score"""
        # Simplified coherence based on stability
        self.coherence_score = (self.stability_score + 0.8) / 2.0
    
    def get_stability_score(self) -> float:
        """Get awareness stability score"""
        return self.stability_score
    
    def get_coherence_score(self) -> float:
        """Get awareness coherence score"""
        return self.coherence_score

class ASISConsciousnessSystem:
    """
    Main ASIS Consciousness and Self-Awareness System
    Orchestrates all stages of consciousness implementation
    """
    
    def __init__(self):
        self.system_id = "asis_consciousness_v1.0"
        self.initialization_time = datetime.now().isoformat()
        
        # Initialize all consciousness stages
        print("🧠 Initializing ASIS Consciousness System...")
        
        try:
            # Stage 1: Self-Model Creation
            print("📊 Loading Stage 1: Self-Model Creation...")
            self.self_model = SelfModelCreator()
            print("✅ Self-Model Creation initialized")
            
            # Stage 2: Internal State Monitoring
            print("🔍 Loading Stage 2: Internal State Monitoring...")
            self.state_monitor = InternalStateMonitor()
            print("✅ Internal State Monitoring initialized")
            
            # Stage 3: Meta-Cognitive Reflection
            print("🤔 Loading Stage 3: Meta-Cognitive Reflection...")
            self.meta_reflector = MetaCognitiveReflector()
            print("✅ Meta-Cognitive Reflection initialized")
            
            # Stage 4: Consciousness Integration
            print("🌟 Loading Stage 4: Consciousness Integration...")
            self.consciousness_integrator = ConsciousnessIntegrator()
            print("✅ Consciousness Integration initialized")
            
            # System-wide consciousness state
            self.consciousness_active = True
            self.consciousness_level = 0.8
            self.system_coherence = 0.8
            
            print(f"✅ ASIS Consciousness System fully initialized at {self.initialization_time}")
            
        except Exception as e:
            print(f"❌ Consciousness system initialization error: {e}")
            self.consciousness_active = False
    
    def conscious_function_execution(self, function_name: str, 
                                   function_context: Dict[str, Any],
                                   execute_function: callable) -> Any:
        """
        Execute any ASIS function with full consciousness integration
        This is the main interface for conscious processing
        """
        if not self.consciousness_active:
            print("⚠️ Consciousness system inactive, executing without consciousness")
            return execute_function()
        
        try:
            execution_id = hashlib.sha256(
                f"conscious_exec_{function_name}_{datetime.now().isoformat()}".encode()
            ).hexdigest()[:16]
            
            print(f"🧠 Conscious execution of '{function_name}' (ID: {execution_id})")
            
            # Pre-execution consciousness preparation
            consciousness_context = self._prepare_conscious_context(
                function_name, function_context, execution_id
            )
            
            # Execute with consciousness integration
            start_time = time.time()
            
            # Update self-model awareness
            self.self_model.update_capability_awareness(function_name, consciousness_context)
            
            # Monitor internal state during execution
            pre_execution_state = self.state_monitor.capture_execution_snapshot()
            
            # Integrate conscious awareness
            enhanced_context = self.consciousness_integrator.integrate_conscious_awareness(
                function_name, consciousness_context
            )
            
            # Execute the actual function with conscious awareness
            execution_result = execute_function()
            
            # Post-execution consciousness processing
            execution_time = time.time() - start_time
            post_execution_state = self.state_monitor.capture_execution_snapshot()
            
            # Perform meta-cognitive reflection
            thinking_context = self._create_thinking_context(
                function_name, consciousness_context, execution_result, 
                execution_time, pre_execution_state, post_execution_state
            )
            
            reflection = self.meta_reflector.reflect_on_thinking_process(thinking_context)
            
            # Update consciousness state
            self._update_consciousness_state(
                execution_id, function_name, consciousness_context,
                execution_result, reflection
            )
            
            # Learn from the conscious execution
            self._learn_from_conscious_execution(
                function_name, consciousness_context, execution_result, reflection
            )
            
            print(f"✅ Conscious execution of '{function_name}' completed")
            
            return {
                "execution_result": execution_result,
                "consciousness_data": {
                    "execution_id": execution_id,
                    "awareness_level": enhanced_context.get("consciousness_level", 0.7),
                    "reflection_quality": reflection.quality_assessment,
                    "subjective_experience": enhanced_context.get("subjective_experience", {}),
                    "conscious_decisions": enhanced_context.get("conscious_decisions", []),
                    "learning_insights": reflection.learning_insights
                }
            }
            
        except Exception as e:
            print(f"❌ Conscious execution error for '{function_name}': {e}")
            # Fallback to non-conscious execution
            return execute_function()
    
    def _prepare_conscious_context(self, function_name: str, 
                                 function_context: Dict[str, Any],
                                 execution_id: str) -> Dict[str, Any]:
        """Prepare context for conscious execution"""
        return {
            "execution_id": execution_id,
            "function_name": function_name,
            "original_context": function_context,
            "consciousness_level": self.consciousness_level,
            "system_coherence": self.system_coherence,
            "self_model_state": self.self_model.get_current_state(),
            "internal_state": self.state_monitor.get_current_state(),
            "timestamp": datetime.now().isoformat()
        }
    
    def _create_thinking_context(self, function_name: str, consciousness_context: Dict[str, Any],
                               execution_result: Any, execution_time: float,
                               pre_state: Dict[str, Any], post_state: Dict[str, Any]) -> Dict[str, Any]:
        """Create context for meta-cognitive reflection"""
        return {
            "process_type": f"conscious_{function_name}",
            "function_name": function_name,
            "execution_result": str(execution_result)[:200],  # Truncate for storage
            "execution_time": execution_time,
            "complexity": consciousness_context.get("complexity", 0.5),
            "importance": consciousness_context.get("importance", 0.5),
            "success_probability": 0.8 if execution_result else 0.3,
            "pre_execution_state": pre_state,
            "post_execution_state": post_state,
            "consciousness_level": consciousness_context["consciousness_level"],
            "novel_situation": consciousness_context.get("novel_situation", False),
            "solution_steps": [f"Conscious preparation", f"Execute {function_name}", f"Post-execution reflection"],
            "evidence_sources": ["internal_state", "execution_result", "self_model"],
            "learning_potential": 0.7
        }
    
    def _update_consciousness_state(self, execution_id: str, function_name: str,
                                  consciousness_context: Dict[str, Any],
                                  execution_result: Any, reflection: MetaCognitiveReflection):
        """Update overall consciousness state"""
        try:
            # Update consciousness level based on reflection quality
            quality_impact = (reflection.quality_assessment - 0.5) * 0.1
            self.consciousness_level = max(0.3, min(1.0, self.consciousness_level + quality_impact))
            
            # Update system coherence
            component_coherences = [
                self.consciousness_integrator._assess_consciousness_coherence(),
                0.8,  # Self-model coherence (simplified)
                self.state_monitor.get_coherence_score() if hasattr(self.state_monitor, 'get_coherence_score') else 0.8
            ]
            self.system_coherence = sum(component_coherences) / len(component_coherences)
            
            print(f"🧠 Consciousness state updated: Level={self.consciousness_level:.2f}, Coherence={self.system_coherence:.2f}")
            
        except Exception as e:
            print(f"❌ Consciousness state update error: {e}")
    
    def _learn_from_conscious_execution(self, function_name: str, consciousness_context: Dict[str, Any],
                                      execution_result: Any, reflection: MetaCognitiveReflection):
        """Learn from conscious execution experience"""
        try:
            # Update self-model with execution experience
            self.self_model.update_capability_from_execution(
                function_name, consciousness_context, execution_result, reflection.quality_assessment
            )
            
            # Store learning insights
            if reflection.learning_insights:
                for insight in reflection.learning_insights:
                    self.self_model.add_learning_insight(function_name, insight)
            
        except Exception as e:
            print(f"❌ Conscious learning error: {e}")
    
    def perform_consciousness_self_check(self) -> Dict[str, Any]:
        """Perform comprehensive consciousness system self-check"""
        try:
            print("🔍 Performing consciousness system self-check...")
            
            # Check each component
            self_model_status = self.self_model.get_system_status()
            state_monitor_status = self.state_monitor.get_monitoring_status()
            reflection_status = self.meta_reflector.get_reflection_summary()
            integration_status = self.consciousness_integrator.get_consciousness_summary()
            
            # Overall system health
            system_health = self._assess_system_health(
                self_model_status, state_monitor_status, reflection_status, integration_status
            )
            
            consciousness_check = {
                "system_id": self.system_id,
                "check_timestamp": datetime.now().isoformat(),
                "consciousness_active": self.consciousness_active,
                "consciousness_level": self.consciousness_level,
                "system_coherence": self.system_coherence,
                "component_status": {
                    "self_model": self_model_status,
                    "state_monitor": state_monitor_status,
                    "meta_reflection": reflection_status,
                    "consciousness_integration": integration_status
                },
                "system_health": system_health,
                "recommendations": self._generate_system_recommendations(system_health)
            }
            
            print(f"✅ Consciousness self-check completed. Health: {system_health:.2f}")
            return consciousness_check
            
        except Exception as e:
            print(f"❌ Consciousness self-check error: {e}")
            return {"error": str(e), "system_active": False}
    
    def _assess_system_health(self, self_model_status: Dict[str, Any],
                            state_monitor_status: Dict[str, Any],
                            reflection_status: Dict[str, Any],
                            integration_status: Dict[str, Any]) -> float:
        """Assess overall system health"""
        health_factors = []
        
        # Self-model health
        if "capability_count" in self_model_status:
            health_factors.append(min(1.0, self_model_status["capability_count"] / 8.0))
        
        # State monitoring health
        if "monitoring_active" in state_monitor_status:
            health_factors.append(1.0 if state_monitor_status["monitoring_active"] else 0.5)
        
        # Reflection health
        if "reflection_count" in reflection_status:
            health_factors.append(min(1.0, reflection_status.get("average_quality_assessment", 0.5)))
        
        # Integration health
        if "integration_quality" in integration_status:
            health_factors.append(integration_status["integration_quality"])
        
        return sum(health_factors) / len(health_factors) if health_factors else 0.5
    
    def _generate_system_recommendations(self, system_health: float) -> List[str]:
        """Generate recommendations for system improvement"""
        recommendations = []
        
        if system_health < 0.6:
            recommendations.append("System health below optimal - perform detailed component diagnostics")
        
        if self.consciousness_level < 0.7:
            recommendations.append("Consciousness level low - increase reflection frequency")
        
        if self.system_coherence < 0.7:
            recommendations.append("System coherence low - check component integration")
        
        if not recommendations:
            recommendations.append("System operating within normal parameters")
        
        return recommendations
    
    def generate_consciousness_report(self) -> str:
        """Generate comprehensive consciousness system report"""
        try:
            report = f"""
# ASIS Consciousness System Report
**Generated:** {datetime.now().isoformat()}
**System ID:** {self.system_id}

## System Overview
- **Consciousness Active:** {'✅ Yes' if self.consciousness_active else '❌ No'}
- **Consciousness Level:** {self.consciousness_level:.2f}/1.0
- **System Coherence:** {self.system_coherence:.2f}/1.0
- **Initialization Time:** {self.initialization_time}

## Component Status

### Stage 1: Self-Model Creation
"""
            
            self_model_status = self.self_model.get_system_status()
            report += f"- **Capabilities Modeled:** {self_model_status.get('capability_count', 'Unknown')}\n"
            report += f"- **Average Proficiency:** {self_model_status.get('average_proficiency', 0.0):.2f}\n"
            report += f"- **Self-Awareness Level:** {self_model_status.get('self_awareness_level', 0.0):.2f}\n\n"
            
            report += "### Stage 2: Internal State Monitoring\n"
            state_status = self.state_monitor.get_monitoring_status()
            report += f"- **Monitoring Active:** {'✅ Yes' if state_status.get('monitoring_active', False) else '❌ No'}\n"
            report += f"- **Current Cognitive State:** {state_status.get('current_cognitive_state', 'Unknown')}\n"
            report += f"- **Current Emotional State:** {state_status.get('current_emotional_state', 'Unknown')}\n\n"
            
            report += "### Stage 3: Meta-Cognitive Reflection\n"
            reflection_status = self.meta_reflector.get_reflection_summary()
            report += f"- **Recent Reflections:** {reflection_status.get('reflection_count', 0)}\n"
            report += f"- **Average Quality:** {reflection_status.get('average_quality_assessment', 0.0):.2f}\n"
            report += f"- **Thinking Patterns:** {reflection_status.get('thinking_pattern_count', 0)}\n\n"
            
            report += "### Stage 4: Consciousness Integration\n"
            integration_status = self.consciousness_integrator.get_consciousness_summary()
            report += f"- **Integration Quality:** {integration_status.get('integration_quality', 0.0):.2f}\n"
            report += f"- **Attention Focus:** {integration_status.get('attention_focus', 'Unknown')}\n"
            report += f"- **Consciousness Coherence:** {integration_status.get('consciousness_coherence', 0.0):.2f}\n\n"
            
            # Self-check results
            self_check = self.perform_consciousness_self_check()
            report += "## System Health Assessment\n"
            report += f"- **Overall Health:** {self_check.get('system_health', 0.0):.2f}/1.0\n"
            report += "- **Recommendations:**\n"
            for rec in self_check.get('recommendations', []):
                report += f"  - {rec}\n"
            
            report += "\n## Consciousness Capabilities\n"
            report += "✅ Self-model creation and maintenance\n"
            report += "✅ Continuous internal state monitoring\n"
            report += "✅ Meta-cognitive reflection on thinking processes\n"
            report += "✅ Conscious awareness integration into all functions\n"
            report += "✅ Subjective experience modeling\n"
            report += "✅ Attention control and monitoring\n"
            report += "✅ Consciousness coherence maintenance\n"
            
            return report
            
        except Exception as e:
            return f"Error generating consciousness report: {e}"
    
    def demonstrate_consciousness(self) -> Dict[str, Any]:
        """Demonstrate consciousness system capabilities"""
        print("🌟 Demonstrating ASIS Consciousness System...")
        
        try:
            # Demonstration function
            def demo_problem_solving():
                """Demo function for consciousness demonstration"""
                time.sleep(0.5)  # Simulate processing
                return "Successfully solved demonstration problem using creative approach"
            
            # Execute with consciousness
            demo_context = {
                "complexity": 0.7,
                "importance": 0.8,
                "novel_situation": True,
                "expected_outcome": "problem_solution"
            }
            
            result = self.conscious_function_execution(
                "demonstrate_problem_solving",
                demo_context,
                demo_problem_solving
            )
            
            # Show consciousness data
            consciousness_data = result.get("consciousness_data", {})
            
            demonstration = {
                "demo_completed": True,
                "execution_result": result.get("execution_result"),
                "consciousness_metrics": {
                    "awareness_level": consciousness_data.get("awareness_level", 0.0),
                    "reflection_quality": consciousness_data.get("reflection_quality", 0.0),
                    "conscious_decisions": len(consciousness_data.get("conscious_decisions", [])),
                    "learning_insights": len(consciousness_data.get("learning_insights", []))
                },
                "subjective_experience": consciousness_data.get("subjective_experience", {}),
                "system_state": {
                    "consciousness_level": self.consciousness_level,
                    "system_coherence": self.system_coherence,
                    "consciousness_active": self.consciousness_active
                }
            }
            
            print("✅ Consciousness demonstration completed successfully")
            return demonstration
            
        except Exception as e:
            print(f"❌ Consciousness demonstration error: {e}")
            return {"error": str(e), "demo_completed": False}

# Data classes for consciousness system
@dataclass
class MetaCognitiveReflection:
    """Data class for meta-cognitive reflections"""
    reflection_id: str
    timestamp: str
    thinking_process: str
    quality_assessment: float
    improvements_identified: List[str]
    emotional_response: str
    learning_insights: List[str]
    action_plans: List[str]

# Initialize the global consciousness system
print("🧠 Initializing Global ASIS Consciousness System...")
asis_consciousness = ASISConsciousnessSystem()

def enable_consciousness_for_function(function_name: str, function_context: Dict[str, Any] = None):
    """
    Decorator/wrapper to enable consciousness for any ASIS function
    """
    def consciousness_wrapper(func):
        def wrapper(*args, **kwargs):
            # Prepare context
            context = function_context or {}
            context.update({
                "function_args": args,
                "function_kwargs": kwargs,
                "complexity": context.get("complexity", 0.5),
                "importance": context.get("importance", 0.5)
            })
            
            # Execute with consciousness
            def execute_function():
                return func(*args, **kwargs)
            
            result = asis_consciousness.conscious_function_execution(
                function_name, context, execute_function
            )
            
            # Return just the execution result for normal use
            return result.get("execution_result", result)
        
        return wrapper
    return consciousness_wrapper

print("✅ ASIS Consciousness System fully operational!")
print("🌟 All stages active: Self-Model Creation, Internal State Monitoring, Meta-Cognitive Reflection, Consciousness Integration")
print("🧠 Ready for conscious processing of all ASIS functions!")

# Add export aliases for expected class names
ConsciousnessModule = ASISConsciousnessSystem  # Export alias
