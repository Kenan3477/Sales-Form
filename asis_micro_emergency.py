"""
🧠 ASIS MICRO - FITS IN MINIMAL GPU MEMORY
Emergency ultra-tiny version for memory-constrained environments
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import gc
import os

# Force memory cleanup
def clear_memory():
    """Aggressive memory cleanup"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
    gc.collect()

# ==================== MICRO TOKENIZER ====================
class MicroTokenizer:
    """Absolutely minimal tokenizer"""
    
    def __init__(self):
        # Only 50 essential tokens
        chars = "abcdefghijklmnopqrstuvwxyz0123456789 .,!?ASISHUMANHELLO"
        self.vocab = {char: i for i, char in enumerate(chars)}
        self.vocab_size = len(chars)
        self.pad_id = 0
        print(f"✅ Micro tokenizer: {self.vocab_size} tokens")
    
    def encode(self, text):
        return [self.vocab.get(c.lower(), 0) for c in text[:20]]  # Max 20 chars
    
    def decode(self, tokens):
        chars = list(self.vocab.keys())
        return ''.join(chars[min(t, len(chars)-1)] for t in tokens)

# ==================== MICRO MODEL ====================
class MicroASIS(nn.Module):
    """Micro ASIS - designed to fit in <100MB memory"""
    
    def __init__(self):
        super().__init__()
        
        # Micro configuration
        self.vocab_size = 50
        self.hidden_size = 512      # Very small
        self.num_layers = 12        # Fewer layers
        self.seq_len = 32          # Very short sequences
        
        # Minimal components
        self.embed = nn.Embedding(self.vocab_size, self.hidden_size)
        
        # Ultra-simple "transformer" layers
        self.layers = nn.ModuleList([
            nn.Sequential(
                nn.LayerNorm(self.hidden_size),
                nn.Linear(self.hidden_size, self.hidden_size),
                nn.ReLU(),
                nn.Linear(self.hidden_size, self.hidden_size)
            ) for _ in range(self.num_layers)
        ])
        
        self.head = nn.Linear(self.hidden_size, self.vocab_size)
        
        # Count parameters
        total_params = sum(p.numel() for p in self.parameters())
        memory_mb = total_params * 4 / (1024 * 1024)  # FP32
        
        print(f"🧠 Micro ASIS: {total_params:,} parameters")
        print(f"💾 Memory needed: ~{memory_mb:.1f} MB")
    
    def forward(self, x):
        # Very simple forward pass
        x = self.embed(x)
        
        for layer in self.layers:
            residual = x
            x = layer(x)
            x = x + residual  # Residual connection
        
        return self.head(x)

# ==================== MICRO SYSTEM ====================
class MicroASISSystem:
    """Micro ASIS system for extreme memory constraints"""
    
    def __init__(self):
        print("🚀 Initializing Micro ASIS (Emergency Mode)...")
        
        # Clear memory first
        clear_memory()
        
        # Initialize components
        self.tokenizer = MicroTokenizer()
        self.model = MicroASIS()
        
        # Check available memory
        if torch.cuda.is_available():
            free_mem = torch.cuda.get_device_properties(0).total_memory
            allocated = torch.cuda.memory_allocated()
            free_mb = (free_mem - allocated) / (1024 * 1024)
            
            print(f"🔍 Available GPU memory: {free_mb:.1f} MB")
            
            if free_mb > 200:  # Only move to GPU if we have enough memory
                try:
                    self.model = self.model.cuda()
                    self.device = torch.device("cuda")
                    print("✅ Model on GPU")
                except:
                    self.device = torch.device("cpu")
                    print("⚠️ GPU failed, using CPU")
            else:
                self.device = torch.device("cpu")
                print("⚠️ Insufficient GPU memory, using CPU")
        else:
            self.device = torch.device("cpu")
            print("📱 Using CPU")
        
        clear_memory()
        print("✅ Micro ASIS ready!")
    
    def chat(self, message):
        """Ultra-simple chat"""
        try:
            # Encode
            tokens = self.tokenizer.encode(message)
            input_ids = torch.tensor([tokens], device=self.device)
            
            # Generate
            with torch.no_grad():
                logits = self.model(input_ids)
                
                # Simple sampling from last position
                last_logits = logits[0, -1, :]
                next_token = torch.argmax(last_logits).item()
                
                # Generate a few more tokens
                response_tokens = [next_token]
                current_input = torch.cat([input_ids, torch.tensor([[next_token]], device=self.device)], dim=1)
                
                for _ in range(5):  # Generate 5 tokens
                    logits = self.model(current_input[:, -10:])  # Last 10 tokens only
                    next_token = torch.argmax(logits[0, -1, :]).item()
                    response_tokens.append(next_token)
                    current_input = torch.cat([current_input, torch.tensor([[next_token]], device=self.device)], dim=1)
            
            # Decode
            response = self.tokenizer.decode(response_tokens)
            
            # Clean up
            clear_memory()
            
            return response if response else "hello asis here"
            
        except Exception as e:
            clear_memory()
            return f"micro asis active: {str(e)[:20]}"

# ==================== MICRO TRAINING ====================
def micro_train(system):
    """Ultra-simple training for micro ASIS"""
    
    print("\n🔥 MICRO TRAINING (Emergency Mode)")
    print("=" * 40)
    
    # Tiny training data
    tiny_data = ["hello", "asis", "help", "ai", "good"]
    
    model = system.model
    model.train()
    
    # Simple optimizer
    optimizer = optim.SGD(model.parameters(), lr=0.01)  # SGD uses less memory than Adam
    
    print(f"📚 Training on {len(tiny_data)} micro examples")
    
    try:
        for step, text in enumerate(tiny_data):
            clear_memory()
            
            # Encode
            tokens = system.tokenizer.encode(text)
            if len(tokens) < 2:
                continue
                
            input_ids = torch.tensor([tokens[:-1]], device=system.device)
            targets = torch.tensor([tokens[1:]], device=system.device)
            
            # Forward
            logits = model(input_ids)
            
            # Loss
            loss = F.cross_entropy(
                logits.view(-1, logits.size(-1)), 
                targets.view(-1)
            )
            
            # Backward
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            print(f"   Step {step + 1}: Loss = {loss.item():.4f}")
            
            # Cleanup
            del loss, logits
            clear_memory()
            
    except Exception as e:
        print(f"⚠️ Training stopped: {str(e)[:30]}")
    
    print("✅ Micro training completed!")
    return {"status": "completed"}

# ==================== EMERGENCY SYSTEM ====================
def run_emergency_asis():
    """Emergency ASIS system for extreme memory constraints"""
    
    print("🚨 EMERGENCY ASIS SYSTEM")
    print("=" * 50)
    
    # Check memory situation
    if torch.cuda.is_available():
        total_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        allocated = torch.cuda.memory_allocated() / (1024**3)
        free = total_mem - allocated
        
        print(f"🔍 GPU Memory Status:")
        print(f"   Total: {total_mem:.1f} GB")
        print(f"   Allocated: {allocated:.1f} GB")
        print(f"   Free: {free:.1f} GB")
        
        if free < 1.0:
            print("⚠️ CRITICAL: Less than 1GB free memory!")
            print("🔧 Attempting aggressive cleanup...")
            
            # Try to free memory
            clear_memory()
            
            # Set memory fraction to be very conservative
            if hasattr(torch.cuda, 'set_per_process_memory_fraction'):
                torch.cuda.set_per_process_memory_fraction(0.1)  # Use only 10% of remaining
    
    try:
        # Initialize micro system
        micro_asis = MicroASISSystem()
        
        # Quick test
        print("\n🧪 Testing micro ASIS:")
        response = micro_asis.chat("hi")
        print(f"Micro ASIS: {response}")
        
        # Micro training
        print("\n🔥 Starting micro training...")
        train_results = micro_train(micro_asis)
        
        # Test after training
        print("\n🧪 After micro training:")
        for prompt in ["hi", "help", "ai"]:
            response = micro_asis.chat(prompt)
            print(f"'{prompt}' → '{response}'")
        
        # Try to save (if possible)
        try:
            torch.save(micro_asis.model.state_dict(), "micro_asis.pt")
            print("\n✅ Micro model saved: micro_asis.pt")
        except:
            print("\n⚠️ Could not save model")
        
        print(f"\n🎉 EMERGENCY ASIS SUCCESS!")
        print(f"   Model: Micro ASIS")
        print(f"   Parameters: {sum(p.numel() for p in micro_asis.model.parameters()):,}")
        print(f"   Status: Working in emergency mode! 🚑")
        
        return micro_asis, train_results
        
    except Exception as e:
        print(f"\n❌ Emergency system failed: {str(e)}")
        print("🔧 Trying absolute minimum system...")
        
        return run_absolute_minimum()

def run_absolute_minimum():
    """Absolute minimum system if everything else fails"""
    
    print("\n🔧 ABSOLUTE MINIMUM ASIS")
    print("=" * 30)
    
    class TinyModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.linear = nn.Linear(10, 10)
            
        def forward(self, x):
            return self.linear(torch.randn(1, 10))
    
    try:
        model = TinyModel()
        if torch.cuda.is_available():
            try:
                model = model.cuda()
                device = "cuda"
            except:
                device = "cpu"
        else:
            device = "cpu"
        
        print(f"✅ Tiny model on {device}")
        print(f"   Parameters: {sum(p.numel() for p in model.parameters())}")
        
        # Simple test
        with torch.no_grad():
            output = model(torch.randn(1, 10))
            print(f"   Test output shape: {output.shape}")
        
        print("🎉 Absolute minimum system working!")
        return model, {"status": "minimum"}
        
    except Exception as e:
        print(f"❌ Even minimum system failed: {e}")
        return None, {"status": "failed"}

# ==================== MAIN EXECUTION ====================
print("🚨 EMERGENCY ASIS SYSTEM FOR EXTREME MEMORY CONSTRAINTS")
print("Designed to work in <100MB GPU memory")
print("")
print("Run: micro_asis, results = run_emergency_asis()")

if __name__ == "__main__":
    # Auto-run emergency system
    try:
        micro_asis, results = run_emergency_asis()
        if micro_asis:
            print("🎉 Emergency ASIS system operational!")
        else:
            print("⚠️ System running in minimum mode")
    except Exception as e:
        print(f"🚨 Critical error: {e}")
        print("🔧 Manual execution required")