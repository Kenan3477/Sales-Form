"""
🚀 ASIS NANO & MICRO - GITHUB COLAB LOADER
Download ASIS directly from GitHub into Google Colab
NO ZIP UPLOADS NEEDED - PULLS FROM YOUR GITHUB REPO
"""

# ==================== GITHUB COLAB LOADER ====================
# Copy this into Google Colab and run!

def load_asis_from_github():
    """Load ASIS Nano & Micro directly from GitHub into Colab"""
    
    print("🚀 ASIS NANO & MICRO - GITHUB LOADER")
    print("=" * 50)
    
    # Install required packages
    print("📦 Installing requirements...")
    import subprocess
    import sys
    
    packages = ['torch', 'transformers', 'numpy', 'matplotlib']
    for package in packages:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    
    # Import after installation
    import torch
    import requests
    import os
    
    print("✅ Packages installed!")
    
    # GitHub repository info
    repo_owner = "Kenan3477"
    repo_name = "ASIS"
    branch = "main"
    
    # Files to download from your repo
    files_to_download = {
        "asis_emergency.py": f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/asis_emergency_copy_paste.py",
        "asis_micro.py": f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/asis_micro_emergency.py", 
        "asis_native.py": f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/asis_true_native_package.py",
        "asis_core.py": f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/asis_native_agi_llm.py"
    }
    
    print("🔗 Downloading ASIS files from GitHub...")
    
    # Download files
    downloaded_files = {}
    for filename, url in files_to_download.items():
        try:
            print(f"📥 Downloading {filename}...")
            response = requests.get(url)
            if response.status_code == 200:
                with open(filename, 'w') as f:
                    f.write(response.text)
                downloaded_files[filename] = True
                print(f"✅ {filename} downloaded successfully")
            else:
                print(f"⚠️  {filename} not found (status {response.status_code})")
                downloaded_files[filename] = False
        except Exception as e:
            print(f"❌ Error downloading {filename}: {e}")
            downloaded_files[filename] = False
    
    # Try to download model files if they exist
    model_files = {
        "asis_nano_model.pt": f"https://github.com/{repo_owner}/{repo_name}/raw/{branch}/asis_nano_model.pt",
        "asis_micro_model.pt": f"https://github.com/{repo_owner}/{repo_name}/raw/{branch}/asis_micro_model.pt"
    }
    
    print("\n🧠 Attempting to download model files...")
    for model_name, model_url in model_files.items():
        try:
            print(f"📥 Downloading {model_name}...")
            response = requests.get(model_url)
            if response.status_code == 200:
                with open(model_name, 'wb') as f:
                    f.write(response.content)
                print(f"✅ {model_name} downloaded ({len(response.content)} bytes)")
                downloaded_files[model_name] = True
            else:
                print(f"⚠️  {model_name} not available")
                downloaded_files[model_name] = False
        except Exception as e:
            print(f"❌ Could not download {model_name}: {e}")
            downloaded_files[model_name] = False
    
    # Check what we have
    available_files = [k for k, v in downloaded_files.items() if v]
    print(f"\n📁 Available files: {len(available_files)}")
    for file in available_files:
        print(f"   ✅ {file}")
    
    return downloaded_files

def start_github_asis():
    """Start ASIS from downloaded GitHub files"""
    
    print("\n🚀 Starting ASIS from GitHub files...")
    
    # Try different ASIS versions in order of preference
    import os
    
    # Option 1: Try emergency ASIS (most reliable)
    if os.path.exists('asis_emergency.py'):
        print("🚨 Loading Emergency ASIS...")
        try:
            exec(open('asis_emergency.py').read())
            asis, results = run_emergency_asis()
            print("✅ Emergency ASIS loaded successfully!")
            return asis, "emergency"
        except Exception as e:
            print(f"❌ Emergency ASIS failed: {e}")
    
    # Option 2: Try micro ASIS
    if os.path.exists('asis_micro.py'):
        print("🧠 Loading Micro ASIS...")
        try:
            exec(open('asis_micro.py').read())
            asis, results = run_emergency_asis()
            print("✅ Micro ASIS loaded successfully!")
            return asis, "micro"
        except Exception as e:
            print(f"❌ Micro ASIS failed: {e}")
    
    # Option 3: Try native ASIS
    if os.path.exists('asis_native.py'):
        print("🏛️  Loading Native ASIS...")
        try:
            exec(open('asis_native.py').read())
            asis = ASISNativeCoreSystem()
            asis.activate()
            print("✅ Native ASIS loaded successfully!")
            return asis, "native"
        except Exception as e:
            print(f"❌ Native ASIS failed: {e}")
    
    # Fallback: Create minimal ASIS
    print("🔧 Creating minimal fallback ASIS...")
    
    class MinimalGitHubASIS:
        def __init__(self):
            self.name = "ASIS Minimal"
            self.principles = ["safety", "alignment", "transparency", "ethics"]
        
        def chat(self, message):
            message_lower = message.lower()
            
            if 'hello' in message_lower or 'hi' in message_lower:
                return "Hello! I'm ASIS running in minimal mode from GitHub. How can I help you?"
            elif 'principles' in message_lower:
                return f"My core principles are: {', '.join(self.principles)}"
            elif 'safety' in message_lower:
                return "AI safety is my top priority. I'm designed to be helpful, harmless, and honest."
            elif 'what are you' in message_lower:
                return "I'm ASIS (Artificial Safety Intelligence System) running from GitHub in Google Colab."
            else:
                return f"I understand you're asking about '{message}'. I'm operating in minimal mode but committed to being helpful and safe."
        
        def get_status(self):
            return {"mode": "minimal", "source": "github", "status": "active"}
    
    asis = MinimalGitHubASIS()
    print("✅ Minimal ASIS created as fallback!")
    return asis, "minimal"

def github_colab_demo():
    """Complete GitHub to Colab demo"""
    
    print("🎬 ASIS GITHUB TO COLAB DEMO")
    print("=" * 50)
    
    # Step 1: Download from GitHub
    downloaded = load_asis_from_github()
    
    # Step 2: Start ASIS
    asis, mode = start_github_asis()
    
    # Step 3: Test ASIS
    print(f"\n🧪 Testing ASIS ({mode} mode)...")
    
    test_prompts = [
        "Hello ASIS!",
        "What are your core principles?",
        "How do you ensure safety?",
        "What can you do in Colab?"
    ]
    
    for prompt in test_prompts:
        try:
            response = asis.chat(prompt)
            print(f"\n👤 {prompt}")
            print(f"🤖 {response}")
        except Exception as e:
            print(f"❌ Error with '{prompt}': {e}")
    
    # Step 4: Interactive mode
    print(f"\n💬 ASIS ({mode}) is ready for interaction!")
    print("Available commands:")
    print("   asis.chat('Your message here')  # Chat with ASIS")
    if hasattr(asis, 'get_status'):
        print("   asis.get_status()               # Get system status")
    
    return asis, downloaded

# ==================== QUICK GITHUB SETUP ====================
def quick_github_setup():
    """One-command GitHub setup for Colab"""
    
    print("⚡ ASIS QUICK GITHUB SETUP")
    print("=" * 30)
    
    try:
        # Download and start in one go
        load_asis_from_github()
        asis, mode = start_github_asis()
        
        print(f"\n🎉 SUCCESS! ASIS ({mode}) ready!")
        print("\nQuick test:")
        
        response = asis.chat("Hello! Are you working?")
        print(f"🤖 ASIS: {response}")
        
        return asis
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        print("🔧 Try the manual method or copy-paste option")
        return None

# ==================== COLAB INSTRUCTIONS ====================
def print_colab_instructions():
    """Print instructions for Colab users"""
    
    instructions = """
🧠 ASIS NANO & MICRO - COLAB INSTRUCTIONS
==========================================

OPTION 1: QUICK SETUP (Recommended)
------------------------------------
asis = quick_github_setup()

OPTION 2: FULL DEMO
-------------------
asis, files = github_colab_demo()

OPTION 3: MANUAL CONTROL  
------------------------
# Download files
files = load_asis_from_github()

# Start ASIS
asis, mode = start_github_asis()

# Chat with ASIS
response = asis.chat("Hello ASIS!")
print(response)

OPTION 4: INTERACTIVE CHAT
--------------------------
# After setup, run:
while True:
    msg = input("You: ")
    if msg.lower() == 'quit': break
    print("ASIS:", asis.chat(msg))

TROUBLESHOOTING
---------------
If GitHub download fails:
1. Check internet connection
2. Try the copy-paste method instead
3. Use: load_asis_from_github() to retry

If ASIS fails to start:
- The system will fallback to minimal mode
- All modes support basic chat functionality
- Emergency ASIS is most reliable

FEATURES AVAILABLE
------------------
✅ Core ASIS principles and safety
✅ Conversational interface
✅ Ethical reasoning
✅ Colab-optimized performance
✅ Multiple fallback modes
✅ No file uploads required
"""
    
    print(instructions)

# ==================== AUTO EXECUTION ====================
print("🚀 ASIS GITHUB COLAB LOADER READY!")
print("=" * 40)
print()
print("📋 Quick Commands:")
print("   asis = quick_github_setup()      # One-click setup")
print("   github_colab_demo()              # Full demo")
print("   print_colab_instructions()       # Show help")
print()
print("✨ Downloads directly from your GitHub repository!")
print("🔗 Repository: https://github.com/Kenan3477/ASIS")

# Show instructions by default
print_colab_instructions()

# If running directly, do quick setup
if __name__ == "__main__":
    asis = quick_github_setup()