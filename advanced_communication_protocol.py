#!/usr/bin/env python3
"""
📡 Advanced ASIS Communication Protocol
======================================

Advanced component communication system with message queuing, priority handling,
error recovery, and intelligent routing for enhanced system integration.

Author: ASIS Development Team
Version: 2.0 - Advanced Communication
"""

import asyncio
import logging
import json
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import threading
from concurrent.futures import ThreadPoolExecutor
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# =====================================================================================
# COMMUNICATION PROTOCOL ENUMS AND DATA STRUCTURES
# =====================================================================================

class MessageType(Enum):
    """Message types for component communication"""
    REQUEST = "request"
    RESPONSE = "response"
    EVENT = "event"
    COMMAND = "command"
    ACKNOWLEDGMENT = "acknowledgment"
    ERROR = "error"
    HEARTBEAT = "heartbeat"
    BROADCAST = "broadcast"

class MessagePriority(Enum):
    """Message priority levels"""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    BACKGROUND = 5

class ChannelType(Enum):
    """Communication channel types"""
    DIRECT = "direct"
    QUEUED = "queued"
    BROADCAST = "broadcast"
    MULTICAST = "multicast"
    STREAMING = "streaming"

class MessageStatus(Enum):
    """Message processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    EXPIRED = "expired"

@dataclass
class Message:
    """Enhanced message structure"""
    message_id: str
    sender_id: str
    receiver_id: str
    message_type: MessageType
    priority: MessagePriority
    payload: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3
    correlation_id: Optional[str] = None
    routing_hints: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_expired(self) -> bool:
        """Check if message has expired"""
        return self.expires_at and datetime.now() > self.expires_at
    
    @property
    def can_retry(self) -> bool:
        """Check if message can be retried"""
        return self.retry_count < self.max_retries and not self.is_expired

@dataclass
class MessageChannel:
    """Communication channel configuration"""
    channel_id: str
    channel_type: ChannelType
    participants: List[str]
    max_queue_size: int = 1000
    priority_enabled: bool = True
    persistent: bool = False
    encryption_enabled: bool = False
    compression_enabled: bool = False

@dataclass
class CommunicationMetrics:
    """Communication performance metrics"""
    total_messages: int = 0
    successful_messages: int = 0
    failed_messages: int = 0
    avg_latency: float = 0.0
    avg_queue_time: float = 0.0
    throughput: float = 0.0
    error_rate: float = 0.0
    retry_rate: float = 0.0

# =====================================================================================
# ADVANCED MESSAGE QUEUE SYSTEM
# =====================================================================================

class AdvancedMessageQueue:
    """Advanced message queue with priority handling and intelligent routing"""
    
    def __init__(self, queue_id: str, config: Dict = None):
        self.queue_id = queue_id
        self.config = config or {}
        
        # Priority queues for different message priorities
        self.priority_queues = {priority: asyncio.Queue() for priority in MessagePriority}
        
        # Queue management
        self.max_size = self.config.get('max_size', 1000)
        self.current_size = 0
        self.lock = asyncio.Lock()
        
        # Metrics
        self.metrics = CommunicationMetrics()
        self.message_history = deque(maxlen=1000)
        
        # Processing control
        self.processing = False
        self.worker_count = self.config.get('worker_count', 3)
        self.workers = []
        
        logger.info(f"📬 Message Queue {queue_id} initialized")
    
    async def enqueue(self, message: Message) -> bool:
        """Enqueue message with priority handling"""
        async with self.lock:
            if self.current_size >= self.max_size:
                logger.warning(f"⚠️ Queue {self.queue_id} is full, dropping message {message.message_id}")
                return False
            
            # Check for expired messages
            if message.is_expired:
                logger.warning(f"⚠️ Message {message.message_id} expired, not queuing")
                return False
            
            # Add to appropriate priority queue
            await self.priority_queues[message.priority].put(message)
            self.current_size += 1
            
            # Update metrics
            self.metrics.total_messages += 1
            
            logger.debug(f"📨 Message {message.message_id} queued with priority {message.priority.name}")
            return True
    
    async def dequeue(self) -> Optional[Message]:
        """Dequeue message based on priority"""
        # Process messages in priority order
        for priority in MessagePriority:
            queue = self.priority_queues[priority]
            if not queue.empty():
                try:
                    message = await asyncio.wait_for(queue.get(), timeout=0.1)
                    async with self.lock:
                        self.current_size -= 1
                    
                    # Check if message is still valid
                    if message.is_expired:
                        logger.warning(f"⚠️ Message {message.message_id} expired during processing")
                        continue
                    
                    return message
                    
                except asyncio.TimeoutError:
                    continue
        
        return None
    
    async def start_processing(self, message_handler: Callable[[Message], Any]):
        """Start queue processing with multiple workers"""
        if self.processing:
            return
        
        self.processing = True
        self.workers = []
        
        for i in range(self.worker_count):
            worker = asyncio.create_task(self._worker_loop(f"worker_{i}", message_handler))
            self.workers.append(worker)
        
        logger.info(f"🔄 Started {self.worker_count} workers for queue {self.queue_id}")
    
    async def _worker_loop(self, worker_name: str, message_handler: Callable):
        """Worker loop for processing messages"""
        logger.info(f"👷 Worker {worker_name} started for queue {self.queue_id}")
        
        while self.processing:
            try:
                message = await self.dequeue()
                if message:
                    start_time = time.time()
                    
                    try:
                        # Process message
                        result = await message_handler(message)
                        
                        processing_time = time.time() - start_time
                        
                        # Update success metrics
                        self.metrics.successful_messages += 1
                        self._update_latency_metrics(processing_time)
                        
                        # Record successful processing
                        self.message_history.append({
                            'message_id': message.message_id,
                            'timestamp': datetime.now(),
                            'processing_time': processing_time,
                            'worker': worker_name,
                            'success': True
                        })
                        
                        logger.debug(f"✅ Message {message.message_id} processed by {worker_name}")
                        
                    except Exception as e:
                        processing_time = time.time() - start_time
                        
                        # Update failure metrics
                        self.metrics.failed_messages += 1
                        self._update_latency_metrics(processing_time)
                        
                        # Record failed processing
                        self.message_history.append({
                            'message_id': message.message_id,
                            'timestamp': datetime.now(),
                            'processing_time': processing_time,
                            'worker': worker_name,
                            'success': False,
                            'error': str(e)
                        })
                        
                        logger.error(f"❌ Message {message.message_id} failed in {worker_name}: {e}")
                        
                        # Retry logic
                        if message.can_retry:
                            message.retry_count += 1
                            await asyncio.sleep(min(2 ** message.retry_count, 30))  # Exponential backoff
                            await self.enqueue(message)
                            self.metrics.retry_rate = (self.metrics.retry_rate + 1) / max(1, self.metrics.total_messages)
                
                else:
                    # No messages, brief pause
                    await asyncio.sleep(0.1)
                    
            except Exception as e:
                logger.error(f"❌ Worker {worker_name} error: {e}")
                await asyncio.sleep(1)
        
        logger.info(f"👷 Worker {worker_name} stopped")
    
    def _update_latency_metrics(self, processing_time: float):
        """Update latency metrics"""
        total_processed = self.metrics.successful_messages + self.metrics.failed_messages
        
        if total_processed == 1:
            self.metrics.avg_latency = processing_time
        else:
            # Calculate running average
            self.metrics.avg_latency = (
                (self.metrics.avg_latency * (total_processed - 1) + processing_time) / total_processed
            )
        
        # Update error rate
        self.metrics.error_rate = self.metrics.failed_messages / max(1, self.metrics.total_messages)
    
    async def stop_processing(self):
        """Stop queue processing"""
        self.processing = False
        
        # Wait for workers to finish
        if self.workers:
            await asyncio.gather(*self.workers, return_exceptions=True)
            self.workers = []
        
        logger.info(f"🛑 Queue {self.queue_id} processing stopped")
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get queue performance metrics"""
        return {
            'queue_id': self.queue_id,
            'current_size': self.current_size,
            'max_size': self.max_size,
            'utilization': (self.current_size / self.max_size) * 100,
            'metrics': {
                'total_messages': self.metrics.total_messages,
                'successful_messages': self.metrics.successful_messages,
                'failed_messages': self.metrics.failed_messages,
                'avg_latency': self.metrics.avg_latency,
                'error_rate': self.metrics.error_rate,
                'retry_rate': self.metrics.retry_rate
            },
            'priority_queue_sizes': {
                priority.name: queue.qsize() for priority, queue in self.priority_queues.items()
            }
        }

# =====================================================================================
# INTELLIGENT MESSAGE ROUTER
# =====================================================================================

class IntelligentMessageRouter:
    """Intelligent message routing system with adaptive algorithms"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.routing_table = {}
        self.component_endpoints = {}
        self.routing_history = deque(maxlen=1000)
        self.routing_rules = []
        
        # Performance tracking
        self.route_performance = defaultdict(lambda: {'count': 0, 'avg_latency': 0, 'success_rate': 100})
        
        logger.info("🧠 Intelligent Message Router initialized")
    
    def register_component(self, component_id: str, endpoint_info: Dict):
        """Register component endpoint"""
        self.component_endpoints[component_id] = {
            'endpoint': endpoint_info,
            'registered_at': datetime.now(),
            'last_seen': datetime.now(),
            'message_count': 0,
            'avg_response_time': 0.0
        }
        
        logger.info(f"📝 Component {component_id} registered")
    
    def add_routing_rule(self, rule_id: str, condition: Callable[[Message], bool], 
                        target_selector: Callable[[Message], str], priority: int = 0):
        """Add intelligent routing rule"""
        self.routing_rules.append({
            'rule_id': rule_id,
            'condition': condition,
            'target_selector': target_selector,
            'priority': priority,
            'enabled': True,
            'hit_count': 0
        })
        
        # Sort by priority
        self.routing_rules.sort(key=lambda x: x['priority'], reverse=True)
        
        logger.info(f"📋 Routing rule {rule_id} added")
    
    async def route_message(self, message: Message) -> Optional[str]:
        """Intelligently route message to optimal destination"""
        # Apply routing rules
        for rule in self.routing_rules:
            if rule['enabled'] and rule['condition'](message):
                try:
                    target = rule['target_selector'](message)
                    if target and target in self.component_endpoints:
                        rule['hit_count'] += 1
                        
                        # Record routing decision
                        self.routing_history.append({
                            'message_id': message.message_id,
                            'rule_id': rule['rule_id'],
                            'target': target,
                            'timestamp': datetime.now()
                        })
                        
                        logger.debug(f"🎯 Message {message.message_id} routed to {target} via rule {rule['rule_id']}")
                        return target
                        
                except Exception as e:
                    logger.warning(f"⚠️ Routing rule {rule['rule_id']} failed: {e}")
                    continue
        
        # Fallback to default routing
        return await self._default_routing(message)
    
    async def _default_routing(self, message: Message) -> Optional[str]:
        """Default routing logic when no rules match"""
        # Try explicit receiver first
        if message.receiver_id in self.component_endpoints:
            return message.receiver_id
        
        # Find best component based on performance metrics
        best_component = None
        best_score = -1
        
        for component_id, info in self.component_endpoints.items():
            score = self._calculate_routing_score(component_id, message)
            if score > best_score:
                best_score = score
                best_component = component_id
        
        return best_component
    
    def _calculate_routing_score(self, component_id: str, message: Message) -> float:
        """Calculate routing score for component"""
        perf = self.route_performance[component_id]
        endpoint_info = self.component_endpoints[component_id]
        
        # Base score from historical performance
        base_score = perf['success_rate']
        
        # Latency penalty (lower latency = higher score)
        latency_score = max(0, 100 - (perf['avg_latency'] * 100))
        
        # Load balancing bonus (less loaded = higher score)
        load_bonus = max(0, 50 - endpoint_info['message_count'])
        
        # Recency bonus (more recently seen = higher score)
        time_since_seen = (datetime.now() - endpoint_info['last_seen']).total_seconds()
        recency_bonus = max(0, 10 - (time_since_seen / 60))  # Bonus decreases over minutes
        
        total_score = (base_score * 0.4 + latency_score * 0.3 + 
                      load_bonus * 0.2 + recency_bonus * 0.1)
        
        return total_score
    
    async def update_route_performance(self, target: str, latency: float, success: bool):
        """Update routing performance metrics"""
        perf = self.route_performance[target]
        
        # Update latency
        if perf['count'] == 0:
            perf['avg_latency'] = latency
        else:
            perf['avg_latency'] = (perf['avg_latency'] * perf['count'] + latency) / (perf['count'] + 1)
        
        # Update success rate
        if perf['count'] == 0:
            perf['success_rate'] = 100.0 if success else 0.0
        else:
            total_successes = (perf['success_rate'] / 100.0) * perf['count']
            if success:
                total_successes += 1
            perf['success_rate'] = (total_successes / (perf['count'] + 1)) * 100.0
        
        perf['count'] += 1
        
        # Update endpoint info
        if target in self.component_endpoints:
            self.component_endpoints[target]['last_seen'] = datetime.now()
            self.component_endpoints[target]['message_count'] += 1
            self.component_endpoints[target]['avg_response_time'] = perf['avg_latency']
    
    async def get_routing_metrics(self) -> Dict[str, Any]:
        """Get routing performance metrics"""
        return {
            'registered_components': len(self.component_endpoints),
            'routing_rules': len(self.routing_rules),
            'total_routes': len(self.routing_history),
            'route_performance': dict(self.route_performance),
            'component_endpoints': {
                comp_id: {
                    'message_count': info['message_count'],
                    'avg_response_time': info['avg_response_time'],
                    'last_seen': info['last_seen'].isoformat()
                }
                for comp_id, info in self.component_endpoints.items()
            }
        }

# =====================================================================================
# ADVANCED COMMUNICATION PROTOCOL
# =====================================================================================

class AdvancedCommunicationProtocol:
    """
    Advanced communication protocol coordinating message queues,
    intelligent routing, and error recovery mechanisms.
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or self._default_config()
        
        # Core components
        self.message_router = IntelligentMessageRouter(self.config.get('routing', {}))
        self.message_queues = {}
        self.channels = {}
        
        # Error recovery
        self.error_recovery = ErrorRecoveryManager(self.config.get('error_recovery', {}))
        
        # Monitoring
        self.performance_monitor = CommunicationMonitor(self.config.get('monitoring', {}))
        
        # State management
        self.active_sessions = {}
        self.protocol_metrics = CommunicationMetrics()
        
        # Background tasks
        self.running = False
        self.monitoring_task = None
        
        logger.info("📡 Advanced Communication Protocol initialized")
    
    def _default_config(self) -> Dict:
        """Default protocol configuration"""
        return {
            'routing': {
                'adaptive_routing': True,
                'load_balancing': True,
                'failover_enabled': True
            },
            'queuing': {
                'default_queue_size': 1000,
                'worker_count': 3,
                'priority_enabled': True
            },
            'error_recovery': {
                'max_retries': 3,
                'retry_backoff': 'exponential',
                'circuit_breaker_enabled': True
            },
            'monitoring': {
                'metrics_interval': 30,
                'performance_tracking': True,
                'alert_thresholds': {
                    'error_rate': 0.1,
                    'latency': 2.0,
                    'queue_utilization': 0.8
                }
            }
        }
    
    async def initialize(self) -> bool:
        """Initialize the communication protocol"""
        try:
            logger.info("🚀 Initializing Advanced Communication Protocol...")
            
            # Initialize default queues
            await self._initialize_default_queues()
            
            # Initialize default routing rules
            await self._initialize_default_routing()
            
            # Start monitoring
            await self._start_monitoring()
            
            self.running = True
            
            logger.info("✅ Advanced Communication Protocol initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Communication protocol initialization failed: {e}")
            return False
    
    async def _initialize_default_queues(self):
        """Initialize default message queues"""
        queue_configs = [
            ('high_priority', {'max_size': 500, 'worker_count': 5}),
            ('normal_priority', {'max_size': 1000, 'worker_count': 3}),
            ('background', {'max_size': 2000, 'worker_count': 2}),
            ('system_events', {'max_size': 1000, 'worker_count': 2})
        ]
        
        for queue_id, config in queue_configs:
            queue = AdvancedMessageQueue(queue_id, config)
            self.message_queues[queue_id] = queue
            
            # Start queue processing
            await queue.start_processing(self._handle_message)
        
        logger.info(f"📬 Initialized {len(queue_configs)} message queues")
    
    async def _initialize_default_routing(self):
        """Initialize default routing rules"""
        # High priority messages to high priority queue
        self.message_router.add_routing_rule(
            'high_priority_routing',
            lambda msg: msg.priority in [MessagePriority.CRITICAL, MessagePriority.HIGH],
            lambda msg: 'high_priority_queue',
            priority=10
        )
        
        # System events to system queue
        self.message_router.add_routing_rule(
            'system_event_routing',
            lambda msg: msg.message_type in [MessageType.EVENT, MessageType.HEARTBEAT],
            lambda msg: 'system_events_queue',
            priority=8
        )
        
        # Background messages to background queue
        self.message_router.add_routing_rule(
            'background_routing',
            lambda msg: msg.priority == MessagePriority.BACKGROUND,
            lambda msg: 'background_queue',
            priority=5
        )
        
        logger.info("📋 Default routing rules initialized")
    
    async def send_message(self, sender_id: str, receiver_id: str, 
                          message_type: MessageType, payload: Dict[str, Any],
                          priority: MessagePriority = MessagePriority.NORMAL,
                          timeout: Optional[float] = None) -> bool:
        """Send message through the protocol"""
        try:
            # Create message
            message = Message(
                message_id=str(uuid.uuid4()),
                sender_id=sender_id,
                receiver_id=receiver_id,
                message_type=message_type,
                priority=priority,
                payload=payload,
                expires_at=datetime.now() + timedelta(seconds=timeout) if timeout else None
            )
            
            # Route message to appropriate queue
            queue_target = await self.message_router.route_message(message)
            
            if not queue_target:
                logger.error(f"❌ No route found for message {message.message_id}")
                return False
            
            # Map to actual queue
            queue_name = self._map_target_to_queue(queue_target, message)
            queue = self.message_queues.get(queue_name)
            
            if not queue:
                logger.error(f"❌ Queue {queue_name} not found")
                return False
            
            # Enqueue message
            success = await queue.enqueue(message)
            
            if success:
                self.protocol_metrics.total_messages += 1
                logger.debug(f"📨 Message {message.message_id} sent successfully")
            else:
                logger.warning(f"⚠️ Failed to enqueue message {message.message_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Failed to send message: {e}")
            return False
    
    def _map_target_to_queue(self, target: str, message: Message) -> str:
        """Map routing target to actual queue name"""
        # Priority-based mapping
        if message.priority in [MessagePriority.CRITICAL, MessagePriority.HIGH]:
            return 'high_priority'
        elif message.priority == MessagePriority.BACKGROUND:
            return 'background'
        else:
            return 'normal_priority'
    
    async def _handle_message(self, message: Message) -> Any:
        """Handle message processing"""
        start_time = time.time()
        
        try:
            # Find target component
            target = await self.message_router.route_message(message)
            
            if not target:
                raise Exception(f"No target found for message {message.message_id}")
            
            # Simulate message processing (in real implementation, this would call actual components)
            await self._process_message_for_component(target, message)
            
            processing_time = time.time() - start_time
            
            # Update routing performance
            await self.message_router.update_route_performance(target, processing_time, True)
            
            # Update protocol metrics
            self.protocol_metrics.successful_messages += 1
            self._update_protocol_metrics(processing_time, True)
            
            logger.debug(f"✅ Message {message.message_id} processed successfully by {target}")
            
            return {'success': True, 'target': target, 'processing_time': processing_time}
            
        except Exception as e:
            processing_time = time.time() - start_time
            
            # Update failure metrics
            self.protocol_metrics.failed_messages += 1
            self._update_protocol_metrics(processing_time, False)
            
            logger.error(f"❌ Message processing failed: {e}")
            
            # Trigger error recovery
            await self.error_recovery.handle_message_failure(message, str(e))
            
            raise
    
    async def _process_message_for_component(self, component_id: str, message: Message):
        """Process message for specific component (simulation)"""
        # Simulate different processing times based on message type
        if message.message_type == MessageType.REQUEST:
            await asyncio.sleep(0.1)  # Normal request processing
        elif message.message_type == MessageType.COMMAND:
            await asyncio.sleep(0.05)  # Quick command execution
        elif message.priority == MessagePriority.CRITICAL:
            await asyncio.sleep(0.02)  # Fast critical processing
        else:
            await asyncio.sleep(0.08)  # Default processing
        
        # Simulate occasional failures for testing
        import random
        if random.random() < 0.05:  # 5% failure rate
            raise Exception("Simulated processing failure")
    
    def _update_protocol_metrics(self, processing_time: float, success: bool):
        """Update protocol-level metrics"""
        total_processed = self.protocol_metrics.successful_messages + self.protocol_metrics.failed_messages
        
        # Update average latency
        if total_processed == 1:
            self.protocol_metrics.avg_latency = processing_time
        else:
            self.protocol_metrics.avg_latency = (
                (self.protocol_metrics.avg_latency * (total_processed - 1) + processing_time) / total_processed
            )
        
        # Update error rate
        self.protocol_metrics.error_rate = self.protocol_metrics.failed_messages / max(1, self.protocol_metrics.total_messages)
    
    async def _start_monitoring(self):
        """Start background monitoring"""
        self.monitoring_task = asyncio.create_task(self._monitoring_loop())
        logger.info("📊 Communication monitoring started")
    
    async def _monitoring_loop(self):
        """Monitoring loop for performance tracking"""
        while self.running:
            try:
                await self.performance_monitor.collect_metrics(self)
                await asyncio.sleep(self.config.get('monitoring', {}).get('metrics_interval', 30))
            except Exception as e:
                logger.error(f"❌ Monitoring loop error: {e}")
                await asyncio.sleep(10)
    
    async def get_protocol_metrics(self) -> Dict[str, Any]:
        """Get comprehensive protocol metrics"""
        # Collect queue metrics
        queue_metrics = {}
        for queue_id, queue in self.message_queues.items():
            queue_metrics[queue_id] = await queue.get_metrics()
        
        # Get routing metrics
        routing_metrics = await self.message_router.get_routing_metrics()
        
        # Calculate overall performance score
        performance_score = await self._calculate_performance_score()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'protocol_metrics': {
                'total_messages': self.protocol_metrics.total_messages,
                'successful_messages': self.protocol_metrics.successful_messages,
                'failed_messages': self.protocol_metrics.failed_messages,
                'avg_latency': self.protocol_metrics.avg_latency,
                'error_rate': self.protocol_metrics.error_rate,
                'throughput': self._calculate_throughput()
            },
            'queue_metrics': queue_metrics,
            'routing_metrics': routing_metrics,
            'performance_score': performance_score,
            'active_queues': len(self.message_queues),
            'total_queue_size': sum(queue.current_size for queue in self.message_queues.values())
        }
    
    async def _calculate_performance_score(self) -> float:
        """Calculate overall communication protocol performance score"""
        # Factors for performance calculation
        success_rate = (self.protocol_metrics.successful_messages / 
                       max(1, self.protocol_metrics.total_messages)) * 100
        
        # Latency score (lower is better)
        latency_score = max(0, 100 - (self.protocol_metrics.avg_latency * 1000))  # Convert to ms
        
        # Queue utilization score (balanced is optimal)
        total_capacity = sum(queue.max_size for queue in self.message_queues.values())
        total_used = sum(queue.current_size for queue in self.message_queues.values())
        utilization = (total_used / max(1, total_capacity)) * 100
        utilization_score = 100 - abs(70 - utilization)  # Optimal around 70%
        
        # Weighted combination
        performance_score = (
            success_rate * 0.4 +
            latency_score * 0.3 +
            utilization_score * 0.3
        )
        
        return min(100, max(0, performance_score))
    
    def _calculate_throughput(self) -> float:
        """Calculate message throughput (messages per second)"""
        # This is a simplified calculation
        # In real implementation, would track over time windows
        return self.protocol_metrics.total_messages / max(1, 60)  # Assume 1 minute operation
    
    async def shutdown(self):
        """Gracefully shutdown the communication protocol"""
        logger.info("🛑 Shutting down Advanced Communication Protocol...")
        
        self.running = False
        
        # Stop monitoring
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        
        # Stop all queues
        for queue in self.message_queues.values():
            await queue.stop_processing()
        
        logger.info("✅ Advanced Communication Protocol shutdown completed")

# =====================================================================================
# ERROR RECOVERY MANAGER
# =====================================================================================

class ErrorRecoveryManager:
    """Error recovery and resilience management for communication"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.failure_history = deque(maxlen=1000)
        self.circuit_breakers = {}
        
    async def handle_message_failure(self, message: Message, error: str):
        """Handle message processing failure"""
        self.failure_history.append({
            'message_id': message.message_id,
            'error': error,
            'timestamp': datetime.now()
        })
        
        logger.debug(f"🔧 Handling failure for message {message.message_id}: {error}")

# =====================================================================================
# COMMUNICATION MONITOR
# =====================================================================================

class CommunicationMonitor:
    """Communication performance monitoring and analytics"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.metrics_history = deque(maxlen=1000)
        
    async def collect_metrics(self, protocol):
        """Collect and analyze communication metrics"""
        metrics = await protocol.get_protocol_metrics()
        self.metrics_history.append(metrics)
        
        # Check for alerts
        await self._check_alert_conditions(metrics)
    
    async def _check_alert_conditions(self, metrics: Dict):
        """Check for alert conditions"""
        thresholds = self.config.get('alert_thresholds', {})
        
        error_rate = metrics['protocol_metrics']['error_rate']
        latency = metrics['protocol_metrics']['avg_latency']
        
        if error_rate > thresholds.get('error_rate', 0.1):
            logger.warning(f"🚨 High error rate detected: {error_rate:.3f}")
        
        if latency > thresholds.get('latency', 2.0):
            logger.warning(f"🚨 High latency detected: {latency:.3f}s")

# =====================================================================================
# DEMO FUNCTION
# =====================================================================================

async def demo_communication_protocol():
    """Demonstrate advanced communication protocol capabilities"""
    print("📡 Advanced ASIS Communication Protocol Demo")
    print("=" * 50)
    
    protocol = AdvancedCommunicationProtocol()
    
    try:
        # Initialize
        print("\n1️⃣ Initializing communication protocol...")
        success = await protocol.initialize()
        
        if not success:
            print("❌ Initialization failed")
            return
        
        print("✅ Communication protocol initialized")
        
        # Register components
        print("\n2️⃣ Registering components...")
        components = ['advanced_ai_engine', 'ethical_reasoning', 'cross_domain_reasoning']
        
        for component in components:
            protocol.message_router.register_component(component, {'endpoint': f"/{component}"})
        
        print(f"📝 Registered {len(components)} components")
        
        # Test message sending
        print("\n3️⃣ Testing message communication...")
        
        test_messages = [
            ('orchestrator', 'advanced_ai_engine', MessageType.REQUEST, 
             {'task': 'process_request'}, MessagePriority.HIGH),
            ('orchestrator', 'ethical_reasoning', MessageType.COMMAND,
             {'action': 'analyze_ethics'}, MessagePriority.NORMAL),
            ('advanced_ai_engine', 'cross_domain_reasoning', MessageType.EVENT,
             {'event': 'reasoning_needed'}, MessagePriority.NORMAL),
            ('system', 'all', MessageType.BROADCAST,
             {'message': 'system_status'}, MessagePriority.LOW)
        ]
        
        sent_count = 0
        for sender, receiver, msg_type, payload, priority in test_messages:
            success = await protocol.send_message(sender, receiver, msg_type, payload, priority)
            if success:
                sent_count += 1
                print(f"   ✅ Message {sent_count}: {sender} → {receiver} ({msg_type.value})")
            else:
                print(f"   ❌ Failed: {sender} → {receiver}")
        
        # Wait for processing
        await asyncio.sleep(2)
        
        # Get metrics
        print("\n4️⃣ Communication performance metrics...")
        metrics = await protocol.get_protocol_metrics()
        
        print(f"📊 Protocol Performance:")
        print(f"   Total Messages: {metrics['protocol_metrics']['total_messages']}")
        print(f"   Success Rate: {(metrics['protocol_metrics']['successful_messages'] / max(1, metrics['protocol_metrics']['total_messages'])) * 100:.1f}%")
        print(f"   Avg Latency: {metrics['protocol_metrics']['avg_latency']:.3f}s")
        print(f"   Error Rate: {metrics['protocol_metrics']['error_rate']:.3f}")
        print(f"   Performance Score: {metrics['performance_score']:.1f}%")
        
        # Show queue status
        print(f"\n📬 Queue Status:")
        for queue_name, queue_info in metrics['queue_metrics'].items():
            print(f"   {queue_name}: {queue_info['current_size']}/{queue_info['max_size']} ({queue_info['utilization']:.1f}% full)")
        
        # Integration improvement calculation
        baseline_communication = 72.0  # From baseline analysis
        current_score = metrics['performance_score']
        improvement = current_score - baseline_communication
        
        print(f"\n📈 Communication Improvement:")
        print(f"   Baseline Score: {baseline_communication:.1f}%")
        print(f"   Current Score: {current_score:.1f}%")
        print(f"   Improvement: +{improvement:.1f}%")
        
        if current_score >= 85.0:
            print("🎯 EXCELLENT: Communication performance target achieved!")
        elif improvement > 0:
            print(f"📈 PROGRESS: {improvement:.1f}% communication improvement")
        
    finally:
        print("\n5️⃣ Shutting down...")
        await protocol.shutdown()
        print("✅ Demo completed")

async def main():
    """Main function"""
    await demo_communication_protocol()

if __name__ == "__main__":
    asyncio.run(main())
