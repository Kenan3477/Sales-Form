# ASIS Dashboard Enhancement Remote Deployment Guide
==================================================

## 🚀 Quick Start Deployment

### Option 1: Automated SSH Deployment (Recommended)

1. **Install deployment requirements:**
   ```bash
   pip install paramiko scp
   ```

2. **Configure your server details:**
   Edit `deployment_config.json`:
   ```json
   {
     "server": {
       "host": "YOUR_SERVER_IP",
       "username": "YOUR_SSH_USERNAME", 
       "password": "YOUR_SSH_PASSWORD",
       "asis_path": "/path/to/your/asis/directory"
     }
   }
   ```

3. **Run quick deployment:**
   ```bash
   python quick_deploy.py
   ```

### Option 2: Full Deployment Suite

1. **Run the comprehensive deployment script:**
   ```bash
   python deploy_to_server.py
   ```

2. **Select deployment method:**
   - Option 1: Full automated deployment (SSH)
   - Option 2: Generate manual deployment package
   - Option 3: Configure deployment settings

---

## 📋 Manual Deployment (if SSH not available)

1. **Upload these files to your ASIS server:**
   - `asis_dashboard_enhancer.py`
   - `dashboard_control.py`
   - `templates/dashboard_control.html`
   - `test_dashboard_integration.py`
   - `deployment_requirements.txt`

2. **On your server, run:**
   ```bash
   cd /path/to/asis
   pip install -r deployment_requirements.txt
   python test_dashboard_integration.py
   ```

3. **Restart ASIS:**
   ```bash
   pkill -f "python.*app.py"
   nohup python app.py > asis.log 2>&1 &
   ```

---

## 🎯 Post-Deployment

### Access Enhanced Dashboard:
**Internal Network Access (Secure Development Setup):**
```
ASIS Main Interface: http://192.168.2.156:5000/
Dashboard Control:   http://192.168.2.156:5000/dashboard/control
SSH Access:          ssh creator_kenandavies@192.168.2.156
```

### Security Configuration Applied:
✅ **fail2ban** - Protects SSH from brute force attacks
✅ **iptables firewall** - Restricts access to internal network only (192.168.0.0/16)
✅ **Persistent rules** - Security settings survive reboots

### Network Architecture:
- **Server Internal IP:** 192.168.2.156 (Ubuntu desktop converted to server)
- **Router Public IP:** 81.134.136.242 (no port forwarding - internal access only)
- **SSH Ports:** 22, 2222 (both protected by fail2ban)
- **ASIS Port:** 5000 (accessible from internal network)

### Security Rules Active:
```bash
# Firewall allows only internal network access:
iptables -A INPUT -s 192.168.0.0/16 -p tcp --dport 22 -j ACCEPT    # SSH
iptables -A INPUT -s 192.168.0.0/16 -p tcp --dport 2222 -j ACCEPT  # SSH Alt
iptables -A INPUT -s 192.168.0.0/16 -p tcp --dport 5000 -j ACCEPT  # ASIS
iptables -P INPUT DROP  # Block all other traffic
```

### Activation Steps:
1. Open the dashboard control interface: http://192.168.2.156:5000/dashboard/control
2. Click "Activate Enhancement" 
3. Monitor real-time system metrics
4. Access comprehensive ASIS monitoring and control features

### Development Benefits:
- **Secure internal access** - No external exposure to internet threats
- **Real-time monitoring** - CPU, memory, disk, and component health tracking
- **Enhanced control** - Dashboard activation/deactivation capabilities
- **Persistent security** - Firewall and fail2ban protection maintained across reboots

---

*ASIS Dashboard Enhancement Deployment v1.0 - Secure Internal Configuration*