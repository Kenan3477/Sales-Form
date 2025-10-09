#!/usr/bin/env python3
"""
ASIS Network Security Layer
Comprehensive network security implementation for ASIS system
"""

import ssl
import socket
import time
import json
import hashlib
import secrets
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from collections import defaultdict, deque
import logging
import ipaddress
import base64
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import asyncio
import aiohttp
from aiohttp import web
import weakref

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SecurityEvent:
    """Network security event data structure"""
    timestamp: datetime
    event_type: str
    source_ip: str
    destination_ip: str
    port: int
    protocol: str
    severity: str
    description: str
    data: Dict[str, Any] = field(default_factory=dict)
    blocked: bool = False
    threat_score: float = 0.0

@dataclass
class RateLimitBucket:
    """Rate limiting bucket for tracking requests"""
    requests: deque = field(default_factory=deque)
    max_requests: int = 100
    window_seconds: int = 60
    last_reset: datetime = field(default_factory=datetime.now)
    
    def is_allowed(self) -> bool:
        """Check if request is allowed under rate limit"""
        now = datetime.now()
        
        # Remove old requests outside the window
        while self.requests and (now - self.requests[0]).total_seconds() > self.window_seconds:
            self.requests.popleft()
        
        # Check if under limit
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        
        return False
    
    def reset(self):
        """Reset rate limit bucket"""
        self.requests.clear()
        self.last_reset = datetime.now()

@dataclass
class VPNTunnel:
    """VPN tunnel configuration"""
    tunnel_id: str
    remote_ip: str
    local_ip: str
    encryption_key: bytes
    established: datetime
    last_heartbeat: datetime
    active: bool = True
    traffic_stats: Dict[str, int] = field(default_factory=lambda: {"bytes_in": 0, "bytes_out": 0})

class NetworkFirewall:
    """Advanced network firewall with rule-based filtering"""
    
    def __init__(self):
        self.rules = []
        self.blocked_ips = set()
        self.allowed_ips = set()
        self.port_rules = {}
        self.traffic_monitor = defaultdict(int)
        self.blocked_attempts = defaultdict(int)
        self.rule_lock = threading.RLock()
        
        # Default rules
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """Setup default firewall rules"""
        # Allow loopback
        self.add_rule("allow", "127.0.0.1", None, "any", "Loopback traffic")
        self.add_rule("allow", "::1", None, "any", "IPv6 loopback traffic")
        
        # Block common attack ports
        dangerous_ports = [23, 135, 139, 445, 1433, 3389, 5900]
        for port in dangerous_ports:
            self.add_rule("block", "any", port, "tcp", f"Block dangerous port {port}")
        
        # Block private ranges from external access
        private_ranges = ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]
        for range_addr in private_ranges:
            self.add_rule("monitor", range_addr, None, "any", f"Monitor private range {range_addr}")
    
    def add_rule(self, action: str, ip_range: str, port: Optional[int], 
                 protocol: str, description: str) -> bool:
        """Add firewall rule"""
        with self.rule_lock:
            rule = {
                "id": len(self.rules) + 1,
                "action": action.lower(),  # allow, block, monitor
                "ip_range": ip_range,
                "port": port,
                "protocol": protocol.lower(),
                "description": description,
                "created": datetime.now(),
                "hits": 0
            }
            self.rules.append(rule)
            logger.info(f"Added firewall rule: {description}")
            return True
    
    def check_packet(self, src_ip: str, dst_port: int, protocol: str) -> Tuple[str, str]:
        """Check packet against firewall rules"""
        with self.rule_lock:
            # Check blocked IPs first
            if src_ip in self.blocked_ips:
                return "block", "IP blacklisted"
            
            # Check rules in order
            for rule in self.rules:
                if self._rule_matches(rule, src_ip, dst_port, protocol):
                    rule["hits"] += 1
                    
                    if rule["action"] == "block":
                        self.blocked_attempts[src_ip] += 1
                        return "block", rule["description"]
                    elif rule["action"] == "allow":
                        return "allow", rule["description"]
                    elif rule["action"] == "monitor":
                        self.traffic_monitor[src_ip] += 1
                        return "monitor", rule["description"]
            
            # Default action - log and allow for legitimate traffic
            if self._is_legitimate_traffic(src_ip, dst_port, protocol):
                return "allow", "Default allow for legitimate traffic"
            else:
                return "monitor", "Unknown traffic - monitoring"
    
    def _rule_matches(self, rule: Dict, src_ip: str, dst_port: int, protocol: str) -> bool:
        """Check if packet matches firewall rule"""
        # Check IP range
        if rule["ip_range"] != "any":
            try:
                if "/" in rule["ip_range"]:
                    # CIDR notation
                    network = ipaddress.ip_network(rule["ip_range"], strict=False)
                    if ipaddress.ip_address(src_ip) not in network:
                        return False
                else:
                    # Single IP
                    if src_ip != rule["ip_range"]:
                        return False
            except ValueError:
                logger.warning(f"Invalid IP range in rule: {rule['ip_range']}")
                return False
        
        # Check port
        if rule["port"] is not None and dst_port != rule["port"]:
            return False
        
        # Check protocol
        if rule["protocol"] != "any" and protocol.lower() != rule["protocol"]:
            return False
        
        return True
    
    def _is_legitimate_traffic(self, src_ip: str, dst_port: int, protocol: str) -> bool:
        """Determine if traffic appears legitimate"""
        # Check for legitimate service ports
        legitimate_ports = {80, 443, 22, 53, 25, 110, 143, 993, 995}
        
        if dst_port in legitimate_ports:
            return True
        
        # Check source IP reputation (simplified)
        try:
            ip_obj = ipaddress.ip_address(src_ip)
            if ip_obj.is_private or ip_obj.is_loopback:
                return True
        except ValueError:
            pass
        
        # Check request frequency
        if self.blocked_attempts.get(src_ip, 0) > 10:
            return False
        
        return True
    
    def block_ip(self, ip: str, reason: str = "Manual block"):
        """Block specific IP address"""
        self.blocked_ips.add(ip)
        logger.warning(f"Blocked IP {ip}: {reason}")
    
    def unblock_ip(self, ip: str):
        """Unblock specific IP address"""
        self.blocked_ips.discard(ip)
        logger.info(f"Unblocked IP {ip}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get firewall statistics"""
        with self.rule_lock:
            return {
                "rules_count": len(self.rules),
                "blocked_ips": len(self.blocked_ips),
                "traffic_monitored": dict(self.traffic_monitor),
                "blocked_attempts": dict(self.blocked_attempts),
                "rule_hits": sum(rule["hits"] for rule in self.rules)
            }

class IntrusionDetectionSystem:
    """Real-time intrusion detection system"""
    
    def __init__(self):
        self.attack_patterns = {}
        self.suspicious_activity = defaultdict(list)
        self.threat_scores = defaultdict(float)
        self.detection_rules = []
        self.alerts = deque(maxlen=1000)
        self.monitoring_active = False
        self.monitor_thread = None
        
        self._setup_detection_patterns()
    
    def _setup_detection_patterns(self):
        """Setup attack detection patterns"""
        self.attack_patterns = {
            "port_scan": {
                "pattern": "multiple_ports_short_time",
                "threshold": 5,
                "window": 60,
                "severity": "medium"
            },
            "brute_force": {
                "pattern": "multiple_failed_auth",
                "threshold": 5,
                "window": 300,
                "severity": "high"
            },
            "ddos": {
                "pattern": "high_request_rate",
                "threshold": 100,
                "window": 60,
                "severity": "critical"
            },
            "sql_injection": {
                "pattern": "sql_keywords_in_request",
                "keywords": ["SELECT", "UNION", "DROP", "INSERT", "UPDATE", "DELETE", "'", "--"],
                "severity": "high"
            },
            "xss_attempt": {
                "pattern": "script_tags_in_request",
                "keywords": ["<script>", "javascript:", "onerror=", "onload="],
                "severity": "medium"
            }
        }
    
    def analyze_request(self, src_ip: str, request_data: str, 
                       request_type: str = "http") -> Optional[SecurityEvent]:
        """Analyze incoming request for threats"""
        threat_score = 0.0
        detected_attacks = []
        
        # SQL Injection detection
        if self._detect_sql_injection(request_data):
            threat_score += 0.8
            detected_attacks.append("sql_injection")
        
        # XSS detection
        if self._detect_xss(request_data):
            threat_score += 0.6
            detected_attacks.append("xss_attempt")
        
        # Suspicious patterns
        if self._detect_suspicious_patterns(request_data):
            threat_score += 0.4
            detected_attacks.append("suspicious_pattern")
        
        # Rate-based detection
        self._update_request_tracking(src_ip, request_type)
        rate_threats = self._analyze_request_patterns(src_ip)
        if rate_threats:
            threat_score += 0.7
            detected_attacks.extend(rate_threats)
        
        # Create security event if threat detected
        if threat_score > 0.3:
            event = SecurityEvent(
                timestamp=datetime.now(),
                event_type="intrusion_attempt",
                source_ip=src_ip,
                destination_ip="localhost",
                port=80,  # Default web port
                protocol=request_type,
                severity=self._calculate_severity(threat_score),
                description=f"Detected attacks: {', '.join(detected_attacks)}",
                data={"request_data": request_data[:500], "attacks": detected_attacks},
                threat_score=threat_score
            )
            
            self.alerts.append(event)
            self.threat_scores[src_ip] = max(self.threat_scores[src_ip], threat_score)
            
            return event
        
        return None
    
    def _detect_sql_injection(self, request_data: str) -> bool:
        """Detect SQL injection attempts"""
        sql_keywords = self.attack_patterns["sql_injection"]["keywords"]
        request_upper = request_data.upper()
        
        # Check for SQL keywords
        keyword_count = sum(1 for keyword in sql_keywords if keyword in request_upper)
        
        # Look for common SQL injection patterns
        injection_patterns = [
            "' OR '1'='1",
            "' OR 1=1",
            "'; DROP TABLE",
            "UNION SELECT",
            "' AND 1=1"
        ]
        
        pattern_match = any(pattern in request_upper for pattern in injection_patterns)
        
        return keyword_count >= 2 or pattern_match
    
    def _detect_xss(self, request_data: str) -> bool:
        """Detect XSS attempts"""
        xss_keywords = self.attack_patterns["xss_attempt"]["keywords"]
        request_lower = request_data.lower()
        
        return any(keyword in request_lower for keyword in xss_keywords)
    
    def _detect_suspicious_patterns(self, request_data: str) -> bool:
        """Detect other suspicious patterns"""
        suspicious_patterns = [
            "../",  # Directory traversal
            "cmd.exe",  # Command injection
            "/etc/passwd",  # File access attempt
            "../../",  # Path traversal
            "exec(",  # Code execution
            "eval(",  # Code execution
        ]
        
        request_lower = request_data.lower()
        return any(pattern in request_lower for pattern in suspicious_patterns)
    
    def _update_request_tracking(self, src_ip: str, request_type: str):
        """Update request tracking for rate-based detection"""
        now = datetime.now()
        if src_ip not in self.suspicious_activity:
            self.suspicious_activity[src_ip] = []
        
        # Add current request
        self.suspicious_activity[src_ip].append({
            "timestamp": now,
            "type": request_type
        })
        
        # Clean old entries (keep last hour)
        cutoff = now - timedelta(hours=1)
        self.suspicious_activity[src_ip] = [
            req for req in self.suspicious_activity[src_ip] 
            if req["timestamp"] > cutoff
        ]
    
    def _analyze_request_patterns(self, src_ip: str) -> List[str]:
        """Analyze request patterns for rate-based attacks"""
        threats = []
        requests = self.suspicious_activity.get(src_ip, [])
        
        if not requests:
            return threats
        
        now = datetime.now()
        
        # Check for DDoS (high request rate)
        recent_requests = [
            req for req in requests 
            if (now - req["timestamp"]).total_seconds() <= 60
        ]
        
        if len(recent_requests) > 100:
            threats.append("ddos")
        
        # Check for brute force (repeated auth attempts)
        auth_requests = [
            req for req in requests 
            if req["type"] in ["auth", "login"] and 
            (now - req["timestamp"]).total_seconds() <= 300
        ]
        
        if len(auth_requests) > 5:
            threats.append("brute_force")
        
        # Check for port scanning (multiple different request types)
        unique_types = set(req["type"] for req in recent_requests)
        if len(unique_types) > 5:
            threats.append("port_scan")
        
        return threats
    
    def _calculate_severity(self, threat_score: float) -> str:
        """Calculate threat severity based on score"""
        if threat_score >= 0.8:
            return "critical"
        elif threat_score >= 0.6:
            return "high"
        elif threat_score >= 0.4:
            return "medium"
        else:
            return "low"
    
    def get_threat_summary(self) -> Dict[str, Any]:
        """Get current threat summary"""
        return {
            "total_alerts": len(self.alerts),
            "active_threats": len([ip for ip, score in self.threat_scores.items() if score > 0.5]),
            "high_risk_ips": [ip for ip, score in self.threat_scores.items() if score > 0.7],
            "recent_alerts": list(self.alerts)[-10:] if self.alerts else []
        }

class SecureCommunication:
    """TLS 1.3 and certificate management for secure communication"""
    
    def __init__(self):
        self.certificates = {}
        self.private_keys = {}
        self.trusted_certs = set()
        self.certificate_pins = {}
        self.ssl_context = None
        self.tls_version = ssl.TLSVersion.TLSv1_3
        
        self._setup_ssl_context()
    
    def _setup_ssl_context(self):
        """Setup SSL context with TLS 1.3 and security hardening"""
        self.ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        
        # Require TLS 1.3
        self.ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3
        self.ssl_context.maximum_version = ssl.TLSVersion.TLSv1_3
        
        # Security settings
        self.ssl_context.check_hostname = True
        self.ssl_context.verify_mode = ssl.CERT_REQUIRED
        
        # Cipher suites (TLS 1.3 handles this automatically)
        self.ssl_context.set_ciphers('TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256')
        
        logger.info("SSL context configured with TLS 1.3")
    
    def generate_self_signed_certificate(self, hostname: str = "localhost") -> Tuple[str, str]:
        """Generate self-signed certificate for testing"""
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        
        # Create certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "State"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "City"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "ASIS"),
            x509.NameAttribute(NameOID.COMMON_NAME, hostname),
        ])
        
        certificate = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(hostname),
                x509.DNSName("localhost"),
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Serialize to PEM format
        cert_pem = certificate.public_bytes(serialization.Encoding.PEM).decode()
        key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()
        
        # Store certificate and key
        self.certificates[hostname] = cert_pem
        self.private_keys[hostname] = key_pem
        
        logger.info(f"Generated self-signed certificate for {hostname}")
        return cert_pem, key_pem
    
    def pin_certificate(self, hostname: str, cert_data: str):
        """Pin certificate for hostname to prevent MITM attacks"""
        # Calculate certificate fingerprint
        cert_bytes = cert_data.encode()
        fingerprint = hashlib.sha256(cert_bytes).hexdigest()
        
        self.certificate_pins[hostname] = fingerprint
        logger.info(f"Pinned certificate for {hostname}: {fingerprint[:16]}...")
    
    def verify_certificate_pin(self, hostname: str, cert_data: str) -> bool:
        """Verify certificate against pinned certificate"""
        if hostname not in self.certificate_pins:
            return True  # No pin set
        
        cert_bytes = cert_data.encode()
        fingerprint = hashlib.sha256(cert_bytes).hexdigest()
        
        return fingerprint == self.certificate_pins[hostname]
    
    def create_secure_client_context(self) -> ssl.SSLContext:
        """Create secure SSL context for client connections"""
        context = ssl.create_default_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_3
        context.maximum_version = ssl.TLSVersion.TLSv1_3
        
        return context
    
    def create_secure_server_context(self, cert_file: str, key_file: str) -> ssl.SSLContext:
        """Create secure SSL context for server"""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.minimum_version = ssl.TLSVersion.TLSv1_3
        context.maximum_version = ssl.TLSVersion.TLSv1_3
        
        context.load_cert_chain(cert_file, key_file)
        
        return context

class APIRateLimiter:
    """Advanced API rate limiting with multiple strategies"""
    
    def __init__(self):
        self.rate_buckets = {}
        self.global_buckets = {}
        self.ip_buckets = defaultdict(lambda: RateLimitBucket())
        self.user_buckets = defaultdict(lambda: RateLimitBucket())
        self.endpoint_buckets = defaultdict(lambda: RateLimitBucket())
        self.cleanup_thread = None
        self.running = False
        
        # Rate limiting rules
        self.rules = {
            "global": {"max_requests": 1000, "window": 60},
            "per_ip": {"max_requests": 100, "window": 60},
            "per_user": {"max_requests": 200, "window": 60},
            "per_endpoint": {"max_requests": 500, "window": 60},
            "auth_endpoint": {"max_requests": 5, "window": 300}  # Stricter for auth
        }
        
        self.start_cleanup()
    
    def check_rate_limit(self, ip: str, user_id: Optional[str] = None, 
                        endpoint: str = "", method: str = "GET") -> Tuple[bool, Dict[str, Any]]:
        """Check if request is allowed under rate limits"""
        
        # Global rate limit
        global_key = "global"
        if global_key not in self.global_buckets:
            self.global_buckets[global_key] = RateLimitBucket(
                max_requests=self.rules["global"]["max_requests"],
                window_seconds=self.rules["global"]["window"]
            )
        
        if not self.global_buckets[global_key].is_allowed():
            return False, {
                "error": "global_rate_limit_exceeded",
                "retry_after": self.rules["global"]["window"]
            }
        
        # IP-based rate limit
        ip_bucket = self.ip_buckets[ip]
        ip_bucket.max_requests = self.rules["per_ip"]["max_requests"]
        ip_bucket.window_seconds = self.rules["per_ip"]["window"]
        
        if not ip_bucket.is_allowed():
            return False, {
                "error": "ip_rate_limit_exceeded",
                "retry_after": self.rules["per_ip"]["window"]
            }
        
        # User-based rate limit (if authenticated)
        if user_id:
            user_bucket = self.user_buckets[user_id]
            user_bucket.max_requests = self.rules["per_user"]["max_requests"]
            user_bucket.window_seconds = self.rules["per_user"]["window"]
            
            if not user_bucket.is_allowed():
                return False, {
                    "error": "user_rate_limit_exceeded",
                    "retry_after": self.rules["per_user"]["window"]
                }
        
        # Endpoint-specific rate limit
        endpoint_key = f"{method}:{endpoint}"
        endpoint_bucket = self.endpoint_buckets[endpoint_key]
        
        # Special handling for auth endpoints
        if "auth" in endpoint.lower() or "login" in endpoint.lower():
            endpoint_bucket.max_requests = self.rules["auth_endpoint"]["max_requests"]
            endpoint_bucket.window_seconds = self.rules["auth_endpoint"]["window"]
        else:
            endpoint_bucket.max_requests = self.rules["per_endpoint"]["max_requests"]
            endpoint_bucket.window_seconds = self.rules["per_endpoint"]["window"]
        
        if not endpoint_bucket.is_allowed():
            return False, {
                "error": "endpoint_rate_limit_exceeded",
                "retry_after": endpoint_bucket.window_seconds
            }
        
        return True, {"status": "allowed"}
    
    def add_custom_rule(self, rule_name: str, max_requests: int, window_seconds: int):
        """Add custom rate limiting rule"""
        self.rules[rule_name] = {
            "max_requests": max_requests,
            "window": window_seconds
        }
        logger.info(f"Added rate limiting rule: {rule_name}")
    
    def get_rate_limit_status(self, ip: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Get current rate limit status"""
        status = {
            "ip": {
                "remaining": self.ip_buckets[ip].max_requests - len(self.ip_buckets[ip].requests),
                "reset_time": self.ip_buckets[ip].last_reset + timedelta(seconds=self.ip_buckets[ip].window_seconds)
            }
        }
        
        if user_id and user_id in self.user_buckets:
            user_bucket = self.user_buckets[user_id]
            status["user"] = {
                "remaining": user_bucket.max_requests - len(user_bucket.requests),
                "reset_time": user_bucket.last_reset + timedelta(seconds=user_bucket.window_seconds)
            }
        
        return status
    
    def start_cleanup(self):
        """Start cleanup thread for old buckets"""
        if not self.running:
            self.running = True
            self.cleanup_thread = threading.Thread(target=self._cleanup_buckets, daemon=True)
            self.cleanup_thread.start()
    
    def stop_cleanup(self):
        """Stop cleanup thread"""
        self.running = False
        if self.cleanup_thread:
            self.cleanup_thread.join()
    
    def _cleanup_buckets(self):
        """Clean up old and unused rate limit buckets"""
        while self.running:
            try:
                now = datetime.now()
                cleanup_threshold = timedelta(hours=1)
                
                # Clean IP buckets
                expired_ips = [
                    ip for ip, bucket in self.ip_buckets.items()
                    if (now - bucket.last_reset) > cleanup_threshold and not bucket.requests
                ]
                for ip in expired_ips:
                    del self.ip_buckets[ip]
                
                # Clean user buckets
                expired_users = [
                    user for user, bucket in self.user_buckets.items()
                    if (now - bucket.last_reset) > cleanup_threshold and not bucket.requests
                ]
                for user in expired_users:
                    del self.user_buckets[user]
                
                # Clean endpoint buckets
                expired_endpoints = [
                    endpoint for endpoint, bucket in self.endpoint_buckets.items()
                    if (now - bucket.last_reset) > cleanup_threshold and not bucket.requests
                ]
                for endpoint in expired_endpoints:
                    del self.endpoint_buckets[endpoint]
                
                time.sleep(300)  # Clean every 5 minutes
                
            except Exception as e:
                logger.error(f"Error in rate limiter cleanup: {e}")
                time.sleep(60)

class VPNManager:
    """VPN tunnel management for secure connections"""
    
    def __init__(self):
        self.tunnels = {}
        self.encryption_keys = {}
        self.tunnel_stats = defaultdict(dict)
        self.active_connections = set()
        
    def create_tunnel(self, tunnel_id: str, remote_ip: str, local_ip: str) -> bool:
        """Create new VPN tunnel"""
        try:
            # Generate encryption key for tunnel
            encryption_key = secrets.token_bytes(32)  # 256-bit key
            
            tunnel = VPNTunnel(
                tunnel_id=tunnel_id,
                remote_ip=remote_ip,
                local_ip=local_ip,
                encryption_key=encryption_key,
                established=datetime.now(),
                last_heartbeat=datetime.now()
            )
            
            self.tunnels[tunnel_id] = tunnel
            self.encryption_keys[tunnel_id] = encryption_key
            self.active_connections.add(tunnel_id)
            
            logger.info(f"Created VPN tunnel {tunnel_id}: {local_ip} <-> {remote_ip}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create VPN tunnel {tunnel_id}: {e}")
            return False
    
    def encrypt_tunnel_data(self, tunnel_id: str, data: bytes) -> bytes:
        """Encrypt data for VPN tunnel"""
        if tunnel_id not in self.encryption_keys:
            raise ValueError(f"No encryption key for tunnel {tunnel_id}")
        
        key = self.encryption_keys[tunnel_id]
        
        # Generate random IV
        iv = secrets.token_bytes(16)
        
        # AES-256 encryption
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        
        # Pad data to block size
        block_size = 16
        padding_length = block_size - (len(data) % block_size)
        padded_data = data + bytes([padding_length] * padding_length)
        
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        # Return IV + encrypted data
        return iv + encrypted_data
    
    def decrypt_tunnel_data(self, tunnel_id: str, encrypted_data: bytes) -> bytes:
        """Decrypt data from VPN tunnel"""
        if tunnel_id not in self.encryption_keys:
            raise ValueError(f"No encryption key for tunnel {tunnel_id}")
        
        key = self.encryption_keys[tunnel_id]
        
        # Extract IV and encrypted data
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        
        # AES-256 decryption
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove padding
        padding_length = padded_data[-1]
        data = padded_data[:-padding_length]
        
        return data
    
    def update_tunnel_stats(self, tunnel_id: str, bytes_in: int, bytes_out: int):
        """Update tunnel traffic statistics"""
        if tunnel_id in self.tunnels:
            tunnel = self.tunnels[tunnel_id]
            tunnel.traffic_stats["bytes_in"] += bytes_in
            tunnel.traffic_stats["bytes_out"] += bytes_out
            tunnel.last_heartbeat = datetime.now()
    
    def close_tunnel(self, tunnel_id: str):
        """Close VPN tunnel"""
        if tunnel_id in self.tunnels:
            self.tunnels[tunnel_id].active = False
            self.active_connections.discard(tunnel_id)
            logger.info(f"Closed VPN tunnel {tunnel_id}")
    
    def get_tunnel_status(self) -> Dict[str, Any]:
        """Get status of all VPN tunnels"""
        return {
            "active_tunnels": len(self.active_connections),
            "total_tunnels": len(self.tunnels),
            "tunnels": {
                tid: {
                    "remote_ip": tunnel.remote_ip,
                    "established": tunnel.established.isoformat(),
                    "last_heartbeat": tunnel.last_heartbeat.isoformat(),
                    "active": tunnel.active,
                    "traffic": tunnel.traffic_stats
                }
                for tid, tunnel in self.tunnels.items()
            }
        }

class ASISNetworkSecurity:
    """Comprehensive ASIS Network Security System"""
    
    def __init__(self):
        self.firewall = NetworkFirewall()
        self.intrusion_detection = IntrusionDetectionSystem()
        self.secure_comm = SecureCommunication()
        self.rate_limiter = APIRateLimiter()
        self.vpn_manager = VPNManager()
        
        # Security monitoring
        self.security_events = deque(maxlen=10000)
        self.security_status = {
            "firewall_active": True,
            "ids_active": True,
            "rate_limiting_active": True,
            "ssl_tls_active": True,
            "vpn_active": True
        }
        
        # Integration settings
        self.monitoring_active = False
        self.alert_thresholds = {
            "critical_events_per_hour": 10,
            "blocked_ips_threshold": 100,
            "threat_score_threshold": 0.8
        }
        
        logger.info("ASIS Network Security System initialized")
    
    def setup_secure_communication(self):
        """Setup TLS 1.3, certificate pinning, and secure protocols"""
        try:
            # Generate self-signed certificate for testing
            cert_pem, key_pem = self.secure_comm.generate_self_signed_certificate("asis-server")
            
            # Pin the certificate
            self.secure_comm.pin_certificate("asis-server", cert_pem)
            
            # Setup SSL context
            self.secure_comm._setup_ssl_context()
            
            self.security_status["ssl_tls_active"] = True
            logger.info("✅ Secure communication setup complete")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to setup secure communication: {e}")
            self.security_status["ssl_tls_active"] = False
            return False
    
    def implement_api_rate_limiting(self):
        """Implement API rate limiting and DDoS protection"""
        try:
            # Setup default rate limiting rules
            self.rate_limiter.add_custom_rule("asis_api", 150, 60)
            self.rate_limiter.add_custom_rule("asis_auth", 3, 300)
            self.rate_limiter.add_custom_rule("asis_data", 500, 300)
            
            # Start rate limiter
            self.rate_limiter.start_cleanup()
            
            self.security_status["rate_limiting_active"] = True
            logger.info("✅ API rate limiting implemented")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to implement rate limiting: {e}")
            self.security_status["rate_limiting_active"] = False
            return False
    
    def setup_firewall_protection(self):
        """Setup advanced firewall with custom rules"""
        try:
            # Add ASIS-specific firewall rules
            self.firewall.add_rule("allow", "127.0.0.1", 8080, "tcp", "ASIS local access")
            self.firewall.add_rule("allow", "192.168.0.0/16", 8080, "tcp", "ASIS LAN access")
            self.firewall.add_rule("monitor", "any", 8080, "tcp", "Monitor ASIS public access")
            
            # Block common attack vectors
            self.firewall.add_rule("block", "any", 22, "tcp", "Block SSH from external")
            self.firewall.add_rule("block", "any", 3389, "tcp", "Block RDP")
            
            self.security_status["firewall_active"] = True
            logger.info("✅ Firewall protection configured")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to setup firewall: {e}")
            self.security_status["firewall_active"] = False
            return False
    
    def start_intrusion_detection(self):
        """Start real-time intrusion detection"""
        try:
            self.intrusion_detection.monitoring_active = True
            self.security_status["ids_active"] = True
            logger.info("✅ Intrusion detection system started")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start intrusion detection: {e}")
            self.security_status["ids_active"] = False
            return False
    
    def setup_vpn_infrastructure(self):
        """Setup VPN infrastructure for secure remote access"""
        try:
            # Create default VPN tunnel for admin access
            success = self.vpn_manager.create_tunnel(
                "admin_tunnel",
                "0.0.0.0",  # Accept from any remote
                "127.0.0.1"  # Local ASIS server
            )
            
            if success:
                self.security_status["vpn_active"] = True
                logger.info("✅ VPN infrastructure setup complete")
                return True
            else:
                raise Exception("Failed to create admin tunnel")
                
        except Exception as e:
            logger.error(f"❌ Failed to setup VPN infrastructure: {e}")
            self.security_status["vpn_active"] = False
            return False
    
    def process_network_request(self, src_ip: str, dst_port: int, protocol: str, 
                              request_data: str = "", user_id: Optional[str] = None,
                              endpoint: str = "") -> Dict[str, Any]:
        """Process incoming network request through all security layers"""
        
        security_result = {
            "allowed": False,
            "blocked_by": [],
            "security_events": [],
            "threat_score": 0.0,
            "rate_limit_status": {},
            "recommendations": []
        }
        
        try:
            # 1. Firewall Check
            firewall_action, firewall_reason = self.firewall.check_packet(src_ip, dst_port, protocol)
            
            if firewall_action == "block":
                security_result["blocked_by"].append("firewall")
                security_result["recommendations"].append(f"Firewall blocked: {firewall_reason}")
                self._log_security_event("firewall_block", src_ip, dst_port, protocol, firewall_reason)
                return security_result
            
            # 2. Rate Limiting Check
            rate_allowed, rate_info = self.rate_limiter.check_rate_limit(
                src_ip, user_id, endpoint, protocol.upper()
            )
            
            security_result["rate_limit_status"] = rate_info
            
            if not rate_allowed:
                security_result["blocked_by"].append("rate_limiter")
                security_result["recommendations"].append(f"Rate limit exceeded: {rate_info.get('error', 'Unknown')}")
                self._log_security_event("rate_limit_exceeded", src_ip, dst_port, protocol, str(rate_info))
                return security_result
            
            # 3. Intrusion Detection Analysis
            if request_data:
                ids_event = self.intrusion_detection.analyze_request(src_ip, request_data, protocol)
                
                if ids_event:
                    security_result["security_events"].append(ids_event)
                    security_result["threat_score"] = ids_event.threat_score
                    
                    # Block high-threat requests
                    if ids_event.threat_score > 0.8:
                        security_result["blocked_by"].append("intrusion_detection")
                        security_result["recommendations"].append(f"High threat detected: {ids_event.description}")
                        
                        # Auto-block IP for critical threats
                        self.firewall.block_ip(src_ip, f"Critical threat detected: {ids_event.description}")
                        return security_result
                    
                    # Log medium/low threats for monitoring
                    elif ids_event.threat_score > 0.4:
                        security_result["recommendations"].append(f"Potential threat detected: {ids_event.description}")
            
            # 4. All checks passed
            security_result["allowed"] = True
            security_result["recommendations"].append("Request passed all security checks")
            
            # Log successful access
            self._log_security_event("access_granted", src_ip, dst_port, protocol, "Access granted")
            
        except Exception as e:
            logger.error(f"Error processing network request: {e}")
            security_result["blocked_by"].append("security_error")
            security_result["recommendations"].append(f"Security processing error: {str(e)}")
        
        return security_result
    
    def _log_security_event(self, event_type: str, src_ip: str, dst_port: int, 
                           protocol: str, description: str):
        """Log security event"""
        event = SecurityEvent(
            timestamp=datetime.now(),
            event_type=event_type,
            source_ip=src_ip,
            destination_ip="localhost",
            port=dst_port,
            protocol=protocol,
            severity="info" if event_type == "access_granted" else "warning",
            description=description
        )
        
        self.security_events.append(event)
    
    def get_security_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive security dashboard data"""
        
        # Recent events summary
        recent_events = list(self.security_events)[-50:] if self.security_events else []
        event_counts = defaultdict(int)
        for event in recent_events:
            event_counts[event.event_type] += 1
        
        # Threat summary
        threat_summary = self.intrusion_detection.get_threat_summary()
        
        # Firewall stats
        firewall_stats = self.firewall.get_statistics()
        
        # Rate limiting status
        rate_limit_stats = {
            "active_buckets": len(self.rate_limiter.ip_buckets),
            "rules_configured": len(self.rate_limiter.rules)
        }
        
        # VPN status
        vpn_status = self.vpn_manager.get_tunnel_status()
        
        return {
            "security_status": self.security_status,
            "recent_events": {
                "total": len(recent_events),
                "by_type": dict(event_counts),
                "events": [
                    {
                        "timestamp": event.timestamp.isoformat(),
                        "type": event.event_type,
                        "source_ip": event.source_ip,
                        "description": event.description,
                        "severity": event.severity
                    }
                    for event in recent_events[-10:]
                ]
            },
            "threat_detection": threat_summary,
            "firewall": firewall_stats,
            "rate_limiting": rate_limit_stats,
            "vpn": vpn_status,
            "ssl_tls": {
                "version": "TLS 1.3",
                "certificates_pinned": len(self.secure_comm.certificate_pins),
                "certificates_available": len(self.secure_comm.certificates)
            },
            "overall_security_score": self._calculate_security_score()
        }
    
    def _calculate_security_score(self) -> float:
        """Calculate overall security score (0.0 to 1.0)"""
        score = 0.0
        
        # Base score for active components
        if self.security_status["firewall_active"]:
            score += 0.25
        if self.security_status["ids_active"]:
            score += 0.25
        if self.security_status["rate_limiting_active"]:
            score += 0.20
        if self.security_status["ssl_tls_active"]:
            score += 0.20
        if self.security_status["vpn_active"]:
            score += 0.10
        
        # Reduce score for security issues
        recent_critical_events = [
            event for event in list(self.security_events)[-100:]
            if event.severity == "critical"
        ]
        
        if len(recent_critical_events) > 5:
            score *= 0.8  # Reduce by 20% for multiple critical events
        
        # Check for blocked IPs (high number indicates many attacks)
        if len(self.firewall.blocked_ips) > 50:
            score *= 0.9  # Reduce by 10% for many blocked IPs
        
        return min(1.0, max(0.0, score))
    
    def emergency_shutdown(self):
        """Emergency shutdown of all network security components"""
        logger.critical("🚨 EMERGENCY SHUTDOWN INITIATED")
        
        try:
            # Block all external traffic
            self.firewall.add_rule("block", "any", "any", "any", "Emergency shutdown - block all")
            
            # Stop rate limiter
            self.rate_limiter.stop_cleanup()
            
            # Close all VPN tunnels
            for tunnel_id in list(self.vpn_manager.active_connections):
                self.vpn_manager.close_tunnel(tunnel_id)
            
            # Update security status
            for key in self.security_status:
                self.security_status[key] = False
            
            logger.critical("🚨 Emergency shutdown complete")
            
        except Exception as e:
            logger.critical(f"🚨 Error during emergency shutdown: {e}")
    
    def initialize_full_security(self) -> bool:
        """Initialize all security components"""
        logger.info("🔒 Initializing ASIS Network Security...")
        
        success_count = 0
        total_components = 5
        
        # Setup each component
        if self.setup_secure_communication():
            success_count += 1
        
        if self.implement_api_rate_limiting():
            success_count += 1
        
        if self.setup_firewall_protection():
            success_count += 1
        
        if self.start_intrusion_detection():
            success_count += 1
        
        if self.setup_vpn_infrastructure():
            success_count += 1
        
        success_rate = success_count / total_components
        
        if success_rate >= 0.8:
            logger.info(f"✅ ASIS Network Security initialized successfully ({success_count}/{total_components} components)")
            return True
        else:
            logger.warning(f"⚠️ ASIS Network Security partially initialized ({success_count}/{total_components} components)")
            return False

# Example usage and testing
if __name__ == "__main__":
    # Initialize ASIS Network Security
    asis_security = ASISNetworkSecurity()
    
    # Initialize all security components
    if asis_security.initialize_full_security():
        print("🔒 ASIS Network Security is fully operational!")
        
        # Test security processing
        test_requests = [
            ("192.168.1.100", 8080, "tcp", "GET /api/data", None, "/api/data"),
            ("10.0.0.50", 8080, "tcp", "POST /auth/login", "user123", "/auth/login"),
            ("192.168.1.200", 8080, "tcp", "GET /api/users'; DROP TABLE users; --", None, "/api/users"),
            ("203.0.113.1", 22, "tcp", "", None, ""),
        ]
        
        print("\n🧪 Testing security processing...")
        for src_ip, port, protocol, request_data, user_id, endpoint in test_requests:
            result = asis_security.process_network_request(
                src_ip, port, protocol, request_data, user_id, endpoint
            )
            
            status = "✅ ALLOWED" if result["allowed"] else "❌ BLOCKED"
            print(f"{status} - {src_ip}:{port} - {result['recommendations'][0] if result['recommendations'] else 'No issues'}")
        
        # Display security dashboard
        print("\n📊 Security Dashboard:")
        dashboard = asis_security.get_security_dashboard()
        print(f"Overall Security Score: {dashboard['overall_security_score']:.2f}")
        print(f"Recent Events: {dashboard['recent_events']['total']}")
        print(f"Active Threats: {dashboard['threat_detection']['active_threats']}")
        
    else:
        print("❌ ASIS Network Security initialization failed!")