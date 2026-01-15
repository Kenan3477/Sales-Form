#!/usr/bin/env python3
"""
Simple Learning System Test
"""

import asyncio
import sys
import traceback

async def simple_learning_test():
    try:
        print("🧠 Testing Advanced Learning System")
        print("=" * 50)
        
        # Import the learning system
        print("Importing learning system...")
        from advanced_learning_system import ComprehensiveLearningSystem, LearningType
        
        # Initialize system
        print("Initializing learning system...")
        learning_system = ComprehensiveLearningSystem()
        learning_system.start()
        
        print("✅ Learning system initialized successfully!")
        
        # Test 1: Create a simple supervised learning task
        print("\n1. Testing supervised learning task creation...")
        data = ["good product", "bad service"]
        labels = [1, 0]
        
        task = learning_system.create_supervised_task("test_task", data, labels)
        print(f"✅ Task created: {task.task_id}")
        
        # Test 2: Submit and process task
        print("\n2. Testing task submission and processing...")
        await learning_system.submit_learning_task(task)
        await learning_system.process_learning_tasks()
        
        # Test 3: Get result
        print("\n3. Testing result retrieval...")
        result = learning_system.get_task_result("test_task")
        
        if result:
            print(f"✅ Task completed: Success={result.success}")
            print(f"   Strategy used: {result.strategy_used.value}")
            print(f"   Confidence: {result.confidence:.3f}")
        else:
            print("❌ No result found")
        
        # Test 4: System status
        print("\n4. Testing system status...")
        status = learning_system.get_system_status()
        print(f"✅ System status retrieved:")
        print(f"   Running: {status['is_running']}")
        print(f"   Completed tasks: {status['completed_tasks']}")
        
        # Stop system
        learning_system.stop()
        print("\n✅ Learning system test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(simple_learning_test())
    if success:
        print("\n🎉 SUCCESS: Advanced Learning System is operational!")
    else:
        print("\n💥 FAILURE: Learning system has issues")
        sys.exit(1)
