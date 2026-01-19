import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';

export async function GET(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    
    return NextResponse.json({
      hasSession: !!session,
      sessionData: session ? {
        user: {
          id: session.user.id,
          email: session.user.email,
          role: session.user.role,
          roleType: typeof session.user.role,
          roleLength: session.user.role?.length
        }
      } : null,
      isAdmin: session?.user.role === 'admin',
      isADMIN: session?.user.role === 'ADMIN',
      comparison: {
        'role === admin': session?.user.role === 'admin',
        'role === ADMIN': session?.user.role === 'ADMIN',
        'role !== admin': session?.user.role !== 'admin',
        'role !== ADMIN': session?.user.role !== 'ADMIN'
      }
    });

  } catch (error) {
    console.error('Error checking session:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: String(error) },
      { status: 500 }
    );
  }
}