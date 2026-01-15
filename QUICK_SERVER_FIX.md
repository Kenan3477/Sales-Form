# 🎯 ASIS Server Setup - Quick Fix Guide

## 🔍 **Issue Identified**
- ASIS directory not at `/home/ASIS`
- No git repository set up on server
- Need to locate existing ASIS installation

## 🚀 **Quick Solution Steps**

### **Step 1: Find ASIS Directory**
Run this on your server to find where ASIS is currently running:

```bash
ps aux | grep python
find / -name "app_enhanced.py" 2>/dev/null
```

### **Step 2A: If ASIS Found - Set Up Git**
Once you find the directory (e.g., `/root/ASIS` or `/opt/ASIS`):

```bash
cd /path/to/your/asis/directory
git init
git remote add origin https://github.com/Kenan3477/ASIS.git
git fetch origin
git checkout main
```

### **Step 2B: If ASIS Not Found - Fresh Install**
If no ASIS installation is found:

```bash
cd /root
git clone https://github.com/Kenan3477/ASIS.git
cd ASIS
```

### **Step 3: Deploy Meta-Learning System**
Once git is set up in the correct directory:

```bash
git pull origin main
pkill -f "python3 app_enhanced.py"
pip3 install --upgrade numpy scikit-learn matplotlib seaborn
nohup python3 app_enhanced.py &
```

### **Step 4: Verify Deployment**
```bash
curl http://192.168.2.156:5000/api/status
```

Should show `agi_level: 120.0` and `meta_learning: true`

## 🎯 **Most Likely Scenarios**

### **Scenario 1: ASIS in Root Directory**
```bash
cd /root
ls -la | grep -i asis
cd ASIS  # or whatever the directory is named
```

### **Scenario 2: ASIS in Current User Home**
```bash
cd ~
ls -la | grep -i asis
cd ASIS
```

### **Scenario 3: Fresh Installation Needed**
```bash
cd /root
git clone https://github.com/Kenan3477/ASIS.git
cd ASIS
pip3 install flask flask-socketio requests beautifulsoup4 numpy scikit-learn matplotlib seaborn
```

## ✅ **Success Indicators**

After setup, you should be able to:
1. ✅ `git status` works (shows git repository)
2. ✅ `git pull origin main` works (pulls latest code)  
3. ✅ Server restarts with new meta-learning system
4. ✅ `curl http://192.168.2.156:5000/api/status` shows 120% AGI level

---

**🎯 Start with Step 1 to find your ASIS directory, then follow the appropriate scenario!**