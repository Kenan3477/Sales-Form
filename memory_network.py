#!/usr/bin/env python3
"""
Memory Network System - Export Interface
========================================
Provides standardized exports for memory network functionality
Uses EnhancedMemoryNetwork as the underlying implementation
"""

# Import the enhanced memory network components
try:
    from enhanced_memory_network import (
        EnhancedMemoryNetwork,
        MemoryType,
        ImportanceLevel,
        EnhancedMemory,
        EmotionalTag
    )
    
    # Export aliases for expected class names
    MemoryNetwork = EnhancedMemoryNetwork  # Main export alias
    
    # Additional exports that might be expected
    Memory = EnhancedMemory
    
    # Create a simple Thought class for compatibility
    class Thought:
        """Simple thought class for backward compatibility"""
        def __init__(self, content: str, timestamp: str = None, importance: float = 0.5):
            self.content = content
            self.timestamp = timestamp or str(datetime.now())
            self.importance = importance
            self.id = hashlib.sha256(f"{content}{self.timestamp}".encode()).hexdigest()[:16]
    
    print("✅ Memory Network exports loaded successfully from enhanced_memory_network")
    
except ImportError as e:
    print(f"⚠️ Enhanced memory network not available: {e}")
    
    # Fallback simple memory network implementation
    import hashlib
    from datetime import datetime
    from typing import List, Dict, Any, Optional
    
    class MemoryNetwork:
        """Simple fallback memory network implementation"""
        
        def __init__(self, embedding_method='tfidf'):
            self.memories = []
            self.embedding_method = embedding_method
            print("⚠️ Using fallback MemoryNetwork implementation")
        
        def store_memory(self, content: str, memory_type: str = "general", 
                        importance: float = 0.5, **kwargs) -> str:
            """Store a memory"""
            memory_id = hashlib.sha256(f"{content}{datetime.now()}".encode()).hexdigest()[:16]
            memory = {
                "id": memory_id,
                "content": content,
                "memory_type": memory_type,
                "importance": importance,
                "timestamp": datetime.now().isoformat(),
                **kwargs
            }
            self.memories.append(memory)
            return memory_id
        
        def retrieve_memories(self, query: str, limit: int = 5) -> List[Dict]:
            """Retrieve relevant memories"""
            # Simple keyword matching for fallback
            query_lower = query.lower()
            relevant = []
            
            for memory in self.memories:
                if any(word in memory["content"].lower() for word in query_lower.split()):
                    relevant.append(memory)
            
            # Sort by importance and return top results
            relevant.sort(key=lambda x: x["importance"], reverse=True)
            return relevant[:limit]
        
        def get_memory_count(self) -> int:
            """Get total memory count"""
            return len(self.memories)
    
    class Thought:
        """Simple thought class"""
        def __init__(self, content: str, timestamp: str = None, importance: float = 0.5):
            self.content = content
            self.timestamp = timestamp or datetime.now().isoformat()
            self.importance = importance
            self.id = hashlib.sha256(f"{content}{self.timestamp}".encode()).hexdigest()[:16]
    
    # Create mock types for compatibility
    class MemoryType:
        EPISODIC = "episodic"
        SEMANTIC = "semantic"
        PROCEDURAL = "procedural"
    
    class ImportanceLevel:
        LOW = 0.2
        MEDIUM = 0.5
        HIGH = 0.8
        CRITICAL = 1.0
    
    print("✅ Fallback Memory Network implementation loaded")

# Make sure all expected exports are available
__all__ = [
    'MemoryNetwork',
    'Thought', 
    'Memory',
    'MemoryType',
    'ImportanceLevel'
]
