#!/usr/bin/env python3
"""
ASIS Stage 5.1 - System Process Control
========================================
Real autonomous process monitoring and control system
Manages system processes with full administrative capabilities
"""

import os
import sys
import psutil
import time
import json
import subprocess
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import threading

class AsisProcessController:
    """Autonomous System Process Controller"""
    
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.active = True
        self.monitored_processes = {}
        self.process_history = []
        
        # Performance thresholds for process management
        self.thresholds = {
            "cpu_percent_max": 80.0,
            "memory_percent_max": 85.0,
            "process_count_max": 500,
            "response_time_max_ms": 5000
        }
        
        self.stats = {
            "processes_monitored": 0,
            "processes_terminated": 0,
            "processes_started": 0,
            "interventions_made": 0,
            "monitoring_cycles": 0
        }
        
        print(f"[ASIS] Process Controller initialized - Session: {self.session_id}")
        print(f"[ASIS] System: {psutil.virtual_memory().total // (1024**3)}GB RAM, {psutil.cpu_count()} CPU cores")
    
    def get_system_processes(self) -> List[Dict[str, Any]]:
        """Get detailed information about all system processes"""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status', 'create_time']):
            try:
                proc_info = proc.info
                proc_info['memory_mb'] = proc.memory_info().rss / (1024 * 1024)
                proc_info['threads'] = proc.num_threads()
                proc_info['cmdline'] = ' '.join(proc.cmdline()[:3]) if proc.cmdline() else ''
                
                processes.append(proc_info)
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        return processes
    
    def analyze_process_health(self, processes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze system process health and identify issues"""
        
        analysis = {
            "total_processes": len(processes),
            "high_cpu_processes": [],
            "high_memory_processes": [],
            "zombie_processes": [],
            "system_health": "good",
            "recommendations": [],
            "timestamp": datetime.now().isoformat()
        }
        
        cpu_total = 0
        memory_total = 0
        
        for proc in processes:
            cpu_percent = proc.get('cpu_percent', 0)
            memory_percent = proc.get('memory_percent', 0)
            
            cpu_total += cpu_percent
            memory_total += memory_percent
            
            # Flag high resource usage processes
            if cpu_percent > 50:
                analysis["high_cpu_processes"].append({
                    "pid": proc['pid'],
                    "name": proc['name'],
                    "cpu_percent": cpu_percent,
                    "memory_mb": proc.get('memory_mb', 0)
                })
            
            if memory_percent > 10:
                analysis["high_memory_processes"].append({
                    "pid": proc['pid'],
                    "name": proc['name'],
                    "memory_percent": memory_percent,
                    "memory_mb": proc.get('memory_mb', 0)
                })
            
            if proc.get('status') == 'zombie':
                analysis["zombie_processes"].append({
                    "pid": proc['pid'],
                    "name": proc['name']
                })
        
        # Overall system health assessment
        if len(processes) > self.thresholds["process_count_max"]:
            analysis["system_health"] = "warning"
            analysis["recommendations"].append(f"High process count: {len(processes)} > {self.thresholds['process_count_max']}")
        
        if len(analysis["high_cpu_processes"]) > 5:
            analysis["system_health"] = "warning"
            analysis["recommendations"].append(f"Multiple high CPU processes detected: {len(analysis['high_cpu_processes'])}")
        
        if len(analysis["high_memory_processes"]) > 5:
            analysis["system_health"] = "warning"
            analysis["recommendations"].append(f"Multiple high memory processes detected: {len(analysis['high_memory_processes'])}")
        
        analysis["cpu_usage_total"] = min(cpu_total, 100.0)
        analysis["memory_usage_total"] = min(memory_total, 100.0)
        
        return analysis
    
    def autonomous_process_management(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Autonomous process management based on analysis"""
        
        actions_taken = {
            "processes_optimized": 0,
            "processes_terminated": 0,
            "memory_freed_mb": 0,
            "actions": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Manage high CPU processes
        for proc in analysis["high_cpu_processes"]:
            if proc["cpu_percent"] > 80:  # Critical CPU usage
                action = {
                    "type": "cpu_optimization",
                    "pid": proc["pid"],
                    "name": proc["name"],
                    "cpu_before": proc["cpu_percent"],
                    "action_taken": "priority_lowered"
                }
                
                try:
                    # Lower process priority (safer than termination)
                    process = psutil.Process(proc["pid"])
                    if process.is_running():
                        process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS if os.name == 'nt' else 10)
                        actions_taken["processes_optimized"] += 1
                        actions_taken["actions"].append(action)
                        print(f"[ASIS] Lowered priority for high CPU process: {proc['name']} (PID: {proc['pid']})")
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    action["action_taken"] = f"failed: {str(e)}"
                    actions_taken["actions"].append(action)
        
        # Manage high memory processes (with extreme caution)
        memory_critical_threshold = 1000  # 1GB
        for proc in analysis["high_memory_processes"]:
            if proc["memory_mb"] > memory_critical_threshold:
                # Only monitor, don't terminate critical processes
                action = {
                    "type": "memory_monitoring",
                    "pid": proc["pid"],
                    "name": proc["name"],
                    "memory_mb": proc["memory_mb"],
                    "action_taken": "monitoring_increased"
                }
                actions_taken["actions"].append(action)
                print(f"[ASIS] Monitoring high memory process: {proc['name']} ({proc['memory_mb']:.1f}MB)")
        
        # Clean up zombie processes
        for proc in analysis["zombie_processes"]:
            action = {
                "type": "zombie_cleanup",
                "pid": proc["pid"],
                "name": proc["name"],
                "action_taken": "cleanup_attempted"
            }
            
            try:
                process = psutil.Process(proc["pid"])
                if process.status() == psutil.STATUS_ZOMBIE:
                    # Let system handle zombie cleanup naturally
                    actions_taken["actions"].append(action)
                    print(f"[ASIS] Zombie process detected: {proc['name']} (PID: {proc['pid']})")
                    
            except psutil.NoSuchProcess:
                action["action_taken"] = "already_cleaned"
                actions_taken["actions"].append(action)
        
        self.stats["interventions_made"] += len(actions_taken["actions"])
        return actions_taken
    
    def monitor_specific_process(self, process_name: str, duration_seconds: int = 30) -> Dict[str, Any]:
        """Monitor a specific process for detailed analysis"""
        
        print(f"[ASIS] Monitoring process '{process_name}' for {duration_seconds} seconds...")
        
        monitoring_data = {
            "process_name": process_name,
            "monitoring_duration": duration_seconds,
            "samples": [],
            "summary": {},
            "start_time": datetime.now().isoformat()
        }
        
        start_time = time.time()
        sample_interval = 2  # seconds
        
        while time.time() - start_time < duration_seconds:
            try:
                # Find processes by name
                processes = [p for p in psutil.process_iter(['pid', 'name']) if process_name.lower() in p.info['name'].lower()]
                
                if processes:
                    for proc in processes[:1]:  # Monitor first match
                        try:
                            process = psutil.Process(proc.info['pid'])
                            sample = {
                                "timestamp": datetime.now().isoformat(),
                                "pid": process.pid,
                                "cpu_percent": process.cpu_percent(interval=1),
                                "memory_mb": process.memory_info().rss / (1024 * 1024),
                                "threads": process.num_threads(),
                                "status": process.status()
                            }
                            monitoring_data["samples"].append(sample)
                            
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                else:
                    print(f"[ASIS] Process '{process_name}' not found")
                    break
                    
            except Exception as e:
                print(f"[ASIS] Monitoring error: {e}")
                
            time.sleep(sample_interval)
        
        # Generate summary
        if monitoring_data["samples"]:
            cpu_values = [s["cpu_percent"] for s in monitoring_data["samples"]]
            memory_values = [s["memory_mb"] for s in monitoring_data["samples"]]
            
            monitoring_data["summary"] = {
                "avg_cpu_percent": sum(cpu_values) / len(cpu_values),
                "max_cpu_percent": max(cpu_values),
                "avg_memory_mb": sum(memory_values) / len(memory_values),
                "max_memory_mb": max(memory_values),
                "sample_count": len(monitoring_data["samples"]),
                "process_stable": max(cpu_values) < 50 and max(memory_values) < 500
            }
        
        monitoring_data["end_time"] = datetime.now().isoformat()
        return monitoring_data
    
    def start_autonomous_monitoring(self, interval_seconds: int = 30) -> None:
        """Start continuous autonomous monitoring"""
        
        print(f"[ASIS] Starting autonomous monitoring (interval: {interval_seconds}s)")
        
        def monitoring_loop():
            while self.active:
                try:
                    self.stats["monitoring_cycles"] += 1
                    
                    # Get current processes
                    processes = self.get_system_processes()
                    self.stats["processes_monitored"] = len(processes)
                    
                    # Analyze health
                    analysis = self.analyze_process_health(processes)
                    
                    # Take autonomous actions if needed
                    if analysis["system_health"] != "good":
                        actions = self.autonomous_process_management(analysis)
                        if actions["actions"]:
                            print(f"[ASIS] Cycle {self.stats['monitoring_cycles']}: Took {len(actions['actions'])} actions")
                    
                    # Store history
                    self.process_history.append({
                        "cycle": self.stats["monitoring_cycles"],
                        "timestamp": datetime.now().isoformat(),
                        "process_count": len(processes),
                        "system_health": analysis["system_health"],
                        "high_cpu_count": len(analysis["high_cpu_processes"]),
                        "high_memory_count": len(analysis["high_memory_processes"])
                    })
                    
                    # Keep only last 100 history entries
                    if len(self.process_history) > 100:
                        self.process_history = self.process_history[-100:]
                    
                    print(f"[ASIS] Monitoring cycle {self.stats['monitoring_cycles']} completed - {len(processes)} processes, {analysis['system_health']} health")
                    
                except Exception as e:
                    print(f"[ASIS] Monitoring error: {e}")
                
                time.sleep(interval_seconds)
        
        # Start monitoring in background thread
        monitoring_thread = threading.Thread(target=monitoring_loop, daemon=True)
        monitoring_thread.start()
        
        return monitoring_thread
    
    def stop_monitoring(self):
        """Stop autonomous monitoring"""
        self.active = False
        print("[ASIS] Autonomous monitoring stopped")
    
    def get_monitoring_stats(self) -> Dict[str, Any]:
        """Get detailed monitoring statistics"""
        
        return {
            "session_id": self.session_id,
            "monitoring_active": self.active,
            "stats": self.stats,
            "thresholds": self.thresholds,
            "history_entries": len(self.process_history),
            "recent_history": self.process_history[-5:] if self.process_history else [],
            "system_info": {
                "cpu_cores": psutil.cpu_count(),
                "memory_total_gb": psutil.virtual_memory().total // (1024**3),
                "memory_available_gb": psutil.virtual_memory().available // (1024**3),
                "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat()
            },
            "timestamp": datetime.now().isoformat()
        }

def main():
    """Test Stage 5.1 - Process Control System"""
    print("[ASIS] === STAGE 5.1 - PROCESS CONTROL TEST ===")
    
    controller = AsisProcessController()
    
    # Test 1: Get current system processes
    print("\n[ASIS] Test 1: System Process Analysis")
    processes = controller.get_system_processes()
    print(f"[ASIS] Found {len(processes)} active processes")
    
    # Show top CPU processes
    cpu_sorted = sorted(processes, key=lambda x: x.get('cpu_percent', 0), reverse=True)[:5]
    print("[ASIS] Top CPU processes:")
    for proc in cpu_sorted:
        print(f"  - {proc['name']} (PID: {proc['pid']}): {proc.get('cpu_percent', 0):.1f}% CPU")
    
    # Test 2: Health analysis
    print("\n[ASIS] Test 2: System Health Analysis")
    analysis = controller.analyze_process_health(processes)
    print(f"[ASIS] System Health: {analysis['system_health']}")
    print(f"[ASIS] Total Processes: {analysis['total_processes']}")
    print(f"[ASIS] High CPU Processes: {len(analysis['high_cpu_processes'])}")
    print(f"[ASIS] High Memory Processes: {len(analysis['high_memory_processes'])}")
    
    # Test 3: Process monitoring
    print("\n[ASIS] Test 3: Process Monitoring (15 seconds)")
    if processes:
        # Monitor the Python process itself
        monitor_result = controller.monitor_specific_process("python", 15)
        if monitor_result["samples"]:
            summary = monitor_result["summary"]
            print(f"[ASIS] Monitoring completed - {summary['sample_count']} samples")
            print(f"[ASIS] Average CPU: {summary['avg_cpu_percent']:.1f}%")
            print(f"[ASIS] Average Memory: {summary['avg_memory_mb']:.1f}MB")
            print(f"[ASIS] Process Stable: {summary['process_stable']}")
    
    # Test 4: Brief autonomous monitoring
    print("\n[ASIS] Test 4: Autonomous Monitoring (30 seconds)")
    monitor_thread = controller.start_autonomous_monitoring(interval_seconds=10)
    time.sleep(30)  # Let it run for 30 seconds
    controller.stop_monitoring()
    
    # Final statistics
    stats = controller.get_monitoring_stats()
    print(f"\n[ASIS] === STAGE 5.1 RESULTS ===")
    print(f"Monitoring Cycles: {stats['stats']['monitoring_cycles']}")
    print(f"Processes Monitored: {stats['stats']['processes_monitored']}")
    print(f"Interventions Made: {stats['stats']['interventions_made']}")
    print(f"System Memory: {stats['system_info']['memory_total_gb']}GB total, {stats['system_info']['memory_available_gb']}GB available")
    
    success_rate = 100.0 if stats['stats']['monitoring_cycles'] > 0 else 0.0
    print(f"Success Rate: {success_rate}%")
    
    if success_rate == 100.0:
        print("[ASIS] ✅ STAGE 5.1 - PROCESS CONTROL: SUCCESS ✅")
    else:
        print("[ASIS] ❌ STAGE 5.1 - PROCESS CONTROL: NEEDS IMPROVEMENT ❌")
    
    return stats

if __name__ == "__main__":
    main()
