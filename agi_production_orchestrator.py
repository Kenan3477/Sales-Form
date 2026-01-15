#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 ASIS AGI Production Integration System
Master orchestration system for comprehensive AGI deployment

This module provides:
- Unified system orchestration
- Component health monitoring
- Automated deployment management
- Performance optimization
- Customer service integration
- System administration tools

Author: ASIS AGI Development Team
Version: 1.0.0
"""

import os
import sys
import time
import json
import threading
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import all AGI system components
try:
    from asis_agi_production import UnifiedAGIControllerProduction
    from agi_testing_framework import AGITestFramework
    from agi_health_check import AGIHealthChecker
    from agi_performance_monitor import AGIPerformanceMonitor
    from agi_customer_interface import CustomerAGIInterface
    from migrations.agi_database_migrations import AGIDatabaseMigrator
except ImportError as e:
    print(f"⚠️ Warning: Some AGI components not available: {e}")

@dataclass
class SystemComponent:
    """System component definition"""
    name: str
    service_type: str  # 'core', 'monitoring', 'interface', 'database'
    status: str  # 'starting', 'running', 'stopped', 'error'
    health_score: float  # 0.0 to 1.0
    last_check: datetime
    error_message: Optional[str] = None
    process_id: Optional[int] = None

class AGIProductionOrchestrator:
    """Master orchestrator for AGI production system"""
    
    def __init__(self, config_path: str = "agi_production_config.json"):
        self.config_path = config_path
        self.components = {}
        self.system_status = "initializing"
        self.orchestrator_thread = None
        self.running = False
        
        # System managers
        self.agi_controller = None
        self.health_checker = None
        self.performance_monitor = None
        self.customer_interface = None
        self.database_migrator = None
        self.test_framework = None
        
        # Configuration
        self.config = self._load_configuration()
        
        # Logging setup
        self._setup_logging()
        
        print("🔧 AGI Production Orchestrator initialized")
    
    def _load_configuration(self) -> Dict[str, Any]:
        """Load system configuration"""
        default_config = {
            "system": {
                "deployment_environment": "production",
                "debug_mode": False,
                "auto_recovery": True,
                "health_check_interval": 30,
                "performance_monitoring_interval": 60
            },
            "components": {
                "agi_core": {
                    "enabled": True,
                    "priority": 1,
                    "auto_start": True,
                    "health_threshold": 0.8
                },
                "database": {
                    "enabled": True,
                    "priority": 1,
                    "auto_migrate": True,
                    "backup_enabled": True
                },
                "monitoring": {
                    "enabled": True,
                    "priority": 2,
                    "auto_start": True,
                    "alert_threshold": 0.7
                },
                "customer_interface": {
                    "enabled": True,
                    "priority": 3,
                    "port": 5001,
                    "auto_start": True
                },
                "health_checks": {
                    "enabled": True,
                    "priority": 2,
                    "critical_threshold": 0.6
                }
            },
            "deployment": {
                "run_tests_on_startup": True,
                "migrate_database_on_startup": True,
                "enable_performance_monitoring": True,
                "customer_interface_port": 5001
            }
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                # Merge with defaults
                default_config.update(loaded_config)
            except Exception as e:
                print(f"⚠️ Error loading config: {e}, using defaults")
        
        return default_config
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_level = logging.DEBUG if self.config["system"]["debug_mode"] else logging.INFO
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('agi_production.log'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('AGIOrchestrator')
        self.logger.info("Logging system initialized")
    
    def initialize_system(self) -> bool:
        """Initialize all system components"""
        self.logger.info("🔧 Initializing AGI Production System...")
        
        initialization_steps = [
            ("Database Migration", self._initialize_database),
            ("AGI Core System", self._initialize_agi_core),
            ("Health Checker", self._initialize_health_checker),
            ("Performance Monitor", self._initialize_performance_monitor),
            ("Customer Interface", self._initialize_customer_interface),
            ("Test Framework", self._initialize_test_framework)
        ]
        
        success_count = 0
        for step_name, init_function in initialization_steps:
            try:
                self.logger.info(f"🔧 Initializing: {step_name}")
                if init_function():
                    success_count += 1
                    self.logger.info(f"✅ {step_name} initialized successfully")
                else:
                    self.logger.error(f"❌ {step_name} initialization failed")
            except Exception as e:
                self.logger.error(f"❌ {step_name} initialization error: {e}")
        
        success_rate = success_count / len(initialization_steps)
        
        if success_rate >= 0.8:  # 80% success rate required
            self.system_status = "initialized"
            self.logger.info(f"🔧 System initialization completed: {success_count}/{len(initialization_steps)} components")
            return True
        else:
            self.system_status = "failed"
            self.logger.error(f"🔧 System initialization failed: {success_count}/{len(initialization_steps)} components")
            return False
    
    def _initialize_database(self) -> bool:
        """Initialize database system"""
        try:
            if self.config["components"]["database"]["enabled"]:
                self.database_migrator = AGIDatabaseMigrator()
                
                if self.config["components"]["database"]["auto_migrate"]:
                    self.database_migrator.run_all_migrations()
                
                self._register_component("database", "database", "running", 1.0)
                return True
            return True
        except Exception as e:
            self.logger.error(f"Database initialization error: {e}")
            self._register_component("database", "database", "error", 0.0, str(e))
            return False
    
    def _initialize_agi_core(self) -> bool:
        """Initialize AGI core system"""
        try:
            if self.config["components"]["agi_core"]["enabled"]:
                self.agi_controller = UnifiedAGIControllerProduction()
                status = self.agi_controller.get_agi_system_status()
                
                if "error" not in status:
                    health_score = status.get("system_status", {}).get("system_coherence", 0.5)
                    self._register_component("agi_core", "core", "running", health_score)
                    return True
                else:
                    self._register_component("agi_core", "core", "error", 0.0, status.get("error"))
                    return False
            return True
        except Exception as e:
            self.logger.error(f"AGI core initialization error: {e}")
            self._register_component("agi_core", "core", "error", 0.0, str(e))
            return False
    
    def _initialize_health_checker(self) -> bool:
        """Initialize health checking system"""
        try:
            if self.config["components"]["health_checks"]["enabled"]:
                self.health_checker = AGIHealthChecker()
                self._register_component("health_checker", "monitoring", "running", 1.0)
                return True
            return True
        except Exception as e:
            self.logger.error(f"Health checker initialization error: {e}")
            self._register_component("health_checker", "monitoring", "error", 0.0, str(e))
            return False
    
    def _initialize_performance_monitor(self) -> bool:
        """Initialize performance monitoring system"""
        try:
            if self.config["components"]["monitoring"]["enabled"]:
                self.performance_monitor = AGIPerformanceMonitor()
                
                if self.config["deployment"]["enable_performance_monitoring"]:
                    monitoring_interval = self.config["system"]["performance_monitoring_interval"]
                    self.performance_monitor.start_monitoring(monitoring_interval)
                
                self._register_component("performance_monitor", "monitoring", "running", 1.0)
                return True
            return True
        except Exception as e:
            self.logger.error(f"Performance monitor initialization error: {e}")
            self._register_component("performance_monitor", "monitoring", "error", 0.0, str(e))
            return False
    
    def _initialize_customer_interface(self) -> bool:
        """Initialize customer interface system"""
        try:
            if self.config["components"]["customer_interface"]["enabled"]:
                self.customer_interface = CustomerAGIInterface()
                self._register_component("customer_interface", "interface", "running", 1.0)
                return True
            return True
        except Exception as e:
            self.logger.error(f"Customer interface initialization error: {e}")
            self._register_component("customer_interface", "interface", "error", 0.0, str(e))
            return False
    
    def _initialize_test_framework(self) -> bool:
        """Initialize testing framework"""
        try:
            self.test_framework = AGITestFramework()
            
            if self.config["deployment"]["run_tests_on_startup"]:
                self.logger.info("Running startup tests...")
                test_results = self.test_framework.run_all_tests()
                
                if test_results["overall_success"]:
                    self.logger.info("✅ Startup tests passed")
                else:
                    self.logger.warning("⚠️ Some startup tests failed")
            
            self._register_component("test_framework", "testing", "running", 1.0)
            return True
        except Exception as e:
            self.logger.error(f"Test framework initialization error: {e}")
            self._register_component("test_framework", "testing", "error", 0.0, str(e))
            return False
    
    def _register_component(self, name: str, service_type: str, status: str, 
                           health_score: float, error_message: str = None):
        """Register a system component"""
        self.components[name] = SystemComponent(
            name=name,
            service_type=service_type,
            status=status,
            health_score=health_score,
            last_check=datetime.now(),
            error_message=error_message
        )
    
    def start_system(self) -> bool:
        """Start the complete AGI production system"""
        self.logger.info("🚀 Starting AGI Production System...")
        
        if not self.initialize_system():
            self.logger.error("❌ System initialization failed, cannot start")
            return False
        
        self.running = True
        self.system_status = "starting"
        
        # Start orchestrator thread
        self.orchestrator_thread = threading.Thread(target=self._orchestration_loop, daemon=True)
        self.orchestrator_thread.start()
        
        # Start customer interface if enabled
        if self.config["components"]["customer_interface"]["enabled"]:
            self._start_customer_interface()
        
        self.system_status = "running"
        self.logger.info("🚀 AGI Production System started successfully")
        
        return True
    
    def _start_customer_interface(self):
        """Start customer interface in separate process"""
        try:
            port = self.config["components"]["customer_interface"]["port"]
            
            # Start customer interface server
            def run_customer_server():
                from agi_customer_interface import create_customer_app
                app = create_customer_app()
                app.run(host='0.0.0.0', port=port, debug=False)
            
            interface_thread = threading.Thread(target=run_customer_server, daemon=True)
            interface_thread.start()
            
            self.logger.info(f"🌐 Customer interface started on port {port}")
            
        except Exception as e:
            self.logger.error(f"Customer interface startup error: {e}")
    
    def _orchestration_loop(self):
        """Main orchestration loop"""
        self.logger.info("🔧 Orchestration loop started")
        
        while self.running:
            try:
                # Perform health checks
                self._perform_health_checks()
                
                # Monitor system performance
                self._monitor_system_performance()
                
                # Handle component failures
                self._handle_component_failures()
                
                # Cleanup and maintenance
                self._perform_maintenance()
                
                # Sleep until next cycle
                time.sleep(self.config["system"]["health_check_interval"])
                
            except Exception as e:
                self.logger.error(f"Orchestration loop error: {e}")
                time.sleep(30)  # Emergency fallback interval
    
    def _perform_health_checks(self):
        """Perform comprehensive health checks"""
        try:
            if self.health_checker:
                health_status = self.health_checker.run_all_health_checks()
                
                # Update component health scores
                for component_name, component_health in health_status.get("components", {}).items():
                    if component_name.lower().replace(" ", "_") in self.components:
                        comp_key = component_name.lower().replace(" ", "_")
                        
                        # Convert status to health score
                        if component_health["status"] == "healthy":
                            health_score = 1.0
                        elif component_health["status"] == "warning":
                            health_score = 0.7
                        else:
                            health_score = 0.3
                        
                        self.components[comp_key].health_score = health_score
                        self.components[comp_key].last_check = datetime.now()
                
                # Log critical issues
                if health_status.get("critical_issues"):
                    for issue in health_status["critical_issues"]:
                        self.logger.critical(f"🚨 Critical Issue: {issue}")
                
        except Exception as e:
            self.logger.error(f"Health check error: {e}")
    
    def _monitor_system_performance(self):
        """Monitor system performance metrics"""
        try:
            if self.performance_monitor:
                # Get performance summary
                summary = self.performance_monitor.get_performance_summary(1)  # Last hour
                
                # Check for performance alerts
                if summary.get("alerts", {}).get("total", 0) > 0:
                    self.logger.warning(f"⚠️ Performance alerts: {summary['alerts']['total']}")
                
                # Log system metrics
                if summary.get("system_metrics"):
                    sys_metrics = summary["system_metrics"]
                    self.logger.debug(f"System metrics - CPU: {sys_metrics.get('cpu_usage', {}).get('avg', 0):.1f}%, "
                                    f"Memory: {sys_metrics.get('memory_usage', {}).get('avg', 0):.1f}%")
                
        except Exception as e:
            self.logger.error(f"Performance monitoring error: {e}")
    
    def _handle_component_failures(self):
        """Handle component failures with auto-recovery"""
        if not self.config["system"]["auto_recovery"]:
            return
        
        for component_name, component in self.components.items():
            if component.health_score < self.config["components"].get(component_name, {}).get("health_threshold", 0.5):
                self.logger.warning(f"⚠️ Component {component_name} health below threshold: {component.health_score}")
                
                # Attempt recovery
                if self._attempt_component_recovery(component_name):
                    self.logger.info(f"✅ Component {component_name} recovered")
                else:
                    self.logger.error(f"❌ Component {component_name} recovery failed")
    
    def _attempt_component_recovery(self, component_name: str) -> bool:
        """Attempt to recover a failed component"""
        try:
            component = self.components.get(component_name)
            if not component:
                return False
            
            self.logger.info(f"🔧 Attempting recovery for component: {component_name}")
            
            # Component-specific recovery logic
            if component_name == "agi_core":
                return self._recover_agi_core()
            elif component_name == "performance_monitor":
                return self._recover_performance_monitor()
            elif component_name == "customer_interface":
                return self._recover_customer_interface()
            
            return False
            
        except Exception as e:
            self.logger.error(f"Component recovery error for {component_name}: {e}")
            return False
    
    def _recover_agi_core(self) -> bool:
        """Recover AGI core system"""
        try:
            if self.agi_controller:
                self.agi_controller.shutdown_agi_system()
            
            # Reinitialize
            return self._initialize_agi_core()
            
        except Exception as e:
            self.logger.error(f"AGI core recovery error: {e}")
            return False
    
    def _recover_performance_monitor(self) -> bool:
        """Recover performance monitoring system"""
        try:
            if self.performance_monitor:
                self.performance_monitor.stop_monitoring()
            
            return self._initialize_performance_monitor()
            
        except Exception as e:
            self.logger.error(f"Performance monitor recovery error: {e}")
            return False
    
    def _recover_customer_interface(self) -> bool:
        """Recover customer interface system"""
        try:
            # Reinitialize customer interface
            return self._initialize_customer_interface()
            
        except Exception as e:
            self.logger.error(f"Customer interface recovery error: {e}")
            return False
    
    def _perform_maintenance(self):
        """Perform system maintenance tasks"""
        try:
            current_time = datetime.now()
            
            # Daily maintenance tasks
            if current_time.hour == 2 and current_time.minute < 30:  # 2 AM
                self._daily_maintenance()
            
            # Weekly maintenance tasks
            if current_time.weekday() == 6 and current_time.hour == 3:  # Sunday 3 AM
                self._weekly_maintenance()
                
        except Exception as e:
            self.logger.error(f"Maintenance error: {e}")
    
    def _daily_maintenance(self):
        """Daily maintenance tasks"""
        self.logger.info("🧹 Performing daily maintenance...")
        
        try:
            # Clean up old performance data
            if self.performance_monitor:
                self.performance_monitor.cleanup_old_data(days=7)
            
            # Generate daily report
            self._generate_daily_report()
            
        except Exception as e:
            self.logger.error(f"Daily maintenance error: {e}")
    
    def _weekly_maintenance(self):
        """Weekly maintenance tasks"""
        self.logger.info("🧹 Performing weekly maintenance...")
        
        try:
            # Run comprehensive tests
            if self.test_framework:
                test_results = self.test_framework.run_all_tests()
                self.logger.info(f"Weekly test results: {test_results['tests_passed']}/{test_results['total_tests']} passed")
            
            # Database maintenance
            if self.database_migrator:
                # Could add database optimization here
                pass
            
        except Exception as e:
            self.logger.error(f"Weekly maintenance error: {e}")
    
    def _generate_daily_report(self):
        """Generate daily system report"""
        try:
            if self.performance_monitor:
                report = self.performance_monitor.generate_performance_report()
                
                # Save report to file
                report_filename = f"daily_report_{datetime.now().strftime('%Y%m%d')}.md"
                with open(report_filename, 'w') as f:
                    f.write(report)
                
                self.logger.info(f"📋 Daily report saved: {report_filename}")
                
        except Exception as e:
            self.logger.error(f"Daily report generation error: {e}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            "system_status": self.system_status,
            "timestamp": datetime.now().isoformat(),
            "components": {name: asdict(component) for name, component in self.components.items()},
            "uptime": self._get_system_uptime(),
            "health_summary": self._get_health_summary(),
            "performance_summary": self._get_performance_summary()
        }
    
    def _get_system_uptime(self) -> str:
        """Get system uptime"""
        # This would be calculated from system start time
        return "System uptime tracking not implemented"
    
    def _get_health_summary(self) -> Dict[str, Any]:
        """Get health summary"""
        if not self.components:
            return {"overall_health": 0.0, "component_count": 0}
        
        total_health = sum(comp.health_score for comp in self.components.values())
        avg_health = total_health / len(self.components)
        
        return {
            "overall_health": avg_health,
            "component_count": len(self.components),
            "healthy_components": len([c for c in self.components.values() if c.health_score > 0.8]),
            "warning_components": len([c for c in self.components.values() if 0.5 <= c.health_score <= 0.8]),
            "critical_components": len([c for c in self.components.values() if c.health_score < 0.5])
        }
    
    def _get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        try:
            if self.performance_monitor:
                return self.performance_monitor.get_performance_summary(1)
            return {}
        except:
            return {}
    
    def stop_system(self):
        """Stop the AGI production system"""
        self.logger.info("🛑 Stopping AGI Production System...")
        
        self.running = False
        self.system_status = "stopping"
        
        # Stop components
        if self.performance_monitor:
            self.performance_monitor.stop_monitoring()
        
        if self.agi_controller:
            self.agi_controller.shutdown_agi_system()
        
        # Wait for orchestrator thread to finish
        if self.orchestrator_thread:
            self.orchestrator_thread.join(timeout=30)
        
        self.system_status = "stopped"
        self.logger.info("🛑 AGI Production System stopped")

def main():
    """Main production system function"""
    print("🔧 ASIS AGI Production Integration System")
    print("=" * 50)
    
    orchestrator = AGIProductionOrchestrator()
    
    try:
        # Start the system
        if orchestrator.start_system():
            print("🚀 AGI Production System started successfully!")
            print("📊 System Status Dashboard:")
            
            # Main monitoring loop
            while True:
                status = orchestrator.get_system_status()
                
                print(f"\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"📈 System Status: {status['system_status']}")
                print(f"🏥 Overall Health: {status['health_summary']['overall_health']:.2f}")
                print(f"🧩 Components: {status['health_summary']['healthy_components']}/{status['health_summary']['component_count']} healthy")
                
                time.sleep(60)  # Update every minute
                
        else:
            print("❌ Failed to start AGI Production System")
            
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested...")
        orchestrator.stop_system()
        print("✅ AGI Production System shutdown complete")

if __name__ == "__main__":
    main()
