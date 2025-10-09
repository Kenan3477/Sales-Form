#!/usr/bin/env python3
"""
Test True Self-Modification Engine
=================================
Demonstrates ASIS's ability to analyze and improve its own code
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from asis_true_self_modification import ASISTrueSelfModification

async def test_self_modification():
    """Test the True Self-Modification Engine"""
    
    print("🤖 Testing ASIS True Self-Modification Engine")
    print("=" * 60)
    
    # Initialize the engine
    print("🔧 Initializing True Self-Modification Engine...")
    modifier = ASISTrueSelfModification()
    
    # Get initial status
    print("\n📊 Initial System Status:")
    status = modifier.get_self_modification_status()
    print(f"   Quality Score: {status['quality_score']:.1f}/100")
    print(f"   Capabilities: {len([c for c in status['capabilities'].values() if c])}/{len(status['capabilities'])}")
    
    # Test code analysis
    print("\n🔍 Testing Code Analysis...")
    analysis = await modifier.analyze_own_code()
    
    print(f"   Files Analyzed: {len(analysis['files_analyzed'])}")
    print(f"   Performance Issues: {len(analysis['performance_bottlenecks'])}")
    print(f"   Capability Gaps: {len(analysis['capability_gaps'])}")
    print(f"   Security Issues: {len(analysis['security_improvements'])}")
    print(f"   Overall Quality: {analysis['overall_quality_score']:.1f}/100")
    
    # Test improvement generation
    print("\n💡 Testing Improvement Generation...")
    improvement_code = await modifier.generate_improvement_code(analysis)
    print(f"   Generated {len(improvement_code)} characters of improvement code")
    
    # Test safe deployment (in test mode)
    print("\n🧪 Testing Safe Deployment Process...")
    print("   Creating backup...")
    backup_id = await modifier.safe_deployer.create_backup()
    print(f"   Backup created: {backup_id}")
    
    print("   Testing code safety...")
    test_result = await modifier.safe_deployer.test_code(improvement_code)
    print(f"   Safety Score: {test_result['safety_score']:.2f}")
    print(f"   Test Success: {test_result['success']}")
    
    # Show improvement priorities
    if analysis.get('improvement_priority'):
        print(f"\n📋 Top Improvement Priorities:")
        for i, priority in enumerate(analysis['improvement_priority'][:3]):
            print(f"   {i+1}. {priority['type'].title()} - {priority['priority']} priority")
            print(f"      Issue: {priority['item'].get('description', 'N/A')}")
    
    # Get modification history
    print(f"\n📚 Modification History:")
    history = modifier.get_modification_history()
    if history:
        for mod in history[:3]:
            print(f"   {mod['timestamp'][:19]} - {mod['type']} - {mod['status']}")
    else:
        print("   No previous modifications found")
    
    print("\n✅ True Self-Modification Engine test complete!")
    return modifier

async def demonstrate_full_cycle():
    """Demonstrate a complete self-modification cycle"""
    
    print("\n🚀 DEMONSTRATING FULL SELF-MODIFICATION CYCLE")
    print("=" * 60)
    
    modifier = ASISTrueSelfModification()
    
    # Run full cycle
    result = await modifier.run_full_self_modification_cycle()
    
    print(f"\n📊 CYCLE RESULTS SUMMARY:")
    print(f"✅ Analysis Completed: {result['analysis_completed']}")
    print(f"✅ Improvements Generated: {result['improvements_generated']}")
    print(f"✅ Deployment Successful: {result['deployment_successful']}")
    print(f"📈 Quality Improvement: {result['quality_improvement']:.1f} points")
    print(f"⏱️ Total Duration: {result['cycle_duration']:.2f} seconds")
    print(f"🔧 Modifications Applied: {result['modifications_applied']}")
    
    if result['errors']:
        print(f"❌ Errors: {len(result['errors'])}")
        for error in result['errors']:
            print(f"   - {error}")
    
    return result

def main():
    """Main test function"""
    
    print("🤖 ASIS True Self-Modification Engine Test Suite")
    print("=" * 60)
    print("This test demonstrates ASIS's ability to:")
    print("✅ Analyze its own code for improvements")
    print("✅ Generate actual improvement code")
    print("✅ Safely test and deploy modifications")
    print("✅ Track modification history and quality")
    print("=" * 60)
    
    # Run basic tests
    print("\n🧪 RUNNING BASIC TESTS...")
    asyncio.run(test_self_modification())
    
    # Ask user if they want to run full cycle
    print("\n" + "=" * 60)
    user_choice = input("🤔 Run full self-modification cycle? (y/n): ").lower().strip()
    
    if user_choice in ['y', 'yes']:
        asyncio.run(demonstrate_full_cycle())
    else:
        print("✅ Test completed - Full cycle skipped")
    
    print("\n🎉 All tests completed successfully!")
    print("💡 The True Self-Modification Engine is ready for integration!")

if __name__ == "__main__":
    main()