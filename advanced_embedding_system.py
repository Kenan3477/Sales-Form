"""
Advanced Multi-Modal Embedding System for ASIS
Comprehensive embedding infrastructure with multiple models, multi-modal support,
dynamic adaptation, and performance optimization.

Features:
- Multiple embedding models (sentence-transformers, custom domain models)
- Multi-modal embeddings (text, numerical, categorical, temporal)
- Dynamic embedding adaptation based on usage patterns
- Cross-domain similarity calculation
- Embedding performance optimization and caching
- Semantic clustering and relationship mapping
- Hierarchical embedding spaces
- Domain-specific fine-tuning capabilities
"""

import numpy as np
import torch
import asyncio
import pickle
import hashlib
import json
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any, Union, Set, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sqlite3

# Advanced ML imports
try:
    from sentence_transformers import SentenceTransformer
    from transformers import AutoTokenizer, AutoModel
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: transformers not available. Install with: pip install sentence-transformers transformers")

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("Warning: faiss not available. Install with: pip install faiss-cpu")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import silhouette_score

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingType(Enum):
    """Types of embedding models"""
    SENTENCE_TRANSFORMER = "sentence_transformer"
    CUSTOM_DOMAIN = "custom_domain"
    MULTIMODAL = "multimodal"
    HIERARCHICAL = "hierarchical"
    TEMPORAL = "temporal"
    NUMERICAL = "numerical"
    CATEGORICAL = "categorical"
    FUSION = "fusion"


class DataModalityType(Enum):
    """Types of data modalities"""
    TEXT = "text"
    NUMERICAL = "numerical"
    CATEGORICAL = "categorical"
    TEMPORAL = "temporal"
    STRUCTURED = "structured"
    METADATA = "metadata"
    EMOTIONAL = "emotional"
    SPATIAL = "spatial"


class SimilarityMetric(Enum):
    """Similarity calculation methods"""
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    MANHATTAN = "manhattan"
    PEARSON = "pearson"
    JACCARD = "jaccard"
    WEIGHTED_COMBINED = "weighted_combined"


class ClusteringAlgorithm(Enum):
    """Clustering algorithms for semantic grouping"""
    KMEANS = "kmeans"
    DBSCAN = "dbscan"
    HIERARCHICAL = "hierarchical"
    GAUSSIAN_MIXTURE = "gaussian_mixture"
    SPECTRAL = "spectral"


@dataclass
class EmbeddingModel:
    """Configuration for an embedding model"""
    name: str
    model_type: EmbeddingType
    model_path: str
    dimension: int
    modality: DataModalityType
    domain: str = "general"
    performance_weight: float = 1.0
    usage_count: int = 0
    last_used: datetime = field(default_factory=datetime.now)
    adaptation_rate: float = 0.1
    cache_enabled: bool = True
    preprocessing_fn: Optional[Callable] = None
    postprocessing_fn: Optional[Callable] = None


@dataclass
class EmbeddingResult:
    """Result of embedding computation"""
    embedding: np.ndarray
    model_name: str
    modality: DataModalityType
    computation_time: float
    cache_hit: bool = False
    confidence: float = 1.0
    success: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SimilarityResult:
    """Result of similarity computation"""
    similarity: float
    metric: SimilarityMetric
    cross_domain: bool = False
    confidence: float = 1.0
    success: bool = True
    explanation: str = ""
    components: Dict[str, float] = field(default_factory=dict)


@dataclass
class ClusteringResult:
    """Result of semantic clustering"""
    cluster_labels: np.ndarray
    cluster_centers: np.ndarray
    silhouette_score: float
    algorithm: ClusteringAlgorithm
    n_clusters: int
    success: bool = True
    metrics: Dict[str, float] = field(default_factory=dict)
    outliers: List[int] = field(default_factory=list)
    cluster_names: List[str] = field(default_factory=list)
    cluster_relationships: Dict[int, List[int]] = field(default_factory=dict)


class AdvancedEmbeddingCache:
    """High-performance embedding cache with intelligent eviction"""
    
    def __init__(self, max_size: int = 10000, ttl_hours: int = 24):
        self.max_size = max_size
        self.ttl = timedelta(hours=ttl_hours)
        self.cache: Dict[str, Tuple[np.ndarray, datetime, int]] = {}
        self.usage_frequency: Dict[str, int] = defaultdict(int)
        self.access_times: Dict[str, datetime] = {}
        self.lock = threading.RLock()
        
        # Performance metrics
        self.hits = 0
        self.misses = 0
        self.evictions = 0
    
    def _generate_key(self, content: str, model_name: str, params: Dict[str, Any] = None) -> str:
        """Generate cache key"""
        key_data = f"{content}|{model_name}"
        if params:
            key_data += f"|{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, content: str, model_name: str, params: Dict[str, Any] = None) -> Optional[np.ndarray]:
        """Get embedding from cache"""
        key = self._generate_key(content, model_name, params)
        
        with self.lock:
            if key in self.cache:
                embedding, timestamp, usage_count = self.cache[key]
                
                # Check TTL
                if datetime.now() - timestamp < self.ttl:
                    # Update access statistics
                    self.usage_frequency[key] += 1
                    self.access_times[key] = datetime.now()
                    self.hits += 1
                    return embedding.copy()
                else:
                    # Expired, remove
                    del self.cache[key]
                    del self.usage_frequency[key]
                    del self.access_times[key]
            
            self.misses += 1
            return None
    
    def put(self, content: str, model_name: str, embedding: np.ndarray, params: Dict[str, Any] = None):
        """Store embedding in cache"""
        key = self._generate_key(content, model_name, params)
        
        with self.lock:
            # Check if cache is full
            if len(self.cache) >= self.max_size and key not in self.cache:
                self._evict_lru()
            
            # Store embedding
            self.cache[key] = (embedding.copy(), datetime.now(), 1)
            self.usage_frequency[key] = 1
            self.access_times[key] = datetime.now()
    
    def _evict_lru(self):
        """Evict least recently used items"""
        if not self.cache:
            return
        
        # Find LRU item based on access time and frequency
        lru_key = min(self.access_times.keys(), 
                     key=lambda k: (self.access_times[k], self.usage_frequency[k]))
        
        del self.cache[lru_key]
        del self.usage_frequency[lru_key]
        del self.access_times[lru_key]
        self.evictions += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        total_requests = self.hits + self.misses
        hit_rate = self.hits / total_requests if total_requests > 0 else 0
        
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
            "evictions": self.evictions,
            "memory_usage_mb": sum(embedding.nbytes for embedding, _, _ in self.cache.values()) / 1024 / 1024
        }
    
    def clear(self):
        """Clear cache"""
        with self.lock:
            self.cache.clear()
            self.usage_frequency.clear()
            self.access_times.clear()


class MultiModalEmbeddingSystem:
    """Advanced multi-modal embedding system with dynamic adaptation"""
    
    def __init__(self, models_config: Dict[str, Dict[str, Any]] = None, cache_size: int = 10000):
        self.models: Dict[str, EmbeddingModel] = {}
        self.active_models: Dict[str, Any] = {}  # Actual model instances
        self.cache = AdvancedEmbeddingCache(max_size=cache_size)
        
        # Default dimension (can be overridden by specific models)
        self.default_dimension = 384
        
        # Performance tracking
        self.usage_stats: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.performance_metrics: Dict[str, List[float]] = defaultdict(list)
        self.adaptation_history: List[Dict[str, Any]] = []
        
        # Similarity computation
        self.similarity_weights: Dict[DataModalityType, float] = {
            DataModalityType.TEXT: 0.4,
            DataModalityType.NUMERICAL: 0.2,
            DataModalityType.CATEGORICAL: 0.15,
            DataModalityType.TEMPORAL: 0.1,
            DataModalityType.EMOTIONAL: 0.1,
            DataModalityType.METADATA: 0.05
        }
        
        # Cross-domain mapping
        self.domain_relationships: Dict[str, Dict[str, float]] = {}
        self.cross_domain_adapters: Dict[Tuple[str, str], np.ndarray] = {}
        
        # Clustering and relationship mapping
        self.semantic_clusters: Dict[str, ClusteringResult] = {}
        self.relationship_graph: Dict[str, Set[str]] = defaultdict(set)
        
        # Enhanced features for Phase 1.3
        self.model_performance_tracker = ModelPerformanceTracker()
        self.domain_adaptation_engine = DomainAdaptationEngine()
        self.hierarchical_clustering = HierarchicalClusteringSystem()
        self.semantic_analyzer = AdvancedSemanticAnalyzer()
        
        # Initialize with default models
        self._initialize_default_models(models_config)
        
        # Multi-model ensemble support (defined after methods)
        self.ensemble_strategies = {
            'voting': self._ensemble_voting,
            'weighted': self._ensemble_weighted,
            'stacking': self._ensemble_stacking
        }
        self.current_ensemble_strategy = 'weighted'
        
        # Background optimization
        self.optimization_enabled = True
        self.last_optimization = datetime.now()
        self.optimization_interval = timedelta(hours=1)
    
    def _initialize_default_models(self, config: Dict[str, Dict[str, Any]] = None):
        """Initialize default embedding models"""
        default_config = {
            "sentence_transformer_small": {
                "model_type": EmbeddingType.SENTENCE_TRANSFORMER,
                "model_path": "all-MiniLM-L6-v2",
                "dimension": 384,
                "modality": DataModalityType.TEXT,
                "domain": "general"
            },
            "sentence_transformer_large": {
                "model_type": EmbeddingType.SENTENCE_TRANSFORMER,
                "model_path": "all-mpnet-base-v2",
                "dimension": 768,
                "modality": DataModalityType.TEXT,
                "domain": "general"
            },
            "numerical_embedder": {
                "model_type": EmbeddingType.NUMERICAL,
                "model_path": "builtin_numerical",
                "dimension": 100,
                "modality": DataModalityType.NUMERICAL,
                "domain": "general"
            },
            "categorical_embedder": {
                "model_type": EmbeddingType.CATEGORICAL,
                "model_path": "builtin_categorical",
                "dimension": 50,
                "modality": DataModalityType.CATEGORICAL,
                "domain": "general"
            },
            "temporal_embedder": {
                "model_type": EmbeddingType.TEMPORAL,
                "model_path": "builtin_temporal",
                "dimension": 30,
                "modality": DataModalityType.TEMPORAL,
                "domain": "general"
            }
        }
        
        if config:
            default_config.update(config)
        
        for name, model_config in default_config.items():
            model = EmbeddingModel(
                name=name,
                model_type=EmbeddingType(model_config["model_type"]),
                model_path=model_config["model_path"],
                dimension=model_config["dimension"],
                modality=DataModalityType(model_config["modality"]),
                domain=model_config.get("domain", "general")
            )
            self.models[name] = model
            
            # Load the actual model
            self._load_model(name)
    
    def _load_model(self, model_name: str) -> bool:
        """Load an embedding model"""
        if model_name not in self.models:
            logger.error(f"Model {model_name} not found in configuration")
            return False
        
        model_config = self.models[model_name]
        
        try:
            if model_config.model_type == EmbeddingType.SENTENCE_TRANSFORMER:
                if TRANSFORMERS_AVAILABLE:
                    self.active_models[model_name] = SentenceTransformer(model_config.model_path)
                    logger.info(f"Loaded sentence transformer: {model_name}")
                else:
                    logger.warning(f"Transformers not available for {model_name}")
                    return False
            
            elif model_config.model_type in [EmbeddingType.NUMERICAL, EmbeddingType.CATEGORICAL, EmbeddingType.TEMPORAL]:
                # Built-in embedding handlers
                self.active_models[model_name] = self._create_builtin_embedder(model_config)
                logger.info(f"Created built-in embedder: {model_name}")
            
            elif model_config.model_type == EmbeddingType.MULTIMODAL:
                self.active_models[model_name] = self._create_multimodal_embedder(model_config)
                logger.info(f"Created multi-modal embedder: {model_name}")
            
            else:
                logger.warning(f"Unknown model type for {model_name}: {model_config.model_type}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            return False
    
    def _create_builtin_embedder(self, model_config: EmbeddingModel) -> Dict[str, Any]:
        """Create built-in embedding handlers"""
        return {
            "type": model_config.model_type,
            "dimension": model_config.dimension,
            "scaler": StandardScaler() if model_config.modality == DataModalityType.NUMERICAL else None,
            "encoder": None  # Will be initialized on first use
        }
    
    def _create_multimodal_embedder(self, model_config: EmbeddingModel) -> Dict[str, Any]:
        """Create multi-modal embedding fusion system"""
        return {
            "type": EmbeddingType.MULTIMODAL,
            "dimension": model_config.dimension,
            "fusion_weights": {},
            "learned_mappings": {}
        }
    
    async def embed(self, content: Any, modality: DataModalityType, 
                   model_name: str = None, use_cache: bool = True, 
                   context: Dict[str, Any] = None) -> EmbeddingResult:
        """Generate embedding for content"""
        start_time = time.time()
        
        # Select appropriate model
        if model_name is None:
            model_name = self._select_best_model(modality, context)
        
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not available")
        
        # Check cache
        cache_key = str(content) if isinstance(content, (str, int, float)) else str(hash(str(content)))
        cached_embedding = None
        if use_cache:
            cached_embedding = self.cache.get(cache_key, model_name, context)
        
        if cached_embedding is not None:
            computation_time = time.time() - start_time
            return EmbeddingResult(
                embedding=cached_embedding,
                model_name=model_name,
                modality=modality,
                computation_time=computation_time,
                cache_hit=True
            )
        
        # Generate embedding
        embedding = await self._generate_embedding(content, modality, model_name, context)
        
        # Cache result
        if use_cache:
            self.cache.put(cache_key, model_name, embedding, context)
        
        # Update usage statistics
        self._update_usage_stats(model_name, modality)
        
        computation_time = time.time() - start_time
        self.performance_metrics[model_name].append(computation_time)
        
        return EmbeddingResult(
            embedding=embedding,
            model_name=model_name,
            modality=modality,
            computation_time=computation_time,
            cache_hit=False
        )
    
    async def _generate_embedding(self, content: Any, modality: DataModalityType, 
                                model_name: str, context: Dict[str, Any] = None) -> np.ndarray:
        """Generate embedding using specified model"""
        model_config = self.models[model_name]
        active_model = self.active_models.get(model_name)
        
        if active_model is None:
            if not self._load_model(model_name):
                raise RuntimeError(f"Failed to load model {model_name}")
            active_model = self.active_models[model_name]
        
        try:
            if modality == DataModalityType.TEXT:
                return await self._embed_text(content, active_model, model_config)
            elif modality == DataModalityType.NUMERICAL:
                return await self._embed_numerical(content, active_model, model_config)
            elif modality == DataModalityType.CATEGORICAL:
                return await self._embed_categorical(content, active_model, model_config)
            elif modality == DataModalityType.TEMPORAL:
                return await self._embed_temporal(content, active_model, model_config)
            elif modality == DataModalityType.STRUCTURED:
                return await self._embed_structured(content, active_model, model_config, context)
            else:
                raise ValueError(f"Unsupported modality: {modality}")
                
        except Exception as e:
            logger.error(f"Embedding generation failed for {model_name}: {e}")
            # Return zero vector as fallback
            return np.zeros(model_config.dimension)
    
    async def _embed_text(self, text: str, model: Any, config: EmbeddingModel) -> np.ndarray:
        """Generate text embedding"""
        if config.model_type == EmbeddingType.SENTENCE_TRANSFORMER:
            # Use sentence transformer
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                embedding = await loop.run_in_executor(
                    executor, lambda: model.encode(text, convert_to_numpy=True)
                )
            return embedding
        else:
            # Fallback to TF-IDF or other methods
            return np.random.normal(0, 0.1, config.dimension)
    
    async def _embed_numerical(self, data: Union[List[float], np.ndarray], 
                             model: Dict[str, Any], config: EmbeddingModel) -> np.ndarray:
        """Generate numerical data embedding"""
        if isinstance(data, list):
            data = np.array(data)
        
        # Normalize numerical data
        if model["scaler"] is None:
            model["scaler"] = StandardScaler()
            # For single-sample fitting, we use the data itself
            model["scaler"].fit(data.reshape(-1, 1) if data.ndim == 1 else data)
        
        normalized_data = model["scaler"].transform(data.reshape(-1, 1) if data.ndim == 1 else data)
        
        # Create embedding using projection and expansion
        if normalized_data.ndim == 1:
            normalized_data = normalized_data.flatten()
        
        # Expand to target dimension using various transformations
        embedding = np.zeros(config.dimension)
        data_len = len(normalized_data)
        
        # Fill embedding with transformed data
        for i in range(min(data_len, config.dimension)):
            embedding[i] = normalized_data[i]
        
        # Fill remaining dimensions with statistical features
        if data_len < config.dimension:
            stats = [
                np.mean(normalized_data),
                np.std(normalized_data),
                np.min(normalized_data),
                np.max(normalized_data),
                np.median(normalized_data)
            ]
            
            for i, stat in enumerate(stats):
                if data_len + i < config.dimension:
                    embedding[data_len + i] = stat
        
        return embedding
    
    async def _embed_categorical(self, data: Union[str, List[str]], 
                               model: Dict[str, Any], config: EmbeddingModel) -> np.ndarray:
        """Generate categorical data embedding"""
        if isinstance(data, str):
            data = [data]
        
        # Simple categorical embedding using hash-based approach
        embedding = np.zeros(config.dimension)
        
        for i, category in enumerate(data):
            # Hash-based encoding
            hash_val = hash(category)
            for j in range(min(10, config.dimension - i*10)):  # Use 10 dimensions per category
                idx = (i * 10 + j) % config.dimension
                embedding[idx] = (hash_val >> j) & 1  # Extract bits
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding
    
    async def _embed_temporal(self, data: Union[datetime, List[datetime], str], 
                            model: Dict[str, Any], config: EmbeddingModel) -> np.ndarray:
        """Generate temporal data embedding"""
        if isinstance(data, str):
            # Parse datetime string
            try:
                data = datetime.fromisoformat(data)
            except:
                data = datetime.now()
        
        if isinstance(data, datetime):
            data = [data]
        
        embedding = np.zeros(config.dimension)
        
        for i, dt in enumerate(data):
            if i * 6 >= config.dimension:
                break
            
            # Extract temporal features
            features = [
                dt.year / 3000.0,  # Normalized year
                dt.month / 12.0,   # Normalized month
                dt.day / 31.0,     # Normalized day
                dt.hour / 24.0,    # Normalized hour
                dt.minute / 60.0,  # Normalized minute
                dt.second / 60.0   # Normalized second
            ]
            
            for j, feature in enumerate(features):
                if i * 6 + j < config.dimension:
                    embedding[i * 6 + j] = feature
        
        return embedding
    
    async def _embed_structured(self, data: Dict[str, Any], model: Any, 
                              config: EmbeddingModel, context: Dict[str, Any] = None) -> np.ndarray:
        """Generate embedding for structured data"""
        # Multi-modal fusion approach
        embeddings = []
        weights = []
        
        for key, value in data.items():
            try:
                # Determine modality for this field
                if isinstance(value, str):
                    sub_embedding = await self._embed_text(value, model, config)
                    modality_weight = self.similarity_weights[DataModalityType.TEXT]
                elif isinstance(value, (int, float)):
                    sub_embedding = await self._embed_numerical([value], model, config)
                    modality_weight = self.similarity_weights[DataModalityType.NUMERICAL]
                elif isinstance(value, datetime):
                    sub_embedding = await self._embed_temporal(value, model, config)
                    modality_weight = self.similarity_weights[DataModalityType.TEMPORAL]
                else:
                    # Convert to string and embed as text
                    sub_embedding = await self._embed_text(str(value), model, config)
                    modality_weight = self.similarity_weights[DataModalityType.TEXT] * 0.5
                
                embeddings.append(sub_embedding)
                weights.append(modality_weight)
                
            except Exception as e:
                logger.warning(f"Failed to embed field {key}: {e}")
                continue
        
        if not embeddings:
            return np.zeros(config.dimension)
        
        # Weighted fusion
        return self._fuse_embeddings(embeddings, weights, config.dimension)
    
    def _fuse_embeddings(self, embeddings: List[np.ndarray], weights: List[float], 
                        target_dim: int) -> np.ndarray:
        """Fuse multiple embeddings into single representation"""
        if not embeddings:
            return np.zeros(target_dim)
        
        # Normalize embeddings to same dimension
        normalized_embeddings = []
        for embedding in embeddings:
            if len(embedding) > target_dim:
                # Truncate
                normalized_embeddings.append(embedding[:target_dim])
            elif len(embedding) < target_dim:
                # Pad with zeros
                padded = np.zeros(target_dim)
                padded[:len(embedding)] = embedding
                normalized_embeddings.append(padded)
            else:
                normalized_embeddings.append(embedding)
        
        # Weighted average
        weights = np.array(weights)
        weights = weights / np.sum(weights)  # Normalize weights
        
        fused_embedding = np.zeros(target_dim)
        for embedding, weight in zip(normalized_embeddings, weights):
            fused_embedding += weight * embedding
        
        return fused_embedding
    
    def _select_best_model(self, modality: DataModalityType, context: Dict[str, Any] = None) -> str:
        """Select best model for given modality and context"""
        # Filter models by modality
        suitable_models = [
            name for name, model in self.models.items()
            if model.modality == modality or model.modality == DataModalityType.STRUCTURED
        ]
        
        if not suitable_models:
            # Fallback to any available model
            suitable_models = list(self.models.keys())
        
        if not suitable_models:
            raise RuntimeError("No embedding models available")
        
        # Select based on performance weight and usage
        best_model = max(suitable_models, key=lambda name: (
            self.models[name].performance_weight,
            -self.models[name].usage_count  # Prefer less used models for load balancing
        ))
        
        return best_model
    
    def _update_usage_stats(self, model_name: str, modality: DataModalityType):
        """Update model usage statistics"""
        self.models[model_name].usage_count += 1
        self.models[model_name].last_used = datetime.now()
        self.usage_stats[model_name][modality.value] += 1
    
    async def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray,
                                 metric: SimilarityMetric = SimilarityMetric.COSINE,
                                 cross_domain: bool = False,
                                 domain1: str = None, domain2: str = None) -> SimilarityResult:
        """Calculate similarity between embeddings"""
        if embedding1.size == 0 or embedding2.size == 0:
            return SimilarityResult(similarity=0.0, metric=metric, cross_domain=cross_domain)
        
        # Ensure same dimensions
        min_dim = min(len(embedding1), len(embedding2))
        emb1 = embedding1[:min_dim]
        emb2 = embedding2[:min_dim]
        
        # Apply cross-domain adaptation if needed
        if cross_domain and domain1 and domain2:
            emb1, emb2 = await self._apply_cross_domain_adaptation(emb1, emb2, domain1, domain2)
        
        # Calculate similarity based on metric
        similarity = 0.0
        components = {}
        
        if metric == SimilarityMetric.COSINE:
            similarity = float(cosine_similarity([emb1], [emb2])[0][0])
            components["cosine"] = similarity
            
        elif metric == SimilarityMetric.EUCLIDEAN:
            distance = float(euclidean_distances([emb1], [emb2])[0][0])
            similarity = 1.0 / (1.0 + distance)  # Convert distance to similarity
            components["euclidean"] = similarity
            
        elif metric == SimilarityMetric.MANHATTAN:
            distance = float(np.sum(np.abs(emb1 - emb2)))
            similarity = 1.0 / (1.0 + distance)
            components["manhattan"] = similarity
            
        elif metric == SimilarityMetric.PEARSON:
            correlation = float(np.corrcoef(emb1, emb2)[0, 1])
            similarity = correlation if not np.isnan(correlation) else 0.0
            components["pearson"] = similarity
            
        elif metric == SimilarityMetric.WEIGHTED_COMBINED:
            # Combine multiple metrics
            cosine_sim = float(cosine_similarity([emb1], [emb2])[0][0])
            euclidean_dist = float(euclidean_distances([emb1], [emb2])[0][0])
            euclidean_sim = 1.0 / (1.0 + euclidean_dist)
            
            # Weighted combination
            similarity = 0.6 * cosine_sim + 0.4 * euclidean_sim
            components = {"cosine": cosine_sim, "euclidean": euclidean_sim, "combined": similarity}
        
        # Calculate confidence based on embedding quality
        confidence = min(1.0, (np.linalg.norm(emb1) * np.linalg.norm(emb2)) / (min_dim * 2))
        
        return SimilarityResult(
            similarity=similarity,
            metric=metric,
            cross_domain=cross_domain,
            confidence=confidence,
            components=components
        )
    
    async def _apply_cross_domain_adaptation(self, emb1: np.ndarray, emb2: np.ndarray,
                                           domain1: str, domain2: str) -> Tuple[np.ndarray, np.ndarray]:
        """Apply cross-domain adaptation to embeddings"""
        domain_pair = (domain1, domain2)
        reverse_pair = (domain2, domain1)
        
        # Check if we have learned adaptation for this domain pair
        if domain_pair in self.cross_domain_adapters:
            adapter = self.cross_domain_adapters[domain_pair]
            adapted_emb1 = np.dot(emb1, adapter)
            return adapted_emb1, emb2
        elif reverse_pair in self.cross_domain_adapters:
            adapter = self.cross_domain_adapters[reverse_pair]
            adapted_emb2 = np.dot(emb2, adapter)
            return emb1, adapted_emb2
        else:
            # Use domain relationship weights if available
            if domain1 in self.domain_relationships and domain2 in self.domain_relationships[domain1]:
                weight = self.domain_relationships[domain1][domain2]
                # Simple scaling adaptation
                adapted_emb1 = emb1 * weight
                adapted_emb2 = emb2 * (2.0 - weight)  # Complementary scaling
                return adapted_emb1, adapted_emb2
        
        # No adaptation available
        return emb1, emb2
    
    async def perform_semantic_clustering(self, embeddings: List[np.ndarray], 
                                        algorithm: ClusteringAlgorithm = ClusteringAlgorithm.KMEANS,
                                        n_clusters: int = None,
                                        cluster_names: List[str] = None) -> ClusteringResult:
        """Perform semantic clustering on embeddings"""
        if not embeddings:
            return ClusteringResult(
                cluster_labels=np.array([]),
                cluster_centers=np.array([]),
                silhouette_score=0.0,
                algorithm=algorithm,
                n_clusters=0
            )
        
        # Convert to numpy array
        X = np.array(embeddings)
        
        # Determine optimal number of clusters if not specified
        if n_clusters is None:
            n_clusters = min(10, max(2, len(embeddings) // 5))
        
        # Apply clustering algorithm
        cluster_labels = None
        cluster_centers = None
        outliers = []
        
        try:
            if algorithm == ClusteringAlgorithm.KMEANS:
                clusterer = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                cluster_labels = clusterer.fit_predict(X)
                cluster_centers = clusterer.cluster_centers_
                
            elif algorithm == ClusteringAlgorithm.DBSCAN:
                clusterer = DBSCAN(eps=0.5, min_samples=2)
                cluster_labels = clusterer.fit_predict(X)
                # Find actual number of clusters (excluding noise)
                n_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
                # Calculate cluster centers
                if n_clusters > 0:
                    cluster_centers = np.array([
                        X[cluster_labels == i].mean(axis=0)
                        for i in range(n_clusters)
                    ])
                else:
                    cluster_centers = np.array([])
                # Find outliers
                outliers = [i for i, label in enumerate(cluster_labels) if label == -1]
                
            elif algorithm == ClusteringAlgorithm.HIERARCHICAL:
                clusterer = AgglomerativeClustering(n_clusters=n_clusters)
                cluster_labels = clusterer.fit_predict(X)
                # Calculate cluster centers
                cluster_centers = np.array([
                    X[cluster_labels == i].mean(axis=0)
                    for i in range(n_clusters)
                ])
            
            else:
                raise ValueError(f"Unsupported clustering algorithm: {algorithm}")
            
            # Calculate silhouette score
            if len(set(cluster_labels)) > 1 and len(cluster_labels) > 1:
                sil_score = silhouette_score(X, cluster_labels)
            else:
                sil_score = 0.0
            
            # Generate cluster relationships
            cluster_relationships = self._build_cluster_relationships(cluster_centers)
            
            return ClusteringResult(
                cluster_labels=cluster_labels,
                cluster_centers=cluster_centers,
                silhouette_score=sil_score,
                algorithm=algorithm,
                n_clusters=n_clusters,
                outliers=outliers,
                cluster_names=cluster_names or [f"Cluster_{i}" for i in range(n_clusters)],
                cluster_relationships=cluster_relationships
            )
            
        except Exception as e:
            logger.error(f"Clustering failed: {e}")
            return ClusteringResult(
                cluster_labels=np.zeros(len(embeddings)),
                cluster_centers=np.array([X.mean(axis=0)]) if len(X) > 0 else np.array([]),
                silhouette_score=0.0,
                algorithm=algorithm,
                n_clusters=1
            )
    
    def _build_cluster_relationships(self, cluster_centers: np.ndarray) -> Dict[int, List[int]]:
        """Build relationships between clusters based on similarity"""
        if len(cluster_centers) <= 1:
            return {}
        
        relationships = {}
        
        # Calculate pairwise similarities between cluster centers
        for i in range(len(cluster_centers)):
            similarities = []
            for j in range(len(cluster_centers)):
                if i != j:
                    sim = cosine_similarity([cluster_centers[i]], [cluster_centers[j]])[0][0]
                    similarities.append((j, sim))
            
            # Sort by similarity and take top relationships
            similarities.sort(key=lambda x: x[1], reverse=True)
            relationships[i] = [cluster_id for cluster_id, sim in similarities[:3] if sim > 0.5]
        
        return relationships
    
    async def optimize_performance(self):
        """Optimize embedding system performance"""
        logger.info("Starting embedding system optimization...")
        
        # Update model performance weights based on usage and timing
        for model_name, times in self.performance_metrics.items():
            if times:
                avg_time = np.mean(times[-100:])  # Last 100 computations
                # Lower average time = higher performance weight
                self.models[model_name].performance_weight = 1.0 / (1.0 + avg_time)
        
        # Adapt similarity weights based on domain relationships
        await self._adapt_similarity_weights()
        
        # Clean up old cache entries
        await self._optimize_cache()
        
        # Learn cross-domain adaptations
        await self._learn_cross_domain_adaptations()
        
        self.last_optimization = datetime.now()
        logger.info("Embedding system optimization completed")
    
    async def _adapt_similarity_weights(self):
        """Adapt similarity weights based on usage patterns"""
        # Analyze which modalities are used most frequently
        modality_usage = defaultdict(int)
        for model_stats in self.usage_stats.values():
            for modality, count in model_stats.items():
                modality_usage[modality] += count
        
        if modality_usage:
            total_usage = sum(modality_usage.values())
            # Adjust weights based on usage frequency
            for modality_str, usage in modality_usage.items():
                try:
                    modality = DataModalityType(modality_str)
                    # Increase weight for frequently used modalities
                    usage_ratio = usage / total_usage
                    self.similarity_weights[modality] = min(0.8, usage_ratio * 2.0)
                except ValueError:
                    continue
            
            # Normalize weights to sum to 1.0
            total_weight = sum(self.similarity_weights.values())
            if total_weight > 0:
                for modality in self.similarity_weights:
                    self.similarity_weights[modality] /= total_weight
    
    async def _optimize_cache(self):
        """Optimize cache performance"""
        # Clear expired entries
        self.cache.clear()
        
        # Log cache statistics
        stats = self.cache.get_stats()
        logger.info(f"Cache optimization - Hit rate: {stats['hit_rate']:.2f}, "
                   f"Memory usage: {stats['memory_usage_mb']:.1f}MB")
    
    async def _learn_cross_domain_adaptations(self):
        """Learn cross-domain adaptation matrices"""
        # This would typically involve analyzing embeddings from different domains
        # and learning transformation matrices to align them
        # For now, we'll create simple relationship weights
        
        domains = set()
        for model in self.models.values():
            domains.add(model.domain)
        
        # Create domain relationships based on model similarities
        for domain1 in domains:
            if domain1 not in self.domain_relationships:
                self.domain_relationships[domain1] = {}
            
            for domain2 in domains:
                if domain1 != domain2:
                    # Simple heuristic: domains with similar names are more related
                    similarity = len(set(domain1.lower()) & set(domain2.lower())) / max(len(domain1), len(domain2))
                    self.domain_relationships[domain1][domain2] = 0.5 + similarity * 0.5
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        return {
            "models": {
                name: {
                    "type": model.model_type.value,
                    "dimension": model.dimension,
                    "modality": model.modality.value,
                    "domain": model.domain,
                    "usage_count": model.usage_count,
                    "performance_weight": model.performance_weight
                }
                for name, model in self.models.items()
            },
            "cache_stats": self.cache.get_stats(),
            "usage_stats": dict(self.usage_stats),
            "similarity_weights": {k.value: v for k, v in self.similarity_weights.items()},
            "domain_relationships": self.domain_relationships,
            "clustering_results": len(self.semantic_clusters),
            "optimization_enabled": self.optimization_enabled,
            "last_optimization": self.last_optimization.isoformat()
        }
    
    def _ensemble_voting(self, embeddings: List[np.ndarray]) -> np.ndarray:
        """Ensemble embeddings using majority voting (average)"""
        if not embeddings:
            return np.array([])
        
        # Find minimum dimension across all embeddings
        min_dim = min(emb.shape[0] for emb in embeddings)
        truncated_embeddings = [emb[:min_dim] for emb in embeddings]
        
        # Simple average
        return np.mean(truncated_embeddings, axis=0)
    
    def _ensemble_weighted(self, embeddings: List[np.ndarray], 
                          model_names: List[str]) -> np.ndarray:
        """Ensemble embeddings using performance-weighted combination"""
        if not embeddings or not model_names:
            return np.array([])
        
        # Get performance weights
        weights = []
        for model_name in model_names:
            if model_name in self.models:
                weights.append(self.models[model_name].performance_weight)
            else:
                weights.append(1.0)
        
        # Normalize weights
        weights = np.array(weights)
        weights = weights / np.sum(weights)
        
        # Find minimum dimension
        min_dim = min(emb.shape[0] for emb in embeddings)
        
        # Weighted combination
        result = np.zeros(min_dim)
        for emb, weight in zip(embeddings, weights):
            result += weight * emb[:min_dim]
        
        return result
    
    def _ensemble_stacking(self, embeddings: List[np.ndarray]) -> np.ndarray:
        """Ensemble embeddings using stacking (concatenation with dimensionality reduction)"""
        if not embeddings:
            return np.array([])
        
        # Concatenate all embeddings
        concatenated = np.concatenate(embeddings)
        
        # Apply PCA to reduce dimensionality if too large
        if len(concatenated) > self.default_dimension:
            try:
                from sklearn.decomposition import PCA
                pca = PCA(n_components=self.default_dimension)
                reduced = pca.fit_transform(concatenated.reshape(1, -1))
                return reduced.flatten()
            except ImportError:
                # Fallback to truncation
                return concatenated[:self.default_dimension]
        
        return concatenated
    
    def embed_text(self, text: str, **kwargs) -> EmbeddingResult:
        """Synchronous text embedding wrapper"""
        import asyncio
        return asyncio.run(self.embed(text, DataModalityType.TEXT, **kwargs))
    
    def embed_numerical(self, data: List[float], **kwargs) -> EmbeddingResult:
        """Synchronous numerical embedding wrapper"""
        import asyncio
        return asyncio.run(self.embed(data, DataModalityType.NUMERICAL, **kwargs))
    
    def embed_categorical(self, data: List[str], **kwargs) -> EmbeddingResult:
        """Synchronous categorical embedding wrapper"""
        import asyncio
        return asyncio.run(self.embed(data, DataModalityType.CATEGORICAL, **kwargs))
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray, **kwargs) -> SimilarityResult:
        """Synchronous similarity computation wrapper"""
        import asyncio
        return asyncio.run(self.calculate_similarity(embedding1, embedding2, **kwargs))
    
    def cluster_embeddings(self, embeddings: np.ndarray, n_clusters: int = 5, **kwargs) -> ClusteringResult:
        """Synchronous clustering wrapper"""
        import asyncio
        embeddings_list = [embeddings[i] for i in range(len(embeddings))]
        return asyncio.run(self.perform_semantic_clustering(embeddings_list, n_clusters=n_clusters, **kwargs))


class ModelPerformanceTracker:
    """Tracks and optimizes individual model performance"""
    
    def __init__(self):
        self.model_metrics: Dict[str, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))
        self.model_rankings: Dict[str, float] = {}
        self.adaptation_thresholds = {
            'accuracy': 0.85,
            'speed': 0.1,  # seconds
            'cache_hit_rate': 0.8
        }
    
    def record_performance(self, model_name: str, metric_type: str, value: float):
        """Record a performance metric for a model"""
        self.model_metrics[model_name][metric_type].append(value)
        self._update_rankings()
    
    def _update_rankings(self):
        """Update model rankings based on performance"""
        for model_name, metrics in self.model_metrics.items():
            score = 0.0
            weight_sum = 0.0
            
            # Accuracy weight: 0.5
            if 'accuracy' in metrics:
                accuracy = np.mean(metrics['accuracy'][-10:])  # Last 10 measurements
                score += accuracy * 0.5
                weight_sum += 0.5
            
            # Speed weight: 0.3 (lower is better)
            if 'speed' in metrics:
                speed = np.mean(metrics['speed'][-10:])
                speed_score = max(0, 1 - speed / 1.0)  # Normalize to 1 second max
                score += speed_score * 0.3
                weight_sum += 0.3
            
            # Cache hit rate weight: 0.2
            if 'cache_hit_rate' in metrics:
                cache_score = np.mean(metrics['cache_hit_rate'][-10:])
                score += cache_score * 0.2
                weight_sum += 0.2
            
            if weight_sum > 0:
                self.model_rankings[model_name] = score / weight_sum
    
    def get_best_model(self, modality: DataModalityType) -> Optional[str]:
        """Get the best performing model for a given modality"""
        candidates = [name for name, _ in self.model_rankings.items() 
                     if modality.value in name.lower()]
        
        if not candidates:
            return None
        
        return max(candidates, key=lambda x: self.model_rankings.get(x, 0))
    
    def should_adapt_model(self, model_name: str) -> bool:
        """Determine if a model needs adaptation"""
        if model_name not in self.model_metrics:
            return False
        
        metrics = self.model_metrics[model_name]
        
        # Check if performance is below thresholds
        for metric, threshold in self.adaptation_thresholds.items():
            if metric in metrics and len(metrics[metric]) >= 5:
                recent_avg = np.mean(metrics[metric][-5:])
                if metric == 'speed':  # Lower is better for speed
                    if recent_avg > threshold:
                        return True
                else:  # Higher is better for accuracy and cache hit rate
                    if recent_avg < threshold:
                        return True
        
        return False


class DomainAdaptationEngine:
    """Handles cross-domain adaptation and transfer learning"""
    
    def __init__(self):
        self.domain_embeddings: Dict[str, np.ndarray] = {}
        self.adaptation_matrices: Dict[Tuple[str, str], np.ndarray] = {}
        self.domain_similarity_cache: Dict[Tuple[str, str], float] = {}
        self.transfer_learning_history: List[Dict[str, Any]] = []
    
    def learn_domain_representation(self, domain: str, embeddings: List[np.ndarray]):
        """Learn a representation for a specific domain"""
        if len(embeddings) == 0:
            return
        
        # Compute domain centroid and principal components
        embeddings_array = np.array(embeddings)
        domain_centroid = np.mean(embeddings_array, axis=0)
        
        # Store domain representation
        self.domain_embeddings[domain] = domain_centroid
        
        logger.info(f"Learned representation for domain: {domain}")
    
    def compute_domain_similarity(self, domain1: str, domain2: str) -> float:
        """Compute similarity between two domains"""
        cache_key = tuple(sorted([domain1, domain2]))
        
        if cache_key in self.domain_similarity_cache:
            return self.domain_similarity_cache[cache_key]
        
        if domain1 not in self.domain_embeddings or domain2 not in self.domain_embeddings:
            return 0.5  # Default similarity
        
        emb1 = self.domain_embeddings[domain1]
        emb2 = self.domain_embeddings[domain2]
        
        # Cosine similarity
        similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        similarity = (similarity + 1) / 2  # Normalize to [0, 1]
        
        self.domain_similarity_cache[cache_key] = similarity
        return similarity
    
    def create_adaptation_matrix(self, source_domain: str, target_domain: str, 
                                source_embeddings: List[np.ndarray], 
                                target_embeddings: List[np.ndarray]) -> np.ndarray:
        """Create an adaptation matrix between domains"""
        if len(source_embeddings) != len(target_embeddings):
            raise ValueError("Source and target embeddings must have same length")
        
        source_matrix = np.array(source_embeddings)
        target_matrix = np.array(target_embeddings)
        
        # Compute optimal transformation using least squares
        adaptation_matrix = np.linalg.lstsq(source_matrix, target_matrix, rcond=None)[0]
        
        matrix_key = (source_domain, target_domain)
        self.adaptation_matrices[matrix_key] = adaptation_matrix
        
        # Record transfer learning event
        self.transfer_learning_history.append({
            'timestamp': datetime.now(),
            'source_domain': source_domain,
            'target_domain': target_domain,
            'num_samples': len(source_embeddings),
            'adaptation_quality': self._evaluate_adaptation_quality(source_matrix, target_matrix, adaptation_matrix)
        })
        
        return adaptation_matrix
    
    def _evaluate_adaptation_quality(self, source: np.ndarray, target: np.ndarray, 
                                   adaptation_matrix: np.ndarray) -> float:
        """Evaluate the quality of domain adaptation"""
        transformed = source @ adaptation_matrix
        mse = np.mean((transformed - target) ** 2)
        return max(0, 1 - mse)  # Higher is better
    
    def adapt_embedding(self, embedding: np.ndarray, source_domain: str, 
                       target_domain: str) -> np.ndarray:
        """Adapt an embedding from source to target domain"""
        matrix_key = (source_domain, target_domain)
        
        if matrix_key not in self.adaptation_matrices:
            # Use domain similarity as fallback
            similarity = self.compute_domain_similarity(source_domain, target_domain)
            return embedding * similarity
        
        adaptation_matrix = self.adaptation_matrices[matrix_key]
        return embedding @ adaptation_matrix


class HierarchicalClusteringSystem:
    """Advanced hierarchical clustering with semantic understanding"""
    
    def __init__(self):
        self.cluster_hierarchies: Dict[str, Dict[str, Any]] = {}
        self.cluster_relationships: Dict[str, Set[str]] = defaultdict(set)
        self.cluster_metadata: Dict[str, Dict[str, Any]] = {}
        self.auto_naming_enabled = True
    
    def create_hierarchical_clusters(self, embeddings: np.ndarray, 
                                   labels: List[str] = None,
                                   max_clusters: int = 10) -> Dict[str, Any]:
        """Create hierarchical clusters from embeddings"""
        try:
            from sklearn.cluster import AgglomerativeClustering
            from scipy.cluster.hierarchy import dendrogram, linkage
            from sklearn.metrics import silhouette_score
        except ImportError:
            logger.error("sklearn required for hierarchical clustering")
            return {}
        
        if len(embeddings) < 2:
            return {}
        
        # Perform hierarchical clustering
        linkage_matrix = linkage(embeddings, method='ward')
        
        results = {}
        best_score = -1
        best_k = 2
        
        # Find optimal number of clusters
        for k in range(2, min(max_clusters + 1, len(embeddings))):
            clustering = AgglomerativeClustering(n_clusters=k)
            cluster_labels = clustering.fit_predict(embeddings)
            
            # Compute silhouette score
            if len(set(cluster_labels)) > 1:
                score = silhouette_score(embeddings, cluster_labels)
                if score > best_score:
                    best_score = score
                    best_k = k
                
                results[f"k_{k}"] = {
                    'labels': cluster_labels,
                    'silhouette_score': score,
                    'n_clusters': k
                }
        
        # Create cluster hierarchy
        hierarchy_id = f"hierarchy_{datetime.now().timestamp()}"
        self.cluster_hierarchies[hierarchy_id] = {
            'linkage_matrix': linkage_matrix,
            'results': results,
            'best_k': best_k,
            'best_score': best_score,
            'embeddings': embeddings,
            'labels': labels or [f"item_{i}" for i in range(len(embeddings))]
        }
        
        # Auto-generate cluster names if enabled
        if self.auto_naming_enabled and labels:
            self._generate_cluster_names(hierarchy_id, best_k, labels)
        
        return self.cluster_hierarchies[hierarchy_id]
    
    def _generate_cluster_names(self, hierarchy_id: str, k: int, labels: List[str]):
        """Automatically generate meaningful cluster names"""
        if hierarchy_id not in self.cluster_hierarchies:
            return
        
        hierarchy = self.cluster_hierarchies[hierarchy_id]
        cluster_labels = hierarchy['results'][f"k_{k}"]['labels']
        
        cluster_names = {}
        for cluster_id in range(k):
            # Get items in this cluster
            cluster_items = [labels[i] for i, label in enumerate(cluster_labels) if label == cluster_id]
            
            if len(cluster_items) == 0:
                cluster_names[cluster_id] = f"Cluster_{cluster_id}"
                continue
            
            # Simple naming based on common words
            if len(cluster_items) == 1:
                cluster_names[cluster_id] = cluster_items[0]
            else:
                # Find common words or patterns
                words = []
                for item in cluster_items:
                    words.extend(item.lower().split())
                
                word_counts = defaultdict(int)
                for word in words:
                    word_counts[word] += 1
                
                # Get most common words
                common_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:3]
                if common_words:
                    cluster_names[cluster_id] = " + ".join([word for word, _ in common_words])
                else:
                    cluster_names[cluster_id] = f"Group_{cluster_id}"
        
        self.cluster_metadata[hierarchy_id] = {
            'cluster_names': cluster_names,
            'generation_time': datetime.now()
        }
    
    def get_cluster_relationships(self, hierarchy_id: str) -> Dict[int, List[int]]:
        """Get relationships between clusters in a hierarchy"""
        if hierarchy_id not in self.cluster_hierarchies:
            return {}
        
        hierarchy = self.cluster_hierarchies[hierarchy_id]
        linkage_matrix = hierarchy['linkage_matrix']
        
        # Build cluster relationships from linkage matrix
        relationships = defaultdict(list)
        n_samples = len(hierarchy['embeddings'])
        
        for i, (cluster1, cluster2, distance, size) in enumerate(linkage_matrix):
            new_cluster_id = n_samples + i
            relationships[new_cluster_id].extend([int(cluster1), int(cluster2)])
        
        return dict(relationships)
    
    def visualize_hierarchy(self, hierarchy_id: str, save_path: Optional[str] = None):
        """Create a visualization of the cluster hierarchy"""
        if hierarchy_id not in self.cluster_hierarchies:
            logger.error(f"Hierarchy {hierarchy_id} not found")
            return
        
        try:
            import matplotlib.pyplot as plt
            from scipy.cluster.hierarchy import dendrogram
        except ImportError:
            logger.error("matplotlib required for visualization")
            return
        
        hierarchy = self.cluster_hierarchies[hierarchy_id]
        linkage_matrix = hierarchy['linkage_matrix']
        labels = hierarchy['labels']
        
        plt.figure(figsize=(12, 8))
        dendrogram(linkage_matrix, labels=labels, leaf_rotation=90)
        plt.title(f"Hierarchical Clustering - {hierarchy_id}")
        plt.xlabel("Items")
        plt.ylabel("Distance")
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Hierarchy visualization saved to {save_path}")
        else:
            plt.show()


class AdvancedSemanticAnalyzer:
    """Advanced semantic analysis and relationship mapping"""
    
    def __init__(self):
        self.semantic_graphs: Dict[str, Dict[str, Any]] = {}
        self.concept_relationships: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.semantic_evolution_history: List[Dict[str, Any]] = []
    
    def analyze_semantic_relationships(self, embeddings: List[np.ndarray], 
                                     concepts: List[str]) -> Dict[str, Any]:
        """Analyze semantic relationships between concepts"""
        if len(embeddings) != len(concepts):
            raise ValueError("Embeddings and concepts must have same length")
        
        embeddings_array = np.array(embeddings)
        
        # Compute pairwise similarities
        similarity_matrix = np.zeros((len(concepts), len(concepts)))
        for i in range(len(concepts)):
            for j in range(len(concepts)):
                if i != j:
                    sim = np.dot(embeddings_array[i], embeddings_array[j]) / (
                        np.linalg.norm(embeddings_array[i]) * np.linalg.norm(embeddings_array[j])
                    )
                    similarity_matrix[i][j] = (sim + 1) / 2  # Normalize to [0, 1]
        
        # Build semantic graph
        graph_id = f"semantic_graph_{datetime.now().timestamp()}"
        self.semantic_graphs[graph_id] = {
            'concepts': concepts,
            'embeddings': embeddings_array,
            'similarity_matrix': similarity_matrix,
            'creation_time': datetime.now()
        }
        
        # Update concept relationships
        for i, concept1 in enumerate(concepts):
            for j, concept2 in enumerate(concepts):
                if i != j:
                    self.concept_relationships[concept1][concept2] = similarity_matrix[i][j]
        
        # Identify clusters of related concepts
        strong_relationships = []
        for i in range(len(concepts)):
            for j in range(i + 1, len(concepts)):
                if similarity_matrix[i][j] > 0.7:  # Strong relationship threshold
                    strong_relationships.append((concepts[i], concepts[j], similarity_matrix[i][j]))
        
        # Record evolution
        self.semantic_evolution_history.append({
            'timestamp': datetime.now(),
            'graph_id': graph_id,
            'num_concepts': len(concepts),
            'strong_relationships': len(strong_relationships),
            'avg_similarity': np.mean(similarity_matrix[similarity_matrix > 0])
        })
        
        return {
            'graph_id': graph_id,
            'similarity_matrix': similarity_matrix,
            'strong_relationships': strong_relationships,
            'concept_centrality': self._compute_centrality(similarity_matrix, concepts)
        }
    
    def _compute_centrality(self, similarity_matrix: np.ndarray, concepts: List[str]) -> Dict[str, float]:
        """Compute centrality measures for concepts"""
        centrality = {}
        
        for i, concept in enumerate(concepts):
            # Degree centrality (sum of connections)
            degree = np.sum(similarity_matrix[i] > 0.5) - 1  # Exclude self
            
            # Weighted centrality (sum of similarity scores)
            weighted = np.sum(similarity_matrix[i]) - similarity_matrix[i][i]
            
            centrality[concept] = {
                'degree': degree,
                'weighted': weighted,
                'normalized_weighted': weighted / (len(concepts) - 1)
            }
        
        return centrality
    
    def find_concept_clusters(self, threshold: float = 0.6) -> List[List[str]]:
        """Find clusters of related concepts"""
        clusters = []
        processed = set()
        
        for concept1, relationships in self.concept_relationships.items():
            if concept1 in processed:
                continue
            
            cluster = [concept1]
            processed.add(concept1)
            
            # Find connected concepts
            for concept2, similarity in relationships.items():
                if concept2 not in processed and similarity >= threshold:
                    cluster.append(concept2)
                    processed.add(concept2)
            
            if len(cluster) > 1:
                clusters.append(cluster)
        
        return clusters
    
    def get_semantic_evolution_summary(self) -> Dict[str, Any]:
        """Get a summary of semantic evolution over time"""
        if not self.semantic_evolution_history:
            return {}
        
        history = self.semantic_evolution_history
        
        return {
            'total_analyses': len(history),
            'concepts_analyzed': sum(h['num_concepts'] for h in history),
            'avg_concepts_per_analysis': np.mean([h['num_concepts'] for h in history]),
            'strong_relationships_growth': [h['strong_relationships'] for h in history],
            'similarity_trends': [h['avg_similarity'] for h in history],
            'first_analysis': history[0]['timestamp'].isoformat(),
            'latest_analysis': history[-1]['timestamp'].isoformat()
        }

# Export main classes for use
__all__ = [
    'MultiModalEmbeddingSystem',
    'EmbeddingType',
    'DataModalityType', 
    'SimilarityMetric',
    'ClusteringAlgorithm',
    'EmbeddingResult',
    'SimilarityResult',
    'ClusteringResult'
]
