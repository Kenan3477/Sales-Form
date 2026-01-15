#!/usr/bin/env python3
"""
ASIS Dashboard Control Interface
==============================

Command-line interface to control the ASIS Dashboard Enhancer
Allows activation, deactivation, and monitoring of the enhanced dashboard.

Usage:
    python asis_dashboard_control.py activate
    python asis_dashboard_control.py deactivate
    python asis_dashboard_control.py status
    python asis_dashboard_control.py restart

Author: ASIS Development Team
Version: 1.0
"""

import sys
import os
import time
import requests
import json
from datetime import datetime
from typing import Dict, Any

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from asis_dashboard_enhancer import ASISSystemMonitor, ASISDashboardEnhancer
    from asis_integration_system import ASISIntegrationSystem
except ImportError as e:
    print(f"⚠️ Warning: Could not import ASIS components: {e}")
    print("Make sure you're running this from the ASIS directory.")

class ASISDashboardController:
    """Controller for ASIS Dashboard Enhancement System"""
    
    def __init__(self):
        self.base_url = "http://localhost:5000"  # Default ASIS web interface URL
        self.dashboard_enhancer = None
        self.system_monitor = None
        self.integration_system = None
        
    def check_asis_server_status(self) -> Dict[str, Any]:
        """Check if ASIS server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/status", timeout=5)
            if response.status_code == 200:
                return {
                    "status": "running",
                    "server_available": True,
                    "response_time": response.elapsed.total_seconds()
                }
        except requests.exceptions.RequestException as e:
            return {
                "status": "not_running",
                "server_available": False,
                "error": str(e)
            }
        
        return {"status": "unknown", "server_available": False}
    
    def check_dashboard_enhancer_status(self) -> Dict[str, Any]:
        """Check dashboard enhancer status via API"""
        try:
            response = requests.get(f"{self.base_url}/api/v1/dashboard/data", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "active",
                    "enhanced_dashboard": True,
                    "system_health": data.get("current_metrics", {}).get("system_health", 0),
                    "monitoring_active": True
                }
        except requests.exceptions.RequestException:
            pass
        
        # Try alternative endpoints
        for endpoint in ["/api/v1/metrics", "/api/v1/components/enhanced"]:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=3)
                if response.status_code == 200:
                    return {
                        "status": "partially_active",
                        "enhanced_dashboard": True,
                        "monitoring_active": True
                    }
            except requests.exceptions.RequestException:
                continue
        
        return {
            "status": "inactive",
            "enhanced_dashboard": False,
            "monitoring_active": False
        }
    
    def activate_dashboard_enhancer(self) -> Dict[str, Any]:
        """Activate the dashboard enhancer"""
        print("🚀 Activating ASIS Dashboard Enhancer...")
        
        try:
            # Check if server is running
            server_status = self.check_asis_server_status()
            if not server_status["server_available"]:
                return {
                    "success": False,
                    "error": "ASIS server is not running. Please start the main ASIS system first.",
                    "suggestion": "Run: python app.py or python asis.py"
                }
            
            # Initialize system monitor
            self.system_monitor = ASISSystemMonitor()
            self.system_monitor.start_monitoring()
            
            print("✅ System monitor activated")
            print("📊 Real-time metrics collection started")
            
            # Test dashboard endpoints
            dashboard_status = self.check_dashboard_enhancer_status()
            
            result = {
                "success": True,
                "status": "activated",
                "timestamp": datetime.now().isoformat(),
                "system_monitor_active": self.system_monitor.monitoring_active,
                "dashboard_status": dashboard_status,
                "endpoints": [
                    f"{self.base_url}/api/v1/metrics",
                    f"{self.base_url}/api/v1/dashboard/data",
                    f"{self.base_url}/api/v1/components/enhanced"
                ]
            }
            
            print(f"🎯 Dashboard enhancer activated successfully!")
            print(f"📡 Monitoring endpoints available at: {self.base_url}/api/v1/*")
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to activate dashboard enhancer: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def deactivate_dashboard_enhancer(self) -> Dict[str, Any]:
        """Deactivate the dashboard enhancer"""
        print("🛑 Deactivating ASIS Dashboard Enhancer...")
        
        try:
            # Stop system monitor if active
            if self.system_monitor:
                self.system_monitor.stop_monitoring()
                print("📊 System monitoring stopped")
            
            # Clean up resources
            self.dashboard_enhancer = None
            self.system_monitor = None
            
            result = {
                "success": True,
                "status": "deactivated",
                "timestamp": datetime.now().isoformat(),
                "message": "Dashboard enhancer deactivated successfully"
            }
            
            print("✅ Dashboard enhancer deactivated")
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to deactivate dashboard enhancer: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_comprehensive_status(self) -> Dict[str, Any]:
        """Get comprehensive status of all systems"""
        server_status = self.check_asis_server_status()
        dashboard_status = self.check_dashboard_enhancer_status()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "asis_server": server_status,
            "dashboard_enhancer": dashboard_status,
            "system_monitor": {
                "active": self.system_monitor.monitoring_active if self.system_monitor else False,
                "metrics_available": len(self.system_monitor.metrics_history) if self.system_monitor else 0
            },
            "integration_status": {
                "components_loaded": ["ASISSystemMonitor", "ASISDashboardEnhancer"],
                "api_endpoints": [
                    "/api/v1/metrics",
                    "/api/v1/metrics/history",
                    "/api/v1/components/enhanced",
                    "/api/v1/performance",
                    "/api/v1/dashboard/data"
                ]
            }
        }
    
    def restart_dashboard_enhancer(self) -> Dict[str, Any]:
        """Restart the dashboard enhancer"""
        print("🔄 Restarting ASIS Dashboard Enhancer...")
        
        # Deactivate first
        deactivate_result = self.deactivate_dashboard_enhancer()
        if not deactivate_result["success"]:
            return deactivate_result
        
        # Wait a moment
        time.sleep(2)
        
        # Reactivate
        activate_result = self.activate_dashboard_enhancer()
        
        if activate_result["success"]:
            print("🎯 Dashboard enhancer restarted successfully!")
        
        return activate_result
    
    def test_dashboard_endpoints(self) -> Dict[str, Any]:
        """Test all dashboard API endpoints"""
        print("🧪 Testing Dashboard API Endpoints...")
        
        endpoints = [
            "/api/v1/metrics",
            "/api/v1/metrics/history?minutes=5",
            "/api/v1/components/enhanced",
            "/api/v1/performance", 
            "/api/v1/dashboard/data"
        ]
        
        results = {}
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                results[endpoint] = {
                    "status_code": response.status_code,
                    "response_time_ms": response.elapsed.total_seconds() * 1000,
                    "success": response.status_code == 200,
                    "data_size": len(response.content) if response.content else 0
                }
                
                if response.status_code == 200:
                    print(f"✅ {endpoint} - OK ({response.elapsed.total_seconds()*1000:.1f}ms)")
                else:
                    print(f"❌ {endpoint} - Error {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                results[endpoint] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"❌ {endpoint} - Connection Error: {e}")
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_endpoints": len(endpoints),
            "successful_endpoints": len([r for r in results.values() if r.get("success", False)]),
            "results": results
        }

def print_status_summary(status: Dict[str, Any]):
    """Print a formatted status summary"""
    print("\n" + "="*60)
    print("🎯 ASIS Dashboard Enhancement Status")
    print("="*60)
    
    # Server status
    server = status["asis_server"]
    server_emoji = "🟢" if server["server_available"] else "🔴"
    print(f"{server_emoji} ASIS Server: {server['status'].upper()}")
    
    # Dashboard status
    dashboard = status["dashboard_enhancer"]
    dashboard_emoji = "🟢" if dashboard["enhanced_dashboard"] else "🔴"
    print(f"{dashboard_emoji} Dashboard Enhancer: {dashboard['status'].upper()}")
    
    # System monitor
    monitor = status["system_monitor"]
    monitor_emoji = "🟢" if monitor["active"] else "🔴"
    print(f"{monitor_emoji} System Monitor: {'ACTIVE' if monitor['active'] else 'INACTIVE'}")
    
    if monitor["active"]:
        print(f"   📊 Metrics collected: {monitor['metrics_available']}")
    
    # API endpoints
    print(f"\n📡 Available API Endpoints:")
    for endpoint in status["integration_status"]["api_endpoints"]:
        print(f"   • http://localhost:5000{endpoint}")
    
    print("\n" + "="*60)

def main():
    """Main command-line interface"""
    if len(sys.argv) < 2:
        print("🎯 ASIS Dashboard Control Interface")
        print("=" * 40)
        print("Usage:")
        print("  python asis_dashboard_control.py activate    - Activate dashboard enhancer")
        print("  python asis_dashboard_control.py deactivate  - Deactivate dashboard enhancer")
        print("  python asis_dashboard_control.py status      - Show status")
        print("  python asis_dashboard_control.py restart     - Restart dashboard enhancer")
        print("  python asis_dashboard_control.py test        - Test API endpoints")
        print("\nExamples:")
        print("  python asis_dashboard_control.py status")
        print("  python asis_dashboard_control.py activate")
        return
    
    command = sys.argv[1].lower()
    controller = ASISDashboardController()
    
    if command == "activate":
        result = controller.activate_dashboard_enhancer()
        if result["success"]:
            print(f"\n✅ Success: {result.get('message', 'Dashboard enhancer activated')}")
        else:
            print(f"\n❌ Error: {result['error']}")
            if 'suggestion' in result:
                print(f"💡 Suggestion: {result['suggestion']}")
    
    elif command == "deactivate":
        result = controller.deactivate_dashboard_enhancer()
        if result["success"]:
            print(f"\n✅ Success: {result['message']}")
        else:
            print(f"\n❌ Error: {result['error']}")
    
    elif command == "status":
        status = controller.get_comprehensive_status()
        print_status_summary(status)
        
        # Show additional details in JSON format
        if len(sys.argv) > 2 and sys.argv[2] == "--json":
            print(f"\n📋 Detailed Status (JSON):")
            print(json.dumps(status, indent=2))
    
    elif command == "restart":
        result = controller.restart_dashboard_enhancer()
        if result["success"]:
            print(f"\n✅ Success: Dashboard enhancer restarted")
        else:
            print(f"\n❌ Error: {result['error']}")
    
    elif command == "test":
        results = controller.test_dashboard_endpoints()
        print(f"\n📊 Endpoint Test Results:")
        print(f"Success Rate: {results['successful_endpoints']}/{results['total_endpoints']}")
        
        if len(sys.argv) > 2 and sys.argv[2] == "--detailed":
            print(f"\n📋 Detailed Results:")
            print(json.dumps(results, indent=2))
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Use 'activate', 'deactivate', 'status', 'restart', or 'test'")

if __name__ == "__main__":
    main()