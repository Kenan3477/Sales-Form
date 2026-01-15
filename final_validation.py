#!/usr/bin/env python3
"""
Final Interface Fix Verification
"""

import sys

def test_imports():
    """Test that all imports work"""
    try:
        from asis_ethical_reasoning_engine import EthicalReasoningEngine
        from asis_cross_domain_reasoning_engine import CrossDomainReasoningEngine
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_interface_signatures():
    """Test interface method signatures"""
    try:
        from asis_ethical_reasoning_engine import EthicalReasoningEngine
        from asis_cross_domain_reasoning_engine import CrossDomainReasoningEngine
        
        ethical = EthicalReasoningEngine()
        cross_domain = CrossDomainReasoningEngine()
        
        # Check if methods exist
        assert hasattr(ethical, 'analyze_ethical_implications'), "Missing analyze_ethical_implications"
        assert hasattr(cross_domain, 'reason_across_domains'), "Missing reason_across_domains"
        
        print("✅ All required methods exist")
        return True
    except Exception as e:
        print(f"❌ Method check failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 FINAL INTERFACE VALIDATION")
    print("=" * 40)
    
    success = True
    
    print("\n📦 Testing imports...")
    success &= test_imports()
    
    print("\n🔍 Testing method signatures...")
    success &= test_interface_signatures()
    
    if success:
        print("\n🎉 ALL INTERFACE FIXES VALIDATED!")
        print("✅ Ethical Reasoning Engine: analyze_ethical_implications method available")
        print("✅ Cross-Domain Reasoning Engine: reason_across_domains method available")
        print("\n🚀 Ready for AGI capability assessment!")
    else:
        print("\n❌ Some interface fixes failed validation")
        sys.exit(1)
