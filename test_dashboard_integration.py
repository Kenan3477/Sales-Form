#!/usr/bin/env python3
"""
Test Dashboard Integration
=========================
Test script to verify dashboard enhancer integration with ASIS
"""

import sys
import json
from datetime import datetime

def test_dashboard_integration():
    """Test dashboard integration components"""
    
    print("🧪 Testing ASIS Dashboard Integration")
    print("=" * 50)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'tests': [],
        'overall_status': 'unknown'
    }
    
    # Test 1: Import dashboard enhancer
    print("1. Testing dashboard enhancer import...")
    try:
        from asis_dashboard_enhancer import ASISDashboardEnhancer
        results['tests'].append({
            'name': 'Dashboard Enhancer Import',
            'status': 'pass',
            'message': 'Successfully imported ASISDashboardEnhancer'
        })
        print("   ✅ Dashboard enhancer imported successfully")
    except ImportError as e:
        results['tests'].append({
            'name': 'Dashboard Enhancer Import',
            'status': 'fail',
            'message': f'Import failed: {e}'
        })
        print(f"   ❌ Import failed: {e}")
    
    # Test 2: Import dashboard controller
    print("2. Testing dashboard controller import...")
    try:
        from dashboard_control import DashboardController
        results['tests'].append({
            'name': 'Dashboard Controller Import',
            'status': 'pass',
            'message': 'Successfully imported DashboardController'
        })
        print("   ✅ Dashboard controller imported successfully")
    except ImportError as e:
        results['tests'].append({
            'name': 'Dashboard Controller Import',
            'status': 'fail',
            'message': f'Import failed: {e}'
        })
        print(f"   ❌ Import failed: {e}")
    
    # Test 3: Check Flask template
    print("3. Testing dashboard control template...")
    try:
        import os
        template_path = 'templates/dashboard_control.html'
        if os.path.exists(template_path):
            results['tests'].append({
                'name': 'Dashboard Control Template',
                'status': 'pass',
                'message': 'Template file exists'
            })
            print("   ✅ Dashboard control template exists")
        else:
            results['tests'].append({
                'name': 'Dashboard Control Template',
                'status': 'fail',
                'message': 'Template file missing'
            })
            print("   ❌ Template file missing")
    except Exception as e:
        results['tests'].append({
            'name': 'Dashboard Control Template',
            'status': 'fail',
            'message': f'Template check failed: {e}'
        })
        print(f"   ❌ Template check failed: {e}")
    
    # Test 4: Check app.py integration
    print("4. Testing app.py integration...")
    try:
        # Try different encodings to handle potential encoding issues
        encodings = ['utf-8', 'utf-8-sig', 'cp1252', 'latin1']
        app_content = None
        
        for encoding in encodings:
            try:
                with open('app.py', 'r', encoding=encoding) as f:
                    app_content = f.read()
                break
            except UnicodeDecodeError:
                continue
        
        if app_content is None:
            results['tests'].append({
                'name': 'App.py Integration',
                'status': 'fail',
                'message': 'Could not read app.py with any encoding'
            })
            print("   ❌ Could not read app.py with any encoding")
        else:
            # Check for dashboard control imports and routes (more flexible)
            integration_indicators = [
                'dashboard_control' in app_content,
                'ASISDashboardEnhancer' in app_content,
                '/dashboard/control' in app_content,
                '/api/dashboard' in app_content
            ]
            
            found_indicators = sum(integration_indicators)
            
            if found_indicators >= 2:  # At least 2 indicators should be present
                results['tests'].append({
                    'name': 'App.py Integration',
                    'status': 'pass',
                    'message': f'Dashboard integration found in app.py ({found_indicators}/4 indicators)'
                })
                print(f"   ✅ App.py integration confirmed ({found_indicators}/4 indicators)")
            else:
                results['tests'].append({
                    'name': 'App.py Integration',
                    'status': 'fail',
                    'message': f'Insufficient integration indicators ({found_indicators}/4)'
                })
                print(f"   ❌ App.py integration insufficient ({found_indicators}/4 indicators)")
                
    except Exception as e:
        results['tests'].append({
            'name': 'App.py Integration',
            'status': 'fail',
            'message': f'App.py check failed: {e}'
        })
        print(f"   ❌ App.py check failed: {e}")
    
    # Test 5: Test controller instantiation
    print("5. Testing controller instantiation...")
    try:
        from dashboard_control import DashboardController
        controller = DashboardController()
        status = controller.get_status()
        
        results['tests'].append({
            'name': 'Controller Instantiation',
            'status': 'pass',
            'message': 'Controller created and status retrieved'
        })
        print("   ✅ Controller instantiation successful")
        print(f"   📊 Controller status: {json.dumps(status, indent=2)}")
        
    except Exception as e:
        results['tests'].append({
            'name': 'Controller Instantiation',
            'status': 'fail',
            'message': f'Controller instantiation failed: {e}'
        })
        print(f"   ❌ Controller instantiation failed: {e}")
    
    # Calculate overall status
    passed_tests = len([t for t in results['tests'] if t['status'] == 'pass'])
    total_tests = len(results['tests'])
    
    if passed_tests == total_tests:
        results['overall_status'] = 'all_pass'
        print(f"\n🎉 All tests passed! ({passed_tests}/{total_tests})")
    elif passed_tests > 0:
        results['overall_status'] = 'partial_pass'
        print(f"\n⚠️ Partial success: {passed_tests}/{total_tests} tests passed")
    else:
        results['overall_status'] = 'all_fail'
        print(f"\n❌ All tests failed: {passed_tests}/{total_tests}")
    
    # Integration summary
    print("\n🎛️ Dashboard Integration Summary:")
    print("=" * 50)
    
    if results['overall_status'] == 'all_pass':
        print("✅ Dashboard enhancer is fully integrated with ASIS!")
        print("🌐 Access the control interface at: http://localhost:5000/dashboard/control")
        print("🎯 Use the control interface to activate/deactivate enhanced dashboard")
        print("📊 Real-time monitoring will be available when activated")
        
        print("\n🚀 Quick Start Instructions:")
        print("1. Start ASIS: python app.py")
        print("2. Open browser: http://localhost:5000/dashboard/control")
        print("3. Click 'Activate Enhancement' to enable monitoring")
        print("4. Monitor system health and performance in real-time")
        
    elif results['overall_status'] == 'partial_pass':
        print("⚠️ Dashboard enhancer is partially integrated")
        print("🔧 Some components may need additional setup")
        
    else:
        print("❌ Dashboard enhancer integration incomplete")
        print("🛠️ Manual setup required")
    
    return results

if __name__ == "__main__":
    test_dashboard_integration()