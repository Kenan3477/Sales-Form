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
  console.log('📝 Document generation request started');
  
  try {
    // Rate limiting
    const clientIP = request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || 'unknown';
    console.log('📝 Client IP:', clientIP);
    
    const rateLimitCheck = await checkApiRateLimit(clientIP);
    if (!rateLimitCheck.success) {
      console.log('❌ Rate limit exceeded');
      return NextResponse.json(
        { error: 'Rate limit exceeded. Please try again later.' },
        { status: 429 }
      );
    }

    // Authentication
    const session = await getServerSession(authOptions);
    if (!session?.user) {
      console.log('❌ No session or user found');
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }
    console.log('✅ User authenticated:', session.user.email);

    // Parse and validate request body
    const body = await request.json();
    console.log('📝 Request body:', body);
    
    const validatedData = generateDocumentSchema.parse(body);
    console.log('✅ Request data validated:', validatedData);

    // Initialize enhanced template service
    const enhancedTemplateService = new EnhancedTemplateService();
    console.log('✅ Enhanced template service initialized');

    // Load sale data for document generation
    const { prisma } = await import('@/lib/prisma');
    console.log('📝 Loading sale data for ID:', validatedData.saleId);
    
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
      console.log('❌ Sale not found for ID:', validatedData.saleId);
      return NextResponse.json({ error: 'Sale not found' }, { status: 404 });
    }
    
    console.log('✅ Sale loaded:', {
      id: sale.id,
      customer: `${sale.customerFirstName} ${sale.customerLastName}`,
      email: sale.email
    });

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
    console.log('📝 Looking for template:', { 
      templateType: validatedData.templateType, 
      isActive: true 
    });
    
    const template = await prisma.documentTemplate.findFirst({
      where: {
        templateType: validatedData.templateType,
        isActive: true
      }
    });

    if (!template) {
      console.log('❌ Template not found for type:', validatedData.templateType);
      
      // List available templates for debugging
      const availableTemplates = await prisma.documentTemplate.findMany({
        where: { isActive: true },
        select: { templateType: true, name: true }
      });
      console.log('📋 Available templates:', availableTemplates);
      
      return NextResponse.json({ error: 'Template not found' }, { status: 404 });
    }
    
    console.log('✅ Template found:', {
      id: template.id,
      name: template.name,
      type: template.templateType
    });

    // Generate the document using enhanced service
    console.log('📝 Generating document with template data...');
    console.log('🧪 Template data being used:', JSON.stringify(templateData, null, 2));
    
    // For now, use the hardcoded template while we ensure the database template matches
    const result = await enhancedTemplateService.generateDocument('welcome-letter', templateData);
    console.log('✅ Document generated, length:', result.length);
    console.log('📄 Document preview (first 500 chars):', result.substring(0, 500));
    console.log('📄 Document contains Flash Team:', result.includes('Flash Team'));
    console.log('📄 Document contains CSS:', result.includes('linear-gradient'));

    // Generate filename 
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const fileName = `welcome-letter-${sale.customerFirstName}-${sale.customerLastName}-${timestamp}.html`;
    
    // Note: On Vercel/serverless platforms, we can't write to the local file system
    // So we store the document content directly in the database metadata instead
    console.log(`📄 Storing document in database (serverless environment)`);

    // Create GeneratedDocument record in database
    console.log('📝 Creating GeneratedDocument record with data:', {
      saleId: sale.id,
      templateId: template.id,
      filename: fileName,
      fileSize: Buffer.byteLength(result, 'utf8'),
      mimeType: 'text/html'
    });

    const generatedDocument = await prisma.generatedDocument.create({
      data: {
        saleId: sale.id,
        templateId: template.id,
        filename: fileName,
        filePath: `virtual://generated-documents/${fileName}`, // Virtual path since we can't write to filesystem
        fileSize: Buffer.byteLength(result, 'utf8'),
        mimeType: 'text/html',
        metadata: {
          templateType: validatedData.templateType,
          customerName: templateData.customerName,
          generationMethod: 'enhanced-template-service',
          // Store the actual content in metadata since we can't write to filesystem
          documentContent: result
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
    console.error('❌ Document generation error:', error);
    console.error('❌ Error stack:', error instanceof Error ? error.stack : 'No stack trace');

    if (error instanceof z.ZodError) {
      console.error('❌ Validation error details:', error.issues);
      return NextResponse.json(
        { 
          error: 'Invalid request data',
          details: error.issues,
        },
        { status: 400 }
      );
    }

    if (error instanceof Error) {
      console.error('❌ Known error:', error.message);
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