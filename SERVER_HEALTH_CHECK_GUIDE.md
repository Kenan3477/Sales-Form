# 🔍 Server Health Check Guide - Remote & Direct Methods

## 🌐 **Remote Checks (From Your Computer)**

### **1. Basic Connectivity Test**
```powershell
# Test if port 5000 is responding
Test-NetConnection -ComputerName 192.168.2.156 -Port 5000

# Or use telnet equivalent
powershell -Command "try { (New-Object Net.Sockets.TcpClient).Connect('192.168.2.156', 5000); Write-Host 'Port 5000 is open' } catch { Write-Host 'Port 5000 is closed/not responding' }"
```

### **2. HTTP Health Check**
```powershell
# Simple ping to see if server responds
Invoke-WebRequest -Uri "http://192.168.2.156:5000" -UseBasicParsing -TimeoutSec 10

# Check if any basic endpoint works
curl -i http://192.168.2.156:5000
```

### **3. Alternative Port Check**
```powershell
# Check if server started on different port
Test-NetConnection -ComputerName 192.168.2.156 -Port 5001
Test-NetConnection -ComputerName 192.168.2.156 -Port 8000
```

## 🖥️ **Direct Server Checks (SSH/Console)**

### **1. Process Status**
```bash
# Check if Python processes are running
ps aux | grep python
ps aux | grep app_enhanced

# Check specific ASIS processes
pgrep -f "app_enhanced"
pgrep -af "python.*app_enhanced"
```

### **2. Port Usage**
```bash
# See what's using port 5000
ss -tulpn | grep :5000
lsof -i :5000

# Check all listening ports
ss -tulpn | grep LISTEN
```

### **3. Server Logs**
```bash
# Check recent logs
tail -20 nohup.out
tail -20 meta_learning_fixed.log
tail -20 clean_restart.log
tail -20 complete_restart.log

# Follow live logs
tail -f nohup.out

# Search for errors
grep -i error nohup.out
grep -i exception nohup.out
grep -i failed nohup.out
```

### **4. System Resources**
```bash
# Check system load
top
htop

# Check memory usage
free -h

# Check disk space
df -h
```

### **5. Network Status**
```bash
# Check network interfaces
ip addr show
ifconfig

# Test local connectivity
curl localhost:5000/api/status
wget -O- localhost:5000/api/status
```

## 🔧 **Common Issues & Solutions**

### **Issue 1: Import Errors**
```bash
# Test Python imports manually
python3 -c "
try:
    import flask
    print('✅ Flask OK')
except Exception as e:
    print(f'❌ Flask: {e}')

try:
    import numpy
    print('✅ NumPy OK')
except Exception as e:
    print(f'❌ NumPy: {e}')

try:
    from asis_meta_learning import asis_meta_learning
    print('✅ Meta-learning OK')
except Exception as e:
    print(f'❌ Meta-learning: {e}')
"
```

### **Issue 2: Permission Problems**
```bash
# Check file permissions
ls -la app_enhanced.py
ls -la asis_meta_learning.py

# Check if user can run Python
python3 --version
which python3
```

### **Issue 3: Dependencies Missing**
```bash
# Check installed packages
pip3 list | grep -E "(flask|numpy|scikit|torch)"

# Install missing dependencies
pip3 install flask flask-socketio numpy scikit-learn matplotlib seaborn
```

## 🚀 **Quick Diagnostic Script**

```bash
#!/bin/bash
echo "=== ASIS Server Health Check ==="
echo ""

echo "1. Process Status:"
ps aux | grep -E "(python|app_enhanced)" | grep -v grep

echo ""
echo "2. Port Status:"
ss -tulpn | grep :5000

echo ""
echo "3. Recent Logs (last 10 lines):"
if [ -f "nohup.out" ]; then
    tail -10 nohup.out
else
    echo "No nohup.out found"
fi

echo ""
echo "4. Python Test:"
python3 -c "print('Python is working')"

echo ""
echo "5. Network Test:"
curl -s localhost:5000/api/status 2>/dev/null || echo "Local API not responding"

echo ""
echo "=== Health Check Complete ==="
```

## ⚡ **Emergency Recovery Commands**

### **If Server is Stuck:**
```bash
# Nuclear option - kill all Python
sudo pkill -9 python3
sudo fuser -k 5000/tcp

# Clean start
cd /home/creator_kenandavies/ASIS
python3 app_enhanced.py

# Watch for errors in real-time
```

### **If Dependencies Are Missing:**
```bash
# Install everything fresh
pip3 install --upgrade pip
pip3 install flask flask-socketio requests beautifulsoup4
pip3 install numpy scikit-learn matplotlib seaborn
pip3 install networkx sentence-transformers torch
```

## 🎯 **Success Indicators**

### **Healthy Server Shows:**
- ✅ Python process running
- ✅ Port 5000 listening
- ✅ HTTP responses working
- ✅ No error messages in logs
- ✅ AGI level 120.0 in status

### **Problem Indicators:**
- ❌ No Python processes
- ❌ Port 5000 not listening
- ❌ Import errors in logs
- ❌ Permission denied errors
- ❌ Memory/disk issues

---

**🔍 Start with the remote connectivity test, then check processes and logs on the server!**