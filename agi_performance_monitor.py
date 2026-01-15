#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 ASIS AGI Performance Monitoring System
Real-time monitoring and analytics for AGI performance and learning

This module provides:
- Real-time AGI performance monitoring
- Learning progress tracking
- System resource monitoring
- Performance analytics dashboard
- Alert system for performance issues
- Historical performance data analysis

Author: ASIS AGI Development Team
Version: 1.0.0
"""

import time
import json
import sqlite3
import psutil
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import numpy as np
import pandas as pd

@dataclass
class PerformanceMetric:
    """Performance metric data structure"""
    timestamp: datetime
    metric_name: str
    value: float
    unit: str
    category: str
    component: str
    metadata: Dict[str, Any] = None

@dataclass
class AlertConfig:
    """Alert configuration"""
    metric_name: str
    threshold: float
    comparison: str  # 'greater', 'less', 'equal'
    severity: str  # 'low', 'medium', 'high', 'critical'
    callback: Optional[Callable] = None

class AGIPerformanceMonitor:
    """Comprehensive AGI performance monitoring system"""
    
    def __init__(self, db_path: str = "agi_performance.db"):
        self.db_path = db_path
        self.metrics_buffer = deque(maxlen=10000)  # Ring buffer for recent metrics
        self.alerts = []
        self.alert_configs = []
        self.monitoring_active = False
        self.monitor_thread = None
        
        # Performance tracking
        self.performance_history = defaultdict(list)
        self.system_stats = {}
        
        # Initialize database
        self._initialize_database()
        
        # Setup default alert configurations
        self._setup_default_alerts()
        
        print("📊 AGI Performance Monitor initialized")
    
    def _initialize_database(self):
        """Initialize performance monitoring database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Performance metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT,
                category TEXT,
                component TEXT,
                metadata TEXT
            )
        """)
        
        # System resources table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                cpu_percent REAL,
                memory_percent REAL,
                disk_percent REAL,
                network_bytes_sent INTEGER,
                network_bytes_recv INTEGER
            )
        """)
        
        # AGI learning events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                learning_domain TEXT,
                performance_change REAL,
                confidence_level REAL,
                details TEXT
            )
        """)
        
        # Performance alerts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                metric_name TEXT,
                threshold_value REAL,
                actual_value REAL,
                message TEXT,
                resolved BOOLEAN DEFAULT FALSE
            )
        """)
        
        conn.commit()
        conn.close()
        print("📊 Performance monitoring database initialized")
    
    def _setup_default_alerts(self):
        """Setup default performance alert configurations"""
        default_alerts = [
            AlertConfig("cpu_usage", 85.0, "greater", "high"),
            AlertConfig("memory_usage", 90.0, "greater", "critical"),
            AlertConfig("consciousness_level", 0.3, "less", "medium"),
            AlertConfig("learning_rate", 0.1, "less", "medium"),
            AlertConfig("response_time", 5000.0, "greater", "high"),  # milliseconds
            AlertConfig("error_rate", 0.05, "greater", "high"),  # 5% error rate
        ]
        
        self.alert_configs.extend(default_alerts)
        print(f"📊 Configured {len(default_alerts)} default performance alerts")
    
    def start_monitoring(self, interval: float = 30.0):
        """Start continuous performance monitoring"""
        if self.monitoring_active:
            print("📊 Monitoring already active")
            return
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
        print(f"📊 Performance monitoring started (interval: {interval}s)")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)
        print("📊 Performance monitoring stopped")
    
    def _monitoring_loop(self, interval: float):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect system metrics
                self._collect_system_metrics()
                
                # Collect AGI metrics
                self._collect_agi_metrics()
                
                # Check alerts
                self._check_alerts()
                
                # Sleep until next collection
                time.sleep(interval)
                
            except Exception as e:
                print(f"📊 Monitoring loop error: {e}")
                time.sleep(interval)
    
    def _collect_system_metrics(self):
        """Collect system resource metrics"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            self.record_metric("cpu_usage", cpu_percent, "percent", "system", "cpu")
            
            # Memory metrics
            memory = psutil.virtual_memory()
            self.record_metric("memory_usage", memory.percent, "percent", "system", "memory")
            self.record_metric("memory_available", memory.available / 1024**3, "GB", "system", "memory")
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            self.record_metric("disk_usage", disk.percent, "percent", "system", "disk")
            
            # Network metrics
            network = psutil.net_io_counters()
            self.record_metric("network_bytes_sent", network.bytes_sent, "bytes", "system", "network")
            self.record_metric("network_bytes_recv", network.bytes_recv, "bytes", "system", "network")
            
            # Store in database
            self._store_system_resources(cpu_percent, memory.percent, disk.percent, 
                                       network.bytes_sent, network.bytes_recv)
            
        except Exception as e:
            print(f"📊 System metrics collection error: {e}")
    
    def _collect_agi_metrics(self):
        """Collect AGI-specific performance metrics"""
        try:
            # Try to get AGI system status
            from asis_agi_production import UnifiedAGIControllerProduction
            
            agi = UnifiedAGIControllerProduction()
            status = agi.get_agi_system_status()
            
            if "error" not in status:
                system_status = status.get("system_status", {})
                
                # Consciousness metrics
                consciousness_level = system_status.get("consciousness_level", 0)
                self.record_metric("consciousness_level", consciousness_level, "score", "agi", "consciousness")
                
                # Learning metrics
                learning_rate = system_status.get("learning_rate", 0)
                self.record_metric("learning_rate", learning_rate, "score", "agi", "learning")
                
                # System coherence
                coherence = system_status.get("system_coherence", 0)
                self.record_metric("system_coherence", coherence, "score", "agi", "coherence")
                
                # Performance metrics
                if "performance_metrics" in status:
                    perf = status["performance_metrics"]
                    self.record_metric("response_time", perf.get("avg_response_time", 0), "ms", "agi", "performance")
                    self.record_metric("success_rate", perf.get("success_rate", 0), "percent", "agi", "performance")
                    self.record_metric("error_rate", perf.get("error_rate", 0), "percent", "agi", "performance")
            
            agi.shutdown_agi_system()
            
        except Exception as e:
            print(f"📊 AGI metrics collection error: {e}")
    
    def record_metric(self, name: str, value: float, unit: str, category: str, 
                     component: str, metadata: Dict[str, Any] = None):
        """Record a performance metric"""
        metric = PerformanceMetric(
            timestamp=datetime.now(),
            metric_name=name,
            value=value,
            unit=unit,
            category=category,
            component=component,
            metadata=metadata or {}
        )
        
        # Add to buffer
        self.metrics_buffer.append(metric)
        
        # Store in database
        self._store_metric(metric)
        
        # Update history for quick access
        self.performance_history[name].append((metric.timestamp, value))
        
        # Keep only recent history (last 1000 points)
        if len(self.performance_history[name]) > 1000:
            self.performance_history[name] = self.performance_history[name][-1000:]
    
    def _store_metric(self, metric: PerformanceMetric):
        """Store metric in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO performance_metrics 
                (timestamp, metric_name, value, unit, category, component, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                metric.timestamp.isoformat(),
                metric.metric_name,
                metric.value,
                metric.unit,
                metric.category,
                metric.component,
                json.dumps(metric.metadata) if metric.metadata else None
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"📊 Metric storage error: {e}")
    
    def _store_system_resources(self, cpu_percent: float, memory_percent: float, 
                               disk_percent: float, bytes_sent: int, bytes_recv: int):
        """Store system resource metrics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO system_resources 
                (timestamp, cpu_percent, memory_percent, disk_percent, 
                 network_bytes_sent, network_bytes_recv)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                cpu_percent,
                memory_percent,
                disk_percent,
                bytes_sent,
                bytes_recv
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"📊 System resource storage error: {e}")
    
    def _check_alerts(self):
        """Check performance metrics against alert configurations"""
        recent_metrics = dict()
        
        # Get most recent values for each metric
        for metric in reversed(self.metrics_buffer):
            if metric.metric_name not in recent_metrics:
                recent_metrics[metric.metric_name] = metric.value
        
        # Check each alert configuration
        for alert_config in self.alert_configs:
            metric_value = recent_metrics.get(alert_config.metric_name)
            
            if metric_value is None:
                continue
            
            # Check threshold
            alert_triggered = False
            if alert_config.comparison == "greater" and metric_value > alert_config.threshold:
                alert_triggered = True
            elif alert_config.comparison == "less" and metric_value < alert_config.threshold:
                alert_triggered = True
            elif alert_config.comparison == "equal" and abs(metric_value - alert_config.threshold) < 0.001:
                alert_triggered = True
            
            if alert_triggered:
                self._trigger_alert(alert_config, metric_value)
    
    def _trigger_alert(self, alert_config: AlertConfig, actual_value: float):
        """Trigger a performance alert"""
        alert_message = (f"Performance alert: {alert_config.metric_name} "
                        f"{alert_config.comparison} {alert_config.threshold} "
                        f"(actual: {actual_value})")
        
        alert_data = {
            "timestamp": datetime.now().isoformat(),
            "alert_type": "performance",
            "severity": alert_config.severity,
            "metric_name": alert_config.metric_name,
            "threshold_value": alert_config.threshold,
            "actual_value": actual_value,
            "message": alert_message
        }
        
        # Store alert
        self._store_alert(alert_data)
        
        # Add to alerts list
        self.alerts.append(alert_data)
        
        # Execute callback if provided
        if alert_config.callback:
            try:
                alert_config.callback(alert_data)
            except Exception as e:
                print(f"📊 Alert callback error: {e}")
        
        print(f"🚨 {alert_config.severity.upper()} ALERT: {alert_message}")
    
    def _store_alert(self, alert_data: Dict[str, Any]):
        """Store alert in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO performance_alerts 
                (timestamp, alert_type, severity, metric_name, threshold_value, 
                 actual_value, message)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                alert_data["timestamp"],
                alert_data["alert_type"],
                alert_data["severity"],
                alert_data["metric_name"],
                alert_data["threshold_value"],
                alert_data["actual_value"],
                alert_data["message"]
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"📊 Alert storage error: {e}")
    
    def get_performance_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance summary for the last N hours"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Get metrics from last N hours
            since_time = (datetime.now() - timedelta(hours=hours)).isoformat()
            
            # System metrics summary
            df_system = pd.read_sql_query("""
                SELECT * FROM system_resources 
                WHERE timestamp > ?
                ORDER BY timestamp DESC
            """, conn, params=[since_time])
            
            # Performance metrics summary
            df_metrics = pd.read_sql_query("""
                SELECT * FROM performance_metrics 
                WHERE timestamp > ?
                ORDER BY timestamp DESC
            """, conn, params=[since_time])
            
            # Recent alerts
            df_alerts = pd.read_sql_query("""
                SELECT * FROM performance_alerts 
                WHERE timestamp > ? AND resolved = FALSE
                ORDER BY timestamp DESC
            """, conn, params=[since_time])
            
            conn.close()
            
            summary = {
                "period_hours": hours,
                "timestamp": datetime.now().isoformat(),
                "system_metrics": {},
                "agi_metrics": {},
                "alerts": {
                    "total": len(df_alerts),
                    "by_severity": df_alerts.groupby('severity').size().to_dict() if not df_alerts.empty else {},
                    "recent": df_alerts.head(10).to_dict('records') if not df_alerts.empty else []
                }
            }
            
            # System metrics statistics
            if not df_system.empty:
                summary["system_metrics"] = {
                    "cpu_usage": {
                        "avg": df_system['cpu_percent'].mean(),
                        "max": df_system['cpu_percent'].max(),
                        "min": df_system['cpu_percent'].min()
                    },
                    "memory_usage": {
                        "avg": df_system['memory_percent'].mean(),
                        "max": df_system['memory_percent'].max(),
                        "min": df_system['memory_percent'].min()
                    },
                    "disk_usage": {
                        "current": df_system['disk_percent'].iloc[0] if len(df_system) > 0 else 0
                    }
                }
            
            # AGI metrics statistics
            if not df_metrics.empty:
                agi_metrics = df_metrics[df_metrics['category'] == 'agi']
                if not agi_metrics.empty:
                    for metric_name in agi_metrics['metric_name'].unique():
                        metric_data = agi_metrics[agi_metrics['metric_name'] == metric_name]['value']
                        summary["agi_metrics"][metric_name] = {
                            "avg": metric_data.mean(),
                            "max": metric_data.max(),
                            "min": metric_data.min(),
                            "current": metric_data.iloc[0] if len(metric_data) > 0 else 0
                        }
            
            return summary
            
        except Exception as e:
            print(f"📊 Performance summary error: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_learning_progress(self, days: int = 7) -> Dict[str, Any]:
        """Get AGI learning progress over time"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            since_time = (datetime.now() - timedelta(days=days)).isoformat()
            
            # Get learning-related metrics
            df_learning = pd.read_sql_query("""
                SELECT timestamp, metric_name, value 
                FROM performance_metrics 
                WHERE timestamp > ? AND category = 'agi'
                AND metric_name IN ('learning_rate', 'consciousness_level', 'system_coherence')
                ORDER BY timestamp
            """, conn, params=[since_time])
            
            # Get learning events
            df_events = pd.read_sql_query("""
                SELECT * FROM learning_events 
                WHERE timestamp > ?
                ORDER BY timestamp
            """, conn, params=[since_time])
            
            conn.close()
            
            progress = {
                "period_days": days,
                "timestamp": datetime.now().isoformat(),
                "learning_trends": {},
                "learning_events": df_events.to_dict('records') if not df_events.empty else [],
                "improvement_rate": 0.0
            }
            
            # Calculate trends for each learning metric
            if not df_learning.empty:
                for metric_name in df_learning['metric_name'].unique():
                    metric_data = df_learning[df_learning['metric_name'] == metric_name]
                    
                    # Calculate trend (simple linear regression slope)
                    if len(metric_data) > 1:
                        x = np.arange(len(metric_data))
                        y = metric_data['value'].values
                        trend = np.polyfit(x, y, 1)[0]  # slope
                        
                        progress["learning_trends"][metric_name] = {
                            "trend": trend,
                            "direction": "improving" if trend > 0 else "declining" if trend < 0 else "stable",
                            "current_value": y[-1] if len(y) > 0 else 0,
                            "change_rate": trend * 100  # percentage change per measurement
                        }
            
            # Calculate overall improvement rate
            if progress["learning_trends"]:
                improvement_rates = [trend["trend"] for trend in progress["learning_trends"].values()]
                progress["improvement_rate"] = np.mean(improvement_rates)
            
            return progress
            
        except Exception as e:
            print(f"📊 Learning progress error: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def generate_performance_report(self) -> str:
        """Generate comprehensive performance report"""
        summary = self.get_performance_summary(24)
        learning = self.get_learning_progress(7)
        
        report = f"""
# 📊 ASIS AGI Performance Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🖥️ System Performance (Last 24 Hours)
"""
        
        if summary.get("system_metrics"):
            sys_metrics = summary["system_metrics"]
            report += f"""
- **CPU Usage:** Avg: {sys_metrics['cpu_usage']['avg']:.1f}%, Max: {sys_metrics['cpu_usage']['max']:.1f}%
- **Memory Usage:** Avg: {sys_metrics['memory_usage']['avg']:.1f}%, Max: {sys_metrics['memory_usage']['max']:.1f}%
- **Disk Usage:** {sys_metrics['disk_usage']['current']:.1f}%
"""
        
        report += f"""
## 🧠 AGI Performance Metrics
"""
        
        if summary.get("agi_metrics"):
            for metric_name, stats in summary["agi_metrics"].items():
                report += f"- **{metric_name.replace('_', ' ').title()}:** Current: {stats['current']:.3f}, Avg: {stats['avg']:.3f}\n"
        
        report += f"""
## 📈 Learning Progress (Last 7 Days)
"""
        
        if learning.get("learning_trends"):
            for metric_name, trend in learning["learning_trends"].items():
                direction = trend["direction"]
                emoji = "📈" if direction == "improving" else "📉" if direction == "declining" else "📊"
                report += f"- **{metric_name.replace('_', ' ').title()}:** {emoji} {direction.title()} (Rate: {trend['change_rate']:.4f}%)\n"
        
        report += f"""
## 🚨 Recent Alerts
"""
        
        if summary.get("alerts", {}).get("recent"):
            for alert in summary["alerts"]["recent"][:5]:  # Show top 5
                severity_emoji = {"low": "🔵", "medium": "🟡", "high": "🟠", "critical": "🔴"}.get(alert.get("severity", ""), "⚪")
                report += f"- {severity_emoji} **{alert.get('severity', 'unknown').upper()}:** {alert.get('message', 'No message')}\n"
        else:
            report += "- ✅ No recent alerts\n"
        
        report += f"""
## 📋 Summary
- **Overall Improvement Rate:** {learning.get('improvement_rate', 0):.4f}
- **Total Alerts (24h):** {summary.get('alerts', {}).get('total', 0)}
- **System Status:** {'🟢 Healthy' if summary.get('alerts', {}).get('total', 0) == 0 else '🟡 Monitoring'}

---
*Generated by ASIS AGI Performance Monitoring System v1.0.0*
"""
        
        return report
    
    def cleanup_old_data(self, days: int = 30):
        """Clean up old performance data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_time = (datetime.now() - timedelta(days=days)).isoformat()
            
            # Clean up old metrics
            cursor.execute("DELETE FROM performance_metrics WHERE timestamp < ?", [cutoff_time])
            cursor.execute("DELETE FROM system_resources WHERE timestamp < ?", [cutoff_time])
            cursor.execute("DELETE FROM learning_events WHERE timestamp < ?", [cutoff_time])
            cursor.execute("DELETE FROM performance_alerts WHERE timestamp < ? AND resolved = TRUE", [cutoff_time])
            
            conn.commit()
            conn.close()
            
            print(f"📊 Cleaned up performance data older than {days} days")
            
        except Exception as e:
            print(f"📊 Data cleanup error: {e}")

def main():
    """Main performance monitoring function"""
    print("📊 ASIS AGI Performance Monitoring System")
    print("=" * 50)
    
    monitor = AGIPerformanceMonitor()
    
    # Start monitoring
    monitor.start_monitoring(interval=30.0)
    
    try:
        # Generate initial report
        print("\n📊 Generating initial performance report...")
        report = monitor.generate_performance_report()
        print(report)
        
        # Keep monitoring running
        print("\n📊 Performance monitoring active. Press Ctrl+C to stop.")
        while True:
            time.sleep(60)  # Print status every minute
            print(f"📊 Monitoring active... ({datetime.now().strftime('%H:%M:%S')})")
            
    except KeyboardInterrupt:
        print("\n📊 Stopping performance monitoring...")
        monitor.stop_monitoring()
        print("📊 Performance monitoring stopped!")

if __name__ == "__main__":
    main()
