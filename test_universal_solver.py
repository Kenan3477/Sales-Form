#!/usr/bin/env python3
"""
Simple test script for ASIS Universal Solver
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_universal_solver():
    """Simple test of the Universal Solver"""
    try:
        print("🧪 Testing ASIS Universal Solver...")
        
        # Import the solver
        from asis_universal_solver import ASISUniversalSolver
        
        # Initialize solver
        print("📦 Initializing Universal Solver...")
        solver = ASISUniversalSolver()
        
        # Test problem
        test_problem = "How can I improve my team's productivity while maintaining work-life balance?"
        
        print(f"🤔 Test Problem: {test_problem}")
        print("⏳ Processing...")
        
        # Solve the problem
        result = solver.solve_problem(test_problem)
        
        if "error" not in result:
            print("✅ SUCCESS! Universal Solver is working correctly")
            print(f"📊 Solutions Generated: {len(result['solution_approaches'])}")
            
            if result['solution_approaches']:
                best = result['solution_approaches'][0]
                print(f"🏆 Best Strategy: {best['strategy']}")
                print(f"📈 Confidence: {best['confidence_score']:.2f}")
                print(f"⏱️  Estimated Time: {best['estimated_time']} minutes")
            
            print(f"🔗 Pattern Matches: {len(result['pattern_matches'])}")
            print(f"🧠 Learning Integration: {len(result['learning_integration']['learning_recommendations'])} recommendations")
            
            # Test statistics
            stats = solver.get_solver_statistics()
            print(f"📈 System Stats: {stats['total_sessions']} sessions, {stats['total_solutions_generated']} solutions")
            
            return True
        else:
            print(f"❌ ERROR: {result['error']}")
            return False
            
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test Error: {e}")
        return False

if __name__ == "__main__":
    success = test_universal_solver()
    if success:
        print("\n🎉 ASIS Universal Solver Test PASSED!")
    else:
        print("\n💥 ASIS Universal Solver Test FAILED!")
    
    sys.exit(0 if success else 1)
