#!/usr/bin/env python3
"""
ASIS Async Utilities
Enhanced by True Self-Modification Engine
"""

import asyncio
from typing import Any, List, Callable, Awaitable

async def async_gather_safe(*coroutines) -> List[Any]:
    """Safely gather async operations with error handling"""
    try:
        results = await asyncio.gather(*coroutines, return_exceptions=True)
        return results
    except Exception as e:
        print(f"Error in async_gather_safe: {e}")
        return []

async def async_timeout(coro: Awaitable[Any], timeout_seconds: float) -> Any:
    """Run async operation with timeout"""
    try:
        return await asyncio.wait_for(coro, timeout=timeout_seconds)
    except asyncio.TimeoutError:
        print(f"Operation timed out after {timeout_seconds} seconds")
        return None
    except Exception as e:
        print(f"Error in async operation: {e}")
        return None

class AsyncTaskManager:
    """Manage async tasks for ASIS"""
    
    def __init__(self):
        self.tasks = []
    
    def add_task(self, coro: Awaitable[Any]) -> None:
        """Add a task to be managed"""
        task = asyncio.create_task(coro)
        self.tasks.append(task)
    
    async def wait_all(self) -> List[Any]:
        """Wait for all tasks to complete"""
        if not self.tasks:
            return []
        
        results = await asyncio.gather(*self.tasks, return_exceptions=True)
        self.tasks.clear()
        return results
