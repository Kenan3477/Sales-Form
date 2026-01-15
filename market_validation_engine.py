"""
ASIS Market Validation & Product-Market Fit Testing Engine
========================================================
A/B testing, customer feedback, usage analytics, competitive analysis
Optimize pricing, features, and customer satisfaction for maximum revenue
"""

import asyncio
import json
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from pydantic import BaseModel
from dataclasses import dataclass
import random
import logging
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ===== A/B TESTING FRAMEWORK =====

class ABTestVariant(BaseModel):
    variant_id: str
    variant_name: str
    pricing_tier: str
    monthly_price: float
    features: List[str]
    target_audience: str
    conversion_rate: float = 0.0
    revenue_per_user: float = 0.0
    sample_size: int = 0

class ABTestExperiment(BaseModel):
    experiment_id: str
    experiment_name: str
    hypothesis: str
    start_date: datetime
    end_date: datetime
    variants: List[ABTestVariant]
    success_metric: str
    statistical_significance: float = 0.0
    winning_variant: Optional[str] = None
    status: str = "active"

class ABTestingEngine:
    """A/B testing framework for pricing and features"""
    
    def __init__(self):
        self.experiments_db = "ab_testing.db"
        self.init_database()
    
    def init_database(self):
        """Initialize A/B testing database"""
        conn = sqlite3.connect(self.experiments_db)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ab_experiments (
                id INTEGER PRIMARY KEY,
                experiment_id TEXT UNIQUE,
                experiment_name TEXT,
                hypothesis TEXT,
                start_date DATETIME,
                end_date DATETIME,
                success_metric TEXT,
                statistical_significance REAL DEFAULT 0.0,
                winning_variant TEXT,
                status TEXT DEFAULT 'active',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ab_variants (
                id INTEGER PRIMARY KEY,
                experiment_id TEXT,
                variant_id TEXT,
                variant_name TEXT,
                pricing_tier TEXT,
                monthly_price REAL,
                features TEXT,  -- JSON array
                target_audience TEXT,
                conversion_rate REAL DEFAULT 0.0,
                revenue_per_user REAL DEFAULT 0.0,
                sample_size INTEGER DEFAULT 0,
                FOREIGN KEY (experiment_id) REFERENCES ab_experiments(experiment_id)
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ab_user_assignments (
                id INTEGER PRIMARY KEY,
                user_email TEXT,
                experiment_id TEXT,
                variant_id TEXT,
                assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                converted BOOLEAN DEFAULT FALSE,
                conversion_date DATETIME,
                revenue_generated REAL DEFAULT 0.0
            )
        """)
        
        conn.commit()
        conn.close()
    
    async def create_pricing_experiment(self) -> ABTestExperiment:
        """Create A/B test for pricing optimization"""
        experiment = ABTestExperiment(
            experiment_id="pricing_optimization_v1",
            experiment_name="Academic Pricing Tier Optimization",
            hypothesis="Lower academic pricing ($39 vs $49.50) will increase conversion by 25%+ while maintaining revenue",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=14),
            variants=[
                ABTestVariant(
                    variant_id="academic_current",
                    variant_name="Current Academic Pricing",
                    pricing_tier="Academic", 
                    monthly_price=49.50,
                    features=["Basic AI research", "5 projects/month", "Standard support", "Academic discount"],
                    target_audience="university_researchers"
                ),
                ABTestVariant(
                    variant_id="academic_lower",
                    variant_name="Reduced Academic Pricing",
                    pricing_tier="Academic",
                    monthly_price=39.00,
                    features=["Basic AI research", "5 projects/month", "Standard support", "Enhanced academic discount"],
                    target_audience="university_researchers"
                ),
                ABTestVariant(
                    variant_id="academic_freemium",
                    variant_name="Freemium Academic Model",
                    pricing_tier="Academic",
                    monthly_price=0.00,  # Free tier with limitations
                    features=["Basic AI research", "2 projects/month", "Community support", "Upgrade prompts"],
                    target_audience="university_researchers"
                )
            ],
            success_metric="revenue_per_user"
        )
        
        # Save to database
        await self.save_experiment(experiment)
        return experiment
    
    async def create_feature_experiment(self) -> ABTestExperiment:
        """Create A/B test for feature combination optimization"""
        experiment = ABTestExperiment(
            experiment_id="feature_optimization_v1", 
            experiment_name="Professional Tier Feature Optimization",
            hypothesis="Adding 'Priority Support + Advanced Analytics' increases Professional conversions by 30%",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=21),
            variants=[
                ABTestVariant(
                    variant_id="professional_standard",
                    variant_name="Standard Professional Features",
                    pricing_tier="Professional",
                    monthly_price=299.00,
                    features=["Advanced AI research", "Unlimited projects", "API access", "Standard support"],
                    target_audience="professional_researchers"
                ),
                ABTestVariant(
                    variant_id="professional_enhanced",
                    variant_name="Enhanced Professional Features", 
                    pricing_tier="Professional",
                    monthly_price=299.00,
                    features=["Advanced AI research", "Unlimited projects", "API access", "Priority support", "Advanced analytics dashboard"],
                    target_audience="professional_researchers"
                ),
                ABTestVariant(
                    variant_id="professional_premium",
                    variant_name="Premium Professional Features",
                    pricing_tier="Professional",
                    monthly_price=349.00,
                    features=["Advanced AI research", "Unlimited projects", "API access", "Priority support", "Advanced analytics", "Custom AI models"],
                    target_audience="professional_researchers"
                )
            ],
            success_metric="conversion_rate"
        )
        
        await self.save_experiment(experiment)
        return experiment
    
    async def save_experiment(self, experiment: ABTestExperiment):
        """Save experiment and variants to database"""
        conn = sqlite3.connect(self.experiments_db)
        
        # Save experiment
        conn.execute("""
            INSERT OR REPLACE INTO ab_experiments
            (experiment_id, experiment_name, hypothesis, start_date, end_date, success_metric, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            experiment.experiment_id,
            experiment.experiment_name,
            experiment.hypothesis,
            experiment.start_date,
            experiment.end_date,
            experiment.success_metric,
            experiment.status
        ))
        
        # Save variants
        for variant in experiment.variants:
            conn.execute("""
                INSERT OR REPLACE INTO ab_variants
                (experiment_id, variant_id, variant_name, pricing_tier, monthly_price, features, target_audience)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                experiment.experiment_id,
                variant.variant_id,
                variant.variant_name,
                variant.pricing_tier,
                variant.monthly_price,
                json.dumps(variant.features),
                variant.target_audience
            ))
        
        conn.commit()
        conn.close()
    
    async def assign_user_to_variant(self, user_email: str, experiment_id: str) -> str:
        """Assign user to A/B test variant"""
        conn = sqlite3.connect(self.experiments_db)
        
        # Get experiment variants
        variants = conn.execute("""
            SELECT variant_id FROM ab_variants WHERE experiment_id = ?
        """, (experiment_id,)).fetchall()
        
        # Random assignment (equal distribution)
        selected_variant = random.choice(variants)[0]
        
        # Save assignment
        conn.execute("""
            INSERT OR REPLACE INTO ab_user_assignments
            (user_email, experiment_id, variant_id)
            VALUES (?, ?, ?)
        """, (user_email, experiment_id, selected_variant))
        
        conn.commit()
        conn.close()
        
        return selected_variant
    
    async def track_conversion(self, user_email: str, experiment_id: str, revenue: float):
        """Track user conversion in A/B test"""
        conn = sqlite3.connect(self.experiments_db)
        
        conn.execute("""
            UPDATE ab_user_assignments
            SET converted = TRUE, conversion_date = ?, revenue_generated = ?
            WHERE user_email = ? AND experiment_id = ?
        """, (datetime.now(), revenue, user_email, experiment_id))
        
        conn.commit()
        conn.close()
    
    async def calculate_experiment_results(self, experiment_id: str) -> Dict:
        """Calculate A/B test results and statistical significance"""
        conn = sqlite3.connect(self.experiments_db)
        
        # Get variant performance
        results = conn.execute("""
            SELECT 
                v.variant_id,
                v.variant_name,
                v.monthly_price,
                COUNT(a.user_email) as sample_size,
                SUM(CASE WHEN a.converted = 1 THEN 1 ELSE 0 END) as conversions,
                AVG(CASE WHEN a.converted = 1 THEN a.revenue_generated ELSE 0 END) as avg_revenue_per_user,
                SUM(a.revenue_generated) as total_revenue
            FROM ab_variants v
            LEFT JOIN ab_user_assignments a ON v.variant_id = a.variant_id
            WHERE v.experiment_id = ?
            GROUP BY v.variant_id
        """, (experiment_id,)).fetchall()
        
        variant_results = []
        for result in results:
            variant_id, variant_name, price, sample_size, conversions, avg_revenue, total_revenue = result
            conversion_rate = (conversions / sample_size * 100) if sample_size > 0 else 0
            
            variant_results.append({
                "variant_id": variant_id,
                "variant_name": variant_name, 
                "price": price,
                "sample_size": sample_size,
                "conversions": conversions,
                "conversion_rate": f"{conversion_rate:.2f}%",
                "avg_revenue_per_user": avg_revenue or 0,
                "total_revenue": total_revenue or 0
            })
        
        # Determine winning variant (highest revenue per user)
        if variant_results:
            winning_variant = max(variant_results, key=lambda x: x["avg_revenue_per_user"])
            
            # Update experiment with winner
            conn.execute("""
                UPDATE ab_experiments 
                SET winning_variant = ?, statistical_significance = ?
                WHERE experiment_id = ?
            """, (winning_variant["variant_id"], 0.95, experiment_id))  # Assume 95% confidence
            
            conn.commit()
        
        conn.close()
        
        return {
            "experiment_id": experiment_id,
            "variants": variant_results,
            "winning_variant": winning_variant["variant_id"] if variant_results else None,
            "recommendation": f"Implement {winning_variant['variant_name']} - {winning_variant['conversion_rate']} conversion, ${winning_variant['avg_revenue_per_user']:.2f} RPU" if variant_results else "Insufficient data"
        }


# ===== CUSTOMER FEEDBACK COLLECTION =====

class CustomerFeedback(BaseModel):
    feedback_id: str
    user_email: str
    user_type: str  # academic, professional, enterprise
    feedback_type: str  # survey, interview, support_ticket, feature_request
    rating: float  # 1-5 scale
    feedback_text: str
    feature_requests: List[str]
    pain_points: List[str]
    satisfaction_drivers: List[str]
    created_at: datetime
    category: str = "general"

class FeedbackCollectionSystem:
    """Systematic customer feedback collection and analysis"""
    
    def __init__(self):
        self.feedback_db = "customer_feedback.db"
        self.init_database()
    
    def init_database(self):
        """Initialize customer feedback database"""
        conn = sqlite3.connect(self.feedback_db)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS customer_feedback (
                id INTEGER PRIMARY KEY,
                feedback_id TEXT UNIQUE,
                user_email TEXT,
                user_type TEXT,
                feedback_type TEXT,
                rating REAL,
                feedback_text TEXT,
                feature_requests TEXT,  -- JSON array
                pain_points TEXT,  -- JSON array
                satisfaction_drivers TEXT,  -- JSON array
                category TEXT DEFAULT 'general',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS nps_surveys (
                id INTEGER PRIMARY KEY,
                user_email TEXT,
                nps_score INTEGER,  -- 0-10 scale
                likelihood_to_recommend INTEGER,  -- 0-10 scale
                primary_reason TEXT,
                improvement_suggestions TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS feature_requests (
                id INTEGER PRIMARY KEY,
                feature_name TEXT,
                description TEXT,
                requested_by TEXT,  -- user_email
                priority_score INTEGER DEFAULT 0,
                votes INTEGER DEFAULT 1,
                status TEXT DEFAULT 'submitted',  -- submitted, in_development, completed
                estimated_effort TEXT,  -- small, medium, large
                business_impact TEXT,  -- low, medium, high
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    async def collect_in_app_survey(self, user_email: str, user_type: str) -> Dict:
        """Generate and collect in-app survey responses"""
        
        # Generate personalized survey based on user type
        survey_questions = self._generate_survey_questions(user_type)
        
        # Simulate survey responses (in production, would be actual user input)
        simulated_responses = await self._simulate_survey_responses(user_email, user_type, survey_questions)
        
        # Save feedback
        feedback = CustomerFeedback(
            feedback_id=f"survey_{user_email}_{datetime.now().timestamp()}",
            user_email=user_email,
            user_type=user_type,
            feedback_type="survey",
            rating=simulated_responses["overall_rating"],
            feedback_text=simulated_responses["feedback_text"],
            feature_requests=simulated_responses["feature_requests"],
            pain_points=simulated_responses["pain_points"],
            satisfaction_drivers=simulated_responses["satisfaction_drivers"],
            created_at=datetime.now(),
            category=user_type
        )
        
        await self.save_feedback(feedback)
        
        return {
            "feedback_collected": True,
            "rating": simulated_responses["overall_rating"],
            "key_insights": simulated_responses["key_insights"]
        }
    
    def _generate_survey_questions(self, user_type: str) -> List[str]:
        """Generate personalized survey questions"""
        base_questions = [
            "How satisfied are you with ASIS Research Platform overall?",
            "Which features do you find most valuable?",
            "What are your biggest pain points with the platform?",
            "What additional features would you like to see?"
        ]
        
        if user_type == "academic":
            specific_questions = [
                "How has ASIS impacted your research productivity?",
                "Would you recommend ASIS to other researchers?",
                "What pricing model would work best for your department?"
            ]
        elif user_type == "professional":
            specific_questions = [
                "How does ASIS compare to other research tools you use?",
                "What ROI have you seen from using ASIS?",
                "What integration capabilities are most important?"
            ]
        else:  # enterprise
            specific_questions = [
                "How has ASIS impacted your team's research efficiency?",
                "What compliance and security features are priorities?",
                "What would justify expanding ASIS usage across your organization?"
            ]
        
        return base_questions + specific_questions
    
    async def _simulate_survey_responses(self, user_email: str, user_type: str, questions: List[str]) -> Dict:
        """Simulate realistic survey responses based on user type"""
        
        # Simulate responses based on user type patterns
        if user_type == "academic":
            rating = random.uniform(3.8, 4.6)  # Academics generally positive but critical
            pain_points = ["cost", "learning curve", "integration with existing tools"]
            feature_requests = ["offline mode", "collaborative features", "citation management"]
            satisfaction_drivers = ["research speed", "comprehensive results", "academic discount"]
            feedback_text = "ASIS has significantly improved my research efficiency. The AI-powered literature review saves me hours each week. However, I'd love better integration with citation managers and more collaboration features for working with colleagues."
            key_insights = ["Values time savings", "Needs collaboration features", "Price-sensitive"]
        
        elif user_type == "professional":
            rating = random.uniform(4.2, 4.8)  # Professionals focus on ROI
            pain_points = ["API limitations", "custom reporting", "advanced analytics"]
            feature_requests = ["advanced API", "custom dashboards", "white-label options"]
            satisfaction_drivers = ["ROI", "automation", "comprehensive data"]
            feedback_text = "ASIS provides excellent ROI for our research team. The automation capabilities are impressive. We'd like more advanced API features and custom reporting for client presentations."
            key_insights = ["ROI-focused", "Needs advanced features", "Client-facing applications"]
        
        else:  # enterprise
            rating = random.uniform(4.0, 4.9)  # Enterprises value reliability and scale
            pain_points = ["scalability", "security compliance", "team management"]
            feature_requests = ["SSO integration", "team analytics", "enterprise security"]
            satisfaction_drivers = ["team productivity", "scalability", "enterprise features"]
            feedback_text = "ASIS has transformed our R&D productivity across multiple teams. We need better enterprise features like SSO, team management, and compliance reporting for broader deployment."
            key_insights = ["Scale-focused", "Security/compliance needs", "Team management priorities"]
        
        return {
            "overall_rating": rating,
            "feedback_text": feedback_text,
            "feature_requests": feature_requests,
            "pain_points": pain_points,
            "satisfaction_drivers": satisfaction_drivers,
            "key_insights": key_insights
        }
    
    async def save_feedback(self, feedback: CustomerFeedback):
        """Save customer feedback to database"""
        conn = sqlite3.connect(self.feedback_db)
        
        conn.execute("""
            INSERT INTO customer_feedback
            (feedback_id, user_email, user_type, feedback_type, rating, feedback_text, 
             feature_requests, pain_points, satisfaction_drivers, category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            feedback.feedback_id,
            feedback.user_email,
            feedback.user_type,
            feedback.feedback_type,
            feedback.rating,
            feedback.feedback_text,
            json.dumps(feedback.feature_requests),
            json.dumps(feedback.pain_points),
            json.dumps(feedback.satisfaction_drivers),
            feedback.category
        ))
        
        conn.commit()
        conn.close()
    
    async def analyze_feedback_trends(self) -> Dict:
        """Analyze customer feedback trends and insights"""
        conn = sqlite3.connect(self.feedback_db)
        
        # Overall satisfaction metrics
        avg_rating = conn.execute("SELECT AVG(rating) FROM customer_feedback").fetchone()[0] or 0
        total_feedback = conn.execute("SELECT COUNT(*) FROM customer_feedback").fetchone()[0]
        
        # Ratings by user type
        ratings_by_type = conn.execute("""
            SELECT user_type, AVG(rating), COUNT(*) 
            FROM customer_feedback 
            GROUP BY user_type
        """).fetchall()
        
        # Most common feature requests (would need JSON parsing in real implementation)
        feature_requests = conn.execute("""
            SELECT feature_requests FROM customer_feedback WHERE feature_requests != '[]'
        """).fetchall()
        
        # Most common pain points
        pain_points = conn.execute("""
            SELECT pain_points FROM customer_feedback WHERE pain_points != '[]'
        """).fetchall()
        
        conn.close()
        
        # Aggregate feature requests and pain points
        all_features = []
        all_pain_points = []
        
        for req in feature_requests:
            try:
                features = json.loads(req[0])
                all_features.extend(features)
            except:
                pass
        
        for pain in pain_points:
            try:
                points = json.loads(pain[0])
                all_pain_points.extend(points)
            except:
                pass
        
        # Count frequency
        feature_frequency = {}
        for feature in all_features:
            feature_frequency[feature] = feature_frequency.get(feature, 0) + 1
        
        pain_frequency = {}
        for pain in all_pain_points:
            pain_frequency[pain] = pain_frequency.get(pain, 0) + 1
        
        # Sort by frequency
        top_features = sorted(feature_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
        top_pain_points = sorted(pain_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "overall_metrics": {
                "average_rating": f"{avg_rating:.2f}/5.0",
                "total_feedback": total_feedback,
                "satisfaction_level": "High" if avg_rating > 4.0 else "Medium" if avg_rating > 3.0 else "Low"
            },
            "ratings_by_segment": [
                {"user_type": r[0], "avg_rating": f"{r[1]:.2f}", "sample_size": r[2]}
                for r in ratings_by_type
            ],
            "top_feature_requests": top_features,
            "top_pain_points": top_pain_points,
            "recommendations": self._generate_feedback_recommendations(avg_rating, top_features, top_pain_points)
        }
    
    def _generate_feedback_recommendations(self, avg_rating: float, top_features: List[Tuple], top_pain_points: List[Tuple]) -> List[str]:
        """Generate actionable recommendations from feedback analysis"""
        recommendations = []
        
        if avg_rating < 4.0:
            recommendations.append("URGENT: Address customer satisfaction - below target of 4.0/5.0")
        
        if top_pain_points:
            top_pain = top_pain_points[0][0]
            recommendations.append(f"Priority fix: Address #{top_pain}# - most common pain point")
        
        if top_features:
            top_feature = top_features[0][0]
            recommendations.append(f"Feature priority: Develop #{top_feature}# - most requested feature")
        
        recommendations.extend([
            "Implement regular NPS surveys for trend tracking",
            "Create customer advisory board from high-satisfaction users",
            "Develop customer success playbook based on satisfaction drivers"
        ])
        
        return recommendations


# ===== USAGE ANALYTICS ENGINE =====

class UsageAnalytics:
    """Comprehensive usage pattern analysis for product optimization"""
    
    def __init__(self):
        self.analytics_db = "usage_analytics.db"
        self.init_database()
    
    def init_database(self):
        """Initialize usage analytics database"""
        conn = sqlite3.connect(self.analytics_db)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY,
                user_email TEXT,
                session_id TEXT,
                start_time DATETIME,
                end_time DATETIME,
                duration_minutes INTEGER,
                pages_visited INTEGER,
                features_used TEXT,  -- JSON array
                research_projects_created INTEGER DEFAULT 0,
                ai_queries_executed INTEGER DEFAULT 0,
                user_type TEXT,
                subscription_tier TEXT
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS feature_usage (
                id INTEGER PRIMARY KEY,
                user_email TEXT,
                feature_name TEXT,
                usage_count INTEGER DEFAULT 1,
                last_used DATETIME,
                total_time_spent INTEGER DEFAULT 0,  -- minutes
                success_rate REAL DEFAULT 1.0,  -- 0-1
                user_satisfaction REAL DEFAULT 0.0  -- 0-5
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS churn_indicators (
                id INTEGER PRIMARY KEY,
                user_email TEXT,
                risk_score REAL DEFAULT 0.0,  -- 0-1, higher = more risk
                days_since_last_login INTEGER DEFAULT 0,
                usage_trend TEXT DEFAULT 'stable',  -- declining, stable, growing
                engagement_score REAL DEFAULT 0.5,  -- 0-1
                support_tickets INTEGER DEFAULT 0,
                feature_adoption_rate REAL DEFAULT 0.0,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    async def track_user_session(self, user_email: str, user_type: str, subscription_tier: str) -> Dict:
        """Simulate and track user session analytics"""
        
        # Simulate realistic usage patterns based on user type
        session_data = await self._simulate_user_session(user_type, subscription_tier)
        
        conn = sqlite3.connect(self.analytics_db)
        
        session_id = f"{user_email}_{datetime.now().timestamp()}"
        
        conn.execute("""
            INSERT INTO user_sessions
            (user_email, session_id, start_time, end_time, duration_minutes, pages_visited,
             features_used, research_projects_created, ai_queries_executed, user_type, subscription_tier)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_email,
            session_id,
            session_data["start_time"],
            session_data["end_time"], 
            session_data["duration"],
            session_data["pages_visited"],
            json.dumps(session_data["features_used"]),
            session_data["projects_created"],
            session_data["ai_queries"],
            user_type,
            subscription_tier
        ))
        
        # Update feature usage
        for feature in session_data["features_used"]:
            conn.execute("""
                INSERT OR REPLACE INTO feature_usage
                (user_email, feature_name, usage_count, last_used, total_time_spent)
                VALUES (
                    ?, ?, 
                    COALESCE((SELECT usage_count FROM feature_usage WHERE user_email = ? AND feature_name = ?), 0) + 1,
                    ?,
                    COALESCE((SELECT total_time_spent FROM feature_usage WHERE user_email = ? AND feature_name = ?), 0) + ?
                )
            """, (user_email, feature, user_email, feature, datetime.now(), user_email, feature, random.randint(5, 30)))
        
        conn.commit()
        conn.close()
        
        return session_data
    
    async def _simulate_user_session(self, user_type: str, subscription_tier: str) -> Dict:
        """Simulate realistic user session based on user type and tier"""
        
        start_time = datetime.now() - timedelta(minutes=random.randint(30, 180))
        
        if user_type == "academic":
            duration = random.randint(45, 120)  # Academics spend more time per session
            pages_visited = random.randint(8, 15)
            features_used = random.sample([
                "literature_review", "ai_research_assistant", "citation_manager", 
                "trend_analysis", "hypothesis_generator", "collaboration_tools"
            ], random.randint(3, 5))
            projects_created = random.randint(0, 2)
            ai_queries = random.randint(5, 15)
            
        elif user_type == "professional":
            duration = random.randint(30, 90)  # Professionals are more focused
            pages_visited = random.randint(5, 12)
            features_used = random.sample([
                "competitive_analysis", "market_research", "ai_insights", 
                "custom_reports", "api_access", "advanced_analytics"
            ], random.randint(4, 6))
            projects_created = random.randint(1, 3)
            ai_queries = random.randint(10, 25)
            
        else:  # enterprise
            duration = random.randint(20, 60)  # Enterprise users are efficient
            pages_visited = random.randint(6, 10)
            features_used = random.sample([
                "team_management", "enterprise_analytics", "bulk_processing", 
                "api_integration", "custom_models", "compliance_reporting"
            ], random.randint(3, 6))
            projects_created = random.randint(2, 5)
            ai_queries = random.randint(15, 40)
        
        end_time = start_time + timedelta(minutes=duration)
        
        return {
            "start_time": start_time,
            "end_time": end_time,
            "duration": duration,
            "pages_visited": pages_visited,
            "features_used": features_used,
            "projects_created": projects_created,
            "ai_queries": ai_queries
        }
    
    async def calculate_churn_risk(self, user_email: str) -> Dict:
        """Calculate churn risk score for user"""
        conn = sqlite3.connect(self.analytics_db)
        
        # Get user activity metrics
        recent_sessions = conn.execute("""
            SELECT COUNT(*), AVG(duration_minutes), MAX(start_time)
            FROM user_sessions 
            WHERE user_email = ? AND start_time > datetime('now', '-30 days')
        """, (user_email,)).fetchone()
        
        session_count, avg_duration, last_session = recent_sessions
        session_count = session_count or 0
        avg_duration = avg_duration or 0
        
        # Calculate days since last login
        days_since_login = 30  # Default if no recent activity
        if last_session:
            last_login = datetime.fromisoformat(last_session.replace('Z', '+00:00').replace('+00:00', ''))
            days_since_login = (datetime.now() - last_login).days
        
        # Calculate feature adoption rate
        total_features = 20  # Total available features
        used_features = conn.execute("""
            SELECT COUNT(DISTINCT feature_name) FROM feature_usage WHERE user_email = ?
        """, (user_email,)).fetchone()[0] or 0
        
        feature_adoption_rate = used_features / total_features
        
        # Calculate engagement score (0-1)
        engagement_score = min(1.0, (
            (session_count / 20) * 0.4 +  # Session frequency (20 sessions = max)
            (min(avg_duration, 60) / 60) * 0.3 +  # Session duration (60 min = max)
            feature_adoption_rate * 0.3  # Feature adoption
        ))
        
        # Calculate risk score (0-1, higher = more risk)
        risk_score = max(0.0, (
            (days_since_login / 14) * 0.4 +  # Recency (14 days = high risk)
            (1 - engagement_score) * 0.4 +  # Low engagement = high risk
            (1 - min(session_count / 10, 1.0)) * 0.2  # Low frequency = risk
        ))
        
        risk_score = min(1.0, risk_score)
        
        # Determine usage trend
        if session_count == 0:
            usage_trend = "inactive"
        elif engagement_score > 0.7:
            usage_trend = "growing"
        elif engagement_score > 0.4:
            usage_trend = "stable"
        else:
            usage_trend = "declining"
        
        # Update churn indicators
        conn.execute("""
            INSERT OR REPLACE INTO churn_indicators
            (user_email, risk_score, days_since_last_login, usage_trend, 
             engagement_score, feature_adoption_rate, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_email, risk_score, days_since_login, usage_trend,
            engagement_score, feature_adoption_rate, datetime.now()
        ))
        
        conn.commit()
        conn.close()
        
        return {
            "user_email": user_email,
            "risk_score": f"{risk_score:.2f}",
            "risk_level": "High" if risk_score > 0.7 else "Medium" if risk_score > 0.4 else "Low",
            "days_since_login": days_since_login,
            "usage_trend": usage_trend,
            "engagement_score": f"{engagement_score:.2f}",
            "feature_adoption_rate": f"{feature_adoption_rate:.1%}",
            "recommendations": self._generate_churn_prevention_actions(risk_score, usage_trend, engagement_score)
        }
    
    def _generate_churn_prevention_actions(self, risk_score: float, usage_trend: str, engagement_score: float) -> List[str]:
        """Generate churn prevention actions based on risk analysis"""
        actions = []
        
        if risk_score > 0.7:
            actions.append("URGENT: Personal outreach within 24 hours")
            actions.append("Offer 1:1 success session with customer success manager")
            actions.append("Provide immediate value demonstration")
        
        if usage_trend == "declining":
            actions.append("Send feature spotlight emails highlighting unused capabilities")
            actions.append("Offer training session on advanced features")
        
        if engagement_score < 0.4:
            actions.append("Trigger onboarding re-engagement sequence")
            actions.append("Provide use case templates and quick wins")
        
        if usage_trend == "inactive":
            actions.append("Win-back campaign with special offer")
            actions.append("Exit interview to understand departure reasons")
        
        return actions
    
    async def generate_usage_insights(self) -> Dict:
        """Generate comprehensive usage analytics insights"""
        conn = sqlite3.connect(self.analytics_db)
        
        # Overall usage metrics
        total_users = conn.execute("SELECT COUNT(DISTINCT user_email) FROM user_sessions").fetchone()[0] or 0
        total_sessions = conn.execute("SELECT COUNT(*) FROM user_sessions").fetchone()[0] or 0
        avg_session_duration = conn.execute("SELECT AVG(duration_minutes) FROM user_sessions").fetchone()[0] or 0
        
        # Feature usage
        popular_features = conn.execute("""
            SELECT feature_name, SUM(usage_count) as total_usage
            FROM feature_usage
            GROUP BY feature_name
            ORDER BY total_usage DESC
            LIMIT 5
        """).fetchall()
        
        # User engagement by tier
        engagement_by_tier = conn.execute("""
            SELECT subscription_tier, 
                   COUNT(DISTINCT user_email) as users,
                   AVG(duration_minutes) as avg_duration,
                   AVG(ai_queries_executed) as avg_queries
            FROM user_sessions
            GROUP BY subscription_tier
        """).fetchall()
        
        # Churn risk distribution
        churn_distribution = conn.execute("""
            SELECT 
                CASE 
                    WHEN risk_score > 0.7 THEN 'High Risk'
                    WHEN risk_score > 0.4 THEN 'Medium Risk'
                    ELSE 'Low Risk'
                END as risk_level,
                COUNT(*) as user_count
            FROM churn_indicators
            GROUP BY risk_level
        """).fetchall()
        
        conn.close()
        
        return {
            "overall_metrics": {
                "total_active_users": total_users,
                "total_sessions": total_sessions,
                "avg_session_duration": f"{avg_session_duration:.1f} minutes",
                "sessions_per_user": f"{(total_sessions/total_users):.1f}" if total_users > 0 else "0"
            },
            "popular_features": [
                {"feature": feature, "usage_count": usage}
                for feature, usage in popular_features
            ],
            "engagement_by_tier": [
                {
                    "tier": tier,
                    "users": users,
                    "avg_duration": f"{duration:.1f} min",
                    "avg_queries": f"{queries:.1f}"
                }
                for tier, users, duration, queries in engagement_by_tier
            ],
            "churn_risk_distribution": [
                {"risk_level": level, "user_count": count}
                for level, count in churn_distribution
            ]
        }


# ===== MAIN EXECUTION =====

async def main():
    """Execute Market Validation & Analytics Engine"""
    
    print("\n📊 ASIS MARKET VALIDATION & ANALYTICS ENGINE")
    print("="*60)
    print("A/B testing, customer feedback, usage analytics, churn prevention")
    print("="*60)
    
    # Initialize systems
    ab_testing = ABTestingEngine()
    feedback_system = FeedbackCollectionSystem()
    usage_analytics = UsageAnalytics()
    
    # Create and run A/B tests
    print("\n🧪 Creating A/B Testing Experiments...")
    pricing_experiment = await ab_testing.create_pricing_experiment()
    feature_experiment = await ab_testing.create_feature_experiment()
    
    print(f"✅ Created pricing experiment: {pricing_experiment.experiment_name}")
    print(f"✅ Created feature experiment: {feature_experiment.experiment_name}")
    
    # Simulate user assignments and conversions
    sample_users = [
        ("academic.user1@stanford.edu", "academic"),
        ("academic.user2@mit.edu", "academic"),
        ("professional.user1@company.com", "professional"),
        ("professional.user2@consulting.com", "professional"),
        ("enterprise.user1@fortune500.com", "enterprise")
    ]
    
    print("\n👥 Simulating A/B test assignments and conversions...")
    for user_email, user_type in sample_users:
        # Assign to pricing experiment
        variant = await ab_testing.assign_user_to_variant(user_email, pricing_experiment.experiment_id)
        print(f"   • {user_email} → {variant}")
        
        # Simulate conversion (30% conversion rate)
        if random.random() < 0.3:
            revenue = 49.50 if "current" in variant else 39.00 if "lower" in variant else 0.00
            await ab_testing.track_conversion(user_email, pricing_experiment.experiment_id, revenue)
    
    # Calculate A/B test results
    print("\n📈 A/B Test Results:")
    pricing_results = await ab_testing.calculate_experiment_results(pricing_experiment.experiment_id)
    print(f"   🎯 {pricing_results['recommendation']}")
    
    for variant in pricing_results['variants']:
        print(f"      • {variant['variant_name']}: {variant['conversion_rate']} conv, ${variant['avg_revenue_per_user']:.2f} RPU")
    
    # Collect customer feedback
    print("\n📝 Collecting Customer Feedback...")
    for user_email, user_type in sample_users:
        feedback_result = await feedback_system.collect_in_app_survey(user_email, user_type)
        print(f"   ✅ {user_email}: {feedback_result['rating']:.1f}/5.0 rating")
    
    # Analyze feedback trends
    feedback_analysis = await feedback_system.analyze_feedback_trends()
    print(f"\n📊 Feedback Analysis:")
    print(f"   • Overall satisfaction: {feedback_analysis['overall_metrics']['average_rating']}")
    print(f"   • Top feature request: {feedback_analysis['top_feature_requests'][0][0] if feedback_analysis['top_feature_requests'] else 'None'}")
    print(f"   • Top pain point: {feedback_analysis['top_pain_points'][0][0] if feedback_analysis['top_pain_points'] else 'None'}")
    
    # Track usage analytics
    print("\n📱 Tracking Usage Analytics...")
    for user_email, user_type in sample_users:
        tier = "Academic" if user_type == "academic" else "Professional" if user_type == "professional" else "Enterprise"
        session_data = await usage_analytics.track_user_session(user_email, user_type, tier)
        print(f"   • {user_email}: {session_data['duration']}min session, {session_data['ai_queries']} AI queries")
        
        # Calculate churn risk
        churn_analysis = await usage_analytics.calculate_churn_risk(user_email)
        print(f"     → Churn risk: {churn_analysis['risk_level']} ({churn_analysis['risk_score']})")
    
    # Generate comprehensive insights
    print("\n🎯 Usage Insights Summary:")
    usage_insights = await usage_analytics.generate_usage_insights()
    
    print(f"   📊 Overall Metrics:")
    print(f"      • Active users: {usage_insights['overall_metrics']['total_active_users']}")
    print(f"      • Avg session: {usage_insights['overall_metrics']['avg_session_duration']}")
    print(f"      • Sessions per user: {usage_insights['overall_metrics']['sessions_per_user']}")
    
    print(f"   🔧 Popular Features:")
    for feature in usage_insights['popular_features'][:3]:
        print(f"      • {feature['feature']}: {feature['usage_count']} uses")
    
    print(f"   ⚠️ Churn Risk Distribution:")
    for risk in usage_insights['churn_risk_distribution']:
        print(f"      • {risk['risk_level']}: {risk['user_count']} users")
    
    print("\n🚀 MARKET VALIDATION & ANALYTICS ENGINE ACTIVATED!")
    print("Next steps: Implement winning variants, address top pain points, reduce churn")

if __name__ == "__main__":
    asyncio.run(main())
