import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import { isAdminRole } from '@/lib/apiSecurity';
import fs from 'fs/promises';
import path from 'path';
import chromium from '@sparticuz/chromium';
import puppeteer from 'puppeteer';

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    
    if (!session || !isAdminRole(session.user.role)) {
      return NextResponse.json(
        { error: 'Unauthorized - Admin access required' },
        { status: 401 }
      );
    }

    const { documentId, saleId, templateId } = await request.json();

    // Validate required fields
    if (!documentId || !saleId || !templateId) {
      return NextResponse.json(
        { error: 'Missing required fields: documentId, saleId, and templateId are required' },
        { status: 400 }
      );
    }

    // Find the existing document
    const existingDocument = await prisma.generatedDocument.findUnique({
      where: { id: documentId },
      include: {
        sale: {
          include: {
            createdBy: true
          }
        },
        template: true
      }
    });

    if (!existingDocument) {
      return NextResponse.json(
        { error: 'Document not found' },
        { status: 404 }
      );
    }

    // Get the template and sale data
    const template = await prisma.documentTemplate.findUnique({
      where: { id: templateId }
    });

    if (!template) {
      return NextResponse.json(
        { error: 'Template not found' },
        { status: 404 }
      );
    }

    const sale = existingDocument.sale;

    // Generate PDF using Flash Team template
    const pdfData = {
      customerName: `${sale.customerFirstName} ${sale.customerLastName}`,
      email: sale.email,
      phone: sale.phoneNumber,
      address: sale.mailingStreet || '',
      postcode: sale.mailingPostalCode || '',
      coverageStartDate: sale.createdAt.toLocaleDateString('en-GB'),
      policyNumber: `FT${sale.id.toString().padStart(6, '0')}`,
      monthlyCost: sale.totalPlanCost?.toString() || '0',
      applianceCover: sale.applianceCoverSelected ? 'Yes' : 'No',
      boilerCover: sale.boilerCoverSelected ? 'Yes' : 'No'
    };

    const pdfBytes = await generateFlashTeamPDF(pdfData);

    // Generate new filename for PDF
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `${template.name}-REGENERATED-${sale.customerFirstName}-${sale.customerLastName}-${timestamp}.pdf`;
    const relativePath = `storage/documents/${filename}`;
    const fullPath = path.join(process.cwd(), relativePath);

    // Ensure directory exists
    await fs.mkdir(path.dirname(fullPath), { recursive: true });

    // Write the PDF to file
    await fs.writeFile(fullPath, pdfBytes);

    // Delete old file if it exists
    if (existingDocument.filePath) {
      try {
        const oldFullPath = path.join(process.cwd(), existingDocument.filePath);
        await fs.unlink(oldFullPath);
      } catch (fileError) {
        console.warn('Failed to delete old file:', fileError);
      }
    }

    // Update the document in database (remove content field and include relations)
    const updatedDocument = await prisma.generatedDocument.update({
      where: { id: documentId },
      data: {
        filePath: relativePath,
        filename: filename
      },
      include: {
        template: true,
        sale: {
          include: {
            createdBy: true
          }
        }
      }
    });

    return NextResponse.json({
      success: true,
      document: updatedDocument,
      message: 'Document regenerated successfully'
    });

  } catch (error) {
    console.error('Error regenerating document:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
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
    executablePath = await chromium.executablePath();
    args = chromium.args.concat(args);
  }
  
  const browser = await puppeteer.launch({
    headless: true,
    executablePath,
    args,
  });
  
  try {
    const page = await browser.newPage();
    const htmlContent = buildFlashTeamHtml(data);
    
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