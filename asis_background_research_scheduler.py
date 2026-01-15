#!/usr/bin/env python3
"""
ASIS Background Research Scheduler
Integrates with main ASIS system for continuous autonomous learning
"""

import threading
import time
import schedule
from datetime import datetime
import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class ASISBackgroundResearchScheduler:
    def __init__(self):
        self.scheduler_active = False
        self.scheduler_thread = None
        self.research_config = None
        self.research_system = None
        self.setup_logging()
        
    def setup_logging(self):
        """Set up logging for background research"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - ASIS Research - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('asis_background_research.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def initialize_systems(self):
        """Initialize research systems"""
        try:
            from asis_automated_research_config import ASISAutomatedResearchConfig
            from asis_autonomous_research_fixed import ASISAutonomousResearch
            
            self.research_config = ASISAutomatedResearchConfig()
            self.research_system = ASISAutonomousResearch()
            
            self.logger.info("✅ Background research systems initialized")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize research systems: {e}")
            return False
    
    def start_background_research(self):
        """Start continuous background research"""
        
        if not self.initialize_systems():
            return False
            
        if self.scheduler_active:
            self.logger.warning("⚠️  Background research scheduler already running")
            return False
        
        self.logger.info("🚀 Starting ASIS background research scheduler...")
        
        # Schedule research at different intervals
        schedule.every(30).minutes.do(self._quick_research_cycle)
        schedule.every(2).hours.do(self._regular_research_cycle)
        schedule.every().day.at("06:00").do(self._daily_research_cycle)
        schedule.every().day.at("18:00").do(self._evening_research_cycle)
        schedule.every().sunday.at("02:00").do(self._weekly_comprehensive_research)
        
        self.scheduler_active = True
        
        # Start scheduler thread
        def run_background_scheduler():
            self.logger.info("🔄 Background research scheduler thread started")
            while self.scheduler_active:
                try:
                    schedule.run_pending()
                    time.sleep(60)  # Check every minute
                except Exception as e:
                    self.logger.error(f"Scheduler error: {e}")
                    time.sleep(300)  # Wait 5 minutes on error
                    
            self.logger.info("🛑 Background research scheduler thread stopped")
        
        self.scheduler_thread = threading.Thread(target=run_background_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        self.logger.info("✅ ASIS background research scheduler started successfully!")
        return True
    
    def stop_background_research(self):
        """Stop background research scheduler"""
        
        if not self.scheduler_active:
            self.logger.warning("⚠️  Background research scheduler not running")
            return
            
        self.logger.info("🛑 Stopping background research scheduler...")
        self.scheduler_active = False
        schedule.clear()
        
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=10)
        
        self.logger.info("✅ Background research scheduler stopped")
    
    def _quick_research_cycle(self):
        """Quick research cycle - high priority topics only"""
        self.logger.info("⚡ Starting quick research cycle...")
        self._execute_research_cycle("quick", max_topics=1, min_priority=8)
    
    def _regular_research_cycle(self):
        """Regular research cycle - moderate topics"""
        self.logger.info("🔬 Starting regular research cycle...")
        self._execute_research_cycle("regular", max_topics=3, min_priority=6)
    
    def _daily_research_cycle(self):
        """Daily comprehensive research"""
        self.logger.info("📅 Starting daily research cycle...")
        self._execute_research_cycle("daily", max_topics=5, min_priority=4)
    
    def _evening_research_cycle(self):
        """Evening research cycle - catch up on missed topics"""
        self.logger.info("🌆 Starting evening research cycle...")
        self._execute_research_cycle("evening", max_topics=4, min_priority=5)
    
    def _weekly_comprehensive_research(self):
        """Weekly comprehensive research - all active topics"""
        self.logger.info("📈 Starting weekly comprehensive research...")
        self._execute_research_cycle("weekly", max_topics=15, min_priority=1)
    
    def _execute_research_cycle(self, cycle_type: str, max_topics: int, min_priority: int = 1):
        """Execute a research cycle with specified parameters"""
        
        if not self.research_config or not self.research_system:
            self.logger.error("❌ Research systems not initialized")
            return
            
        try:
            # Get available topics
            topics = self.research_config.get_active_topics(max_topics * 2)  # Get extra to filter
            
            # Filter by priority
            priority_topics = [t for t in topics if t['priority'] >= min_priority][:max_topics]
            
            if not priority_topics:
                self.logger.info(f"  ⚠️  No topics available for {cycle_type} cycle")
                return
            
            self.logger.info(f"  📚 Researching {len(priority_topics)} topics in {cycle_type} cycle")
            
            successful_sessions = 0
            total_findings = 0
            cycle_start_time = time.time()
            
            for i, topic in enumerate(priority_topics, 1):
                session_start_time = time.time()
                
                try:
                    self.logger.info(f"  [{i}/{len(priority_topics)}] Researching: {topic['topic']}")
                    
                    result = self.research_system.force_research_session(
                        topic['topic'],
                        topic['search_terms']
                    )
                    
                    session_time = time.time() - session_start_time
                    success = result.get('status') == 'completed'
                    findings_count = result.get('findings_count', 0)
                    relevance_score = result.get('average_relevance', 0.0)
                    
                    if success:
                        successful_sessions += 1
                        total_findings += findings_count
                        self.logger.info(f"    ✅ Success: {findings_count} findings (score: {relevance_score:.2f})")
                    else:
                        self.logger.warning(f"    ❌ Failed: {result.get('error', 'Unknown error')}")
                    
                    # Update performance tracking
                    self.research_config.update_research_performance(
                        topic['id'], success, findings_count,
                        relevance_score, session_time
                    )
                    
                    # Brief pause between research sessions
                    if i < len(priority_topics):
                        time.sleep(2)
                        
                except Exception as e:
                    session_time = time.time() - session_start_time
                    self.logger.error(f"    ❌ Research session error: {e}")
                    
                    self.research_config.update_research_performance(
                        topic['id'], False, 0, 0.0, session_time, str(e)
                    )
            
            cycle_duration = time.time() - cycle_start_time
            
            # Log cycle summary
            self.logger.info(f"  ✅ {cycle_type.title()} cycle completed:")
            self.logger.info(f"    • Duration: {cycle_duration:.1f} seconds")
            self.logger.info(f"    • Successful sessions: {successful_sessions}/{len(priority_topics)}")
            self.logger.info(f"    • Total findings: {total_findings}")
            self.logger.info(f"    • Success rate: {successful_sessions/len(priority_topics)*100:.1f}%")
            
        except Exception as e:
            self.logger.error(f"❌ Research cycle error ({cycle_type}): {e}")
    
    def get_scheduler_status(self) -> dict:
        """Get current scheduler status"""
        
        status = {
            'active': self.scheduler_active,
            'thread_alive': self.scheduler_thread.is_alive() if self.scheduler_thread else False,
            'systems_initialized': self.research_config is not None and self.research_system is not None
        }
        
        if self.research_config:
            stats = self.research_config.get_research_statistics()
            status['research_stats'] = stats
            
        return status
    
    def force_research_cycle(self, cycle_type: str = "manual"):
        """Force an immediate research cycle"""
        
        self.logger.info(f"🔥 Forcing {cycle_type} research cycle...")
        self._execute_research_cycle(cycle_type, max_topics=3, min_priority=5)

# Integration with main ASIS system
class ASISWithBackgroundResearch:
    """ASIS system with integrated background research"""
    
    def __init__(self):
        self.background_scheduler = ASISBackgroundResearchScheduler()
        self.research_enabled = False
    
    def enable_background_research(self):
        """Enable background research for continuous learning"""
        
        if self.research_enabled:
            print("⚠️  Background research already enabled")
            return
            
        success = self.background_scheduler.start_background_research()
        if success:
            self.research_enabled = True
            print("✅ ASIS background research enabled - continuous learning active!")
            print("   • Quick cycles: Every 30 minutes")
            print("   • Regular cycles: Every 2 hours")
            print("   • Daily cycles: 6:00 AM and 6:00 PM")
            print("   • Weekly comprehensive: Sunday 2:00 AM")
        else:
            print("❌ Failed to enable background research")
    
    def disable_background_research(self):
        """Disable background research"""
        
        if not self.research_enabled:
            print("⚠️  Background research not enabled")
            return
            
        self.background_scheduler.stop_background_research()
        self.research_enabled = False
        print("🛑 ASIS background research disabled")
    
    def get_learning_status(self):
        """Get current learning and research status"""
        
        status = self.background_scheduler.get_scheduler_status()
        
        print("📊 ASIS Learning Status:")
        print(f"  • Background Research: {'🟢 Active' if status['active'] else '🔴 Inactive'}")
        print(f"  • Scheduler Thread: {'🟢 Running' if status['thread_alive'] else '🔴 Stopped'}")
        print(f"  • Systems: {'🟢 Initialized' if status['systems_initialized'] else '🔴 Not Ready'}")
        
        if 'research_stats' in status:
            stats = status['research_stats']
            print(f"  • Active Topics: {stats['topics']['active']}")
            print(f"  • Total Sessions: {stats['topics']['total_sessions']}")
            print(f"  • Success Rate: {stats['topics']['avg_success_rate']:.1%}")
            print(f"  • Total Findings: {stats['performance']['total_findings']}")
        
        return status
    
    def force_learning_session(self):
        """Force an immediate learning session"""
        
        if not self.research_enabled:
            print("⚠️  Background research not enabled. Enabling temporarily...")
            self.background_scheduler.initialize_systems()
        
        self.background_scheduler.force_research_cycle("manual")

def main():
    """Demonstrate ASIS with background research"""
    
    print("🤖 ASIS with Background Research System")
    print("=" * 50)
    
    asis = ASISWithBackgroundResearch()
    
    # Show initial status
    asis.get_learning_status()
    
    print(f"\n🚀 To enable continuous learning:")
    print(f"   asis.enable_background_research()")
    print(f"\n📊 To check status:")
    print(f"   asis.get_learning_status()")
    print(f"\n🔥 To force immediate learning:")
    print(f"   asis.force_learning_session()")
    
    return asis

if __name__ == "__main__":
    main()
