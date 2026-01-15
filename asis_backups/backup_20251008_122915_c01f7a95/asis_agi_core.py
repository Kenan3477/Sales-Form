#!/usr/bin/env python3
"""
ASIS AGI Core Architecture
=========================
Unified Intelligence Framework for Advanced Autonomous Intelligence

This module implements:
1. Unified Knowledge Graph Integration
2. Cross-Domain Reasoning Engine
3. Meta-Cognitive Controller
4. Integration with Current ASIS Systems

Author: ASIS Development Team
Version: 1.0.0
Date: September 26, 2025
"""

import os
import sys
import json
import sqlite3
import threading
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from collections import defaultdict, deque
import hashlib
import numpy as np
from enum import Enum

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class ReasoningStrategy(Enum):
    """Available reasoning strategies"""
    ANALYTICAL = "analytical"
    ANALOGICAL = "analogical"
    CREATIVE = "creative"
    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"
    ABDUCTIVE = "abductive"
    HOLISTIC = "holistic"

class KnowledgeDomain(Enum):
    """Knowledge domains in the unified graph"""
    PATTERNS = "patterns"
    LEARNING = "learning"
    RESEARCH = "research"
    META_LEARNING = "meta_learning"
    REASONING = "reasoning"
    EXPERIENCE = "experience"
    CONTEXT = "context"

@dataclass
class KnowledgeNode:
    """Represents a node in the unified knowledge graph"""
    id: str
    domain: KnowledgeDomain
    content: Dict[str, Any]
    confidence: float
    timestamp: datetime
    connections: Set[str] = field(default_factory=set)
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    embedding_vector: Optional[List[float]] = None
    
    def __post_init__(self):
        if self.last_accessed is None:
            self.last_accessed = self.timestamp

@dataclass
class KnowledgeConnection:
    """Represents a connection between knowledge nodes"""
    source_id: str
    target_id: str
    connection_type: str
    strength: float
    created: datetime
    last_reinforced: datetime
    reinforcement_count: int = 1

@dataclass
class ReasoningContext:
    """Context for reasoning operations"""
    problem_type: str
    domain: KnowledgeDomain
    complexity_level: int
    time_constraint: Optional[float]
    quality_requirement: float
    available_strategies: List[ReasoningStrategy]
    context_data: Dict[str, Any] = field(default_factory=dict)

class UnifiedKnowledgeGraph:
    """
    Unified Knowledge Graph Integration System
    Replaces separate databases with integrated knowledge representation
    """
    
    def __init__(self, database_path: str = "asis_unified_knowledge.db"):
        self.database_path = database_path
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.connections: Dict[str, KnowledgeConnection] = {}
        self.domain_indices: Dict[KnowledgeDomain, Set[str]] = defaultdict(set)
        self.embedding_cache: Dict[str, List[float]] = {}
        self.lock = threading.RLock()
        
        self._initialize_database()
        self._load_existing_knowledge()
        
    def _initialize_database(self):
        """Initialize the unified knowledge database"""
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            
            # Knowledge nodes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge_nodes (
                    id TEXT PRIMARY KEY,
                    domain TEXT NOT NULL,
                    content TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    timestamp TEXT NOT NULL,
                    access_count INTEGER DEFAULT 0,
                    last_accessed TEXT,
                    embedding_vector TEXT
                )
            ''')
            
            # Knowledge connections table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge_connections (
                    id TEXT PRIMARY KEY,
                    source_id TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    connection_type TEXT NOT NULL,
                    strength REAL NOT NULL,
                    created TEXT NOT NULL,
                    last_reinforced TEXT NOT NULL,
                    reinforcement_count INTEGER DEFAULT 1,
                    FOREIGN KEY (source_id) REFERENCES knowledge_nodes (id),
                    FOREIGN KEY (target_id) REFERENCES knowledge_nodes (id)
                )
            ''')
            
            # Create indices for performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_nodes_domain ON knowledge_nodes (domain)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_nodes_timestamp ON knowledge_nodes (timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_connections_source ON knowledge_connections (source_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_connections_target ON knowledge_connections (target_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_connections_type ON knowledge_connections (connection_type)')
            
            conn.commit()
    
    def _load_existing_knowledge(self):
        """Load existing knowledge from legacy databases"""
        print("🧠 Loading existing ASIS knowledge into unified graph...")
        
        # Load from patterns database
        self._migrate_patterns_database()
        
        # Load from realtime learning database
        self._migrate_realtime_database()
        
        # Load from meta-learning database
        self._migrate_meta_learning_database()
        
        # Load from research database
        self._migrate_research_database()
        
        print(f"✅ Unified knowledge graph initialized with {len(self.nodes)} nodes")
    
    def _migrate_patterns_database(self):
        """Migrate pattern recognition data to unified graph"""
        try:
            with sqlite3.connect('asis_patterns_fixed.db') as conn:
                cursor = conn.cursor()
                
                # Get all tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                
                for table_name in tables:
                    if table_name == 'sqlite_sequence':
                        continue
                        
                    try:
                        cursor.execute(f"SELECT * FROM {table_name}")
                        rows = cursor.fetchall()
                        
                        # Get column names
                        cursor.execute(f"PRAGMA table_info({table_name})")
                        columns = [col[1] for col in cursor.fetchall()]
                        
                        for row in rows:
                            data = dict(zip(columns, row))
                            
                            node_id = f"pattern_{table_name}_{data.get('id', uuid.uuid4().hex[:8])}"
                            
                            knowledge_node = KnowledgeNode(
                                id=node_id,
                                domain=KnowledgeDomain.PATTERNS,
                                content={
                                    'table': table_name,
                                    'data': data,
                                    'source': 'asis_patterns_fixed.db'
                                },
                                confidence=data.get('confidence_score', 0.8),
                                timestamp=datetime.now()
                            )
                            
                            self._add_node(knowledge_node)
                            
                    except Exception as e:
                        print(f"Warning: Could not migrate table {table_name}: {e}")
                        
        except Exception as e:
            print(f"Warning: Could not migrate patterns database: {e}")
    
    def _migrate_realtime_database(self):
        """Migrate realtime learning data to unified graph"""
        try:
            with sqlite3.connect('asis_realtime_learning.db') as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                
                for table_name in tables:
                    if table_name == 'sqlite_sequence':
                        continue
                        
                    try:
                        cursor.execute(f"SELECT * FROM {table_name} LIMIT 100")  # Limit for performance
                        rows = cursor.fetchall()
                        
                        cursor.execute(f"PRAGMA table_info({table_name})")
                        columns = [col[1] for col in cursor.fetchall()]
                        
                        for row in rows:
                            data = dict(zip(columns, row))
                            
                            node_id = f"learning_{table_name}_{data.get('id', uuid.uuid4().hex[:8])}"
                            
                            knowledge_node = KnowledgeNode(
                                id=node_id,
                                domain=KnowledgeDomain.LEARNING,
                                content={
                                    'table': table_name,
                                    'data': data,
                                    'source': 'asis_realtime_learning.db'
                                },
                                confidence=0.9,
                                timestamp=datetime.now()
                            )
                            
                            self._add_node(knowledge_node)
                            
                    except Exception as e:
                        print(f"Warning: Could not migrate learning table {table_name}: {e}")
                        
        except Exception as e:
            print(f"Warning: Could not migrate realtime learning database: {e}")
    
    def _migrate_meta_learning_database(self):
        """Migrate meta-learning data to unified graph"""
        try:
            with sqlite3.connect('asis_adaptive_meta_learning.db') as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                
                for table_name in tables:
                    if table_name == 'sqlite_sequence':
                        continue
                        
                    try:
                        cursor.execute(f"SELECT * FROM {table_name} LIMIT 50")
                        rows = cursor.fetchall()
                        
                        cursor.execute(f"PRAGMA table_info({table_name})")
                        columns = [col[1] for col in cursor.fetchall()]
                        
                        for row in rows:
                            data = dict(zip(columns, row))
                            
                            node_id = f"meta_{table_name}_{data.get('id', uuid.uuid4().hex[:8])}"
                            
                            knowledge_node = KnowledgeNode(
                                id=node_id,
                                domain=KnowledgeDomain.META_LEARNING,
                                content={
                                    'table': table_name,
                                    'data': data,
                                    'source': 'asis_adaptive_meta_learning.db'
                                },
                                confidence=0.85,
                                timestamp=datetime.now()
                            )
                            
                            self._add_node(knowledge_node)
                            
                    except Exception as e:
                        print(f"Warning: Could not migrate meta-learning table {table_name}: {e}")
                        
        except Exception as e:
            print(f"Warning: Could not migrate meta-learning database: {e}")
    
    def _migrate_research_database(self):
        """Migrate research data to unified graph"""
        try:
            with sqlite3.connect('asis_autonomous_research_fixed.db') as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                
                for table_name in tables:
                    if table_name == 'sqlite_sequence':
                        continue
                        
                    try:
                        cursor.execute(f"SELECT * FROM {table_name} LIMIT 30")
                        rows = cursor.fetchall()
                        
                        cursor.execute(f"PRAGMA table_info({table_name})")
                        columns = [col[1] for col in cursor.fetchall()]
                        
                        for row in rows:
                            data = dict(zip(columns, row))
                            
                            node_id = f"research_{table_name}_{data.get('id', uuid.uuid4().hex[:8])}"
                            
                            knowledge_node = KnowledgeNode(
                                id=node_id,
                                domain=KnowledgeDomain.RESEARCH,
                                content={
                                    'table': table_name,
                                    'data': data,
                                    'source': 'asis_autonomous_research_fixed.db'
                                },
                                confidence=0.8,
                                timestamp=datetime.now()
                            )
                            
                            self._add_node(knowledge_node)
                            
                    except Exception as e:
                        print(f"Warning: Could not migrate research table {table_name}: {e}")
                        
        except Exception as e:
            print(f"Warning: Could not migrate research database: {e}")
    
    def _add_node(self, node: KnowledgeNode):
        """Add a node to the knowledge graph"""
        with self.lock:
            self.nodes[node.id] = node
            self.domain_indices[node.domain].add(node.id)
    
    def add_knowledge(self, domain: KnowledgeDomain, content: Dict[str, Any], 
                     confidence: float = 0.8) -> str:
        """Add new knowledge to the unified graph"""
        node_id = f"{domain.value}_{uuid.uuid4().hex[:12]}"
        
        knowledge_node = KnowledgeNode(
            id=node_id,
            domain=domain,
            content=content,
            confidence=confidence,
            timestamp=datetime.now()
        )
        
        self._add_node(knowledge_node)
        self._create_automatic_connections(knowledge_node)
        self._persist_node(knowledge_node)
        
        return node_id
    
    def _create_automatic_connections(self, new_node: KnowledgeNode):
        """Create automatic connections based on content similarity"""
        # Find related nodes in different domains for cross-domain linking
        for domain in KnowledgeDomain:
            if domain == new_node.domain:
                continue
                
            related_nodes = self._find_related_nodes(new_node, domain, limit=3)
            
            for related_node_id, similarity in related_nodes:
                if similarity > 0.6:  # Threshold for automatic connection
                    self._create_connection(
                        new_node.id, 
                        related_node_id, 
                        "cross_domain_similarity",
                        similarity
                    )
    
    def _find_related_nodes(self, node: KnowledgeNode, target_domain: KnowledgeDomain, 
                           limit: int = 5) -> List[Tuple[str, float]]:
        """Find related nodes in a specific domain"""
        related = []
        
        for target_node_id in self.domain_indices[target_domain]:
            target_node = self.nodes[target_node_id]
            similarity = self._calculate_content_similarity(node, target_node)
            
            if similarity > 0.3:  # Minimum similarity threshold
                related.append((target_node_id, similarity))
        
        # Sort by similarity and return top matches
        related.sort(key=lambda x: x[1], reverse=True)
        return related[:limit]
    
    def _calculate_content_similarity(self, node1: KnowledgeNode, node2: KnowledgeNode) -> float:
        """Calculate similarity between two knowledge nodes"""
        # Simple keyword-based similarity (can be enhanced with embeddings)
        content1_str = json.dumps(node1.content, default=str).lower()
        content2_str = json.dumps(node2.content, default=str).lower()
        
        # Extract key terms
        terms1 = set(content1_str.split())
        terms2 = set(content2_str.split())
        
        if not terms1 or not terms2:
            return 0.0
        
        # Jaccard similarity
        intersection = len(terms1.intersection(terms2))
        union = len(terms1.union(terms2))
        
        return intersection / union if union > 0 else 0.0
    
    def _create_connection(self, source_id: str, target_id: str, 
                          connection_type: str, strength: float):
        """Create a connection between two nodes"""
        connection_id = f"{source_id}_{target_id}_{connection_type}"
        
        connection = KnowledgeConnection(
            source_id=source_id,
            target_id=target_id,
            connection_type=connection_type,
            strength=strength,
            created=datetime.now(),
            last_reinforced=datetime.now()
        )
        
        with self.lock:
            self.connections[connection_id] = connection
            self.nodes[source_id].connections.add(target_id)
            self.nodes[target_id].connections.add(source_id)
    
    def _persist_node(self, node: KnowledgeNode):
        """Persist a node to the database"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO knowledge_nodes 
                    (id, domain, content, confidence, timestamp, access_count, last_accessed, embedding_vector)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    node.id,
                    node.domain.value,
                    json.dumps(node.content, default=str),
                    node.confidence,
                    node.timestamp.isoformat(),
                    node.access_count,
                    node.last_accessed.isoformat() if node.last_accessed else None,
                    json.dumps(node.embedding_vector) if node.embedding_vector else None
                ))
                conn.commit()
        except Exception as e:
            print(f"Warning: Could not persist node {node.id}: {e}")
    
    def get_cross_domain_insights(self, query: str, domains: List[KnowledgeDomain] = None) -> List[Dict[str, Any]]:
        """Get insights that span multiple domains"""
        if domains is None:
            domains = list(KnowledgeDomain)
        
        insights = []
        query_terms = set(query.lower().split())
        
        # Find relevant nodes across domains
        for domain in domains:
            for node_id in self.domain_indices[domain]:
                node = self.nodes[node_id]
                content_str = json.dumps(node.content, default=str).lower()
                content_terms = set(content_str.split())
                
                # Calculate relevance
                relevance = len(query_terms.intersection(content_terms)) / len(query_terms) if query_terms else 0
                
                if relevance > 0.2:  # Relevance threshold
                    # Find cross-domain connections
                    cross_domain_connections = []
                    for connected_id in node.connections:
                        connected_node = self.nodes[connected_id]
                        if connected_node.domain != domain:
                            cross_domain_connections.append({
                                'domain': connected_node.domain.value,
                                'content': connected_node.content,
                                'confidence': connected_node.confidence
                            })
                    
                    if cross_domain_connections:  # Only include nodes with cross-domain connections
                        insights.append({
                            'node_id': node_id,
                            'domain': domain.value,
                            'content': node.content,
                            'confidence': node.confidence,
                            'relevance': relevance,
                            'cross_domain_connections': cross_domain_connections
                        })
        
        # Sort by relevance and cross-domain connection count
        insights.sort(key=lambda x: (x['relevance'], len(x['cross_domain_connections'])), reverse=True)
        return insights[:10]  # Return top 10 insights
    
    def get_knowledge_statistics(self) -> Dict[str, Any]:
        """Get statistics about the unified knowledge graph"""
        stats = {
            'total_nodes': len(self.nodes),
            'total_connections': len(self.connections),
            'nodes_by_domain': {},
            'cross_domain_connections': 0,
            'average_node_confidence': 0.0,
            'most_connected_domains': [],
            'knowledge_growth_rate': 0.0
        }
        
        # Count nodes by domain
        for domain in KnowledgeDomain:
            stats['nodes_by_domain'][domain.value] = len(self.domain_indices[domain])
        
        # Calculate cross-domain connections
        for connection in self.connections.values():
            source_domain = self.nodes[connection.source_id].domain
            target_domain = self.nodes[connection.target_id].domain
            if source_domain != target_domain:
                stats['cross_domain_connections'] += 1
        
        # Calculate average confidence
        if self.nodes:
            total_confidence = sum(node.confidence for node in self.nodes.values())
            stats['average_node_confidence'] = total_confidence / len(self.nodes)
        
        return stats


class CrossDomainReasoningEngine:
    """
    Cross-Domain Reasoning Engine
    Implements reasoning that spans multiple knowledge domains
    """
    
    def __init__(self, knowledge_graph: UnifiedKnowledgeGraph):
        self.knowledge_graph = knowledge_graph
        self.reasoning_history = deque(maxlen=1000)
        self.strategy_performance = defaultdict(list)
        self.lock = threading.RLock()
    
    def apply_cross_domain_reasoning(self, problem: str, context: ReasoningContext) -> Dict[str, Any]:
        """Apply cross-domain reasoning to solve a problem"""
        reasoning_id = uuid.uuid4().hex[:12]
        start_time = time.time()
        
        print(f"🧠 Starting cross-domain reasoning for: {problem[:50]}...")
        
        # Step 1: Analyze the problem and identify relevant domains
        relevant_domains = self._identify_relevant_domains(problem, context)
        
        # Step 2: Gather knowledge from multiple domains
        cross_domain_knowledge = self._gather_cross_domain_knowledge(problem, relevant_domains)
        
        # Step 3: Apply analogical reasoning across domains
        analogies = self._find_cross_domain_analogies(problem, cross_domain_knowledge)
        
        # Step 4: Synthesize insights from different domains
        synthesized_insights = self._synthesize_domain_insights(cross_domain_knowledge, analogies)
        
        # Step 5: Generate reasoning-based solution
        solution = self._generate_reasoned_solution(problem, synthesized_insights, context)
        
        reasoning_time = time.time() - start_time
        
        # Record reasoning session
        reasoning_record = {
            'id': reasoning_id,
            'problem': problem,
            'context': context,
            'relevant_domains': [d.value for d in relevant_domains],
            'knowledge_nodes_used': len(cross_domain_knowledge),
            'analogies_found': len(analogies),
            'solution': solution,
            'reasoning_time': reasoning_time,
            'timestamp': datetime.now(),
            'quality_score': self._assess_solution_quality(solution, context)
        }
        
        self.reasoning_history.append(reasoning_record)
        
        print(f"✅ Cross-domain reasoning completed in {reasoning_time:.2f}s")
        
        return reasoning_record
    
    def _identify_relevant_domains(self, problem: str, context: ReasoningContext) -> List[KnowledgeDomain]:
        """Identify which knowledge domains are relevant to the problem"""
        relevant_domains = []
        problem_lower = problem.lower()
        
        # Primary domain from context
        if context.domain:
            relevant_domains.append(context.domain)
        
        # Domain keyword mapping
        domain_keywords = {
            KnowledgeDomain.PATTERNS: ['pattern', 'recognize', 'detect', 'identify', 'classify'],
            KnowledgeDomain.LEARNING: ['learn', 'adapt', 'improve', 'train', 'develop'],
            KnowledgeDomain.RESEARCH: ['research', 'investigate', 'explore', 'analyze', 'study'],
            KnowledgeDomain.META_LEARNING: ['meta', 'strategy', 'approach', 'method', 'optimize'],
            KnowledgeDomain.REASONING: ['reason', 'logic', 'infer', 'deduce', 'conclude'],
            KnowledgeDomain.EXPERIENCE: ['experience', 'history', 'past', 'previous', 'memory'],
            KnowledgeDomain.CONTEXT: ['context', 'situation', 'environment', 'circumstances']
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in problem_lower for keyword in keywords):
                if domain not in relevant_domains:
                    relevant_domains.append(domain)
        
        # Ensure we have at least 2 domains for cross-domain reasoning
        if len(relevant_domains) < 2:
            # Add complementary domains
            for domain in KnowledgeDomain:
                if domain not in relevant_domains:
                    relevant_domains.append(domain)
                    if len(relevant_domains) >= 3:
                        break
        
        return relevant_domains[:4]  # Limit to 4 domains for performance
    
    def _gather_cross_domain_knowledge(self, problem: str, domains: List[KnowledgeDomain]) -> List[Dict[str, Any]]:
        """Gather relevant knowledge from multiple domains"""
        cross_domain_knowledge = []
        
        for domain in domains:
            # Get relevant nodes from this domain
            domain_nodes = []
            problem_terms = set(problem.lower().split())
            
            for node_id in self.knowledge_graph.domain_indices[domain]:
                node = self.knowledge_graph.nodes[node_id]
                content_str = json.dumps(node.content, default=str).lower()
                content_terms = set(content_str.split())
                
                # Calculate relevance
                relevance = len(problem_terms.intersection(content_terms)) / len(problem_terms) if problem_terms else 0
                
                if relevance > 0.1:  # Minimum relevance threshold
                    domain_nodes.append({
                        'node': node,
                        'relevance': relevance,
                        'domain': domain
                    })
            
            # Sort by relevance and take top nodes
            domain_nodes.sort(key=lambda x: x['relevance'], reverse=True)
            cross_domain_knowledge.extend(domain_nodes[:5])  # Top 5 from each domain
        
        return cross_domain_knowledge
    
    def _find_cross_domain_analogies(self, problem: str, knowledge: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find analogies between different domains"""
        analogies = []
        
        # Group knowledge by domain
        domain_groups = defaultdict(list)
        for item in knowledge:
            domain_groups[item['domain']].append(item)
        
        # Find analogies between domain pairs
        domains = list(domain_groups.keys())
        for i in range(len(domains)):
            for j in range(i + 1, len(domains)):
                domain1, domain2 = domains[i], domains[j]
                
                # Compare nodes between domains
                for item1 in domain_groups[domain1][:3]:  # Limit for performance
                    for item2 in domain_groups[domain2][:3]:
                        similarity = self._calculate_analogy_strength(item1['node'], item2['node'])
                        
                        if similarity > 0.4:  # Analogy threshold
                            analogies.append({
                                'domain1': domain1.value,
                                'domain2': domain2.value,
                                'node1': item1['node'],
                                'node2': item2['node'],
                                'similarity': similarity,
                                'analogy_type': self._classify_analogy_type(item1['node'], item2['node'])
                            })
        
        # Sort by similarity strength
        analogies.sort(key=lambda x: x['similarity'], reverse=True)
        return analogies[:10]  # Top 10 analogies
    
    def _calculate_analogy_strength(self, node1: KnowledgeNode, node2: KnowledgeNode) -> float:
        """Calculate the strength of analogy between two nodes"""
        # Extract structural and semantic features
        content1_str = json.dumps(node1.content, default=str).lower()
        content2_str = json.dumps(node2.content, default=str).lower()
        
        # Keyword similarity
        terms1 = set(content1_str.split())
        terms2 = set(content2_str.split())
        
        keyword_similarity = len(terms1.intersection(terms2)) / len(terms1.union(terms2)) if terms1.union(terms2) else 0
        
        # Confidence similarity
        confidence_similarity = 1 - abs(node1.confidence - node2.confidence)
        
        # Connection pattern similarity
        connection_similarity = len(node1.connections.intersection(node2.connections)) / len(node1.connections.union(node2.connections)) if node1.connections.union(node2.connections) else 0
        
        # Weighted combination
        analogy_strength = (
            0.5 * keyword_similarity +
            0.3 * confidence_similarity +
            0.2 * connection_similarity
        )
        
        return analogy_strength
    
    def _classify_analogy_type(self, node1: KnowledgeNode, node2: KnowledgeNode) -> str:
        """Classify the type of analogy between nodes"""
        content1 = json.dumps(node1.content, default=str).lower()
        content2 = json.dumps(node2.content, default=str).lower()
        
        # Structural analogy
        if 'structure' in content1 and 'structure' in content2:
            return 'structural'
        
        # Functional analogy
        if any(word in content1 and word in content2 for word in ['function', 'purpose', 'goal']):
            return 'functional'
        
        # Causal analogy
        if any(word in content1 and word in content2 for word in ['cause', 'effect', 'result']):
            return 'causal'
        
        # Process analogy
        if any(word in content1 and word in content2 for word in ['process', 'method', 'procedure']):
            return 'process'
        
        return 'semantic'  # Default
    
    def _synthesize_domain_insights(self, knowledge: List[Dict[str, Any]], analogies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize insights from different domains"""
        synthesis = {
            'primary_insights': [],
            'cross_domain_patterns': [],
            'analogical_insights': [],
            'confidence_distribution': defaultdict(list),
            'knowledge_convergence_points': []
        }
        
        # Extract primary insights from each domain
        domain_insights = defaultdict(list)
        for item in knowledge:
            domain = item['domain']
            node = item['node']
            relevance = item['relevance']
            
            insight = {
                'content': node.content,
                'confidence': node.confidence,
                'relevance': relevance,
                'connections': len(node.connections)
            }
            
            domain_insights[domain].append(insight)
            synthesis['confidence_distribution'][domain.value].append(node.confidence)
        
        # Identify patterns across domains
        for domain, insights in domain_insights.items():
            if len(insights) >= 2:
                synthesis['primary_insights'].append({
                    'domain': domain.value,
                    'insight_count': len(insights),
                    'average_confidence': sum(i['confidence'] for i in insights) / len(insights),
                    'top_insights': sorted(insights, key=lambda x: x['relevance'], reverse=True)[:3]
                })
        
        # Process analogical insights
        for analogy in analogies:
            synthesis['analogical_insights'].append({
                'domains': [analogy['domain1'], analogy['domain2']],
                'analogy_type': analogy['analogy_type'],
                'strength': analogy['similarity'],
                'insight': f"Pattern from {analogy['domain1']} domain applies to {analogy['domain2']} domain"
            })
        
        # Find knowledge convergence points
        convergence_threshold = 0.7
        for analogy in analogies:
            if analogy['similarity'] > convergence_threshold:
                synthesis['knowledge_convergence_points'].append({
                    'domains': [analogy['domain1'], analogy['domain2']],
                    'convergence_strength': analogy['similarity'],
                    'convergence_type': analogy['analogy_type']
                })
        
        return synthesis
    
    def _generate_reasoned_solution(self, problem: str, insights: Dict[str, Any], context: ReasoningContext) -> Dict[str, Any]:
        """Generate a solution based on cross-domain reasoning"""
        solution = {
            'problem': problem,
            'reasoning_approach': 'cross-domain',
            'solution_components': [],
            'confidence': 0.0,
            'supporting_evidence': [],
            'alternative_approaches': [],
            'implementation_steps': []
        }
        
        # Generate solution components from primary insights
        for domain_insight in insights['primary_insights']:
            domain = domain_insight['domain']
            top_insights = domain_insight['top_insights']
            
            for insight in top_insights:
                solution['solution_components'].append({
                    'source_domain': domain,
                    'component': f"Apply {domain} knowledge: {str(insight['content'])[:100]}...",
                    'confidence': insight['confidence'],
                    'relevance': insight['relevance']
                })
        
        # Add analogical reasoning solutions
        for analogy_insight in insights['analogical_insights']:
            if analogy_insight['strength'] > 0.5:
                solution['solution_components'].append({
                    'source_domains': analogy_insight['domains'],
                    'component': f"Analogical reasoning: {analogy_insight['insight']}",
                    'confidence': analogy_insight['strength'],
                    'reasoning_type': 'analogical'
                })
        
        # Calculate overall solution confidence
        if solution['solution_components']:
            total_confidence = sum(comp['confidence'] for comp in solution['solution_components'])
            solution['confidence'] = total_confidence / len(solution['solution_components'])
        
        # Generate implementation steps
        solution['implementation_steps'] = [
            "1. Analyze problem context using cross-domain knowledge",
            "2. Apply insights from primary relevant domains",
            "3. Leverage analogical patterns from related domains", 
            "4. Synthesize solutions using convergence points",
            "5. Validate solution using meta-cognitive assessment"
        ]
        
        # Add supporting evidence
        solution['supporting_evidence'] = [
            f"Knowledge from {len(insights['primary_insights'])} domains",
            f"Found {len(insights['analogical_insights'])} cross-domain analogies",
            f"Identified {len(insights['knowledge_convergence_points'])} convergence points"
        ]
        
        return solution
    
    def _assess_solution_quality(self, solution: Dict[str, Any], context: ReasoningContext) -> float:
        """Assess the quality of a generated solution"""
        quality_factors = []
        
        # Confidence score
        quality_factors.append(solution.get('confidence', 0.0))
        
        # Number of solution components
        num_components = len(solution.get('solution_components', []))
        component_score = min(1.0, num_components / 5.0)  # Normalize to max 5 components
        quality_factors.append(component_score)
        
        # Cross-domain integration
        domains_used = set()
        for component in solution.get('solution_components', []):
            if 'source_domain' in component:
                domains_used.add(component['source_domain'])
            elif 'source_domains' in component:
                domains_used.update(component['source_domains'])
        
        domain_diversity = min(1.0, len(domains_used) / 3.0)  # Normalize to max 3 domains
        quality_factors.append(domain_diversity)
        
        # Evidence strength
        evidence_count = len(solution.get('supporting_evidence', []))
        evidence_score = min(1.0, evidence_count / 5.0)
        quality_factors.append(evidence_score)
        
        # Calculate weighted average
        weights = [0.4, 0.2, 0.3, 0.1]  # Confidence, components, diversity, evidence
        quality_score = sum(factor * weight for factor, weight in zip(quality_factors, weights))
        
        return quality_score
    
    def get_reasoning_analytics(self) -> Dict[str, Any]:
        """Get analytics about reasoning performance"""
        if not self.reasoning_history:
            return {'message': 'No reasoning history available'}
        
        recent_sessions = list(self.reasoning_history)[-50:]  # Last 50 sessions
        
        analytics = {
            'total_reasoning_sessions': len(self.reasoning_history),
            'average_reasoning_time': sum(s['reasoning_time'] for s in recent_sessions) / len(recent_sessions),
            'average_quality_score': sum(s['quality_score'] for s in recent_sessions) / len(recent_sessions),
            'domains_most_used': defaultdict(int),
            'analogies_per_session': sum(s['analogies_found'] for s in recent_sessions) / len(recent_sessions),
            'knowledge_utilization': sum(s['knowledge_nodes_used'] for s in recent_sessions) / len(recent_sessions),
            'reasoning_trends': self._analyze_reasoning_trends(recent_sessions)
        }
        
        # Count domain usage
        for session in recent_sessions:
            for domain in session['relevant_domains']:
                analytics['domains_most_used'][domain] += 1
        
        return analytics
    
    def _analyze_reasoning_trends(self, sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze trends in reasoning performance"""
        if len(sessions) < 10:
            return {'message': 'Insufficient data for trend analysis'}
        
        # Split into early and recent sessions
        mid_point = len(sessions) // 2
        early_sessions = sessions[:mid_point]
        recent_sessions = sessions[mid_point:]
        
        early_avg_quality = sum(s['quality_score'] for s in early_sessions) / len(early_sessions)
        recent_avg_quality = sum(s['quality_score'] for s in recent_sessions) / len(recent_sessions)
        
        early_avg_time = sum(s['reasoning_time'] for s in early_sessions) / len(early_sessions)
        recent_avg_time = sum(s['reasoning_time'] for s in recent_sessions) / len(recent_sessions)
        
        return {
            'quality_improvement': recent_avg_quality - early_avg_quality,
            'speed_improvement': early_avg_time - recent_avg_time,  # Positive = faster
            'trend_direction': 'improving' if recent_avg_quality > early_avg_quality else 'declining'
        }


# Continue with Meta-Cognitive Controller in next part...
print("✅ ASIS AGI Core - Stage 1 (Unified Knowledge Graph & Cross-Domain Reasoning) loaded successfully")
