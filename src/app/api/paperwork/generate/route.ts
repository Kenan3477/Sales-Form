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
      policyNumber: `TFT${String(Math.floor(Math.random() * 10000)).padStart(4, '0')}`, // Format: TFT0123
      totalCost: (sale.totalPlanCost * 12).toFixed(2), // Annual cost = monthly * 12
      monthlyCost: sale.totalPlanCost.toFixed(2), // Monthly cost
      hasApplianceCover: sale.applianceCoverSelected,
      hasBoilerCover: sale.boilerCoverSelected,
      appliances: sale.appliances.map(appliance => ({
        name: appliance.appliance + (appliance.otherText ? ` (${appliance.otherText})` : ''),
        coverLimit: `£${appliance.coverLimit.toFixed(2)}`,
        monthlyCost: `£${appliance.cost.toFixed(2)}`
      })),
      boilerCost: sale.boilerPriceSelected ? `£${sale.boilerPriceSelected.toFixed(2)}` : null,
      currentDate: new Date().toLocaleDateString('en-GB', { 
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      }),
      // Add agreement structure for backward compatibility with existing template
      agreement: {
        coverage: {
          hasBoilerCover: sale.boilerCoverSelected,
          boilerPriceFormatted: sale.boilerPriceSelected ? `£${sale.boilerPriceSelected.toFixed(2)}/month` : null
        }
      },
      metadata: {
        agentName: sale.agentName || sale.createdBy?.email || 'Flash Team Support'
      }
    };

    // Find the template record
    const template = await prisma.documentTemplate.findFirst({
      where: {
        templateType: validatedData.templateType,
        isActive: true
      }
    });

    if (!template) {
      return NextResponse.json({ error: 'Template not found' }, { status: 404 });
    }

    // Generate the document using enhanced service
    const result = await enhancedTemplateService.generateDocument('welcome-letter', templateData);

    // Generate filename and file path
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const fileName = `welcome-letter-${sale.customerFirstName}-${sale.customerLastName}-${timestamp}.html`;
    const filePath = `storage/documents/${fileName}`;

    // Save the document content to file
    const fs = await import('fs/promises');
    const path = await import('path');
    
    // Ensure storage directory exists
    const fullStoragePath = path.join(process.cwd(), 'storage/documents');
    await fs.mkdir(fullStoragePath, { recursive: true });
    
    // Write the document content to file
    const fullFilePath = path.join(process.cwd(), filePath);
    await fs.writeFile(fullFilePath, result, 'utf8');

    // Create GeneratedDocument record in database
    console.log('📝 Creating GeneratedDocument record with data:', {
      saleId: sale.id,
      templateId: template.id,
      filename: fileName,
      filePath: filePath,
      fileSize: Buffer.byteLength(result, 'utf8'),
      mimeType: 'text/html'
    });

    const generatedDocument = await prisma.generatedDocument.create({
      data: {
        saleId: sale.id,
        templateId: template.id,
        filename: fileName,
        filePath: filePath,
        fileSize: Buffer.byteLength(result, 'utf8'),
        mimeType: 'text/html',
        metadata: {
          templateType: validatedData.templateType,
          customerName: templateData.customerName,
          generationMethod: 'enhanced-template-service'
        }
      }
    });

    console.log('📝 Successfully created GeneratedDocument:', generatedDocument.id);

    return NextResponse.json({
      success: true,
      document: {
        id: generatedDocument.id,
        content: result,
        fileName: fileName,
        templateName: template.name,
        saleId: sale.id,
        customerName: `${sale.customerFirstName} ${sale.customerLastName}`,
        customerEmail: sale.email,
        generatedAt: generatedDocument.generatedAt.toISOString(),
        downloadUrl: `/api/paperwork/download/${generatedDocument.id}`
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