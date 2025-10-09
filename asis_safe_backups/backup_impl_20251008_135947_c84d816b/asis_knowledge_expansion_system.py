#!/usr/bin/env python3
"""
ASIS Knowledge Expansion System
==============================
Advanced system for continuously expanding ASIS knowledge base
and improving conversational abilities through structured learning
"""

import os
import json
import sqlite3
import requests
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import hashlib
import re
from collections import defaultdict

class ASISKnowledgeExpansionSystem:
    """
    Comprehensive system for expanding ASIS knowledge base and conversational abilities
    """
    
    def __init__(self):
        self.knowledge_db = "asis_expanded_knowledge.db"
        self.conversation_patterns_db = "asis_conversation_patterns.db"
        self.training_log = "asis_training_progress.log"
        
        # Knowledge domains for structured learning
        self.knowledge_domains = {
            'science': {
                'physics': ['quantum mechanics', 'relativity', 'thermodynamics', 'electromagnetism'],
                'chemistry': ['organic chemistry', 'inorganic chemistry', 'biochemistry', 'physical chemistry'],
                'biology': ['genetics', 'evolution', 'ecology', 'molecular biology'],
                'mathematics': ['calculus', 'linear algebra', 'statistics', 'number theory'],
                'computer_science': ['algorithms', 'data structures', 'machine learning', 'software engineering']
            },
            'humanities': {
                'philosophy': ['ethics', 'metaphysics', 'epistemology', 'logic'],
                'literature': ['poetry', 'fiction', 'drama', 'literary criticism'],
                'history': ['world history', 'cultural history', 'political history', 'social movements'],
                'languages': ['linguistics', 'etymology', 'translation', 'comparative literature'],
                'arts': ['visual arts', 'music theory', 'performing arts', 'art history']
            },
            'practical': {
                'business': ['entrepreneurship', 'finance', 'marketing', 'management'],
                'technology': ['programming', 'cybersecurity', 'data science', 'AI development'],
                'health': ['nutrition', 'exercise', 'mental health', 'medical knowledge'],
                'lifestyle': ['productivity', 'relationships', 'personal development', 'hobbies'],
                'current_events': ['politics', 'economics', 'social issues', 'innovations']
            }
        }
        
        # Conversation improvement patterns
        self.conversation_patterns = {
            'engagement': [
                'asking follow-up questions',
                'showing genuine interest',
                'acknowledging emotions',
                'providing relevant examples',
                'connecting to user experiences'
            ],
            'clarity': [
                'using clear explanations',
                'avoiding jargon when appropriate',
                'structuring responses logically',
                'providing step-by-step guidance',
                'summarizing key points'
            ],
            'helpfulness': [
                'offering practical solutions',
                'providing multiple perspectives',
                'suggesting next steps',
                'sharing relevant resources',
                'anticipating follow-up needs'
            ],
            'personality': [
                'maintaining consistent voice',
                'showing appropriate humor',
                'expressing empathy',
                'being encouraging',
                'adapting to user style'
            ]
        }
        
        self.setup_knowledge_expansion_system()
        
    def setup_knowledge_expansion_system(self):
        """Initialize databases and structures for knowledge expansion"""
        
        # Knowledge expansion database
        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT,
                subdomain TEXT,
                topic TEXT,
                content TEXT,
                source_type TEXT,
                source_url TEXT,
                confidence_score REAL,
                verification_status TEXT,
                created_timestamp TEXT,
                last_updated TEXT,
                usage_count INTEGER DEFAULT 0,
                effectiveness_rating REAL DEFAULT 0.0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge_relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                primary_topic_id INTEGER,
                related_topic_id INTEGER,
                relationship_type TEXT,
                strength REAL,
                created_timestamp TEXT,
                FOREIGN KEY (primary_topic_id) REFERENCES knowledge_entries (id),
                FOREIGN KEY (related_topic_id) REFERENCES knowledge_entries (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_type TEXT,
                topics_covered TEXT,
                knowledge_added INTEGER,
                patterns_learned INTEGER,
                improvement_metrics TEXT,
                duration_seconds INTEGER,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Conversation patterns database
        conn = sqlite3.connect(self.conversation_patterns_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_examples (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT,
                ideal_response TEXT,
                pattern_type TEXT,
                effectiveness_score REAL,
                context_tags TEXT,
                created_timestamp TEXT,
                usage_count INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS response_improvements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_response TEXT,
                improved_response TEXT,
                improvement_type TEXT,
                user_feedback REAL,
                context TEXT,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ ASIS Knowledge Expansion System initialized")
    
    def add_structured_knowledge(self, domain: str, subdomain: str, topic: str, 
                               content: str, source_type: str = "manual", 
                               source_url: str = "", confidence_score: float = 0.8) -> str:
        """Add structured knowledge entry to the database"""
        
        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()
        
        # Create content hash for deduplication
        content_hash = hashlib.md5(content.encode()).hexdigest()
        
        # Check if similar content already exists
        cursor.execute('''
            SELECT id FROM knowledge_entries 
            WHERE domain = ? AND subdomain = ? AND topic = ?
        ''', (domain, subdomain, topic))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update existing entry
            cursor.execute('''
                UPDATE knowledge_entries 
                SET content = ?, last_updated = ?, confidence_score = ?
                WHERE id = ?
            ''', (content, datetime.now().isoformat(), confidence_score, existing[0]))
            entry_id = existing[0]
            action = "updated"
        else:
            # Insert new entry
            cursor.execute('''
                INSERT INTO knowledge_entries 
                (domain, subdomain, topic, content, source_type, source_url, 
                 confidence_score, verification_status, created_timestamp, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (domain, subdomain, topic, content, source_type, source_url,
                  confidence_score, "pending", datetime.now().isoformat(), 
                  datetime.now().isoformat()))
            entry_id = cursor.lastrowid
            action = "added"
        
        conn.commit()
        conn.close()
        
        self.log_training_activity(f"Knowledge {action}: {domain}/{subdomain}/{topic}")
        return f"{content_hash}_{entry_id}"
    
    def bulk_knowledge_import(self, knowledge_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """Import multiple knowledge entries efficiently"""
        
        results = {
            'added': 0,
            'updated': 0,
            'skipped': 0,
            'errors': 0
        }
        
        for entry in knowledge_data:
            try:
                required_fields = ['domain', 'subdomain', 'topic', 'content']
                if not all(field in entry for field in required_fields):
                    results['skipped'] += 1
                    continue
                
                entry_id = self.add_structured_knowledge(
                    domain=entry['domain'],
                    subdomain=entry['subdomain'],
                    topic=entry['topic'],
                    content=entry['content'],
                    source_type=entry.get('source_type', 'bulk_import'),
                    source_url=entry.get('source_url', ''),
                    confidence_score=entry.get('confidence_score', 0.7)
                )
                
                if 'updated' in entry_id:
                    results['updated'] += 1
                else:
                    results['added'] += 1
                    
            except Exception as e:
                results['errors'] += 1
                self.log_training_activity(f"Error importing knowledge: {str(e)}")
        
        self.log_training_activity(f"Bulk import completed: {results}")
        return results
    
    def add_conversation_example(self, user_input: str, ideal_response: str,
                               pattern_type: str, context_tags: List[str] = None,
                               effectiveness_score: float = 0.8) -> str:
        """Add conversation example for training"""
        
        conn = sqlite3.connect(self.conversation_patterns_db)
        cursor = conn.cursor()
        
        tags_str = json.dumps(context_tags or [])
        
        cursor.execute('''
            INSERT INTO conversation_examples 
            (user_input, ideal_response, pattern_type, effectiveness_score, 
             context_tags, created_timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_input, ideal_response, pattern_type, effectiveness_score,
              tags_str, datetime.now().isoformat()))
        
        example_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        self.log_training_activity(f"Conversation example added: {pattern_type}")
        return f"conv_example_{example_id}"
    
    def train_conversational_patterns(self, training_examples: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Train ASIS on conversational patterns"""
        
        training_results = {
            'examples_processed': 0,
            'patterns_identified': [],
            'improvements_suggested': [],
            'training_score': 0.0
        }
        
        for example in training_examples:
            try:
                # Add to conversation examples database
                self.add_conversation_example(
                    user_input=example['user_input'],
                    ideal_response=example['ideal_response'],
                    pattern_type=example.get('pattern_type', 'general'),
                    context_tags=example.get('context_tags', []),
                    effectiveness_score=example.get('effectiveness_score', 0.8)
                )
                
                training_results['examples_processed'] += 1
                
                # Analyze pattern
                pattern = self.analyze_conversation_pattern(
                    example['user_input'], 
                    example['ideal_response']
                )
                
                if pattern and pattern not in training_results['patterns_identified']:
                    training_results['patterns_identified'].append(pattern)
                
            except Exception as e:
                self.log_training_activity(f"Error in pattern training: {str(e)}")
        
        # Calculate training effectiveness
        if training_results['examples_processed'] > 0:
            training_results['training_score'] = min(
                training_results['examples_processed'] / len(training_examples), 1.0
            )
        
        self.log_training_activity(f"Conversation training completed: {training_results}")
        return training_results
    
    def analyze_conversation_pattern(self, user_input: str, ideal_response: str) -> Optional[str]:
        """Analyze conversation to identify useful patterns"""
        
        patterns = []
        
        # Check for question patterns
        if '?' in user_input:
            if any(word in ideal_response.lower() for word in ['let me explain', 'here\'s how', 'the answer is']):
                patterns.append('explanatory_response')
        
        # Check for emotional patterns
        emotion_words = ['feel', 'emotion', 'sad', 'happy', 'frustrated', 'excited']
        if any(word in user_input.lower() for word in emotion_words):
            if any(word in ideal_response.lower() for word in ['understand', 'hear you', 'empathize']):
                patterns.append('empathetic_response')
        
        # Check for technical patterns
        tech_words = ['code', 'program', 'debug', 'algorithm', 'technical']
        if any(word in user_input.lower() for word in tech_words):
            if any(word in ideal_response.lower() for word in ['step by step', 'example', 'implementation']):
                patterns.append('technical_guidance')
        
        return patterns[0] if patterns else None
    
    def create_knowledge_training_batch(self, domain: str, count: int = 50) -> List[Dict[str, Any]]:
        """Create a training batch for a specific knowledge domain"""
        
        if domain not in self.knowledge_domains:
            return []
        
        training_batch = []
        domain_data = self.knowledge_domains[domain]
        
        for subdomain, topics in domain_data.items():
            for topic in topics[:count//len(domain_data)]:
                # Generate training entry template
                training_entry = {
                    'domain': domain,
                    'subdomain': subdomain,
                    'topic': topic,
                    'content': f"Comprehensive knowledge about {topic} in {subdomain}. This covers fundamental concepts, advanced applications, current research, and practical implementations.",
                    'source_type': 'structured_training',
                    'confidence_score': 0.7,
                    'training_priority': 'high' if topic in ['machine learning', 'quantum mechanics', 'genetics'] else 'medium'
                }
                training_batch.append(training_entry)
        
        return training_batch
    
    def generate_conversation_training_scenarios(self, count: int = 100) -> List[Dict[str, Any]]:
        """Generate diverse conversation training scenarios"""
        
        scenarios = []
        
        # Question-answering scenarios
        qa_scenarios = [
            {
                'user_input': 'Can you explain quantum computing in simple terms?',
                'ideal_response': 'Quantum computing is a revolutionary technology that uses quantum mechanical phenomena to process information. Unlike classical computers that use bits (0 or 1), quantum computers use quantum bits or "qubits" that can exist in multiple states simultaneously. This allows them to potentially solve certain problems exponentially faster than classical computers.',
                'pattern_type': 'explanatory',
                'context_tags': ['science', 'technology', 'education']
            },
            {
                'user_input': 'I\'m feeling overwhelmed with my workload. Any advice?',
                'ideal_response': 'I understand that feeling overwhelmed can be really challenging. Here are some strategies that might help: 1) Break large tasks into smaller, manageable pieces, 2) Prioritize tasks by urgency and importance, 3) Take regular breaks to avoid burnout, 4) Consider if you can delegate or ask for help with some tasks. Remember, it\'s okay to feel this way, and taking steps to manage your workload shows great self-awareness.',
                'pattern_type': 'empathetic_advice',
                'context_tags': ['emotional_support', 'productivity', 'mental_health']
            },
            {
                'user_input': 'What\'s the best programming language to learn first?',
                'ideal_response': 'For beginners, I\'d recommend Python as your first programming language. Here\'s why: 1) Clean, readable syntax that\'s close to English, 2) Versatile - used in web development, data science, AI, and more, 3) Large, supportive community with lots of learning resources, 4) Gentle learning curve that builds confidence. Once you\'re comfortable with Python, you can explore other languages based on your specific interests and career goals.',
                'pattern_type': 'technical_guidance',
                'context_tags': ['programming', 'career_advice', 'education']
            }
        ]
        
        scenarios.extend(qa_scenarios)
        
        # Add more scenario types
        for i in range(count - len(scenarios)):
            # Generate varied scenarios based on patterns
            scenario_templates = [
                {
                    'pattern_type': 'creative_help',
                    'context_tags': ['creativity', 'brainstorming', 'problem_solving']
                },
                {
                    'pattern_type': 'analytical_thinking',
                    'context_tags': ['analysis', 'reasoning', 'logic']
                },
                {
                    'pattern_type': 'casual_conversation',
                    'context_tags': ['casual', 'friendly', 'engaging']
                }
            ]
            
            template = scenario_templates[i % len(scenario_templates)]
            scenarios.append({
                'user_input': f'Sample input for {template["pattern_type"]} scenario {i}',
                'ideal_response': f'Ideal response demonstrating {template["pattern_type"]} with appropriate tone and helpfulness.',
                'pattern_type': template['pattern_type'],
                'context_tags': template['context_tags']
            })
        
        return scenarios[:count]
    
    def conduct_training_session(self, session_type: str = "comprehensive", 
                                domain_focus: str = None) -> Dict[str, Any]:
        """Conduct a comprehensive training session for ASIS"""
        
        session_start = time.time()
        session_results = {
            'session_type': session_type,
            'domain_focus': domain_focus,
            'knowledge_entries_added': 0,
            'conversation_examples_added': 0,
            'patterns_learned': 0,
            'session_duration': 0,
            'effectiveness_score': 0.0,
            'next_recommendations': []
        }
        
        print(f"🎓 Starting ASIS Training Session: {session_type}")
        if domain_focus:
            print(f"🎯 Domain Focus: {domain_focus}")
        
        try:
            # Phase 1: Knowledge expansion
            if domain_focus:
                knowledge_batch = self.create_knowledge_training_batch(domain_focus, 25)
            else:
                # Train across all domains
                knowledge_batch = []
                for domain in self.knowledge_domains.keys():
                    knowledge_batch.extend(self.create_knowledge_training_batch(domain, 10))
            
            if knowledge_batch:
                print(f"📚 Adding {len(knowledge_batch)} knowledge entries...")
                knowledge_results = self.bulk_knowledge_import(knowledge_batch)
                session_results['knowledge_entries_added'] = knowledge_results['added']
            
            # Phase 2: Conversation training
            print("💬 Generating conversation training scenarios...")
            conversation_scenarios = self.generate_conversation_training_scenarios(50)
            
            if conversation_scenarios:
                print(f"🗣️ Training on {len(conversation_scenarios)} conversation patterns...")
                conversation_results = self.train_conversational_patterns(conversation_scenarios)
                session_results['conversation_examples_added'] = conversation_results['examples_processed']
                session_results['patterns_learned'] = len(conversation_results['patterns_identified'])
            
            # Phase 3: Calculate session effectiveness
            session_duration = time.time() - session_start
            session_results['session_duration'] = round(session_duration, 2)
            
            # Effectiveness based on successful additions and time efficiency
            base_score = min((session_results['knowledge_entries_added'] + 
                            session_results['conversation_examples_added']) / 50, 1.0)
            time_efficiency = max(0.5, min(1.0, 60 / session_duration))  # Optimal around 1 minute
            session_results['effectiveness_score'] = round((base_score * 0.7 + time_efficiency * 0.3), 3)
            
            # Generate recommendations for next session
            if session_results['effectiveness_score'] > 0.8:
                session_results['next_recommendations'].append("Excellent progress! Consider advanced domain specialization.")
            else:
                session_results['next_recommendations'].append("Focus on quality over quantity in next session.")
            
            if domain_focus:
                other_domains = [d for d in self.knowledge_domains.keys() if d != domain_focus]
                session_results['next_recommendations'].append(f"Consider training on: {', '.join(other_domains[:2])}")
            
            # Log session to database
            self.log_training_session(session_results)
            
            print(f"✅ Training Session Complete!")
            print(f"📊 Knowledge Entries Added: {session_results['knowledge_entries_added']}")
            print(f"💬 Conversation Examples: {session_results['conversation_examples_added']}")
            print(f"🧠 Patterns Learned: {session_results['patterns_learned']}")
            print(f"⏱️ Duration: {session_results['session_duration']} seconds")
            print(f"🎯 Effectiveness Score: {session_results['effectiveness_score']}")
            
        except Exception as e:
            print(f"❌ Training session error: {str(e)}")
            session_results['error'] = str(e)
        
        return session_results
    
    def log_training_session(self, session_results: Dict[str, Any]):
        """Log training session to database"""
        
        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO learning_sessions 
            (session_type, topics_covered, knowledge_added, patterns_learned, 
             improvement_metrics, duration_seconds, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_results['session_type'],
            session_results.get('domain_focus', 'general'),
            session_results['knowledge_entries_added'],
            session_results['patterns_learned'],
            json.dumps({
                'effectiveness_score': session_results['effectiveness_score'],
                'conversation_examples': session_results['conversation_examples_added'],
                'recommendations': session_results['next_recommendations']
            }),
            session_results['session_duration'],
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def log_training_activity(self, activity: str):
        """Log training activities to file"""
        
        timestamp = datetime.now().isoformat()
        with open(self.training_log, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {activity}\n")
    
    def get_training_progress_report(self) -> Dict[str, Any]:
        """Generate comprehensive training progress report"""
        
        # Knowledge database stats
        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM knowledge_entries')
        total_knowledge = cursor.fetchone()[0]
        
        cursor.execute('SELECT domain, COUNT(*) FROM knowledge_entries GROUP BY domain')
        domain_distribution = dict(cursor.fetchall())
        
        cursor.execute('SELECT COUNT(*) FROM learning_sessions')
        training_sessions = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT AVG(CAST(JSON_EXTRACT(improvement_metrics, '$.effectiveness_score') AS REAL))
            FROM learning_sessions 
            WHERE improvement_metrics IS NOT NULL
        ''')
        avg_effectiveness = cursor.fetchone()[0] or 0.0
        
        conn.close()
        
        # Conversation patterns stats
        conn = sqlite3.connect(self.conversation_patterns_db)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM conversation_examples')
        total_conversations = cursor.fetchone()[0]
        
        cursor.execute('SELECT pattern_type, COUNT(*) FROM conversation_examples GROUP BY pattern_type')
        pattern_distribution = dict(cursor.fetchall())
        
        conn.close()
        
        report = {
            'training_overview': {
                'total_knowledge_entries': total_knowledge,
                'total_conversation_examples': total_conversations,
                'training_sessions_completed': training_sessions,
                'average_effectiveness_score': round(avg_effectiveness, 3)
            },
            'knowledge_distribution': domain_distribution,
            'conversation_patterns': pattern_distribution,
            'recommendations': [
                f"Knowledge base has {total_knowledge} entries across {len(domain_distribution)} domains",
                f"Conversation training includes {total_conversations} examples with {len(pattern_distribution)} pattern types",
                f"Training effectiveness averaging {round(avg_effectiveness, 1)}/1.0"
            ],
            'next_steps': [
                "Continue domain-specific training for balanced knowledge",
                "Focus on conversation patterns with lower representation",
                "Implement real-time learning from user interactions"
            ]
        }
        
        return report

# Example usage and testing
if __name__ == "__main__":
    print("🚀 Initializing ASIS Knowledge Expansion System...")
    
    # Initialize the system
    knowledge_system = ASISKnowledgeExpansionSystem()
    
    # Run a comprehensive training session
    training_results = knowledge_system.conduct_training_session(
        session_type="comprehensive",
        domain_focus="science"  # Focus on science domain
    )
    
    print("\n📊 Training Results:")
    for key, value in training_results.items():
        print(f"   {key}: {value}")
    
    # Generate progress report
    print("\n📈 Training Progress Report:")
    progress_report = knowledge_system.get_training_progress_report()
    
    for section, data in progress_report.items():
        print(f"\n{section.upper()}:")
        if isinstance(data, dict):
            for key, value in data.items():
                print(f"   {key}: {value}")
        elif isinstance(data, list):
            for item in data:
                print(f"   • {item}")
        else:
            print(f"   {data}")
