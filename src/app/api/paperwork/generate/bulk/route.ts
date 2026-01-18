import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { EnhancedTemplateService } from '@/lib/paperwork/enhanced-template-service';
import { checkApiRateLimit } from '@/lib/rateLimit';
import { z } from 'zod';

// Bulk generation schema
const bulkGenerateSchema = z.object({
  saleIds: z.array(z.string().min(1)).min(1),
  templateIds: z.array(z.string().min(1)).min(1),
});

export async function POST(request: NextRequest) {
  console.log('📄 Bulk generation request started');
  
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

    // Authentication - only admins can bulk generate
    const session = await getServerSession(authOptions);
    if (!session?.user || session.user.role !== 'ADMIN') {
      console.log('❌ Access denied - not admin');
      return NextResponse.json({ error: 'Admin access required' }, { status: 403 });
    }

    // Parse and validate request body
    const body = await request.json();
    console.log('📄 Request body received:', body);
    
    const { saleIds, templateIds } = bulkGenerateSchema.parse(body);
    console.log('📄 Validated data:', { saleIds, templateIds });

    // Debug: Check what templates exist in the database
    const { prisma } = await import('@/lib/prisma');
    const allTemplates = await prisma.documentTemplate.findMany({
      select: { id: true, name: true, templateType: true, isActive: true }
    });
    console.log('📄 Available templates in database:', allTemplates);
    
    // Check if the requested templates exist
    const missingTemplates = templateIds.filter(id => 
      !allTemplates.find(t => t.id === id && t.isActive)
    );
    if (missingTemplates.length > 0) {
      console.error('❌ Missing template IDs:', missingTemplates);
      console.log('📄 Valid template IDs:', allTemplates.filter(t => t.isActive).map(t => t.id));
    }

    // Initialize enhanced template service
    const enhancedTemplateService = new EnhancedTemplateService();
    
    // Track results
    const results: {
      generated: number;
      failed: number;
      errors: string[];
      documents: any[];
    } = {
      generated: 0,
      failed: 0,
      errors: [],
      documents: []
    };

    // Generate documents for each sale and template combination
    for (const saleId of saleIds) {
      for (const templateId of templateIds) {
        try {
          console.log(`📄 Processing sale ID: ${saleId} with template ID: ${templateId}`);
          
          // Load sale data
          const sale = await prisma.sale.findUnique({
            where: { id: saleId },
            include: {
              appliances: true,
              createdBy: {
                select: { email: true }
              }
            }
          });

          if (!sale) {
            console.log(`❌ Sale ${saleId} not found in database`);
            results.failed++;
            results.errors.push(`Sale ${saleId.slice(-6)}: Sale not found`);
            continue;
          }
          
          console.log(`✅ Found sale: ${sale.customerFirstName} ${sale.customerLastName}`);

          // Find the template in database OR use EnhancedTemplateService template
          let template;
          let isEnhancedServiceTemplate = false;
          
          // Check if this is an EnhancedTemplateService template ID
          if (['welcome-letter', 'service-agreement', 'direct-debit-form', 'coverage-summary'].includes(templateId)) {
            console.log(`📄 Using EnhancedTemplateService template: ${templateId}`);
            isEnhancedServiceTemplate = true;
            template = {
              id: templateId,
              name: templateId.replace('-', ' ').replace(/\b\w/g, (l: string) => l.toUpperCase()),
              templateType: templateId.replace('-', '_')
            };
          } else {
            // Look for database template
            template = await prisma.documentTemplate.findFirst({
              where: {
                id: templateId,
                isActive: true
              }
            });
          }

          if (!template) {
            console.log(`❌ Template ${templateId} not found`);
            results.failed++;
            results.errors.push(`Sale ${saleId.slice(-6)}: Template ${templateId.slice(-6)} not found`);
            continue;
          }
          
          console.log(`✅ Found template: ${template.name} (${template.templateType})`);

          // Check if this is an EnhancedTemplateService template ID or database template ID
          let templateForGeneration;
          if (['welcome-letter', 'service-agreement', 'direct-debit-form', 'coverage-summary'].includes(templateId)) {
            // This is an EnhancedTemplateService template ID
            console.log(`📄 Using EnhancedTemplateService template: ${templateId}`);
            templateForGeneration = { 
              id: templateId, 
              name: templateId.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase()),
              templateType: templateId.replace('-', '_') 
            };
          } else {
            // This should be a database template - but we already handled this above
            templateForGeneration = template;
          }

          // Transform sale data for template
          const templateData = {
            customerName: `${sale.customerFirstName} ${sale.customerLastName}`,
            email: sale.email,
            phone: sale.phoneNumber,
            address: `${sale.mailingStreet || ''}, ${sale.mailingCity || ''}, ${sale.mailingProvince || ''}, ${sale.mailingPostalCode || ''}`.replace(/^,\s*|,\s*$/g, ''), // Clean up empty address parts
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

          console.log(`📄 Template data prepared for ${sale.customerFirstName} ${sale.customerLastName}:`, {
            customerName: templateData.customerName,
            email: templateData.email,
            phone: templateData.phone,
            hasValidAddress: !!templateData.address && templateData.address.length > 5,
            totalCost: templateData.totalCost,
            monthlyCost: templateData.monthlyCost,
            appliancesCount: templateData.appliances.length,
            hasBoilerCover: templateData.hasBoilerCover
          });        // Generate document using enhanced service
        console.log(`📄 Generating document using Enhanced Template Service...`);
        let documentContent;
        
        try {
          // Use the original templateId for EnhancedTemplateService (e.g., 'welcome-letter')
          const templateIdForGeneration = isEnhancedServiceTemplate ? templateId : 'welcome-letter';
          documentContent = await enhancedTemplateService.generateDocument(templateIdForGeneration, templateData);
          console.log(`✅ Generated document content length: ${documentContent.length}`);
          
          if (!documentContent || documentContent.length < 100) {
            throw new Error(`Generated content is too short (${documentContent?.length || 0} chars) - likely generation failed`);
          }
        } catch (enhancedServiceError) {
          console.error(`❌ Enhanced Template Service error:`, enhancedServiceError);
          throw new Error(`Template generation failed: ${enhancedServiceError instanceof Error ? enhancedServiceError.message : 'Unknown template error'}`);
        }
        
        // Generate filename and file path
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const fileName = `${template.templateType}-${sale.customerFirstName}-${sale.customerLastName}-${timestamp}.html`;
        const filePath = `storage/documents/${fileName}`;

        // Save the document content to file
        const fs = await import('fs/promises');
        const path = await import('path');
        
        // Ensure storage directory exists
        const fullStoragePath = path.join(process.cwd(), 'storage/documents');
        await fs.mkdir(fullStoragePath, { recursive: true });
        
        // Write the document content to file
        const fullFilePath = path.join(process.cwd(), filePath);
        await fs.writeFile(fullFilePath, documentContent, 'utf8');

        // Create GeneratedDocument record in database
        // For EnhancedTemplateService templates, we need to find or create a database template
        let dbTemplate = template;
        if (isEnhancedServiceTemplate) {
          // Try to find existing database template with this templateType
          const existingTemplate = await prisma.documentTemplate.findFirst({
            where: {
              templateType: template.templateType,
              isActive: true
            }
          });
          
          if (existingTemplate) {
            dbTemplate = existingTemplate;
          } else {
            console.log(`📄 Creating database template for ${template.templateType}`);
            // Create a database template record for this EnhancedTemplateService template
            dbTemplate = await prisma.documentTemplate.create({
              data: {
                name: template.name,
                templateType: template.templateType,
                htmlContent: documentContent, // Use the generated content as template
                description: `Auto-created template for ${template.name}`,
                isActive: true,
                version: 1,
                createdById: 'cmkfyoun90000kk62g97wyhsx' // Default to admin user - this should be dynamic
              }
            });
          }
        }
        
        const generatedDocument = await prisma.generatedDocument.create({
          data: {
            saleId: sale.id,
            templateId: dbTemplate.id,
            filename: fileName,
            filePath: filePath,
            fileSize: Buffer.byteLength(documentContent, 'utf8'),
            mimeType: 'text/html',
            metadata: {
              templateType: template.templateType,
              customerName: templateData.customerName,
              generationMethod: isEnhancedServiceTemplate ? 'enhanced-template-service-bulk' : 'database-template-bulk',
              originalTemplateId: templateId
            }
          }
        });
        
        const document = {
          id: generatedDocument.id,
          content: documentContent,
          fileName: fileName,
          templateName: template.name,
          saleId: sale.id,
          customerName: `${sale.customerFirstName} ${sale.customerLastName}`,
          customerEmail: sale.email,
          generatedAt: generatedDocument.generatedAt.toISOString(),
          downloadUrl: `/api/paperwork/download/${generatedDocument.id}`
        };

        results.documents.push(document);
        results.generated++;
        console.log(`✅ Successfully generated document for ${sale.customerFirstName} ${sale.customerLastName}`);
        
      } catch (error) {
        results.failed++;
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        results.errors.push(`Sale ${saleId.slice(-6)}: ${errorMessage}`);
        console.error(`❌ Bulk generation error for sale ${saleId}:`, error);
      }
      }
    }

    console.log(`📄 Bulk generation complete. Generated: ${results.generated}, Failed: ${results.failed}`);

    return NextResponse.json({
      success: true,
      ...results,
      total: saleIds.length * templateIds.length // Updated to reflect sale x template combinations
    });

  } catch (error) {
    console.error('❌ Bulk generate documents error:', error);

    if (error instanceof z.ZodError) {
      console.error('❌ Validation error:', error.issues);
      return NextResponse.json(
        { error: 'Invalid request data', details: error.issues },
        { status: 400 }
      );
    }

    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}