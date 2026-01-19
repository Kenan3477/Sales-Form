#!/bin/bash

echo "🔍 Finding your Vercel deployment URL..."
echo ""

# Check if vercel CLI is available
if command -v vercel &> /dev/null; then
    echo "✅ Vercel CLI found. Getting deployment info..."
    vercel ls || echo "❌ Not authenticated with Vercel CLI"
else
    echo "❌ Vercel CLI not found"
fi

echo ""
echo "📋 Manual steps to find your URL:"
echo ""
echo "1. Go to https://vercel.com"
echo "2. Sign in with your account"
echo "3. Look for project: 'sales-form'"
echo "4. Click on the project"
echo "5. Your URL will be shown (something like: https://sales-form-abc123.vercel.app)"
echo ""
echo "🔧 Once you have your URL, update these environment variables in Vercel:"
echo ""
echo "Variable: NEXTAUTH_URL"
echo "Value: https://your-sales-form-url.vercel.app"
echo ""
echo "Variable: NODE_ENV"  
echo "Value: production"
echo ""
echo "🚀 After updating, redeploy your app!"