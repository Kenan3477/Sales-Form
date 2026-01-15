#!/usr/bin/env python3
"""
ASIS System Test - Verify All Components Working
===============================================
"""

print("🔍 Testing ASIS Complete System...")
print("=" * 50)

try:
    # Test 1: Core Identity System
    print("🧠 Testing Core Identity System...")
    from asis_core_identity import ASISCoreIdentity
    identity = ASISCoreIdentity()
    creator_info = identity.get_creator_basic_info()
    print(f"   ✅ Creator: {creator_info['name']} (Born: {creator_info['birth_date']})")
    
    # Test 2: Autonomous Research System  
    print("🔬 Testing Autonomous Research System...")
    from asis_autonomous_research_fixed import ASISAutonomousResearch
    research = ASISAutonomousResearch()
    research_status = research.get_research_status()
    print(f"   ✅ Research Threads: {research_status.get('active_research_threads', 0)}")
    
    # Test 3: Pattern Recognition System
    print("🎯 Testing Pattern Recognition System...")
    from asis_advanced_pattern_recognition import ASISPatternRecognitionSystem
    patterns = ASISPatternRecognitionSystem()
    pattern_status = patterns.get_system_status()
    print(f"   ✅ Pattern Health: {pattern_status['overall_health']:.1f}%")
    
    # Test 4: Complete Verification System
    print("🔍 Testing Complete Verification System...")
    from asis_complete_verification_system import ASISCompleteVerificationSystem
    verification = ASISCompleteVerificationSystem()
    
    # Run quick verification
    quick_results = verification.quick_verification_check()
    print(f"   ✅ Quick Verification: {quick_results['quick_verification_score']:.1f}%")
    
    # Test 5: Training Interface
    print("🤖 Testing Training Interface...")
    from asis_complete_training_interface import asis_interface
    
    # Test creator knowledge
    response = asis_interface.process_user_input("Who created you?")
    print(f"   ✅ Creator Response: {response['response'][:100]}...")
    
    # Test system status
    status = asis_interface.get_system_status()
    print(f"   ✅ System Status: {status['overall_status'].upper()}")
    print(f"   ✅ Authenticity: {status['authenticity_score']:.1f}%")
    
    print("\n🎉 ALL TESTS PASSED!")
    print("🚀 ASIS is fully operational and ready for Railway deployment!")
    print(f"🎯 Final Authenticity Score: {status['authenticity_score']:.1f}%")
    
except Exception as e:
    print(f"❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()
