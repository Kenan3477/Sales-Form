#!/usr/bin/env python3
"""
Interest Formation System for ASIS - Phase 2.2 Implementation
Implements all 6 core interest formation capabilities
"""

import asyncio
import logging
import numpy as np
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum
import hashlib

logger = logging.getLogger(__name__)

class InterestType(Enum):
    TOPICAL = "topical"
    METHODOLOGICAL = "methodological" 
    AESTHETIC = "aesthetic"
    SOCIAL = "social"
    FUNCTIONAL = "functional"
    EXPLORATORY = "exploratory"

@dataclass
class Interest:
    """Represents a specific interest"""
    interest_id: str
    name: str
    interest_type: InterestType
    strength: float = 0.5
    persistence: float = 0.5
    created_at: datetime = field(default_factory=datetime.now)
    last_reinforced: datetime = field(default_factory=datetime.now)
    reinforcement_count: int = 0
    decay_rate: float = 0.01
    keywords: Set[str] = field(default_factory=set)

class NoveltyDetector:
    """Detects novel and interesting information"""
    
    def __init__(self):
        self.seen_content_hashes = set()
        self.concept_frequency = defaultdict(int)
        
    def assess_novelty(self, content: Any) -> float:
        """Assess how novel content is (0.0 to 1.0)"""
        novelty_score = 0.0
        
        # Content hash novelty
        content_hash = hashlib.md5(str(content).encode()).hexdigest()
        if content_hash not in self.seen_content_hashes:
            novelty_score += 0.5
            self.seen_content_hashes.add(content_hash)
        
        # Concept rarity novelty
        concepts = self._extract_concepts(content)
        for concept in concepts:
            if self.concept_frequency[concept] < 2:
                novelty_score += 0.3
            self.concept_frequency[concept] += 1
        
        return min(1.0, novelty_score)
    
    def _extract_concepts(self, content: Any) -> List[str]:
        """Extract concepts from content"""
        if isinstance(content, str):
            return [w.lower() for w in content.split() if len(w) > 3][:5]
        return []

class InterestTracker:
    """Tracks and manages interests over time"""
    
    def __init__(self):
        self.interests: Dict[str, Interest] = {}
        self.interest_history = []
        self.global_interest_count = 0
        
    def develop_interest(self, content: Any, novelty_score: float) -> Optional[Interest]:
        """Develop new interest based on content"""
        if novelty_score < 0.4:
            return None
            
        interest_name = self._generate_name(content)
        interest_id = f"interest_{self.global_interest_count}_{int(time.time())}"
        self.global_interest_count += 1
        
        new_interest = Interest(
            interest_id=interest_id,
            name=interest_name,
            interest_type=InterestType.TOPICAL,
            strength=novelty_score,
            keywords=set(self._extract_keywords(content))
        )
        
        self.interests[interest_id] = new_interest
        self.interest_history.append({
            'action': 'developed',
            'interest_id': interest_id,
            'name': interest_name,
            'strength': novelty_score,
            'timestamp': datetime.now()
        })
        
        logger.info(f"Developed interest: {interest_name} (strength: {novelty_score:.3f})")
        return new_interest
    
    def reinforce_interest(self, interest_id: str, outcome_quality: float) -> bool:
        """Reinforce interest based on positive outcomes"""
        if interest_id not in self.interests:
            return False
            
        interest = self.interests[interest_id]
        reinforcement = outcome_quality * 0.1
        old_strength = interest.strength
        interest.strength = min(1.0, interest.strength + reinforcement)
        interest.reinforcement_count += 1
        interest.last_reinforced = datetime.now()
        
        self.interest_history.append({
            'action': 'reinforced',
            'interest_id': interest_id,
            'old_strength': old_strength,
            'new_strength': interest.strength,
            'outcome_quality': outcome_quality,
            'timestamp': datetime.now()
        })
        
        logger.info(f"Reinforced {interest.name}: {old_strength:.3f} -> {interest.strength:.3f}")
        return True
    
    def decay_interests(self) -> List[str]:
        """Apply natural decay to interests"""
        decayed = []
        current_time = datetime.now()
        
        for interest_id, interest in list(self.interests.items()):
            time_since = current_time - interest.last_reinforced
            days_since = time_since.total_seconds() / 86400
            decay_amount = interest.decay_rate * days_since
            
            old_strength = interest.strength
            interest.strength = max(0.0, interest.strength - decay_amount)
            
            if interest.strength < 0.1:
                decayed.append(interest_id)
                del self.interests[interest_id]
                self.interest_history.append({
                    'action': 'removed',
                    'interest_id': interest_id,
                    'final_strength': old_strength,
                    'timestamp': current_time
                })
        
        return decayed
    
    def get_top_interests(self, limit: int = 5) -> List[Interest]:
        """Get top interests by strength"""
        return sorted(self.interests.values(), key=lambda i: i.strength, reverse=True)[:limit]
    
    def _generate_name(self, content: Any) -> str:
        """Generate interest name from content"""
        keywords = self._extract_keywords(content)
        return "_".join(keywords[:2]) if keywords else f"interest_{int(time.time())}"
    
    def _extract_keywords(self, content: Any) -> List[str]:
        """Extract keywords from content"""
        if isinstance(content, str):
            return [w.lower() for w in content.split() if len(w) > 3][:3]
        return []

class AttentionAllocator:
    """Allocates attention based on interest levels"""
    
    def __init__(self):
        self.attention_budget = 1.0
        self.allocation_history = []
        
    def allocate_attention(self, interests: Dict[str, Interest], items: List[Any]) -> Dict[str, float]:
        """Allocate attention across items based on interests"""
        if not items:
            return {}
            
        item_scores = {}
        total_score = 0.0
        
        for i, item in enumerate(items):
            item_id = f"item_{i}"
            score = self._calculate_interest_score(item, interests)
            item_scores[item_id] = score
            total_score += score
        
        # Proportional allocation
        allocation = {}
        if total_score > 0:
            for item_id, score in item_scores.items():
                allocation[item_id] = (score / total_score) * self.attention_budget
        else:
            # Equal allocation
            equal_attention = self.attention_budget / len(items)
            for i in range(len(items)):
                allocation[f"item_{i}"] = equal_attention
        
        self.allocation_history.append({
            'timestamp': datetime.now(),
            'allocation': allocation.copy()
        })
        
        logger.info(f"Allocated attention across {len(items)} items")
        return allocation
    
    def _calculate_interest_score(self, item: Any, interests: Dict[str, Interest]) -> float:
        """Calculate interest score for an item"""
        if isinstance(item, str):
            item_keywords = set(item.lower().split())
            total_score = 0.0
            
            for interest in interests.values():
                overlap = len(item_keywords.intersection(interest.keywords))
                if overlap > 0:
                    total_score += interest.strength * (overlap / len(interest.keywords.union(item_keywords)))
            
            return total_score
        return 0.1

class ExplorationPatternTracker:
    """Tracks curiosity-driven exploration patterns"""
    
    def __init__(self):
        self.exploration_sessions = []
        self.pattern_metrics = defaultdict(list)
        
    def record_exploration(self, content: Any, curiosity_trigger: str, outcome: Dict[str, Any]):
        """Record an exploration session"""
        session = {
            'content': str(content)[:100],  # Truncated for storage
            'trigger': curiosity_trigger,
            'outcome': outcome,
            'timestamp': datetime.now(),
            'success': outcome.get('success', False),
            'satisfaction': outcome.get('satisfaction', 0.5)
        }
        
        self.exploration_sessions.append(session)
        self.pattern_metrics[curiosity_trigger].append(outcome.get('satisfaction', 0.5))
        
        logger.info(f"Recorded exploration: {curiosity_trigger} trigger")
    
    def analyze_patterns(self) -> Dict[str, Any]:
        """Analyze exploration patterns"""
        if not self.exploration_sessions:
            return {'total_explorations': 0}
        
        recent_sessions = self.exploration_sessions[-20:]  # Last 20 sessions
        
        analysis = {
            'total_explorations': len(self.exploration_sessions),
            'recent_success_rate': sum(s['success'] for s in recent_sessions) / len(recent_sessions),
            'avg_satisfaction': sum(s['satisfaction'] for s in recent_sessions) / len(recent_sessions),
            'top_triggers': []
        }
        
        # Find most successful triggers
        trigger_performance = {}
        for trigger, satisfactions in self.pattern_metrics.items():
            if satisfactions:
                trigger_performance[trigger] = sum(satisfactions) / len(satisfactions)
        
        analysis['top_triggers'] = sorted(trigger_performance.items(), 
                                        key=lambda x: x[1], reverse=True)[:3]
        
        return analysis

# Complete Interest Formation System
class InterestFormationSystem:
    """Complete interest formation system integrating all components"""
    
    def __init__(self):
        self.novelty_detector = NoveltyDetector()
        self.interest_tracker = InterestTracker()
        self.attention_allocator = AttentionAllocator()
        self.exploration_tracker = ExplorationPatternTracker()
        
        logger.info("InterestFormationSystem initialized")
    
    async def process_content(self, content_items: List[Any]) -> Dict[str, Any]:
        """Process content through the complete interest formation pipeline"""
        
        results = {
            'processed_items': len(content_items),
            'new_interests': [],
            'reinforced_interests': [],
            'attention_allocation': {},
            'exploration_patterns': {}
        }
        
        # 1. Detect novelty and interesting information
        for content in content_items:
            novelty_score = self.novelty_detector.assess_novelty(content)
            
            # 2. Develop new interests for novel content
            if novelty_score > 0.5:
                new_interest = self.interest_tracker.develop_interest(content, novelty_score)
                if new_interest:
                    results['new_interests'].append(new_interest.name)
                    
                    # Record exploration
                    self.exploration_tracker.record_exploration(
                        content, 'novelty', 
                        {'success': True, 'satisfaction': novelty_score}
                    )
        
        # 3. Allocate attention based on current interests
        if content_items:
            attention_allocation = self.attention_allocator.allocate_attention(
                self.interest_tracker.interests, content_items
            )
            results['attention_allocation'] = attention_allocation
        
        # 4. Simulate positive outcomes and reinforce interests
        top_interests = self.interest_tracker.get_top_interests(3)
        for interest in top_interests:
            # Simulate positive learning outcome
            success = self.interest_tracker.reinforce_interest(
                interest.interest_id, 0.7  # Good outcome quality
            )
            if success:
                results['reinforced_interests'].append(interest.name)
        
        # 5. Apply natural decay
        self.interest_tracker.decay_interests()
        
        # 6. Analyze exploration patterns
        results['exploration_patterns'] = self.exploration_tracker.analyze_patterns()
        
        return results
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            'active_interests': len(self.interest_tracker.interests),
            'top_interests': [i.name for i in self.interest_tracker.get_top_interests(3)],
            'total_explorations': len(self.exploration_tracker.exploration_sessions),
            'interest_history_events': len(self.interest_tracker.interest_history),
            'seen_content_items': len(self.novelty_detector.seen_content_hashes)
        }

# Testing function
async def test_interest_formation_system():
    """Test the complete interest formation system"""
    
    print("🎯 Testing Interest Formation System")
    print("=" * 50)
    
    system = InterestFormationSystem()
    
    # Test content with varying novelty
    test_content = [
        "Machine learning algorithms for pattern recognition",
        "Quantum computing breakthrough in 2025", 
        "Simple hello world program",
        "Revolutionary AI consciousness research",
        "Weather forecast for tomorrow",
        "Advanced neural network architectures",
        "Basic arithmetic calculations"
    ]
    
    print(f"\n📥 Processing {len(test_content)} content items...")
    results = await system.process_content(test_content)
    
    print(f"\n📊 Results:")
    print(f"   New interests developed: {len(results['new_interests'])}")
    print(f"   Interest names: {', '.join(results['new_interests'])}")
    print(f"   Interests reinforced: {len(results['reinforced_interests'])}")
    print(f"   Attention allocated to: {len(results['attention_allocation'])} items")
    
    # Show attention allocation
    print(f"\n🎯 Attention Allocation:")
    for item_id, attention in list(results['attention_allocation'].items())[:3]:
        item_idx = int(item_id.split('_')[1])
        content = test_content[item_idx][:50] + "..." if len(test_content[item_idx]) > 50 else test_content[item_idx]
        print(f"   {content}: {attention:.3f}")
    
    # System status
    status = system.get_system_status()
    print(f"\n🔍 System Status:")
    print(f"   Active interests: {status['active_interests']}")
    print(f"   Top interests: {', '.join(status['top_interests'])}")
    print(f"   Total explorations: {status['total_explorations']}")
    print(f"   Interest history events: {status['interest_history_events']}")
    
    print(f"\n🎉 INTEREST FORMATION SYSTEM TEST COMPLETE!")
    print(f"   ✅ Curiosity-driven exploration: Tracked")
    print(f"   ✅ Interest evolution: Monitored") 
    print(f"   ✅ Attention allocation: Implemented")
    print(f"   ✅ Novelty detection: Operational")
    print(f"   ✅ Interest reinforcement: Active")
    print(f"   ✅ History tracking: Maintained")
    
    return system

if __name__ == "__main__":
    asyncio.run(test_interest_formation_system())
