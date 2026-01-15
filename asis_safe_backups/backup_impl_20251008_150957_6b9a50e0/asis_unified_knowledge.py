#!/usr/bin/env python3
"""
ASIS Unified Memory & Knowledge Architecture
==========================================
Advanced memory and knowledge management system for ASIS AGI
Integrates episodic memory, semantic networks, procedural knowledge, and knowledge graphs
"""

import asyncio
import json
import time
import sqlite3
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import networkx as nx
import pickle

@dataclass
class Experience:
    timestamp: float
    context: Dict
    actions: List[str]
    outcomes: Dict
    emotions: Dict
    importance_score: float
    memory_id: str

@dataclass
class Concept:
    name: str
    definition: Dict
    properties: Dict
    relations: List[Dict]
    confidence: float
    last_updated: float

@dataclass
class Procedure:
    task_name: str
    steps: List[Dict]
    conditions: Dict
    success_rate: float
    complexity_score: float
    learned_timestamp: float

class EpisodicMemory:
    """Stores and retrieves episodic experiences with temporal context"""
    
    def __init__(self, db_path: str = "asis_episodic_memory.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize episodic memory database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS experiences (
                memory_id TEXT PRIMARY KEY,
                timestamp REAL,
                context TEXT,
                actions TEXT,
                outcomes TEXT,
                emotions TEXT,
                importance_score REAL,
                retrieval_count INTEGER DEFAULT 0,
                last_accessed REAL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    async def store(self, experience: Dict) -> str:
        """Store episodic experience"""
        memory_id = f"exp_{int(time.time() * 1000000)}"
        
        exp = Experience(
            timestamp=time.time(),
            context=experience.get('context', {}),
            actions=experience.get('actions', []),
            outcomes=experience.get('outcomes', {}),
            emotions=experience.get('emotions', {}),
            importance_score=experience.get('importance', 0.5),
            memory_id=memory_id
        )
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO experiences 
            (memory_id, timestamp, context, actions, outcomes, emotions, importance_score, last_accessed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            exp.memory_id,
            exp.timestamp,
            json.dumps(exp.context),
            json.dumps(exp.actions),
            json.dumps(exp.outcomes),
            json.dumps(exp.emotions),
            exp.importance_score,
            exp.timestamp
        ))
        
        conn.commit()
        conn.close()
        
        return memory_id
    
    async def retrieve(self, query: Dict, limit: int = 10) -> List[Experience]:
        """Retrieve relevant episodic memories"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Simple retrieval based on context similarity
        cursor.execute('''
            SELECT * FROM experiences 
            ORDER BY importance_score DESC, timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        experiences = []
        
        for row in rows:
            exp = Experience(
                memory_id=row[0],
                timestamp=row[1],
                context=json.loads(row[2]),
                actions=json.loads(row[3]),
                outcomes=json.loads(row[4]),
                emotions=json.loads(row[5]),
                importance_score=row[6]
            )
            experiences.append(exp)
        
        conn.close()
        return experiences

class SemanticNetwork:
    """Manages conceptual knowledge and semantic relationships"""
    
    def __init__(self, db_path: str = "asis_semantic_network.db"):
        self.db_path = db_path
        self.graph = nx.DiGraph()
        self.init_database()
        self.load_graph()
    
    def init_database(self):
        """Initialize semantic network database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS concepts (
                name TEXT PRIMARY KEY,
                definition TEXT,
                properties TEXT,
                relations TEXT,
                confidence REAL,
                last_updated REAL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_graph(self):
        """Load semantic network from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM concepts')
        rows = cursor.fetchall()
        
        for row in rows:
            concept_name = row[0]
            relations = json.loads(row[3])
            
            self.graph.add_node(concept_name)
            
            for relation in relations:
                target = relation.get('target')
                rel_type = relation.get('type', 'related_to')
                strength = relation.get('strength', 0.5)
                
                if target:
                    self.graph.add_edge(concept_name, target, 
                                      relation_type=rel_type, 
                                      strength=strength)
        
        conn.close()
    
    async def integrate_concept(self, concept: str, definition: Dict, relations: List[Dict]) -> bool:
        """Integrate new conceptual knowledge"""
        try:
            concept_obj = Concept(
                name=concept,
                definition=definition,
                properties=definition.get('properties', {}),
                relations=relations,
                confidence=definition.get('confidence', 0.8),
                last_updated=time.time()
            )
            
            # Store in database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO concepts 
                (name, definition, properties, relations, confidence, last_updated)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                concept_obj.name,
                json.dumps(concept_obj.definition),
                json.dumps(concept_obj.properties),
                json.dumps(concept_obj.relations),
                concept_obj.confidence,
                concept_obj.last_updated
            ))
            
            conn.commit()
            conn.close()
            
            # Update graph
            self.graph.add_node(concept)
            for relation in relations:
                target = relation.get('target')
                rel_type = relation.get('type', 'related_to')
                strength = relation.get('strength', 0.5)
                
                if target:
                    self.graph.add_edge(concept, target, 
                                      relation_type=rel_type, 
                                      strength=strength)
            
            return True
            
        except Exception as e:
            print(f"❌ Error integrating concept: {e}")
            return False
    
    async def find_related_concepts(self, concept: str, depth: int = 2) -> List[Dict]:
        """Find concepts related to given concept"""
        if concept not in self.graph:
            return []
        
        related = []
        visited = set()
        
        def dfs(node, current_depth):
            if current_depth > depth or node in visited:
                return
            
            visited.add(node)
            
            for neighbor in self.graph.neighbors(node):
                edge_data = self.graph.get_edge_data(node, neighbor)
                related.append({
                    'concept': neighbor,
                    'relation_type': edge_data.get('relation_type', 'related_to'),
                    'strength': edge_data.get('strength', 0.5),
                    'depth': current_depth + 1
                })
                dfs(neighbor, current_depth + 1)
        
        dfs(concept, 0)
        return related

class ProceduralKnowledge:
    """Manages procedural knowledge and skills"""
    
    def __init__(self, db_path: str = "asis_procedural_knowledge.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize procedural knowledge database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS procedures (
                task_name TEXT PRIMARY KEY,
                steps TEXT,
                conditions TEXT,
                success_rate REAL,
                complexity_score REAL,
                learned_timestamp REAL,
                usage_count INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    async def learn(self, task: str, procedure: List[Dict]) -> bool:
        """Learn and store procedural knowledge"""
        try:
            # Calculate complexity score
            complexity = len(procedure) * 0.1
            for step in procedure:
                if step.get('complexity', 'simple') == 'complex':
                    complexity += 0.5
            
            proc = Procedure(
                task_name=task,
                steps=procedure,
                conditions={},
                success_rate=0.5,  # Initial success rate
                complexity_score=complexity,
                learned_timestamp=time.time()
            )
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO procedures 
                (task_name, steps, conditions, success_rate, complexity_score, learned_timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                proc.task_name,
                json.dumps(proc.steps),
                json.dumps(proc.conditions),
                proc.success_rate,
                proc.complexity_score,
                proc.learned_timestamp
            ))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"❌ Error learning procedure: {e}")
            return False
    
    async def retrieve_procedure(self, task: str) -> Optional[Procedure]:
        """Retrieve procedure for a task"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM procedures WHERE task_name = ?', (task,))
        row = cursor.fetchone()
        
        if row:
            proc = Procedure(
                task_name=row[0],
                steps=json.loads(row[1]),
                conditions=json.loads(row[2]),
                success_rate=row[3],
                complexity_score=row[4],
                learned_timestamp=row[5]
            )
            conn.close()
            return proc
        
        conn.close()
        return None

class KnowledgeGraph:
    """Advanced knowledge graph with reasoning capabilities"""
    
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.entity_embeddings = {}
        
    async def query(self, query: Dict) -> Dict:
        """Perform advanced knowledge retrieval"""
        query_type = query.get('type', 'simple')
        entity = query.get('entity')
        relation = query.get('relation')
        
        if query_type == 'simple' and entity:
            return await self._simple_query(entity)
        elif query_type == 'relational' and entity and relation:
            return await self._relational_query(entity, relation)
        elif query_type == 'path':
            return await self._path_query(query.get('start'), query.get('end'))
        
        return {'error': 'Unsupported query type'}
    
    async def _simple_query(self, entity: str) -> Dict:
        """Simple entity lookup"""
        if entity in self.graph:
            neighbors = list(self.graph.neighbors(entity))
            return {
                'entity': entity,
                'neighbors': neighbors,
                'degree': self.graph.degree(entity)
            }
        return {'entity': entity, 'found': False}
    
    async def _relational_query(self, entity: str, relation: str) -> Dict:
        """Query based on specific relationship"""
        results = []
        
        if entity in self.graph:
            for neighbor in self.graph.neighbors(entity):
                edges = self.graph.get_edge_data(entity, neighbor)
                for edge_data in edges.values():
                    if edge_data.get('relation_type') == relation:
                        results.append({
                            'target': neighbor,
                            'confidence': edge_data.get('confidence', 0.5)
                        })
        
        return {'entity': entity, 'relation': relation, 'results': results}
    
    async def _path_query(self, start: str, end: str) -> Dict:
        """Find paths between entities"""
        try:
            if start in self.graph and end in self.graph:
                paths = list(nx.all_simple_paths(self.graph, start, end, cutoff=3))
                return {'start': start, 'end': end, 'paths': paths[:5]}  # Limit to 5 paths
        except Exception:
            pass
        
        return {'start': start, 'end': end, 'paths': []}
    
    async def complex_reasoning(self, reasoning_query: Dict) -> Dict:
        """Perform complex reasoning using integrated knowledge"""
        reasoning_type = reasoning_query.get('type', 'inference')
        
        if reasoning_type == 'inference':
            return await self._inference_reasoning(reasoning_query)
        elif reasoning_type == 'analogy':
            return await self._analogy_reasoning(reasoning_query)
        elif reasoning_type == 'causal':
            return await self._causal_reasoning(reasoning_query)
        
        return {'reasoning_type': reasoning_type, 'result': 'unsupported'}
    
    async def _inference_reasoning(self, query: Dict) -> Dict:
        """Perform inference-based reasoning"""
        premises = query.get('premises', [])
        conclusion_candidates = []
        
        # Simple inference: if A relates to B, and B relates to C, then A might relate to C
        for premise in premises:
            entity = premise.get('entity')
            if entity in self.graph:
                for neighbor in self.graph.neighbors(entity):
                    for second_neighbor in self.graph.neighbors(neighbor):
                        if second_neighbor != entity:
                            conclusion_candidates.append({
                                'entity': entity,
                                'inferred_relation': second_neighbor,
                                'path': [entity, neighbor, second_neighbor],
                                'confidence': 0.6
                            })
        
        return {'reasoning_type': 'inference', 'conclusions': conclusion_candidates[:10]}
    
    async def _analogy_reasoning(self, query: Dict) -> Dict:
        """Perform analogy-based reasoning"""
        source = query.get('source')
        target = query.get('target')
        
        analogies = []
        
        if source in self.graph and target in self.graph:
            source_neighbors = set(self.graph.neighbors(source))
            target_neighbors = set(self.graph.neighbors(target))
            
            common_neighbors = source_neighbors.intersection(target_neighbors)
            
            for common in common_neighbors:
                analogies.append({
                    'source': source,
                    'target': target,
                    'common_relation': common,
                    'analogy_strength': 0.7
                })
        
        return {'reasoning_type': 'analogy', 'analogies': analogies}
    
    async def _causal_reasoning(self, query: Dict) -> Dict:
        """Perform causal reasoning"""
        cause = query.get('cause')
        
        causal_chains = []
        
        if cause in self.graph:
            for neighbor in self.graph.neighbors(cause):
                edges = self.graph.get_edge_data(cause, neighbor)
                for edge_data in edges.values():
                    if edge_data.get('relation_type') == 'causes':
                        causal_chains.append({
                            'cause': cause,
                            'effect': neighbor,
                            'strength': edge_data.get('strength', 0.5)
                        })
        
        return {'reasoning_type': 'causal', 'causal_chains': causal_chains}

class ASISUnifiedKnowledge:
    """Main unified knowledge architecture class"""
    
    def __init__(self):
        self.episodic_memory = EpisodicMemory()
        self.semantic_network = SemanticNetwork()
        self.procedural_knowledge = ProceduralKnowledge()
        self.knowledge_graph = KnowledgeGraph()
        
        print("🧠 ASIS Unified Knowledge Architecture initialized")
        
    async def store_experience(self, experience: Dict) -> str:
        """Store episodic experience with full context"""
        return await self.episodic_memory.store(experience)
        
    async def integrate_concept(self, concept: str, definition: Dict, relations: List[Dict]) -> bool:
        """Integrate new conceptual knowledge"""
        return await self.semantic_network.integrate_concept(concept, definition, relations)
        
    async def learn_procedure(self, task: str, procedure: List[Dict]) -> bool:
        """Learn and store procedural knowledge"""
        return await self.procedural_knowledge.learn(task, procedure)
        
    async def query_knowledge(self, query: Dict) -> Dict:
        """Perform advanced knowledge retrieval"""
        return await self.knowledge_graph.query(query)
        
    async def reason_over_knowledge(self, reasoning_query: Dict) -> Dict:
        """Perform complex reasoning using integrated knowledge"""
        return await self.knowledge_graph.complex_reasoning(reasoning_query)
    
    async def comprehensive_search(self, search_query: str) -> Dict:
        """Perform comprehensive search across all knowledge systems"""
        results = {
            'episodic_memories': [],
            'related_concepts': [],
            'relevant_procedures': [],
            'knowledge_connections': []
        }
        
        # Search episodic memories
        try:
            memories = await self.episodic_memory.retrieve({'query': search_query})
            results['episodic_memories'] = [asdict(mem) for mem in memories[:5]]
        except Exception as e:
            print(f"⚠️ Error searching episodic memories: {e}")
        
        # Search semantic network
        try:
            concepts = await self.semantic_network.find_related_concepts(search_query)
            results['related_concepts'] = concepts[:10]
        except Exception as e:
            print(f"⚠️ Error searching semantic network: {e}")
        
        # Search knowledge graph
        try:
            knowledge = await self.knowledge_graph.query({'type': 'simple', 'entity': search_query})
            results['knowledge_connections'] = knowledge
        except Exception as e:
            print(f"⚠️ Error searching knowledge graph: {e}")
        
        return results
    
    def get_system_stats(self) -> Dict:
        """Get statistics about the knowledge systems"""
        return {
            'semantic_network_nodes': self.semantic_network.graph.number_of_nodes(),
            'semantic_network_edges': self.semantic_network.graph.number_of_edges(),
            'knowledge_graph_nodes': self.knowledge_graph.graph.number_of_nodes(),
            'knowledge_graph_edges': self.knowledge_graph.graph.number_of_edges(),
            'system_status': 'operational',
            'initialization_time': time.time()
        }

# Test function
async def test_unified_knowledge():
    """Test the unified knowledge architecture"""
    uk = ASISUnifiedKnowledge()
    
    print("🧪 Testing Unified Knowledge Architecture...")
    
    # Test 1: Store experience
    experience = {
        'context': {'task': 'research', 'topic': 'AI'},
        'actions': ['search', 'analyze', 'synthesize'],
        'outcomes': {'success': True, 'confidence': 0.9},
        'emotions': {'satisfaction': 0.8},
        'importance': 0.9
    }
    
    memory_id = await uk.store_experience(experience)
    print(f"✅ Stored experience: {memory_id}")
    
    # Test 2: Integrate concept
    concept_result = await uk.integrate_concept(
        "artificial_intelligence",
        {
            'definition': 'Intelligence demonstrated by machines',
            'properties': {'computational': True, 'learning': True},
            'confidence': 0.9
        },
        [
            {'target': 'machine_learning', 'type': 'includes', 'strength': 0.8},
            {'target': 'neural_networks', 'type': 'uses', 'strength': 0.7}
        ]
    )
    print(f"✅ Integrated concept: {concept_result}")
    
    # Test 3: Learn procedure
    procedure_result = await uk.learn_procedure(
        "research_task",
        [
            {'step': 1, 'action': 'define_query', 'complexity': 'simple'},
            {'step': 2, 'action': 'search_sources', 'complexity': 'moderate'},
            {'step': 3, 'action': 'synthesize_results', 'complexity': 'complex'}
        ]
    )
    print(f"✅ Learned procedure: {procedure_result}")
    
    # Test 4: Knowledge query
    query_result = await uk.query_knowledge({
        'type': 'simple',
        'entity': 'artificial_intelligence'
    })
    print(f"✅ Knowledge query result: {query_result}")
    
    # Test 5: System stats
    stats = uk.get_system_stats()
    print(f"✅ System stats: {stats}")
    
    return uk

if __name__ == "__main__":
    # Run test
    asyncio.run(test_unified_knowledge())