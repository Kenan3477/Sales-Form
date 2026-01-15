#!/usr/bin/env python3
"""
ASIS Autonomous Cycle Performance Optimizer
===========================================

Intelligent scheduling, load balancing, and adaptive timing for
autonomous cycle operations in production environments.

Author: ASIS Development Team
Date: September 18, 2025
Version: 1.0
"""

import asyncio
import time
import threading
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import statistics
import logging

logger = logging.getLogger(__name__)

class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = 4
    HIGH = 3
    NORMAL = 2
    LOW = 1

class CyclePhase(Enum):
    """Autonomous cycle phases"""
    LEARNING = "learning"
    REASONING = "reasoning"
    RESEARCH = "research"
    INTEGRATION = "integration"
    OPTIMIZATION = "optimization"

@dataclass
class CycleTask:
    """Individual task in autonomous cycle"""
    id: str
    phase: CyclePhase
    priority: TaskPriority
    execution_time_estimate: float
    dependencies: List[str] = field(default_factory=list)
    payload: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    attempts: int = 0
    max_attempts: int = 3

@dataclass
class PerformanceMetrics:
    """Performance metrics for cycle operations"""
    cycle_duration: float
    tasks_completed: int
    tasks_failed: int
    cpu_usage: float
    memory_usage: float
    throughput: float
    efficiency_score: float

class AdaptiveScheduler:
    """Adaptive task scheduler for autonomous cycles"""
    
    def __init__(self):
        self.task_queue: List[CycleTask] = []
        self.executing_tasks: Dict[str, CycleTask] = {}
        self.completed_tasks: List[CycleTask] = []
        self.failed_tasks: List[CycleTask] = []
        
        # Performance tracking
        self.execution_history: List[float] = []
        self.phase_performance: Dict[CyclePhase, List[float]] = {
            phase: [] for phase in CyclePhase
        }
        
        # Adaptive parameters
        self.base_cycle_interval = 5.0  # seconds
        self.current_cycle_interval = 5.0
        self.load_factor = 0.7
        self.adaptation_rate = 0.1
        
        self.lock = threading.Lock()
        logger.info("📅 Adaptive Scheduler initialized")
    
    def add_task(self, task: CycleTask):
        """Add task to scheduler"""
        with self.lock:
            self.task_queue.append(task)
            self.task_queue.sort(key=lambda t: (t.priority.value, t.created_at), reverse=True)
    
    def get_next_tasks(self, max_concurrent: int = 4) -> List[CycleTask]:
        """Get next batch of tasks to execute"""
        with self.lock:
            available_tasks = []
            
            for task in self.task_queue[:]:
                # Check dependencies
                if all(dep in [t.id for t in self.completed_tasks] for dep in task.dependencies):
                    available_tasks.append(task)
                    self.task_queue.remove(task)
                    
                    if len(available_tasks) >= max_concurrent:
                        break
            
            # Move to executing
            for task in available_tasks:
                self.executing_tasks[task.id] = task
            
            return available_tasks
    
    def complete_task(self, task_id: str, execution_time: float, success: bool = True):
        """Mark task as completed"""
        with self.lock:
            if task_id in self.executing_tasks:
                task = self.executing_tasks.pop(task_id)
                
                if success:
                    self.completed_tasks.append(task)
                    
                    # Update performance tracking
                    self.execution_history.append(execution_time)
                    self.phase_performance[task.phase].append(execution_time)
                    
                    # Keep history limited
                    if len(self.execution_history) > 1000:
                        self.execution_history = self.execution_history[-500:]
                    
                    for phase_history in self.phase_performance.values():
                        if len(phase_history) > 200:
                            phase_history[:] = phase_history[-100:]
                else:
                    task.attempts += 1
                    if task.attempts < task.max_attempts:
                        # Retry with lower priority
                        task.priority = TaskPriority(max(1, task.priority.value - 1))
                        self.add_task(task)
                    else:
                        self.failed_tasks.append(task)
    
    def adapt_timing(self) -> Dict[str, Any]:
        """Adapt cycle timing based on performance"""
        if len(self.execution_history) < 10:
            return {'status': 'insufficient_data'}
        
        # Calculate recent performance metrics
        recent_times = self.execution_history[-50:]
        avg_execution_time = statistics.mean(recent_times)
        std_deviation = statistics.stdev(recent_times) if len(recent_times) > 1 else 0
        
        # Adapt cycle interval
        target_utilization = 0.8
        current_utilization = avg_execution_time / self.current_cycle_interval
        
        if current_utilization > target_utilization + 0.1:
            # System overloaded, increase interval
            adjustment = min(2.0, 1 + (current_utilization - target_utilization))
            self.current_cycle_interval = min(30.0, self.current_cycle_interval * adjustment)
        elif current_utilization < target_utilization - 0.1:
            # System underutilized, decrease interval
            adjustment = max(0.5, 1 - (target_utilization - current_utilization))
            self.current_cycle_interval = max(1.0, self.current_cycle_interval * adjustment)
        
        return {
            'previous_interval': self.current_cycle_interval / (1 + self.adaptation_rate),
            'new_interval': self.current_cycle_interval,
            'average_execution_time': avg_execution_time,
            'utilization': current_utilization,
            'adaptation_reason': 'performance_optimization'
        }
    
    def get_scheduling_stats(self) -> Dict[str, Any]:
        """Get scheduler statistics"""
        with self.lock:
            return {
                'queued_tasks': len(self.task_queue),
                'executing_tasks': len(self.executing_tasks),
                'completed_tasks': len(self.completed_tasks),
                'failed_tasks': len(self.failed_tasks),
                'current_cycle_interval': self.current_cycle_interval,
                'average_execution_time': statistics.mean(self.execution_history) if self.execution_history else 0,
                'phase_performance': {
                    phase.value: statistics.mean(times) if times else 0 
                    for phase, times in self.phase_performance.items()
                }
            }

class LoadBalancer:
    """Dynamic load balancer for autonomous operations"""
    
    def __init__(self, max_concurrent_cycles: int = 3):
        self.max_concurrent_cycles = max_concurrent_cycles
        self.active_cycles: Dict[str, Dict[str, Any]] = {}
        self.cycle_performance: Dict[str, List[float]] = {}
        self.resource_usage: Dict[str, float] = {
            'cpu': 0.0,
            'memory': 0.0,
            'io': 0.0
        }
        self.balancing_strategy = "weighted_round_robin"
        
        logger.info("⚖️ Load Balancer initialized")
    
    def register_cycle(self, cycle_id: str, cycle_type: str, weight: float = 1.0):
        """Register autonomous cycle for load balancing"""
        self.active_cycles[cycle_id] = {
            'type': cycle_type,
            'weight': weight,
            'load': 0.0,
            'performance_score': 1.0,
            'last_execution': 0,
            'total_executions': 0
        }
        self.cycle_performance[cycle_id] = []
        logger.info(f"📝 Registered cycle for load balancing: {cycle_id}")
    
    def get_next_cycle(self) -> Optional[str]:
        """Get next cycle to execute based on load balancing"""
        if not self.active_cycles:
            return None
        
        if self.balancing_strategy == "weighted_round_robin":
            return self._weighted_round_robin()
        elif self.balancing_strategy == "performance_based":
            return self._performance_based_selection()
        else:
            return self._simple_round_robin()
    
    def _weighted_round_robin(self) -> Optional[str]:
        """Weighted round robin selection"""
        # Calculate selection weights based on performance and current load
        candidates = []
        
        for cycle_id, cycle_info in self.active_cycles.items():
            if cycle_info['load'] < 1.0:  # Not overloaded
                weight = cycle_info['weight'] * cycle_info['performance_score'] / (cycle_info['load'] + 0.1)
                candidates.append((cycle_id, weight))
        
        if not candidates:
            return None
        
        # Select based on weights
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0]
    
    def _performance_based_selection(self) -> Optional[str]:
        """Performance-based selection"""
        best_cycle = None
        best_score = -1
        
        for cycle_id, cycle_info in self.active_cycles.items():
            if cycle_info['load'] < 0.9:  # Not severely overloaded
                score = cycle_info['performance_score'] / (cycle_info['load'] + 0.1)
                if score > best_score:
                    best_score = score
                    best_cycle = cycle_id
        
        return best_cycle
    
    def _simple_round_robin(self) -> Optional[str]:
        """Simple round robin selection"""
        if not self.active_cycles:
            return None
        
        # Find cycle with oldest last execution
        oldest_cycle = min(
            self.active_cycles.items(),
            key=lambda x: x[1]['last_execution']
        )
        
        return oldest_cycle[0] if oldest_cycle[1]['load'] < 1.0 else None
    
    def update_cycle_load(self, cycle_id: str, load: float):
        """Update cycle load"""
        if cycle_id in self.active_cycles:
            self.active_cycles[cycle_id]['load'] = load
    
    def record_cycle_execution(self, cycle_id: str, execution_time: float, success: bool = True):
        """Record cycle execution for performance tracking"""
        if cycle_id not in self.active_cycles:
            return
        
        cycle_info = self.active_cycles[cycle_id]
        cycle_info['last_execution'] = time.time()
        cycle_info['total_executions'] += 1
        
        # Update performance history
        if cycle_id not in self.cycle_performance:
            self.cycle_performance[cycle_id] = []
        
        self.cycle_performance[cycle_id].append(execution_time)
        
        # Keep history limited
        if len(self.cycle_performance[cycle_id]) > 100:
            self.cycle_performance[cycle_id] = self.cycle_performance[cycle_id][-50:]
        
        # Update performance score
        recent_times = self.cycle_performance[cycle_id][-10:]
        if recent_times:
            avg_time = statistics.mean(recent_times)
            # Performance score based on speed (inverse of time)
            cycle_info['performance_score'] = max(0.1, min(2.0, 5.0 / (avg_time + 1.0)))
    
    def get_load_balancing_stats(self) -> Dict[str, Any]:
        """Get load balancing statistics"""
        return {
            'active_cycles': len(self.active_cycles),
            'balancing_strategy': self.balancing_strategy,
            'cycle_details': {
                cycle_id: {
                    'type': info['type'],
                    'load': info['load'],
                    'performance_score': info['performance_score'],
                    'total_executions': info['total_executions']
                }
                for cycle_id, info in self.active_cycles.items()
            },
            'resource_usage': self.resource_usage.copy()
        }

class ASISAutonomousCycleOptimizer:
    """Main autonomous cycle performance optimizer"""
    
    def __init__(self):
        self.scheduler = AdaptiveScheduler()
        self.load_balancer = LoadBalancer()
        self.optimization_active = False
        self.cycle_thread = None
        
        # Performance tracking
        self.cycle_metrics: List[PerformanceMetrics] = []
        self.optimization_history: List[Dict[str, Any]] = []
        
        logger.info("🔄 Autonomous Cycle Optimizer initialized")
    
    def start_optimization(self):
        """Start autonomous cycle optimization"""
        if self.optimization_active:
            return
        
        self.optimization_active = True
        self.cycle_thread = threading.Thread(target=self._optimization_loop, daemon=True)
        self.cycle_thread.start()
        
        # Register default cycles
        self._register_default_cycles()
        
        logger.info("🚀 Autonomous cycle optimization started")
    
    def stop_optimization(self):
        """Stop autonomous cycle optimization"""
        self.optimization_active = False
        if self.cycle_thread:
            self.cycle_thread.join(timeout=5.0)
        
        logger.info("🛑 Autonomous cycle optimization stopped")
    
    def _register_default_cycles(self):
        """Register default autonomous cycles"""
        cycles = [
            ("learning_cycle", "learning", 1.2),
            ("reasoning_cycle", "reasoning", 1.5),
            ("research_cycle", "research", 1.0),
            ("integration_cycle", "integration", 1.3)
        ]
        
        for cycle_id, cycle_type, weight in cycles:
            self.load_balancer.register_cycle(cycle_id, cycle_type, weight)
    
    def _optimization_loop(self):
        """Main optimization loop"""
        while self.optimization_active:
            try:
                cycle_start = time.time()
                
                # Get next cycle to execute
                next_cycle = self.load_balancer.get_next_cycle()
                if next_cycle:
                    success = self._execute_cycle(next_cycle)
                    
                    execution_time = time.time() - cycle_start
                    self.load_balancer.record_cycle_execution(next_cycle, execution_time, success)
                
                # Adapt timing based on performance
                adaptation_result = self.scheduler.adapt_timing()
                if 'new_interval' in adaptation_result:
                    time.sleep(max(0.1, adaptation_result['new_interval']))
                else:
                    time.sleep(self.scheduler.current_cycle_interval)
                
                # Record metrics
                self._record_cycle_metrics(time.time() - cycle_start)
                
            except Exception as e:
                logger.error(f"Error in optimization loop: {e}")
                time.sleep(5.0)
    
    def _execute_cycle(self, cycle_id: str) -> bool:
        """Execute autonomous cycle"""
        try:
            # Get tasks for this cycle
            tasks = self.scheduler.get_next_tasks(max_concurrent=4)
            
            if not tasks:
                # Create default tasks for cycle
                tasks = self._create_cycle_tasks(cycle_id)
                for task in tasks:
                    self.scheduler.add_task(task)
                tasks = self.scheduler.get_next_tasks(max_concurrent=4)
            
            # Execute tasks
            success_count = 0
            for task in tasks:
                task_start = time.time()
                
                # Simulate task execution
                success = self._execute_task(task)
                
                task_duration = time.time() - task_start
                self.scheduler.complete_task(task.id, task_duration, success)
                
                if success:
                    success_count += 1
            
            # Update load balancer
            load = len(tasks) / 4.0  # Normalize by max concurrent
            self.load_balancer.update_cycle_load(cycle_id, load)
            
            return success_count > 0
            
        except Exception as e:
            logger.error(f"Error executing cycle {cycle_id}: {e}")
            return False
    
    def _create_cycle_tasks(self, cycle_id: str) -> List[CycleTask]:
        """Create tasks for autonomous cycle"""
        cycle_type = self.load_balancer.active_cycles.get(cycle_id, {}).get('type', 'generic')
        
        if cycle_type == "learning":
            return [
                CycleTask("learn_1", CyclePhase.LEARNING, TaskPriority.NORMAL, 2.0),
                CycleTask("adapt_1", CyclePhase.LEARNING, TaskPriority.HIGH, 1.5)
            ]
        elif cycle_type == "reasoning":
            return [
                CycleTask("reason_1", CyclePhase.REASONING, TaskPriority.HIGH, 3.0),
                CycleTask("infer_1", CyclePhase.REASONING, TaskPriority.NORMAL, 2.0)
            ]
        elif cycle_type == "research":
            return [
                CycleTask("research_1", CyclePhase.RESEARCH, TaskPriority.NORMAL, 4.0),
                CycleTask("analyze_1", CyclePhase.RESEARCH, TaskPriority.NORMAL, 2.5)
            ]
        else:
            return [
                CycleTask("integrate_1", CyclePhase.INTEGRATION, TaskPriority.NORMAL, 2.0)
            ]
    
    def _execute_task(self, task: CycleTask) -> bool:
        """Execute individual task"""
        # Simulate task execution
        time.sleep(min(0.1, task.execution_time_estimate / 10))  # Scaled down simulation
        
        # Success rate based on priority and attempts
        success_rate = 0.9 - (task.attempts * 0.1)
        return time.time() % 1.0 < success_rate
    
    def _record_cycle_metrics(self, cycle_duration: float):
        """Record cycle performance metrics"""
        scheduler_stats = self.scheduler.get_scheduling_stats()
        
        metrics = PerformanceMetrics(
            cycle_duration=cycle_duration,
            tasks_completed=scheduler_stats['completed_tasks'],
            tasks_failed=scheduler_stats['failed_tasks'],
            cpu_usage=50.0,  # Mock CPU usage
            memory_usage=200.0,  # Mock memory usage (MB)
            throughput=scheduler_stats['completed_tasks'] / max(1, cycle_duration),
            efficiency_score=scheduler_stats['completed_tasks'] / max(1, scheduler_stats['completed_tasks'] + scheduler_stats['failed_tasks'])
        )
        
        self.cycle_metrics.append(metrics)
        
        # Keep metrics history limited
        if len(self.cycle_metrics) > 1000:
            self.cycle_metrics = self.cycle_metrics[-500:]
    
    def get_optimization_report(self) -> Dict[str, Any]:
        """Get comprehensive optimization report"""
        scheduler_stats = self.scheduler.get_scheduling_stats()
        load_balancer_stats = self.load_balancer.get_load_balancing_stats()
        
        # Calculate performance metrics
        if self.cycle_metrics:
            recent_metrics = self.cycle_metrics[-50:]
            avg_cycle_duration = statistics.mean([m.cycle_duration for m in recent_metrics])
            avg_throughput = statistics.mean([m.throughput for m in recent_metrics])
            avg_efficiency = statistics.mean([m.efficiency_score for m in recent_metrics])
        else:
            avg_cycle_duration = avg_throughput = avg_efficiency = 0
        
        return {
            'scheduler_statistics': scheduler_stats,
            'load_balancer_statistics': load_balancer_stats,
            'performance_metrics': {
                'average_cycle_duration': round(avg_cycle_duration, 3),
                'average_throughput': round(avg_throughput, 2),
                'average_efficiency': round(avg_efficiency, 3),
                'total_cycles_executed': len(self.cycle_metrics)
            },
            'optimization_status': 'active' if self.optimization_active else 'inactive',
            'recommendations': self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        scheduler_stats = self.scheduler.get_scheduling_stats()
        
        if scheduler_stats['failed_tasks'] > scheduler_stats['completed_tasks'] * 0.1:
            recommendations.append("High task failure rate - consider reducing task complexity or increasing retry limits")
        
        if scheduler_stats['current_cycle_interval'] > 10:
            recommendations.append("Cycle interval is high - system may be overloaded, consider scaling resources")
        
        if scheduler_stats['queued_tasks'] > 20:
            recommendations.append("Task queue is growing - consider increasing concurrent task limit")
        
        if not recommendations:
            recommendations.append("System performance is optimal")
        
        return recommendations

# Global autonomous cycle optimizer instance
cycle_optimizer = ASISAutonomousCycleOptimizer()

def get_cycle_optimizer() -> ASISAutonomousCycleOptimizer:
    """Get global autonomous cycle optimizer instance"""
    return cycle_optimizer
