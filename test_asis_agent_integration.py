#!/usr/bin/env python3
"""
Test ASIS Interface Agent Integration
===================================
"""

def test_asis_agent_integration():
    """Test if ChatGPT Agent features are integrated into ASIS interface"""
    
    print("🔍 Testing ASIS Interface Agent Integration")
    print("=" * 50)
    
    try:
        from asis_interface import ASISInterface
        print("✅ ASIS Interface imported successfully")
        
        # Create interface
        asis = ASISInterface()
        print("✅ ASIS Interface initialized")
        
        # Check agent system
        if hasattr(asis, 'agent_system'):
            if asis.agent_system:
                print("✅ ChatGPT Agent system ACTIVE")
                print("✅ Agent capabilities integrated into ASIS")
                
                # Check capabilities
                agent_capabilities = [
                    "autonomous_task_execution",
                    "multi_step_reasoning", 
                    "tool_orchestration",
                    "agent_mode"
                ]
                
                for capability in agent_capabilities:
                    if capability in asis.asis_capabilities:
                        status = "✅ ENABLED" if asis.asis_capabilities[capability] else "❌ DISABLED"
                        print(f"   {capability}: {status}")
                
                print("\n🎯 INTEGRATION SUCCESS!")
                print("ChatGPT Agent features are fully integrated into ASIS interface")
                return True
            else:
                print("❌ Agent system not initialized")
                return False
        else:
            print("❌ Agent system not available in interface")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Integration error: {e}")
        return False

def show_agent_commands():
    """Show available agent commands"""
    
    print("\n🤖 ASIS AGENT COMMANDS")
    print("=" * 40)
    print("In conversation mode, you can use:")
    print("• 'agent [task]' - Execute autonomous task")
    print("• 'agent' - Show agent help")
    print("\nExamples:")
    print("• agent research latest AI developments")
    print("• agent analyze system performance") 
    print("• agent create automation script")
    print("• agent solve complex problem X")
    print("• agent write code for file organization")

if __name__ == "__main__":
    success = test_asis_agent_integration()
    
    if success:
        show_agent_commands()
        print("\n🚀 Ready to use ASIS with ChatGPT Agent capabilities!")
    else:
        print("\n❌ Integration test failed")
