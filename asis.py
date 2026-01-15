#!/usr/bin/env python3
"""
ASIS Simple Activation
=====================

Simple command to start ASIS with asis.activate()
"""

import sys
import os

# Add current directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from asis_activation_controller import ASISMasterController, ActivationConfig
from asis_control_interface import ASISControlInterface

class ASIS:
    """Simple ASIS interface for easy activation"""
    
    def __init__(self):
        self.controller = None
        self.control_interface = None
        self._activated = False
        
    def activate(self, config=None, interactive=False):
        """Simple activation command"""
        print("🚀 ASIS Activation Starting...")
        
        # Create config if not provided
        if config is None:
            config = ActivationConfig(
                interests=["Artificial Intelligence", "Learning", "Research"],
                learning_rate=0.1,
                reasoning_depth=5,
                autonomous_mode=True,
                debug_mode=False
            )
        
        # Initialize controller
        self.controller = ASISMasterController(config)
        
        # Activate system
        success = self.controller.activate()
        
        if success:
            self._activated = True
            print("\n✅ ASIS ACTIVATED SUCCESSFULLY!")
            
            if interactive:
                # Start interactive interface
                self.control_interface = ASISControlInterface(self.controller)
                print("\n🎮 Starting Interactive Control Interface...")
                self.control_interface.start_interactive_loop()
            else:
                print("\n🎯 ASIS is now running autonomously!")
                self.status()
                
            return True
        else:
            print("\n❌ ASIS ACTIVATION FAILED")
            return False
    
    def status(self):
        """Show current status"""
        if not self._activated or not self.controller:
            print("❌ ASIS is not activated. Use asis.activate() first.")
            return
            
        dashboard = self.controller.get_status_dashboard()
        print(f"\n📊 ASIS STATUS:")
        print(f"   System: {dashboard['system_status']}")
        print(f"   Components: {dashboard['components_online']}")
        print(f"   Health: {dashboard['average_health']}")
        print(f"   Autonomous: {dashboard['autonomous_cycle']}")
        print(f"   Mode: {dashboard['current_mode']}")
    
    def shutdown(self):
        """Shutdown ASIS system"""
        if self.controller:
            self.controller.shutdown()
            self._activated = False
            print("✅ ASIS shutdown complete")
        else:
            print("❌ ASIS is not running")
    
    def interact(self):
        """Start interactive session"""
        if not self._activated:
            print("❌ ASIS is not activated. Use asis.activate() first.")
            return
            
        if not self.control_interface:
            self.control_interface = ASISControlInterface(self.controller)
            
        self.control_interface.start_interactive_loop()

# Create global ASIS instance for easy use
asis = ASIS()

def quick_demo():
    """Run a quick demo of ASIS capabilities"""
    print("🎯 ASIS Quick Demo")
    print("=" * 50)
    
    # Activate ASIS
    success = asis.activate()
    
    if success:
        print("\n🎉 ASIS is now operational!")
        
        # Show status
        asis.status()
        
        # Demonstrate different modes
        modes = ["conversational", "research", "learning", "creative"]
        
        print(f"\n🎭 Demonstrating interaction modes:")
        for mode in modes:
            print(f"   • {mode.title()} mode: Ready")
            
        print(f"\n💡 Quick usage examples:")
        print(f"   • asis.activate() - Start the system")
        print(f"   • asis.status() - Check system status") 
        print(f"   • asis.interact() - Start interactive session")
        print(f"   • asis.shutdown() - Stop the system")
        
        print(f"\n📚 For full interactive control, run:")
        print(f"   python asis_control_interface.py")
        
        return True
    else:
        print("\n❌ Demo failed - ASIS could not be activated")
        return False

if __name__ == "__main__":
    # If run directly, show demo
    quick_demo()
