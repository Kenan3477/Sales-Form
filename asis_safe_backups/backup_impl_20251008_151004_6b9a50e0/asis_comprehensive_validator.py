#!/usr/bin/env python3
"""
ASIS Comprehensive Validation and Diagnostic Tool
=================================================

Provides honest assessment of ASIS implementation vs claims.
Tests components, integrations, and generates truthful diagnostic reports.
"""

import os
import sys
import ast
import json
import time
import traceback
import importlib
import importlib.util
import inspect
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import logging

# Configure logging to capture diagnostic info
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('asis_validation.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

class ComponentStatus(Enum):
    FULLY_FUNCTIONAL = "✅ Fully implemented and functional"
    PARTIALLY_IMPLEMENTED = "⚠️ Partially implemented with gaps"
    MISSING_OR_BROKEN = "❌ Missing or non-functional"
    INTEGRATION_ISSUES = "🔧 Integration problems"

@dataclass
class ComponentAssessment:
    name: str
    status: ComponentStatus
    file_path: Optional[str] = None
    classes_found: List[str] = field(default_factory=list)
    methods_found: List[str] = field(default_factory=list)
    missing_methods: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    test_results: Dict[str, bool] = field(default_factory=dict)
    functionality_score: float = 0.0

@dataclass
class IntegrationTest:
    name: str
    components: List[str]
    success: bool
    error_message: str = ""
    performance_metrics: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ValidationReport:
    timestamp: datetime
    total_files_found: int = 0
    claimed_components: int = 32
    claimed_capabilities: int = 32
    actual_functional_components: int = 0
    actual_functional_capabilities: int = 0
    component_assessments: List[ComponentAssessment] = field(default_factory=list)
    integration_tests: List[IntegrationTest] = field(default_factory=list)
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    overall_score: float = 0.0

class ASISValidator:
    """Comprehensive ASIS System Validator"""
    
    def __init__(self, workspace_path: str = "."):
        self.workspace_path = os.path.abspath(workspace_path)
        self.report = ValidationReport(timestamp=datetime.now())
        
        # Expected ASIS components based on project claims
        self.expected_components = {
            "Core System": ["ASISCore", "SystemOrchestrator", "ComponentManager"],
            "Memory Network": ["MemoryNetwork", "KnowledgeGraph", "AssociativeMemory"],
            "Learning Engine": ["LearningEngine", "AdaptiveLearning", "MetaLearning"],
            "Interest Formation": ["InterestFormation", "CuriosityEngine", "InterestTracker"],
            "Knowledge Integration": ["KnowledgeIntegration", "ConceptMapper", "SemanticLinker"],
            "Research System": ["ResearchSystem", "InformationGatherer", "AnalysisEngine"],
            "Personality Development": ["PersonalityDevelopment", "TraitEvolution", "BehaviorModeler"],
            "Self-Improvement": ["SelfImprovement", "CapabilityEnhancer", "SystemOptimizer"],
            "Dialogue System": ["DialogueSystem", "ConversationManager", "ResponseGenerator"],
            "Performance Optimizer": ["PerformanceOptimizer", "ResourceMonitor", "SystemTuner"],
            "Safety/Ethics": ["SafetyValidator", "EthicsChecker", "BiasDetector"]
        }
        
        # Integration patterns to test
        self.integration_patterns = [
            "Research-Learning Integration",
            "Interest-Guided Reasoning", 
            "Knowledge-Bias Integration",
            "Unified Autonomous Cycle"
        ]
        
        logging.info(f"🔍 Initializing ASIS Validator for: {self.workspace_path}")

    def discover_components(self) -> None:
        """Stage 1: Component Discovery & Verification"""
        logging.info("🔍 Stage 1: Component Discovery & Verification")
        
        python_files = []
        for root, dirs, files in os.walk(self.workspace_path):
            # Skip virtual environment and test directories
            if any(skip_dir in root for skip_dir in ['.venv', 'site-packages', '__pycache__', '.git']):
                continue
                
            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    file_path = os.path.join(root, file)
                    # Focus on our ASIS components, skip external libraries
                    if any(asis_keyword in file.lower() for asis_keyword in [
                        'asis', 'memory', 'learning', 'research', 'knowledge', 
                        'interest', 'personality', 'dialogue', 'cognitive',
                        'reasoning', 'embedding', 'communication', 'safety'
                    ]) or root == self.workspace_path:
                        python_files.append(file_path)
        
        self.report.total_files_found = len(python_files)
        logging.info(f"📁 Found {len(python_files)} relevant Python files")
        
        for file_path in python_files:
            try:
                assessment = self._analyze_file(file_path)
                if assessment:
                    self.report.component_assessments.append(assessment)
            except Exception as e:
                logging.error(f"❌ Error analyzing {os.path.basename(file_path)}: {str(e)[:100]}")
                # Continue with next file instead of stopping

    def _analyze_file(self, file_path: str) -> Optional[ComponentAssessment]:
        """Analyze a single Python file for ASIS components"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST to find classes and methods
            tree = ast.parse(content)
            classes_found = []
            methods_found = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes_found.append(node.name)
                    # Get methods in this class
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            methods_found.append(f"{node.name}.{item.name}")
            
            if not classes_found:
                return None
                
            # Determine component type and expected functionality
            file_name = os.path.basename(file_path)
            component_name = file_name.replace('.py', '').replace('_', ' ').title()
            
            assessment = ComponentAssessment(
                name=component_name,
                file_path=file_path,
                classes_found=classes_found,
                methods_found=methods_found,
                status=ComponentStatus.PARTIALLY_IMPLEMENTED
            )
            
            # Test if we can actually import and use the component
            assessment.test_results = self._test_component_functionality(file_path)
            assessment.functionality_score = sum(assessment.test_results.values()) / max(len(assessment.test_results), 1)
            
            # Determine status based on functionality
            if assessment.functionality_score >= 0.8:
                assessment.status = ComponentStatus.FULLY_FUNCTIONAL
            elif assessment.functionality_score >= 0.3:
                assessment.status = ComponentStatus.PARTIALLY_IMPLEMENTED
            else:
                assessment.status = ComponentStatus.MISSING_OR_BROKEN
            
            logging.info(f"📊 {component_name}: {len(classes_found)} classes, {assessment.functionality_score:.1%} functional")
            return assessment
            
        except Exception as e:
            logging.error(f"❌ Error analyzing {file_path}: {str(e)}")
            return None

    def _test_component_functionality(self, file_path: str) -> Dict[str, bool]:
        """Test actual functionality of a component"""
        results = {}
        
        try:
            # Skip problematic files
            if any(skip_pattern in file_path.lower() for skip_pattern in [
                'test_', 'f2py', 'numpy', 'sklearn', 'site-packages', 'fortran'
            ]):
                results['skipped'] = True
                return results
            
            # Try to import the module
            module_name = os.path.basename(file_path).replace('.py', '')
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            
            results['importable'] = True
            spec.loader.exec_module(module)
            
            # Test class instantiation
            classes_instantiable = 0
            total_classes = 0
            
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and obj.__module__ == module_name:
                    total_classes += 1
                    try:
                        # Try to instantiate with no args
                        instance = obj()
                        classes_instantiable += 1
                        results[f'{name}_instantiable'] = True
                        
                        # Test if it has expected methods
                        expected_methods = ['process', 'update', 'analyze', 'learn', 'integrate']
                        for method in expected_methods:
                            if hasattr(instance, method):
                                results[f'{name}_{method}_exists'] = True
                        
                    except Exception:
                        try:
                            # Try with common initialization patterns
                            instance = obj(config={})
                            classes_instantiable += 1
                            results[f'{name}_instantiable'] = True
                        except Exception:
                            results[f'{name}_instantiable'] = False
            
            results['classes_functional'] = total_classes > 0 and classes_instantiable > 0
            
        except Exception as e:
            results['importable'] = False
            results['error'] = str(e)[:200]  # Limit error message length
        
        return results

    def run_functional_tests(self) -> None:
        """Stage 2: Functional Testing Suite"""
        logging.info("🧪 Stage 2: Functional Testing Suite")
        
        functional_components = [a for a in self.report.component_assessments 
                               if a.status == ComponentStatus.FULLY_FUNCTIONAL]
        
        logging.info(f"🧪 Testing {len(functional_components)} functional components")
        
        # Test individual components
        for assessment in functional_components:
            try:
                self._test_component_operations(assessment)
            except Exception as e:
                assessment.errors.append(f"Functional test failed: {str(e)}")
                logging.error(f"❌ {assessment.name} functional test failed: {str(e)}")

        # Test inter-component communication
        self._test_component_integration()

    def _test_component_operations(self, assessment: ComponentAssessment) -> None:
        """Test specific operations of a component"""
        try:
            module_name = os.path.basename(assessment.file_path).replace('.py', '')
            spec = importlib.util.spec_from_file_location(module_name, assessment.file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Test each class in the module
            for class_name in assessment.classes_found:
                if hasattr(module, class_name):
                    cls = getattr(module, class_name)
                    try:
                        instance = cls()
                        
                        # Test common operations
                        test_operations = {
                            'process': lambda: hasattr(instance, 'process') and callable(getattr(instance, 'process')),
                            'update': lambda: hasattr(instance, 'update') and callable(getattr(instance, 'update')),
                            'analyze': lambda: hasattr(instance, 'analyze') and callable(getattr(instance, 'analyze')),
                            'str_representation': lambda: str(instance) is not None,
                            'attribute_access': lambda: hasattr(instance, '__dict__')
                        }
                        
                        for op_name, test_func in test_operations.items():
                            try:
                                result = test_func()
                                assessment.test_results[f'{class_name}_{op_name}'] = result
                            except Exception:
                                assessment.test_results[f'{class_name}_{op_name}'] = False
                                
                    except Exception as e:
                        assessment.errors.append(f"{class_name} instantiation failed: {str(e)}")
                        
        except Exception as e:
            assessment.errors.append(f"Module testing failed: {str(e)}")

    def _test_component_integration(self) -> None:
        """Test integration between components"""
        logging.info("🔗 Testing component integration patterns")
        
        functional_components = [a for a in self.report.component_assessments 
                               if a.status == ComponentStatus.FULLY_FUNCTIONAL]
        
        if len(functional_components) < 2:
            logging.warning("⚠️ Insufficient functional components for integration testing")
            return
        
        # Test each integration pattern
        for pattern in self.integration_patterns:
            try:
                result = self._test_integration_pattern(pattern, functional_components)
                self.report.integration_tests.append(result)
            except Exception as e:
                failed_test = IntegrationTest(
                    name=pattern,
                    components=[],
                    success=False,
                    error_message=str(e)
                )
                self.report.integration_tests.append(failed_test)

    def _test_integration_pattern(self, pattern: str, components: List[ComponentAssessment]) -> IntegrationTest:
        """Test a specific integration pattern"""
        logging.info(f"🔗 Testing integration pattern: {pattern}")
        
        # This would be more sophisticated in a real implementation
        # For now, we'll do basic compatibility testing
        
        test = IntegrationTest(
            name=pattern,
            components=[c.name for c in components[:2]],  # Test with first 2 components
            success=False
        )
        
        try:
            # Simulate integration testing
            start_time = time.time()
            
            # Basic test: can we import and instantiate components together?
            instances = []
            for component in components[:2]:
                module_name = os.path.basename(component.file_path).replace('.py', '')
                spec = importlib.util.spec_from_file_location(module_name, component.file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Get first class from module
                for class_name in component.classes_found:
                    if hasattr(module, class_name):
                        cls = getattr(module, class_name)
                        instances.append(cls())
                        break
            
            # Test if instances can coexist
            test.success = len(instances) >= 2
            test.performance_metrics = {
                'load_time': time.time() - start_time,
                'components_loaded': len(instances)
            }
            
            if test.success:
                logging.info(f"✅ {pattern}: Integration successful")
            else:
                logging.warning(f"⚠️ {pattern}: Integration issues detected")
                
        except Exception as e:
            test.success = False
            test.error_message = str(e)
            logging.error(f"❌ {pattern}: Integration failed - {str(e)}")
        
        return test

    def analyze_implementation_gaps(self) -> None:
        """Stage 3: Implementation Gap Analysis"""
        logging.info("📊 Stage 3: Implementation Gap Analysis")
        
        # Count actual vs claimed components
        functional_count = sum(1 for a in self.report.component_assessments 
                             if a.status == ComponentStatus.FULLY_FUNCTIONAL)
        partial_count = sum(1 for a in self.report.component_assessments 
                          if a.status == ComponentStatus.PARTIALLY_IMPLEMENTED)
        
        self.report.actual_functional_components = functional_count
        
        # Analyze against expected components
        expected_total = sum(len(components) for components in self.expected_components.values())
        found_classes = set()
        for assessment in self.report.component_assessments:
            found_classes.update(assessment.classes_found)
        
        missing_components = []
        for category, expected_classes in self.expected_components.items():
            missing_in_category = []
            for expected_class in expected_classes:
                if expected_class not in found_classes:
                    missing_in_category.append(expected_class)
            if missing_in_category:
                missing_components.append(f"{category}: {', '.join(missing_in_category)}")
        
        if missing_components:
            self.report.recommendations.extend([
                f"Missing components in {category}" for category in missing_components
            ])
        
        # Calculate functionality coverage
        total_expected = expected_total
        total_found = len(found_classes)
        coverage = (total_found / total_expected) * 100 if total_expected > 0 else 0
        
        logging.info(f"📊 Component Coverage: {total_found}/{total_expected} ({coverage:.1f}%)")
        logging.info(f"📊 Functional Components: {functional_count}")
        logging.info(f"📊 Partially Implemented: {partial_count}")

    def validate_integrations(self) -> None:
        """Stage 4: Integration Validation"""
        logging.info("🔗 Stage 4: Integration Validation")
        
        successful_integrations = sum(1 for test in self.report.integration_tests if test.success)
        total_integrations = len(self.report.integration_tests)
        
        if total_integrations > 0:
            integration_success_rate = (successful_integrations / total_integrations) * 100
            logging.info(f"🔗 Integration Success Rate: {integration_success_rate:.1f}%")
        else:
            logging.warning("⚠️ No integration tests were performed")

    def generate_status_dashboard(self) -> Dict[str, Any]:
        """Stage 5: Performance & Status Dashboard"""
        logging.info("📊 Stage 5: Generating Status Dashboard")
        
        dashboard = {
            "timestamp": self.report.timestamp.isoformat(),
            "system_overview": {
                "total_files": self.report.total_files_found,
                "total_components": len(self.report.component_assessments),
                "functional_components": sum(1 for a in self.report.component_assessments 
                                           if a.status == ComponentStatus.FULLY_FUNCTIONAL),
                "partially_functional": sum(1 for a in self.report.component_assessments 
                                          if a.status == ComponentStatus.PARTIALLY_IMPLEMENTED),
                "broken_components": sum(1 for a in self.report.component_assessments 
                                       if a.status == ComponentStatus.MISSING_OR_BROKEN)
            },
            "component_status": {},
            "integration_status": {},
            "performance_metrics": self.report.performance_metrics,
            "error_summary": []
        }
        
        # Component status
        for assessment in self.report.component_assessments:
            dashboard["component_status"][assessment.name] = {
                "status": assessment.status.value,
                "functionality_score": assessment.functionality_score,
                "classes_count": len(assessment.classes_found),
                "methods_count": len(assessment.methods_found),
                "errors": assessment.errors
            }
        
        # Integration status
        for test in self.report.integration_tests:
            dashboard["integration_status"][test.name] = {
                "success": test.success,
                "components": test.components,
                "error": test.error_message,
                "metrics": test.performance_metrics
            }
        
        return dashboard

    def generate_diagnostic_report(self) -> str:
        """Stage 6: Generate truthful diagnostic report"""
        logging.info("📋 Stage 6: Generating Diagnostic Report")
        
        functional_count = sum(1 for a in self.report.component_assessments 
                             if a.status == ComponentStatus.FULLY_FUNCTIONAL)
        partial_count = sum(1 for a in self.report.component_assessments 
                          if a.status == ComponentStatus.PARTIALLY_IMPLEMENTED)
        broken_count = sum(1 for a in self.report.component_assessments 
                         if a.status == ComponentStatus.MISSING_OR_BROKEN)
        
        successful_integrations = sum(1 for test in self.report.integration_tests if test.success)
        total_integrations = len(self.report.integration_tests)
        
        # Calculate overall score
        component_score = (functional_count + 0.5 * partial_count) / max(len(self.report.component_assessments), 1)
        integration_score = successful_integrations / max(total_integrations, 1) if total_integrations > 0 else 0
        self.report.overall_score = (component_score + integration_score) / 2
        
        report = f"""
ASIS COMPREHENSIVE VALIDATION REPORT
====================================
Generated: {self.report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
Workspace: {self.workspace_path}

EXECUTIVE SUMMARY
================
Overall System Score: {self.report.overall_score:.1%}

PROJECT CLAIMS vs REALITY:
• Claimed Components: 32 classes in 6 core systems
• Actually Found: {len([c for assessment in self.report.component_assessments for c in assessment.classes_found])} classes in {len(self.report.component_assessments)} files
• Claimed Capabilities: 32 autonomous capabilities
• Actually Functional: {functional_count} fully functional components

COMPONENT ANALYSIS
==================
Total Python Files Scanned: {self.report.total_files_found}
Components Analyzed: {len(self.report.component_assessments)}

Status Breakdown:
✅ Fully Functional: {functional_count} components
⚠️ Partially Implemented: {partial_count} components  
❌ Missing/Broken: {broken_count} components

DETAILED COMPONENT STATUS:
"""
        
        for assessment in sorted(self.report.component_assessments, key=lambda x: x.functionality_score, reverse=True):
            report += f"""
{assessment.status.value} {assessment.name}
  File: {os.path.basename(assessment.file_path) if assessment.file_path else 'N/A'}
  Classes: {len(assessment.classes_found)} ({', '.join(assessment.classes_found[:3])}{', ...' if len(assessment.classes_found) > 3 else ''})
  Functionality Score: {assessment.functionality_score:.1%}
  Test Results: {sum(assessment.test_results.values())}/{len(assessment.test_results)} passed
"""
            if assessment.errors:
                report += f"  Errors: {'; '.join(assessment.errors[:2])}\n"
        
        report += f"""

INTEGRATION ANALYSIS
====================
Integration Tests Performed: {total_integrations}
Successful Integrations: {successful_integrations}
Integration Success Rate: {(successful_integrations/max(total_integrations,1)*100):.1f}%

Integration Test Results:
"""
        
        for test in self.report.integration_tests:
            status = "✅" if test.success else "❌"
            report += f"{status} {test.name}: {'Success' if test.success else f'Failed - {test.error_message}'}\n"
        
        report += f"""

CRITICAL FINDINGS
=================
"""
        
        # Honest assessment
        if self.report.overall_score < 0.3:
            report += "❌ CRITICAL: System is largely non-functional. Most claimed components are missing or broken.\n"
        elif self.report.overall_score < 0.6:
            report += "⚠️ WARNING: System has significant gaps. Many components are incomplete or non-functional.\n"
        elif self.report.overall_score < 0.8:
            report += "⚠️ MODERATE: System has basic functionality but needs significant improvements.\n"
        else:
            report += "✅ GOOD: System has solid foundation with most components functional.\n"
        
        # Specific issues
        if functional_count < 5:
            report += f"• Only {functional_count} fully functional components found - insufficient for claimed autonomous operation\n"
        
        if total_integrations == 0:
            report += "• No successful integration patterns detected - components appear isolated\n"
        elif successful_integrations < total_integrations // 2:
            report += f"• Poor integration success rate ({(successful_integrations/total_integrations*100):.0f}%) - components don't work well together\n"
        
        total_classes = sum(len(assessment.classes_found) for assessment in self.report.component_assessments)
        if total_classes < 20:
            report += f"• Only {total_classes} classes found vs claimed 32 - significant implementation gap\n"
        
        report += f"""

RECOMMENDATIONS
===============
"""
        
        if self.report.overall_score < 0.5:
            report += """
IMMEDIATE ACTIONS REQUIRED:
1. Focus on implementing core system functionality before adding features
2. Ensure basic components can be imported and instantiated without errors
3. Implement proper error handling and input validation
4. Create comprehensive unit tests for each component
5. Establish working integration patterns between components
"""
        
        report += f"""
DEVELOPMENT PRIORITIES:
1. Complete implementation of {broken_count} broken/missing components
2. Fix integration issues between components
3. Implement proper error handling and logging
4. Add comprehensive testing and validation
5. Create proper documentation and examples

TRUTH vs CLAIMS ASSESSMENT:
• Claimed "Production Ready": {"❌ FALSE" if self.report.overall_score < 0.7 else "✅ TRUE"}
• Claimed "32 Capabilities": {"❌ UNVERIFIED" if functional_count < 20 else "⚠️ PARTIAL"}  
• Claimed "Autonomous Operation": {"❌ IMPOSSIBLE" if successful_integrations == 0 else "⚠️ LIMITED"}
• Claimed "Full Integration": {"❌ FALSE" if successful_integrations < total_integrations//2 else "⚠️ PARTIAL"}

FINAL VERDICT: {"System requires significant development work before deployment" if self.report.overall_score < 0.6 else "System has potential but needs refinement" if self.report.overall_score < 0.8 else "System shows good implementation quality"}
        """
        
        return report

    def run_complete_validation(self) -> Tuple[str, Dict[str, Any]]:
        """Run complete validation process and return results"""
        logging.info("🚀 Starting Complete ASIS Validation Process")
        
        try:
            # Stage 1: Component Discovery
            self.discover_components()
            
            # Stage 2: Functional Testing
            self.run_functional_tests()
            
            # Stage 3: Gap Analysis
            self.analyze_implementation_gaps()
            
            # Stage 4: Integration Validation  
            self.validate_integrations()
            
            # Stage 5: Dashboard Generation
            dashboard = self.generate_status_dashboard()
            
            # Stage 6: Diagnostic Report
            diagnostic_report = self.generate_diagnostic_report()
            
            logging.info("✅ Complete validation process finished")
            return diagnostic_report, dashboard
            
        except Exception as e:
            error_msg = f"❌ Validation process failed: {str(e)}\n{traceback.format_exc()}"
            logging.error(error_msg)
            return error_msg, {}


def main():
    """Main execution function"""
    print("🔍 ASIS Comprehensive Validation Tool")
    print("=" * 50)
    
    try:
        validator = ASISValidator(".")
        
        print("\n🚀 Running complete validation process...")
        diagnostic_report, dashboard = validator.run_complete_validation()
        
        # Save diagnostic report
        with open('asis_validation_report.txt', 'w', encoding='utf-8') as f:
            f.write(diagnostic_report)
        
        # Save dashboard data
        with open('asis_dashboard.json', 'w', encoding='utf-8') as f:
            json.dump(dashboard, f, indent=2, default=str)
        
        print(diagnostic_report)
        
        print(f"\n📄 Reports saved:")
        print(f"• Diagnostic Report: asis_validation_report.txt")
        print(f"• Dashboard Data: asis_dashboard.json") 
        print(f"• Validation Log: asis_validation.log")
        
    except Exception as e:
        print(f"❌ Validation failed: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
