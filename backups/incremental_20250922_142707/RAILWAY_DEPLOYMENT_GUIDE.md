# 🚀 ASIS Research Platform - Railway Deployment Guide

## Manual Deployment Steps (Railway CLI not working)

### 1. 🌐 Railway Web Dashboard Setup
1. Go to https://railway.app
2. Sign up/Login to your account
3. Click "New Project"
4. Select "Deploy from GitHub repo"

### 2. 📂 GitHub Repository Setup
Since Railway CLI isn't working, we'll deploy via GitHub:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "ASIS Research Platform - Production ready for Railway"

# Create GitHub repository and connect
# 1. Go to github.com and create new repo: asis-research-platform
# 2. Copy the commands GitHub provides, typically:
git remote add origin https://github.com/YOUR_USERNAME/asis-research-platform.git
git branch -M main
git push -u origin main
```

### 3. ⚙️ Railway Project Configuration
1. In Railway dashboard, click "Deploy from GitHub repo"
2. Connect your GitHub account if not already connected
3. Select your `asis-research-platform` repository
4. Railway will automatically detect it's a Python project

### 4. 🗄️ Add Required Services
**PostgreSQL Database:**
1. In your Railway project, click the "+" button
2. Select "Database" → "Add PostgreSQL"
3. This automatically creates `DATABASE_URL` environment variable

**Redis Cache:**
1. Click "+" again
2. Select "Database" → "Add Redis"  
3. This automatically creates `REDIS_URL` environment variable

### 5. 🔑 Environment Variables Setup
In Railway project settings, add these environment variables:

**Authentication & Security:**
```
JWT_SECRET=your_super_secure_jwt_secret_key_here_change_this
```

**Stripe Payment Processing:**
```
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

**Application Settings:**
```
ENVIRONMENT=production
API_BASE_URL=https://your-railway-app.railway.app
FRONTEND_URL=https://your-domain.com
```

**Research Platform API Keys (Optional):**
```
PUBMED_API_KEY=your_pubmed_api_key
CROSSREF_EMAIL=api@asisai.com
SEMANTIC_SCHOLAR_API_KEY=your_semantic_scholar_key
IEEE_API_KEY=your_ieee_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
```

### 6. 🌐 Custom Domain Setup (Optional)
1. In Railway project settings, go to "Domains"
2. Click "Add Domain"
3. Enter your domain: `research.asisai.com`
4. Configure DNS records as Railway instructs
5. SSL certificate is automatically handled

### 7. 🚀 Deploy!
1. Push your code to GitHub (Railway auto-deploys)
2. Monitor deployment in Railway dashboard
3. View logs to ensure everything starts correctly
4. Access your app at the provided Railway URL

## ✅ Current Project Status

**Application Files Ready:**
- ✅ `main.py` - FastAPI application with authentication
- ✅ `requirements.txt` - Production dependencies
- ✅ `Dockerfile` - Optimized for Railway
- ✅ `Procfile` - Process definition
- ✅ `railway.toml` - Railway configuration
- ✅ `.env.example` - Environment variables template
- ✅ `.gitignore` - Git ignore rules

**Systems Implemented:**
- ✅ Multi-tier SaaS platform (Academic/Professional/Enterprise)
- ✅ Stripe billing integration with academic discounts
- ✅ PostgreSQL database with user/subscription management
- ✅ Redis caching for performance
- ✅ JWT authentication with role-based access
- ✅ Research platform API integration
- ✅ Health checks and monitoring

**Revenue Strategy Ready:**
- ✅ $100K in 60 days execution plan
- ✅ University partnership system
- ✅ Corporate customer acquisition
- ✅ Competitive positioning vs Web of Science/Scopus

## 💰 Deployment Costs

**Railway Infrastructure:**
- Web service: ~$5-10/month
- PostgreSQL: ~$5/month  
- Redis: ~$5/month
- **Total: ~$15-20/month** (vs $500+ on AWS)

## ⏱️ Estimated Deployment Time
- GitHub setup: 2 minutes
- Railway configuration: 3 minutes
- Environment variables: 2 minutes
- First deployment: 3-5 minutes
- **Total: ~10-15 minutes**

## 🆘 Troubleshooting

**If deployment fails:**
1. Check logs in Railway dashboard
2. Verify all environment variables are set
3. Ensure PostgreSQL and Redis services are running
4. Check that `main.py` starts correctly

**Common issues:**
- Missing environment variables → Add them in Railway settings
- Database connection errors → Verify DATABASE_URL is set
- Port binding issues → Railway automatically sets PORT variable

## 🎯 Post-Deployment Steps

1. **Test the application:** Visit your Railway URL
2. **Create admin user:** Register first user with admin privileges
3. **Configure Stripe:** Set up products and webhooks
4. **Test billing:** Create test subscription
5. **Launch customer acquisition:** Begin university outreach

---

**🌟 Your ASIS Research Platform is ready for production deployment on Railway.app! 🌟**
