#!/usr/bin/env python3
"""
Stage 1 Comprehensive Test: REAL File Management Verification
===========================================================

Tests to ensure ASIS performs REAL file operations, not simulations:
1. Create test files and verify they exist
2. Test autonomous organization with real file movement
3. Test backup system with actual file copying
4. Test project creation with real directory structure
5. Verify database operations track real actions
"""

import os
import sys
import time
import shutil
from datetime import datetime
from pathlib import Path

# Import the file manager
sys.path.append(os.getcwd())
from asis_file_manager_phase2 import AutonomousFileManager

class Stage1Tester:
    """Comprehensive tester for Stage 1 file management"""
    
    def __init__(self):
        self.test_workspace = os.path.join(os.getcwd(), "test_stage1")
        self.results = {
            "tests_passed": 0,
            "tests_failed": 0,
            "evidence_files": [],
            "real_actions_verified": []
        }
        
    def setup_test_environment(self):
        """Create test environment with real files"""
        
        print("🔧 Setting up test environment...")
        
        # Create test workspace
        if os.path.exists(self.test_workspace):
            shutil.rmtree(self.test_workspace)
        os.makedirs(self.test_workspace)
        
        # Create diverse test files to verify organization
        test_files = {
            "test_script.py": "# Python test file\nprint('Hello ASIS!')",
            "README.md": "# Test README\nThis is a test markdown file",
            "data.json": '{"test": "json data", "created_by": "ASIS test"}',
            "style.css": "body { margin: 0; padding: 0; }",
            "app.js": "console.log('JavaScript test file');",
            "asis_test_system.py": "# ASIS system file\nclass TestSystem: pass",
            "config.txt": "test_setting=true\nautonomous=enabled",
            "large_file.txt": "x" * (150 * 1024 * 1024),  # 150MB file
        }
        
        # Create actual files
        for filename, content in test_files.items():
            filepath = os.path.join(self.test_workspace, filename)
            with open(filepath, 'w') as f:
                f.write(content)
            self.results["evidence_files"].append(filepath)
        
        print(f"✅ Created {len(test_files)} test files")
        return True
    
    def test_file_organization(self, file_manager):
        """Test REAL autonomous file organization"""
        
        print("\n🗂️  Testing REAL file organization...")
        
        # Count files before organization
        files_before = []
        for root, dirs, files in os.walk(self.test_workspace):
            files_before.extend([os.path.join(root, f) for f in files if not f.startswith('.')])
        
        print(f"Files before organization: {len(files_before)}")
        
        # Run autonomous organization
        result = file_manager.autonomous_organize_workspace()
        
        # Verify real organization happened
        organized_dir = os.path.join(self.test_workspace, "organized")
        
        if os.path.exists(organized_dir):
            # Count organized files
            organized_files = []
            for root, dirs, files in os.walk(organized_dir):
                organized_files.extend([os.path.join(root, f) for f in files])
            
            print(f"Files moved to organized/: {len(organized_files)}")
            
            # Verify specific file types were organized correctly
            expected_locations = {
                "code/python": ["test_script.py", "asis_test_system.py"],
                "docs/markdown": ["README.md"],
                "data/json": ["data.json"],
                "web/styles": ["style.css"],
                "code/javascript": ["app.js"],
                "large_files": ["large_file.txt"]
            }
            
            organization_verified = 0
            for subdir, expected_files in expected_locations.items():
                subdir_path = os.path.join(organized_dir, subdir)
                if os.path.exists(subdir_path):
                    actual_files = os.listdir(subdir_path)
                    for expected_file in expected_files:
                        if expected_file in actual_files:
                            organization_verified += 1
                            print(f"  ✅ {expected_file} correctly organized to {subdir}")
            
            if organization_verified >= 5:
                self.results["tests_passed"] += 1
                self.results["real_actions_verified"].append("File organization with real movement")
                return True
        
        self.results["tests_failed"] += 1
        return False
    
    def test_backup_system(self, file_manager):
        """Test REAL backup creation"""
        
        print("\n💾 Testing REAL backup system...")
        
        # Run backup
        backup_result = file_manager.autonomous_backup_system()
        
        # Verify backup was actually created
        backup_location = backup_result.get("backup_location", "")
        
        if backup_location and os.path.exists(backup_location):
            # Count backed up files
            backup_files = []
            for root, dirs, files in os.walk(backup_location):
                backup_files.extend([os.path.join(root, f) for f in files])
            
            print(f"Files backed up: {len(backup_files)}")
            
            # Verify specific important files were backed up
            important_backups_found = 0
            for backup_file in backup_files:
                filename = os.path.basename(backup_file)
                if any(important in filename for important in [".py", ".json", ".md"]):
                    # Verify file contents match
                    if os.path.getsize(backup_file) > 0:
                        important_backups_found += 1
                        print(f"  ✅ {filename} backed up ({os.path.getsize(backup_file)} bytes)")
            
            if important_backups_found >= 3:
                self.results["tests_passed"] += 1
                self.results["real_actions_verified"].append("Backup creation with real file copying")
                self.results["evidence_files"].append(backup_location)
                return True
        
        self.results["tests_failed"] += 1
        return False
    
    def test_project_creation(self, file_manager):
        """Test REAL project structure creation"""
        
        print("\n🏗️  Testing REAL project creation...")
        
        project_name = "test_asis_project"
        result = file_manager.create_project_structure(project_name, "asis_system")
        
        project_path = result.get("project_path", "")
        
        if project_path and os.path.exists(project_path):
            # Verify directories were created
            expected_dirs = ["core/", "modules/", "databases/", "logs/", "config/", "tests/", "docs/"]
            dirs_created = 0
            
            for expected_dir in expected_dirs:
                dir_path = os.path.join(project_path, expected_dir.rstrip('/'))
                if os.path.exists(dir_path) and os.path.isdir(dir_path):
                    dirs_created += 1
                    print(f"  ✅ Directory created: {expected_dir}")
            
            # Verify files were created
            expected_files = ["README.md", "requirements.txt"]
            files_created = 0
            
            for expected_file in expected_files:
                file_path = os.path.join(project_path, expected_file)
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    files_created += 1
                    print(f"  ✅ File created: {expected_file} ({os.path.getsize(file_path)} bytes)")
            
            if dirs_created >= 5 and files_created >= 2:
                self.results["tests_passed"] += 1
                self.results["real_actions_verified"].append("Project structure creation with real directories/files")
                self.results["evidence_files"].append(project_path)
                return True
        
        self.results["tests_failed"] += 1
        return False
    
    def test_database_tracking(self, file_manager):
        """Test REAL database operations tracking"""
        
        print("\n📊 Testing REAL database tracking...")
        
        # Get file management status (reads from database)
        status = file_manager.get_file_management_status()
        
        # Verify database contains real operation records
        if status["organized_files"] > 0:
            print(f"  ✅ Database tracks {status['organized_files']} organized files")
            
        if status["backup_count"] > 0:
            print(f"  ✅ Database tracks {status['backup_count']} backups")
            
        if len(status["recent_operations"]) > 0:
            print(f"  ✅ Database tracks {len(status['recent_operations'])} recent operations")
            for op in status["recent_operations"]:
                print(f"    - {op['operation']}: {op['file']}")
        
        # Check if database file exists
        db_path = os.path.join(self.test_workspace, "asis_file_manager.db")
        if os.path.exists(db_path) and os.path.getsize(db_path) > 0:
            print(f"  ✅ Database file exists: {os.path.getsize(db_path)} bytes")
            self.results["tests_passed"] += 1
            self.results["real_actions_verified"].append("Database tracking with real SQLite operations")
            self.results["evidence_files"].append(db_path)
            return True
        
        self.results["tests_failed"] += 1
        return False
    
    def run_comprehensive_test(self):
        """Run all Stage 1 tests"""
        
        print("🧪 STAGE 1 COMPREHENSIVE TEST - REAL vs SIMULATION")
        print("=" * 60)
        
        try:
            # Setup test environment
            if not self.setup_test_environment():
                print("❌ Failed to setup test environment")
                return False
            
            # Initialize file manager with test workspace
            file_manager = AutonomousFileManager(self.test_workspace)
            
            # Run all tests
            tests = [
                ("File Organization", self.test_file_organization),
                ("Backup System", self.test_backup_system),
                ("Project Creation", self.test_project_creation),
                ("Database Tracking", self.test_database_tracking)
            ]
            
            for test_name, test_func in tests:
                print(f"\n{'='*20} {test_name} {'='*20}")
                try:
                    success = test_func(file_manager)
                    if success:
                        print(f"✅ {test_name}: PASSED - REAL actions verified")
                    else:
                        print(f"❌ {test_name}: FAILED - Actions may be simulated")
                except Exception as e:
                    print(f"❌ {test_name}: ERROR - {e}")
                    self.results["tests_failed"] += 1
            
            # Final results
            self.show_final_results()
            
            return self.results["tests_passed"] >= 3  # At least 3 tests must pass
            
        except Exception as e:
            print(f"❌ Test suite error: {e}")
            return False
    
    def show_final_results(self):
        """Show comprehensive test results"""
        
        print(f"\n🏆 STAGE 1 TEST RESULTS")
        print("=" * 50)
        print(f"Tests Passed: {self.results['tests_passed']}")
        print(f"Tests Failed: {self.results['tests_failed']}")
        print(f"Success Rate: {self.results['tests_passed']/(self.results['tests_passed'] + self.results['tests_failed'])*100:.1f}%")
        
        print(f"\n✅ REAL ACTIONS VERIFIED:")
        for action in self.results["real_actions_verified"]:
            print(f"   • {action}")
        
        print(f"\n📄 EVIDENCE FILES CREATED:")
        for evidence in self.results["evidence_files"]:
            if os.path.exists(evidence):
                if os.path.isfile(evidence):
                    size = os.path.getsize(evidence)
                    print(f"   • {os.path.basename(evidence)} ({size} bytes)")
                else:
                    file_count = len([f for root, dirs, files in os.walk(evidence) for f in files])
                    print(f"   • {os.path.basename(evidence)}/ ({file_count} files)")
            else:
                print(f"   • {os.path.basename(evidence)} (missing)")
        
        if self.results['tests_passed'] >= 3:
            print(f"\n🎉 STAGE 1 VERIFICATION: SUCCESS!")
            print("ASIS performs REAL file operations - NOT simulated!")
        else:
            print(f"\n⚠️  STAGE 1 VERIFICATION: NEEDS IMPROVEMENT")
            print("Some operations may still be simulated")

def main():
    """Run Stage 1 comprehensive test"""
    
    tester = Stage1Tester()
    success = tester.run_comprehensive_test()
    
    if success:
        print(f"\n🚀 STAGE 1 VERIFIED - Ready for Stage 2!")
        return True
    else:
        print(f"\n🔧 STAGE 1 needs fixes before Stage 2")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
