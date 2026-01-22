import { NextRequest, NextResponse } from 'next/server';
import { secureDebugEndpoint } from '@/lib/debugSecurity';

export async function GET(request: NextRequest) {
  return await secureDebugEndpoint(request, async () => {
    // This endpoint is now secured and only accessible by super admins in development
    return NextResponse.json({
      message: 'Debug endpoint access is restricted',
      note: 'This endpoint requires SUPER_ADMIN privileges and is disabled in production',
      timestamp: new Date().toISOString()
    });
  });
}