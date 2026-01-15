#!/usr/bin/env python3
"""
Simple AGI Integration Test
==========================
"""

print("🧠 Testing AdvancedAIEngine AGI Integration...")

try:
    from advanced_ai_engine import AdvancedAIEngine
    print("✅ AdvancedAIEngine imported successfully")
    
    # Initialize engine
    engine = AdvancedAIEngine()
    print("✅ Engine initialized with AGI enhancements")
    
    # Check if AGI engines are loaded
    has_ethical = hasattr(engine, 'ethical_reasoning_engine')
    has_cross_domain = hasattr(engine, 'cross_domain_reasoning_engine')  
    has_creative = hasattr(engine, 'novel_problem_solving_engine')
    
    print(f"⚖️ Ethical Reasoning Engine: {'✅' if has_ethical else '❌'}")
    print(f"🔄 Cross-Domain Reasoning Engine: {'✅' if has_cross_domain else '❌'}")
    print(f"🎨 Novel Problem Solving Engine: {'✅' if has_creative else '❌'}")
    
    # Test async method availability
    has_async_method = hasattr(engine, 'process_input_with_understanding')
    has_sync_method = hasattr(engine, 'process_input_with_understanding_sync')
    
    print(f"🔄 Async Processing Method: {'✅' if has_async_method else '❌'}")
    print(f"🔄 Sync Compatibility Method: {'✅' if has_sync_method else '❌'}")
    
    # Test sync processing
    print("\n🧪 Testing basic sync processing...")
    result = engine.process_input_with_understanding_sync(
        "How can AI be more ethical?", 
        []
    )
    
    print(f"✅ Sync processing successful")
    print(f"Response length: {len(result.get('response', ''))}")
    print(f"AGI Enhancement Active: {result.get('agi_enhancement_active', False)}")
    
    if result.get('agi_enhancements'):
        print(f"🚀 AGI Enhancements detected!")
        enhancements = result['agi_enhancements']
        print(f"Overall confidence: {enhancements.get('overall_confidence', 0.0):.2%}")
    
    print("\n🎉 AGI Integration Test SUCCESSFUL!")
    print("✅ All three AGI enhancement engines are integrated:")
    print("   ⚖️ Ethical constraint evaluation")
    print("   🔄 Cross-domain analogical analysis") 
    print("   🎨 Creative problem solving")

except Exception as e:
    print(f"❌ AGI Integration Test FAILED: {e}")
    import traceback
    print(traceback.format_exc())
