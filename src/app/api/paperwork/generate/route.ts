import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { checkApiRateLimit } from '@/lib/rateLimit';
import { z } from 'zod';
import { chromium } from 'playwright';

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

function buildFlashTeamHtml(data: any): string {
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>The Flash Team's Protection Plan</title>

<style>
  :root{
    --navy:#0b2a4a;
    --navy2:#081f36;
    --orange:#ff6b35;
    --orange2:#ff8c42;
    --ink:#1f2a3a;
    --muted:#5e6b7a;
    --line:#e4e9f1;
    --paper:#ffffff;
  }

  *{box-sizing:border-box}
  html,body{margin:0;padding:0;background:#fff;color:var(--ink);font-family:"Segoe UI",Arial,Helvetica,sans-serif}

  /* A4 canvas (screen + print) */
  .sheet{
    width: 210mm;
    min-height: 297mm;
    margin: 0 auto;
    background: var(--paper);
  }
  .wrap{
    padding: 10mm; /* keep tight for one-page */
  }

  /* Header band */
  .banner{
    position:relative;
    padding: 12mm 10mm 8mm 10mm;
    color:#fff;
    background:
      radial-gradient(900px 220px at 20% 30%, rgba(255,255,255,.10), transparent 55%),
      radial-gradient(700px 200px at 80% 35%, rgba(255,255,255,.08), transparent 55%),
      linear-gradient(135deg, var(--navy) 0%, var(--navy2) 100%);
  }
  .banner:after{
    content:"";
    position:absolute;left:0;right:0;bottom:0;height:4mm;
    background: linear-gradient(90deg, var(--orange), var(--orange2));
  }
  .brand{
    display:flex;justify-content:center;align-items:center;gap:10px;text-align:center;
  }
  .bolt{
    width: 12mm;height: 12mm;border-radius:4mm;
    background: linear-gradient(135deg, var(--orange), var(--orange2));
    display:flex;align-items:center;justify-content:center;
    font-weight:900;color:#10243c;
    box-shadow:0 3mm 7mm rgba(255,107,53,.25);
  }
  .brand h1{
    margin:0;font-size: 18mm;line-height:1;font-weight:900;letter-spacing:.2px;
  }
  .tagline{margin-top:2mm;font-size:4mm;font-weight:600;opacity:.92}

  /* Main title */
  .title{
    font-size: 9mm;
    margin: 6mm 0 2mm 0;
    color: var(--navy);
    font-weight: 900;
    letter-spacing:.2px;
  }
  .rule{height:1px;background:var(--line);margin: 2mm 0 4mm 0}

  /* Intro */
  .p{margin:0 0 2.5mm 0;font-size:3.6mm;line-height:1.35}
  .p strong{font-weight:900}

  /* Activation bar */
  .active{
    margin: 4mm 0 5mm 0;
    border-radius:3mm;
    overflow:hidden;
    border:1px solid rgba(10,20,35,.12);
  }
  .active .top{
    background: linear-gradient(135deg, var(--orange), var(--orange2));
    color:#fff;
    padding: 3mm 4mm;
    display:flex;align-items:center;justify-content:center;gap:3mm;
    font-weight:900;font-size:4.6mm;
    text-align:center;
  }
  .miniBolt{
    width:7mm;height:7mm;border-radius:2mm;
    background: rgba(0,0,0,.16);
    display:flex;align-items:center;justify-content:center;
    font-size:4mm;
  }
  .active .bottom{
    background: linear-gradient(135deg, var(--navy), var(--navy2));
    color:#eaf1ff;
    padding: 2.8mm 4mm;
    text-align:center;
    font-weight:700;
    font-size:3.3mm;
  }

  /* Cards */
  .grid{
    display:grid;
    grid-template-columns: 1fr 1fr;
    gap: 4mm;
    align-items:start;
  }
  .card{
    border:1px solid var(--line);
    border-radius:3mm;
    overflow:hidden;
    background:#fff;
  }
  .head{
    background: linear-gradient(135deg, var(--navy), var(--navy2));
    color:#fff;
    padding: 2.6mm 3.2mm;
    font-weight:900;
    font-size:4.2mm;
  }
  .body{padding:2.6mm 3.2mm}

  /* Account rows */
  .row{
    display:flex;justify-content:space-between;gap:3mm;
    padding: 1.8mm 0;
    border-bottom:1px solid var(--line);
    font-size:3.3mm;
    line-height:1.2;
  }
  .row:last-child{border-bottom:none}
  .k{font-weight:900}
  .v{font-weight:700;color:#2c3a52;text-align:right;max-width:85mm}

  /* Plan list */
  .kv{font-size:3.3mm;margin:0 0 2mm 0}
  .kv .k2{font-weight:900}
  .checks{list-style:none;margin:1mm 0 0 0;padding:0}
  .checks li{
    display:flex;gap:2.2mm;
    margin: 1.8mm 0;
    font-size:3.2mm;
    line-height:1.25;
  }
  .tick{
    width:5mm;height:5mm;border-radius:1.6mm;
    background: rgba(255,107,53,.18);
    display:flex;align-items:center;justify-content:center;
    color: var(--orange);
    font-weight:1000;
    flex: 0 0 5mm;
    font-size:3.2mm;
  }

  /* Lower row: assistance + small note */
  .lower{
    display:grid;
    grid-template-columns: 1fr 1fr;
    gap: 4mm;
    margin-top: 4mm;
    align-items:start;
  }
  .steps{margin:0;padding-left:4.6mm;font-size:3.3mm}
  .steps li{margin:1.8mm 0}
  .phone{font-weight:1000;color:var(--navy);text-decoration:none}

  /* Direct Debit (concise) */
  .dd p{margin:0 0 2mm 0;font-size:3.3mm;line-height:1.25}
  .dd ul{margin:0;padding-left:4.6mm;font-size:3.2mm}
  .dd li{margin:1.6mm 0}

  /* Important info (concise) */
  .important{
    margin-top: 4mm;
  }
  .important h2{
    margin:0 0 2mm 0;
    font-size:4.4mm;
    color: var(--navy);
    font-weight:900;
  }
  .important ul{margin:0;padding-left:4.6mm;font-size:3.2mm}
  .important li{margin:1.6mm 0}

  /* Footer band */
  .footer{
    margin-top: 4mm;
    background: linear-gradient(135deg, var(--navy), var(--navy2));
    color:#eaf1ff;
    padding: 3.2mm 4mm;
    font-weight:800;
    text-align:center;
    font-size:3.2mm;
    border-top: 3mm solid;
    border-image: linear-gradient(90deg, var(--orange), var(--orange2)) 1;
  }
  .dot{opacity:.7;padding:0 1.5mm}

  /* --- PRINT: force one-page A4, keep colours, avoid splitting --- */
  @page { size: A4; margin: 0; }
  @media print {
    html,body{background:#fff !important}
    .sheet{width:210mm;min-height:297mm;margin:0}
    .wrap{padding:10mm}
    *{
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }
    /* prevent page breaks inside key blocks */
    .banner,.active,.grid,.card,.lower,.important,.footer{break-inside:avoid;page-break-inside:avoid}
  }
</style>
</head>

<body>
  <div class="sheet">
    <div class="banner">
      <div class="brand">
        <div class="bolt">⚡</div>
        <div>
          <h1>Flash Team</h1>
          <div class="tagline">Fast, Friendly Repairs You Can Trust</div>
        </div>
      </div>
    </div>

    <div class="wrap">
      <div class="title">The Flash Team's Protection Plan</div>
      <div class="rule"></div>

      <p class="p">Dear <strong>${escapeHtml(data.customerName)}</strong>,</p>
      <p class="p">
        Thank you for choosing Flash Team. This document confirms your <strong>Protection Plan</strong> is now active,
        subject to the plan terms, conditions and exclusions.
      </p>

      <div class="active">
        <div class="top"><span class="miniBolt">⚡</span> Your Protection Plan is now active</div>
        <div class="bottom">This letter explains your cover and how to request assistance</div>
      </div>

      <div class="grid">
        <!-- LEFT: Account -->
        <div class="card">
          <div class="head">Your Account Details</div>
          <div class="body">
            <div class="row"><div class="k">Customer</div><div class="v">${escapeHtml(data.customerName)}</div></div>
            <div class="row"><div class="k">Email</div><div class="v">${escapeHtml(data.email)}</div></div>
            <div class="row"><div class="k">Phone</div><div class="v">${escapeHtml(data.phone)}</div></div>
            <div class="row"><div class="k">Address</div><div class="v">${escapeHtml(data.address)}</div></div>
            <div class="row"><div class="k">Start Date</div><div class="v">${escapeHtml(data.coverageStartDate)}</div></div>
            <div class="row"><div class="k">Policy Ref</div><div class="v">${escapeHtml(data.policyNumber)}</div></div>
          </div>
        </div>

        <!-- RIGHT: Plan provides -->
        <div class="card">
          <div class="head">What Your Plan Provides</div>
          <div class="body">
            ${data.monthlyCost ? `
              <div class="kv"><span class="k2">Monthly Payment:</span> ${money(data.monthlyCost)}</div>
            ` : ''}

            <ul class="checks">
              ${data.hasApplianceCover ? `
                <li><span class="tick">✓</span><span>Access to qualified engineers for covered appliance breakdowns</span></li>
              ` : ''}
              ${data.hasBoilerCover ? `
                <li><span class="tick">✓</span><span>Access to qualified engineers for covered boiler and central heating breakdowns</span></li>
              ` : ''}
              <li><span class="tick">✓</span><span>Repairs to covered appliances or systems, where repair is possible</span></li>
              <li><span class="tick">✓</span><span>If a repair is not economically viable, we may, at our discretion, offer a replacement of equivalent specification (new for old where applicable), subject to availability and the plan terms</span></li>
              <li><span class="tick">✓</span><span>Fixed pricing with no call-out charge for covered faults</span></li>
              <li><span class="tick">✓</span><span>Appointments offered subject to engineer availability</span></li>
            </ul>
          </div>
        </div>
      </div>

      <div class="lower">
        <!-- Requesting assistance -->
        <div class="card">
          <div class="head">Requesting Assistance</div>
          <div class="body">
            <ol class="steps">
              <li>Call <a class="phone" href="tel:03308227695">0330 822 7695</a></li>
              <li>Quote your policy reference <strong>${escapeHtml(data.policyNumber)}</strong></li>
              <li>Describe the issue so we can assess eligibility</li>
              <li>Book an appointment subject to availability</li>
            </ol>
          </div>
        </div>

        <!-- Direct debit (compact) -->
        <div class="card dd">
          <div class="head">Direct Debit Guarantee</div>
          <div class="body">
            <p>If you pay by <strong>Direct Debit</strong>, payments will appear on your bank statement as <strong>Warmcare</strong>.</p>
            <ul>
              <li>We'll notify you in advance of any changes to amount, date or frequency.</li>
              <li>If an error is made, you're entitled to a full and immediate refund from your bank.</li>
              <li>You can cancel a Direct Debit at any time via your bank or building society.</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="important">
        <h2>Important Information</h2>
        <ul>
          <li>This Protection Plan is a <strong>service agreement</strong> and is not an insurance policy.</li>
          <li>All services are provided subject to <strong>plan terms, conditions and exclusions</strong>.</li>
          <li>Annual boiler service: Please contact us to book your annual boiler service.</li>
        </ul>
      </div>

      <div class="footer">
        Flash Team <span class="dot">•</span> Nationwide UK <span class="dot">•</span> 0330 822 7695 <span class="dot">•</span> theflashteam.co.uk
      </div>
    </div>
  </div>
</body>
</html>`;
}

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
    
    // Generate HTML using Flash Team template
    const htmlContent = buildFlashTeamHtml(flashTeamData);
    console.log('✅ Flash Team HTML generated, length:', htmlContent.length);

    // Generate PDF from Flash Team HTML
    console.log('📄 Converting Flash Team HTML to PDF...');
    
    const browser = await chromium.launch({
      headless: true,
      args: ["--font-render-hinting=medium"]
    });
    
    try {
      const page = await browser.newPage();
      
      // Load HTML
      await page.setContent(htmlContent, { waitUntil: "networkidle" });
      
      // Ensure deterministic layout
      await page.emulateMedia({ media: "print" });
      
      // A4 PDF with proper margins
      const pdfBuffer = await page.pdf({
        format: "A4",
        printBackground: true,
        margin: { top: "12mm", right: "12mm", bottom: "12mm", left: "12mm" },
        preferCSSPageSize: true
      });
      
      console.log('✅ PDF generated, size:', pdfBuffer.length, 'bytes');

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
      
    } finally {
      await browser.close();
    }

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