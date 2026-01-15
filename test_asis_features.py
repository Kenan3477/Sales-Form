#!/usr/bin/env python3
"""
ASIS Feature Testing Suite
=========================
Comprehensive testing of all ASIS features to verify real functionality
"""

import os
import sys
import json
import sqlite3
from datetime import datetime
import traceback

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_real_learning_system():
    """Test the real learning system for actual functionality"""
    print("🔍 TESTING REAL LEARNING SYSTEM")
    print("=" * 50)
    
    try:
        from asis_real_learning_system import ASISRealLearningSystem
        
        # Initialize the system
        learning_system = ASISRealLearningSystem()
        
        # Check if database actually exists
        db_path = learning_system.learning_db
        print(f"Database path: {db_path}")
        print(f"Database exists: {os.path.exists(db_path)}")
        
        if not os.path.exists(db_path):
            print("❌ FAILED: Learning database does not exist")
            return False
        
        # Test 1: Check actual database content
        print("\n📊 TESTING DATABASE CONTENT:")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        table_names = [t[0] for t in tables]
        print(f"Tables found: {table_names}")
        
        if 'learning_sessions' not in table_names or 'knowledge_base' not in table_names:
            print("❌ FAILED: Required tables missing")
            conn.close()
            return False
        
        # Check learning sessions
        cursor.execute('SELECT COUNT(*) FROM learning_sessions')
        sessions_count = cursor.fetchone()[0]
        print(f"Learning sessions: {sessions_count}")
        
        # Check knowledge base
        cursor.execute('SELECT COUNT(*) FROM knowledge_base')
        knowledge_count = cursor.fetchone()[0]
        print(f"Knowledge entries: {knowledge_count}")
        
        # Show recent entries
        cursor.execute('SELECT * FROM knowledge_base ORDER BY added_timestamp DESC LIMIT 3')
        recent_entries = cursor.fetchall()
        print(f"Recent knowledge entries: {len(recent_entries)}")
        for entry in recent_entries:
            print(f"  - Topic: {entry[1]}")
            print(f"    Content: {entry[2][:100]}...")
        
        conn.close()
        
        # Test 2: Add new knowledge and verify it's stored
        print("\n🧠 TESTING ACTUAL LEARNING:")
        test_topic = f"test_learning_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        test_content = f"This is a test learning entry created at {datetime.now()}"
        
        # Record new learning
        learning_result = learning_system.record_learning_session(
            session_id=f"test_session_{datetime.now().strftime('%H%M%S')}",
            learning_data={
                'topic': test_topic,
                'content': test_content,
                'type': 'verification_test'
            }
        )
        
        print(f"Learning recorded: {learning_result}")
        
        # Verify it was actually stored
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM knowledge_base WHERE topic = ?', (test_topic,))
        stored_entry = cursor.fetchone()
        conn.close()
        
        if stored_entry:
            print("✅ VERIFICATION PASSED: New knowledge was actually stored in database")
            print(f"   Stored topic: {stored_entry[1]}")
            print(f"   Stored content: {stored_entry[2][:50]}...")
        else:
            print("❌ VERIFICATION FAILED: Knowledge was not stored")
            return False
        
        # Test 3: Check knowledge retrieval
        print("\n📚 TESTING KNOWLEDGE RETRIEVAL:")
        retrieved_knowledge = learning_system.get_relevant_knowledge(test_topic)
        print(f"Retrieved knowledge entries: {len(retrieved_knowledge)}")
        if retrieved_knowledge:
            print("✅ VERIFICATION PASSED: Knowledge retrieval working")
            for knowledge in retrieved_knowledge[:2]:
                print(f"   - {knowledge.get('topic', 'unknown')}: {knowledge.get('content', 'no content')[:30]}...")
        else:
            print("❌ VERIFICATION FAILED: Knowledge retrieval not working")
            return False
        
        print("\n✅ REAL LEARNING SYSTEM TEST PASSED")
        return True
        
    except Exception as e:
        print(f"❌ REAL LEARNING SYSTEM TEST FAILED: {e}")
        traceback.print_exc()
        return False

def test_adaptive_meta_learning():
    """Test adaptive meta-learning for real functionality"""
    print("\n🧠 TESTING ADAPTIVE META-LEARNING SYSTEM")
    print("=" * 50)
    
    try:
        from asis_adaptive_meta_learning import ASISAdaptiveMetaLearning
        
        # Initialize the system
        adaptive_system = ASISAdaptiveMetaLearning()
        
        # Check if database exists
        db_path = adaptive_system.adaptive_db
        print(f"Database path: {db_path}")
        print(f"Database exists: {os.path.exists(db_path)}")
        
        if not os.path.exists(db_path):
            print("❌ FAILED: Adaptive database does not exist")
            return False
        
        # Test 1: Check database structure
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"Tables found: {tables}")
        
        required_tables = ['user_interactions', 'adaptation_patterns', 'meta_learning_insights']
        missing_tables = [t for t in required_tables if t not in tables]
        if missing_tables:
            print(f"❌ FAILED: Missing required tables: {missing_tables}")
            conn.close()
            return False
        
        # Test 2: Record user interaction and check storage
        print("\n📊 TESTING USER INTERACTION RECORDING:")
        test_interaction = {
            'user_input': 'test interaction for verification',
            'response_style': 'detailed',
            'user_satisfaction': 4.5,
            'timestamp': datetime.now().isoformat()
        }
        
        # Record interaction
        result = adaptive_system.record_user_interaction(
            user_input=test_interaction['user_input'],
            response_generated='test response',
            user_feedback_rating=4.5,
            response_style='detailed'
        )
        
        print(f"Interaction recorded: {result}")
        
        # Verify storage
        cursor.execute('SELECT COUNT(*) FROM user_interactions')
        interaction_count = cursor.fetchone()[0]
        print(f"Total interactions in database: {interaction_count}")
        
        if interaction_count > 0:
            print("✅ VERIFICATION PASSED: User interactions being stored")
        else:
            print("❌ VERIFICATION FAILED: No interactions found")
            conn.close()
            return False
        
        # Test 3: Check pattern detection
        print("\n🎯 TESTING PATTERN DETECTION:")
        patterns = adaptive_system.detect_user_patterns()
        print(f"Patterns detected: {len(patterns)}")
        
        if patterns:
            print("✅ VERIFICATION PASSED: Pattern detection working")
            for pattern_type, pattern_data in patterns.items():
                print(f"   - {pattern_type}: {pattern_data}")
        else:
            print("⚠️ WARNING: No patterns detected (may be normal for new system)")
        
        # Test 4: Check adaptation effectiveness
        print("\n📈 TESTING ADAPTATION EFFECTIVENESS:")
        effectiveness_report = adaptive_system.get_adaptation_effectiveness_report()
        print(f"Report generated: {len(effectiveness_report) > 100}")
        
        if "Adaptation Effectiveness" in effectiveness_report:
            print("✅ VERIFICATION PASSED: Effectiveness reporting working")
        else:
            print("❌ VERIFICATION FAILED: Effectiveness reporting not working")
            conn.close()
            return False
        
        conn.close()
        print("\n✅ ADAPTIVE META-LEARNING SYSTEM TEST PASSED")
        return True
        
    except Exception as e:
        print(f"❌ ADAPTIVE META-LEARNING SYSTEM TEST FAILED: {e}")
        traceback.print_exc()
        return False

def test_evidence_display_system():
    """Test enhanced learning evidence display for real data"""
    print("\n📊 TESTING ENHANCED LEARNING EVIDENCE DISPLAY")
    print("=" * 50)
    
    try:
        from asis_enhanced_learning_display import ASISEnhancedLearningDisplay
        
        # Initialize the system
        evidence_system = ASISEnhancedLearningDisplay()
        
        # Test 1: Generate comprehensive report
        print("📋 TESTING COMPREHENSIVE REPORT GENERATION:")
        report = evidence_system.generate_comprehensive_learning_report()
        
        if len(report) < 100:
            print("❌ FAILED: Report too short, likely simulated")
            return False
        
        # Check for real data indicators
        real_data_indicators = [
            "Real-time Learning Metrics",
            "Learning Velocity:",
            "Adaptation Rate:",
            "Pattern Recognition:",
            "Database Verification:",
            datetime.now().strftime("%Y-%m-%d")
        ]
        
        missing_indicators = []
        for indicator in real_data_indicators:
            if indicator not in report:
                missing_indicators.append(indicator)
        
        if missing_indicators:
            print(f"❌ FAILED: Missing real data indicators: {missing_indicators}")
            return False
        
        print("✅ VERIFICATION PASSED: Report contains real data indicators")
        
        # Test 2: Check database connections
        print("\n🗄️ TESTING DATABASE CONNECTIONS:")
        databases_checked = evidence_system.get_database_verification()
        print(f"Databases verified: {len(databases_checked)}")
        
        if len(databases_checked) > 0:
            print("✅ VERIFICATION PASSED: Database verification working")
            for db_name, status in databases_checked.items():
                print(f"   - {db_name}: {status.get('status', 'unknown')}")
        else:
            print("❌ VERIFICATION FAILED: No databases verified")
            return False
        
        print("\n✅ EVIDENCE DISPLAY SYSTEM TEST PASSED")
        return True
        
    except Exception as e:
        print(f"❌ EVIDENCE DISPLAY SYSTEM TEST FAILED: {e}")
        traceback.print_exc()
        return False

def test_analytics_dashboard():
    """Test learning analytics dashboard for real metrics"""
    print("\n📈 TESTING LEARNING ANALYTICS DASHBOARD")
    print("=" * 50)
    
    try:
        from asis_learning_analytics_dashboard import ASISLearningAnalyticsDashboard
        
        # Initialize the system
        dashboard_system = ASISLearningAnalyticsDashboard()
        
        # Test 1: Generate dashboard display
        print("📊 TESTING DASHBOARD DISPLAY GENERATION:")
        dashboard = dashboard_system.generate_dashboard_display()
        
        if len(dashboard) < 200:
            print("❌ FAILED: Dashboard too short, likely simulated")
            return False
        
        # Check for real dashboard components
        dashboard_components = [
            "LEARNING ANALYTICS DASHBOARD",
            "KEY PERFORMANCE INDICATORS",
            "Learning Velocity",
            "Adaptation Rate",
            "Pattern Accuracy",
            "REAL-TIME MONITORING",
            "System Health"
        ]
        
        missing_components = []
        for component in dashboard_components:
            if component not in dashboard:
                missing_components.append(component)
        
        if missing_components:
            print(f"❌ FAILED: Missing dashboard components: {missing_components}")
            return False
        
        print("✅ VERIFICATION PASSED: Dashboard contains all required components")
        
        # Test 2: Check live metrics
        print("\n⚡ TESTING LIVE METRICS:")
        metrics = dashboard_system.get_live_metrics()
        print(f"Live metrics generated: {len(metrics)}")
        
        required_metrics = ['learning_velocity', 'adaptation_rate', 'pattern_accuracy']
        for metric in required_metrics:
            if metric in metrics:
                print(f"   ✅ {metric}: {metrics[metric]}")
            else:
                print(f"   ❌ Missing metric: {metric}")
                return False
        
        print("\n✅ ANALYTICS DASHBOARD TEST PASSED")
        return True
        
    except Exception as e:
        print(f"❌ ANALYTICS DASHBOARD TEST FAILED: {e}")
        traceback.print_exc()
        return False

def test_verification_system():
    """Test learning verification tools for real validation"""
    print("\n🔍 TESTING LEARNING VERIFICATION SYSTEM")
    print("=" * 50)
    
    try:
        from asis_learning_verification_tools import ASISLearningVerificationTools
        
        # Initialize the system
        verification_system = ASISLearningVerificationTools()
        
        # Test 1: Run comprehensive verification
        print("🔍 TESTING COMPREHENSIVE VERIFICATION:")
        verification_results = verification_system.comprehensive_learning_verification()
        
        if not isinstance(verification_results, dict):
            print("❌ FAILED: Verification results not in expected format")
            return False
        
        required_keys = ['overall_authenticity', 'individual_verifications', 'integrity_checks']
        for key in required_keys:
            if key not in verification_results:
                print(f"❌ FAILED: Missing verification key: {key}")
                return False
        
        print(f"✅ Overall authenticity score: {verification_results['overall_authenticity']:.1%}")
        
        # Test 2: Check individual verifications
        print("\n📋 TESTING INDIVIDUAL VERIFICATIONS:")
        individual_verifications = verification_results['individual_verifications']
        
        for verification_type, results in individual_verifications.items():
            score = results.get('authenticity_score', 0)
            status = "✅ PASS" if score > 0.5 else "⚠️ PARTIAL" if score > 0.3 else "❌ FAIL"
            print(f"   {verification_type}: {status} ({score:.1%})")
        
        # Test 3: Check integrity verification
        print("\n🔐 TESTING INTEGRITY VERIFICATION:")
        integrity_checks = verification_results['integrity_checks']
        overall_integrity = integrity_checks.get('overall_integrity', 0)
        
        print(f"   Overall integrity: {overall_integrity:.1%}")
        
        if overall_integrity > 0.8:
            print("✅ VERIFICATION PASSED: High integrity score")
        elif overall_integrity > 0.6:
            print("⚠️ VERIFICATION PARTIAL: Moderate integrity score")
        else:
            print("❌ VERIFICATION FAILED: Low integrity score")
            return False
        
        # Test 4: Generate verification report
        print("\n📄 TESTING VERIFICATION REPORT:")
        report = verification_system.generate_verification_report(verification_results)
        
        if len(report) > 500 and "VERIFICATION REPORT" in report:
            print("✅ VERIFICATION PASSED: Comprehensive report generated")
        else:
            print("❌ VERIFICATION FAILED: Report generation issue")
            return False
        
        print("\n✅ VERIFICATION SYSTEM TEST PASSED")
        return True
        
    except Exception as e:
        print(f"❌ VERIFICATION SYSTEM TEST FAILED: {e}")
        traceback.print_exc()
        return False

def test_autonomous_research():
    """Test autonomous research system for real functionality"""
    print("\n🔬 TESTING AUTONOMOUS RESEARCH SYSTEM")
    print("=" * 50)
    
    try:
        # Check if autonomous research database exists
        research_db = "asis_autonomous_research.db"
        print(f"Research database exists: {os.path.exists(research_db)}")
        
        if not os.path.exists(research_db):
            print("❌ FAILED: Autonomous research database not found")
            return False
        
        # Test database content
        conn = sqlite3.connect(research_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"Research tables: {tables}")
        
        if not tables:
            print("❌ FAILED: No research tables found")
            conn.close()
            return False
        
        # Check for research entries
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   {table}: {count} entries")
            except:
                continue
        
        conn.close()
        print("✅ AUTONOMOUS RESEARCH SYSTEM TEST PASSED")
        return True
        
    except Exception as e:
        print(f"❌ AUTONOMOUS RESEARCH SYSTEM TEST FAILED: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all feature tests"""
    print("🧪 ASIS COMPREHENSIVE FEATURE TESTING")
    print("=" * 60)
    print(f"Test Date: {datetime.now()}")
    print("=" * 60)
    
    tests = [
        ("Real Learning System", test_real_learning_system),
        ("Adaptive Meta-Learning", test_adaptive_meta_learning),
        ("Evidence Display System", test_evidence_display_system),
        ("Analytics Dashboard", test_analytics_dashboard), 
        ("Verification System", test_verification_system),
        ("Autonomous Research", test_autonomous_research)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} CRITICAL ERROR: {e}")
            results[test_name] = False
        print(f"{'='*60}")
    
    # Final summary
    print(f"\n🎯 FINAL TEST RESULTS")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - ASIS features are fully functional!")
    elif passed >= total * 0.8:
        print("⚠️ MOST TESTS PASSED - Minor issues detected")
    else:
        print("❌ MULTIPLE FAILURES - Significant issues detected")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
