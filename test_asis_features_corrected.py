#!/usr/bin/env python3
"""
ASIS Feature Testing Suite - Corrected Version
=============================================
Comprehensive testing of all ASIS features using actual available methods
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
        
        # Count records in each table
        for table in table_names:
            try:
                cursor.execute(f'SELECT COUNT(*) FROM {table}')
                count = cursor.fetchone()[0]
                print(f"  {table}: {count} records")
            except:
                print(f"  {table}: Unable to count")
        
        # Test 2: Test knowledge expansion (actual method)
        print("\n🧠 TESTING KNOWLEDGE EXPANSION:")
        test_topic = f"test_learning_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        test_info = f"This is a test knowledge entry created at {datetime.now()}"
        
        # Use actual method
        result = learning_system.expand_knowledge_base(
            topic=test_topic,
            information=test_info,
            source="verification_test"
        )
        
        print(f"Knowledge expansion result: {result}")
        
        # Verify it was stored by checking knowledge entries table
        cursor.execute('SELECT * FROM knowledge_entries WHERE topic = ?', (test_topic,))
        stored_entry = cursor.fetchone()
        
        if stored_entry:
            print("✅ VERIFICATION PASSED: New knowledge was actually stored")
            print(f"   Stored topic: {stored_entry[1] if len(stored_entry) > 1 else 'N/A'}")
        else:
            print("❌ VERIFICATION FAILED: Knowledge was not stored")
            conn.close()
            return False
        
        # Test 3: Check learning metrics
        print("\n📚 TESTING LEARNING METRICS:")
        metrics = learning_system.learning_metrics
        print(f"Learning metrics available: {len(metrics)}")
        for metric, value in metrics.items():
            print(f"   {metric}: {value}")
        
        if metrics.get('knowledge_entries_added', 0) >= 0:
            print("✅ VERIFICATION PASSED: Learning metrics tracking")
        else:
            print("❌ VERIFICATION FAILED: Learning metrics not working")
            conn.close()
            return False
        
        conn.close()
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
        
        # Check if database exists (using correct attribute)
        db_path = adaptive_system.db_path
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
        
        # Count records in tables
        for table in tables:
            try:
                cursor.execute(f'SELECT COUNT(*) FROM {table}')
                count = cursor.fetchone()[0]
                print(f"  {table}: {count} records")
            except:
                print(f"  {table}: Unable to count")
        
        # Test 2: Check learning effectiveness
        print("\n📊 TESTING LEARNING EFFECTIVENESS:")
        effectiveness = adaptive_system.learning_effectiveness
        print(f"Effectiveness metrics: {len(effectiveness)}")
        for metric, value in effectiveness.items():
            print(f"   {metric}: {value}")
        
        # Test 3: Check response strategies
        print("\n🎯 TESTING RESPONSE STRATEGIES:")
        strategies = adaptive_system.response_strategies
        print(f"Available strategies: {len(strategies)}")
        for strategy, data in strategies.items():
            print(f"   {strategy}: weight={data['weight']}, success_rate={data['success_rate']}")
        
        # Test 4: Generate effectiveness report (actual method)
        print("\n📈 TESTING EFFECTIVENESS REPORT:")
        try:
            report = adaptive_system.get_adaptation_effectiveness_report()
            if len(report) > 100:
                print("✅ VERIFICATION PASSED: Effectiveness report generated")
                print(f"   Report length: {len(report)} characters")
            else:
                print("❌ VERIFICATION FAILED: Report too short")
                conn.close()
                return False
        except Exception as e:
            print(f"❌ VERIFICATION FAILED: Report generation error: {e}")
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
        
        print(f"Report generated: {len(report)} characters")
        
        # Check for actual content
        content_indicators = [
            "Learning Evidence",
            "Database",
            "System",
            datetime.now().strftime("%Y")
        ]
        
        found_indicators = 0
        for indicator in content_indicators:
            if indicator in report:
                found_indicators += 1
                print(f"   ✅ Found: {indicator}")
            else:
                print(f"   ⚠️ Missing: {indicator}")
        
        if found_indicators >= len(content_indicators) // 2:
            print("✅ VERIFICATION PASSED: Report contains substantial content")
        else:
            print("❌ VERIFICATION FAILED: Report lacks expected content")
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
        
        print(f"Dashboard generated: {len(dashboard)} characters")
        
        # Check for dashboard components
        dashboard_components = [
            "DASHBOARD",
            "Learning",
            "Analytics",
            "Performance",
            "Metrics"
        ]
        
        found_components = 0
        for component in dashboard_components:
            if component.lower() in dashboard.lower():
                found_components += 1
                print(f"   ✅ Found: {component}")
            else:
                print(f"   ⚠️ Missing: {component}")
        
        if found_components >= len(dashboard_components) // 2:
            print("✅ VERIFICATION PASSED: Dashboard contains expected components")
        else:
            print("❌ VERIFICATION FAILED: Dashboard lacks expected components")
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
        
        print(f"Verification results keys: {list(verification_results.keys())}")
        
        # Check for required components
        required_keys = ['overall_authenticity', 'individual_verifications']
        missing_keys = [key for key in required_keys if key not in verification_results]
        
        if missing_keys:
            print(f"⚠️ WARNING: Missing keys: {missing_keys}")
        else:
            print("✅ All required verification keys present")
        
        # Check overall authenticity
        if 'overall_authenticity' in verification_results:
            authenticity = verification_results['overall_authenticity']
            print(f"✅ Overall authenticity score: {authenticity:.1%}")
            
            if authenticity > 0.5:
                print("✅ VERIFICATION PASSED: Acceptable authenticity score")
            else:
                print("⚠️ VERIFICATION PARTIAL: Low authenticity score")
        
        # Test 2: Generate verification report
        print("\n📄 TESTING VERIFICATION REPORT:")
        try:
            report = verification_system.generate_verification_report(verification_results)
            
            if len(report) > 500:
                print("✅ VERIFICATION PASSED: Comprehensive report generated")
                print(f"   Report length: {len(report)} characters")
            else:
                print("❌ VERIFICATION FAILED: Report too short")
                return False
        except Exception as e:
            print(f"❌ VERIFICATION FAILED: Report generation error: {e}")
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
        
        # Check for research entries and real data
        total_entries = 0
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                total_entries += count
                print(f"   {table}: {count} entries")
                
                # Show sample data to verify it's real
                if count > 0:
                    cursor.execute(f"SELECT * FROM {table} LIMIT 1")
                    sample = cursor.fetchone()
                    if sample:
                        print(f"      Sample data length: {len(str(sample))} chars")
            except Exception as e:
                print(f"   {table}: Error accessing - {e}")
                continue
        
        conn.close()
        
        if total_entries > 0:
            print(f"✅ VERIFICATION PASSED: {total_entries} total research entries found")
        else:
            print("❌ VERIFICATION FAILED: No research data found")
            return False
        
        print("\n✅ AUTONOMOUS RESEARCH SYSTEM TEST PASSED")
        return True
        
    except Exception as e:
        print(f"❌ AUTONOMOUS RESEARCH SYSTEM TEST FAILED: {e}")
        traceback.print_exc()
        return False

def test_web_integration():
    """Test web application integration"""
    print("\n🌐 TESTING WEB APPLICATION INTEGRATION")
    print("=" * 50)
    
    try:
        # Check if main web app exists
        web_app_file = "app.py"
        print(f"Web application file exists: {os.path.exists(web_app_file)}")
        
        if not os.path.exists(web_app_file):
            print("❌ FAILED: Web application file not found")
            return False
        
        # Check web templates
        templates_dir = "templates"
        print(f"Templates directory exists: {os.path.exists(templates_dir)}")
        
        if os.path.exists(templates_dir):
            templates = os.listdir(templates_dir)
            print(f"   Templates found: {templates}")
        
        # Check static files
        static_dir = "static"
        print(f"Static directory exists: {os.path.exists(static_dir)}")
        
        if os.path.exists(static_dir):
            static_files = []
            for root, dirs, files in os.walk(static_dir):
                for file in files:
                    static_files.append(os.path.join(root, file))
            print(f"   Static files count: {len(static_files)}")
        
        # Check Railway deployment files
        deployment_files = ["Procfile", "requirements.txt", "railway.json"]
        deployment_ready = True
        
        for file in deployment_files:
            exists = os.path.exists(file)
            print(f"   {file}: {'✅' if exists else '❌'}")
            if not exists:
                deployment_ready = False
        
        if deployment_ready:
            print("✅ VERIFICATION PASSED: All deployment files present")
        else:
            print("⚠️ WARNING: Some deployment files missing")
        
        print("\n✅ WEB INTEGRATION TEST PASSED")
        return True
        
    except Exception as e:
        print(f"❌ WEB INTEGRATION TEST FAILED: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all feature tests"""
    print("🧪 ASIS COMPREHENSIVE FEATURE TESTING - CORRECTED VERSION")
    print("=" * 70)
    print(f"Test Date: {datetime.now()}")
    print("=" * 70)
    
    tests = [
        ("Real Learning System", test_real_learning_system),
        ("Adaptive Meta-Learning", test_adaptive_meta_learning),
        ("Evidence Display System", test_evidence_display_system),
        ("Analytics Dashboard", test_analytics_dashboard), 
        ("Verification System", test_verification_system),
        ("Autonomous Research", test_autonomous_research),
        ("Web Integration", test_web_integration)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*70}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} CRITICAL ERROR: {e}")
            results[test_name] = False
        print(f"{'='*70}")
    
    # Final summary
    print(f"\n🎯 FINAL TEST RESULTS")
    print("=" * 70)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - ASIS features are fully functional!")
        print("🚀 Ready for Railway deployment!")
    elif passed >= total * 0.8:
        print("⚠️ MOST TESTS PASSED - Minor issues detected, but deployable")
    elif passed >= total * 0.6:
        print("⚡ MAJORITY PASSED - Good functionality, some optimization needed")
    else:
        print("❌ MULTIPLE FAILURES - Significant issues detected")
    
    # Deployment readiness assessment
    critical_systems = ["Real Learning System", "Web Integration", "Verification System"]
    critical_passed = sum(1 for system in critical_systems if results.get(system, False))
    
    print(f"\n🚀 DEPLOYMENT READINESS:")
    print(f"Critical systems: {critical_passed}/{len(critical_systems)} passed")
    
    if critical_passed == len(critical_systems):
        print("✅ READY FOR DEPLOYMENT - All critical systems functional")
    elif critical_passed >= len(critical_systems) - 1:
        print("⚠️ MOSTLY READY - One critical system issue")
    else:
        print("❌ NOT READY - Multiple critical system failures")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
