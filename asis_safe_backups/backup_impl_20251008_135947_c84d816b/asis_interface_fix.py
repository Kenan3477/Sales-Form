#!/usr/bin/env python3
"""
ASIS INTERFACE FIX - REPLACES FAKE VERIFICATION WITH REAL DATA
==============================================================
This fixes the actual ASIS interface to show REAL verification results
"""

import sqlite3
import json
import os
from datetime import datetime

def get_real_verification_data():
    """Get real verification data from databases"""
    
    print("🔍 READING REAL ASIS DATABASE DATA")
    print("=" * 50)
    
    real_data = {
        'overall_authenticity': 0.0,
        'pattern_recognition': {'score': 0.0, 'details': ''},
        'learning_velocity': {'score': 0.0, 'details': ''},
        'adaptation_effectiveness': {'score': 0.0, 'details': ''},
        'knowledge_base': {'score': 0.0, 'details': ''},
        'meta_learning': {'score': 0.0, 'details': ''}
    }
    
    # 1. Check Pattern Recognition Database
    try:
        conn = sqlite3.connect('asis_patterns_fixed.db')
        cursor = conn.cursor()
        
        # Get pattern count and confidence
        cursor.execute('SELECT COUNT(*), AVG(confidence_score) FROM recognized_patterns WHERE confidence_score IS NOT NULL')
        result = cursor.fetchone()
        pattern_count = result[0] if result[0] else 0
        avg_confidence = result[1] if result[1] else 0.0
        
        # Get high confidence patterns
        cursor.execute('SELECT COUNT(*) FROM recognized_patterns WHERE confidence_score >= 0.85')
        high_confidence = cursor.fetchone()[0]
        
        conn.close()
        
        if pattern_count >= 50 and avg_confidence >= 0.85:
            real_data['pattern_recognition']['score'] = 100.0
            real_data['pattern_recognition']['details'] = f"✅ {pattern_count} patterns, {avg_confidence:.2f} confidence, {high_confidence} high-confidence"
        elif pattern_count >= 20:
            real_data['pattern_recognition']['score'] = 75.0
            real_data['pattern_recognition']['details'] = f"⚡ {pattern_count} patterns, {avg_confidence:.2f} confidence"
        elif pattern_count > 0:
            real_data['pattern_recognition']['score'] = 60.0
            real_data['pattern_recognition']['details'] = f"🟡 {pattern_count} patterns found"
        else:
            real_data['pattern_recognition']['score'] = 0.0
            real_data['pattern_recognition']['details'] = "❌ No patterns found"
        
        print(f"Pattern Recognition: {real_data['pattern_recognition']['details']}")
        
    except Exception as e:
        real_data['pattern_recognition']['score'] = 0.0
        real_data['pattern_recognition']['details'] = f"❌ Database error: {str(e)}"
        print(f"Pattern Recognition: {real_data['pattern_recognition']['details']}")
    
    # 2. Check Real-time Learning Database
    try:
        conn = sqlite3.connect('asis_realtime_learning.db')
        cursor = conn.cursor()
        
        # Count learning events
        cursor.execute('SELECT COUNT(*) FROM realtime_knowledge')
        knowledge_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM conversation_insights')
        insights_count = cursor.fetchone()[0]
        
        # Calculate velocity (simplified)
        cursor.execute('SELECT COUNT(*) FROM realtime_knowledge WHERE timestamp > datetime("now", "-24 hours")')
        recent_events = cursor.fetchone()[0]
        velocity = recent_events / 24.0 if recent_events > 0 else 0
        
        conn.close()
        
        total_events = knowledge_count + insights_count
        
        if total_events >= 200 and 0.5 <= velocity <= 10.0:
            real_data['learning_velocity']['score'] = 100.0
            real_data['learning_velocity']['details'] = f"✅ {total_events} events, {velocity:.1f}/hr velocity"
        elif total_events >= 50:
            real_data['learning_velocity']['score'] = 75.0
            real_data['learning_velocity']['details'] = f"⚡ {total_events} learning events"
        elif total_events > 0:
            real_data['learning_velocity']['score'] = 50.0
            real_data['learning_velocity']['details'] = f"🟡 {total_events} events found"
        else:
            real_data['learning_velocity']['score'] = 30.0
            real_data['learning_velocity']['details'] = "❌ Limited learning data"
        
        print(f"Learning Velocity: {real_data['learning_velocity']['details']}")
        
    except Exception as e:
        real_data['learning_velocity']['score'] = 30.0
        real_data['learning_velocity']['details'] = f"❌ Database error: {str(e)}"
        print(f"Learning Velocity: {real_data['learning_velocity']['details']}")
    
    # 3. Check Adaptive Meta-Learning Database
    try:
        conn = sqlite3.connect('asis_adaptive_meta_learning.db')
        cursor = conn.cursor()
        
        # Count different types of adaptations
        cursor.execute('SELECT COUNT(*) FROM strategy_performance')
        strategies = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM meta_learning_insights')
        insights = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM learning_optimizations')
        optimizations = cursor.fetchone()[0]
        
        conn.close()
        
        total_adaptations = strategies + insights + optimizations
        
        if total_adaptations >= 150:
            real_data['adaptation_effectiveness']['score'] = 100.0
            real_data['adaptation_effectiveness']['details'] = f"✅ {total_adaptations} adaptations ({strategies} strategies, {insights} insights)"
        elif total_adaptations >= 50:
            real_data['adaptation_effectiveness']['score'] = 75.0
            real_data['adaptation_effectiveness']['details'] = f"⚡ {total_adaptations} adaptations"
        elif total_adaptations > 0:
            real_data['adaptation_effectiveness']['score'] = 50.0
            real_data['adaptation_effectiveness']['details'] = f"🟡 {total_adaptations} adaptations"
        else:
            real_data['adaptation_effectiveness']['score'] = 0.0
            real_data['adaptation_effectiveness']['details'] = "❌ No adaptation data"
        
        print(f"Adaptation Effectiveness: {real_data['adaptation_effectiveness']['details']}")
        
    except Exception as e:
        real_data['adaptation_effectiveness']['score'] = 0.0
        real_data['adaptation_effectiveness']['details'] = f"❌ Database error: {str(e)}"
        print(f"Adaptation Effectiveness: {real_data['adaptation_effectiveness']['details']}")
    
    # 4. Check Research Database
    try:
        conn = sqlite3.connect('asis_autonomous_research_fixed.db')
        cursor = conn.cursor()
        
        # Count research data
        cursor.execute('SELECT COUNT(*) FROM research_sessions WHERE status = "active"')
        active_sessions = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM research_findings')
        findings = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM learning_insights WHERE verified = 1')
        verified_insights = cursor.fetchone()[0]
        
        conn.close()
        
        if active_sessions >= 5 and findings >= 20:
            real_data['knowledge_base']['score'] = 100.0
            real_data['knowledge_base']['details'] = f"✅ {active_sessions} sessions, {findings} findings, {verified_insights} insights"
        elif active_sessions >= 2 or findings >= 10:
            real_data['knowledge_base']['score'] = 75.0
            real_data['knowledge_base']['details'] = f"⚡ {active_sessions} sessions, {findings} findings"
        elif active_sessions > 0 or findings > 0:
            real_data['knowledge_base']['score'] = 50.0
            real_data['knowledge_base']['details'] = f"🟡 Some research activity"
        else:
            real_data['knowledge_base']['score'] = 0.0
            real_data['knowledge_base']['details'] = "❌ No research data"
        
        print(f"Knowledge Base: {real_data['knowledge_base']['details']}")
        
    except Exception as e:
        real_data['knowledge_base']['score'] = 0.0
        real_data['knowledge_base']['details'] = f"❌ Database error: {str(e)}"
        print(f"Knowledge Base: {real_data['knowledge_base']['details']}")
    
    # 5. Meta-learning verification (using same database)
    try:
        conn = sqlite3.connect('asis_adaptive_meta_learning.db')
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
            real_data['meta_learning']['score'] = 100.0
            real_data['meta_learning']['details'] = f"✅ {verified_insights} insights, {success_rate:.0f}% success rate"
        elif verified_insights >= 10:
            real_data['meta_learning']['score'] = 75.0
            real_data['meta_learning']['details'] = f"⚡ {verified_insights} insights"
        elif verified_insights > 0:
            real_data['meta_learning']['score'] = 50.0
            real_data['meta_learning']['details'] = f"🟡 {verified_insights} insights"
        else:
            real_data['meta_learning']['score'] = 0.0
            real_data['meta_learning']['details'] = "❌ No meta-learning data"
        
        print(f"Meta Learning: {real_data['meta_learning']['details']}")
        
    except Exception as e:
        real_data['meta_learning']['score'] = 0.0
        real_data['meta_learning']['details'] = f"❌ Database error: {str(e)}"
        print(f"Meta Learning: {real_data['meta_learning']['details']}")
    
    # Calculate overall authenticity
    scores = [
        real_data['pattern_recognition']['score'],
        real_data['learning_velocity']['score'],
        real_data['adaptation_effectiveness']['score'],
        real_data['knowledge_base']['score'],
        real_data['meta_learning']['score']
    ]
    
    real_data['overall_authenticity'] = sum(scores) / len(scores)
    
    print("=" * 50)
    print(f"🎯 REAL OVERALL AUTHENTICITY: {real_data['overall_authenticity']:.1f}%")
    
    if real_data['overall_authenticity'] >= 90:
        print("📊 AUTHENTICITY LEVEL: 🟢 HIGHLY AUTHENTIC")
    elif real_data['overall_authenticity'] >= 70:
        print("📊 AUTHENTICITY LEVEL: 🟡 MOSTLY AUTHENTIC")
    elif real_data['overall_authenticity'] >= 50:
        print("📊 AUTHENTICITY LEVEL: 🟡 PARTIALLY AUTHENTIC")
    else:
        print("📊 AUTHENTICITY LEVEL: 🔴 NEEDS IMPROVEMENT")
    
    return real_data

def create_fixed_interface_report():
    """Create a fixed interface report with real data"""
    
    real_data = get_real_verification_data()
    
    report = f"""
🔍 ASIS REAL VERIFICATION REPORT - FIXED INTERFACE
==================================================
🕒 Verification Timestamp: {datetime.now().isoformat()}
🎯 Overall Authenticity Score: {real_data['overall_authenticity']:.1f}%

📋 REAL DATABASE ANALYSIS RESULTS:
──────────────────────────────────

Pattern Recognition:
  Status: {real_data['pattern_recognition']['details']}
  Score: {real_data['pattern_recognition']['score']:.1f}%
  Method: Direct database query from asis_patterns_fixed.db

Learning Velocity:
  Status: {real_data['learning_velocity']['details']}
  Score: {real_data['learning_velocity']['score']:.1f}%
  Method: Real-time event analysis from asis_realtime_learning.db

Adaptation Effectiveness:
  Status: {real_data['adaptation_effectiveness']['details']}
  Score: {real_data['adaptation_effectiveness']['score']:.1f}%
  Method: Adaptation database analysis from asis_adaptive_meta_learning.db

Knowledge Base:
  Status: {real_data['knowledge_base']['details']}
  Score: {real_data['knowledge_base']['score']:.1f}%
  Method: Research database analysis from asis_autonomous_research_fixed.db

Meta Learning:
  Status: {real_data['meta_learning']['details']}
  Score: {real_data['meta_learning']['score']:.1f}%
  Method: Meta-learning database analysis

🔐 VERIFICATION SIGNATURE:
─────────────────────────
Verifier: ASIS Real Data Interface Fix v2.0.0
Fixed: Replaced fake verification with actual database reads
Timestamp: {datetime.now().isoformat()}

✅ This interface now reads REAL data from ASIS databases!
==================================================
"""
    
    return report

if __name__ == "__main__":
    print("🚀 FIXING ASIS INTERFACE TO SHOW REAL DATA...")
    print()
    
    report = create_fixed_interface_report()
    print(report)
    
    # Save the report
    with open("ASIS_REAL_VERIFICATION_FIXED.md", "w") as f:
        f.write(report)
    
    print("📄 Report saved to: ASIS_REAL_VERIFICATION_FIXED.md")
