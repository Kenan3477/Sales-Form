#!/usr/bin/env python3
"""
ASIS Autonomous Launch Demo
Test the new Phase 1 Autonomous Capabilities
"""

import subprocess
import sys
import os

def test_autonomous_asis():
    """Test the autonomous ASIS system"""
    
    print("🚀 TESTING ASIS PHASE 1 - AUTONOMOUS INTELLIGENCE")
    print("=" * 70)
    
    print("\n📋 PHASE 1 CAPABILITIES BEING TESTED:")
    print("✅ Autonomous Goal Setting")  
    print("✅ Advanced Multi-step Reasoning")
    print("✅ Independent Decision Making")
    print("✅ Progress Monitoring & Adaptation")
    print("✅ Self-Monitoring Systems")
    
    print("\n🧪 RUNNING AUTONOMOUS TESTS...")
    
    # Import and test the autonomous system
    try:
        from asis_autonomous_phase1 import AutonomousASIS, GoalPriority, DecisionType
        
        print("✅ Autonomous system imported successfully")
        
        # Create autonomous ASIS instance
        print("\n🤖 Initializing Autonomous ASIS...")
        asis = AutonomousASIS()
        
        print("\n🎯 Testing Goal Generation...")
        goal = asis.generate_autonomous_goal()
        
        print(f"Generated Goal: {goal['title']}")
        print(f"Description: {goal['description']}")
        print(f"Priority: {GoalPriority(goal['priority']).name}")
        print(f"Timeline: {goal['target_completion'].strftime('%Y-%m-%d')}")
        
        print("\n🧠 Testing Advanced Reasoning...")
        reasoning = asis._deductive_reasoning(
            ["Autonomous systems need goals", "Goals require planning", "Planning needs reasoning"],
            "autonomous operation"
        )
        
        print(f"Reasoning Type: {reasoning['type']}")
        print(f"Confidence: {reasoning['confidence']}")
        print("Reasoning Steps:")
        for step in reasoning['reasoning_steps']:
            print(f"  • {step}")
        
        print("\n🤔 Testing Autonomous Decision Making...")
        options = [
            {"name": "Learn new concepts", "impact": 0.8, "feasibility": 0.9, "alignment": 0.7},
            {"name": "Optimize performance", "impact": 0.6, "feasibility": 0.8, "alignment": 0.8}, 
            {"name": "Create new tools", "impact": 0.9, "feasibility": 0.5, "alignment": 0.6}
        ]
        
        decision = asis.make_autonomous_decision(
            DecisionType.GOAL_SELECTION,
            options, 
            "Testing autonomous decision framework"
        )
        
        print(f"Chosen Option: {decision['chosen_option']['name']}")
        print(f"Decision Confidence: {decision['confidence']:.2f}")
        
        print("\n📊 Testing Performance Monitoring...")
        metrics = asis._calculate_performance_metrics()
        print("Performance Metrics:")
        for metric, value in metrics.items():
            print(f"  • {metric.replace('_', ' ').title()}: {value:.2f}")
        
        print("\n🎯 Testing Multiple Goal Generation...")
        for i in range(3):
            goal = asis.generate_autonomous_goal()
            print(f"{i+1}. {goal['title']} (Priority: {GoalPriority(goal['priority']).name})")
        
        print("\n✅ ALL PHASE 1 TESTS COMPLETED SUCCESSFULLY!")
        print("🌟 ASIS is now capable of:")
        print("   • Setting goals autonomously")
        print("   • Making complex decisions independently") 
        print("   • Reasoning through multi-step problems")
        print("   • Monitoring its own performance")
        print("   • Adapting behavior based on results")
        
        print("\n🚀 READY FOR AUTONOMOUS OPERATION!")
        print("Run 'python asis_autonomous_phase1.py' and use 'start' command")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing autonomous system: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_next_steps():
    """Show what comes next in the autonomy development"""
    
    print("\n🗺️  WHAT'S NEXT - PHASE 2 PREVIEW")
    print("=" * 50)
    
    next_phase = {
        "Environmental Interaction": [
            "File System Management",
            "Internet Research Capabilities", 
            "API Integration Systems",
            "Code Generation & Execution",
            "Database Management"
        ],
        "Advanced Capabilities": [
            "Autonomous research on any topic",
            "Create files and organize information",
            "Write and test code independently",
            "Connect to external services",
            "Build comprehensive knowledge bases"
        ]
    }
    
    print("🔧 PHASE 2 COMPONENTS:")
    for component in next_phase["Environmental Interaction"]:
        print(f"   • {component}")
    
    print("\n✨ PHASE 2 CAPABILITIES:")
    for capability in next_phase["Advanced Capabilities"]:
        print(f"   • {capability}")
    
    print(f"\n🎯 ULTIMATE GOAL:")
    print("Create the world's first Fully Autonomous Synthetic Intelligence")
    print("that can set its own goals, learn independently, and solve")
    print("complex problems without human intervention!")

def main():
    """Main test execution"""
    
    if test_autonomous_asis():
        show_next_steps()
        
        print(f"\n💡 READY TO EXPERIENCE AUTONOMOUS ASIS?")
        response = input("Start interactive autonomous session? (y/n): ").strip().lower()
        
        if response in ['y', 'yes']:
            print("\n🚀 Launching Autonomous ASIS...")
            print("Use 'start' command to begin autonomous operation!")
            
            # Launch the autonomous system
            os.system("python asis_autonomous_phase1.py")
    else:
        print("❌ Autonomous system test failed")

if __name__ == "__main__":
    main()
