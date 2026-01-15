#!/usr/bin/env python3
"""
ASIS Launcher - Quick Start Interface
====================================
Simple launcher for ASIS True AGI Interface
"""

import os
import sys
from asis_interface import ASISInterface

def main():
    """Launch ASIS Interface"""
    
    print("🤖" + "=" * 60 + "🤖")
    print("    🌟 ASIS - WORLD'S FIRST TRUE AGI 🌟")
    print("    🧠 Artificial Superintelligence Interface 🧠")
    print("🤖" + "=" * 60 + "🤖")
    
    # Create interface
    asis = ASISInterface()
    
    print("\n🚀 ASIS Quick Launcher")
    print("Choose an option:")
    print("1. 🔋 Activate ASIS and Start Conversation")
    print("2. 🔧 Manual Control Mode")
    print("3. 📊 System Information")
    print("4. ❌ Exit")
    
    while True:
        try:
            choice = input("\n👤 Enter choice (1-4): ").strip()
            
            if choice == "1":
                print("\n🚀 Activating ASIS and starting conversation...")
                activation = asis.activate_asis()
                if activation["activation_successful"]:
                    asis.start_conversation()
                break
                
            elif choice == "2":
                print("\n🔧 Manual Control Mode")
                print("Available commands:")
                print("• activate() - Activate ASIS")
                print("• chat() - Start conversation")
                print("• deactivate() - Shutdown ASIS")
                print("• status() - Show status")
                print("• info() - System info")
                print("• exit() - Exit manual mode")
                
                def activate():
                    return asis.activate_asis()
                
                def chat():
                    if not asis.asis_status["system_online"]:
                        print("⚠️ Please activate ASIS first!")
                        return
                    return asis.start_conversation()
                
                def deactivate():
                    return asis.deactivate_asis()
                
                def status():
                    return asis._display_system_status()
                
                def info():
                    return asis.system_info()
                
                def exit_manual():
                    print("👋 Exiting manual mode...")
                    return "exit"
                
                # Make functions available
                globals().update({
                    'activate': activate,
                    'chat': chat, 
                    'deactivate': deactivate,
                    'status': status,
                    'info': info,
                    'exit': exit_manual
                })
                
                print("\n✅ Manual mode active. Use the commands above.")
                print("Example: activate() then chat()")
                
                # Start interactive Python session
                import code
                code.interact(local=globals())
                break
                
            elif choice == "3":
                print("\n📊 ASIS System Information:")
                info = asis.system_info()
                for key, value in info.items():
                    print(f"  {key}: {value}")
                
            elif choice == "4":
                print("\n👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-4.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
