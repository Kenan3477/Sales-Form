"""
Advanced Synthetic Intelligence System (ASIS) - Core Cognitive Architecture
Complete implementation of Phase 1.2 requirements:
- Attention System for focus management and context switching  
- Working Memory for short-term processing and manipulation
- Executive Control for goal setting, planning, and monitoring
- Meta-Cognition for self-awareness and thinking about thinking
- Emotional Processing for affect generation and regulation

Interfaces with the Enhanced Memory Network for persistent storage and retrieval.
"""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union, Callable
import json
import numpy as np
from collections import deque, defaultdict
import threading
import uuid
import heapq
from concurrent.futures import ThreadPoolExecutor

# Import enhanced memory network for integration
try:
    from enhanced_memory_network import (
        EnhancedMemoryNetwork, MemoryType, EmotionalTag, 
        EmotionalValence, ImportanceLevel, EnhancedMemory
    )
    MEMORY_NETWORK_AVAILABLE = True
except ImportError:
    MEMORY_NETWORK_AVAILABLE = False
    print("Warning: Enhanced Memory Network not available. Some features may be limited.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CognitiveState(Enum):
    """Overall cognitive states of the system"""
    IDLE = "idle"
    PROCESSING = "processing"
    LEARNING = "learning"
    PROBLEM_SOLVING = "problem_solving"
    CREATIVE = "creative"
    REFLECTIVE = "reflective"
    EMOTIONAL = "emotional"
    GOAL_PLANNING = "goal_planning"


class AttentionType(Enum):
    """Types of attention mechanisms"""
    FOCUSED = "focused"          # Concentrated attention on specific target
    DIVIDED = "divided"          # Split attention across multiple targets
    SUSTAINED = "sustained"      # Prolonged attention over time
    SELECTIVE = "selective"      # Filtering relevant from irrelevant
    EXECUTIVE = "executive"      # Goal-directed attention control


class GoalStatus(Enum):
    """Status of cognitive goals"""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ABANDONED = "abandoned"
    BLOCKED = "blocked"


class GoalPriority(Enum):
    """Priority levels for goals"""
    CRITICAL = 1.0
    HIGH = 0.8
    MEDIUM = 0.6
    LOW = 0.4
    BACKGROUND = 0.2


class EmotionType(Enum):
    """Emotion types for affect generation and emotional processing"""
    # Primary emotions
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    
    # Cognitive emotions
    CURIOSITY = "curiosity"
    SATISFACTION = "satisfaction"
    FRUSTRATION = "frustration"
    EXCITEMENT = "excitement"
    CONFUSION = "confusion"
    CONFIDENCE = "confidence"
    DOUBT = "doubt"
    
    # Social emotions
    EMPATHY = "empathy"
    PRIDE = "pride"
    SHAME = "shame"
    GUILT = "guilt"
    
    # Complex emotions
    ANTICIPATION = "anticipation"
    NOSTALGIA = "nostalgia"
    AWE = "awe"
    CONTEMPT = "contempt"


@dataclass
class Emotion:
    """Represents an emotional state or response"""
    emotion_type: EmotionType
    intensity: float  # 0.0 to 1.0
    context: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if not 0.0 <= self.intensity <= 1.0:
            raise ValueError("Emotion intensity must be between 0.0 and 1.0")


@dataclass
class Interest:
    """Represents an area of interest with dynamic strength"""
    topic: str
    strength: float  # 0.0 to 1.0
    last_reinforced: datetime = field(default_factory=datetime.now)
    reinforcement_count: int = 0
    related_concepts: Set[str] = field(default_factory=set)
    emotional_associations: List[Emotion] = field(default_factory=list)
    
    def reinforce(self, amount: float = 0.1):
        """Strengthen interest through reinforcement"""
        self.strength = min(1.0, self.strength + amount)
        self.reinforcement_count += 1
        self.last_reinforced = datetime.now()
    
    def decay(self, amount: float = 0.01):
        """Natural decay of interest over time"""
        self.strength = max(0.0, self.strength - amount)


@dataclass
class Goal:
    """Represents a cognitive goal or objective"""
    description: str
    priority: float  # 0.0 to 1.0
    deadline: Optional[datetime] = None
    sub_goals: List['Goal'] = field(default_factory=list)
    status: str = "active"  # active, paused, completed, abandoned
    created_at: datetime = field(default_factory=datetime.now)
    progress: float = 0.0  # 0.0 to 1.0
    
    def add_sub_goal(self, sub_goal: 'Goal'):
        """Add a sub-goal to this goal"""
        self.sub_goals.append(sub_goal)
    
    def update_progress(self):
        """Update progress based on sub-goal completion"""
        if not self.sub_goals:
            return
        
        completed_count = sum(1 for sg in self.sub_goals if sg.status == "completed")
        self.progress = completed_count / len(self.sub_goals)
        
        if self.progress >= 1.0:
            self.status = "completed"


class CognitiveComponent(ABC):
    """Abstract base class for cognitive architecture components"""
    
    def __init__(self, name: str):
        self.name = name
        self.active = True
        self.last_update = datetime.now()
    
    @abstractmethod
    async def process(self, input_data: Any) -> Any:
        """Process input data and return output"""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Return current status of the component"""
        pass


class AttentionSystem(CognitiveComponent):
    """Advanced attention system with focus management and context switching"""
    
    def __init__(self):
        super().__init__("AttentionSystem")
        self.current_focus: Optional[str] = None
        self.attention_queue: deque = deque(maxlen=20)
        self.attention_weights: Dict[str, float] = {}
        self.attention_history: List[Tuple[str, datetime]] = []
        self.context_stack: List[Dict[str, Any]] = []
        self.attention_type: AttentionType = AttentionType.SELECTIVE
        self.focus_intensity: float = 0.5
        self.distraction_threshold: float = 0.3
        self.attention_spans: Dict[str, List[float]] = defaultdict(list)
        self.inhibition_targets: Set[str] = set()
        
        # Advanced attention mechanisms
        self.salience_map: Dict[str, float] = {}
        self.attention_networks = {
            "alerting": 0.5,
            "orienting": 0.5, 
            "executive": 0.5
        }
        self.attention_filters: List[Callable] = []
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Advanced attention processing with context switching and focus management"""
        stimulus = input_data.get("stimulus")
        priority = input_data.get("priority", 0.5)
        attention_type = input_data.get("attention_type", "selective")
        context = input_data.get("context", {})
        
        if stimulus:
            # Calculate salience
            salience = self._calculate_salience(stimulus, context)
            self.salience_map[stimulus] = salience
            
            # Apply attention filters
            filtered_priority = self._apply_attention_filters(stimulus, priority)
            
            # Add to attention queue with enhanced metadata
            attention_item = {
                "stimulus": stimulus,
                "priority": filtered_priority,
                "salience": salience,
                "timestamp": datetime.now(),
                "context": context,
                "attention_type": attention_type
            }
            self.attention_queue.append(attention_item)
            
            # Update attention networks
            self._update_attention_networks(attention_item)
        
        # Advanced focus selection with context switching
        new_focus = await self._select_focus()
        
        # Handle context switching if focus changed
        if new_focus != self.current_focus:
            await self._handle_context_switch(self.current_focus, new_focus)
            self.current_focus = new_focus
        
        # Update attention intensity based on focus stability
        self._update_focus_intensity()
        
        # Manage inhibition of distractors
        self._manage_inhibition()
        
        return {
            "current_focus": self.current_focus,
            "focus_intensity": self.focus_intensity,
            "attention_type": self.attention_type.value,
            "queue_length": len(self.attention_queue),
            "salience_peak": max(self.salience_map.values()) if self.salience_map else 0,
            "attention_networks": self.attention_networks,
            "inhibited_items": len(self.inhibition_targets),
            "context_depth": len(self.context_stack)
        }
    
    def _calculate_salience(self, stimulus: str, context: Dict[str, Any]) -> float:
        """Calculate the salience (attention-grabbing quality) of a stimulus"""
        base_salience = 0.5
        
        # Novelty factor
        novelty = 1.0 if stimulus not in self.salience_map else 0.3
        
        # Relevance to current context
        relevance = self._assess_relevance(stimulus, context)
        
        # Emotional significance
        emotional_weight = context.get("emotional_intensity", 0.0)
        
        # Goal relevance
        goal_relevance = context.get("goal_relevance", 0.0)
        
        salience = (base_salience + novelty * 0.3 + relevance * 0.3 + 
                   emotional_weight * 0.2 + goal_relevance * 0.2)
        
        return min(1.0, salience)
    
    def _assess_relevance(self, stimulus: str, context: Dict[str, Any]) -> float:
        """Assess relevance of stimulus to current focus and goals"""
        if not self.current_focus:
            return 0.5
        
        # Simple keyword matching - could be enhanced with semantic similarity
        focus_keywords = self.current_focus.lower().split()
        stimulus_keywords = stimulus.lower().split()
        
        overlap = len(set(focus_keywords) & set(stimulus_keywords))
        max_possible = max(len(focus_keywords), len(stimulus_keywords))
        
        return overlap / max_possible if max_possible > 0 else 0.0
    
    def _apply_attention_filters(self, stimulus: str, priority: float) -> float:
        """Apply attention filters to modify priority"""
        filtered_priority = priority
        
        for filter_func in self.attention_filters:
            filtered_priority = filter_func(stimulus, filtered_priority)
        
        # Apply inhibition
        if stimulus in self.inhibition_targets:
            filtered_priority *= 0.1
        
        return filtered_priority
    
    async def _select_focus(self) -> Optional[str]:
        """Advanced focus selection considering multiple factors"""
        if not self.attention_queue:
            return None
        
        # Score each item based on multiple criteria
        scored_items = []
        current_time = datetime.now()
        
        for item in self.attention_queue:
            age_penalty = (current_time - item["timestamp"]).seconds / 3600 * 0.1
            
            score = (item["priority"] * 0.4 + 
                    item["salience"] * 0.3 + 
                    self.attention_networks["executive"] * 0.2 +
                    (1.0 - age_penalty) * 0.1)
            
            scored_items.append((score, item["stimulus"]))
        
        # Select highest scoring item
        if scored_items:
            best_score, best_stimulus = max(scored_items)
            
            # Check if it's worth switching focus
            switch_threshold = 0.1  # Prevent rapid switching
            if (self.current_focus is None or 
                best_score > self._get_current_focus_score() + switch_threshold):
                return best_stimulus
        
        return self.current_focus
    
    def _get_current_focus_score(self) -> float:
        """Get score of current focus for comparison"""
        if not self.current_focus:
            return 0.0
        
        for item in self.attention_queue:
            if item["stimulus"] == self.current_focus:
                return item["priority"] * item["salience"]
        
        return 0.0
    
    async def _handle_context_switch(self, old_focus: Optional[str], new_focus: Optional[str]):
        """Handle context switching between different foci"""
        if old_focus:
            # Save current context
            context_frame = {
                "focus": old_focus,
                "timestamp": datetime.now(),
                "attention_state": {
                    "intensity": self.focus_intensity,
                    "type": self.attention_type.value
                },
                "working_set": list(self.attention_weights.keys())[:5]
            }
            self.context_stack.append(context_frame)
            
            # Record attention span
            if old_focus in self.attention_spans:
                last_switch_time = None
                for timestamp in reversed(self.attention_history):
                    if timestamp[0] == old_focus:
                        last_switch_time = timestamp[1]
                        break
                
                if last_switch_time:
                    span = (datetime.now() - last_switch_time).seconds
                    self.attention_spans[old_focus].append(span)
        
        if new_focus:
            # Update attention history
            self.attention_history.append((new_focus, datetime.now()))
            
            # Adjust attention type based on new focus
            self._adapt_attention_type(new_focus)
        
        # Keep context stack manageable
        if len(self.context_stack) > 10:
            self.context_stack.pop(0)
    
    def _adapt_attention_type(self, focus: str):
        """Adapt attention type based on the nature of the focus"""
        # Simple heuristics - could be enhanced with learning
        if "problem" in focus.lower() or "debug" in focus.lower():
            self.attention_type = AttentionType.FOCUSED
        elif "multitask" in focus.lower() or "monitor" in focus.lower():
            self.attention_type = AttentionType.DIVIDED
        elif "search" in focus.lower() or "explore" in focus.lower():
            self.attention_type = AttentionType.SELECTIVE
        else:
            self.attention_type = AttentionType.SUSTAINED
    
    def _update_focus_intensity(self):
        """Update focus intensity based on stability and duration"""
        if self.current_focus:
            # Increase intensity with stable focus
            recent_switches = len([h for h in self.attention_history[-10:] 
                                 if h[0] == self.current_focus])
            
            if recent_switches > 0:
                stability_factor = min(1.0, recent_switches / 5.0)
                self.focus_intensity = min(1.0, self.focus_intensity + stability_factor * 0.1)
            else:
                self.focus_intensity = max(0.1, self.focus_intensity - 0.05)
    
    def _update_attention_networks(self, attention_item: Dict[str, Any]):
        """Update attention network activations"""
        # Alerting network - responds to stimulus onset
        self.attention_networks["alerting"] = min(1.0, 
            self.attention_networks["alerting"] + attention_item["salience"] * 0.1)
        
        # Orienting network - directs attention to location
        priority_value = attention_item["priority"]
        if isinstance(priority_value, (int, float)):
            orientation_boost = priority_value * 0.1
        else:
            orientation_boost = 0.05  # Default boost
        self.attention_networks["orienting"] = min(1.0,
            self.attention_networks["orienting"] + orientation_boost)
        
        # Executive network - resolves conflict
        if len(self.attention_queue) > 5:  # High load situation
            self.attention_networks["executive"] = min(1.0,
                self.attention_networks["executive"] + 0.1)
        
        # Gradual decay
        for network in self.attention_networks:
            self.attention_networks[network] = max(0.1, 
                self.attention_networks[network] - 0.01)
    
    def _manage_inhibition(self):
        """Manage inhibition of distracting stimuli"""
        if len(self.attention_queue) > 10:  # High load
            # Inhibit low-priority items
            low_priority_items = [item["stimulus"] for item in self.attention_queue 
                                if item["priority"] < self.distraction_threshold]
            self.inhibition_targets.update(low_priority_items[:3])
        
        # Remove old inhibitions
        if len(self.inhibition_targets) > 5:
            old_inhibitions = list(self.inhibition_targets)[:2]
            for item in old_inhibitions:
                self.inhibition_targets.discard(item)
    
    def add_attention_filter(self, filter_func: Callable[[str, float], float]):
        """Add a custom attention filter function"""
        self.attention_filters.append(filter_func)
    
    def get_attention_span_stats(self, focus: str) -> Dict[str, float]:
        """Get attention span statistics for a specific focus"""
        if focus not in self.attention_spans or not self.attention_spans[focus]:
            return {"mean": 0, "max": 0, "min": 0, "count": 0}
        
        spans = self.attention_spans[focus]
        return {
            "mean": np.mean(spans),
            "max": max(spans),
            "min": min(spans),
            "count": len(spans)
        }
    
    def get_status(self) -> Dict[str, Any]:
        attention_span_data = {}
        if self.current_focus:
            attention_span_data = self.get_attention_span_stats(self.current_focus)
        
        return {
            "name": self.name,
            "current_focus": self.current_focus,
            "focus_intensity": self.focus_intensity,
            "attention_type": self.attention_type.value,
            "queue_size": len(self.attention_queue),
            "salience_items": len(self.salience_map),
            "attention_networks": self.attention_networks,
            "context_depth": len(self.context_stack),
            "inhibited_targets": len(self.inhibition_targets),
            "attention_span_stats": attention_span_data,
            "last_update": self.last_update.isoformat()
        }


class WorkingMemory(CognitiveComponent):
    """Advanced working memory with manipulation, rehearsal, and capacity management"""
    
    def __init__(self, capacity: int = 7):  # Miller's magical number
        super().__init__("WorkingMemory")
        self.capacity = capacity
        self.items: deque = deque(maxlen=capacity)
        self.processing_buffer: Dict[str, Any] = {}
        
        # Advanced working memory features
        self.rehearsal_queue: List[Dict[str, Any]] = []
        self.manipulation_workspace: Dict[str, Any] = {}
        self.chunk_registry: Dict[str, List[str]] = {}
        self.interference_log: List[Dict[str, Any]] = []
        self.capacity_utilization: List[float] = []
        
        # Cognitive operations
        self.active_operations: Set[str] = set()
        self.operation_history: List[Dict[str, Any]] = []
        
        # Memory subsystems
        self.phonological_loop: deque = deque(maxlen=3)  # Verbal working memory
        self.visuospatial_sketchpad: deque = deque(maxlen=3)  # Visual working memory
        self.episodic_buffer: deque = deque(maxlen=4)  # Integration buffer
        
        # Central executive functions
        self.executive_attention: float = 1.0
        self.updating_efficiency: float = 0.8
        self.inhibition_strength: float = 0.6
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Advanced working memory processing with manipulation and rehearsal"""
        action = input_data.get("action", "add")
        
        if action == "add":
            return await self._add_item(input_data)
        elif action == "retrieve":
            return await self._retrieve_item(input_data)
        elif action == "manipulate":
            return await self._manipulate_items(input_data)
        elif action == "rehearse":
            return await self._rehearse_items(input_data)
        elif action == "chunk":
            return await self._create_chunk(input_data)
        elif action == "clear":
            return await self._clear_memory(input_data)
        elif action == "update":
            return await self._update_item(input_data)
        else:
            return await self._get_status_internal()
    
    async def _add_item(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add item to working memory with subsystem routing"""
        item_data = input_data.get("item")
        item_type = input_data.get("item_type", "general")
        priority = input_data.get("priority", 0.5)
        
        if not item_data:
            return {"error": "No item data provided"}
        
        # Create enhanced memory item
        memory_item = {
            "content": item_data,
            "type": item_type,
            "priority": priority,
            "timestamp": datetime.now(),
            "access_count": 0,
            "last_accessed": datetime.now(),
            "decay_rate": 0.1,
            "activation_level": 1.0,
            "associations": [],
            "rehearsal_count": 0
        }
        
        # Route to appropriate subsystem
        if item_type in ["verbal", "linguistic", "auditory"]:
            if len(self.phonological_loop) >= self.phonological_loop.maxlen:
                self._handle_capacity_overflow("phonological")
            self.phonological_loop.append(memory_item)
            
        elif item_type in ["visual", "spatial", "imagery"]:
            if len(self.visuospatial_sketchpad) >= self.visuospatial_sketchpad.maxlen:
                self._handle_capacity_overflow("visuospatial")
            self.visuospatial_sketchpad.append(memory_item)
            
        elif item_type in ["episodic", "contextual", "integrated"]:
            if len(self.episodic_buffer) >= self.episodic_buffer.maxlen:
                self._handle_capacity_overflow("episodic")
            self.episodic_buffer.append(memory_item)
            
        else:
            # General working memory
            if len(self.items) >= self.capacity:
                self._handle_capacity_overflow("general")
            self.items.append(memory_item)
        
        # Update capacity utilization tracking
        current_utilization = self._calculate_utilization()
        self.capacity_utilization.append(current_utilization)
        
        # Keep utilization history manageable
        if len(self.capacity_utilization) > 100:
            self.capacity_utilization.pop(0)
        
        # Check for interference
        await self._check_interference(memory_item)
        
        return {
            "status": "added",
            "item_id": id(memory_item),
            "subsystem": self._get_item_subsystem(item_type),
            "utilization": current_utilization,
            "capacity_remaining": self._get_remaining_capacity()
        }
    
    def _get_item_subsystem(self, item_type: str) -> str:
        """Get the subsystem name for an item type"""
        if item_type in ["verbal", "linguistic", "auditory"]:
            return "phonological"
        elif item_type in ["visual", "spatial", "imagery"]:
            return "visuospatial"
        elif item_type in ["episodic", "contextual", "integrated"]:
            return "episodic"
        else:
            return "general"
    
    async def _retrieve_item(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve items with cue-based search and activation spreading"""
        query = input_data.get("query", "")
        cue_type = input_data.get("cue_type", "content")
        activation_threshold = input_data.get("threshold", 0.3)
        
        retrieved_items = []
        
        # Search across all subsystems
        all_items = (list(self.items) + list(self.phonological_loop) + 
                    list(self.visuospatial_sketchpad) + list(self.episodic_buffer))
        
        for item in all_items:
            activation = self._calculate_activation(item, query, cue_type)
            
            if activation >= activation_threshold:
                # Update access statistics
                item["access_count"] += 1
                item["last_accessed"] = datetime.now()
                item["activation_level"] = min(1.0, item["activation_level"] + 0.1)
                
                retrieved_items.append({
                    "content": item["content"],
                    "activation": activation,
                    "access_count": item["access_count"],
                    "subsystem": self._identify_subsystem(item)
                })
        
        # Sort by activation level
        retrieved_items.sort(key=lambda x: x["activation"], reverse=True)
        
        return {
            "retrieved_items": retrieved_items[:5],  # Top 5 matches
            "total_matches": len(retrieved_items),
            "search_query": query,
            "cue_type": cue_type
        }
    
    async def _manipulate_items(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform cognitive operations on working memory items"""
        operation = input_data.get("operation", "transform")
        targets = input_data.get("targets", [])
        parameters = input_data.get("parameters", {})
        
        if operation not in ["transform", "combine", "compare", "reorder", "abstract"]:
            return {"error": f"Unknown operation: {operation}"}
        
        self.active_operations.add(operation)
        operation_start = datetime.now()
        
        try:
            if operation == "transform":
                result = await self._transform_items(targets, parameters)
            elif operation == "combine":
                result = await self._combine_items(targets, parameters)
            elif operation == "compare":
                result = await self._compare_items(targets, parameters)
            elif operation == "reorder":
                result = await self._reorder_items(targets, parameters)
            elif operation == "abstract":
                result = await self._abstract_pattern(targets, parameters)
            
            # Record operation history
            operation_record = {
                "operation": operation,
                "targets": targets,
                "parameters": parameters,
                "result": result,
                "duration": (datetime.now() - operation_start).total_seconds(),
                "timestamp": datetime.now()
            }
            self.operation_history.append(operation_record)
            
            # Update executive attention based on operation complexity
            complexity = len(targets) * len(parameters) * 0.1
            self.executive_attention = max(0.1, self.executive_attention - complexity)
            
            return {
                "operation": operation,
                "result": result,
                "complexity": complexity,
                "executive_load": 1.0 - self.executive_attention
            }
            
        finally:
            self.active_operations.discard(operation)
    
    async def _rehearse_items(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Maintain items in working memory through rehearsal"""
        rehearsal_type = input_data.get("rehearsal_type", "maintenance")
        target_items = input_data.get("targets", [])
        
        rehearsed_count = 0
        
        if rehearsal_type == "maintenance":
            # Simple maintenance rehearsal
            all_items = self._get_all_items()
            
            for item in all_items:
                if not target_items or item["content"] in target_items:
                    item["activation_level"] = min(1.0, item["activation_level"] + 0.2)
                    item["rehearsal_count"] += 1
                    rehearsed_count += 1
                    
        elif rehearsal_type == "elaborative":
            # Elaborative rehearsal with association building
            for item in self._get_all_items():
                if not target_items or item["content"] in target_items:
                    # Create associations with other items
                    other_items = [i for i in self._get_all_items() if i != item]
                    if other_items:
                        related_item = max(other_items, 
                                         key=lambda x: self._calculate_similarity(item, x))
                        item["associations"].append(related_item["content"])
                    
                    item["activation_level"] = min(1.0, item["activation_level"] + 0.3)
                    item["rehearsal_count"] += 1
                    rehearsed_count += 1
        
        return {
            "rehearsal_type": rehearsal_type,
            "items_rehearsed": rehearsed_count,
            "total_rehearsals": sum(item["rehearsal_count"] for item in self._get_all_items())
        }
    
    async def _create_chunk(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create chunks to increase effective capacity"""
        chunk_name = input_data.get("chunk_name", f"chunk_{len(self.chunk_registry)}")
        items_to_chunk = input_data.get("items", [])
        
        if len(items_to_chunk) < 2:
            return {"error": "Need at least 2 items to create a chunk"}
        
        # Create chunk
        self.chunk_registry[chunk_name] = items_to_chunk
        
        # Replace individual items with chunk in working memory
        chunk_item = {
            "content": f"CHUNK:{chunk_name}",
            "type": "chunk",
            "priority": 0.8,
            "timestamp": datetime.now(),
            "access_count": 0,
            "last_accessed": datetime.now(),
            "decay_rate": 0.05,  # Chunks decay slower
            "activation_level": 1.0,
            "associations": items_to_chunk,
            "rehearsal_count": 0,
            "chunk_size": len(items_to_chunk)
        }
        
        # Remove individual items and add chunk
        all_items = self._get_all_items()
        for item in all_items[:]:
            if item["content"] in items_to_chunk:
                self._remove_item_from_subsystems(item)
        
        self.items.append(chunk_item)
        
        return {
            "chunk_name": chunk_name,
            "chunk_size": len(items_to_chunk),
            "capacity_freed": len(items_to_chunk) - 1,
            "total_chunks": len(self.chunk_registry)
        }
    
    def _calculate_activation(self, item: Dict[str, Any], query: str, cue_type: str) -> float:
        """Calculate activation level of an item given a retrieval cue"""
        base_activation = item["activation_level"]
        
        # Content matching
        if cue_type == "content":
            content_match = self._calculate_content_similarity(item["content"], query)
        else:
            content_match = 0.5
        
        # Recency effect
        time_since_access = (datetime.now() - item["last_accessed"]).seconds / 3600
        recency = max(0.1, 1.0 - time_since_access * 0.1)
        
        # Frequency effect
        frequency = min(1.0, item["access_count"] * 0.1)
        
        # Association spreading
        association_boost = 0.0
        for assoc in item.get("associations", []):
            if query.lower() in str(assoc).lower():
                association_boost += 0.1
        
        total_activation = (base_activation * 0.4 + content_match * 0.3 + 
                          recency * 0.2 + frequency * 0.1 + association_boost)
        
        return min(1.0, total_activation)
    
    def _calculate_content_similarity(self, content1: str, content2: str) -> float:
        """Simple content similarity calculation"""
        words1 = set(str(content1).lower().split())
        words2 = set(str(content2).lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_similarity(self, item1: Dict[str, Any], item2: Dict[str, Any]) -> float:
        """Calculate similarity between two memory items"""
        return self._calculate_content_similarity(item1["content"], item2["content"])
    
    def _handle_capacity_overflow(self, subsystem: str):
        """Handle capacity overflow using various strategies"""
        if subsystem == "general":
            items_list = self.items
        elif subsystem == "phonological":
            items_list = self.phonological_loop
        elif subsystem == "visuospatial":
            items_list = self.visuospatial_sketchpad
        elif subsystem == "episodic":
            items_list = self.episodic_buffer
        else:
            return
        
        if items_list:
            # Remove least activated item
            least_activated = min(items_list, key=lambda x: x["activation_level"])
            items_list.remove(least_activated)
            
            # Log interference
            self.interference_log.append({
                "type": "capacity_overflow",
                "subsystem": subsystem,
                "removed_item": least_activated["content"],
                "timestamp": datetime.now()
            })
    
    async def _check_interference(self, new_item: Dict[str, Any]):
        """Check for interference between memory items"""
        all_items = self._get_all_items()
        
        for existing_item in all_items:
            if existing_item != new_item:
                similarity = self._calculate_similarity(new_item, existing_item)
                
                if similarity > 0.7:  # High similarity threshold
                    # Interference detected
                    interference_strength = similarity * 0.3
                    existing_item["activation_level"] -= interference_strength
                    
                    self.interference_log.append({
                        "type": "similarity_interference",
                        "new_item": new_item["content"],
                        "existing_item": existing_item["content"],
                        "similarity": similarity,
                        "interference_strength": interference_strength,
                        "timestamp": datetime.now()
                    })
    
    def _calculate_utilization(self) -> float:
        """Calculate current memory utilization across all subsystems"""
        total_used = (len(self.items) + len(self.phonological_loop) + 
                     len(self.visuospatial_sketchpad) + len(self.episodic_buffer))
        total_capacity = (self.capacity + self.phonological_loop.maxlen + 
                         self.visuospatial_sketchpad.maxlen + self.episodic_buffer.maxlen)
        
        return total_used / total_capacity
    
    def _get_remaining_capacity(self) -> Dict[str, int]:
        """Get remaining capacity for each subsystem"""
        return {
            "general": self.capacity - len(self.items),
            "phonological": self.phonological_loop.maxlen - len(self.phonological_loop),
            "visuospatial": self.visuospatial_sketchpad.maxlen - len(self.visuospatial_sketchpad),
            "episodic": self.episodic_buffer.maxlen - len(self.episodic_buffer)
        }
    
    def _get_all_items(self) -> List[Dict[str, Any]]:
        """Get all items across all subsystems"""
        return (list(self.items) + list(self.phonological_loop) + 
               list(self.visuospatial_sketchpad) + list(self.episodic_buffer))
    
    def _identify_subsystem(self, item: Dict[str, Any]) -> str:
        """Identify which subsystem an item belongs to"""
        if item in self.phonological_loop:
            return "phonological"
        elif item in self.visuospatial_sketchpad:
            return "visuospatial"
        elif item in self.episodic_buffer:
            return "episodic"
        elif item in self.items:
            return "general"
        else:
            return "unknown"
    
    def _remove_item_from_subsystems(self, item: Dict[str, Any]):
        """Remove an item from all subsystems"""
        if item in self.items:
            self.items.remove(item)
        if item in self.phonological_loop:
            self.phonological_loop.remove(item)
        if item in self.visuospatial_sketchpad:
            self.visuospatial_sketchpad.remove(item)
        if item in self.episodic_buffer:
            self.episodic_buffer.remove(item)
    
    async def _clear_memory(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Clear working memory contents"""
        clear_type = input_data.get("clear_type", "all")
        
        cleared_items = 0
        
        if clear_type == "all" or clear_type == "general":
            cleared_items += len(self.items)
            self.items.clear()
        
        if clear_type == "all" or clear_type == "phonological":
            cleared_items += len(self.phonological_loop)
            self.phonological_loop.clear()
        
        if clear_type == "all" or clear_type == "visuospatial":
            cleared_items += len(self.visuospatial_sketchpad)
            self.visuospatial_sketchpad.clear()
        
        if clear_type == "all" or clear_type == "episodic":
            cleared_items += len(self.episodic_buffer)
            self.episodic_buffer.clear()
        
        return {
            "cleared_items": cleared_items,
            "clear_type": clear_type,
            "remaining_capacity": self._get_remaining_capacity()
        }
    
    async def _update_item(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing item in working memory"""
        target_content = input_data.get("target_content")
        new_content = input_data.get("new_content")
        
        if not target_content or not new_content:
            return {"error": "Both target_content and new_content required"}
        
        updated_count = 0
        all_items = self._get_all_items()
        
        for item in all_items:
            if item["content"] == target_content:
                item["content"] = new_content
                item["last_accessed"] = datetime.now()
                item["access_count"] += 1
                updated_count += 1
        
        return {
            "updated_items": updated_count,
            "target_content": target_content,
            "new_content": new_content
        }
    
    async def _get_status_internal(self) -> Dict[str, Any]:
        """Get internal status without recursion"""
        return self.get_status()
    
    async def _transform_items(self, targets: List[str], parameters: Dict[str, Any]) -> Any:
        """Transform working memory items"""
        transformation = parameters.get("transformation", "identity")
        
        if transformation == "reverse":
            return [target[::-1] for target in targets if isinstance(target, str)]
        elif transformation == "uppercase":
            return [target.upper() for target in targets if isinstance(target, str)]
        elif transformation == "abstract":
            return [f"CONCEPT({target})" for target in targets]
        else:
            return targets
    
    async def _combine_items(self, targets: List[str], parameters: Dict[str, Any]) -> str:
        """Combine multiple items into one"""
        combiner = parameters.get("combiner", " + ")
        return combiner.join(str(target) for target in targets)
    
    async def _compare_items(self, targets: List[str], parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Compare items along specified dimensions"""
        if len(targets) < 2:
            return {"error": "Need at least 2 items to compare"}
        
        comparison_type = parameters.get("type", "similarity")
        
        if comparison_type == "similarity":
            similarities = {}
            for i, item1 in enumerate(targets):
                for j, item2 in enumerate(targets[i+1:], i+1):
                    similarity = self._calculate_content_similarity(str(item1), str(item2))
                    similarities[f"{i}-{j}"] = similarity
            return {"similarities": similarities}
        
        elif comparison_type == "length":
            lengths = {f"item_{i}": len(str(item)) for i, item in enumerate(targets)}
            return {"lengths": lengths}
        
        return {"comparison_type": comparison_type, "targets": targets}
    
    async def _reorder_items(self, targets: List[str], parameters: Dict[str, Any]) -> List[str]:
        """Reorder items according to specified criteria"""
        order_type = parameters.get("order", "reverse")
        
        if order_type == "reverse":
            return list(reversed(targets))
        elif order_type == "alphabetical":
            return sorted(targets, key=str)
        elif order_type == "length":
            return sorted(targets, key=lambda x: len(str(x)))
        else:
            return targets
    
    async def _abstract_pattern(self, targets: List[str], parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Extract abstract patterns from items"""
        pattern_type = parameters.get("pattern", "common_elements")
        
        if pattern_type == "common_elements":
            if not targets:
                return {"common_elements": []}
            
            # Find common words across all targets
            word_sets = [set(str(target).lower().split()) for target in targets]
            common_words = set.intersection(*word_sets) if word_sets else set()
            
            return {"common_elements": list(common_words)}
        
        elif pattern_type == "sequence":
            return {"sequence_length": len(targets), "first": targets[0] if targets else None}
        
        return {"pattern_type": pattern_type, "targets": targets}
    
    def get_status(self) -> Dict[str, Any]:
        utilization_stats = {
            "current": self._calculate_utilization(),
            "average": np.mean(self.capacity_utilization) if self.capacity_utilization else 0,
            "peak": max(self.capacity_utilization) if self.capacity_utilization else 0
        }
        
        return {
            "name": self.name,
            "total_capacity": self.capacity + 10,  # Total across all subsystems
            "utilization_stats": utilization_stats,
            "subsystem_usage": {
                "general": len(self.items),
                "phonological": len(self.phonological_loop),
                "visuospatial": len(self.visuospatial_sketchpad),
                "episodic": len(self.episodic_buffer)
            },
            "active_operations": len(self.active_operations),
            "total_chunks": len(self.chunk_registry),
            "interference_events": len(self.interference_log),
            "executive_attention": self.executive_attention,
            "operation_history": len(self.operation_history),
            "last_update": self.last_update.isoformat()
        }


class ExecutiveControl(CognitiveComponent):
    """Advanced executive control with goal management, planning, and monitoring"""
    
    def __init__(self):
        super().__init__("ExecutiveControl")
        self.current_goals: List[Goal] = []
        self.completed_goals: List[Goal] = []
        self.planning_horizon: int = 24  # hours
        self.decision_history: List[Dict[str, Any]] = []
        
        # Advanced executive functions
        self.goal_hierarchy: Dict[str, List[str]] = {}  # parent -> children mapping
        self.planning_strategies: Dict[str, Callable] = {}
        self.monitoring_metrics: Dict[str, float] = {}
        self.inhibition_rules: List[Dict[str, Any]] = []
        self.cognitive_flexibility: float = 0.7
        self.working_memory_updating: float = 0.8
        
        # Executive attention and control
        self.executive_resources: float = 1.0
        self.cognitive_load: float = 0.0
        self.task_switching_cost: float = 0.1
        self.current_strategy: Optional[str] = None
        
        # Planning and scheduling
        self.action_queue: List[Dict[str, Any]] = []
        self.resource_allocation: Dict[str, float] = {}
        self.constraint_satisfaction: Dict[str, Any] = {}
        self.contingency_plans: Dict[str, List[Dict[str, Any]]] = {}
        
        # Performance monitoring
        self.error_detection: List[Dict[str, Any]] = []
        self.performance_standards: Dict[str, float] = {}
        self.adaptation_triggers: List[Dict[str, Any]] = []
        
        # Register default planning strategies
        self._register_default_strategies()
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Advanced executive control processing"""
        action = input_data.get("action")
        
        if action == "add_goal":
            return await self._add_goal(input_data)
        elif action == "plan":
            return await self._create_plan(input_data)
        elif action == "monitor":
            return await self._monitor_progress(input_data)
        elif action == "adapt":
            return await self._adapt_strategy(input_data)
        elif action == "inhibit":
            return await self._apply_inhibition(input_data)
        elif action == "switch_task":
            return await self._switch_task(input_data)
        elif action == "allocate_resources":
            return await self._allocate_resources(input_data)
        elif action == "make_decision":
            return await self._make_advanced_decision(input_data)
        elif action == "update_goals":
            return await self._update_goals_advanced()
        else:
            return await self._get_executive_status()
    
    async def _add_goal(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add goal with hierarchical organization and planning"""
        goal_data = input_data.get("goal", {})
        parent_goal_id = input_data.get("parent_goal_id")
        
        # Create enhanced goal
        goal = Goal(
            description=goal_data.get("description", ""),
            priority=goal_data.get("priority", 0.5),
            deadline=goal_data.get("deadline"),
            status="active"
        )
        
        # Assign unique ID
        goal_id = str(uuid.uuid4())
        goal.id = goal_id
        
        # Add to goal hierarchy
        if parent_goal_id:
            if parent_goal_id not in self.goal_hierarchy:
                self.goal_hierarchy[parent_goal_id] = []
            self.goal_hierarchy[parent_goal_id].append(goal_id)
            goal.parent_id = parent_goal_id
        
        self.current_goals.append(goal)
        self._prioritize_goals()
        
        # Automatic planning for complex goals
        if goal_data.get("auto_plan", False):
            plan_result = await self._create_plan({
                "goal_id": goal_id,
                "planning_depth": goal_data.get("planning_depth", 2)
            })
            goal.action_plan = plan_result.get("plan", [])
        
        # Resource allocation
        required_resources = goal_data.get("required_resources", {})
        if required_resources:
            allocation_result = await self._allocate_resources({
                "goal_id": goal_id,
                "resources": required_resources
            })
        
        return {
            "goal_id": goal_id,
            "status": "added",
            "hierarchy_level": self._get_hierarchy_level(goal_id),
            "planned_actions": len(getattr(goal, 'action_plan', [])),
            "resource_allocation": self.resource_allocation.get(goal_id, {})
        }
    
    async def _create_plan(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive action plan for goals"""
        goal_id = input_data.get("goal_id")
        planning_strategy = input_data.get("strategy", "hierarchical_decomposition")
        planning_depth = input_data.get("planning_depth", 3)
        constraints = input_data.get("constraints", {})
        
        if not goal_id:
            return {"error": "Goal ID required for planning"}
        
        goal = self._find_goal_by_id(goal_id)
        if not goal:
            return {"error": f"Goal {goal_id} not found"}
        
        # Apply planning strategy
        if planning_strategy in self.planning_strategies:
            plan = await self.planning_strategies[planning_strategy](
                goal, planning_depth, constraints
            )
        else:
            plan = await self._default_planning_strategy(goal, planning_depth, constraints)
        
        # Create contingency plans
        contingencies = await self._create_contingency_plans(goal, plan)
        self.contingency_plans[goal_id] = contingencies
        
        # Schedule actions
        scheduled_actions = self._schedule_actions(plan, constraints)
        self.action_queue.extend(scheduled_actions)
        
        return {
            "goal_id": goal_id,
            "plan": plan,
            "contingencies": len(contingencies),
            "scheduled_actions": len(scheduled_actions),
            "planning_strategy": planning_strategy,
            "estimated_duration": self._estimate_plan_duration(plan)
        }
    
    async def _monitor_progress(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor goal progress and performance"""
        goal_id = input_data.get("goal_id")
        performance_data = input_data.get("performance_data", {})
        
        monitoring_results = {}
        
        if goal_id:
            # Monitor specific goal
            goal = self._find_goal_by_id(goal_id)
            if goal:
                progress_update = self._assess_goal_progress(goal, performance_data)
                monitoring_results[goal_id] = progress_update
        else:
            # Monitor all active goals
            for goal in self.current_goals:
                if hasattr(goal, 'id'):
                    progress_update = self._assess_goal_progress(goal, performance_data)
                    monitoring_results[goal.id] = progress_update
        
        # Error detection
        errors_detected = self._detect_errors(performance_data)
        if errors_detected:
            self.error_detection.extend(errors_detected)
        
        # Performance evaluation
        performance_summary = self._evaluate_performance(performance_data)
        
        # Adaptation triggers
        adaptation_needed = self._check_adaptation_triggers(monitoring_results)
        
        return {
            "monitoring_results": monitoring_results,
            "errors_detected": len(errors_detected),
            "performance_summary": performance_summary,
            "adaptation_needed": adaptation_needed,
            "cognitive_load": self.cognitive_load
        }
    
    async def _adapt_strategy(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt strategies based on performance feedback"""
        adaptation_type = input_data.get("type", "performance_based")
        trigger_data = input_data.get("trigger_data", {})
        
        adaptations_made = []
        
        if adaptation_type == "performance_based":
            # Adapt based on performance metrics
            for metric, value in trigger_data.items():
                if metric in self.performance_standards:
                    expected = self.performance_standards[metric]
                    if value < expected * 0.8:  # Performance drop threshold
                        adaptation = self._adapt_to_poor_performance(metric, value, expected)
                        adaptations_made.append(adaptation)
        
        elif adaptation_type == "cognitive_load":
            # Adapt to high cognitive load
            if self.cognitive_load > 0.8:
                adaptation = self._adapt_to_high_load()
                adaptations_made.append(adaptation)
        
        elif adaptation_type == "goal_conflict":
            # Resolve goal conflicts
            conflicts = self._detect_goal_conflicts()
            for conflict in conflicts:
                resolution = self._resolve_goal_conflict(conflict)
                adaptations_made.append(resolution)
        
        # Update cognitive flexibility based on successful adaptations
        if adaptations_made:
            self.cognitive_flexibility = min(1.0, self.cognitive_flexibility + 0.05)
        
        return {
            "adaptation_type": adaptation_type,
            "adaptations_made": len(adaptations_made),
            "adaptations": adaptations_made,
            "cognitive_flexibility": self.cognitive_flexibility
        }
    
    async def _apply_inhibition(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply inhibitory control"""
        target = input_data.get("target")
        inhibition_strength = input_data.get("strength", 0.7)
        duration = input_data.get("duration", 300)  # seconds
        
        inhibition_rule = {
            "target": target,
            "strength": inhibition_strength,
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(seconds=duration),
            "active": True
        }
        
        self.inhibition_rules.append(inhibition_rule)
        
        # Apply immediate inhibition effects
        suppression_result = self._apply_immediate_suppression(target, inhibition_strength)
        
        return {
            "target": target,
            "inhibition_strength": inhibition_strength,
            "duration": duration,
            "immediate_effect": suppression_result,
            "active_inhibitions": len([r for r in self.inhibition_rules if r["active"]])
        }
    
    async def _switch_task(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle task switching with cognitive costs"""
        new_task = input_data.get("new_task")
        current_task = input_data.get("current_task", self.current_strategy)
        switch_type = input_data.get("switch_type", "voluntary")
        
        if not new_task:
            return {"error": "New task specification required"}
        
        # Calculate switching cost
        switch_cost = self._calculate_switch_cost(current_task, new_task, switch_type)
        
        # Apply cognitive cost
        self.executive_resources = max(0.1, self.executive_resources - switch_cost)
        self.cognitive_load = min(1.0, self.cognitive_load + switch_cost * 0.5)
        
        # Update current strategy
        old_strategy = self.current_strategy
        self.current_strategy = new_task
        
        # Task switching effects
        switching_effects = {
            "reconfiguration_time": switch_cost * 1000,  # milliseconds
            "performance_cost": switch_cost * 0.3,
            "resource_depletion": switch_cost
        }
        
        return {
            "old_task": old_strategy,
            "new_task": new_task,
            "switch_cost": switch_cost,
            "switch_type": switch_type,
            "switching_effects": switching_effects,
            "remaining_resources": self.executive_resources
        }
    
    async def _allocate_resources(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Allocate cognitive resources to goals and tasks"""
        goal_id = input_data.get("goal_id")
        requested_resources = input_data.get("resources", {})
        allocation_strategy = input_data.get("strategy", "priority_based")
        
        if goal_id and goal_id not in self.resource_allocation:
            self.resource_allocation[goal_id] = {}
        
        total_allocation = 0.0
        allocation_details = {}
        
        for resource_type, amount in requested_resources.items():
            if allocation_strategy == "priority_based":
                goal = self._find_goal_by_id(goal_id)
                priority_weight = goal.priority if goal else 0.5
                allocated_amount = amount * priority_weight
            elif allocation_strategy == "equal_share":
                allocated_amount = amount / len(self.current_goals) if self.current_goals else amount
            else:
                allocated_amount = amount
            
            # Ensure we don't over-allocate
            current_total = sum(sum(alloc.values()) for alloc in self.resource_allocation.values())
            if current_total + allocated_amount <= 1.0:
                if goal_id:
                    self.resource_allocation[goal_id][resource_type] = allocated_amount
                total_allocation += allocated_amount
                allocation_details[resource_type] = allocated_amount
            else:
                # Resource constraint violation
                available = 1.0 - current_total
                allocation_details[resource_type] = available
                total_allocation += available
                break
        
        return {
            "goal_id": goal_id,
            "allocation_strategy": allocation_strategy,
            "allocated_resources": allocation_details,
            "total_allocation": total_allocation,
            "resource_utilization": sum(sum(alloc.values()) for alloc in self.resource_allocation.values())
        }
    
    async def _make_advanced_decision(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Advanced decision making with multiple criteria"""
        decision_context = input_data.get("context", "")
        options = input_data.get("options", [])
        criteria = input_data.get("criteria", ["utility", "feasibility", "risk"])
        decision_strategy = input_data.get("strategy", "multi_criteria")
        
        if not options:
            return {"decision": "no_action", "reason": "No options provided"}
        
        # Multi-criteria decision analysis
        option_scores = {}
        
        for option in options:
            scores = {}
            
            for criterion in criteria:
                if criterion == "utility":
                    scores[criterion] = self._assess_utility(option, decision_context)
                elif criterion == "feasibility":
                    scores[criterion] = self._assess_feasibility(option, decision_context)
                elif criterion == "risk":
                    scores[criterion] = 1.0 - self._assess_risk(option, decision_context)
                elif criterion == "goal_alignment":
                    scores[criterion] = self._assess_goal_alignment(option)
                else:
                    scores[criterion] = 0.5  # Default neutral score
            
            # Weighted combination
            weights = input_data.get("criterion_weights", {c: 1.0/len(criteria) for c in criteria})
            total_score = sum(scores[c] * weights.get(c, 1.0/len(criteria)) for c in criteria)
            option_scores[option] = {
                "total_score": total_score,
                "criterion_scores": scores
            }
        
        # Select best option
        best_option = max(option_scores.keys(), key=lambda o: option_scores[o]["total_score"])
        
        # Record decision
        decision_record = {
            "context": decision_context,
            "options": options,
            "criteria": criteria,
            "option_scores": option_scores,
            "decision": best_option,
            "confidence": option_scores[best_option]["total_score"],
            "timestamp": datetime.now()
        }
        
        self.decision_history.append(decision_record)
        
        return {
            "decision": best_option,
            "confidence": option_scores[best_option]["total_score"],
            "reasoning": option_scores[best_option]["criterion_scores"],
            "alternative_scores": {k: v["total_score"] for k, v in option_scores.items()},
            "decision_strategy": decision_strategy
        }
    
    async def _update_goals_advanced(self) -> Dict[str, Any]:
        """Advanced goal updating with progress assessment and adaptation"""
        updated_goals = []
        completed_goals = []
        
        for goal in self.current_goals[:]:  # Copy to avoid modification during iteration
            # Update progress
            goal.update_progress()
            
            # Check for completion
            if goal.status == "completed":
                self.current_goals.remove(goal)
                self.completed_goals.append(goal)
                completed_goals.append(goal.description)
            else:
                updated_goals.append(goal.description)
        
        # Clean up old goals
        self._prioritize_goals()
        
        return {
            "updated_goals": len(updated_goals),
            "completed_goals": len(completed_goals),
            "completed_goal_descriptions": completed_goals,
            "total_active_goals": len(self.current_goals)
        }
    
    def _prioritize_goals(self):
        """Prioritize goals based on multiple factors"""
        current_time = datetime.now()
        
        for goal in self.current_goals:
            # Adjust priority based on deadline proximity
            if goal.deadline:
                time_to_deadline = (goal.deadline - current_time).total_seconds()
                if time_to_deadline > 0:
                    urgency_factor = max(0.1, 1.0 - (time_to_deadline / (7 * 24 * 3600)))  # 7 days baseline
                    goal.priority = min(1.0, goal.priority + urgency_factor * 0.2)
        
        # Sort goals by priority
        self.current_goals.sort(key=lambda g: g.priority, reverse=True)
    
    async def _create_contingency_plans(self, goal: Goal, plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create contingency plans for potential failures"""
        contingencies = []
        
        for action in plan:
            # Create simple contingency for each action
            contingency = {
                "original_action": action["action"],
                "risk_factors": ["resource_shortage", "time_constraint", "complexity_underestimation"],
                "alternative_actions": [
                    f"simplify_{action['action']}",
                    f"delegate_{action['action']}",
                    f"postpone_{action['action']}"
                ],
                "trigger_conditions": {
                    "resource_availability": 0.3,
                    "time_remaining": 0.2,
                    "success_probability": 0.4
                }
            }
            contingencies.append(contingency)
        
        return contingencies
    
    def _schedule_actions(self, plan: List[Dict[str, Any]], constraints: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Schedule actions from plan considering constraints"""
        scheduled_actions = []
        current_time = datetime.now()
        
        for i, action in enumerate(plan):
            scheduled_time = current_time + timedelta(hours=i * 2)  # Simple 2-hour intervals
            
            scheduled_action = {
                "action": action["action"],
                "scheduled_time": scheduled_time,
                "estimated_duration": timedelta(hours=1),  # Default 1 hour
                "prerequisites": plan[:i],  # Previous actions as prerequisites
                "resources_required": constraints.get("resources", {}),
                "priority": action.get("level", 1)
            }
            
            scheduled_actions.append(scheduled_action)
        
        return scheduled_actions
    
    def _estimate_plan_duration(self, plan: List[Dict[str, Any]]) -> timedelta:
        """Estimate total duration for plan execution"""
        base_duration_per_action = timedelta(hours=1)
        complexity_multiplier = 1.0
        
        for action in plan:
            if "complex" in action.get("action", "").lower():
                complexity_multiplier += 0.5
            elif "simple" in action.get("action", "").lower():
                complexity_multiplier += 0.2
            else:
                complexity_multiplier += 0.3
        
        total_duration = base_duration_per_action * len(plan) * complexity_multiplier
        return total_duration
    
    def _assess_goal_progress(self, goal: Goal, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess progress toward a specific goal"""
        progress_update = {
            "goal_id": getattr(goal, 'id', 'unknown'),
            "description": goal.description,
            "current_progress": goal.progress,
            "priority": goal.priority,
            "status": goal.status,
            "time_since_creation": (datetime.now() - goal.created_at).total_seconds() / 3600  # hours
        }
        
        # Assess progress based on performance data
        relevant_metrics = self._extract_relevant_metrics(goal, performance_data)
        if relevant_metrics:
            estimated_progress = np.mean(list(relevant_metrics.values()))
            progress_update["estimated_progress"] = estimated_progress
            
            # Update goal progress if estimated progress is significantly different
            if abs(estimated_progress - goal.progress) > 0.1:
                goal.progress = estimated_progress
                progress_update["progress_updated"] = True
        
        return progress_update
    
    def _extract_relevant_metrics(self, goal: Goal, performance_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract performance metrics relevant to a specific goal"""
        relevant_metrics = {}
        goal_keywords = set(goal.description.lower().split())
        
        for metric, value in performance_data.items():
            if isinstance(value, (int, float)):
                metric_keywords = set(metric.lower().split('_'))
                overlap = len(goal_keywords & metric_keywords)
                
                if overlap > 0:
                    relevant_metrics[metric] = value
        
        return relevant_metrics
    
    def _detect_errors(self, performance_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect errors or anomalies in performance"""
        errors = []
        
        for metric, value in performance_data.items():
            if isinstance(value, (int, float)):
                # Check for anomalous values
                if value < 0.0 or value > 1.0:
                    errors.append({
                        "type": "value_out_of_range",
                        "metric": metric,
                        "value": value,
                        "expected_range": "[0.0, 1.0]",
                        "severity": "high"
                    })
                elif value < 0.2:  # Very low performance
                    errors.append({
                        "type": "performance_degradation",
                        "metric": metric,
                        "value": value,
                        "threshold": 0.2,
                        "severity": "medium"
                    })
        
        return errors
    
    def _evaluate_performance(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate overall performance"""
        if not performance_data:
            return {"overall_score": 0.5, "assessment": "insufficient_data"}
        
        valid_metrics = {k: v for k, v in performance_data.items() 
                        if isinstance(v, (int, float)) and 0.0 <= v <= 1.0}
        
        if not valid_metrics:
            return {"overall_score": 0.5, "assessment": "no_valid_metrics"}
        
        overall_score = np.mean(list(valid_metrics.values()))
        
        if overall_score >= 0.8:
            assessment = "excellent"
        elif overall_score >= 0.6:
            assessment = "good"
        elif overall_score >= 0.4:
            assessment = "fair"
        else:
            assessment = "needs_improvement"
        
        return {
            "overall_score": overall_score,
            "assessment": assessment,
            "metric_count": len(valid_metrics),
            "best_metric": max(valid_metrics.keys(), key=lambda k: valid_metrics[k]) if valid_metrics else None,
            "worst_metric": min(valid_metrics.keys(), key=lambda k: valid_metrics[k]) if valid_metrics else None
        }
    
    def _check_adaptation_triggers(self, monitoring_results: Dict[str, Any]) -> bool:
        """Check if adaptation is needed based on monitoring results"""
        adaptation_needed = False
        
        for goal_id, result in monitoring_results.items():
            if isinstance(result, dict):
                # Check for poor performance
                if result.get("estimated_progress", 1.0) < 0.3:
                    adaptation_needed = True
                
                # Check for stalled progress
                if result.get("progress_updated") is False and result.get("time_since_creation", 0) > 24:
                    adaptation_needed = True
        
        return adaptation_needed
    
    def _adapt_to_poor_performance(self, metric: str, current_value: float, expected_value: float) -> Dict[str, Any]:
        """Adapt strategy based on poor performance"""
        performance_gap = expected_value - current_value
        
        adaptation = {
            "type": "performance_adaptation",
            "metric": metric,
            "performance_gap": performance_gap,
            "adaptations": []
        }
        
        if "attention" in metric.lower():
            adaptation["adaptations"].append("increase_focus_training")
        elif "memory" in metric.lower():
            adaptation["adaptations"].append("enhance_rehearsal_strategies")
        elif "execution" in metric.lower():
            adaptation["adaptations"].append("simplify_action_plans")
        else:
            adaptation["adaptations"].append("general_strategy_review")
        
        # Adjust cognitive flexibility
        self.cognitive_flexibility = min(1.0, self.cognitive_flexibility + 0.02)
        
        return adaptation
    
    def _adapt_to_high_load(self) -> Dict[str, Any]:
        """Adapt to high cognitive load"""
        adaptation = {
            "type": "load_adaptation",
            "current_load": self.cognitive_load,
            "adaptations": [
                "reduce_parallel_processing",
                "simplify_current_goals",
                "increase_rest_periods"
            ]
        }
        
        # Reduce resource allocation to non-critical goals
        for goal_id, resources in self.resource_allocation.items():
            for resource_type in resources:
                resources[resource_type] *= 0.8  # 20% reduction
        
        return adaptation
    
    def _detect_goal_conflicts(self) -> List[Dict[str, Any]]:
        """Detect conflicts between current goals"""
        conflicts = []
        
        for i, goal1 in enumerate(self.current_goals):
            for j, goal2 in enumerate(self.current_goals[i+1:], i+1):
                # Simple conflict detection based on keyword overlap and priority
                words1 = set(goal1.description.lower().split())
                words2 = set(goal2.description.lower().split())
                
                overlap = len(words1 & words2)
                if overlap > 0 and abs(goal1.priority - goal2.priority) < 0.1:
                    conflicts.append({
                        "goal1_id": getattr(goal1, 'id', i),
                        "goal2_id": getattr(goal2, 'id', j),
                        "conflict_type": "resource_competition",
                        "severity": overlap / len(words1 | words2)
                    })
        
        return conflicts
    
    def _resolve_goal_conflict(self, conflict: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve a goal conflict"""
        resolution = {
            "conflict": conflict,
            "resolution_strategy": "priority_adjustment",
            "actions_taken": []
        }
        
        # Find the conflicting goals
        goal1 = self._find_goal_by_id(conflict["goal1_id"])
        goal2 = self._find_goal_by_id(conflict["goal2_id"])
        
        if goal1 and goal2:
            # Adjust priorities to reduce conflict
            if goal1.priority > goal2.priority:
                goal1.priority = min(1.0, goal1.priority + 0.1)
                goal2.priority = max(0.1, goal2.priority - 0.1)
                resolution["actions_taken"].append("increased_priority_goal1")
            else:
                goal2.priority = min(1.0, goal2.priority + 0.1)
                goal1.priority = max(0.1, goal1.priority - 0.1)
                resolution["actions_taken"].append("increased_priority_goal2")
        
        return resolution
    
    def _calculate_switch_cost(self, current_task: Optional[str], new_task: str, switch_type: str) -> float:
        """Calculate cognitive cost of task switching"""
        base_cost = 0.1
        
        if not current_task:
            return base_cost * 0.5  # Lower cost when no current task
        
        # Calculate similarity between tasks
        if current_task and new_task:
            current_words = set(current_task.lower().split())
            new_words = set(new_task.lower().split())
            similarity = len(current_words & new_words) / len(current_words | new_words) if (current_words | new_words) else 0
            
            # Higher similarity = lower switch cost
            similarity_factor = 1.0 - similarity
        else:
            similarity_factor = 1.0
        
        # Switch type affects cost
        switch_type_multiplier = {
            "voluntary": 1.0,
            "involuntary": 1.5,
            "emergency": 2.0
        }.get(switch_type, 1.0)
        
        total_cost = base_cost * similarity_factor * switch_type_multiplier
        return min(0.5, total_cost)  # Cap at 50% resource cost
    
    def _apply_immediate_suppression(self, target: str, strength: float) -> Dict[str, Any]:
        """Apply immediate inhibitory effects"""
        suppression_result = {
            "target": target,
            "suppression_strength": strength,
            "effects": []
        }
        
        # Reduce attention to target
        if target in getattr(self, 'attention_weights', {}):
            original_weight = self.attention_weights[target]
            self.attention_weights[target] *= (1.0 - strength)
            suppression_result["effects"].append({
                "type": "attention_reduction",
                "original_weight": original_weight,
                "new_weight": self.attention_weights[target]
            })
        
        # Reduce resource allocation to target-related goals
        target_words = set(target.lower().split())
        for goal in self.current_goals:
            goal_words = set(goal.description.lower().split())
            if len(target_words & goal_words) > 0:
                original_priority = goal.priority
                goal.priority *= (1.0 - strength * 0.5)  # Partial suppression
                suppression_result["effects"].append({
                    "type": "goal_priority_reduction",
                    "goal": goal.description,
                    "original_priority": original_priority,
                    "new_priority": goal.priority
                })
        
        return suppression_result
    
    def _get_hierarchy_level(self, goal_id: str) -> int:
        """Get the hierarchy level of a goal"""
        level = 0
        current_id = goal_id
        
        # Traverse up the hierarchy
        for parent_id, children in self.goal_hierarchy.items():
            if current_id in children:
                level += 1
                current_id = parent_id
                # Continue traversing if this parent has a parent
                found_higher_parent = False
                for higher_parent_id, higher_children in self.goal_hierarchy.items():
                    if parent_id in higher_children:
                        found_higher_parent = True
                        break
                if not found_higher_parent:
                    break
        
        return level
    
    async def _get_executive_status(self) -> Dict[str, Any]:
        """Get current executive control status"""
        return self.get_status()
    
    def _register_default_strategies(self):
        """Register default planning strategies"""
        self.planning_strategies.update({
            "hierarchical_decomposition": self._hierarchical_decomposition_strategy,
            "means_ends_analysis": self._means_ends_analysis_strategy,
            "forward_chaining": self._forward_chaining_strategy,
            "backward_chaining": self._backward_chaining_strategy
        })
    
    async def _hierarchical_decomposition_strategy(self, goal: Goal, depth: int, constraints: Dict) -> List[Dict[str, Any]]:
        """Hierarchical decomposition planning strategy"""
        plan = []
        
        if depth <= 0:
            return [{"action": f"execute_{goal.description}", "level": 0}]
        
        # Simple decomposition based on goal description keywords
        if "learn" in goal.description.lower():
            plan.extend([
                {"action": "identify_learning_objectives", "level": depth},
                {"action": "gather_resources", "level": depth},
                {"action": "study_materials", "level": depth},
                {"action": "practice_skills", "level": depth},
                {"action": "evaluate_progress", "level": depth}
            ])
        elif "solve" in goal.description.lower():
            plan.extend([
                {"action": "understand_problem", "level": depth},
                {"action": "brainstorm_solutions", "level": depth},
                {"action": "evaluate_options", "level": depth},
                {"action": "implement_solution", "level": depth},
                {"action": "test_results", "level": depth}
            ])
        else:
            plan.append({"action": f"complete_{goal.description}", "level": depth})
        
        return plan
    
    async def _means_ends_analysis_strategy(self, goal: Goal, depth: int, constraints: Dict) -> List[Dict[str, Any]]:
        """Means-ends analysis planning strategy"""
        current_state = constraints.get("current_state", "initial")
        target_state = goal.description
        
        plan = [
            {"action": f"analyze_gap_between_{current_state}_and_{target_state}", "level": depth},
            {"action": f"identify_operators_to_reduce_gap", "level": depth},
            {"action": f"apply_operators_sequentially", "level": depth}
        ]
        
        return plan
    
    async def _forward_chaining_strategy(self, goal: Goal, depth: int, constraints: Dict) -> List[Dict[str, Any]]:
        """Forward chaining planning strategy"""
        initial_facts = constraints.get("initial_facts", [])
        
        plan = [
            {"action": f"start_from_initial_state", "level": depth},
            {"action": f"apply_forward_rules", "level": depth},
            {"action": f"reach_goal_state", "level": depth}
        ]
        
        return plan
    
    async def _backward_chaining_strategy(self, goal: Goal, depth: int, constraints: Dict) -> List[Dict[str, Any]]:
        """Backward chaining planning strategy"""
        plan = [
            {"action": f"start_from_goal_{goal.description}", "level": depth},
            {"action": f"identify_prerequisites", "level": depth},
            {"action": f"work_backwards_to_current_state", "level": depth}
        ]
        
        return plan
    
    def _find_goal_by_id(self, goal_id: str) -> Optional[Goal]:
        """Find goal by its ID"""
        for goal in self.current_goals + self.completed_goals:
            if hasattr(goal, 'id') and goal.id == goal_id:
                return goal
        return None
    
    def _assess_utility(self, option: str, context: str) -> float:
        """Assess utility of an option"""
        # Simple utility assessment - could be enhanced with learned preferences
        utility_keywords = ["benefit", "gain", "improve", "solve", "achieve"]
        option_lower = option.lower()
        
        utility_score = 0.5  # Base utility
        for keyword in utility_keywords:
            if keyword in option_lower:
                utility_score += 0.1
        
        return min(1.0, utility_score)
    
    def _assess_feasibility(self, option: str, context: str) -> float:
        """Assess feasibility of an option"""
        # Consider resource constraints and current capabilities
        feasibility = 0.7  # Base feasibility
        
        # Adjust based on resource availability
        if self.executive_resources < 0.3:
            feasibility *= 0.7  # Reduced feasibility with low resources
        
        if self.cognitive_load > 0.8:
            feasibility *= 0.6  # Reduced feasibility with high load
        
        return feasibility
    
    def _assess_risk(self, option: str, context: str) -> float:
        """Assess risk of an option"""
        risk_keywords = ["risk", "danger", "uncertain", "complex", "difficult"]
        option_lower = option.lower()
        
        risk_score = 0.3  # Base risk
        for keyword in risk_keywords:
            if keyword in option_lower:
                risk_score += 0.1
        
        return min(1.0, risk_score)
    
    def _assess_goal_alignment(self, option: str) -> float:
        """Assess how well option aligns with current goals"""
        if not self.current_goals:
            return 0.5
        
        alignment_scores = []
        option_words = set(option.lower().split())
        
        for goal in self.current_goals:
            goal_words = set(goal.description.lower().split())
            overlap = len(option_words & goal_words)
            total_words = len(option_words | goal_words)
            
            if total_words > 0:
                alignment = overlap / total_words
                alignment_scores.append(alignment * goal.priority)
        
        return np.mean(alignment_scores) if alignment_scores else 0.5
    
    def get_status(self) -> Dict[str, Any]:
        goal_stats = {
            "active": len(self.current_goals),
            "completed": len(self.completed_goals),
            "avg_priority": np.mean([g.priority for g in self.current_goals]) if self.current_goals else 0,
            "hierarchy_depth": max([self._get_hierarchy_level(getattr(g, 'id', '')) 
                                  for g in self.current_goals] + [0])
        }
        
        resource_stats = {
            "total_allocated": sum(sum(alloc.values()) for alloc in self.resource_allocation.values()),
            "allocation_efficiency": len(self.resource_allocation) / max(1, len(self.current_goals))
        }
        
        return {
            "name": self.name,
            "goal_statistics": goal_stats,
            "resource_statistics": resource_stats,
            "executive_resources": self.executive_resources,
            "cognitive_load": self.cognitive_load,
            "cognitive_flexibility": self.cognitive_flexibility,
            "current_strategy": self.current_strategy,
            "active_inhibitions": len([r for r in self.inhibition_rules if r["active"]]),
            "pending_actions": len(self.action_queue),
            "recent_decisions": len([d for d in self.decision_history 
                                   if (datetime.now() - d["timestamp"]).seconds < 3600]),
            "last_update": self.last_update.isoformat()
        }


class MetaCognition(CognitiveComponent):
    """Advanced meta-cognition with self-awareness and cognitive monitoring"""
    
    def __init__(self):
        super().__init__("MetaCognition")
        self.self_model: Dict[str, Any] = {
            "cognitive_strengths": [],
            "cognitive_weaknesses": [],
            "learning_preferences": {},
            "confidence_levels": {},
            "performance_metrics": {},
            "knowledge_domains": {},
            "cognitive_biases": {},
            "metacognitive_strategies": {}
        }
        
        # Advanced metacognitive capabilities
        self.reflection_history: List[Dict[str, Any]] = []
        self.self_improvement_goals: List[Goal] = []
        self.cognitive_monitoring: Dict[str, Any] = {}
        self.strategy_effectiveness: Dict[str, List[float]] = defaultdict(list)
        self.metacognitive_awareness: float = 0.6
        
        # Self-assessment and monitoring
        self.performance_tracking: Dict[str, List[float]] = defaultdict(list)
        self.confidence_calibration: Dict[str, float] = {}
        self.knowledge_assessment: Dict[str, Dict[str, float]] = {}
        self.cognitive_load_awareness: float = 0.0
        
        # Strategy management
        self.available_strategies: Dict[str, Dict[str, Any]] = {}
        self.strategy_selection_history: List[Dict[str, Any]] = []
        self.adaptive_strategy_parameters: Dict[str, float] = {}
        
        # Self-modification capabilities
        self.self_modification_log: List[Dict[str, Any]] = []
        self.improvement_tracking: Dict[str, List[float]] = defaultdict(list)
        self.cognitive_plasticity: float = 0.7
        
        self._initialize_default_strategies()
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Advanced metacognitive processing"""
        action = input_data.get("action")
        
        if action == "self_reflect":
            return await self._conduct_comprehensive_reflection(input_data)
        elif action == "monitor_cognition":
            return await self._monitor_cognitive_processes(input_data)
        elif action == "assess_performance":
            return await self._assess_cognitive_performance(input_data)
        elif action == "select_strategy":
            return await self._select_optimal_strategy(input_data)
        elif action == "calibrate_confidence":
            return await self._calibrate_confidence(input_data)
        elif action == "update_self_model":
            return await self._update_self_model(input_data)
        elif action == "plan_improvement":
            return await self._plan_cognitive_improvement(input_data)
        elif action == "modify_cognition":
            return await self._modify_cognitive_processes(input_data)
        else:
            return await self._get_metacognitive_status()
    
    async def _conduct_comprehensive_reflection(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct deep self-reflection on cognitive processes"""
        domain = input_data.get("domain", "general")
        performance_data = input_data.get("performance_data", {})
        reflection_depth = input_data.get("depth", "deep")
        
        reflection = {
            "domain": domain,
            "timestamp": datetime.now(),
            "reflection_depth": reflection_depth,
            "performance_analysis": self._analyze_performance_deeply(performance_data),
            "cognitive_insights": await self._generate_cognitive_insights(domain, performance_data),
            "strategy_evaluation": self._evaluate_current_strategies(domain),
            "improvement_opportunities": self._identify_improvement_opportunities(performance_data),
            "metacognitive_awareness_update": self._update_metacognitive_awareness(performance_data),
            "confidence_assessment": self._assess_domain_confidence(domain),
            "learning_insights": self._extract_learning_insights(performance_data)
        }
        
        self.reflection_history.append(reflection)
        
        # Update self-model based on reflection
        await self._integrate_reflection_insights(reflection)
        
        # Keep reflection history manageable
        if len(self.reflection_history) > 100:
            self.reflection_history.pop(0)
        
        return reflection
    
    async def _monitor_cognitive_processes(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor ongoing cognitive processes for efficiency and effectiveness"""
        process_type = input_data.get("process_type", "general")
        monitoring_window = input_data.get("window_minutes", 30)
        
        monitoring_data = {
            "process_type": process_type,
            "monitoring_window": monitoring_window,
            "timestamp": datetime.now()
        }
        
        # Monitor attention allocation
        attention_metrics = self._monitor_attention_allocation(input_data)
        monitoring_data["attention_metrics"] = attention_metrics
        
        # Monitor working memory usage
        memory_metrics = self._monitor_memory_usage(input_data)
        monitoring_data["memory_metrics"] = memory_metrics
        
        # Monitor executive control efficiency
        executive_metrics = self._monitor_executive_efficiency(input_data)
        monitoring_data["executive_metrics"] = executive_metrics
        
        # Monitor emotional regulation
        emotional_metrics = self._monitor_emotional_processes(input_data)
        monitoring_data["emotional_metrics"] = emotional_metrics
        
        # Overall cognitive load assessment
        cognitive_load = self._assess_current_cognitive_load(monitoring_data)
        monitoring_data["cognitive_load"] = cognitive_load
        self.cognitive_load_awareness = cognitive_load
        
        # Store monitoring data
        self.cognitive_monitoring[process_type] = monitoring_data
        
        return monitoring_data
    
    async def _assess_cognitive_performance(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive assessment of cognitive performance"""
        assessment_type = input_data.get("assessment_type", "comprehensive")
        time_period = input_data.get("time_period", "recent")
        performance_data = input_data.get("performance_data", {})
        
        assessment = {
            "assessment_type": assessment_type,
            "time_period": time_period,
            "timestamp": datetime.now()
        }
        
        if assessment_type == "comprehensive":
            # Multi-dimensional performance assessment
            assessment.update({
                "learning_efficiency": self._assess_learning_efficiency(performance_data),
                "problem_solving_ability": self._assess_problem_solving(performance_data),
                "memory_performance": self._assess_memory_performance(performance_data),
                "attention_control": self._assess_attention_control(performance_data),
                "executive_function": self._assess_executive_function(performance_data),
                "emotional_regulation": self._assess_emotional_regulation(performance_data),
                "metacognitive_accuracy": self._assess_metacognitive_accuracy(performance_data)
            })
        
        # Performance trend analysis
        performance_trends = self._analyze_performance_trends(assessment)
        assessment["performance_trends"] = performance_trends
        
        # Identify strengths and weaknesses
        strengths_weaknesses = self._identify_strengths_weaknesses(assessment)
        assessment.update(strengths_weaknesses)
        
        # Update performance tracking
        for metric, value in assessment.items():
            if isinstance(value, (int, float)):
                self.performance_tracking[metric].append(value)
        
        return assessment
    
    def _analyze_performance_trends(self, assessment: Dict[str, Any]) -> Dict[str, str]:
        """Analyze performance trends from assessment data"""
        trends = {}
        
        for metric, value in assessment.items():
            if isinstance(value, (int, float)) and metric in self.performance_tracking:
                recent_values = self.performance_tracking[metric][-5:]
                if len(recent_values) >= 3:
                    trend = self._calculate_trend(recent_values)
                    trends[metric] = trend
        
        return trends
    
    def _identify_strengths_weaknesses(self, assessment: Dict[str, Any]) -> Dict[str, List[str]]:
        """Identify cognitive strengths and weaknesses from assessment"""
        strengths = []
        weaknesses = []
        
        for metric, value in assessment.items():
            if isinstance(value, (int, float)):
                if value >= 0.8:
                    strengths.append(metric)
                elif value <= 0.4:
                    weaknesses.append(metric)
        
        return {"strengths": strengths, "weaknesses": weaknesses}
    
    def _evaluate_strategy_effectiveness(self, strategy: Dict[str, Any], task_type: str, context: Dict[str, Any]) -> float:
        """Evaluate effectiveness of a strategy for current context"""
        base_effectiveness = strategy.get("confidence", 0.5)
        
        # Check if strategy is suitable for task type
        suitable_domains = strategy.get("effectiveness_domains", [])
        domain_match = any(domain in task_type.lower() for domain in suitable_domains)
        
        if domain_match:
            domain_bonus = 0.2
        else:
            domain_bonus = -0.1
        
        # Adjust for context complexity
        context_complexity = len(str(context)) / 100.0  # Simple complexity measure
        complexity_penalty = min(0.1, context_complexity * 0.05)
        
        effectiveness = base_effectiveness + domain_bonus - complexity_penalty
        return max(0.0, min(1.0, effectiveness))
    
    def _calculate_calibration_trend(self, domain_calibrations: List[Dict[str, Any]]) -> str:
        """Calculate trend in confidence calibration"""
        if len(domain_calibrations) < 3:
            return "stable"
        
        recent_errors = [c["error"] for c in domain_calibrations[-3:]]
        earlier_errors = [c["error"] for c in domain_calibrations[-6:-3]] if len(domain_calibrations) >= 6 else []
        
        if not earlier_errors:
            return "stable"
        
        recent_avg = np.mean(recent_errors)
        earlier_avg = np.mean(earlier_errors)
        
        if recent_avg < earlier_avg * 0.8:
            return "improving"
        elif recent_avg > earlier_avg * 1.2:
            return "declining"
        else:
            return "stable"
    
    def _assess_confidence(self, domain: str) -> float:
        """Assess current confidence in a domain"""
        # Get historical performance in domain
        domain_performance = []
        for metric, values in self.performance_tracking.items():
            if domain.lower() in metric.lower() and values:
                domain_performance.extend(values[-5:])  # Recent performance
        
        if domain_performance:
            avg_performance = np.mean(domain_performance)
            # Confidence should roughly match performance but with some uncertainty
            confidence = avg_performance * 0.9  # Slight underconfidence bias
        else:
            confidence = 0.5  # Default moderate confidence
        
        return max(0.1, min(0.9, confidence))
    
    async def _get_metacognitive_status(self) -> Dict[str, Any]:
        """Get current metacognitive status"""
        return self.get_status()
    
    async def _update_self_model(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update the self-model based on new information"""
        update_type = input_data.get("update_type", "general")
        new_information = input_data.get("information", {})
        
        updates_made = []
        
        if update_type == "strength":
            domain = new_information.get("domain")
            if domain and domain not in self.self_model["cognitive_strengths"]:
                self.self_model["cognitive_strengths"].append(domain)
                updates_made.append(f"Added strength: {domain}")
        
        elif update_type == "weakness":
            domain = new_information.get("domain")
            if domain and domain not in self.self_model["cognitive_weaknesses"]:
                self.self_model["cognitive_weaknesses"].append(domain)
                updates_made.append(f"Added weakness: {domain}")
        
        elif update_type == "preference":
            preference_type = new_information.get("type")
            preference_value = new_information.get("value")
            if preference_type and preference_value:
                self.self_model["learning_preferences"][preference_type] = preference_value
                updates_made.append(f"Updated preference: {preference_type}")
        
        return {
            "update_type": update_type,
            "updates_made": updates_made,
            "self_model_size": len(self.self_model)
        }
    
    async def _plan_cognitive_improvement(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Plan cognitive improvement based on current assessment"""
        target_area = input_data.get("target_area", "general")
        improvement_timeline = input_data.get("timeline_days", 30)
        
        # Identify improvement opportunities
        opportunities = self._identify_improvement_opportunities({})
        
        # Create improvement goals
        improvement_goals = []
        for opportunity in opportunities[:3]:  # Top 3 opportunities
            goal = Goal(
                description=f"Improve {opportunity.get('metric', target_area)}",
                priority=0.7,
                deadline=datetime.now() + timedelta(days=improvement_timeline)
            )
            improvement_goals.append(goal)
            self.self_improvement_goals.append(goal)
        
        return {
            "target_area": target_area,
            "improvement_timeline": improvement_timeline,
            "goals_created": len(improvement_goals),
            "total_improvement_goals": len(self.self_improvement_goals),
            "opportunities_identified": len(opportunities)
        }
    
    async def _modify_cognitive_processes(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Modify cognitive processes for self-improvement"""
        modification_type = input_data.get("modification_type", "strategy_adjustment")
        target_process = input_data.get("target_process", "general")
        modification_strength = input_data.get("strength", 0.1)
        
        modification_record = {
            "type": modification_type,
            "target": target_process,
            "strength": modification_strength,
            "timestamp": datetime.now(),
            "effects": []
        }
        
        if modification_type == "strategy_adjustment":
            # Adjust strategy parameters
            if target_process in self.adaptive_strategy_parameters:
                old_value = self.adaptive_strategy_parameters[target_process]
                self.adaptive_strategy_parameters[target_process] += modification_strength
                modification_record["effects"].append({
                    "parameter": target_process,
                    "old_value": old_value,
                    "new_value": self.adaptive_strategy_parameters[target_process]
                })
            else:
                self.adaptive_strategy_parameters[target_process] = 0.5 + modification_strength
                modification_record["effects"].append({
                    "parameter": target_process,
                    "initial_value": 0.5 + modification_strength
                })
        
        elif modification_type == "awareness_enhancement":
            # Enhance metacognitive awareness
            old_awareness = self.metacognitive_awareness
            self.metacognitive_awareness = min(1.0, self.metacognitive_awareness + modification_strength)
            modification_record["effects"].append({
                "awareness_change": self.metacognitive_awareness - old_awareness
            })
        
        self.self_modification_log.append(modification_record)
        
        return {
            "modification_applied": True,
            "modification_record": modification_record,
            "total_modifications": len(self.self_modification_log)
        }
    
    async def _select_optimal_strategy(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Select optimal cognitive strategy for current context"""
        task_type = input_data.get("task_type", "general")
        context = input_data.get("context", {})
        available_strategies = input_data.get("strategies", list(self.available_strategies.keys()))
        
        strategy_evaluation = {}
        
        for strategy_name in available_strategies:
            if strategy_name in self.available_strategies:
                strategy = self.available_strategies[strategy_name]
                
                # Evaluate strategy effectiveness for current context
                effectiveness_score = self._evaluate_strategy_effectiveness(
                    strategy, task_type, context
                )
                
                # Consider past performance of this strategy
                historical_performance = np.mean(self.strategy_effectiveness[strategy_name]) \
                    if self.strategy_effectiveness[strategy_name] else 0.5
                
                # Combine current and historical assessments
                combined_score = (effectiveness_score * 0.6 + historical_performance * 0.4)
                
                strategy_evaluation[strategy_name] = {
                    "effectiveness_score": effectiveness_score,
                    "historical_performance": historical_performance,
                    "combined_score": combined_score,
                    "confidence": strategy.get("confidence", 0.5)
                }
        
        # Select best strategy
        if strategy_evaluation:
            best_strategy = max(strategy_evaluation.keys(), 
                              key=lambda s: strategy_evaluation[s]["combined_score"])
        else:
            best_strategy = "default"
        
        # Record strategy selection
        selection_record = {
            "task_type": task_type,
            "context": context,
            "available_strategies": available_strategies,
            "strategy_evaluation": strategy_evaluation,
            "selected_strategy": best_strategy,
            "timestamp": datetime.now()
        }
        
        self.strategy_selection_history.append(selection_record)
        
        return {
            "selected_strategy": best_strategy,
            "strategy_evaluation": strategy_evaluation,
            "selection_confidence": strategy_evaluation.get(best_strategy, {}).get("combined_score", 0.5),
            "alternative_strategies": sorted(strategy_evaluation.keys(), 
                                           key=lambda s: strategy_evaluation[s]["combined_score"], 
                                           reverse=True)[1:3]
        }
    
    async def _calibrate_confidence(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calibrate confidence estimates with actual performance"""
        domain = input_data.get("domain", "general")
        predicted_performance = input_data.get("predicted_performance")
        actual_performance = input_data.get("actual_performance")
        
        if predicted_performance is not None and actual_performance is not None:
            # Calculate calibration error
            calibration_error = abs(predicted_performance - actual_performance)
            
            # Update confidence calibration for this domain
            if domain not in self.confidence_calibration:
                self.confidence_calibration[domain] = []
            
            self.confidence_calibration[domain].append({
                "predicted": predicted_performance,
                "actual": actual_performance,
                "error": calibration_error,
                "timestamp": datetime.now()
            })
            
            # Calculate domain-specific calibration metrics
            domain_calibrations = self.confidence_calibration[domain]
            mean_error = np.mean([c["error"] for c in domain_calibrations])
            calibration_trend = self._calculate_calibration_trend(domain_calibrations)
            
            # Update self-model confidence levels
            current_confidence = self.self_model["confidence_levels"].get(domain, 0.5)
            
            if calibration_error < 0.1:  # Good calibration
                adjusted_confidence = min(1.0, current_confidence + 0.05)
            elif calibration_error > 0.3:  # Poor calibration
                adjusted_confidence = max(0.1, current_confidence - 0.1)
            else:
                adjusted_confidence = current_confidence
            
            self.self_model["confidence_levels"][domain] = adjusted_confidence
            
            return {
                "domain": domain,
                "calibration_error": calibration_error,
                "mean_domain_error": mean_error,
                "calibration_trend": calibration_trend,
                "adjusted_confidence": adjusted_confidence,
                "calibration_quality": "good" if mean_error < 0.15 else "needs_improvement"
            }
        
        else:
            # Assess confidence without explicit performance comparison
            current_confidence = self._assess_confidence(domain)
            return {
                "domain": domain,
                "current_confidence": current_confidence,
                "assessment_basis": "internal_evaluation"
            }
    
    def _analyze_performance_deeply(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Deep analysis of performance data"""
        analysis = {
            "raw_metrics": performance_data,
            "normalized_scores": {},
            "performance_patterns": {},
            "anomalies": [],
            "improvement_areas": []
        }
        
        # Normalize performance metrics
        for metric, value in performance_data.items():
            if isinstance(value, (int, float)):
                # Simple normalization (0-1 scale)
                normalized = max(0.0, min(1.0, value))
                analysis["normalized_scores"][metric] = normalized
                
                # Identify patterns
                if metric in self.performance_tracking:
                    recent_values = self.performance_tracking[metric][-10:]
                    if recent_values:
                        trend = self._calculate_trend(recent_values)
                        analysis["performance_patterns"][metric] = trend
                
                # Detect anomalies
                if self._is_performance_anomaly(metric, value):
                    analysis["anomalies"].append({
                        "metric": metric,
                        "value": value,
                        "expected_range": self._get_expected_range(metric)
                    })
                
                # Identify improvement areas
                if normalized < 0.6:  # Below acceptable threshold
                    analysis["improvement_areas"].append(metric)
        
        return analysis
    
    async def _generate_cognitive_insights(self, domain: str, performance_data: Dict[str, Any]) -> List[str]:
        """Generate insights about cognitive processes"""
        insights = []
        
        # Learning pattern insights
        if "learning_rate" in performance_data:
            rate = performance_data["learning_rate"]
            if rate > 0.8:
                insights.append("Demonstrating rapid learning ability in this domain")
            elif rate < 0.3:
                insights.append("Learning rate is below optimal - consider strategy adjustment")
        
        # Memory performance insights
        if "memory_accuracy" in performance_data:
            accuracy = performance_data["memory_accuracy"]
            if accuracy > 0.9:
                insights.append("Excellent memory performance - leverage for complex tasks")
            elif accuracy < 0.6:
                insights.append("Memory performance needs improvement - consider rehearsal strategies")
        
        # Attention insights
        if "attention_stability" in performance_data:
            stability = performance_data["attention_stability"]
            if stability < 0.5:
                insights.append("Attention frequently shifting - may benefit from focus training")
        
        # Domain-specific insights
        domain_history = [r for r in self.reflection_history if r["domain"] == domain]
        if len(domain_history) > 3:
            insights.append(f"Extensive experience in {domain} - expertise level increasing")
        
        return insights
    
    def _evaluate_current_strategies(self, domain: str) -> Dict[str, Any]:
        """Evaluate effectiveness of current cognitive strategies"""
        evaluation = {
            "domain": domain,
            "active_strategies": [],
            "strategy_effectiveness": {},
            "recommended_adjustments": []
        }
        
        # Evaluate strategies used in this domain
        domain_selections = [s for s in self.strategy_selection_history 
                           if s.get("context", {}).get("domain") == domain]
        
        for selection in domain_selections[-5:]:  # Recent selections
            strategy = selection["selected_strategy"]
            if strategy not in evaluation["strategy_effectiveness"]:
                evaluation["strategy_effectiveness"][strategy] = []
            
            # Get effectiveness from historical data
            if strategy in self.strategy_effectiveness:
                recent_effectiveness = self.strategy_effectiveness[strategy][-3:]
                if recent_effectiveness:
                    avg_effectiveness = np.mean(recent_effectiveness)
                    evaluation["strategy_effectiveness"][strategy].append(avg_effectiveness)
        
        # Generate recommendations
        for strategy, effectiveness_list in evaluation["strategy_effectiveness"].items():
            if effectiveness_list:
                avg_effectiveness = np.mean(effectiveness_list)
                if avg_effectiveness < 0.6:
                    evaluation["recommended_adjustments"].append(
                        f"Consider replacing {strategy} with more effective alternative"
                    )
                elif avg_effectiveness > 0.8:
                    evaluation["recommended_adjustments"].append(
                        f"Continue using {strategy} - showing high effectiveness"
                    )
        
        return evaluation
    
    def _identify_improvement_opportunities(self, performance_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify specific opportunities for cognitive improvement"""
        opportunities = []
        
        # Analyze each performance metric
        for metric, value in performance_data.items():
            if isinstance(value, (int, float)):
                # Compare with historical performance
                if metric in self.performance_tracking:
                    historical_values = self.performance_tracking[metric]
                    if historical_values:
                        historical_avg = np.mean(historical_values)
                        
                        if value < historical_avg * 0.8:  # Significant decline
                            opportunities.append({
                                "type": "performance_recovery",
                                "metric": metric,
                                "current_value": value,
                                "historical_average": historical_avg,
                                "improvement_potential": historical_avg - value,
                                "priority": "high"
                            })
                        elif value < 0.7:  # Below good performance threshold
                            opportunities.append({
                                "type": "skill_development",
                                "metric": metric,
                                "current_value": value,
                                "target_value": 0.8,
                                "improvement_potential": 0.8 - value,
                                "priority": "medium"
                            })
        
        # Identify skill gaps
        skill_gaps = self._identify_skill_gaps()
        for gap in skill_gaps:
            opportunities.append({
                "type": "skill_gap",
                "area": gap["area"],
                "severity": gap["severity"],
                "priority": "high" if gap["severity"] > 0.7 else "medium"
            })
        
        # Sort by priority and potential impact
        opportunities.sort(key=lambda x: (
            {"high": 3, "medium": 2, "low": 1}[x["priority"]],
            x.get("improvement_potential", 0)
        ), reverse=True)
        
        return opportunities[:5]  # Top 5 opportunities
    
    def _initialize_default_strategies(self):
        """Initialize default cognitive strategies"""
        self.available_strategies.update({
            "sequential_processing": {
                "description": "Process information step by step",
                "effectiveness_domains": ["logical_reasoning", "problem_solving"],
                "confidence": 0.7
            },
            "parallel_processing": {
                "description": "Process multiple information streams simultaneously",
                "effectiveness_domains": ["pattern_recognition", "creativity"],
                "confidence": 0.6
            },
            "elaborative_encoding": {
                "description": "Create rich associations during learning",
                "effectiveness_domains": ["memory", "learning"],
                "confidence": 0.8
            },
            "metacognitive_monitoring": {
                "description": "Continuously monitor and adjust cognitive processes",
                "effectiveness_domains": ["self_regulation", "performance_optimization"],
                "confidence": 0.9
            },
            "analogical_reasoning": {
                "description": "Use analogies and metaphors for understanding",
                "effectiveness_domains": ["problem_solving", "creativity"],
                "confidence": 0.7
            }
        })
    
    def _get_overall_performance_trend(self) -> str:
        """Calculate overall performance trend across all metrics"""
        if not self.performance_tracking:
            return "stable"
        
        recent_trends = []
        for metric, values in self.performance_tracking.items():
            if len(values) >= 3:
                recent_avg = np.mean(values[-3:])
                earlier_avg = np.mean(values[-6:-3]) if len(values) >= 6 else np.mean(values[:-3])
                
                if recent_avg > earlier_avg * 1.1:
                    recent_trends.append("improving")
                elif recent_avg < earlier_avg * 0.9:
                    recent_trends.append("declining")
                else:
                    recent_trends.append("stable")
        
        if not recent_trends:
            return "stable"
        
        trend_counts = {
            "improving": recent_trends.count("improving"),
            "declining": recent_trends.count("declining"),
            "stable": recent_trends.count("stable")
        }
        
        return max(trend_counts.keys(), key=lambda k: trend_counts[k])
    
    def _monitor_attention_allocation(self, input_data: Dict[str, Any]) -> Dict[str, float]:
        """Monitor attention allocation efficiency"""
        return {
            "focus_stability": 0.7,  # Placeholder - would integrate with actual attention system
            "distraction_resistance": 0.6,
            "context_switching_efficiency": 0.8
        }
    
    def _monitor_memory_usage(self, input_data: Dict[str, Any]) -> Dict[str, float]:
        """Monitor working memory usage patterns"""
        return {
            "capacity_utilization": 0.6,  # Placeholder
            "retrieval_accuracy": 0.8,
            "interference_management": 0.7
        }
    
    def _monitor_executive_efficiency(self, input_data: Dict[str, Any]) -> Dict[str, float]:
        """Monitor executive control efficiency"""
        return {
            "goal_pursuit_consistency": 0.8,  # Placeholder
            "decision_making_speed": 0.7,
            "resource_allocation_efficiency": 0.6
        }
    
    def _monitor_emotional_processes(self, input_data: Dict[str, Any]) -> Dict[str, float]:
        """Monitor emotional processing and regulation"""
        return {
            "emotional_awareness": 0.7,  # Placeholder
            "regulation_effectiveness": 0.6,
            "emotional_intelligence": 0.8
        }
    
    def _assess_current_cognitive_load(self, monitoring_data: Dict[str, Any]) -> float:
        """Assess overall cognitive load from monitoring data"""
        load_factors = []
        
        for component_metrics in monitoring_data.values():
            if isinstance(component_metrics, dict):
                for metric_name, value in component_metrics.items():
                    if isinstance(value, (int, float)):
                        # Higher values in some metrics indicate higher load
                        if "utilization" in metric_name or "load" in metric_name:
                            load_factors.append(value)
                        elif "efficiency" in metric_name or "accuracy" in metric_name:
                            load_factors.append(1.0 - value)  # Lower efficiency = higher load
        
        return np.mean(load_factors) if load_factors else 0.5
    
    async def _integrate_reflection_insights(self, reflection: Dict[str, Any]):
        """Integrate insights from reflection into self-model"""
        insights = reflection.get("cognitive_insights", [])
        
        for insight in insights:
            if "strength" in insight.lower() or "excellent" in insight.lower():
                domain = reflection.get("domain", "general")
                if domain not in self.self_model["cognitive_strengths"]:
                    self.self_model["cognitive_strengths"].append(domain)
            elif "weakness" in insight.lower() or "needs improvement" in insight.lower():
                domain = reflection.get("domain", "general")
                if domain not in self.self_model["cognitive_weaknesses"]:
                    self.self_model["cognitive_weaknesses"].append(domain)
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from a series of values"""
        if len(values) < 2:
            return "stable"
        
        recent_avg = np.mean(values[-len(values)//2:])
        earlier_avg = np.mean(values[:len(values)//2])
        
        if recent_avg > earlier_avg * 1.1:
            return "improving"
        elif recent_avg < earlier_avg * 0.9:
            return "declining"
        else:
            return "stable"
    
    def _is_performance_anomaly(self, metric: str, value: float) -> bool:
        """Detect if a performance value is anomalous"""
        if metric not in self.performance_tracking:
            return False
        
        historical_values = self.performance_tracking[metric]
        if len(historical_values) < 5:
            return False
        
        mean_val = np.mean(historical_values)
        std_val = np.std(historical_values)
        
        # Consider values more than 2 standard deviations away as anomalies
        return abs(value - mean_val) > 2 * std_val
    
    def _get_expected_range(self, metric: str) -> Tuple[float, float]:
        """Get expected range for a performance metric"""
        if metric not in self.performance_tracking:
            return (0.0, 1.0)
        
        historical_values = self.performance_tracking[metric]
        if not historical_values:
            return (0.0, 1.0)
        
        mean_val = np.mean(historical_values)
        std_val = np.std(historical_values)
        
        return (mean_val - 2*std_val, mean_val + 2*std_val)
    
    def _identify_skill_gaps(self) -> List[Dict[str, Any]]:
        """Identify areas where skills need development"""
        gaps = []
        
        # Analyze performance across different domains
        domain_performance = {}
        for metric, values in self.performance_tracking.items():
            if values:
                domain = metric.split('_')[0] if '_' in metric else 'general'
                if domain not in domain_performance:
                    domain_performance[domain] = []
                domain_performance[domain].extend(values)
        
        # Identify domains with consistently low performance
        for domain, performances in domain_performance.items():
            if performances:
                avg_performance = np.mean(performances)
                if avg_performance < 0.5:  # Below average threshold
                    gaps.append({
                        "area": domain,
                        "severity": 1.0 - avg_performance,
                        "recent_performance": avg_performance
                    })
        
        return gaps
    
    def _assess_learning_efficiency(self, performance_data: Dict[str, Any]) -> float:
        """Assess learning efficiency based on performance data"""
        learning_indicators = ["learning_rate", "adaptation_speed", "knowledge_retention"]
        scores = []
        
        for indicator in learning_indicators:
            if indicator in performance_data:
                scores.append(performance_data[indicator])
        
        return np.mean(scores) if scores else 0.5
    
    def _assess_problem_solving(self, performance_data: Dict[str, Any]) -> float:
        """Assess problem-solving capability"""
        problem_solving_indicators = ["solution_quality", "problem_decomposition", "creative_solutions"]
        scores = []
        
        for indicator in problem_solving_indicators:
            if indicator in performance_data:
                scores.append(performance_data[indicator])
        
        return np.mean(scores) if scores else 0.5
    
    def _assess_memory_performance(self, performance_data: Dict[str, Any]) -> float:
        """Assess memory system performance"""
        memory_indicators = ["memory_accuracy", "retrieval_speed", "capacity_utilization"]
        scores = []
        
        for indicator in memory_indicators:
            if indicator in performance_data:
                scores.append(performance_data[indicator])
        
        return np.mean(scores) if scores else 0.5
    
    def _assess_attention_control(self, performance_data: Dict[str, Any]) -> float:
        """Assess attention control capabilities"""
        attention_indicators = ["attention_stability", "focus_intensity", "distraction_resistance"]
        scores = []
        
        for indicator in attention_indicators:
            if indicator in performance_data:
                scores.append(performance_data[indicator])
        
        return np.mean(scores) if scores else 0.5
    
    def _assess_executive_function(self, performance_data: Dict[str, Any]) -> float:
        """Assess executive function performance"""
        executive_indicators = ["goal_achievement", "planning_effectiveness", "decision_quality"]
        scores = []
        
        for indicator in executive_indicators:
            if indicator in performance_data:
                scores.append(performance_data[indicator])
        
        return np.mean(scores) if scores else 0.5
    
    def _assess_emotional_regulation(self, performance_data: Dict[str, Any]) -> float:
        """Assess emotional regulation capabilities"""
        emotion_indicators = ["emotional_stability", "regulation_effectiveness", "emotional_awareness"]
        scores = []
        
        for indicator in emotion_indicators:
            if indicator in performance_data:
                scores.append(performance_data[indicator])
        
        return np.mean(scores) if scores else 0.5
    
    def _assess_metacognitive_accuracy(self, performance_data: Dict[str, Any]) -> float:
        """Assess accuracy of metacognitive judgments"""
        metacog_indicators = ["confidence_calibration", "strategy_selection_accuracy", "self_assessment_accuracy"]
        scores = []
        
        for indicator in metacog_indicators:
            if indicator in performance_data:
                scores.append(performance_data[indicator])
        
        return np.mean(scores) if scores else 0.5
    
    def get_status(self) -> Dict[str, Any]:
        metacognitive_metrics = {
            "awareness_level": self.metacognitive_awareness,
            "reflection_frequency": len(self.reflection_history),
            "strategy_repertoire": len(self.available_strategies),
            "confidence_domains": len(self.self_model["confidence_levels"]),
            "performance_trends": self._get_overall_performance_trend(),
            "cognitive_load_awareness": self.cognitive_load_awareness,
            "self_improvement_goals": len(self.self_improvement_goals)
        }
        
        return {
            "name": self.name,
            "metacognitive_metrics": metacognitive_metrics,
            "self_model_completeness": len(self.self_model),
            "cognitive_plasticity": self.cognitive_plasticity,
            "recent_insights": len([r for r in self.reflection_history 
                                  if (datetime.now() - r["timestamp"]).days < 1]),
            "strategy_effectiveness_avg": np.mean([np.mean(scores) for scores in self.strategy_effectiveness.values()]) 
                                         if self.strategy_effectiveness else 0.5,
            "last_update": self.last_update.isoformat()
        }


class EmotionalProcessing(CognitiveComponent):
    """Emotional intelligence and affect generation"""
    
    def __init__(self):
        super().__init__("EmotionalProcessing")
        self.current_emotions: List[Emotion] = []
        self.emotional_memory: List[Tuple[str, Emotion]] = []
        self.emotional_patterns: Dict[str, List[EmotionType]] = {}
        self.mood_baseline: Dict[EmotionType, float] = {
            emotion: 0.5 for emotion in EmotionType
        }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process emotional responses and states"""
        action = input_data.get("action")
        
        if action == "generate_emotion":
            stimulus = input_data.get("stimulus")
            context = input_data.get("context")
            emotion = self._generate_emotional_response(stimulus, context)
            
            if emotion:
                self.current_emotions.append(emotion)
                self.emotional_memory.append((stimulus, emotion))
                self._update_emotional_patterns(stimulus, emotion)
            
            return {"emotion": emotion}
        
        elif action == "assess_mood":
            mood = self._assess_current_mood()
            return {"mood": mood}
        
        elif action == "emotional_decay":
            self._decay_emotions()
        
        return {
            "current_emotions": len(self.current_emotions),
            "emotional_memory_size": len(self.emotional_memory),
            "tracked_patterns": len(self.emotional_patterns)
        }
    
    def _generate_emotional_response(self, stimulus: str, context: str) -> Optional[Emotion]:
        """Generate appropriate emotional response to stimulus"""
        # Simple emotion generation - would be much more sophisticated
        emotion_mapping = {
            "learning": EmotionType.CURIOSITY,
            "success": EmotionType.SATISFACTION,
            "failure": EmotionType.FRUSTRATION,
            "discovery": EmotionType.EXCITEMENT,
            "uncertainty": EmotionType.CONFUSION,
            "achievement": EmotionType.CONFIDENCE,
            "mistake": EmotionType.DOUBT,
            "unexpected": EmotionType.SURPRISE
        }
        
        for key, emotion_type in emotion_mapping.items():
            if key in stimulus.lower() or key in context.lower():
                intensity = np.random.uniform(0.3, 0.8)  # Random for now
                return Emotion(emotion_type, intensity, context)
        
        return None
    
    def _assess_current_mood(self) -> Dict[str, float]:
        """Assess current overall mood"""
        mood = {}
        recent_emotions = [e for e in self.current_emotions 
                          if (datetime.now() - e.timestamp).seconds < 3600]
        
        for emotion_type in EmotionType:
            relevant_emotions = [e for e in recent_emotions if e.emotion_type == emotion_type]
            if relevant_emotions:
                avg_intensity = np.mean([e.intensity for e in relevant_emotions])
                mood[emotion_type.value] = avg_intensity
            else:
                mood[emotion_type.value] = self.mood_baseline[emotion_type]
        
        return mood
    
    def _update_emotional_patterns(self, stimulus: str, emotion: Emotion):
        """Update emotional patterns based on new responses"""
        if stimulus not in self.emotional_patterns:
            self.emotional_patterns[stimulus] = []
        self.emotional_patterns[stimulus].append(emotion.emotion_type)
    
    def _decay_emotions(self):
        """Natural decay of emotional intensity over time"""
        current_time = datetime.now()
        decayed_emotions = []
        
        for emotion in self.current_emotions:
            age_hours = (current_time - emotion.timestamp).seconds / 3600
            decay_factor = max(0.1, 1.0 - (age_hours * 0.1))  # 10% decay per hour
            
            if decay_factor > 0.1:
                emotion.intensity *= decay_factor
                decayed_emotions.append(emotion)
        
        self.current_emotions = decayed_emotions
    
    def get_status(self) -> Dict[str, Any]:
        # Synchronous mood assessment for status
        mood = {}
        recent_emotions = [e for e in self.current_emotions 
                          if (datetime.now() - e.timestamp).seconds < 3600]
        
        for emotion_type in EmotionType:
            relevant_emotions = [e for e in recent_emotions if e.emotion_type == emotion_type]
            if relevant_emotions:
                avg_intensity = np.mean([e.intensity for e in relevant_emotions])
                mood[emotion_type.value] = avg_intensity
            else:
                mood[emotion_type.value] = self.mood_baseline[emotion_type]
        
        return {
            "name": self.name,
            "active_emotions": len(self.current_emotions),
            "emotional_memory": len(self.emotional_memory),
            "current_mood": mood,
            "pattern_recognition": len(self.emotional_patterns),
            "last_update": self.last_update.isoformat()
        }


class InterestTracker:
    """Tracks and manages evolving interests and preferences"""
    
    def __init__(self):
        self.interests: Dict[str, Interest] = {}
        self.interest_history: List[Tuple[str, float, datetime]] = []
        self.decay_rate = 0.01  # Daily decay rate
        self.reinforcement_threshold = 0.1
    
    def register_interest(self, topic: str, initial_strength: float = 0.5):
        """Register a new interest"""
        if topic not in self.interests:
            self.interests[topic] = Interest(topic, initial_strength)
            logger.info(f"New interest registered: {topic}")
    
    def reinforce_interest(self, topic: str, amount: float = 0.1):
        """Reinforce an existing interest"""
        if topic in self.interests:
            self.interests[topic].reinforce(amount)
            self.interest_history.append((topic, amount, datetime.now()))
        else:
            self.register_interest(topic, amount)
    
    def decay_interests(self):
        """Apply natural decay to all interests"""
        for interest in self.interests.values():
            interest.decay(self.decay_rate)
    
    def get_top_interests(self, n: int = 5) -> List[Interest]:
        """Get top N interests by strength"""
        return sorted(self.interests.values(), 
                     key=lambda i: i.strength, reverse=True)[:n]
    
    def associate_concepts(self, topic1: str, topic2: str):
        """Create association between related concepts"""
        if topic1 in self.interests and topic2 in self.interests:
            self.interests[topic1].related_concepts.add(topic2)
            self.interests[topic2].related_concepts.add(topic1)


class CognitiveArchitecture:
    """Main cognitive architecture orchestrating all components with memory network integration"""
    
    def __init__(self):
        self.components: Dict[str, CognitiveComponent] = {
            "attention": AttentionSystem(),
            "working_memory": WorkingMemory(),
            "executive": ExecutiveControl(),
            "metacognition": MetaCognition(),
            "emotional": EmotionalProcessing()
        }
        
        self.interest_tracker = InterestTracker()
        self.processing_queue: asyncio.Queue = asyncio.Queue()
        self.system_status = "initializing"
        self.cycle_count = 0
        self.last_maintenance = datetime.now()
        
        # Memory network integration
        self.memory_network: Optional[EnhancedMemoryNetwork] = None
        self.memory_integration_enabled = MEMORY_NETWORK_AVAILABLE
        
        # Cross-component communication channels
        self.component_channels: Dict[str, asyncio.Queue] = {}
        self.shared_context: Dict[str, Any] = {}
        self.global_state: Dict[str, Any] = {
            "current_focus": None,
            "cognitive_load": 0.0,
            "emotional_state": "neutral",
            "active_goals": [],
            "learning_mode": "adaptive"
        }
        
        # Performance monitoring
        self.performance_metrics: Dict[str, List[float]] = defaultdict(list)
        self.component_interactions: List[Dict[str, Any]] = []
        
    async def initialize(self):
        """Initialize the cognitive architecture with memory network integration"""
        logger.info("Initializing Cognitive Architecture...")
        
        # Initialize memory network if available
        if self.memory_integration_enabled:
            try:
                self.memory_network = EnhancedMemoryNetwork()
                await self._initialize_memory_network()
                logger.info("Memory network integration initialized")
            except Exception as e:
                logger.error(f"Failed to initialize memory network: {e}")
                self.memory_integration_enabled = False
        
        # Create communication channels between components
        for component_name in self.components.keys():
            self.component_channels[component_name] = asyncio.Queue(maxsize=100)
        
        # Initialize all components
        for name, component in self.components.items():
            try:
                # Pass references to shared resources
                init_data = {
                    "action": "initialize",
                    "memory_network": self.memory_network,
                    "shared_context": self.shared_context,
                    "global_state": self.global_state,
                    "component_channel": self.component_channels[name]
                }
                await component.process(init_data)
                logger.info(f"Component {name} initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize component {name}: {e}")
        
        self.system_status = "active"
        logger.info("Cognitive Architecture initialization complete")
    
    async def _initialize_memory_network(self):
        """Initialize and configure the memory network"""
        if not self.memory_network:
            return
        
        # Create memory categories for cognitive components
        cognitive_categories = [
            "attention_focus_history",
            "working_memory_traces", 
            "executive_decisions",
            "metacognitive_reflections",
            "emotional_experiences",
            "learning_outcomes",
            "goal_progressions",
            "strategy_effectiveness"
        ]
        
        # Initialize memory categories (if needed by the memory network)
        for category in cognitive_categories:
            # Store initial configuration memories
            await self._store_memory(
                content=f"Initialized {category} tracking",
                memory_type=MemoryType.PROCEDURAL,
                importance=ImportanceLevel.MEDIUM,
                emotional_tags=[EmotionalTag(EmotionalValence.NEUTRAL, 0.1, "system_initialization")]
            )
    
    async def process_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced input processing with memory integration and component coordination"""
        self.cycle_count += 1
        processing_start = datetime.now()
        
        # Store input in memory network
        if self.memory_integration_enabled:
            await self._store_input_memory(input_data)
        
        # Update shared context with input information
        self.shared_context.update({
            "current_input": input_data,
            "processing_cycle": self.cycle_count,
            "processing_timestamp": processing_start
        })
        
        # Phase 1: Attention Processing
        attention_result = await self._process_attention(input_data)
        self.global_state["current_focus"] = attention_result.get("current_focus")
        
        # Phase 2: Working Memory Processing
        memory_result = await self._process_working_memory(input_data, attention_result)
        
        # Phase 3: Emotional Processing
        emotional_result = await self._process_emotions(input_data, attention_result)
        self.global_state["emotional_state"] = emotional_result.get("dominant_emotion", "neutral")
        
        # Phase 4: Executive Control Processing
        executive_result = await self._process_executive_control(input_data, {
            "attention": attention_result,
            "memory": memory_result,
            "emotion": emotional_result
        })
        
        # Phase 5: Meta-cognitive Processing
        metacog_result = await self._process_metacognition(input_data, {
            "attention": attention_result,
            "memory": memory_result,
            "emotion": emotional_result,
            "executive": executive_result
        })
        
        # Phase 6: Interest and Learning Updates
        learning_result = await self._update_interests_and_learning(input_data, {
            "attention": attention_result,
            "emotion": emotional_result,
            "executive": executive_result,
            "metacognition": metacog_result
        })
        
        # Phase 7: Memory Consolidation
        if self.memory_integration_enabled:
            await self._consolidate_processing_memories({
                "input": input_data,
                "attention": attention_result,
                "memory": memory_result,
                "emotion": emotional_result,
                "executive": executive_result,
                "metacognition": metacog_result,
                "learning": learning_result
            })
        
        # Update performance metrics
        processing_time = (datetime.now() - processing_start).total_seconds()
        self.performance_metrics["processing_time"].append(processing_time)
        self.performance_metrics["cycle_count"].append(self.cycle_count)
        
        # Record component interaction
        interaction_record = {
            "cycle": self.cycle_count,
            "input_complexity": len(str(input_data)),
            "processing_time": processing_time,
            "components_involved": ["attention", "working_memory", "emotional", "executive", "metacognition"],
            "timestamp": processing_start
        }
        self.component_interactions.append(interaction_record)
        
        return {
            "cycle": self.cycle_count,
            "processing_time": processing_time,
            "attention": attention_result,
            "memory": memory_result,
            "emotion": emotional_result,
            "executive": executive_result,
            "metacognition": metacog_result,
            "learning": learning_result,
            "interests": [i.topic for i in self.interest_tracker.get_top_interests(3)],
            "global_state": self.global_state.copy(),
            "memory_integration": self.memory_integration_enabled
        }
    
    async def _process_attention(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process attention component with enhanced integration"""
        attention_input = {
            "stimulus": input_data.get("content", ""),
            "priority": float(input_data.get("priority", 0.5)),  # Ensure numeric type
            "context": {
                "topic": input_data.get("topic"),
                "emotional_intensity": 0.0,  # Will be updated by emotional processing
                "goal_relevance": self._assess_goal_relevance(input_data)
            }
        }
        
        result = await self.components["attention"].process(attention_input)
        
        # Store attention focus in memory if enabled
        if self.memory_integration_enabled and result.get("current_focus"):
            await self._store_memory(
                content=f"Focused attention on: {result['current_focus']}",
                memory_type=MemoryType.EPISODIC,
                importance=ImportanceLevel.MEDIUM,
                context={"component": "attention", "cycle": self.cycle_count}
            )
        
        return result
    
    async def _process_working_memory(self, input_data: Dict[str, Any], attention_result: Dict[str, Any]) -> Dict[str, Any]:
        """Process working memory with attention-guided updates"""
        memory_input = {
            "action": "add",
            "item": input_data.get("content", ""),
            "item_type": self._classify_content_type(input_data.get("content", "")),
            "priority": attention_result.get("focus_intensity", 0.5),
            "context": {
                "attention_focus": attention_result.get("current_focus"),
                "processing_cycle": self.cycle_count
            }
        }
        
        result = await self.components["working_memory"].process(memory_input)
        
        # Update cognitive load in global state
        utilization = result.get("utilization", 0.0)
        self.global_state["cognitive_load"] = utilization
        
        return result
    
    async def _process_emotions(self, input_data: Dict[str, Any], attention_result: Dict[str, Any]) -> Dict[str, Any]:
        """Process emotional responses with attention context"""
        emotional_input = {
            "action": "generate_emotion",
            "stimulus": input_data.get("content", ""),
            "context": f"{input_data.get('context', '')} | focus: {attention_result.get('current_focus', 'none')}"
        }
        
        emotion_result = await self.components["emotional"].process(emotional_input)
        
        # Assess current mood for global state
        mood_result = await self.components["emotional"].process({"action": "assess_mood"})
        
        # Find dominant emotion
        dominant_emotion = "neutral"
        if mood_result.get("mood"):
            dominant_emotion = max(mood_result["mood"].items(), key=lambda x: x[1])[0]
        
        return {
            "emotion_generated": emotion_result.get("emotion"),
            "current_mood": mood_result.get("mood", {}),
            "dominant_emotion": dominant_emotion
        }
    
    async def _process_executive_control(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Process executive control with full cognitive context"""
        # Determine appropriate executive action based on input
        if input_data.get("requires_decision"):
            executive_input = {
                "action": "make_decision",
                "context": input_data.get("content", ""),
                "options": input_data.get("options", []),
                "criteria": ["utility", "feasibility", "goal_alignment"]
            }
        elif input_data.get("topic"):
            # Create a goal for exploring this topic
            executive_input = {
                "action": "add_goal",
                "goal": {
                    "description": f"Explore {input_data.get('topic')}",
                    "priority": input_data.get("priority", 0.5),
                    "auto_plan": True
                }
            }
        else:
            # Monitor current progress
            executive_input = {
                "action": "monitor",
                "performance_data": {
                    "attention_stability": context.get("attention", {}).get("focus_intensity", 0.5),
                    "memory_utilization": context.get("memory", {}).get("utilization", 0.0),
                    "emotional_intensity": self._calculate_emotional_intensity(context.get("emotion", {}))
                }
            }
        
        result = await self.components["executive"].process(executive_input)
        
        # Store significant executive decisions in memory
        if self.memory_integration_enabled and result.get("decision"):
            await self._store_memory(
                content=f"Executive decision: {result['decision']}",
                memory_type=MemoryType.EPISODIC,
                importance=ImportanceLevel.HIGH,
                context={"component": "executive", "confidence": result.get("confidence", 0.5)}
            )
        
        return result
    
    async def _process_metacognition(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Process metacognitive reflection and monitoring"""
        # Assess current cognitive performance
        performance_data = {
            "attention_effectiveness": context.get("attention", {}).get("focus_intensity", 0.5),
            "memory_efficiency": 1.0 - context.get("memory", {}).get("utilization", 0.0),
            "emotional_regulation": 1.0 - self._calculate_emotional_intensity(context.get("emotion", {})),
            "executive_decisiveness": context.get("executive", {}).get("confidence", 0.5)
        }
        
        metacog_input = {
            "action": "assess_performance",
            "assessment_type": "comprehensive",
            "performance_data": performance_data
        }
        
        result = await self.components["metacognition"].process(metacog_input)
        
        # Store metacognitive insights in memory
        if self.memory_integration_enabled and result.get("cognitive_insights"):
            for insight in result.get("cognitive_insights", []):
                await self._store_memory(
                    content=f"Metacognitive insight: {insight}",
                    memory_type=MemoryType.SEMANTIC,
                    importance=ImportanceLevel.HIGH,
                    context={"component": "metacognition", "cycle": self.cycle_count}
                )
        
        return result
    
    async def _update_interests_and_learning(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Update interest tracking and learning outcomes"""
        topic = input_data.get("topic")
        interest_strength = input_data.get("interest_strength", 0.1)
        
        learning_outcomes = {}
        
        if topic:
            # Register or reinforce interest
            if topic in self.interest_tracker.interests:
                self.interest_tracker.reinforce_interest(topic, interest_strength)
                learning_outcomes["interest_reinforced"] = topic
            else:
                self.interest_tracker.register_interest(topic, interest_strength)
                learning_outcomes["new_interest"] = topic
            
            # Associate with emotional context
            dominant_emotion = context.get("emotion", {}).get("dominant_emotion")
            if dominant_emotion and topic in self.interest_tracker.interests:
                emotion_obj = Emotion(
                    EmotionType(dominant_emotion) if dominant_emotion in [e.value for e in EmotionType] else EmotionType.CURIOSITY,
                    self._calculate_emotional_intensity(context.get("emotion", {})),
                    f"Learning about {topic}"
                )
                self.interest_tracker.interests[topic].emotional_associations.append(emotion_obj)
        
        # Update learning mode based on performance
        metacog_result = context.get("metacognition", {})
        if metacog_result.get("performance_trends"):
            # Simplified learning mode adaptation
            overall_performance = sum(performance_data.values()) / len(performance_data) if hasattr(locals(), 'performance_data') else 0.5
            if overall_performance > 0.7:
                self.global_state["learning_mode"] = "accelerated"
            elif overall_performance < 0.3:
                self.global_state["learning_mode"] = "remedial"
            else:
                self.global_state["learning_mode"] = "adaptive"
        
        learning_outcomes.update({
            "top_interests": [i.topic for i in self.interest_tracker.get_top_interests(3)],
            "learning_mode": self.global_state["learning_mode"],
            "interest_count": len(self.interest_tracker.interests)
        })
        
        return learning_outcomes
    
    async def _store_memory(self, content: str, memory_type: MemoryType, importance: ImportanceLevel, 
                           context: Dict[str, Any] = None, emotional_tags: List[EmotionalTag] = None):
        """Store information in the memory network"""
        if not self.memory_integration_enabled or not self.memory_network:
            return
        
        try:
            memory = EnhancedMemory(
                content=content,
                memory_type=memory_type,
                importance=importance,
                emotional_tags=emotional_tags or [],
                context=context or {}
            )
            
            memory_id = await asyncio.to_thread(self.memory_network.store_memory, memory)
            return memory_id
        except Exception as e:
            logger.error(f"Failed to store memory: {e}")
            return None
    
    async def _store_input_memory(self, input_data: Dict[str, Any]):
        """Store input data as episodic memory"""
        content = f"Input received: {input_data.get('content', 'Unknown content')}"
        context = {
            "input_type": input_data.get("context", "general"),
            "priority": input_data.get("priority", 0.5),
            "processing_cycle": self.cycle_count
        }
        
        await self._store_memory(
            content=content,
            memory_type=MemoryType.EPISODIC,
            importance=ImportanceLevel.MEDIUM,
            context=context
        )
    
    async def _consolidate_processing_memories(self, processing_data: Dict[str, Any]):
        """Consolidate memories from a complete processing cycle"""
        if not self.memory_integration_enabled:
            return
        
        # Create a summary memory of the processing cycle
        summary_content = f"Processing cycle {self.cycle_count}: "
        summary_content += f"Focus: {processing_data.get('attention', {}).get('current_focus', 'none')}, "
        summary_content += f"Emotion: {processing_data.get('emotion', {}).get('dominant_emotion', 'neutral')}, "
        summary_content += f"Decision: {processing_data.get('executive', {}).get('decision', 'none')}"
        
        await self._store_memory(
            content=summary_content,
            memory_type=MemoryType.EPISODIC,
            importance=ImportanceLevel.MEDIUM,
            context={
                "cycle": self.cycle_count,
                "processing_summary": True,
                "components_involved": list(processing_data.keys())
            }
        )
    
    def _assess_goal_relevance(self, input_data: Dict[str, Any]) -> float:
        """Assess how relevant input is to current goals"""
        if not hasattr(self.components["executive"], "current_goals"):
            return 0.5
        
        content_words = set(input_data.get("content", "").lower().split())
        topic = input_data.get("topic", "")
        
        relevance_scores = []
        
        # Access current goals from executive component
        executive_component = self.components["executive"]
        if hasattr(executive_component, "current_goals"):
            for goal in executive_component.current_goals:
                goal_words = set(goal.description.lower().split())
                overlap = len(content_words & goal_words)
                total_words = len(content_words | goal_words)
                
                if total_words > 0:
                    word_relevance = overlap / total_words
                    topic_relevance = 1.0 if topic.lower() in goal.description.lower() else 0.0
                    combined_relevance = (word_relevance * 0.7 + topic_relevance * 0.3) * goal.priority
                    relevance_scores.append(combined_relevance)
        
        return max(relevance_scores) if relevance_scores else 0.5
    
    def _classify_content_type(self, content: str) -> str:
        """Classify content type for working memory routing"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["see", "look", "visual", "image", "color", "shape"]):
            return "visual"
        elif any(word in content_lower for word in ["hear", "sound", "audio", "music", "voice"]):
            return "auditory"
        elif any(word in content_lower for word in ["remember", "recall", "happened", "experience"]):
            return "episodic"
        elif any(word in content_lower for word in ["think", "analyze", "process", "understand"]):
            return "verbal"
        else:
            return "general"
    
    def _calculate_emotional_intensity(self, emotion_data: Dict[str, Any]) -> float:
        """Calculate overall emotional intensity from emotion data"""
        if not emotion_data or not emotion_data.get("current_mood"):
            return 0.0
        
        mood_values = emotion_data.get("current_mood", {})
        if isinstance(mood_values, dict):
            # Calculate weighted average of emotional intensities
            total_intensity = sum(mood_values.values())
            num_emotions = len(mood_values)
            return total_intensity / num_emotions if num_emotions > 0 else 0.0
        
        return 0.0
    
    async def maintenance_cycle(self):
        """Perform regular maintenance operations"""
        if (datetime.now() - self.last_maintenance).seconds > 3600:  # Hourly
            logger.info("Performing maintenance cycle...")
            
            # Decay emotions
            await self.components["emotional"].process({"action": "emotional_decay"})
            
            # Decay interests
            self.interest_tracker.decay_interests()
            
            # Update goals
            await self.components["executive"].process({"action": "update_goals"})
            
            # Clear old working memory items
            await self.components["working_memory"].process({"action": "clear"})
            
            self.last_maintenance = datetime.now()
            logger.info("Maintenance cycle complete")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        component_status = {}
        for name, component in self.components.items():
            component_status[name] = component.get_status()
        
        return {
            "system_status": self.system_status,
            "cycle_count": self.cycle_count,
            "last_maintenance": self.last_maintenance.isoformat(),
            "top_interests": [i.topic for i in self.interest_tracker.get_top_interests(5)],
            "components": component_status,
            "timestamp": datetime.now().isoformat()
        }
    
    async def run_cognitive_loop(self, duration_seconds: int = 3600):
        """Run the main cognitive processing loop"""
        logger.info(f"Starting cognitive loop for {duration_seconds} seconds")
        start_time = time.time()
        
        while time.time() - start_time < duration_seconds:
            try:
                # Process any queued inputs
                if not self.processing_queue.empty():
                    input_data = await self.processing_queue.get()
                    result = await self.process_input(input_data)
                    logger.debug(f"Processed input: {result}")
                
                # Regular maintenance
                await self.maintenance_cycle()
                
                # Brief pause to prevent overwhelming the system
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error in cognitive loop: {e}")
                await asyncio.sleep(5)  # Longer pause on error
        
        logger.info("Cognitive loop completed")
    
    async def add_input(self, input_data: Dict[str, Any]):
        """Add input to the processing queue"""
        await self.processing_queue.put(input_data)


# Example usage and testing
async def demo_cognitive_architecture():
    """Demonstrate the cognitive architecture"""
    print("=== Cognitive Architecture Demo ===\n")
    
    # Create and initialize the architecture
    arch = CognitiveArchitecture()
    await arch.initialize()
    
    # Simulate various inputs
    test_inputs = [
        {
            "content": "Learning about machine learning algorithms",
            "context": "education",
            "topic": "machine_learning",
            "priority": 0.8,
            "interest_strength": 0.2
        },
        {
            "content": "Solving a complex programming problem",
            "context": "problem_solving",
            "topic": "programming",
            "requires_decision": True,
            "options": ["debug", "rewrite", "research"],
            "priority": 0.9
        },
        {
            "content": "Reading about cognitive science",
            "context": "research",
            "topic": "cognitive_science",
            "priority": 0.7,
            "interest_strength": 0.15
        }
    ]
    
    # Process inputs
    for i, input_data in enumerate(test_inputs):
        print(f"Processing input {i+1}...")
        result = await arch.process_input(input_data)
        print(f"Result: {result}\n")
    
    # Show system status
    status = arch.get_system_status()
    print("System Status:")
    print(json.dumps(status, indent=2, default=str))
    
    return arch


if __name__ == "__main__":
    # Run the demo
    asyncio.run(demo_cognitive_architecture())
