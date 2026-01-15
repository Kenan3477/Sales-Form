#!/usr/bin/env python3
"""
Advanced ASIS Knowledge Expansion Test Suite
Tests multiple types of learning and knowledge expansion scenarios
"""

import sqlite3
import os
import sys
import time
import json
from datetime import datetime
from typing import Dict, List, Any

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class AdvancedKnowledgeExpansionTester:
    def __init__(self):
        self.research_db = 'asis_autonomous_research_fixed.db'
        self.meta_learning_db = 'asis_adaptive_meta_learning.db'
        self.memory_db = 'asis_complete_memory.db'
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: Dict):
        """Log test results"""
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })
        
    def get_database_stats(self, db_path: str) -> Dict:
        """Get current database statistics"""
        if not os.path.exists(db_path):
            return {'exists': False}
            
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            stats = {'exists': True, 'size': os.path.getsize(db_path)}
            
            # Get table counts
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            for table in tables:
                try:
                    cursor.execute(f'SELECT COUNT(*) FROM {table}')
                    stats[f'{table}_count'] = cursor.fetchone()[0]
                except:
                    stats[f'{table}_count'] = 0
                    
            conn.close()
            return stats
            
        except Exception as e:
            return {'exists': True, 'error': str(e)}
    
    def test_technical_research(self) -> bool:
        """Test ASIS researching technical topics"""
        print("🔬 Testing Technical Research Capabilities...")
        
        try:
            from asis_autonomous_research_fixed import ASISAutonomousResearch
            research_system = ASISAutonomousResearch()
            
            # Get initial state
            initial_stats = self.get_database_stats(self.research_db)
            initial_findings = initial_stats.get('research_findings_count', 0)
            
            # Research technical topics
            technical_topics = [
                ("Quantum Computing", "quantum computing algorithms qubits"),
                ("Neural Networks", "deep learning neural networks transformers"),
                ("Blockchain Technology", "blockchain cryptocurrency distributed ledger")
            ]
            
            successful_research = 0
            for topic, search_terms in technical_topics:
                print(f"  📚 Researching: {topic}")
                result = research_system.force_research_session(topic, search_terms)
                
                if result.get('status') == 'completed':
                    successful_research += 1
                    
                time.sleep(1)  # Brief pause between research sessions
            
            # Check final state
            final_stats = self.get_database_stats(self.research_db)
            final_findings = final_stats.get('research_findings_count', 0)
            
            new_findings = final_findings - initial_findings
            success = new_findings >= 2  # At least 2 successful research sessions
            
            details = {
                'topics_researched': len(technical_topics),
                'successful_sessions': successful_research,
                'new_findings': new_findings,
                'initial_findings': initial_findings,
                'final_findings': final_findings
            }
            
            self.log_test('technical_research', success, details)
            print(f"  ✅ Technical Research: {new_findings} new findings added")
            return success
            
        except Exception as e:
            print(f"  ❌ Technical Research Error: {e}")
            self.log_test('technical_research', False, {'error': str(e)})
            return False
    
    def test_cross_domain_learning(self) -> bool:
        """Test ASIS learning across different domains"""
        print("🌐 Testing Cross-Domain Learning...")
        
        try:
            from asis_autonomous_research_fixed import ASISAutonomousResearch
            research_system = ASISAutonomousResearch()
            
            # Research diverse domains
            domains = [
                ("Healthcare AI", "artificial intelligence healthcare medical diagnosis"),
                ("Financial Technology", "fintech blockchain digital payments"),
                ("Climate Science", "climate change renewable energy sustainability"),
                ("Space Technology", "space exploration satellites mars missions")
            ]
            
            domain_results = {}
            for domain, search_terms in domains:
                print(f"  🎯 Domain: {domain}")
                result = research_system.force_research_session(domain, search_terms)
                domain_results[domain] = result.get('status') == 'completed'
                time.sleep(1)
            
            successful_domains = sum(domain_results.values())
            success = successful_domains >= 3
            
            details = {
                'domains_tested': len(domains),
                'successful_domains': successful_domains,
                'domain_results': domain_results
            }
            
            self.log_test('cross_domain_learning', success, details)
            print(f"  ✅ Cross-Domain Learning: {successful_domains}/{len(domains)} domains successful")
            return success
            
        except Exception as e:
            print(f"  ❌ Cross-Domain Learning Error: {e}")
            self.log_test('cross_domain_learning', False, {'error': str(e)})
            return False
    
    def test_interaction_based_learning(self) -> bool:
        """Test if ASIS learns from interactions"""
        print("💬 Testing Interaction-Based Learning...")
        
        try:
            # Check if pattern recognition system exists
            pattern_file = 'asis_advanced_pattern_recognition.py'
            if not os.path.exists(pattern_file):
                print("  ⚠️  Pattern recognition system not found")
                return False
                
            from asis_advanced_pattern_recognition import ASISAdvancedPatternRecognition
            pattern_system = ASISAdvancedPatternRecognition()
            
            # Simulate user interactions
            test_interactions = [
                {
                    'user_input': 'How does machine learning work?',
                    'context': 'technical_inquiry',
                    'user_expertise': 'beginner'
                },
                {
                    'user_input': 'Explain neural networks in detail',
                    'context': 'deep_technical',
                    'user_expertise': 'advanced'
                },
                {
                    'user_input': 'What are the latest AI developments?',
                    'context': 'research_inquiry',
                    'user_expertise': 'intermediate'
                }
            ]
            
            patterns_learned = 0
            for interaction in test_interactions:
                try:
                    # Process interaction pattern
                    result = pattern_system.analyze_interaction_pattern(
                        interaction['user_input'],
                        interaction['context'],
                        {'expertise_level': interaction['user_expertise']}
                    )
                    
                    if result and result.get('pattern_confidence', 0) > 0.5:
                        patterns_learned += 1
                        
                except Exception as e:
                    print(f"    ⚠️  Interaction processing error: {e}")
            
            success = patterns_learned >= 2
            
            details = {
                'interactions_tested': len(test_interactions),
                'patterns_learned': patterns_learned,
                'learning_rate': patterns_learned / len(test_interactions)
            }
            
            self.log_test('interaction_learning', success, details)
            print(f"  ✅ Interaction Learning: {patterns_learned} patterns learned")
            return success
            
        except Exception as e:
            print(f"  ❌ Interaction Learning Error: {e}")
            self.log_test('interaction_learning', False, {'error': str(e)})
            return False
    
    def test_knowledge_synthesis(self) -> bool:
        """Test ASIS ability to synthesize knowledge from multiple sources"""
        print("🧠 Testing Knowledge Synthesis...")
        
        try:
            from asis_autonomous_research_fixed import ASISAutonomousResearch
            research_system = ASISAutonomousResearch()
            
            # Get knowledge summary
            knowledge_summary = research_system.get_knowledge_summary()
            
            # Test if ASIS can analyze learning effectiveness
            learning_analysis = research_system.analyze_learning_effectiveness()
            
            # Check for synthesis capabilities
            has_analysis = learning_analysis and len(learning_analysis) > 0
            has_knowledge = knowledge_summary.get('total_entries', 0) > 0
            
            synthesis_score = 0
            if has_knowledge:
                synthesis_score += 0.5
            if has_analysis:
                synthesis_score += 0.5
                
            success = synthesis_score >= 0.5
            
            details = {
                'knowledge_entries': knowledge_summary.get('total_entries', 0),
                'has_learning_analysis': has_analysis,
                'synthesis_score': synthesis_score,
                'knowledge_summary': knowledge_summary
            }
            
            self.log_test('knowledge_synthesis', success, details)
            print(f"  ✅ Knowledge Synthesis: Score {synthesis_score}")
            return success
            
        except Exception as e:
            print(f"  ❌ Knowledge Synthesis Error: {e}")
            self.log_test('knowledge_synthesis', False, {'error': str(e)})
            return False
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run all knowledge expansion tests"""
        print("🚀 COMPREHENSIVE ASIS KNOWLEDGE EXPANSION TEST")
        print("=" * 60)
        
        start_time = datetime.now()
        
        # Run all tests
        tests = [
            self.test_technical_research,
            self.test_cross_domain_learning, 
            self.test_interaction_based_learning,
            self.test_knowledge_synthesis
        ]
        
        passed_tests = 0
        for test in tests:
            if test():
                passed_tests += 1
            print()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Generate comprehensive report
        report = {
            'total_tests': len(tests),
            'passed_tests': passed_tests,
            'success_rate': passed_tests / len(tests),
            'duration_seconds': duration,
            'test_results': self.test_results,
            'final_database_stats': {
                'research_db': self.get_database_stats(self.research_db),
                'meta_learning_db': self.get_database_stats(self.meta_learning_db),
                'memory_db': self.get_database_stats(self.memory_db)
            }
        }
        
        print("📊 COMPREHENSIVE TEST RESULTS:")
        print("=" * 60)
        print(f"✅ Tests Passed: {passed_tests}/{len(tests)} ({report['success_rate']:.1%})")
        print(f"⏱️  Duration: {duration:.1f} seconds")
        print(f"📈 Research Findings: {report['final_database_stats']['research_db'].get('research_findings_count', 0)}")
        
        if report['success_rate'] >= 0.75:
            print("🎉 EXCELLENT: ASIS demonstrates strong autonomous knowledge expansion!")
        elif report['success_rate'] >= 0.5:
            print("✅ GOOD: ASIS shows solid knowledge expansion capabilities")
        else:
            print("⚠️  NEEDS IMPROVEMENT: Knowledge expansion needs optimization")
        
        return report

def main():
    """Run the advanced knowledge expansion test suite"""
    tester = AdvancedKnowledgeExpansionTester()
    results = tester.run_comprehensive_test()
    
    # Save detailed results
    with open('knowledge_expansion_test_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Detailed results saved to: knowledge_expansion_test_results.json")
    return results

if __name__ == "__main__":
    main()
