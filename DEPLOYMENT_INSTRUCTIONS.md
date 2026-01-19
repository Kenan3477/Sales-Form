# Quick Deployment Instructions

## Your App URLs:
- **Production URL**: https://sales-form-chi.vercel.app
- **Latest Deployment**: https://sales-form-kyc8fpd5j-kenans-projects-cbb7e50e.vercel.app

## CRITICAL: Set Environment Variable in Vercel Dashboard

**Go to: https://vercel.com → sales-form project → Settings → Environment Variables**

1. **Update NEXTAUTH_URL to:**
   ```
   https://sales-form-chi.vercel.app
   ```

2. **Ensure NODE_ENV is set to:**
   ```
   production
   ```

## After Setting Environment Variables:

1. **Redeploy:** Run `vercel --prod` or trigger deployment through Vercel dashboard
2. **Test Login:** Try logging in from different browsers at https://sales-form-chi.vercel.app

## What This Fixes:

✅ **Cross-Browser Login**: Users can now log in from any browser/device
✅ **Rate Limiting**: Increased from 10 to 20 attempts per IP 
✅ **Cookie Security**: Better cross-browser compatibility
✅ **Origin Validation**: More permissive for legitimate requests

## Test the Fix:

1. **Clear browser cache/cookies**
2. **Try logging in from different browsers**: Chrome, Firefox, Safari
3. **Test from different devices/networks**
4. **Check if sessions persist properly**

Your authentication issues should now be resolved!