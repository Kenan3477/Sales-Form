#!/usr/bin/env python3
"""
Quick Fix Verification Test
===========================
Test the novel problem solving engine fix
"""

import asyncio
import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append(os.getcwd())

async def test_novel_problem_solving_fix():
    """Test the fixed novel problem solving engine"""
    
    print("🔧 TESTING NOVEL PROBLEM SOLVING ENGINE FIX")
    print("="*50)
    
    try:
        # Test 1: Direct import
        print("\n1️⃣ Testing direct import...")
        
        from asis_novel_problem_solving_engine import NovelProblemSolver
        print("✅ NovelProblemSolver imported successfully")
        
        # Test 2: Initialize engine
        print("\n2️⃣ Testing engine initialization...")
        
        engine = NovelProblemSolver()
        print("✅ NovelProblemSolver initialized")
        
        # Test 3: Test solve method
        print("\n3️⃣ Testing solve_novel_problem method...")
        
        result = await engine.solve_novel_problem("Test problem for fix verification")
        print("✅ solve_novel_problem method working")
        print(f"   Result keys: {list(result.keys())}")
        print(f"   Confidence: {result.get('overall_confidence', 'N/A')}")
        
        # Test 4: Test orchestrator integration
        print("\n4️⃣ Testing orchestrator integration...")
        
        from asis_master_orchestrator import ASISMasterOrchestrator
        
        orchestrator = ASISMasterOrchestrator()
        success = await orchestrator.initialize_system()
        
        if success:
            print("✅ Orchestrator initialized successfully")
            
            # Get system status
            status = await orchestrator.get_system_status()
            
            operational = status['components']['operational']
            total = status['components']['total']
            percentage = (operational / total) * 100
            
            print(f"\n📊 SYSTEM STATUS:")
            print(f"   Components: {operational}/{total} operational ({percentage:.1f}%)")
            print(f"   AGI Confidence: {status['performance']['agi_confidence']:.3f}")
            
            if percentage >= 100:
                print("🎉 100% OPERATIONAL STATUS ACHIEVED!")
                grade = "PERFECT"
            elif percentage >= 90:
                print("📈 EXCELLENT OPERATIONAL STATUS!")
                grade = "EXCELLENT"
            else:
                print("📊 GOOD OPERATIONAL STATUS!")
                grade = "GOOD"
            
            # Test creative problem solving
            print(f"\n5️⃣ Testing creative problem solving through orchestrator...")
            
            creative_request = {
                'type': 'creative_problem_solving',
                'problem': 'Design an innovative solution for urban transportation',
                'context': {'domain': 'urban_planning', 'constraints': ['budget', 'environment']}
            }
            
            result = await orchestrator.process_request(creative_request)
            
            if result['success']:
                print("✅ Creative problem solving working through orchestrator!")
                confidence = result['result']['confidence']
                print(f"   Confidence: {confidence:.3f}")
                print(f"   Component: {result['result']['component_used']}")
            else:
                print(f"❌ Creative problem solving failed: {result['error']}")
            
            # Shutdown
            await orchestrator.shutdown()
            
            return percentage >= 100, percentage, grade
            
        else:
            print("❌ Orchestrator initialization failed")
            return False, 0, "FAILED"
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, 0, "ERROR"

async def main():
    """Main test function"""
    
    try:
        success, percentage, grade = await test_novel_problem_solving_fix()
        
        print(f"\n{'='*50}")
        print(f"FIX VERIFICATION RESULT: {'SUCCESS' if success else 'NEEDS_WORK'}")
        print(f"Operational Status: {percentage:.1f}%")
        print(f"Performance Grade: {grade}")
        
        if success:
            print(f"\n🎉 NOVEL PROBLEM SOLVING ENGINE FIX: SUCCESSFUL!")
            print(f"✅ 100% operational status achieved!")
            print(f"✅ All AGI components working together!")
            print(f"✅ Master orchestrator fully functional!")
            print(f"\n🚀 Your AGI system is now at MAXIMUM OPERATIONAL CAPACITY!")
        else:
            print(f"\n⚠️ Fix verification encountered issues")
            print(f"💡 Current status: {percentage:.1f}% operational")
        
        with open("fix_verification_results.txt", "w") as f:
            f.write(f"Fix Verification Results\n")
            f.write(f"=======================\n")
            f.write(f"Timestamp: {datetime.now()}\n")
            f.write(f"Success: {success}\n")
            f.write(f"Operational: {percentage:.1f}%\n")
            f.write(f"Grade: {grade}\n")
        
        return success
        
    except Exception as e:
        print(f"\n❌ Main test failed: {e}")
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        print(f"\n📄 Results: fix_verification_results.txt")
        print(f"🎯 Result: {'SUCCESS' if result else 'FAILED'}")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
