import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { EnhancedTemplateService } from '@/lib/paperwork/enhanced-template-service';
import { checkApiRateLimit } from '@/lib/rateLimit';
import { z } from 'zod';

// Request validation schema
const generateDocumentSchema = z.object({
  saleId: z.string().min(1),
  templateType: z.enum(['welcome_letter', 'service_agreement', 'direct_debit_form', 'coverage_summary']),
  templateId: z.string().optional(),
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
    const validatedData = generateDocumentSchema.parse(body);

    // Initialize enhanced template service
    const enhancedTemplateService = new EnhancedTemplateService();

    // Load sale data for document generation
    const { prisma } = await import('@/lib/prisma');
    const sale = await prisma.sale.findUnique({
      where: { id: validatedData.saleId },
      include: {
        appliances: true,
        createdBy: {
          select: {
            email: true,
          }
        }
      }
    });

    if (!sale) {
      return NextResponse.json({ error: 'Sale not found' }, { status: 404 });
    }

    // Check user permissions (agents can only generate for their own sales)
    if (session.user.role === 'AGENT') {
      if (sale.createdById !== session.user.id) {
        return NextResponse.json({ error: 'Access denied' }, { status: 403 });
      }
    }

    // Transform sale data for template
    const templateData = {
      customerName: `${sale.customerFirstName} ${sale.customerLastName}`,
      email: sale.email,
      phone: sale.phoneNumber,
      address: `${sale.mailingStreet}, ${sale.mailingCity}, ${sale.mailingProvince}, ${sale.mailingPostalCode}`,
      coverageStartDate: new Date().toLocaleDateString('en-GB'),
      policyNumber: `FT-2025-${sale.id.slice(-6)}`,
      totalCost: sale.totalPlanCost.toString(),
      monthlyCost: (sale.totalPlanCost / 12).toFixed(2),
      hasApplianceCover: sale.applianceCoverSelected,
      hasBoilerCover: sale.boilerCoverSelected,
      currentDate: new Date().toLocaleDateString('en-GB', { 
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      })
    };

    // Generate the document using enhanced service
    const result = await enhancedTemplateService.generateDocument('welcome-letter', templateData);

    return NextResponse.json({
      success: true,
      document: {
        id: `doc-${Date.now()}`,
        content: result,
        fileName: `welcome-letter-${sale.customerFirstName}-${sale.customerLastName}.html`,
        templateName: 'Flash Team Welcome Letter',
        saleId: sale.id,
        customerName: `${sale.customerFirstName} ${sale.customerLastName}`,
        customerEmail: sale.email,
        generatedAt: new Date().toISOString(),
        downloadUrl: `/api/paperwork/download/${sale.id}`
      }
    });

  } catch (error) {
    console.error('Document generation error:', error);

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