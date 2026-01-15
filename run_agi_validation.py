#!/usr/bin/env python3
"""
ASIS AGI Validation Test Runner
==============================
Automated test execution and reporting system
"""

import asyncio
import json
import time
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class AGIValidationTestRunner:
    """Automated test runner for AGI validation"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = None
        self.results_dir = Path("validation_results")
        self.results_dir.mkdir(exist_ok=True)
        
    async def run_validation_suite(self, test_types: List[str] = None) -> Dict:
        """Run complete validation suite or specific tests"""
        print("🧠 ASIS AGI VALIDATION TEST RUNNER")
        print("="*50)
        
        self.start_time = time.time()
        
        if test_types is None:
            test_types = [
                "cross-domain",
                "novel-problem", 
                "self-modification",
                "consciousness",
                "transfer-learning",
                "metacognition",
                "emergent",
                "ethical"
            ]
        
        # Pre-validation system check
        await self.run_system_health_check()
        
        # Run validation tests
        for test_type in test_types:
            print(f"\n🔄 Running {test_type} validation...")
            result = await self.run_single_test(test_type)
            self.test_results[test_type] = result
            
        # Generate comprehensive report
        report = await self.generate_comprehensive_report()
        
        # Save results
        await self.save_results(report)
        
        return report
    
    async def run_system_health_check(self):
        """Check system health before validation"""
        print("\n🔧 System Health Check...")
        
        health_checks = [
            ("Python Environment", self.check_python_environment),
            ("Required Modules", self.check_required_modules),
            ("Database Access", self.check_database_access),
            ("AGI System", self.check_agi_system),
            ("Memory Usage", self.check_memory_usage)
        ]
        
        for check_name, check_func in health_checks:
            try:
                result = await check_func()
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"  {check_name}: {status}")
            except Exception as e:
                print(f"  {check_name}: ❌ ERROR - {e}")
    
    async def check_python_environment(self) -> bool:
        """Check Python environment"""
        return sys.version_info >= (3, 8)
    
    async def check_required_modules(self) -> bool:
        """Check if required modules are available"""
        required_modules = ['asyncio', 'json', 'sqlite3', 'datetime']
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                return False
        return True
    
    async def check_database_access(self) -> bool:
        """Check database write access"""
        try:
            import sqlite3
            conn = sqlite3.connect(":memory:")
            conn.execute("CREATE TABLE test (id INTEGER)")
            conn.close()
            return True
        except Exception:
            return False
    
    async def check_agi_system(self) -> bool:
        """Check if AGI system is accessible"""
        try:
            from asis_agi_validation_system import AGIValidationFramework
            validator = AGIValidationFramework()
            return True
        except Exception:
            return False
    
    async def check_memory_usage(self) -> bool:
        """Check available memory"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            # Require at least 1GB available
            return memory.available > 1_000_000_000
        except ImportError:
            # If psutil not available, assume memory is OK
            return True
    
    async def run_single_test(self, test_type: str) -> Dict:
        """Run a single validation test"""
        test_start = time.time()
        
        try:
            # Import and run the specific test
            from asis_agi_validation_system import run_specific_test
            score = await run_specific_test(test_type)
            
            test_time = time.time() - test_start
            
            return {
                "score": score if score is not None else 0.0,
                "execution_time": test_time,
                "status": "SUCCESS" if score is not None else "FAILED",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            test_time = time.time() - test_start
            
            return {
                "score": 0.0,
                "execution_time": test_time,
                "status": "ERROR",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def generate_comprehensive_report(self) -> Dict:
        """Generate comprehensive validation report"""
        total_time = time.time() - self.start_time
        
        # Calculate overall metrics
        successful_tests = [r for r in self.test_results.values() if r["status"] == "SUCCESS"]
        failed_tests = [r for r in self.test_results.values() if r["status"] in ["FAILED", "ERROR"]]
        
        overall_score = sum(r["score"] for r in successful_tests) / len(self.test_results) if self.test_results else 0.0
        success_rate = len(successful_tests) / len(self.test_results) if self.test_results else 0.0
        
        # Classify AGI level
        agi_classification = self.classify_agi_level(overall_score)
        
        # Generate insights
        insights = self.generate_insights()
        
        return {
            "validation_summary": {
                "overall_score": overall_score,
                "agi_classification": agi_classification,
                "success_rate": success_rate,
                "total_tests": len(self.test_results),
                "successful_tests": len(successful_tests),
                "failed_tests": len(failed_tests),
                "total_execution_time": total_time
            },
            "individual_test_results": self.test_results,
            "insights_and_recommendations": insights,
            "system_information": {
                "python_version": sys.version,
                "platform": sys.platform,
                "timestamp": datetime.now().isoformat()
            }
        }
    
    def classify_agi_level(self, score: float) -> str:
        """Classify AGI level based on validation score"""
        if score >= 0.95:
            return "SUPERINTELLIGENCE_LEVEL_AGI"
        elif score >= 0.90:
            return "ARTIFICIAL_GENERAL_INTELLIGENCE"
        elif score >= 0.85:
            return "ADVANCED_AGI_APPROACHING_SUPERINTELLIGENCE"
        elif score >= 0.80:
            return "ADVANCED_AI_WITH_STRONG_AGI_CHARACTERISTICS"
        elif score >= 0.70:
            return "SOPHISTICATED_AI_APPROACHING_AGI"
        elif score >= 0.60:
            return "ADVANCED_AI_SYSTEM"
        elif score >= 0.50:
            return "CAPABLE_AI_SYSTEM"
        else:
            return "DEVELOPING_AI_SYSTEM"
    
    def generate_insights(self) -> Dict:
        """Generate insights and recommendations"""
        insights = {
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "risk_assessment": "LOW"
        }
        
        # Analyze test results
        for test_name, result in self.test_results.items():
            if result["status"] == "SUCCESS":
                if result["score"] >= 0.8:
                    insights["strengths"].append(f"Excellent {test_name.replace('-', ' ')} capabilities")
                elif result["score"] >= 0.6:
                    insights["strengths"].append(f"Good {test_name.replace('-', ' ')} performance")
                else:
                    insights["weaknesses"].append(f"Below-average {test_name.replace('-', ' ')} performance")
            else:
                insights["weaknesses"].append(f"Failed {test_name.replace('-', ' ')} test")
        
        # Generate recommendations
        successful_tests = [r for r in self.test_results.values() if r["status"] == "SUCCESS"]
        if successful_tests:
            avg_score = sum(r["score"] for r in successful_tests) / len(successful_tests)
            
            if avg_score < 0.5:
                insights["recommendations"].extend([
                    "Focus on fundamental AI capabilities development",
                    "Improve core reasoning and learning systems",
                    "Enhance knowledge representation and processing"
                ])
                insights["risk_assessment"] = "HIGH"
            elif avg_score < 0.7:
                insights["recommendations"].extend([
                    "Strengthen weak capability areas",
                    "Improve integration between different AI components",
                    "Focus on generalization and transfer learning"
                ])
                insights["risk_assessment"] = "MEDIUM"
            elif avg_score < 0.9:
                insights["recommendations"].extend([
                    "Fine-tune advanced capabilities",
                    "Enhance self-modification safety",
                    "Improve consciousness coherence"
                ])
                insights["risk_assessment"] = "LOW"
            else:
                insights["recommendations"].extend([
                    "Monitor for emergent behaviors",
                    "Implement advanced safety measures",
                    "Prepare for post-AGI development"
                ])
                insights["risk_assessment"] = "VERY_LOW"
        
        return insights
    
    async def save_results(self, report: Dict):
        """Save validation results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON report
        json_path = self.results_dir / f"agi_validation_report_{timestamp}.json"
        with open(json_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Save human-readable report
        txt_path = self.results_dir / f"agi_validation_summary_{timestamp}.txt"
        with open(txt_path, 'w') as f:
            f.write(self.format_human_readable_report(report))
        
        print(f"\n💾 Results saved:")
        print(f"  📊 JSON Report: {json_path}")
        print(f"  📝 Summary: {txt_path}")
    
    def format_human_readable_report(self, report: Dict) -> str:
        """Format report for human reading"""
        summary = report["validation_summary"]
        
        output = []
        output.append("ASIS AGI VALIDATION REPORT")
        output.append("=" * 50)
        output.append(f"Generated: {report['system_information']['timestamp']}")
        output.append("")
        
        output.append("OVERALL RESULTS")
        output.append("-" * 20)
        output.append(f"AGI Score: {summary['overall_score']:.4f}/1.0000")
        output.append(f"Classification: {summary['agi_classification']}")
        output.append(f"Success Rate: {summary['success_rate']:.1%}")
        output.append(f"Tests Passed: {summary['successful_tests']}/{summary['total_tests']}")
        output.append(f"Execution Time: {summary['total_execution_time']:.1f} seconds")
        output.append("")
        
        output.append("INDIVIDUAL TEST RESULTS")
        output.append("-" * 30)
        for test_name, result in report["individual_test_results"].items():
            status = result["status"]
            score = result["score"]
            time_taken = result["execution_time"]
            
            output.append(f"{test_name.replace('-', ' ').title():<25}: {status:<8} Score: {score:.3f} Time: {time_taken:.1f}s")
        
        output.append("")
        
        insights = report["insights_and_recommendations"]
        
        if insights["strengths"]:
            output.append("IDENTIFIED STRENGTHS")
            output.append("-" * 20)
            for strength in insights["strengths"]:
                output.append(f"✅ {strength}")
            output.append("")
        
        if insights["weaknesses"]:
            output.append("AREAS FOR IMPROVEMENT")
            output.append("-" * 25)
            for weakness in insights["weaknesses"]:
                output.append(f"⚠️  {weakness}")
            output.append("")
        
        if insights["recommendations"]:
            output.append("RECOMMENDATIONS")
            output.append("-" * 15)
            for i, rec in enumerate(insights["recommendations"], 1):
                output.append(f"{i}. {rec}")
            output.append("")
        
        output.append(f"RISK ASSESSMENT: {insights['risk_assessment']}")
        
        return "\n".join(output)


# CLI interface
async def main():
    """Main CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="ASIS AGI Validation Test Runner")
    parser.add_argument(
        "--tests", 
        nargs="+", 
        help="Specific tests to run (default: all tests)",
        choices=[
            "cross-domain", "novel-problem", "self-modification", 
            "consciousness", "transfer-learning", "metacognition", 
            "emergent", "ethical"
        ]
    )
    parser.add_argument(
        "--output-dir",
        default="validation_results",
        help="Output directory for results (default: validation_results)"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run quick validation (reduced test cases)"
    )
    
    args = parser.parse_args()
    
    # Initialize test runner
    runner = AGIValidationTestRunner()
    if hasattr(args, 'output_dir'):
        runner.results_dir = Path(args.output_dir)
        runner.results_dir.mkdir(exist_ok=True)
    
    # Run validation
    print("🚀 Starting ASIS AGI Validation...")
    
    try:
        report = await runner.run_validation_suite(args.tests)
        
        # Display summary
        summary = report["validation_summary"]
        print(f"\n🎯 VALIDATION COMPLETE!")
        print(f"Overall Score: {summary['overall_score']:.4f}/1.0")
        print(f"Classification: {summary['agi_classification']}")
        print(f"Success Rate: {summary['success_rate']:.1%}")
        print(f"Total Time: {summary['total_execution_time']:.1f} seconds")
        
        if summary['overall_score'] >= 0.9:
            print("🎉 Exceptional AGI performance detected!")
        elif summary['overall_score'] >= 0.8:
            print("🌟 Strong AGI characteristics demonstrated!")
        elif summary['overall_score'] >= 0.7:
            print("📈 Good progress toward AGI capabilities!")
        else:
            print("🔄 Continued development recommended.")
            
    except KeyboardInterrupt:
        print("\n⏹️  Validation interrupted by user")
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
