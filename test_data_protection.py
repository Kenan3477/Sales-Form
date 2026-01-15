#!/usr/bin/env python3
"""
ASIS Data Protection Test Suite
Comprehensive testing for the ASIS Data Protection System
"""

import unittest
import tempfile
import shutil
import os
import json
import time
from pathlib import Path
from datetime import datetime
import logging
import sys

# Add current directory to path for imports
sys.path.insert(0, '.')

try:
    from asis_data_protection import (
        ASISDataProtection,
        ASISEncryptionManager,
        ASISBackupSystem,
        ASISDataSanitization,
        BackupMetadata,
        DataClassification
    )
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure asis_data_protection.py is in the current directory")
    sys.exit(1)

# Configure logging for tests
logging.basicConfig(level=logging.WARNING)  # Reduce noise during tests

class TestASISEncryptionManager(unittest.TestCase):
    """Test cases for ASIS Encryption Manager"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.key_storage_path = os.path.join(self.test_dir, "keys")
        self.encryption_manager = ASISEncryptionManager(self.key_storage_path)
        
        # Create test data
        self.test_data = b"This is test data for encryption testing"
        self.test_file = os.path.join(self.test_dir, "test_file.txt")
        with open(self.test_file, 'wb') as f:
            f.write(self.test_data)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_encryption_manager_initialization(self):
        """Test encryption manager initialization"""
        self.assertIsNotNone(self.encryption_manager.master_key)
        self.assertIsNotNone(self.encryption_manager.fernet_cipher)
        self.assertIsNotNone(self.encryption_manager.aes_key)
        self.assertIsNotNone(self.encryption_manager.rsa_private_key)
        self.assertIsNotNone(self.encryption_manager.rsa_public_key)
    
    def test_aes256_encryption_decryption(self):
        """Test AES-256 encryption and decryption"""
        # Encrypt data
        encrypted_data, key_id = self.encryption_manager.encrypt_data_aes256(self.test_data)
        
        self.assertNotEqual(encrypted_data, self.test_data)
        self.assertIsInstance(key_id, str)
        self.assertIn(key_id, self.encryption_manager.data_encryption_keys)
        
        # Decrypt data
        decrypted_data = self.encryption_manager.decrypt_data_aes256(encrypted_data, key_id)
        
        self.assertEqual(decrypted_data, self.test_data)
    
    def test_file_encryption_decryption(self):
        """Test file encryption and decryption"""
        # Encrypt file
        encrypted_path, key_id = self.encryption_manager.encrypt_file(self.test_file)
        
        self.assertTrue(os.path.exists(encrypted_path))
        self.assertTrue(os.path.exists(f"{encrypted_path}.meta"))
        
        # Load metadata
        with open(f"{encrypted_path}.meta", 'r') as f:
            metadata = json.load(f)
        
        self.assertEqual(metadata["key_id"], key_id)
        self.assertEqual(metadata["original_file"], self.test_file)
        
        # Decrypt file
        decrypted_path = os.path.join(self.test_dir, "decrypted_file.txt")
        result_path = self.encryption_manager.decrypt_file(encrypted_path, decrypted_path)
        
        self.assertEqual(result_path, decrypted_path)
        self.assertTrue(os.path.exists(decrypted_path))
        
        # Verify content
        with open(decrypted_path, 'rb') as f:
            decrypted_content = f.read()
        
        self.assertEqual(decrypted_content, self.test_data)
    
    def test_key_rotation(self):
        """Test encryption key rotation"""
        old_aes_key = self.encryption_manager.aes_key
        
        # Rotate keys
        self.encryption_manager.rotate_keys()
        
        # Verify new key is different
        self.assertNotEqual(self.encryption_manager.aes_key, old_aes_key)
    
    def test_encryption_status(self):
        """Test encryption status reporting"""
        status = self.encryption_manager.get_encryption_status()
        
        self.assertIn("master_key_available", status)
        self.assertIn("fernet_cipher_ready", status)
        self.assertIn("aes_key_ready", status)
        self.assertIn("rsa_keys_ready", status)
        self.assertTrue(status["master_key_available"])
        self.assertTrue(status["fernet_cipher_ready"])
        self.assertTrue(status["aes_key_ready"])
        self.assertTrue(status["rsa_keys_ready"])

class TestASISBackupSystem(unittest.TestCase):
    """Test cases for ASIS Backup System"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.backup_path = os.path.join(self.test_dir, "backups")
        self.backup_system = ASISBackupSystem(self.backup_path)
        
        # Create test files to backup
        self.test_files_dir = os.path.join(self.test_dir, "test_data")
        os.makedirs(self.test_files_dir, exist_ok=True)
        
        for i in range(5):
            test_file = os.path.join(self.test_files_dir, f"test_file_{i}.txt")
            with open(test_file, 'w') as f:
                f.write(f"Test data for file {i}")
        
        # Change working directory for backup tests
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_backup_system_initialization(self):
        """Test backup system initialization"""
        self.assertIsNotNone(self.backup_system.encryption_manager)
        self.assertIsInstance(self.backup_system.backup_metadata, list)
        self.assertIsInstance(self.backup_system.backup_policies, dict)
        self.assertGreater(len(self.backup_system.backup_policies), 0)
    
    def test_full_backup_creation(self):
        """Test full backup creation"""
        # Create backup
        backup_id = self.backup_system.create_full_backup("test_full_backup")
        
        self.assertIsInstance(backup_id, str)
        self.assertGreater(len(self.backup_system.backup_metadata), 0)
        
        # Find backup metadata
        backup_metadata = None
        for backup in self.backup_system.backup_metadata:
            if backup.backup_id == backup_id:
                backup_metadata = backup
                break
        
        self.assertIsNotNone(backup_metadata)
        self.assertEqual(backup_metadata.backup_type, "full")
        self.assertTrue(os.path.exists(backup_metadata.backup_path))
    
    def test_incremental_backup_creation(self):
        """Test incremental backup creation"""
        # First create a full backup
        full_backup_id = self.backup_system.create_full_backup("test_full_for_incremental")
        
        # Wait a moment to ensure timestamp difference
        time.sleep(1)
        
        # Modify a file
        test_file = os.path.join(self.test_files_dir, "test_file_0.txt")
        with open(test_file, 'a') as f:
            f.write("\nAdditional content for incremental test")
        
        # Create incremental backup
        incremental_backup_id = self.backup_system.create_incremental_backup(
            full_backup_id, "test_incremental_backup"
        )
        
        self.assertIsInstance(incremental_backup_id, str)
        self.assertNotEqual(incremental_backup_id, full_backup_id)
        
        # Find incremental backup metadata
        incremental_metadata = None
        for backup in self.backup_system.backup_metadata:
            if backup.backup_id == incremental_backup_id:
                incremental_metadata = backup
                break
        
        self.assertIsNotNone(incremental_metadata)
        self.assertEqual(incremental_metadata.backup_type, "incremental")
    
    def test_backup_restore(self):
        """Test backup restoration"""
        # Create backup
        backup_id = self.backup_system.create_full_backup("test_restore_backup")
        
        # Create restore directory
        restore_path = os.path.join(self.test_dir, "restore_test")
        
        # Restore backup
        success = self.backup_system.restore_backup(backup_id, restore_path)
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(restore_path))
    
    def test_backup_cleanup(self):
        """Test backup cleanup"""
        initial_backup_count = len(self.backup_system.backup_metadata)
        
        # Create a test backup
        backup_id = self.backup_system.create_full_backup("test_cleanup_backup")
        
        self.assertEqual(len(self.backup_system.backup_metadata), initial_backup_count + 1)
        
        # Cleanup (this won't remove the backup since it's recent, but tests the function)
        self.backup_system.cleanup_old_backups()
        
        # Backup should still exist since it's new
        self.assertEqual(len(self.backup_system.backup_metadata), initial_backup_count + 1)
    
    def test_backup_status(self):
        """Test backup status reporting"""
        status = self.backup_system.get_backup_status()
        
        self.assertIn("total_backups", status)
        self.assertIn("total_size", status)
        self.assertIn("backup_types", status)
        self.assertIn("storage_path", status)
        self.assertIn("encryption_available", status)

class TestASISDataSanitization(unittest.TestCase):
    """Test cases for ASIS Data Sanitization"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.sanitization = ASISDataSanitization()
        
        # Create test files
        self.test_file = os.path.join(self.test_dir, "test_sanitize.txt")
        with open(self.test_file, 'w') as f:
            f.write("Sensitive data to be sanitized")
        
        self.test_dir_files = os.path.join(self.test_dir, "sanitize_dir")
        os.makedirs(self.test_dir_files, exist_ok=True)
        
        for i in range(3):
            test_file = os.path.join(self.test_dir_files, f"file_{i}.txt")
            with open(test_file, 'w') as f:
                f.write(f"Content for file {i}")
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_simple_delete_sanitization(self):
        """Test simple delete sanitization"""
        # File should exist initially
        self.assertTrue(os.path.exists(self.test_file))
        
        # Sanitize file
        result = self.sanitization.sanitize_file(self.test_file, "simple_delete")
        
        self.assertTrue(result)
        self.assertFalse(os.path.exists(self.test_file))
    
    def test_secure_overwrite_sanitization(self):
        """Test secure overwrite sanitization"""
        # Create a copy for testing since secure overwrite will delete the file
        test_file_copy = os.path.join(self.test_dir, "test_secure_overwrite.txt")
        shutil.copy2(self.test_file, test_file_copy)
        
        # File should exist initially
        self.assertTrue(os.path.exists(test_file_copy))
        
        # Sanitize file
        result = self.sanitization.sanitize_file(test_file_copy, "secure_overwrite")
        
        self.assertTrue(result)
        self.assertFalse(os.path.exists(test_file_copy))
    
    def test_crypto_erase_sanitization(self):
        """Test cryptographic erasure sanitization"""
        # Create a copy for testing
        test_file_copy = os.path.join(self.test_dir, "test_crypto_erase.txt")
        shutil.copy2(self.test_file, test_file_copy)
        
        # File should exist initially
        self.assertTrue(os.path.exists(test_file_copy))
        
        # Sanitize file
        result = self.sanitization.sanitize_file(test_file_copy, "crypto_erase")
        
        self.assertTrue(result)
        self.assertFalse(os.path.exists(test_file_copy))
    
    def test_directory_sanitization(self):
        """Test directory sanitization"""
        # Verify files exist initially
        self.assertTrue(os.path.exists(self.test_dir_files))
        file_count = len(list(Path(self.test_dir_files).glob("*")))
        self.assertGreater(file_count, 0)
        
        # Sanitize directory
        sanitized_count = self.sanitization.sanitize_directory(
            self.test_dir_files, "simple_delete", recursive=True
        )
        
        self.assertEqual(sanitized_count, file_count)
    
    def test_sanitization_log(self):
        """Test sanitization logging"""
        initial_log_count = len(self.sanitization.get_sanitization_log())
        
        # Sanitize a file
        self.sanitization.sanitize_file(self.test_file, "simple_delete")
        
        # Check log was updated
        log_entries = self.sanitization.get_sanitization_log()
        self.assertEqual(len(log_entries), initial_log_count + 1)
        
        # Verify log entry structure
        last_entry = log_entries[-1]
        self.assertIn("timestamp", last_entry)
        self.assertIn("file_path", last_entry)
        self.assertIn("method", last_entry)
        self.assertIn("status", last_entry)

class TestASISDataProtection(unittest.TestCase):
    """Test cases for comprehensive ASIS Data Protection"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create test data structure
        self.create_test_data_structure()
        
        # Initialize data protection
        self.data_protection = ASISDataProtection(os.path.join(self.test_dir, "asis"))
    
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def create_test_data_structure(self):
        """Create test data structure"""
        # Create directories
        os.makedirs("var/lib/asis", exist_ok=True)
        os.makedirs("var/log/asis/security", exist_ok=True)
        os.makedirs("etc/asis", exist_ok=True)
        
        # Create test files
        with open("var/lib/asis/test.db", 'w') as f:
            f.write("Test database content")
        
        with open("var/log/asis/security/test.log", 'w') as f:
            f.write("Test security log content")
        
        with open("etc/asis/config.conf", 'w') as f:
            f.write("Test configuration content")
    
    def test_data_protection_initialization(self):
        """Test data protection system initialization"""
        self.assertIsNotNone(self.data_protection.encryption_manager)
        self.assertIsNotNone(self.data_protection.backup_system)
        self.assertIsNotNone(self.data_protection.data_sanitization)
        self.assertIsInstance(self.data_protection.protection_policies, dict)
    
    def test_aes256_encryption_implementation(self):
        """Test AES-256 encryption implementation"""
        result = self.data_protection.implement_aes_256_encryption()
        
        # Should return True if any files were encrypted
        self.assertIsInstance(result, bool)
        
        # Check protection status
        self.assertTrue(self.data_protection.protection_status["encryption_active"])
    
    def test_secure_backup_setup(self):
        """Test secure backup system setup"""
        result = self.data_protection.setup_secure_backups()
        
        self.assertTrue(result)
        self.assertTrue(self.data_protection.protection_status["backup_active"])
        
        # Verify backup was created
        backup_status = self.data_protection.backup_system.get_backup_status()
        self.assertGreater(backup_status["total_backups"], 0)
    
    def test_data_sanitization_setup(self):
        """Test data sanitization setup"""
        result = self.data_protection.setup_data_sanitization()
        
        self.assertTrue(result)
        self.assertTrue(self.data_protection.protection_status["sanitization_active"])
    
    def test_data_integrity_check(self):
        """Test data integrity check"""
        integrity_report = self.data_protection.perform_data_integrity_check()
        
        self.assertIn("timestamp", integrity_report)
        self.assertIn("checks_performed", integrity_report)
        self.assertIn("issues_found", integrity_report)
        self.assertIn("overall_status", integrity_report)
        self.assertIn(integrity_report["overall_status"], ["healthy", "warning", "critical", "error"])
    
    def test_emergency_backup_creation(self):
        """Test emergency backup creation"""
        backup_id = self.data_protection.create_emergency_backup()
        
        self.assertIsInstance(backup_id, str)
        self.assertGreater(len(backup_id), 0)
    
    def test_protection_status_reporting(self):
        """Test protection status reporting"""
        status = self.data_protection.get_protection_status()
        
        self.assertIn("protection_status", status)
        self.assertIn("encryption_status", status)
        self.assertIn("backup_status", status)
        self.assertIn("protection_policies", status)
        self.assertIn("system_info", status)

class TestDataProtectionIntegration(unittest.TestCase):
    """Integration tests for data protection components"""
    
    def setUp(self):
        """Set up integration test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create realistic test environment
        self.create_realistic_test_environment()
    
    def tearDown(self):
        """Clean up integration test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def create_realistic_test_environment(self):
        """Create realistic test environment"""
        # Create ASIS directory structure
        directories = [
            "var/lib/asis",
            "var/lib/asis/users",
            "var/log/asis/security",
            "etc/asis",
            "etc/asis/ssl"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        # Create test files
        test_files = {
            "var/lib/asis/main.db": "Main database content",
            "var/lib/asis/users/user1.json": '{"user": "test1", "role": "admin"}',
            "var/lib/asis/users/user2.json": '{"user": "test2", "role": "user"}',
            "var/log/asis/security/audit.log": "2024-01-01 10:00:00 - Login attempt",
            "etc/asis/config.yaml": "security:\n  level: high",
            "etc/asis/ssl/cert.pem": "-----BEGIN CERTIFICATE-----\ntest\n-----END CERTIFICATE-----"
        }
        
        for file_path, content in test_files.items():
            with open(file_path, 'w') as f:
                f.write(content)
    
    def test_end_to_end_protection_workflow(self):
        """Test complete end-to-end protection workflow"""
        # Initialize data protection
        data_protection = ASISDataProtection()
        
        # Step 1: Setup encryption
        encryption_result = data_protection.implement_aes_256_encryption()
        self.assertIsInstance(encryption_result, bool)
        
        # Step 2: Setup backups
        backup_result = data_protection.setup_secure_backups()
        self.assertTrue(backup_result)
        
        # Step 3: Setup sanitization
        sanitization_result = data_protection.setup_data_sanitization()
        self.assertTrue(sanitization_result)
        
        # Step 4: Perform integrity check
        integrity_report = data_protection.perform_data_integrity_check()
        self.assertIn("overall_status", integrity_report)
        
        # Step 5: Create emergency backup
        emergency_backup_id = data_protection.create_emergency_backup()
        self.assertIsInstance(emergency_backup_id, str)
        
        # Step 6: Verify protection status
        status = data_protection.get_protection_status()
        self.assertTrue(status["protection_status"]["encryption_active"])
        self.assertTrue(status["protection_status"]["backup_active"])
        self.assertTrue(status["protection_status"]["sanitization_active"])
    
    def test_encryption_backup_integration(self):
        """Test integration between encryption and backup systems"""
        data_protection = ASISDataProtection()
        
        # Create and encrypt a test file
        test_file = "test_integration.txt"
        with open(test_file, 'w') as f:
            f.write("Integration test data")
        
        encrypted_path, key_id = data_protection.encryption_manager.encrypt_file(test_file)
        
        # Create backup that includes encrypted file
        backup_id = data_protection.backup_system.create_full_backup("integration_test")
        
        # Verify backup exists and contains data
        backup_status = data_protection.backup_system.get_backup_status()
        self.assertGreater(backup_status["total_backups"], 0)
        
        # Test restore workflow
        restore_path = os.path.join(self.test_dir, "integration_restore")
        restore_success = data_protection.backup_system.restore_backup(backup_id, restore_path)
        self.assertTrue(restore_success)

def run_performance_tests():
    """Run performance tests for data protection system"""
    print("🚀 Running performance tests...")
    
    test_dir = tempfile.mkdtemp()
    original_cwd = os.getcwd()
    
    try:
        os.chdir(test_dir)
        
        # Create large test dataset
        print("📊 Creating test dataset...")
        os.makedirs("var/lib/asis", exist_ok=True)
        
        # Create multiple test files
        for i in range(10):
            test_file = f"var/lib/asis/large_file_{i}.txt"
            with open(test_file, 'w') as f:
                # Write 1MB of test data
                f.write("x" * (1024 * 1024))
        
        # Test encryption performance
        print("🔐 Testing encryption performance...")
        data_protection = ASISDataProtection()
        
        start_time = time.time()
        data_protection.implement_aes_256_encryption()
        encryption_time = time.time() - start_time
        
        print(f"   Encryption time: {encryption_time:.2f} seconds")
        
        # Test backup performance
        print("📦 Testing backup performance...")
        start_time = time.time()
        backup_id = data_protection.backup_system.create_full_backup("performance_test")
        backup_time = time.time() - start_time
        
        print(f"   Backup time: {backup_time:.2f} seconds")
        
        # Test integrity check performance
        print("🔍 Testing integrity check performance...")
        start_time = time.time()
        integrity_report = data_protection.perform_data_integrity_check()
        integrity_time = time.time() - start_time
        
        print(f"   Integrity check time: {integrity_time:.2f} seconds")
        
        print("✅ Performance tests completed successfully")
        
    finally:
        os.chdir(original_cwd)
        shutil.rmtree(test_dir)

if __name__ == "__main__":
    print("🧪 ASIS Data Protection Test Suite")
    print("=" * 50)
    
    # Configure test runner
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestASISEncryptionManager,
        TestASISBackupSystem,
        TestASISDataSanitization,
        TestASISDataProtection,
        TestDataProtectionIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Run performance tests
    if result.wasSuccessful():
        print("\n" + "=" * 50)
        run_performance_tests()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("✅ All tests passed successfully!")
        print("🔒 ASIS Data Protection System is ready for deployment")
    else:
        print("❌ Some tests failed")
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback}")
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"  - {test}: {traceback}")
    
    print("\n🛡️ ASIS Data Protection testing complete!")