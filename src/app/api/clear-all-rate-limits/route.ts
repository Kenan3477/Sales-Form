import { NextRequest, NextResponse } from 'next/server'
import { clearFailedLoginAttempts } from '@/lib/rateLimit'

export async function POST(request: NextRequest) {
  try {
    // Clear rate limits for the specific IP that's blocked
    const blockedIP = "176.35.52.123"
    
    // Clear all possible rate limit keys for this IP
    await clearFailedLoginAttempts(blockedIP)
    await clearFailedLoginAttempts(`ip:${blockedIP}`)
    await clearFailedLoginAttempts(`login:${blockedIP}`)
    await clearFailedLoginAttempts(`api:${blockedIP}`)
    
    // Also clear for any admin emails that might be blocked
    await clearFailedLoginAttempts("admin@salesportal.com")
    await clearFailedLoginAttempts("admin@salesportal.co.uk")
    await clearFailedLoginAttempts("agent@salesportal.com")
    
    return NextResponse.json({ 
      success: true,
      message: "All rate limits cleared successfully",
      clearedFor: [
        `IP: ${blockedIP}`,
        "admin@salesportal.com",
        "admin@salesportal.co.uk", 
        "agent@salesportal.com"
      ]
    })
    
  } catch (error) {
    console.error('Failed to clear rate limits:', error)
    return NextResponse.json({ 
      error: 'Failed to clear rate limits',
      message: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}

export async function GET() {
  return NextResponse.json({ 
    message: "Use POST to clear rate limits",
    endpoint: "/api/clear-all-rate-limits"
  })
}