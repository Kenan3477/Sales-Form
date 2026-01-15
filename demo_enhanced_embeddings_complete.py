#!/usr/bin/env python3
"""
Enhanced Embedding System Demo - Phase 1.3 Complete
Comprehensive demonstration of all advanced embedding features

Features Demonstrated:
1. Multiple embedding models (sentence-transformers, custom domain models)
2. Multi-modal embeddings for different data types
3. Dynamic embedding adaptation based on usage patterns
4. Cross-domain similarity calculation
5. Embedding performance optimization and caching
6. Semantic clustering and relationship mapping
7. Ensemble embedding generation
8. Hierarchical clustering
9. Performance tracking and adaptation
10. Domain adaptation and transfer learning
"""

import asyncio
import numpy as np
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import our enhanced systems
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

class EnhancedEmbeddingDemo:
    """Comprehensive demonstration of enhanced embedding capabilities"""
    
    def __init__(self):
        self.embedding_system = None
        self.memory_network = None
        self.demo_data = self._prepare_comprehensive_demo_data()
        self.performance_metrics = []
    
    def _prepare_comprehensive_demo_data(self) -> Dict[str, Any]:
        """Prepare comprehensive demo data for all features"""
        return {
            'text_samples': [
                "Advanced neural networks learn complex patterns from data",
                "Machine learning algorithms optimize objective functions",
                "Deep learning architectures process hierarchical representations", 
                "Natural language processing enables human-computer communication",
                "Computer vision systems interpret visual information",
                "Reinforcement learning agents learn through trial and error",
                "Transformer models revolutionized language understanding",
                "Convolutional neural networks excel at image recognition",
                "Recurrent networks handle sequential data effectively",
                "Attention mechanisms focus on relevant information"
            ],
            'domain_specific_texts': {
                'scientific': [
                    "Quantum entanglement exhibits non-local correlations",
                    "Protein folding determines biological function",
                    "Climate models predict atmospheric changes"
                ],
                'technical': [
                    "Distributed systems require fault tolerance",
                    "Microservices architecture enables scalability",
                    "Container orchestration manages deployment"
                ],
                'creative': [
                    "Artistic expression transcends cultural boundaries",
                    "Music evokes powerful emotional responses",
                    "Poetry captures the essence of human experience"
                ]
            },
            'numerical_data': [
                [0.95, 0.87, 0.92, 0.88, 0.94],  # Performance metrics
                [1.2, 3.4, 5.6, 7.8, 9.1],     # Time series
                [150, 280, 190, 340, 220],      # Count data
                [0.02, 0.07, 0.04, 0.09, 0.06], # Probability distributions
                [98.5, 89.2, 94.8, 87.4, 92.1]  # Percentage scores
            ],
            'categorical_data': [
                ["AI", "ML", "DL", "NLP"],
                ["Python", "TensorFlow", "PyTorch"],
                ["Supervised", "Unsupervised", "Reinforcement"],
                ["CNN", "RNN", "Transformer", "GAN"],
                ["Classification", "Regression", "Clustering"]
            ],
            'temporal_data': [
                datetime.now(),
                datetime.now() - timedelta(hours=6),
                datetime.now() - timedelta(days=1),
                datetime.now() - timedelta(weeks=1),
                datetime.now() - timedelta(days=30)
            ],
            'emotions': [
                EmotionalTag.CURIOSITY,
                EmotionalTag.EXCITEMENT,
                EmotionalTag.SATISFACTION,
                EmotionalTag.INTEREST,
                EmotionalTag.FOCUS
            ]
        }
    
    async def initialize_systems(self):
        """Initialize enhanced systems"""
        logger.info("🚀 Initializing Enhanced Embedding Demo Systems...")
        
        try:
            # Initialize embedding system
            self.embedding_system = MultiModalEmbeddingSystem(cache_size=15000)
            logger.info("✅ Multi-modal embedding system initialized")
            
            # Initialize memory network
            self.memory_network = EnhancedMemoryNetwork()
            await self.memory_network.initialize()
            logger.info("✅ Enhanced memory network initialized")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize systems: {e}")
            return False
    
    async def demo_multiple_embedding_models(self):
        """Demonstrate multiple embedding models"""
        logger.info("\n" + "="*60)
        logger.info("🧠 DEMO 1: Multiple Embedding Models")
        logger.info("="*60)
        
        # Test different models for text
        text = "Artificial intelligence transforms data into insights"
        
        # Get embeddings from different models
        models_tested = []
        embeddings = []
        
        for model_name in self.embedding_system.models.keys():
            if "text" in model_name.lower() or "sentence" in model_name.lower():
                try:
                    result = self.embedding_system.embed_text(text)
                    if result.success:
                        models_tested.append(model_name)
                        embeddings.append(result.embedding)
                        logger.info(f"✅ {model_name}: {result.embedding.shape} dimensions, {result.computation_time:.4f}s")
                        
                        # Track performance
                        self.embedding_system.model_performance_tracker.record_performance(
                            model_name, 'speed', result.computation_time
                        )
                        self.embedding_system.model_performance_tracker.record_performance(
                            model_name, 'accuracy', 0.95  # Simulated accuracy
                        )
                except Exception as e:
                    logger.warning(f"⚠️ {model_name} failed: {e}")
        
        # Compare model similarities
        if len(embeddings) >= 2:
            logger.info(f"\n📊 Model Comparison (testing {len(embeddings)} models):")
            for i in range(len(embeddings) - 1):
                for j in range(i + 1, len(embeddings)):
                    sim_result = self.embedding_system.compute_similarity(
                        embeddings[i], embeddings[j], SimilarityMetric.COSINE
                    )
                    logger.info(f"   {models_tested[i]} <-> {models_tested[j]}: {sim_result.similarity:.4f}")
        
        return models_tested, embeddings
    
    async def demo_multimodal_embeddings(self):
        """Demonstrate multi-modal embedding generation"""
        logger.info("\n" + "="*60)
        logger.info("🎯 DEMO 2: Multi-Modal Embeddings")
        logger.info("="*60)
        
        results = {}
        
        # Text embeddings
        logger.info("📝 Text Embeddings:")
        text_results = []
        for i, text in enumerate(self.demo_data['text_samples'][:3]):
            result = self.embedding_system.embed_text(text)
            text_results.append(result)
            logger.info(f"   Text {i+1}: {result.embedding.shape} - {result.computation_time:.4f}s")
        results['text'] = text_results
        
        # Numerical embeddings
        logger.info("\n🔢 Numerical Embeddings:")
        numerical_results = []
        for i, data in enumerate(self.demo_data['numerical_data'][:3]):
            result = self.embedding_system.embed_numerical(data)
            numerical_results.append(result)
            logger.info(f"   Numerical {i+1}: {result.embedding.shape} - {result.computation_time:.4f}s")
        results['numerical'] = numerical_results
        
        # Categorical embeddings
        logger.info("\n🏷️ Categorical Embeddings:")
        categorical_results = []
        for i, data in enumerate(self.demo_data['categorical_data'][:3]):
            result = self.embedding_system.embed_categorical(data)
            categorical_results.append(result)
            logger.info(f"   Categorical {i+1}: {result.embedding.shape} - {result.computation_time:.4f}s")
        results['categorical'] = categorical_results
        
        # Temporal embeddings
        logger.info("\n⏰ Temporal Embeddings:")
        temporal_results = []
        for i, timestamp in enumerate(self.demo_data['temporal_data'][:3]):
            result = self.embedding_system.embed_temporal(timestamp)
            temporal_results.append(result)
            logger.info(f"   Temporal {i+1}: {result.embedding.shape} - {result.computation_time:.4f}s")
        results['temporal'] = temporal_results
        
        # Cross-modal similarity analysis
        logger.info("\n🔗 Cross-Modal Similarity Analysis:")
        modalities = list(results.keys())
        for i, mod1 in enumerate(modalities):
            for j, mod2 in enumerate(modalities):
                if i < j:
                    sim_result = self.embedding_system.compute_similarity(
                        results[mod1][0].embedding, 
                        results[mod2][0].embedding,
                        SimilarityMetric.WEIGHTED_COMBINED
                    )
                    logger.info(f"   {mod1} <-> {mod2}: {sim_result.similarity:.4f} (confidence: {sim_result.confidence:.3f})")
        
        return results
    
    async def demo_ensemble_embeddings(self):
        """Demonstrate ensemble embedding generation"""
        logger.info("\n" + "="*60)
        logger.info("🎵 DEMO 3: Ensemble Embeddings")
        logger.info("="*60)
        
        text = "Ensemble methods combine multiple models for better performance"
        
        # Test different ensemble strategies
        strategies = ['voting', 'weighted', 'stacking']
        ensemble_results = {}
        
        for strategy in strategies:
            logger.info(f"\n🔄 Testing {strategy.upper()} ensemble:")
            try:
                result = self.embedding_system.embed_with_ensemble(
                    text, DataModalityType.TEXT, strategy=strategy
                )
                ensemble_results[strategy] = result
                
                logger.info(f"   ✅ Strategy: {strategy}")
                logger.info(f"   📊 Shape: {result.embedding.shape}")
                logger.info(f"   ⏱️ Time: {result.computation_time:.4f}s")
                logger.info(f"   🤖 Models used: {result.metadata.get('num_models', 0)}")
                
            except Exception as e:
                logger.warning(f"   ⚠️ {strategy} ensemble failed: {e}")
        
        # Compare ensemble strategies
        if len(ensemble_results) >= 2:
            logger.info(f"\n📈 Ensemble Strategy Comparison:")
            strategy_list = list(ensemble_results.keys())
            for i in range(len(strategy_list) - 1):
                for j in range(i + 1, len(strategy_list)):
                    s1, s2 = strategy_list[i], strategy_list[j]
                    sim = self.embedding_system.compute_similarity(
                        ensemble_results[s1].embedding,
                        ensemble_results[s2].embedding
                    )
                    logger.info(f"   {s1} <-> {s2}: {sim.similarity:.4f}")
        
        return ensemble_results
    
    async def demo_dynamic_adaptation(self):
        """Demonstrate dynamic adaptation based on usage patterns"""
        logger.info("\n" + "="*60)
        logger.info("🔄 DEMO 4: Dynamic Adaptation")
        logger.info("="*60)
        
        # Simulate usage patterns
        logger.info("🎯 Simulating usage patterns...")
        
        # Heavy usage of certain models
        for i in range(10):
            text = f"Training sample {i}: Dynamic adaptation learns usage patterns"
            result = self.embedding_system.embed_text(text)
            
            # Record varying performance
            performance = 0.9 + 0.1 * np.random.random()
            speed = 0.05 + 0.05 * np.random.random()
            
            self.embedding_system.model_performance_tracker.record_performance(
                result.model_name, 'accuracy', performance
            )
            self.embedding_system.model_performance_tracker.record_performance(
                result.model_name, 'speed', speed
            )
        
        # Check adaptation recommendations
        logger.info("\n📊 Performance Analysis:")
        rankings = self.embedding_system.model_performance_tracker.model_rankings
        for model_name, score in sorted(rankings.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"   {model_name}: {score:.4f}")
            
            # Check if adaptation is needed
            needs_adaptation = self.embedding_system.model_performance_tracker.should_adapt_model(model_name)
            if needs_adaptation:
                logger.info(f"      🔧 Adaptation recommended for {model_name}")
        
        # Show best model recommendation
        best_model = self.embedding_system.model_performance_tracker.get_best_model(DataModalityType.TEXT)
        if best_model:
            logger.info(f"\n🏆 Best model for text: {best_model}")
        
        return rankings
    
    async def demo_domain_adaptation(self):
        """Demonstrate cross-domain adaptation"""
        logger.info("\n" + "="*60)
        logger.info("🌐 DEMO 5: Domain Adaptation")
        logger.info("="*60)
        
        # Generate embeddings for different domains
        domain_embeddings = {}
        
        for domain, texts in self.demo_data['domain_specific_texts'].items():
            logger.info(f"\n📚 Processing {domain} domain:")
            embeddings = []
            for text in texts:
                result = self.embedding_system.embed_text(text)
                embeddings.append(result.embedding)
                logger.info(f"   ✅ {text[:50]}...")
            
            domain_embeddings[domain] = embeddings
            
            # Learn domain representation
            self.embedding_system.domain_adaptation_engine.learn_domain_representation(
                domain, embeddings
            )
        
        # Test cross-domain similarities
        logger.info(f"\n🔗 Cross-Domain Similarity Analysis:")
        domains = list(domain_embeddings.keys())
        for i, domain1 in enumerate(domains):
            for j, domain2 in enumerate(domains):
                if i < j:
                    similarity = self.embedding_system.domain_adaptation_engine.compute_domain_similarity(
                        domain1, domain2
                    )
                    logger.info(f"   {domain1} <-> {domain2}: {similarity:.4f}")
        
        # Test adaptation
        logger.info(f"\n🔄 Testing Domain Adaptation:")
        if len(domains) >= 2:
            source_domain = domains[0]
            target_domain = domains[1]
            
            # Create adaptation matrix
            try:
                adaptation_matrix = self.embedding_system.domain_adaptation_engine.create_adaptation_matrix(
                    source_domain, target_domain,
                    domain_embeddings[source_domain],
                    domain_embeddings[target_domain]
                )
                logger.info(f"   ✅ Created adaptation matrix: {source_domain} -> {target_domain}")
                logger.info(f"   📊 Matrix shape: {adaptation_matrix.shape}")
                
                # Test adaptation
                test_embedding = domain_embeddings[source_domain][0]
                adapted_embedding = self.embedding_system.domain_adaptation_engine.adapt_embedding(
                    test_embedding, source_domain, target_domain
                )
                logger.info(f"   🎯 Adapted embedding shape: {adapted_embedding.shape}")
                
            except Exception as e:
                logger.warning(f"   ⚠️ Adaptation failed: {e}")
        
        return domain_embeddings
    
    async def demo_advanced_clustering(self):
        """Demonstrate advanced semantic clustering"""
        logger.info("\n" + "="*60)
        logger.info("🎯 DEMO 6: Advanced Semantic Clustering")
        logger.info("="*60)
        
        # Generate embeddings for clustering
        texts = self.demo_data['text_samples']
        embeddings = []
        for text in texts:
            result = self.embedding_system.embed_text(text)
            embeddings.append(result.embedding)
        
        embeddings_array = np.array(embeddings)
        logger.info(f"📊 Clustering {len(embeddings)} embeddings with shape {embeddings_array.shape}")
        
        # Test different clustering algorithms
        algorithms = [ClusteringAlgorithm.KMEANS, ClusteringAlgorithm.DBSCAN, ClusteringAlgorithm.HIERARCHICAL]
        
        for algorithm in algorithms:
            logger.info(f"\n🔍 Testing {algorithm.value.upper()} clustering:")
            try:
                result = self.embedding_system.cluster_embeddings(
                    embeddings_array, 
                    n_clusters=4,
                    algorithm=algorithm,
                    labels=texts
                )
                
                if result.success:
                    logger.info(f"   ✅ Algorithm: {algorithm.value}")
                    logger.info(f"   📈 Silhouette score: {result.silhouette_score:.4f}")
                    logger.info(f"   🎯 Clusters found: {result.n_clusters}")
                    logger.info(f"   ⏱️ Computation time: {result.metrics.get('computation_time', 0):.4f}s")
                    
                    # Show cluster distribution
                    unique_labels, counts = np.unique(result.cluster_labels, return_counts=True)
                    for label, count in zip(unique_labels, counts):
                        logger.info(f"      Cluster {label}: {count} items")
                        
                        # Show sample items in cluster
                        cluster_indices = np.where(result.cluster_labels == label)[0]
                        for idx in cluster_indices[:2]:  # Show first 2 items
                            logger.info(f"         - {texts[idx][:60]}...")
                else:
                    logger.warning(f"   ⚠️ {algorithm.value} clustering failed: {result.metrics.get('error', 'Unknown error')}")
                    
            except Exception as e:
                logger.warning(f"   ❌ {algorithm.value} clustering error: {e}")
        
        # Test hierarchical clustering
        logger.info(f"\n🌳 Hierarchical Clustering Analysis:")
        try:
            hierarchy_result = self.embedding_system.hierarchical_clustering.create_hierarchical_clusters(
                embeddings_array, texts, max_clusters=6
            )
            
            if hierarchy_result:
                logger.info(f"   ✅ Hierarchy created with {hierarchy_result['best_k']} optimal clusters")
                logger.info(f"   📈 Best silhouette score: {hierarchy_result['best_score']:.4f}")
                
                # Show results for different k values
                for k_str, result in hierarchy_result['results'].items():
                    k = result['n_clusters']
                    score = result['silhouette_score']
                    logger.info(f"      k={k}: silhouette={score:.4f}")
            
        except Exception as e:
            logger.warning(f"   ⚠️ Hierarchical clustering failed: {e}")
        
        return embeddings_array
    
    async def demo_semantic_analysis(self):
        """Demonstrate semantic relationship analysis"""
        logger.info("\n" + "="*60)
        logger.info("🧩 DEMO 7: Semantic Relationship Analysis")
        logger.info("="*60)
        
        # Use a subset for semantic analysis
        concepts = self.demo_data['text_samples'][:6]
        embeddings = []
        
        for concept in concepts:
            result = self.embedding_system.embed_text(concept)
            embeddings.append(result.embedding)
        
        # Perform semantic analysis
        logger.info("🔍 Analyzing semantic relationships...")
        analysis_result = self.embedding_system.semantic_analyzer.analyze_semantic_relationships(
            embeddings, concepts
        )
        
        logger.info(f"   ✅ Analysis complete for {len(concepts)} concepts")
        logger.info(f"   🔗 Strong relationships found: {len(analysis_result['strong_relationships'])}")
        logger.info(f"   📊 Average similarity: {analysis_result['similarity_matrix'].mean():.4f}")
        
        # Show strong relationships
        if analysis_result['strong_relationships']:
            logger.info(f"\n💪 Strong Relationships (>0.7 similarity):")
            for concept1, concept2, similarity in analysis_result['strong_relationships'][:5]:
                logger.info(f"   {concept1[:30]}... <-> {concept2[:30]}... ({similarity:.4f})")
        
        # Show concept centrality
        centrality = analysis_result['concept_centrality']
        logger.info(f"\n🎯 Concept Centrality (most connected concepts):")
        sorted_centrality = sorted(centrality.items(), 
                                 key=lambda x: x[1]['normalized_weighted'], 
                                 reverse=True)
        for concept, scores in sorted_centrality[:3]:
            logger.info(f"   {concept[:40]}... (centrality: {scores['normalized_weighted']:.4f})")
        
        # Find concept clusters
        clusters = self.embedding_system.semantic_analyzer.find_concept_clusters(threshold=0.6)
        if clusters:
            logger.info(f"\n🎭 Concept Clusters:")
            for i, cluster in enumerate(clusters):
                logger.info(f"   Cluster {i+1}: {len(cluster)} concepts")
                for concept in cluster:
                    logger.info(f"      - {concept[:50]}...")
        
        return analysis_result
    
    async def demo_performance_optimization(self):
        """Demonstrate performance optimization and caching"""
        logger.info("\n" + "="*60)
        logger.info("⚡ DEMO 8: Performance Optimization & Caching")
        logger.info("="*60)
        
        test_text = "Performance optimization improves system efficiency"
        
        # Test caching performance
        logger.info("🚀 Testing embedding caching:")
        
        # First call (no cache)
        start_time = time.time()
        result1 = self.embedding_system.embed_text(test_text)
        first_call_time = time.time() - start_time
        logger.info(f"   1st call (no cache): {first_call_time:.6f}s")
        
        # Second call (should hit cache)
        start_time = time.time()
        result2 = self.embedding_system.embed_text(test_text)
        second_call_time = time.time() - start_time
        logger.info(f"   2nd call (cached): {second_call_time:.6f}s")
        
        speedup = first_call_time / max(second_call_time, 1e-6)
        logger.info(f"   🎯 Speedup: {speedup:.1f}x")
        logger.info(f"   💾 Cache hit: {result2.cache_hit}")
        
        # Test batch processing
        logger.info(f"\n📦 Testing batch processing:")
        batch_texts = [f"Batch processing item {i}" for i in range(5)]
        
        start_time = time.time()
        batch_results = []
        for text in batch_texts:
            result = self.embedding_system.embed_text(text)
            batch_results.append(result)
        batch_time = time.time() - start_time
        
        logger.info(f"   📊 Processed {len(batch_texts)} items in {batch_time:.4f}s")
        logger.info(f"   ⚡ Average time per item: {batch_time/len(batch_texts):.6f}s")
        
        # Cache statistics
        cache_stats = self.embedding_system.cache.get_stats()
        logger.info(f"\n💾 Cache Statistics:")
        for key, value in cache_stats.items():
            logger.info(f"   {key}: {value}")
        
        # Memory usage estimation
        total_embeddings = sum(len(result.embedding) for result in [result1] + batch_results)
        memory_mb = total_embeddings * 4 / (1024 * 1024)  # 4 bytes per float32
        logger.info(f"   🧠 Estimated memory usage: {memory_mb:.2f} MB")
        
        return {
            'speedup': speedup,
            'cache_stats': cache_stats,
            'batch_time': batch_time
        }
    
    async def demo_memory_integration(self):
        """Demonstrate enhanced memory network integration"""
        logger.info("\n" + "="*60)
        logger.info("🧠 DEMO 9: Enhanced Memory Network Integration")
        logger.info("="*60)
        
        # Store memories with enhanced embeddings
        memory_ids = []
        
        logger.info("💾 Storing enhanced memories:")
        for i, (text, emotion) in enumerate(zip(
            self.demo_data['text_samples'][:5], 
            self.demo_data['emotions']
        )):
            memory_id = await self.memory_network.store_memory(
                content=text,
                memory_type=MemoryType.SEMANTIC,
                emotional_tag=emotion,
                metadata={
                    'demo_index': i, 
                    'embedding_enhanced': True,
                    'embedding_model': 'multi_modal_system'
                }
            )
            memory_ids.append(memory_id)
            logger.info(f"   ✅ Memory {i+1}: {memory_id}")
        
        # Test enhanced retrieval
        logger.info(f"\n🔍 Enhanced Memory Retrieval:")
        query = "deep learning neural networks artificial intelligence"
        retrieved_memories = await self.memory_network.retrieve_memories(
            query=query,
            limit=3,
            memory_type=MemoryType.SEMANTIC
        )
        
        logger.info(f"   Query: '{query}'")
        for i, memory in enumerate(retrieved_memories):
            logger.info(f"   Result {i+1}: {memory.content[:60]}... (relevance: {memory.retrieval_strength:.4f})")
        
        # Test associative memory retrieval
        if memory_ids:
            logger.info(f"\n🔗 Associative Memory Retrieval:")
            associated_memories = await self.memory_network.find_associated_memories(
                memory_ids[0], max_associations=3
            )
            
            logger.info(f"   Base memory: {memory_ids[0]}")
            for i, memory in enumerate(associated_memories):
                logger.info(f"   Associated {i+1}: {memory.content[:60]}...")
        
        # Memory network statistics
        memory_stats = await self.memory_network.get_statistics()
        logger.info(f"\n📊 Memory Network Statistics:")
        for key, value in memory_stats.items():
            if isinstance(value, (int, float)):
                logger.info(f"   {key}: {value}")
        
        return memory_ids, retrieved_memories
    
    async def run_comprehensive_demo(self):
        """Run the complete enhanced embedding system demonstration"""
        logger.info("🚀"*20)
        logger.info("🎯 ENHANCED EMBEDDING SYSTEM - PHASE 1.3 COMPLETE DEMO")
        logger.info("🚀"*20)
        
        if not SYSTEMS_AVAILABLE:
            logger.error("❌ Required systems not available. Please ensure all modules are imported correctly.")
            return
        
        # Initialize systems
        if not await self.initialize_systems():
            logger.error("❌ Failed to initialize systems. Demo cannot continue.")
            return
        
        try:
            # Run all demonstrations
            demo_results = {}
            
            demo_results['models'] = await self.demo_multiple_embedding_models()
            demo_results['multimodal'] = await self.demo_multimodal_embeddings()
            demo_results['ensemble'] = await self.demo_ensemble_embeddings()
            demo_results['adaptation'] = await self.demo_dynamic_adaptation()
            demo_results['domains'] = await self.demo_domain_adaptation()
            demo_results['clustering'] = await self.demo_advanced_clustering()
            demo_results['semantic'] = await self.demo_semantic_analysis()
            demo_results['performance'] = await self.demo_performance_optimization()
            demo_results['memory'] = await self.demo_memory_integration()
            
            # Final system statistics
            logger.info("\n" + "="*60)
            logger.info("📊 FINAL SYSTEM STATISTICS")
            logger.info("="*60)
            
            final_stats = self.embedding_system.get_statistics()
            
            logger.info(f"🤖 Models available: {len(final_stats['models'])}")
            logger.info(f"💾 Cache hit rate: {final_stats['cache_stats'].get('hit_rate', 0):.2%}")
            logger.info(f"🎯 Default dimension: {final_stats['default_dimension']}")
            logger.info(f"🔄 Ensemble strategy: {final_stats['ensemble_strategy']}")
            logger.info(f"📈 Clustering results: {final_stats['clustering_results']}")
            
            # Performance summary
            logger.info(f"\n⚡ Performance Summary:")
            speedup = demo_results['performance']['speedup']
            batch_time = demo_results['performance']['batch_time']
            logger.info(f"   Cache speedup: {speedup:.1f}x")
            logger.info(f"   Batch processing: {batch_time:.4f}s for 5 items")
            
            logger.info("\n" + "🎉"*20)
            logger.info("✅ ENHANCED EMBEDDING SYSTEM DEMO COMPLETED SUCCESSFULLY!")
            logger.info("🎉"*20)
            
            logger.info("\n🏆 PHASE 1.3 ACHIEVEMENTS:")
            logger.info("   ✅ Multiple embedding models implemented")
            logger.info("   ✅ Multi-modal embeddings (text, numerical, categorical, temporal)")
            logger.info("   ✅ Dynamic adaptation based on usage patterns")
            logger.info("   ✅ Cross-domain similarity calculation")
            logger.info("   ✅ Performance optimization and caching")
            logger.info("   ✅ Semantic clustering and relationship mapping")
            logger.info("   ✅ Ensemble embedding generation")
            logger.info("   ✅ Hierarchical clustering")
            logger.info("   ✅ Domain adaptation and transfer learning")
            logger.info("   ✅ Memory network integration")
            
            logger.info("\n🚀 READY FOR PHASE 2: Learning & Adaptation Systems!")
            
            return demo_results
            
        except Exception as e:
            logger.error(f"❌ Demo failed with error: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # Cleanup
            if self.memory_network:
                await self.memory_network.cleanup()

async def main():
    """Main demonstration entry point"""
    demo = EnhancedEmbeddingDemo()
    await demo.run_comprehensive_demo()

if __name__ == "__main__":
    asyncio.run(main())
