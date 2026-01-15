#!/usr/bin/env python3
"""
ASIS Phase 2 - Stage 1: File System Management
==============================================

Autonomous File System Operations:
- Directory creation and organization  
- File backup and versioning
- Workspace management
- Automated file organization
- Storage optimization
"""

import os
import shutil
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import sqlite3
import threading

class AutonomousFileManager:
    """
    Autonomous File System Management for ASIS
    """
    
    def __init__(self, workspace_root: str = None):
        self.workspace_root = workspace_root or os.getcwd()
        self.db_path = os.path.join(self.workspace_root, "asis_file_manager.db")
        self.db_lock = threading.Lock()
        
        # Initialize file management database
        self._init_database()
        
        # File organization rules
        self.organization_rules = self._load_organization_rules()
        
        print("🗂️  ASIS Autonomous File Manager initialized")
        print(f"📁 Workspace: {self.workspace_root}")
    
    def _init_database(self):
        """Initialize file management database"""
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS file_operations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_type TEXT,
                    source_path TEXT,
                    target_path TEXT,
                    file_hash TEXT,
                    size_bytes INTEGER,
                    timestamp TIMESTAMP,
                    success BOOLEAN,
                    notes TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS workspace_organization (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    directory_path TEXT,
                    purpose TEXT,
                    file_count INTEGER,
                    total_size_bytes INTEGER,
                    last_organized TIMESTAMP,
                    organization_rules TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS file_backups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_path TEXT,
                    backup_path TEXT,
                    backup_type TEXT,
                    file_hash TEXT,
                    created_at TIMESTAMP,
                    size_bytes INTEGER
                )
            ''')
    
    def _load_organization_rules(self) -> Dict[str, Any]:
        """Load file organization rules"""
        
        return {
            "by_extension": {
                ".py": "code/python",
                ".js": "code/javascript", 
                ".html": "web/html",
                ".css": "web/styles",
                ".md": "docs/markdown",
                ".txt": "docs/text",
                ".json": "data/json",
                ".csv": "data/csv",
                ".db": "databases",
                ".log": "logs",
                ".bak": "backups"
            },
            "by_pattern": {
                "asis_": "asis_systems",
                "test_": "tests",
                "demo_": "demos",
                "config": "config",
                "setup": "setup"
            },
            "by_size": {
                "large_threshold_mb": 100,
                "large_files_dir": "large_files"
            }
        }
    
    def autonomous_organize_workspace(self) -> Dict[str, Any]:
        """Autonomously organize the entire workspace"""
        
        print("🤖 Starting autonomous workspace organization...")
        
        results = {
            "files_processed": 0,
            "directories_created": 0,
            "files_moved": 0,
            "errors": [],
            "organization_summary": {}
        }
        
        try:
            # Scan all files in workspace
            for root, dirs, files in os.walk(self.workspace_root):
                # Skip hidden directories and git
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    if file.startswith('.'):
                        continue
                        
                    file_path = os.path.join(root, file)
                    results["files_processed"] += 1
                    
                    # Determine organization destination
                    target_dir = self._determine_organization_target(file_path)
                    
                    if target_dir:
                        moved = self._move_to_organized_location(file_path, target_dir)
                        if moved:
                            results["files_moved"] += 1
            
            # Update organization database
            self._record_workspace_organization(results)
            
            print(f"✅ Workspace organization complete!")
            print(f"   Files processed: {results['files_processed']}")
            print(f"   Files organized: {results['files_moved']}")
            
            return results
            
        except Exception as e:
            results["errors"].append(f"Organization error: {str(e)}")
            print(f"❌ Organization error: {e}")
            return results
    
    def _determine_organization_target(self, file_path: str) -> Optional[str]:
        """Determine where a file should be organized"""
        
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1].lower()
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        
        # Skip files already in organized directories
        relative_path = os.path.relpath(file_path, self.workspace_root)
        if any(org_dir in relative_path for org_dir in ["code/", "docs/", "data/", "asis_systems/"]):
            return None
        
        # Check by extension
        if file_ext in self.organization_rules["by_extension"]:
            return self.organization_rules["by_extension"][file_ext]
        
        # Check by pattern
        for pattern, target_dir in self.organization_rules["by_pattern"].items():
            if file_name.startswith(pattern):
                return target_dir
        
        # Check by size
        if file_size_mb > self.organization_rules["by_size"]["large_threshold_mb"]:
            return self.organization_rules["by_size"]["large_files_dir"]
        
        return None
    
    def _move_to_organized_location(self, source_path: str, target_subdir: str) -> bool:
        """Move file to organized location"""
        
        try:
            # Create target directory
            target_dir = os.path.join(self.workspace_root, "organized", target_subdir)
            os.makedirs(target_dir, exist_ok=True)
            
            # Generate target path
            file_name = os.path.basename(source_path)
            target_path = os.path.join(target_dir, file_name)
            
            # Handle file conflicts
            if os.path.exists(target_path):
                base, ext = os.path.splitext(file_name)
                counter = 1
                while os.path.exists(target_path):
                    new_name = f"{base}_{counter}{ext}"
                    target_path = os.path.join(target_dir, new_name)
                    counter += 1
            
            # Move the file
            shutil.move(source_path, target_path)
            
            # Record operation
            self._record_file_operation("move", source_path, target_path, True)
            
            return True
            
        except Exception as e:
            self._record_file_operation("move", source_path, "", False, str(e))
            return False
    
    def autonomous_backup_system(self, backup_type: str = "incremental") -> Dict[str, Any]:
        """Create autonomous backups of important files"""
        
        print(f"💾 Creating {backup_type} backup...")
        
        backup_results = {
            "backup_type": backup_type,
            "files_backed_up": 0,
            "total_size_mb": 0,
            "backup_location": "",
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Create backup directory
            backup_dir = os.path.join(self.workspace_root, "backups", 
                                    f"{backup_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            os.makedirs(backup_dir, exist_ok=True)
            backup_results["backup_location"] = backup_dir
            
            # Identify files to backup
            important_files = self._identify_important_files()
            
            for file_path in important_files:
                if os.path.exists(file_path):
                    # Create backup
                    relative_path = os.path.relpath(file_path, self.workspace_root)
                    backup_path = os.path.join(backup_dir, relative_path)
                    
                    # Ensure backup subdirectory exists
                    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                    
                    # Copy file
                    shutil.copy2(file_path, backup_path)
                    
                    # Calculate file hash and size
                    file_hash = self._calculate_file_hash(file_path)
                    file_size = os.path.getsize(file_path)
                    
                    # Record backup
                    self._record_backup(file_path, backup_path, backup_type, file_hash, file_size)
                    
                    backup_results["files_backed_up"] += 1
                    backup_results["total_size_mb"] += file_size / (1024 * 1024)
            
            print(f"✅ Backup complete: {backup_results['files_backed_up']} files")
            print(f"   Total size: {backup_results['total_size_mb']:.2f} MB")
            print(f"   Location: {backup_dir}")
            
            return backup_results
            
        except Exception as e:
            print(f"❌ Backup error: {e}")
            backup_results["error"] = str(e)
            return backup_results
    
    def _identify_important_files(self) -> List[str]:
        """Identify files that should be backed up"""
        
        important_files = []
        important_patterns = [
            "asis_*.py",
            "*.db", 
            "*.json",
            "*.md",
            "config*",
            "requirements*.txt"
        ]
        
        # Skip certain directories
        skip_dirs = {".git", ".venv", "__pycache__", "backups", "logs"}
        
        for root, dirs, files in os.walk(self.workspace_root):
            # Remove skip directories
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            for file in files:
                file_path = os.path.join(root, file)
                
                # Check if file matches important patterns
                for pattern in important_patterns:
                    if self._matches_pattern(file, pattern):
                        important_files.append(file_path)
                        break
        
        return important_files
    
    def _matches_pattern(self, filename: str, pattern: str) -> bool:
        """Check if filename matches pattern"""
        import fnmatch
        return fnmatch.fnmatch(filename, pattern)
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate MD5 hash of file"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def create_project_structure(self, project_name: str, project_type: str = "python") -> Dict[str, Any]:
        """Autonomously create organized project structure"""
        
        print(f"🏗️  Creating project structure: {project_name}")
        
        project_templates = {
            "python": [
                "src/",
                "tests/", 
                "docs/",
                "config/",
                "data/",
                "logs/",
                "requirements.txt",
                "README.md",
                ".gitignore"
            ],
            "web": [
                "src/html/",
                "src/css/", 
                "src/js/",
                "assets/images/",
                "docs/",
                "index.html",
                "README.md"
            ],
            "asis_system": [
                "core/",
                "modules/",
                "databases/",
                "logs/",
                "config/",
                "tests/",
                "docs/",
                "README.md",
                "requirements.txt"
            ]
        }
        
        structure_result = {
            "project_name": project_name,
            "project_type": project_type,
            "directories_created": [],
            "files_created": [],
            "project_path": ""
        }
        
        try:
            # Create project root
            project_path = os.path.join(self.workspace_root, "projects", project_name)
            os.makedirs(project_path, exist_ok=True)
            structure_result["project_path"] = project_path
            
            # Get template structure
            template = project_templates.get(project_type, project_templates["python"])
            
            # Create structure
            for item in template:
                item_path = os.path.join(project_path, item)
                
                if item.endswith("/"):
                    # Directory
                    os.makedirs(item_path, exist_ok=True)
                    structure_result["directories_created"].append(item)
                else:
                    # File
                    if not os.path.exists(item_path):
                        with open(item_path, 'w') as f:
                            f.write(self._get_template_content(item, project_name))
                        structure_result["files_created"].append(item)
            
            print(f"✅ Project structure created: {project_name}")
            print(f"   Directories: {len(structure_result['directories_created'])}")
            print(f"   Files: {len(structure_result['files_created'])}")
            
            return structure_result
            
        except Exception as e:
            print(f"❌ Project creation error: {e}")
            structure_result["error"] = str(e)
            return structure_result
    
    def _get_template_content(self, filename: str, project_name: str) -> str:
        """Get template content for project files"""
        
        templates = {
            "README.md": f"""# {project_name}

Created automatically by ASIS File Manager on {datetime.now().strftime('%Y-%m-%d')}

## Description
Autonomous project structure generated for {project_name}.

## Structure
- src/: Source code
- tests/: Test files  
- docs/: Documentation
- config/: Configuration files

## Usage
[Add usage instructions here]

---
*Generated by ASIS Autonomous File Management System*
""",
            
            "requirements.txt": """# Project dependencies
# Add required packages here
""",
            
            ".gitignore": """__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
.venv/
.env
*.log
*.db
.DS_Store
""",
            
            "index.html": f"""<!DOCTYPE html>
<html>
<head>
    <title>{project_name}</title>
</head>
<body>
    <h1>{project_name}</h1>
    <p>Project created by ASIS File Manager</p>
</body>
</html>
"""
        }
        
        return templates.get(filename, f"# {filename}\n# Created by ASIS File Manager\n")
    
    def _record_file_operation(self, operation: str, source: str, target: str, 
                             success: bool, notes: str = ""):
        """Record file operation in database"""
        
        with self.db_lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO file_operations 
                    (operation_type, source_path, target_path, success, timestamp, notes)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (operation, source, target, success, datetime.now(), notes))
    
    def _record_workspace_organization(self, results: Dict[str, Any]):
        """Record workspace organization results"""
        
        with self.db_lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO workspace_organization
                    (directory_path, purpose, file_count, last_organized, organization_rules)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    self.workspace_root,
                    "autonomous_organization", 
                    results["files_moved"],
                    datetime.now(),
                    json.dumps(self.organization_rules)
                ))
    
    def _record_backup(self, original_path: str, backup_path: str, backup_type: str,
                      file_hash: str, size_bytes: int):
        """Record backup operation"""
        
        with self.db_lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO file_backups
                    (original_path, backup_path, backup_type, file_hash, created_at, size_bytes)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (original_path, backup_path, backup_type, file_hash, datetime.now(), size_bytes))
    
    def get_file_management_status(self) -> Dict[str, Any]:
        """Get current file management status"""
        
        status = {
            "workspace_root": self.workspace_root,
            "total_files": 0,
            "organized_files": 0,
            "backup_count": 0,
            "recent_operations": []
        }
        
        # Count total files
        for root, dirs, files in os.walk(self.workspace_root):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            status["total_files"] += len([f for f in files if not f.startswith('.')])
        
        # Get database statistics
        with self.db_lock:
            with sqlite3.connect(self.db_path) as conn:
                # Count successful operations
                cursor = conn.execute('SELECT COUNT(*) FROM file_operations WHERE success = 1')
                status["organized_files"] = cursor.fetchone()[0]
                
                # Count backups
                cursor = conn.execute('SELECT COUNT(*) FROM file_backups')
                status["backup_count"] = cursor.fetchone()[0]
                
                # Get recent operations
                cursor = conn.execute('''
                    SELECT operation_type, source_path, timestamp 
                    FROM file_operations 
                    WHERE success = 1 
                    ORDER BY timestamp DESC 
                    LIMIT 5
                ''')
                status["recent_operations"] = [
                    {"operation": op, "file": os.path.basename(path), "time": time}
                    for op, path, time in cursor.fetchall()
                ]
        
        return status

def main():
    """Test the autonomous file manager"""
    
    print("🗂️  ASIS Autonomous File Manager - Stage 1")
    print("=" * 50)
    
    file_manager = AutonomousFileManager()
    
    print("\nAvailable operations:")
    print("1. 'organize' - Organize workspace autonomously")
    print("2. 'backup' - Create backup of important files") 
    print("3. 'project [name]' - Create new project structure")
    print("4. 'status' - Show file management status")
    print("5. 'quit' - Exit")
    
    while True:
        try:
            user_input = input("\nFile Manager> ").strip().lower()
            
            if user_input == "quit":
                break
            elif user_input == "organize":
                result = file_manager.autonomous_organize_workspace()
                print(f"Organization result: {result}")
            elif user_input == "backup":
                result = file_manager.autonomous_backup_system()
                print(f"Backup result: {result}")
            elif user_input.startswith("project"):
                parts = user_input.split()
                project_name = parts[1] if len(parts) > 1 else "test_project"
                result = file_manager.create_project_structure(project_name, "asis_system")
                print(f"Project creation result: {result}")
            elif user_input == "status":
                status = file_manager.get_file_management_status()
                print("\n📊 File Management Status:")
                for key, value in status.items():
                    print(f"   {key}: {value}")
            else:
                print("🗂️  Autonomous File Manager ready!")
                print("Commands: organize, backup, project [name], status, quit")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
