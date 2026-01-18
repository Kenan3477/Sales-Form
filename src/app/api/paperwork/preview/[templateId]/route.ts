import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { checkApiRateLimit } from '@/lib/rateLimit';
import { EnhancedTemplateService } from '@/lib/paperwork/enhanced-template-service';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ templateId: string }> }
) {
  try {
    // Rate limiting
    const clientIP = request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || 'unknown';
    const rateLimitCheck = await checkApiRateLimit(clientIP);
    if (!rateLimitCheck.success) {
      return new Response('Rate limit exceeded', { status: 429 });
    }

    // Authentication
    const session = await getServerSession(authOptions);
    if (!session?.user) {
      return new Response('Unauthorized', { status: 401 });
    }

    // Await params since they're now a Promise in Next.js 16
    const { templateId } = await params;

    // Initialize enhanced template service
    const enhancedTemplateService = new EnhancedTemplateService();

    // For Flash Team, we only have the welcome-letter template
    // Use sample data for preview
    const result = await enhancedTemplateService.previewTemplate('welcome-letter');

    // Return HTML response
    return new Response(result, {
      headers: {
        'Content-Type': 'text/html',
        'X-Frame-Options': 'SAMEORIGIN', // Allow iframe preview
      },
    });
      },
      agreement: {
        startDate: new Date().toLocaleDateString(),
        totalPrice: '£299.99',
        monthlyPrice: '£24.99',
        paymentMethod: 'Direct Debit'
      },
      appliances: [
  } catch (error) {
    console.error('Template preview error:', error);
    
    if (error instanceof Error && error.message.includes('not found')) {
      return new Response('Template not found', { status: 404 });
    }
    
    return new Response('Internal server error', { status: 500 });
  }
}