#!/usr/bin/env python3
"""
Simple Advanced AI Engine Fix Test
=================================
"""

def test_fix():
    print("🔥 Testing Advanced AI Engine Fix")
    
    try:
        from advanced_ai_engine import AdvancedAIEngine
        engine = AdvancedAIEngine()
        
        print("✅ Engine imported successfully")
        
        if hasattr(engine, 'process_query'):
            print("✅ process_query method found!")
            print("🎉 FIX SUCCESSFUL!")
            return True
        else:
            print("❌ process_query method missing")
            methods = [method for method in dir(engine) if not method.startswith('_')]
            print(f"Available methods: {methods}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_fix()
