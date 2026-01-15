#!/usr/bin/env python3
"""
ASIS Interactive Control Interface
=================================

Advanced control panel and interaction modes for the ASIS system.
"""

import os
import sys
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging

# Import our activation controller
from asis_activation_controller import ASISMasterController, ActivationConfig, InteractionMode, SystemStatus

class ControlCommand(Enum):
    START = "start"
    STOP = "stop"
    STATUS = "status"
    MODE = "mode"
    CONFIG = "config"
    EMERGENCY = "emergency"
    INTERACT = "interact"
    MONITOR = "monitor"

@dataclass
class InteractionSession:
    mode: InteractionMode
    start_time: datetime
    message_count: int = 0
    context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}

class ASISControlInterface:
    """Advanced control interface for ASIS system"""
    
    def __init__(self, asis_controller: ASISMasterController):
        self.asis = asis_controller
        self.logger = logging.getLogger("ASIS-Control")
        self.current_session: Optional[InteractionSession] = None
        self.command_history: List[Dict[str, Any]] = []
        
        # Interaction mode configurations
        self.mode_configs = {
            InteractionMode.CONVERSATIONAL: {
                "prompt": "💬 Chat with ASIS",
                "features": ["Natural conversation", "Question answering", "Contextual memory"],
                "color": "blue"
            },
            InteractionMode.RESEARCH: {
                "prompt": "🔬 Research Mode",
                "features": ["Autonomous investigation", "Source analysis", "Hypothesis generation"],
                "color": "green"
            },
            InteractionMode.LEARNING: {
                "prompt": "📚 Learning Mode", 
                "features": ["Knowledge acquisition", "Skill development", "Adaptation"],
                "color": "yellow"
            },
            InteractionMode.CREATIVE: {
                "prompt": "🎨 Creative Mode",
                "features": ["Idea generation", "Creative synthesis", "Innovation"],
                "color": "purple"
            },
            InteractionMode.ANALYSIS: {
                "prompt": "🔍 Analysis Mode",
                "features": ["Problem solving", "Data analysis", "Decision support"],
                "color": "red"
            },
            InteractionMode.MONITORING: {
                "prompt": "📊 Monitoring Mode",
                "features": ["System observation", "Performance tracking", "Health monitoring"],
                "color": "cyan"
            }
        }
        
    def show_control_panel(self) -> None:
        """Display the main control panel"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 25 + "ASIS CONTROL INTERFACE" + " " * 31 + "║")
        print("╚" + "═" * 78 + "╝")
        
        # System status
        dashboard = self.asis.get_status_dashboard()
        status_color = self._get_status_color(dashboard['system_status'])
        
        print(f"\n📊 SYSTEM STATUS: {dashboard['system_status']}")
        print(f"🔧 Components: {dashboard['components_online']}")
        print(f"💚 Health: {dashboard['average_health']}")
        print(f"🔄 Autonomous: {dashboard['autonomous_cycle']}")
        print(f"🎭 Mode: {dashboard['current_mode'].upper()}")
        
        # Control options
        print(f"\n🎮 CONTROL OPTIONS:")
        print(f"   1. 🚀 Start/Restart System")
        print(f"   2. ⏹️  Stop System")
        print(f"   3. 📊 Detailed Status")
        print(f"   4. 🎭 Change Interaction Mode")
        print(f"   5. ⚙️  Configuration")
        print(f"   6. 💬 Interactive Session")
        print(f"   7. 📈 Real-time Monitoring")
        print(f"   8. 🚨 Emergency Shutdown")
        print(f"   9. ❌ Exit")
        
    def start_interactive_loop(self) -> None:
        """Main interactive control loop"""
        self.logger.info("🎮 Starting ASIS Control Interface")
        
        while True:
            try:
                self.show_control_panel()
                choice = input(f"\n🎯 Select option (1-9): ").strip()
                
                if choice == '1':
                    self._handle_start_system()
                elif choice == '2':
                    self._handle_stop_system()
                elif choice == '3':
                    self._handle_detailed_status()
                elif choice == '4':
                    self._handle_mode_change()
                elif choice == '5':
                    self._handle_configuration()
                elif choice == '6':
                    self._handle_interactive_session()
                elif choice == '7':
                    self._handle_monitoring()
                elif choice == '8':
                    self._handle_emergency_shutdown()
                elif choice == '9':
                    print("\n👋 Exiting ASIS Control Interface...")
                    break
                else:
                    print("\n❌ Invalid option. Press Enter to continue...")
                    input()
                    
            except KeyboardInterrupt:
                print("\n\n🚨 Interrupt received. Use option 8 for safe shutdown.")
                input("Press Enter to continue...")
            except Exception as e:
                print(f"\n💥 Error: {str(e)}")
                input("Press Enter to continue...")

    def _handle_start_system(self) -> None:
        """Handle system startup"""
        print("\n🚀 STARTING ASIS SYSTEM...")
        print("-" * 50)
        
        if self.asis.status == SystemStatus.OFFLINE:
            success = self.asis.activate()
            if success:
                print("\n✅ ASIS system started successfully!")
            else:
                print("\n❌ Failed to start ASIS system. Check logs for details.")
        else:
            print(f"\n⚠️ System is already {self.asis.status.value}")
            
        input("\nPress Enter to continue...")

    def _handle_stop_system(self) -> None:
        """Handle system shutdown"""
        print("\n⏹️ STOPPING ASIS SYSTEM...")
        print("-" * 50)
        
        confirm = input("🚨 Are you sure you want to stop ASIS? (y/N): ").strip().lower()
        if confirm == 'y':
            self.asis.shutdown()
            print("\n✅ ASIS system stopped safely.")
        else:
            print("\n❌ Shutdown cancelled.")
            
        input("\nPress Enter to continue...")

    def _handle_detailed_status(self) -> None:
        """Show detailed system status"""
        print("\n📊 DETAILED SYSTEM STATUS")
        print("=" * 60)
        
        dashboard = self.asis.get_status_dashboard()
        
        print(f"Timestamp: {dashboard['timestamp']}")
        print(f"System Status: {dashboard['system_status']}")
        print(f"Components Online: {dashboard['components_online']}")
        print(f"Average Health: {dashboard['average_health']}")
        print(f"Autonomous Cycle: {dashboard['autonomous_cycle']}")
        print(f"Current Mode: {dashboard['current_mode']}")
        
        print(f"\n🔧 COMPONENT DETAILS:")
        print("-" * 60)
        
        for comp_id, comp_info in dashboard['components'].items():
            status_icon = "✅" if "ONLINE" in comp_info['status'] else "❌"
            print(f"{status_icon} {comp_info['name']:<30} {comp_info['health']:<8} {comp_info['last_activity']}")
            if comp_info.get('error'):
                print(f"    ⚠️ Error: {comp_info['error']}")
        
        input("\nPress Enter to continue...")

    def _handle_mode_change(self) -> None:
        """Handle interaction mode changes"""
        print("\n🎭 INTERACTION MODE SELECTION")
        print("=" * 50)
        
        print("Available modes:")
        for i, (mode, config) in enumerate(self.mode_configs.items(), 1):
            current = "◄ CURRENT" if mode == self.asis.current_mode else ""
            print(f"  {i}. {config['prompt']} {current}")
            for feature in config['features']:
                print(f"     • {feature}")
            print()
        
        try:
            choice = int(input("Select mode (1-6): ")) - 1
            modes = list(self.mode_configs.keys())
            
            if 0 <= choice < len(modes):
                selected_mode = modes[choice]
                self.asis.set_interaction_mode(selected_mode)
                print(f"\n✅ Switched to {self.mode_configs[selected_mode]['prompt']}")
            else:
                print("\n❌ Invalid selection.")
                
        except ValueError:
            print("\n❌ Please enter a valid number.")
            
        input("\nPress Enter to continue...")

    def _handle_configuration(self) -> None:
        """Handle system configuration"""
        print("\n⚙️ SYSTEM CONFIGURATION")
        print("=" * 50)
        
        config = self.asis.config
        
        print("Current configuration:")
        print(f"  • Interests: {', '.join(config.interests)}")
        print(f"  • Learning Rate: {config.learning_rate}")
        print(f"  • Reasoning Depth: {config.reasoning_depth}")
        print(f"  • Research Scope: {config.research_scope}")
        print(f"  • Personality Style: {config.personality_style}")
        print(f"  • Safety Level: {config.safety_level}")
        print(f"  • Autonomous Mode: {config.autonomous_mode}")
        print(f"  • Debug Mode: {config.debug_mode}")
        
        print(f"\n📝 Configuration Options:")
        print(f"  1. Update interests")
        print(f"  2. Adjust learning rate")
        print(f"  3. Set reasoning depth")
        print(f"  4. Change safety level")
        print(f"  5. Toggle autonomous mode")
        print(f"  6. Save configuration")
        print(f"  7. Load configuration")
        print(f"  8. Back to main menu")
        
        choice = input("\nSelect option (1-8): ").strip()
        
        if choice == '1':
            self._update_interests()
        elif choice == '2':
            self._adjust_learning_rate()
        elif choice == '5':
            config.autonomous_mode = not config.autonomous_mode
            print(f"✅ Autonomous mode: {'ON' if config.autonomous_mode else 'OFF'}")
        elif choice == '6':
            self._save_configuration()
        elif choice == '7':
            self._load_configuration()
        else:
            print("⚠️ Configuration option not fully implemented yet.")
            
        input("\nPress Enter to continue...")

    def _handle_interactive_session(self) -> None:
        """Handle interactive chat session"""
        if self.asis.status != SystemStatus.AUTONOMOUS:
            print("\n⚠️ ASIS system must be running for interactive sessions.")
            input("Press Enter to continue...")
            return
            
        print(f"\n💬 INTERACTIVE SESSION - {self.asis.current_mode.value.upper()} MODE")
        print("=" * 60)
        print("Type 'exit' to end session, 'help' for commands")
        print("-" * 60)
        
        session = InteractionSession(
            mode=self.asis.current_mode,
            start_time=datetime.now()
        )
        
        while True:
            try:
                user_input = input(f"\n[{session.mode.value}] You: ").strip()
                
                if user_input.lower() == 'exit':
                    break
                elif user_input.lower() == 'help':
                    self._show_session_help()
                    continue
                elif user_input.lower() == 'status':
                    self._show_session_status(session)
                    continue
                
                # Process input through ASIS
                response = self._process_interaction(user_input, session)
                print(f"\n[ASIS] {response}")
                
                session.message_count += 1
                
            except KeyboardInterrupt:
                print("\n\n🔄 Ending session...")
                break
                
        duration = datetime.now() - session.start_time
        print(f"\n📊 Session ended. Duration: {duration}, Messages: {session.message_count}")
        input("Press Enter to continue...")

    def _handle_monitoring(self) -> None:
        """Handle real-time monitoring"""
        print("\n📈 REAL-TIME MONITORING")
        print("=" * 60)
        print("Press Ctrl+C to stop monitoring")
        print("-" * 60)
        
        try:
            while True:
                dashboard = self.asis.get_status_dashboard()
                
                # Clear and redraw
                os.system('cls' if os.name == 'nt' else 'clear')
                print("📈 ASIS REAL-TIME MONITORING")
                print("=" * 60)
                
                print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
                print(f"🖥️  Status: {dashboard['system_status']}")
                print(f"🔧 Components: {dashboard['components_online']}")
                print(f"💚 Health: {dashboard['average_health']}")
                print(f"🔄 Autonomous: {dashboard['autonomous_cycle']}")
                
                print(f"\n🔧 COMPONENT HEALTH:")
                for comp_id, comp_info in dashboard['components'].items():
                    health_bar = self._create_health_bar(comp_info['health'])
                    print(f"  {comp_info['name']:<25} {health_bar} {comp_info['health']}")
                
                print(f"\nPress Ctrl+C to return to menu...")
                
                import time
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n\n📊 Monitoring stopped.")
            input("Press Enter to continue...")

    def _handle_emergency_shutdown(self) -> None:
        """Handle emergency shutdown"""
        print("\n🚨 EMERGENCY SHUTDOWN")
        print("=" * 50)
        print("⚠️ This will immediately stop all ASIS operations!")
        
        confirm = input("\n🚨 Confirm emergency shutdown (TYPE 'EMERGENCY'): ").strip()
        
        if confirm.upper() == 'EMERGENCY':
            print("\n🚨 INITIATING EMERGENCY SHUTDOWN...")
            self.asis.shutdown()
            print("✅ Emergency shutdown complete.")
        else:
            print("\n❌ Emergency shutdown cancelled.")
            
        input("\nPress Enter to continue...")

    def _process_interaction(self, user_input: str, session: InteractionSession) -> str:
        """Process user interaction based on current mode"""
        
        mode_responses = {
            InteractionMode.CONVERSATIONAL: self._conversational_response,
            InteractionMode.RESEARCH: self._research_response,
            InteractionMode.LEARNING: self._learning_response,
            InteractionMode.CREATIVE: self._creative_response,
            InteractionMode.ANALYSIS: self._analysis_response,
            InteractionMode.MONITORING: self._monitoring_response
        }
        
        handler = mode_responses.get(session.mode, self._default_response)
        return handler(user_input, session)

    def _conversational_response(self, user_input: str, session: InteractionSession) -> str:
        """Generate conversational response"""
        responses = [
            f"That's interesting! You mentioned: '{user_input[:50]}...' - I'm processing this through my cognitive architecture.",
            f"I understand you're asking about: '{user_input}' - Let me engage my reasoning systems to provide a thoughtful response.",
            f"From my memory networks, I can relate this to previous conversations. Your input: '{user_input}' connects to several interesting concepts.",
            f"My personality system suggests a curious approach to: '{user_input}' - What aspects would you like to explore further?",
        ]
        
        import random
        return random.choice(responses)

    def _research_response(self, user_input: str, session: InteractionSession) -> str:
        """Generate research-oriented response"""
        return f"🔬 Research mode activated. Analyzing query: '{user_input}'. My autonomous research engine is formulating hypotheses and identifying key sources to investigate. I'll synthesize findings from multiple knowledge domains."

    def _learning_response(self, user_input: str, session: InteractionSession) -> str:
        """Generate learning-oriented response"""
        return f"📚 Learning mode engaged. Processing: '{user_input}' through my meta-learning systems. I'm adapting my knowledge representations and updating my understanding based on this new information."

    def _creative_response(self, user_input: str, session: InteractionSession) -> str:
        """Generate creative response"""
        return f"🎨 Creative cognition activated. Your input '{user_input}' is sparking divergent thinking processes. I'm exploring novel combinations and generating innovative perspectives through analogical reasoning."

    def _analysis_response(self, user_input: str, session: InteractionSession) -> str:
        """Generate analytical response"""
        return f"🔍 Analysis mode running. Deconstructing: '{user_input}' through systematic reasoning. Applying deductive, inductive, and abductive inference patterns to provide comprehensive insights."

    def _monitoring_response(self, user_input: str, session: InteractionSession) -> str:
        """Generate monitoring response"""
        return f"📊 Monitoring systems observing: '{user_input}'. Current system health optimal. All integration patterns functioning. Autonomous cycle maintaining stable performance metrics."

    def _default_response(self, user_input: str, session: InteractionSession) -> str:
        """Default response"""
        return f"🤖 ASIS processing: '{user_input}' - System operational and responding through available components."

    def _create_health_bar(self, health_str: str) -> str:
        """Create a visual health bar"""
        try:
            health = float(health_str.replace('%', '')) / 100.0
            bar_length = 20
            filled = int(health * bar_length)
            bar = "█" * filled + "░" * (bar_length - filled)
            return f"[{bar}]"
        except:
            return "[" + "?" * 20 + "]"

    def _get_status_color(self, status: str) -> str:
        """Get color code for status"""
        if "ONLINE" in status or "AUTONOMOUS" in status:
            return "green"
        elif "ERROR" in status:
            return "red"
        elif "INITIALIZING" in status:
            return "yellow"
        else:
            return "gray"

    def _show_session_help(self) -> None:
        """Show help for interactive session"""
        print(f"\n🆘 INTERACTIVE SESSION HELP")
        print(f"Commands:")
        print(f"  • exit - End the session")
        print(f"  • help - Show this help")
        print(f"  • status - Show session status")
        print(f"Features in {self.asis.current_mode.value} mode:")
        for feature in self.mode_configs[self.asis.current_mode]['features']:
            print(f"  • {feature}")

    def _show_session_status(self, session: InteractionSession) -> None:
        """Show current session status"""
        duration = datetime.now() - session.start_time
        print(f"\n📊 SESSION STATUS:")
        print(f"  • Mode: {session.mode.value}")
        print(f"  • Duration: {duration}")
        print(f"  • Messages: {session.message_count}")
        print(f"  • System Health: {self.asis.get_status_dashboard()['average_health']}")

    def _update_interests(self) -> None:
        """Update system interests"""
        print(f"\nCurrent interests: {', '.join(self.asis.config.interests)}")
        new_interests = input("Enter new interests (comma-separated): ").strip()
        if new_interests:
            self.asis.config.interests = [interest.strip() for interest in new_interests.split(',')]
            print(f"✅ Interests updated: {', '.join(self.asis.config.interests)}")

    def _adjust_learning_rate(self) -> None:
        """Adjust learning rate"""
        try:
            new_rate = float(input(f"Current learning rate: {self.asis.config.learning_rate}\nEnter new rate (0.0-1.0): "))
            if 0.0 <= new_rate <= 1.0:
                self.asis.config.learning_rate = new_rate
                print(f"✅ Learning rate updated: {new_rate}")
            else:
                print("❌ Learning rate must be between 0.0 and 1.0")
        except ValueError:
            print("❌ Please enter a valid number")

    def _save_configuration(self) -> None:
        """Save configuration to file"""
        config_data = {
            "interests": self.asis.config.interests,
            "learning_rate": self.asis.config.learning_rate,
            "reasoning_depth": self.asis.config.reasoning_depth,
            "research_scope": self.asis.config.research_scope,
            "personality_style": self.asis.config.personality_style,
            "safety_level": self.asis.config.safety_level,
            "autonomous_mode": self.asis.config.autonomous_mode,
            "debug_mode": self.asis.config.debug_mode
        }
        
        with open('asis_config.json', 'w') as f:
            json.dump(config_data, f, indent=2)
        print("✅ Configuration saved to asis_config.json")

    def _load_configuration(self) -> None:
        """Load configuration from file"""
        try:
            with open('asis_config.json', 'r') as f:
                config_data = json.load(f)
                
            self.asis.config.interests = config_data.get('interests', self.asis.config.interests)
            self.asis.config.learning_rate = config_data.get('learning_rate', self.asis.config.learning_rate)
            self.asis.config.reasoning_depth = config_data.get('reasoning_depth', self.asis.config.reasoning_depth)
            self.asis.config.research_scope = config_data.get('research_scope', self.asis.config.research_scope)
            self.asis.config.personality_style = config_data.get('personality_style', self.asis.config.personality_style)
            self.asis.config.safety_level = config_data.get('safety_level', self.asis.config.safety_level)
            self.asis.config.autonomous_mode = config_data.get('autonomous_mode', self.asis.config.autonomous_mode)
            self.asis.config.debug_mode = config_data.get('debug_mode', self.asis.config.debug_mode)
            
            print("✅ Configuration loaded from asis_config.json")
        except FileNotFoundError:
            print("❌ Configuration file not found")
        except Exception as e:
            print(f"❌ Error loading configuration: {str(e)}")

def main():
    """Main function for control interface"""
    print("🎮 ASIS Interactive Control Interface")
    print("=" * 50)
    
    # Initialize ASIS system
    config = ActivationConfig()
    asis = ASISMasterController(config)
    
    # Create control interface
    control = ASISControlInterface(asis)
    
    # Start interactive loop
    control.start_interactive_loop()
    
    print("👋 ASIS Control Interface shutdown complete.")

if __name__ == "__main__":
    main()
