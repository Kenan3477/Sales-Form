#!/usr/bin/env python3
"""
Step-by-Step AGI Debug Test
===========================
Debug each step of AGI integration to find the issue
"""

import sys
import os
import asyncio
from datetime import datetime

# Add current directory to path
sys.path.append(os.getcwd())

class StepByStepLogger:
    """Detailed step-by-step logger"""
    
    def __init__(self, filename="step_by_step_debug.txt"):
        self.filename = filename
        with open(filename, "w") as f:
            f.write(f"Step-by-Step AGI Debug Results\n")
            f.write(f"==============================\n")
            f.write(f"Start time: {datetime.now()}\n\n")
    
    def log(self, message):
        print(message)
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")

async def debug_agi_step_by_step():
    """Debug AGI integration step by step"""
    
    logger = StepByStepLogger()
    
    logger.log("🔍 STEP-BY-STEP AGI DEBUG")
    logger.log("="*30)
    
    # Step 1: Test imports
    logger.log("\n1️⃣ IMPORT TEST")
    logger.log("-"*15)
    
    try:
        from advanced_ai_engine import AdvancedAIEngine
        logger.log("✅ AdvancedAIEngine imported successfully")
    except Exception as e:
        logger.log(f"❌ Import failed: {e}")
        import traceback
        logger.log(traceback.format_exc())
        return False
    
    # Step 2: Test initialization
    logger.log("\n2️⃣ INITIALIZATION TEST")
    logger.log("-"*20)
    
    try:
        ai_engine = AdvancedAIEngine()
        logger.log("✅ AdvancedAIEngine initialized successfully")
        
        # Check AGI engines
        logger.log(f"📋 Ethical Engine Type: {type(ai_engine.ethical_reasoning_engine)}")
        logger.log(f"📋 Cross-Domain Engine Type: {type(ai_engine.cross_domain_reasoning_engine)}")
        logger.log(f"📋 Problem Solving Engine Type: {type(ai_engine.novel_problem_solving_engine)}")
        
    except Exception as e:
        logger.log(f"❌ Initialization failed: {e}")
        import traceback
        logger.log(traceback.format_exc())
        return False
    
    # Step 3: Test individual components
    logger.log("\n3️⃣ INDIVIDUAL ENGINE TEST")
    logger.log("-"*25)
    
    # Test ethical engine
    try:
        ethical_result = await ai_engine.ethical_reasoning_engine.comprehensive_ethical_analysis({
            "scenario": "Test scenario",
            "context": {"test": True},
            "stakeholders": ["user"],
            "decision_type": "test"
        })
        logger.log(f"✅ Ethical Engine: {ethical_result}")
    except Exception as e:
        logger.log(f"❌ Ethical Engine failed: {e}")
    
    # Test cross-domain engine
    try:
        cd_result = await ai_engine.cross_domain_reasoning_engine.advanced_cross_domain_reasoning(
            "physics", "economics", "conservation", "test problem"
        )
        logger.log(f"✅ Cross-Domain Engine: {cd_result}")
    except Exception as e:
        logger.log(f"❌ Cross-Domain Engine failed: {e}")
    
    # Test creative engine
    try:
        creative_result = await ai_engine.novel_problem_solving_engine.solve_novel_problem(
            "Test problem", {"context": "test"}
        )
        logger.log(f"✅ Creative Engine: {creative_result}")
    except Exception as e:
        logger.log(f"❌ Creative Engine failed: {e}")
    
    # Step 4: Test helper methods
    logger.log("\n4️⃣ HELPER METHODS TEST")
    logger.log("-"*20)
    
    test_input = "How can we solve climate change?"
    conversation_history = [{"role": "user", "content": "Hello"}]
    
    # Test semantic parsing
    try:
        semantic_result = ai_engine._semantic_parsing(test_input)
        logger.log(f"✅ Semantic Parsing: {len(semantic_result)} keys")
        logger.log(f"   Key concepts: {semantic_result.get('key_concepts', [])}")
    except Exception as e:
        logger.log(f"❌ Semantic Parsing failed: {e}")
    
    # Test context analysis
    try:
        context_result = ai_engine._analyze_conversation_context(test_input, conversation_history)
        logger.log(f"✅ Context Analysis: {len(context_result)} keys")
    except Exception as e:
        logger.log(f"❌ Context Analysis failed: {e}")
    
    # Step 5: Test AGI integration method
    logger.log("\n5️⃣ AGI INTEGRATION METHOD TEST")
    logger.log("-"*30)
    
    try:
        # Get required parameters
        semantic_analysis = ai_engine._semantic_parsing(test_input)
        context_analysis = ai_engine._analyze_conversation_context(test_input, conversation_history)
        intent_analysis = ai_engine._infer_user_intent(test_input, semantic_analysis, context_analysis)
        
        logger.log("✅ Prepared required parameters")
        
        # Test AGI integration method directly
        agi_result = await ai_engine._integrate_agi_enhancements(
            test_input, semantic_analysis, context_analysis, intent_analysis, conversation_history
        )
        
        logger.log(f"✅ AGI Integration Method: {len(agi_result)} keys")
        logger.log(f"   Enhancement Applied: {agi_result.get('enhancement_applied', False)}")
        logger.log(f"   Overall Confidence: {agi_result.get('overall_confidence', 0):.3f}")
        logger.log(f"   Available Keys: {list(agi_result.keys())}")
        
    except Exception as e:
        logger.log(f"❌ AGI Integration Method failed: {e}")
        import traceback
        logger.log(traceback.format_exc())
    
    # Step 6: Test full method call
    logger.log("\n6️⃣ FULL METHOD TEST")
    logger.log("-"*18)
    
    try:
        full_result = await ai_engine.process_input_with_understanding(test_input, conversation_history)
        
        logger.log(f"✅ Full Method Call: {type(full_result)}")
        logger.log(f"   Result Keys: {list(full_result.keys()) if isinstance(full_result, dict) else 'Not a dict'}")
        
        if isinstance(full_result, dict):
            logger.log(f"   Response Length: {len(full_result.get('response', ''))}")
            logger.log(f"   AGI Confidence: {full_result.get('agi_confidence_score', 0):.3f}")
            logger.log(f"   AGI Enhancement Active: {full_result.get('agi_enhancement_active', False)}")
            
            agi_enhancements = full_result.get('agi_enhancements', {})
            logger.log(f"   AGI Enhancements Keys: {list(agi_enhancements.keys())}")
            
        logger.log("✅ FULL TEST SUCCESSFUL!")
        return True
        
    except Exception as e:
        logger.log(f"❌ Full Method failed: {e}")
        import traceback
        logger.log(traceback.format_exc())
        return False

async def main():
    """Main debug function"""
    
    logger = StepByStepLogger()
    
    try:
        success = await debug_agi_step_by_step()
        
        logger.log(f"\n{'='*30}")
        logger.log(f"DEBUG RESULT: {'SUCCESS' if success else 'FAILED'}")
        logger.log(f"End time: {datetime.now()}")
        
        if success:
            logger.log(f"\n🎉 AGI DEBUG: All components working!")
            logger.log(f"💡 The issue might be in result processing or return values")
        else:
            logger.log(f"\n⚠️ AGI DEBUG: Issues found!")
            logger.log(f"💡 Check the specific component failures above")
        
        return success
        
    except Exception as e:
        logger.log(f"\n❌ Debug failed: {e}")
        import traceback
        logger.log(traceback.format_exc())
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        print(f"📄 Debug results: step_by_step_debug.txt")
        print(f"🎯 Result: {'SUCCESS' if result else 'FAILED'}")
        
    except KeyboardInterrupt:
        print("\n⚠️ Debug interrupted")
    except Exception as e:
        print(f"\n❌ Debug failed: {e}")
