#!/usr/bin/env python3
"""
ASIS Quick Validation Tool
=========================
Focused validation of ASIS components without deep imports.
"""

import os
import ast
import json
from datetime import datetime
from typing import Dict, List, Any

def analyze_asis_workspace():
    """Analyze ASIS workspace for components and functionality"""
    
    print("🔍 ASIS Quick Validation Analysis")
    print("=" * 40)
    
    workspace_files = []
    
    # Scan for Python files in workspace root only
    for file in os.listdir('.'):
        if file.endswith('.py') and not file.startswith('__'):
            workspace_files.append(file)
    
    print(f"📁 Found {len(workspace_files)} Python files in workspace root")
    
    component_analysis = {}
    total_classes = 0
    total_methods = 0
    
    # Analyze each file using AST (safe parsing)
    for file_path in workspace_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            classes = []
            methods = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                    total_classes += 1
                    
                    # Count methods in class
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            methods.append(f"{node.name}.{item.name}")
                            total_methods += 1
            
            if classes:  # Only include files with classes
                component_analysis[file_path] = {
                    'classes': classes,
                    'method_count': len([m for m in methods if file_path.replace('.py', '') in m.split('.')[0]]),
                    'file_size': len(content),
                    'line_count': content.count('\n') + 1
                }
                
        except Exception as e:
            print(f"⚠️ Could not analyze {file_path}: {str(e)[:50]}")
    
    print(f"\n📊 ANALYSIS RESULTS:")
    print(f"Components with classes: {len(component_analysis)}")
    print(f"Total classes found: {total_classes}")
    print(f"Total methods found: {total_methods}")
    
    # Detailed component breakdown
    print(f"\n🔍 COMPONENT DETAILS:")
    for file_name, info in sorted(component_analysis.items(), key=lambda x: len(x[1]['classes']), reverse=True):
        component_name = file_name.replace('.py', '').replace('_', ' ').title()
        print(f"\n✅ {component_name}")
        print(f"   File: {file_name}")
        print(f"   Classes: {len(info['classes'])} ({', '.join(info['classes'][:5])}{'...' if len(info['classes']) > 5 else ''})")
        print(f"   Methods: {info['method_count']}")
        print(f"   Size: {info['line_count']} lines")
    
    # Expected ASIS components check
    expected_core_components = [
        'memory_network', 'learning_engine', 'interest_formation_system',
        'knowledge_integration_system', 'research_system', 'personality_development_system',
        'dialogue_system', 'asis_production_system'
    ]
    
    found_core = []
    missing_core = []
    
    for expected in expected_core_components:
        found = any(expected in file_name.lower() for file_name in component_analysis.keys())
        if found:
            found_core.append(expected)
        else:
            missing_core.append(expected)
    
    print(f"\n🎯 CORE COMPONENT STATUS:")
    print(f"✅ Found: {len(found_core)}/{len(expected_core_components)} core components")
    for component in found_core:
        print(f"   ✅ {component.replace('_', ' ').title()}")
    
    if missing_core:
        print(f"❌ Missing: {len(missing_core)} core components")
        for component in missing_core:
            print(f"   ❌ {component.replace('_', ' ').title()}")
    
    # Calculate implementation score
    implementation_score = (len(found_core) / len(expected_core_components)) * 100
    class_density_score = min(total_classes / 30, 1.0) * 100  # Expected ~30 classes
    method_density_score = min(total_methods / 200, 1.0) * 100  # Expected ~200 methods
    
    overall_score = (implementation_score + class_density_score + method_density_score) / 3
    
    print(f"\n📊 IMPLEMENTATION SCORES:")
    print(f"Core Components: {implementation_score:.1f}%")
    print(f"Class Density: {class_density_score:.1f}% ({total_classes}/30 expected)")
    print(f"Method Density: {method_density_score:.1f}% ({total_methods}/200 expected)")
    print(f"Overall Score: {overall_score:.1f}%")
    
    # Truth assessment
    print(f"\n🎯 TRUTH vs CLAIMS ASSESSMENT:")
    
    if total_classes >= 25:
        print("✅ Claimed '32 classes': REASONABLE (found sufficient classes)")
    elif total_classes >= 15:
        print("⚠️ Claimed '32 classes': PARTIAL (found moderate number)")
    else:
        print("❌ Claimed '32 classes': QUESTIONABLE (found few classes)")
    
    if implementation_score >= 75:
        print("✅ Claimed 'Production Ready': LIKELY")
    elif implementation_score >= 50:
        print("⚠️ Claimed 'Production Ready': QUESTIONABLE")
    else:
        print("❌ Claimed 'Production Ready': UNLIKELY")
    
    if overall_score >= 70:
        print("✅ Overall Assessment: GOOD implementation")
    elif overall_score >= 40:
        print("⚠️ Overall Assessment: MODERATE implementation")
    else:
        print("❌ Overall Assessment: WEAK implementation")
    
    # Create summary report
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_files': len(workspace_files),
        'components_with_classes': len(component_analysis),
        'total_classes': total_classes,
        'total_methods': total_methods,
        'core_components_found': len(found_core),
        'core_components_expected': len(expected_core_components),
        'implementation_score': implementation_score,
        'overall_score': overall_score,
        'component_details': component_analysis
    }
    
    # Save report
    with open('asis_quick_validation.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved: asis_quick_validation.json")
    
    return report

if __name__ == "__main__":
    analyze_asis_workspace()
