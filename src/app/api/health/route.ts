import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET(request: NextRequest) {
  try {
    // SECURITY: Disable setup functionality
    const url = new URL(request.url);
    const setup = url.searchParams.get('setup');
    
    if (setup === 'init') {
      return NextResponse.json({
        error: 'Setup functionality disabled for security',
        message: 'Use proper admin panel for user management'
      }, { status: 403 });
    }

    // Basic health check only
    await prisma.$connect();
    
    const adminCount = await prisma.user.count({ where: { role: 'ADMIN' } });
    const agentCount = await prisma.user.count({ where: { role: 'AGENT' } });
    const settingsCount = await prisma.fieldConfiguration.count();
    
    return NextResponse.json({
      status: 'healthy',
      database: 'connected',
      users: {
        admins: adminCount,
        agents: agentCount,
        total: adminCount + agentCount
      },
      settings: settingsCount > 0 ? 'configured' : 'not configured',
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('Health check error:', error);
    return NextResponse.json(
      { 
        status: 'unhealthy',
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      }, 
      { status: 500 }
    );
  }
}
