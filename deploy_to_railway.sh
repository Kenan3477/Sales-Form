#!/bin/bash
# ASIS Railway Deployment Script

echo "🚀 ASIS Railway Deployment Script"
echo "=================================="

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

echo "🔐 Logging into Railway..."
railway login

echo "📦 Initializing Railway project..."
railway init

echo "🌐 Deploying ASIS to Railway..."
railway up

echo "📊 Getting deployment status..."
railway status

echo "🎉 ASIS deployment complete!"
echo "🌍 Your AGI is now live on the internet!"
echo ""
echo "📋 Next steps:"
echo "1. Check the deployment URL from 'railway status'"
echo "2. Test the chat interface"
echo "3. Try the dashboard features"
echo "4. Share your AGI with the world!"
echo ""
echo "💡 Useful Railway commands:"
echo "  railway logs    - View application logs"
echo "  railway status  - Check deployment status"
echo "  railway open    - Open your app in browser"
