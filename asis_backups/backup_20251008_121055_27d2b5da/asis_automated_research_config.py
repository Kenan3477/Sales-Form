#!/usr/bin/env python3
"""
ASIS Automated Research Configuration System
Sets up continuous learning topics and automated research scheduling
"""

import sqlite3
import json
import threading
import time
import schedule
from datetime import datetime, timedelta
from typing import Dict, List, Any
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class ASISAutomatedResearchConfig:
    def __init__(self):
        self.config_db = 'asis_automated_research_config.db'
        self.research_scheduler_active = False
        self.scheduler_thread = None
        self._init_database()
        self._setup_default_topics()
    
    def _init_database(self):
        """Initialize automated research configuration database"""
        conn = sqlite3.connect(self.config_db)
        cursor = conn.cursor()
        
        # Research topics configuration
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS research_topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                topic TEXT NOT NULL,
                search_terms TEXT NOT NULL,
                priority INTEGER DEFAULT 5,
                frequency_hours INTEGER DEFAULT 24,
                last_researched TIMESTAMP,
                research_count INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0,
                active BOOLEAN DEFAULT 1,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Research schedule configuration
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS research_schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                schedule_type TEXT NOT NULL, -- 'hourly', 'daily', 'weekly'
                interval_value INTEGER NOT NULL,
                max_topics_per_run INTEGER DEFAULT 3,
                active BOOLEAN DEFAULT 1,
                last_run TIMESTAMP,
                total_runs INTEGER DEFAULT 0,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Research performance tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS research_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id INTEGER,
                research_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                success BOOLEAN,
                findings_count INTEGER DEFAULT 0,
                relevance_score REAL DEFAULT 0.0,
                processing_time REAL DEFAULT 0.0,
                error_message TEXT,
                FOREIGN KEY (topic_id) REFERENCES research_topics (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _setup_default_topics(self):
        """Set up default research topics for continuous learning"""
        
        default_topics = [
            # AI and Technology
            {
                'category': 'artificial_intelligence',
                'topic': 'AI Technology Advances',
                'search_terms': 'artificial intelligence breakthrough technology 2024 2025',
                'priority': 10,
                'frequency_hours': 6
            },
            {
                'category': 'machine_learning',
                'topic': 'Machine Learning Research',
                'search_terms': 'machine learning deep learning neural networks research',
                'priority': 9,
                'frequency_hours': 8
            },
            {
                'category': 'technology_trends',
                'topic': 'Emerging Technology Trends',
                'search_terms': 'technology trends innovation emerging tech startup',
                'priority': 8,
                'frequency_hours': 12
            },
            
            # Science and Research
            {
                'category': 'quantum_computing',
                'topic': 'Quantum Computing Developments',
                'search_terms': 'quantum computing qubits quantum algorithms IBM Google',
                'priority': 7,
                'frequency_hours': 24
            },
            {
                'category': 'biotechnology',
                'topic': 'Biotechnology Innovations',
                'search_terms': 'biotechnology gene therapy CRISPR medical research',
                'priority': 6,
                'frequency_hours': 24
            },
            {
                'category': 'space_technology',
                'topic': 'Space Exploration Updates',
                'search_terms': 'space exploration mars missions SpaceX NASA satellite',
                'priority': 5,
                'frequency_hours': 48
            },
            
            # Business and Economics
            {
                'category': 'fintech',
                'topic': 'Financial Technology',
                'search_terms': 'fintech blockchain cryptocurrency digital payments DeFi',
                'priority': 6,
                'frequency_hours': 24
            },
            {
                'category': 'startup_ecosystem',
                'topic': 'Startup and Investment Trends',
                'search_terms': 'startup funding venture capital unicorn company valuation',
                'priority': 5,
                'frequency_hours': 48
            },
            
            # Environmental and Sustainability
            {
                'category': 'sustainability',
                'topic': 'Climate and Sustainability',
                'search_terms': 'climate change renewable energy sustainability green technology',
                'priority': 7,
                'frequency_hours': 24
            },
            {
                'category': 'clean_energy',
                'topic': 'Clean Energy Innovation',
                'search_terms': 'solar power wind energy battery technology energy storage',
                'priority': 6,
                'frequency_hours': 36
            },
            
            # Health and Medicine
            {
                'category': 'medical_ai',
                'topic': 'AI in Healthcare',
                'search_terms': 'artificial intelligence healthcare medical diagnosis AI medicine',
                'priority': 8,
                'frequency_hours': 12
            },
            {
                'category': 'medical_research',
                'topic': 'Medical Research Breakthroughs',
                'search_terms': 'medical research breakthrough drug discovery clinical trials',
                'priority': 7,
                'frequency_hours': 24
            },
            
            # Education and Learning
            {
                'category': 'educational_technology',
                'topic': 'Educational Technology',
                'search_terms': 'educational technology online learning AI tutoring EdTech',
                'priority': 5,
                'frequency_hours': 48
            },
            
            # Cybersecurity
            {
                'category': 'cybersecurity',
                'topic': 'Cybersecurity Developments',
                'search_terms': 'cybersecurity data protection privacy security breach AI security',
                'priority': 8,
                'frequency_hours': 12
            }
        ]
        
        conn = sqlite3.connect(self.config_db)
        cursor = conn.cursor()
        
        # Check if topics already exist
        cursor.execute('SELECT COUNT(*) FROM research_topics')
        existing_count = cursor.fetchone()[0]
        
        if existing_count == 0:
            print("📚 Setting up default research topics...")
            for topic in default_topics:
                cursor.execute('''
                    INSERT INTO research_topics 
                    (category, topic, search_terms, priority, frequency_hours)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    topic['category'],
                    topic['topic'],
                    topic['search_terms'],
                    topic['priority'],
                    topic['frequency_hours']
                ))
            
            print(f"✅ Added {len(default_topics)} default research topics")
        
        # Set up default schedule
        cursor.execute('SELECT COUNT(*) FROM research_schedule')
        schedule_count = cursor.fetchone()[0]
        
        if schedule_count == 0:
            # Add multiple schedule configurations
            schedules = [
                ('hourly', 2, 2),     # Every 2 hours, max 2 topics
                ('daily', 1, 5),      # Daily, max 5 topics  
                ('weekly', 1, 10)     # Weekly comprehensive research
            ]
            
            for schedule_type, interval, max_topics in schedules:
                cursor.execute('''
                    INSERT INTO research_schedule 
                    (schedule_type, interval_value, max_topics_per_run)
                    VALUES (?, ?, ?)
                ''', (schedule_type, interval, max_topics))
            
            print("✅ Set up default research schedules")
        
        conn.commit()
        conn.close()
    
    def get_active_topics(self, max_topics: int = None) -> List[Dict]:
        """Get active research topics ready for research"""
        
        conn = sqlite3.connect(self.config_db)
        cursor = conn.cursor()
        
        current_time = datetime.now()
        
        # Get topics that haven't been researched recently
        query = '''
            SELECT id, category, topic, search_terms, priority, frequency_hours, 
                   last_researched, research_count, success_rate
            FROM research_topics 
            WHERE active = 1 
            AND (last_researched IS NULL OR 
                 datetime(last_researched, '+' || frequency_hours || ' hours') <= datetime('now'))
            ORDER BY priority DESC, last_researched ASC
        '''
        
        if max_topics:
            query += f' LIMIT {max_topics}'
        
        cursor.execute(query)
        topics = []
        
        for row in cursor.fetchall():
            topics.append({
                'id': row[0],
                'category': row[1],
                'topic': row[2],
                'search_terms': row[3],
                'priority': row[4],
                'frequency_hours': row[5],
                'last_researched': row[6],
                'research_count': row[7],
                'success_rate': row[8]
            })
        
        conn.close()
        return topics
    
    def update_research_performance(self, topic_id: int, success: bool, 
                                  findings_count: int = 0, relevance_score: float = 0.0,
                                  processing_time: float = 0.0, error_message: str = None):
        """Update research performance tracking"""
        
        conn = sqlite3.connect(self.config_db)
        cursor = conn.cursor()
        
        # Log performance
        cursor.execute('''
            INSERT INTO research_performance 
            (topic_id, success, findings_count, relevance_score, processing_time, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (topic_id, success, findings_count, relevance_score, processing_time, error_message))
        
        # Update topic statistics
        cursor.execute('''
            UPDATE research_topics 
            SET last_researched = CURRENT_TIMESTAMP,
                research_count = research_count + 1
            WHERE id = ?
        ''', (topic_id,))
        
        # Update success rate
        cursor.execute('''
            SELECT COUNT(*), SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END)
            FROM research_performance 
            WHERE topic_id = ?
        ''', (topic_id,))
        
        total_runs, successful_runs = cursor.fetchone()
        if total_runs > 0:
            success_rate = successful_runs / total_runs
            cursor.execute('''
                UPDATE research_topics 
                SET success_rate = ?
                WHERE id = ?
            ''', (success_rate, topic_id))
        
        conn.commit()
        conn.close()
    
    def add_custom_topic(self, category: str, topic: str, search_terms: str,
                        priority: int = 5, frequency_hours: int = 24) -> int:
        """Add a custom research topic"""
        
        conn = sqlite3.connect(self.config_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO research_topics 
            (category, topic, search_terms, priority, frequency_hours)
            VALUES (?, ?, ?, ?, ?)
        ''', (category, topic, search_terms, priority, frequency_hours))
        
        topic_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return topic_id
    
    def get_research_statistics(self) -> Dict[str, Any]:
        """Get comprehensive research statistics"""
        
        conn = sqlite3.connect(self.config_db)
        cursor = conn.cursor()
        
        # Topic statistics
        cursor.execute('''
            SELECT COUNT(*) as total_topics,
                   COUNT(CASE WHEN active = 1 THEN 1 END) as active_topics,
                   AVG(success_rate) as avg_success_rate,
                   SUM(research_count) as total_research_sessions
            FROM research_topics
        ''')
        
        topic_stats = cursor.fetchone()
        
        # Performance statistics
        cursor.execute('''
            SELECT COUNT(*) as total_runs,
                   COUNT(CASE WHEN success = 1 THEN 1 END) as successful_runs,
                   AVG(relevance_score) as avg_relevance,
                   AVG(processing_time) as avg_processing_time,
                   SUM(findings_count) as total_findings
            FROM research_performance
        ''')
        
        perf_stats = cursor.fetchone()
        
        # Category breakdown
        cursor.execute('''
            SELECT category, COUNT(*) as topic_count, AVG(success_rate) as category_success_rate
            FROM research_topics
            WHERE active = 1
            GROUP BY category
            ORDER BY category_success_rate DESC
        ''')
        
        category_stats = [{'category': row[0], 'topics': row[1], 'success_rate': row[2]} 
                         for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            'topics': {
                'total': topic_stats[0] or 0,
                'active': topic_stats[1] or 0,
                'avg_success_rate': topic_stats[2] or 0.0,
                'total_sessions': topic_stats[3] or 0
            },
            'performance': {
                'total_runs': perf_stats[0] or 0,
                'successful_runs': perf_stats[1] or 0,
                'avg_relevance': perf_stats[2] or 0.0,
                'avg_processing_time': perf_stats[3] or 0.0,
                'total_findings': perf_stats[4] or 0
            },
            'categories': category_stats
        }
    
    def start_automated_research(self):
        """Start the automated research scheduler"""
        
        if self.research_scheduler_active:
            print("⚠️  Automated research scheduler is already running")
            return
        
        print("🚀 Starting automated research scheduler...")
        
        # Schedule different research intervals
        schedule.every(2).hours.do(self._run_hourly_research)
        schedule.every().day.at("09:00").do(self._run_daily_research)
        schedule.every().week.do(self._run_weekly_research)
        
        self.research_scheduler_active = True
        
        # Start scheduler in background thread
        def run_scheduler():
            while self.research_scheduler_active:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        print("✅ Automated research scheduler started!")
        print("  • Hourly research: Every 2 hours")
        print("  • Daily research: 9:00 AM every day") 
        print("  • Weekly research: Comprehensive weekly sessions")
    
    def stop_automated_research(self):
        """Stop the automated research scheduler"""
        
        if not self.research_scheduler_active:
            print("⚠️  Automated research scheduler is not running")
            return
        
        self.research_scheduler_active = False
        schedule.clear()
        
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        
        print("🛑 Automated research scheduler stopped")
    
    def _run_hourly_research(self):
        """Run high-priority research topics every 2 hours"""
        self._execute_scheduled_research('hourly', max_topics=2)
    
    def _run_daily_research(self):
        """Run daily research session"""
        self._execute_scheduled_research('daily', max_topics=5)
    
    def _run_weekly_research(self):
        """Run comprehensive weekly research"""
        self._execute_scheduled_research('weekly', max_topics=10)
    
    def _execute_scheduled_research(self, schedule_type: str, max_topics: int):
        """Execute a scheduled research session"""
        
        print(f"🔬 Running {schedule_type} automated research...")
        
        try:
            from asis_autonomous_research_fixed import ASISAutonomousResearch
            research_system = ASISAutonomousResearch()
            
            # Get topics for this session
            topics = self.get_active_topics(max_topics)
            
            if not topics:
                print(f"  ⚠️  No topics available for {schedule_type} research")
                return
            
            successful_sessions = 0
            total_findings = 0
            
            for topic in topics:
                start_time = time.time()
                
                try:
                    print(f"  📚 Researching: {topic['topic']}")
                    
                    result = research_system.force_research_session(
                        topic['topic'], 
                        topic['search_terms']
                    )
                    
                    processing_time = time.time() - start_time
                    success = result.get('status') == 'completed'
                    findings_count = result.get('findings_count', 0)
                    relevance_score = result.get('average_relevance', 0.0)
                    
                    if success:
                        successful_sessions += 1
                        total_findings += findings_count
                    
                    # Update performance tracking
                    self.update_research_performance(
                        topic['id'], success, findings_count, 
                        relevance_score, processing_time
                    )
                    
                except Exception as e:
                    processing_time = time.time() - start_time
                    print(f"    ❌ Research error: {e}")
                    
                    self.update_research_performance(
                        topic['id'], False, 0, 0.0, processing_time, str(e)
                    )
            
            # Update schedule tracking
            conn = sqlite3.connect(self.config_db)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE research_schedule 
                SET last_run = CURRENT_TIMESTAMP, total_runs = total_runs + 1
                WHERE schedule_type = ?
            ''', (schedule_type,))
            conn.commit()
            conn.close()
            
            print(f"  ✅ {schedule_type.title()} research completed:")
            print(f"    • Successful sessions: {successful_sessions}/{len(topics)}")
            print(f"    • Total findings: {total_findings}")
            
        except Exception as e:
            print(f"  ❌ Scheduled research error: {e}")

def main():
    """Initialize and demonstrate automated research configuration"""
    
    print("🤖 ASIS Automated Research Configuration")
    print("=" * 50)
    
    config = ASISAutomatedResearchConfig()
    
    # Show current statistics
    stats = config.get_research_statistics()
    print(f"\n📊 Research Configuration:")
    print(f"  • Active Topics: {stats['topics']['active']}")
    print(f"  • Categories: {len(stats['categories'])}")
    print(f"  • Total Sessions: {stats['topics']['total_sessions']}")
    
    # Show ready topics
    ready_topics = config.get_active_topics(5)
    print(f"\n🎯 Topics Ready for Research ({len(ready_topics)}):")
    for topic in ready_topics[:3]:  # Show first 3
        print(f"  • {topic['topic']} (Priority: {topic['priority']})")
    
    print(f"\n✅ Automated research system configured!")
    print(f"🚀 Use start_automated_research() to begin continuous learning")
    
    return config

if __name__ == "__main__":
    main()
