"""
ASIS Customer Acquisition System Test
====================================
Quick test of all 5 customer acquisition systems
"""

import sys
import traceback
import os

def test_imports():
    """Test all required imports"""
    print("🧪 TESTING SYSTEM IMPORTS...")
    
    try:
        import pandas as pd
        print("   ✅ pandas imported successfully")
    except ImportError as e:
        print(f"   ❌ pandas import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("   ✅ numpy imported successfully")
    except ImportError as e:
        print(f"   ❌ numpy import failed: {e}")
        return False
    
    try:
        import aiohttp
        print("   ✅ aiohttp imported successfully")
    except ImportError as e:
        print(f"   ❌ aiohttp import failed: {e}")
        return False
    
    try:
        import requests
        print("   ✅ requests imported successfully")
    except ImportError as e:
        print(f"   ❌ requests import failed: {e}")
        return False
    
    return True

def test_customer_acquisition_engine():
    """Test customer acquisition engine"""
    print("\n🎯 TESTING CUSTOMER ACQUISITION ENGINE...")
    
    try:
        # Import the module
        sys.path.append(os.getcwd())
        from customer_acquisition_engine import AcademicOutreachEngine
        
        # Initialize engine
        engine = AcademicOutreachEngine()
        print("   ✅ AcademicOutreachEngine initialized")
        
        # Test database initialization
        engine.init_database()
        print("   ✅ Database initialized")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Customer acquisition engine test failed: {e}")
        traceback.print_exc()
        return False

def test_enterprise_pilot_system():
    """Test enterprise pilot system"""
    print("\n🏢 TESTING ENTERPRISE PILOT SYSTEM...")
    
    try:
        from enterprise_pilot_system import EnterpriseOutreachEngine
        
        engine = EnterpriseOutreachEngine()
        print("   ✅ EnterpriseOutreachEngine initialized")
        
        engine.init_database()
        print("   ✅ Enterprise database initialized")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Enterprise pilot system test failed: {e}")
        return False

def test_market_validation_engine():
    """Test market validation engine"""
    print("\n📊 TESTING MARKET VALIDATION ENGINE...")
    
    try:
        from market_validation_engine import ABTestingEngine
        
        engine = ABTestingEngine()
        print("   ✅ ABTestingEngine initialized")
        
        engine.init_database()
        print("   ✅ A/B testing database initialized")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Market validation engine test failed: {e}")
        return False

def test_revenue_acceleration_system():
    """Test revenue acceleration system"""
    print("\n💰 TESTING REVENUE ACCELERATION SYSTEM...")
    
    try:
        from revenue_acceleration_system import ReferralEngine
        
        engine = ReferralEngine()
        print("   ✅ ReferralEngine initialized")
        
        engine.init_database()
        print("   ✅ Referral database initialized")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Revenue acceleration system test failed: {e}")
        return False

def test_customer_success_platform():
    """Test customer success platform"""
    print("\n🎯 TESTING CUSTOMER SUCCESS PLATFORM...")
    
    try:
        from customer_success_platform import OnboardingEngine
        
        engine = OnboardingEngine()
        print("   ✅ OnboardingEngine initialized")
        
        engine.init_database()
        print("   ✅ Onboarding database initialized")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Customer success platform test failed: {e}")
        return False

def main():
    """Run all system tests"""
    print("🔬 ASIS CUSTOMER ACQUISITION SYSTEM TESTS")
    print("="*50)
    
    tests = [
        ("Import Dependencies", test_imports),
        ("Customer Acquisition Engine", test_customer_acquisition_engine),
        ("Enterprise Pilot System", test_enterprise_pilot_system),
        ("Market Validation Engine", test_market_validation_engine),
        ("Revenue Acceleration System", test_revenue_acceleration_system),
        ("Customer Success Platform", test_customer_success_platform),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"   ❌ {test_name} test crashed: {e}")
    
    print("\n📈 TEST RESULTS:")
    print(f"   Passed: {passed}/{total}")
    print(f"   Success Rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL SYSTEMS OPERATIONAL!")
        print("Ready to launch customer acquisition campaign!")
    else:
        print(f"\n⚠️  {total-passed} systems need attention")
        print("Check error messages above for details")

if __name__ == "__main__":
    main()
