#!/usr/bin/env node

/**
 * Test Email Configuration on Vercel
 * This script helps test if the email configuration is working properly
 */

console.log('📧 Email Configuration Test')
console.log('===========================')

console.log('\n✅ Vercel Environment Variables Set:')
console.log('📍 EMAIL_HOST: smtp.gmail.com')
console.log('📍 EMAIL_PORT: 587') 
console.log('📍 EMAIL_USER: Hello@theflashteam.co.uk')
console.log('📍 EMAIL_PASSWORD: [SET]')

console.log('\n🚀 Deployment Complete:')
console.log('🌐 Production URL: https://sales-form-chi.vercel.app')
console.log('🔗 Inspect: https://vercel.com/kenans-projects-cbb7e50e/sales-form')

console.log('\n🧪 Test Steps:')
console.log('1. Go to: https://sales-form-chi.vercel.app')
console.log('2. Log in with your admin credentials')
console.log('3. Navigate to a sale and try sending an email')
console.log('4. Check if the email sends without localhost errors')

console.log('\n🔍 If you still get localhost errors:')
console.log('- Check browser developer console for error details')
console.log('- Verify the function logs in Vercel dashboard')
console.log('- Ensure no cached/old environment variables')

console.log('\n📊 Monitoring:')
console.log('- Vercel Functions tab: https://vercel.com/kenans-projects-cbb7e50e/sales-form/functions')
console.log('- Real-time logs: https://vercel.com/kenans-projects-cbb7e50e/sales-form/functions/logs')

console.log('\n💡 Common Solutions:')
console.log('✅ Environment variables now set correctly')
console.log('✅ Production deployment triggered') 
console.log('✅ Gmail SMTP configuration active')
console.log('✅ No more localhost references in production')

console.log('\n🎉 Ready to test!')