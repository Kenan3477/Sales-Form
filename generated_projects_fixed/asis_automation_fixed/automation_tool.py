#!/usr/bin/env python3
"""
ASIS Generated Automation Tool
==============================
"""

import time
import os
import json
from typing import List, Dict, Any, Callable

class AsisAutomationTool:
    """ASIS Generated Task Automation System"""
    
    def __init__(self):
        self.tasks = []
        self.completed_tasks = 0
        self.failed_tasks = 0
        self.running = False
    
    def add_task(self, name: str, action: Callable, interval: int = 60) -> bool:
        """Add a new automation task"""
        
        task = {
            "name": name,
            "action": action,
            "interval": interval,
            "last_run": 0,
            "runs": 0,
            "success": True
        }
        
        self.tasks.append(task)
        return True
    
    def execute_task(self, task: Dict[str, Any]) -> bool:
        """Execute a single task"""
        
        try:
            current_time = time.time()
            
            if current_time - task["last_run"] >= task["interval"]:
                result = task["action"]()
                task["last_run"] = current_time
                task["runs"] += 1
                task["success"] = True
                self.completed_tasks += 1
                return True
                
        except Exception as e:
            task["success"] = False
            self.failed_tasks += 1
            return False
        
        return False
    
    def run_automation_cycle(self) -> Dict[str, Any]:
        """Run one automation cycle"""
        
        executed = 0
        
        for task in self.tasks:
            if self.execute_task(task):
                executed += 1
        
        return {
            "executed_tasks": executed,
            "total_tasks": len(self.tasks),
            "completed": self.completed_tasks,
            "failed": self.failed_tasks
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get automation status"""
        
        return {
            "running": self.running,
            "total_tasks": len(self.tasks),
            "completed_tasks": self.completed_tasks,
            "failed_tasks": self.failed_tasks,
            "task_details": [
                {
                    "name": task["name"],
                    "runs": task["runs"],
                    "success": task["success"]
                }
                for task in self.tasks
            ]
        }

def sample_task():
    """Sample automation task"""
    print("Executing sample task...")
    return True

def main():
    """Main entry point"""
    automation = AsisAutomationTool()
    
    # Add sample tasks
    automation.add_task("sample_task", sample_task, 1)
    automation.add_task("status_check", lambda: True, 2)
    
    # Run cycles
    for i in range(3):
        result = automation.run_automation_cycle()
        print(f"Cycle {i+1}: {result}")
        time.sleep(1)
    
    status = automation.get_status()
    print(f"Final status: {status}")
    
    return True

if __name__ == "__main__":
    main()
