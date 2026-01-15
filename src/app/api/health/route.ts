import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    return NextResponse.json(
      { 
        status: 'healthy',
        service: 'Sales Form Portal',
        timestamp: new Date().toISOString(),
        version: '1.0.0'
      },
      { status: 200 }
    );
  } catch (error) {
    return NextResponse.json(
      { 
        status: 'unhealthy',
        error: 'Service unavailable'
      },
      { status: 503 }
    );
  }
}