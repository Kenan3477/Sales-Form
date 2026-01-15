#!/usr/bin/env python3
"""
Quick test of the REAL autonomous ASIS system
"""

import sys
import os
sys.path.append(os.getcwd())

try:
    from asis_real_autonomous_phase1 import RealAutonomousASIS, ActionType
    
    print("🔥 Creating REAL Autonomous ASIS...")
    asis = RealAutonomousASIS()
    
    print("🎯 Generating a REAL goal...")
    goal = asis.generate_real_autonomous_goal()
    print(f"Goal: {goal['title']}")
    print(f"Description: {goal['description']}")
    
    print("💾 Saving goal to database...")
    goal_id = asis._save_goal(goal)
    goal["id"] = goal_id
    
    print(f"⚡ Executing REAL action: CREATE_FILE...")
    result = asis.execute_real_action(goal, ActionType.CREATE_FILE)
    
    print(f"Result: {result}")
    
    if result["success"]:
        print(f"✅ PROOF: File created at {result.get('evidence_path', 'Unknown')}")
        
        # Check if file actually exists
        if "evidence_path" in result:
            if os.path.exists(result["evidence_path"]):
                print(f"✅ VERIFIED: File exists on disk!")
                print(f"📄 File size: {os.path.getsize(result['evidence_path'])} bytes")
            else:
                print(f"❌ File not found")
    
    print("🔥 REAL autonomous action test completed!")
    
    # Show evidence
    asis.show_real_work_evidence()
    
except Exception as e:
    import traceback
    print(f"❌ Error: {e}")
    print("Traceback:")
    traceback.print_exc()
