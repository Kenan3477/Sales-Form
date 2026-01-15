#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗄️ ASIS AGI Database Migration System
Handles database schema creation and updates for AGI production deployment

This migration system manages:
- AGI tasks and results storage
- Cross-domain patterns and learning data
- Consciousness states and metrics
- Performance benchmarks and monitoring
- User access and subscription data

Author: ASIS AGI Development Team
Version: 1.0.0
"""

import sqlite3
import psycopg2
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class AGIDatabaseMigrator:
    """Handles AGI database migrations for production deployment"""
    
    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or os.getenv('DATABASE_URL', 'sqlite:///asis_agi_production.db')
        self.is_postgres = self.database_url.startswith('postgres')
        
    def run_migrations(self):
        """Run all database migrations"""
        print("🗄️ Starting AGI Database Migrations...")
        
        migrations = [
            self._create_agi_tasks_table,
            self._create_cross_domain_patterns_table,
            self._create_consciousness_states_table,
            self._create_performance_metrics_table,
            self._create_user_subscriptions_table,
            self._create_agi_usage_tracking_table,
            self._create_system_health_table,
            self._create_learning_events_table,
            self._insert_initial_data
        ]
        
        for i, migration in enumerate(migrations, 1):
            try:
                print(f"📊 Running migration {i}/{len(migrations)}: {migration.__name__}")
                migration()
                print(f"✅ Migration {i} completed successfully")
            except Exception as e:
                print(f"❌ Migration {i} failed: {e}")
                raise
        
        print("✅ All AGI database migrations completed successfully!")
    
    def _get_connection(self):
        """Get database connection"""
        if self.is_postgres:
            return psycopg2.connect(self.database_url)
        else:
            db_path = self.database_url.replace('sqlite:///', '')
            return sqlite3.connect(db_path)
    
    def _create_agi_tasks_table(self):
        """Create AGI tasks table"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if self.is_postgres:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agi_tasks (
                    id SERIAL PRIMARY KEY,
                    task_id VARCHAR(32) UNIQUE NOT NULL,
                    user_id VARCHAR(64),
                    task_type VARCHAR(50) NOT NULL,
                    description TEXT NOT NULL,
                    domain VARCHAR(50) NOT NULL,
                    complexity REAL NOT NULL,
                    priority REAL NOT NULL,
                    status VARCHAR(20) NOT NULL DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    processing_time REAL,
                    verification_score REAL,
                    solution_data JSONB,
                    error_message TEXT,
                    agi_components_used JSONB,
                    cross_domain_insights INTEGER DEFAULT 0
                );
                
                CREATE INDEX IF NOT EXISTS idx_agi_tasks_user_id ON agi_tasks(user_id);
                CREATE INDEX IF NOT EXISTS idx_agi_tasks_status ON agi_tasks(status);
                CREATE INDEX IF NOT EXISTS idx_agi_tasks_domain ON agi_tasks(domain);
                CREATE INDEX IF NOT EXISTS idx_agi_tasks_created_at ON agi_tasks(created_at);
            ''')
        else:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agi_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT UNIQUE NOT NULL,
                    user_id TEXT,
                    task_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    complexity REAL NOT NULL,
                    priority REAL NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    started_at TEXT,
                    completed_at TEXT,
                    processing_time REAL,
                    verification_score REAL,
                    solution_data TEXT,
                    error_message TEXT,
                    agi_components_used TEXT,
                    cross_domain_insights INTEGER DEFAULT 0
                );
            ''')
        
        conn.commit()
        conn.close()
    
    def _create_cross_domain_patterns_table(self):
        """Create cross-domain patterns table"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if self.is_postgres:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cross_domain_patterns (
                    id SERIAL PRIMARY KEY,
                    pattern_id VARCHAR(32) UNIQUE NOT NULL,
                    source_domain VARCHAR(50) NOT NULL,
                    target_domain VARCHAR(50) NOT NULL,
                    pattern_description TEXT NOT NULL,
                    pattern_data JSONB,
                    effectiveness_score REAL NOT NULL DEFAULT 0.5,
                    usage_count INTEGER DEFAULT 0,
                    success_rate REAL DEFAULT 0.0,
                    last_used_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE
                );
                
                CREATE INDEX IF NOT EXISTS idx_patterns_source_domain ON cross_domain_patterns(source_domain);
                CREATE INDEX IF NOT EXISTS idx_patterns_target_domain ON cross_domain_patterns(target_domain);
                CREATE INDEX IF NOT EXISTS idx_patterns_effectiveness ON cross_domain_patterns(effectiveness_score);
            ''')
        else:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cross_domain_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_id TEXT UNIQUE NOT NULL,
                    source_domain TEXT NOT NULL,
                    target_domain TEXT NOT NULL,
                    pattern_description TEXT NOT NULL,
                    pattern_data TEXT,
                    effectiveness_score REAL NOT NULL DEFAULT 0.5,
                    usage_count INTEGER DEFAULT 0,
                    success_rate REAL DEFAULT 0.0,
                    last_used_at TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    is_active INTEGER DEFAULT 1
                );
            ''')
        
        conn.commit()
        conn.close()
    
    def _create_consciousness_states_table(self):
        """Create consciousness states tracking table"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if self.is_postgres:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS consciousness_states (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    consciousness_level REAL NOT NULL,
                    cognitive_state VARCHAR(50) NOT NULL,
                    processing_load REAL DEFAULT 0.0,
                    self_awareness_score REAL DEFAULT 0.0,
                    meta_cognitive_activity REAL DEFAULT 0.0,
                    learning_rate REAL DEFAULT 0.0,
                    system_coherence REAL DEFAULT 0.0,
                    active_processes JSONB,
                    internal_state_data JSONB
                );
                
                CREATE INDEX IF NOT EXISTS idx_consciousness_timestamp ON consciousness_states(timestamp);
                CREATE INDEX IF NOT EXISTS idx_consciousness_level ON consciousness_states(consciousness_level);
            ''')
        else:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS consciousness_states (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    consciousness_level REAL NOT NULL,
                    cognitive_state TEXT NOT NULL,
                    processing_load REAL DEFAULT 0.0,
                    self_awareness_score REAL DEFAULT 0.0,
                    meta_cognitive_activity REAL DEFAULT 0.0,
                    learning_rate REAL DEFAULT 0.0,
                    system_coherence REAL DEFAULT 0.0,
                    active_processes TEXT,
                    internal_state_data TEXT
                );
            ''')
        
        conn.commit()
        conn.close()
    
    def _create_performance_metrics_table(self):
        """Create performance metrics table"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if self.is_postgres:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id SERIAL PRIMARY KEY,
                    metric_id VARCHAR(32) UNIQUE NOT NULL,
                    metric_name VARCHAR(100) NOT NULL,
                    metric_category VARCHAR(50) NOT NULL,
                    metric_value REAL NOT NULL,
                    baseline_value REAL,
                    improvement_percentage REAL,
                    measurement_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    context_data JSONB,
                    tags JSONB
                );
                
                CREATE INDEX IF NOT EXISTS idx_metrics_category ON performance_metrics(metric_category);
                CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON performance_metrics(measurement_timestamp);
            ''')
        else:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_id TEXT UNIQUE NOT NULL,
                    metric_name TEXT NOT NULL,
                    metric_category TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    baseline_value REAL,
                    improvement_percentage REAL,
                    measurement_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    context_data TEXT,
                    tags TEXT
                );
            ''')
        
        conn.commit()
        conn.close()
    
    def _create_user_subscriptions_table(self):
        """Create user subscriptions table"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if self.is_postgres:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_subscriptions (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(64) UNIQUE NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    subscription_tier VARCHAR(20) NOT NULL DEFAULT 'free',
                    agi_requests_used INTEGER DEFAULT 0,
                    agi_requests_limit INTEGER NOT NULL,
                    self_modification_allowed BOOLEAN DEFAULT FALSE,
                    cross_domain_access BOOLEAN DEFAULT FALSE,
                    priority_processing BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    payment_info JSONB,
                    usage_stats JSONB
                );
                
                CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id ON user_subscriptions(user_id);
                CREATE INDEX IF NOT EXISTS idx_subscriptions_tier ON user_subscriptions(subscription_tier);
            ''')
        else:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_subscriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE NOT NULL,
                    email TEXT NOT NULL,
                    subscription_tier TEXT NOT NULL DEFAULT 'free',
                    agi_requests_used INTEGER DEFAULT 0,
                    agi_requests_limit INTEGER NOT NULL,
                    self_modification_allowed INTEGER DEFAULT 0,
                    cross_domain_access INTEGER DEFAULT 0,
                    priority_processing INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    expires_at TEXT,
                    is_active INTEGER DEFAULT 1,
                    payment_info TEXT,
                    usage_stats TEXT
                );
            ''')
        
        conn.commit()
        conn.close()
    
    def _create_agi_usage_tracking_table(self):
        """Create AGI usage tracking table"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if self.is_postgres:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agi_usage_tracking (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(64) NOT NULL,
                    task_id VARCHAR(32) NOT NULL,
                    feature_used VARCHAR(50) NOT NULL,
                    usage_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    processing_time REAL,
                    success BOOLEAN NOT NULL,
                    cost_units INTEGER DEFAULT 1,
                    ip_address INET,
                    user_agent TEXT,
                    api_endpoint VARCHAR(100),
                    request_data JSONB,
                    response_size INTEGER
                );
                
                CREATE INDEX IF NOT EXISTS idx_usage_user_id ON agi_usage_tracking(user_id);
                CREATE INDEX IF NOT EXISTS idx_usage_timestamp ON agi_usage_tracking(usage_timestamp);
                CREATE INDEX IF NOT EXISTS idx_usage_feature ON agi_usage_tracking(feature_used);
            ''')
        else:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agi_usage_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    task_id TEXT NOT NULL,
                    feature_used TEXT NOT NULL,
                    usage_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    processing_time REAL,
                    success INTEGER NOT NULL,
                    cost_units INTEGER DEFAULT 1,
                    ip_address TEXT,
                    user_agent TEXT,
                    api_endpoint TEXT,
                    request_data TEXT,
                    response_size INTEGER
                );
            ''')
        
        conn.commit()
        conn.close()
    
    def _create_system_health_table(self):
        """Create system health monitoring table"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if self.is_postgres:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_health (
                    id SERIAL PRIMARY KEY,
                    check_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    component_name VARCHAR(50) NOT NULL,
                    health_status VARCHAR(20) NOT NULL,
                    response_time_ms REAL,
                    error_rate REAL DEFAULT 0.0,
                    cpu_usage REAL,
                    memory_usage REAL,
                    active_connections INTEGER,
                    queue_length INTEGER,
                    custom_metrics JSONB,
                    alerts_triggered JSONB
                );
                
                CREATE INDEX IF NOT EXISTS idx_health_timestamp ON system_health(check_timestamp);
                CREATE INDEX IF NOT EXISTS idx_health_component ON system_health(component_name);
                CREATE INDEX IF NOT EXISTS idx_health_status ON system_health(health_status);
            ''')
        else:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_health (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    check_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    component_name TEXT NOT NULL,
                    health_status TEXT NOT NULL,
                    response_time_ms REAL,
                    error_rate REAL DEFAULT 0.0,
                    cpu_usage REAL,
                    memory_usage REAL,
                    active_connections INTEGER,
                    queue_length INTEGER,
                    custom_metrics TEXT,
                    alerts_triggered TEXT
                );
            ''')
        
        conn.commit()
        conn.close()
    
    def _create_learning_events_table(self):
        """Create learning events table"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if self.is_postgres:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learning_events (
                    id SERIAL PRIMARY KEY,
                    event_id VARCHAR(32) UNIQUE NOT NULL,
                    event_type VARCHAR(50) NOT NULL,
                    source_domain VARCHAR(50),
                    target_domain VARCHAR(50),
                    learning_data JSONB NOT NULL,
                    effectiveness_score REAL,
                    confidence_level REAL,
                    impact_assessment REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    applied_at TIMESTAMP,
                    verification_status VARCHAR(20) DEFAULT 'pending',
                    feedback_score REAL
                );
                
                CREATE INDEX IF NOT EXISTS idx_learning_type ON learning_events(event_type);
                CREATE INDEX IF NOT EXISTS idx_learning_timestamp ON learning_events(created_at);
            ''')
        else:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learning_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT UNIQUE NOT NULL,
                    event_type TEXT NOT NULL,
                    source_domain TEXT,
                    target_domain TEXT,
                    learning_data TEXT NOT NULL,
                    effectiveness_score REAL,
                    confidence_level REAL,
                    impact_assessment REAL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    applied_at TEXT,
                    verification_status TEXT DEFAULT 'pending',
                    feedback_score REAL
                );
            ''')
        
        conn.commit()
        conn.close()
    
    def _insert_initial_data(self):
        """Insert initial configuration and reference data"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Insert subscription tiers
        subscription_tiers = [
            ('free', 10, False, False, False),
            ('basic', 100, True, False, False),
            ('professional', 1000, True, True, True),
            ('enterprise', 10000, True, True, True)
        ]
        
        if self.is_postgres:
            for tier, limit, self_mod, cross_domain, priority in subscription_tiers:
                cursor.execute('''
                    INSERT INTO user_subscriptions 
                    (user_id, email, subscription_tier, agi_requests_limit, 
                     self_modification_allowed, cross_domain_access, priority_processing)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (user_id) DO NOTHING
                ''', (f'template_{tier}', f'{tier}@example.com', tier, limit, self_mod, cross_domain, priority))
        else:
            for tier, limit, self_mod, cross_domain, priority in subscription_tiers:
                cursor.execute('''
                    INSERT OR IGNORE INTO user_subscriptions 
                    (user_id, email, subscription_tier, agi_requests_limit, 
                     self_modification_allowed, cross_domain_access, priority_processing)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (f'template_{tier}', f'{tier}@example.com', tier, limit, self_mod, cross_domain, priority))
        
        # Insert initial performance baselines
        baseline_metrics = [
            ('problem_solving_speed', 'performance', 2.5, 'seconds'),
            ('solution_quality', 'performance', 0.75, 'score'),
            ('consciousness_level', 'system', 0.85, 'level'),
            ('learning_rate', 'system', 0.70, 'rate'),
            ('cross_domain_effectiveness', 'learning', 0.65, 'score')
        ]
        
        for metric, category, value, unit in baseline_metrics:
            metric_id = f"baseline_{metric}"
            if self.is_postgres:
                cursor.execute('''
                    INSERT INTO performance_metrics 
                    (metric_id, metric_name, metric_category, metric_value, baseline_value)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (metric_id) DO NOTHING
                ''', (metric_id, metric, category, value, value))
            else:
                cursor.execute('''
                    INSERT OR IGNORE INTO performance_metrics 
                    (metric_id, metric_name, metric_category, metric_value, baseline_value)
                    VALUES (?, ?, ?, ?, ?)
                ''', (metric_id, metric, category, value, value))
        
        conn.commit()
        conn.close()

def main():
    """Main migration function"""
    print("🗄️ ASIS AGI Database Migration System")
    print("=" * 50)
    
    try:
        migrator = AGIDatabaseMigrator()
        migrator.run_migrations()
        
        print("\n✅ AGI database migrations completed successfully!")
        print("🚀 Ready for production deployment!")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
