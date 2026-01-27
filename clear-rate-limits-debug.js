/**
 * Clear rate limits script
 * Run this to clear all rate limiting data
 */

console.log('🧹 Clearing rate limits...')

// Check if we're in development mode
if (process.env.NODE_ENV === 'development') {
  console.log('✅ Development mode detected - rate limits are memory-based and will clear automatically')
  console.log('💡 Simply restart your development server to clear all rate limits')
} else {
  console.log('⚠️  Production mode detected')
  console.log('📝 You may need to clear Redis rate limit data manually')
  console.log('🔧 Check your Upstash Redis dashboard or contact support')
}

console.log('')
console.log('🎯 Quick fixes for rate limiting issues:')
console.log('1. Restart your development server: npm run dev')
console.log('2. Check if multiple browser tabs are making requests')
console.log('3. Clear browser cache and cookies')
console.log('4. Wait 15-60 minutes for rate limits to reset')
console.log('')
console.log('📍 If the issue persists, the problem may be:')
console.log('- Database connectivity issues')
console.log('- Authentication problems')  
console.log('- API endpoint configuration')
console.log('- Client-side request loops')