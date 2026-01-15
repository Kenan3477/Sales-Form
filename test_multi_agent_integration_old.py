#!/usr/bin/env python3
"""
ASIS Multi-Agent Integration Test
=================================
Test the integrated Multi-Agent Coordination System
"""

import asyncio
from asis_true_self_modification import ASISTrueSelfModification

async def test_multi_agent_integration():
    print('[AGENT] Testing ASIS Multi-Agent Integration...')
    print('=' * 50)
    
    # Initialize ASIS with Multi-Agent System
    asis = ASISTrueSelfModification()
    
    # Get system status including multi-agent
    status = asis.get_self_modification_status()
    print(f'[OK] System Version: {status["system_version"]}')
    print(f'[OK] Modification Engine: {status["modification_engine"]}')
    print(f'[DATA] Quality Score: {status["quality_score"]:.1f}/100')
    
    # Check capabilities
    capabilities = status['capabilities']
    print(f'\n[TOOL] Capabilities:')
    for cap, enabled in capabilities.items():
        icon = '[OK]' if enabled else '[ERROR]'
        print(f'   {icon} {cap.replace("_", " ").title()}: {enabled}')
    
    # Check multi-agent system status
    multi_agent_status = status.get('multi_agent_system', {})
    print(f'\n[AGENT] Multi-Agent System:')
    print(f'   Active: {multi_agent_status.get("multi_agent_available", False)}')
    
    if multi_agent_status.get('multi_agent_available'):
        specializations = multi_agent_status.get('specializations_supported', [])
        print(f'   Specializations Available: {len(specializations)}')
        for spec in specializations:
            print(f'     [UNICODE] {spec.replace("_", " ").title()}')
        
        strategies = multi_agent_status.get('coordination_strategies', [])
        print(f'   Coordination Strategies: {strategies}')
        
        # Test multi-agent demonstration if available
        if asis.multi_agent_system:
            print(f'\n[START] Testing Multi-Agent Demonstration...')
            try:
                demo_result = await asis.multi_agent_system.demonstrate_multi_agent_coordination()
                
                coord_result = demo_result.get('coordination_result', {})
                coord_summary = coord_result.get('coordination_summary', {})
                
                print(f'[OK] Demo completed successfully!')
                print(f'   Strategy: {coord_summary.get("strategy", "unknown")}')
                print(f'   Agents: {coord_summary.get("total_agents", 0)}')
                print(f'   Success Rate: {coord_summary.get("success_rate", 0.0):.1%}')
                print(f'   Efficiency: {coord_summary.get("efficiency_score", 0.0):.1f}')
                
                # Test spawning specialized agents
                print(f'\n[AGENT] Testing Specialized Agent Spawning...')
                try:
                    # Use the multi-agent system directly instead of non-existent method
                    multi_agent_system = asis.self_modification_engine.multi_agent_coordinator if hasattr(asis.self_modification_engine, 'multi_agent_coordinator') else None
                    
                    if multi_agent_system:
                        spawn_results = {}
                        spawn_count = 0
                        
                        for specialization in ['code_analysis', 'security', 'optimization']:
                            try:
                                agent_id = await multi_agent_system.spawn_specialized_agent(specialization, {
                                    'type': 'improvement_analysis',
                                    'priority': 'high'
                                })
                                spawn_results[specialization] = agent_id
                                spawn_count += 1
                                print(f'   [UNICODE] {specialization}: {agent_id}')
                            except Exception as e:
                                print(f'   [ERROR] Failed to spawn {specialization} agent: {e}')
                        
                        print(f'[OK] Spawned {spawn_count} specialized agents')
                    else:
                        print(f'[WARNING] Multi-agent system not available in self-modification engine')
                        
                except Exception as e:
                    print(f'[ERROR] Agent spawning test failed: {e}')
                
            except Exception as e:
                print(f'[ERROR] Multi-agent demonstration failed: {e}')
    else:
        print(f'   Reason: {multi_agent_status.get("reason", "unknown")}')
        print(f'[WARNING] Running in single agent mode')
    
    # Test enhanced self-modification cycle with multi-agent
    print(f'\n[PROCESS] Testing Enhanced Self-Modification Cycle...')
    try:
        cycle_result = await asis.run_full_self_modification_cycle(use_multi_agent=True)
        
        print(f'[OK] Cycle completed!')
        print(f'   Multi-Agent Used: {cycle_result.get("multi_agent_used", False)}')
        print(f'   Analysis: {"[OK]" if cycle_result["analysis_completed"] else "[ERROR]"}')
        print(f'   Improvements: {"[OK]" if cycle_result["improvements_generated"] else "[ERROR]"}')
        print(f'   Deployment: {"[OK]" if cycle_result["deployment_successful"] else "[ERROR]"}')
        print(f'   Quality Improvement: {cycle_result["quality_improvement"]:.1f}')
        print(f'   Duration: {cycle_result["cycle_duration"]:.2f}s')
        
        if cycle_result.get("coordination_result"):
            coord_summary = cycle_result["coordination_result"].get("coordination_summary", {})
            print(f'   Coordination Success Rate: {coord_summary.get("success_rate", 0.0):.1%}')
        
    except Exception as e:
        print(f'[ERROR] Enhanced cycle failed: {e}')
    
    print(f'\n[OK] Multi-Agent Integration Test Complete!')
    return status

async def main():
    """Main test function"""
    
    print("[AGENT] ASIS Multi-Agent Coordination System Test")
    print("=" * 60)
    
    result = await test_multi_agent_integration()
    
    print('\n[DATA] Final Status Summary:')
    print('=' * 30)
    print(f'Quality Score: {result["quality_score"]:.1f}/100')
    print(f'Multi-Agent Available: {result.get("multi_agent_system", {}).get("multi_agent_available", False)}')
    print(f'Knowledge System: {result.get("knowledge_system", {}).get("active", False)}')
    print(f'System Version: {result["system_version"]}')
    
    # Display capabilities summary
    capabilities = result['capabilities']
    enabled_capabilities = [cap for cap, enabled in capabilities.items() if enabled]
    print(f'Enabled Capabilities: {len(enabled_capabilities)}/{len(capabilities)}')
    
    return result

if __name__ == "__main__":
    asyncio.run(main())