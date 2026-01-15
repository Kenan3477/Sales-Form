"""
Simple System Validation - Windows Compatible
============================================
"""

def test_imports():
    print("Testing core dependencies...")
    try:
        import pandas as pd
        print("  pandas: OK")
    except Exception as e:
        print(f"  pandas: FAILED - {e}")
        return False
    
    try:
        import numpy as np
        print("  numpy: OK")
    except Exception as e:
        print(f"  numpy: FAILED - {e}")
        return False
    
    try:
        import aiohttp
        print("  aiohttp: OK")
    except Exception as e:
        print(f"  aiohttp: FAILED - {e}")
        return False
    
    try:
        import requests
        print("  requests: OK")
    except Exception as e:
        print(f"  requests: FAILED - {e}")
        return False
    
    return True

def test_customer_acquisition():
    print("\nTesting Customer Acquisition Engine...")
    try:
        from customer_acquisition_engine import AcademicOutreachEngine
        engine = AcademicOutreachEngine()
        engine.init_database()
        print("  Academic Beta Launch: OK")
        return True
    except Exception as e:
        print(f"  Academic Beta Launch: FAILED - {e}")
        return False

def test_enterprise_system():
    print("\nTesting Enterprise Pilot System...")
    try:
        from enterprise_pilot_system import EnterpriseOutreachEngine
        engine = EnterpriseOutreachEngine()
        engine.init_database()
        print("  Enterprise Pilots: OK")
        return True
    except Exception as e:
        print(f"  Enterprise Pilots: FAILED - {e}")
        return False

def test_market_validation():
    print("\nTesting Market Validation Engine...")
    try:
        from market_validation_engine import ABTestingEngine
        engine = ABTestingEngine()
        engine.init_database()
        print("  Market Validation: OK")
        return True
    except Exception as e:
        print(f"  Market Validation: FAILED - {e}")
        return False

def test_revenue_acceleration():
    print("\nTesting Revenue Acceleration System...")
    try:
        from revenue_acceleration_system import ReferralEngine
        engine = ReferralEngine()
        engine.init_database()
        print("  Revenue Acceleration: OK")
        return True
    except Exception as e:
        print(f"  Revenue Acceleration: FAILED - {e}")
        return False

def test_customer_success():
    print("\nTesting Customer Success Platform...")
    try:
        from customer_success_platform import OnboardingEngine
        engine = OnboardingEngine()
        engine.init_database()
        print("  Customer Success: OK")
        return True
    except Exception as e:
        print(f"  Customer Success: FAILED - {e}")
        return False

def main():
    print("ASIS Customer Acquisition System Validation")
    print("=" * 50)
    
    tests = [
        ("Dependencies", test_imports),
        ("Customer Acquisition", test_customer_acquisition),
        ("Enterprise System", test_enterprise_system),
        ("Market Validation", test_market_validation),
        ("Revenue Acceleration", test_revenue_acceleration),
        ("Customer Success", test_customer_success),
    ]
    
    passed = 0
    for test_name, test_func in tests:
        if test_func():
            passed += 1
    
    print(f"\nResults: {passed}/{len(tests)} systems operational")
    
    if passed == len(tests):
        print("\nALL SYSTEMS READY FOR LAUNCH!")
        print("\nRevenue Targets:")
        print("  Month 1: $25,000+ MRR")
        print("  Customers: 100+ active users")
        print("  Academic trials: 50+ universities")
        print("  Enterprise pilots: 10+ Fortune 500")
        print("\nNext: Execute campaign phases")
    else:
        print(f"\n{len(tests) - passed} systems need fixes")

if __name__ == "__main__":
    main()
