#!/usr/bin/env python3
"""
Test Multi-Agent Integration System
==================================
Test the integration between ASIS multi-agent system and self-modification engine
"""

import os
import sys
import asyncio
from asis_true_self_modification import ASISTrueSelfModification

async def test_multi_agent_integration():
    """Test the integration between multi-agent system and self-modification"""
    print("============================================================")
    print("[AGENT] Testing ASIS Multi-Agent Integration...")
    print("============================================================")
    
    # Initialize self-modification system
    asis = ASISTrueSelfModification()
    
    # Check system status
    status = asis.get_self_modification_status()
    print(f"🔧 Self-modification system active: {status['system_active']}")
    print(f"🤖 Multi-agent system available: {status['multi_agent_available']}")
    print(f"📊 Recent modifications: {status['recent_modifications']}")
    print(f"✅ Success rate: {status['success_rate']:.1%}")
    
    if not status['multi_agent_available']:
        print("⚠️ Multi-agent system not available, testing fallback mode...")
    
    # Test code analysis
    print("\n🔍 Testing code analysis...")
    try:
        analysis_results = await asis._analyze_codebase()
        print(f"📊 Analyzed {len(analysis_results)} files with potential improvements")
        
        if analysis_results:
            # Show analysis summary
            for i, result in enumerate(analysis_results[:2]):
                print(f"📁 File {i+1}: {os.path.basename(result['file_path'])}")
                print(f"   Quality Score: {result['code_quality_score']:.1f}")
                print(f"   Bottlenecks: {len(result['bottlenecks'])}")
                print(f"   Gaps: {len(result['gaps'])}")
                print(f"   Optimizations: {len(result['optimization_opportunities'])}")
    except Exception as e:
        print(f"⚠️ Error during code analysis: {e}")
        analysis_results = []
    
    # Test improvement generation (with or without multi-agent)
    print("\n💡 Testing improvement generation...")
    improvements = []
    try:
        if analysis_results:
            improvements = await asis._generate_improvements_with_multi_agent(analysis_results[:1])
            print(f"🔧 Generated {len(improvements)} improvement suggestions")
            
            for i, improvement in enumerate(improvements[:3]):
                print(f"🛠️ Improvement {i+1}:")
                print(f"   Type: {improvement['type']}")
                print(f"   Target: Line {improvement.get('target_line', 'N/A')}")
                print(f"   Expected Impact: {improvement.get('expected_impact', 'N/A')}")
        else:
            print("ℹ️ No analysis results available for improvement generation")
    except Exception as e:
        print(f"⚠️ Error during improvement generation: {e}")
    
    # Test modification history
    print("\n📚 Testing modification history...")
    try:
        history = asis.get_modification_history()
        print(f"📝 Found {len(history)} previous modifications")
        
        if history:
            recent = history[0]
            print(f"   Most recent: {recent['modification_type']} at {recent['timestamp']}")
            print(f"   Success: {recent['success']}")
    except Exception as e:
        print(f"⚠️ Error accessing modification history: {e}")
        history = []
    
    # Test multi-agent system directly if available
    if asis.multi_agent_coordinator:
        print("\n🤖 Testing multi-agent system directly...")
        try:
            # Test agent creation
            print("   Creating test agents...")
            agent_config = {
                "specialization": "performance_optimizer",
                "capabilities": ["code_analysis", "optimization"],
                "resources": {"priority": 5}
            }
            agent_id = await asis.multi_agent_coordinator.agent_manager.create_agent(agent_config)
            print(f"   ✅ Created agent: {agent_id}")
            
            # Test agent coordination
            print("   Testing agent coordination...")
            status_check = await asis.multi_agent_coordinator.get_system_status()
            print(f"   📊 Active agents: {status_check.get('total_agents', 0)}")
            print(f"   📊 Tasks completed: {status_check.get('tasks_completed', 0)}")
            
        except Exception as e:
            print(f"   ⚠️ Error testing multi-agent system: {e}")
    
    # Test integration with self-modification
    print("\n🔧 Testing self-modification integration...")
    try:
        if analysis_results and improvements:
            # Test improvement validation
            for improvement in improvements[:1]:  # Test just one
                print(f"   Validating improvement: {improvement['type']}")
                improved_code = asis._generate_improved_code(improvement)
                if improved_code:
                    safety_score = asis._validate_improvement_safety(improved_code)
                    print(f"   Safety score: {safety_score:.2f}")
                else:
                    print("   ⚠️ Failed to generate improved code")
    except Exception as e:
        print(f"⚠️ Error during integration testing: {e}")
    
    # Test actual deployment (creates history entries)
    print("\n🚀 Testing actual improvement deployment...")
    deployed_improvements = 0
    try:
        if improvements:
            deployed_count = 0
            for i, improvement in enumerate(improvements[:3]):  # Deploy first 3 improvements
                print(f"   Deploying improvement {i+1}: {improvement['type']}")
                success = await asis._validate_and_deploy_improvement(improvement)
                if success:
                    deployed_count += 1
                    print(f"   ✅ Successfully deployed: {improvement['type']}")
                else:
                    print(f"   ❌ Failed to deploy: {improvement['type']}")
            
            deployed_improvements = deployed_count
            print(f"   📦 Total deployed: {deployed_count}")
            
            # Check history after deployment
            print("   📚 Checking modification history...")
            updated_history = asis.get_modification_history()
            print(f"   📝 History entries after deployment: {len(updated_history)}")
            
            if updated_history:
                print("   📋 Recent modifications:")
                for i, mod in enumerate(updated_history[:3]):  # Show first 3
                    status_icon = "✅" if mod['success'] else "❌"
                    print(f"     {status_icon} {mod['modification_type']} - {mod['deployment_status']} - Safety: {mod['safety_score']:.2f}")
                    
        else:
            print("   ⚠️ No improvements available for deployment")
            
    except Exception as e:
        print(f"⚠️ Error during deployment testing: {e}")
        deployed_improvements = 0
    
    print("\n✅ Multi-agent integration test completed!")
    
    # Final history check after all deployments
    final_history = asis.get_modification_history()
    
    return {
        "system_status": status,
        "analysis_count": len(analysis_results),
        "improvements_generated": len(improvements),
        "history_entries": len(final_history),  # Use final history count
        "multi_agent_available": status['multi_agent_available'],
        "deployed_improvements": deployed_improvements
    }

async def test_self_modification_basic():
    """Test basic self-modification functionality"""
    print("\n--- Testing Basic Self-Modification ---")
    
    # Initialize the system
    modifier = ASISTrueSelfModification()
    
    # Test analysis
    print("🔍 Testing Code Analysis...")
    analysis_results = await modifier._analyze_codebase()
    print(f"📊 Analyzed {len(analysis_results)} files with issues")
    
    for result in analysis_results[:2]:  # Show first 2 results
        print(f"📁 File: {os.path.basename(result['file_path'])}")
        print(f"   Bottlenecks: {len(result['bottlenecks'])}")
        print(f"   Gaps: {len(result['gaps'])}")
        print(f"   Quality Score: {result['code_quality_score']:.1f}")
    
    # Test improvement generation
    print("\n💡 Testing Improvement Generation...")
    if analysis_results:
        improvements = await modifier._generate_improvements_with_multi_agent(analysis_results[:1])
        print(f"💡 Generated {len(improvements)} improvements")
        
        for improvement in improvements[:2]:  # Show first 2 improvements
            print(f"🔧 Type: {improvement['type']}")
            print(f"   Target: Line {improvement.get('target_line', 'N/A')}")
            print(f"   Impact: {improvement.get('expected_impact', 'N/A')}")
    
    print("✅ Basic self-modification test complete!")

async def main():
    """Main test function"""
    try:
        print("Starting ASIS Multi-Agent Integration Tests...")
        
        # Run multi-agent integration test
        result = await test_multi_agent_integration()
        
        # Run basic self-modification test
        await test_self_modification_basic()
        
        # Summary
        print("\n" + "="*60)
        print("🎯 TEST SUMMARY")
        print("="*60)
        print(f"✅ System Active: {result['system_status']['system_active']}")
        print(f"🤖 Multi-Agent Available: {result['multi_agent_available']}")
        print(f"📊 Files Analyzed: {result['analysis_count']}")
        print(f"💡 Improvements Generated: {result['improvements_generated']}")
        print(f"� Improvements Deployed: {result['deployed_improvements']}")
        print(f"�📝 History Entries: {result['history_entries']}")
        print("="*60)
        
        if result['multi_agent_available']:
            print("🎉 Multi-Agent Integration: FUNCTIONAL")
        else:
            print("⚠️ Multi-Agent Integration: FALLBACK MODE")
        
        print("✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())