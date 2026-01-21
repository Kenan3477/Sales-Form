#!/bin/bash

# Test Vercel Integration After Private Repo Fix
# Run this script to test if Vercel is now picking up GitHub pushes

echo "🧪 Testing Vercel-GitHub Integration..."
echo "================================================"

# Create test file with timestamp
TEST_FILE="INTEGRATION_TEST_$(date +%s).txt"
echo "# Vercel Integration Test" > "$TEST_FILE"
echo "Timestamp: $(date)" >> "$TEST_FILE" 
echo "Commit: Testing private repo integration" >> "$TEST_FILE"
echo "Expected: Should trigger Vercel deployment" >> "$TEST_FILE"

# Add, commit, and push
git add "$TEST_FILE"
git commit -m "🧪 TEST: Verify Vercel integration after private repo fix

- Test file: $TEST_FILE
- Purpose: Confirm auto-deployment working
- Expected: New deployment in Vercel within 2 minutes
- Time: $(date)"

echo "✅ Test commit created"
echo "🚀 Pushing to GitHub..."

git push origin main

echo ""
echo "⏰ Next steps:"
echo "1. Check Vercel dashboard in 1-2 minutes"
echo "2. Look for new deployment triggered by this commit"
echo "3. If deployment appears, integration is fixed!"
echo "4. If no deployment, check GitHub App permissions"
echo ""
echo "🎯 Production URL: https://sales-form-chi.vercel.app"
echo "📊 Vercel Dashboard: https://vercel.com/dashboard"
echo ""
echo "⚠️  Remember: Once integration works, CSP fixes will deploy and login will be restored!"