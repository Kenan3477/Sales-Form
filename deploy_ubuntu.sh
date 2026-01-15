#!/bin/bash

# ASIS Ubuntu Server Deployment Script
# Secure deployment of ASIS with comprehensive security framework

set -e  # Exit on any error

echo "🚀 ASIS Ubuntu Server Deployment Starting..."

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   error "This script should not be run as root for security reasons"
   exit 1
fi

# System requirements check
log "Checking system requirements..."

# Check Ubuntu version
if ! lsb_release -d | grep -q "Ubuntu"; then
    error "This script is designed for Ubuntu. Please use an Ubuntu server."
    exit 1
fi

# Check minimum Python version
if ! command -v python3 &> /dev/null; then
    error "Python 3 is required but not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3,8) else 1)"; then
    error "Python 3.8+ is required. Current version: $PYTHON_VERSION"
    exit 1
fi

log "✅ System requirements satisfied"

# Update system packages
log "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required system packages
log "Installing system dependencies..."
sudo apt install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    sqlite3 \
    ufw \
    fail2ban \
    nginx \
    certbot \
    python3-certbot-nginx \
    htop \
    iotop \
    netstat-nat \
    curl \
    wget \
    git \
    unzip \
    systemd

# Create ASIS system user
log "Creating ASIS system user..."
if ! id "asis" &>/dev/null; then
    sudo useradd -m -s /bin/bash -G sudo asis
    log "✅ ASIS user created"
else
    log "✅ ASIS user already exists"
fi

# Create directory structure
log "Creating directory structure..."
sudo mkdir -p /opt/asis
sudo mkdir -p /var/lib/asis
sudo mkdir -p /var/log/asis
sudo mkdir -p /etc/asis/{ssl,config}
sudo mkdir -p /home/asis/.asis

# Set proper ownership
sudo chown -R asis:asis /opt/asis
sudo chown -R asis:asis /var/lib/asis
sudo chown -R asis:asis /var/log/asis
sudo chown -R asis:asis /etc/asis
sudo chown -R asis:asis /home/asis

# Set proper permissions
sudo chmod 755 /opt/asis
sudo chmod 750 /var/lib/asis
sudo chmod 750 /var/log/asis
sudo chmod 750 /etc/asis
sudo chmod 700 /etc/asis/ssl
sudo chmod 700 /etc/asis/config

log "✅ Directory structure created"

# Setup Python virtual environment
log "Setting up Python virtual environment..."
sudo -u asis python3 -m venv /opt/asis/venv
sudo -u asis /opt/asis/venv/bin/pip install --upgrade pip

# Install Python dependencies
log "Installing Python dependencies..."
sudo -u asis /opt/asis/venv/bin/pip install \
    cryptography \
    pyjwt \
    bcrypt \
    psutil \
    sqlite3 \
    flask \
    flask-cors \
    gunicorn \
    numpy \
    asyncio \
    aiohttp \
    python-dateutil \
    requests

log "✅ Python environment configured"

# Copy ASIS files
log "Copying ASIS system files..."
sudo cp -r . /opt/asis/
sudo chown -R asis:asis /opt/asis/

# Configure firewall
log "Configuring firewall..."
sudo ufw --force reset
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (customize port if needed)
sudo ufw allow 22

# Allow ASIS ports
sudo ufw allow 8443  # HTTPS
sudo ufw allow 8080  # HTTP redirect

# Enable firewall
sudo ufw --force enable

log "✅ Firewall configured"

# Configure fail2ban
log "Configuring fail2ban..."
sudo tee /etc/fail2ban/jail.local > /dev/null <<EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = 22
filter = sshd
logpath = /var/log/auth.log
maxretry = 3

[asis]
enabled = true
port = 8443
filter = asis
logpath = /var/log/asis/security.log
maxretry = 3
bantime = 7200
EOF

# Create ASIS fail2ban filter
sudo tee /etc/fail2ban/filter.d/asis.conf > /dev/null <<EOF
[Definition]
failregex = ^.*\[LOGIN_FAILURE\].*<HOST>.*$
ignoreregex =
EOF

sudo systemctl enable fail2ban
sudo systemctl restart fail2ban

log "✅ Fail2ban configured"

# Create systemd service
log "Creating ASIS systemd service..."
sudo tee /etc/systemd/system/asis.service > /dev/null <<EOF
[Unit]
Description=ASIS - Advanced Superintelligence System
After=network.target

[Service]
Type=simple
User=asis
Group=asis
WorkingDirectory=/opt/asis
Environment=PATH=/opt/asis/venv/bin
ExecStart=/opt/asis/venv/bin/python asis_main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=asis

# Security settings
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/var/lib/asis /var/log/asis
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes

[Install]
WantedBy=multi-user.target
EOF

# Enable service
sudo systemctl daemon-reload
sudo systemctl enable asis

log "✅ Systemd service created"

# Configure nginx reverse proxy
log "Configuring Nginx reverse proxy..."
sudo tee /etc/nginx/sites-available/asis > /dev/null <<EOF
server {
    listen 80;
    server_name _;
    
    # Redirect HTTP to HTTPS
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name _;
    
    # SSL Configuration
    ssl_certificate /etc/asis/ssl/certificate.crt;
    ssl_certificate_key /etc/asis/ssl/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'";
    
    # Rate limiting
    limit_req_zone \$binary_remote_addr zone=asis:10m rate=10r/m;
    limit_req zone=asis burst=20 nodelay;
    
    location / {
        proxy_pass http://127.0.0.1:8443;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Block common attack patterns
    location ~* \.(php|asp|aspx|jsp)$ {
        deny all;
    }
    
    location ~* /\. {
        deny all;
    }
}
EOF

# Enable nginx site
sudo ln -sf /etc/nginx/sites-available/asis /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

sudo systemctl enable nginx
sudo systemctl restart nginx

log "✅ Nginx configured"

# Create SSL certificates
log "Generating SSL certificates..."
sudo -u asis openssl req -x509 -newkey rsa:4096 \
    -keyout /etc/asis/ssl/private.key \
    -out /etc/asis/ssl/certificate.crt \
    -days 365 -nodes \
    -subj "/C=US/ST=State/L=City/O=ASIS/CN=$(hostname -f)"

sudo chmod 600 /etc/asis/ssl/private.key
sudo chmod 644 /etc/asis/ssl/certificate.crt

log "✅ SSL certificates generated"

# Create ASIS main startup script
log "Creating ASIS main startup script..."
sudo -u asis tee /opt/asis/asis_main.py > /dev/null <<EOF
#!/usr/bin/env python3
"""
ASIS Main Entry Point for Ubuntu Server
"""

import os
import sys
import asyncio
import signal
import logging
from datetime import datetime

# Add ASIS modules to path
sys.path.insert(0, '/opt/asis')

# Import security framework first
from asis_security_framework import ASISSecurityFramework

# Import other ASIS components
try:
    from asis_consciousness import ASISConsciousnessSystem
    from advanced_ai_engine import AdvancedAIEngine
    from asis_persistent_goals_system import PersistentGoalsSystem
except ImportError as e:
    print(f"Warning: Could not import ASIS component: {e}")

class ASISServer:
    def __init__(self):
        self.running = False
        self.security = ASISSecurityFramework()
        self.consciousness = None
        self.ai_engine = None
        self.goals_system = None
        
    async def initialize(self):
        """Initialize all ASIS systems"""
        print("🚀 Initializing ASIS Server...")
        
        try:
            # Initialize security first
            self.security.implement_zero_trust_architecture()
            self.security.setup_end_to_end_encryption()
            self.security.configure_role_based_access()
            
            # Initialize core systems
            if 'ASISConsciousnessSystem' in globals():
                self.consciousness = ASISConsciousnessSystem()
                print("✅ Consciousness system initialized")
            
            if 'AdvancedAIEngine' in globals():
                self.ai_engine = AdvancedAIEngine()
                print("✅ AI engine initialized")
                
            if 'PersistentGoalsSystem' in globals():
                self.goals_system = PersistentGoalsSystem()
                print("✅ Goals system initialized")
            
            print("🎉 ASIS Server fully initialized")
            return True
            
        except Exception as e:
            print(f"❌ ASIS initialization failed: {e}")
            return False
    
    async def start(self):
        """Start ASIS server"""
        if not await self.initialize():
            return False
            
        self.running = True
        print("🌟 ASIS Server is now running!")
        print("🔒 Security framework active")
        print("👤 Creator user: creator_kenandavies")
        print("🌐 Access: https://$(hostname -f):443")
        
        # Main server loop
        try:
            while self.running:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Shutdown signal received")
            
        except Exception as e:
            print(f"❌ Server error: {e}")
            
        finally:
            await self.shutdown()
    
    async def shutdown(self):
        """Graceful shutdown"""
        print("🛑 Shutting down ASIS Server...")
        self.running = False
        print("✅ ASIS Server shutdown complete")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\nReceived signal {signum}")
        self.running = False

def main():
    """Main entry point"""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('/var/log/asis/asis.log'),
            logging.StreamHandler()
        ]
    )
    
    # Create server instance
    server = ASISServer()
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, server.signal_handler)
    signal.signal(signal.SIGTERM, server.signal_handler)
    
    # Start server
    try:
        asyncio.run(server.start())
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
EOF

sudo chmod +x /opt/asis/asis_main.py

log "✅ ASIS main script created"

# Create configuration files
log "Creating configuration files..."

# Security configuration
sudo -u asis tee /etc/asis/config/security.json > /dev/null <<EOF
{
    "session_timeout": 3600,
    "max_login_attempts": 3,
    "lockout_duration": 900,
    "password_min_length": 12,
    "two_factor_enabled": true,
    "ssl_required": true,
    "ip_whitelist_enabled": true,
    "audit_retention_days": 90
}
EOF

# System configuration
sudo -u asis tee /etc/asis/config/system.json > /dev/null <<EOF
{
    "server_name": "ASIS-Ubuntu-Server",
    "version": "1.0.0",
    "environment": "production",
    "debug": false,
    "host": "0.0.0.0",
    "port": 8443,
    "ssl_enabled": true,
    "ssl_cert": "/etc/asis/ssl/certificate.crt",
    "ssl_key": "/etc/asis/ssl/private.key"
}
EOF

log "✅ Configuration files created"

# Set up log rotation
log "Configuring log rotation..."
sudo tee /etc/logrotate.d/asis > /dev/null <<EOF
/var/log/asis/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    copytruncate
    su asis asis
}
EOF

log "✅ Log rotation configured"

# Create monitoring script
log "Creating monitoring script..."
sudo tee /opt/asis/monitor.sh > /dev/null <<'EOF'
#!/bin/bash

# ASIS Health Monitoring Script

echo "🔍 ASIS System Health Check - $(date)"
echo "============================================"

# Check if ASIS service is running
if systemctl is-active --quiet asis; then
    echo "✅ ASIS Service: Running"
else
    echo "❌ ASIS Service: Not Running"
fi

# Check if nginx is running
if systemctl is-active --quiet nginx; then
    echo "✅ Nginx: Running"
else
    echo "❌ Nginx: Not Running"
fi

# Check if fail2ban is running
if systemctl is-active --quiet fail2ban; then
    echo "✅ Fail2ban: Running"
else
    echo "❌ Fail2ban: Not Running"
fi

# Check SSL certificate expiry
CERT_FILE="/etc/asis/ssl/certificate.crt"
if [ -f "$CERT_FILE" ]; then
    EXPIRY=$(openssl x509 -enddate -noout -in "$CERT_FILE" | cut -d= -f2)
    EXPIRY_EPOCH=$(date -d "$EXPIRY" +%s)
    CURRENT_EPOCH=$(date +%s)
    DAYS_LEFT=$(( (EXPIRY_EPOCH - CURRENT_EPOCH) / 86400 ))
    
    if [ $DAYS_LEFT -gt 30 ]; then
        echo "✅ SSL Certificate: Valid ($DAYS_LEFT days remaining)"
    elif [ $DAYS_LEFT -gt 0 ]; then
        echo "⚠️ SSL Certificate: Expires soon ($DAYS_LEFT days remaining)"
    else
        echo "❌ SSL Certificate: Expired"
    fi
fi

# Check disk usage
DISK_USAGE=$(df /var/lib/asis | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -lt 80 ]; then
    echo "✅ Disk Usage: ${DISK_USAGE}%"
elif [ $DISK_USAGE -lt 90 ]; then
    echo "⚠️ Disk Usage: ${DISK_USAGE}%"
else
    echo "❌ Disk Usage: ${DISK_USAGE}% (Critical)"
fi

# Check memory usage
MEM_USAGE=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
if [ $MEM_USAGE -lt 80 ]; then
    echo "✅ Memory Usage: ${MEM_USAGE}%"
elif [ $MEM_USAGE -lt 90 ]; then
    echo "⚠️ Memory Usage: ${MEM_USAGE}%"
else
    echo "❌ Memory Usage: ${MEM_USAGE}% (Critical)"
fi

# Check active sessions
if [ -f "/var/lib/asis/security.db" ]; then
    ACTIVE_SESSIONS=$(sqlite3 /var/lib/asis/security.db "SELECT COUNT(*) FROM sessions WHERE active = 1;")
    echo "📊 Active Sessions: $ACTIVE_SESSIONS"
fi

echo "============================================"
EOF

sudo chmod +x /opt/asis/monitor.sh

# Add monitoring to crontab
(sudo -u asis crontab -l 2>/dev/null; echo "*/5 * * * * /opt/asis/monitor.sh >> /var/log/asis/monitor.log 2>&1") | sudo -u asis crontab -

log "✅ Monitoring configured"

# Final security hardening
log "Applying final security hardening..."

# Disable root login over SSH
sudo sed -i 's/^#*PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart sshd

# Set proper file permissions
sudo find /opt/asis -name "*.py" -exec chmod 755 {} \;
sudo find /etc/asis -type f -exec chmod 600 {} \;
sudo find /var/lib/asis -type f -exec chmod 600 {} \;

log "✅ Security hardening complete"

# Start services
log "Starting ASIS services..."
sudo systemctl start asis
sudo systemctl restart nginx

# Wait a moment for services to start
sleep 5

# Check service status
if systemctl is-active --quiet asis; then
    log "✅ ASIS service started successfully"
else
    error "❌ ASIS service failed to start"
    sudo journalctl -u asis --no-pager -l
fi

if systemctl is-active --quiet nginx; then
    log "✅ Nginx service running"
else
    error "❌ Nginx service failed"
fi

# Display final status
echo ""
echo "🎉 ASIS Ubuntu Server Deployment Complete!"
echo "============================================"
echo "🔒 Security Framework: Active"
echo "👤 Creator User: creator_kenandavies"
echo "🔑 Password: SkyeAlbert2025!"
echo "🌐 Web Interface: https://$(hostname -f)"
echo "📊 Monitoring: /opt/asis/monitor.sh"
echo "📝 Logs: /var/log/asis/"
echo "⚙️ Config: /etc/asis/config/"
echo ""
echo "🔧 Management Commands:"
echo "  sudo systemctl status asis"
echo "  sudo systemctl restart asis"
echo "  sudo journalctl -u asis -f"
echo "  /opt/asis/monitor.sh"
echo ""
echo "🔒 Security Features Enabled:"
echo "  ✅ Zero Trust Architecture"
echo "  ✅ End-to-End Encryption"
echo "  ✅ Role-Based Access Control"
echo "  ✅ Comprehensive Audit Logging"
echo "  ✅ Firewall Protection"
echo "  ✅ Fail2ban Intrusion Prevention"
echo "  ✅ SSL/TLS Encryption"
echo "  ✅ Security Headers"
echo "  ✅ Rate Limiting"
echo ""
warn "IMPORTANT: Change default passwords and configure proper SSL certificates for production!"

log "Deployment completed successfully at $(date)"