import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';

export async function GET() {
  try {
    console.log('🧪 Testing minimal batch endpoint...');
    
    // Test 1: Authentication
    const session = await getServerSession(authOptions);
    if (!session?.user) {
      return NextResponse.json({ 
        error: 'No session found',
        step: 'authentication',
        hasAuthOptions: !!authOptions
      }, { status: 401 });
    }

    if (session.user.role !== 'ADMIN' && session.user.role !== 'AGENT') {
      return NextResponse.json({ 
        error: 'Insufficient permissions', 
        role: session.user.role,
        step: 'authorization'
      }, { status: 403 });
    }

    console.log('✅ Authentication passed');

    // Test 2: Basic response
    return NextResponse.json({
      status: 'success',
      message: 'Minimal batch endpoint working',
      user: {
        id: session.user.id,
        email: session.user.email,
        role: session.user.role
      },
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('❌ Minimal batch test error:', error);
    
    // Return detailed error information
    return NextResponse.json({
      error: 'Minimal batch test failed',
      message: error instanceof Error ? error.message : 'Unknown error',
      stack: error instanceof Error ? error.stack?.split('\n').slice(0, 10) : [],
      type: typeof error,
      name: error instanceof Error ? error.name : 'Unknown'
    }, { status: 500 });
  }
}