#!/usr/bin/env python3
"""
Advanced Embedding System Integration Demo
Demonstrates the enhanced memory network with multi-modal embeddings

This demo showcases:
1. Multi-modal embedding generation (text, numerical, categorical, temporal)
2. Advanced similarity computation with multiple metrics
3. Semantic clustering with different algorithms
4. Memory network integration with enhanced embeddings
5. Performance monitoring and statistics
6. Dynamic adaptation capabilities
"""

import asyncio
import numpy as np
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import our systems
try:
    from enhanced_memory_network import EnhancedMemoryNetwork, MemoryType, EmotionalTag
    from advanced_embedding_system import (
        MultiModalEmbeddingSystem, DataModalityType, SimilarityMetric,
        ClusteringAlgorithm, EmbeddingResult, SimilarityResult, ClusteringResult
    )
    SYSTEMS_AVAILABLE = True
except ImportError as e:
    logger.error(f"Failed to import systems: {e}")
    SYSTEMS_AVAILABLE = False

class AdvancedEmbeddingDemo:
    """Comprehensive demonstration of advanced embedding capabilities"""
    
    def __init__(self):
        self.memory_network = None
        self.embedding_system = None
        self.demo_data = self._prepare_demo_data()
    
    def _prepare_demo_data(self) -> Dict[str, Any]:
        """Prepare diverse demo data for testing"""
        return {
            'text_samples': [
                "The cognitive architecture processes information hierarchically",
                "Machine learning algorithms adapt to new patterns in data",
                "Neural networks exhibit emergent behavior through layer interactions",
                "Artificial intelligence systems require robust memory mechanisms",
                "Embedding spaces capture semantic relationships between concepts",
                "Multi-modal learning integrates different data types effectively",
                "Attention mechanisms focus on relevant information",
                "Working memory maintains active information during processing",
                "Executive control coordinates cognitive processes",
                "Meta-cognition enables self-reflection and adaptation"
            ],
            'numerical_data': [
                [0.85, 0.92, 0.78, 0.96],  # Performance metrics
                [1.2, 3.4, 5.6, 7.8],     # Time series data
                [100, 250, 180, 320],     # Count data
                [0.01, 0.05, 0.03, 0.08], # Probability data
                [95.5, 87.2, 91.8, 89.4]  # Percentage data
            ],
            'categorical_data': [
                ["AI", "Machine Learning", "Deep Learning"],
                ["Text", "Audio", "Video", "Image"],
                ["Classification", "Regression", "Clustering"],
                ["Supervised", "Unsupervised", "Reinforcement"],
                ["CNN", "RNN", "Transformer", "GAN"]
            ],
            'temporal_data': [
                datetime.now(),
                datetime.now() - timedelta(hours=1),
                datetime.now() - timedelta(days=1),
                datetime.now() - timedelta(weeks=1),
                datetime.now() - timedelta(days=30)
            ],
            'emotions': [
                EmotionalTag.CURIOSITY,
                EmotionalTag.SATISFACTION,
                EmotionalTag.INTEREST,
                EmotionalTag.FOCUS,
                EmotionalTag.EXCITEMENT
            ]
        }
    
    async def initialize_systems(self):
        """Initialize memory network and embedding systems"""
        logger.info("Initializing advanced embedding demo systems...")
        
        try:
            # Initialize memory network
            self.memory_network = EnhancedMemoryNetwork()
            await self.memory_network.initialize()
            
            # Get the embedding system from memory network
            self.embedding_system = self.memory_network.embedding_system
            
            logger.info("Systems initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize systems: {e}")
            return False
    
    async def demo_text_embeddings(self):
        """Demonstrate text embedding capabilities"""
        logger.info("\n=== TEXT EMBEDDING DEMONSTRATION ===")
        
        texts = self.demo_data['text_samples'][:5]  # Use first 5 samples
        
        # Generate embeddings
        embeddings = self.embedding_system.embed(texts, modality="text")
        logger.info(f"Generated {len(embeddings)} text embeddings with shape {embeddings.shape}")
        
        # Test similarity computation
        similarities = []
        for i in range(len(embeddings) - 1):
            sim = self.embedding_system.compute_similarity(
                embeddings[i], embeddings[i + 1], metric="cosine"
            )
            similarities.append(sim)
            logger.info(f"Similarity between text {i} and {i+1}: {sim:.4f}")
        
        # Cluster embeddings
        clustering_result = self.embedding_system.cluster_embeddings(
            embeddings, n_clusters=3, algorithm="kmeans"
        )
        
        if clustering_result and 'labels' in clustering_result:
            logger.info(f"Clustering results: {clustering_result['labels']}")
            logger.info(f"Clustering metrics: {clustering_result.get('metrics', {})}")
        
        return embeddings, similarities, clustering_result
    
    async def demo_multimodal_embeddings(self):
        """Demonstrate multi-modal embedding capabilities"""
        logger.info("\n=== MULTI-MODAL EMBEDDING DEMONSTRATION ===")
        
        results = {}
        
        # Text embeddings
        text_embeddings = self.embedding_system.embed(
            self.demo_data['text_samples'][:3], modality="text"
        )
        results['text'] = text_embeddings
        logger.info(f"Text embeddings shape: {text_embeddings.shape}")
        
        # Numerical embeddings
        numerical_embeddings = self.embedding_system.embed(
            [json.dumps(data) for data in self.demo_data['numerical_data'][:3]], 
            modality="numerical"
        )
        results['numerical'] = numerical_embeddings
        logger.info(f"Numerical embeddings shape: {numerical_embeddings.shape}")
        
        # Categorical embeddings
        categorical_embeddings = self.embedding_system.embed(
            [str(data) for data in self.demo_data['categorical_data'][:3]], 
            modality="categorical"
        )
        results['categorical'] = categorical_embeddings
        logger.info(f"Categorical embeddings shape: {categorical_embeddings.shape}")
        
        # Temporal embeddings
        temporal_embeddings = self.embedding_system.embed(
            [dt.isoformat() for dt in self.demo_data['temporal_data'][:3]], 
            modality="temporal"
        )
        results['temporal'] = temporal_embeddings
        logger.info(f"Temporal embeddings shape: {temporal_embeddings.shape}")
        
        # Cross-modal similarity analysis
        logger.info("\nCross-modal similarity analysis:")
        modalities = list(results.keys())
        for i, mod1 in enumerate(modalities):
            for j, mod2 in enumerate(modalities):
                if i < j:
                    sim = self.embedding_system.compute_similarity(
                        results[mod1][0], results[mod2][0]
                    )
                    logger.info(f"Similarity {mod1} <-> {mod2}: {sim:.4f}")
        
        return results
    
    async def demo_memory_integration(self):
        """Demonstrate enhanced memory network integration"""
        logger.info("\n=== MEMORY NETWORK INTEGRATION DEMONSTRATION ===")
        
        # Store diverse memories with enhanced embeddings
        memory_ids = []
        
        for i, (text, emotion) in enumerate(zip(
            self.demo_data['text_samples'][:5], 
            self.demo_data['emotions']
        )):
            memory_id = await self.memory_network.store_memory(
                content=text,
                memory_type=MemoryType.SEMANTIC,
                emotional_tag=emotion,
                metadata={'demo_index': i, 'embedding_enhanced': True}
            )
            memory_ids.append(memory_id)
            logger.info(f"Stored memory {i+1}: {memory_id}")
        
        # Test enhanced retrieval
        query = "cognitive processes and neural networks"
        logger.info(f"\nRetrieving memories for query: '{query}'")
        
        retrieved_memories = await self.memory_network.retrieve_memories(
            query=query,
            limit=3,
            memory_type=MemoryType.SEMANTIC
        )
        
        for i, memory in enumerate(retrieved_memories):
            logger.info(f"Retrieved {i+1}: {memory.content[:100]}... (similarity: {memory.retrieval_strength:.4f})")
        
        # Test associative retrieval
        if memory_ids:
            associated_memories = await self.memory_network.find_associated_memories(
                memory_ids[0], max_associations=3
            )
            logger.info(f"\nAssociated memories for {memory_ids[0]}:")
            for memory in associated_memories:
                logger.info(f"  - {memory.content[:100]}...")
        
        return memory_ids, retrieved_memories
    
    async def demo_clustering_analysis(self):
        """Demonstrate advanced clustering capabilities"""
        logger.info("\n=== CLUSTERING ANALYSIS DEMONSTRATION ===")
        
        # Get all text embeddings
        texts = self.demo_data['text_samples']
        embeddings = self.embedding_system.embed(texts, modality="text")
        
        # Test different clustering algorithms
        algorithms = ["kmeans", "dbscan"]  # Add hierarchical when supported
        
        for algorithm in algorithms:
            try:
                logger.info(f"\nTesting {algorithm.upper()} clustering:")
                
                n_clusters = 4 if algorithm == "kmeans" else None
                clustering_result = self.embedding_system.cluster_embeddings(
                    embeddings, 
                    n_clusters=n_clusters or 4, 
                    algorithm=algorithm
                )
                
                if clustering_result and 'labels' in clustering_result:
                    labels = clustering_result['labels']
                    unique_labels = np.unique(labels)
                    
                    logger.info(f"Found {len(unique_labels)} clusters")
                    
                    # Show cluster assignments
                    for cluster_id in unique_labels:
                        cluster_texts = [texts[i] for i in range(len(texts)) if labels[i] == cluster_id]
                        logger.info(f"Cluster {cluster_id}: {len(cluster_texts)} items")
                        for text in cluster_texts[:2]:  # Show first 2 items
                            logger.info(f"  - {text[:80]}...")
                    
                    # Show metrics if available
                    metrics = clustering_result.get('metrics', {})
                    if metrics:
                        logger.info(f"Clustering metrics: {metrics}")
                
            except Exception as e:
                logger.warning(f"Clustering with {algorithm} failed: {e}")
        
        return embeddings, clustering_result
    
    async def demo_performance_monitoring(self):
        """Demonstrate performance monitoring and statistics"""
        logger.info("\n=== PERFORMANCE MONITORING DEMONSTRATION ===")
        
        # Get embedding system statistics
        stats = self.embedding_system.get_statistics()
        logger.info("Embedding System Statistics:")
        for key, value in stats.items():
            logger.info(f"  {key}: {value}")
        
        # Get memory network statistics
        memory_stats = await self.memory_network.get_statistics()
        logger.info("\nMemory Network Statistics:")
        for key, value in memory_stats.items():
            logger.info(f"  {key}: {value}")
        
        # Performance timing test
        import time
        
        logger.info("\nPerformance timing test:")
        test_texts = ["Test text for performance measurement"] * 10
        
        start_time = time.time()
        embeddings = self.embedding_system.embed(test_texts)
        end_time = time.time()
        
        logger.info(f"Embedded {len(test_texts)} texts in {end_time - start_time:.4f} seconds")
        logger.info(f"Average time per embedding: {(end_time - start_time) / len(test_texts):.4f} seconds")
        
        return stats, memory_stats
    
    async def run_comprehensive_demo(self):
        """Run the complete demonstration"""
        logger.info("🚀 Starting Advanced Embedding System Comprehensive Demo")
        
        if not SYSTEMS_AVAILABLE:
            logger.error("Required systems not available. Please ensure all modules are imported correctly.")
            return
        
        # Initialize systems
        if not await self.initialize_systems():
            logger.error("Failed to initialize systems. Demo cannot continue.")
            return
        
        try:
            # Run all demonstrations
            await self.demo_text_embeddings()
            await self.demo_multimodal_embeddings()
            await self.demo_memory_integration()
            await self.demo_clustering_analysis()
            await self.demo_performance_monitoring()
            
            logger.info("\n✅ Advanced Embedding System Demo completed successfully!")
            logger.info("🎯 Key achievements demonstrated:")
            logger.info("   • Multi-modal embedding generation")
            logger.info("   • Advanced similarity computation")
            logger.info("   • Semantic clustering capabilities")
            logger.info("   • Memory network integration")
            logger.info("   • Performance monitoring")
            logger.info("   • Cross-domain similarity analysis")
            
        except Exception as e:
            logger.error(f"Demo failed with error: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # Cleanup
            if self.memory_network:
                await self.memory_network.cleanup()

async def main():
    """Main demonstration entry point"""
    demo = AdvancedEmbeddingDemo()
    await demo.run_comprehensive_demo()

if __name__ == "__main__":
    asyncio.run(main())
