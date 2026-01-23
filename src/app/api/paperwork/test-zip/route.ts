import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    // Test if JSZip can be imported
    const JSZip = await import('jszip');
    return NextResponse.json({ 
      success: true, 
      message: 'JSZip imported successfully',
      hasDefault: !!JSZip.default
    });
  } catch (error) {
    return NextResponse.json({ 
      success: false, 
      error: error instanceof Error ? error.message : 'Unknown error',
      message: 'JSZip import failed'
    }, { status: 500 });
  }
}

export async function GET() {
  return NextResponse.json({ message: 'Test endpoint is working' });
}