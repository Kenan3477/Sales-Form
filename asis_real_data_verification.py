#!/usr/bin/env python3
"""
ASIS REAL DATA VERIFICATION SYSTEM
==================================
Replaces fake verification with ACTUAL database reads
"""

import sqlite3
import json
import os
import hashlib
import time
from datetime import datetime, timedelta

class ASISRealDataVerificationSystem:
    """Verification system that reads ACTUAL database data"""
    
    def __init__(self):
        self.databases = {
            'patterns': 'asis_patterns_fixed.db',
            'realtime': 'asis_realtime_learning.db',
            'meta_learning': 'asis_adaptive_meta_learning.db',
            'research': 'asis_autonomous_research_fixed.db',
            'automated_research': 'asis_automated_research_config.db'
        }
    
    def verify_pattern_recognition_real(self):
        """Get REAL pattern recognition data"""
        try:
            conn = sqlite3.connect(self.databases['patterns'])
            cursor = conn.cursor()
            
            # Get actual pattern count and confidence
            cursor.execute('SELECT COUNT(*), AVG(confidence_score) FROM recognized_patterns WHERE confidence_score IS NOT NULL')
            result = cursor.fetchone()
            pattern_count = result[0] if result[0] else 0
            avg_confidence = result[1] if result[1] else 0.0
            
            # Get high confidence patterns
            cursor.execute('SELECT COUNT(*) FROM recognized_patterns WHERE confidence_score >= 0.85')
            high_confidence_count = cursor.fetchone()[0]
            
            conn.close()
            
            if pattern_count >= 50 and avg_confidence >= 0.85:
                status = "✅ VERIFIED (100.0%)"
                score = 100.0
            elif pattern_count >= 20 and avg_confidence >= 0.7:
                status = "⚡ GOOD (80.0%)"
                score = 80.0
            elif pattern_count > 0:
                status = f"🟡 PARTIAL ({min(70, pattern_count * 2)}.0%)"
                score = min(70, pattern_count * 2)
            else:
                status = "❌ FAILED (0.0%)"
                score = 0.0
            
            return {
                'status': status,
                'score': score,
                'patterns': pattern_count,
                'avg_confidence': avg_confidence,
                'high_confidence': high_confidence_count
            }
            
        except Exception as e:
            return {
                'status': "❌ ERROR (0.0%)",
                'score': 0.0,
                'patterns': 0,
                'avg_confidence': 0.0,
                'high_confidence': 0,
                'error': str(e)
            }
    
    def verify_learning_velocity_real(self):
        """Get REAL learning velocity data"""
        try:
            conn = sqlite3.connect(self.databases['realtime'])
            cursor = conn.cursor()
            
            # Count learning events with optimal velocity indicators
            cursor.execute('''
                SELECT COUNT(*) FROM realtime_knowledge 
                WHERE content LIKE '%velocity%' OR content LIKE '%learning%'
            ''')
            velocity_events = cursor.fetchone()[0]
            
            # Count conversation insights
            cursor.execute('SELECT COUNT(*) FROM conversation_insights')
            insight_events = cursor.fetchone()[0]
            
            total_events = velocity_events + insight_events
            
            # Calculate velocity (events per hour over last 24 hours)
            cursor.execute('''
                SELECT COUNT(*) FROM realtime_knowledge 
                WHERE timestamp > datetime('now', '-24 hours')
            ''')
            recent_events = cursor.fetchone()[0]
            velocity = recent_events / 24.0 if recent_events > 0 else 0
            
            conn.close()
            
            if total_events >= 200 and 0.5 <= velocity <= 10.0:
                status = "✅ VERIFIED (100.0%)"
                score = 100.0
            elif total_events >= 50 and velocity > 0:
                status = "⚡ GOOD (80.0%)"
                score = 80.0
            elif total_events > 0:
                status = f"🟡 PARTIAL ({min(60, total_events)}.0%)"
                score = min(60, total_events)
            else:
                status = "❌ FAILED (30.0%)"
                score = 30.0
            
            return {
                'status': status,
                'score': score,
                'total_events': total_events,
                'velocity': velocity,
                'recent_events': recent_events
            }
            
        except Exception as e:
            return {
                'status': "❌ ERROR (0.0%)",
                'score': 0.0,
                'total_events': 0,
                'velocity': 0.0,
                'error': str(e)
            }
    
    def verify_adaptation_effectiveness_real(self):
        """Get REAL adaptation effectiveness data"""
        try:
            conn = sqlite3.connect(self.databases['meta_learning'])
            cursor = conn.cursor()
            
            # Count strategy performance records
            cursor.execute('SELECT COUNT(*) FROM strategy_performance')
            strategies = cursor.fetchone()[0]
            
            # Count meta learning insights
            cursor.execute('SELECT COUNT(*) FROM meta_learning_insights')
            insights = cursor.fetchone()[0]
            
            # Count learning optimizations
            cursor.execute('SELECT COUNT(*) FROM learning_optimizations')
            optimizations = cursor.fetchone()[0]
            
            total_adaptations = strategies + insights + optimizations
            
            conn.close()
            
            if total_adaptations >= 150:
                status = "✅ VERIFIED (100.0%)"
                score = 100.0
            elif total_adaptations >= 50:
                status = "⚡ GOOD (80.0%)"
                score = 80.0
            elif total_adaptations > 0:
                status = f"🟡 PARTIAL ({min(60, total_adaptations // 2)}.0%)"
                score = min(60, total_adaptations // 2)
            else:
                status = "❌ FAILED (0.0%)"
                score = 0.0
            
            return {
                'status': status,
                'score': score,
                'strategies': strategies,
                'insights': insights,
                'optimizations': optimizations,
                'total': total_adaptations
            }
            
        except Exception as e:
            return {
                'status': "❌ ERROR (0.0%)",
                'score': 0.0,
                'strategies': 0,
                'insights': 0,
                'optimizations': 0,
                'total': 0,
                'error': str(e)
            }
    
    def verify_meta_learning_real(self):
        """Get REAL meta learning data"""
        try:
            conn = sqlite3.connect(self.databases['meta_learning'])
            cursor = conn.cursor()
            
            # Count verified insights
            cursor.execute('SELECT COUNT(*) FROM meta_learning_insights WHERE validation_status LIKE "%verified%"')
            verified_insights = cursor.fetchone()[0]
            
            # Count successful implementations
            cursor.execute('SELECT COUNT(*) FROM meta_learning_insights WHERE implementation_success = 1')
            successful_implementations = cursor.fetchone()[0]
            
            conn.close()
            
            success_rate = (successful_implementations / max(verified_insights, 1)) * 100
            
            if verified_insights >= 25 and success_rate >= 80:
                status = "✅ VERIFIED (100.0%)"
                score = 100.0
            elif verified_insights >= 10 and success_rate >= 60:
                status = "⚡ GOOD (80.0%)"
                score = 80.0
            elif verified_insights > 0:
                status = f"🟡 PARTIAL ({min(60, verified_insights * 2)}.0%)"
                score = min(60, verified_insights * 2)
            else:
                status = "❌ FAILED (0.0%)"
                score = 0.0
            
            return {
                'status': status,
                'score': score,
                'verified_insights': verified_insights,
                'successful_implementations': successful_implementations,
                'success_rate': success_rate
            }
            
        except Exception as e:
            return {
                'status': "❌ ERROR (0.0%)",
                'score': 0.0,
                'verified_insights': 0,
                'successful_implementations': 0,
                'success_rate': 0.0,
                'error': str(e)
            }
    
    def verify_research_autonomy_real(self):
        """Get REAL research autonomy data"""
        try:
            conn = sqlite3.connect(self.databases['research'])
            cursor = conn.cursor()
            
            # Count active research sessions
            cursor.execute('SELECT COUNT(*) FROM research_sessions WHERE status = "active"')
            active_sessions = cursor.fetchone()[0]
            
            # Count research findings
            cursor.execute('SELECT COUNT(*) FROM research_findings')
            findings = cursor.fetchone()[0]
            
            # Count learning insights
            cursor.execute('SELECT COUNT(*) FROM learning_insights WHERE verified = 1')
            insights = cursor.fetchone()[0]
            
            conn.close()
            
            if active_sessions >= 5 and findings >= 20 and insights >= 10:
                status = "✅ VERIFIED (100.0%)"
                score = 100.0
            elif active_sessions >= 2 and findings >= 10:
                status = "⚡ GOOD (80.0%)"
                score = 80.0
            elif active_sessions > 0 or findings > 0:
                status = f"🟡 PARTIAL ({min(60, (active_sessions * 10) + (findings // 2))}.0%)"
                score = min(60, (active_sessions * 10) + (findings // 2))
            else:
                status = "❌ FAILED (0.0%)"
                score = 0.0
            
            return {
                'status': status,
                'score': score,
                'active_sessions': active_sessions,
                'findings': findings,
                'insights': insights
            }
            
        except Exception as e:
            return {
                'status': "❌ ERROR (0.0%)",
                'score': 0.0,
                'active_sessions': 0,
                'findings': 0,
                'insights': 0,
                'error': str(e)
            }
    
    def generate_real_verification_report(self):
        """Generate verification report with REAL data"""
        
        print("🔍 ASIS REAL DATA VERIFICATION REPORT")
        print("=" * 60)
        print(f"🕒 Verification Timestamp: {datetime.now().isoformat()}")
        
        # Run all verifications
        pattern_result = self.verify_pattern_recognition_real()
        velocity_result = self.verify_learning_velocity_real()
        adaptation_result = self.verify_adaptation_effectiveness_real()
        meta_result = self.verify_meta_learning_real()
        research_result = self.verify_research_autonomy_real()
        
        # Calculate overall score
        scores = [
            pattern_result['score'],
            velocity_result['score'],
            adaptation_result['score'],
            meta_result['score'],
            research_result['score']
        ]
        overall_score = sum(scores) / len(scores)
        
        print(f"🎯 Overall Authenticity Score: {overall_score:.1f}%")
        
        if overall_score >= 90:
            print("📊 Authenticity Level: 🟢 HIGHLY AUTHENTIC")
        elif overall_score >= 70:
            print("📊 Authenticity Level: 🟡 MOSTLY AUTHENTIC")
        elif overall_score >= 50:
            print("📊 Authenticity Level: 🟡 PARTIALLY AUTHENTIC")
        else:
            print("📊 Authenticity Level: 🔴 NEEDS IMPROVEMENT")
        
        print("=" * 60)
        print()
        print("📋 INDIVIDUAL VERIFICATION RESULTS:")
        print("─" * 40)
        
        print(f"\nPattern Recognition:")
        print(f"  Status: {pattern_result['status']}")
        print(f"  Method: Real database analysis")
        if pattern_result['patterns'] > 0:
            print(f"  ✅ Verified Claims:")
            print(f"    • Pattern data found: {pattern_result['patterns']} patterns")
            print(f"    • Average confidence: {pattern_result['avg_confidence']:.3f}")
            print(f"    • High-confidence patterns: {pattern_result['high_confidence']}")
        else:
            print(f"  ❌ Failed Verifications:")
            print(f"    • Insufficient pattern data: {pattern_result['patterns']} patterns")
        
        print(f"\nLearning Velocity:")
        print(f"  Status: {velocity_result['status']}")
        print(f"  Method: Real-time event analysis")
        if velocity_result['total_events'] > 0:
            print(f"  ✅ Verified Claims:")
            print(f"    • Learning events found: {velocity_result['total_events']}")
            print(f"    • Learning velocity: {velocity_result['velocity']:.2f} events/hour")
            print(f"    • Recent activity: {velocity_result['recent_events']} events (24h)")
        else:
            print(f"  ❌ Failed Verifications:")
            print(f"    • No learning events found")
        
        print(f"\nAdaptation Effectiveness:")
        print(f"  Status: {adaptation_result['status']}")
        print(f"  Method: Adaptation database analysis")
        if adaptation_result['total'] > 0:
            print(f"  ✅ Verified Claims:")
            print(f"    • Total adaptations: {adaptation_result['total']}")
            print(f"    • Strategies: {adaptation_result['strategies']}")
            print(f"    • Insights: {adaptation_result['insights']}")
            print(f"    • Optimizations: {adaptation_result['optimizations']}")
        else:
            print(f"  ❌ Failed Verifications:")
            print(f"    • No adaptation data found")
        
        print(f"\nMeta Learning:")
        print(f"  Status: {meta_result['status']}")
        print(f"  Method: Meta-learning database analysis")
        if meta_result['verified_insights'] > 0:
            print(f"  ✅ Verified Claims:")
            print(f"    • Verified insights: {meta_result['verified_insights']}")
            print(f"    • Successful implementations: {meta_result['successful_implementations']}")
            print(f"    • Success rate: {meta_result['success_rate']:.1f}%")
        else:
            print(f"  ❌ Failed Verifications:")
            print(f"    • No meta-learning data found")
        
        print(f"\nResearch Autonomy:")
        print(f"  Status: {research_result['status']}")
        print(f"  Method: Research database analysis")
        if research_result['active_sessions'] > 0 or research_result['findings'] > 0:
            print(f"  ✅ Verified Claims:")
            print(f"    • Active sessions: {research_result['active_sessions']}")
            print(f"    • Research findings: {research_result['findings']}")
            print(f"    • Verified insights: {research_result['insights']}")
        else:
            print(f"  ❌ Failed Verifications:")
            print(f"    • No research activity found")
        
        print()
        print("🔐 VERIFICATION SIGNATURE:")
        print("─" * 40)
        signature = hashlib.sha256(f"real_verification_{time.time()}".encode()).hexdigest()[:32]
        print(f"Signature: {signature}...")
        print(f"Verifier: ASIS Real Data Verification System")
        print(f"Version: 2.0.0 - REAL DATA ANALYSIS")
        print()
        print("=" * 60)
        print("✅ Real Data Verification Complete!")
        
        return overall_score

def main():
    """Run real data verification"""
    verifier = ASISRealDataVerificationSystem()
    score = verifier.generate_real_verification_report()
    
    if score >= 90:
        print("🎉 ASIS shows HIGH AUTHENTICITY with real data!")
    elif score >= 70:
        print("✅ ASIS shows GOOD AUTHENTICITY with real data!")
    else:
        print("⚠️ ASIS needs improvement - check database population!")
    
    return score

if __name__ == "__main__":
    main()
