import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { EnhancedTemplateService } from '@/lib/paperwork/enhanced-template-service';
import { checkApiRateLimit } from '@/lib/rateLimit';
import chromium from '@sparticuz/chromium';
import puppeteer from 'puppeteer';
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
    console.log('📄 Request body received:', JSON.stringify(body, null, 2));
    
    const { saleIds, templateIds } = bulkGenerateSchema.parse(body);
    console.log('📄 Validated data:', { 
      saleIds: saleIds.length > 0 ? `${saleIds.length} sales: [${saleIds.slice(0, 3).map(id => id.slice(-6)).join(', ')}${saleIds.length > 3 ? '...' : ''}]` : 'none',
      templateIds: templateIds.length > 0 ? `${templateIds.length} templates: [${templateIds.join(', ')}]` : 'none'
    });

    // Limit batch size to prevent timeout
    const totalCombinations = saleIds.length * templateIds.length;
    if (totalCombinations > 50) {
      return NextResponse.json({
        error: `Batch too large (${totalCombinations} documents). Please select fewer items (max 50 documents per batch).`,
        maxRecommended: Math.floor(50 / templateIds.length)
      }, { status: 400 });
    }

    // Debug: Check what templates exist in the database
    const { prisma } = await import('@/lib/prisma');
    const allTemplates = await prisma.documentTemplate.findMany({
      select: { id: true, name: true, templateType: true, isActive: true }
    });
    console.log('📄 Available database templates:', allTemplates);
    
    // Enhanced Template Service built-in templates
    const enhancedServiceTemplates = ['welcome-letter', 'service-agreement', 'direct-debit-form', 'coverage-summary'];
    console.log('📄 Enhanced Service templates:', enhancedServiceTemplates);
    
    // Check if the requested templates exist (either in database or enhanced service)
    const invalidTemplates = templateIds.filter(id => {
      const inDatabase = allTemplates.find(t => t.id === id && t.isActive);
      const inEnhancedService = enhancedServiceTemplates.includes(id);
      console.log(`📄 Checking template ${id}: inDB=${!!inDatabase}, inEnhanced=${inEnhancedService}`);
      return !inDatabase && !inEnhancedService;
    });
    
    if (invalidTemplates.length > 0) {
      console.error('❌ Invalid template IDs:', invalidTemplates);
      const validIds = [
        ...allTemplates.filter(t => t.isActive).map(t => t.id),
        ...enhancedServiceTemplates
      ];
      console.log('📄 Valid template IDs:', validIds);
      return NextResponse.json({
        error: `Invalid template IDs: ${invalidTemplates.join(', ')}`,
        validTemplateIds: validIds,
        requestedTemplates: templateIds,
        databaseTemplates: allTemplates.filter(t => t.isActive).map(t => ({ id: t.id, name: t.name })),
        enhancedTemplates: enhancedServiceTemplates
      }, { status: 400 });
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

    // Track which sales have been processed for document status
    const processedSales = new Set<string>();

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
          });        // Generate document using Enhanced Template Service
        console.log(`📄 Generating document for ${sale.customerFirstName} ${sale.customerLastName}...`);
        console.log('🧪 Template data prepared');
        let documentContent;
        
        try {
          // ALWAYS use Enhanced Template Service for consistent beautiful templates
          console.log('📄 Using Enhanced Template Service for consistent Flash Team branding');
          // Use the original templateId for EnhancedTemplateService (e.g., 'welcome-letter')
          const templateIdForGeneration = isEnhancedServiceTemplate ? templateId : 'welcome-letter';
          documentContent = await enhancedTemplateService.generateDocument(templateIdForGeneration, templateData);
          
          console.log(`✅ Generated document content length: ${documentContent.length}`);
          
          if (!documentContent || documentContent.length < 100) {
            throw new Error(`Generated content is too short (${documentContent?.length || 0} chars) - likely generation failed`);
          }
        } catch (enhancedServiceError) {
          console.error(`❌ Template generation error:`, enhancedServiceError);
          throw new Error(`Template generation failed: ${enhancedServiceError instanceof Error ? enhancedServiceError.message : 'Unknown template error'}`);
        }
        
        // Generate PDF using the Enhanced Template Service HTML content
        const pdfBytes = await generateFlashTeamPDF(templateData);
        
        // Generate PDF filename and metadata
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const fileName = `${template.templateType}-${sale.customerFirstName}-${sale.customerLastName}-${timestamp}.pdf`;
        
        // Note: On Vercel/serverless platforms, we can't write to the local file system
        // So we store the document content directly in the database instead
        console.log(`📄 Storing document in database (serverless environment)`);

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
            console.log(`📄 Using existing template for ${template.templateType}`);
            dbTemplate = existingTemplate;
          } else {
            console.log(`📄 Creating new template for ${template.templateType}`);
            // Find the highest version for this template type to avoid conflicts
            const latestTemplate = await prisma.documentTemplate.findFirst({
              where: {
                templateType: template.templateType
              },
              orderBy: {
                version: 'desc'
              }
            });
            
            const nextVersion = latestTemplate ? latestTemplate.version + 1 : 1;
            
            // Create a database template record for this Flash Team PDF template
            dbTemplate = await prisma.documentTemplate.create({
              data: {
                name: template.name,
                templateType: template.templateType,
                htmlContent: `Flash Team PDF Template - Generated content stored as PDF binary`, // Placeholder since we generate PDFs
                description: `Auto-created Flash Team PDF template for ${template.name}`,
                isActive: true,
                version: nextVersion,
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
            filePath: `virtual://generated-documents/${fileName}`, // Virtual path since we can't write to filesystem
            fileSize: pdfBytes.length,
            mimeType: 'application/pdf',
            metadata: {
              templateType: template.templateType,
              customerName: templateData.customerName,
              generationMethod: 'flash-team-pdf-bulk',
              originalTemplateId: templateId,
              // Store the PDF content as base64 in metadata since we can't write to filesystem
              documentContent: pdfBytes.toString('base64')
            }
          }
        });
        
        const document = {
          id: generatedDocument.id,
          content: pdfBytes.toString('base64'), // PDF as base64
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
        
        // Mark the sale as having documents generated (only once per sale)
        if (!processedSales.has(saleId)) {
          await prisma.sale.update({
            where: { id: sale.id },
            data: {
              documentsGenerated: true,
              documentsGeneratedAt: new Date(),
              documentsGeneratedBy: session.user.id
            }
          });
          processedSales.add(saleId);
          console.log(`✅ Sale ${sale.id} marked as having documents generated`);
        }
        
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
      const validationDetails = error.issues.map(issue => `${issue.path.join('.')}: ${issue.message}`);
      return NextResponse.json(
        { 
          error: 'Invalid request data', 
          details: error.issues,
          message: `Validation failed: ${validationDetails.join(', ')}`
        },
        { status: 400 }
      );
    }

    // Check if error is due to missing data
    if (error instanceof Error) {
      if (error.message.includes('Invalid template IDs') || error.message.includes('Batch too large')) {
        return NextResponse.json(
          { error: error.message },
          { status: 400 }
        );
      }
    }

    return NextResponse.json(
      { error: 'Internal server error', message: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

// ---------- Flash Team PDF Generator ----------
function escapeHtml(v: any): string {
  if (v === null || v === undefined) return "";
  return String(v)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function money(v: any): string {
  if (v === null || v === undefined || v === "") return "";
  const n = Number(v);
  if (Number.isFinite(n)) return n.toFixed(2);
  return String(v);
}

function joinAddressLines(addr: any): string {
  if (!addr) return "";
  if (Array.isArray(addr)) return addr.filter(Boolean).join("<br/>");
  return escapeHtml(addr).replace(/\n/g, "<br/>");
}

function buildFlashTeamHtml(data: any): string {
  const d = data || {};
  const customerName = escapeHtml(d.customerName || "");
  const email = escapeHtml(d.email || "");
  const phone = escapeHtml(d.phone || "");
  const address = joinAddressLines(d.address || "");
  const coverageStartDate = escapeHtml(d.coverageStartDate || "");
  const policyNumber = escapeHtml(d.policyNumber || "");
  const monthlyCost = d.monthlyCost !== undefined && d.monthlyCost !== null && d.monthlyCost !== ""
    ? money(d.monthlyCost)
    : "";

  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flash Team Protection Plan</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #fff;
            padding: 20px;
        }
        .container {
            max-width: 210mm;
            margin: 0 auto;
            background: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            border-bottom: 3px solid #1a237e;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .logo {
            flex: 1;
        }
        .company-name {
            font-size: 32px;
            font-weight: bold;
            color: #1a237e;
            margin-bottom: 5px;
        }
        .tagline {
            font-size: 14px;
            color: #666;
            font-style: italic;
        }
        .document-title {
            flex: 1;
            text-align: right;
        }
        .document-title h1 {
            font-size: 24px;
            color: #1a237e;
            margin-bottom: 10px;
        }
        .policy-number {
            font-size: 16px;
            color: #666;
            font-weight: bold;
        }
        .customer-details {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 30px;
            border-left: 4px solid #ff6b35;
        }
        .customer-details h2 {
            color: #1a237e;
            margin-bottom: 15px;
            font-size: 20px;
        }
        .detail-row {
            margin-bottom: 10px;
            display: flex;
            align-items: flex-start;
        }
        .detail-label {
            font-weight: bold;
            color: #1a237e;
            min-width: 120px;
            margin-right: 15px;
        }
        .coverage-section {
            margin-bottom: 30px;
        }
        .coverage-section h2 {
            color: #1a237e;
            border-bottom: 2px solid #ff6b35;
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-size: 20px;
        }
        .coverage-item {
            background: #fff;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .coverage-item h3 {
            color: #1a237e;
            margin-bottom: 8px;
            font-size: 16px;
        }
        .cost-summary {
            background: linear-gradient(135deg, #1a237e 0%, #303f9f 100%);
            color: #fff;
            padding: 25px;
            border-radius: 8px;
            margin-top: 30px;
            text-align: center;
        }
        .cost-summary h2 {
            margin-bottom: 15px;
            font-size: 22px;
        }
        .monthly-cost {
            font-size: 36px;
            font-weight: bold;
            margin: 10px 0;
        }
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
            text-align: center;
            color: #666;
            font-size: 12px;
        }
        .footer .company-info {
            margin-bottom: 10px;
        }
        .footer .contact-info {
            font-weight: bold;
            color: #1a237e;
        }
        @media print {
            body { padding: 0; }
            .container { box-shadow: none; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">
                <div class="company-name">Flash Team</div>
                <div class="tagline">Protection Plans</div>
            </div>
            <div class="document-title">
                <h1>Protection Plan Agreement</h1>
                <div class="policy-number">Policy: ${policyNumber}</div>
            </div>
        </div>

        <div class="customer-details">
            <h2>Customer Information</h2>
            <div class="detail-row">
                <span class="detail-label">Name:</span>
                <span>${customerName}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Email:</span>
                <span>${email}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Phone:</span>
                <span>${phone}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Address:</span>
                <span>${address}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Coverage Start:</span>
                <span>${coverageStartDate}</span>
            </div>
        </div>

        <div class="coverage-section">
            <h2>Coverage Details</h2>
            
            <div class="coverage-item">
                <h3>🔧 Appliance Cover</h3>
                <p><strong>Status:</strong> ${d.applianceCover || 'No'}</p>
                <p>Comprehensive protection for your household appliances including repairs, parts, and labor costs.</p>
            </div>

            <div class="coverage-item">
                <h3>🏠 Boiler Cover</h3>
                <p><strong>Status:</strong> ${d.boilerCover || 'No'}</p>
                <p>Complete boiler protection including annual service, emergency repairs, and replacement parts.</p>
            </div>
        </div>

        <div class="cost-summary">
            <h2>Monthly Investment</h2>
            <div class="monthly-cost">£${monthlyCost}</div>
            <p>Your monthly protection plan cost</p>
        </div>

        <div class="footer">
            <div class="company-info">
                Flash Team Protection Plans - Your trusted partner in home protection
            </div>
            <div class="contact-info">
                📞 Support: 0800-FLASH-TEAM | 📧 support@flashteam.co.uk
            </div>
        </div>
    </div>
</body>
</html>`;
}

async function generateFlashTeamPDF(data: any): Promise<Buffer> {
  // Configure for serverless environment
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
  
  if (process.env.VERCEL || process.env.NODE_ENV === 'production') {
    try {
      executablePath = await chromium.executablePath();
      args = (chromium as any).args.concat(args);
    } catch (e) {
      console.warn('Could not get chromium executable path:', e);
    }
  }
  
  const browser = await puppeteer.launch({
    headless: true,
    executablePath,
    args,
  });
  
  try {
    const page = await browser.newPage();
    
    // Use Enhanced Template Service instead of hardcoded HTML
    const templateService = new EnhancedTemplateService();
    const htmlContent = await templateService.generateDocument('welcome-letter', {
      customerName: data.customerName || '[Customer Name]',
      email: data.email || '',
      phone: data.phone || '',
      address: data.address || '',
      coverageStartDate: data.coverageStartDate || '',
      policyNumber: data.policyNumber || '',
      monthlyCost: data.monthlyCost || '',
      totalCost: data.totalCost || data.monthlyCost || ''
    });
    
    await page.setContent(htmlContent, { waitUntil: 'networkidle0' });
    
    const pdfBuffer = await page.pdf({
      format: 'A4',
      margin: { top: '1cm', bottom: '1cm', left: '1cm', right: '1cm' },
      printBackground: true,
      preferCSSPageSize: true
    });
    
    return Buffer.from(pdfBuffer);
  } finally {
    await browser.close();
  }
}