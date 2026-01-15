#!/usr/bin/env python3
"""
ASIS Real-Time Research Monitor
Watch ASIS learn and expand its knowledge in real-time
"""

import sqlite3
import time
import os
import sys
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class ASISRealTimeMonitor:
    def __init__(self):
        self.research_db = 'asis_autonomous_research_fixed.db'
        self.config_db = 'asis_automated_research_config.db'
        self.pattern_db = 'asis_patterns_fixed.db'
        self.last_findings_count = 0
        self.last_sessions_count = 0
        self.monitoring = False
        
    def get_live_stats(self) -> Dict[str, Any]:
        """Get current live statistics"""
        stats = {}
        
        # Research database stats
        if os.path.exists(self.research_db):
            conn = sqlite3.connect(self.research_db)
            cursor = conn.cursor()
            
            try:
                cursor.execute('SELECT COUNT(*) FROM research_findings')
                stats['total_findings'] = cursor.fetchone()[0]
                
                cursor.execute('SELECT COUNT(*) FROM research_sessions')
                stats['total_sessions'] = cursor.fetchone()[0]
                
                # Recent findings
                cursor.execute('''
                    SELECT title, content, relevance_score, extraction_time 
                    FROM research_findings 
                    ORDER BY extraction_time DESC 
                    LIMIT 3
                ''')
                stats['recent_findings'] = cursor.fetchall()
                
                # Recent sessions
                cursor.execute('''
                    SELECT session_id, topic, start_time, end_time, status, findings_count 
                    FROM research_sessions 
                    ORDER BY start_time DESC 
                    LIMIT 3
                ''')
                stats['recent_sessions'] = cursor.fetchall()
                
            except Exception as e:
                stats['research_error'] = str(e)
            finally:
                conn.close()
        
        # Config database stats
        if os.path.exists(self.config_db):
            conn = sqlite3.connect(self.config_db)
            cursor = conn.cursor()
            
            try:
                cursor.execute('SELECT COUNT(*) FROM research_topics WHERE active = 1')
                stats['active_topics'] = cursor.fetchone()[0]
                
                # Next topics ready for research
                cursor.execute('''
                    SELECT topic, priority, last_researched, frequency_hours
                    FROM research_topics 
                    WHERE active = 1 
                    AND (last_researched IS NULL OR 
                         datetime(last_researched, '+' || frequency_hours || ' hours') <= datetime('now'))
                    ORDER BY priority DESC 
                    LIMIT 5
                ''')
                stats['ready_topics'] = cursor.fetchall()
                
            except Exception as e:
                stats['config_error'] = str(e)
            finally:
                conn.close()
        
        return stats
    
    def detect_new_activity(self, current_stats: Dict, previous_stats: Dict) -> List[str]:
        """Detect new research activity"""
        activities = []
        
        # New findings
        if current_stats.get('total_findings', 0) > previous_stats.get('total_findings', 0):
            new_findings = current_stats['total_findings'] - previous_stats.get('total_findings', 0)
            activities.append(f"🔍 {new_findings} new research finding(s) discovered!")
            
            # Show new findings details
            if current_stats.get('recent_findings'):
                for title, content, score, timestamp in current_stats['recent_findings'][:new_findings]:
                    activities.append(f"   📚 '{title}' (confidence: {score:.2f})")
        
        # New sessions
        if current_stats.get('total_sessions', 0) > previous_stats.get('total_sessions', 0):
            new_sessions = current_stats['total_sessions'] - previous_stats.get('total_sessions', 0)
            activities.append(f"🚀 {new_sessions} new research session(s) started!")
            
            # Show session details
            if current_stats.get('recent_sessions'):
                for session_id, topic, start_time, end_time, status, findings_count in current_stats['recent_sessions'][:new_sessions]:
                    status_icon = "✅" if status == "completed" else "🔄" if status == "active" else "⚠️"
                    activities.append(f"   {status_icon} Researching: '{topic}'")
        
        return activities
    
    def display_current_status(self, stats: Dict):
        """Display current research status"""
        print(f"\n🤖 ASIS Live Research Status - {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 60)
        
        # Basic stats
        print(f"📊 Knowledge Base:")
        print(f"   • Total Findings: {stats.get('total_findings', 0)}")
        print(f"   • Research Sessions: {stats.get('total_sessions', 0)}")
        print(f"   • Active Topics: {stats.get('active_topics', 0)}")
        
        # Recent findings
        if stats.get('recent_findings'):
            print(f"\n🔍 Latest Discoveries:")
            for i, (title, content, score, timestamp) in enumerate(stats['recent_findings'][:3], 1):
                print(f"   {i}. {title}")
                print(f"      Content: {content[:80]}...")
                print(f"      Confidence: {score:.2f} | Time: {timestamp}")
        
        # Ready topics
        if stats.get('ready_topics'):
            print(f"\n🎯 Next Research Topics Ready:")
            for topic, priority, last_researched, frequency in stats['ready_topics'][:3]:
                last_time = "Never" if not last_researched else last_researched
                print(f"   • {topic} (Priority: {priority})")
                print(f"     Last researched: {last_time}")
        
        # Recent sessions
        if stats.get('recent_sessions'):
            print(f"\n🚀 Recent Research Sessions:")
            for session_id, topic, start_time, end_time, status, findings_count in stats['recent_sessions'][:2]:
                status_icon = "✅" if status == "completed" else "🔄" if status == "active" else "⚠️"
                duration = "In progress" if not end_time else f"{(datetime.fromisoformat(end_time) - datetime.fromisoformat(start_time)).seconds}s"
                print(f"   {status_icon} {topic}")
                print(f"     Duration: {duration} | Findings: {findings_count}")
    
    def start_monitoring(self, refresh_interval: int = 30):
        """Start real-time monitoring"""
        
        print("🔍 ASIS REAL-TIME RESEARCH MONITOR")
        print("=" * 50)
        print("Watching ASIS learn and expand its knowledge...")
        print(f"Refresh interval: {refresh_interval} seconds")
        print("Press Ctrl+C to stop monitoring\n")
        
        self.monitoring = True
        previous_stats = {}
        
        try:
            while self.monitoring:
                current_stats = self.get_live_stats()
                
                # Detect new activity
                if previous_stats:
                    new_activities = self.detect_new_activity(current_stats, previous_stats)
                    if new_activities:
                        print(f"\n🚨 NEW ACTIVITY DETECTED!")
                        for activity in new_activities:
                            print(f"   {activity}")
                        print()
                
                # Display current status
                self.display_current_status(current_stats)
                
                previous_stats = current_stats.copy()
                
                # Wait for next refresh
                print(f"\n⏱️  Next update in {refresh_interval} seconds... (Ctrl+C to stop)")
                time.sleep(refresh_interval)
                
                # Clear screen for next update
                os.system('cls' if os.name == 'nt' else 'clear')
                
        except KeyboardInterrupt:
            print(f"\n\n🛑 Monitoring stopped by user")
            self.monitoring = False
        except Exception as e:
            print(f"\n❌ Monitoring error: {e}")
            self.monitoring = False
    
    def start_research_and_monitor(self):
        """Start background research and monitor in real-time"""
        
        print("🚀 Starting ASIS Background Research + Real-Time Monitor")
        print("=" * 60)
        
        try:
            # Start background research
            from asis_background_research_scheduler import ASISWithBackgroundResearch
            asis = ASISWithBackgroundResearch()
            
            print("🔥 Enabling continuous learning...")
            asis.enable_background_research()
            
            print("✅ Background research started!")
            print("🔍 Starting real-time monitoring...\n")
            
            # Start monitoring
            self.start_monitoring(refresh_interval=15)  # More frequent updates
            
        except Exception as e:
            print(f"❌ Error starting research and monitoring: {e}")
    
    def force_research_and_watch(self):
        """Force research sessions and watch them happen"""
        
        print("🔥 FORCING RESEARCH SESSIONS - WATCH ASIS LEARN!")
        print("=" * 55)
        
        try:
            from asis_autonomous_research_fixed import ASISAutonomousResearch
            research_system = ASISAutonomousResearch()
            
            # Get initial stats
            initial_stats = self.get_live_stats()
            print(f"📊 Starting with {initial_stats.get('total_findings', 0)} findings, {initial_stats.get('total_sessions', 0)} sessions")
            
            # Force several research sessions
            research_topics = [
                ("Latest AI Developments 2024", "artificial intelligence 2024 breakthrough GPT-4 Claude"),
                ("Quantum Computing Progress", "quantum computing IBM Google quantum supremacy qubits"),
                ("Renewable Energy Technology", "renewable energy solar wind battery storage green technology"),
                ("Space Exploration Updates", "SpaceX Mars mission NASA space telescope satellite technology"),
                ("Medical AI Applications", "artificial intelligence healthcare medical diagnosis AI medicine")
            ]
            
            for i, (topic, search_terms) in enumerate(research_topics, 1):
                print(f"\n🚀 [{i}/{len(research_topics)}] Starting research: '{topic}'")
                print("   Search terms:", search_terms)
                print("   ⏳ Researching...")
                
                # Start research
                result = research_system.force_research_session(topic, search_terms)
                
                # Show immediate results
                if result.get('status') == 'completed':
                    print(f"   ✅ Research completed!")
                    print(f"   📊 Findings: {result.get('findings_count', 0)}")
                    print(f"   🎯 Relevance: {result.get('average_relevance', 0):.2f}")
                else:
                    print(f"   ⚠️  Research status: {result.get('status', 'unknown')}")
                
                # Show updated stats
                current_stats = self.get_live_stats()
                new_findings = current_stats.get('total_findings', 0) - initial_stats.get('total_findings', 0)
                print(f"   📈 Total new findings so far: {new_findings}")
                
                time.sleep(2)  # Brief pause between research sessions
            
            # Final summary
            final_stats = self.get_live_stats()
            total_new_findings = final_stats.get('total_findings', 0) - initial_stats.get('total_findings', 0)
            total_new_sessions = final_stats.get('total_sessions', 0) - initial_stats.get('total_sessions', 0)
            
            print(f"\n🎉 RESEARCH SESSION COMPLETE!")
            print(f"📊 Results:")
            print(f"   • New findings discovered: {total_new_findings}")
            print(f"   • New research sessions: {total_new_sessions}")
            print(f"   • Total knowledge entries: {final_stats.get('total_findings', 0)}")
            
            # Show latest discoveries
            if final_stats.get('recent_findings'):
                print(f"\n🔍 Latest Discoveries:")
                for i, (title, content, score, timestamp) in enumerate(final_stats['recent_findings'][:3], 1):
                    print(f"   {i}. {title}")
                    print(f"      {content[:100]}...")
                    print(f"      Confidence: {score:.2f}")
            
        except Exception as e:
            print(f"❌ Error during forced research: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Main monitoring interface"""
    
    monitor = ASISRealTimeMonitor()
    
    print("🔍 ASIS REAL-TIME RESEARCH MONITOR")
    print("=" * 50)
    print("Choose monitoring option:")
    print("1. 🔄 Start continuous monitoring (watch background research)")
    print("2. 🚀 Start background research + monitor")
    print("3. 🔥 Force research sessions + watch live")
    print("4. 📊 Show current status only")
    
    try:
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            monitor.start_monitoring()
        elif choice == "2":
            monitor.start_research_and_monitor()
        elif choice == "3":
            monitor.force_research_and_watch()
        elif choice == "4":
            stats = monitor.get_live_stats()
            monitor.display_current_status(stats)
        else:
            print("Invalid choice. Starting continuous monitoring...")
            monitor.start_monitoring()
            
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
