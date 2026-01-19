# Authentication Troubleshooting Guide

## Current Issues Identified and Fixed:

### 1. **NEXTAUTH_URL Configuration**
**Problem**: Your `.env` file has `NEXTAUTH_URL="http://localhost:3000"` which only works locally.

**Solution**: 
- For production, update `NEXTAUTH_URL` to your actual domain
- Example: `NEXTAUTH_URL="https://yourdomain.com"`

### 2. **Rate Limiting Too Strict**
**Problem**: IP rate limiting was set to 10 attempts, blocking users on shared networks.

**Solution**: 
- ✅ Increased IP rate limit from 10 to 20 attempts
- ✅ Kept email-specific rate limit at 5 attempts

### 3. **Cookie Security Issues**
**Problem**: Cookies might not work properly across different browsers/domains.

**Solution**: 
- ✅ Improved cookie configuration for better cross-browser compatibility
- ✅ Added debug mode for authentication

### 4. **Origin Validation Too Strict**
**Problem**: Middleware was blocking legitimate requests from different browsers.

**Solution**: 
- ✅ Made origin validation more permissive
- ✅ Only blocks clearly malicious requests

## How to Test the Fixes:

1. **Check Authentication Debug Info**:
   Visit: `http://localhost:3000/api/debug/auth`
   This will show you session status, cookies, and environment info.

2. **Test from Different Browsers**:
   - Try logging in from Chrome, Firefox, Safari
   - Check if cookies are being set properly
   - Verify session persistence

3. **Check Rate Limiting**:
   - Test multiple failed login attempts
   - Should allow up to 5 attempts per email
   - Should allow up to 20 attempts per IP

## Environment Variables to Set:

### For Development:
```bash
NODE_ENV=development
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key
DEBUG_AUTH=true
```

### For Production:
```bash
NODE_ENV=production
NEXTAUTH_URL=https://yourdomain.com
NEXTAUTH_SECRET=your-production-secret-key
DEBUG_AUTH=false
```

## Common Solutions for Different Deployment Platforms:

### Railway:
```bash
NEXTAUTH_URL=https://your-app-name.up.railway.app
```

### Vercel:
```bash
NEXTAUTH_URL=https://your-app-name.vercel.app
```

### Custom Domain:
```bash
NEXTAUTH_URL=https://yourdomain.com
```

## Debugging Steps:

1. **Check the debug endpoint**: `/api/debug/auth`
2. **Verify environment variables** are set correctly
3. **Clear browser cache** and cookies
4. **Test from incognito/private mode**
5. **Check browser console** for errors
6. **Verify database connectivity** for user lookup

## If Issues Persist:

1. Check if users are being rate-limited
2. Verify NEXTAUTH_URL matches the actual domain
3. Ensure NEXTAUTH_SECRET is set and consistent
4. Check if database connection is working
5. Review browser network tab for failed requests