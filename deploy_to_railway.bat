@echo off
REM ASIS Railway Deployment Script for Windows

echo 🚀 ASIS Railway Deployment Script
echo ==================================

REM Check if Railway CLI is installed
where railway >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ❌ Railway CLI not found. Please install it:
    echo    npm install -g @railway/cli
    echo    Then run this script again.
    pause
    exit /b 1
)

echo 🔐 Logging into Railway...
railway login

echo 📦 Initializing Railway project...
railway init

echo 🌐 Deploying ASIS to Railway...
railway up

echo 📊 Getting deployment status...
railway status

echo 🎉 ASIS deployment complete!
echo 🌍 Your AGI is now live on the internet!
echo.
echo 📋 Next steps:
echo 1. Check the deployment URL from 'railway status'
echo 2. Test the chat interface
echo 3. Try the dashboard features
echo 4. Share your AGI with the world!
echo.
echo 💡 Useful Railway commands:
echo   railway logs    - View application logs
echo   railway status  - Check deployment status
echo   railway open    - Open your app in browser

pause
