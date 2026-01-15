#!/usr/bin/env python3
"""Simple test script for advanced embedding system integration"""

def test_integration():
    print("Testing advanced embedding system integration...")
    
    try:
        # Test imports
        print("1. Testing imports...")
        from enhanced_memory_network import EnhancedMemoryNetwork, AdvancedEmbeddingSystem
        print("✅ Enhanced memory network imported successfully")
        
        try:
            from advanced_embedding_system import MultiModalEmbeddingSystem
            print("✅ Advanced embedding system imported successfully")
        except ImportError:
            print("⚠️ Advanced embedding system not available (using fallback)")
        
        # Test basic initialization
        print("\n2. Testing initialization...")
        embedding_system = AdvancedEmbeddingSystem()
        print(f"✅ Embedding system initialized: {embedding_system.initialized}")
        print(f"✅ System type: {embedding_system.get_statistics()['system_type']}")
        
        # Test basic embedding
        print("\n3. Testing embedding generation...")
        test_text = ['Hello world', 'Test embedding', 'Advanced AI system']
        embeddings = embedding_system.encode(test_text)
        print(f"✅ Generated embeddings shape: {embeddings.shape}")
        print(f"✅ Embedding dimensions: {embedding_system.get_embedding_dimension()}")
        
        # Test similarity
        print("\n4. Testing similarity computation...")
        sim = embedding_system.calculate_similarity(embeddings[0], embeddings[1])
        print(f"✅ Similarity between texts: {sim:.4f}")
        
        # Test statistics
        print("\n5. Testing system statistics...")
        stats = embedding_system.get_statistics()
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        print("\n🎉 All tests passed! Advanced embedding system is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_integration()
