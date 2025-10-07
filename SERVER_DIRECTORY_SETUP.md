# 🔍 ASIS Server Directory Setup Guide

## 🎯 **Finding and Setting Up ASIS on Server**

Since `/home/ASIS` doesn't exist and there's no git repository, let's locate and properly set up ASIS:

## 📍 **Step 1: Find Current ASIS Installation**

Run these commands on your server to find where ASIS is running from:

### **Find the Running Process**
```bash
ps aux | grep python
ps aux | grep app_enhanced
```

### **Find ASIS Files**
```bash
find / -name "app_enhanced.py" 2>/dev/null
find / -name "asis_interface.py" 2>/dev/null
find /root -name "*.py" | grep asis
find /home -name "*.py" | grep asis
```

### **Check Common Locations**
```bash
ls -la /root/
ls -la /root/ASIS/
ls -la /opt/
ls -la /var/www/
```

## 🔧 **Step 2: Set Up Git Repository**

Once you find the ASIS directory, navigate to it and set up git:

### **Navigate to ASIS Directory** (replace with actual path)
```bash
cd /path/to/asis/directory
```

### **Initialize Git Repository**
```bash
git init
git remote add origin https://github.com/Kenan3477/ASIS.git
git fetch origin
git checkout main
```

### **Or Clone Fresh Repository**
```bash
# If you want to start fresh
cd /root
git clone https://github.com/Kenan3477/ASIS.git
cd ASIS
```

## 🚀 **Step 3: Deploy Meta-Learning System**

Once git is set up:

### **Pull Latest Changes**
```bash
git pull origin main
```

### **Install Dependencies**
```bash
pip3 install --upgrade numpy scikit-learn matplotlib seaborn
```

### **Stop Current Server**
```bash
pkill -f "python3 app_enhanced.py"
pkill -f "python app_enhanced.py"
```

### **Start Enhanced Server**
```bash
nohup python3 app_enhanced.py &
```

## 🔍 **Alternative: Quick Directory Finder**

Run this one-liner to find ASIS:

```bash
find / -name "app_enhanced.py" -exec dirname {} \; 2>/dev/null | head -1
```

## 📋 **Common Server Setups**

### **If ASIS is in Root Directory**
```bash
cd /root
ls -la | grep -i asis
```

### **If ASIS is in Home Directory**
```bash
cd ~
ls -la | grep -i asis
```

### **If ASIS is in Opt Directory**
```bash
cd /opt
ls -la | grep -i asis
```

## 🎯 **After Finding ASIS Directory**

1. **Navigate to it**: `cd /path/to/asis`
2. **Set up git**: Follow Step 2 above
3. **Deploy updates**: Follow Step 3 above
4. **Test**: Access http://192.168.2.156:5000/api/status

## 🚨 **If No ASIS Installation Found**

If ASIS files aren't found, clone fresh:

```bash
cd /root
git clone https://github.com/Kenan3477/ASIS.git
cd ASIS
pip3 install flask flask-socketio requests beautifulsoup4 numpy scikit-learn matplotlib seaborn
nohup python3 app_enhanced.py &
```

---

**🔍 First, run the finder commands to locate your current ASIS installation!**