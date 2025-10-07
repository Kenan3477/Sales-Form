# 🔧 Find Port Usage Without Netstat

## 🎯 **Alternative Commands (No Netstat)**

Since `netstat` isn't available, use these alternatives:

### **Option 1: Use ss (Socket Statistics)**
```bash
ss -tulpn | grep :5000
```

### **Option 2: Use lsof (List Open Files)**
```bash
lsof -i :5000
```

### **Option 3: Use fuser**
```bash
fuser 5000/tcp
```

### **Option 4: Find Python Processes**
```bash
ps aux | grep python
ps aux | grep app_enhanced
```

### **Option 5: Check All Listening Ports**
```bash
ss -tulpn | grep LISTEN
```

## 🚀 **Quick Kill Commands**

### **Kill All app_enhanced Processes**
```bash
pkill -f "app_enhanced"
pkill -f "python3.*app_enhanced"
pkill -f "python.*app_enhanced"
```

### **Kill Process Using Port 5000**
```bash
fuser -k 5000/tcp
```

### **Nuclear Option - Kill All Python**
```bash
pkill python3
pkill python
```

## 🎯 **Simple Process Check**
```bash
# See all processes with 'python' in name
ps aux | grep python

# See all processes with 'asis' in name  
ps aux | grep -i asis

# See all processes with '5000' in command
ps aux | grep 5000
```

## ⚡ **Easy Fix Sequence**

```bash
# 1. Kill all ASIS processes
pkill -f "app_enhanced"

# 2. Kill anything on port 5000
fuser -k 5000/tcp

# 3. Wait a moment
sleep 2

# 4. Start new ASIS
cd /root/ASIS
nohup python3 app_enhanced.py &

# 5. Test after a few seconds
sleep 5
curl http://192.168.2.156:5000/api/status
```

## 🔍 **If Still Having Issues**

### **Check What's Running**
```bash
ps aux | grep -E "(python|app_enhanced|asis)"
```

### **Use Different Port**
```bash
# Edit app_enhanced.py to use port 5001
sed -i 's/port=5000/port=5001/g' app_enhanced.py
nohup python3 app_enhanced.py &
curl http://192.168.2.156:5001/api/status
```

---

**🎯 Try `ss -tulpn | grep :5000` first, then use the kill commands!**