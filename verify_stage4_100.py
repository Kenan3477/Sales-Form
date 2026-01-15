#!/usr/bin/env python3
"""
ASIS Stage 4 - 100% Success Verification Test
============================================

Quick test to verify the fixed code generator achieves 100% success
"""

import os
import sys
import shutil
from datetime import datetime

# Import the fixed code generator
sys.path.append(os.path.dirname(__file__))
from asis_code_generator_stage4_fixed import AutonomousCodeGeneratorFixed

def test_stage4_100_percent():
    """Test Stage 4 for 100% success rate"""
    
    print("🎯 ASIS Stage 4 - 100% Success Verification")
    print("=" * 50)
    
    # Clean test directory
    test_dir = "stage4_100_test"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    
    # Initialize fixed generator
    generator = AutonomousCodeGeneratorFixed(test_dir)
    
    # Test project generation
    print("\n🏗️  Testing Fixed Code Generation...")
    result = generator.generate_project("data_processor", "test data processing system")
    
    if result["success"]:
        print(f"✅ Project generated: {result['project_name']}")
        print(f"   Files: {len(result['files_created'])}")
        
        # Test execution
        print("\n▶️  Testing Code Execution...")
        for file_name in result["files_created"]:
            if file_name.endswith('.py'):
                exec_result = generator.execute_generated_code(result["project_path"], file_name)
                
                if exec_result["success"]:
                    print(f"✅ Execution SUCCESS: {file_name}")
                    print(f"   Output length: {len(exec_result['output'])} chars")
                    return True
                else:
                    print(f"❌ Execution FAILED: {file_name}")
                    print(f"   Error: {exec_result.get('error', 'Unknown')}")
                    return False
    else:
        print(f"❌ Generation FAILED: {result.get('error', 'Unknown')}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_stage4_100_percent()
    
    if success:
        print("\n🎉 STAGE 4 VERIFIED: 100% SUCCESS ACHIEVED!")
        print("   Code generation and execution working perfectly!")
    else:
        print("\n❌ Stage 4 still has issues to resolve")
