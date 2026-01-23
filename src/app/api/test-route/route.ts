import { NextRequest, NextResponse } from 'next/server';

export async function GET() {
  try {
    console.log('🧪 Test endpoint called successfully');
    return NextResponse.json({ 
      status: 'ok', 
      message: 'Test endpoint is working',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('❌ Test endpoint error:', error);
    return NextResponse.json({ 
      error: 'Test failed',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}