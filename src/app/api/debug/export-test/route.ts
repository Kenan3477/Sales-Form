import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    console.log('POST test endpoint called')
    const body = await request.json()
    console.log('Request body:', body)
    
    return NextResponse.json({ 
      success: true, 
      message: 'POST endpoint is working',
      receivedData: body 
    })
  } catch (error) {
    console.error('Test POST error:', error)
    return NextResponse.json({ 
      error: 'Test POST failed',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}

export async function GET() {
  return NextResponse.json({ 
    message: 'GET endpoint is working' 
  })
}