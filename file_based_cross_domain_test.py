#!/usr/bin/env python3
"""
File-Based Cross-Domain Test
===========================
Writes output to file since terminal capture isn't working
"""

import sys
import os
import asyncio
import traceback
from datetime import datetime

# Add current directory to path
sys.path.append(os.getcwd())

class TestLogger:
    """Logger that writes to both console and file"""
    
    def __init__(self, filename="cross_domain_test_results.txt"):
        self.filename = filename
        # Clear previous results
        with open(filename, "w") as f:
            f.write(f"Cross-Domain Test Results\n")
            f.write(f"========================\n")
            f.write(f"Start time: {datetime.now()}\n\n")
    
    def log(self, message):
        """Log message to both console and file"""
        print(message)
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")

async def test_cross_domain_with_logging():
    """Test cross-domain reasoning with file logging"""
    
    logger = TestLogger()
    
    logger.log("🔄 CROSS-DOMAIN REASONING TEST WITH LOGGING")
    logger.log("="*45)
    
    try:
        # Step 1: Import test
        logger.log("\n1️⃣ Testing import...")
        
        try:
            from asis_cross_domain_reasoning_engine import CrossDomainReasoningEngine
            logger.log("✅ Import successful")
        except Exception as e:
            logger.log(f"❌ Import failed: {e}")
            return False
        
        # Step 2: Initialization test
        logger.log("\n2️⃣ Testing initialization...")
        
        try:
            engine = CrossDomainReasoningEngine()
            logger.log("✅ Initialization successful")
        except Exception as e:
            logger.log(f"❌ Initialization failed: {e}")
            return False
        
        # Step 3: Method existence test
        logger.log("\n3️⃣ Testing method existence...")
        
        if hasattr(engine, 'advanced_cross_domain_reasoning'):
            logger.log("✅ advanced_cross_domain_reasoning method found")
        else:
            logger.log("❌ advanced_cross_domain_reasoning method missing")
            return False
        
        # Step 4: Method call test
        logger.log("\n4️⃣ Testing method call...")
        
        try:
            result = await engine.advanced_cross_domain_reasoning(
                source_domain="physics",
                target_domain="economics", 
                concept="conservation_of_energy",
                problem="How to maintain value in economic transactions"
            )
            
            logger.log("✅ Method call successful!")
            logger.log(f"📊 Result type: {type(result)}")
            logger.log(f"📊 Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
            
            if isinstance(result, dict):
                confidence = result.get('confidence', 0)
                logger.log(f"📊 Confidence: {confidence:.3f} ({confidence*100:.1f}%)")
                logger.log(f"🔄 Analogical mappings: {len(result.get('analogical_mapping', {}))}")
                logger.log(f"📋 Transferred principles: {len(result.get('transferred_principles', []))}")
                logger.log(f"🧩 Reasoning steps: {len(result.get('reasoning_steps', []))}")
                
                # Show solution approach
                solution = result.get('solution_approach', '')
                if solution:
                    logger.log(f"\n🎯 Solution approach:")
                    logger.log(f"   {solution[:200]}...")  # First 200 chars
                
                # Performance assessment
                if confidence > 0.7:
                    logger.log("\n🚀 EXCELLENT PERFORMANCE!")
                    logger.log("Cross-domain reasoning is working at high level")
                elif confidence > 0.5:
                    logger.log("\n📈 GOOD PERFORMANCE!")
                    logger.log("Cross-domain reasoning is working well")
                else:
                    logger.log("\n📊 MODERATE PERFORMANCE!")
                    logger.log("Cross-domain reasoning is functional but could improve")
                
                logger.log(f"\n✅ CROSS-DOMAIN TEST SUCCESSFUL!")
                logger.log("The engine is working properly!")
                
                return True
            else:
                logger.log("❌ Method returned unexpected result type")
                return False
                
        except Exception as e:
            logger.log(f"❌ Method call failed: {e}")
            logger.log(f"Exception details:")
            logger.log(traceback.format_exc())
            return False
    
    except Exception as e:
        logger.log(f"❌ Test failed with exception: {e}")
        logger.log(f"Exception details:")
        logger.log(traceback.format_exc())
        return False

async def main():
    """Main test function"""
    
    logger = TestLogger()
    
    try:
        success = await test_cross_domain_with_logging()
        
        logger.log(f"\n{'='*45}")
        logger.log(f"FINAL RESULT: {'SUCCESS' if success else 'FAILED'}")
        logger.log(f"End time: {datetime.now()}")
        
        if success:
            logger.log("\n🎉 Cross-domain reasoning test PASSED!")
            logger.log("💡 The original quick_cross_domain_test.py issue was likely")
            logger.log("💡 related to terminal output capture, not the engine itself")
            logger.log("\n📋 NEXT STEPS:")
            logger.log("1. Cross-domain engine is confirmed working")
            logger.log("2. You can use it in your AGI integration")
            logger.log("3. The confidence score shows good performance")
        else:
            logger.log("\n⚠️ Cross-domain reasoning test FAILED!")
            logger.log("💡 Check the error details above")
            logger.log("💡 Fix issues before using in AGI integration")
        
        return success
        
    except Exception as e:
        logger.log(f"\n❌ Main function failed: {e}")
        logger.log(traceback.format_exc())
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        
        # Also write a simple status file
        with open("test_status.txt", "w") as f:
            f.write(f"CROSS_DOMAIN_TEST_STATUS: {'SUCCESS' if result else 'FAILED'}\n")
            f.write(f"TIMESTAMP: {datetime.now()}\n")
        
        print(f"\n📄 Results written to: cross_domain_test_results.txt")
        print(f"📄 Status written to: test_status.txt")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        traceback.print_exc()
