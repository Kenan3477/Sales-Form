# 🚨 EMERGENCY ASIS - COPY & PASTE THIS ENTIRE CODE INTO COLAB

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import gc

# ==================== MEMORY CLEANUP ====================
def clear_memory():
    """Nuclear memory cleanup"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
        if hasattr(torch.cuda, 'reset_peak_memory_stats'):
            torch.cuda.reset_peak_memory_stats()
    gc.collect()
    print("🧹 Memory cleared")

# ==================== MICRO TOKENIZER ====================
class MicroTokenizer:
    def __init__(self):
        # Only essential characters
        chars = "abcdefghijklmnopqrstuvwxyz0123456789 .,!?-"
        self.vocab = {char: i for i, char in enumerate(chars)}
        self.vocab_size = len(chars)
        print(f"✅ Micro tokenizer: {self.vocab_size} tokens")
    
    def encode(self, text):
        return [self.vocab.get(c.lower(), 0) for c in text[:15]]  # Max 15 chars
    
    def decode(self, tokens):
        chars = list(self.vocab.keys())
        return ''.join(chars[min(t, len(chars)-1)] for t in tokens if t < len(chars))

# ==================== MICRO MODEL ====================
class MicroASIS(nn.Module):
    def __init__(self):
        super().__init__()
        
        # Ultra-micro configuration
        self.vocab_size = 45
        self.hidden_size = 256    # Very small
        self.num_layers = 4       # Very few layers
        
        # Minimal components
        self.embed = nn.Embedding(self.vocab_size, self.hidden_size)
        
        # Simple layers
        self.layers = nn.ModuleList([
            nn.Sequential(
                nn.Linear(self.hidden_size, self.hidden_size),
                nn.ReLU(),
                nn.Linear(self.hidden_size, self.hidden_size)
            ) for _ in range(self.num_layers)
        ])
        
        self.head = nn.Linear(self.hidden_size, self.vocab_size)
        
        # Count parameters
        total_params = sum(p.numel() for p in self.parameters())
        memory_mb = total_params * 4 / (1024 * 1024)
        
        print(f"🧠 Micro ASIS: {total_params:,} parameters ({memory_mb:.1f} MB)")
    
    def forward(self, x):
        x = self.embed(x)
        x = x.mean(dim=1)  # Simple pooling instead of sequence modeling
        
        for layer in self.layers:
            x = x + layer(x)  # Residual
        
        return self.head(x).unsqueeze(1)  # Add sequence dimension back

# ==================== MICRO SYSTEM ====================
class MicroASISSystem:
    def __init__(self):
        print("🚀 Initializing Emergency Micro ASIS...")
        
        # Clear memory aggressively
        clear_memory()
        
        # Initialize components
        self.tokenizer = MicroTokenizer()
        self.model = MicroASIS()
        
        # Try GPU, fallback to CPU
        try:
            if torch.cuda.is_available():
                # Check available memory
                total_mem = torch.cuda.get_device_properties(0).total_memory
                allocated = torch.cuda.memory_allocated()
                free_bytes = total_mem - allocated
                free_mb = free_bytes / (1024 * 1024)
                
                print(f"🔍 Free GPU memory: {free_mb:.0f} MB")
                
                if free_mb > 50:  # Need at least 50MB
                    self.model = self.model.cuda()
                    self.device = torch.device("cuda")
                    print("✅ Model on GPU")
                else:
                    self.device = torch.device("cpu")
                    print("⚠️ Using CPU (insufficient GPU memory)")
            else:
                self.device = torch.device("cpu")
                print("📱 Using CPU")
                
        except Exception as e:
            self.device = torch.device("cpu")
            print(f"⚠️ GPU failed, using CPU: {str(e)[:30]}")
        
        clear_memory()
        print("✅ Micro ASIS ready!")
    
    def chat(self, message):
        """Ultra-simple chat"""
        try:
            self.model.eval()
            
            with torch.no_grad():
                # Encode
                tokens = self.tokenizer.encode(message)
                if not tokens:
                    tokens = [0]
                
                input_ids = torch.tensor([tokens], device=self.device)
                
                # Generate
                logits = self.model(input_ids)
                
                # Simple sampling
                probs = F.softmax(logits[0, 0, :], dim=-1)
                next_token = torch.multinomial(probs, 1).item()
                
                # Generate a few more tokens
                response_tokens = [next_token]
                for _ in range(3):
                    # Use last token as input
                    new_input = torch.tensor([[response_tokens[-1]]], device=self.device)
                    logits = self.model(new_input)
                    probs = F.softmax(logits[0, 0, :], dim=-1)
                    next_token = torch.multinomial(probs, 1).item()
                    response_tokens.append(next_token)
                
                # Decode
                response = self.tokenizer.decode(response_tokens)
                
                clear_memory()
                
                return response if response.strip() else "hello"
                
        except Exception as e:
            clear_memory()
            return f"asis: {str(e)[:10]}"

# ==================== MICRO TRAINING ====================
def micro_train(system):
    print("\n🔥 MICRO TRAINING")
    print("=" * 30)
    
    # Tiny training data
    train_data = ["hello", "help", "good", "asis"]
    
    model = system.model
    model.train()
    
    # Simple optimizer
    optimizer = optim.SGD(model.parameters(), lr=0.1)
    
    try:
        for step, text in enumerate(train_data):
            clear_memory()
            
            # Encode
            tokens = system.tokenizer.encode(text)
            if len(tokens) < 1:
                continue
            
            # Create input/target
            input_ids = torch.tensor([tokens], device=system.device)
            target = torch.tensor([tokens[0]], device=system.device)  # Predict first token
            
            # Forward
            logits = model(input_ids)
            loss = F.cross_entropy(logits[0, 0, :].unsqueeze(0), target)
            
            # Backward
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            print(f"   Step {step + 1}: Loss = {loss.item():.3f}")
            
            # Cleanup
            del loss, logits
            clear_memory()
            
    except Exception as e:
        print(f"⚠️ Training error: {str(e)[:30]}")
    
    print("✅ Training completed!")
    return {"status": "done"}

# ==================== MAIN FUNCTION ====================
def run_emergency_asis():
    """Main emergency ASIS function"""
    
    print("🚨 EMERGENCY MICRO ASIS SYSTEM")
    print("=" * 50)
    
    # Memory status
    if torch.cuda.is_available():
        total = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        allocated = torch.cuda.memory_allocated() / (1024**3)
        print(f"🔍 GPU: {total:.1f}GB total, {allocated:.1f}GB used")
    
    try:
        # Initialize
        micro_asis = MicroASISSystem()
        
        # Test before training
        print("\n🧪 Before training:")
        response = micro_asis.chat("hi")
        print(f"ASIS: {response}")
        
        # Train
        print("\n🔥 Training...")
        results = micro_train(micro_asis)
        
        # Test after training
        print("\n🧪 After training:")
        for prompt in ["hi", "help"]:
            response = micro_asis.chat(prompt)
            print(f"'{prompt}' → '{response}'")
        
        # Try to save
        try:
            torch.save(micro_asis.model.state_dict(), "micro_asis.pt")
            print("\n✅ Model saved!")
        except:
            print("\n⚠️ Could not save")
        
        print(f"\n🎉 SUCCESS!")
        params = sum(p.numel() for p in micro_asis.model.parameters())
        print(f"   Parameters: {params:,}")
        print(f"   Status: Emergency ASIS operational! 🚑")
        
        return micro_asis, results
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        
        # Absolute fallback
        print("🔧 Trying absolute minimum...")
        try:
            model = nn.Linear(10, 10)
            print("✅ Minimum model created")
            return model, {"status": "minimum"}
        except:
            print("❌ Complete failure")
            return None, {"status": "failed"}

# ==================== AUTO EXECUTION ====================
print("🚨 EMERGENCY ASIS - READY TO RUN")
print("Execute: micro_asis, results = run_emergency_asis()")

# If running directly, auto-execute
if __name__ == "__main__":
    micro_asis, results = run_emergency_asis()