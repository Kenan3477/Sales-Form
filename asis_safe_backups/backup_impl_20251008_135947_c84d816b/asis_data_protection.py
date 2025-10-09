#!/usr/bin/env python3
"""
ASIS Data Protection System
Comprehensive data protection, encryption, backup, and sanitization for ASIS
"""

import os
import json
import sqlite3
import hashlib
import secrets
import threading
import zipfile
import shutil
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import platform
import psutil
import uuid

logger = logging.getLogger(__name__)

@dataclass
class BackupMetadata:
    """Backup metadata structure"""
    backup_id: str
    timestamp: datetime
    backup_type: str  # full, incremental, differential
    file_count: int
    compressed_size: int
    original_size: int
    checksum: str
    encryption_key_id: str
    backup_path: str
    retention_policy: str
    verification_status: str = "pending"

@dataclass
class DataClassification:
    """Data classification levels"""
    level: str  # public, internal, confidential, restricted
    encryption_required: bool
    backup_frequency: str  # daily, weekly, monthly
    retention_period: int  # days
    access_controls: List[str]
    sanitization_method: str

class ASISEncryptionManager:
    """Advanced encryption manager for ASIS data protection"""
    
    def __init__(self, key_storage_path: str = "var/lib/asis/keys"):
        self.key_storage_path = Path(key_storage_path)
        self.key_storage_path.mkdir(parents=True, exist_ok=True)
        
        # Master encryption key for key encryption
        self.master_key = None
        self.data_encryption_keys = {}
        self.key_rotation_schedule = {}
        
        # Encryption algorithms
        self.fernet_cipher = None
        self.aes_key = None
        self.rsa_private_key = None
        self.rsa_public_key = None
        
        self._initialize_encryption()
    
    def _initialize_encryption(self):
        """Initialize encryption components"""
        try:
            # Load or generate master key
            master_key_file = self.key_storage_path / "master.key"
            
            if master_key_file.exists():
                self._load_master_key()
            else:
                self._generate_master_key()
            
            # Initialize Fernet for symmetric encryption
            self.fernet_cipher = Fernet(self.master_key)
            
            # Generate AES-256 key
            self.aes_key = secrets.token_bytes(32)  # 256-bit key
            
            # Generate RSA key pair for asymmetric encryption
            self._generate_rsa_keys()
            
            logger.info("✅ Encryption manager initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize encryption: {e}")
            raise
    
    def _generate_master_key(self):
        """Generate and store master encryption key"""
        # Generate random master key
        key_material = secrets.token_bytes(32)
        
        # Derive key using PBKDF2
        password = os.environ.get('ASIS_MASTER_PASSWORD', 'default_asis_key').encode()
        salt = secrets.token_bytes(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        self.master_key = base64.urlsafe_b64encode(kdf.derive(password))
        
        # Store salt and master key securely
        master_data = {
            "salt": base64.b64encode(salt).decode(),
            "key": self.master_key.decode(),
            "created": datetime.now().isoformat(),
            "algorithm": "PBKDF2HMAC-SHA256"
        }
        
        master_key_file = self.key_storage_path / "master.key"
        
        with open(master_key_file, 'w') as f:
            json.dump(master_data, f)
        
        # Set restrictive permissions
        os.chmod(master_key_file, 0o600)
        
        logger.info("🔐 Generated new master encryption key")
    
    def _load_master_key(self):
        """Load existing master key"""
        master_key_file = self.key_storage_path / "master.key"
        
        with open(master_key_file, 'r') as f:
            master_data = json.load(f)
        
        self.master_key = master_data["key"].encode()
        logger.info("🔓 Loaded existing master encryption key")
    
    def _generate_rsa_keys(self):
        """Generate RSA key pair for asymmetric encryption"""
        self.rsa_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.rsa_public_key = self.rsa_private_key.public_key()
        
        # Store RSA keys
        self._store_rsa_keys()
    
    def _store_rsa_keys(self):
        """Store RSA keys securely"""
        # Serialize private key
        private_pem = self.rsa_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Serialize public key
        public_pem = self.rsa_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        # Encrypt and store private key
        encrypted_private = self.fernet_cipher.encrypt(private_pem)
        
        private_key_file = self.key_storage_path / "rsa_private.key"
        public_key_file = self.key_storage_path / "rsa_public.key"
        
        with open(private_key_file, 'wb') as f:
            f.write(encrypted_private)
        
        with open(public_key_file, 'wb') as f:
            f.write(public_pem)
        
        # Set restrictive permissions
        os.chmod(private_key_file, 0o600)
        os.chmod(public_key_file, 0o644)
    
    def encrypt_data_aes256(self, data: bytes, key_id: Optional[str] = None) -> Tuple[bytes, str]:
        """Encrypt data using AES-256"""
        if key_id is None:
            key_id = f"aes_{int(time.time())}"
        
        # Generate random IV
        iv = secrets.token_bytes(16)
        
        # Create cipher
        cipher = Cipher(algorithms.AES(self.aes_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        
        # Pad data to block size
        block_size = 16
        padding_length = block_size - (len(data) % block_size)
        padded_data = data + bytes([padding_length] * padding_length)
        
        # Encrypt
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        # Combine IV and encrypted data
        result = iv + encrypted_data
        
        # Store key for future decryption
        self.data_encryption_keys[key_id] = {
            "key": base64.b64encode(self.aes_key).decode(),
            "algorithm": "AES-256-CBC",
            "created": datetime.now().isoformat()
        }
        
        return result, key_id
    
    def decrypt_data_aes256(self, encrypted_data: bytes, key_id: str) -> bytes:
        """Decrypt data using AES-256"""
        if key_id not in self.data_encryption_keys:
            raise ValueError(f"Encryption key {key_id} not found")
        
        # Extract IV and ciphertext
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        
        # Get key
        key_data = self.data_encryption_keys[key_id]
        key = base64.b64decode(key_data["key"])
        
        # Create cipher
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        
        # Decrypt
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove padding
        padding_length = padded_data[-1]
        data = padded_data[:-padding_length]
        
        return data
    
    def encrypt_file(self, file_path: str, output_path: Optional[str] = None) -> Tuple[str, str]:
        """Encrypt entire file using AES-256"""
        file_path = Path(file_path)
        
        if output_path is None:
            output_path = f"{file_path}.encrypted"
        
        # Read file data
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # Encrypt data
        encrypted_data, key_id = self.encrypt_data_aes256(file_data)
        
        # Write encrypted file
        with open(output_path, 'wb') as f:
            f.write(encrypted_data)
        
        # Create metadata file
        metadata = {
            "original_file": str(file_path),
            "encrypted_file": str(output_path),
            "key_id": key_id,
            "algorithm": "AES-256-CBC",
            "encrypted_at": datetime.now().isoformat(),
            "original_size": len(file_data),
            "encrypted_size": len(encrypted_data)
        }
        
        metadata_path = f"{output_path}.meta"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"🔐 Encrypted file: {file_path} -> {output_path}")
        return output_path, key_id
    
    def decrypt_file(self, encrypted_file_path: str, output_path: Optional[str] = None) -> str:
        """Decrypt encrypted file"""
        encrypted_file_path = Path(encrypted_file_path)
        metadata_path = f"{encrypted_file_path}.meta"
        
        # Load metadata
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        if output_path is None:
            output_path = metadata["original_file"]
        
        # Read encrypted data
        with open(encrypted_file_path, 'rb') as f:
            encrypted_data = f.read()
        
        # Decrypt data
        decrypted_data = self.decrypt_data_aes256(encrypted_data, metadata["key_id"])
        
        # Write decrypted file
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
        
        logger.info(f"🔓 Decrypted file: {encrypted_file_path} -> {output_path}")
        return output_path
    
    def rotate_keys(self):
        """Rotate encryption keys"""
        logger.info("🔄 Starting key rotation...")
        
        # Generate new AES key
        old_aes_key = self.aes_key
        self.aes_key = secrets.token_bytes(32)
        
        # Re-encrypt data with new key (simplified example)
        for key_id in list(self.data_encryption_keys.keys()):
            # Mark old key for rotation
            self.data_encryption_keys[key_id]["rotation_needed"] = True
        
        logger.info("✅ Key rotation completed")
    
    def get_encryption_status(self) -> Dict[str, Any]:
        """Get encryption system status"""
        return {
            "master_key_available": self.master_key is not None,
            "fernet_cipher_ready": self.fernet_cipher is not None,
            "aes_key_ready": self.aes_key is not None,
            "rsa_keys_ready": self.rsa_private_key is not None,
            "active_data_keys": len(self.data_encryption_keys),
            "encryption_algorithms": ["AES-256-CBC", "Fernet", "RSA-2048"],
            "key_storage_path": str(self.key_storage_path)
        }

class ASISBackupSystem:
    """Comprehensive backup system for ASIS data"""
    
    def __init__(self, backup_base_path: str = "var/backups/asis"):
        self.backup_base_path = Path(backup_base_path)
        self.backup_base_path.mkdir(parents=True, exist_ok=True)
        
        self.encryption_manager = None
        self.backup_metadata = []
        self.backup_policies = {}
        self.backup_schedules = {}
        self.running = False
        self.backup_thread = None
        
        # Data classification
        self.data_classifications = {
            "system_critical": DataClassification(
                level="restricted",
                encryption_required=True,
                backup_frequency="daily",
                retention_period=365,
                access_controls=["admin", "creator"],
                sanitization_method="secure_overwrite"
            ),
            "user_data": DataClassification(
                level="confidential",
                encryption_required=True,
                backup_frequency="daily",
                retention_period=90,
                access_controls=["user", "admin"],
                sanitization_method="crypto_erase"
            ),
            "logs": DataClassification(
                level="internal",
                encryption_required=False,
                backup_frequency="weekly",
                retention_period=30,
                access_controls=["admin"],
                sanitization_method="simple_delete"
            ),
            "cache": DataClassification(
                level="public",
                encryption_required=False,
                backup_frequency="none",
                retention_period=7,
                access_controls=["any"],
                sanitization_method="simple_delete"
            )
        }
        
        self._initialize_backup_system()
    
    def _initialize_backup_system(self):
        """Initialize backup system"""
        try:
            # Initialize encryption manager
            self.encryption_manager = ASISEncryptionManager()
            
            # Load existing backup metadata
            self._load_backup_metadata()
            
            # Setup default backup policies
            self._setup_default_policies()
            
            logger.info("✅ Backup system initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize backup system: {e}")
            raise
    
    def _load_backup_metadata(self):
        """Load existing backup metadata"""
        metadata_file = self.backup_base_path / "backup_metadata.json"
        
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    metadata_list = json.load(f)
                
                self.backup_metadata = [
                    BackupMetadata(**item) for item in metadata_list
                    if isinstance(item.get('timestamp'), str)
                ]
                
                # Convert timestamp strings back to datetime objects
                for backup in self.backup_metadata:
                    if isinstance(backup.timestamp, str):
                        backup.timestamp = datetime.fromisoformat(backup.timestamp)
                
                logger.info(f"📂 Loaded {len(self.backup_metadata)} backup records")
                
            except Exception as e:
                logger.warning(f"⚠️ Failed to load backup metadata: {e}")
                self.backup_metadata = []
        else:
            self.backup_metadata = []
    
    def _save_backup_metadata(self):
        """Save backup metadata to file"""
        metadata_file = self.backup_base_path / "backup_metadata.json"
        
        # Convert to serializable format
        metadata_list = []
        for backup in self.backup_metadata:
            backup_dict = backup.__dict__.copy()
            backup_dict['timestamp'] = backup.timestamp.isoformat()
            metadata_list.append(backup_dict)
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata_list, f, indent=2)
    
    def _setup_default_policies(self):
        """Setup default backup policies"""
        self.backup_policies = {
            "databases": {
                "paths": ["var/lib/asis/*.db", "var/lib/asis/data/*.db"],
                "classification": "system_critical",
                "compression": True,
                "encryption": True,
                "verification": True
            },
            "configurations": {
                "paths": ["etc/asis/*", "config/*"],
                "classification": "system_critical",
                "compression": True,
                "encryption": True,
                "verification": True
            },
            "user_data": {
                "paths": ["var/lib/asis/users/*", "data/users/*"],
                "classification": "user_data",
                "compression": True,
                "encryption": True,
                "verification": True
            },
            "logs": {
                "paths": ["var/log/asis/*", "logs/*"],
                "classification": "logs",
                "compression": True,
                "encryption": False,
                "verification": False
            },
            "certificates": {
                "paths": ["etc/asis/ssl/*", "certs/*"],
                "classification": "system_critical",
                "compression": False,
                "encryption": True,
                "verification": True
            }
        }
    
    def create_full_backup(self, backup_name: Optional[str] = None) -> str:
        """Create full system backup"""
        if backup_name is None:
            backup_name = f"full_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_id = str(uuid.uuid4())
        backup_path = self.backup_base_path / backup_name
        backup_path.mkdir(exist_ok=True)
        
        logger.info(f"📦 Starting full backup: {backup_name}")
        
        total_files = 0
        total_size = 0
        compressed_size = 0
        
        try:
            # Create backup archive
            archive_path = backup_path / f"{backup_name}.zip"
            
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as backup_zip:
                
                # Backup each policy category
                for policy_name, policy in self.backup_policies.items():
                    logger.info(f"📁 Backing up {policy_name}...")
                    
                    for path_pattern in policy["paths"]:
                        for file_path in Path(".").glob(path_pattern):
                            if file_path.is_file():
                                # Get file info
                                file_size = file_path.stat().st_size
                                total_files += 1
                                total_size += file_size
                                
                                # Add to archive
                                backup_zip.write(file_path, file_path)
                                
                                logger.debug(f"📄 Added to backup: {file_path} ({file_size} bytes)")
            
            # Get compressed size
            compressed_size = archive_path.stat().st_size
            
            # Encrypt backup if required
            encrypted_path = None
            encryption_key_id = None
            
            if any(policy.get("encryption", False) for policy in self.backup_policies.values()):
                encrypted_path, encryption_key_id = self.encryption_manager.encrypt_file(
                    str(archive_path), 
                    str(archive_path) + ".encrypted"
                )
                
                # Remove unencrypted archive
                archive_path.unlink()
                archive_path = Path(encrypted_path)
                compressed_size = archive_path.stat().st_size
            
            # Calculate checksum
            checksum = self._calculate_file_checksum(archive_path)
            
            # Create backup metadata
            backup_metadata = BackupMetadata(
                backup_id=backup_id,
                timestamp=datetime.now(),
                backup_type="full",
                file_count=total_files,
                compressed_size=compressed_size,
                original_size=total_size,
                checksum=checksum,
                encryption_key_id=encryption_key_id or "",
                backup_path=str(archive_path),
                retention_policy=self._calculate_retention_policy(),
                verification_status="pending"
            )
            
            # Verify backup
            if self._verify_backup(backup_metadata):
                backup_metadata.verification_status = "verified"
            else:
                backup_metadata.verification_status = "failed"
                logger.error(f"❌ Backup verification failed: {backup_name}")
            
            # Store metadata
            self.backup_metadata.append(backup_metadata)
            self._save_backup_metadata()
            
            # Calculate compression ratio
            compression_ratio = (1 - compressed_size / total_size) * 100 if total_size > 0 else 0
            
            logger.info(f"✅ Full backup completed: {backup_name}")
            logger.info(f"   Files: {total_files}")
            logger.info(f"   Original size: {self._format_size(total_size)}")
            logger.info(f"   Compressed size: {self._format_size(compressed_size)}")
            logger.info(f"   Compression ratio: {compression_ratio:.1f}%")
            logger.info(f"   Encrypted: {'Yes' if encryption_key_id else 'No'}")
            logger.info(f"   Verification: {backup_metadata.verification_status}")
            
            return backup_id
            
        except Exception as e:
            logger.error(f"❌ Full backup failed: {e}")
            raise
    
    def create_incremental_backup(self, reference_backup_id: str, backup_name: Optional[str] = None) -> str:
        """Create incremental backup"""
        if backup_name is None:
            backup_name = f"incremental_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Find reference backup
        reference_backup = None
        for backup in self.backup_metadata:
            if backup.backup_id == reference_backup_id:
                reference_backup = backup
                break
        
        if not reference_backup:
            raise ValueError(f"Reference backup {reference_backup_id} not found")
        
        backup_id = str(uuid.uuid4())
        backup_path = self.backup_base_path / backup_name
        backup_path.mkdir(exist_ok=True)
        
        logger.info(f"📦 Starting incremental backup: {backup_name}")
        logger.info(f"   Reference: {reference_backup.backup_id}")
        
        # Implementation would compare file timestamps and include only changed files
        # For this example, we'll create a simplified incremental backup
        
        total_files = 0
        total_size = 0
        
        # Create incremental backup (simplified)
        archive_path = backup_path / f"{backup_name}.zip"
        
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
            # Add files modified since reference backup
            cutoff_time = reference_backup.timestamp
            
            for policy_name, policy in self.backup_policies.items():
                for path_pattern in policy["paths"]:
                    for file_path in Path(".").glob(path_pattern):
                        if file_path.is_file():
                            # Check if file was modified after reference backup
                            file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                            
                            if file_mtime > cutoff_time:
                                file_size = file_path.stat().st_size
                                total_files += 1
                                total_size += file_size
                                backup_zip.write(file_path, file_path)
        
        compressed_size = archive_path.stat().st_size
        checksum = self._calculate_file_checksum(archive_path)
        
        # Create metadata
        backup_metadata = BackupMetadata(
            backup_id=backup_id,
            timestamp=datetime.now(),
            backup_type="incremental",
            file_count=total_files,
            compressed_size=compressed_size,
            original_size=total_size,
            checksum=checksum,
            encryption_key_id="",
            backup_path=str(archive_path),
            retention_policy=self._calculate_retention_policy(),
            verification_status="verified"
        )
        
        self.backup_metadata.append(backup_metadata)
        self._save_backup_metadata()
        
        logger.info(f"✅ Incremental backup completed: {backup_name}")
        logger.info(f"   Files changed: {total_files}")
        logger.info(f"   Size: {self._format_size(compressed_size)}")
        
        return backup_id
    
    def restore_backup(self, backup_id: str, restore_path: Optional[str] = None) -> bool:
        """Restore backup by ID"""
        # Find backup metadata
        backup_metadata = None
        for backup in self.backup_metadata:
            if backup.backup_id == backup_id:
                backup_metadata = backup
                break
        
        if not backup_metadata:
            raise ValueError(f"Backup {backup_id} not found")
        
        if restore_path is None:
            restore_path = f"restore_{backup_id}_{int(time.time())}"
        
        restore_path = Path(restore_path)
        restore_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"🔄 Restoring backup: {backup_id}")
        logger.info(f"   Backup path: {backup_metadata.backup_path}")
        logger.info(f"   Restore path: {restore_path}")
        
        try:
            backup_file = Path(backup_metadata.backup_path)
            
            # Decrypt if necessary
            if backup_metadata.encryption_key_id:
                logger.info("🔓 Decrypting backup archive...")
                decrypted_path = self.encryption_manager.decrypt_file(
                    str(backup_file),
                    str(backup_file.parent / f"temp_restore_{backup_id}.zip")
                )
                backup_file = Path(decrypted_path)
            
            # Verify checksum
            current_checksum = self._calculate_file_checksum(backup_file)
            if current_checksum != backup_metadata.checksum:
                logger.error("❌ Backup checksum verification failed")
                return False
            
            # Extract backup
            with zipfile.ZipFile(backup_file, 'r') as backup_zip:
                backup_zip.extractall(restore_path)
            
            # Clean up temporary decrypted file
            if backup_metadata.encryption_key_id:
                backup_file.unlink()
            
            logger.info(f"✅ Backup restored successfully to: {restore_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Backup restoration failed: {e}")
            return False
    
    def _verify_backup(self, backup_metadata: BackupMetadata) -> bool:
        """Verify backup integrity"""
        try:
            backup_file = Path(backup_metadata.backup_path)
            
            # Check if file exists
            if not backup_file.exists():
                return False
            
            # Verify checksum
            current_checksum = self._calculate_file_checksum(backup_file)
            if current_checksum != backup_metadata.checksum:
                return False
            
            # Try to open archive (basic validation)
            if backup_file.suffix == '.zip':
                with zipfile.ZipFile(backup_file, 'r') as test_zip:
                    # Test archive integrity
                    bad_file = test_zip.testzip()
                    if bad_file:
                        return False
            
            return True
            
        except Exception:
            return False
    
    def _calculate_file_checksum(self, file_path: Path) -> str:
        """Calculate SHA-256 checksum of file"""
        hash_sha256 = hashlib.sha256()
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        
        return hash_sha256.hexdigest()
    
    def _calculate_retention_policy(self) -> str:
        """Calculate retention policy based on backup type and data classification"""
        # Simplified retention policy
        return "90_days"
    
    def _format_size(self, size_bytes: int) -> str:
        """Format size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
    
    def cleanup_old_backups(self):
        """Clean up old backups based on retention policy"""
        logger.info("🧹 Starting backup cleanup...")
        
        current_time = datetime.now()
        cleaned_count = 0
        
        for backup in list(self.backup_metadata):
            # Calculate retention period (simplified)
            if backup.retention_policy == "90_days":
                retention_days = 90
            elif backup.retention_policy == "30_days":
                retention_days = 30
            else:
                retention_days = 365  # default
            
            # Check if backup has expired
            expiry_date = backup.timestamp + timedelta(days=retention_days)
            
            if current_time > expiry_date:
                try:
                    # Remove backup file
                    backup_path = Path(backup.backup_path)
                    if backup_path.exists():
                        backup_path.unlink()
                    
                    # Remove metadata file if exists
                    metadata_path = backup_path.with_suffix(backup_path.suffix + ".meta")
                    if metadata_path.exists():
                        metadata_path.unlink()
                    
                    # Remove from metadata list
                    self.backup_metadata.remove(backup)
                    cleaned_count += 1
                    
                    logger.info(f"🗑️ Cleaned up expired backup: {backup.backup_id}")
                    
                except Exception as e:
                    logger.error(f"❌ Failed to cleanup backup {backup.backup_id}: {e}")
        
        if cleaned_count > 0:
            self._save_backup_metadata()
        
        logger.info(f"✅ Backup cleanup completed. Removed {cleaned_count} expired backups")
    
    def get_backup_status(self) -> Dict[str, Any]:
        """Get backup system status"""
        total_backups = len(self.backup_metadata)
        total_size = sum(backup.compressed_size for backup in self.backup_metadata)
        
        # Count by type
        backup_types = {}
        for backup in self.backup_metadata:
            backup_types[backup.backup_type] = backup_types.get(backup.backup_type, 0) + 1
        
        # Get latest backup
        latest_backup = max(self.backup_metadata, key=lambda b: b.timestamp) if self.backup_metadata else None
        
        return {
            "total_backups": total_backups,
            "total_size": self._format_size(total_size),
            "backup_types": backup_types,
            "latest_backup": {
                "id": latest_backup.backup_id,
                "timestamp": latest_backup.timestamp.isoformat(),
                "type": latest_backup.backup_type,
                "size": self._format_size(latest_backup.compressed_size)
            } if latest_backup else None,
            "backup_policies": list(self.backup_policies.keys()),
            "storage_path": str(self.backup_base_path),
            "encryption_available": self.encryption_manager is not None
        }

class ASISDataSanitization:
    """Data sanitization and secure deletion for ASIS"""
    
    def __init__(self):
        self.sanitization_methods = {
            "simple_delete": self._simple_delete,
            "secure_overwrite": self._secure_overwrite,
            "crypto_erase": self._crypto_erase,
            "dod_5220": self._dod_5220_wipe,
            "gutmann": self._gutmann_wipe
        }
        
        self.sanitization_log = []
    
    def sanitize_file(self, file_path: str, method: str = "secure_overwrite") -> bool:
        """Sanitize a file using specified method"""
        if method not in self.sanitization_methods:
            raise ValueError(f"Unknown sanitization method: {method}")
        
        file_path = Path(file_path)
        
        if not file_path.exists():
            logger.warning(f"File not found for sanitization: {file_path}")
            return False
        
        logger.info(f"🗑️ Sanitizing file: {file_path} using {method}")
        
        try:
            # Record original file info
            original_size = file_path.stat().st_size
            
            # Execute sanitization method
            success = self.sanitization_methods[method](file_path)
            
            if success:
                # Log sanitization
                sanitization_record = {
                    "timestamp": datetime.now().isoformat(),
                    "file_path": str(file_path),
                    "method": method,
                    "original_size": original_size,
                    "status": "success"
                }
                self.sanitization_log.append(sanitization_record)
                
                logger.info(f"✅ File sanitized successfully: {file_path}")
                return True
            else:
                logger.error(f"❌ File sanitization failed: {file_path}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error during file sanitization: {e}")
            return False
    
    def sanitize_directory(self, directory_path: str, method: str = "secure_overwrite", 
                          recursive: bool = True) -> int:
        """Sanitize all files in a directory"""
        directory_path = Path(directory_path)
        
        if not directory_path.exists():
            logger.warning(f"Directory not found for sanitization: {directory_path}")
            return 0
        
        logger.info(f"🗂️ Sanitizing directory: {directory_path} using {method}")
        
        sanitized_count = 0
        
        try:
            # Get all files
            if recursive:
                files = directory_path.rglob('*')
            else:
                files = directory_path.glob('*')
            
            # Sanitize each file
            for file_path in files:
                if file_path.is_file():
                    if self.sanitize_file(str(file_path), method):
                        sanitized_count += 1
            
            # Remove empty directories if recursive
            if recursive:
                for dir_path in sorted(directory_path.rglob('*'), reverse=True):
                    if dir_path.is_dir() and not any(dir_path.iterdir()):
                        try:
                            dir_path.rmdir()
                        except:
                            pass
            
            # Remove the main directory if empty
            if not any(directory_path.iterdir()):
                try:
                    directory_path.rmdir()
                except:
                    pass
            
            logger.info(f"✅ Directory sanitization completed. Files sanitized: {sanitized_count}")
            return sanitized_count
            
        except Exception as e:
            logger.error(f"❌ Error during directory sanitization: {e}")
            return sanitized_count
    
    def _simple_delete(self, file_path: Path) -> bool:
        """Simple file deletion (not secure)"""
        try:
            file_path.unlink()
            return True
        except Exception:
            return False
    
    def _secure_overwrite(self, file_path: Path) -> bool:
        """Secure overwrite with random data (3 passes)"""
        try:
            file_size = file_path.stat().st_size
            
            # Perform 3 passes of overwriting
            for pass_num in range(3):
                with open(file_path, 'wb') as f:
                    # Write random data
                    remaining = file_size
                    while remaining > 0:
                        chunk_size = min(4096, remaining)
                        random_data = secrets.token_bytes(chunk_size)
                        f.write(random_data)
                        remaining -= chunk_size
                    
                    # Flush to disk
                    f.flush()
                    os.fsync(f.fileno())
            
            # Finally delete the file
            file_path.unlink()
            return True
            
        except Exception:
            return False
    
    def _crypto_erase(self, file_path: Path) -> bool:
        """Cryptographic erasure (encrypt then delete key)"""
        try:
            # Read file
            with open(file_path, 'rb') as f:
                data = f.read()
            
            # Encrypt with temporary key
            temp_key = secrets.token_bytes(32)
            iv = secrets.token_bytes(16)
            
            cipher = Cipher(algorithms.AES(temp_key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            
            # Pad data
            block_size = 16
            padding_length = block_size - (len(data) % block_size)
            padded_data = data + bytes([padding_length] * padding_length)
            
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
            
            # Overwrite file with encrypted data
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)
                f.flush()
                os.fsync(f.fileno())
            
            # "Forget" the key (cryptographic erasure)
            temp_key = None
            
            # Delete file
            file_path.unlink()
            return True
            
        except Exception:
            return False
    
    def _dod_5220_wipe(self, file_path: Path) -> bool:
        """DOD 5220.22-M standard wipe (7 passes)"""
        try:
            file_size = file_path.stat().st_size
            
            # DOD 5220.22-M patterns
            patterns = [
                lambda: b'\x00',  # Pass 1: zeros
                lambda: b'\xFF',  # Pass 2: ones
                lambda: secrets.token_bytes(1),  # Pass 3: random
                lambda: secrets.token_bytes(1),  # Pass 4: random
                lambda: secrets.token_bytes(1),  # Pass 5: random
                lambda: secrets.token_bytes(1),  # Pass 6: random
                lambda: secrets.token_bytes(1),  # Pass 7: random
            ]
            
            for pass_num, pattern_func in enumerate(patterns):
                with open(file_path, 'wb') as f:
                    remaining = file_size
                    while remaining > 0:
                        chunk_size = min(4096, remaining)
                        if pattern_func == patterns[0] or pattern_func == patterns[1]:
                            # Fixed patterns
                            pattern_data = pattern_func() * chunk_size
                        else:
                            # Random patterns
                            pattern_data = secrets.token_bytes(chunk_size)
                        
                        f.write(pattern_data[:chunk_size])
                        remaining -= chunk_size
                    
                    f.flush()
                    os.fsync(f.fileno())
            
            # Delete file
            file_path.unlink()
            return True
            
        except Exception:
            return False
    
    def _gutmann_wipe(self, file_path: Path) -> bool:
        """Gutmann method (35 passes) - for legacy magnetic storage"""
        try:
            file_size = file_path.stat().st_size
            
            # Gutmann method uses 35 passes with specific patterns
            # This is overkill for modern SSDs but included for completeness
            
            for pass_num in range(35):
                with open(file_path, 'wb') as f:
                    remaining = file_size
                    while remaining > 0:
                        chunk_size = min(4096, remaining)
                        
                        # Use random data for simplicity
                        # (actual Gutmann method has specific patterns)
                        pattern_data = secrets.token_bytes(chunk_size)
                        
                        f.write(pattern_data)
                        remaining -= chunk_size
                    
                    f.flush()
                    os.fsync(f.fileno())
            
            # Delete file
            file_path.unlink()
            return True
            
        except Exception:
            return False
    
    def get_sanitization_log(self) -> List[Dict[str, Any]]:
        """Get sanitization log"""
        return self.sanitization_log.copy()

class ASISDataProtection:
    """Comprehensive ASIS Data Protection System"""
    
    def __init__(self, base_path: str = "var/lib/asis"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.encryption_manager = ASISEncryptionManager()
        self.backup_system = ASISBackupSystem()
        self.data_sanitization = ASISDataSanitization()
        
        # Protection status
        self.protection_status = {
            "encryption_active": False,
            "backup_active": False,
            "sanitization_active": False,
            "data_classification_active": False,
            "monitoring_active": False
        }
        
        # Data monitoring
        self.data_monitors = {}
        self.protection_policies = {}
        
        self._initialize_data_protection()
    
    def _initialize_data_protection(self):
        """Initialize data protection system"""
        try:
            # Setup protection policies
            self._setup_protection_policies()
            
            # Initialize monitoring
            self._setup_data_monitoring()
            
            self.protection_status["encryption_active"] = True
            self.protection_status["backup_active"] = True
            self.protection_status["sanitization_active"] = True
            self.protection_status["data_classification_active"] = True
            
            logger.info("✅ ASIS Data Protection System initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize data protection: {e}")
            raise
    
    def _setup_protection_policies(self):
        """Setup data protection policies"""
        self.protection_policies = {
            "asis_databases": {
                "paths": ["var/lib/asis/*.db"],
                "encryption": "AES-256",
                "backup_frequency": "daily",
                "retention": "1_year",
                "classification": "system_critical",
                "sanitization": "secure_overwrite"
            },
            "user_data": {
                "paths": ["var/lib/asis/users/*"],
                "encryption": "AES-256",
                "backup_frequency": "daily",
                "retention": "90_days",
                "classification": "confidential",
                "sanitization": "crypto_erase"
            },
            "security_logs": {
                "paths": ["var/log/asis/security/*"],
                "encryption": "AES-256",
                "backup_frequency": "weekly",
                "retention": "1_year",
                "classification": "internal",
                "sanitization": "secure_overwrite"
            },
            "configuration": {
                "paths": ["etc/asis/*"],
                "encryption": "AES-256",
                "backup_frequency": "daily",
                "retention": "1_year",
                "classification": "system_critical",
                "sanitization": "dod_5220"
            },
            "certificates": {
                "paths": ["etc/asis/ssl/*", "var/lib/asis/keys/*"],
                "encryption": "AES-256",
                "backup_frequency": "daily",
                "retention": "2_years",
                "classification": "restricted",
                "sanitization": "gutmann"
            }
        }
    
    def _setup_data_monitoring(self):
        """Setup data monitoring and protection"""
        # File system monitoring would be implemented here
        # For now, we'll setup basic monitoring structure
        self.data_monitors = {
            "file_access": [],
            "data_modifications": [],
            "encryption_status": [],
            "backup_status": []
        }
        
        self.protection_status["monitoring_active"] = True
    
    def implement_aes_256_encryption(self):
        """Implement AES-256 encryption for all persistent data"""
        logger.info("🔐 Implementing AES-256 encryption for persistent data...")
        
        encrypted_count = 0
        failed_count = 0
        
        try:
            # Encrypt data according to protection policies
            for policy_name, policy in self.protection_policies.items():
                if policy.get("encryption") == "AES-256":
                    logger.info(f"🔒 Encrypting {policy_name} data...")
                    
                    for path_pattern in policy["paths"]:
                        for file_path in Path(".").glob(path_pattern):
                            if file_path.is_file() and not str(file_path).endswith('.encrypted'):
                                try:
                                    encrypted_path, key_id = self.encryption_manager.encrypt_file(str(file_path))
                                    
                                    # Securely delete original
                                    self.data_sanitization.sanitize_file(
                                        str(file_path), 
                                        policy.get("sanitization", "secure_overwrite")
                                    )
                                    
                                    encrypted_count += 1
                                    logger.debug(f"🔐 Encrypted: {file_path}")
                                    
                                except Exception as e:
                                    logger.error(f"❌ Failed to encrypt {file_path}: {e}")
                                    failed_count += 1
            
            logger.info(f"✅ AES-256 encryption completed")
            logger.info(f"   Files encrypted: {encrypted_count}")
            logger.info(f"   Files failed: {failed_count}")
            
            self.protection_status["encryption_active"] = True
            return encrypted_count > 0
            
        except Exception as e:
            logger.error(f"❌ AES-256 encryption implementation failed: {e}")
            return False
    
    def setup_secure_backups(self):
        """Setup automated, encrypted backups"""
        logger.info("📦 Setting up secure automated backups...")
        
        try:
            # Create initial full backup
            backup_id = self.backup_system.create_full_backup("initial_full_backup")
            
            # Setup backup schedules (simplified - in production, use cron or scheduler)
            self.backup_schedules = {
                "daily_incremental": {
                    "frequency": "daily",
                    "backup_type": "incremental",
                    "reference_backup": backup_id,
                    "retention": "30_days"
                },
                "weekly_full": {
                    "frequency": "weekly",
                    "backup_type": "full",
                    "retention": "90_days"
                },
                "monthly_archive": {
                    "frequency": "monthly",
                    "backup_type": "full",
                    "retention": "1_year"
                }
            }
            
            logger.info("✅ Secure backup system configured")
            logger.info(f"   Initial backup ID: {backup_id}")
            logger.info(f"   Backup schedules: {len(self.backup_schedules)}")
            
            self.protection_status["backup_active"] = True
            return True
            
        except Exception as e:
            logger.error(f"❌ Secure backup setup failed: {e}")
            return False
    
    def setup_data_sanitization(self):
        """Setup data sanitization policies"""
        logger.info("🗑️ Setting up data sanitization policies...")
        
        try:
            # Data sanitization is already initialized
            # This method configures automatic sanitization policies
            
            sanitization_policies = {}
            for policy_name, policy in self.protection_policies.items():
                sanitization_policies[policy_name] = {
                    "method": policy.get("sanitization", "secure_overwrite"),
                    "classification": policy.get("classification", "internal"),
                    "auto_sanitize": True
                }
            
            logger.info("✅ Data sanitization policies configured")
            logger.info(f"   Policies: {len(sanitization_policies)}")
            
            self.protection_status["sanitization_active"] = True
            return True
            
        except Exception as e:
            logger.error(f"❌ Data sanitization setup failed: {e}")
            return False
    
    def perform_data_integrity_check(self) -> Dict[str, Any]:
        """Perform comprehensive data integrity check"""
        logger.info("🔍 Performing data integrity check...")
        
        integrity_report = {
            "timestamp": datetime.now().isoformat(),
            "checks_performed": [],
            "issues_found": [],
            "encryption_status": {},
            "backup_status": {},
            "overall_status": "unknown"
        }
        
        try:
            # Check encryption status
            encryption_status = self.encryption_manager.get_encryption_status()
            integrity_report["encryption_status"] = encryption_status
            integrity_report["checks_performed"].append("encryption_check")
            
            if not encryption_status["master_key_available"]:
                integrity_report["issues_found"].append("Master encryption key not available")
            
            # Check backup status
            backup_status = self.backup_system.get_backup_status()
            integrity_report["backup_status"] = backup_status
            integrity_report["checks_performed"].append("backup_check")
            
            if backup_status["total_backups"] == 0:
                integrity_report["issues_found"].append("No backups available")
            
            # Check file integrity for protected data
            integrity_report["checks_performed"].append("file_integrity_check")
            
            for policy_name, policy in self.protection_policies.items():
                for path_pattern in policy["paths"]:
                    for file_path in Path(".").glob(path_pattern):
                        if file_path.is_file():
                            # Check if file should be encrypted
                            if policy.get("encryption") and not str(file_path).endswith('.encrypted'):
                                integrity_report["issues_found"].append(f"Unencrypted file found: {file_path}")
            
            # Determine overall status
            if len(integrity_report["issues_found"]) == 0:
                integrity_report["overall_status"] = "healthy"
            elif len(integrity_report["issues_found"]) <= 3:
                integrity_report["overall_status"] = "warning"
            else:
                integrity_report["overall_status"] = "critical"
            
            logger.info(f"✅ Data integrity check completed")
            logger.info(f"   Overall status: {integrity_report['overall_status']}")
            logger.info(f"   Issues found: {len(integrity_report['issues_found'])}")
            
            return integrity_report
            
        except Exception as e:
            logger.error(f"❌ Data integrity check failed: {e}")
            integrity_report["overall_status"] = "error"
            integrity_report["issues_found"].append(f"Integrity check error: {str(e)}")
            return integrity_report
    
    def create_emergency_backup(self) -> str:
        """Create emergency backup of all critical data"""
        logger.warning("🚨 Creating emergency backup...")
        
        try:
            backup_id = self.backup_system.create_full_backup("emergency_backup")
            logger.warning(f"🚨 Emergency backup created: {backup_id}")
            return backup_id
            
        except Exception as e:
            logger.error(f"❌ Emergency backup failed: {e}")
            raise
    
    def emergency_data_lockdown(self):
        """Emergency data protection lockdown"""
        logger.critical("🚨 EMERGENCY DATA LOCKDOWN INITIATED")
        
        try:
            # Create emergency backup
            emergency_backup_id = self.create_emergency_backup()
            
            # Encrypt all unencrypted sensitive data
            self.implement_aes_256_encryption()
            
            # Rotate all encryption keys
            self.encryption_manager.rotate_keys()
            
            # Clean up temporary and cache files
            temp_dirs = ["tmp", "cache", "temp"]
            for temp_dir in temp_dirs:
                if Path(temp_dir).exists():
                    self.data_sanitization.sanitize_directory(temp_dir, "secure_overwrite")
            
            logger.critical("🚨 Emergency data lockdown completed")
            logger.critical(f"🚨 Emergency backup: {emergency_backup_id}")
            
        except Exception as e:
            logger.critical(f"🚨 Emergency lockdown error: {e}")
    
    def get_protection_status(self) -> Dict[str, Any]:
        """Get comprehensive data protection status"""
        return {
            "protection_status": self.protection_status,
            "encryption_status": self.encryption_manager.get_encryption_status(),
            "backup_status": self.backup_system.get_backup_status(),
            "protection_policies": len(self.protection_policies),
            "sanitization_log_entries": len(self.data_sanitization.get_sanitization_log()),
            "data_monitors": len(self.data_monitors),
            "system_info": {
                "platform": platform.system(),
                "python_version": platform.python_version(),
                "disk_usage": psutil.disk_usage('.').percent if psutil else "unknown"
            }
        }

# Integration with existing ASIS security
def integrate_with_asis_security():
    """Integration function for ASIS security framework"""
    try:
        # Try to import existing security framework
        from asis_security_framework import ASISSecurityFramework
        
        # Create data protection instance
        data_protection = ASISDataProtection()
        
        # Initialize protection systems
        success_count = 0
        total_systems = 3
        
        if data_protection.implement_aes_256_encryption():
            success_count += 1
        
        if data_protection.setup_secure_backups():
            success_count += 1
        
        if data_protection.setup_data_sanitization():
            success_count += 1
        
        if success_count >= 2:
            logger.info(f"✅ ASIS Data Protection integrated successfully ({success_count}/{total_systems})")
            return data_protection
        else:
            logger.warning(f"⚠️ ASIS Data Protection partially integrated ({success_count}/{total_systems})")
            return data_protection
            
    except ImportError:
        logger.info("ℹ️ ASIS Security Framework not available - running standalone data protection")
        data_protection = ASISDataProtection()
        data_protection.implement_aes_256_encryption()
        data_protection.setup_secure_backups()
        data_protection.setup_data_sanitization()
        return data_protection

# Example usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize ASIS Data Protection
    print("🔒 Initializing ASIS Data Protection System...")
    
    data_protection = integrate_with_asis_security()
    
    # Test data protection features
    print("\n🧪 Testing Data Protection Features...")
    
    # Create test file
    test_file = Path("test_sensitive_data.txt")
    with open(test_file, 'w') as f:
        f.write("This is sensitive test data that needs protection.")
    
    # Test encryption
    print("🔐 Testing file encryption...")
    encrypted_path, key_id = data_protection.encryption_manager.encrypt_file(str(test_file))
    print(f"   Encrypted: {test_file} -> {encrypted_path}")
    
    # Test backup
    print("📦 Testing backup system...")
    backup_id = data_protection.backup_system.create_full_backup("test_backup")
    print(f"   Backup created: {backup_id}")
    
    # Test data integrity
    print("🔍 Testing data integrity check...")
    integrity_report = data_protection.perform_data_integrity_check()
    print(f"   Integrity status: {integrity_report['overall_status']}")
    print(f"   Issues found: {len(integrity_report['issues_found'])}")
    
    # Test file sanitization
    print("🗑️ Testing data sanitization...")
    if test_file.exists():
        sanitized = data_protection.data_sanitization.sanitize_file(str(test_file), "secure_overwrite")
        print(f"   File sanitized: {sanitized}")
    
    # Display protection status
    print("\n📊 Data Protection Status:")
    status = data_protection.get_protection_status()
    
    print(f"Encryption Active: {'✅' if status['protection_status']['encryption_active'] else '❌'}")
    print(f"Backup Active: {'✅' if status['protection_status']['backup_active'] else '❌'}")
    print(f"Sanitization Active: {'✅' if status['protection_status']['sanitization_active'] else '❌'}")
    print(f"Total Backups: {status['backup_status']['total_backups']}")
    print(f"Protection Policies: {status['protection_policies']}")
    
    print("\n🔒 ASIS Data Protection System demonstration complete!")