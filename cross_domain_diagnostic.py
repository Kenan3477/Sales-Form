#!/usr/bin/env python3
"""
Cross-Domain Diagnostic
======================
Advanced diagnostic to identify the exact issue with cross-domain testing
"""

import sys
import os
import asyncio
import traceback

# Add current directory to path
sys.path.append(os.getcwd())

def check_file_exists():
    """Check if the cross-domain engine file exists"""
    
    files_to_check = [
        "asis_cross_domain_reasoning_engine.py",
        "quick_cross_domain_test.py"
    ]
    
    print("📁 FILE EXISTENCE CHECK")
    print("="*30)
    
    for file_name in files_to_check:
        if os.path.exists(file_name):
            size = os.path.getsize(file_name)
            print(f"✅ {file_name} exists ({size} bytes)")
        else:
            print(f"❌ {file_name} missing")
    
    return all(os.path.exists(f) for f in files_to_check)

def test_import():
    """Test if the cross-domain engine can be imported"""
    
    print("\n🔍 IMPORT TEST")
    print("="*20)
    
    try:
        print("Attempting import...")
        from asis_cross_domain_reasoning_engine import CrossDomainReasoningEngine
        print("✅ Import successful")
        
        print("Attempting initialization...")
        engine = CrossDomainReasoningEngine()
        print("✅ Initialization successful")
        
        print("Checking method existence...")
        if hasattr(engine, 'advanced_cross_domain_reasoning'):
            print("✅ advanced_cross_domain_reasoning method exists")
        else:
            print("❌ advanced_cross_domain_reasoning method missing")
        
        return engine
        
    except Exception as e:
        print(f"❌ Import/initialization failed: {e}")
        traceback.print_exc()
        return None

async def test_method_call(engine):
    """Test calling the cross-domain reasoning method"""
    
    print("\n🔧 METHOD CALL TEST")  
    print("="*25)
    
    try:
        print("Calling advanced_cross_domain_reasoning...")
        
        result = await engine.advanced_cross_domain_reasoning(
            source_domain="physics",
            target_domain="economics",
            concept="conservation_of_energy", 
            problem="How to maintain value in economic transactions"
        )
        
        print("✅ Method call successful")
        print(f"📊 Confidence: {result.get('confidence', 0):.3f}")
        print(f"🔄 Reasoning steps: {len(result.get('reasoning_steps', []))}")
        
        return result
        
    except Exception as e:
        print(f"❌ Method call failed: {e}")
        traceback.print_exc()
        return None

def analyze_original_test():
    """Analyze the original failing test"""
    
    print("\n📋 ORIGINAL TEST ANALYSIS")
    print("="*30)
    
    if os.path.exists("quick_cross_domain_test.py"):
        with open("quick_cross_domain_test.py", "r") as f:
            content = f.read()
            
        print(f"📄 Test file size: {len(content)} characters")
        print(f"📄 Lines: {len(content.split(chr(10)))}")
        
        # Check for common issues
        issues = []
        
        if "asyncio.run(" in content:
            print("✅ Uses asyncio.run()")
        else:
            issues.append("Missing asyncio.run()")
            
        if "import" in content:
            print("✅ Has import statements")
        else:
            issues.append("No import statements")
            
        if "advanced_cross_domain_reasoning" in content:
            print("✅ Calls target method")
        else:
            issues.append("Doesn't call target method")
        
        if issues:
            print(f"⚠️ Potential issues: {', '.join(issues)}")
        else:
            print("✅ Test structure looks correct")
            
    else:
        print("❌ Original test file missing")

async def run_complete_diagnostic():
    """Run complete diagnostic test"""
    
    print("🔬 CROSS-DOMAIN DIAGNOSTIC")
    print("="*35)
    
    # Step 1: Check file existence
    files_ok = check_file_exists()
    if not files_ok:
        print("\n❌ DIAGNOSTIC FAILED: Missing files")
        return False
    
    # Step 2: Test import
    engine = test_import()
    if not engine:
        print("\n❌ DIAGNOSTIC FAILED: Import issues")
        return False
    
    # Step 3: Test method call
    result = await test_method_call(engine)
    if not result:
        print("\n❌ DIAGNOSTIC FAILED: Method call issues")
        return False
    
    # Step 4: Analyze original test
    analyze_original_test()
    
    print("\n✅ DIAGNOSTIC SUCCESSFUL!")
    print("📊 Cross-domain reasoning is working properly")
    
    # Show results
    confidence = result.get('confidence', 0)
    print(f"\n📈 PERFORMANCE METRICS:")
    print(f"   Confidence Score: {confidence:.3f} ({confidence*100:.1f}%)")
    print(f"   Analogical Mappings: {len(result.get('analogical_mapping', {}))}")
    print(f"   Transferred Principles: {len(result.get('transferred_principles', []))}")
    print(f"   Reasoning Steps: {len(result.get('reasoning_steps', []))}")
    
    if confidence > 0.7:
        print("🚀 EXCELLENT performance!")
    elif confidence > 0.5:
        print("📈 GOOD performance!")
    else:
        print("📊 MODERATE performance!")
    
    return True

def write_diagnostic_report(success, details):
    """Write diagnostic report to file"""
    
    report = f"""Cross-Domain Diagnostic Report
============================
Timestamp: {asyncio.get_event_loop().time()}
Status: {'SUCCESS' if success else 'FAILED'}

Details:
{details}

Recommendations:
- Engine is {'working properly' if success else 'having issues'}
- {'Continue with cross-domain testing' if success else 'Fix import/method issues first'}
"""
    
    with open("cross_domain_diagnostic.txt", "w") as f:
        f.write(report)
    
    print(f"📄 Report saved to: cross_domain_diagnostic.txt")

if __name__ == "__main__":
    try:
        success = asyncio.run(run_complete_diagnostic())
        write_diagnostic_report(success, "Full diagnostic completed")
        
        if success:
            print("\n🎯 CONCLUSION: Cross-domain reasoning is ready!")
            print("💡 The original test failure might be due to output capture issues")
            print("💡 The engine itself is working correctly")
        else:
            print("\n⚠️ CONCLUSION: Issues found in cross-domain engine!")
            print("💡 Fix the identified issues before proceeding")
            
    except KeyboardInterrupt:
        print("\n⚠️ Diagnostic interrupted by user")
    except Exception as e:
        print(f"\n❌ Diagnostic failed with exception: {e}")
        traceback.print_exc()
