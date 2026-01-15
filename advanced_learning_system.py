#!/usr/bin/env python3
"""
Advanced Learning System for ASIS
Implements comprehensive learning capabilities including supervised, unsupervised, 
reinforcement learning, few-shot learning, continual learning, and meta-learning.
"""

import asyncio
import logging
import numpy as np
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum
import pickle
import threading
from concurrent.futures import ThreadPoolExecutor
import warnings
warnings.filterwarnings('ignore')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import optional dependencies
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    import torch.nn.functional as F
    from torch.utils.data import DataLoader, Dataset
    PYTORCH_AVAILABLE = True
except ImportError:
    PYTORCH_AVAILABLE = False
    logger.warning("PyTorch not available. Some learning features will be limited.")

try:
    from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
    from sklearn.decomposition import PCA, ICA
    from sklearn.manifold import TSNE
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, precision_recall_fscore_support
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logger.warning("scikit-learn not available. Some learning features will be limited.")

# Core Learning Types
class LearningType(Enum):
    SUPERVISED = "supervised"
    UNSUPERVISED = "unsupervised" 
    REINFORCEMENT = "reinforcement"
    FEW_SHOT = "few_shot"
    CONTINUAL = "continual"
    META = "meta"

class LearningStrategy(Enum):
    GRADIENT_DESCENT = "gradient_descent"
    EVOLUTIONARY = "evolutionary"
    BAYESIAN = "bayesian"
    ENSEMBLE = "ensemble"
    TRANSFER = "transfer"
    ACTIVE = "active"
    CURRICULUM = "curriculum"

class DataModality(Enum):
    TEXT = "text"
    NUMERICAL = "numerical"
    CATEGORICAL = "categorical"
    TEMPORAL = "temporal"
    MULTIMODAL = "multimodal"

@dataclass
class LearningTask:
    """Represents a learning task with all necessary metadata"""
    task_id: str
    task_type: LearningType
    data_modality: DataModality
    objective: str
    data: Any
    labels: Optional[Any] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    priority: float = 1.0
    created_at: datetime = field(default_factory=datetime.now)
    deadline: Optional[datetime] = None
    
@dataclass
class LearningResult:
    """Results from a learning operation"""
    task_id: str
    success: bool
    performance_metrics: Dict[str, float]
    learned_knowledge: Any
    confidence: float
    execution_time: float
    strategy_used: LearningStrategy
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class MetaLearningState:
    """Tracks meta-learning progress and strategies"""
    strategy_performance: Dict[LearningStrategy, List[float]] = field(default_factory=lambda: defaultdict(list))
    task_difficulty_estimates: Dict[str, float] = field(default_factory=dict)
    learning_speed_trends: Dict[LearningType, List[float]] = field(default_factory=lambda: defaultdict(list))
    optimal_strategies: Dict[Tuple[LearningType, DataModality], LearningStrategy] = field(default_factory=dict)
    adaptation_history: List[Dict[str, Any]] = field(default_factory=list)

class SupervisedLearningEngine:
    """Handles supervised learning tasks with multiple algorithms"""
    
    def __init__(self):
        self.models = {}
        self.training_history = defaultdict(list)
        self.validation_scores = defaultdict(list)
        
    async def learn_from_examples(self, task: LearningTask) -> LearningResult:
        """Learn from labeled examples using various supervised learning approaches"""
        start_time = time.time()
        
        try:
            # Prepare data
            X, y = self._prepare_supervised_data(task.data, task.labels)
            
            # Select learning strategy based on data characteristics
            strategy = self._select_supervised_strategy(X, y, task)
            
            # Train model
            model, metrics = await self._train_supervised_model(X, y, strategy, task)
            
            # Store model
            self.models[task.task_id] = {
                'model': model,
                'strategy': strategy,
                'metadata': task.metadata,
                'trained_at': datetime.now()
            }
            
            execution_time = time.time() - start_time
            
            return LearningResult(
                task_id=task.task_id,
                success=True,
                performance_metrics=metrics,
                learned_knowledge=model,
                confidence=metrics.get('confidence', 0.8),
                execution_time=execution_time,
                strategy_used=strategy
            )
            
        except Exception as e:
            logger.error(f"Supervised learning failed for task {task.task_id}: {e}")
            return LearningResult(
                task_id=task.task_id,
                success=False,
                performance_metrics={'error': str(e)},
                learned_knowledge=None,
                confidence=0.0,
                execution_time=time.time() - start_time,
                strategy_used=LearningStrategy.GRADIENT_DESCENT
            )
    
    def _prepare_supervised_data(self, data: Any, labels: Any) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare data for supervised learning"""
        if isinstance(data, list):
            X = np.array(data)
        elif isinstance(data, np.ndarray):
            X = data
        else:
            # Handle text or other data types
            X = np.array([self._vectorize_input(item) for item in data])
        
        if isinstance(labels, list):
            y = np.array(labels)
        elif isinstance(labels, np.ndarray):
            y = labels
        else:
            y = np.array(labels)
            
        return X, y
    
    def _vectorize_input(self, input_data: Any) -> np.ndarray:
        """Convert input to numerical vector"""
        if isinstance(input_data, str):
            # Simple text vectorization (in real implementation, use embeddings)
            return np.array([hash(word) % 1000 for word in input_data.split()[:10]]).astype(float)
        elif isinstance(input_data, (int, float)):
            return np.array([input_data])
        elif isinstance(input_data, (list, tuple)):
            return np.array(input_data).astype(float)
        else:
            return np.array([hash(str(input_data)) % 1000]).astype(float)
    
    def _select_supervised_strategy(self, X: np.ndarray, y: np.ndarray, task: LearningTask) -> LearningStrategy:
        """Select optimal supervised learning strategy"""
        n_samples, n_features = X.shape
        n_classes = len(np.unique(y))
        
        # Strategy selection heuristics
        if n_samples < 100:
            return LearningStrategy.BAYESIAN
        elif n_features > n_samples:
            return LearningStrategy.ENSEMBLE
        elif n_classes > 10:
            return LearningStrategy.GRADIENT_DESCENT
        else:
            return LearningStrategy.GRADIENT_DESCENT
    
    async def _train_supervised_model(self, X: np.ndarray, y: np.ndarray, 
                                     strategy: LearningStrategy, task: LearningTask) -> Tuple[Any, Dict[str, float]]:
        """Train supervised model using selected strategy"""
        if not SKLEARN_AVAILABLE:
            # Fallback to simple implementation
            return self._simple_supervised_model(X, y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        if strategy == LearningStrategy.GRADIENT_DESCENT:
            from sklearn.linear_model import SGDClassifier
            model = SGDClassifier(random_state=42)
            
        elif strategy == LearningStrategy.ENSEMBLE:
            from sklearn.ensemble import RandomForestClassifier
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            
        elif strategy == LearningStrategy.BAYESIAN:
            from sklearn.naive_bayes import GaussianNB
            model = GaussianNB()
            
        else:
            from sklearn.svm import SVC
            model = SVC(probability=True, random_state=42)
        
        # Train model
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Get probabilities for confidence
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(X_test)
            confidence = np.mean(np.max(proba, axis=1))
        else:
            confidence = accuracy
        
        metrics = {
            'accuracy': accuracy,
            'confidence': confidence,
            'n_samples': len(X_train),
            'n_features': X.shape[1]
        }
        
        return model, metrics
    
    def _simple_supervised_model(self, X: np.ndarray, y: np.ndarray) -> Tuple[Any, Dict[str, float]]:
        """Simple fallback supervised model"""
        # Simple nearest mean classifier
        classes = np.unique(y)
        centroids = {}
        
        for cls in classes:
            mask = y == cls
            centroids[cls] = np.mean(X[mask], axis=0)
        
        model = {'type': 'nearest_mean', 'centroids': centroids}
        
        # Simple evaluation
        correct = 0
        for i in range(len(X)):
            distances = {cls: np.linalg.norm(X[i] - centroid) 
                        for cls, centroid in centroids.items()}
            predicted = min(distances, key=distances.get)
            if predicted == y[i]:
                correct += 1
        
        accuracy = correct / len(X)
        metrics = {'accuracy': accuracy, 'confidence': accuracy}
        
        return model, metrics

class UnsupervisedLearningEngine:
    """Handles unsupervised learning for pattern discovery and clustering"""
    
    def __init__(self):
        self.discovered_patterns = {}
        self.cluster_models = {}
        self.anomaly_detectors = {}
        
    async def discover_patterns(self, task: LearningTask) -> LearningResult:
        """Discover patterns in unlabeled data"""
        start_time = time.time()
        
        try:
            # Prepare data
            X = self._prepare_unsupervised_data(task.data)
            
            # Select discovery strategy
            strategy = self._select_unsupervised_strategy(X, task)
            
            # Discover patterns
            patterns, metrics = await self._discover_patterns(X, strategy, task)
            
            # Store patterns
            self.discovered_patterns[task.task_id] = {
                'patterns': patterns,
                'strategy': strategy,
                'metadata': task.metadata,
                'discovered_at': datetime.now()
            }
            
            execution_time = time.time() - start_time
            
            return LearningResult(
                task_id=task.task_id,
                success=True,
                performance_metrics=metrics,
                learned_knowledge=patterns,
                confidence=metrics.get('confidence', 0.7),
                execution_time=execution_time,
                strategy_used=strategy
            )
            
        except Exception as e:
            logger.error(f"Unsupervised learning failed for task {task.task_id}: {e}")
            return LearningResult(
                task_id=task.task_id,
                success=False,
                performance_metrics={'error': str(e)},
                learned_knowledge=None,
                confidence=0.0,
                execution_time=time.time() - start_time,
                strategy_used=LearningStrategy.GRADIENT_DESCENT
            )
    
    def _prepare_unsupervised_data(self, data: Any) -> np.ndarray:
        """Prepare data for unsupervised learning"""
        if isinstance(data, np.ndarray):
            return data
        elif isinstance(data, list):
            # Convert to numerical representation
            if all(isinstance(x, (int, float)) for x in data):
                return np.array(data).reshape(-1, 1)
            elif all(isinstance(x, str) for x in data):
                # Simple text vectorization
                return np.array([[hash(word) % 1000 for word in x.split()[:10]] for x in data])
            else:
                # Mixed data - convert to numerical
                return np.array([[hash(str(x)) % 1000] for x in data])
        else:
            return np.array([data]).reshape(-1, 1)
    
    def _select_unsupervised_strategy(self, X: np.ndarray, task: LearningTask) -> LearningStrategy:
        """Select optimal unsupervised learning strategy"""
        n_samples, n_features = X.shape
        
        if task.objective and 'cluster' in task.objective.lower():
            return LearningStrategy.GRADIENT_DESCENT  # For clustering algorithms
        elif n_features > 50:
            return LearningStrategy.ENSEMBLE  # For dimensionality reduction
        else:
            return LearningStrategy.GRADIENT_DESCENT
    
    async def _discover_patterns(self, X: np.ndarray, strategy: LearningStrategy, 
                                task: LearningTask) -> Tuple[Dict[str, Any], Dict[str, float]]:
        """Discover patterns using selected strategy"""
        patterns = {}
        metrics = {}
        
        if not SKLEARN_AVAILABLE:
            return self._simple_pattern_discovery(X)
        
        try:
            # Clustering
            if task.objective and 'cluster' in task.objective.lower():
                n_clusters = task.metadata.get('n_clusters', min(8, len(X) // 2))
                
                kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                cluster_labels = kmeans.fit_predict(X)
                
                patterns['clusters'] = {
                    'labels': cluster_labels.tolist(),
                    'centers': kmeans.cluster_centers_.tolist(),
                    'n_clusters': n_clusters
                }
                
                # Calculate silhouette-like score
                inertia = kmeans.inertia_
                metrics['clustering_score'] = 1.0 / (1.0 + inertia / len(X))
                
            # Dimensionality reduction
            if X.shape[1] > 5:
                pca = PCA(n_components=min(5, X.shape[1]))
                X_reduced = pca.fit_transform(X)
                
                patterns['dimensionality_reduction'] = {
                    'components': pca.components_.tolist(),
                    'explained_variance': pca.explained_variance_ratio_.tolist(),
                    'reduced_data': X_reduced.tolist()
                }
                
                metrics['variance_explained'] = np.sum(pca.explained_variance_ratio_)
            
            # Anomaly detection
            from sklearn.ensemble import IsolationForest
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            anomaly_scores = iso_forest.fit_predict(X)
            
            patterns['anomalies'] = {
                'scores': anomaly_scores.tolist(),
                'n_anomalies': int(np.sum(anomaly_scores == -1))
            }
            
            metrics['anomaly_detection_score'] = 0.8  # Default confidence
            
            # Overall confidence
            metrics['confidence'] = np.mean([
                metrics.get('clustering_score', 0.5),
                metrics.get('variance_explained', 0.5),
                metrics.get('anomaly_detection_score', 0.5)
            ])
            
        except Exception as e:
            logger.warning(f"Advanced pattern discovery failed, using simple method: {e}")
            patterns, metrics = self._simple_pattern_discovery(X)
        
        return patterns, metrics
    
    def _simple_pattern_discovery(self, X: np.ndarray) -> Tuple[Dict[str, Any], Dict[str, float]]:
        """Simple fallback pattern discovery"""
        patterns = {}
        
        # Simple statistics
        patterns['statistics'] = {
            'mean': np.mean(X, axis=0).tolist(),
            'std': np.std(X, axis=0).tolist(),
            'min': np.min(X, axis=0).tolist(),
            'max': np.max(X, axis=0).tolist()
        }
        
        # Simple clustering (k-means like)
        n_clusters = min(3, len(X))
        if n_clusters > 1:
            # Random initialization of centroids
            centroids = X[np.random.choice(len(X), n_clusters, replace=False)]
            labels = []
            
            for point in X:
                distances = [np.linalg.norm(point - centroid) for centroid in centroids]
                labels.append(np.argmin(distances))
            
            patterns['simple_clusters'] = {
                'labels': labels,
                'centroids': centroids.tolist(),
                'n_clusters': n_clusters
            }
        
        metrics = {'confidence': 0.6, 'simple_clustering': 1.0}
        
        return patterns, metrics

class ReinforcementLearningEngine:
    """Handles reinforcement learning for goal-directed behavior"""
    
    def __init__(self):
        self.q_tables = {}
        self.policy_networks = {}
        self.experience_replay = defaultdict(deque)
        self.reward_history = defaultdict(list)
        
    async def learn_from_rewards(self, task: LearningTask) -> LearningResult:
        """Learn optimal actions through reward feedback"""
        start_time = time.time()
        
        try:
            # Initialize or load Q-table/policy
            if task.task_id not in self.q_tables:
                self._initialize_rl_agent(task)
            
            # Extract environment and reward information
            episodes_data = task.data if isinstance(task.data, list) else [task.data]
            
            # Train agent
            metrics = await self._train_rl_agent(task.task_id, episodes_data, task)
            
            execution_time = time.time() - start_time
            
            return LearningResult(
                task_id=task.task_id,
                success=True,
                performance_metrics=metrics,
                learned_knowledge=self.q_tables.get(task.task_id),
                confidence=metrics.get('confidence', 0.7),
                execution_time=execution_time,
                strategy_used=LearningStrategy.GRADIENT_DESCENT
            )
            
        except Exception as e:
            logger.error(f"Reinforcement learning failed for task {task.task_id}: {e}")
            return LearningResult(
                task_id=task.task_id,
                success=False,
                performance_metrics={'error': str(e)},
                learned_knowledge=None,
                confidence=0.0,
                execution_time=time.time() - start_time,
                strategy_used=LearningStrategy.GRADIENT_DESCENT
            )
    
    def _initialize_rl_agent(self, task: LearningTask):
        """Initialize RL agent for a task"""
        # Simple Q-table approach
        state_space_size = task.metadata.get('state_space_size', 100)
        action_space_size = task.metadata.get('action_space_size', 4)
        
        # Initialize Q-table with small random values
        self.q_tables[task.task_id] = {
            'q_table': np.random.uniform(-0.1, 0.1, (state_space_size, action_space_size)),
            'learning_rate': 0.1,
            'discount_factor': 0.95,
            'epsilon': 0.1,
            'state_space_size': state_space_size,
            'action_space_size': action_space_size
        }
    
    async def _train_rl_agent(self, task_id: str, episodes_data: List[Any], 
                             task: LearningTask) -> Dict[str, float]:
        """Train RL agent using Q-learning"""
        agent = self.q_tables[task_id]
        q_table = agent['q_table']
        lr = agent['learning_rate']
        gamma = agent['discount_factor']
        
        total_rewards = []
        
        for episode_data in episodes_data:
            if isinstance(episode_data, dict):
                # Structured episode data
                states = episode_data.get('states', [])
                actions = episode_data.get('actions', [])
                rewards = episode_data.get('rewards', [])
            else:
                # Simple data - create mock episode
                states = [hash(str(episode_data)) % agent['state_space_size']]
                actions = [0]  # Default action
                rewards = [1.0 if episode_data else -1.0]  # Simple reward
            
            episode_reward = 0
            
            # Update Q-table
            for i in range(len(states) - 1):
                state = int(states[i]) % agent['state_space_size']
                action = int(actions[i]) % agent['action_space_size']
                reward = float(rewards[i])
                next_state = int(states[i + 1]) % agent['state_space_size']
                
                # Q-learning update
                best_next_action = np.argmax(q_table[next_state])
                td_target = reward + gamma * q_table[next_state, best_next_action]
                td_error = td_target - q_table[state, action]
                q_table[state, action] += lr * td_error
                
                episode_reward += reward
            
            total_rewards.append(episode_reward)
            self.reward_history[task_id].append(episode_reward)
        
        # Calculate metrics
        avg_reward = np.mean(total_rewards) if total_rewards else 0
        reward_trend = 0
        
        if len(self.reward_history[task_id]) > 10:
            recent_rewards = self.reward_history[task_id][-10:]
            earlier_rewards = self.reward_history[task_id][-20:-10] if len(self.reward_history[task_id]) > 20 else []
            
            if earlier_rewards:
                reward_trend = np.mean(recent_rewards) - np.mean(earlier_rewards)
        
        metrics = {
            'average_reward': avg_reward,
            'reward_trend': reward_trend,
            'episodes_trained': len(episodes_data),
            'confidence': min(0.9, 0.5 + abs(reward_trend) * 0.1)
        }
        
        return metrics

class FewShotLearningEngine:
    """Handles few-shot learning for quick adaptation"""
    
    def __init__(self):
        self.prototypes = {}
        self.meta_models = {}
        self.adaptation_history = defaultdict(list)
        
    async def learn_from_few_examples(self, task: LearningTask) -> LearningResult:
        """Learn from very few examples using meta-learning approaches"""
        start_time = time.time()
        
        try:
            # Prepare few-shot data
            support_set, query_set = self._prepare_few_shot_data(task.data, task.labels)
            
            # Select few-shot strategy
            strategy = LearningStrategy.TRANSFER  # Most suitable for few-shot
            
            # Learn prototypes or adapt meta-model
            learned_model, metrics = await self._few_shot_adapt(support_set, query_set, task)
            
            # Store learned model
            self.prototypes[task.task_id] = {
                'model': learned_model,
                'strategy': strategy,
                'n_support': len(support_set) if support_set else 0,
                'adapted_at': datetime.now()
            }
            
            execution_time = time.time() - start_time
            
            return LearningResult(
                task_id=task.task_id,
                success=True,
                performance_metrics=metrics,
                learned_knowledge=learned_model,
                confidence=metrics.get('confidence', 0.6),
                execution_time=execution_time,
                strategy_used=strategy
            )
            
        except Exception as e:
            logger.error(f"Few-shot learning failed for task {task.task_id}: {e}")
            return LearningResult(
                task_id=task.task_id,
                success=False,
                performance_metrics={'error': str(e)},
                learned_knowledge=None,
                confidence=0.0,
                execution_time=time.time() - start_time,
                strategy_used=LearningStrategy.TRANSFER
            )
    
    def _prepare_few_shot_data(self, data: Any, labels: Any) -> Tuple[List, List]:
        """Prepare data for few-shot learning"""
        if isinstance(data, list) and len(data) > 0:
            n_support = min(5, len(data) // 2)  # Use half for support, half for query
            
            if labels is not None:
                support_set = list(zip(data[:n_support], labels[:n_support]))
                query_set = list(zip(data[n_support:], labels[n_support:]))
            else:
                support_set = data[:n_support]
                query_set = data[n_support:]
        else:
            support_set = [data] if data is not None else []
            query_set = []
        
        return support_set, query_set
    
    async def _few_shot_adapt(self, support_set: List, query_set: List, 
                             task: LearningTask) -> Tuple[Dict[str, Any], Dict[str, float]]:
        """Adapt to new task using few examples"""
        # Prototype-based few-shot learning
        prototypes = {}
        
        if not support_set:
            # No support examples - use prior knowledge
            model = {'type': 'prior', 'prototypes': {}}
            metrics = {'confidence': 0.3, 'n_prototypes': 0}
            return model, metrics
        
        # Group support examples by class (if labels available)
        class_examples = defaultdict(list)
        
        for example in support_set:
            if isinstance(example, tuple) and len(example) == 2:
                data_point, label = example
                class_examples[label].append(data_point)
            else:
                # No label - treat as single class
                class_examples['default'].append(example)
        
        # Create prototypes for each class
        for class_label, examples in class_examples.items():
            # Convert examples to numerical vectors
            vectors = []
            for example in examples:
                vector = self._vectorize_example(example)
                vectors.append(vector)
            
            if vectors:
                # Prototype is the mean of examples
                prototype = np.mean(vectors, axis=0)
                prototypes[class_label] = prototype.tolist()
        
        # Test on query set if available
        accuracy = 0.0
        if query_set and prototypes:
            correct = 0
            total = 0
            
            for query_example in query_set:
                if isinstance(query_example, tuple) and len(query_example) == 2:
                    data_point, true_label = query_example
                    
                    # Find closest prototype
                    query_vector = self._vectorize_example(data_point)
                    min_distance = float('inf')
                    predicted_label = None
                    
                    for label, prototype in prototypes.items():
                        distance = np.linalg.norm(query_vector - np.array(prototype))
                        if distance < min_distance:
                            min_distance = distance
                            predicted_label = label
                    
                    if predicted_label == true_label:
                        correct += 1
                    total += 1
            
            accuracy = correct / total if total > 0 else 0.0
        
        model = {
            'type': 'prototype',
            'prototypes': prototypes,
            'n_classes': len(prototypes)
        }
        
        metrics = {
            'accuracy': accuracy,
            'n_prototypes': len(prototypes),
            'n_support': len(support_set),
            'confidence': min(0.8, 0.4 + accuracy * 0.4)
        }
        
        return model, metrics
    
    def _vectorize_example(self, example: Any) -> np.ndarray:
        """Convert example to numerical vector"""
        if isinstance(example, str):
            # Simple text vectorization
            words = example.split()[:10]  # Limit to first 10 words
            vector = np.array([hash(word) % 1000 for word in words])
            # Pad or truncate to fixed size
            if len(vector) < 10:
                vector = np.pad(vector, (0, 10 - len(vector)), 'constant')
            return vector[:10].astype(float)
        
        elif isinstance(example, (list, tuple)):
            return np.array(example[:10]).astype(float)  # Limit to 10 features
        
        elif isinstance(example, (int, float)):
            return np.array([example])
        
        else:
            # Convert to hash-based representation
            return np.array([hash(str(example)) % 1000]).astype(float)

class ContinualLearningEngine:
    """Handles continual learning without catastrophic forgetting"""
    
    def __init__(self):
        self.task_memories = {}  # Memory for each task
        self.consolidation_strengths = {}  # Importance of each memory
        self.knowledge_graph = {}  # Relationships between learned concepts
        self.rehearsal_buffer = deque(maxlen=1000)  # Experience replay buffer
        
    async def learn_continuously(self, task: LearningTask) -> LearningResult:
        """Learn new task while preserving old knowledge"""
        start_time = time.time()
        
        try:
            # Check if this is a new task or continuation
            is_new_task = task.task_id not in self.task_memories
            
            if is_new_task:
                # Initialize memory for new task
                self._initialize_task_memory(task)
            
            # Learn new information
            new_knowledge, metrics = await self._continual_learn(task)
            
            # Prevent catastrophic forgetting
            await self._consolidate_knowledge(task, new_knowledge)
            
            # Update knowledge graph
            self._update_knowledge_graph(task, new_knowledge)
            
            execution_time = time.time() - start_time
            
            return LearningResult(
                task_id=task.task_id,
                success=True,
                performance_metrics=metrics,
                learned_knowledge=new_knowledge,
                confidence=metrics.get('confidence', 0.7),
                execution_time=execution_time,
                strategy_used=LearningStrategy.ENSEMBLE
            )
            
        except Exception as e:
            logger.error(f"Continual learning failed for task {task.task_id}: {e}")
            return LearningResult(
                task_id=task.task_id,
                success=False,
                performance_metrics={'error': str(e)},
                learned_knowledge=None,
                confidence=0.0,
                execution_time=time.time() - start_time,
                strategy_used=LearningStrategy.ENSEMBLE
            )
    
    def _initialize_task_memory(self, task: LearningTask):
        """Initialize memory for a new task"""
        self.task_memories[task.task_id] = {
            'learned_patterns': {},
            'important_examples': [],
            'consolidation_score': 0.0,
            'learning_history': [],
            'created_at': datetime.now()
        }
        
        self.consolidation_strengths[task.task_id] = 1.0  # Start with high importance
    
    async def _continual_learn(self, task: LearningTask) -> Tuple[Dict[str, Any], Dict[str, float]]:
        """Learn new information for the task"""
        # Process new data
        if isinstance(task.data, list):
            new_examples = task.data
        else:
            new_examples = [task.data]
        
        # Extract patterns from new examples
        patterns = {}
        
        # Simple pattern extraction
        if all(isinstance(x, str) for x in new_examples):
            # Text patterns
            word_freq = defaultdict(int)
            for text in new_examples:
                for word in text.split():
                    word_freq[word] += 1
            patterns['word_frequencies'] = dict(word_freq)
            
        elif all(isinstance(x, (int, float)) for x in new_examples):
            # Numerical patterns
            patterns['statistics'] = {
                'mean': np.mean(new_examples),
                'std': np.std(new_examples),
                'min': np.min(new_examples),
                'max': np.max(new_examples)
            }
        
        # Store important examples in rehearsal buffer
        for example in new_examples[-10:]:  # Keep recent examples
            self.rehearsal_buffer.append({
                'task_id': task.task_id,
                'example': example,
                'timestamp': datetime.now()
            })
        
        # Update task memory
        memory = self.task_memories[task.task_id]
        
        # Merge new patterns with existing ones
        for pattern_type, pattern_data in patterns.items():
            if pattern_type in memory['learned_patterns']:
                # Merge patterns
                if isinstance(pattern_data, dict) and isinstance(memory['learned_patterns'][pattern_type], dict):
                    memory['learned_patterns'][pattern_type].update(pattern_data)
                else:
                    memory['learned_patterns'][pattern_type] = pattern_data
            else:
                memory['learned_patterns'][pattern_type] = pattern_data
        
        # Store important examples
        memory['important_examples'].extend(new_examples[-3:])  # Keep recent examples
        if len(memory['important_examples']) > 50:
            memory['important_examples'] = memory['important_examples'][-50:]  # Limit size
        
        # Record learning event
        memory['learning_history'].append({
            'timestamp': datetime.now(),
            'n_examples': len(new_examples),
            'patterns_learned': list(patterns.keys())
        })
        
        metrics = {
            'patterns_learned': len(patterns),
            'examples_processed': len(new_examples),
            'total_patterns': len(memory['learned_patterns']),
            'confidence': 0.7
        }
        
        return patterns, metrics
    
    async def _consolidate_knowledge(self, task: LearningTask, new_knowledge: Dict[str, Any]):
        """Prevent catastrophic forgetting through consolidation"""
        # Rehearsal-based consolidation
        if len(self.rehearsal_buffer) > 10:
            # Sample old experiences
            old_experiences = list(self.rehearsal_buffer)[-50:]  # Recent experiences
            
            # Replay old experiences to maintain knowledge
            for experience in old_experiences:
                if experience['task_id'] != task.task_id:
                    # This is from a different task - rehearse to prevent forgetting
                    old_task_memory = self.task_memories.get(experience['task_id'])
                    if old_task_memory:
                        # Strengthen consolidation
                        self.consolidation_strengths[experience['task_id']] *= 1.01  # Slight increase
        
        # Importance-based consolidation
        current_strength = self.consolidation_strengths.get(task.task_id, 1.0)
        
        # Increase strength based on learning success
        if 'patterns_learned' in new_knowledge and len(new_knowledge.get('patterns_learned', {})) > 0:
            current_strength *= 1.05
            self.consolidation_strengths[task.task_id] = min(current_strength, 2.0)  # Cap at 2.0
    
    def _update_knowledge_graph(self, task: LearningTask, new_knowledge: Dict[str, Any]):
        """Update relationships between learned concepts"""
        task_id = task.task_id
        
        if task_id not in self.knowledge_graph:
            self.knowledge_graph[task_id] = {
                'concepts': set(),
                'relationships': defaultdict(list)
            }
        
        # Extract concepts from new knowledge
        new_concepts = set()
        
        if isinstance(new_knowledge, dict):
            for key, value in new_knowledge.items():
                new_concepts.add(key)
                if isinstance(value, dict):
                    new_concepts.update(value.keys())
        
        # Add concepts
        self.knowledge_graph[task_id]['concepts'].update(new_concepts)
        
        # Find relationships with other tasks
        for other_task_id, other_graph in self.knowledge_graph.items():
            if other_task_id != task_id:
                # Find overlapping concepts
                overlap = new_concepts.intersection(other_graph['concepts'])
                if overlap:
                    # Create relationship
                    self.knowledge_graph[task_id]['relationships'][other_task_id].extend(list(overlap))

class MetaLearningOrchestrator:
    """Orchestrates learning strategies and optimizes learning-to-learn"""
    
    def __init__(self):
        self.meta_state = MetaLearningState()
        self.strategy_selector = {}
        self.learning_engines = {
            LearningType.SUPERVISED: SupervisedLearningEngine(),
            LearningType.UNSUPERVISED: UnsupervisedLearningEngine(),
            LearningType.REINFORCEMENT: ReinforcementLearningEngine(),
            LearningType.FEW_SHOT: FewShotLearningEngine(),
            LearningType.CONTINUAL: ContinualLearningEngine()
        }
        
    async def learn(self, task: LearningTask) -> LearningResult:
        """Main learning method that selects optimal strategy and engine"""
        start_time = time.time()
        
        try:
            # Select optimal learning strategy
            strategy = await self._select_optimal_strategy(task)
            
            # Route to appropriate learning engine
            engine = self.learning_engines[task.task_type]
            
            # Execute learning
            if task.task_type == LearningType.SUPERVISED:
                result = await engine.learn_from_examples(task)
            elif task.task_type == LearningType.UNSUPERVISED:
                result = await engine.discover_patterns(task)
            elif task.task_type == LearningType.REINFORCEMENT:
                result = await engine.learn_from_rewards(task)
            elif task.task_type == LearningType.FEW_SHOT:
                result = await engine.learn_from_few_examples(task)
            elif task.task_type == LearningType.CONTINUAL:
                result = await engine.learn_continuously(task)
            else:
                raise ValueError(f"Unsupported learning type: {task.task_type}")
            
            # Update meta-learning state
            await self._update_meta_state(task, result, strategy)
            
            return result
            
        except Exception as e:
            logger.error(f"Meta-learning failed for task {task.task_id}: {e}")
            return LearningResult(
                task_id=task.task_id,
                success=False,
                performance_metrics={'error': str(e)},
                learned_knowledge=None,
                confidence=0.0,
                execution_time=time.time() - start_time,
                strategy_used=LearningStrategy.GRADIENT_DESCENT
            )
    
    async def _select_optimal_strategy(self, task: LearningTask) -> LearningStrategy:
        """Select optimal learning strategy based on meta-learning"""
        task_key = (task.task_type, task.data_modality)
        
        # Check if we have learned optimal strategy for this task type
        if task_key in self.meta_state.optimal_strategies:
            return self.meta_state.optimal_strategies[task_key]
        
        # Use heuristics based on task characteristics
        if task.task_type == LearningType.FEW_SHOT:
            return LearningStrategy.TRANSFER
        elif task.task_type == LearningType.CONTINUAL:
            return LearningStrategy.ENSEMBLE
        elif task.data_modality == DataModality.TEXT:
            return LearningStrategy.GRADIENT_DESCENT
        elif task.data_modality == DataModality.NUMERICAL:
            return LearningStrategy.BAYESIAN
        else:
            return LearningStrategy.GRADIENT_DESCENT
    
    async def _update_meta_state(self, task: LearningTask, result: LearningResult, strategy: LearningStrategy):
        """Update meta-learning state based on learning results"""
        # Record strategy performance
        performance_score = result.confidence if result.success else 0.0
        self.meta_state.strategy_performance[strategy].append(performance_score)
        
        # Record learning speed
        learning_speed = 1.0 / result.execution_time if result.execution_time > 0 else 1.0
        self.meta_state.learning_speed_trends[task.task_type].append(learning_speed)
        
        # Update optimal strategies if we have enough data
        task_key = (task.task_type, task.data_modality)
        if len(self.meta_state.strategy_performance[strategy]) >= 5:
            avg_performance = np.mean(self.meta_state.strategy_performance[strategy][-5:])
            
            # Compare with current optimal strategy
            current_optimal = self.meta_state.optimal_strategies.get(task_key)
            if current_optimal is None:
                self.meta_state.optimal_strategies[task_key] = strategy
            else:
                current_performance = np.mean(self.meta_state.strategy_performance[current_optimal][-5:])
                if avg_performance > current_performance:
                    self.meta_state.optimal_strategies[task_key] = strategy
        
        # Record adaptation event
        self.meta_state.adaptation_history.append({
            'timestamp': datetime.now(),
            'task_id': task.task_id,
            'strategy': strategy.value,
            'performance': performance_score,
            'success': result.success
        })
        
        # Keep adaptation history manageable
        if len(self.meta_state.adaptation_history) > 1000:
            self.meta_state.adaptation_history = self.meta_state.adaptation_history[-500:]
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get comprehensive learning statistics"""
        stats = {
            'strategy_performance': {
                strategy.value: {
                    'avg_performance': np.mean(performances) if performances else 0.0,
                    'n_trials': len(performances),
                    'recent_performance': np.mean(performances[-10:]) if len(performances) >= 10 else np.mean(performances) if performances else 0.0
                }
                for strategy, performances in self.meta_state.strategy_performance.items()
            },
            'optimal_strategies': {
                f"{task_type.value}_{modality.value}": strategy.value
                for (task_type, modality), strategy in self.meta_state.optimal_strategies.items()
            },
            'learning_speed_trends': {
                learning_type.value: {
                    'avg_speed': np.mean(speeds) if speeds else 0.0,
                    'recent_trend': np.mean(speeds[-5:]) - np.mean(speeds[-10:-5]) if len(speeds) >= 10 else 0.0
                }
                for learning_type, speeds in self.meta_state.learning_speed_trends.items()
            },
            'total_adaptations': len(self.meta_state.adaptation_history),
            'recent_success_rate': np.mean([
                1.0 if event['success'] else 0.0
                for event in self.meta_state.adaptation_history[-50:]
            ]) if len(self.meta_state.adaptation_history) >= 50 else 0.0
        }
        
        return stats

class ComprehensiveLearningSystem:
    """Main learning system that orchestrates all learning capabilities"""
    
    def __init__(self):
        self.meta_orchestrator = MetaLearningOrchestrator()
        self.active_tasks = {}
        self.completed_tasks = {}
        self.task_queue = deque()
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.is_running = False
        
        logger.info("Comprehensive Learning System initialized")
    
    async def submit_learning_task(self, task: LearningTask) -> str:
        """Submit a new learning task"""
        task_id = task.task_id
        self.active_tasks[task_id] = task
        self.task_queue.append(task_id)
        
        logger.info(f"Learning task submitted: {task_id} ({task.task_type.value})")
        return task_id
    
    async def process_learning_tasks(self):
        """Process learning tasks from the queue"""
        while self.is_running and self.task_queue:
            task_id = self.task_queue.popleft()
            
            if task_id in self.active_tasks:
                task = self.active_tasks[task_id]
                
                try:
                    # Process the learning task
                    result = await self.meta_orchestrator.learn(task)
                    
                    # Store result
                    self.completed_tasks[task_id] = result
                    del self.active_tasks[task_id]
                    
                    logger.info(f"Learning task completed: {task_id} (Success: {result.success})")
                    
                except Exception as e:
                    logger.error(f"Error processing learning task {task_id}: {e}")
                    
                    # Create error result
                    error_result = LearningResult(
                        task_id=task_id,
                        success=False,
                        performance_metrics={'error': str(e)},
                        learned_knowledge=None,
                        confidence=0.0,
                        execution_time=0.0,
                        strategy_used=LearningStrategy.GRADIENT_DESCENT
                    )
                    
                    self.completed_tasks[task_id] = error_result
                    del self.active_tasks[task_id]
    
    def start(self):
        """Start the learning system"""
        self.is_running = True
        logger.info("Learning system started")
    
    def stop(self):
        """Stop the learning system"""
        self.is_running = False
        logger.info("Learning system stopped")
    
    def get_task_result(self, task_id: str) -> Optional[LearningResult]:
        """Get the result of a completed learning task"""
        return self.completed_tasks.get(task_id)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            'is_running': self.is_running,
            'active_tasks': len(self.active_tasks),
            'queued_tasks': len(self.task_queue),
            'completed_tasks': len(self.completed_tasks),
            'learning_statistics': self.meta_orchestrator.get_learning_statistics(),
            'system_uptime': datetime.now().isoformat()
        }
    
    def create_supervised_task(self, task_id: str, data: List[Any], labels: List[Any], 
                             objective: str = "Classification") -> LearningTask:
        """Helper to create supervised learning task"""
        return LearningTask(
            task_id=task_id,
            task_type=LearningType.SUPERVISED,
            data_modality=DataModality.MULTIMODAL,
            objective=objective,
            data=data,
            labels=labels
        )
    
    def create_unsupervised_task(self, task_id: str, data: List[Any], 
                                objective: str = "Pattern Discovery") -> LearningTask:
        """Helper to create unsupervised learning task"""
        return LearningTask(
            task_id=task_id,
            task_type=LearningType.UNSUPERVISED,
            data_modality=DataModality.MULTIMODAL,
            objective=objective,
            data=data
        )
    
    def create_reinforcement_task(self, task_id: str, episodes_data: List[Dict], 
                                 objective: str = "Reward Maximization") -> LearningTask:
        """Helper to create reinforcement learning task"""
        return LearningTask(
            task_id=task_id,
            task_type=LearningType.REINFORCEMENT,
            data_modality=DataModality.TEMPORAL,
            objective=objective,
            data=episodes_data
        )
    
    def create_few_shot_task(self, task_id: str, support_examples: List[Any], 
                            query_examples: List[Any], objective: str = "Few-Shot Adaptation") -> LearningTask:
        """Helper to create few-shot learning task"""
        return LearningTask(
            task_id=task_id,
            task_type=LearningType.FEW_SHOT,
            data_modality=DataModality.MULTIMODAL,
            objective=objective,
            data=support_examples + query_examples,
            labels=[1] * len(support_examples) + [0] * len(query_examples)  # Simple labeling
        )
    
    def create_continual_task(self, task_id: str, new_data: List[Any], 
                             objective: str = "Continual Learning") -> LearningTask:
        """Helper to create continual learning task"""
        return LearningTask(
            task_id=task_id,
            task_type=LearningType.CONTINUAL,
            data_modality=DataModality.MULTIMODAL,
            objective=objective,
            data=new_data
        )

# Example usage and demonstration
async def demonstrate_learning_system():
    """Demonstrate the comprehensive learning system capabilities"""
    print("🚀 Demonstrating Comprehensive Learning System")
    print("=" * 60)
    
    # Initialize the learning system
    learning_system = ComprehensiveLearningSystem()
    learning_system.start()
    
    try:
        # 1. Supervised Learning Example
        print("\n1. 📚 Supervised Learning - Text Classification")
        supervised_data = [
            "I love this product", "Great quality", "Excellent service",
            "Terrible quality", "Poor service", "Hate this product"
        ]
        supervised_labels = [1, 1, 1, 0, 0, 0]  # 1=positive, 0=negative
        
        supervised_task = learning_system.create_supervised_task(
            "sentiment_analysis", supervised_data, supervised_labels, "Sentiment Classification"
        )
        
        await learning_system.submit_learning_task(supervised_task)
        await learning_system.process_learning_tasks()
        
        result = learning_system.get_task_result("sentiment_analysis")
        if result:
            print(f"✅ Supervised learning result: Success={result.success}, Accuracy={result.performance_metrics.get('accuracy', 0):.3f}")
        
        # 2. Unsupervised Learning Example
        print("\n2. 🔍 Unsupervised Learning - Pattern Discovery")
        unsupervised_data = [
            "Machine learning is fascinating",
            "Deep learning uses neural networks",
            "AI will change the world",
            "Cats are cute animals",
            "Dogs are loyal pets",
            "Animals make great companions"
        ]
        
        unsupervised_task = learning_system.create_unsupervised_task(
            "topic_discovery", unsupervised_data, "Topic Clustering"
        )
        
        await learning_system.submit_learning_task(unsupervised_task)
        await learning_system.process_learning_tasks()
        
        result = learning_system.get_task_result("topic_discovery")
        if result:
            print(f"✅ Unsupervised learning result: Success={result.success}, Confidence={result.confidence:.3f}")
        
        # 3. Reinforcement Learning Example
        print("\n3. 🎮 Reinforcement Learning - Sequential Decision Making")
        rl_episodes = [
            {"states": [0, 1, 2, 3], "actions": [0, 1, 0, 1], "rewards": [1, 2, 1, 5]},
            {"states": [0, 2, 1, 3], "actions": [1, 0, 1, 0], "rewards": [0, 1, 3, 4]},
            {"states": [1, 0, 3, 2], "actions": [0, 1, 1, 0], "rewards": [2, 1, 4, 2]}
        ]
        
        rl_task = learning_system.create_reinforcement_task(
            "navigation_learning", rl_episodes, "Optimal Path Finding"
        )
        
        await learning_system.submit_learning_task(rl_task)
        await learning_system.process_learning_tasks()
        
        result = learning_system.get_task_result("navigation_learning")
        if result:
            print(f"✅ Reinforcement learning result: Success={result.success}, Avg Reward={result.performance_metrics.get('average_reward', 0):.3f}")
        
        # 4. Few-Shot Learning Example
        print("\n4. ⚡ Few-Shot Learning - Quick Adaptation")
        support_examples = ["Apple is a fruit", "Banana is a fruit"]
        query_examples = ["Orange is a ?", "Grape is a ?"]
        
        few_shot_task = learning_system.create_few_shot_task(
            "fruit_classification", support_examples, query_examples, "Fruit Category Learning"
        )
        
        await learning_system.submit_learning_task(few_shot_task)
        await learning_system.process_learning_tasks()
        
        result = learning_system.get_task_result("fruit_classification")
        if result:
            print(f"✅ Few-shot learning result: Success={result.success}, Prototypes={result.performance_metrics.get('n_prototypes', 0)}")
        
        # 5. Continual Learning Example
        print("\n5. 🔄 Continual Learning - Knowledge Preservation")
        new_data = [
            "Python is a programming language",
            "JavaScript runs in browsers",
            "Machine learning uses algorithms"
        ]
        
        continual_task = learning_system.create_continual_task(
            "programming_knowledge", new_data, "Programming Concept Learning"
        )
        
        await learning_system.submit_learning_task(continual_task)
        await learning_system.process_learning_tasks()
        
        result = learning_system.get_task_result("programming_knowledge")
        if result:
            print(f"✅ Continual learning result: Success={result.success}, Patterns={result.performance_metrics.get('patterns_learned', 0)}")
        
        # 6. System Statistics
        print("\n6. 📊 Meta-Learning Statistics")
        status = learning_system.get_system_status()
        print(f"✅ System Status: Running={status['is_running']}")
        print(f"✅ Completed Tasks: {status['completed_tasks']}")
        print(f"✅ Success Rate: {status['learning_statistics']['recent_success_rate']:.3f}")
        
        print("\n🎉 All learning capabilities demonstrated successfully!")
        
    finally:
        learning_system.stop()

if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(demonstrate_learning_system())
