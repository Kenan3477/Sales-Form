#!/usr/bin/env python3
"""
Simple Cross-Domain Engine Test
==============================
Minimal test to check if the engine can be imported and initialized
"""

import sys
import os
import traceback

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_engine_import():
    """Test if the cross-domain engine can be imported and initialized"""
    
    print("🔍 Testing Cross-Domain Engine Import")
    print("="*40)
    
    try:
        print("📋 Step 1: Attempting import...")
        from asis_cross_domain_reasoning_engine import CrossDomainReasoningEngine
        print("✅ Import successful!")
        
        print("📋 Step 2: Attempting initialization...")
        engine = CrossDomainReasoningEngine()
        print("✅ Initialization successful!")
        
        print("📋 Step 3: Checking engine attributes...")
        
        # Check for key attributes
        attributes = ['domain_knowledge', 'reasoning_patterns', 'cross_domain_mappings']
        for attr in attributes:
            if hasattr(engine, attr):
                print(f"   ✅ {attr}: Present")
            else:
                print(f"   ❌ {attr}: Missing")
        
        print("📋 Step 4: Checking key methods...")
        methods = ['advanced_cross_domain_reasoning']
        for method in methods:
            if hasattr(engine, method):
                print(f"   ✅ {method}: Present")
            else:
                print(f"   ❌ {method}: Missing")
        
        print("\n✅ ENGINE TEST SUCCESSFUL!")
        print("📊 Cross-domain reasoning engine is ready for use")
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Cross-domain engine file may be missing or corrupted")
        return False
        
    except Exception as e:
        print(f"❌ Initialization Error: {e}")
        print("💡 Engine may have initialization issues")
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    
    print("🧪 CROSS-DOMAIN ENGINE DIAGNOSTIC TEST")
    print("="*45)
    
    success = test_engine_import()
    
    if success:
        print("\n🎯 CONCLUSION: Engine is ready for testing!")
        print("💡 You can now run cross-domain reasoning tests")
    else:
        print("\n⚠️ CONCLUSION: Engine has issues!")
        print("💡 Fix import/initialization issues before testing")
    
    return success

if __name__ == "__main__":
    main()
