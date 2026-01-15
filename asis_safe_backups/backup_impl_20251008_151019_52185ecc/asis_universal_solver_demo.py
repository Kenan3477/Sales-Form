#!/usr/bin/env python3
"""
ASIS Universal Solver Demo
=========================
Demonstrates the capabilities of the Universal Problem-Solving System
"""

import os
import sys
import json
import time
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from asis_universal_solver import ASISUniversalSolver
except ImportError:
    print("❌ ASIS Universal Solver not found")
    sys.exit(1)

class UniversalSolverDemo:
    """Demo class for Universal Solver capabilities"""
    
    def __init__(self):
        self.solver = ASISUniversalSolver()
        self.demo_problems = self._load_demo_problems()
    
    def _load_demo_problems(self):
        """Load comprehensive demo problems across different domains"""
        return {
            "technology": [
                "How can I optimize a distributed database system to handle 1 million concurrent users while maintaining sub-100ms query response times and ensuring data consistency?",
                "Design a microservices architecture that can scale automatically based on load, maintain fault tolerance, and reduce operational costs by 30%.",
                "Create a machine learning pipeline that can process real-time streaming data, detect anomalies, and adapt to changing patterns without manual intervention."
            ],
            "business": [
                "Develop a customer retention strategy for a SaaS company that increases customer lifetime value by 40% while reducing churn to under 5% annually.",
                "Design a supply chain optimization system that reduces costs by 20%, improves delivery times by 30%, and increases sustainability metrics.",
                "Create a digital transformation strategy for a traditional manufacturing company to compete with tech-native startups."
            ],
            "science_research": [
                "Design an experimental protocol to test the effectiveness of a new drug treatment while minimizing patient risk and maximizing statistical significance.",
                "Develop a method to accurately predict climate change impacts on agricultural yields across different geographic regions over the next 20 years.",
                "Create a research methodology to study the long-term effects of remote work on productivity, creativity, and employee well-being."
            ],
            "engineering": [
                "Design a renewable energy system for a smart city that can meet 80% of energy needs, handle peak demand fluctuations, and integrate with existing infrastructure.",
                "Develop a transportation system that reduces urban congestion by 50%, cuts emissions by 60%, and improves accessibility for disabled users.",
                "Create a water management system that reduces waste by 40%, ensures quality standards, and adapts to climate variability."
            ],
            "creative_design": [
                "Design an immersive user experience for a virtual reality education platform that increases learning retention by 25% and engagement by 50%.",
                "Create a sustainable packaging solution that reduces environmental impact by 70% while maintaining product protection and brand appeal.",
                "Develop a community space design that fosters social interaction, supports mental health, and adapts to diverse cultural needs."
            ],
            "complex_interdisciplinary": [
                "Design a comprehensive approach to reduce homelessness in urban areas by 60% over 5 years, addressing housing, employment, healthcare, and social services.",
                "Create a framework for ethical AI development that balances innovation, privacy, safety, and fairness across different cultural contexts.",
                "Develop a pandemic preparedness system that can detect emerging threats early, coordinate global response, and minimize economic disruption."
            ]
        }
    
    def run_comprehensive_demo(self):
        """Run comprehensive demo across all problem types"""
        print("🌟 ASIS Universal Problem-Solving System Demo")
        print("=" * 60)
        print(f"🕒 Demo Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        total_problems = 0
        successful_solutions = 0
        total_strategies = 0
        
        for domain, problems in self.demo_problems.items():
            print(f"\n🎯 Testing {domain.upper()} Domain Problems")
            print("-" * 40)
            
            for i, problem in enumerate(problems, 1):
                print(f"\n📝 Problem {i}: {problem[:80]}...")
                total_problems += 1
                
                try:
                    # Solve the problem
                    start_time = time.time()
                    result = self.solver.solve_problem(problem)
                    solve_time = time.time() - start_time
                    
                    if "error" not in result:
                        successful_solutions += 1
                        solution_count = len(result['solution_approaches'])
                        total_strategies += solution_count
                        
                        print(f"   ✅ Success! Generated {solution_count} solutions in {solve_time:.2f}s")
                        
                        # Display best solution summary
                        if result['solution_approaches']:
                            best = result['solution_approaches'][0]
                            print(f"   🏆 Best Strategy: {best['strategy']}")
                            print(f"   📊 Confidence: {best['confidence_score']:.2f}")
                            print(f"   ⏱️  Estimated Time: {best['estimated_time']} minutes")
                            print(f"   ⚠️  Risk Level: {best['risk_level']}")
                        
                        # Show pattern matching results
                        if result['pattern_matches']:
                            best_pattern = result['pattern_matches'][0]
                            print(f"   🔗 Best Pattern Match: {best_pattern['pattern_name']} (Score: {best_pattern['similarity_score']:.3f})")
                        
                        # Show learning integration
                        learning = result['learning_integration']
                        print(f"   🧠 Learning Integration: {len(learning['builtin_knowledge_matched'])} knowledge matches, {len(learning['learning_recommendations'])} recommendations")
                        
                    else:
                        print(f"   ❌ Error: {result['error']}")
                    
                except Exception as e:
                    print(f"   ❌ Exception: {e}")
        
        # Display comprehensive results
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE DEMO RESULTS")
        print("=" * 60)
        print(f"Total Problems Tested: {total_problems}")
        print(f"Successful Solutions: {successful_solutions}")
        print(f"Success Rate: {(successful_solutions/total_problems*100):.1f}%")
        print(f"Total Strategies Generated: {total_strategies}")
        print(f"Average Strategies per Problem: {(total_strategies/successful_solutions):.1f}" if successful_solutions > 0 else "N/A")
        
        # Get solver statistics
        stats = self.solver.get_solver_statistics()
        print(f"\nSystem Statistics:")
        print(f"  Total Sessions: {stats.get('total_sessions', 0)}")
        print(f"  Problems Analyzed: {stats.get('total_problems_analyzed', 0)}")
        print(f"  Solutions Generated: {stats.get('total_solutions_generated', 0)}")
        
        print(f"\n🕒 Demo Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("✅ Universal Problem-Solving System Demo Complete!")
    
    def run_interactive_demo(self):
        """Run interactive demo allowing user input"""
        print("🌟 ASIS Universal Solver - Interactive Demo")
        print("=" * 50)
        print("Enter any problem and see how the Universal Solver tackles it!")
        print("Type 'quit' to exit, 'examples' to see sample problems")
        
        while True:
            print("\n" + "-" * 50)
            user_input = input("🤔 Enter your problem: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Thanks for using ASIS Universal Solver!")
                break
            
            if user_input.lower() == 'examples':
                self._show_example_problems()
                continue
            
            if not user_input:
                print("Please enter a problem description.")
                continue
            
            try:
                print(f"\n🔍 Analyzing: {user_input}")
                print("⏳ Processing... (this may take a moment)")
                
                start_time = time.time()
                result = self.solver.solve_problem(user_input)
                process_time = time.time() - start_time
                
                if "error" not in result:
                    print(f"\n✅ Analysis Complete! ({process_time:.2f}s)")
                    self._display_interactive_results(result)
                    
                    # Ask if user wants solution details
                    if result['solution_approaches']:
                        detail_choice = input("\n❓ Would you like detailed implementation guide for the best solution? (y/n): ").strip().lower()
                        if detail_choice == 'y':
                            self._show_solution_details(result)
                else:
                    print(f"❌ Error processing problem: {result['error']}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _show_example_problems(self):
        """Show example problems to user"""
        print("\n📚 Example Problems:")
        print("-" * 30)
        
        examples = [
            "How can I improve team productivity by 25% while maintaining work-life balance?",
            "Design a mobile app that helps users reduce food waste and save money.",
            "Create a learning system that adapts to individual student needs and learning styles.",
            "Optimize a manufacturing process to reduce costs by 15% and improve quality.",
            "Develop a marketing strategy to increase brand awareness in a competitive market."
        ]
        
        for i, example in enumerate(examples, 1):
            print(f"{i}. {example}")
    
    def _display_interactive_results(self, result):
        """Display results in interactive format"""
        print("\n🎯 PROBLEM ANALYSIS")
        print("-" * 20)
        analysis = result['problem_analysis']
        print(f"Problem Type: {analysis['problem_type']}")
        print(f"Domain: {analysis['domain']}")
        print(f"Complexity: {analysis['complexity_score']:.2f} ({'HIGH' if analysis['complexity_score'] > 0.7 else 'MEDIUM' if analysis['complexity_score'] > 0.4 else 'LOW'})")
        print(f"Key Components: {', '.join(analysis['key_components'][:5])}")
        
        if analysis['objectives']:
            print(f"Objectives: {', '.join(analysis['objectives'])}")
        
        print("\n💡 SOLUTION APPROACHES")
        print("-" * 25)
        
        for i, solution in enumerate(result['solution_approaches'][:3], 1):
            print(f"\n{i}. {solution['strategy']} Strategy")
            print(f"   Description: {solution['description']}")
            print(f"   Confidence: {solution['confidence_score']:.2f}")
            print(f"   Time Estimate: {solution['estimated_time']} minutes")
            print(f"   Success Probability: {solution['success_probability']:.2f}")
            print(f"   Risk Level: {solution['risk_level']}")
        
        if result['pattern_matches']:
            print("\n🔗 PATTERN MATCHES")
            print("-" * 20)
            for i, pattern in enumerate(result['pattern_matches'][:2], 1):
                print(f"{i}. {pattern['pattern_name']} (Similarity: {pattern['similarity_score']:.3f})")
                print(f"   From domains: {', '.join(pattern['source_domains'])}")
        
        if result['learning_integration']['learning_recommendations']:
            print("\n🧠 LEARNING RECOMMENDATIONS")
            print("-" * 30)
            for i, rec in enumerate(result['learning_integration']['learning_recommendations'], 1):
                print(f"{i}. {rec}")
    
    def _show_solution_details(self, result):
        """Show detailed implementation guide for best solution"""
        if not result['solution_approaches']:
            return
        
        best_solution = result['solution_approaches'][0]
        details = self.solver.get_solution_details(
            result['session_id'], 
            best_solution['approach_id']
        )
        
        if 'error' in details:
            print(f"❌ Could not get solution details: {details['error']}")
            return
        
        print("\n📋 IMPLEMENTATION GUIDE")
        print("=" * 30)
        
        if 'implementation_guide' in details:
            for step in details['implementation_guide']:
                print(step)
        
        print("\n⚠️ RISK MITIGATION")
        print("-" * 20)
        if 'risk_mitigation' in details:
            for mitigation in details['risk_mitigation']:
                print(f"• {mitigation}")
        
        print("\n📈 SUCCESS METRICS")
        print("-" * 18)
        if 'success_metrics' in details:
            for metric in details['success_metrics']:
                print(f"• {metric}")
    
    def run_specific_domain_demo(self, domain):
        """Run demo for a specific domain"""
        if domain not in self.demo_problems:
            print(f"❌ Domain '{domain}' not found")
            return
        
        print(f"🎯 {domain.upper()} Domain Demo")
        print("=" * 40)
        
        problems = self.demo_problems[domain]
        for i, problem in enumerate(problems, 1):
            print(f"\n--- Problem {i} ---")
            print(f"Problem: {problem}")
            
            result = self.solver.solve_problem(problem)
            
            if "error" not in result:
                print(f"✅ Generated {len(result['solution_approaches'])} solutions")
                if result['solution_approaches']:
                    best = result['solution_approaches'][0]
                    print(f"🏆 Best: {best['strategy']} (Confidence: {best['confidence_score']:.2f})")
            else:
                print(f"❌ Error: {result['error']}")

def main():
    """Main demo function"""
    print("Welcome to ASIS Universal Problem-Solving System Demo!")
    print("\nSelect demo mode:")
    print("1. Comprehensive Demo (test all problem types)")
    print("2. Interactive Demo (enter your own problems)")
    print("3. Domain-Specific Demo")
    print("4. Quick Test")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    demo = UniversalSolverDemo()
    
    if choice == "1":
        demo.run_comprehensive_demo()
    elif choice == "2":
        demo.run_interactive_demo()
    elif choice == "3":
        print("\nAvailable domains:")
        domains = list(demo.demo_problems.keys())
        for i, domain in enumerate(domains, 1):
            print(f"{i}. {domain}")
        
        domain_choice = input("Enter domain number: ").strip()
        try:
            domain_index = int(domain_choice) - 1
            if 0 <= domain_index < len(domains):
                demo.run_specific_domain_demo(domains[domain_index])
            else:
                print("Invalid domain choice")
        except ValueError:
            print("Invalid input")
    elif choice == "4":
        # Quick test with one problem
        test_problem = "How can I improve my team's productivity while maintaining work-life balance?"
        print(f"🧪 Quick Test Problem: {test_problem}")
        result = demo.solver.solve_problem(test_problem)
        
        if "error" not in result:
            print(f"✅ Success! Generated {len(result['solution_approaches'])} solutions")
            if result['solution_approaches']:
                best = result['solution_approaches'][0]
                print(f"🏆 Best Strategy: {best['strategy']}")
                print(f"📊 Confidence: {best['confidence_score']:.2f}")
        else:
            print(f"❌ Error: {result['error']}")
    else:
        print("Invalid choice. Running interactive demo...")
        demo.run_interactive_demo()

if __name__ == "__main__":
    main()
