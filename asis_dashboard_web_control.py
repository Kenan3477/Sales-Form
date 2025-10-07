#!/usr/bin/env python3
"""
ASIS Dashboard Web Control Interface
==================================

Web interface integration for controlling the ASIS Dashboard Enhancer
from within the main ASIS web interface.

Author: ASIS Development Team
Version: 1.0
"""

from flask import Blueprint, request, jsonify, render_template_string
from datetime import datetime
import threading
import time

# Import dashboard components
try:
    from asis_dashboard_enhancer import ASISSystemMonitor, ASISDashboardEnhancer
    from asis_dashboard_control import ASISDashboardController
except ImportError as e:
    print(f"Warning: Dashboard components not available: {e}")

def create_dashboard_control_blueprint():
    """Create Flask blueprint for dashboard control"""
    
    dashboard_bp = Blueprint('dashboard_control', __name__, url_prefix='/dashboard-control')
    
    # Global dashboard controller
    controller = ASISDashboardController()
    
    @dashboard_bp.route('/')
    def dashboard_control_index():
        """Dashboard control interface"""
        return render_template_string(DASHBOARD_CONTROL_TEMPLATE)
    
    @dashboard_bp.route('/api/status')
    def api_status():
        """Get dashboard enhancement status"""
        try:
            status = controller.get_comprehensive_status()
            return jsonify(status)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @dashboard_bp.route('/api/activate', methods=['POST'])
    def api_activate():
        """Activate dashboard enhancer"""
        try:
            result = controller.activate_dashboard_enhancer()
            return jsonify(result)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @dashboard_bp.route('/api/deactivate', methods=['POST'])
    def api_deactivate():
        """Deactivate dashboard enhancer"""
        try:
            result = controller.deactivate_dashboard_enhancer()
            return jsonify(result)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @dashboard_bp.route('/api/restart', methods=['POST'])
    def api_restart():
        """Restart dashboard enhancer"""
        try:
            result = controller.restart_dashboard_enhancer()
            return jsonify(result)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @dashboard_bp.route('/api/test-endpoints')
    def api_test_endpoints():
        """Test dashboard API endpoints"""
        try:
            results = controller.test_dashboard_endpoints()
            return jsonify(results)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return dashboard_bp

# Web interface template
DASHBOARD_CONTROL_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASIS Dashboard Control</title>
    <style>
        :root {
            --primary-green: #00ff88;
            --bg-primary: #0a0a0a;
            --bg-secondary: #1a1a1a;
            --bg-tertiary: #1e1e1e;
            --text-primary: #e0e0e0;
            --text-secondary: #ccc;
            --border-color: #333;
            --warning-color: #ffaa00;
            --error-color: #ff4444;
            --success-color: #00ff88;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: var(--bg-tertiary);
            border-radius: 12px;
            border: 1px solid var(--border-color);
        }
        
        .header h1 {
            margin: 0;
            color: var(--primary-green);
            font-size: 2.5em;
        }
        
        .header p {
            margin: 10px 0 0 0;
            color: var(--text-secondary);
        }
        
        .control-panel {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .control-button {
            padding: 20px;
            background: var(--bg-secondary);
            border: 2px solid var(--border-color);
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
            font-size: 16px;
            font-weight: bold;
        }
        
        .control-button:hover {
            border-color: var(--primary-green);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 255, 136, 0.2);
        }
        
        .control-button.activate {
            background: linear-gradient(135deg, #1a4a3a, #2a5a4a);
        }
        
        .control-button.deactivate {
            background: linear-gradient(135deg, #4a1a1a, #5a2a2a);
        }
        
        .control-button.restart {
            background: linear-gradient(135deg, #4a3a1a, #5a4a2a);
        }
        
        .control-button.test {
            background: linear-gradient(135deg, #1a1a4a, #2a2a5a);
        }
        
        .status-panel {
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 30px;
        }
        
        .status-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid var(--border-color);
        }
        
        .status-item:last-child {
            border-bottom: none;
        }
        
        .status-label {
            font-weight: bold;
        }
        
        .status-value {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
        }
        
        .status-active {
            background: rgba(0, 255, 136, 0.2);
            color: var(--success-color);
        }
        
        .status-inactive {
            background: rgba(255, 68, 68, 0.2);
            color: var(--error-color);
        }
        
        .status-warning {
            background: rgba(255, 170, 0, 0.2);
            color: var(--warning-color);
        }
        
        .log-panel {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            height: 300px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 14px;
        }
        
        .log-entry {
            margin: 5px 0;
            padding: 5px;
            border-radius: 4px;
        }
        
        .log-info {
            color: var(--text-secondary);
        }
        
        .log-success {
            color: var(--success-color);
        }
        
        .log-error {
            color: var(--error-color);
        }
        
        .log-warning {
            color: var(--warning-color);
        }
        
        .loading {
            opacity: 0.6;
            pointer-events: none;
        }
        
        .navigation {
            text-align: center;
            margin-top: 30px;
        }
        
        .nav-link {
            display: inline-block;
            margin: 0 15px;
            padding: 10px 20px;
            background: var(--bg-secondary);
            color: var(--text-primary);
            text-decoration: none;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
        }
        
        .nav-link:hover {
            border-color: var(--primary-green);
            color: var(--primary-green);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 ASIS Dashboard Control</h1>
            <p>Enhanced Dashboard System Management Interface</p>
        </div>
        
        <div class="control-panel">
            <div class="control-button activate" onclick="activateDashboard()">
                <div style="font-size: 2em; margin-bottom: 10px;">🚀</div>
                <div>Activate</div>
                <div style="font-size: 12px; margin-top: 5px;">Start enhanced monitoring</div>
            </div>
            
            <div class="control-button deactivate" onclick="deactivateDashboard()">
                <div style="font-size: 2em; margin-bottom: 10px;">🛑</div>
                <div>Deactivate</div>
                <div style="font-size: 12px; margin-top: 5px;">Stop monitoring system</div>
            </div>
            
            <div class="control-button restart" onclick="restartDashboard()">
                <div style="font-size: 2em; margin-bottom: 10px;">🔄</div>
                <div>Restart</div>
                <div style="font-size: 12px; margin-top: 5px;">Restart dashboard enhancer</div>
            </div>
            
            <div class="control-button test" onclick="testEndpoints()">
                <div style="font-size: 2em; margin-bottom: 10px;">🧪</div>
                <div>Test</div>
                <div style="font-size: 12px; margin-top: 5px;">Test API endpoints</div>
            </div>
        </div>
        
        <div class="status-panel">
            <h3 style="margin-top: 0; color: var(--primary-green);">📊 System Status</h3>
            
            <div class="status-item">
                <span class="status-label">ASIS Server</span>
                <span class="status-value status-inactive" id="server-status">Checking...</span>
            </div>
            
            <div class="status-item">
                <span class="status-label">Dashboard Enhancer</span>
                <span class="status-value status-inactive" id="dashboard-status">Checking...</span>
            </div>
            
            <div class="status-item">
                <span class="status-label">System Monitor</span>
                <span class="status-value status-inactive" id="monitor-status">Checking...</span>
            </div>
            
            <div class="status-item">
                <span class="status-label">API Endpoints</span>
                <span class="status-value status-inactive" id="api-status">Checking...</span>
            </div>
            
            <div class="status-item">
                <span class="status-label">Last Update</span>
                <span class="status-value" id="last-update" style="background: var(--bg-primary);">Never</span>
            </div>
        </div>
        
        <div style="margin-bottom: 20px;">
            <h3 style="color: var(--primary-green); margin-bottom: 15px;">📋 Activity Log</h3>
        </div>
        
        <div class="log-panel" id="activity-log">
            <div class="log-entry log-info">[Init] Dashboard control interface loaded</div>
            <div class="log-entry log-info">[Init] Checking system status...</div>
        </div>
        
        <div class="navigation">
            <a href="/" class="nav-link">🏠 Main Dashboard</a>
            <a href="/chat" class="nav-link">💬 Chat Interface</a>
            <a href="#" class="nav-link" onclick="refreshStatus()">🔄 Refresh Status</a>
        </div>
    </div>

    <script>
        let isLoading = false;
        
        function addLogEntry(message, type = 'info') {
            const log = document.getElementById('activity-log');
            const timestamp = new Date().toLocaleTimeString();
            const entry = document.createElement('div');
            entry.className = `log-entry log-${type}`;
            entry.textContent = `[${timestamp}] ${message}`;
            log.appendChild(entry);
            log.scrollTop = log.scrollHeight;
            
            // Keep only last 50 entries
            while (log.children.length > 50) {
                log.removeChild(log.firstChild);
            }
        }
        
        function setLoading(loading) {
            isLoading = loading;
            const buttons = document.querySelectorAll('.control-button');
            buttons.forEach(button => {
                if (loading) {
                    button.classList.add('loading');
                } else {
                    button.classList.remove('loading');
                }
            });
        }
        
        function updateStatus(status) {
            try {
                // Update server status
                const serverElement = document.getElementById('server-status');
                if (status.asis_server.server_available) {
                    serverElement.textContent = 'Running';
                    serverElement.className = 'status-value status-active';
                } else {
                    serverElement.textContent = 'Not Running';
                    serverElement.className = 'status-value status-inactive';
                }
                
                // Update dashboard status
                const dashboardElement = document.getElementById('dashboard-status');
                if (status.dashboard_enhancer.enhanced_dashboard) {
                    dashboardElement.textContent = status.dashboard_enhancer.status.toUpperCase();
                    dashboardElement.className = 'status-value status-active';
                } else {
                    dashboardElement.textContent = 'Inactive';
                    dashboardElement.className = 'status-value status-inactive';
                }
                
                // Update monitor status
                const monitorElement = document.getElementById('monitor-status');
                if (status.system_monitor.active) {
                    monitorElement.textContent = `Active (${status.system_monitor.metrics_available} metrics)`;
                    monitorElement.className = 'status-value status-active';
                } else {
                    monitorElement.textContent = 'Inactive';
                    monitorElement.className = 'status-value status-inactive';
                }
                
                // Update API status
                const apiElement = document.getElementById('api-status');
                const apiCount = status.integration_status.api_endpoints.length;
                apiElement.textContent = `${apiCount} endpoints`;
                apiElement.className = 'status-value status-active';
                
                // Update last update time
                document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
                
            } catch (error) {
                console.error('Error updating status:', error);
                addLogEntry('Error updating status display', 'error');
            }
        }
        
        async function refreshStatus() {
            try {
                addLogEntry('Checking system status...');
                const response = await fetch('/dashboard-control/api/status');
                const status = await response.json();
                
                if (response.ok) {
                    updateStatus(status);
                    addLogEntry('System status updated', 'success');
                } else {
                    addLogEntry('Failed to get status: ' + status.error, 'error');
                }
            } catch (error) {
                addLogEntry('Error checking status: ' + error.message, 'error');
            }
        }
        
        async function activateDashboard() {
            if (isLoading) return;
            
            setLoading(true);
            addLogEntry('Activating dashboard enhancer...');
            
            try {
                const response = await fetch('/dashboard-control/api/activate', {
                    method: 'POST'
                });
                const result = await response.json();
                
                if (result.success) {
                    addLogEntry('Dashboard enhancer activated successfully!', 'success');
                    setTimeout(refreshStatus, 1000);
                } else {
                    addLogEntry('Activation failed: ' + result.error, 'error');
                }
            } catch (error) {
                addLogEntry('Activation error: ' + error.message, 'error');
            } finally {
                setLoading(false);
            }
        }
        
        async function deactivateDashboard() {
            if (isLoading) return;
            
            setLoading(true);
            addLogEntry('Deactivating dashboard enhancer...');
            
            try {
                const response = await fetch('/dashboard-control/api/deactivate', {
                    method: 'POST'
                });
                const result = await response.json();
                
                if (result.success) {
                    addLogEntry('Dashboard enhancer deactivated', 'success');
                    setTimeout(refreshStatus, 1000);
                } else {
                    addLogEntry('Deactivation failed: ' + result.error, 'error');
                }
            } catch (error) {
                addLogEntry('Deactivation error: ' + error.message, 'error');
            } finally {
                setLoading(false);
            }
        }
        
        async function restartDashboard() {
            if (isLoading) return;
            
            setLoading(true);
            addLogEntry('Restarting dashboard enhancer...');
            
            try {
                const response = await fetch('/dashboard-control/api/restart', {
                    method: 'POST'
                });
                const result = await response.json();
                
                if (result.success) {
                    addLogEntry('Dashboard enhancer restarted successfully!', 'success');
                    setTimeout(refreshStatus, 1000);
                } else {
                    addLogEntry('Restart failed: ' + result.error, 'error');
                }
            } catch (error) {
                addLogEntry('Restart error: ' + error.message, 'error');
            } finally {
                setLoading(false);
            }
        }
        
        async function testEndpoints() {
            if (isLoading) return;
            
            setLoading(true);
            addLogEntry('Testing API endpoints...');
            
            try {
                const response = await fetch('/dashboard-control/api/test-endpoints');
                const result = await response.json();
                
                if (response.ok) {
                    const successRate = result.successful_endpoints / result.total_endpoints;
                    addLogEntry(`Endpoint test completed: ${result.successful_endpoints}/${result.total_endpoints} successful`, 
                               successRate === 1 ? 'success' : 'warning');
                    
                    Object.entries(result.results).forEach(([endpoint, data]) => {
                        if (data.success) {
                            addLogEntry(`✅ ${endpoint} - OK (${data.response_time_ms.toFixed(1)}ms)`, 'success');
                        } else {
                            addLogEntry(`❌ ${endpoint} - Failed`, 'error');
                        }
                    });
                } else {
                    addLogEntry('Endpoint test failed: ' + result.error, 'error');
                }
            } catch (error) {
                addLogEntry('Test error: ' + error.message, 'error');
            } finally {
                setLoading(false);
            }
        }
        
        // Initialize on load
        document.addEventListener('DOMContentLoaded', function() {
            addLogEntry('Dashboard control interface ready', 'success');
            refreshStatus();
            
            // Auto-refresh status every 30 seconds
            setInterval(refreshStatus, 30000);
        });
    </script>
</body>
</html>
'''

def integrate_dashboard_control_with_app(app):
    """Integrate dashboard control with existing Flask app"""
    try:
        dashboard_bp = create_dashboard_control_blueprint()
        app.register_blueprint(dashboard_bp)
        print("✅ Dashboard control interface integrated")
        return True
    except Exception as e:
        print(f"❌ Failed to integrate dashboard control: {e}")
        return False

if __name__ == "__main__":
    # For standalone testing
    from flask import Flask
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-key'
    
    integrate_dashboard_control_with_app(app)
    
    @app.route('/')
    def index():
        return '<h1>ASIS Dashboard Control Test</h1><a href="/dashboard-control/">Dashboard Control</a>'
    
    print("🎯 ASIS Dashboard Control Interface")
    print("Running test server on http://localhost:5001")
    print("Visit http://localhost:5001/dashboard-control/ to test")
    
    app.run(host='0.0.0.0', port=5001, debug=True)