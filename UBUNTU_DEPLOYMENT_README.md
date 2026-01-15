# ASIS Ubuntu Server Deployment Guide

🔒 **Secure deployment of ASIS (Advanced Superintelligence System) on Ubuntu Server with comprehensive security framework**

## 🚀 Quick Start

### Prerequisites
- Ubuntu Server 20.04 LTS or newer
- Minimum 4GB RAM, 20GB storage
- Root/sudo access
- Internet connection

### One-Command Deployment
```bash
chmod +x deploy_ubuntu.sh && ./deploy_ubuntu.sh
```

## 🔐 Security Framework

### Default Credentials
- **Username**: `creator_kenandavies`
- **Password**: `SkyeAlbert2025!`
- **Security Level**: Creator (Full Access)

### Security Features

#### 🛡️ Zero Trust Architecture
- Never trust, always verify
- Continuous monitoring and validation
- Network segmentation
- Minimal privilege access

#### 🔒 End-to-End Encryption
- AES-256 encryption for data at rest
- TLS 1.3 for data in transit
- RSA-2048 for key exchange
- Encrypted audit logs

#### 👥 Role-Based Access Control (RBAC)
- **Creator**: Full system control
- **Admin**: Administrative privileges
- **User**: Standard operations
- **Guest**: Read-only access

#### 📊 Comprehensive Audit Logging
- All user actions logged
- Security events tracked
- Encrypted log storage
- 90-day retention policy

## 🌐 Network Architecture

### Ports
- **443**: HTTPS (Primary access)
- **80**: HTTP (Redirects to HTTPS)
- **22**: SSH (Administrative access)
- **8443**: Internal ASIS service

### Firewall Rules
```bash
# View current rules
sudo ufw status

# Add custom rules
sudo ufw allow from 192.168.1.0/24 to any port 443
sudo ufw deny from 10.0.0.0/8
```

## 🔧 System Management

### Service Management
```bash
# Check ASIS status
sudo systemctl status asis

# Start/Stop/Restart ASIS
sudo systemctl start asis
sudo systemctl stop asis
sudo systemctl restart asis

# View logs
sudo journalctl -u asis -f

# Monitor system health
/opt/asis/monitor.sh
```

### Configuration Files
```
/etc/asis/config/
├── security.json      # Security settings
├── system.json        # System configuration
└── ssl/
    ├── certificate.crt # SSL certificate
    └── private.key     # SSL private key
```

### Log Files
```
/var/log/asis/
├── asis.log          # Main application log
├── security.log      # Security events
└── monitor.log       # Health monitoring
```

## 🔑 User Management

### Create New User
```python
from asis_security_framework import ASISSecurityFramework, SecurityLevel, AccessPermission

security = ASISSecurityFramework()

# Create admin user
security.create_user(
    username="admin_user",
    password="SecurePassword123!",
    security_level=SecurityLevel.ADMIN,
    permissions=[
        AccessPermission.READ,
        AccessPermission.WRITE,
        AccessPermission.EXECUTE,
        AccessPermission.ADMIN
    ],
    ip_whitelist=["192.168.1.0/24"]
)
```

### Authentication Example
```python
# Authenticate user
token = security.authenticate_user(
    username="creator_kenandavies",
    password="SkyeAlbert2025!",
    ip_address="192.168.1.100"
)

# Verify access
has_access = security.verify_access(
    token=token,
    ip_address="192.168.1.100",
    resource="asis_core",
    action=AccessPermission.SYSTEM_CONTROL
)
```

## 🛠️ Advanced Configuration

### SSL Certificate Setup
#### Self-Signed (Development)
```bash
sudo openssl req -x509 -newkey rsa:4096 \
    -keyout /etc/asis/ssl/private.key \
    -out /etc/asis/ssl/certificate.crt \
    -days 365 -nodes \
    -subj "/C=US/ST=State/L=City/O=ASIS/CN=your-domain.com"
```

#### Let's Encrypt (Production)
```bash
sudo certbot --nginx -d your-domain.com
sudo ln -sf /etc/letsencrypt/live/your-domain.com/fullchain.pem /etc/asis/ssl/certificate.crt
sudo ln -sf /etc/letsencrypt/live/your-domain.com/privkey.pem /etc/asis/ssl/private.key
```

### Database Encryption
```python
# Encrypt sensitive data
encrypted_data = security.encryption_manager.encrypt_data("sensitive_info")

# Decrypt when needed
decrypted_data = security.encryption_manager.decrypt_data(encrypted_data)
```

### IP Whitelisting
```python
# Update user IP whitelist
security.authentication_system.create_user(
    username="restricted_user",
    password="password",
    security_level=SecurityLevel.USER,
    ip_whitelist=[
        "192.168.1.100",      # Single IP
        "10.0.0.0/8",         # Network range
        "203.0.113.0/24"      # Another range
    ]
)
```

## 📊 Monitoring & Alerting

### Health Check Script
```bash
# Run manual health check
/opt/asis/monitor.sh

# View monitoring logs
tail -f /var/log/asis/monitor.log
```

### Security Monitoring
```bash
# View security events
sudo tail -f /var/log/asis/security.log

# Check failed login attempts
sudo fail2ban-client status asis

# View firewall logs
sudo journalctl -u ufw
```

### Performance Monitoring
```bash
# System resources
htop
iotop

# Network connections
sudo netstat -tulpn | grep asis

# Process information
ps aux | grep asis
```

## 🔧 Troubleshooting

### Common Issues

#### Service Won't Start
```bash
# Check detailed logs
sudo journalctl -u asis --no-pager -l

# Check configuration
sudo -u asis python3 /opt/asis/asis_main.py --check-config

# Verify permissions
sudo chown -R asis:asis /opt/asis /var/lib/asis /var/log/asis
```

#### SSL/TLS Issues
```bash
# Test SSL configuration
openssl s_client -connect localhost:443

# Verify certificate
openssl x509 -in /etc/asis/ssl/certificate.crt -text -noout

# Check nginx configuration
sudo nginx -t
```

#### Database Errors
```bash
# Check database permissions
ls -la /var/lib/asis/

# Verify database integrity
sqlite3 /var/lib/asis/security.db ".schema"

# Reset database (CAUTION: This will delete all data)
sudo -u asis rm /var/lib/asis/*.db
sudo systemctl restart asis
```

#### Authentication Problems
```bash
# Reset user password
sudo -u asis python3 -c "
from asis_security_framework import ASISSecurityFramework
security = ASISSecurityFramework()
security.create_user('creator_kenandavies', 'SkyeAlbert2025!', 
                    SecurityLevel.CREATOR, [AccessPermission.SYSTEM_CONTROL])
"
```

### Log Analysis
```bash
# Search for specific events
grep "LOGIN_FAILURE" /var/log/asis/security.log

# Monitor real-time security events
tail -f /var/log/asis/security.log | grep -E "(FAILURE|DENIED|VIOLATION)"

# Analyze access patterns
awk '/ACCESS_GRANTED/ {print $1, $2, $6}' /var/log/asis/security.log
```

## 🔄 Backup & Recovery

### Database Backup
```bash
# Create backup
sudo -u asis sqlite3 /var/lib/asis/security.db ".backup /var/lib/asis/backup_$(date +%Y%m%d).db"

# Automated backup script
echo "0 2 * * * sqlite3 /var/lib/asis/security.db \".backup /var/lib/asis/backup_\$(date +\%Y\%m\%d).db\"" | sudo -u asis crontab -
```

### Configuration Backup
```bash
# Backup configuration
sudo tar -czf /home/asis/asis_config_$(date +%Y%m%d).tar.gz /etc/asis/

# Restore configuration
sudo tar -xzf /home/asis/asis_config_20231201.tar.gz -C /
```

### Full System Backup
```bash
# Create complete backup
sudo tar --exclude='/opt/asis/venv' -czf /backup/asis_full_$(date +%Y%m%d).tar.gz \
    /opt/asis /etc/asis /var/lib/asis /var/log/asis
```

## 🔐 Security Best Practices

### Password Policy
- Minimum 12 characters
- Mix of uppercase, lowercase, numbers, symbols
- Regular rotation (90 days)
- No password reuse

### Network Security
- Use VPN for remote access
- Implement network segmentation
- Regular security updates
- Monitor network traffic

### Access Control
- Principle of least privilege
- Regular access reviews
- Multi-factor authentication
- Session timeout enforcement

### Audit & Compliance
- Regular security audits
- Log monitoring and alerting
- Incident response procedures
- Compliance documentation

## 📈 Performance Optimization

### System Tuning
```bash
# Increase file descriptor limits
echo "asis soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "asis hard nofile 65536" | sudo tee -a /etc/security/limits.conf

# Optimize networking
echo "net.core.somaxconn = 1024" | sudo tee -a /etc/sysctl.conf
echo "net.core.netdev_max_backlog = 5000" | sudo tee -a /etc/sysctl.conf
```

### Database Optimization
```python
# Configure SQLite for performance
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
PRAGMA cache_size=10000;
PRAGMA temp_store=memory;
```

## 🆕 Updates & Maintenance

### System Updates
```bash
# Update ASIS
cd /opt/asis
sudo -u asis git pull origin main
sudo systemctl restart asis

# Update system packages
sudo apt update && sudo apt upgrade -y
sudo systemctl restart asis
```

### Security Updates
```bash
# Update security components
sudo -u asis /opt/asis/venv/bin/pip install --upgrade cryptography pyjwt bcrypt

# Regenerate encryption keys (if needed)
sudo -u asis python3 -c "
from asis_security_framework import EncryptionManager
em = EncryptionManager()
# Follow key rotation procedures
"
```

## 📞 Support & Documentation

### Getting Help
- Check logs: `/var/log/asis/`
- Run diagnostics: `/opt/asis/monitor.sh`
- Review configuration: `/etc/asis/config/`

### Additional Resources
- Security documentation: `/opt/asis/docs/security.md`
- API documentation: `/opt/asis/docs/api.md`
- Architecture guide: `/opt/asis/docs/architecture.md`

---

**⚠️ SECURITY NOTICE**: This deployment includes strong security measures, but always:
1. Change default passwords immediately
2. Use proper SSL certificates in production
3. Regularly update all components
4. Monitor security logs continuously
5. Follow your organization's security policies

**🔒 For production deployment, consider additional security measures such as:**
- Hardware Security Modules (HSM)
- Network intrusion detection systems
- Security information and event management (SIEM)
- Regular penetration testing
- Compliance auditing