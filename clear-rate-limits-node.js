const { clearFailedLoginAttempts } = require('./src/lib/rateLimit')

async function clearAllRateLimits() {
  console.log('🧹 Clearing all rate limits...')
  
  try {
    // Clear rate limits for the specific IP that's blocked
    const blockedIP = "176.35.52.123"
    
    // Clear all possible rate limit keys
    await clearFailedLoginAttempts(blockedIP)
    await clearFailedLoginAttempts(`ip:${blockedIP}`)
    await clearFailedLoginAttempts(`login:${blockedIP}`)
    await clearFailedLoginAttempts(`api:${blockedIP}`)
    
    // Clear for admin emails  
    await clearFailedLoginAttempts("admin@salesportal.com")
    await clearFailedLoginAttempts("admin@salesportal.co.uk")
    await clearFailedLoginAttempts("agent@salesportal.com")
    
    console.log('✅ Rate limits cleared successfully!')
    console.log('📋 Cleared for:')
    console.log(`   - IP: ${blockedIP}`)
    console.log('   - admin@salesportal.com')
    console.log('   - admin@salesportal.co.uk')
    console.log('   - agent@salesportal.com')
    console.log('')
    console.log('🎯 Users can now login from the previously blocked IP!')
    
  } catch (error) {
    console.error('❌ Failed to clear rate limits:', error)
    console.log('💡 Rate limits are memory-based, they will reset automatically after time expires')
  }
}

clearAllRateLimits()