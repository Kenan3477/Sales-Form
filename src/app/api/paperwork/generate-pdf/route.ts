import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { checkApiRateLimit } from '@/lib/rateLimit';
import { z } from 'zod';
import chromium from '@sparticuz/chromium';
import puppeteer from 'puppeteer';
import { EnhancedTemplateService } from '@/lib/paperwork/enhanced-template-service';
import { WiseguysProfessionalTemplateService } from '@/lib/paperwork/wiseguys-professional-template';

// Request validation schema
const generateDocumentSchema = z.object({
  saleId: z.string().min(1),
  templateType: z.enum(['welcome_letter', 'service_agreement', 'direct_debit_form', 'coverage_summary', 'uncontacted_customer_notice', 'wiseguys-tech-plan']),
  templateId: z.string().optional(),
});

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

function safeFilename(s: string): string {
  return String(s || "protection-plan")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "")
    .slice(0, 80);
}

// Generate PDF using appropriate template service
async function generatePDF(templateType: string, data: any): Promise<Buffer> {
  let html: string;
  
  // Choose the appropriate template service
  if (templateType === 'wiseguys-tech-plan') {
    console.log('📄 Using Wiseguys Professional Template Service');
    html = await WiseguysProfessionalTemplateService.renderTemplate('wiseguys-tech-plan', {
      customerName: data.customerName || '[Customer Name]',
      customerAddress: data.address || '[Customer Address]',
      planType: 'Remote Support Tech Plan',
      monthlyPrice: data.monthlyCost || '0.00',
      planId: data.policyNumber || 'PLAN001'
    });
  } else {
    console.log('📄 Using Enhanced Template Service (Flash Team)');
    const templateService = new EnhancedTemplateService();
    html = await templateService.generateDocument('welcome-letter', {
      customerName: data.customerName || '[Customer Name]',
      email: data.email || '',
      phone: data.phone || '',
      address: data.address || '',
      coverageStartDate: data.coverageStartDate || '',
      policyNumber: data.policyNumber || '',
      monthlyCost: data.monthlyCost || '',
      totalCost: data.totalCost || data.monthlyCost || ''
    });
  }

  console.log('📄 HTML generated, length:', html.length);

  // Configure for serverless environment with better error handling
  let executablePath: string | undefined;
  let args: string[] = [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--disable-accelerated-2d-canvas',
    '--no-first-run',
    '--no-zygote',
    '--disable-gpu',
    '--disable-web-security',
    '--disable-features=VizDisplayCompositor'
  ];
  
  // Try to use system Chrome for development, bundled chromium for production
  try {
    if (process.env.NODE_ENV === 'development') {
      // In development, try to use system Chrome
      const { execSync } = await import('child_process');
      const systemChromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
      execSync(`ls "${systemChromePath}"`, { stdio: 'ignore' });
      executablePath = systemChromePath;
      console.log('📄 Using system Chrome for development');
    }
  } catch (e) {
    console.log('📄 System Chrome not found, trying bundled chromium');
  }
  
  if (!executablePath && (process.env.VERCEL || process.env.NODE_ENV === 'production')) {
    try {
      executablePath = await chromium.executablePath();
      args = [...chromium.args, ...args];
      console.log('📄 Using bundled chromium for production');
    } catch (e) {
      console.error('📄 Could not get chromium executable path:', e);
      throw new Error('PDF generation not available - Chromium executable not found');
    }
  }

  if (!executablePath) {
    throw new Error('No Chrome/Chromium executable found for PDF generation');
  }

  console.log('📄 Launching browser with args:', args.length);
  
  let browser;
  try {
    browser = await puppeteer.launch({
      headless: true,
      executablePath,
      args,
      timeout: 30000, // 30 second timeout
    });
    console.log('📄 Browser launched successfully');
  } catch (error) {
    console.error('📄 Browser launch failed:', error);
    throw new Error(`PDF generation failed: ${error instanceof Error ? error.message : 'Browser launch error'}`);
  }
  
  try {
    const page = await browser.newPage();
    console.log('📄 New page created');
    
    await page.setContent(html, { 
      waitUntil: "domcontentloaded", // Changed from networkidle0 to be faster
      timeout: 30000 // Increased timeout to 30 seconds
    });
    console.log('📄 Content set on page');
    
    // Wait a bit for any CSS animations or transitions to complete
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    await page.emulateMediaType("print");
    console.log('📄 Print media type emulated');
    
    const pdfBuffer = await page.pdf({
      format: "A4",
      printBackground: true,
      margin: {
        top: '0.1in',
        right: '0.1in',
        bottom: '0.1in',
        left: '0.1in'
      },
      scale: 1.0,
      timeout: 15000 // 15 second timeout for PDF generation
    });
    
    console.log('📄 PDF generated, size:', pdfBuffer.length, 'bytes');
    return Buffer.from(pdfBuffer);
  } catch (error) {
    console.error('📄 PDF generation error:', error);
    throw new Error(`PDF generation failed: ${error instanceof Error ? error.message : 'Unknown PDF error'}`);
  } finally {
    await browser.close();
    console.log('📄 Browser closed');
  }
}

export async function POST(request: NextRequest) {
  console.log('📝 Document generation request started - FLASH TEAM PDF ONLY');
  
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
    console.log('✅ Request data validated - WILL GENERATE PDF ONLY:', validatedData);

    // Initialize template data for Flash Team PDF
    console.log('📝 Preparing data for Flash Team PDF generation');

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
      // New coverage fields for template
      applianceCount: sale.appliances.length,
      boilerCover: sale.boilerCoverSelected,
      annualBoilerService: sale.boilerCoverSelected, // Include service if boiler cover selected
      // Customer data structure for new template
      customer: {
        name: `${sale.customerFirstName} ${sale.customerLastName}`,
        email: sale.email,
        phone: sale.phoneNumber,
        address: `${sale.mailingStreet}, ${sale.mailingCity}, ${sale.mailingProvince}, ${sale.mailingPostalCode}`
      },
      coverage: {
        startDate: new Date().toLocaleDateString('en-GB')
      },
      agreement: {
        referenceNumber: `TFT${String(Math.floor(Math.random() * 10000)).padStart(4, '0')}`,
        coverage: {
          hasBoilerCover: sale.boilerCoverSelected,
          boilerPriceFormatted: sale.boilerPriceSelected ? `£${sale.boilerPriceSelected.toFixed(2)}/month` : null
        }
      },
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
      metadata: {
        agentName: sale.agentName || sale.createdBy?.email || 'Flash Team Support'
      }
    };

    // Generate Flash Team PDF directly
    console.log('� Generating Flash Team PDF...');
    
    // Prepare data for Flash Team template
    const flashTeamData = {
      customerName: `${sale.customerFirstName} ${sale.customerLastName}`,
      email: sale.email,
      phone: sale.phoneNumber,
      address: `${sale.mailingStreet}, ${sale.mailingCity}, ${sale.mailingProvince}, ${sale.mailingPostalCode}`,
      coverageStartDate: new Date().toLocaleDateString('en-GB'),
      policyNumber: `TFT${String(Math.floor(Math.random() * 10000)).padStart(4, '0')}`, 
      monthlyCost: sale.totalPlanCost?.toFixed(2) || "0.00",
      hasApplianceCover: sale.applianceCoverSelected,
      hasBoilerCover: sale.boilerCoverSelected,
    };

    console.log('📄 Flash Team data prepared:', flashTeamData);
    
    // Generate PDF using appropriate template service
    console.log('📄 Generating PDF with template type:', validatedData.templateType);
    
    const pdfBuffer = await generatePDF(validatedData.templateType, flashTeamData);
    console.log('✅ PDF generated, size:', pdfBuffer.length, 'bytes');

      // Generate filename 
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const templateName = validatedData.templateType === 'wiseguys-tech-plan' ? 'Wiseguys Remote Support Tech Plan' : 'Flash Team Protection Plan';
      const fileName = `${validatedData.templateType}-${sale.customerFirstName}-${sale.customerLastName}-${timestamp}.pdf`;
      
      // Use appropriate template ID
      const templateId = validatedData.templateType === 'wiseguys-tech-plan' ? 'wiseguys-tech-plan' : 'flash-team-default';
      
      // Store PDF document in database
      console.log(`📄 Storing ${templateName} PDF in database`);

      const generatedDocument = await prisma.generatedDocument.create({
        data: {
          saleId: sale.id,
          templateId: templateId,
          filename: fileName,
          filePath: `virtual://generated-documents/${fileName}`,
          fileSize: pdfBuffer.length,
          mimeType: 'application/pdf',
          metadata: {
            templateType: validatedData.templateType,
            customerName: flashTeamData.customerName,
            generationMethod: validatedData.templateType === 'wiseguys-tech-plan' ? 'wiseguys-pdf-generator' : 'flash-team-pdf-generator',
            // Store the actual PDF content in metadata
            documentContent: pdfBuffer.toString('base64')
          }
        }
      });

      console.log('📝 Successfully created GeneratedDocument:', generatedDocument.id);

      // Mark the sale as having documents generated
      await prisma.sale.update({
        where: { id: sale.id },
        data: {
          documentsGenerated: true,
          documentsGeneratedAt: new Date(),
          documentsGeneratedBy: session.user.id
        }
      });

      console.log('✅ Sale marked as having documents generated:', sale.id);

      console.log('🎯 FINAL RESULT: Generated PDF file:', fileName);
      console.log('🎯 Template name:', templateName);
      console.log('🎯 File type: application/pdf');
      console.log('🎯 Template type:', validatedData.templateType);

      return NextResponse.json({
        success: true,
        document: {
          id: generatedDocument.id,
          content: `${templateName} PDF generated successfully (${pdfBuffer.length} bytes)`,
          fileName: fileName,
          templateName: templateName,
          saleId: sale.id,
          customerName: flashTeamData.customerName,
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