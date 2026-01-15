#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 ASIS Commercial AGI Platform Test Client
Test client for the commercial AGI API endpoints

Author: ASIS AGI Development Team
Version: 1.0.0
"""

import requests
import json
import time
from datetime import datetime

class AGICommercialTestClient:
    """Test client for commercial AGI platform"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_solve_any_problem(self):
        """Test universal problem solving endpoint"""
        print("\n🧪 Testing Universal Problem Solving...")
        
        test_data = {
            "problem_description": "How can we optimize supply chain logistics for a global e-commerce company while reducing costs and environmental impact?",
            "domain": "logistics",
            "complexity_level": 0.8,
            "context": {"industry": "e-commerce", "scale": "global"},
            "require_explanation": True
        }
        
        try:
            response = self.session.post(f"{self.base_url}/api/agi/solve-any-problem", json=test_data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success! Confidence: {result.get('confidence_score', 0):.2f}")
                print(f"   • Processing Time: {result.get('processing_time', 0):.2f}s") 
                print(f"   • AGI Instances: {result.get('agi_instances_used', 0)}")
                return True
            else:
                print(f"   ❌ Failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    def test_creative_collaboration(self):
        """Test creative collaboration endpoint"""
        print("\n🎨 Testing Creative Collaboration...")
        
        test_data = {
            "project_type": "mobile_app_design",
            "requirements": {
                "target_audience": "young professionals",
                "platform": "iOS/Android",
                "features": ["social networking", "productivity", "gamification"],
                "timeline": "3 months"
            },
            "style_preferences": {
                "design_style": "modern minimalist",
                "color_scheme": "vibrant",
                "user_experience": "intuitive"
            },
            "collaboration_level": "full",
            "timeline": "12_weeks"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/api/agi/creative-collaboration", json=test_data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success! Confidence: {result.get('confidence_score', 0):.2f}")
                print(f"   • Creative Approach: AGI-Human Collaboration")
                print(f"   • Project Type: {test_data['project_type']}")
                return True
            else:
                print(f"   ❌ Failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    def test_research_breakthrough(self):
        """Test research breakthrough endpoint"""
        print("\n🔬 Testing Research Breakthrough...")
        
        test_data = {
            "field": "renewable_energy",
            "current_knowledge": {
                "solar_efficiency": "22% commercial",
                "wind_capacity": "growing rapidly",
                "storage_challenges": "battery technology limitations",
                "grid_integration": "intermittency issues"
            },
            "research_goals": [
                "Breakthrough in energy storage efficiency",
                "Novel solar cell materials",
                "Smart grid optimization algorithms"
            ],
            "innovation_level": "breakthrough",
            "methodology_preferences": ["experimental_validation", "computational_modeling", "field_testing"]
        }
        
        try:
            response = self.session.post(f"{self.base_url}/api/agi/research-breakthrough", json=test_data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success! Confidence: {result.get('confidence_score', 0):.2f}")
                print(f"   • Research Field: {test_data['field']}")
                print(f"   • Innovation Level: {test_data['innovation_level']}")
                return True
            else:
                print(f"   ❌ Failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    def test_business_strategy(self):
        """Test business strategy endpoint"""
        print("\n📊 Testing Business Strategy Development...")
        
        test_data = {
            "company_data": {
                "industry": "fintech",
                "company_size": "mid-market",
                "revenue": "$50M annual",
                "employees": 200,
                "current_products": ["payment processing", "business loans", "financial analytics"]
            },
            "market_conditions": {
                "competition": "high",
                "growth_rate": "15% annually",
                "regulatory_environment": "increasing oversight",
                "technology_trends": ["AI/ML", "blockchain", "open banking"]
            },
            "strategic_goals": [
                "Expand into new markets",
                "Develop AI-powered products",
                "Improve customer retention",
                "Achieve sustainable profitability"
            ],
            "time_horizon": "24_months",
            "risk_tolerance": "moderate"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/api/agi/business-strategy", json=test_data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success! Confidence: {result.get('confidence_score', 0):.2f}")
                print(f"   • Strategy Horizon: {test_data['time_horizon']}")
                print(f"   • Risk Profile: {test_data['risk_tolerance']}")
                return True
            else:
                print(f"   ❌ Failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    def test_platform_status(self):
        """Test platform status endpoint"""
        print("\n📊 Testing Platform Status...")
        
        try:
            response = self.session.get(f"{self.base_url}/api/agi/platform-status")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Platform Status: {result.get('status', 'unknown')}")
                print(f"   • Version: {result.get('version', 'unknown')}")
                print(f"   • Total Requests: {result.get('usage_metrics', {}).get('total_requests', 0)}")
                return True
            else:
                print(f"   ❌ Failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all API endpoint tests"""
        print("🚀 ASIS Commercial AGI Platform API Tests")
        print("=" * 50)
        
        tests = [
            ("Platform Status", self.test_platform_status),
            ("Universal Problem Solving", self.test_solve_any_problem),
            ("Creative Collaboration", self.test_creative_collaboration),
            ("Research Breakthrough", self.test_research_breakthrough),
            ("Business Strategy", self.test_business_strategy)
        ]
        
        results = []
        
        for test_name, test_func in tests:
            try:
                success = test_func()
                results.append((test_name, success))
                time.sleep(1)  # Brief pause between tests
            except Exception as e:
                print(f"   ❌ {test_name} test failed: {e}")
                results.append((test_name, False))
        
        # Summary
        print(f"\n{'='*50}")
        print("📊 TEST SUMMARY")
        print(f"{'='*50}")
        
        passed = sum(1 for _, success in results if success)
        total = len(results)
        
        for test_name, success in results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"   {status} {test_name}")
        
        print(f"\n🎯 OVERALL RESULT: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 All tests passed! Commercial AGI platform is operational.")
        else:
            print("⚠️ Some tests failed. Check platform status.")
        
        return passed == total

def main():
    """Main test function"""
    print("Starting ASIS Commercial AGI Platform Tests...")
    
    # Note: This assumes the platform is running on localhost:8000
    # To test, first start the platform with:
    # python agi_commercial_platform.py
    
    test_client = AGICommercialTestClient()
    success = test_client.run_all_tests()
    
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
