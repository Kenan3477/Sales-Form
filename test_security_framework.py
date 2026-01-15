#!/usr/bin/env python3
"""
ASIS Security Framework Test Suite
Comprehensive testing of security components
"""

import sys
import os
import time
import json
import tempfile
import shutil
from datetime import datetime, timedelta

# Add current directory to path for testing
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from asis_security_framework import (
        ASISSecurityFramework, SecurityLevel, AccessPermission, 
        AuditEventType, EncryptionManager, AuthenticationSystem
    )
    print("✅ Successfully imported ASIS Security Framework")
except ImportError as e:
    print(f"❌ Failed to import security framework: {e}")
    sys.exit(1)

class SecurityFrameworkTester:
    """Test suite for ASIS Security Framework"""
    
    def __init__(self):
        self.test_dir = tempfile.mkdtemp(prefix="asis_test_")
        self.passed_tests = 0
        self.failed_tests = 0
        self.test_results = []
        
        print(f"🧪 Testing in temporary directory: {self.test_dir}")
        
        # Change to test directory
        os.chdir(self.test_dir)
        
        # Create test directories
        os.makedirs("var/lib/asis", exist_ok=True)
        os.makedirs("var/log/asis", exist_ok=True)
        os.makedirs("etc/asis/ssl", exist_ok=True)
    
    def run_test(self, test_name, test_function):
        """Run individual test and track results"""
        print(f"\n🔍 Testing: {test_name}")
        try:
            start_time = time.time()
            result = test_function()
            end_time = time.time()
            
            if result:
                print(f"✅ PASSED: {test_name} ({end_time - start_time:.3f}s)")
                self.passed_tests += 1
                self.test_results.append({"test": test_name, "status": "PASSED", "time": end_time - start_time})
            else:
                print(f"❌ FAILED: {test_name}")
                self.failed_tests += 1
                self.test_results.append({"test": test_name, "status": "FAILED", "time": end_time - start_time})
                
        except Exception as e:
            print(f"❌ ERROR in {test_name}: {e}")
            self.failed_tests += 1
            self.test_results.append({"test": test_name, "status": "ERROR", "error": str(e)})
    
    def test_encryption_manager(self):
        """Test encryption functionality"""
        try:
            em = EncryptionManager()
            
            # Test symmetric encryption
            test_data = "This is sensitive test data! 🔒"
            encrypted = em.encrypt_data(test_data)
            decrypted = em.decrypt_data(encrypted)
            
            if decrypted != test_data:
                print(f"❌ Symmetric encryption failed: {test_data} != {decrypted}")
                return False
            
            # Test password hashing
            password = "TestPassword123!"
            hash1, salt1 = em.hash_password(password)
            hash2, salt2 = em.hash_password(password)
            
            # Hashes should be different (different salts)
            if hash1 == hash2:
                print("❌ Password hashing not using unique salts")
                return False
            
            # Verification should work
            if not em.verify_password(password, hash1):
                print("❌ Password verification failed")
                return False
            
            # Wrong password should fail
            if em.verify_password("WrongPassword", hash1):
                print("❌ Password verification allowing wrong password")
                return False
            
            # Test RSA encryption
            rsa_test_data = "RSA test data"
            rsa_encrypted = em.encrypt_with_rsa(rsa_test_data)
            rsa_decrypted = em.decrypt_with_rsa(rsa_encrypted)
            
            if rsa_decrypted != rsa_test_data:
                print(f"❌ RSA encryption failed: {rsa_test_data} != {rsa_decrypted}")
                return False
            
            print("✅ All encryption tests passed")
            return True
            
        except Exception as e:
            print(f"❌ Encryption test error: {e}")
            return False
    
    def test_authentication_system(self):
        """Test authentication functionality"""
        try:
            em = EncryptionManager()
            auth = AuthenticationSystem(em)
            
            # Test user creation
            username = "test_user"
            password = "SecureTestPassword123!"
            
            success = auth.create_user(
                username=username,
                password=password,
                security_level=SecurityLevel.USER,
                permissions=[AccessPermission.READ, AccessPermission.WRITE],
                ip_whitelist=["127.0.0.1", "192.168.1.0/24"]
            )
            
            if not success:
                print("❌ User creation failed")
                return False
            
            # Test authentication with correct credentials
            token = auth.authenticate_user(username, password, "127.0.0.1")
            if not token:
                print("❌ Authentication with correct credentials failed")
                return False
            
            # Test authentication with wrong password
            wrong_token = auth.authenticate_user(username, "WrongPassword", "127.0.0.1")
            if wrong_token:
                print("❌ Authentication with wrong password succeeded")
                return False
            
            # Test authentication from unauthorized IP
            unauthorized_token = auth.authenticate_user(username, password, "10.0.0.1")
            if unauthorized_token:
                print("❌ Authentication from unauthorized IP succeeded")
                return False
            
            # Test session verification
            verified_user = auth.verify_session(token, "127.0.0.1")
            if verified_user != username:
                print(f"❌ Session verification failed: {verified_user} != {username}")
                return False
            
            # Test session verification with wrong IP
            wrong_ip_user = auth.verify_session(token, "10.0.0.1")
            if wrong_ip_user:
                print("❌ Session verification with wrong IP succeeded")
                return False
            
            print("✅ All authentication tests passed")
            return True
            
        except Exception as e:
            print(f"❌ Authentication test error: {e}")
            return False
    
    def test_access_control(self):
        """Test access control functionality"""
        try:
            security = ASISSecurityFramework()
            
            # Create test users with different levels
            users = [
                ("creator_test", "password", SecurityLevel.CREATOR),
                ("admin_test", "password", SecurityLevel.ADMIN),
                ("user_test", "password", SecurityLevel.USER),
                ("guest_test", "password", SecurityLevel.GUEST)
            ]
            
            for username, password, level in users:
                if level == SecurityLevel.CREATOR:
                    permissions = [AccessPermission.SYSTEM_CONTROL, AccessPermission.ADMIN, 
                                 AccessPermission.DELETE, AccessPermission.WRITE, 
                                 AccessPermission.READ, AccessPermission.EXECUTE]
                elif level == SecurityLevel.ADMIN:
                    permissions = [AccessPermission.ADMIN, AccessPermission.DELETE, 
                                 AccessPermission.WRITE, AccessPermission.READ, AccessPermission.EXECUTE]
                elif level == SecurityLevel.USER:
                    permissions = [AccessPermission.WRITE, AccessPermission.READ, AccessPermission.EXECUTE]
                else:
                    permissions = [AccessPermission.READ]
                
                security.create_user(username, password, level, permissions, ["127.0.0.1"])
            
            # Test access control scenarios
            test_cases = [
                ("creator_test", "asis_core", AccessPermission.SYSTEM_CONTROL, True),
                ("admin_test", "asis_core", AccessPermission.SYSTEM_CONTROL, False),
                ("admin_test", "user_data", AccessPermission.ADMIN, True),
                ("user_test", "user_data", AccessPermission.WRITE, True),
                ("user_test", "system_config", AccessPermission.ADMIN, False),
                ("guest_test", "user_data", AccessPermission.READ, True),
                ("guest_test", "user_data", AccessPermission.WRITE, False)
            ]
            
            for username, resource, action, expected in test_cases:
                # Authenticate user
                token = security.authenticate_user(username, "password", "127.0.0.1")
                if not token:
                    print(f"❌ Failed to authenticate {username}")
                    return False
                
                # Check access
                has_access = security.verify_access(token, "127.0.0.1", resource, action)
                
                if has_access != expected:
                    print(f"❌ Access control failed: {username} -> {resource}:{action.value} expected {expected}, got {has_access}")
                    return False
            
            print("✅ All access control tests passed")
            return True
            
        except Exception as e:
            print(f"❌ Access control test error: {e}")
            return False
    
    def test_audit_logging(self):
        """Test audit logging functionality"""
        try:
            em = EncryptionManager()
            
            # Mock the database path to use test directory
            import asis_security_framework
            original_audit_db = asis_security_framework.AuditLogger.__init__
            
            def mock_audit_init(self, encryption_manager):
                self.encryption_manager = encryption_manager
                self.db_path = os.path.join(os.getcwd(), "audit_test.db")
                self._initialize_audit_database()
                
                # Setup minimal logging
                import logging
                self.logger = logging.getLogger('test_audit')
                self.logger.setLevel(logging.INFO)
            
            asis_security_framework.AuditLogger.__init__ = mock_audit_init
            
            from asis_security_framework import AuditLogger
            
            audit = AuditLogger(em)
            
            # Test event logging
            test_events = [
                (AuditEventType.LOGIN_SUCCESS, "test_user", "127.0.0.1", "auth", "login", "success"),
                (AuditEventType.ACCESS_GRANTED, "test_user", "127.0.0.1", "data", "read", "granted"),
                (AuditEventType.SECURITY_VIOLATION, "attacker", "10.0.0.1", "system", "hack", "blocked")
            ]
            
            for event_type, username, ip, resource, action, result in test_events:
                audit.log_event(event_type, username, ip, resource, action, result, {"test": True})
            
            # Verify events were logged
            import sqlite3
            conn = sqlite3.connect(audit.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM audit_events")
            count = cursor.fetchone()[0]
            conn.close()
            
            if count != len(test_events):
                print(f"❌ Expected {len(test_events)} audit events, found {count}")
                return False
            
            # Restore original method
            asis_security_framework.AuditLogger.__init__ = original_audit_db
            
            print("✅ All audit logging tests passed")
            return True
            
        except Exception as e:
            print(f"❌ Audit logging test error: {e}")
            return False
    
    def test_session_management(self):
        """Test session management functionality"""
        try:
            em = EncryptionManager()
            auth = AuthenticationSystem(em)
            
            # Create test user
            username = "session_test_user"
            password = "TestPassword123!"
            
            auth.create_user(
                username=username,
                password=password,
                security_level=SecurityLevel.USER,
                permissions=[AccessPermission.READ],
                ip_whitelist=["127.0.0.1"]
            )
            
            # Test session creation
            token1 = auth.authenticate_user(username, password, "127.0.0.1")
            token2 = auth.authenticate_user(username, password, "127.0.0.1")
            
            if not token1 or not token2:
                print("❌ Session creation failed")
                return False
            
            if token1 == token2:
                print("❌ Sessions should be unique")
                return False
            
            # Test concurrent sessions
            user1 = auth.verify_session(token1, "127.0.0.1")
            user2 = auth.verify_session(token2, "127.0.0.1")
            
            if user1 != username or user2 != username:
                print("❌ Concurrent session verification failed")
                return False
            
            print("✅ All session management tests passed")
            return True
            
        except Exception as e:
            print(f"❌ Session management test error: {e}")
            return False
    
    def test_security_framework_integration(self):
        """Test full security framework integration"""
        try:
            security = ASISSecurityFramework()
            
            # Test all security measures
            security.implement_zero_trust_architecture()
            security.setup_end_to_end_encryption()
            security.configure_role_based_access()
            
            # Test default creator user
            token = security.authenticate_user("creator_kenandavies", "SkyeAlbert2025!", "127.0.0.1")
            if not token:
                print("❌ Default creator authentication failed")
                return False
            
            # Test creator access
            has_access = security.verify_access(token, "127.0.0.1", "asis_core", AccessPermission.SYSTEM_CONTROL)
            if not has_access:
                print("❌ Creator access verification failed")
                return False
            
            # Test security status
            status = security.get_security_status()
            required_fields = ["active_sessions", "encryption_status", "firewall_status", 
                             "ssl_status", "audit_logging", "zero_trust"]
            
            for field in required_fields:
                if field not in status:
                    print(f"❌ Security status missing field: {field}")
                    return False
            
            print("✅ All integration tests passed")
            return True
            
        except Exception as e:
            print(f"❌ Integration test error: {e}")
            return False
    
    def test_security_edge_cases(self):
        """Test security edge cases and attack scenarios"""
        try:
            security = ASISSecurityFramework()
            
            # Test SQL injection attempts (should be prevented by parameterized queries)
            malicious_usernames = [
                "'; DROP TABLE users; --",
                "admin' OR '1'='1",
                "test\"; DELETE FROM users WHERE 1=1; --"
            ]
            
            for username in malicious_usernames:
                token = security.authenticate_user(username, "password", "127.0.0.1")
                if token:
                    print(f"❌ SQL injection attack succeeded with username: {username}")
                    return False
            
            # Test password brute force protection
            for i in range(5):  # Exceed max attempts
                token = security.authenticate_user("nonexistent", "wrong", "127.0.0.1")
                if token:
                    print("❌ Brute force attack succeeded")
                    return False
            
            # Test very long inputs
            long_string = "A" * 10000
            token = security.authenticate_user(long_string, long_string, "127.0.0.1")
            if token:
                print("❌ Long input attack succeeded")
                return False
            
            print("✅ All security edge case tests passed")
            return True
            
        except Exception as e:
            print(f"❌ Security edge case test error: {e}")
            return False
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🔒 ASIS Security Framework Test Suite")
        print("=" * 50)
        
        test_suite = [
            ("Encryption Manager", self.test_encryption_manager),
            ("Authentication System", self.test_authentication_system),
            ("Access Control", self.test_access_control),
            ("Audit Logging", self.test_audit_logging),
            ("Session Management", self.test_session_management),
            ("Framework Integration", self.test_security_framework_integration),
            ("Security Edge Cases", self.test_security_edge_cases)
        ]
        
        start_time = time.time()
        
        for test_name, test_function in test_suite:
            self.run_test(test_name, test_function)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Print summary
        print("\n" + "=" * 50)
        print("🧪 TEST SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {self.passed_tests + self.failed_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"⏱️ Total Time: {total_time:.3f}s")
        print(f"📊 Success Rate: {(self.passed_tests / (self.passed_tests + self.failed_tests) * 100):.1f}%")
        
        if self.failed_tests == 0:
            print("\n🎉 ALL TESTS PASSED! Security framework is ready for deployment.")
            return True
        else:
            print(f"\n⚠️ {self.failed_tests} tests failed. Please review and fix issues before deployment.")
            return False
    
    def cleanup(self):
        """Clean up test environment"""
        try:
            os.chdir("/")
            shutil.rmtree(self.test_dir)
            print(f"🧹 Cleaned up test directory: {self.test_dir}")
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")

def main():
    """Main test execution"""
    tester = SecurityFrameworkTester()
    
    try:
        success = tester.run_all_tests()
        return 0 if success else 1
    
    except KeyboardInterrupt:
        print("\n⏹️ Test suite interrupted by user")
        return 1
    
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        return 1
    
    finally:
        tester.cleanup()

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)