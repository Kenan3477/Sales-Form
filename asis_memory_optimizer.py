#!/usr/bin/env python3
"""
ASIS Memory Optimization Module
===============================

Advanced memory management and optimization for ASIS production deployment.
Implements caching strategies, garbage collection tuning, and memory leak detection.

Author: ASIS Development Team
Date: September 18, 2025
Version: 1.0
"""

import gc
import sys
import weakref
import threading
import time
from typing import Dict, Any, Optional, Set, List
from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)

class LRUCache:
    """Least Recently Used cache with size limits"""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache: OrderedDict = OrderedDict()
        self.hits = 0
        self.misses = 0
        self.lock = threading.RLock()
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache"""
        with self.lock:
            if key in self.cache:
                # Move to end (most recently used)
                value = self.cache.pop(key)
                self.cache[key] = value
                self.hits += 1
                return value
            else:
                self.misses += 1
                return None
    
    def put(self, key: str, value: Any):
        """Put item in cache"""
        with self.lock:
            if key in self.cache:
                # Update existing
                self.cache.pop(key)
            elif len(self.cache) >= self.max_size:
                # Remove oldest
                self.cache.popitem(last=False)
            
            self.cache[key] = value
    
    def clear(self):
        """Clear all cached items"""
        with self.lock:
            self.cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate_percent': round(hit_rate, 2)
        }

class ObjectPool:
    """Object pool for reusing expensive objects"""
    
    def __init__(self, factory_func, max_size: int = 100):
        self.factory_func = factory_func
        self.max_size = max_size
        self.pool: List[Any] = []
        self.lock = threading.Lock()
        self.created_count = 0
        self.reused_count = 0
    
    def get_object(self):
        """Get object from pool or create new one"""
        with self.lock:
            if self.pool:
                obj = self.pool.pop()
                self.reused_count += 1
                return obj
            else:
                obj = self.factory_func()
                self.created_count += 1
                return obj
    
    def return_object(self, obj):
        """Return object to pool"""
        with self.lock:
            if len(self.pool) < self.max_size:
                # Reset object state if needed
                if hasattr(obj, 'reset'):
                    obj.reset()
                self.pool.append(obj)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get pool statistics"""
        return {
            'pool_size': len(self.pool),
            'max_size': self.max_size,
            'created': self.created_count,
            'reused': self.reused_count,
            'reuse_rate': (self.reused_count / (self.created_count + self.reused_count) * 100) 
                         if (self.created_count + self.reused_count) > 0 else 0
        }

class MemoryLeakDetector:
    """Detect and track potential memory leaks"""
    
    def __init__(self, check_interval: int = 60):
        self.check_interval = check_interval
        self.object_counts: Dict[str, List[int]] = {}
        self.tracking_active = False
        self.thread: Optional[threading.Thread] = None
        self.suspicious_types: Set[str] = set()
    
    def start_tracking(self):
        """Start memory leak tracking"""
        if self.tracking_active:
            return
        
        self.tracking_active = True
        self.thread = threading.Thread(target=self._tracking_loop, daemon=True)
        self.thread.start()
        logger.info("🔍 Memory leak detection started")
    
    def stop_tracking(self):
        """Stop memory leak tracking"""
        self.tracking_active = False
        if self.thread:
            self.thread.join(timeout=5.0)
    
    def _tracking_loop(self):
        """Main tracking loop"""
        while self.tracking_active:
            try:
                self._check_object_counts()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error in memory leak tracking: {e}")
                time.sleep(self.check_interval)
    
    def _check_object_counts(self):
        """Check object counts for potential leaks"""
        # Get current object counts by type
        current_counts = {}
        for obj in gc.get_objects():
            obj_type = type(obj).__name__
            current_counts[obj_type] = current_counts.get(obj_type, 0) + 1
        
        # Track significant types
        significant_types = {k: v for k, v in current_counts.items() if v > 100}
        
        for obj_type, count in significant_types.items():
            if obj_type not in self.object_counts:
                self.object_counts[obj_type] = []
            
            self.object_counts[obj_type].append(count)
            
            # Keep only recent history
            if len(self.object_counts[obj_type]) > 10:
                self.object_counts[obj_type] = self.object_counts[obj_type][-10:]
            
            # Check for consistent growth
            if len(self.object_counts[obj_type]) >= 5:
                recent_counts = self.object_counts[obj_type][-5:]
                if all(recent_counts[i] < recent_counts[i+1] for i in range(len(recent_counts)-1)):
                    if obj_type not in self.suspicious_types:
                        self.suspicious_types.add(obj_type)
                        logger.warning(f"⚠️ Potential memory leak detected: {obj_type} (growing consistently)")
    
    def get_leak_report(self) -> Dict[str, Any]:
        """Get memory leak detection report"""
        return {
            'suspicious_types': list(self.suspicious_types),
            'tracked_types': len(self.object_counts),
            'tracking_duration': self.check_interval * max(len(counts) for counts in self.object_counts.values()) if self.object_counts else 0
        }

class ASISMemoryManager:
    """Comprehensive memory management system"""
    
    def __init__(self):
        self.caches: Dict[str, LRUCache] = {}
        self.object_pools: Dict[str, ObjectPool] = {}
        self.leak_detector = MemoryLeakDetector()
        self.cleanup_thread: Optional[threading.Thread] = None
        self.cleanup_active = False
        self.gc_stats = {'collections': 0, 'collected': 0}
        
        # Initialize default caches
        self._initialize_caches()
        
        logger.info("🧠 ASIS Memory Manager initialized")
    
    def _initialize_caches(self):
        """Initialize default caches"""
        self.caches['component_cache'] = LRUCache(max_size=500)
        self.caches['response_cache'] = LRUCache(max_size=1000)
        self.caches['knowledge_cache'] = LRUCache(max_size=2000)
        self.caches['reasoning_cache'] = LRUCache(max_size=800)
    
    def start_management(self):
        """Start memory management services"""
        # Start leak detection
        self.leak_detector.start_tracking()
        
        # Start cleanup thread
        self.cleanup_active = True
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.cleanup_thread.start()
        
        # Optimize garbage collection
        self.optimize_garbage_collection()
        
        logger.info("🚀 Memory management services started")
    
    def stop_management(self):
        """Stop memory management services"""
        self.cleanup_active = False
        if self.cleanup_thread:
            self.cleanup_thread.join(timeout=5.0)
        
        self.leak_detector.stop_tracking()
        logger.info("🛑 Memory management services stopped")
    
    def optimize_garbage_collection(self):
        """Optimize Python garbage collection"""
        # Set more aggressive thresholds
        gc.set_threshold(700, 10, 10)
        
        # Enable garbage collection debugging in development
        if __debug__:
            gc.set_debug(gc.DEBUG_STATS)
        
        # Force initial cleanup
        collected = gc.collect()
        self.gc_stats['collections'] += 1
        self.gc_stats['collected'] += collected
        
        logger.info(f"♻️ Garbage collection optimized, collected {collected} objects")
    
    def _cleanup_loop(self):
        """Periodic cleanup operations"""
        while self.cleanup_active:
            try:
                # Clean caches periodically
                self._periodic_cache_cleanup()
                
                # Force garbage collection
                collected = gc.collect()
                self.gc_stats['collections'] += 1
                self.gc_stats['collected'] += collected
                
                time.sleep(300)  # 5 minutes
                
            except Exception as e:
                logger.error(f"Error in cleanup loop: {e}")
                time.sleep(60)
    
    def _periodic_cache_cleanup(self):
        """Periodic cache cleanup"""
        for name, cache in self.caches.items():
            stats = cache.get_stats()
            
            # Clear cache if hit rate is very low
            if stats['hit_rate_percent'] < 5 and stats['size'] > 100:
                cache.clear()
                logger.info(f"🧹 Cleared low-efficiency cache: {name}")
    
    def get_cache(self, name: str) -> Optional[LRUCache]:
        """Get cache by name"""
        return self.caches.get(name)
    
    def create_cache(self, name: str, max_size: int = 1000) -> LRUCache:
        """Create new cache"""
        cache = LRUCache(max_size=max_size)
        self.caches[name] = cache
        return cache
    
    def create_object_pool(self, name: str, factory_func, max_size: int = 100) -> ObjectPool:
        """Create object pool"""
        pool = ObjectPool(factory_func, max_size=max_size)
        self.object_pools[name] = pool
        return pool
    
    def get_object_pool(self, name: str) -> Optional[ObjectPool]:
        """Get object pool by name"""
        return self.object_pools.get(name)
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get comprehensive memory statistics"""
        import psutil
        
        process = psutil.Process()
        memory_info = process.memory_info()
        
        # Cache statistics
        cache_stats = {}
        for name, cache in self.caches.items():
            cache_stats[name] = cache.get_stats()
        
        # Pool statistics
        pool_stats = {}
        for name, pool in self.object_pools.items():
            pool_stats[name] = pool.get_stats()
        
        # Garbage collection stats
        gc_info = {
            'counts': gc.get_count(),
            'thresholds': gc.get_threshold(),
            'collections_performed': self.gc_stats['collections'],
            'objects_collected': self.gc_stats['collected']
        }
        
        # Memory leak detection
        leak_report = self.leak_detector.get_leak_report()
        
        return {
            'system_memory': {
                'rss_mb': round(memory_info.rss / 1024 / 1024, 2),
                'vms_mb': round(memory_info.vms / 1024 / 1024, 2),
                'percent': round(process.memory_percent(), 2)
            },
            'cache_statistics': cache_stats,
            'object_pool_statistics': pool_stats,
            'garbage_collection': gc_info,
            'leak_detection': leak_report,
            'total_objects': len(gc.get_objects())
        }
    
    def force_cleanup(self) -> Dict[str, Any]:
        """Force immediate memory cleanup"""
        logger.info("🧹 Forcing memory cleanup...")
        
        # Clear all caches
        cleared_items = 0
        for cache in self.caches.values():
            stats = cache.get_stats()
            cleared_items += stats['size']
            cache.clear()
        
        # Force garbage collection
        collected = 0
        for _ in range(3):  # Multiple passes
            collected += gc.collect()
        
        self.gc_stats['collections'] += 3
        self.gc_stats['collected'] += collected
        
        result = {
            'caches_cleared': len(self.caches),
            'items_cleared': cleared_items,
            'objects_collected': collected
        }
        
        logger.info(f"✅ Cleanup complete: {collected} objects collected, {cleared_items} cache items cleared")
        return result

# Global memory manager instance
memory_manager = ASISMemoryManager()

def get_memory_manager() -> ASISMemoryManager:
    """Get global memory manager instance"""
    return memory_manager
