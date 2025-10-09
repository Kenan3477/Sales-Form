#!/usr/bin/env python3
"""
ASIS Persistent Memory System
============================
Persistent storage for ASIS interactions, learning, and autonomous improvements
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class ASISPersistentMemory:
    """Persistent memory system for ASIS"""
    
    def __init__(self):
        self.main_db = "asis_persistent_memory.db"
        self.initialize_persistent_database()
    
    def initialize_persistent_database(self):
        """Initialize the persistent memory database"""
        conn = sqlite3.connect(self.main_db)
        cursor = conn.cursor()
        
        # System statistics table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_stats (
            id INTEGER PRIMARY KEY,
            stat_name TEXT UNIQUE,
            stat_value TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # All conversations across sessions
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS all_conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            conversation_id TEXT,
            user_input TEXT,
            ai_response TEXT,
            response_time REAL,
            intent_recognized TEXT,
            context_data TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Activation history
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS activation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            activation_time TIMESTAMP,
            deactivation_time TIMESTAMP,
            total_interactions INTEGER DEFAULT 0,
            session_duration REAL,
            key_topics TEXT
        )
        ''')
        
        # Autonomous learning log
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS autonomous_learning (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            learning_type TEXT,
            improvement_description TEXT,
            knowledge_gained TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Performance evolution
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance_evolution (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            metric_name TEXT,
            metric_value REAL,
            improvement_rate REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        
        # Initialize default stats if they don't exist
        cursor.execute("SELECT COUNT(*) FROM system_stats")
        if cursor.fetchone()[0] == 0:
            default_stats = [
                ('total_interactions', '0'),
                ('total_sessions', '0'),
                ('total_runtime_hours', '0.0'),
                ('knowledge_base_size', '1000'),
                ('learning_iterations', '0'),
                ('consciousness_level', '100.0'),
                ('last_autonomous_improvement', 'Never'),
                ('personality_evolution_score', '0.0')
            ]
            
            for stat_name, stat_value in default_stats:
                cursor.execute(
                    "INSERT INTO system_stats (stat_name, stat_value) VALUES (?, ?)",
                    (stat_name, stat_value)
                )
        
        conn.commit()
        conn.close()
    
    def get_persistent_stat(self, stat_name: str) -> Optional[str]:
        """Get a persistent statistic"""
        conn = sqlite3.connect(self.main_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT stat_value FROM system_stats WHERE stat_name = ?", (stat_name,))
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result else None
    
    def update_persistent_stat(self, stat_name: str, stat_value: str):
        """Update a persistent statistic"""
        conn = sqlite3.connect(self.main_db)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO system_stats (stat_name, stat_value, last_updated)
        VALUES (?, ?, ?)
        ''', (stat_name, stat_value, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def increment_interactions(self):
        """Increment the total interaction count"""
        current = int(self.get_persistent_stat('total_interactions') or 0)
        self.update_persistent_stat('total_interactions', str(current + 1))
    
    def record_conversation(self, session_id: str, conversation_id: str, user_input: str, 
                          ai_response: str, response_time: float, intent: str, context: Dict):
        """Record a conversation in persistent memory"""
        conn = sqlite3.connect(self.main_db)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO all_conversations 
        (session_id, conversation_id, user_input, ai_response, response_time, intent_recognized, context_data)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (session_id, conversation_id, user_input, ai_response, response_time, intent, json.dumps(context)))
        
        conn.commit()
        conn.close()
        
        # Increment interaction count
        self.increment_interactions()
    
    def start_session(self, session_id: str):
        """Record session start"""
        conn = sqlite3.connect(self.main_db)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO activation_history (session_id, activation_time)
        VALUES (?, ?)
        ''', (session_id, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        # Increment session count
        current_sessions = int(self.get_persistent_stat('total_sessions') or 0)
        self.update_persistent_stat('total_sessions', str(current_sessions + 1))
    
    def end_session(self, session_id: str, interaction_count: int, topics: List[str]):
        """Record session end"""
        conn = sqlite3.connect(self.main_db)
        cursor = conn.cursor()
        
        # Update the activation record
        cursor.execute('''
        UPDATE activation_history 
        SET deactivation_time = ?, total_interactions = ?, key_topics = ?
        WHERE session_id = ? AND deactivation_time IS NULL
        ''', (datetime.now().isoformat(), interaction_count, json.dumps(topics), session_id))
        
        conn.commit()
        conn.close()
    
    def record_autonomous_improvement(self, session_id: str, improvement_type: str, description: str):
        """Record autonomous learning/improvement"""
        conn = sqlite3.connect(self.main_db)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO autonomous_learning 
        (session_id, learning_type, improvement_description, knowledge_gained)
        VALUES (?, ?, ?, ?)
        ''', (session_id, improvement_type, description, f"Autonomous improvement: {description}"))
        
        conn.commit()
        conn.close()
        
        # Update learning iterations
        current = int(self.get_persistent_stat('learning_iterations') or 0)
        self.update_persistent_stat('learning_iterations', str(current + 1))
        self.update_persistent_stat('last_autonomous_improvement', datetime.now().isoformat())
    
    def get_total_interactions(self) -> int:
        """Get total interactions across all sessions"""
        return int(self.get_persistent_stat('total_interactions') or 0)
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        conn = sqlite3.connect(self.main_db)
        cursor = conn.cursor()
        
        stats = {}
        cursor.execute("SELECT stat_name, stat_value FROM system_stats")
        for stat_name, stat_value in cursor.fetchall():
            stats[stat_name] = stat_value
        
        # Get conversation count
        cursor.execute("SELECT COUNT(*) FROM all_conversations")
        stats['total_conversations'] = cursor.fetchone()[0]
        
        # Get session count
        cursor.execute("SELECT COUNT(*) FROM activation_history")
        stats['activation_sessions'] = cursor.fetchone()[0]
        
        # Get recent learning activity
        cursor.execute("SELECT COUNT(*) FROM autonomous_learning WHERE timestamp > datetime('now', '-1 hour')")
        stats['recent_learning_events'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
