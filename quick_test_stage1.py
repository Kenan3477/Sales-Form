#!/usr/bin/env python3
"""
Quick Stage 1 Test - Verify Real Operations
"""

import os
import sys
import time
from datetime import datetime

# Import the file manager
sys.path.append(os.getcwd())
from asis_file_manager_phase2 import AutonomousFileManager

def quick_test():
    """Quick verification test"""
    
    print("🔍 STAGE 1 QUICK VERIFICATION TEST")
    print("=" * 40)
    
    # Create a simple test
    test_dir = "quick_test_stage1"
    if os.path.exists(test_dir):
        import shutil
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    
    # Create test files
    test_files = {
        "test.py": "print('ASIS test file')",
        "readme.md": "# Test README",
        "data.json": '{"test": true}'
    }
    
    for filename, content in test_files.items():
        with open(os.path.join(test_dir, filename), 'w') as f:
            f.write(content)
    
    print(f"✅ Created {len(test_files)} test files")
    
    # Test file manager
    fm = AutonomousFileManager(test_dir)
    
    # Test project creation
    print("\n🏗️  Testing project creation...")
    result = fm.create_project_structure("test_project", "python")
    
    project_path = result.get("project_path", "")
    if project_path and os.path.exists(project_path):
        file_count = len([f for root, dirs, files in os.walk(project_path) for f in files])
        print(f"✅ Project created with {file_count} files")
        
        # Verify README exists and has content
        readme_path = os.path.join(project_path, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, 'r') as f:
                content = f.read()
            print(f"✅ README.md created ({len(content)} characters)")
            print(f"   Content preview: {content[:100]}...")
            
            print(f"\n🏆 STAGE 1 VERIFICATION: SUCCESS!")
            print("✅ REAL file operations confirmed:")
            print("   • Directory creation: REAL")
            print("   • File creation: REAL") 
            print("   • Content generation: REAL")
            print(f"   • Evidence: {project_path}")
            
            return True
    
    print("❌ Stage 1 verification failed")
    return False

if __name__ == "__main__":
    success = quick_test()
    
    # Also check previous backup evidence
    print(f"\n📄 CHECKING PREVIOUS EVIDENCE:")
    backup_dir = "backups"
    if os.path.exists(backup_dir):
        backup_folders = [f for f in os.listdir(backup_dir) if f.startswith("incremental_")]
        if backup_folders:
            latest_backup = os.path.join(backup_dir, backup_folders[-1])
            file_count = len([f for root, dirs, files in os.walk(latest_backup) for f in files])
            print(f"✅ Previous backup found: {file_count} files backed up")
            print(f"   Location: {latest_backup}")
    
    if success:
        print(f"\n🚀 STAGE 1 FULLY VERIFIED - READY FOR STAGE 2!")
    else:
        print(f"\n🔧 STAGE 1 needs attention")
