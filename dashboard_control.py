#!/usr/bin/env python3
"""
ASIS Dashboard Control Interface
===============================
Control interface for activating/deactivating the enhanced dashboard
and managing system monitoring components.
"""

import sys
import json
import time
import subprocess
from datetime import datetime
from typing import Dict, Any, Optional

class DashboardController:
    """Control interface for ASIS dashboard enhancement"""
    
    def __init__(self):
        self.dashboard_enhancer = None
        self.monitoring_active = False
        self.integration_status = {
            'dashboard_enhanced': False,
            'monitoring_active': False,
            'api_endpoints_active': False,
            'last_update': datetime.now().isoformat()
        }
        print("🎛️ Dashboard Controller initialized")
    
    def activate_dashboard_enhancement(self) -> Dict[str, Any]:
        """Activate the enhanced dashboard with real-time monitoring"""
        try:
            print("🚀 Activating Dashboard Enhancement...")
            
            # Import and initialize dashboard enhancer
            from asis_dashboard_enhancer import ASISDashboardEnhancer
            
            # Check if we have a web API instance
            web_api = self._get_web_api_instance()
            if not web_api:
                return {
                    'success': False,
                    'error': 'Web API instance not found. Start ASIS web interface first.',
                    'status': 'failed'
                }
            
            # Initialize dashboard enhancer
            self.dashboard_enhancer = ASISDashboardEnhancer(web_api)
            self.monitoring_active = True
            
            # Update integration status
            self.integration_status.update({
                'dashboard_enhanced': True,
                'monitoring_active': True,
                'api_endpoints_active': True,
                'last_update': datetime.now().isoformat()
            })
            
            print("✅ Dashboard Enhancement activated successfully!")
            print("📊 Real-time monitoring started")
            print("🌐 Enhanced API endpoints active")
            
            return {
                'success': True,
                'message': 'Dashboard enhancement activated successfully',
                'status': 'active',
                'monitoring_active': self.monitoring_active,
                'api_endpoints': self._get_active_endpoints()
            }
            
        except ImportError as e:
            error_msg = f"Failed to import dashboard enhancer: {e}"
            print(f"❌ {error_msg}")
            return {'success': False, 'error': error_msg, 'status': 'import_error'}
            
        except Exception as e:
            error_msg = f"Failed to activate dashboard enhancement: {e}"
            print(f"❌ {error_msg}")
            return {'success': False, 'error': error_msg, 'status': 'activation_error'}
    
    def deactivate_dashboard_enhancement(self) -> Dict[str, Any]:
        """Deactivate the enhanced dashboard and stop monitoring"""
        try:
            print("🛑 Deactivating Dashboard Enhancement...")
            
            if self.dashboard_enhancer:
                # Stop monitoring
                self.dashboard_enhancer.system_monitor.stop_monitoring()
                self.dashboard_enhancer = None
                
            self.monitoring_active = False
            
            # Update integration status
            self.integration_status.update({
                'dashboard_enhanced': False,
                'monitoring_active': False,
                'api_endpoints_active': False,
                'last_update': datetime.now().isoformat()
            })
            
            print("✅ Dashboard Enhancement deactivated")
            print("📊 Real-time monitoring stopped")
            
            return {
                'success': True,
                'message': 'Dashboard enhancement deactivated successfully',
                'status': 'inactive',
                'monitoring_active': self.monitoring_active
            }
            
        except Exception as e:
            error_msg = f"Failed to deactivate dashboard enhancement: {e}"
            print(f"❌ {error_msg}")
            return {'success': False, 'error': error_msg, 'status': 'deactivation_error'}
    
    def get_status(self) -> Dict[str, Any]:
        """Get current dashboard enhancement status"""
        status = {
            **self.integration_status,
            'controller_active': True,
            'dashboard_enhancer_available': self.dashboard_enhancer is not None,
            'current_time': datetime.now().isoformat()
        }
        
        if self.dashboard_enhancer:
            enhancement_data = self.dashboard_enhancer.get_dashboard_enhancement_data()
            status.update({
                'system_metrics': enhancement_data.get('system_monitor', {}),
                'component_health': enhancement_data.get('component_health', {}),
                'metrics_available': enhancement_data.get('metrics_available', 0),
                'monitoring_active': enhancement_data.get('monitoring_active', False)
            })
        
        return status
    
    def restart_monitoring(self) -> Dict[str, Any]:
        """Restart monitoring system"""
        try:
            if self.dashboard_enhancer:
                self.dashboard_enhancer.system_monitor.stop_monitoring()
                time.sleep(1)
                self.dashboard_enhancer.system_monitor.start_monitoring()
                
                return {
                    'success': True,
                    'message': 'Monitoring system restarted successfully',
                    'monitoring_active': True
                }
            else:
                return {
                    'success': False,
                    'error': 'Dashboard enhancer not active',
                    'monitoring_active': False
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to restart monitoring: {e}",
                'monitoring_active': False
            }
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get current system health information"""
        if not self.dashboard_enhancer:
            return {
                'status': 'dashboard_inactive',
                'health_score': 0,
                'message': 'Dashboard enhancement not active'
            }
        
        try:
            current_metrics = self.dashboard_enhancer.system_monitor.get_current_metrics()
            performance_summary = self.dashboard_enhancer.system_monitor.get_performance_summary()
            
            return {
                'status': 'active',
                'health_score': current_metrics.get('system_health', 0),
                'current_metrics': current_metrics,
                'performance_summary': performance_summary,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'health_score': 0,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _get_web_api_instance(self):
        """Try to get the web API instance from the running ASIS application"""
        try:
            # Try to import from the main app
            import app
            if hasattr(app, 'web_api') and app.web_api:
                return app.web_api
            
            # Try to find in globals
            if 'web_api' in globals():
                return globals()['web_api']
            
            return None
            
        except Exception as e:
            print(f"⚠️ Could not get web API instance: {e}")
            return None
    
    def _get_active_endpoints(self) -> list:
        """Get list of active dashboard API endpoints"""
        if not self.dashboard_enhancer:
            return []
        
        return [
            '/api/v1/metrics',
            '/api/v1/metrics/history',
            '/api/v1/components/enhanced',
            '/api/v1/performance',
            '/api/v1/dashboard/data'
        ]
    
    def fix_database_issues(self) -> Dict[str, Any]:
        """Attempt to fix database locking issues"""
        try:
            print("🔧 Attempting to fix database issues...")
            
            # Stop any active monitoring that might be using the database
            if self.dashboard_enhancer:
                self.dashboard_enhancer.system_monitor.stop_monitoring()
                time.sleep(2)
            
            # Try to clear database locks
            import sqlite3
            import os
            
            db_files = ['asis_consciousness.db', 'asis_memory.db', 'asis_learning.db']
            fixed_dbs = []
            
            for db_file in db_files:
                if os.path.exists(db_file):
                    try:
                        # Try to connect and close to clear locks
                        conn = sqlite3.connect(db_file, timeout=1.0)
                        conn.execute("PRAGMA journal_mode=WAL;")
                        conn.commit()
                        conn.close()
                        fixed_dbs.append(db_file)
                        print(f"✅ Fixed database: {db_file}")
                    except Exception as e:
                        print(f"⚠️ Could not fix {db_file}: {e}")
            
            # Restart monitoring if it was active
            if self.dashboard_enhancer:
                time.sleep(1)
                self.dashboard_enhancer.system_monitor.start_monitoring()
            
            return {
                'success': True,
                'message': f'Database fix attempted. Fixed {len(fixed_dbs)} databases.',
                'fixed_databases': fixed_dbs,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Database fix failed: {e}',
                'timestamp': datetime.now().isoformat()
            }

def main():
    """Main control interface - only runs when called directly"""
    controller = DashboardController()
    
    print("\n🎛️ ASIS Dashboard Control Interface")
    print("=" * 50)
    print("Commands:")
    print("  activate   - Activate dashboard enhancement")
    print("  deactivate - Deactivate dashboard enhancement")
    print("  status     - Show current status")
    print("  health     - Show system health")
    print("  restart    - Restart monitoring")
    print("  fix-db     - Fix database issues")
    print("  quit       - Exit")
    print("=" * 50)
    
    while True:
        try:
            command = input("\n🎛️ Dashboard Control > ").strip().lower()
            
            if command == "quit" or command == "exit":
                print("👋 Goodbye!")
                break
                
            elif command == "activate":
                result = controller.activate_dashboard_enhancement()
                print(json.dumps(result, indent=2))
                
            elif command == "deactivate":
                result = controller.deactivate_dashboard_enhancement()
                print(json.dumps(result, indent=2))
                
            elif command == "status":
                result = controller.get_status()
                print(json.dumps(result, indent=2))
                
            elif command == "health":
                result = controller.get_system_health()
                print(json.dumps(result, indent=2))
                
            elif command == "restart":
                result = controller.restart_monitoring()
                print(json.dumps(result, indent=2))
                
            elif command == "fix-db":
                result = controller.fix_database_issues()
                print(json.dumps(result, indent=2))
                
            elif command == "help":
                print("\nAvailable commands: activate, deactivate, status, health, restart, fix-db, quit")
                
            else:
                print(f"❌ Unknown command: {command}")
                print("Type 'help' for available commands")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

# Create convenience functions for programmatic access
def create_controller():
    """Create a dashboard controller instance without starting interactive mode"""
    return DashboardController()

def quick_status():
    """Get quick status without interactive mode"""
    controller = DashboardController()
    return controller.get_status()

def quick_activate():
    """Quick activate without interactive mode"""
    controller = DashboardController()
    return controller.activate_dashboard_enhancement()

def quick_deactivate():
    """Quick deactivate without interactive mode"""
    controller = DashboardController()
    return controller.deactivate_dashboard_enhancement()

if __name__ == "__main__":
    main()