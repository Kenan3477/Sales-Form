import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { PaperworkService } from '@/lib/paperwork';

export async function GET(request: NextRequest) {
  try {
    // Authentication - only admins can check health
    const session = await getServerSession(authOptions);
    if (!session?.user || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Admin access required' }, { status: 403 });
    }

    // Initialize paperwork service and run health check
    const paperworkService = new PaperworkService();
    const healthResult = await paperworkService.healthCheck();

    const statusCode = healthResult.healthy ? 200 : 503;

    return NextResponse.json({
      ...healthResult,
      timestamp: new Date().toISOString(),
    }, { status: statusCode });

  } catch (error) {
    console.error('Paperwork health check error:', error);

    return NextResponse.json({
      healthy: false,
      services: {
        database: false,
        pdfService: false,
        templateService: false,
        storage: false,
      },
      errors: ['Health check failed'],
      timestamp: new Date().toISOString(),
    }, { status: 503 });
  }
}