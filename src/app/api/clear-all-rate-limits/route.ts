import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    return NextResponse.json({ 
      message: 'Rate limit clearing is now handled automatically by Redis-based system',
      deprecated: true,
      timestamp: new Date().toISOString()
    })
  } catch (error) {
    console.error('Clear rate limits error:', error)
    return NextResponse.json(
      { error: 'Failed to clear rate limits' },
      { status: 500 }
    )
  }
}

export async function GET() {
  return NextResponse.json({ 
    message: "Use POST to clear rate limits",
    endpoint: "/api/clear-all-rate-limits"
  })
}
