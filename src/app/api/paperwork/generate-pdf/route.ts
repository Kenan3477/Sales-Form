import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth/next';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import { PDFService } from '@/lib/paperwork/pdf-service';
import { EnhancedTemplateService } from '@/lib/paperwork/enhanced-template-service';

export async function POST(req: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    
    if (!session || session.user.role !== 'ADMIN') {
      return NextResponse.json(
        { error: 'Unauthorized' }, 
        { status: 401 }
      );
    }

    const { saleId, templateType, templateId } = await req.json();

    if (!saleId || !templateType) {
      return NextResponse.json(
        { error: 'Missing required fields: saleId and templateType' },
        { status: 400 }
      );
    }

    console.log(`🎯 Direct PDF generation request:`, { saleId, templateType, templateId });

    // Get sale data
    const sale = await prisma.sale.findUnique({
      where: { id: saleId },
      include: {
        appliances: true,
        createdBy: true,
      },
    });

    if (!sale) {
      return NextResponse.json(
        { error: 'Sale not found' },
        { status: 404 }
      );
    }

    // Get template
    let template;
    if (templateId) {
      template = await prisma.documentTemplate.findUnique({
        where: { id: templateId },
      });
    } else {
      template = await prisma.documentTemplate.findFirst({
        where: { 
          templateType,
          isActive: true,
        },
        orderBy: { version: 'desc' },
      });
    }

    if (!template) {
      return NextResponse.json(
        { error: 'Template not found' },
        { status: 404 }
      );
    }

    console.log(`📄 Using template: ${template.name} (v${template.version})`);

    // Use enhanced template service for rendering
    const enhancedTemplateService = new EnhancedTemplateService();
    
    // Generate document using the enhanced template service
    const htmlContent = await enhancedTemplateService.generateDocument('welcome-letter', {
      sale,
      customerName: `${sale.customerFirstName} ${sale.customerLastName}`.trim(),
      totalCost: sale.totalPlanCost,
      monthlyPayment: sale.totalPlanCost,
      coverageStartDate: sale.directDebitDate,
      policyNumber: sale.id.toUpperCase(),
      email: sale.email,
      phone: sale.phoneNumber,
      address: [sale.mailingStreet, sale.mailingCity, sale.mailingProvince, sale.mailingPostalCode]
        .filter(Boolean)
        .join(', '),
    });
    
    // Add template-perfect styling
    const styledHtmlContent = `
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>${template.name}</title>
        <style>
          /* Perfect template matching styles */
          * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
          }
          
          @page {
            size: A4;
            margin: 20mm;
          }
          
          body {
            font-family: Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.4;
            color: #333;
            background: white;
          }
          
          /* Flash Team Header */
          .header {
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #f59e0b 100%);
            color: white;
            padding: 20pt;
            text-align: center;
            margin-bottom: 20pt;
            border-radius: 8pt;
          }
          
          .header h1 {
            font-size: 24pt;
            font-weight: bold;
            margin-bottom: 8pt;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
          }
          
          .header .tagline {
            font-size: 12pt;
            opacity: 0.9;
          }
          
          /* Document title */
          .document-title {
            font-size: 20pt;
            font-weight: bold;
            color: #1e40af;
            text-align: center;
            margin: 20pt 0;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 10pt;
          }
          
          /* Status banner */
          .status-banner {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: white;
            padding: 12pt;
            text-align: center;
            font-weight: bold;
            font-size: 14pt;
            margin: 20pt 0;
            border-radius: 6pt;
          }
          
          .status-subtitle {
            background: #1e40af;
            color: white;
            padding: 8pt;
            text-align: center;
            font-size: 11pt;
            margin-bottom: 20pt;
          }
          
          /* Two column layout */
          .two-column {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20pt;
            margin: 20pt 0;
          }
          
          .column-header {
            background: #1e40af;
            color: white;
            padding: 10pt;
            font-weight: bold;
            font-size: 12pt;
          }
          
          .column-content {
            background: #f8fafc;
            padding: 12pt;
            border: 1px solid #e5e7eb;
            border-top: none;
            min-height: 150pt;
          }
          
          /* Section styling */
          .section {
            margin: 20pt 0;
          }
          
          .section-header {
            background: #1e40af;
            color: white;
            padding: 10pt;
            font-weight: bold;
            font-size: 12pt;
          }
          
          .section-content {
            background: #f8fafc;
            padding: 12pt;
            border: 1px solid #e5e7eb;
            border-top: none;
          }
          
          /* Lists */
          ul {
            list-style: none;
            padding: 0;
          }
          
          li {
            position: relative;
            padding-left: 20pt;
            margin-bottom: 6pt;
            font-size: 10pt;
          }
          
          li::before {
            content: "✓";
            position: absolute;
            left: 0;
            color: #22c55e;
            font-weight: bold;
          }
          
          /* Footer */
          .footer {
            background: linear-gradient(135deg, #1e40af 0%, #f59e0b 100%);
            color: white;
            padding: 15pt;
            text-align: center;
            margin-top: 30pt;
            border-radius: 6pt;
          }
          
          .footer strong {
            color: white;
          }
          
          /* Ensure colors print */
          @media print {
            body { 
              print-color-adjust: exact !important;
              -webkit-print-color-adjust: exact !important;
            }
          }
        </style>
      </head>
      <body>
        ${htmlContent}
      </body>
      </html>
    `;

    console.log(`🎨 Template styled for direct PDF generation`);

    // Generate PDF directly
    const pdfBuffer = await PDFService.generatePDFBuffer(styledHtmlContent, {
      format: 'A4',
      printBackground: true,
      margin: {
        top: '0mm',
        right: '0mm',
        bottom: '0mm',
        left: '0mm',
      },
    });

    console.log(`✅ Direct PDF generated successfully (${pdfBuffer.length} bytes)`);

    // Convert buffer to Uint8Array for Response
    const uint8Buffer = new Uint8Array(pdfBuffer);

    // Return PDF as response
    return new Response(uint8Buffer, {
      status: 200,
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': `attachment; filename="${templateType}-${saleId}.pdf"`,
        'Content-Length': pdfBuffer.length.toString(),
      },
    });

  } catch (error) {
    console.error('❌ Direct PDF generation failed:', error);
    
    return NextResponse.json(
      { 
        error: 'PDF generation failed',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}