#!/usr/bin/env python3
"""
ASIS Knowledge Cross-Referencing Test
Tests ASIS ability to connect knowledge from different domains
"""

import sqlite3
import os
import sys
from datetime import datetime
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_interaction_learning():
    """Test interaction-based learning directly"""
    print("💬 Testing Interaction-Based Learning...")
    
    try:
        from asis_advanced_pattern_recognition import ASISAdvancedPatternRecognition
        pattern_system = ASISAdvancedPatternRecognition()
        
        test_interactions = [
            {
                'user_input': 'How does machine learning work in healthcare?',
                'context': 'technical_inquiry',
                'user_expertise': 'intermediate'
            },
            {
                'user_input': 'Explain neural networks for financial predictions',
                'context': 'deep_technical',
                'user_expertise': 'advanced'
            },
            {
                'user_input': 'What are AI applications in climate science?',
                'context': 'research_inquiry',
                'user_expertise': 'beginner'
            }
        ]
        
        patterns_learned = 0
        for i, interaction in enumerate(test_interactions, 1):
            print(f"  [{i}] Processing: '{interaction['user_input'][:50]}...'")
            
            result = pattern_system.analyze_interaction_pattern(
                interaction['user_input'],
                interaction['context'],
                {'expertise_level': interaction['user_expertise']}
            )
            
            if result and result.get('pattern_confidence', 0) > 0.5:
                patterns_learned += 1
                print(f"      ✅ Pattern learned (confidence: {result['pattern_confidence']:.2f})")
            else:
                print(f"      ⚠️  Low confidence: {result.get('pattern_confidence', 0):.2f}")
        
        success = patterns_learned >= 2
        print(f"  📊 Results: {patterns_learned}/3 patterns learned")
        print(f"  {'✅ SUCCESS' if success else '❌ FAILED'}: Interaction learning")
        
        return success
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_knowledge_cross_referencing():
    """Test ASIS ability to connect knowledge across domains"""
    print("🧠 Testing Knowledge Cross-Referencing...")
    
    try:
        from asis_autonomous_research_fixed import ASISAutonomousResearch
        research_system = ASISAutonomousResearch()
        
        # Get current knowledge entries
        conn = sqlite3.connect('asis_autonomous_research_fixed.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT title, content, source_url 
            FROM research_findings 
            ORDER BY extraction_time DESC 
            LIMIT 5
        ''')
        
        findings = cursor.fetchall()
        conn.close()
        
        if len(findings) < 3:
            print("  ⚠️  Not enough research findings for cross-referencing test")
            return False
        
        print(f"  📚 Found {len(findings)} recent findings to cross-reference:")
        
        # Analyze connections between different domains
        connections_found = 0
        domain_keywords = {
            'AI/ML': ['artificial intelligence', 'machine learning', 'neural', 'AI', 'ML'],
            'Healthcare': ['healthcare', 'medical', 'diagnosis', 'health', 'clinical'],
            'Technology': ['technology', 'tech', 'innovation', 'digital', 'software'],
            'Finance': ['financial', 'fintech', 'blockchain', 'cryptocurrency', 'payment'],
            'Climate': ['climate', 'renewable', 'energy', 'sustainability', 'environment'],
            'Space': ['space', 'satellite', 'mars', 'exploration', 'NASA']
        }
        
        # Check for cross-domain connections
        for i, finding1 in enumerate(findings):
            for j, finding2 in enumerate(findings[i+1:], i+1):
                
                # Determine domains of each finding
                domain1 = None
                domain2 = None
                
                content1 = (finding1[0] + ' ' + finding1[1]).lower()
                content2 = (finding2[0] + ' ' + finding2[1]).lower()
                
                for domain, keywords in domain_keywords.items():
                    if any(keyword in content1 for keyword in keywords):
                        domain1 = domain
                    if any(keyword in content2 for keyword in keywords):
                        domain2 = domain
                
                if domain1 and domain2 and domain1 != domain2:
                    connections_found += 1
                    print(f"    🔗 Connection: {domain1} ↔ {domain2}")
                    print(f"       • {finding1[0][:40]}...")
                    print(f"       • {finding2[0][:40]}...")
        
        # Test knowledge synthesis
        knowledge_summary = research_system.get_knowledge_summary()
        categories = knowledge_summary.get('categories_explored', [])
        
        cross_domain_score = 0
        if len(categories) >= 3:
            cross_domain_score += 0.4
        if connections_found >= 2:
            cross_domain_score += 0.4
        if knowledge_summary.get('total_entries', 0) >= 5:
            cross_domain_score += 0.2
        
        success = cross_domain_score >= 0.6
        
        print(f"  📊 Cross-Referencing Results:")
        print(f"    • Knowledge categories: {len(categories)}")
        print(f"    • Cross-domain connections: {connections_found}")
        print(f"    • Total knowledge entries: {knowledge_summary.get('total_entries', 0)}")
        print(f"    • Cross-referencing score: {cross_domain_score:.1f}/1.0")
        print(f"  {'✅ SUCCESS' if success else '❌ NEEDS WORK'}: Knowledge cross-referencing")
        
        return success
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    """Run final knowledge expansion tests"""
    print("🔬 FINAL ASIS KNOWLEDGE EXPANSION VERIFICATION")
    print("=" * 55)
    
    results = {}
    
    # Test 1: Interaction Learning (fixed)
    results['interaction_learning'] = test_interaction_learning()
    print()
    
    # Test 2: Knowledge Cross-Referencing
    results['knowledge_cross_referencing'] = test_knowledge_cross_referencing()
    print()
    
    # Summary
    passed_tests = sum(results.values())
    total_tests = len(results)
    
    print("📊 FINAL TEST RESULTS:")
    print("=" * 25)
    print(f"✅ Passed: {passed_tests}/{total_tests}")
    print(f"📈 Success Rate: {passed_tests/total_tests:.1%}")
    
    if passed_tests == total_tests:
        print("🎉 PERFECT: All knowledge expansion capabilities verified!")
    elif passed_tests >= total_tests * 0.5:
        print("✅ GOOD: Strong knowledge expansion capabilities confirmed!")
    else:
        print("⚠️  PARTIAL: Some knowledge expansion needs improvement")
    
    # Save results
    final_results = {
        'test_results': results,
        'passed_tests': passed_tests,
        'total_tests': total_tests,
        'success_rate': passed_tests/total_tests,
        'timestamp': datetime.now().isoformat()
    }
    
    with open('final_knowledge_test_results.json', 'w') as f:
        json.dump(final_results, f, indent=2)
    
    print(f"\n📄 Results saved to: final_knowledge_test_results.json")
    
    return results

if __name__ == "__main__":
    main()
