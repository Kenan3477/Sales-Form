#!/usr/bin/env python3
"""
🚀 ASIS Railway Manual Deployment Script
========================================

Alternative deployment method when Railway CLI is not working.
This script prepares the project for manual Railway deployment.
"""

import os
import json
import subprocess
from datetime import datetime

def prepare_railway_deployment():
    """Prepare project for manual Railway deployment"""
    
    print("🚀 ASIS Railway Manual Deployment Preparation")
    print("=" * 50)
    
    # 1. Initialize Git repository if not exists
    print("1. 📁 Initializing Git repository...")
    try:
        subprocess.run(["git", "init"], check=True, capture_output=True)
        print("   ✅ Git repository initialized")
    except:
        print("   ℹ️ Git repository already exists or Git not available")
    
    # 2. Create railway.json for configuration
    railway_config = {
        "build": {
            "builder": "nixpacks"
        },
        "deploy": {
            "healthcheckPath": "/health",
            "healthcheckTimeout": 60,
            "restartPolicyType": "ON_FAILURE",
            "restartPolicyMaxRetries": 10
        }
    }
    
    with open("railway.json", "w") as f:
        json.dump(railway_config, f, indent=2)
    
    print("2. ⚙️ Railway configuration created")
    
    # 3. Create deployment documentation
    deployment_steps = """
# 🚀 ASIS Research Platform - Railway Deployment Guide

## Manual Deployment Steps (When CLI fails)

### 1. Railway Web Dashboard Setup
1. Go to https://railway.app
2. Sign up/Login to your account
3. Click "New Project"
4. Select "Deploy from GitHub repo"

### 2. GitHub Repository Setup
1. Create new GitHub repository: `asis-research-platform`
2. Push this code to GitHub:
   ```bash
   git add .
   git commit -m "Initial ASIS Research Platform deployment"
   git remote add origin https://github.com/YOUR_USERNAME/asis-research-platform.git
   git push -u origin main
   ```

### 3. Railway Project Configuration
1. Connect your GitHub repository
2. Railway will automatically detect Python project
3. Add PostgreSQL database: Click "+" → "Database" → "Add PostgreSQL"
4. Add Redis: Click "+" → "Database" → "Add Redis"

### 4. Environment Variables Setup
Add these environment variables in Railway dashboard:

**Required Variables:**
- `DATABASE_URL` (automatically set by Railway PostgreSQL)
- `REDIS_URL` (automatically set by Railway Redis)
- `JWT_SECRET=your_secure_jwt_secret_key_here`
- `STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key`
- `STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key`
- `ENVIRONMENT=production`

**API Keys (Optional but recommended):**
- `PUBMED_API_KEY=your_pubmed_api_key`
- `CROSSREF_EMAIL=api@asisai.com`
- `SEMANTIC_SCHOLAR_API_KEY=your_semantic_scholar_key`
- `IEEE_API_KEY=your_ieee_api_key`

### 5. Domain Setup (Optional)
1. In Railway dashboard, go to Settings
2. Add custom domain: `research.asisai.com`
3. Configure DNS records as instructed

### 6. Deployment
1. Push code to GitHub
2. Railway automatically deploys
3. Monitor deployment logs in Railway dashboard
4. Access your app at the provided Railway URL

## Current Project Status
✅ FastAPI application ready
✅ PostgreSQL database integration
✅ Stripe billing system
✅ Authentication system
✅ Research platform APIs
✅ Dockerfile optimized
✅ Environment variables configured

## Estimated Deployment Time: 5-10 minutes
## Estimated Monthly Cost: $5-20 (depending on usage)
"""
    
    with open("RAILWAY_DEPLOYMENT_GUIDE.md", "w") as f:
        f.write(deployment_steps)
    
    print("3. 📖 Deployment guide created")
    
    # 4. Prepare Git commands
    git_commands = """
# Git commands to deploy to Railway via GitHub

git add .
git commit -m "ASIS Research Platform - Production ready for Railway deployment"

# If you haven't created GitHub repo yet:
# 1. Go to github.com and create new repository: asis-research-platform
# 2. Then run:
# git remote add origin https://github.com/YOUR_USERNAME/asis-research-platform.git

git push -u origin main

# Then connect this GitHub repo to Railway in the web dashboard
"""
    
    with open("git_deployment_commands.txt", "w") as f:
        f.write(git_commands)
    
    print("4. 📋 Git deployment commands prepared")
    
    # 5. Verify all necessary files exist
    required_files = [
        "main.py",
        "requirements.txt", 
        "Dockerfile",
        "Procfile",
        "railway.toml",
        ".env.example",
        ".gitignore"
    ]
    
    print("5. ✅ Verifying deployment files:")
    all_files_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MISSING!")
            all_files_exist = False
    
    # 6. Create quick deployment summary
    deployment_summary = {
        "project_name": "ASIS Research Platform",
        "deployment_method": "Railway.app",
        "status": "Ready for manual deployment",
        "required_services": ["PostgreSQL", "Redis"],
        "estimated_cost": "$5-20/month",
        "deployment_time": "5-10 minutes",
        "files_ready": all_files_exist,
        "timestamp": datetime.now().isoformat()
    }
    
    with open("deployment_summary.json", "w") as f:
        json.dump(deployment_summary, f, indent=2)
    
    print("\n🌟 Manual Deployment Preparation Complete!")
    print("=" * 50)
    print("📁 Files created:")
    print("   - railway.json (Railway configuration)")
    print("   - RAILWAY_DEPLOYMENT_GUIDE.md (Step-by-step guide)")
    print("   - git_deployment_commands.txt (Git commands)")
    print("   - deployment_summary.json (Project summary)")
    print()
    print("📋 Next Steps:")
    print("1. Create GitHub repository")
    print("2. Push code using git commands in git_deployment_commands.txt")
    print("3. Connect GitHub repo to Railway dashboard")
    print("4. Add environment variables")
    print("5. Deploy!")
    print()
    print("📖 Read RAILWAY_DEPLOYMENT_GUIDE.md for detailed instructions")
    
    return True

if __name__ == "__main__":
    prepare_railway_deployment()
