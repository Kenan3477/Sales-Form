#!/usr/bin/env python3
"""
ASIS Automation Scheduler
=========================
"""

import time
import threading
from typing import Dict, List, Any

class AsisScheduler:
    """Task scheduling system"""
    
    def __init__(self):
        self.scheduled_tasks = []
        self.running_tasks = {}
        self.scheduler_active = False
    
    def schedule_task(self, task_name: str, interval: int, action: callable) -> bool:
        """Schedule a recurring task"""
        
        task_info = {
            "name": task_name,
            "interval": interval,
            "action": action,
            "next_run": time.time() + interval,
            "executions": 0
        }
        
        self.scheduled_tasks.append(task_info)
        return True
    
    def run_scheduler(self) -> None:
        """Run the task scheduler"""
        
        self.scheduler_active = True
        
        while self.scheduler_active:
            current_time = time.time()
            
            for task in self.scheduled_tasks:
                if current_time >= task["next_run"]:
                    try:
                        task["action"]()
                        task["executions"] += 1
                        task["next_run"] = current_time + task["interval"]
                    except Exception:
                        pass
            
            time.sleep(1)
    
    def stop_scheduler(self) -> None:
        """Stop the scheduler"""
        self.scheduler_active = False
    
    def get_scheduler_status(self) -> Dict[str, Any]:
        """Get scheduler status"""
        
        return {
            "active": self.scheduler_active,
            "scheduled_tasks": len(self.scheduled_tasks),
            "task_info": [
                {
                    "name": task["name"],
                    "interval": task["interval"],
                    "executions": task["executions"]
                }
                for task in self.scheduled_tasks
            ]
        }
