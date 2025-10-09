#!/usr/bin/env python3
"""
ASIS Stage 5.5 - System Resource Management Integration Test
============================================================
Complete integration test of all Stage 5 components
Tests the full autonomous system resource management capability
"""

import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Any

# Import all Stage 5 components
sys.path.append(os.path.dirname(__file__))

try:
    from asis_stage5_1_process_control import AsisProcessController
    from asis_stage5_2_resource_monitoring import AsisResourceMonitor  
    from asis_stage5_3_performance_optimization import AsisPerformanceOptimizer
    from asis_stage5_4_environmental_adaptation import AsisEnvironmentalAdapter
except ImportError as e:
    print(f"[ASIS] Import error: {e}")
    print("[ASIS] Please ensure all Stage 5 components are in the same directory")
    sys.exit(1)

class AsisStage5IntegrationTest:
    """Complete Stage 5 Integration Test Suite"""
    
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.test_results = {}
        self.overall_stats = {
            "tests_passed": 0,
            "tests_failed": 0,
            "components_tested": 0,
            "integration_success": False
        }
        
        print(f"[ASIS] Stage 5 Integration Test initialized - Session: {self.session_id}")
    
    def test_process_control_component(self) -> Dict[str, Any]:
        """Test Stage 5.1 - Process Control"""
        
        print("\n[ASIS] === Testing Process Control Component ===")
        
        test_result = {
            "component": "Process Control",
            "version": "5.1",
            "success": False,
            "details": {},
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            controller = AsisProcessController()
            
            # Test process monitoring
            processes = controller.get_system_processes()
            test_result["details"]["processes_found"] = len(processes)
            
            # Test health analysis
            analysis = controller.analyze_process_health(processes)
            test_result["details"]["system_health"] = analysis["system_health"]
            
            # Test brief monitoring
            monitor_thread = controller.start_autonomous_monitoring(interval_seconds=5)
            time.sleep(10)  # 10 second test
            controller.stop_monitoring()
            
            stats = controller.get_monitoring_stats()
            test_result["details"]["monitoring_cycles"] = stats["stats"]["monitoring_cycles"]
            
            # Success criteria
            test_result["success"] = (
                len(processes) > 50 and 
                stats["stats"]["monitoring_cycles"] >= 1
            )
            
            if test_result["success"]:
                self.overall_stats["tests_passed"] += 1
                print("[ASIS] ✅ Process Control: PASSED")
            else:
                self.overall_stats["tests_failed"] += 1
                print("[ASIS] ❌ Process Control: FAILED")
            
        except Exception as e:
            test_result["error"] = str(e)
            self.overall_stats["tests_failed"] += 1
            print(f"[ASIS] ❌ Process Control: ERROR - {e}")
        
        self.overall_stats["components_tested"] += 1
        return test_result
    
    def test_resource_monitoring_component(self) -> Dict[str, Any]:
        """Test Stage 5.2 - Resource Monitoring"""
        
        print("\n[ASIS] === Testing Resource Monitoring Component ===")
        
        test_result = {
            "component": "Resource Monitoring",
            "version": "5.2", 
            "success": False,
            "details": {},
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            monitor = AsisResourceMonitor()
            
            # Test comprehensive metrics
            metrics = monitor.get_comprehensive_metrics()
            test_result["details"]["cpu_usage"] = metrics["cpu"]["cpu_percent_total"]
            test_result["details"]["memory_usage"] = metrics["memory"]["memory_percent_used"]
            
            # Test health analysis
            analysis = monitor.analyze_resource_health(metrics)
            test_result["details"]["overall_health"] = analysis["overall_health"]
            test_result["details"]["overall_score"] = analysis["overall_score"]
            
            # Test continuous monitoring
            monitor_thread = monitor.start_continuous_monitoring(interval_seconds=5)
            time.sleep(10)  # 10 second test
            monitor.stop_monitoring()
            
            report = monitor.get_monitoring_report()
            test_result["details"]["resource_samples"] = report["monitoring_stats"]["resource_samples"]
            
            # Success criteria
            test_result["success"] = (
                report["monitoring_stats"]["resource_samples"] >= 2 and
                analysis["overall_score"] > 0
            )
            
            if test_result["success"]:
                self.overall_stats["tests_passed"] += 1
                print("[ASIS] ✅ Resource Monitoring: PASSED")
            else:
                self.overall_stats["tests_failed"] += 1
                print("[ASIS] ❌ Resource Monitoring: FAILED")
            
        except Exception as e:
            test_result["error"] = str(e)
            self.overall_stats["tests_failed"] += 1
            print(f"[ASIS] ❌ Resource Monitoring: ERROR - {e}")
        
        self.overall_stats["components_tested"] += 1
        return test_result
    
    def test_performance_optimization_component(self) -> Dict[str, Any]:
        """Test Stage 5.3 - Performance Optimization"""
        
        print("\n[ASIS] === Testing Performance Optimization Component ===")
        
        test_result = {
            "component": "Performance Optimization",
            "version": "5.3",
            "success": False,
            "details": {},
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            optimizer = AsisPerformanceOptimizer()
            
            # Test performance analysis
            analysis = optimizer.analyze_performance_bottlenecks()
            test_result["details"]["performance_score"] = analysis["performance_score"]
            
            # Test individual optimizations
            memory_result = optimizer.optimize_memory_usage()
            test_result["details"]["memory_optimization"] = memory_result["success"]
            
            cpu_result = optimizer.optimize_cpu_usage()
            test_result["details"]["cpu_optimization"] = cpu_result["success"]
            
            # Test optimization cycle
            cycle_result = optimizer.autonomous_optimization_cycle()
            test_result["details"]["optimization_cycle"] = cycle_result["overall_success"]
            
            report = optimizer.get_optimization_report()
            test_result["details"]["optimizations_attempted"] = report["optimization_stats"]["optimizations_attempted"]
            
            # Success criteria
            test_result["success"] = (
                report["optimization_stats"]["optimizations_attempted"] >= 1 and
                cycle_result["overall_success"]
            )
            
            if test_result["success"]:
                self.overall_stats["tests_passed"] += 1
                print("[ASIS] ✅ Performance Optimization: PASSED")
            else:
                self.overall_stats["tests_failed"] += 1
                print("[ASIS] ❌ Performance Optimization: FAILED")
            
        except Exception as e:
            test_result["error"] = str(e)
            self.overall_stats["tests_failed"] += 1
            print(f"[ASIS] ❌ Performance Optimization: ERROR - {e}")
        
        self.overall_stats["components_tested"] += 1
        return test_result
    
    def test_environmental_adaptation_component(self) -> Dict[str, Any]:
        """Test Stage 5.4 - Environmental Adaptation"""
        
        print("\n[ASIS] === Testing Environmental Adaptation Component ===")
        
        test_result = {
            "component": "Environmental Adaptation",
            "version": "5.4",
            "success": False,
            "details": {},
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            adapter = AsisEnvironmentalAdapter()
            
            # Test environment detection
            test_result["details"]["environment_type"] = adapter.environment_profile["environment_type"]
            
            # Test environmental monitoring
            env_status = adapter.monitor_environmental_changes()
            test_result["details"]["changes_detected"] = len(env_status["changes_detected"])
            
            # Test adaptation cycle
            cycle_result = adapter.autonomous_adaptation_cycle()
            test_result["details"]["adaptation_success"] = cycle_result["success"]
            test_result["details"]["performance_impact"] = cycle_result["performance_impact"]
            
            report = adapter.get_adaptation_report()
            test_result["details"]["environment_changes_detected"] = report["adaptation_stats"]["environment_changes_detected"]
            
            # Success criteria
            test_result["success"] = (
                adapter.environment_profile["environment_type"] is not None and
                cycle_result["success"]
            )
            
            if test_result["success"]:
                self.overall_stats["tests_passed"] += 1
                print("[ASIS] ✅ Environmental Adaptation: PASSED")
            else:
                self.overall_stats["tests_failed"] += 1
                print("[ASIS] ❌ Environmental Adaptation: FAILED")
            
        except Exception as e:
            test_result["error"] = str(e)
            self.overall_stats["tests_failed"] += 1
            print(f"[ASIS] ❌ Environmental Adaptation: ERROR - {e}")
        
        self.overall_stats["components_tested"] += 1
        return test_result
    
    def test_integrated_system_operation(self) -> Dict[str, Any]:
        """Test integrated operation of all components"""
        
        print("\n[ASIS] === Testing Integrated System Operation ===")
        
        test_result = {
            "component": "Integrated System",
            "version": "5.5",
            "success": False,
            "details": {},
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Initialize all components simultaneously
            controller = AsisProcessController()
            monitor = AsisResourceMonitor()
            optimizer = AsisPerformanceOptimizer()
            adapter = AsisEnvironmentalAdapter()
            
            print("[ASIS] All components initialized successfully")
            
            # Test coordinated operation
            start_time = time.time()
            
            # Get baseline metrics
            processes = controller.get_system_processes()
            metrics = monitor.get_comprehensive_metrics()
            analysis = optimizer.analyze_performance_bottlenecks()
            env_status = adapter.monitor_environmental_changes()
            
            # Simulate coordinated resource management
            process_health = controller.analyze_process_health(processes)
            resource_analysis = monitor.analyze_resource_health(metrics)
            performance_cycle = optimizer.autonomous_optimization_cycle()
            adaptation_cycle = adapter.autonomous_adaptation_cycle()
            
            integration_time = time.time() - start_time
            
            test_result["details"]["integration_time_seconds"] = integration_time
            test_result["details"]["processes_monitored"] = len(processes)
            test_result["details"]["system_health"] = process_health["system_health"]
            test_result["details"]["resource_health"] = resource_analysis["overall_health"]
            test_result["details"]["performance_optimized"] = performance_cycle["overall_success"]
            test_result["details"]["environment_adapted"] = adaptation_cycle["success"]
            
            # Integration success criteria
            integration_success = (
                len(processes) > 50 and
                resource_analysis["overall_score"] > 0 and
                integration_time < 60  # Complete integration in under 60 seconds
            )
            
            test_result["success"] = integration_success
            
            if test_result["success"]:
                self.overall_stats["tests_passed"] += 1
                self.overall_stats["integration_success"] = True
                print("[ASIS] ✅ Integrated System: PASSED")
            else:
                self.overall_stats["tests_failed"] += 1
                print("[ASIS] ❌ Integrated System: FAILED")
            
        except Exception as e:
            test_result["error"] = str(e)
            self.overall_stats["tests_failed"] += 1
            print(f"[ASIS] ❌ Integrated System: ERROR - {e}")
        
        self.overall_stats["components_tested"] += 1
        return test_result
    
    def run_complete_integration_test(self) -> Dict[str, Any]:
        """Run complete Stage 5 integration test suite"""
        
        print("[ASIS] === STAGE 5 COMPLETE INTEGRATION TEST ===")
        print(f"[ASIS] Session ID: {self.session_id}")
        print(f"[ASIS] Test Start: {datetime.now().isoformat()}")
        
        # Run all component tests
        self.test_results["process_control"] = self.test_process_control_component()
        self.test_results["resource_monitoring"] = self.test_resource_monitoring_component()
        self.test_results["performance_optimization"] = self.test_performance_optimization_component()
        self.test_results["environmental_adaptation"] = self.test_environmental_adaptation_component()
        self.test_results["integrated_system"] = self.test_integrated_system_operation()
        
        # Calculate overall results
        total_tests = self.overall_stats["tests_passed"] + self.overall_stats["tests_failed"]
        success_rate = (self.overall_stats["tests_passed"] / total_tests * 100) if total_tests > 0 else 0
        
        final_report = {
            "session_id": self.session_id,
            "test_completion_timestamp": datetime.now().isoformat(),
            "overall_stats": self.overall_stats,
            "success_rate_percent": success_rate,
            "test_results": self.test_results,
            "stage_5_complete": success_rate >= 80.0 and self.overall_stats["integration_success"]
        }
        
        return final_report

def main():
    """Execute Stage 5.5 - Complete Integration Test"""
    
    integration_tester = AsisStage5IntegrationTest()
    final_report = integration_tester.run_complete_integration_test()
    
    print(f"\n[ASIS] === STAGE 5.5 FINAL RESULTS ===")
    print(f"Components Tested: {final_report['overall_stats']['components_tested']}")
    print(f"Tests Passed: {final_report['overall_stats']['tests_passed']}")
    print(f"Tests Failed: {final_report['overall_stats']['tests_failed']}")
    print(f"Success Rate: {final_report['success_rate_percent']:.1f}%")
    print(f"Integration Success: {final_report['overall_stats']['integration_success']}")
    print(f"Stage 5 Complete: {final_report['stage_5_complete']}")
    
    if final_report['stage_5_complete']:
        print("\n[ASIS] 🎉 STAGE 5 - SYSTEM RESOURCE MANAGEMENT: COMPLETE! 🎉")
        print("[ASIS] ✅ All components integrated and functioning")
        print("[ASIS] ✅ Autonomous resource management achieved")
        print("[ASIS] ✅ Ready for Stage 6 - AGI Integration")
    else:
        print(f"\n[ASIS] ⚠️ STAGE 5: {final_report['success_rate_percent']:.1f}% success rate")
        print("[ASIS] ❌ Stage 5 needs improvement before Stage 6")
    
    return final_report

if __name__ == "__main__":
    main()
