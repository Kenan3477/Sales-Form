"""
Enhanced Memory Network System for Advanced Synthetic Intelligence
Multi-modal, hierarchical memory with temporal dynamics and emotional tagging

Features:
- Multi-modal memory storage (text, structured data, metadata)
- Hierarchical organization (episodic, semantic, procedural)
- Temporal decay and reinforcement mechanisms
- Emotional memory tagging
- Advanced multi-modal embedding system with dynamic adaptation
- Memory consolidation algorithms
- Database integration for persistence
- Cross-domain similarity and clustering
"""

import numpy as np
import sqlite3
import json
import pickle
import hashlib
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any, Union, Set
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict, deque
import threading
from concurrent.futures import ThreadPoolExecutor
import time

# Import the advanced embedding system
try:
    from advanced_embedding_system import (
        MultiModalEmbeddingSystem, DataModalityType, SimilarityMetric,
        ClusteringAlgorithm, EmbeddingResult, SimilarityResult, ClusteringResult
    )
    ADVANCED_EMBEDDINGS_AVAILABLE = True
except ImportError:
    ADVANCED_EMBEDDINGS_AVAILABLE = False
    print("Warning: Advanced embedding system not available")

# Fallback imports for basic functionality
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("Warning: sentence-transformers not available. Install with: pip install sentence-transformers")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MemoryType(Enum):
    """Types of memory in the hierarchical system"""
    EPISODIC = "episodic"        # Specific experiences and events
    SEMANTIC = "semantic"        # General knowledge and facts
    PROCEDURAL = "procedural"    # Skills and procedures
    WORKING = "working"          # Temporary processing memory
    EMOTIONAL = "emotional"      # Emotion-linked memories
    AUTOBIOGRAPHICAL = "autobiographical"  # Personal history
    PROSPECTIVE = "prospective"  # Future-oriented memories (plans, intentions)


class EmotionalValence(Enum):
    """Emotional valence for memory tagging"""
    VERY_POSITIVE = 2
    POSITIVE = 1
    NEUTRAL = 0
    NEGATIVE = -1
    VERY_NEGATIVE = -2


class ImportanceLevel(Enum):
    """Importance levels for memory prioritization"""
    CRITICAL = 1.0
    HIGH = 0.8
    MEDIUM = 0.6
    LOW = 0.4
    MINIMAL = 0.2


@dataclass
class EmotionalTag:
    """Emotional context for memories"""
    valence: EmotionalValence
    arousal: float  # 0.0 to 1.0 (intensity)
    emotion_type: str  # joy, fear, anger, sadness, surprise, disgust, etc.
    confidence: float = 0.5
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_vector(self) -> np.ndarray:
        """Convert emotional tag to vector representation"""
        return np.array([
            self.valence.value,
            self.arousal,
            self.confidence,
            hash(self.emotion_type) % 100 / 100.0  # Normalized hash
        ])


@dataclass
class MemoryMetadata:
    """Rich metadata for memory entries"""
    creation_time: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    importance: ImportanceLevel = ImportanceLevel.MEDIUM
    source: str = "internal"
    tags: Set[str] = field(default_factory=set)
    related_memories: Set[str] = field(default_factory=set)
    consolidation_score: float = 0.0
    decay_rate: float = 0.01
    reinforcement_count: int = 0
    context: Dict[str, Any] = field(default_factory=dict)
    
    def update_access(self):
        """Update access statistics"""
        self.last_accessed = datetime.now()
        self.access_count += 1
    
    def calculate_age_hours(self) -> float:
        """Calculate age in hours"""
        return (datetime.now() - self.creation_time).total_seconds() / 3600


@dataclass
class EnhancedMemory:
    """Enhanced memory unit with multi-modal support"""
    memory_id: str
    content: Any  # Can be text, structured data, or any serializable object
    memory_type: MemoryType
    embedding: Optional[np.ndarray] = None
    emotional_tag: Optional[EmotionalTag] = None
    metadata: MemoryMetadata = field(default_factory=MemoryMetadata)
    associations: Dict[str, float] = field(default_factory=dict)  # memory_id -> strength
    retrieval_strength: float = 1.0
    consolidation_level: int = 0  # 0=new, 1=consolidated, 2=long-term
    
    def __post_init__(self):
        if not self.memory_id:
            self.memory_id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate unique memory ID"""
        content_str = str(self.content)[:1000]  # Limit for hashing
        timestamp = str(self.metadata.creation_time)
        unique_string = f"{content_str}{timestamp}{self.memory_type.value}"
        return hashlib.sha256(unique_string.encode()).hexdigest()[:16]
    
    def strengthen(self, amount: float = 0.1):
        """Strengthen memory through reinforcement"""
        self.retrieval_strength = min(1.0, self.retrieval_strength + amount)
        self.metadata.reinforcement_count += 1
        self.metadata.decay_rate *= 0.95  # Reduce decay rate when strengthened
    
    def decay(self, time_factor: float = 1.0):
        """Apply temporal decay to memory strength"""
        age_hours = self.metadata.calculate_age_hours()
        decay_amount = self.metadata.decay_rate * time_factor * (age_hours / 24.0)
        self.retrieval_strength = max(0.0, self.retrieval_strength - decay_amount)
    
    def calculate_relevance(self, query_embedding: np.ndarray, 
                          emotional_context: Optional[EmotionalTag] = None) -> float:
        """Calculate relevance score for retrieval"""
        relevance = 0.0
        
        # Semantic similarity
        if self.embedding is not None and query_embedding is not None:
            semantic_sim = cosine_similarity([self.embedding], [query_embedding])[0][0]
            relevance += semantic_sim * 0.6
        
        # Emotional context matching
        if emotional_context and self.emotional_tag:
            emotional_sim = self._emotional_similarity(emotional_context)
            relevance += emotional_sim * 0.2
        
        # Recency and access patterns
        recency_factor = 1.0 / (1.0 + self.metadata.calculate_age_hours() / 24.0)
        access_factor = min(1.0, self.metadata.access_count / 10.0)
        relevance += (recency_factor * 0.1) + (access_factor * 0.1)
        
        # Importance weighting
        relevance *= self.metadata.importance.value
        
        # Retrieval strength
        relevance *= self.retrieval_strength
        
        return relevance
    
    def _emotional_similarity(self, other_emotion: EmotionalTag) -> float:
        """Calculate emotional similarity between tags"""
        if not self.emotional_tag:
            return 0.0
        
        valence_sim = 1.0 - abs(self.emotional_tag.valence.value - other_emotion.valence.value) / 4.0
        arousal_sim = 1.0 - abs(self.emotional_tag.arousal - other_emotion.arousal)
        type_sim = 1.0 if self.emotional_tag.emotion_type == other_emotion.emotion_type else 0.0
        
        return (valence_sim * 0.4) + (arousal_sim * 0.3) + (type_sim * 0.3)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert memory to dictionary for serialization"""
        emotional_tag_dict = None
        if self.emotional_tag:
            emotional_tag_dict = {
                'valence': self.emotional_tag.valence.value,
                'arousal': self.emotional_tag.arousal,
                'emotion_type': self.emotional_tag.emotion_type,
                'confidence': self.emotional_tag.confidence,
                'timestamp': self.emotional_tag.timestamp.isoformat()
            }
        
        metadata_dict = {
            'creation_time': self.metadata.creation_time.isoformat(),
            'last_accessed': self.metadata.last_accessed.isoformat(),
            'access_count': self.metadata.access_count,
            'importance': self.metadata.importance.value,
            'source': self.metadata.source,
            'tags': list(self.metadata.tags),
            'related_memories': list(self.metadata.related_memories),
            'consolidation_score': self.metadata.consolidation_score,
            'decay_rate': self.metadata.decay_rate,
            'reinforcement_count': self.metadata.reinforcement_count,
            'context': self.metadata.context
        }
        
        return {
            'memory_id': self.memory_id,
            'content': self.content,
            'memory_type': self.memory_type.value,
            'embedding': self.embedding.tolist() if self.embedding is not None else None,
            'emotional_tag': emotional_tag_dict,
            'metadata': metadata_dict,
            'associations': self.associations,
            'retrieval_strength': self.retrieval_strength,
            'consolidation_level': self.consolidation_level
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnhancedMemory':
        """Create memory from dictionary"""
        # Reconstruct objects
        memory_type = MemoryType(data['memory_type'])
        embedding = np.array(data['embedding']) if data['embedding'] else None
        
        emotional_tag = None
        if data['emotional_tag']:
            et_data = data['emotional_tag']
            emotional_tag = EmotionalTag(
                valence=EmotionalValence(et_data['valence']),
                arousal=et_data['arousal'],
                emotion_type=et_data['emotion_type'],
                confidence=et_data['confidence'],
                timestamp=datetime.fromisoformat(et_data['timestamp'])
            )
        
        # Reconstruct metadata
        md_data = data['metadata']
        metadata = MemoryMetadata(
            creation_time=datetime.fromisoformat(md_data['creation_time']),
            last_accessed=datetime.fromisoformat(md_data['last_accessed']),
            access_count=md_data['access_count'],
            importance=ImportanceLevel(md_data['importance']),
            source=md_data['source'],
            tags=set(md_data['tags']),
            related_memories=set(md_data['related_memories']),
            consolidation_score=md_data['consolidation_score'],
            decay_rate=md_data['decay_rate'],
            reinforcement_count=md_data['reinforcement_count'],
            context=md_data['context']
        )
        
        return cls(
            memory_id=data['memory_id'],
            content=data['content'],
            memory_type=memory_type,
            embedding=embedding,
            emotional_tag=emotional_tag,
            metadata=metadata,
            associations=data['associations'],
            retrieval_strength=data['retrieval_strength'],
            consolidation_level=data['consolidation_level']
        )


class AdvancedEmbeddingSystem:
    """
    Wrapper class for integrating with the MultiModalEmbeddingSystem
    Provides backward compatibility while leveraging advanced features
    """
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.initialized = False
        self.multi_modal_system = None
        self.fallback_model = None
        self.tfidf_vectorizer = TfidfVectorizer(max_features=512, stop_words='english')
        self.tfidf_fitted = False
        self.dimensions = 768  # Default for sentence-transformers
        self.embedding_cache = {}
        self.cache_lock = threading.Lock()
        
        self._initialize_embedding_system()
    
    def _initialize_embedding_system(self):
        """Initialize the advanced embedding system"""
        try:
            if ADVANCED_EMBEDDINGS_AVAILABLE:
                self.multi_modal_system = MultiModalEmbeddingSystem()
                logger.info("Advanced multi-modal embedding system initialized")
                self.initialized = True
            elif SENTENCE_TRANSFORMERS_AVAILABLE:
                self.fallback_model = SentenceTransformer(self.model_name)
                logger.info(f"Fallback to basic sentence-transformers: {self.model_name}")
                self.initialized = True
            else:
                logger.warning("Using TF-IDF fallback for embeddings")
                self.dimensions = 512
        except Exception as e:
            logger.error(f"Error initializing embedding system: {e}")
            self.initialized = False
    
    def encode(self, texts: Union[str, List[str]], use_cache: bool = True) -> np.ndarray:
        """
        Encode text(s) to embeddings with backward compatibility
        
        Args:
            texts: Text string or list of strings to embed
            use_cache: Whether to use caching
        
        Returns:
            numpy array of embeddings
        """
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = []
        for text in texts:
            # Check cache first
            if use_cache:
                with self.cache_lock:
                    if text in self.embedding_cache:
                        embeddings.append(self.embedding_cache[text])
                        continue
            
            # Generate embedding
            try:
                if self.multi_modal_system:
                    # Use advanced multi-modal system
                    result = self.multi_modal_system.embed_text(text)
                    if result.success:
                        embedding = result.embedding
                    else:
                        embedding = np.zeros(self.dimensions)
                elif self.fallback_model:
                    # Use sentence-transformers fallback
                    embedding = self.fallback_model.encode(text)
                else:
                    # Use TF-IDF fallback
                    embedding = self._encode_with_tfidf(text)
                
                embeddings.append(embedding)
                
                # Cache result
                if use_cache:
                    with self.cache_lock:
                        self.embedding_cache[text] = embedding
                        
            except Exception as e:
                logger.error(f"Error encoding text: {e}")
                embeddings.append(np.zeros(self.dimensions))
        
        return np.array(embeddings)
    
    def _encode_with_tfidf(self, text: str) -> np.ndarray:
        """Encode using TF-IDF as fallback"""
        try:
            if not self.tfidf_fitted:
                # Fit with current text if not fitted
                self.tfidf_vectorizer.fit([text])
                self.tfidf_fitted = True
            
            embedding = self.tfidf_vectorizer.transform([text]).toarray()[0]
            return embedding
        except Exception as e:
            logger.error(f"TF-IDF encoding failed: {e}")
            return np.random.normal(0, 0.1, self.dimensions)
    
    def embed(self, texts: Union[str, List[str]], modality: str = "text") -> np.ndarray:
        """
        Generate embeddings for text or other modalities
        
        Args:
            texts: Text string or list of strings to embed
            modality: Data modality type (text, numerical, categorical, temporal)
        
        Returns:
            numpy array of embeddings
        """
        if isinstance(texts, str):
            texts = [texts]
        
        try:
            if self.multi_modal_system:
                # Use advanced multi-modal system
                results = []
                
                for text in texts:
                    if modality == "text":
                        result = self.multi_modal_system.embed_text(text)
                    elif modality == "numerical":
                        # Convert text to numerical if needed
                        try:
                            data = json.loads(text) if isinstance(text, str) else text
                            result = self.multi_modal_system.embed_numerical(data)
                        except:
                            result = self.multi_modal_system.embed_text(str(text))
                    elif modality == "categorical":
                        result = self.multi_modal_system.embed_categorical([text])
                    elif modality == "temporal":
                        try:
                            timestamp = datetime.fromisoformat(text) if isinstance(text, str) else text
                            result = self.multi_modal_system.embed_temporal(timestamp)
                        except:
                            result = self.multi_modal_system.embed_text(str(text))
                    else:
                        result = self.multi_modal_system.embed_text(str(text))
                    
                    if result.success:
                        results.append(result.embedding)
                    else:
                        logger.warning(f"Embedding failed for {text[:50]}...")
                        results.append(np.zeros(self.dimensions))
                
                return np.array(results)
            else:
                # Use backward compatible encoding
                return self.encode(texts)
                
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            # Return zero embeddings as fallback
            return np.zeros((len(texts), self.dimensions))
    
    def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calculate cosine similarity between embeddings (backward compatibility)"""
        return self.compute_similarity(embedding1, embedding2)
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray, 
                          metric: str = "cosine") -> float:
        """
        Compute similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            metric: Similarity metric (cosine, euclidean, manhattan)
        
        Returns:
            Similarity score
        """
        try:
            if self.multi_modal_system:
                # Use advanced similarity computation
                try:
                    metric_enum = SimilarityMetric(metric.upper())
                    result = self.multi_modal_system.compute_similarity(
                        embedding1, embedding2, metric_enum
                    )
                    return result.similarity if result.success else 0.0
                except:
                    # Fallback to basic cosine similarity
                    pass
            
            # Fallback similarity computation
            if embedding1.size == 0 or embedding2.size == 0:
                return 0.0
            
            # Ensure same dimensions
            if embedding1.shape != embedding2.shape:
                min_dim = min(len(embedding1), len(embedding2))
                embedding1 = embedding1[:min_dim]
                embedding2 = embedding2[:min_dim]
            
            # Ensure embeddings are 2D for sklearn
            if len(embedding1.shape) == 1:
                embedding1 = embedding1.reshape(1, -1)
            if len(embedding2.shape) == 1:
                embedding2 = embedding2.reshape(1, -1)
            
            similarity = cosine_similarity(embedding1, embedding2)
            return float(similarity[0][0])
                
        except Exception as e:
            logger.error(f"Error computing similarity: {e}")
            return 0.0
    
    def cluster_embeddings(self, embeddings: np.ndarray, n_clusters: int = 5,
                          algorithm: str = "kmeans") -> Dict[str, Any]:
        """
        Cluster embeddings using various algorithms
        
        Args:
            embeddings: Array of embeddings to cluster
            n_clusters: Number of clusters
            algorithm: Clustering algorithm (kmeans, dbscan, hierarchical)
        
        Returns:
            Dictionary with clustering results
        """
        try:
            if self.multi_modal_system:
                # Use advanced clustering
                try:
                    algorithm_enum = ClusteringAlgorithm(algorithm.upper())
                    result = self.multi_modal_system.cluster_embeddings(
                        embeddings, n_clusters, algorithm_enum
                    )
                    
                    if result.success:
                        return {
                            'labels': result.labels,
                            'centroids': result.centroids,
                            'metrics': result.metrics,
                            'algorithm': algorithm
                        }
                except:
                    # Fallback to basic clustering
                    pass
            
            # Fallback clustering
            if algorithm.lower() == "kmeans":
                kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                labels = kmeans.fit_predict(embeddings)
                return {
                    'labels': labels,
                    'centroids': kmeans.cluster_centers_,
                    'metrics': {'inertia': kmeans.inertia_},
                    'algorithm': 'kmeans'
                }
            
        except Exception as e:
            logger.error(f"Error clustering embeddings: {e}")
            return {'labels': np.zeros(len(embeddings)), 'centroids': None}
    
    def get_embedding_dimension(self) -> int:
        """Get embedding dimension (backward compatibility)"""
        if self.multi_modal_system:
            return self.multi_modal_system.default_dimension
        elif self.fallback_model:
            return self.fallback_model.get_sentence_embedding_dimension()
        else:
            return self.dimensions
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get embedding system statistics"""
        stats = {
            'initialized': self.initialized,
            'system_type': 'advanced' if self.multi_modal_system else 'fallback',
            'dimensions': self.get_embedding_dimension(),
            'cache_size': len(self.embedding_cache)
        }
        
        if self.multi_modal_system:
            stats.update(self.multi_modal_system.get_statistics())
        
        return stats


class MemoryDatabase:
    """SQLite database interface for persistent memory storage"""
    
    def __init__(self, db_path: str = "memory_network.db"):
        self.db_path = db_path
        self.connection_pool = []
        self.pool_lock = threading.Lock()
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        
        # Create main memories table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                memory_id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                embedding BLOB,
                emotional_tag TEXT,
                metadata TEXT,
                associations TEXT,
                retrieval_strength REAL,
                consolidation_level INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create associations table for efficient relationship queries
        conn.execute('''
            CREATE TABLE IF NOT EXISTS memory_associations (
                source_id TEXT,
                target_id TEXT,
                strength REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (source_id, target_id),
                FOREIGN KEY (source_id) REFERENCES memories (memory_id),
                FOREIGN KEY (target_id) REFERENCES memories (memory_id)
            )
        ''')
        
        # Create index for faster retrieval
        conn.execute('CREATE INDEX IF NOT EXISTS idx_memory_type ON memories (memory_type)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_retrieval_strength ON memories (retrieval_strength)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON memories (created_at)')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized")
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection from pool"""
        with self.pool_lock:
            if self.connection_pool:
                return self.connection_pool.pop()
            else:
                return sqlite3.connect(self.db_path, timeout=30.0)
    
    def _return_connection(self, conn: sqlite3.Connection):
        """Return connection to pool"""
        with self.pool_lock:
            if len(self.connection_pool) < 10:  # Limit pool size
                self.connection_pool.append(conn)
            else:
                conn.close()
    
    def store_memory(self, memory: EnhancedMemory) -> bool:
        """Store memory in database"""
        try:
            conn = self._get_connection()
            
            # Serialize complex objects
            embedding_blob = pickle.dumps(memory.embedding) if memory.embedding is not None else None
            emotional_tag_json = None
            if memory.emotional_tag:
                emotional_tag_json = json.dumps({
                    'valence': memory.emotional_tag.valence.value,
                    'arousal': memory.emotional_tag.arousal,
                    'emotion_type': memory.emotional_tag.emotion_type,
                    'confidence': memory.emotional_tag.confidence,
                    'timestamp': memory.emotional_tag.timestamp.isoformat()
                })
            
            metadata_json = json.dumps({
                'creation_time': memory.metadata.creation_time.isoformat(),
                'last_accessed': memory.metadata.last_accessed.isoformat(),
                'access_count': memory.metadata.access_count,
                'importance': memory.metadata.importance.value,
                'source': memory.metadata.source,
                'tags': list(memory.metadata.tags),
                'related_memories': list(memory.metadata.related_memories),
                'consolidation_score': memory.metadata.consolidation_score,
                'decay_rate': memory.metadata.decay_rate,
                'reinforcement_count': memory.metadata.reinforcement_count,
                'context': memory.metadata.context
            })
            associations_json = json.dumps(memory.associations)
            
            conn.execute('''
                INSERT OR REPLACE INTO memories 
                (memory_id, content, memory_type, embedding, emotional_tag, metadata, 
                 associations, retrieval_strength, consolidation_level, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                memory.memory_id,
                json.dumps(memory.content) if not isinstance(memory.content, str) else memory.content,
                memory.memory_type.value,
                embedding_blob,
                emotional_tag_json,
                metadata_json,
                associations_json,
                memory.retrieval_strength,
                memory.consolidation_level
            ))
            
            # Store associations
            for target_id, strength in memory.associations.items():
                conn.execute('''
                    INSERT OR REPLACE INTO memory_associations 
                    (source_id, target_id, strength)
                    VALUES (?, ?, ?)
                ''', (memory.memory_id, target_id, strength))
            
            conn.commit()
            self._return_connection(conn)
            return True
            
        except Exception as e:
            logger.error(f"Failed to store memory {memory.memory_id}: {e}")
            try:
                conn.rollback()
                self._return_connection(conn)
            except:
                pass
            return False
    
    def load_memory(self, memory_id: str) -> Optional[EnhancedMemory]:
        """Load memory from database"""
        try:
            conn = self._get_connection()
            cursor = conn.execute(
                'SELECT * FROM memories WHERE memory_id = ?', 
                (memory_id,)
            )
            row = cursor.fetchone()
            self._return_connection(conn)
            
            if not row:
                return None
            
            # Deserialize data
            columns = [desc[0] for desc in cursor.description]
            data = dict(zip(columns, row))
            
            # Reconstruct memory object
            content = data['content']
            try:
                content = json.loads(content)
            except:
                pass  # Keep as string if not JSON
            
            embedding = pickle.loads(data['embedding']) if data['embedding'] else None
            
            emotional_tag = None
            if data['emotional_tag']:
                et_data = json.loads(data['emotional_tag'])
                emotional_tag = EmotionalTag(
                    valence=EmotionalValence(et_data['valence']),
                    arousal=et_data['arousal'],
                    emotion_type=et_data['emotion_type'],
                    confidence=et_data['confidence'],
                    timestamp=datetime.fromisoformat(et_data['timestamp'])
                )
            
            metadata_dict = json.loads(data['metadata'])
            metadata = MemoryMetadata(
                creation_time=datetime.fromisoformat(metadata_dict['creation_time']),
                last_accessed=datetime.fromisoformat(metadata_dict['last_accessed']),
                access_count=metadata_dict['access_count'],
                importance=ImportanceLevel(metadata_dict['importance']),
                source=metadata_dict['source'],
                tags=set(metadata_dict['tags']),
                related_memories=set(metadata_dict['related_memories']),
                consolidation_score=metadata_dict['consolidation_score'],
                decay_rate=metadata_dict['decay_rate'],
                reinforcement_count=metadata_dict['reinforcement_count'],
                context=metadata_dict['context']
            )
            
            associations = json.loads(data['associations'])
            
            return EnhancedMemory(
                memory_id=data['memory_id'],
                content=content,
                memory_type=MemoryType(data['memory_type']),
                embedding=embedding,
                emotional_tag=emotional_tag,
                metadata=metadata,
                associations=associations,
                retrieval_strength=data['retrieval_strength'],
                consolidation_level=data['consolidation_level']
            )
            
        except Exception as e:
            logger.error(f"Failed to load memory {memory_id}: {e}")
            return None
    
    def query_memories(self, memory_type: Optional[MemoryType] = None,
                      min_strength: float = 0.0,
                      limit: int = 1000) -> List[str]:
        """Query memory IDs by criteria"""
        try:
            conn = self._get_connection()
            
            query = 'SELECT memory_id FROM memories WHERE retrieval_strength >= ?'
            params = [min_strength]
            
            if memory_type:
                query += ' AND memory_type = ?'
                params.append(memory_type.value)
            
            query += ' ORDER BY retrieval_strength DESC, created_at DESC LIMIT ?'
            params.append(limit)
            
            cursor = conn.execute(query, params)
            memory_ids = [row[0] for row in cursor.fetchall()]
            self._return_connection(conn)
            
            return memory_ids
            
        except Exception as e:
            logger.error(f"Failed to query memories: {e}")
            return []
    
    def get_associations(self, memory_id: str, min_strength: float = 0.1) -> List[Tuple[str, float]]:
        """Get associated memories"""
        try:
            conn = self._get_connection()
            cursor = conn.execute('''
                SELECT target_id, strength FROM memory_associations 
                WHERE source_id = ? AND strength >= ?
                ORDER BY strength DESC
            ''', (memory_id, min_strength))
            
            associations = [(row[0], row[1]) for row in cursor.fetchall()]
            self._return_connection(conn)
            
            return associations
            
        except Exception as e:
            logger.error(f"Failed to get associations for {memory_id}: {e}")
            return []
    
    def cleanup_weak_memories(self, threshold: float = 0.1) -> int:
        """Remove memories below threshold strength"""
        try:
            conn = self._get_connection()
            
            # Get weak memory IDs first
            cursor = conn.execute(
                'SELECT memory_id FROM memories WHERE retrieval_strength < ?',
                (threshold,)
            )
            weak_ids = [row[0] for row in cursor.fetchall()]
            
            # Delete weak memories and their associations
            for memory_id in weak_ids:
                conn.execute('DELETE FROM memories WHERE memory_id = ?', (memory_id,))
                conn.execute('DELETE FROM memory_associations WHERE source_id = ? OR target_id = ?', 
                           (memory_id, memory_id))
            
            conn.commit()
            self._return_connection(conn)
            
            logger.info(f"Cleaned up {len(weak_ids)} weak memories")
            return len(weak_ids)
            
        except Exception as e:
            logger.error(f"Failed to cleanup weak memories: {e}")
            return 0


class EnhancedMemoryNetwork:
    """Enhanced memory network with multi-modal support and hierarchical organization"""
    
    def __init__(self, 
                 db_path: str = "enhanced_memory.db",
                 embedding_model: str = 'all-MiniLM-L6-v2',
                 max_cache_size: int = 1000):
        
        self.db = MemoryDatabase(db_path)
        self.embedding_system = AdvancedEmbeddingSystem(embedding_model)
        
        # In-memory cache for frequently accessed memories
        self.memory_cache = {}
        self.cache_access_times = {}
        self.max_cache_size = max_cache_size
        self.cache_lock = threading.Lock()
        
        # Memory organization
        self.memory_types = {mt: [] for mt in MemoryType}
        self.consolidation_queue = deque()
        
        # Statistics
        self.stats = {
            'total_memories': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'consolidations_performed': 0,
            'average_retrieval_time': 0.0
        }
        
        # Background processing
        self.background_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="MemoryBG")
        self.consolidation_active = False
        
        logger.info("Enhanced Memory Network initialized")
    
    def store_memory(self, 
                    content: Any,
                    memory_type: MemoryType = MemoryType.SEMANTIC,
                    emotional_tag: Optional[EmotionalTag] = None,
                    importance: ImportanceLevel = ImportanceLevel.MEDIUM,
                    tags: Optional[Set[str]] = None,
                    context: Optional[Dict[str, Any]] = None) -> str:
        """Store a new memory"""
        
        # Create metadata
        metadata = MemoryMetadata(
            importance=importance,
            tags=tags or set(),
            context=context or {}
        )
        
        # Generate embedding
        content_str = str(content)
        embedding = self.embedding_system.encode(content_str)[0]
        
        # Create memory
        memory = EnhancedMemory(
            memory_id="",  # Will be auto-generated
            content=content,
            memory_type=memory_type,
            embedding=embedding,
            emotional_tag=emotional_tag,
            metadata=metadata
        )
        
        # Store in database
        success = self.db.store_memory(memory)
        if success:
            # Add to cache
            with self.cache_lock:
                self._add_to_cache(memory)
            
            # Update statistics
            self.stats['total_memories'] += 1
            
            # Queue for consolidation if important
            if importance.value >= ImportanceLevel.HIGH.value:
                self.consolidation_queue.append(memory.memory_id)
            
            logger.info(f"Stored memory: {memory.memory_id} ({memory_type.value})")
            return memory.memory_id
        else:
            logger.error(f"Failed to store memory")
            return ""
    
    def retrieve_memory(self, memory_id: str) -> Optional[EnhancedMemory]:
        """Retrieve specific memory by ID"""
        start_time = time.time()
        
        # Check cache first
        with self.cache_lock:
            if memory_id in self.memory_cache:
                memory = self.memory_cache[memory_id]
                memory.metadata.update_access()
                self.cache_access_times[memory_id] = time.time()
                self.stats['cache_hits'] += 1
                
                # Update retrieval time stat
                retrieval_time = time.time() - start_time
                self._update_avg_retrieval_time(retrieval_time)
                
                return memory
        
        # Load from database
        memory = self.db.load_memory(memory_id)
        if memory:
            memory.metadata.update_access()
            
            # Add to cache
            with self.cache_lock:
                self._add_to_cache(memory)
            
            self.stats['cache_misses'] += 1
            
            # Update in database
            self.db.store_memory(memory)
        
        # Update retrieval time stat
        retrieval_time = time.time() - start_time
        self._update_avg_retrieval_time(retrieval_time)
        
        return memory
    
    def search_memories(self, 
                       query: str,
                       memory_types: Optional[List[MemoryType]] = None,
                       emotional_context: Optional[EmotionalTag] = None,
                       max_results: int = 10,
                       min_relevance: float = 0.1) -> List[Tuple[EnhancedMemory, float]]:
        """Search memories by semantic similarity and other criteria"""
        
        # Generate query embedding
        query_embedding = self.embedding_system.encode(query)[0]
        
        # Get candidate memory IDs
        candidate_ids = []
        if memory_types:
            for memory_type in memory_types:
                type_ids = self.db.query_memories(memory_type=memory_type, limit=500)
                candidate_ids.extend(type_ids)
        else:
            candidate_ids = self.db.query_memories(limit=1000)
        
        # Score and rank memories
        scored_memories = []
        for memory_id in candidate_ids:
            memory = self.retrieve_memory(memory_id)
            if memory:
                relevance = memory.calculate_relevance(query_embedding, emotional_context)
                if relevance >= min_relevance:
                    scored_memories.append((memory, relevance))
        
        # Sort by relevance and return top results
        scored_memories.sort(key=lambda x: x[1], reverse=True)
        return scored_memories[:max_results]
    
    def associate_memories(self, memory_id1: str, memory_id2: str, strength: float = 0.5):
        """Create bidirectional association between memories"""
        memory1 = self.retrieve_memory(memory_id1)
        memory2 = self.retrieve_memory(memory_id2)
        
        if memory1 and memory2:
            # Add associations
            memory1.associations[memory_id2] = strength
            memory2.associations[memory_id1] = strength
            
            # Update metadata
            memory1.metadata.related_memories.add(memory_id2)
            memory2.metadata.related_memories.add(memory_id1)
            
            # Store updates
            self.db.store_memory(memory1)
            self.db.store_memory(memory2)
            
            logger.info(f"Associated memories: {memory_id1} <-> {memory_id2} (strength: {strength})")
    
    def consolidate_memory(self, memory_id: str) -> bool:
        """Consolidate a memory by strengthening associations and updating embeddings"""
        memory = self.retrieve_memory(memory_id)
        if not memory:
            return False
        
        try:
            # Find similar memories for association
            similar_memories = self.search_memories(
                query=str(memory.content),
                memory_types=[memory.memory_type],
                max_results=5,
                min_relevance=0.3
            )
            
            # Create associations with similar memories
            for similar_memory, similarity in similar_memories:
                if similar_memory.memory_id != memory_id:
                    association_strength = similarity * 0.5  # Moderate association
                    if similar_memory.memory_id not in memory.associations:
                        self.associate_memories(memory_id, similar_memory.memory_id, association_strength)
            
            # Update consolidation level
            memory.consolidation_level = min(2, memory.consolidation_level + 1)
            memory.metadata.consolidation_score = min(1.0, memory.metadata.consolidation_score + 0.2)
            
            # Strengthen memory
            memory.strengthen(0.1)
            
            # Store updates
            self.db.store_memory(memory)
            
            self.stats['consolidations_performed'] += 1
            logger.info(f"Consolidated memory: {memory_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to consolidate memory {memory_id}: {e}")
            return False
    
    def apply_temporal_decay(self, decay_factor: float = 1.0):
        """Apply temporal decay to all memories"""
        logger.info("Applying temporal decay to memories...")
        
        # Get all memory IDs
        memory_ids = self.db.query_memories(min_strength=0.0, limit=10000)
        
        decay_count = 0
        for memory_id in memory_ids:
            memory = self.retrieve_memory(memory_id)
            if memory:
                old_strength = memory.retrieval_strength
                memory.decay(decay_factor)
                
                if memory.retrieval_strength != old_strength:
                    self.db.store_memory(memory)
                    decay_count += 1
        
        # Cleanup very weak memories
        cleaned = self.db.cleanup_weak_memories(threshold=0.05)
        
        logger.info(f"Applied decay to {decay_count} memories, cleaned up {cleaned} weak memories")
    
    def sleep_cycle_consolidation(self):
        """Perform memory consolidation during sleep cycle"""
        if self.consolidation_active:
            return
        
        self.consolidation_active = True
        logger.info("Starting sleep cycle memory consolidation...")
        
        try:
            # Process consolidation queue
            while self.consolidation_queue:
                memory_id = self.consolidation_queue.popleft()
                self.consolidate_memory(memory_id)
            
            # Apply temporal decay
            self.apply_temporal_decay(0.1)
            
            # Auto-associate highly similar memories
            self._auto_associate_memories()
            
        except Exception as e:
            logger.error(f"Error during sleep cycle consolidation: {e}")
        finally:
            self.consolidation_active = False
            
        logger.info("Sleep cycle consolidation completed")
    
    def _auto_associate_memories(self, similarity_threshold: float = 0.7):
        """Automatically create associations between similar memories"""
        # Get recent important memories
        important_ids = self.db.query_memories(min_strength=0.6, limit=100)
        
        associations_created = 0
        for i, memory_id1 in enumerate(important_ids):
            memory1 = self.retrieve_memory(memory_id1)
            if not memory1 or not memory1.embedding:
                continue
            
            for memory_id2 in important_ids[i+1:]:
                memory2 = self.retrieve_memory(memory_id2)
                if not memory2 or not memory2.embedding:
                    continue
                
                # Skip if already associated
                if memory_id2 in memory1.associations:
                    continue
                
                # Calculate similarity
                similarity = self.embedding_system.calculate_similarity(
                    memory1.embedding, memory2.embedding
                )
                
                if similarity >= similarity_threshold:
                    self.associate_memories(memory_id1, memory_id2, similarity * 0.8)
                    associations_created += 1
        
        logger.info(f"Auto-created {associations_created} memory associations")
    
    def _add_to_cache(self, memory: EnhancedMemory):
        """Add memory to cache with LRU eviction"""
        if len(self.memory_cache) >= self.max_cache_size:
            # Remove least recently used memory
            lru_memory_id = min(self.cache_access_times.keys(), 
                              key=self.cache_access_times.get)
            del self.memory_cache[lru_memory_id]
            del self.cache_access_times[lru_memory_id]
        
        self.memory_cache[memory.memory_id] = memory
        self.cache_access_times[memory.memory_id] = time.time()
    
    def _update_avg_retrieval_time(self, new_time: float):
        """Update average retrieval time statistic"""
        if self.stats['average_retrieval_time'] == 0.0:
            self.stats['average_retrieval_time'] = new_time
        else:
            # Exponential moving average
            alpha = 0.1
            self.stats['average_retrieval_time'] = (
                alpha * new_time + (1 - alpha) * self.stats['average_retrieval_time']
            )
    
    def get_memory_statistics(self) -> Dict[str, Any]:
        """Get comprehensive memory network statistics"""
        # Memory type distribution
        type_distribution = {}
        for memory_type in MemoryType:
            count = len(self.db.query_memories(memory_type=memory_type))
            type_distribution[memory_type.value] = count
        
        # Cache statistics
        cache_hit_rate = 0.0
        total_accesses = self.stats['cache_hits'] + self.stats['cache_misses']
        if total_accesses > 0:
            cache_hit_rate = self.stats['cache_hits'] / total_accesses
        
        return {
            'total_memories': self.stats['total_memories'],
            'memory_type_distribution': type_distribution,
            'cache_size': len(self.memory_cache),
            'cache_hit_rate': cache_hit_rate,
            'consolidations_performed': self.stats['consolidations_performed'],
            'average_retrieval_time_ms': self.stats['average_retrieval_time'] * 1000,
            'consolidation_queue_size': len(self.consolidation_queue),
            'embedding_cache_size': len(self.embedding_system.embedding_cache)
        }
    
    def export_memories(self, filepath: str, memory_type: Optional[MemoryType] = None):
        """Export memories to JSON file"""
        memory_ids = self.db.query_memories(memory_type=memory_type, limit=10000)
        
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'memory_count': len(memory_ids),
            'memories': []
        }
        
        for memory_id in memory_ids:
            memory = self.retrieve_memory(memory_id)
            if memory:
                export_data['memories'].append(memory.to_dict())
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        logger.info(f"Exported {len(memory_ids)} memories to {filepath}")
    
    def import_memories(self, filepath: str) -> int:
        """Import memories from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            imported_count = 0
            for memory_data in data['memories']:
                try:
                    memory = EnhancedMemory.from_dict(memory_data)
                    if self.db.store_memory(memory):
                        imported_count += 1
                except Exception as e:
                    logger.error(f"Failed to import memory: {e}")
            
            logger.info(f"Imported {imported_count} memories from {filepath}")
            return imported_count
            
        except Exception as e:
            logger.error(f"Failed to import memories from {filepath}: {e}")
            return 0
    
    def cleanup_and_optimize(self):
        """Perform cleanup and optimization operations"""
        logger.info("Starting memory network cleanup and optimization...")
        
        # Clear cache
        with self.cache_lock:
            self.memory_cache.clear()
            self.cache_access_times.clear()
        
        # Apply aggressive temporal decay
        self.apply_temporal_decay(2.0)
        
        # Remove very weak memories
        cleaned = self.db.cleanup_weak_memories(threshold=0.1)
        
        # Clear embedding cache
        self.embedding_system.embedding_cache.clear()
        
        logger.info(f"Cleanup completed: removed {cleaned} weak memories")
    
    def __del__(self):
        """Cleanup on destruction"""
        if hasattr(self, 'background_executor'):
            self.background_executor.shutdown(wait=True)


# Example usage and demonstration
async def demo_enhanced_memory_network():
    """Demonstrate the enhanced memory network"""
    print("=== Enhanced Memory Network Demo ===\n")
    
    # Initialize the network
    memory_net = EnhancedMemoryNetwork(
        db_path="demo_enhanced_memory.db",
        embedding_model='all-MiniLM-L6-v2'
    )
    
    # Create some test memories with different types and emotional tags
    print("Storing various types of memories...")
    
    # Episodic memory with emotional context
    emotional_tag = EmotionalTag(
        valence=EmotionalValence.POSITIVE,
        arousal=0.8,
        emotion_type="excitement"
    )
    
    episodic_id = memory_net.store_memory(
        content="I successfully completed my first AI research project today",
        memory_type=MemoryType.EPISODIC,
        emotional_tag=emotional_tag,
        importance=ImportanceLevel.HIGH,
        tags={"achievement", "research", "ai"},
        context={"location": "lab", "date": "2025-09-10"}
    )
    
    # Semantic memory
    semantic_id = memory_net.store_memory(
        content="Machine learning algorithms learn patterns from data through statistical methods",
        memory_type=MemoryType.SEMANTIC,
        importance=ImportanceLevel.HIGH,
        tags={"machine learning", "algorithms", "statistics"}
    )
    
    # Procedural memory
    procedural_id = memory_net.store_memory(
        content={
            "skill": "coding_in_python",
            "steps": ["analyze problem", "design solution", "implement code", "test results"],
            "proficiency": 0.8
        },
        memory_type=MemoryType.PROCEDURAL,
        importance=ImportanceLevel.MEDIUM,
        tags={"programming", "python", "skills"}
    )
    
    # Autobiographical memory
    autobio_id = memory_net.store_memory(
        content="My journey into AI started when I read about neural networks in college",
        memory_type=MemoryType.AUTOBIOGRAPHICAL,
        emotional_tag=EmotionalTag(EmotionalValence.POSITIVE, 0.6, "curiosity"),
        importance=ImportanceLevel.MEDIUM,
        tags={"personal history", "education", "neural networks"}
    )
    
    print(f"Stored memories: {episodic_id}, {semantic_id}, {procedural_id}, {autobio_id}")
    
    # Demonstrate memory retrieval
    print("\n--- Memory Retrieval ---")
    retrieved_memory = memory_net.retrieve_memory(episodic_id)
    if retrieved_memory:
        print(f"Retrieved episodic memory: {retrieved_memory.content}")
        print(f"Emotional tag: {retrieved_memory.emotional_tag.emotion_type} ({retrieved_memory.emotional_tag.valence.name})")
        print(f"Access count: {retrieved_memory.metadata.access_count}")
    
    # Demonstrate semantic search
    print("\n--- Semantic Search ---")
    search_results = memory_net.search_memories(
        query="artificial intelligence and learning",
        max_results=5,
        min_relevance=0.1
    )
    
    print(f"Found {len(search_results)} relevant memories:")
    for memory, relevance in search_results:
        content_str = str(memory.content)
        print(f"- {content_str[:100]}... (relevance: {relevance:.3f})")
    
    # Demonstrate memory association
    print("\n--- Memory Association ---")
    memory_net.associate_memories(episodic_id, semantic_id, strength=0.8)
    print(f"Associated episodic and semantic memories")
    
    # Demonstrate emotional context search
    print("\n--- Emotional Context Search ---")
    emotional_context = EmotionalTag(EmotionalValence.POSITIVE, 0.7, "excitement")
    emotional_results = memory_net.search_memories(
        query="achievement success",
        emotional_context=emotional_context,
        max_results=3
    )
    
    print(f"Found {len(emotional_results)} emotionally relevant memories:")
    for memory, relevance in emotional_results:
        content_str = str(memory.content)
        print(f"- {content_str[:50]}... (relevance: {relevance:.3f})")
    
    # Demonstrate memory consolidation
    print("\n--- Memory Consolidation ---")
    consolidation_success = memory_net.consolidate_memory(episodic_id)
    print(f"Memory consolidation {'successful' if consolidation_success else 'failed'}")
    
    # Add more memories for clustering demonstration
    additional_memories = [
        ("Deep learning uses multiple layers of neural networks", MemoryType.SEMANTIC),
        ("I attended a conference on AI ethics last month", MemoryType.EPISODIC),
        ("Natural language processing helps computers understand text", MemoryType.SEMANTIC),
        ("Learning to debug code systematically", MemoryType.PROCEDURAL),
        ("My first programming language was Python", MemoryType.AUTOBIOGRAPHICAL)
    ]
    
    for content, mem_type in additional_memories:
        memory_net.store_memory(content, mem_type, importance=ImportanceLevel.MEDIUM)
    
    # Demonstrate sleep cycle consolidation
    print("\n--- Sleep Cycle Consolidation ---")
    memory_net.sleep_cycle_consolidation()
    
    # Show statistics
    print("\n--- Memory Network Statistics ---")
    stats = memory_net.get_memory_statistics()
    print(f"Total memories: {stats['total_memories']}")
    print(f"Memory type distribution: {stats['memory_type_distribution']}")
    print(f"Cache hit rate: {stats['cache_hit_rate']:.2%}")
    print(f"Average retrieval time: {stats['average_retrieval_time_ms']:.2f} ms")
    print(f"Consolidations performed: {stats['consolidations_performed']}")
    
    # Demonstrate export
    print("\n--- Memory Export ---")
    memory_net.export_memories("demo_memory_export.json")
    print("Memories exported to demo_memory_export.json")
    
    # Demonstrate temporal decay
    print("\n--- Temporal Decay ---")
    memory_net.apply_temporal_decay(0.5)
    print("Applied temporal decay to all memories")
    
    # Final statistics
    final_stats = memory_net.get_memory_statistics()
    print(f"\nFinal statistics:")
    print(f"Total memories: {final_stats['total_memories']}")
    print(f"Cache utilization: {final_stats['cache_size']}/{memory_net.max_cache_size}")
    
    print("\n=== Enhanced Memory Network Demo Complete ===")


if __name__ == "__main__":
    asyncio.run(demo_enhanced_memory_network())
