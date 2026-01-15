#!/usr/bin/env python3
"""
🚀 ASIS QUICK AUTONOMY TEST

Quick test to verify Full Autonomy is working and get the current autonomy score.
"""

import asyncio
from asis_master_orchestrator import ASISMasterOrchestrator

async def quick_autonomy_test():
    """Quick test of the Full Autonomy system."""
    
    print("🚀 ASIS QUICK AUTONOMY TEST")
    print("=" * 40)
    
    # Initialize orchestrator
    orchestrator = ASISMasterOrchestrator()
    print("✅ Master Orchestrator initialized")
    
    # Run one autonomous cycle
    print("🔄 Running autonomous cycle...")
    result = await orchestrator.run_full_autonomous_cycle()
    
    if result and 'autonomy_score' in result:
        score = result['autonomy_score']
        level = result.get('autonomy_level', 'unknown')
        
        print(f"🎯 Autonomy Score: {score:.1%}")
        print(f"🏆 Autonomy Level: {level.upper()}")
        
        if score >= 0.9:
            print("🔥 EXCELLENT: Full autonomy achieved!")
            return True
        elif score >= 0.8:
            print("⚡ HIGH: Advanced autonomous operation!")
            return True
        elif score >= 0.65:
            print("📈 MODERATE: Good autonomous capability!")
            return True
        else:
            print("🌱 DEVELOPING: Basic autonomous functions!")
            return False
    else:
        print("❌ Failed to get autonomy score")
        return False

if __name__ == "__main__":
    success = asyncio.run(quick_autonomy_test())
    print(f"\n{'✅ SUCCESS' if success else '❌ NEEDS IMPROVEMENT'}")
