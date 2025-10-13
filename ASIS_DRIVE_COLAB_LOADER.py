"""
🚀 ASIS NANO & MICRO - GOOGLE DRIVE COLAB LOADER
Upload ASIS files to Google Drive and load them in Colab
EASY ALTERNATIVE TO ZIP UPLOADS
"""

def setup_drive_asis():
    """Setup ASIS using Google Drive in Colab"""
    
    print("🚀 ASIS NANO & MICRO - GOOGLE DRIVE SETUP")
    print("=" * 50)
    
    # Mount Google Drive
    print("📂 Mounting Google Drive...")
    try:
        from google.colab import drive
        drive.mount('/content/drive')
        print("✅ Google Drive mounted!")
    except Exception as e:
        print(f"❌ Could not mount Drive: {e}")
        print("💡 Make sure you're running this in Google Colab")
        return None
    
    import os
    
    # Check for ASIS files in Drive
    drive_paths = [
        "/content/drive/MyDrive/ASIS/",
        "/content/drive/MyDrive/",
        "/content/drive/MyDrive/Colab Notebooks/"
    ]
    
    asis_files = {}
    
    print("\n🔍 Searching for ASIS files in Google Drive...")
    
    for drive_path in drive_paths:
        if os.path.exists(drive_path):
            print(f"📁 Checking: {drive_path}")
            
            # Look for ASIS files
            files_in_path = os.listdir(drive_path)
            
            for file in files_in_path:
                file_lower = file.lower()
                if 'asis' in file_lower and file.endswith('.py'):
                    full_path = os.path.join(drive_path, file)
                    asis_files[file] = full_path
                    print(f"   ✅ Found: {file}")
                elif file.endswith('.pt') and 'asis' in file_lower:
                    full_path = os.path.join(drive_path, file)
                    asis_files[file] = full_path
                    print(f"   ✅ Found model: {file}")
    
    if not asis_files:
        print("⚠️  No ASIS files found in Google Drive")
        print("\n📋 TO USE THIS METHOD:")
        print("1. Upload ASIS files to your Google Drive")
        print("2. Put them in 'My Drive' or 'My Drive/ASIS/' folder")
        print("3. Re-run this setup")
        print("\n💡 Alternatively, use the GitHub method or copy-paste method")
        return create_drive_fallback_asis()
    
    print(f"\n📦 Found {len(asis_files)} ASIS files!")
    
    # Copy files to Colab workspace
    print("📋 Copying files to Colab workspace...")
    
    copied_files = {}
    for filename, filepath in asis_files.items():
        try:
            # Copy to current directory
            import shutil
            local_path = f"./{filename}"
            shutil.copy2(filepath, local_path)
            copied_files[filename] = local_path
            print(f"   ✅ Copied: {filename}")
        except Exception as e:
            print(f"   ❌ Failed to copy {filename}: {e}")
    
    return copied_files

def start_drive_asis(copied_files):
    """Start ASIS from copied Drive files"""
    
    print("\n🚀 Starting ASIS from Drive files...")
    
    # Try to find and run ASIS files in order of preference
    import os
    
    # Look for emergency ASIS first (most reliable)
    emergency_files = [f for f in copied_files.keys() if 'emergency' in f.lower() and f.endswith('.py')]
    
    if emergency_files:
        emergency_file = emergency_files[0]
        print(f"🚨 Loading Emergency ASIS from: {emergency_file}")
        try:
            exec(open(emergency_file).read())
            asis, results = run_emergency_asis()
            print("✅ Emergency ASIS loaded successfully!")
            return asis, "emergency", emergency_file
        except Exception as e:
            print(f"❌ Emergency ASIS failed: {e}")
    
    # Look for micro ASIS
    micro_files = [f for f in copied_files.keys() if 'micro' in f.lower() and f.endswith('.py')]
    
    if micro_files:
        micro_file = micro_files[0]
        print(f"🧠 Loading Micro ASIS from: {micro_file}")
        try:
            exec(open(micro_file).read())
            asis, results = run_emergency_asis()
            print("✅ Micro ASIS loaded successfully!")
            return asis, "micro", micro_file
        except Exception as e:
            print(f"❌ Micro ASIS failed: {e}")
    
    # Look for native ASIS
    native_files = [f for f in copied_files.keys() if ('native' in f.lower() or 'true' in f.lower()) and f.endswith('.py')]
    
    if native_files:
        native_file = native_files[0]
        print(f"🏛️  Loading Native ASIS from: {native_file}")
        try:
            exec(open(native_file).read())
            asis = ASISNativeCoreSystem()
            asis.activate()
            print("✅ Native ASIS loaded successfully!")
            return asis, "native", native_file
        except Exception as e:
            print(f"❌ Native ASIS failed: {e}")
    
    # Try any other ASIS Python files
    other_asis_files = [f for f in copied_files.keys() if f.endswith('.py') and 'asis' in f.lower()]
    
    for asis_file in other_asis_files:
        print(f"🔧 Trying to load: {asis_file}")
        try:
            exec(open(asis_file).read())
            # Try common ASIS initialization patterns
            if 'run_emergency_asis' in globals():
                asis, results = run_emergency_asis()
                return asis, "loaded", asis_file
            elif 'ASISNativeCoreSystem' in globals():
                asis = ASISNativeCoreSystem()
                asis.activate()
                return asis, "loaded", asis_file
        except Exception as e:
            print(f"❌ Could not load {asis_file}: {e}")
            continue
    
    # Fallback
    print("🔧 Creating Drive fallback ASIS...")
    return create_drive_fallback_asis(), "fallback", "built-in"

def create_drive_fallback_asis():
    """Create a fallback ASIS for Drive method"""
    
    class DriveASIS:
        def __init__(self):
            self.name = "ASIS Drive Mode"
            self.principles = {
                "alignment": "Prioritize human wellbeing and safety",
                "transparency": "Make reasoning processes explicit", 
                "ethics": "Maintain awareness of ethical implications",
                "learning": "Continuously improve while preserving principles",
                "safety": "Implement graceful degradation under constraints"
            }
            print("🔧 ASIS Drive fallback mode initialized")
        
        def chat(self, message):
            message_lower = message.lower()
            
            if 'hello' in message_lower or 'hi' in message_lower:
                return "Hello! I'm ASIS running from Google Drive in Colab. How can I help you today?"
            
            elif 'drive' in message_lower:
                return "I'm running from your Google Drive files in Colab. This allows easy access to ASIS without zip uploads!"
            
            elif 'principles' in message_lower or 'values' in message_lower:
                principles_text = ", ".join(self.principles.keys())
                return f"My core principles are: {principles_text}. These guide all my interactions."
            
            elif 'safety' in message_lower:
                return "AI safety is fundamental to my design. I prioritize human wellbeing and maintain ethical guidelines in all responses."
            
            elif 'what are you' in message_lower or 'who are you' in message_lower:
                return "I'm ASIS (Artificial Safety Intelligence System) running from Google Drive in Colab. I'm designed to be helpful, harmless, and honest."
            
            elif 'help' in message_lower:
                return "I can help with questions, explanations, reasoning through problems, and providing information while maintaining ethical guidelines. What would you like to explore?"
            
            elif 'colab' in message_lower:
                return "I'm optimized for Google Colab and can run from Drive files, GitHub, or copy-paste methods. This makes deployment very flexible!"
            
            else:
                return f"I understand you're asking about '{message}'. I'm here to help while maintaining my commitment to safety and ethical AI principles."
        
        def get_status(self):
            return {
                "mode": "Drive fallback",
                "source": "Google Drive", 
                "status": "Active",
                "principles": list(self.principles.keys())
            }
    
    return DriveASIS()

def drive_colab_demo():
    """Complete Google Drive to Colab demo"""
    
    print("🎬 ASIS GOOGLE DRIVE TO COLAB DEMO")
    print("=" * 50)
    
    # Step 1: Setup Drive connection
    copied_files = setup_drive_asis()
    
    if not copied_files:
        print("⚠️  No files found, using fallback mode")
        asis = create_drive_fallback_asis()
        mode = "fallback"
        source_file = "built-in"
    else:
        # Step 2: Start ASIS from Drive files
        asis, mode, source_file = start_drive_asis(copied_files)
    
    # Step 3: Test ASIS
    print(f"\n🧪 Testing ASIS ({mode} mode from {source_file})...")
    
    test_prompts = [
        "Hello ASIS!",
        "What are your core principles?",
        "How does the Drive integration work?",
        "What are your capabilities in Colab?"
    ]
    
    for prompt in test_prompts:
        try:
            response = asis.chat(prompt)
            print(f"\n👤 {prompt}")
            print(f"🤖 {response}")
        except Exception as e:
            print(f"❌ Error with '{prompt}': {e}")
    
    # Step 4: Show status
    if hasattr(asis, 'get_status'):
        try:
            status = asis.get_status()
            print(f"\n📊 System Status:")
            for key, value in status.items():
                print(f"   {key}: {value}")
        except Exception as e:
            print(f"Status check failed: {e}")
    
    print(f"\n💬 ASIS ({mode}) is ready for interaction!")
    print("Commands:")
    print("   asis.chat('Your message')  # Chat with ASIS")
    print("   asis.get_status()          # System status")
    
    return asis, copied_files

def interactive_drive_chat(asis):
    """Interactive chat for Drive-loaded ASIS"""
    
    print("\n💬 INTERACTIVE ASIS DRIVE CHAT")
    print("=" * 40)
    print("Type your messages below. Type 'quit' to exit.")
    
    chat_count = 0
    
    while chat_count < 30:  # Reasonable limit for Colab
        try:
            message = input(f"\n[{chat_count + 1}] You: ").strip()
            
            if message.lower() in ['quit', 'exit', 'stop']:
                print("👋 Chat ended. Goodbye!")
                break
            
            if not message:
                continue
            
            response = asis.chat(message)
            print(f"🤖 ASIS: {response}")
            
            chat_count += 1
            
        except KeyboardInterrupt:
            print("\n👋 Chat interrupted!")
            break
        except Exception as e:
            print(f"❌ Chat error: {e}")
            continue

# ==================== DRIVE SETUP INSTRUCTIONS ====================
def print_drive_instructions():
    """Print Google Drive setup instructions"""
    
    instructions = """
🧠 ASIS GOOGLE DRIVE SETUP INSTRUCTIONS
=======================================

STEP 1: PREPARE YOUR DRIVE
--------------------------
1. Go to your Google Drive (drive.google.com)
2. Create a folder called "ASIS" (optional but recommended)
3. Upload your ASIS files to this folder:
   - asis_emergency_copy_paste.py
   - asis_micro_emergency.py  
   - asis_true_native_package.py
   - Any .pt model files

STEP 2: RUN IN COLAB
--------------------
# Quick setup (recommended):
asis, files = drive_colab_demo()

# Manual setup:
files = setup_drive_asis()        # Mount and find files
asis, mode, source = start_drive_asis(files)  # Start ASIS

# Interactive chat:
interactive_drive_chat(asis)

STEP 3: VERIFY SETUP
--------------------
# Test ASIS:
response = asis.chat("Hello!")
print(response)

# Check status:
status = asis.get_status()
print(status)

TROUBLESHOOTING
---------------
❌ "No ASIS files found":
   - Check file names contain "asis"
   - Check files are .py format
   - Try putting files in root Drive folder

❌ "Could not mount Drive":
   - Make sure you're in Google Colab
   - Allow Drive access when prompted
   - Try refreshing and running again

❌ "ASIS failed to start":
   - System will use fallback mode
   - Check if Python files have syntax errors
   - Try emergency ASIS files first

ADVANTAGES
----------
✅ Easy file management through Drive interface
✅ Persistent storage across Colab sessions
✅ No zip upload size limits
✅ Can organize ASIS files in folders
✅ Shareable with team members

FILE ORGANIZATION
-----------------
Recommended Drive structure:
My Drive/
  └── ASIS/
      ├── asis_emergency_copy_paste.py
      ├── asis_micro_emergency.py
      ├── asis_true_native_package.py
      ├── asis_nano_model.pt (if available)
      └── asis_micro_model.pt (if available)
"""
    
    print(instructions)

# ==================== AUTO EXECUTION ====================
print("🚀 ASIS GOOGLE DRIVE COLAB LOADER READY!")
print("=" * 45)
print()
print("📋 Quick Commands:")
print("   asis, files = drive_colab_demo()    # Complete setup")
print("   setup_drive_asis()                  # Just mount & find files")  
print("   print_drive_instructions()          # Show detailed help")
print()
print("✨ Load ASIS directly from your Google Drive!")
print("📂 No zip uploads needed - uses Drive integration")

# Show instructions by default
print_drive_instructions()

# If running directly, run demo
if __name__ == "__main__":
    asis, files = drive_colab_demo()