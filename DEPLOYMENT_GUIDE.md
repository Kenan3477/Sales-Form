# ASIS Training Interface Deployment Guide

## 🚀 Railway Deployment Instructions

### Prerequisites
1. Railway account (https://railway.app)
2. GitHub repository with the ASIS training interface

### Files Required for Deployment
- `asis_training_interface_production.py` - Main application
- `Procfile` - Railway startup command
- `requirements.txt` - Python dependencies
- `railway.json` - Railway configuration
- `templates/` folder - HTML templates

### Deployment Steps

#### Option 1: Deploy via Railway Dashboard (Recommended)
1. Go to https://railway.app/dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account if not already connected
5. Select your ASIS repository
6. Railway will automatically detect the Python app and deploy

#### Option 2: Deploy via Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project in your directory
railway link

# Deploy
railway up
```

### Environment Variables
No additional environment variables required - the app uses Railway's default PORT.

### Expected Deployment URL
After successful deployment, Railway will provide a URL like:
`https://asis-training-production.up.railway.app`

### Verification
- Health check: `https://your-app.railway.app/health`
- Main interface: `https://your-app.railway.app/`
- Knowledge training: `https://your-app.railway.app/knowledge-training`
- Conversation training: `https://your-app.railway.app/conversation-training`

### Troubleshooting
- Check Railway logs if deployment fails
- Ensure all template files are in the `templates/` directory
- Verify Python version compatibility (3.8+)

## 🎓 ASIS Training Interface Features

### Training Dashboard
- Real-time progress monitoring
- Training session management
- Analytics and metrics

### Knowledge Training
- Add structured knowledge entries
- Bulk import capabilities
- Domain-specific training

### Conversation Training
- Pattern-based conversation improvement
- Quality analysis and scoring
- Real-time response testing
