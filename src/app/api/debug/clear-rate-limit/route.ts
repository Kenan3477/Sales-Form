import { NextRequest, NextResponse } from 'next/server'
import { clearFailedLoginAttempts } from '@/lib/rateLimit'

export async function POST(request: NextRequest) {
  try {
    const { identifier } = await request.json()
    
    if (!identifier) {
      return NextResponse.json({ error: 'Identifier required' }, { status: 400 })
    }

    // Clear failed attempts for the identifier
    await clearFailedLoginAttempts(identifier)
    
    return NextResponse.json({ 
      success: true, 
      message: `Rate limit cleared for ${identifier}` 
    })
  } catch (error) {
    return NextResponse.json({ 
      error: 'Failed to clear rate limit',
      message: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}