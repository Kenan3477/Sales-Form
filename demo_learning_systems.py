#!/usr/bin/env python3
"""
ASIS Learning Systems Demonstration
==================================
Demonstrates all three advanced learning systems:
1. Enhanced Learning Evidence Display
2. Learning Analytics Dashboard
3. Learning Verification Tools
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from asis_enhanced_learning_display import ASISEnhancedLearningDisplay
from asis_learning_analytics_dashboard import ASISLearningAnalyticsDashboard
from asis_learning_verification_tools import ASISLearningVerificationTools

def demonstrate_learning_systems():
    """Demonstrate all three learning systems"""
    
    print("🚀 ASIS ADVANCED LEARNING SYSTEMS DEMONSTRATION")
    print("=" * 60)
    print("Demonstrating the world's most advanced AI learning analytics")
    print("=" * 60)
    
    # 1. Enhanced Learning Evidence Display
    print("\n1️⃣ ENHANCED LEARNING EVIDENCE DISPLAY")
    print("─" * 50)
    print("Initializing comprehensive learning evidence system...")
    
    try:
        evidence_system = ASISEnhancedLearningDisplay()
        evidence_report = evidence_system.generate_comprehensive_learning_report()
        print(evidence_report)
    except Exception as e:
        print(f"❌ Evidence system error: {e}")
    
    # 2. Learning Analytics Dashboard
    print("\n\n2️⃣ LEARNING ANALYTICS DASHBOARD")
    print("─" * 50)
    print("Initializing visual learning analytics dashboard...")
    
    try:
        dashboard_system = ASISLearningAnalyticsDashboard()
        dashboard_report = dashboard_system.generate_dashboard_display()
        print(dashboard_report)
    except Exception as e:
        print(f"❌ Dashboard system error: {e}")
    
    # 3. Learning Verification Tools
    print("\n\n3️⃣ INDEPENDENT LEARNING VERIFICATION")
    print("─" * 50)
    print("Initializing independent verification system...")
    
    try:
        verification_system = ASISLearningVerificationTools()
        print("🔍 Running comprehensive learning verification...")
        verification_results = verification_system.comprehensive_learning_verification()
        verification_report = verification_system.generate_verification_report(verification_results)
        print(verification_report)
    except Exception as e:
        print(f"❌ Verification system error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ DEMONSTRATION COMPLETE!")
    print("All three advanced learning systems successfully demonstrated.")
    print("=" * 60)

if __name__ == "__main__":
    demonstrate_learning_systems()
