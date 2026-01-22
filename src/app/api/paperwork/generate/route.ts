import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { checkApiRateLimit } from '@/lib/rateLimit';
import { z } from 'zod';
import chromium from '@sparticuz/chromium';
import puppeteer from 'puppeteer';

// Request validation schema
const generateDocumentSchema = z.object({
  saleId: z.string().min(1),
  templateType: z.enum(['welcome_letter', 'service_agreement', 'direct_debit_form', 'coverage_summary']),
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

// Generate Flash Team PDF directly using minimal template approach
async function generateFlashTeamPDF(data: any): Promise<Buffer> {
  const { chromium } = await import('playwright');
  
  // Minimal HTML template for PDF generation - one page only
  const minimalHtml = `<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page { size: A4; margin: 10mm; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: Arial, sans-serif; font-size: 12px; line-height: 1.4; color: #333; }
  .header { background: #0b2a4a; color: white; padding: 20px; margin-bottom: 20px; text-align: center; }
  .logo { font-size: 24px; font-weight: bold; margin-bottom: 5px; }
  .tagline { font-size: 12px; opacity: 0.9; }
  .title { font-size: 20px; color: #0b2a4a; margin-bottom: 15px; font-weight: bold; }
  .section { margin-bottom: 20px; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .card { border: 1px solid #ddd; border-radius: 5px; overflow: hidden; }
  .card-header { background: #0b2a4a; color: white; padding: 10px; font-weight: bold; }
  .card-body { padding: 15px; }
  .row { display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid #eee; }
  .row:last-child { border-bottom: none; }
  .label { font-weight: bold; }
  .value { color: #666; }
  .active-box { background: #ff6b35; color: white; padding: 15px; text-align: center; margin: 20px 0; border-radius: 5px; font-weight: bold; }
  .benefits { list-style: none; }
  .benefits li { padding: 5px 0; }
  .benefits li:before { content: "✓"; color: #ff6b35; font-weight: bold; margin-right: 10px; }
  .steps { list-style: decimal; padding-left: 20px; }
  .steps li { padding: 5px 0; }
  .important { background: #f9f9f9; padding: 15px; border-radius: 5px; margin-top: 20px; }
  .footer { background: #0b2a4a; color: white; padding: 10px; text-align: center; margin-top: 20px; }
</style>
</head>
<body>
  <div class="header">
    <div class="logo">⚡ Flash Team</div>
    <div class="tagline">Fast, Friendly Repairs You Can Trust</div>
  </div>
  
  <div class="title">The Flash Team's Protection Plan</div>
  
  <div class="section">
    <p>Dear <strong>${data.customerName || '[Customer Name]'}</strong>,</p>
    <p>Thank you for choosing Flash Team. This document confirms your <strong>Protection Plan</strong> is now active, subject to the plan terms, conditions and exclusions.</p>
  </div>

  <div class="active-box">
    ⚡ Your Protection Plan is now active
  </div>

  <div class="grid">
    <div class="card">
      <div class="card-header">Your Account Details</div>
      <div class="card-body">
        <div class="row"><span class="label">Customer:</span><span class="value">${data.customerName || '[Name]'}</span></div>
        <div class="row"><span class="label">Email:</span><span class="value">${data.email || '[Email]'}</span></div>
        <div class="row"><span class="label">Phone:</span><span class="value">${data.phone || '[Phone]'}</span></div>
        <div class="row"><span class="label">Address:</span><span class="value">${data.address || '[Address]'}</span></div>
        <div class="row"><span class="label">Start Date:</span><span class="value">${data.coverageStartDate || '[Date]'}</span></div>
        <div class="row"><span class="label">Policy Ref:</span><span class="value">${data.policyNumber || '[Policy]'}</span></div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">What Your Plan Provides</div>
      <div class="card-body">
        ${data.monthlyCost ? `<p><strong>Monthly Payment:</strong> £${data.monthlyCost}</p>` : ''}
        <ul class="benefits">
          ${data.hasApplianceCover ? '<li>Access to qualified engineers for appliance breakdowns</li>' : ''}
          ${data.hasBoilerCover ? '<li>Access to qualified engineers for boiler and heating breakdowns</li>' : ''}
          <li>Repairs to covered appliances or systems, where repair is possible</li>
          <li>Fixed pricing with no call-out charge for covered faults</li>
          <li>Appointments offered subject to engineer availability</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="section">
    <h3>How to Request Assistance</h3>
    <ol class="steps">
      <li>Call <strong>0330 822 7695</strong></li>
      <li>Quote your policy reference <strong>${data.policyNumber || '[Policy Ref]'}</strong></li>
      <li>Describe the issue so we can assess eligibility</li>
      <li>Book an appointment subject to availability</li>
    </ol>
  </div>

  <div class="important">
    <h3>Important Information</h3>
    <ul>
      <li>This Protection Plan is a <strong>service agreement</strong> and is not an insurance policy.</li>
      <li>All services are provided subject to <strong>plan terms, conditions and exclusions</strong>.</li>
      <li>Annual boiler service: Please contact us to book your annual boiler service.</li>
    </ul>
  </div>

  <div class="footer">
    Flash Team • Nationwide UK • 0330 822 7695 • theflashteam.co.uk
  </div>
</body>
</html>`;

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
    await page.setContent(minimalHtml, { waitUntil: "networkidle0" });
    await page.emulateMediaType("print");
    
    const pdfBuffer = await page.pdf({
      format: "A4",
      printBackground: true,
      margin: { top: "10mm", right: "10mm", bottom: "10mm", left: "10mm" },
      preferCSSPageSize: true
    });
    
    return Buffer.from(pdfBuffer);
  } finally {
    await browser.close();
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
    
    // Generate PDF directly using one-page template
    console.log('📄 Generating Flash Team PDF directly...');
    
    const pdfBuffer = await generateFlashTeamPDF(flashTeamData);
    console.log('✅ Flash Team PDF generated, size:', pdfBuffer.length, 'bytes');

      // Generate filename 
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const fileName = `flash-team-protection-plan-${sale.customerFirstName}-${sale.customerLastName}-${timestamp}.pdf`;
      
      // Create a basic template record for compatibility
      const templateName = 'Flash Team Protection Plan';
      const templateId = 'flash-team-default';
      
      // Store PDF document in database
      console.log(`� Storing Flash Team PDF in database (serverless environment)`);

      const generatedDocument = await prisma.generatedDocument.create({
        data: {
          saleId: sale.id,
          templateId: templateId, // Use default template ID for Flash Team
          filename: fileName,
          filePath: `virtual://generated-documents/${fileName}`,
          fileSize: pdfBuffer.length,
          mimeType: 'application/pdf',
          metadata: {
            templateType: validatedData.templateType,
            customerName: flashTeamData.customerName,
            generationMethod: 'flash-team-pdf-generator',
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

      return NextResponse.json({
        success: true,
        document: {
          id: generatedDocument.id,
          content: `Flash Team PDF generated successfully (${pdfBuffer.length} bytes)`,
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