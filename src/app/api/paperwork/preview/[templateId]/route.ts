import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { checkApiRateLimit } from '@/lib/rateLimit';
import { EnhancedTemplateService } from '@/lib/paperwork/enhanced-template-service';
import chromium from '@sparticuz/chromium';
import puppeteer from 'puppeteer';

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

    // Generate PDF using puppeteer with @sparticuz/chromium for serverless
    let executablePath: string | undefined;
    let args: string[] = [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-accelerated-2d-canvas',
      '--no-first-run',
      '--no-zygote',
      '--disable-gpu',
    ];
    
    // Configure for serverless environment
    if (process.env.VERCEL || process.env.NODE_ENV === 'production') {
      executablePath = await chromium.executablePath();
      args = chromium.args.concat(args);
    }
    
    const browser = await puppeteer.launch({
      headless: true,
      executablePath,
      args,
    });
    
    const page = await browser.newPage();
    await page.setContent(htmlResult, { waitUntil: 'networkidle0' });
    
    const pdfBuffer = await page.pdf({
      format: 'A4',
      printBackground: true,
      preferCSSPageSize: false,
      scale: 1.0,
      margin: {
        top: '0.2in',
        right: '0.2in',
        bottom: '0.2in',
        left: '0.2in'
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