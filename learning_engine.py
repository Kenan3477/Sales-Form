"""
Learning Engine for Advanced Synthetic Intelligence System
Implements multiple learning paradigms and adaptation mechanisms
"""

import asyncio
import logging
import numpy as np
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from enum import Enum
import pickle
import hashlib
from collections import defaultdict, deque
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LearningType(Enum):
    """Types of learning paradigms"""
    SUPERVISED = "supervised"
    UNSUPERVISED = "unsupervised"  
    REINFORCEMENT = "reinforcement"
    FEW_SHOT = "few_shot"
    CONTINUAL = "continual"
    META = "meta"
    SELF_SUPERVISED = "self_supervised"


class LearningStrategy(Enum):
    """Learning strategies for different contexts"""
    EXPLORATION = "exploration"
    EXPLOITATION = "exploitation"
    BALANCED = "balanced"
    CONSERVATIVE = "conservative"
    AGGRESSIVE = "aggressive"


@dataclass
class LearningExperience:
    """Represents a single learning experience"""
    experience_id: str
    input_data: Any
    expected_output: Optional[Any] = None
    actual_output: Optional[Any] = None
    feedback: Optional[float] = None  # -1.0 to 1.0
    learning_type: LearningType = LearningType.SUPERVISED
    context: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    importance: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.experience_id:
            self.experience_id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate unique experience ID"""
        content = f"{self.input_data}{self.timestamp}{hash(str(self.metadata))}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def calculate_error(self) -> Optional[float]:
        """Calculate error if both expected and actual outputs exist"""
        if self.expected_output is None or self.actual_output is None:
            return None
        
        try:
            if isinstance(self.expected_output, (int, float)):
                return abs(self.expected_output - self.actual_output)
            elif isinstance(self.expected_output, str):
                return 0.0 if self.expected_output == self.actual_output else 1.0
            else:
                # For complex data types, use a simple mismatch metric
                return 0.0 if self.expected_output == self.actual_output else 1.0
        except:
            return 1.0  # Maximum error if comparison fails


@dataclass
class LearningPattern:
    """Represents a learned pattern or rule"""
    pattern_id: str
    description: str
    conditions: List[str]
    action: str
    confidence: float = 0.5
    usage_count: int = 0
    success_rate: float = 0.5
    last_used: Optional[datetime] = None
    examples: List[str] = field(default_factory=list)
    
    def apply(self, context: Dict[str, Any]) -> bool:
        """Check if pattern applies to given context"""
        self.usage_count += 1
        self.last_used = datetime.now()
        
        # Simple condition checking - would be more sophisticated in practice
        for condition in self.conditions:
            if condition not in str(context):
                return False
        return True
    
    def update_success_rate(self, success: bool):
        """Update success rate based on outcome"""
        if self.usage_count == 1:
            self.success_rate = 1.0 if success else 0.0
        else:
            # Exponential moving average
            alpha = 0.1
            self.success_rate = alpha * (1.0 if success else 0.0) + (1 - alpha) * self.success_rate
        
        # Update confidence based on success rate and usage
        self.confidence = self.success_rate * min(1.0, self.usage_count / 10.0)


class LearningModule(ABC):
    """Abstract base class for learning modules"""
    
    def __init__(self, name: str, learning_type: LearningType):
        self.name = name
        self.learning_type = learning_type
        self.experiences: List[LearningExperience] = []
        self.patterns: Dict[str, LearningPattern] = {}
        self.performance_history: List[Tuple[datetime, float]] = []
        self.active = True
    
    @abstractmethod
    async def learn(self, experience: LearningExperience) -> Dict[str, Any]:
        """Learn from a single experience"""
        pass
    
    @abstractmethod
    async def predict(self, input_data: Any) -> Tuple[Any, float]:
        """Make prediction with confidence"""
        pass
    
    @abstractmethod
    def get_patterns(self) -> List[LearningPattern]:
        """Get learned patterns"""
        pass
    
    def add_experience(self, experience: LearningExperience):
        """Add learning experience to module"""
        self.experiences.append(experience)
        
        # Keep only recent experiences to manage memory
        if len(self.experiences) > 10000:
            self.experiences = self.experiences[-8000:]  # Keep last 8000
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """Calculate performance metrics"""
        if not self.experiences:
            return {"accuracy": 0.0, "confidence": 0.0, "experience_count": 0}
        
        errors = [exp.calculate_error() for exp in self.experiences[-100:] 
                 if exp.calculate_error() is not None]
        
        accuracy = 1.0 - (sum(errors) / len(errors)) if errors else 0.0
        confidence = np.mean([p.confidence for p in self.patterns.values()]) if self.patterns else 0.0
        
        return {
            "accuracy": accuracy,
            "confidence": confidence,
            "experience_count": len(self.experiences),
            "pattern_count": len(self.patterns)
        }


class SupervisedLearningModule(LearningModule):
    """Supervised learning with labeled examples"""
    
    def __init__(self):
        super().__init__("SupervisedLearning", LearningType.SUPERVISED)
        self.feature_weights: Dict[str, float] = {}
        self.class_distributions: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    
    async def learn(self, experience: LearningExperience) -> Dict[str, Any]:
        """Learn from labeled experience"""
        if experience.expected_output is None:
            return {"error": "Supervised learning requires expected output"}
        
        self.add_experience(experience)
        
        # Extract features (simple word-based for text)
        features = self._extract_features(experience.input_data)
        target = str(experience.expected_output)
        
        # Update feature weights and class distributions
        for feature in features:
            self.feature_weights[feature] = self.feature_weights.get(feature, 0.0) + 1.0
            self.class_distributions[target][feature] += 1
        
        # Create or update pattern
        pattern_id = f"supervised_{len(self.patterns)}"
        if pattern_id not in self.patterns:
            pattern = LearningPattern(
                pattern_id=pattern_id,
                description=f"Supervised pattern for {target}",
                conditions=features[:5],  # Top features
                action=f"predict_{target}",
                examples=[str(experience.input_data)]
            )
            self.patterns[pattern_id] = pattern
        
        return {
            "features_extracted": len(features),
            "pattern_created": pattern_id,
            "total_patterns": len(self.patterns)
        }
    
    async def predict(self, input_data: Any) -> Tuple[Any, float]:
        """Make supervised prediction"""
        features = self._extract_features(input_data)
        
        if not self.class_distributions:
            return None, 0.0
        
        # Simple Naive Bayes-like prediction
        class_scores = {}
        for class_name, feature_counts in self.class_distributions.items():
            score = 1.0
            for feature in features:
                count = feature_counts.get(feature, 1)
                total = sum(feature_counts.values())
                probability = count / total if total > 0 else 0.01
                score *= probability
            class_scores[class_name] = score
        
        if class_scores:
            best_class = max(class_scores, key=class_scores.get)
            confidence = class_scores[best_class] / sum(class_scores.values())
            return best_class, min(confidence, 1.0)
        
        return None, 0.0
    
    def _extract_features(self, data: Any) -> List[str]:
        """Extract features from input data"""
        if isinstance(data, str):
            # Simple word-based features
            words = data.lower().split()
            return [word for word in words if len(word) > 2]
        elif isinstance(data, dict):
            # Dictionary keys as features
            return list(data.keys())
        else:
            # Convert to string and extract
            return str(data).lower().split()
    
    def get_patterns(self) -> List[LearningPattern]:
        return list(self.patterns.values())


class ReinforcementLearningModule(LearningModule):
    """Reinforcement learning with rewards/penalties"""
    
    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.9):
        super().__init__("ReinforcementLearning", LearningType.REINFORCEMENT)
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.q_table: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        self.state_action_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.epsilon = 0.1  # Exploration rate
    
    async def learn(self, experience: LearningExperience) -> Dict[str, Any]:
        """Learn from reinforcement experience"""
        if experience.feedback is None:
            return {"error": "Reinforcement learning requires feedback"}
        
        self.add_experience(experience)
        
        state = str(experience.input_data)
        action = str(experience.actual_output) if experience.actual_output else "unknown"
        reward = experience.feedback
        
        # Update Q-value using Q-learning formula
        current_q = self.q_table[state][action]
        
        # Estimate future value (simplified - no next state for now)
        future_value = max(self.q_table[state].values()) if self.q_table[state] else 0.0
        
        # Q-learning update
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * future_value - current_q)
        self.q_table[state][action] = new_q
        
        self.state_action_counts[state][action] += 1
        
        # Create pattern if significant Q-value
        if abs(new_q) > 0.5:
            pattern_id = f"rl_{state}_{action}"
            if pattern_id not in self.patterns:
                pattern = LearningPattern(
                    pattern_id=pattern_id,
                    description=f"RL pattern: {action} in {state}",
                    conditions=[state],
                    action=action,
                    confidence=min(abs(new_q), 1.0)
                )
                self.patterns[pattern_id] = pattern
        
        return {
            "state": state,
            "action": action,
            "reward": reward,
            "new_q_value": new_q,
            "total_states": len(self.q_table)
        }
    
    async def predict(self, input_data: Any) -> Tuple[Any, float]:
        """Select action using epsilon-greedy policy"""
        state = str(input_data)
        
        if state not in self.q_table or not self.q_table[state]:
            return "explore", 0.1
        
        # Epsilon-greedy action selection
        if np.random.random() < self.epsilon:
            # Explore: random action
            actions = list(self.q_table[state].keys())
            action = np.random.choice(actions) if actions else "explore"
            confidence = 0.1
        else:
            # Exploit: best action
            action = max(self.q_table[state], key=self.q_table[state].get)
            q_value = self.q_table[state][action]
            confidence = min(abs(q_value), 1.0)
        
        return action, confidence
    
    def get_patterns(self) -> List[LearningPattern]:
        return list(self.patterns.values())


class UnsupervisedLearningModule(LearningModule):
    """Unsupervised learning for pattern discovery"""
    
    def __init__(self):
        super().__init__("UnsupervisedLearning", LearningType.UNSUPERVISED)
        self.clusters: Dict[str, List[Any]] = {}
        self.feature_correlations: Dict[Tuple[str, str], float] = {}
        self.anomaly_threshold = 2.0
    
    async def learn(self, experience: LearningExperience) -> Dict[str, Any]:
        """Learn patterns without labels"""
        self.add_experience(experience)
        
        # Extract features
        features = self._extract_features(experience.input_data)
        
        # Simple clustering based on feature similarity
        cluster_id = self._find_or_create_cluster(features)
        
        # Update feature correlations
        self._update_correlations(features)
        
        # Detect anomalies
        is_anomaly = self._detect_anomaly(features)
        
        # Create pattern if new cluster or anomaly
        if cluster_id.startswith("new_") or is_anomaly:
            pattern_id = f"unsupervised_{len(self.patterns)}"
            pattern = LearningPattern(
                pattern_id=pattern_id,
                description=f"Unsupervised pattern: {cluster_id}",
                conditions=features[:3],
                action=f"cluster_{cluster_id}",
                confidence=0.7 if not is_anomaly else 0.3
            )
            self.patterns[pattern_id] = pattern
        
        return {
            "cluster_id": cluster_id,
            "is_anomaly": is_anomaly,
            "total_clusters": len(self.clusters),
            "feature_count": len(features)
        }
    
    async def predict(self, input_data: Any) -> Tuple[Any, float]:
        """Predict cluster membership"""
        features = self._extract_features(input_data)
        cluster_id = self._find_best_cluster(features)
        
        if cluster_id:
            confidence = self._calculate_cluster_confidence(features, cluster_id)
            return cluster_id, confidence
        
        return "unknown_cluster", 0.1
    
    def _extract_features(self, data: Any) -> List[str]:
        """Extract features from data"""
        if isinstance(data, str):
            return data.lower().split()
        elif isinstance(data, dict):
            return [f"{k}:{v}" for k, v in data.items()]
        else:
            return str(data).split()
    
    def _find_or_create_cluster(self, features: List[str]) -> str:
        """Find best matching cluster or create new one"""
        best_cluster = None
        best_similarity = 0.0
        
        for cluster_id, cluster_data in self.clusters.items():
            similarity = self._calculate_similarity(features, cluster_data[-1] if cluster_data else [])
            if similarity > best_similarity and similarity > 0.7:
                best_similarity = similarity
                best_cluster = cluster_id
        
        if best_cluster:
            self.clusters[best_cluster].append(features)
            return best_cluster
        else:
            # Create new cluster
            new_cluster_id = f"cluster_{len(self.clusters)}"
            self.clusters[new_cluster_id] = [features]
            return f"new_{new_cluster_id}"
    
    def _find_best_cluster(self, features: List[str]) -> Optional[str]:
        """Find best matching existing cluster"""
        best_cluster = None
        best_similarity = 0.0
        
        for cluster_id, cluster_data in self.clusters.items():
            if cluster_data:
                avg_similarity = np.mean([
                    self._calculate_similarity(features, data) 
                    for data in cluster_data[-5:]  # Use last 5 examples
                ])
                if avg_similarity > best_similarity:
                    best_similarity = avg_similarity
                    best_cluster = cluster_id
        
        return best_cluster if best_similarity > 0.3 else None
    
    def _calculate_similarity(self, features1: List[str], features2: List[str]) -> float:
        """Calculate Jaccard similarity between feature sets"""
        set1, set2 = set(features1), set(features2)
        if not set1 and not set2:
            return 1.0
        if not set1 or not set2:
            return 0.0
        return len(set1.intersection(set2)) / len(set1.union(set2))
    
    def _calculate_cluster_confidence(self, features: List[str], cluster_id: str) -> float:
        """Calculate confidence for cluster assignment"""
        if cluster_id not in self.clusters or not self.clusters[cluster_id]:
            return 0.0
        
        similarities = [
            self._calculate_similarity(features, data)
            for data in self.clusters[cluster_id]
        ]
        return np.mean(similarities)
    
    def _update_correlations(self, features: List[str]):
        """Update feature correlation matrix"""
        for i, feat1 in enumerate(features):
            for feat2 in features[i+1:]:
                pair = tuple(sorted([feat1, feat2]))
                self.feature_correlations[pair] = self.feature_correlations.get(pair, 0.0) + 1.0
    
    def _detect_anomaly(self, features: List[str]) -> bool:
        """Simple anomaly detection based on feature frequency"""
        feature_counts = defaultdict(int)
        for exp in self.experiences[-100:]:  # Last 100 experiences
            exp_features = self._extract_features(exp.input_data)
            for feature in exp_features:
                feature_counts[feature] += 1
        
        if not feature_counts:
            return True
        
        avg_count = np.mean(list(feature_counts.values()))
        std_count = np.std(list(feature_counts.values()))
        
        rare_features = sum(1 for feat in features 
                           if feature_counts[feat] < avg_count - self.anomaly_threshold * std_count)
        
        return rare_features > len(features) * 0.5
    
    def get_patterns(self) -> List[LearningPattern]:
        return list(self.patterns.values())


class CuriosityDrivenExploration:
    """Implements curiosity-driven learning and exploration"""
    
    def __init__(self):
        self.novelty_tracker: Dict[str, float] = {}
        self.exploration_history: List[Tuple[str, datetime]] = []
        self.surprise_threshold = 0.7
        self.curiosity_decay = 0.95
    
    def assess_novelty(self, input_data: Any) -> float:
        """Assess how novel the input is"""
        data_hash = hashlib.md5(str(input_data).encode()).hexdigest()
        
        if data_hash in self.novelty_tracker:
            # Familiar data - low novelty
            self.novelty_tracker[data_hash] *= self.curiosity_decay
            return self.novelty_tracker[data_hash]
        else:
            # New data - high novelty
            novelty = 1.0
            self.novelty_tracker[data_hash] = novelty
            self.exploration_history.append((data_hash, datetime.now()))
            return novelty
    
    def generate_curiosity_reward(self, input_data: Any, prediction_confidence: float) -> float:
        """Generate curiosity-based reward signal"""
        novelty = self.assess_novelty(input_data)
        uncertainty = 1.0 - prediction_confidence
        
        # Curiosity is high when novelty is high and uncertainty is high
        curiosity_reward = novelty * uncertainty
        
        return curiosity_reward
    
    def should_explore(self, current_context: str) -> bool:
        """Decide whether to explore or exploit"""
        recent_explorations = [
            exp for exp in self.exploration_history[-50:]
            if (datetime.now() - exp[1]).seconds < 3600  # Last hour
        ]
        
        # Explore if haven't explored recently
        return len(recent_explorations) < 10


class MetaLearningModule(LearningModule):
    """Meta-learning: learning how to learn"""
    
    def __init__(self):
        super().__init__("MetaLearning", LearningType.META)
        self.learning_strategies: Dict[str, Dict[str, Any]] = {}
        self.strategy_performance: Dict[str, List[float]] = defaultdict(list)
        self.current_strategy = "balanced"
    
    async def learn(self, experience: LearningExperience) -> Dict[str, Any]:
        """Learn about learning strategies"""
        self.add_experience(experience)
        
        # Extract learning context
        context = experience.metadata.get("learning_context", "general")
        strategy = experience.metadata.get("strategy_used", "unknown")
        performance = experience.metadata.get("performance", 0.5)
        
        # Update strategy performance
        if strategy != "unknown":
            self.strategy_performance[strategy].append(performance)
        
        # Adapt current strategy based on performance
        self._adapt_strategy(context, performance)
        
        return {
            "context": context,
            "strategy": strategy,
            "performance": performance,
            "current_strategy": self.current_strategy
        }
    
    async def predict(self, input_data: Any) -> Tuple[Any, float]:
        """Predict best learning strategy for given context"""
        context = str(input_data)
        
        # Recommend strategy based on performance history
        best_strategy = self._select_best_strategy(context)
        confidence = self._calculate_strategy_confidence(best_strategy)
        
        return best_strategy, confidence
    
    def _adapt_strategy(self, context: str, performance: float):
        """Adapt learning strategy based on performance"""
        if performance > 0.8:
            # High performance - continue current strategy
            pass
        elif performance < 0.3:
            # Low performance - switch strategy
            strategies = ["exploration", "exploitation", "balanced", "conservative"]
            current_idx = strategies.index(self.current_strategy) if self.current_strategy in strategies else 0
            self.current_strategy = strategies[(current_idx + 1) % len(strategies)]
        # Medium performance - small adjustments
    
    def _select_best_strategy(self, context: str) -> str:
        """Select best strategy for given context"""
        if not self.strategy_performance:
            return "balanced"
        
        # Find strategy with best average performance
        best_strategy = "balanced"
        best_avg = 0.0
        
        for strategy, performances in self.strategy_performance.items():
            if performances:
                avg_performance = np.mean(performances[-10:])  # Recent performance
                if avg_performance > best_avg:
                    best_avg = avg_performance
                    best_strategy = strategy
        
        return best_strategy
    
    def _calculate_strategy_confidence(self, strategy: str) -> float:
        """Calculate confidence in strategy recommendation"""
        if strategy not in self.strategy_performance:
            return 0.5
        
        performances = self.strategy_performance[strategy]
        if not performances:
            return 0.5
        
        # Confidence based on consistency and recency
        recent_perf = performances[-5:] if len(performances) >= 5 else performances
        avg_perf = np.mean(recent_perf)
        std_perf = np.std(recent_perf) if len(recent_perf) > 1 else 0.5
        
        # High average and low std = high confidence
        confidence = avg_perf * (1.0 - min(std_perf, 0.5))
        return min(confidence, 1.0)
    
    def get_patterns(self) -> List[LearningPattern]:
        """Get meta-learning patterns"""
        patterns = []
        for strategy, performances in self.strategy_performance.items():
            if performances:
                avg_perf = np.mean(performances)
                pattern = LearningPattern(
                    pattern_id=f"meta_{strategy}",
                    description=f"Meta pattern for {strategy} strategy",
                    conditions=[f"context_requires_{strategy}"],
                    action=f"use_{strategy}_strategy",
                    confidence=avg_perf
                )
                patterns.append(pattern)
        return patterns


class AdaptiveLearningEngine:
    """Main learning engine coordinating multiple learning modules"""
    
    def __init__(self):
        self.modules: Dict[LearningType, LearningModule] = {
            LearningType.SUPERVISED: SupervisedLearningModule(),
            LearningType.REINFORCEMENT: ReinforcementLearningModule(),
            LearningType.UNSUPERVISED: UnsupervisedLearningModule(),
            LearningType.META: MetaLearningModule()
        }
        
        self.curiosity_system = CuriosityDrivenExploration()
        self.learning_history: List[LearningExperience] = []
        self.active_strategies: Set[LearningStrategy] = {LearningStrategy.BALANCED}
        self.performance_metrics: Dict[str, float] = {}
        
        logger.info("Adaptive Learning Engine initialized")
    
    async def learn_from_experience(self, experience: LearningExperience) -> Dict[str, Any]:
        """Learn from experience using appropriate modules"""
        self.learning_history.append(experience)
        
        results = {}
        
        # Route to appropriate learning module(s)
        if experience.learning_type in self.modules:
            module = self.modules[experience.learning_type]
            result = await module.learn(experience)
            results[experience.learning_type.value] = result
        else:
            # Try multiple modules for comprehensive learning
            for learning_type, module in self.modules.items():
                if module.active:
                    try:
                        result = await module.learn(experience)
                        results[learning_type.value] = result
                    except Exception as e:
                        logger.error(f"Error in {learning_type.value} learning: {e}")
        
        # Generate curiosity reward
        curiosity_reward = self.curiosity_system.generate_curiosity_reward(
            experience.input_data, 
            experience.metadata.get("prediction_confidence", 0.5)
        )
        
        # Update performance metrics
        self._update_performance_metrics(experience, results)
        
        return {
            "experience_id": experience.experience_id,
            "learning_results": results,
            "curiosity_reward": curiosity_reward,
            "performance_metrics": self.performance_metrics
        }
    
    async def make_prediction(self, input_data: Any, learning_types: Optional[List[LearningType]] = None) -> Dict[str, Tuple[Any, float]]:
        """Make predictions using specified learning modules"""
        if learning_types is None:
            learning_types = list(self.modules.keys())
        
        predictions = {}
        
        for learning_type in learning_types:
            if learning_type in self.modules and self.modules[learning_type].active:
                try:
                    prediction, confidence = await self.modules[learning_type].predict(input_data)
                    predictions[learning_type.value] = (prediction, confidence)
                except Exception as e:
                    logger.error(f"Error in {learning_type.value} prediction: {e}")
                    predictions[learning_type.value] = (None, 0.0)
        
        return predictions
    
    def get_learned_patterns(self, learning_type: Optional[LearningType] = None) -> List[LearningPattern]:
        """Get learned patterns from modules"""
        patterns = []
        
        if learning_type and learning_type in self.modules:
            patterns.extend(self.modules[learning_type].get_patterns())
        else:
            for module in self.modules.values():
                patterns.extend(module.get_patterns())
        
        return patterns
    
    def _update_performance_metrics(self, experience: LearningExperience, results: Dict[str, Any]):
        """Update overall performance metrics"""
        # Calculate error if possible
        error = experience.calculate_error()
        if error is not None:
            if "accuracy" not in self.performance_metrics:
                self.performance_metrics["accuracy"] = 1.0 - error
            else:
                # Exponential moving average
                alpha = 0.1
                self.performance_metrics["accuracy"] = (
                    alpha * (1.0 - error) + (1 - alpha) * self.performance_metrics["accuracy"]
                )
        
        # Update learning rate metrics
        total_patterns = sum(len(module.get_patterns()) for module in self.modules.values())
        self.performance_metrics["total_patterns"] = total_patterns
        self.performance_metrics["learning_experiences"] = len(self.learning_history)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive learning system status"""
        module_status = {}
        for learning_type, module in self.modules.items():
            module_status[learning_type.value] = module.get_performance_metrics()
        
        return {
            "active_modules": len([m for m in self.modules.values() if m.active]),
            "total_experiences": len(self.learning_history),
            "performance_metrics": self.performance_metrics,
            "module_status": module_status,
            "curiosity_novelties": len(self.curiosity_system.novelty_tracker),
            "active_strategies": [s.value for s in self.active_strategies]
        }
    
    async def adaptive_learning_cycle(self, duration_minutes: int = 60):
        """Run adaptive learning cycle"""
        logger.info(f"Starting adaptive learning cycle for {duration_minutes} minutes")
        
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        while datetime.now() < end_time:
            try:
                # Simulate learning experiences
                await self._simulate_learning_experience()
                
                # Evaluate and adapt strategies
                await self._evaluate_and_adapt()
                
                # Brief pause
                await asyncio.sleep(10)
                
            except Exception as e:
                logger.error(f"Error in learning cycle: {e}")
                await asyncio.sleep(30)
        
        logger.info("Adaptive learning cycle completed")
    
    async def _simulate_learning_experience(self):
        """Simulate a learning experience for testing"""
        # This would be replaced with real experiences in production
        import random
        
        learning_types = [LearningType.SUPERVISED, LearningType.REINFORCEMENT, LearningType.UNSUPERVISED]
        learning_type = random.choice(learning_types)
        
        experience = LearningExperience(
            experience_id="",
            input_data=f"test_input_{random.randint(1, 100)}",
            expected_output=f"output_{random.randint(1, 10)}" if learning_type == LearningType.SUPERVISED else None,
            actual_output=f"output_{random.randint(1, 10)}",
            feedback=random.uniform(-1, 1) if learning_type == LearningType.REINFORCEMENT else None,
            learning_type=learning_type,
            context="simulation"
        )
        
        await self.learn_from_experience(experience)
    
    async def _evaluate_and_adapt(self):
        """Evaluate performance and adapt strategies"""
        # Simple adaptation logic
        if "accuracy" in self.performance_metrics:
            accuracy = self.performance_metrics["accuracy"]
            
            if accuracy > 0.8:
                self.active_strategies = {LearningStrategy.EXPLOITATION}
            elif accuracy < 0.4:
                self.active_strategies = {LearningStrategy.EXPLORATION}
            else:
                self.active_strategies = {LearningStrategy.BALANCED}


# Example usage and demonstration
async def demo_learning_engine():
    """Demonstrate the learning engine"""
    print("=== Adaptive Learning Engine Demo ===\n")
    
    engine = AdaptiveLearningEngine()
    
    # Create test experiences
    experiences = [
        LearningExperience(
            experience_id="",
            input_data="classify this text as positive or negative",
            expected_output="positive",
            actual_output="positive",
            learning_type=LearningType.SUPERVISED,
            context="sentiment_analysis"
        ),
        LearningExperience(
            experience_id="",
            input_data="action_taken",
            actual_output="move_right", 
            feedback=0.8,
            learning_type=LearningType.REINFORCEMENT,
            context="game_playing"
        ),
        LearningExperience(
            experience_id="",
            input_data="discover patterns in user behavior data",
            learning_type=LearningType.UNSUPERVISED,
            context="user_analysis"
        )
    ]
    
    # Learn from experiences
    for i, exp in enumerate(experiences):
        print(f"Learning from experience {i+1}...")
        result = await engine.learn_from_experience(exp)
        print(f"Result: {result}\n")
    
    # Make predictions
    print("Making predictions...")
    predictions = await engine.make_prediction("new test input")
    for learning_type, (prediction, confidence) in predictions.items():
        print(f"{learning_type}: {prediction} (confidence: {confidence:.3f})")
    
    # Show learned patterns
    patterns = engine.get_learned_patterns()
    print(f"\nLearned {len(patterns)} patterns:")
    for pattern in patterns[:5]:  # Show first 5
        print(f"- {pattern.description} (confidence: {pattern.confidence:.3f})")
    
    # System status
    status = engine.get_system_status()
    print(f"\nSystem Status:")
    print(json.dumps(status, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(demo_learning_engine())
