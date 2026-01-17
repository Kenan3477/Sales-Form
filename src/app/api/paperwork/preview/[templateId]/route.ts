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

    // Get template
    const { prisma } = await import('@/lib/prisma');
    const template = await prisma.documentTemplate.findUnique({
      where: { id: templateId },
    });

    if (!template) {
      return new Response('Template not found', { status: 404 });
    }

    // Create sample context for preview
    const sampleContext = {
      customer: {
        fullName: 'John Smith',
        email: 'john.smith@example.com',
        phone: '01234 567890',
        address: {
          line1: '123 Main Street',
          line2: 'Flat 2B',
          city: 'London',
          postalCode: 'SW1A 1AA',
          country: 'United Kingdom'
        }
      },
      agreement: {
        startDate: new Date().toLocaleDateString(),
        totalPrice: '£299.99',
        monthlyPrice: '£24.99',
        paymentMethod: 'Direct Debit'
      },
      appliances: [
        {
          type: 'Boiler',
          make: 'Worcester',
          model: 'Bosch Greenstar',
          location: 'Kitchen'
        },
        {
          type: 'Central Heating',
          make: 'Various',
          model: 'Full System',
          location: 'Throughout Property'
        }
      ],
      metadata: {
        generatedAt: new Date().toISOString(),
        documentId: 'PREVIEW-' + Date.now(),
        version: template.version
      }
    };

    // Use enhanced template service to render with sample data
    const enhancedService = new EnhancedTemplateService();
    const renderedContent = enhancedService.renderTemplate(template.htmlContent, sampleContext);

    // Return HTML with preview styling
    const previewHtml = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Template Preview: ${template.name}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .preview-banner {
            background: #fbbf24;
            color: #92400e;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: bold;
        }
        .document-content {
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <div class="preview-banner">
        📄 Template Preview: ${template.name} (v${template.version}) - Sample Data
    </div>
    <div class="document-content">
        ${renderedContent}
    </div>
</body>
</html>`;

    return new Response(previewHtml, {
      headers: { 'Content-Type': 'text/html' },
    });

  } catch (error) {
    console.error('Template preview error:', error);
    return new Response('Internal server error', { status: 500 });
  }
}