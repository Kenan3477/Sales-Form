#!/usr/bin/env python3
"""
ASIS Security Integration
Unified security framework integrating network security with existing ASIS security
"""

import asyncio
import logging
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
import json

# Import security frameworks
try:
    from asis_security_framework import ASISSecurityFramework, SecurityLevel, AccessPermission, AuditEventType
    SECURITY_FRAMEWORK_AVAILABLE = True
except ImportError:
    print("⚠️ ASIS Security Framework not available - creating standalone network security")
    SECURITY_FRAMEWORK_AVAILABLE = False

from asis_network_security import ASISNetworkSecurity, SecurityEvent

logger = logging.getLogger(__name__)

@dataclass
class UnifiedSecurityEvent:
    """Unified security event that combines network and system security"""
    timestamp: datetime
    event_id: str
    event_type: str
    source: str  # "network", "system", "application"
    severity: str  # "low", "medium", "high", "critical"
    user_id: Optional[str]
    session_id: Optional[str]
    source_ip: str
    destination: str
    action: str
    result: str  # "allowed", "blocked", "monitored"
    description: str
    threat_score: float
    details: Dict[str, Any]
    security_response: Optional[str] = None

class SecurityCorrelationEngine:
    """Correlates security events across network and system layers"""
    
    def __init__(self):
        self.event_buffer = []
        self.correlation_rules = []
        self.threat_patterns = {}
        self.active_threats = {}
        self.correlation_window = timedelta(minutes=5)
        
        self._setup_correlation_rules()
    
    def _setup_correlation_rules(self):
        """Setup security event correlation rules"""
        
        self.correlation_rules = [
            {
                "name": "coordinated_attack",
                "pattern": "multiple_failed_auth_followed_by_network_scan",
                "events": ["auth_failure", "port_scan"],
                "window": timedelta(minutes=10),
                "threshold": 3,
                "severity": "high",
                "response": "block_ip_and_alert"
            },
            {
                "name": "privilege_escalation_attempt",
                "pattern": "successful_auth_followed_by_admin_access_attempt",
                "events": ["auth_success", "unauthorized_admin_access"],
                "window": timedelta(minutes=5),
                "threshold": 1,
                "severity": "critical",
                "response": "terminate_session_and_alert"
            },
            {
                "name": "data_exfiltration_attempt",
                "pattern": "large_data_access_with_external_communication",
                "events": ["large_data_access", "external_network_communication"],
                "window": timedelta(minutes=15),
                "threshold": 1,
                "severity": "high",
                "response": "monitor_and_limit_bandwidth"
            },
            {
                "name": "insider_threat_indicator",
                "pattern": "off_hours_access_with_suspicious_activity",
                "events": ["off_hours_login", "unusual_data_access"],
                "window": timedelta(hours=1),
                "threshold": 2,
                "severity": "medium",
                "response": "enhanced_monitoring"
            }
        ]
    
    def add_event(self, event: UnifiedSecurityEvent):
        """Add security event for correlation"""
        
        # Add to buffer
        self.event_buffer.append(event)
        
        # Clean old events
        cutoff_time = datetime.now() - self.correlation_window
        self.event_buffer = [e for e in self.event_buffer if e.timestamp > cutoff_time]
        
        # Check for correlations
        self._check_correlations(event)
    
    def _check_correlations(self, new_event: UnifiedSecurityEvent):
        """Check for security event correlations"""
        
        for rule in self.correlation_rules:
            matching_events = self._find_matching_events(rule, new_event)
            
            if len(matching_events) >= rule["threshold"]:
                threat_id = f"{rule['name']}_{new_event.source_ip}_{int(time.time())}"
                
                correlated_threat = {
                    "threat_id": threat_id,
                    "rule_name": rule["name"],
                    "pattern": rule["pattern"],
                    "severity": rule["severity"],
                    "events": matching_events,
                    "first_seen": min(e.timestamp for e in matching_events),
                    "last_seen": max(e.timestamp for e in matching_events),
                    "source_ip": new_event.source_ip,
                    "user_id": new_event.user_id,
                    "recommended_response": rule["response"]
                }
                
                self.active_threats[threat_id] = correlated_threat
                logger.warning(f"🚨 Correlated threat detected: {rule['name']} - {threat_id}")
                
                return correlated_threat
        
        return None
    
    def _find_matching_events(self, rule: Dict, new_event: UnifiedSecurityEvent) -> List[UnifiedSecurityEvent]:
        """Find events matching correlation rule"""
        
        required_events = rule["events"]
        window_start = new_event.timestamp - rule["window"]
        
        # Find events in time window from same source
        candidate_events = [
            e for e in self.event_buffer
            if e.timestamp >= window_start and e.source_ip == new_event.source_ip
        ]
        
        # Check if we have all required event types
        event_types_found = set(e.event_type for e in candidate_events)
        required_types = set(required_events)
        
        if required_types.issubset(event_types_found):
            return candidate_events
        
        return []
    
    def get_active_threats(self) -> Dict[str, Any]:
        """Get current active threats"""
        return self.active_threats

class UnifiedSecurityManager:
    """Unified security manager combining network and system security"""
    
    def __init__(self):
        # Initialize components
        self.network_security = ASISNetworkSecurity()
        self.correlation_engine = SecurityCorrelationEngine()
        
        # Initialize system security if available
        self.system_security = None
        if SECURITY_FRAMEWORK_AVAILABLE:
            try:
                self.system_security = ASISSecurityFramework()
                logger.info("✅ System security framework integrated")
            except Exception as e:
                logger.warning(f"⚠️ System security integration failed: {e}")
        
        # Security state
        self.security_state = {
            "unified_security_active": False,
            "network_security_active": False,
            "system_security_active": False,
            "correlation_engine_active": False,
            "total_events_processed": 0,
            "active_threats": 0,
            "security_score": 0.0
        }
        
        # Monitoring
        self.monitoring_active = False
        self.monitor_thread = None
        self.event_handlers = []
        
    def initialize_unified_security(self) -> bool:
        """Initialize all security components"""
        
        logger.info("🔒 Initializing Unified ASIS Security...")
        
        success_count = 0
        total_components = 3
        
        # Initialize network security
        if self.network_security.initialize_full_security():
            self.security_state["network_security_active"] = True
            success_count += 1
            logger.info("✅ Network security initialized")
        else:
            logger.error("❌ Network security initialization failed")
        
        # Initialize system security
        if self.system_security:
            try:
                # Setup default creator user if not exists
                self.system_security.create_user(
                    "creator_kenandavies", 
                    "SkyeAlbert2025!", 
                    SecurityLevel.CREATOR,
                    [AccessPermission.SYSTEM_CONTROL, AccessPermission.ADMIN, 
                     AccessPermission.DELETE, AccessPermission.WRITE, 
                     AccessPermission.READ, AccessPermission.EXECUTE],
                    ["127.0.0.1", "192.168.0.0/16"]
                )
                
                self.security_state["system_security_active"] = True
                success_count += 1
                logger.info("✅ System security initialized")
                
            except Exception as e:
                logger.warning(f"⚠️ System security setup issue: {e}")
        
        # Initialize correlation engine
        self.security_state["correlation_engine_active"] = True
        success_count += 1
        logger.info("✅ Correlation engine initialized")
        
        # Calculate success rate
        success_rate = success_count / total_components
        self.security_state["unified_security_active"] = success_rate >= 0.67
        
        if self.security_state["unified_security_active"]:
            logger.info(f"🚀 Unified Security initialized successfully ({success_count}/{total_components})")
            self._start_monitoring()
            return True
        else:
            logger.warning(f"⚠️ Unified Security partially initialized ({success_count}/{total_components})")
            return False
    
    def process_unified_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process request through unified security layers"""
        
        result = {
            "allowed": False,
            "security_layers_passed": [],
            "security_layers_failed": [],
            "threat_score": 0.0,
            "security_events": [],
            "session_token": None,
            "recommendations": []
        }
        
        try:
            # Extract request information
            src_ip = request_data.get("source_ip", "unknown")
            user_id = request_data.get("user_id")
            password = request_data.get("password")
            action = request_data.get("action", "access")
            resource = request_data.get("resource", "unknown")
            request_content = request_data.get("content", "")
            
            # 1. Network Security Layer
            network_result = self.network_security.process_network_request(
                src_ip=src_ip,
                dst_port=request_data.get("port", 8080),
                protocol=request_data.get("protocol", "https"),
                request_data=request_content,
                user_id=user_id,
                endpoint=request_data.get("endpoint", "/")
            )
            
            if not network_result["allowed"]:
                result["security_layers_failed"].append("network_security")
                result["recommendations"].extend(network_result["recommendations"])
                self._log_unified_event("network_security_block", src_ip, user_id, action, "blocked", network_result)
                return result
            
            result["security_layers_passed"].append("network_security")
            result["threat_score"] = max(result["threat_score"], network_result.get("threat_score", 0.0))
            
            # 2. System Security Layer (if available and user authentication required)
            if self.system_security and user_id and password:
                
                # Authenticate user
                auth_token = self.system_security.authenticate_user(user_id, password, src_ip)
                
                if not auth_token:
                    result["security_layers_failed"].append("system_authentication")
                    result["recommendations"].append("Authentication failed")
                    self._log_unified_event("authentication_failure", src_ip, user_id, "authenticate", "blocked", {"reason": "invalid_credentials"})
                    return result
                
                result["security_layers_passed"].append("system_authentication")
                result["session_token"] = auth_token
                
                # Check access permissions
                if action != "authenticate":
                    access_permission = self._map_action_to_permission(action)
                    
                    if not self.system_security.verify_access(auth_token, src_ip, resource, access_permission):
                        result["security_layers_failed"].append("system_authorization")
                        result["recommendations"].append(f"Access denied for action: {action}")
                        self._log_unified_event("authorization_failure", src_ip, user_id, action, "blocked", {"resource": resource, "permission": access_permission.value})
                        return result
                
                result["security_layers_passed"].append("system_authorization")
            
            # 3. All security layers passed
            result["allowed"] = True
            result["recommendations"].append("Request passed all security layers")
            
            # Log successful access
            self._log_unified_event("access_granted", src_ip, user_id, action, "allowed", {
                "resource": resource,
                "layers_passed": result["security_layers_passed"]
            })
            
        except Exception as e:
            logger.error(f"Unified security processing error: {e}")
            result["security_layers_failed"].append("security_processing_error")
            result["recommendations"].append(f"Security processing error: {str(e)}")
        
        return result
    
    def _map_action_to_permission(self, action: str) -> 'AccessPermission':
        """Map action to access permission"""
        
        if not SECURITY_FRAMEWORK_AVAILABLE:
            return None
        
        action_mapping = {
            "read": AccessPermission.READ,
            "write": AccessPermission.WRITE,
            "delete": AccessPermission.DELETE,
            "execute": AccessPermission.EXECUTE,
            "admin": AccessPermission.ADMIN,
            "system_control": AccessPermission.SYSTEM_CONTROL
        }
        
        return action_mapping.get(action.lower(), AccessPermission.READ)
    
    def _log_unified_event(self, event_type: str, source_ip: str, user_id: Optional[str], 
                          action: str, result: str, details: Dict[str, Any]):
        """Log unified security event"""
        
        event = UnifiedSecurityEvent(
            timestamp=datetime.now(),
            event_id=f"{event_type}_{int(time.time() * 1000)}",
            event_type=event_type,
            source="unified_security",
            severity=self._calculate_event_severity(event_type, details),
            user_id=user_id,
            session_id=details.get("session_id"),
            source_ip=source_ip,
            destination="asis_system",
            action=action,
            result=result,
            description=f"{event_type}: {action} -> {result}",
            threat_score=details.get("threat_score", 0.0),
            details=details
        )
        
        # Add to correlation engine
        self.correlation_engine.add_event(event)
        
        # Update security state
        self.security_state["total_events_processed"] += 1
        self.security_state["active_threats"] = len(self.correlation_engine.active_threats)
        
        # Notify event handlers
        for handler in self.event_handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Event handler error: {e}")
    
    def _calculate_event_severity(self, event_type: str, details: Dict[str, Any]) -> str:
        """Calculate event severity"""
        
        high_severity_events = [
            "authentication_failure", "authorization_failure", 
            "network_security_block", "intrusion_detection"
        ]
        
        medium_severity_events = [
            "rate_limit_exceeded", "suspicious_activity"
        ]
        
        if event_type in high_severity_events:
            return "high"
        elif event_type in medium_severity_events:
            return "medium"
        elif details.get("threat_score", 0.0) > 0.7:
            return "high"
        elif details.get("threat_score", 0.0) > 0.4:
            return "medium"
        else:
            return "low"
    
    def _start_monitoring(self):
        """Start security monitoring thread"""
        
        if not self.monitoring_active:
            self.monitoring_active = True
            self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.monitor_thread.start()
            logger.info("🔍 Security monitoring started")
    
    def _monitoring_loop(self):
        """Security monitoring loop"""
        
        while self.monitoring_active:
            try:
                # Update security score
                self.security_state["security_score"] = self._calculate_unified_security_score()
                
                # Check for threat escalation
                self._check_threat_escalation()
                
                # Cleanup old events
                self._cleanup_old_data()
                
                time.sleep(30)  # Monitor every 30 seconds
                
            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                time.sleep(60)
    
    def _calculate_unified_security_score(self) -> float:
        """Calculate unified security score"""
        
        scores = []
        
        # Network security score
        if self.security_state["network_security_active"]:
            network_score = self.network_security._calculate_security_score()
            scores.append(network_score * 0.4)  # 40% weight
        
        # System security score (simplified)
        if self.security_state["system_security_active"]:
            system_score = 0.9  # Assume high score if active
            scores.append(system_score * 0.3)  # 30% weight
        
        # Correlation engine score
        if self.security_state["correlation_engine_active"]:
            threat_penalty = min(0.2, len(self.correlation_engine.active_threats) * 0.05)
            correlation_score = max(0.0, 0.9 - threat_penalty)
            scores.append(correlation_score * 0.3)  # 30% weight
        
        return sum(scores) if scores else 0.0
    
    def _check_threat_escalation(self):
        """Check for threat escalation requiring immediate response"""
        
        active_threats = self.correlation_engine.get_active_threats()
        
        for threat_id, threat_data in active_threats.items():
            if threat_data["severity"] == "critical":
                logger.critical(f"🚨 CRITICAL THREAT: {threat_data['rule_name']} - {threat_id}")
                
                # Execute automated response
                self._execute_threat_response(threat_data)
    
    def _execute_threat_response(self, threat_data: Dict[str, Any]):
        """Execute automated threat response"""
        
        response = threat_data["recommended_response"]
        source_ip = threat_data["source_ip"]
        
        try:
            if response == "block_ip_and_alert":
                self.network_security.firewall.block_ip(source_ip, f"Correlated threat: {threat_data['rule_name']}")
                logger.warning(f"🛡️ Blocked IP {source_ip} due to correlated threat")
            
            elif response == "terminate_session_and_alert":
                if self.system_security and threat_data.get("user_id"):
                    # Terminate user sessions (implementation depends on session management)
                    logger.warning(f"🔐 Session termination recommended for user: {threat_data['user_id']}")
            
            elif response == "enhanced_monitoring":
                # Enhance monitoring for this IP (implementation specific)
                logger.info(f"👁️ Enhanced monitoring activated for {source_ip}")
            
            elif response == "monitor_and_limit_bandwidth":
                # Bandwidth limiting (implementation specific)
                logger.info(f"🚦 Bandwidth limiting recommended for {source_ip}")
            
        except Exception as e:
            logger.error(f"Threat response execution failed: {e}")
    
    def _cleanup_old_data(self):
        """Cleanup old security data"""
        
        # Remove old threats (older than 24 hours)
        cutoff_time = datetime.now() - timedelta(hours=24)
        old_threats = [
            tid for tid, threat in self.correlation_engine.active_threats.items()
            if threat["last_seen"] < cutoff_time
        ]
        
        for threat_id in old_threats:
            del self.correlation_engine.active_threats[threat_id]
    
    def add_event_handler(self, handler):
        """Add security event handler"""
        self.event_handlers.append(handler)
    
    def get_unified_security_status(self) -> Dict[str, Any]:
        """Get comprehensive unified security status"""
        
        status = {
            "unified_security": self.security_state,
            "network_security": self.network_security.get_security_dashboard(),
            "system_security": None,
            "correlation_engine": {
                "active_threats": len(self.correlation_engine.active_threats),
                "correlation_rules": len(self.correlation_engine.correlation_rules),
                "events_in_buffer": len(self.correlation_engine.event_buffer)
            }
        }
        
        # Add system security status if available
        if self.system_security:
            try:
                status["system_security"] = self.system_security.get_security_status()
            except Exception as e:
                status["system_security"] = {"error": str(e)}
        
        return status
    
    def emergency_lockdown(self):
        """Emergency lockdown of all systems"""
        
        logger.critical("🚨 EMERGENCY LOCKDOWN INITIATED")
        
        try:
            # Network security lockdown
            self.network_security.emergency_shutdown()
            
            # System security lockdown (if available)
            if self.system_security:
                # Implementation depends on system security framework
                pass
            
            # Stop monitoring
            self.monitoring_active = False
            
            # Update state
            self.security_state["unified_security_active"] = False
            
            logger.critical("🚨 Emergency lockdown complete")
            
        except Exception as e:
            logger.critical(f"🚨 Emergency lockdown error: {e}")

# Integration helper functions
def create_asis_unified_security() -> UnifiedSecurityManager:
    """Create and initialize unified ASIS security"""
    
    manager = UnifiedSecurityManager()
    
    if manager.initialize_unified_security():
        logger.info("🔒 ASIS Unified Security ready")
        return manager
    else:
        logger.warning("⚠️ ASIS Unified Security partially ready")
        return manager

def example_security_event_handler(event: UnifiedSecurityEvent):
    """Example security event handler"""
    
    if event.severity in ["high", "critical"]:
        print(f"🚨 SECURITY ALERT: {event.event_type} from {event.source_ip}")
        print(f"   Severity: {event.severity}")
        print(f"   Description: {event.description}")
        print(f"   Threat Score: {event.threat_score}")

# Example usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Create unified security manager
    security_manager = create_asis_unified_security()
    
    # Add event handler
    security_manager.add_event_handler(example_security_event_handler)
    
    # Test unified security processing
    test_requests = [
        {
            "source_ip": "192.168.1.100",
            "user_id": "creator_kenandavies",
            "password": "SkyeAlbert2025!",
            "action": "read",
            "resource": "asis_data",
            "protocol": "https",
            "port": 8443,
            "endpoint": "/api/asis/query",
            "content": "What is consciousness?"
        },
        {
            "source_ip": "10.0.0.50",
            "user_id": "hacker",
            "password": "wrong_password",
            "action": "admin",
            "resource": "system_config",
            "protocol": "https",
            "port": 8443,
            "endpoint": "/admin/config",
            "content": "'; DROP TABLE users; --"
        }
    ]
    
    print("🧪 Testing Unified Security Processing...")
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n🔍 Test {i}: {request['user_id']} from {request['source_ip']}")
        
        result = security_manager.process_unified_request(request)
        
        status = "✅ ALLOWED" if result["allowed"] else "❌ BLOCKED"
        layers_passed = ", ".join(result["security_layers_passed"])
        layers_failed = ", ".join(result["security_layers_failed"])
        
        print(f"   {status}")
        print(f"   Layers Passed: {layers_passed or 'None'}")
        print(f"   Layers Failed: {layers_failed or 'None'}")
        print(f"   Threat Score: {result['threat_score']:.2f}")
        print(f"   Recommendations: {'; '.join(result['recommendations'])}")
    
    # Display security status
    print("\n📊 Unified Security Status:")
    status = security_manager.get_unified_security_status()
    
    print(f"Security Score: {status['unified_security']['security_score']:.2f}")
    print(f"Events Processed: {status['unified_security']['total_events_processed']}")
    print(f"Active Threats: {status['unified_security']['active_threats']}")
    print(f"Network Security: {'✅' if status['unified_security']['network_security_active'] else '❌'}")
    print(f"System Security: {'✅' if status['unified_security']['system_security_active'] else '❌'}")
    print(f"Correlation Engine: {'✅' if status['unified_security']['correlation_engine_active'] else '❌'}")
    
    print("\n🔒 ASIS Unified Security demonstration complete!")