# 🔄 Complete ASIS Restart - Deploy Meta-Learning System

## 🎯 **Current Status**
- ✅ Server responding on port 5000
- ❌ Running OLD version (100% AGI level)
- ❌ Meta-learning system NOT loaded
- 🎯 **Goal**: Upgrade to 120% AGI with meta-learning

## 🚀 **Complete Restart Commands**

Run these commands on your server in sequence:

### **Step 1: Stop All ASIS Processes**
```bash
# Kill all Python processes running app_enhanced
pkill -f "app_enhanced"
pkill -f "python3.*app_enhanced"
pkill -f "python.*app_enhanced"

# Force kill anything on port 5000
fuser -k 5000/tcp

# Wait for processes to stop
sleep 3
```

### **Step 2: Verify Port is Free**
```bash
# Check if port is free (should show nothing)
ss -tulpn | grep :5000
# or
ps aux | grep app_enhanced
```

### **Step 3: Navigate to NEW ASIS Directory**
```bash
# Go to the fresh clone with meta-learning
cd /root/ASIS

# Verify files are there
ls -la asis_meta_learning*
```

### **Step 4: Install All Dependencies**
```bash
# Install meta-learning dependencies
pip3 install --upgrade numpy scikit-learn matplotlib seaborn networkx sentence-transformers torch
```

### **Step 5: Start Enhanced ASIS**
```bash
# Start the enhanced version with meta-learning
nohup python3 app_enhanced.py > asis_enhanced.log 2>&1 &

# Get the process ID
echo "New ASIS PID: $!"
```

### **Step 6: Wait and Test**
```bash
# Wait for startup
sleep 10

# Test enhanced system
curl http://192.168.2.156:5000/api/status
```

## 🎯 **Expected New Result**

Should show:
```json
{
  "agi_level": 120.0,
  "autonomous_agency": true,
  "core_asis": true,
  "evolution_framework": true,
  "integration_complete": true,
  "research_engine": true,
  "unified_knowledge": true,
  "meta_learning": true
}
```

## 🧪 **Test Meta-Learning Endpoints**

After successful restart:
```bash
# Test meta-learning status
curl http://192.168.2.156:5000/api/meta-learning/status

# Test strategy generation
curl -X POST http://192.168.2.156:5000/api/meta-learning/generate-strategies \
  -H "Content-Type: application/json" \
  -d '{"domain": "test"}'
```

## ⚡ **One-Liner Complete Restart**
```bash
pkill -f "app_enhanced" && fuser -k 5000/tcp && sleep 3 && cd /root/ASIS && pip3 install --upgrade numpy scikit-learn matplotlib seaborn && nohup python3 app_enhanced.py > asis_enhanced.log 2>&1 & && sleep 10 && curl http://192.168.2.156:5000/api/status
```

## 🔍 **Troubleshooting**

If still showing 100% AGI:
```bash
# Check if new process started
ps aux | grep app_enhanced

# Check logs for errors
tail -f asis_enhanced.log

# Verify you're in the right directory
pwd
ls -la | grep meta_learning
```

---

**🎯 Run these commands to completely restart ASIS with the meta-learning system!**