#!/usr/bin/env python3
"""
ASIS Real-Time Web Monitor
Web interface to watch ASIS learn in real-time
"""

from flask import Flask, render_template, jsonify
import sqlite3
import os
import sys
from datetime import datetime
import json
import threading
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

class ASISWebMonitor:
    def __init__(self):
        self.research_db = 'asis_autonomous_research_fixed.db'
        self.config_db = 'asis_automated_research_config.db'
        
    def get_live_data(self):
        """Get current live data for web interface"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'status': 'active'
        }
        
        # Research database stats
        if os.path.exists(self.research_db):
            conn = sqlite3.connect(self.research_db)
            cursor = conn.cursor()
            
            try:
                # Basic counts
                cursor.execute('SELECT COUNT(*) FROM research_findings')
                data['total_findings'] = cursor.fetchone()[0]
                
                cursor.execute('SELECT COUNT(*) FROM research_sessions')
                data['total_sessions'] = cursor.fetchone()[0]
                
                # Recent findings
                cursor.execute('''
                    SELECT title, content, relevance_score, extraction_time 
                    FROM research_findings 
                    ORDER BY extraction_time DESC 
                    LIMIT 10
                ''')
                data['recent_findings'] = [
                    {
                        'title': row[0],
                        'content': row[1][:200] + '...' if len(row[1]) > 200 else row[1],
                        'confidence': row[2],
                        'time': row[3]
                    }
                    for row in cursor.fetchall()
                ]
                
                # Recent sessions
                cursor.execute('''
                    SELECT session_id, topic, start_time, end_time, status, findings_count 
                    FROM research_sessions 
                    ORDER BY start_time DESC 
                    LIMIT 5
                ''')
                data['recent_sessions'] = [
                    {
                        'session_id': row[0],
                        'topic': row[1],
                        'start_time': row[2],
                        'end_time': row[3],
                        'status': row[4],
                        'findings_count': row[5]
                    }
                    for row in cursor.fetchall()
                ]
                
            except Exception as e:
                data['error'] = str(e)
            finally:
                conn.close()
        
        # Config database stats
        if os.path.exists(self.config_db):
            conn = sqlite3.connect(self.config_db)
            cursor = conn.cursor()
            
            try:
                cursor.execute('SELECT COUNT(*) FROM research_topics WHERE active = 1')
                data['active_topics'] = cursor.fetchone()[0]
                
                # Ready topics
                cursor.execute('''
                    SELECT topic, priority, last_researched, frequency_hours
                    FROM research_topics 
                    WHERE active = 1 
                    ORDER BY priority DESC 
                    LIMIT 10
                ''')
                data['topics'] = [
                    {
                        'topic': row[0],
                        'priority': row[1],
                        'last_researched': row[2] or 'Never',
                        'frequency_hours': row[3]
                    }
                    for row in cursor.fetchall()
                ]
                
            except Exception as e:
                data['config_error'] = str(e)
            finally:
                conn.close()
        
        return data

monitor = ASISWebMonitor()

@app.route('/')
def index():
    """Main monitoring dashboard"""
    return render_template('monitor.html')

@app.route('/api/status')
def api_status():
    """API endpoint for live data"""
    return jsonify(monitor.get_live_data())

@app.route('/api/force_research')
def api_force_research():
    """Force a research session"""
    try:
        from asis_autonomous_research_fixed import ASISAutonomousResearch
        research_system = ASISAutonomousResearch()
        
        # Quick research session
        result = research_system.force_research_session(
            "Real-time monitoring test",
            "artificial intelligence machine learning latest developments"
        )
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Create HTML template
html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>ASIS Real-Time Research Monitor</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .content-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        .section {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 15px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .section h3 {
            margin-top: 0;
            color: #FFD700;
        }
        .finding-item, .session-item, .topic-item {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            margin: 10px 0;
            border-radius: 10px;
            border-left: 4px solid #00ff88;
        }
        .timestamp {
            color: #ccc;
            font-size: 0.9em;
        }
        .confidence {
            background: #00ff88;
            color: black;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
        }
        .status {
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
        }
        .status.completed { background: #00ff88; color: black; }
        .status.active { background: #ffaa00; color: black; }
        .status.failed { background: #ff4444; color: white; }
        .force-research {
            background: #ff6b6b;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 1.1em;
            cursor: pointer;
            margin: 20px 0;
            transition: all 0.3s;
        }
        .force-research:hover {
            background: #ff5252;
            transform: translateY(-2px);
        }
        .auto-refresh {
            text-align: center;
            margin: 20px 0;
            color: #ccc;
        }
        @media (max-width: 768px) {
            .content-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 ASIS Real-Time Research Monitor</h1>
            <p>Watch ASIS learn and expand its knowledge autonomously</p>
            <div class="auto-refresh">
                ⏱️ Auto-refreshing every 10 seconds | Last update: <span id="lastUpdate">Loading...</span>
            </div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number" id="totalFindings">-</div>
                <div>Research Findings</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="totalSessions">-</div>
                <div>Research Sessions</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="activeTopics">-</div>
                <div>Active Topics</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="status">🔄</div>
                <div>System Status</div>
            </div>
        </div>
        
        <div style="text-align: center;">
            <button class="force-research" onclick="forceResearch()">
                🔥 Force Research Session
            </button>
        </div>
        
        <div class="content-grid">
            <div class="section">
                <h3>🔍 Latest Discoveries</h3>
                <div id="recentFindings">Loading...</div>
            </div>
            
            <div class="section">
                <h3>🚀 Recent Research Sessions</h3>
                <div id="recentSessions">Loading...</div>
            </div>
        </div>
        
        <div class="content-grid">
            <div class="section">
                <h3>🎯 Research Topics</h3>
                <div id="researchTopics">Loading...</div>
            </div>
            
            <div class="section">
                <h3>📊 System Information</h3>
                <div id="systemInfo">
                    <p>🧠 ASIS is continuously learning through:</p>
                    <ul>
                        <li>Automated research every 30 minutes - 2 hours</li>
                        <li>Cross-domain knowledge synthesis</li>
                        <li>User interaction pattern analysis</li>
                        <li>Real-time knowledge base expansion</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <script>
        let lastFindingsCount = 0;
        let lastSessionsCount = 0;
        
        function updateStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    // Update basic stats
                    document.getElementById('totalFindings').textContent = data.total_findings || 0;
                    document.getElementById('totalSessions').textContent = data.total_sessions || 0;
                    document.getElementById('activeTopics').textContent = data.active_topics || 0;
                    document.getElementById('status').textContent = '✅';
                    document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString();
                    
                    // Check for new activity
                    if (data.total_findings > lastFindingsCount) {
                        showNotification(`🔍 ${data.total_findings - lastFindingsCount} new findings discovered!`);
                    }
                    if (data.total_sessions > lastSessionsCount) {
                        showNotification(`🚀 ${data.total_sessions - lastSessionsCount} new research sessions!`);
                    }
                    
                    lastFindingsCount = data.total_findings || 0;
                    lastSessionsCount = data.total_sessions || 0;
                    
                    // Update recent findings
                    let findingsHtml = '';
                    if (data.recent_findings && data.recent_findings.length > 0) {
                        data.recent_findings.forEach(finding => {
                            findingsHtml += `
                                <div class="finding-item">
                                    <strong>${finding.title}</strong>
                                    <br><span class="confidence">Confidence: ${finding.confidence.toFixed(2)}</span>
                                    <br><small>${finding.content}</small>
                                    <br><span class="timestamp">${finding.time}</span>
                                </div>
                            `;
                        });
                    } else {
                        findingsHtml = '<p>No research findings yet. Research will begin automatically.</p>';
                    }
                    document.getElementById('recentFindings').innerHTML = findingsHtml;
                    
                    // Update recent sessions
                    let sessionsHtml = '';
                    if (data.recent_sessions && data.recent_sessions.length > 0) {
                        data.recent_sessions.forEach(session => {
                            sessionsHtml += `
                                <div class="session-item">
                                    <strong>${session.topic}</strong>
                                    <br><span class="status ${session.status}">${session.status}</span>
                                    <br>Findings: ${session.findings_count || 0}
                                    <br><span class="timestamp">${session.start_time}</span>
                                </div>
                            `;
                        });
                    } else {
                        sessionsHtml = '<p>No research sessions yet.</p>';
                    }
                    document.getElementById('recentSessions').innerHTML = sessionsHtml;
                    
                    // Update research topics
                    let topicsHtml = '';
                    if (data.topics && data.topics.length > 0) {
                        data.topics.slice(0, 5).forEach(topic => {
                            topicsHtml += `
                                <div class="topic-item">
                                    <strong>${topic.topic}</strong>
                                    <br>Priority: ${topic.priority} | Frequency: ${topic.frequency_hours}h
                                    <br><span class="timestamp">Last: ${topic.last_researched}</span>
                                </div>
                            `;
                        });
                    }
                    document.getElementById('researchTopics').innerHTML = topicsHtml;
                })
                .catch(error => {
                    console.error('Error updating status:', error);
                    document.getElementById('status').textContent = '❌';
                });
        }
        
        function forceResearch() {
            const button = document.querySelector('.force-research');
            button.textContent = '⏳ Researching...';
            button.disabled = true;
            
            fetch('/api/force_research')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showNotification('✅ Research session started!');
                        setTimeout(updateStatus, 2000); // Update after 2 seconds
                    } else {
                        showNotification('❌ Research failed: ' + data.error);
                    }
                })
                .catch(error => {
                    showNotification('❌ Error: ' + error);
                })
                .finally(() => {
                    button.textContent = '🔥 Force Research Session';
                    button.disabled = false;
                });
        }
        
        function showNotification(message) {
            // Simple notification
            const notification = document.createElement('div');
            notification.textContent = message;
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: #00ff88;
                color: black;
                padding: 15px 20px;
                border-radius: 10px;
                font-weight: bold;
                z-index: 1000;
                animation: slideIn 0.3s ease;
            `;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 4000);
        }
        
        // Initial load and auto-refresh
        updateStatus();
        setInterval(updateStatus, 10000); // Refresh every 10 seconds
    </script>
</body>
</html>
'''

# Create templates directory and save HTML template
os.makedirs('templates', exist_ok=True)
with open('templates/monitor.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

if __name__ == '__main__':
    print("🌐 Starting ASIS Real-Time Web Monitor...")
    print("🔗 Open your browser to: http://localhost:5000")
    print("🔍 Watch ASIS learn and expand its knowledge in real-time!")
    app.run(host='0.0.0.0', port=5000, debug=False)
