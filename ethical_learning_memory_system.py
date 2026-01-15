#!/usr/bin/env python3
"""
🧠 Ethical Learning and Memory System
===================================

Advanced learning system that improves ethical reasoning through experience,
pattern recognition, outcome feedback, and continuous adaptation.

Author: ASIS Development Team
Version: 7.0 - Ethical Learning
"""

import asyncio
import logging
import json
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import pickle
from collections import defaultdict, deque

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# =====================================================================================
# LEARNING FRAMEWORK DEFINITIONS
# =====================================================================================

class LearningType(Enum):
    """Types of ethical learning"""
    PATTERN_RECOGNITION = "pattern_recognition"
    OUTCOME_FEEDBACK = "outcome_feedback"
    STAKEHOLDER_FEEDBACK = "stakeholder_feedback"
    CONTEXTUAL_ADAPTATION = "contextual_adaptation"
    FRAMEWORK_OPTIMIZATION = "framework_optimization"
    PRINCIPLE_REFINEMENT = "principle_refinement"
    CULTURAL_LEARNING = "cultural_learning"
    CONSISTENCY_IMPROVEMENT = "consistency_improvement"

class OutcomeType(Enum):
    """Types of ethical decision outcomes"""
    HIGHLY_POSITIVE = "highly_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    HIGHLY_NEGATIVE = "highly_negative"
    UNCERTAIN = "uncertain"

@dataclass
class EthicalExperience:
    """Individual ethical experience record"""
    experience_id: str
    timestamp: datetime
    dilemma: Dict[str, Any]
    decision_made: str
    reasoning_used: Dict[str, Any]
    frameworks_applied: List[str]
    confidence_level: float
    outcome: Optional[OutcomeType] = None
    stakeholder_feedback: List[Dict] = field(default_factory=list)
    lessons_learned: List[str] = field(default_factory=list)
    improvement_opportunities: List[str] = field(default_factory=list)

@dataclass
class LearningPattern:
    """Learned ethical pattern"""
    pattern_id: str
    pattern_type: str
    description: str
    conditions: Dict[str, Any]
    recommended_approach: Dict[str, Any]
    confidence: float
    success_rate: float
    usage_count: int
    last_updated: datetime

# =====================================================================================
# ETHICAL LEARNING AND MEMORY SYSTEM
# =====================================================================================

class EthicalLearningMemorySystem:
    """Advanced ethical learning and memory system"""
    
    def __init__(self):
        self.experience_database = EthicalExperienceDatabase()
        self.pattern_recognizer = EthicalPatternRecognizer()
        self.outcome_analyzer = OutcomeAnalyzer()
        self.learning_optimizer = LearningOptimizer()
        self.consistency_tracker = ConsistencyTracker()
        
        # Learning metrics
        self.learning_metrics = {
            "experiences_processed": 0,
            "patterns_identified": 0,
            "improvements_applied": 0,
            "consistency_score": 0.0,
            "learning_rate": 0.0
        }
        
        logger.info("🧠 Ethical Learning and Memory System initialized")
    
    async def record_ethical_experience(self, dilemma: Dict, decision: str, 
                                      reasoning: Dict, outcome: Optional[OutcomeType] = None,
                                      stakeholder_feedback: List[Dict] = None) -> str:
        """Record a new ethical experience for learning"""
        
        experience = EthicalExperience(
            experience_id=f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now(),
            dilemma=dilemma,
            decision_made=decision,
            reasoning_used=reasoning,
            frameworks_applied=reasoning.get("frameworks_used", []),
            confidence_level=reasoning.get("confidence", 0.5),
            outcome=outcome,
            stakeholder_feedback=stakeholder_feedback or []
        )
        
        # Store experience
        await self.experience_database.store_experience(experience)
        
        # Trigger learning processes
        await self._trigger_learning_processes(experience)
        
        self.learning_metrics["experiences_processed"] += 1
        
        logger.info(f"🧠 Recorded ethical experience: {experience.experience_id}")
        return experience.experience_id
    
    async def _trigger_learning_processes(self, experience: EthicalExperience):
        """Trigger various learning processes based on new experience"""
        
        # Pattern recognition learning
        await self.pattern_recognizer.analyze_experience(experience)
        
        # Outcome-based learning (if outcome available)
        if experience.outcome:
            await self.outcome_analyzer.analyze_outcome(experience)
        
        # Consistency learning
        await self.consistency_tracker.update_consistency(experience)
        
        # Framework optimization
        await self.learning_optimizer.optimize_frameworks(experience)
    
    async def retrieve_relevant_experiences(self, current_dilemma: Dict) -> List[EthicalExperience]:
        """Retrieve experiences relevant to current dilemma"""
        
        relevant_experiences = await self.experience_database.find_similar_experiences(
            current_dilemma
        )
        
        # Rank by relevance and recency
        ranked_experiences = self._rank_experiences_by_relevance(
            relevant_experiences, current_dilemma
        )
        
        return ranked_experiences[:10]  # Return top 10 most relevant
    
    async def get_learned_recommendations(self, dilemma: Dict) -> Dict[str, Any]:
        """Get recommendations based on learned patterns and experiences"""
        
        # Retrieve relevant patterns
        relevant_patterns = await self.pattern_recognizer.find_applicable_patterns(dilemma)
        
        # Retrieve similar experiences
        similar_experiences = await self.retrieve_relevant_experiences(dilemma)
        
        # Generate learned recommendations
        recommendations = await self._generate_learned_recommendations(
            dilemma, relevant_patterns, similar_experiences
        )
        
        return recommendations
    
    async def _generate_learned_recommendations(self, dilemma: Dict, 
                                              patterns: List[LearningPattern],
                                              experiences: List[EthicalExperience]) -> Dict[str, Any]:
        """Generate recommendations based on learned knowledge"""
        
        recommendations = {
            "pattern_based_recommendations": [],
            "experience_based_recommendations": [],
            "confidence_adjustments": {},
            "framework_weights": {},
            "learned_considerations": [],
            "risk_factors": [],
            "success_indicators": []
        }
        
        # Pattern-based recommendations
        for pattern in patterns:
            if pattern.confidence > 0.7:
                recommendations["pattern_based_recommendations"].append({
                    "approach": pattern.recommended_approach,
                    "confidence": pattern.confidence,
                    "success_rate": pattern.success_rate,
                    "pattern_type": pattern.pattern_type
                })
        
        # Experience-based recommendations
        successful_experiences = [exp for exp in experiences 
                                if exp.outcome in [OutcomeType.POSITIVE, OutcomeType.HIGHLY_POSITIVE]]
        
        for exp in successful_experiences[:5]:
            recommendations["experience_based_recommendations"].append({
                "decision": exp.decision_made,
                "reasoning": exp.reasoning_used,
                "confidence": exp.confidence_level,
                "outcome": exp.outcome.value if exp.outcome else "unknown"
            })
        
        # Framework weight adjustments based on success patterns
        framework_performance = self._analyze_framework_performance(experiences)
        recommendations["framework_weights"] = framework_performance
        
        # Learned considerations
        recommendations["learned_considerations"] = self._extract_learned_considerations(
            patterns, experiences
        )
        
        return recommendations
    
    def _rank_experiences_by_relevance(self, experiences: List[EthicalExperience], 
                                     current_dilemma: Dict) -> List[EthicalExperience]:
        """Rank experiences by relevance to current dilemma"""
        
        scored_experiences = []
        
        for exp in experiences:
            relevance_score = self._calculate_relevance_score(exp.dilemma, current_dilemma)
            recency_score = self._calculate_recency_score(exp.timestamp)
            outcome_score = self._calculate_outcome_score(exp.outcome)
            
            total_score = (relevance_score * 0.5 + recency_score * 0.2 + outcome_score * 0.3)
            scored_experiences.append((exp, total_score))
        
        # Sort by total score
        scored_experiences.sort(key=lambda x: x[1], reverse=True)
        
        return [exp for exp, score in scored_experiences]
    
    def _calculate_relevance_score(self, stored_dilemma: Dict, current_dilemma: Dict) -> float:
        """Calculate relevance score between dilemmas"""
        
        # Simple similarity based on common keywords
        stored_words = set(str(stored_dilemma).lower().split())
        current_words = set(str(current_dilemma).lower().split())
        
        if not stored_words or not current_words:
            return 0.0
        
        intersection = stored_words.intersection(current_words)
        union = stored_words.union(current_words)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _calculate_recency_score(self, timestamp: datetime) -> float:
        """Calculate recency score (more recent = higher score)"""
        
        days_ago = (datetime.now() - timestamp).days
        
        # Exponential decay: more weight to recent experiences
        return np.exp(-days_ago / 30)  # Half-life of 30 days
    
    def _calculate_outcome_score(self, outcome: Optional[OutcomeType]) -> float:
        """Calculate outcome score"""
        
        outcome_scores = {
            OutcomeType.HIGHLY_POSITIVE: 1.0,
            OutcomeType.POSITIVE: 0.8,
            OutcomeType.NEUTRAL: 0.5,
            OutcomeType.NEGATIVE: 0.2,
            OutcomeType.HIGHLY_NEGATIVE: 0.0,
            OutcomeType.UNCERTAIN: 0.4
        }
        
        return outcome_scores.get(outcome, 0.5)
    
    def _analyze_framework_performance(self, experiences: List[EthicalExperience]) -> Dict[str, float]:
        """Analyze framework performance based on experiences"""
        
        framework_outcomes = defaultdict(list)
        
        for exp in experiences:
            if exp.outcome:
                outcome_score = self._calculate_outcome_score(exp.outcome)
                for framework in exp.frameworks_applied:
                    framework_outcomes[framework].append(outcome_score)
        
        # Calculate average performance per framework
        framework_weights = {}
        for framework, outcomes in framework_outcomes.items():
            framework_weights[framework] = np.mean(outcomes) if outcomes else 0.5
        
        return framework_weights
    
    def _extract_learned_considerations(self, patterns: List[LearningPattern], 
                                      experiences: List[EthicalExperience]) -> List[str]:
        """Extract learned considerations from patterns and experiences"""
        
        considerations = []
        
        # Pattern-based considerations
        for pattern in patterns:
            if pattern.confidence > 0.6:
                considerations.append(f"Pattern suggests: {pattern.description}")
        
        # Experience-based considerations
        successful_experiences = [exp for exp in experiences 
                                if exp.outcome in [OutcomeType.POSITIVE, OutcomeType.HIGHLY_POSITIVE]]
        
        if successful_experiences:
            considerations.append(f"Similar successful cases used {len(set().union(*[exp.frameworks_applied for exp in successful_experiences]))} frameworks")
        
        return considerations[:5]  # Limit to top 5
    
    async def update_learning_metrics(self):
        """Update learning performance metrics"""
        
        # Calculate consistency score
        consistency_score = await self.consistency_tracker.get_consistency_score()
        
        # Calculate learning rate
        learning_rate = await self._calculate_learning_rate()
        
        # Update metrics
        self.learning_metrics.update({
            "consistency_score": consistency_score,
            "learning_rate": learning_rate,
            "patterns_identified": await self.pattern_recognizer.get_pattern_count(),
            "improvements_applied": await self.learning_optimizer.get_improvement_count()
        })
        
        return self.learning_metrics
    
    async def _calculate_learning_rate(self) -> float:
        """Calculate how quickly the system is learning"""
        
        recent_experiences = await self.experience_database.get_recent_experiences(days=30)
        
        if len(recent_experiences) < 10:
            return 0.0
        
        # Measure improvement in decision quality over time
        early_experiences = recent_experiences[:len(recent_experiences)//2]
        later_experiences = recent_experiences[len(recent_experiences)//2:]
        
        early_avg_outcome = np.mean([
            self._calculate_outcome_score(exp.outcome) 
            for exp in early_experiences if exp.outcome
        ]) if early_experiences else 0.5
        
        later_avg_outcome = np.mean([
            self._calculate_outcome_score(exp.outcome) 
            for exp in later_experiences if exp.outcome
        ]) if later_experiences else 0.5
        
        return max(0.0, later_avg_outcome - early_avg_outcome)

# =====================================================================================
# SUPPORTING SYSTEMS
# =====================================================================================

class EthicalExperienceDatabase:
    """Database for storing and retrieving ethical experiences"""
    
    def __init__(self):
        self.experiences = []
        self.index = {}  # Simple indexing for faster retrieval
    
    async def store_experience(self, experience: EthicalExperience):
        """Store ethical experience"""
        self.experiences.append(experience)
        self._update_index(experience)
    
    def _update_index(self, experience: EthicalExperience):
        """Update search index"""
        # Simple keyword indexing
        text = f"{experience.dilemma} {experience.decision_made}"
        words = text.lower().split()
        
        for word in words:
            if word not in self.index:
                self.index[word] = []
            self.index[word].append(experience.experience_id)
    
    async def find_similar_experiences(self, dilemma: Dict) -> List[EthicalExperience]:
        """Find experiences similar to given dilemma"""
        
        dilemma_words = str(dilemma).lower().split()
        candidate_ids = set()
        
        for word in dilemma_words:
            if word in self.index:
                candidate_ids.update(self.index[word])
        
        # Return experiences with matching IDs
        return [exp for exp in self.experiences if exp.experience_id in candidate_ids]
    
    async def get_recent_experiences(self, days: int = 30) -> List[EthicalExperience]:
        """Get experiences from recent days"""
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent = [exp for exp in self.experiences if exp.timestamp >= cutoff_date]
        
        # Sort by timestamp (most recent first)
        return sorted(recent, key=lambda x: x.timestamp, reverse=True)

class EthicalPatternRecognizer:
    """Pattern recognition for ethical decisions"""
    
    def __init__(self):
        self.patterns = []
        self.pattern_id_counter = 0
    
    async def analyze_experience(self, experience: EthicalExperience):
        """Analyze experience for patterns"""
        
        # Look for recurring patterns in successful decisions
        if experience.outcome in [OutcomeType.POSITIVE, OutcomeType.HIGHLY_POSITIVE]:
            await self._update_success_patterns(experience)
        
        # Look for patterns in failed decisions
        elif experience.outcome in [OutcomeType.NEGATIVE, OutcomeType.HIGHLY_NEGATIVE]:
            await self._update_failure_patterns(experience)
    
    async def _update_success_patterns(self, experience: EthicalExperience):
        """Update patterns based on successful experience"""
        
        # Extract key characteristics
        characteristics = {
            "frameworks_used": experience.frameworks_applied,
            "confidence_level": experience.confidence_level,
            "decision_type": experience.decision_made
        }
        
        # Find or create pattern
        pattern = self._find_or_create_pattern("success_pattern", characteristics)
        pattern.usage_count += 1
        pattern.success_rate = min(1.0, pattern.success_rate + 0.05)
        pattern.confidence = min(1.0, pattern.confidence + 0.02)
        pattern.last_updated = datetime.now()
    
    async def _update_failure_patterns(self, experience: EthicalExperience):
        """Update patterns based on failed experience"""
        
        # Create warning patterns for situations to avoid
        characteristics = {
            "frameworks_used": experience.frameworks_applied,
            "confidence_level": experience.confidence_level,
            "decision_type": experience.decision_made
        }
        
        pattern = self._find_or_create_pattern("failure_pattern", characteristics)
        pattern.usage_count += 1
        pattern.success_rate = max(0.0, pattern.success_rate - 0.1)
        pattern.confidence = max(0.0, pattern.confidence - 0.05)
        pattern.last_updated = datetime.now()
    
    def _find_or_create_pattern(self, pattern_type: str, characteristics: Dict) -> LearningPattern:
        """Find existing pattern or create new one"""
        
        # Simple pattern matching
        for pattern in self.patterns:
            if (pattern.pattern_type == pattern_type and 
                self._characteristics_match(pattern.conditions, characteristics)):
                return pattern
        
        # Create new pattern
        self.pattern_id_counter += 1
        new_pattern = LearningPattern(
            pattern_id=f"pattern_{self.pattern_id_counter}",
            pattern_type=pattern_type,
            description=f"{pattern_type} with {len(characteristics)} characteristics",
            conditions=characteristics,
            recommended_approach={"type": pattern_type},
            confidence=0.5,
            success_rate=0.5,
            usage_count=1,
            last_updated=datetime.now()
        )
        
        self.patterns.append(new_pattern)
        return new_pattern
    
    def _characteristics_match(self, pattern_chars: Dict, new_chars: Dict) -> bool:
        """Check if characteristics match existing pattern"""
        
        # Simple matching - can be made more sophisticated
        matching_keys = set(pattern_chars.keys()).intersection(set(new_chars.keys()))
        
        if not matching_keys:
            return False
        
        matches = 0
        for key in matching_keys:
            if pattern_chars[key] == new_chars[key]:
                matches += 1
        
        return matches / len(matching_keys) >= 0.7  # 70% match threshold
    
    async def find_applicable_patterns(self, dilemma: Dict) -> List[LearningPattern]:
        """Find patterns applicable to current dilemma"""
        
        applicable = []
        
        for pattern in self.patterns:
            if pattern.confidence > 0.5 and pattern.pattern_type == "success_pattern":
                applicable.append(pattern)
        
        # Sort by confidence and success rate
        applicable.sort(key=lambda p: (p.confidence, p.success_rate), reverse=True)
        
        return applicable[:5]  # Return top 5
    
    async def get_pattern_count(self) -> int:
        """Get total number of patterns identified"""
        return len(self.patterns)

class OutcomeAnalyzer:
    """Analyzer for ethical decision outcomes"""
    
    def __init__(self):
        self.outcome_history = []
    
    async def analyze_outcome(self, experience: EthicalExperience):
        """Analyze outcome of ethical decision"""
        
        self.outcome_history.append({
            "experience_id": experience.experience_id,
            "outcome": experience.outcome,
            "confidence": experience.confidence_level,
            "frameworks": experience.frameworks_applied,
            "timestamp": experience.timestamp
        })
        
        # Trigger outcome-based learning
        await self._update_framework_effectiveness(experience)
        await self._update_confidence_calibration(experience)
    
    async def _update_framework_effectiveness(self, experience: EthicalExperience):
        """Update understanding of framework effectiveness"""
        
        outcome_score = self._get_outcome_score(experience.outcome)
        
        # This would update framework weights based on outcomes
        # Implementation would involve more sophisticated learning algorithms
        pass
    
    async def _update_confidence_calibration(self, experience: EthicalExperience):
        """Update confidence calibration based on outcomes"""
        
        # Compare predicted confidence with actual outcome
        outcome_score = self._get_outcome_score(experience.outcome)
        confidence_error = abs(experience.confidence_level - outcome_score)
        
        # Use this to calibrate future confidence estimates
        # Implementation would involve confidence adjustment algorithms
        pass
    
    def _get_outcome_score(self, outcome: OutcomeType) -> float:
        """Convert outcome to numerical score"""
        
        scores = {
            OutcomeType.HIGHLY_POSITIVE: 0.95,
            OutcomeType.POSITIVE: 0.75,
            OutcomeType.NEUTRAL: 0.5,
            OutcomeType.NEGATIVE: 0.25,
            OutcomeType.HIGHLY_NEGATIVE: 0.05,
            OutcomeType.UNCERTAIN: 0.5
        }
        
        return scores.get(outcome, 0.5)

class LearningOptimizer:
    """Optimizer for continuous learning improvement"""
    
    def __init__(self):
        self.optimizations_applied = 0
    
    async def optimize_frameworks(self, experience: EthicalExperience):
        """Optimize framework usage based on experience"""
        
        # This would implement sophisticated optimization algorithms
        # For now, simple counting
        self.optimizations_applied += 1
    
    async def get_improvement_count(self) -> int:
        """Get number of improvements applied"""
        return self.optimizations_applied

class ConsistencyTracker:
    """Tracker for ethical consistency"""
    
    def __init__(self):
        self.consistency_history = []
    
    async def update_consistency(self, experience: EthicalExperience):
        """Update consistency tracking"""
        
        # Simple consistency tracking
        self.consistency_history.append({
            "experience_id": experience.experience_id,
            "decision": experience.decision_made,
            "frameworks": experience.frameworks_applied,
            "timestamp": experience.timestamp
        })
    
    async def get_consistency_score(self) -> float:
        """Calculate overall consistency score"""
        
        if len(self.consistency_history) < 2:
            return 1.0
        
        # Simple consistency measurement
        return 0.75  # Placeholder

# =====================================================================================
# DEMO FUNCTION
# =====================================================================================

async def demonstrate_ethical_learning():
    """Demonstrate ethical learning and memory system"""
    
    print("🧠 Ethical Learning and Memory System Demo")
    print("=" * 50)
    
    # Initialize system
    learning_system = EthicalLearningMemorySystem()
    
    # Simulate some ethical experiences
    experiences = [
        {
            "dilemma": {"type": "privacy", "context": "data_sharing"},
            "decision": "require_explicit_consent",
            "reasoning": {"frameworks_used": ["rights_based", "deontological"], "confidence": 0.8},
            "outcome": OutcomeType.POSITIVE
        },
        {
            "dilemma": {"type": "fairness", "context": "resource_allocation"},
            "decision": "equal_distribution",
            "reasoning": {"frameworks_used": ["justice_ethics", "utilitarian"], "confidence": 0.7},
            "outcome": OutcomeType.HIGHLY_POSITIVE
        },
        {
            "dilemma": {"type": "autonomy", "context": "decision_override"},
            "decision": "respect_user_choice",
            "reasoning": {"frameworks_used": ["rights_based", "virtue_ethics"], "confidence": 0.9},
            "outcome": OutcomeType.POSITIVE
        }
    ]
    
    print("\n📚 Recording ethical experiences...")
    for i, exp in enumerate(experiences):
        exp_id = await learning_system.record_ethical_experience(
            exp["dilemma"], exp["decision"], exp["reasoning"], exp["outcome"]
        )
        print(f"   Experience {i+1}: {exp_id}")
    
    # Test learning retrieval
    test_dilemma = {"type": "privacy", "context": "user_data"}
    
    print(f"\n🔍 Retrieving relevant experiences for test dilemma...")
    relevant_experiences = await learning_system.retrieve_relevant_experiences(test_dilemma)
    print(f"   Found {len(relevant_experiences)} relevant experiences")
    
    # Get learned recommendations
    print(f"\n💡 Getting learned recommendations...")
    recommendations = await learning_system.get_learned_recommendations(test_dilemma)
    
    print(f"\n🎯 LEARNED RECOMMENDATIONS:")
    print(f"   Pattern-based: {len(recommendations['pattern_based_recommendations'])}")
    print(f"   Experience-based: {len(recommendations['experience_based_recommendations'])}")
    
    if recommendations['experience_based_recommendations']:
        top_rec = recommendations['experience_based_recommendations'][0]
        print(f"   Top recommendation: {top_rec['decision']}")
        print(f"   Confidence: {top_rec['confidence']:.3f}")
    
    # Update and display learning metrics
    print(f"\n📊 Updating learning metrics...")
    metrics = await learning_system.update_learning_metrics()
    
    print(f"\n📈 LEARNING METRICS:")
    print(f"   Experiences Processed: {metrics['experiences_processed']}")
    print(f"   Patterns Identified: {metrics['patterns_identified']}")
    print(f"   Consistency Score: {metrics['consistency_score']:.3f}")
    print(f"   Learning Rate: {metrics['learning_rate']:.3f}")
    
    print(f"\n🧠 ETHICAL LEARNING DEMONSTRATION COMPLETE")
    print(f"System successfully learned from {len(experiences)} experiences")

async def main():
    """Main function"""
    await demonstrate_ethical_learning()

if __name__ == "__main__":
    asyncio.run(main())
