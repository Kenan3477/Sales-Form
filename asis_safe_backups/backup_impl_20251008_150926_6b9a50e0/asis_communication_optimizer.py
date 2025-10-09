#!/usr/bin/env python3
"""
ASIS Component Communication Optimizer
======================================

Optimizes inter-component communication with efficient messaging,
connection pooling, and data serialization for production performance.

Author: ASIS Development Team
Date: September 18, 2025
Version: 1.0
"""

import asyncio
import json
import pickle
import threading
import time
import zlib
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass
from collections import deque
import logging

logger = logging.getLogger(__name__)

@dataclass
class Message:
    """Inter-component message structure"""
    source: str
    target: str
    message_type: str
    payload: Any
    timestamp: float
    priority: int = 1  # 1=low, 2=normal, 3=high, 4=critical
    compression: bool = False
    serialization: str = "json"  # json, pickle, msgpack

class ConnectionPool:
    """Connection pool for component communications"""
    
    def __init__(self, max_connections: int = 20):
        self.max_connections = max_connections
        self.available_connections = deque()
        self.active_connections = set()
        self.lock = threading.Lock()
        self.created_count = 0
        self.reused_count = 0
    
    def get_connection(self):
        """Get connection from pool"""
        with self.lock:
            if self.available_connections:
                conn = self.available_connections.pop()
                self.active_connections.add(conn)
                self.reused_count += 1
                return conn
            else:
                # Create new connection
                conn = self._create_connection()
                self.active_connections.add(conn)
                self.created_count += 1
                return conn
    
    def return_connection(self, connection):
        """Return connection to pool"""
        with self.lock:
            if connection in self.active_connections:
                self.active_connections.remove(connection)
                
                if len(self.available_connections) < self.max_connections:
                    self.available_connections.append(connection)
                else:
                    # Pool full, close connection
                    self._close_connection(connection)
    
    def _create_connection(self):
        """Create new connection (mock implementation)"""
        return {
            'id': f"conn_{self.created_count}",
            'created_at': time.time(),
            'status': 'active'
        }
    
    def _close_connection(self, connection):
        """Close connection"""
        connection['status'] = 'closed'
    
    def get_stats(self) -> Dict[str, Any]:
        """Get connection pool statistics"""
        return {
            'max_connections': self.max_connections,
            'available': len(self.available_connections),
            'active': len(self.active_connections),
            'created': self.created_count,
            'reused': self.reused_count,
            'reuse_rate': (self.reused_count / (self.created_count + self.reused_count) * 100) 
                         if (self.created_count + self.reused_count) > 0 else 0
        }

class MessageSerializer:
    """Optimized message serialization"""
    
    @staticmethod
    def serialize(data: Any, method: str = "json", compress: bool = False) -> bytes:
        """Serialize data to bytes"""
        if method == "json":
            serialized = json.dumps(data, default=str).encode('utf-8')
        elif method == "pickle":
            serialized = pickle.dumps(data)
        else:
            # Fallback to JSON
            serialized = json.dumps(data, default=str).encode('utf-8')
        
        if compress:
            serialized = zlib.compress(serialized)
        
        return serialized
    
    @staticmethod
    def deserialize(data: bytes, method: str = "json", compressed: bool = False) -> Any:
        """Deserialize bytes to data"""
        if compressed:
            data = zlib.decompress(data)
        
        if method == "json":
            return json.loads(data.decode('utf-8'))
        elif method == "pickle":
            return pickle.loads(data)
        else:
            # Fallback to JSON
            return json.loads(data.decode('utf-8'))

class MessageQueue:
    """Priority-based message queue"""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.queues = {
            4: deque(),  # Critical
            3: deque(),  # High
            2: deque(),  # Normal
            1: deque()   # Low
        }
        self.lock = threading.Lock()
        self.total_messages = 0
        self.processed_messages = 0
    
    def put(self, message: Message) -> bool:
        """Add message to queue"""
        with self.lock:
            if self.total_messages >= self.max_size:
                # Drop lowest priority messages if full
                for priority in [1, 2, 3]:
                    if self.queues[priority]:
                        self.queues[priority].popleft()
                        break
                else:
                    return False  # All queues have critical messages
            
            self.queues[message.priority].append(message)
            self.total_messages += 1
            return True
    
    def get(self) -> Optional[Message]:
        """Get highest priority message"""
        with self.lock:
            # Check priorities from highest to lowest
            for priority in [4, 3, 2, 1]:
                if self.queues[priority]:
                    message = self.queues[priority].popleft()
                    self.total_messages -= 1
                    self.processed_messages += 1
                    return message
            return None
    
    def size(self) -> int:
        """Get total queue size"""
        return self.total_messages
    
    def get_stats(self) -> Dict[str, Any]:
        """Get queue statistics"""
        return {
            'total_messages': self.total_messages,
            'processed_messages': self.processed_messages,
            'queue_sizes': {str(p): len(q) for p, q in self.queues.items()},
            'utilization': (self.total_messages / self.max_size * 100) if self.max_size > 0 else 0
        }

class ComponentCommunicationHub:
    """Central communication hub for components"""
    
    def __init__(self):
        self.registered_components = {}
        self.message_queue = MessageQueue()
        self.connection_pool = ConnectionPool()
        self.serializer = MessageSerializer()
        
        # Statistics
        self.message_stats = {
            'sent': 0,
            'received': 0,
            'failed': 0,
            'bytes_transferred': 0
        }
        
        # Communication optimization settings
        self.optimization_config = {
            'compression_threshold': 1024,  # Compress messages > 1KB
            'batch_size': 50,
            'keep_alive_timeout': 60,
            'default_serialization': 'json'
        }
        
        self.running = False
        self.processor_thread = None
        
        logger.info("📡 Component Communication Hub initialized")
    
    def start(self):
        """Start communication hub"""
        if self.running:
            return
        
        self.running = True
        self.processor_thread = threading.Thread(target=self._message_processor, daemon=True)
        self.processor_thread.start()
        
        logger.info("🚀 Communication hub started")
    
    def stop(self):
        """Stop communication hub"""
        self.running = False
        if self.processor_thread:
            self.processor_thread.join(timeout=5.0)
        
        logger.info("🛑 Communication hub stopped")
    
    def register_component(self, name: str, component: Any, message_handler: Callable):
        """Register component for communication"""
        self.registered_components[name] = {
            'component': component,
            'handler': message_handler,
            'registered_at': time.time()
        }
        logger.info(f"📝 Registered component: {name}")
    
    def send_message(self, source: str, target: str, message_type: str, 
                    payload: Any, priority: int = 2) -> bool:
        """Send message between components"""
        # Determine optimal serialization and compression
        serialization = self.optimization_config['default_serialization']
        compression = False
        
        # Estimate payload size for compression decision
        if isinstance(payload, (dict, list)) and len(str(payload)) > self.optimization_config['compression_threshold']:
            compression = True
        
        message = Message(
            source=source,
            target=target,
            message_type=message_type,
            payload=payload,
            timestamp=time.time(),
            priority=priority,
            compression=compression,
            serialization=serialization
        )
        
        success = self.message_queue.put(message)
        if success:
            self.message_stats['sent'] += 1
        else:
            self.message_stats['failed'] += 1
            logger.warning(f"Failed to queue message from {source} to {target}")
        
        return success
    
    def _message_processor(self):
        """Process messages in queue"""
        while self.running:
            try:
                message = self.message_queue.get()
                if message:
                    self._deliver_message(message)
                else:
                    time.sleep(0.01)  # Small delay when no messages
                    
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                time.sleep(0.1)
    
    def _deliver_message(self, message: Message):
        """Deliver message to target component"""
        target_info = self.registered_components.get(message.target)
        if not target_info:
            logger.warning(f"Target component not found: {message.target}")
            self.message_stats['failed'] += 1
            return
        
        try:
            # Get connection from pool
            connection = self.connection_pool.get_connection()
            
            # Serialize message
            serialized_payload = self.serializer.serialize(
                message.payload, 
                message.serialization, 
                message.compression
            )
            
            # Update statistics
            self.message_stats['bytes_transferred'] += len(serialized_payload)
            
            # Deliver to handler
            handler = target_info['handler']
            handler(message)
            
            self.message_stats['received'] += 1
            
            # Return connection to pool
            self.connection_pool.return_connection(connection)
            
        except Exception as e:
            logger.error(f"Error delivering message: {e}")
            self.message_stats['failed'] += 1
    
    def get_communication_stats(self) -> Dict[str, Any]:
        """Get communication statistics"""
        return {
            'message_stats': self.message_stats.copy(),
            'queue_stats': self.message_queue.get_stats(),
            'connection_pool_stats': self.connection_pool.get_stats(),
            'registered_components': len(self.registered_components),
            'optimization_config': self.optimization_config.copy()
        }
    
    def optimize_communication(self) -> Dict[str, Any]:
        """Apply communication optimizations"""
        optimizations = []
        
        # Adjust batch size based on queue utilization
        queue_stats = self.message_queue.get_stats()
        if queue_stats['utilization'] > 80:
            self.optimization_config['batch_size'] = min(100, self.optimization_config['batch_size'] * 2)
            optimizations.append("Increased batch size for high utilization")
        elif queue_stats['utilization'] < 20:
            self.optimization_config['batch_size'] = max(10, self.optimization_config['batch_size'] // 2)
            optimizations.append("Decreased batch size for low utilization")
        
        # Adjust compression threshold based on transfer stats
        avg_message_size = (self.message_stats['bytes_transferred'] / max(1, self.message_stats['sent']))
        if avg_message_size > 2048:  # Large messages
            self.optimization_config['compression_threshold'] = 512  # More aggressive compression
            optimizations.append("Lowered compression threshold for large messages")
        elif avg_message_size < 256:  # Small messages
            self.optimization_config['compression_threshold'] = 2048  # Less compression overhead
            optimizations.append("Raised compression threshold for small messages")
        
        # Connection pool optimization
        pool_stats = self.connection_pool.get_stats()
        if pool_stats['reuse_rate'] < 50:
            optimizations.append("Connection pool efficiency could be improved")
        
        return {
            'optimizations_applied': optimizations,
            'new_config': self.optimization_config.copy()
        }

class ASISCommunicationOptimizer:
    """Main communication optimization coordinator"""
    
    def __init__(self):
        self.hub = ComponentCommunicationHub()
        self.optimization_active = False
        self.optimization_thread = None
    
    def start_optimization(self):
        """Start communication optimization"""
        self.hub.start()
        
        self.optimization_active = True
        self.optimization_thread = threading.Thread(target=self._optimization_loop, daemon=True)
        self.optimization_thread.start()
        
        logger.info("⚡ Communication optimization started")
    
    def stop_optimization(self):
        """Stop communication optimization"""
        self.optimization_active = False
        if self.optimization_thread:
            self.optimization_thread.join(timeout=5.0)
        
        self.hub.stop()
        logger.info("🛑 Communication optimization stopped")
    
    def _optimization_loop(self):
        """Continuous optimization loop"""
        while self.optimization_active:
            try:
                time.sleep(30)  # Optimize every 30 seconds
                self.hub.optimize_communication()
            except Exception as e:
                logger.error(f"Error in optimization loop: {e}")
                time.sleep(60)
    
    def register_component(self, name: str, component: Any):
        """Register component with optimized communication"""
        def message_handler(message: Message):
            # Handle incoming message
            logger.debug(f"Component {name} received message: {message.message_type}")
            
            # Process message based on type
            if hasattr(component, 'handle_message'):
                component.handle_message(message)
            elif hasattr(component, 'process_message'):
                component.process_message(message)
        
        self.hub.register_component(name, component, message_handler)
    
    def send_message(self, source: str, target: str, message_type: str, 
                    payload: Any, priority: int = 2) -> bool:
        """Send optimized message"""
        return self.hub.send_message(source, target, message_type, payload, priority)
    
    def get_optimization_report(self) -> Dict[str, Any]:
        """Get comprehensive optimization report"""
        stats = self.hub.get_communication_stats()
        
        # Calculate efficiency metrics
        total_messages = stats['message_stats']['sent'] + stats['message_stats']['received']
        success_rate = ((total_messages - stats['message_stats']['failed']) / max(1, total_messages)) * 100
        
        # Throughput calculation
        avg_bytes_per_message = stats['message_stats']['bytes_transferred'] / max(1, stats['message_stats']['sent'])
        
        return {
            'communication_stats': stats,
            'efficiency_metrics': {
                'success_rate_percent': round(success_rate, 2),
                'average_message_size_bytes': round(avg_bytes_per_message, 2),
                'messages_per_second': total_messages / 60,  # Approximate
                'bandwidth_utilization': 'optimized'
            },
            'optimization_status': 'active' if self.optimization_active else 'inactive'
        }

# Global communication optimizer instance
communication_optimizer = ASISCommunicationOptimizer()

def get_communication_optimizer() -> ASISCommunicationOptimizer:
    """Get global communication optimizer instance"""
    return communication_optimizer
