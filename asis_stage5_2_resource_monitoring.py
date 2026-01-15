#!/usr/bin/env python3
"""
ASIS Stage 5.2 - System Resource Monitoring  
===========================================
Real-time monitoring of CPU, memory, disk, and network resources
Autonomous resource analysis and optimization recommendations
"""

import os
import sys
import psutil
import time
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import threading

class AsisResourceMonitor:
    """Autonomous System Resource Monitor"""
    
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S") 
        self.active = True
        self.resource_history = []
        self.alert_thresholds = {
            "cpu_percent": 85.0,
            "memory_percent": 90.0,
            "disk_percent": 85.0,
            "network_mbps": 100.0,
            "temperature_celsius": 80.0
        }
        
        self.stats = {
            "monitoring_cycles": 0,
            "alerts_generated": 0,
            "optimizations_suggested": 0,
            "resource_samples": 0
        }
        
        print(f"[ASIS] Resource Monitor initialized - Session: {self.session_id}")
        self._initialize_baseline()
    
    def _initialize_baseline(self):
        """Initialize system baseline measurements"""
        
        print("[ASIS] Establishing system baseline...")
        
        # CPU baseline
        cpu_counts = psutil.cpu_count(logical=False), psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()
        
        # Memory baseline  
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        # Disk baseline
        disk_partitions = psutil.disk_partitions()
        
        # Network baseline
        network_interfaces = psutil.net_if_addrs()
        
        self.baseline = {
            "cpu_cores_physical": cpu_counts[0],
            "cpu_cores_logical": cpu_counts[1],
            "cpu_max_freq_mhz": cpu_freq.max if cpu_freq else 0,
            "memory_total_gb": memory.total // (1024**3),
            "swap_total_gb": swap.total // (1024**3),
            "disk_partitions": len(disk_partitions),
            "network_interfaces": len(network_interfaces),
            "established_at": datetime.now().isoformat()
        }
        
        print(f"[ASIS] Baseline: {self.baseline['cpu_cores_physical']}C/{self.baseline['cpu_cores_logical']}T CPU, {self.baseline['memory_total_gb']}GB RAM")
    
    def get_cpu_metrics(self) -> Dict[str, Any]:
        """Get detailed CPU performance metrics"""
        
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
        cpu_times = psutil.cpu_times()
        cpu_freq = psutil.cpu_freq()
        
        load_avg = os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
        
        metrics = {
            "cpu_percent_total": cpu_percent,
            "cpu_percent_per_core": cpu_per_core,
            "cpu_freq_current_mhz": cpu_freq.current if cpu_freq else 0,
            "cpu_freq_max_mhz": cpu_freq.max if cpu_freq else 0,
            "cpu_times_user": cpu_times.user,
            "cpu_times_system": cpu_times.system,
            "cpu_times_idle": cpu_times.idle,
            "load_average_1min": load_avg[0],
            "load_average_5min": load_avg[1], 
            "load_average_15min": load_avg[2],
            "cpu_cores_utilized": len([c for c in cpu_per_core if c > 10]),
            "timestamp": datetime.now().isoformat()
        }
        
        return metrics
    
    def get_memory_metrics(self) -> Dict[str, Any]:
        """Get detailed memory performance metrics"""
        
        virtual_mem = psutil.virtual_memory()
        swap_mem = psutil.swap_memory()
        
        metrics = {
            "memory_total_gb": virtual_mem.total / (1024**3),
            "memory_available_gb": virtual_mem.available / (1024**3),
            "memory_used_gb": virtual_mem.used / (1024**3),
            "memory_free_gb": virtual_mem.free / (1024**3),
            "memory_percent_used": virtual_mem.percent,
            "memory_cached_gb": getattr(virtual_mem, 'cached', 0) / (1024**3),
            "memory_buffers_gb": getattr(virtual_mem, 'buffers', 0) / (1024**3),
            "swap_total_gb": swap_mem.total / (1024**3),
            "swap_used_gb": swap_mem.used / (1024**3),
            "swap_free_gb": swap_mem.free / (1024**3),
            "swap_percent_used": swap_mem.percent,
            "memory_pressure": "high" if virtual_mem.percent > 85 else "medium" if virtual_mem.percent > 70 else "low",
            "timestamp": datetime.now().isoformat()
        }
        
        return metrics
    
    def get_disk_metrics(self) -> Dict[str, Any]:
        """Get detailed disk performance metrics"""
        
        disk_usage = {}
        disk_io = psutil.disk_io_counters()
        
        # Get usage for each partition
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_usage[partition.device] = {
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total_gb": usage.total / (1024**3),
                    "used_gb": usage.used / (1024**3), 
                    "free_gb": usage.free / (1024**3),
                    "percent_used": (usage.used / usage.total) * 100
                }
            except PermissionError:
                continue
        
        metrics = {
            "disk_partitions": disk_usage,
            "disk_io_read_count": disk_io.read_count if disk_io else 0,
            "disk_io_write_count": disk_io.write_count if disk_io else 0,
            "disk_io_read_bytes": disk_io.read_bytes if disk_io else 0,
            "disk_io_write_bytes": disk_io.write_bytes if disk_io else 0,
            "disk_io_read_time": disk_io.read_time if disk_io else 0,
            "disk_io_write_time": disk_io.write_time if disk_io else 0,
            "disk_space_critical": any(p["percent_used"] > 90 for p in disk_usage.values()),
            "disk_space_warning": any(p["percent_used"] > 80 for p in disk_usage.values()),
            "timestamp": datetime.now().isoformat()
        }
        
        return metrics
    
    def get_network_metrics(self) -> Dict[str, Any]:
        """Get detailed network performance metrics"""
        
        net_io = psutil.net_io_counters()
        net_connections = len(psutil.net_connections())
        net_interfaces = psutil.net_if_addrs()
        net_stats = psutil.net_if_stats()
        
        # Calculate network speed (requires baseline for accurate measurement)
        active_interfaces = {}
        for interface_name, stats in net_stats.items():
            if stats.isup:
                active_interfaces[interface_name] = {
                    "speed_mbps": stats.speed,
                    "mtu": stats.mtu,
                    "is_up": stats.isup
                }
        
        metrics = {
            "network_bytes_sent": net_io.bytes_sent if net_io else 0,
            "network_bytes_recv": net_io.bytes_recv if net_io else 0,
            "network_packets_sent": net_io.packets_sent if net_io else 0,
            "network_packets_recv": net_io.packets_recv if net_io else 0,
            "network_errors_in": net_io.errin if net_io else 0,
            "network_errors_out": net_io.errout if net_io else 0,
            "network_drops_in": net_io.dropin if net_io else 0,
            "network_drops_out": net_io.dropout if net_io else 0,
            "network_connections_count": net_connections,
            "active_interfaces": active_interfaces,
            "network_interface_count": len(net_interfaces),
            "timestamp": datetime.now().isoformat()
        }
        
        return metrics
    
    def get_temperature_metrics(self) -> Dict[str, Any]:
        """Get system temperature metrics (if available)"""
        
        metrics = {
            "temperature_available": False,
            "cpu_temperature_celsius": None,
            "gpu_temperature_celsius": None,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Try to get temperature readings (Linux/some systems)
            if hasattr(psutil, 'sensors_temperatures'):
                temps = psutil.sensors_temperatures()
                if temps:
                    metrics["temperature_available"] = True
                    
                    # CPU temperature
                    for name, entries in temps.items():
                        if 'cpu' in name.lower() or 'core' in name.lower():
                            if entries:
                                metrics["cpu_temperature_celsius"] = entries[0].current
                                break
                    
                    # GPU temperature  
                    for name, entries in temps.items():
                        if 'gpu' in name.lower() or 'nvidia' in name.lower():
                            if entries:
                                metrics["gpu_temperature_celsius"] = entries[0].current
                                break
                                
        except Exception as e:
            metrics["temperature_error"] = str(e)
        
        return metrics
    
    def get_comprehensive_metrics(self) -> Dict[str, Any]:
        """Get all system resource metrics in one call"""
        
        print("[ASIS] Collecting comprehensive system metrics...")
        
        comprehensive = {
            "session_id": self.session_id,
            "collection_timestamp": datetime.now().isoformat(),
            "cpu": self.get_cpu_metrics(),
            "memory": self.get_memory_metrics(), 
            "disk": self.get_disk_metrics(),
            "network": self.get_network_metrics(),
            "temperature": self.get_temperature_metrics()
        }
        
        self.stats["resource_samples"] += 1
        return comprehensive
    
    def analyze_resource_health(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze system resource health and generate recommendations"""
        
        analysis = {
            "overall_health": "good",
            "warnings": [],
            "critical_issues": [],
            "recommendations": [],
            "resource_scores": {},
            "timestamp": datetime.now().isoformat()
        }
        
        # CPU Analysis
        cpu_score = 100 - metrics["cpu"]["cpu_percent_total"]
        analysis["resource_scores"]["cpu"] = cpu_score
        
        if metrics["cpu"]["cpu_percent_total"] > self.alert_thresholds["cpu_percent"]:
            analysis["critical_issues"].append(f"Critical CPU usage: {metrics['cpu']['cpu_percent_total']:.1f}%")
            analysis["recommendations"].append("Consider closing non-essential applications or upgrading CPU")
        elif metrics["cpu"]["cpu_percent_total"] > 70:
            analysis["warnings"].append(f"High CPU usage: {metrics['cpu']['cpu_percent_total']:.1f}%")
            analysis["recommendations"].append("Monitor CPU-intensive processes")
        
        # Memory Analysis
        memory_score = 100 - metrics["memory"]["memory_percent_used"]
        analysis["resource_scores"]["memory"] = memory_score
        
        if metrics["memory"]["memory_percent_used"] > self.alert_thresholds["memory_percent"]:
            analysis["critical_issues"].append(f"Critical memory usage: {metrics['memory']['memory_percent_used']:.1f}%")
            analysis["recommendations"].append("Free up memory by closing applications or add more RAM")
        elif metrics["memory"]["memory_percent_used"] > 75:
            analysis["warnings"].append(f"High memory usage: {metrics['memory']['memory_percent_used']:.1f}%")
            analysis["recommendations"].append("Monitor memory usage trends")
        
        # Disk Analysis
        disk_scores = []
        for device, disk_info in metrics["disk"]["disk_partitions"].items():
            disk_score = 100 - disk_info["percent_used"]
            disk_scores.append(disk_score)
            
            if disk_info["percent_used"] > self.alert_thresholds["disk_percent"]:
                analysis["critical_issues"].append(f"Critical disk usage on {device}: {disk_info['percent_used']:.1f}%")
                analysis["recommendations"].append(f"Free up space on {device} or expand storage")
            elif disk_info["percent_used"] > 75:
                analysis["warnings"].append(f"High disk usage on {device}: {disk_info['percent_used']:.1f}%")
        
        analysis["resource_scores"]["disk"] = min(disk_scores) if disk_scores else 100
        
        # Network Analysis (basic)
        network_score = 90  # Default good score, adjust based on errors
        if metrics["network"]["network_errors_in"] > 100 or metrics["network"]["network_errors_out"] > 100:
            analysis["warnings"].append("Network errors detected")
            network_score -= 20
        
        analysis["resource_scores"]["network"] = network_score
        
        # Temperature Analysis
        if metrics["temperature"]["temperature_available"] and metrics["temperature"]["cpu_temperature_celsius"]:
            temp = metrics["temperature"]["cpu_temperature_celsius"]
            if temp > self.alert_thresholds["temperature_celsius"]:
                analysis["critical_issues"].append(f"Critical CPU temperature: {temp}°C")
                analysis["recommendations"].append("Check cooling system and clean dust from fans")
            elif temp > 70:
                analysis["warnings"].append(f"High CPU temperature: {temp}°C")
        
        # Overall Health Assessment
        avg_score = sum(analysis["resource_scores"].values()) / len(analysis["resource_scores"])
        
        if analysis["critical_issues"]:
            analysis["overall_health"] = "critical"
        elif analysis["warnings"] or avg_score < 70:
            analysis["overall_health"] = "warning"
        else:
            analysis["overall_health"] = "good"
        
        analysis["overall_score"] = avg_score
        
        if analysis["warnings"] or analysis["critical_issues"]:
            self.stats["alerts_generated"] += 1
        
        if analysis["recommendations"]:
            self.stats["optimizations_suggested"] += len(analysis["recommendations"])
        
        return analysis
    
    def start_continuous_monitoring(self, interval_seconds: int = 60) -> threading.Thread:
        """Start continuous resource monitoring"""
        
        print(f"[ASIS] Starting continuous resource monitoring (interval: {interval_seconds}s)")
        
        def monitoring_loop():
            while self.active:
                try:
                    self.stats["monitoring_cycles"] += 1
                    
                    # Collect metrics
                    metrics = self.get_comprehensive_metrics()
                    
                    # Analyze health
                    analysis = self.analyze_resource_health(metrics)
                    
                    # Store in history
                    history_entry = {
                        "cycle": self.stats["monitoring_cycles"],
                        "timestamp": datetime.now().isoformat(),
                        "overall_health": analysis["overall_health"],
                        "overall_score": analysis["overall_score"],
                        "cpu_percent": metrics["cpu"]["cpu_percent_total"],
                        "memory_percent": metrics["memory"]["memory_percent_used"],
                        "warnings": len(analysis["warnings"]),
                        "critical_issues": len(analysis["critical_issues"])
                    }
                    
                    self.resource_history.append(history_entry)
                    
                    # Keep only last 100 entries
                    if len(self.resource_history) > 100:
                        self.resource_history = self.resource_history[-100:]
                    
                    # Log status
                    print(f"[ASIS] Monitoring cycle {self.stats['monitoring_cycles']}: {analysis['overall_health']} health, score: {analysis['overall_score']:.1f}")
                    
                    if analysis["critical_issues"]:
                        print(f"[ASIS] CRITICAL ISSUES: {analysis['critical_issues']}")
                    
                    if analysis["warnings"]:
                        print(f"[ASIS] WARNINGS: {analysis['warnings']}")
                    
                except Exception as e:
                    print(f"[ASIS] Monitoring error: {e}")
                
                time.sleep(interval_seconds)
        
        monitoring_thread = threading.Thread(target=monitoring_loop, daemon=True)
        monitoring_thread.start()
        
        return monitoring_thread
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.active = False
        print("[ASIS] Resource monitoring stopped")
    
    def get_monitoring_report(self) -> Dict[str, Any]:
        """Generate comprehensive monitoring report"""
        
        current_metrics = self.get_comprehensive_metrics()
        analysis = self.analyze_resource_health(current_metrics)
        
        report = {
            "session_id": self.session_id,
            "report_timestamp": datetime.now().isoformat(),
            "monitoring_stats": self.stats,
            "current_metrics": current_metrics,
            "current_analysis": analysis,
            "baseline": self.baseline,
            "alert_thresholds": self.alert_thresholds,
            "history_summary": {
                "total_entries": len(self.resource_history),
                "recent_entries": self.resource_history[-5:] if self.resource_history else [],
                "avg_cpu_percent": sum(h["cpu_percent"] for h in self.resource_history[-10:]) / min(len(self.resource_history), 10) if self.resource_history else 0,
                "avg_memory_percent": sum(h["memory_percent"] for h in self.resource_history[-10:]) / min(len(self.resource_history), 10) if self.resource_history else 0
            }
        }
        
        return report

def main():
    """Test Stage 5.2 - Resource Monitoring System"""
    print("[ASIS] === STAGE 5.2 - RESOURCE MONITORING TEST ===")
    
    monitor = AsisResourceMonitor()
    
    # Test 1: Single comprehensive metrics collection
    print("\n[ASIS] Test 1: Comprehensive Metrics Collection")
    metrics = monitor.get_comprehensive_metrics()
    
    print(f"[ASIS] CPU Usage: {metrics['cpu']['cpu_percent_total']:.1f}%")
    print(f"[ASIS] Memory Usage: {metrics['memory']['memory_percent_used']:.1f}% ({metrics['memory']['memory_used_gb']:.1f}GB/{metrics['memory']['memory_total_gb']:.1f}GB)")
    print(f"[ASIS] Disk Partitions: {len(metrics['disk']['disk_partitions'])}")
    print(f"[ASIS] Network Connections: {metrics['network']['network_connections_count']}")
    print(f"[ASIS] Temperature Available: {metrics['temperature']['temperature_available']}")
    
    # Test 2: Resource health analysis
    print("\n[ASIS] Test 2: Resource Health Analysis")
    analysis = monitor.analyze_resource_health(metrics)
    
    print(f"[ASIS] Overall Health: {analysis['overall_health']}")
    print(f"[ASIS] Overall Score: {analysis['overall_score']:.1f}/100")
    print(f"[ASIS] Warnings: {len(analysis['warnings'])}")
    print(f"[ASIS] Critical Issues: {len(analysis['critical_issues'])}")
    print(f"[ASIS] Recommendations: {len(analysis['recommendations'])}")
    
    if analysis["recommendations"]:
        print("[ASIS] Top Recommendations:")
        for i, rec in enumerate(analysis["recommendations"][:3], 1):
            print(f"  {i}. {rec}")
    
    # Test 3: Short continuous monitoring
    print("\n[ASIS] Test 3: Continuous Monitoring (30 seconds)")
    monitor_thread = monitor.start_continuous_monitoring(interval_seconds=10)
    time.sleep(30)
    monitor.stop_monitoring()
    
    # Test 4: Generate final report
    print("\n[ASIS] Test 4: Monitoring Report")
    report = monitor.get_monitoring_report()
    
    print(f"[ASIS] === STAGE 5.2 RESULTS ===")
    print(f"Monitoring Cycles: {report['monitoring_stats']['monitoring_cycles']}")
    print(f"Resource Samples: {report['monitoring_stats']['resource_samples']}")
    print(f"Alerts Generated: {report['monitoring_stats']['alerts_generated']}")
    print(f"Optimizations Suggested: {report['monitoring_stats']['optimizations_suggested']}")
    
    success_rate = 100.0 if report['monitoring_stats']['resource_samples'] >= 4 else 0.0
    print(f"Success Rate: {success_rate}%")
    
    if success_rate == 100.0:
        print("[ASIS] ✅ STAGE 5.2 - RESOURCE MONITORING: SUCCESS ✅")
    else:
        print("[ASIS] ❌ STAGE 5.2 - RESOURCE MONITORING: NEEDS IMPROVEMENT ❌")
    
    return report

if __name__ == "__main__":
    main()
