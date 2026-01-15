#!/usr/bin/env python3
"""
🧠 ASIS Novel Problem Solving Test

Quick test to verify the NovelProblemSolvingEngine import issue is resolved.
"""

def test_novel_problem_solving():
    """Test the Novel Problem Solving Engine import and functionality."""
    
    print("🧠 TESTING NOVEL PROBLEM SOLVING ENGINE")
    print("=" * 50)
    
    try:
        # Test direct import
        print("📦 Testing direct import...")
        from asis_novel_problem_solving_engine import NovelProblemSolvingEngine
        print("✅ NovelProblemSolvingEngine imported successfully")
        
        # Test initialization
        print("🔧 Testing engine initialization...")
        engine = NovelProblemSolvingEngine()
        print("✅ Engine initialized successfully")
        
        # Test Master Orchestrator import
        print("🎯 Testing Master Orchestrator integration...")
        from asis_master_orchestrator import ASISMasterOrchestrator
        orchestrator = ASISMasterOrchestrator()
        print("✅ Master Orchestrator imported and initialized")
        
        # Check if novel problem solving is available
        if hasattr(orchestrator, 'components') and 'novel_problem_solving' in orchestrator.components:
            print("✅ Novel problem solving component loaded in orchestrator")
        else:
            print("⚠️ Novel problem solving component will be lazy-loaded")
        
        print("\n" + "=" * 50)
        print("🎉 NOVEL PROBLEM SOLVING TEST COMPLETE!")
        print("✅ All imports and initialization successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_novel_problem_solving()
    print(f"\n{'🎯 SUCCESS: Novel Problem Solving Fixed!' if success else '🔧 NEEDS ATTENTION: Import still failing'}")
