#!/usr/bin/env python3
"""
Agent Launcher for Multi-Agent System
====================================
Simple launcher for specialized agents
"""

import sys
import json
import asyncio
import argparse

def main():
    """Launch a specialized agent with configuration"""
    
    parser = argparse.ArgumentParser(description='Launch ASIS Specialized Agent')
    parser.add_argument('config_file', help='Path to agent configuration file')
    args = parser.parse_args()
    
    try:
        # Load configuration
        with open(args.config_file, 'r') as f:
            config = json.load(f)
        
        print(f"Starting agent {config['agent_id']} with specialization {config['specialization']}")
        
        # Import here to avoid issues
        from asis_specialized_agent import ASISSpecializedAgent
        
        # Create and run specialized agent
        async def run_agent():
            agent = ASISSpecializedAgent(config)
            await agent.start()
        
        # Run the agent
        asyncio.run(run_agent())
        
    except Exception as e:
        print(f"Agent startup error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()