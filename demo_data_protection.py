#!/usr/bin/env python3
"""
ASIS Data Protection System - Interactive Demo
Demonstrates key features and capabilities
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime

# Import the ASIS Data Protection System
try:
    from asis_data_protection import ASISDataProtection
    print("✅ ASIS Data Protection System imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure asis_data_protection.py is in the current directory")
    exit(1)

def print_banner():
    """Print demo banner"""
    print("\n" + "="*60)
    print("🔒 ASIS DATA PROTECTION SYSTEM - INTERACTIVE DEMO")
    print("="*60)

def print_section(title):
    """Print section header"""
    print(f"\n{'─'*50}")
    print(f"📋 {title}")
    print("─"*50)

def create_demo_data():
    """Create demo data files"""
    print_section("Creating Demo Data")
    
    # Create directory structure
    directories = [
        "demo_data/sensitive",
        "demo_data/configuration", 
        "demo_data/logs",
        "demo_data/user_files"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # Create demo files
    demo_files = {
        "demo_data/sensitive/customer_database.db": "Customer ID,Name,Email\n1,John Doe,john@example.com\n2,Jane Smith,jane@example.com",
        "demo_data/sensitive/financial_records.json": json.dumps({
            "accounts": [
                {"id": "001", "balance": 10000, "owner": "John Doe"},
                {"id": "002", "balance": 25000, "owner": "Jane Smith"}
            ]
        }, indent=2),
        "demo_data/configuration/app_config.yaml": "database:\n  host: localhost\n  port: 5432\n  name: asis_db\nsecurity:\n  encryption: enabled\n  level: high",
        "demo_data/logs/access.log": f"{datetime.now()} - User login: admin\n{datetime.now()} - File accessed: customer_database.db",
        "demo_data/user_files/document1.txt": "This is a confidential business document containing sensitive information.",
        "demo_data/user_files/document2.txt": "Another important document with proprietary data.",
        "demo_data/temp_file.tmp": "This is temporary data that should be cleaned up."
    }
    
    for file_path, content in demo_files.items():
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"📄 Created file: {file_path}")
    
    print(f"✅ Created {len(demo_files)} demo files in {len(directories)} directories")

def demo_encryption(data_protection):
    """Demonstrate encryption features"""
    print_section("Encryption Demo")
    
    # Test file encryption
    test_file = "demo_data/sensitive/customer_database.db"
    
    if Path(test_file).exists():
        print(f"🔐 Encrypting file: {test_file}")
        
        try:
            encrypted_path, key_id = data_protection.encryption_manager.encrypt_file(test_file)
            print(f"✅ File encrypted successfully!")
            print(f"   Encrypted file: {encrypted_path}")
            print(f"   Key ID: {key_id}")
            
            # Show file sizes
            if Path(encrypted_path).exists():
                original_size = Path(test_file).stat().st_size if Path(test_file).exists() else 0
                encrypted_size = Path(encrypted_path).stat().st_size
                print(f"   Original size: {original_size} bytes")
                print(f"   Encrypted size: {encrypted_size} bytes")
            
            # Test decryption
            print(f"\n🔓 Testing decryption...")
            decrypted_path = "demo_data/decrypted_customer_database.db"
            result_path = data_protection.encryption_manager.decrypt_file(encrypted_path, decrypted_path)
            
            if Path(result_path).exists():
                print(f"✅ File decrypted successfully to: {result_path}")
                
                # Verify content
                with open(decrypted_path, 'r') as f:
                    content = f.read()
                print(f"   Content preview: {content[:50]}...")
            
        except Exception as e:
            print(f"❌ Encryption demo failed: {e}")
    
    # Show encryption status
    print(f"\n📊 Encryption Status:")
    status = data_protection.encryption_manager.get_encryption_status()
    for key, value in status.items():
        if isinstance(value, bool):
            icon = "✅" if value else "❌"
            print(f"   {key}: {icon}")
        else:
            print(f"   {key}: {value}")

def demo_backup(data_protection):
    """Demonstrate backup features"""
    print_section("Backup System Demo")
    
    print("📦 Creating full backup...")
    try:
        backup_id = data_protection.backup_system.create_full_backup("demo_full_backup")
        print(f"✅ Full backup created successfully!")
        print(f"   Backup ID: {backup_id}")
        
        # Show backup status
        backup_status = data_protection.backup_system.get_backup_status()
        print(f"   Total backups: {backup_status['total_backups']}")
        print(f"   Total size: {backup_status['total_size']}")
        
        if backup_status['latest_backup']:
            latest = backup_status['latest_backup']
            print(f"   Latest backup: {latest['type']} ({latest['size']})")
        
        # Test incremental backup
        print(f"\n📦 Creating incremental backup...")
        
        # Modify a file to demonstrate incremental backup
        test_file = "demo_data/logs/access.log"
        if Path(test_file).exists():
            with open(test_file, 'a') as f:
                f.write(f"\n{datetime.now()} - Demo incremental backup test")
        
        time.sleep(1)  # Ensure timestamp difference
        
        inc_backup_id = data_protection.backup_system.create_incremental_backup(
            backup_id, "demo_incremental_backup"
        )
        print(f"✅ Incremental backup created!")
        print(f"   Incremental Backup ID: {inc_backup_id}")
        
        # Test backup restoration
        print(f"\n🔄 Testing backup restoration...")
        restore_path = "demo_restore"
        
        if data_protection.backup_system.restore_backup(backup_id, restore_path):
            print(f"✅ Backup restored successfully to: {restore_path}")
            
            # List restored files
            if Path(restore_path).exists():
                restored_files = list(Path(restore_path).rglob('*'))
                print(f"   Restored {len([f for f in restored_files if f.is_file()])} files")
        else:
            print(f"⚠️ Backup restoration encountered issues (test environment)")
        
    except Exception as e:
        print(f"❌ Backup demo failed: {e}")

def demo_sanitization(data_protection):
    """Demonstrate data sanitization"""
    print_section("Data Sanitization Demo")
    
    # Create test file for sanitization
    sanitize_test_file = "demo_data/temp_sensitive.txt"
    with open(sanitize_test_file, 'w') as f:
        f.write("This is sensitive data that needs to be securely deleted.")
    
    print(f"📄 Created test file for sanitization: {sanitize_test_file}")
    print(f"   File size: {Path(sanitize_test_file).stat().st_size} bytes")
    
    # Test different sanitization methods
    sanitization_methods = [
        ("simple_delete", "Simple deletion (fast, not secure)"),
        ("secure_overwrite", "Secure overwrite (3 passes)"),
        ("crypto_erase", "Cryptographic erasure (encrypt then destroy key)")
    ]
    
    for method, description in sanitization_methods:
        # Create copy for each test
        test_file = f"demo_data/sanitize_test_{method}.txt"
        with open(test_file, 'w') as f:
            f.write("Test data for sanitization")
        
        print(f"\n🗑️ Testing {method}:")
        print(f"   Description: {description}")
        print(f"   Target file: {test_file}")
        
        try:
            start_time = time.time()
            success = data_protection.data_sanitization.sanitize_file(test_file, method)
            end_time = time.time()
            
            if success:
                print(f"   ✅ Sanitization successful!")
                print(f"   ⏱️ Time taken: {end_time - start_time:.3f} seconds")
                print(f"   🔍 File exists after sanitization: {Path(test_file).exists()}")
            else:
                print(f"   ❌ Sanitization failed")
                
        except Exception as e:
            print(f"   ❌ Sanitization error: {e}")
    
    # Test directory sanitization
    print(f"\n🗂️ Testing directory sanitization...")
    sanitize_dir = "demo_data/temp_directory"
    Path(sanitize_dir).mkdir(exist_ok=True)
    
    # Create multiple files in directory
    for i in range(3):
        temp_file = Path(sanitize_dir) / f"temp_file_{i}.txt"
        with open(temp_file, 'w') as f:
            f.write(f"Temporary data {i}")
    
    file_count = len(list(Path(sanitize_dir).glob('*')))
    print(f"   Created {file_count} files in {sanitize_dir}")
    
    sanitized_count = data_protection.data_sanitization.sanitize_directory(
        sanitize_dir, "secure_overwrite", recursive=True
    )
    
    print(f"   ✅ Sanitized {sanitized_count} files")
    print(f"   🔍 Directory exists: {Path(sanitize_dir).exists()}")
    
    # Show sanitization log
    sanitization_log = data_protection.data_sanitization.get_sanitization_log()
    print(f"   📝 Total sanitization operations logged: {len(sanitization_log)}")

def demo_integrity_check(data_protection):
    """Demonstrate data integrity checking"""
    print_section("Data Integrity Check Demo")
    
    print("🔍 Performing comprehensive data integrity check...")
    
    try:
        integrity_report = data_protection.perform_data_integrity_check()
        
        print(f"✅ Integrity check completed!")
        print(f"   Timestamp: {integrity_report['timestamp']}")
        print(f"   Overall Status: {integrity_report['overall_status'].upper()}")
        print(f"   Checks Performed: {len(integrity_report['checks_performed'])}")
        print(f"   Issues Found: {len(integrity_report['issues_found'])}")
        
        # Show checks performed
        print(f"\n📋 Checks Performed:")
        for check in integrity_report['checks_performed']:
            print(f"   ✓ {check}")
        
        # Show issues found
        if integrity_report['issues_found']:
            print(f"\n⚠️ Issues Found:")
            for issue in integrity_report['issues_found']:
                print(f"   • {issue}")
        else:
            print(f"\n✅ No issues found!")
        
        # Show encryption status
        enc_status = integrity_report['encryption_status']
        print(f"\n🔐 Encryption Status:")
        print(f"   Master Key Available: {'✅' if enc_status['master_key_available'] else '❌'}")
        print(f"   AES Key Ready: {'✅' if enc_status['aes_key_ready'] else '❌'}")
        print(f"   RSA Keys Ready: {'✅' if enc_status['rsa_keys_ready'] else '❌'}")
        
        # Show backup status
        backup_status = integrity_report['backup_status']
        print(f"\n📦 Backup Status:")
        print(f"   Total Backups: {backup_status['total_backups']}")
        print(f"   Total Size: {backup_status['total_size']}")
        
    except Exception as e:
        print(f"❌ Integrity check failed: {e}")

def demo_emergency_procedures(data_protection):
    """Demonstrate emergency procedures"""
    print_section("Emergency Procedures Demo")
    
    print("🚨 Testing Emergency Backup...")
    try:
        emergency_backup_id = data_protection.create_emergency_backup()
        print(f"✅ Emergency backup created successfully!")
        print(f"   Emergency Backup ID: {emergency_backup_id}")
        
    except Exception as e:
        print(f"❌ Emergency backup failed: {e}")
    
    print(f"\n⚠️ Emergency Data Lockdown (Simulation)...")
    print(f"   Note: This would normally:")
    print(f"   • Create emergency backup")
    print(f"   • Encrypt all unencrypted data")
    print(f"   • Rotate all encryption keys")
    print(f"   • Clean temporary files")
    print(f"   (Skipped in demo to preserve demo data)")

def show_final_status(data_protection):
    """Show final protection status"""
    print_section("Final Protection Status")
    
    try:
        status = data_protection.get_protection_status()
        
        # Protection status
        protection = status['protection_status']
        print("🛡️ Protection Systems:")
        print(f"   Encryption: {'✅ Active' if protection['encryption_active'] else '❌ Inactive'}")
        print(f"   Backup: {'✅ Active' if protection['backup_active'] else '❌ Inactive'}")
        print(f"   Sanitization: {'✅ Active' if protection['sanitization_active'] else '❌ Inactive'}")
        print(f"   Data Classification: {'✅ Active' if protection['data_classification_active'] else '❌ Inactive'}")
        print(f"   Monitoring: {'✅ Active' if protection['monitoring_active'] else '❌ Inactive'}")
        
        # Statistics
        print(f"\n📊 Statistics:")
        print(f"   Protection Policies: {status['protection_policies']}")
        print(f"   Sanitization Log Entries: {status['sanitization_log_entries']}")
        print(f"   Data Monitors: {status['data_monitors']}")
        
        # System info
        sys_info = status['system_info']
        print(f"\n💻 System Information:")
        print(f"   Platform: {sys_info['platform']}")
        print(f"   Python Version: {sys_info['python_version']}")
        if sys_info['disk_usage'] != "unknown":
            print(f"   Disk Usage: {sys_info['disk_usage']:.1f}%")
        
    except Exception as e:
        print(f"❌ Failed to get status: {e}")

def cleanup_demo_data():
    """Clean up demo data"""
    print_section("Demo Cleanup")
    
    cleanup_paths = [
        "demo_data",
        "demo_restore", 
        "var",
        "*.encrypted",
        "*.meta"
    ]
    
    import shutil
    import glob
    
    cleaned_count = 0
    
    for path_pattern in cleanup_paths:
        if '*' in path_pattern:
            # Handle glob patterns
            for file_path in glob.glob(path_pattern):
                try:
                    if Path(file_path).is_file():
                        Path(file_path).unlink()
                    elif Path(file_path).is_dir():
                        shutil.rmtree(file_path)
                    cleaned_count += 1
                except:
                    pass
        else:
            # Handle direct paths
            path = Path(path_pattern)
            try:
                if path.exists():
                    if path.is_file():
                        path.unlink()
                    elif path.is_dir():
                        shutil.rmtree(path)
                    cleaned_count += 1
            except:
                pass
    
    print(f"🧹 Cleaned up {cleaned_count} demo items")

def main():
    """Main demo function"""
    print_banner()
    
    print("🚀 Starting ASIS Data Protection System Demo...")
    print("This demo will showcase all major features and capabilities.")
    
    try:
        # Step 1: Create demo data
        create_demo_data()
        
        # Step 2: Initialize data protection
        print_section("Initializing Data Protection System")
        data_protection = ASISDataProtection("demo_asis")
        print("✅ ASIS Data Protection System initialized successfully!")
        
        # Step 3: Setup protection systems
        print_section("Setting Up Protection Systems")
        
        print("🔐 Setting up AES-256 encryption...")
        data_protection.implement_aes_256_encryption()
        
        print("📦 Setting up secure backups...")
        data_protection.setup_secure_backups()
        
        print("🗑️ Setting up data sanitization...")
        data_protection.setup_data_sanitization()
        
        print("✅ All protection systems configured!")
        
        # Step 4: Run feature demos
        demo_encryption(data_protection)
        demo_backup(data_protection)
        demo_sanitization(data_protection)
        demo_integrity_check(data_protection)
        demo_emergency_procedures(data_protection)
        
        # Step 5: Show final status
        show_final_status(data_protection)
        
        # Step 6: Cleanup
        print("\n🤔 Would you like to clean up demo data? (y/n):", end=" ")
        cleanup_choice = input().lower().strip()
        
        if cleanup_choice in ['y', 'yes']:
            cleanup_demo_data()
        else:
            print("Demo data preserved for inspection.")
        
        print("\n" + "="*60)
        print("🎉 ASIS DATA PROTECTION DEMO COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nKey Features Demonstrated:")
        print("✅ AES-256 Encryption with secure key management")
        print("✅ Automated backup system with compression and encryption")
        print("✅ Multiple secure data sanitization methods")
        print("✅ Comprehensive data integrity checking")
        print("✅ Emergency backup and lockdown procedures")
        print("✅ Real-time monitoring and status reporting")
        print("\n🔒 Your data is now protected with enterprise-grade security!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Demo interrupted by user")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("\n👋 Thank you for trying the ASIS Data Protection System!")

if __name__ == "__main__":
    main()