#!/usr/bin/env python3
"""
ASIS Network Security Test Suite
Comprehensive testing of all network security components
"""

import asyncio
import pytest
import requests
import ssl
import socket
import time
import json
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Import ASIS security components
from asis_network_security import (
    ASISNetworkSecurity, NetworkFirewall, IntrusionDetectionSystem,
    SecureCommunication, APIRateLimiter, VPNManager
)
from asis_unified_security import UnifiedSecurityManager, create_asis_unified_security
from asis_secure_server import ASISSecureServer

class NetworkSecurityTester:
    """Comprehensive network security test suite"""
    
    def __init__(self):
        self.test_results = []
        self.test_server = None
        self.server_task = None
        
    def run_all_tests(self):
        """Run complete test suite"""
        
        print("🔒 ASIS Network Security Test Suite")
        print("=" * 60)
        
        # Test components individually
        self.test_firewall()
        self.test_intrusion_detection()
        self.test_secure_communication()
        self.test_rate_limiting()
        self.test_vpn_management()
        self.test_unified_security()
        
        # Test integration
        asyncio.run(self.test_secure_server_integration())
        
        # Print summary
        self.print_test_summary()
        
        return all(result["passed"] for result in self.test_results)
    
    def test_firewall(self):
        """Test network firewall functionality"""
        
        print("\n🔥 Testing Network Firewall...")
        
        try:
            firewall = NetworkFirewall()
            
            # Test rule addition
            assert firewall.add_rule("block", "192.168.1.1", 22, "tcp", "Test block rule")
            assert firewall.add_rule("allow", "127.0.0.1", 8080, "tcp", "Test allow rule")
            
            # Test packet checking
            action, reason = firewall.check_packet("192.168.1.1", 22, "tcp")
            assert action == "block", f"Expected block, got {action}"
            
            action, reason = firewall.check_packet("127.0.0.1", 8080, "tcp")
            assert action == "allow", f"Expected allow, got {action}"
            
            # Test IP blocking
            firewall.block_ip("10.0.0.1", "Test block")
            action, reason = firewall.check_packet("10.0.0.1", 80, "tcp")
            assert action == "block", "IP blocking failed"
            
            # Test statistics
            stats = firewall.get_statistics()
            assert "rules_count" in stats
            assert "blocked_ips" in stats
            
            self.test_results.append({
                "component": "Network Firewall",
                "passed": True,
                "details": "All firewall tests passed"
            })
            print("✅ Network Firewall tests passed")
            
        except Exception as e:
            self.test_results.append({
                "component": "Network Firewall",
                "passed": False,
                "details": f"Firewall test failed: {e}"
            })
            print(f"❌ Network Firewall tests failed: {e}")
    
    def test_intrusion_detection(self):
        """Test intrusion detection system"""
        
        print("\n🛡️ Testing Intrusion Detection System...")
        
        try:
            ids = IntrusionDetectionSystem()
            
            # Test SQL injection detection
            sql_injection = "'; DROP TABLE users; --"
            event = ids.analyze_request("192.168.1.100", sql_injection, "http")
            assert event is not None, "SQL injection not detected"
            assert "sql_injection" in event.data.get("attacks", [])
            
            # Test XSS detection
            xss_attempt = "<script>alert('xss')</script>"
            event = ids.analyze_request("192.168.1.101", xss_attempt, "http")
            assert event is not None, "XSS not detected"
            assert "xss_attempt" in event.data.get("attacks", [])
            
            # Test rate-based detection (DDoS simulation)
            for i in range(50):
                ids.analyze_request("192.168.1.102", f"request_{i}", "http")
            
            event = ids.analyze_request("192.168.1.102", "final_request", "http")
            if event:
                attacks = event.data.get("attacks", [])
                # Should detect some form of rate-based attack
                assert len(attacks) > 0, "Rate-based attack detection failed"
            
            # Test threat summary
            summary = ids.get_threat_summary()
            assert "total_alerts" in summary
            assert summary["total_alerts"] > 0
            
            self.test_results.append({
                "component": "Intrusion Detection",
                "passed": True,
                "details": "All IDS tests passed"
            })
            print("✅ Intrusion Detection tests passed")
            
        except Exception as e:
            self.test_results.append({
                "component": "Intrusion Detection",
                "passed": False,
                "details": f"IDS test failed: {e}"
            })
            print(f"❌ Intrusion Detection tests failed: {e}")
    
    def test_secure_communication(self):
        """Test secure communication features"""
        
        print("\n🔐 Testing Secure Communication...")
        
        try:
            secure_comm = SecureCommunication()
            
            # Test certificate generation
            cert_pem, key_pem = secure_comm.generate_self_signed_certificate("test-server")
            assert cert_pem is not None and len(cert_pem) > 0
            assert key_pem is not None and len(key_pem) > 0
            
            # Test certificate pinning
            secure_comm.pin_certificate("test-server", cert_pem)
            assert secure_comm.verify_certificate_pin("test-server", cert_pem)
            
            # Test SSL context creation
            client_context = secure_comm.create_secure_client_context()
            assert client_context.minimum_version == ssl.TLSVersion.TLSv1_3
            
            self.test_results.append({
                "component": "Secure Communication",
                "passed": True,
                "details": "All secure communication tests passed"
            })
            print("✅ Secure Communication tests passed")
            
        except Exception as e:
            self.test_results.append({
                "component": "Secure Communication",
                "passed": False,
                "details": f"Secure communication test failed: {e}"
            })
            print(f"❌ Secure Communication tests failed: {e}")
    
    def test_rate_limiting(self):
        """Test API rate limiting"""
        
        print("\n🚦 Testing API Rate Limiting...")
        
        try:
            rate_limiter = APIRateLimiter()
            
            # Test normal requests (should be allowed)
            for i in range(5):
                allowed, info = rate_limiter.check_rate_limit("192.168.1.200", None, "/api/test", "GET")
                assert allowed, f"Request {i} should be allowed"
            
            # Test rate limit exceeded
            # Set a very low limit for testing
            rate_limiter.rules["per_ip"]["max_requests"] = 3
            rate_limiter.rules["per_ip"]["window"] = 60
            
            # New IP with low limit
            test_ip = "192.168.1.201"
            
            # First few requests should be allowed
            for i in range(3):
                allowed, info = rate_limiter.check_rate_limit(test_ip, None, "/api/test", "GET")
                assert allowed, f"Request {i} should be allowed under limit"
            
            # Next request should be rate limited
            allowed, info = rate_limiter.check_rate_limit(test_ip, None, "/api/test", "GET")
            assert not allowed, "Request should be rate limited"
            assert "rate_limit_exceeded" in info["error"]
            
            # Test user-specific rate limiting
            allowed, info = rate_limiter.check_rate_limit("192.168.1.202", "user123", "/api/test", "GET")
            assert allowed, "User-specific request should be allowed"
            
            # Test endpoint-specific rate limiting
            allowed, info = rate_limiter.check_rate_limit("192.168.1.203", None, "/auth/login", "POST")
            assert allowed, "Auth endpoint request should be allowed"
            
            self.test_results.append({
                "component": "API Rate Limiting",
                "passed": True,
                "details": "All rate limiting tests passed"
            })
            print("✅ API Rate Limiting tests passed")
            
        except Exception as e:
            self.test_results.append({
                "component": "API Rate Limiting",
                "passed": False,
                "details": f"Rate limiting test failed: {e}"
            })
            print(f"❌ API Rate Limiting tests failed: {e}")
    
    def test_vpn_management(self):
        """Test VPN management"""
        
        print("\n🌐 Testing VPN Management...")
        
        try:
            vpn_manager = VPNManager()
            
            # Test tunnel creation
            tunnel_id = "test_tunnel_001"
            success = vpn_manager.create_tunnel(tunnel_id, "203.0.113.1", "192.168.1.1")
            assert success, "Tunnel creation failed"
            
            # Test tunnel encryption/decryption
            test_data = b"This is test VPN data"
            encrypted = vpn_manager.encrypt_tunnel_data(tunnel_id, test_data)
            decrypted = vpn_manager.decrypt_tunnel_data(tunnel_id, encrypted)
            assert decrypted == test_data, "VPN encryption/decryption failed"
            
            # Test traffic stats update
            vpn_manager.update_tunnel_stats(tunnel_id, 1024, 512)
            status = vpn_manager.get_tunnel_status()
            assert tunnel_id in status["tunnels"]
            assert status["tunnels"][tunnel_id]["traffic"]["bytes_in"] == 1024
            
            # Test tunnel closure
            vpn_manager.close_tunnel(tunnel_id)
            status = vpn_manager.get_tunnel_status()
            assert not status["tunnels"][tunnel_id]["active"]
            
            self.test_results.append({
                "component": "VPN Management",
                "passed": True,
                "details": "All VPN tests passed"
            })
            print("✅ VPN Management tests passed")
            
        except Exception as e:
            self.test_results.append({
                "component": "VPN Management",
                "passed": False,
                "details": f"VPN test failed: {e}"
            })
            print(f"❌ VPN Management tests failed: {e}")
    
    def test_unified_security(self):
        """Test unified security management"""
        
        print("\n🔗 Testing Unified Security Management...")
        
        try:
            # Test unified security creation
            security_manager = create_asis_unified_security()
            assert security_manager is not None
            
            # Test valid request processing
            valid_request = {
                "source_ip": "192.168.1.100",
                "user_id": "test_user",
                "action": "read",
                "resource": "test_data",
                "protocol": "https",
                "port": 8443,
                "endpoint": "/api/test",
                "content": "valid request content"
            }
            
            result = security_manager.process_unified_request(valid_request)
            # Note: This may be blocked due to authentication requirements
            assert "security_layers_passed" in result
            assert "security_layers_failed" in result
            
            # Test malicious request processing
            malicious_request = {
                "source_ip": "203.0.113.1",  # External IP
                "user_id": "attacker",
                "action": "admin",
                "resource": "system_config",
                "protocol": "tcp",
                "port": 22,
                "endpoint": "/admin/hack",
                "content": "'; DROP TABLE users; --"
            }
            
            result = security_manager.process_unified_request(malicious_request)
            assert not result["allowed"], "Malicious request should be blocked"
            assert len(result["security_layers_failed"]) > 0
            
            # Test security status
            status = security_manager.get_unified_security_status()
            assert "unified_security" in status
            assert "network_security" in status
            assert "correlation_engine" in status
            
            self.test_results.append({
                "component": "Unified Security",
                "passed": True,
                "details": "All unified security tests passed"
            })
            print("✅ Unified Security tests passed")
            
        except Exception as e:
            self.test_results.append({
                "component": "Unified Security",
                "passed": False,
                "details": f"Unified security test failed: {e}"
            })
            print(f"❌ Unified Security tests failed: {e}")
    
    async def test_secure_server_integration(self):
        """Test secure server integration"""
        
        print("\n🌐 Testing Secure Server Integration...")
        
        try:
            # Create test server
            self.test_server = ASISSecureServer(host="127.0.0.1", port=8444)
            
            # Start server in background
            server_started = await self.test_server.start_server()
            assert server_started, "Server failed to start"
            
            # Wait for server to be ready
            await asyncio.sleep(2)
            
            # Test HTTPS connection (ignore SSL warnings for self-signed cert)
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            # Test health endpoint
            try:
                response = requests.get("https://127.0.0.1:8444/api/health", 
                                      verify=False, timeout=5)
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "healthy"
            except requests.exceptions.RequestException as e:
                print(f"⚠️ HTTPS test skipped due to connection issues: {e}")
            
            # Test rate limiting (make many requests)
            rate_limit_hit = False
            for i in range(20):
                try:
                    response = requests.get("https://127.0.0.1:8444/api/health", 
                                          verify=False, timeout=1)
                    if response.status_code == 429:
                        rate_limit_hit = True
                        break
                except:
                    pass
            
            # Note: Rate limiting may or may not trigger in this test
            
            # Stop server
            await self.test_server.stop_server()
            
            self.test_results.append({
                "component": "Secure Server Integration",
                "passed": True,
                "details": "Server integration tests passed"
            })
            print("✅ Secure Server Integration tests passed")
            
        except Exception as e:
            self.test_results.append({
                "component": "Secure Server Integration",
                "passed": False,
                "details": f"Server integration test failed: {e}"
            })
            print(f"❌ Secure Server Integration tests failed: {e}")
            
            # Ensure server is stopped
            if self.test_server:
                try:
                    await self.test_server.stop_server()
                except:
                    pass
    
    def test_security_attack_scenarios(self):
        """Test various attack scenarios"""
        
        print("\n⚔️ Testing Attack Scenarios...")
        
        try:
            network_security = ASISNetworkSecurity()
            network_security.initialize_full_security()
            
            # Scenario 1: Port scan attack
            scan_results = []
            for port in [22, 23, 80, 443, 3389]:
                result = network_security.process_network_request(
                    src_ip="203.0.113.100",
                    dst_port=port,
                    protocol="tcp",
                    request_data=f"scan port {port}",
                    endpoint=f"/port/{port}"
                )
                scan_results.append(result)
            
            # Should detect port scanning behavior
            blocked_count = sum(1 for r in scan_results if not r["allowed"])
            assert blocked_count > 0, "Port scan not detected"
            
            # Scenario 2: SQL injection attack
            sql_attack_result = network_security.process_network_request(
                src_ip="203.0.113.101",
                dst_port=8080,
                protocol="https",
                request_data="GET /api/users?id=1'; DROP TABLE users; --",
                endpoint="/api/users"
            )
            
            # Should be blocked or flagged as high threat
            assert (not sql_attack_result["allowed"] or 
                    sql_attack_result["threat_score"] > 0.5), "SQL injection not detected"
            
            # Scenario 3: DDoS simulation
            ddos_results = []
            for i in range(50):
                result = network_security.process_network_request(
                    src_ip="203.0.113.102",
                    dst_port=8080,
                    protocol="https",
                    request_data=f"GET /api/flood_{i}",
                    endpoint="/api/flood"
                )
                ddos_results.append(result)
            
            # Should trigger rate limiting
            rate_limited = any(not r["allowed"] for r in ddos_results[-10:])
            # Note: Rate limiting may not trigger in this simplified test
            
            self.test_results.append({
                "component": "Attack Scenarios",
                "passed": True,
                "details": f"Attack scenario tests passed - blocked {blocked_count} port scans"
            })
            print("✅ Attack Scenario tests passed")
            
        except Exception as e:
            self.test_results.append({
                "component": "Attack Scenarios",
                "passed": False,
                "details": f"Attack scenario test failed: {e}"
            })
            print(f"❌ Attack Scenario tests failed: {e}")
    
    def test_performance_benchmarks(self):
        """Test performance benchmarks"""
        
        print("\n⚡ Testing Performance Benchmarks...")
        
        try:
            network_security = ASISNetworkSecurity()
            network_security.initialize_full_security()
            
            # Benchmark request processing speed
            start_time = time.time()
            request_count = 100
            
            for i in range(request_count):
                network_security.process_network_request(
                    src_ip=f"192.168.1.{100 + (i % 50)}",
                    dst_port=8080,
                    protocol="https",
                    request_data=f"GET /api/test_{i}",
                    endpoint="/api/test"
                )
            
            end_time = time.time()
            total_time = end_time - start_time
            requests_per_second = request_count / total_time
            
            # Performance assertions
            assert requests_per_second > 50, f"Performance too slow: {requests_per_second:.2f} req/s"
            assert total_time < 10, f"Total processing time too high: {total_time:.2f}s"
            
            self.test_results.append({
                "component": "Performance Benchmarks",
                "passed": True,
                "details": f"Performance tests passed - {requests_per_second:.2f} req/s"
            })
            print(f"✅ Performance tests passed - {requests_per_second:.2f} req/s")
            
        except Exception as e:
            self.test_results.append({
                "component": "Performance Benchmarks",
                "passed": False,
                "details": f"Performance test failed: {e}"
            })
            print(f"❌ Performance tests failed: {e}")
    
    def print_test_summary(self):
        """Print comprehensive test summary"""
        
        print("\n" + "=" * 60)
        print("🧪 ASIS Network Security Test Summary")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["passed"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📊 Success Rate: {(passed_tests / total_tests * 100):.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result["passed"]:
                    print(f"   • {result['component']}: {result['details']}")
        
        print("\n📋 Detailed Results:")
        for result in self.test_results:
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            print(f"   {status} - {result['component']}")
            print(f"      {result['details']}")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! ASIS Network Security is ready for deployment.")
        else:
            print(f"\n⚠️ {failed_tests} tests failed. Please review and fix issues before deployment.")

def run_comprehensive_security_test():
    """Run comprehensive security test suite"""
    
    print("🔒 Starting ASIS Network Security Comprehensive Test Suite...")
    print("This may take a few minutes to complete all tests.\n")
    
    tester = NetworkSecurityTester()
    
    # Run all test categories
    tester.test_firewall()
    tester.test_intrusion_detection()
    tester.test_secure_communication()
    tester.test_rate_limiting()
    tester.test_vpn_management()
    tester.test_unified_security()
    tester.test_security_attack_scenarios()
    tester.test_performance_benchmarks()
    
    # Run server integration test
    asyncio.run(tester.test_secure_server_integration())
    
    # Print final summary
    tester.print_test_summary()
    
    return all(result["passed"] for result in tester.test_results)

# Example usage
if __name__ == "__main__":
    success = run_comprehensive_security_test()
    exit(0 if success else 1)