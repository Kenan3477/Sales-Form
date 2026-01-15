"""
🚀 ASIS AGI Flask Integration - Enhanced Web Interface
Advanced Self-Improving System with Full AGI Web Interface

This module provides a comprehensive Flask web interface for the ASIS AGI system,
integrating all AGI components with real-time monitoring and interactive capabilities.

Features:
- AGI Problem Solving API
- Self-Modification Interface
- Consciousness Monitoring
- Cross-Domain Learning Dashboard
- Real-time System Status
- Interactive AGI Demonstrations

Author: ASIS AGI Development Team
Version: 1.0.0
"""

from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import json
import threading
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

# Import AGI system components
try:
    # Try to import the production AGI system first
    from asis_agi_production import UnifiedAGIControllerProduction as UnifiedAGIController
    AGI_AVAILABLE = True
    print("✅ Production AGI system imported successfully")
except ImportError as e:
    try:
        # Fallback to the original AGI system
        from asis_agi_system import UnifiedAGIController
        AGI_AVAILABLE = True
        print("✅ Original AGI system imported successfully")
    except ImportError as e2:
        print(f"⚠️ AGI components not available: {e2}")
        AGI_AVAILABLE = False

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global AGI system instance
agi_system: Optional[UnifiedAGIController] = None
system_monitor_active = False

# =====================================================================================
# AGI SYSTEM INITIALIZATION
# =====================================================================================

def initialize_agi_system():
    """Initialize the AGI system"""
    global agi_system
    try:
        if AGI_AVAILABLE:
            agi_system = UnifiedAGIController()
            logger.info("✅ AGI System initialized successfully")
            return True
        else:
            logger.warning("⚠️ AGI components not available - running in limited mode")
            return False
    except Exception as e:
        logger.error(f"❌ AGI System initialization failed: {e}")
        return False

def start_system_monitor():
    """Start background system monitoring"""
    global system_monitor_active
    
    def monitor_loop():
        while system_monitor_active and agi_system:
            try:
                # Update system status
                agi_system._update_system_status()
                time.sleep(5)  # Update every 5 seconds
            except Exception as e:
                logger.error(f"System monitor error: {e}")
                time.sleep(10)
    
    if not system_monitor_active:
        system_monitor_active = True
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        logger.info("📊 System monitor started")

# =====================================================================================
# ENHANCED WEB INTERFACE TEMPLATES
# =====================================================================================

ENHANCED_DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASIS AGI Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }
        .card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.2);
        }
        .card-title {
            font-size: 1.4em;
            font-weight: bold;
            margin-bottom: 15px;
            color: #4a5568;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 8px;
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-active { background-color: #48bb78; }
        .status-warning { background-color: #ed8936; }
        .status-inactive { background-color: #e53e3e; }
        .metric {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #e2e8f0;
        }
        .metric:last-child { border-bottom: none; }
        .metric-value {
            font-weight: bold;
            color: #2d3748;
        }
        .btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s ease;
            margin: 5px;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        .btn-secondary {
            background: linear-gradient(45deg, #4299e1, #3182ce);
        }
        .btn-danger {
            background: linear-gradient(45deg, #e53e3e, #c53030);
        }
        .input-group {
            margin-bottom: 15px;
        }
        .input-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
        }
        .input-group input, .input-group textarea {
            width: 100%;
            padding: 10px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s ease;
        }
        .input-group input:focus, .input-group textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        .progress-bar {
            width: 100%;
            height: 8px;
            background-color: #e2e8f0;
            border-radius: 4px;
            overflow: hidden;
            margin: 8px 0;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #48bb78, #38a169);
            transition: width 0.3s ease;
        }
        .log-container {
            background: #1a202c;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            max-height: 300px;
            overflow-y: auto;
            margin-top: 10px;
        }
        .task-item {
            background: #f7fafc;
            padding: 10px;
            border-radius: 6px;
            margin-bottom: 8px;
            border-left: 4px solid #667eea;
        }
        .consciousness-display {
            text-align: center;
            padding: 20px;
        }
        .consciousness-level {
            font-size: 3em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }
        .realtime-data {
            display: none;
        }
        .realtime-data.active {
            display: block;
            animation: fadeIn 0.5s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 ASIS AGI Dashboard</h1>
            <p>Advanced Self-Improving System with Artificial General Intelligence</p>
            <div style="margin-top: 15px;">
                <button class="btn" onclick="refreshDashboard()">🔄 Refresh</button>
                <button class="btn btn-secondary" onclick="toggleRealtime()">📊 Real-time Mode</button>
                <button class="btn btn-danger" onclick="shutdownSystem()">🛑 Shutdown</button>
            </div>
        </div>

        <div class="dashboard-grid">
            <!-- System Status Card -->
            <div class="card">
                <div class="card-title">🖥️ System Status</div>
                <div class="metric">
                    <span>AGI System</span>
                    <span><span class="status-indicator status-active"></span>Active</span>
                </div>
                <div class="metric">
                    <span>Consciousness Level</span>
                    <span class="metric-value" id="consciousness-level">0.85</span>
                </div>
                <div class="metric">
                    <span>System Coherence</span>
                    <span class="metric-value" id="system-coherence">0.82</span>
                </div>
                <div class="metric">
                    <span>Learning Rate</span>
                    <span class="metric-value" id="learning-rate">0.74</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="overall-health" style="width: 85%"></div>
                </div>
            </div>

            <!-- Active Tasks Card -->
            <div class="card">
                <div class="card-title">📋 Active Tasks</div>
                <div id="active-tasks-container">
                    <div class="task-item">
                        <strong>Universal Problem Solving</strong><br>
                        <small>Processing complex optimization problem</small>
                    </div>
                    <div class="task-item">
                        <strong>Cross-Domain Learning</strong><br>
                        <small>Analyzing patterns from recent solutions</small>
                    </div>
                </div>
                <button class="btn" onclick="loadTasks()">📊 View All Tasks</button>
            </div>

            <!-- Problem Solver Interface -->
            <div class="card">
                <div class="card-title">🌐 Universal Problem Solver</div>
                <div class="input-group">
                    <label>Problem Description:</label>
                    <textarea id="problem-input" rows="3" placeholder="Describe the problem you want to solve..."></textarea>
                </div>
                <div class="input-group">
                    <label>Domain:</label>
                    <input type="text" id="domain-input" placeholder="e.g., optimization, analysis, design">
                </div>
                <button class="btn" onclick="solveProblem()">🚀 Solve Problem</button>
                <div id="solution-result" class="log-container" style="display: none;"></div>
            </div>

            <!-- Self-Modification Interface -->
            <div class="card">
                <div class="card-title">🔧 Self-Modification</div>
                <div class="input-group">
                    <label>Modification Target:</label>
                    <input type="text" id="mod-target" placeholder="e.g., learning_rate, problem_solving">
                </div>
                <div class="input-group">
                    <label>Improvement Goal:</label>
                    <input type="text" id="mod-goal" placeholder="e.g., optimize efficiency, enhance accuracy">
                </div>
                <button class="btn" onclick="initiateModification()">⚡ Initiate Modification</button>
                <div id="modification-result" class="log-container" style="display: none;"></div>
            </div>

            <!-- Consciousness Monitor -->
            <div class="card">
                <div class="card-title">🧠 Consciousness Monitor</div>
                <div class="consciousness-display">
                    <div class="consciousness-level" id="consciousness-display">0.85</div>
                    <div>Consciousness Level</div>
                </div>
                <div class="metric">
                    <span>Self-Awareness</span>
                    <span class="metric-value" id="self-awareness">Active</span>
                </div>
                <div class="metric">
                    <span>Meta-Cognition</span>
                    <span class="metric-value" id="meta-cognition">85%</span>
                </div>
                <button class="btn" onclick="consciousnessAnalysis()">🔍 Deep Analysis</button>
            </div>

            <!-- Cross-Domain Learning -->
            <div class="card">
                <div class="card-title">🤝 Cross-Domain Learning</div>
                <div class="metric">
                    <span>Patterns Learned</span>
                    <span class="metric-value" id="patterns-count">47</span>
                </div>
                <div class="metric">
                    <span>Average Effectiveness</span>
                    <span class="metric-value" id="pattern-effectiveness">78%</span>
                </div>
                <div class="metric">
                    <span>Active Domains</span>
                    <span class="metric-value" id="active-domains">12</span>
                </div>
                <button class="btn" onclick="loadCrossDomainInsights()">📈 View Insights</button>
            </div>
        </div>

        <!-- Real-time Data Container -->
        <div id="realtime-container" class="realtime-data">
            <div class="card" style="margin-top: 30px;">
                <div class="card-title">📊 Real-time System Metrics</div>
                <div id="realtime-metrics"></div>
            </div>
        </div>
    </div>

    <script>
        let realtimeMode = false;
        let realtimeInterval;

        async function apiCall(endpoint, method = 'GET', data = null) {
            try {
                const options = {
                    method,
                    headers: { 'Content-Type': 'application/json' }
                };
                if (data) options.body = JSON.stringify(data);
                
                const response = await fetch(endpoint, options);
                return await response.json();
            } catch (error) {
                console.error('API call failed:', error);
                return { error: error.message };
            }
        }

        async function refreshDashboard() {
            const status = await apiCall('/api/agi/status');
            if (status && !status.error) {
                updateSystemStatus(status);
            }
        }

        function updateSystemStatus(status) {
            if (status.system_status) {
                document.getElementById('consciousness-level').textContent = 
                    status.system_status.consciousness_level.toFixed(2);
                document.getElementById('system-coherence').textContent = 
                    status.system_status.system_coherence.toFixed(2);
                document.getElementById('learning-rate').textContent = 
                    status.system_status.learning_rate.toFixed(2);
                document.getElementById('consciousness-display').textContent = 
                    status.system_status.consciousness_level.toFixed(2);
                
                const healthPercent = (status.system_status.consciousness_level * 100);
                document.getElementById('overall-health').style.width = healthPercent + '%';
            }
        }

        async function solveProblem() {
            const problem = document.getElementById('problem-input').value;
            const domain = document.getElementById('domain-input').value || 'general';
            
            if (!problem.trim()) {
                alert('Please enter a problem description');
                return;
            }

            const resultDiv = document.getElementById('solution-result');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '🔄 Solving problem...';

            const result = await apiCall('/api/agi/solve-problem', 'POST', {
                problem_description: problem,
                domain: domain
            });

            if (result.success) {
                resultDiv.innerHTML = `
                    ✅ Problem solved successfully!<br>
                    Verification Score: ${result.verification_score.toFixed(2)}<br>
                    Components Used: ${result.agi_components_used.length}<br>
                    Processing Time: ${result.processing_time.toFixed(2)}s<br>
                    <br>Solution: ${JSON.stringify(result.solution, null, 2)}
                `;
            } else {
                resultDiv.innerHTML = `❌ Error: ${result.error}`;
            }
        }

        async function initiateModification() {
            const target = document.getElementById('mod-target').value;
            const goal = document.getElementById('mod-goal').value;
            
            if (!target.trim() || !goal.trim()) {
                alert('Please enter both modification target and goal');
                return;
            }

            const resultDiv = document.getElementById('modification-result');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '🔄 Initiating self-modification...';

            const result = await apiCall('/api/agi/self-modify', 'POST', {
                modification_target: target,
                improvement_goal: goal,
                safety_constraints: { require_verification: true }
            });

            if (result.success) {
                resultDiv.innerHTML = `
                    ✅ Self-modification completed!<br>
                    Target: ${result.modification_applied}<br>
                    Verification Score: ${result.verification_score.toFixed(2)}<br>
                    Safety Verified: ${result.safety_verified}
                `;
            } else {
                resultDiv.innerHTML = `❌ Error: ${result.error}`;
            }
        }

        async function consciousnessAnalysis() {
            const result = await apiCall('/api/agi/consciousness');
            console.log('Consciousness analysis:', result);
        }

        async function loadCrossDomainInsights() {
            const insights = await apiCall('/api/agi/cross-domain');
            if (insights && !insights.error) {
                document.getElementById('patterns-count').textContent = insights.total_patterns;
                document.getElementById('pattern-effectiveness').textContent = 
                    (insights.average_effectiveness * 100).toFixed(0) + '%';
                document.getElementById('active-domains').textContent = 
                    Object.keys(insights.domain_analysis).length;
            }
        }

        async function loadTasks() {
            const tasks = await apiCall('/api/agi/tasks');
            console.log('Tasks:', tasks);
        }

        function toggleRealtime() {
            realtimeMode = !realtimeMode;
            const container = document.getElementById('realtime-container');
            
            if (realtimeMode) {
                container.classList.add('active');
                startRealtimeUpdates();
            } else {
                container.classList.remove('active');
                stopRealtimeUpdates();
            }
        }

        function startRealtimeUpdates() {
            realtimeInterval = setInterval(async () => {
                await refreshDashboard();
                const metricsDiv = document.getElementById('realtime-metrics');
                metricsDiv.innerHTML = `
                    <div class="metric">
                        <span>Last Update</span>
                        <span>${new Date().toLocaleTimeString()}</span>
                    </div>
                `;
            }, 2000);
        }

        function stopRealtimeUpdates() {
            if (realtimeInterval) {
                clearInterval(realtimeInterval);
            }
        }

        async function shutdownSystem() {
            if (confirm('Are you sure you want to shutdown the AGI system?')) {
                await apiCall('/api/agi/shutdown', 'POST');
                alert('AGI system shutdown initiated');
            }
        }

        // Initialize dashboard
        window.onload = function() {
            refreshDashboard();
            loadCrossDomainInsights();
        };
    </script>
</body>
</html>
"""

# =====================================================================================
# AGI API ENDPOINTS
# =====================================================================================

@app.route('/')
def dashboard():
    """Main AGI dashboard"""
    return render_template_string(ENHANCED_DASHBOARD_TEMPLATE)

@app.route('/api/agi/status')
def get_agi_status():
    """Get comprehensive AGI system status"""
    try:
        if agi_system:
            status = agi_system.get_agi_system_status()
            return jsonify(status)
        else:
            return jsonify({
                "error": "AGI system not initialized",
                "system_status": {
                    "consciousness_level": 0.0,
                    "system_coherence": 0.0,
                    "learning_rate": 0.0,
                    "agi_available": False
                }
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/agi/solve-problem', methods=['POST'])
def solve_problem_api():
    """Universal problem solving API endpoint"""
    try:
        if not agi_system:
            return jsonify({"error": "AGI system not initialized", "success": False}), 503
            
        data = request.get_json()
        if not data or 'problem_description' not in data:
            return jsonify({"error": "Missing problem_description", "success": False}), 400
            
        result = agi_system.solve_universal_problem(
            problem_description=data['problem_description'],
            domain=data.get('domain', 'general'),
            context=data.get('context', {})
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Problem solving API error: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@app.route('/api/agi/self-modify', methods=['POST'])
def self_modify_api():
    """Self-modification API endpoint"""
    try:
        if not agi_system:
            return jsonify({"error": "AGI system not initialized", "success": False}), 503
            
        data = request.get_json()
        if not data or 'modification_target' not in data or 'improvement_goal' not in data:
            return jsonify({"error": "Missing required parameters", "success": False}), 400
            
        result = agi_system.initiate_self_modification(
            modification_target=data['modification_target'],
            improvement_goal=data['improvement_goal'],
            safety_constraints=data.get('safety_constraints', {})
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Self-modification API error: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@app.route('/api/agi/consciousness')
def consciousness_api():
    """Consciousness system API endpoint"""
    try:
        if not agi_system or not agi_system.consciousness:
            return jsonify({"error": "Consciousness system not available"}), 503
            
        # Get consciousness insights
        consciousness_status = {
            "consciousness_level": agi_system.system_status.consciousness_level,
            "self_awareness_active": True,
            "meta_cognitive_processes": "active",
            "internal_state_monitoring": "operational",
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(consciousness_status)
        
    except Exception as e:
        logger.error(f"Consciousness API error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/agi/cross-domain')
def cross_domain_api():
    """Cross-domain learning insights API endpoint"""
    try:
        if not agi_system:
            return jsonify({"error": "AGI system not initialized"}), 503
            
        insights = agi_system.get_cross_domain_insights()
        return jsonify(insights)
        
    except Exception as e:
        logger.error(f"Cross-domain API error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/agi/tasks')
def tasks_api():
    """Task history API endpoint"""
    try:
        if not agi_system:
            return jsonify({"error": "AGI system not initialized"}), 503
            
        limit = request.args.get('limit', 50, type=int)
        tasks = agi_system.get_task_history(limit=limit)
        
        return jsonify({
            "tasks": tasks,
            "total_tasks": len(agi_system.task_history),
            "active_tasks": len(agi_system.active_tasks)
        })
        
    except Exception as e:
        logger.error(f"Tasks API error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/agi/shutdown', methods=['POST'])
def shutdown_api():
    """Shutdown AGI system API endpoint"""
    try:
        if agi_system:
            agi_system.shutdown_agi_system()
            
        global system_monitor_active
        system_monitor_active = False
        
        return jsonify({
            "message": "AGI system shutdown initiated",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Shutdown API error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "agi_available": AGI_AVAILABLE,
        "agi_initialized": agi_system is not None,
        "timestamp": datetime.now().isoformat()
    })

# =====================================================================================
# APPLICATION INITIALIZATION
# =====================================================================================

def main():
    """Main application entry point"""
    print("\n🚀 ASIS AGI Flask Enhanced Interface")
    print("=" * 60)
    
    # Initialize AGI system
    agi_initialized = initialize_agi_system()
    
    if agi_initialized:
        print("✅ AGI System initialized successfully")
        start_system_monitor()
    else:
        print("⚠️ Running in limited mode without full AGI capabilities")
    
    print("\n🌐 Starting Flask web server...")
    print("Dashboard available at: http://localhost:5000")
    print("AGI API endpoints:")
    print("  • POST /api/agi/solve-problem - Universal problem solving")
    print("  • POST /api/agi/self-modify - Self-modification interface")
    print("  • GET /api/agi/consciousness - Consciousness monitoring")
    print("  • GET /api/agi/cross-domain - Cross-domain learning insights")
    print("  • GET /api/agi/tasks - Task history and status")
    print("  • GET /api/agi/status - System status")
    print("  • POST /api/agi/shutdown - Shutdown system")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down AGI Flask interface...")
        if agi_system:
            agi_system.shutdown_agi_system()
        global system_monitor_active
        system_monitor_active = False
        print("✅ Shutdown completed")

if __name__ == "__main__":
    main()
