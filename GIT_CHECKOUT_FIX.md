# 🔧 Git Checkout Issue - Quick Fix

## 🎯 **Issue**: Untracked files blocking checkout

**Error**: "The following untracked working tree files would be overwritten by merge"

## ✅ **Quick Solution Options**

### **Option 1: Stash Untracked Files (Recommended)**
```bash
# Save current files and force checkout
git add .
git stash
git checkout main
git pull origin main
```

### **Option 2: Force Checkout (Safe)**
```bash
# Force checkout, overwriting local changes
git checkout -f main
git pull origin main
```

### **Option 3: Clean Untracked Files**
```bash
# Remove untracked files (be careful!)
git clean -fd
git checkout main
git pull origin main
```

### **Option 4: Reset and Pull**
```bash
# Nuclear option - reset everything
git reset --hard
git clean -fd
git checkout main
git pull origin main
```

## 🚀 **Complete Deployment After Git Fix**

Once git is working:

```bash
# Install new dependencies
pip3 install --upgrade numpy scikit-learn matplotlib seaborn

# Stop current server
pkill -f "python3 app_enhanced.py"

# Start enhanced server with meta-learning
nohup python3 app_enhanced.py &

# Test deployment
curl http://192.168.2.156:5000/api/status
```

## 🎯 **Expected Result**

Should show:
```json
{
  "agi_level": 120.0,
  "meta_learning": true,
  "unified_knowledge": true,
  ...
}
```

---

**🔥 Use Option 1 (stash) if you want to preserve files, or Option 2 (force) to overwrite with latest code!**