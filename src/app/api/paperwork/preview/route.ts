import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { PaperworkService } from '@/lib/paperwork';
import { checkApiRateLimit } from '@/lib/rateLimit';
import { z } from 'zod';

// Request validation schema
const previewDocumentSchema = z.object({
  saleId: z.string().min(1),
  templateType: z.enum(['welcome_letter', 'service_agreement', 'direct_debit_form', 'coverage_summary']),
  templateId: z.string().optional(),
  format: z.enum(['html', 'pdf']).default('html'),
});

export async function POST(request: NextRequest) {
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

    // Parse and validate request body
    const body = await request.json();
    const validatedData = previewDocumentSchema.parse(body);

    // Initialize paperwork service
    const paperworkService = new PaperworkService();

    // Check user permissions (agents can only preview their own sales)
    if (session.user.role === 'AGENT') {
      const { prisma } = await import('@/lib/prisma');
      const sale = await prisma.sale.findUnique({
        where: { id: validatedData.saleId },
        select: { createdById: true },
      });

      if (!sale) {
        return NextResponse.json({ error: 'Sale not found' }, { status: 404 });
      }

      if (sale.createdById !== session.user.id) {
        return NextResponse.json({ error: 'Access denied' }, { status: 403 });
      }
    }

    // Generate the preview
    const result = await paperworkService.generatePreview(validatedData, validatedData.format);

    // Return appropriate response based on format
    if (validatedData.format === 'html') {
      return new Response(result.content as string, {
        headers: {
          'Content-Type': result.mimeType,
          'X-Frame-Options': 'SAMEORIGIN', // Allow iframe preview
        },
      });
    } else {
      // PDF format
      const pdfBuffer = result.content as Buffer;
      return new Response(new Uint8Array(pdfBuffer), {
        headers: {
          'Content-Type': result.mimeType,
          'Content-Disposition': 'inline; filename="preview.pdf"',
        },
      });
    }

  } catch (error) {
    console.error('Document preview error:', error);

    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { 
          error: 'Invalid request data',
          details: error.issues,
        },
        { status: 400 }
      );
    }

    if (error instanceof Error) {
      // Handle specific paperwork service errors
      if (error.message.includes('not found')) {
        return NextResponse.json({ error: error.message }, { status: 404 });
      }

      if (error.message.includes('template')) {
        return NextResponse.json({ error: error.message }, { status: 400 });
      }
    }

    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}