import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { checkApiRateLimit } from '@/lib/rateLimit';

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

    const { prisma } = await import('@/lib/prisma');
    
    // Check if this is an Enhanced Service template
    if (templateId === 'welcome-letter') {
      console.log('📝 Loading Enhanced Service template for preview: welcome-letter');
      
      // Import the Enhanced Template Service
      const { EnhancedTemplateService } = await import('@/lib/paperwork/enhanced-template-service');
      const enhancedTemplateService = new EnhancedTemplateService();
      
      // Get the HTML from the enhanced service
      const htmlResult = await enhancedTemplateService.previewTemplate('welcome-letter');
      
      console.log('✅ Enhanced Service template preview generated');
      
      return new NextResponse(htmlResult, {
        headers: {
          'Content-Type': 'text/html',
          'Cache-Control': 'no-cache, no-store, must-revalidate',
          'Pragma': 'no-cache',
          'Expires': '0',
        },
      });
    }
    
    // Load template by ID from database
    const template = await prisma.documentTemplate.findUnique({
      where: {
        id: templateId,
        isActive: true
      }
    });

    if (!template) {
      return new Response('Template not found', { status: 404 });
    }

    console.log('📝 Loading template for preview:', template.name, template.templateType);

    // Prepare sample template variables for preview
    const sampleVars = {
      customerFirstName: 'John',
      customerLastName: 'Smith', 
      customerName: 'John Smith',
      email: 'john.smith@example.com',
      phone: '020 1234 5678',
      address: '123 Sample Street, London, England, SW1A 1AA',
      currentDate: new Date().toLocaleDateString('en-GB', { 
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      }),
      policyNumber: 'TFT1234',
      monthlyCost: '29.99',
      hasApplianceCover: true,
      hasBoilerCover: true,
      applianceCount: 3
    };

    // Replace template variables in HTML
    let html = template.htmlContent;
    Object.entries(sampleVars).forEach(([key, value]) => {
      const regex = new RegExp(`{{${key}}}`, 'g');
      html = html.replace(regex, String(value || ''));
    });

    console.log('✅ Template preview generated for:', template.name);

    // Return the HTML for preview
    return new NextResponse(html, {
      headers: {
        'Content-Type': 'text/html',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
      },
    });

  } catch (error) {
    console.error('❌ Error generating template preview:', error);
    return new NextResponse(
      'Failed to generate template preview',
      { status: 500 }
    );
  }
}