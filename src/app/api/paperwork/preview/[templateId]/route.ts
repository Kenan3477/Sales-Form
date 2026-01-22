import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { checkApiRateLimit } from '@/lib/rateLimit';
import { EnhancedTemplateService } from '@/lib/paperwork/enhanced-template-service';
import { chromium } from 'playwright';

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
    const htmlResult = await enhancedTemplateService.previewTemplate('welcome-letter');

    // Generate PDF using chromium
    const browser = await chromium.launch({ headless: true });
    
    const page = await browser.newPage();
    await page.setContent(htmlResult, { waitUntil: 'networkidle' });
    
    const pdfBuffer = await page.pdf({
      format: 'A4',
      printBackground: true,
      margin: {
        top: '0.5in',
        right: '0.5in',
        bottom: '0.5in',
        left: '0.5in'
      }
    });
    
    await browser.close();

    // Return PDF response
    return new Response(Buffer.from(pdfBuffer), {
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'inline; filename="template-preview.pdf"',
      },
    });

  } catch (error) {
    console.error('Template preview error:', error);
    
    if (error instanceof Error && error.message.includes('not found')) {
      return new Response('Template not found', { status: 404 });
    }
    
    return new Response('Internal server error', { status: 500 });
  }
}