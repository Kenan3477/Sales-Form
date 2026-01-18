import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { checkApiRateLimit } from '@/lib/rateLimit';

export async function GET(request: NextRequest) {
  try {
    // Rate limiting
    const clientIP = request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || 'unknown';
    const rateLimitCheck = await checkApiRateLimit(clientIP);
    if (!rateLimitCheck.success) {
      return NextResponse.json(
        { error: 'Rate limit exceeded. Please try again later.' },
        { status: 429 }
      );
    }

    // Authentication
    const session = await getServerSession(authOptions);
    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Get query parameters
    const url = new URL(request.url);
    const saleId = url.searchParams.get('saleId');
    const userId = session.user.role === 'AGENT' ? session.user.id : undefined;

    // Enhanced Template Service generates documents on-demand
    // Documents are not stored in database for security and storage efficiency
    return NextResponse.json({
      success: true,
      documents: [],
      message: "Documents are generated on-demand using the Flash Team template. Use the Generate Documents tab to create new documents."
    });

  } catch (error) {
    console.error('Get documents error:', error);

    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}