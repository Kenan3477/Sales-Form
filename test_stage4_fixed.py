#!/usr/bin/env python3
"""
ASIS Stage 4 FIXED - Quick Test to Achieve 100% Success
======================================================

Test the fixed code generator to achieve 100% execution success
"""

import os
import sys
import shutil
from datetime import datetime

# Import the fixed code generator
sys.path.append(os.path.dirname(__file__))
from asis_code_generator_stage4_fixed import AutonomousCodeGeneratorFixed

def test_fixed_code_generation():
    """Test fixed code generation for 100% success"""
    
    print("🧪 ASIS Stage 4 FIXED - Quick Test for 100% Success")
    print("=" * 60)
    
    # Clean test directory
    test_directory = os.path.join(os.getcwd(), "stage4_fixed_test")
    if os.path.exists(test_directory):
        shutil.rmtree(test_directory)
    
    # Initialize fixed generator
    generator = AutonomousCodeGeneratorFixed(test_directory)
    
    # Test projects
    test_projects = [
        ("data_processor", "autonomous data analysis system"),
        ("automation_tool", "file management utilities"), 
        ("api_service", "REST API service")
    ]
    
    results = {
        "projects_generated": 0,
        "files_created": 0,
        "executions_attempted": 0,
        "executions_successful": 0,
        "success_rate": 0
    }
    
    print("\n🚀 Generating and Testing Projects...")
    
    for project_type, requirements in test_projects:
        print(f"\n--- Testing {project_type} ---")
        
        # Generate project
        result = generator.generate_project(project_type, requirements)
        
        if result["success"]:
            results["projects_generated"] += 1
            results["files_created"] += len(result["files_created"])
            
            print(f"✅ Project generated: {len(result['files_created'])} files")
            
            # Test execution of each Python file
            for code_file in result["files_created"]:
                if code_file.endswith('.py'):
                    results["executions_attempted"] += 1
                    
                    exec_result = generator.execute_generated_code(
                        result["project_path"], code_file
                    )
                    
                    if exec_result["success"]:
                        results["executions_successful"] += 1
                        print(f"   ✅ {code_file} executed successfully")
                        print(f"      Output length: {len(exec_result['output'])} chars")
                    else:
                        print(f"   ❌ {code_file} execution failed:")
                        print(f"      Error: {exec_result.get('error', 'Unknown')}")
        else:
            print(f"❌ Project generation failed: {result.get('error', 'Unknown')}")
    
    # Calculate final results
    if results["executions_attempted"] > 0:
        results["success_rate"] = (results["executions_successful"] / results["executions_attempted"]) * 100
    
    print(f"\n🎯 FINAL RESULTS:")
    print(f"   Projects Generated: {results['projects_generated']}")
    print(f"   Files Created: {results['files_created']}")
    print(f"   Executions Attempted: {results['executions_attempted']}")
    print(f"   Executions Successful: {results['executions_successful']}")
    print(f"   SUCCESS RATE: {results['success_rate']:.1f}%")
    
    if results["success_rate"] >= 100:
        print("   🎉 STAGE 4 FIXED: 100% SUCCESS ACHIEVED!")
    elif results["success_rate"] >= 90:
        print("   🎉 STAGE 4 FIXED: EXCELLENT SUCCESS RATE!")
    else:
        print("   ⚠️  Still needs improvement")
    
    # Check file system evidence
    if os.path.exists(test_directory):
        total_files = 0
        total_size = 0
        
        for root, dirs, files in os.walk(test_directory):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.exists(file_path):
                    total_files += 1
                    total_size += os.path.getsize(file_path)
        
        print(f"\n📁 File System Evidence:")
        print(f"   Total Files Created: {total_files}")
        print(f"   Total Size: {total_size} bytes ({total_size/1024:.2f} KB)")
        print("   STATUS: REAL file creation verified (not simulated)")
    
    return results

if __name__ == "__main__":
    test_fixed_code_generation()
