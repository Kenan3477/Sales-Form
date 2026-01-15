# 🔧 Port 5000 Conflict - Quick Fix Guide

## ⚠️ **Issue**: Port 5000 Already in Use

**Problem**: Another process is using port 5000, preventing the new ASIS with meta-learning from starting.

## 🔍 **Step 1: Identify What's Using Port 5000**

Run these commands on your server:

### **Find Process Using Port 5000**
```bash
# Check what's running on port 5000
sudo netstat -tulpn | grep :5000
# or
sudo lsof -i :5000
# or  
sudo ss -tulpn | grep :5000
```

### **Find All Python Processes**
```bash
ps aux | grep python
ps aux | grep app_enhanced
```

## 🚀 **Step 2: Stop the Old Process**

### **Option A: Kill by Process Name**
```bash
# Stop all app_enhanced processes
pkill -f "app_enhanced"
pkill -f "python3 app_enhanced"
pkill -f "python app_enhanced"
```

### **Option B: Kill by Port**
```bash
# Find and kill process using port 5000
sudo fuser -k 5000/tcp
```

### **Option C: Kill by Process ID**
```bash
# If you know the PID from netstat/lsof
kill -9 <PID>
```

## 🎯 **Step 3: Verify Port is Free**
```bash
# Should show nothing
sudo netstat -tulpn | grep :5000
```

## 🚀 **Step 4: Start New ASIS with Meta-Learning**
```bash
# Navigate to new ASIS directory
cd /root/ASIS

# Start enhanced server
nohup python3 app_enhanced.py &

# Check if it started properly
sleep 3
curl http://192.168.2.156:5000/api/status
```

## 🔧 **Alternative: Use Different Port**

If you can't kill the other process, start ASIS on a different port:

### **Modify app_enhanced.py**
```bash
# Edit the file to use port 5001
sed -i 's/port=5000/port=5001/g' app_enhanced.py

# Start on new port
nohup python3 app_enhanced.py &

# Test on new port
curl http://192.168.2.156:5001/api/status
```

## 🎯 **Expected Result**

After fixing the port conflict:
```json
{
  "agi_level": 120.0,
  "meta_learning": true,
  "unified_knowledge": true,
  ...
}
```

## ⚡ **Quick Command Sequence**

```bash
# Stop all ASIS processes
pkill -f "app_enhanced"
sudo fuser -k 5000/tcp

# Verify port is free
sudo netstat -tulpn | grep :5000

# Start new ASIS
cd /root/ASIS
nohup python3 app_enhanced.py &

# Test
curl http://192.168.2.156:5000/api/status
```

---

**🎯 First run the netstat command to see what's using port 5000, then kill it!**