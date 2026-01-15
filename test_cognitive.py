#!/usr/bin/env python3
"""
Simple test script for cognitive architecture
"""

import asyncio
import json
from cognitive_architecture import CognitiveArchitecture

async def simple_test():
    """Simple test without memory network"""
    print("=== Simple Cognitive Architecture Test ===\n")
    
    # Create and initialize the architecture
    arch = CognitiveArchitecture()
    # Disable memory network for testing
    arch.memory_integration_enabled = False
    arch.memory_network = None
    
    await arch.initialize()
    
    # Simple test input
    test_input = {
        "content": "Learning about AI",
        "context": "education", 
        "topic": "artificial_intelligence",
        "priority": 0.8
    }
    
    print("Processing input...")
    result = await arch.process_input(test_input)
    
    print("Processing completed!")
    print(f"Cycle: {result.get('cycle')}")
    print(f"Processing time: {result.get('processing_time'):.3f}s")
    print(f"Current focus: {result.get('attention', {}).get('current_focus')}")
    print(f"Memory utilization: {result.get('memory', {}).get('utilization', 0):.2f}")
    
    return arch

if __name__ == "__main__":
    asyncio.run(simple_test())
