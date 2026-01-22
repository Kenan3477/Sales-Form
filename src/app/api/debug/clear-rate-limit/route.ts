import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const { identifier } = await request.json()
    
    if (!identifier) {
      return NextResponse.json({ error: 'Identifier required' }, { status: 400 })
    }

    return NextResponse.json({
      message: 'Rate limit clearing is now handled automatically by Redis-based system',
      deprecated: true,
      identifier,
      timestamp: new Date().toISOString()
    })
  } catch (error) {
    console.error('Debug clear rate limit error:', error)
    return NextResponse.json(
      { error: 'Failed to clear rate limit' },
      { status: 500 }
    )
  }
}
