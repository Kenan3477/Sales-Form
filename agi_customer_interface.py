#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
👥 ASIS AGI Customer Interface System
Customer-facing features for AGI interactions and subscriptions

This module provides:
- Customer AGI interaction interface
- Subscription tier management
- Usage tracking and billing
- Customer dashboard
- AGI capability demonstrations
- Support and feedback systems

Author: ASIS AGI Development Team
Version: 1.0.0
"""

import json
import sqlite3
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from flask import Flask, request, jsonify, render_template_string, session
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

@dataclass
class Customer:
    """Customer data structure"""
    customer_id: str
    email: str
    name: str
    subscription_tier: str
    created_at: datetime
    last_active: datetime
    usage_stats: Dict[str, Any]
    preferences: Dict[str, Any]

@dataclass
class AGIInteraction:
    """AGI interaction record"""
    interaction_id: str
    customer_id: str
    timestamp: datetime
    interaction_type: str
    input_data: str
    output_data: str
    processing_time: float
    success: bool
    tokens_used: int
    cost: float

class CustomerAGIInterface:
    """Customer interface for AGI interactions"""
    
    def __init__(self, db_path: str = "agi_customer_system.db"):
        self.db_path = db_path
        self.subscription_tiers = {
            "free": {
                "name": "Free Tier",
                "monthly_limit": 100,
                "features": ["basic_reasoning", "simple_queries"],
                "cost_per_token": 0.0,
                "priority": "low"
            },
            "basic": {
                "name": "Basic Plan",
                "monthly_limit": 1000,
                "features": ["basic_reasoning", "simple_queries", "cross_domain"],
                "cost_per_token": 0.001,
                "priority": "normal",
                "monthly_cost": 29.99
            },
            "professional": {
                "name": "Professional Plan", 
                "monthly_limit": 10000,
                "features": ["basic_reasoning", "simple_queries", "cross_domain", "advanced_analysis", "consciousness_insights"],
                "cost_per_token": 0.0008,
                "priority": "high",
                "monthly_cost": 99.99
            },
            "enterprise": {
                "name": "Enterprise Plan",
                "monthly_limit": 100000,
                "features": ["all_features", "priority_support", "custom_models"],
                "cost_per_token": 0.0005,
                "priority": "enterprise",
                "monthly_cost": 499.99
            }
        }
        
        self._initialize_database()
        print("👥 Customer AGI Interface initialized")
    
    def _initialize_database(self):
        """Initialize customer system database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Customers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                subscription_tier TEXT DEFAULT 'free',
                created_at TEXT NOT NULL,
                last_active TEXT,
                usage_stats TEXT,
                preferences TEXT,
                billing_info TEXT
            )
        """)
        
        # AGI interactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agi_interactions (
                interaction_id TEXT PRIMARY KEY,
                customer_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                interaction_type TEXT NOT NULL,
                input_data TEXT,
                output_data TEXT,
                processing_time REAL,
                success BOOLEAN,
                tokens_used INTEGER,
                cost REAL,
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )
        """)
        
        # Customer sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer_sessions (
                session_id TEXT PRIMARY KEY,
                customer_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )
        """)
        
        # Feedback and support table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer_feedback (
                feedback_id TEXT PRIMARY KEY,
                customer_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                feedback_type TEXT NOT NULL,
                rating INTEGER,
                message TEXT,
                resolved BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )
        """)
        
        conn.commit()
        conn.close()
        print("👥 Customer system database initialized")
    
    def register_customer(self, email: str, name: str, password: str, 
                         subscription_tier: str = "free") -> Dict[str, Any]:
        """Register a new customer"""
        try:
            # Validate subscription tier
            if subscription_tier not in self.subscription_tiers:
                return {"success": False, "error": "Invalid subscription tier"}
            
            # Generate customer ID
            customer_id = str(uuid.uuid4())
            
            # Hash password
            password_hash = generate_password_hash(password)
            
            # Default usage stats and preferences
            usage_stats = {
                "interactions_this_month": 0,
                "tokens_used_this_month": 0,
                "total_interactions": 0,
                "average_satisfaction": 0.0
            }
            
            preferences = {
                "interface_theme": "light",
                "response_detail_level": "standard",
                "enable_notifications": True,
                "preferred_features": []
            }
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO customers 
                (customer_id, email, name, password_hash, subscription_tier, 
                 created_at, usage_stats, preferences)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                customer_id,
                email,
                name,
                password_hash,
                subscription_tier,
                datetime.now().isoformat(),
                json.dumps(usage_stats),
                json.dumps(preferences)
            ))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "customer_id": customer_id,
                "message": "Customer registered successfully"
            }
            
        except sqlite3.IntegrityError:
            return {"success": False, "error": "Email already registered"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def authenticate_customer(self, email: str, password: str) -> Dict[str, Any]:
        """Authenticate customer login"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT customer_id, password_hash, subscription_tier, name
                FROM customers WHERE email = ?
            """, [email])
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return {"success": False, "error": "Customer not found"}
            
            customer_id, password_hash, subscription_tier, name = result
            
            if not check_password_hash(password_hash, password):
                return {"success": False, "error": "Invalid password"}
            
            # Create session
            session_id = str(uuid.uuid4())
            expires_at = datetime.now() + timedelta(hours=24)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO customer_sessions 
                (session_id, customer_id, created_at, expires_at)
                VALUES (?, ?, ?, ?)
            """, (session_id, customer_id, datetime.now().isoformat(), expires_at.isoformat()))
            
            # Update last active
            cursor.execute("""
                UPDATE customers SET last_active = ? WHERE customer_id = ?
            """, [datetime.now().isoformat(), customer_id])
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "session_id": session_id,
                "customer_id": customer_id,
                "name": name,
                "subscription_tier": subscription_tier
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def process_agi_request(self, customer_id: str, interaction_type: str, 
                           input_data: str) -> Dict[str, Any]:
        """Process AGI request from customer"""
        try:
            # Get customer info
            customer_info = self._get_customer_info(customer_id)
            if not customer_info:
                return {"success": False, "error": "Customer not found"}
            
            # Check subscription limits
            limit_check = self._check_usage_limits(customer_id, customer_info["subscription_tier"])
            if not limit_check["allowed"]:
                return {
                    "success": False, 
                    "error": limit_check["reason"],
                    "upgrade_suggested": True
                }
            
            # Process request with AGI system
            start_time = datetime.now()
            agi_result = self._call_agi_system(interaction_type, input_data, customer_info)
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Calculate cost
            tokens_used = agi_result.get("tokens_used", 0)
            tier_info = self.subscription_tiers[customer_info["subscription_tier"]]
            cost = tokens_used * tier_info["cost_per_token"]
            
            # Record interaction
            interaction_id = str(uuid.uuid4())
            self._record_interaction(
                interaction_id, customer_id, interaction_type, 
                input_data, agi_result.get("output", ""), processing_time,
                agi_result.get("success", False), tokens_used, cost
            )
            
            # Update usage stats
            self._update_usage_stats(customer_id, tokens_used, cost)
            
            return {
                "success": True,
                "interaction_id": interaction_id,
                "result": agi_result.get("output", ""),
                "processing_time": processing_time,
                "tokens_used": tokens_used,
                "cost": cost,
                "remaining_quota": self._get_remaining_quota(customer_id)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _get_customer_info(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Get customer information"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT email, name, subscription_tier, usage_stats, preferences
                FROM customers WHERE customer_id = ?
            """, [customer_id])
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                email, name, subscription_tier, usage_stats, preferences = result
                return {
                    "email": email,
                    "name": name,
                    "subscription_tier": subscription_tier,
                    "usage_stats": json.loads(usage_stats) if usage_stats else {},
                    "preferences": json.loads(preferences) if preferences else {}
                }
            return None
            
        except Exception as e:
            print(f"👥 Error getting customer info: {e}")
            return None
    
    def _check_usage_limits(self, customer_id: str, subscription_tier: str) -> Dict[str, Any]:
        """Check if customer is within usage limits"""
        try:
            tier_info = self.subscription_tiers[subscription_tier]
            monthly_limit = tier_info["monthly_limit"]
            
            # Get current month usage
            current_month = datetime.now().strftime('%Y-%m')
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT COUNT(*), COALESCE(SUM(tokens_used), 0)
                FROM agi_interactions 
                WHERE customer_id = ? AND strftime('%Y-%m', timestamp) = ?
            """, [customer_id, current_month])
            
            interaction_count, tokens_used = cursor.fetchone()
            conn.close()
            
            if interaction_count >= monthly_limit:
                return {
                    "allowed": False,
                    "reason": f"Monthly interaction limit ({monthly_limit}) reached",
                    "current_usage": interaction_count,
                    "limit": monthly_limit
                }
            
            return {
                "allowed": True,
                "current_usage": interaction_count,
                "limit": monthly_limit,
                "remaining": monthly_limit - interaction_count
            }
            
        except Exception as e:
            return {"allowed": False, "reason": f"Usage check error: {str(e)}"}
    
    def _call_agi_system(self, interaction_type: str, input_data: str, 
                        customer_info: Dict[str, Any]) -> Dict[str, Any]:
        """Call AGI system for processing"""
        try:
            from asis_agi_production import UnifiedAGIControllerProduction
            
            agi = UnifiedAGIControllerProduction()
            
            # Prepare request based on interaction type
            if interaction_type == "reasoning":
                result = agi.process_cross_domain_reasoning(input_data)
            elif interaction_type == "consciousness":
                result = agi.get_consciousness_insights(input_data)
            elif interaction_type == "analysis":
                result = agi.analyze_complex_problem(input_data)
            elif interaction_type == "creative":
                result = agi.generate_creative_solution(input_data)
            else:
                result = agi.process_general_query(input_data)
            
            agi.shutdown_agi_system()
            
            # Estimate tokens used (simplified)
            tokens_used = len(input_data.split()) + len(str(result).split())
            
            return {
                "success": True,
                "output": str(result),
                "tokens_used": tokens_used
            }
            
        except Exception as e:
            return {
                "success": False,
                "output": f"AGI processing error: {str(e)}",
                "tokens_used": 0
            }
    
    def _record_interaction(self, interaction_id: str, customer_id: str, 
                           interaction_type: str, input_data: str, output_data: str,
                           processing_time: float, success: bool, tokens_used: int, cost: float):
        """Record customer interaction"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO agi_interactions 
                (interaction_id, customer_id, timestamp, interaction_type,
                 input_data, output_data, processing_time, success, tokens_used, cost)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                interaction_id, customer_id, datetime.now().isoformat(),
                interaction_type, input_data, output_data, processing_time,
                success, tokens_used, cost
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"👥 Error recording interaction: {e}")
    
    def _update_usage_stats(self, customer_id: str, tokens_used: int, cost: float):
        """Update customer usage statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get current stats
            cursor.execute("SELECT usage_stats FROM customers WHERE customer_id = ?", [customer_id])
            result = cursor.fetchone()
            
            if result:
                current_stats = json.loads(result[0]) if result[0] else {}
                
                # Update stats
                current_stats["interactions_this_month"] = current_stats.get("interactions_this_month", 0) + 1
                current_stats["tokens_used_this_month"] = current_stats.get("tokens_used_this_month", 0) + tokens_used
                current_stats["total_interactions"] = current_stats.get("total_interactions", 0) + 1
                current_stats["total_cost"] = current_stats.get("total_cost", 0) + cost
                
                # Update database
                cursor.execute("""
                    UPDATE customers SET usage_stats = ? WHERE customer_id = ?
                """, [json.dumps(current_stats), customer_id])
                
                conn.commit()
            
            conn.close()
            
        except Exception as e:
            print(f"👥 Error updating usage stats: {e}")
    
    def _get_remaining_quota(self, customer_id: str) -> int:
        """Get remaining quota for customer"""
        try:
            customer_info = self._get_customer_info(customer_id)
            if not customer_info:
                return 0
            
            tier_info = self.subscription_tiers[customer_info["subscription_tier"]]
            monthly_limit = tier_info["monthly_limit"]
            
            usage_stats = customer_info["usage_stats"]
            used_this_month = usage_stats.get("interactions_this_month", 0)
            
            return max(0, monthly_limit - used_this_month)
            
        except Exception as e:
            print(f"👥 Error getting remaining quota: {e}")
            return 0
    
    def get_customer_dashboard(self, customer_id: str) -> Dict[str, Any]:
        """Get customer dashboard data"""
        try:
            customer_info = self._get_customer_info(customer_id)
            if not customer_info:
                return {"error": "Customer not found"}
            
            # Get recent interactions
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT interaction_type, timestamp, success, tokens_used, cost
                FROM agi_interactions 
                WHERE customer_id = ? 
                ORDER BY timestamp DESC 
                LIMIT 10
            """, [customer_id])
            
            recent_interactions = [
                {
                    "type": row[0],
                    "timestamp": row[1],
                    "success": row[2],
                    "tokens_used": row[3],
                    "cost": row[4]
                }
                for row in cursor.fetchall()
            ]
            
            # Get usage summary
            current_month = datetime.now().strftime('%Y-%m')
            cursor.execute("""
                SELECT COUNT(*), COALESCE(SUM(tokens_used), 0), COALESCE(SUM(cost), 0)
                FROM agi_interactions 
                WHERE customer_id = ? AND strftime('%Y-%m', timestamp) = ?
            """, [customer_id, current_month])
            
            month_interactions, month_tokens, month_cost = cursor.fetchone()
            
            conn.close()
            
            tier_info = self.subscription_tiers[customer_info["subscription_tier"]]
            
            return {
                "customer_info": {
                    "name": customer_info["name"],
                    "email": customer_info["email"],
                    "subscription_tier": customer_info["subscription_tier"],
                    "tier_name": tier_info["name"]
                },
                "usage_summary": {
                    "interactions_this_month": month_interactions,
                    "tokens_used_this_month": month_tokens,
                    "cost_this_month": month_cost,
                    "monthly_limit": tier_info["monthly_limit"],
                    "remaining_quota": tier_info["monthly_limit"] - month_interactions
                },
                "recent_interactions": recent_interactions,
                "subscription_features": tier_info["features"],
                "recommendations": self._get_recommendations(customer_id, customer_info)
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _get_recommendations(self, customer_id: str, customer_info: Dict[str, Any]) -> List[str]:
        """Get personalized recommendations for customer"""
        recommendations = []
        
        usage_stats = customer_info.get("usage_stats", {})
        current_tier = customer_info["subscription_tier"]
        
        # Usage-based recommendations
        interactions_this_month = usage_stats.get("interactions_this_month", 0)
        monthly_limit = self.subscription_tiers[current_tier]["monthly_limit"]
        
        if interactions_this_month > monthly_limit * 0.8:
            if current_tier != "enterprise":
                recommendations.append("Consider upgrading your plan for higher limits")
        
        if interactions_this_month < monthly_limit * 0.2:
            recommendations.append("Explore more AGI features to maximize your subscription")
        
        # Feature-based recommendations
        if current_tier == "free":
            recommendations.append("Upgrade to Basic plan for cross-domain reasoning capabilities")
        elif current_tier == "basic":
            recommendations.append("Try Professional plan for consciousness insights and advanced analysis")
        
        return recommendations
    
    def submit_feedback(self, customer_id: str, feedback_type: str, 
                       rating: int, message: str) -> Dict[str, Any]:
        """Submit customer feedback"""
        try:
            feedback_id = str(uuid.uuid4())
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO customer_feedback 
                (feedback_id, customer_id, timestamp, feedback_type, rating, message)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                feedback_id, customer_id, datetime.now().isoformat(),
                feedback_type, rating, message
            ))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "feedback_id": feedback_id,
                "message": "Feedback submitted successfully"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

# Flask application for customer interface
def create_customer_app():
    """Create Flask application for customer interface"""
    app = Flask(__name__)
    app.secret_key = "agi_customer_interface_secret_key"
    
    customer_interface = CustomerAGIInterface()
    
    @app.route('/')
    def home():
        """Home page"""
        return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>ASIS AGI - Customer Portal</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; color: #333; margin-bottom: 30px; }
        .feature { background: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #007bff; }
        .btn { background: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; margin: 5px; }
        .btn:hover { background: #0056b3; }
        .tier { border: 1px solid #ddd; padding: 20px; margin: 10px 0; border-radius: 8px; }
        .tier.professional { border-color: #28a745; }
        .tier.enterprise { border-color: #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 ASIS AGI Customer Portal</h1>
            <p>Experience Advanced Artificial General Intelligence</p>
        </div>
        
        <div class="feature">
            <h3>🚀 AGI Capabilities</h3>
            <ul>
                <li><strong>Cross-Domain Reasoning:</strong> Solve complex problems across multiple domains</li>
                <li><strong>Consciousness Insights:</strong> Get deep understanding of consciousness and awareness</li>
                <li><strong>Advanced Analysis:</strong> Comprehensive analysis of complex scenarios</li>
                <li><strong>Creative Solutions:</strong> Generate innovative solutions to challenges</li>
            </ul>
        </div>
        
        <h2>📊 Subscription Plans</h2>
        
        <div class="tier">
            <h3>🆓 Free Tier</h3>
            <p><strong>$0/month</strong> - 100 interactions/month</p>
            <p>Perfect for trying out basic AGI capabilities</p>
        </div>
        
        <div class="tier">
            <h3>⭐ Basic Plan</h3>
            <p><strong>$29.99/month</strong> - 1,000 interactions/month</p>
            <p>Includes cross-domain reasoning and priority support</p>
        </div>
        
        <div class="tier professional">
            <h3>💎 Professional Plan</h3>
            <p><strong>$99.99/month</strong> - 10,000 interactions/month</p>
            <p>Advanced analysis, consciousness insights, and premium features</p>
        </div>
        
        <div class="tier enterprise">
            <h3>🏢 Enterprise Plan</h3>
            <p><strong>$499.99/month</strong> - 100,000 interactions/month</p>
            <p>All features, custom models, and dedicated support</p>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="/register" class="btn">🚀 Get Started</a>
            <a href="/login" class="btn">🔐 Login</a>
            <a href="/demo" class="btn">🎯 Try Demo</a>
        </div>
    </div>
</body>
</html>
        """)
    
    @app.route('/api/register', methods=['POST'])
    def register():
        """Customer registration API"""
        data = request.get_json()
        result = customer_interface.register_customer(
            data.get('email'),
            data.get('name'), 
            data.get('password'),
            data.get('subscription_tier', 'free')
        )
        return jsonify(result)
    
    @app.route('/api/login', methods=['POST'])
    def login():
        """Customer login API"""
        data = request.get_json()
        result = customer_interface.authenticate_customer(
            data.get('email'),
            data.get('password')
        )
        if result.get('success'):
            session['customer_id'] = result['customer_id']
            session['session_id'] = result['session_id']
        return jsonify(result)
    
    @app.route('/api/agi-request', methods=['POST'])
    def agi_request():
        """Process AGI request API"""
        if 'customer_id' not in session:
            return jsonify({"success": False, "error": "Not authenticated"}), 401
        
        data = request.get_json()
        result = customer_interface.process_agi_request(
            session['customer_id'],
            data.get('interaction_type'),
            data.get('input_data')
        )
        return jsonify(result)
    
    @app.route('/api/dashboard')
    def dashboard():
        """Customer dashboard API"""
        if 'customer_id' not in session:
            return jsonify({"error": "Not authenticated"}), 401
        
        dashboard_data = customer_interface.get_customer_dashboard(session['customer_id'])
        return jsonify(dashboard_data)
    
    @app.route('/api/feedback', methods=['POST'])
    def feedback():
        """Submit feedback API"""
        if 'customer_id' not in session:
            return jsonify({"success": False, "error": "Not authenticated"}), 401
        
        data = request.get_json()
        result = customer_interface.submit_feedback(
            session['customer_id'],
            data.get('feedback_type'),
            data.get('rating'),
            data.get('message')
        )
        return jsonify(result)
    
    return app

def main():
    """Main customer interface function"""
    print("👥 ASIS AGI Customer Interface System")
    print("=" * 40)
    
    # Create customer interface
    customer_interface = CustomerAGIInterface()
    
    # Create and run Flask app
    app = create_customer_app()
    
    print("👥 Starting customer interface server...")
    print("👥 Available at: http://localhost:5001")
    print("👥 Features:")
    print("   - Customer registration and authentication")
    print("   - AGI interaction interface")
    print("   - Subscription management")
    print("   - Usage tracking and analytics")
    print("   - Customer dashboard")
    print("   - Feedback system")
    
    app.run(host='0.0.0.0', port=5001, debug=False)

if __name__ == "__main__":
    main()
