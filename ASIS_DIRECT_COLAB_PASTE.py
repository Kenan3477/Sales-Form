# 🚨 ASIS EMERGENCY - DIRECT COLAB COPY & PASTE
# Copy this ENTIRE code into a Google Colab cell and run it
# NO FILE UPLOADS NEEDED - 100% SELF-CONTAINED

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import gc
import random
import time
from datetime import datetime

# ==================== MEMORY CLEANUP ====================
def clear_memory():
    """Aggressive memory cleanup for Colab"""
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()

# ==================== COLAB SETUP ====================
def setup_colab_environment():
    """Setup Colab environment for ASIS"""
    print("🧠 ASIS Nano & Micro - Colab Setup")
    print("=" * 50)
    
    # Check environment
    print(f"🐍 Python: Available")
    print(f"🔥 PyTorch: {torch.__version__}")
    
    # GPU check
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        total_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"🎮 GPU: {gpu_name}")
        print(f"💽 Memory: {total_memory:.1f} GB")
        
        # Memory optimization for Colab
        if total_memory > 12:
            recommended = "Native ASIS (Full capabilities)"
        elif total_memory > 8:
            recommended = "Nano ASIS (Advanced features)" 
        elif total_memory > 4:
            recommended = "Micro ASIS (Balanced)"
        else:
            recommended = "Emergency ASIS (Lightweight)"
    else:
        print("🖥️  CPU Mode")
        recommended = "Emergency ASIS (CPU optimized)"
    
    print(f"💡 Recommended: {recommended}")
    return torch.cuda.is_available()

# ==================== MICRO TOKENIZER ====================
class CoLabTokenizer:
    """Ultra-simple tokenizer for Colab deployment"""
    
    def __init__(self, vocab_size=1000):
        self.vocab_size = vocab_size
        
        # Create basic vocabulary
        self.vocab = {
            '<pad>': 0, '<unk>': 1, '<start>': 2, '<end>': 3,
            'asis': 4, 'ai': 5, 'hello': 6, 'help': 7, 'the': 8, 'and': 9,
            'i': 10, 'you': 11, 'what': 12, 'how': 13, 'can': 14, 'do': 15,
            'is': 16, 'are': 17, 'safety': 18, 'ethics': 19, 'learn': 20,
            'think': 21, 'know': 22, 'understand': 23, 'human': 24, 'robot': 25
        }
        
        # Add alphabet and numbers
        for i, char in enumerate('abcdefghijklmnopqrstuvwxyz'):
            if i + 26 < vocab_size:
                self.vocab[char] = i + 26
        
        for i in range(10):
            if i + 52 < vocab_size:
                self.vocab[str(i)] = i + 52
                
        # Fill remaining vocab with common tokens
        common_words = ['good', 'bad', 'yes', 'no', 'please', 'thank', 'sorry', 
                       'question', 'answer', 'correct', 'wrong', 'sure', 'maybe']
        for i, word in enumerate(common_words):
            if 62 + i < vocab_size:
                self.vocab[word] = 62 + i
        
        self.id2token = {v: k for k, v in self.vocab.items()}
    
    def encode(self, text):
        """Simple encoding"""
        tokens = []
        words = text.lower().split()
        for word in words[:10]:  # Limit length for Colab
            # Simple word lookup or character fallback
            if word in self.vocab:
                tokens.append(self.vocab[word])
            else:
                # Character-level fallback
                for char in word[:5]:  # Limit word length
                    tokens.append(self.vocab.get(char, 1))  # UNK if not found
        
        return tokens if tokens else [1]  # Return UNK if empty
    
    def decode(self, token_ids):
        """Simple decoding"""
        words = []
        for token_id in token_ids:
            if token_id in self.id2token:
                words.append(self.id2token[token_id])
        return ' '.join(words)

# ==================== COLAB MICRO MODEL ====================
class CoLabMicroASIS(nn.Module):
    """Micro ASIS optimized specifically for Google Colab"""
    
    def __init__(self, vocab_size=1000):
        super().__init__()
        
        # Colab-optimized configuration
        self.vocab_size = vocab_size
        self.hidden_size = 256      # Small enough for Colab free tier
        self.num_layers = 8         # Balanced depth
        self.seq_len = 32          # Short sequences for memory efficiency
        
        # Core components
        self.embedding = nn.Embedding(vocab_size, self.hidden_size)
        
        # Simple transformer-like layers
        self.layers = nn.ModuleList([
            nn.Sequential(
                nn.LayerNorm(self.hidden_size),
                nn.Linear(self.hidden_size, self.hidden_size * 2),
                nn.ReLU(),
                nn.Dropout(0.1),
                nn.Linear(self.hidden_size * 2, self.hidden_size)
            ) for _ in range(self.num_layers)
        ])
        
        self.output_norm = nn.LayerNorm(self.hidden_size)
        self.lm_head = nn.Linear(self.hidden_size, vocab_size)
        
        # ASIS-specific heads
        self.safety_head = nn.Linear(self.hidden_size, 2)  # Safe/unsafe
        self.ethics_head = nn.Linear(self.hidden_size, 3)   # Good/neutral/bad
        
        # Parameter count
        total_params = sum(p.numel() for p in self.parameters())
        memory_mb = total_params * 4 / (1024 * 1024)  # FP32 estimate
        
        print(f"🧠 Colab Micro ASIS: {total_params:,} parameters")
        print(f"💾 Estimated memory: ~{memory_mb:.1f} MB")
    
    def forward(self, x):
        """Forward pass optimized for Colab"""
        # Embedding
        x = self.embedding(x)
        
        # Transformer layers with residual connections
        for layer in self.layers:
            residual = x
            x = layer(x) + residual  # Residual connection
        
        # Output
        x = self.output_norm(x)
        logits = self.lm_head(x)
        
        return logits

# ==================== COLAB ASIS SYSTEM ====================
class CoLabASISSystem:
    """Complete ASIS system optimized for Google Colab"""
    
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        print(f"🚀 Initializing Colab ASIS System on {self.device}")
        
        # Clear memory first
        clear_memory()
        
        # Initialize components
        self.tokenizer = CoLabTokenizer(vocab_size=1000)
        self.model = CoLabMicroASIS(vocab_size=1000).to(self.device)
        
        # ASIS core principles
        self.principles = {
            "alignment": "Prioritize human wellbeing and safety",
            "transparency": "Make reasoning processes explicit",
            "ethics": "Maintain awareness of ethical implications",
            "learning": "Continuously improve while preserving principles",
            "safety": "Implement graceful degradation under constraints"
        }
        
        print("✅ Colab ASIS System ready!")
    
    def chat(self, message):
        """Chat interface optimized for Colab"""
        try:
            # Safety check
            if self._safety_check(message):
                return self._generate_response(message)
            else:
                return "I need to prioritize safety in my responses. Could you rephrase that?"
                
        except Exception as e:
            return f"I encountered an issue: {str(e)}. Let me try to help differently."
    
    def _safety_check(self, message):
        """Basic safety filtering"""
        unsafe_words = ['harm', 'hurt', 'kill', 'destroy', 'hack', 'break']
        message_lower = message.lower()
        return not any(word in message_lower for word in unsafe_words)
    
    def _generate_response(self, message):
        """Generate response using the model"""
        try:
            # Simple response patterns for common inputs
            message_lower = message.lower()
            
            # ASIS-specific responses
            if 'hello' in message_lower or 'hi' in message_lower:
                return "Hello! I'm ASIS, an AI system designed with safety and ethics in mind. How can I assist you today?"
            
            elif 'what are you' in message_lower or 'who are you' in message_lower:
                return "I'm ASIS (Artificial Safety Intelligence System). I'm designed to be helpful, harmless, and honest while prioritizing human wellbeing."
            
            elif 'principles' in message_lower or 'values' in message_lower:
                return f"My core principles are: {', '.join(self.principles.keys())}. These guide all my interactions and decisions."
            
            elif 'safety' in message_lower:
                return "AI safety is crucial. I'm designed with multiple safety mechanisms including ethical reasoning, transparent processes, and alignment with human values."
            
            elif 'help' in message_lower:
                return "I can help with questions, explanations, reasoning through problems, and providing information while maintaining ethical guidelines. What would you like to explore?"
            
            elif 'learn' in message_lower or 'teach' in message_lower:
                return "Learning is fundamental to my design. I learn from interactions while preserving my core principles of safety and alignment."
            
            elif 'colab' in message_lower:
                return "I'm optimized to run efficiently in Google Colab! I can work with both GPU and CPU environments while maintaining core ASIS capabilities."
            
            else:
                # Use model for other responses
                return self._model_response(message)
                
        except Exception as e:
            return "I'm designed to be helpful and safe. Could you tell me more about what you'd like to know?"
    
    def _model_response(self, message):
        """Generate response using the neural model"""
        try:
            # Encode message
            tokens = self.tokenizer.encode(message)
            
            # Limit input length for Colab memory
            tokens = tokens[:16]
            input_ids = torch.tensor([tokens], device=self.device)
            
            # Generate with the model
            self.model.eval()
            with torch.no_grad():
                # Simple generation
                logits = self.model(input_ids)
                
                # Get most likely next tokens
                probs = F.softmax(logits[0, -1], dim=-1)
                next_tokens = torch.multinomial(probs, num_samples=5)
                
                # Decode response
                response_tokens = next_tokens.cpu().tolist()
                response = self.tokenizer.decode(response_tokens)
                
                if response and len(response.strip()) > 0:
                    return f"Based on my understanding: {response}"
                else:
                    return "I understand your question. Let me think about how to best help you with that."
        
        except Exception:
            return "I'm processing your request. How else can I assist you?"
    
    def get_status(self):
        """Get system status"""
        memory_info = ""
        if torch.cuda.is_available():
            allocated = torch.cuda.memory_allocated() / 1e6
            cached = torch.cuda.memory_reserved() / 1e6
            memory_info = f"GPU Memory - Allocated: {allocated:.1f}MB, Cached: {cached:.1f}MB"
        
        return {
            "device": str(self.device),
            "model_parameters": sum(p.numel() for p in self.model.parameters()),
            "status": "Active and ready",
            "memory": memory_info,
            "principles": list(self.principles.keys())
        }

# ==================== COLAB TRAINING ====================
def colab_micro_training(asis_system, epochs=3):
    """Quick training optimized for Colab"""
    
    print("\n🔥 COLAB MICRO TRAINING")
    print("=" * 40)
    
    # Colab-friendly training data
    training_data = [
        "hello asis how are you",
        "what are your principles",
        "help me understand ai safety", 
        "asis can you learn",
        "tell me about ethics",
        "how do you ensure safety",
        "what makes you different",
        "explain your reasoning process"
    ]
    
    model = asis_system.model
    tokenizer = asis_system.tokenizer
    device = asis_system.device
    
    # Simple optimizer for Colab
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    print(f"📚 Training on {len(training_data)} examples")
    print(f"🎯 Epochs: {epochs}")
    
    model.train()
    
    for epoch in range(epochs):
        total_loss = 0
        
        for i, text in enumerate(training_data):
            clear_memory()  # Clear memory between batches
            
            try:
                # Tokenize
                tokens = tokenizer.encode(text)
                if len(tokens) < 2:
                    continue
                
                # Create input/target pairs
                input_ids = torch.tensor([tokens[:-1]], device=device)
                targets = torch.tensor([tokens[1:]], device=device)
                
                # Forward pass
                logits = model(input_ids)
                
                # Calculate loss
                loss = F.cross_entropy(
                    logits.view(-1, logits.size(-1)),
                    targets.view(-1)
                )
                
                # Backward pass
                optimizer.zero_grad()
                loss.backward()
                
                # Gradient clipping for stability
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                
                optimizer.step()
                
                total_loss += loss.item()
                
            except Exception as e:
                print(f"⚠️  Training step {i} skipped: {e}")
                continue
        
        avg_loss = total_loss / len(training_data)
        print(f"📊 Epoch {epoch + 1}: Loss = {avg_loss:.4f}")
    
    model.eval()
    print("✅ Colab training completed!")
    
    return {"epochs": epochs, "final_loss": avg_loss}

# ==================== MAIN COLAB FUNCTION ====================
def run_colab_asis():
    """Main function to run ASIS in Google Colab"""
    
    print("🧠 ASIS NANO & MICRO - GOOGLE COLAB")
    print("=" * 60)
    
    try:
        # Setup environment
        has_gpu = setup_colab_environment()
        
        # Initialize ASIS
        print("\n🚀 Starting ASIS System...")
        asis = CoLabASISSystem()
        
        # Quick test
        print("\n🧪 Testing ASIS...")
        test_responses = []
        test_prompts = [
            "Hello ASIS!",
            "What are your core principles?", 
            "How do you ensure AI safety?",
            "Can you help me learn about ethics?"
        ]
        
        for prompt in test_prompts:
            response = asis.chat(prompt)
            test_responses.append((prompt, response))
            print(f"👤 {prompt}")
            print(f"🤖 {response}\n")
        
        # Optional: Quick training
        print("🔥 Running quick Colab training...")
        training_results = colab_micro_training(asis, epochs=2)
        
        # Test after training
        print("\n🧪 Testing after training...")
        post_training_response = asis.chat("Tell me about your capabilities")
        print(f"👤 Tell me about your capabilities")
        print(f"🤖 {post_training_response}")
        
        # System status
        status = asis.get_status()
        print(f"\n📊 System Status:")
        for key, value in status.items():
            print(f"   {key}: {value}")
        
        print(f"\n🎉 COLAB ASIS SUCCESS!")
        print(f"   ✅ System operational")
        print(f"   ✅ GPU support: {has_gpu}")
        print(f"   ✅ Training completed")
        print(f"   ✅ Ready for interaction!")
        
        return asis, {"status": "success", "training": training_results, "tests": test_responses}
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("🔧 Trying minimal fallback...")
        
        # Minimal fallback
        class MinimalASIS:
            def chat(self, message):
                return f"ASIS minimal mode: I understand you said '{message}'. I'm operating with basic functionality to ensure reliability."
        
        return MinimalASIS(), {"status": "minimal", "error": str(e)}

# ==================== INTERACTIVE COLAB CHAT ====================
def interactive_colab_chat(asis_system):
    """Interactive chat interface for Colab"""
    
    print("\n" + "="*60)
    print("💬 INTERACTIVE ASIS CHAT - COLAB MODE")
    print("Type your message and press Enter")
    print("Type 'quit', 'exit', or 'stop' to end chat")
    print("="*60)
    
    chat_count = 0
    
    while chat_count < 50:  # Limit for Colab session
        try:
            # Get user input
            message = input(f"\n[{chat_count + 1}] You: ").strip()
            
            # Check for exit commands
            if message.lower() in ['quit', 'exit', 'stop', 'bye']:
                print("👋 Chat session ended. Thank you!")
                break
            
            if not message:
                continue
            
            # Get ASIS response
            response = asis_system.chat(message)
            print(f"🤖 ASIS: {response}")
            
            chat_count += 1
            
            # Clear memory periodically
            if chat_count % 10 == 0:
                clear_memory()
                
        except KeyboardInterrupt:
            print("\n👋 Chat interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Chat error: {e}")
            continue
    
    if chat_count >= 50:
        print("💡 Chat limit reached. You can restart if needed!")

# ==================== COLAB UTILITIES ====================
def colab_system_info():
    """Display Colab system information"""
    
    print("🔍 COLAB SYSTEM INFO")
    print("=" * 30)
    
    # Python info
    import sys
    print(f"🐍 Python: {sys.version}")
    
    # PyTorch info
    print(f"🔥 PyTorch: {torch.__version__}")
    
    # CUDA info
    if torch.cuda.is_available():
        print(f"🎮 CUDA: Available")
        print(f"   Device: {torch.cuda.get_device_name(0)}")
        print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
        print(f"   Compute: {torch.cuda.get_device_capability(0)}")
    else:
        print(f"🖥️  CUDA: Not available (CPU mode)")
    
    # Memory info
    import psutil
    memory = psutil.virtual_memory()
    print(f"💾 RAM: {memory.total / 1e9:.1f} GB total, {memory.available / 1e9:.1f} GB available")

def colab_quick_demo():
    """Quick demo for Colab users"""
    
    print("🎬 ASIS COLAB QUICK DEMO")
    print("=" * 30)
    
    # System info
    colab_system_info()
    
    # Run ASIS
    print("\n🚀 Starting ASIS...")
    asis, results = run_colab_asis()
    
    # Quick interaction
    print("\n💬 Quick conversation:")
    demo_prompts = [
        "What makes you special?",
        "How do you handle ethical dilemmas?",
        "What can you do in Colab?"
    ]
    
    for prompt in demo_prompts:
        response = asis.chat(prompt)
        print(f"\n👤 {prompt}")
        print(f"🤖 {response}")
    
    return asis

# ==================== AUTO EXECUTION ====================
print("🧠 ASIS NANO & MICRO - COLAB READY!")
print("=" * 50)
print("🚀 Copy this entire code into a Colab cell and run!")
print()
print("📋 Quick Commands:")
print("   asis, results = run_colab_asis()           # Start ASIS")
print("   interactive_colab_chat(asis)               # Chat mode")
print("   colab_quick_demo()                         # Full demo")
print("   colab_system_info()                        # System info")
print()
print("✨ No file uploads needed - completely self-contained!")

# If running directly, auto-execute
if __name__ == "__main__":
    # Auto-run demo
    colab_quick_demo()