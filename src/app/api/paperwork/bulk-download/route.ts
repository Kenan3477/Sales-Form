import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import chromium from '@sparticuz/chromium';
import puppeteer from 'puppeteer';

export async function POST(request: NextRequest) {
  try {
    // Authentication
    const session = await getServerSession(authOptions);
    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    console.log('📥 Bulk download request started:', { 
      userId: session.user.id, 
      userRole: session.user.role
    });
    
    if (session.user.role !== 'ADMIN' && session.user.role !== 'AGENT') {
      console.log('❌ Unauthorized bulk download attempt:', { 
        userId: session.user.id, 
        userRole: session.user.role,
        expectedRoles: ['ADMIN', 'AGENT']
      });
      return NextResponse.json({ error: 'Unauthorized' }, { status: 403 });
    }

    const body = await request.json();
    const { documentIds, downloadAll = false, filter } = body;
    
    console.log('📥 Bulk download parameters:', { documentIds: documentIds?.length, downloadAll, filter });

    let whereClause: any = {
      isDeleted: false
    };

    // If agent user, only allow access to their own sales' documents
    if (session.user.role === 'AGENT') {
      whereClause.sale = {
        createdById: session.user.id
      };
    }

    // Apply filters
    if (filter === 'downloaded') {
      whereClause.downloadCount = { gt: 0 };
    } else if (filter === 'undownloaded') {
      whereClause.downloadCount = 0;
    }

    // Get documents
    let documents;
    if (downloadAll) {
      documents = await prisma.generatedDocument.findMany({
        where: whereClause,
        include: {
          sale: {
            select: {
              customerFirstName: true,
              customerLastName: true,
              email: true
            }
          },
          template: {
            select: {
              name: true,
              templateType: true
            }
          }
        },
        orderBy: {
          generatedAt: 'desc'
        }
      });
    } else {
      documents = await prisma.generatedDocument.findMany({
        where: {
          ...whereClause,
          id: { in: documentIds }
        },
        include: {
          sale: {
            select: {
              customerFirstName: true,
              customerLastName: true,
              email: true
            }
          },
          template: {
            select: {
              name: true,
              templateType: true
            }
          }
        },
        orderBy: {
          generatedAt: 'desc'
        }
      });
    }

    console.log('📥 Found documents for bulk download:', documents.length);

    if (documents.length === 0) {
      console.log('❌ No documents found for bulk download');
      return NextResponse.json({ error: 'No documents found' }, { status: 404 });
    }

    // Group documents by customer (saleId) and select the most recent one per customer
    console.log('📋 Grouping documents by customer...');
    const customerDocuments = new Map<string, typeof documents[0]>();
    
    for (const doc of documents) {
      const customerKey = doc.saleId;
      const existing = customerDocuments.get(customerKey);
      
      // If no existing document for this customer, or this document is newer, use it
      if (!existing || new Date(doc.generatedAt) > new Date(existing.generatedAt)) {
        customerDocuments.set(customerKey, doc);
        console.log(`📄 Selected document for ${doc.sale.customerFirstName} ${doc.sale.customerLastName}: ${doc.filename} (${new Date(doc.generatedAt).toLocaleDateString()})`);
      } else {
        console.log(`� Skipping older document for ${doc.sale.customerFirstName} ${doc.sale.customerLastName}: ${doc.filename}`);
      }
    }

    console.log(`📊 Processing ${customerDocuments.size} unique customers from ${documents.length} total documents`);

    // Create combined HTML file with single-page layout per customer
    console.log('📄 Creating combined single-page PDF document...');
    let skippedFiles = 0;
    let combinedHtml = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Documents - ${new Date().toLocaleDateString()}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.3;
            color: #2d3748;
            background: white;
            margin: 0;
            padding: 0;
        }
        
        .customer-page {
            page-break-before: always;
            page-break-after: always;
            page-break-inside: avoid;
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .customer-page:first-child {
            page-break-before: auto;
        }
        
        @page {
            margin: 15mm 10mm;
            size: A4;
        }
        
        @media print {
            * {
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }
            
            body {
                background: white;
                padding: 0;
                margin: 0;
            }
            
            .customer-page {
                width: 100%;
                height: 100vh;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                page-break-inside: avoid;
            }
        }
    </style>
</head>
<body>`;

    let processedCount = 0;

    for (const doc of Array.from(customerDocuments.values())) {
      try {
        // Get document content from metadata
        let fileContent: string | undefined;
        
        if (doc.metadata && typeof doc.metadata === 'object' && 'documentContent' in doc.metadata) {
          fileContent = doc.metadata.documentContent as string;
        }
        
        if (!fileContent || typeof fileContent !== 'string') {
          console.error(`❌ Document content not found for ${doc.filename}. Document may have been generated before serverless migration.`);
          skippedFiles++;
          continue;
        }

        // The document content should be our enhanced template - extract it properly
        let documentHtml = fileContent;
        
        // For our enhanced template, we want the complete document content as-is
        // Remove only the outer html/head tags but preserve all styles and structure
        let cleanDocumentContent = documentHtml;
        
        // Remove DOCTYPE and outer HTML wrapper, but keep everything else including styles
        cleanDocumentContent = cleanDocumentContent
          .replace(/<!DOCTYPE[^>]*>/gi, '')
          .replace(/<html[^>]*>/gi, '')
          .replace(/<\/html>/gi, '')
          .trim();
        
        // Extract the head content (including styles) and body content separately
        const headMatch = cleanDocumentContent.match(/<head[^>]*>([\s\S]*?)<\/head>/i);
        const bodyMatch = cleanDocumentContent.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
        
        let headContent = headMatch ? headMatch[1] : '';
        let bodyContent = bodyMatch ? bodyMatch[1] : cleanDocumentContent;
        
        // If we have head content, extract just the styles
        let documentStyles = '';
        if (headContent) {
          const styleMatches = headContent.match(/<style[^>]*>([\s\S]*?)<\/style>/gi);
          if (styleMatches) {
            documentStyles = styleMatches.map(style => 
              style.replace(/<\/?style[^>]*>/gi, '')
            ).join('\n');
          }
        }

        // Create a single page for this customer using our enhanced template format
        combinedHtml += `
    <div class="customer-page">
        ${documentStyles ? `<style>${documentStyles}</style>` : ''}
        ${bodyContent}
    </div>
`;

        // Update download count
        await prisma.generatedDocument.update({
          where: { id: doc.id },
          data: { 
            downloadCount: { increment: 1 },
            lastDownloadAt: new Date()
          }
        });
        
        processedCount++;
        console.log(`✅ Added customer ${processedCount}: ${doc.sale.customerFirstName} ${doc.sale.customerLastName}`);
      } catch (error) {
        console.error(`❌ Error processing file ${doc.filename}:`, error);
        skippedFiles++;
        // Continue with other files
      }
    }

    // Close the HTML
    combinedHtml += `
</body>
</html>`;

    console.log(`� Combined HTML document created: ${processedCount} customers processed, ${skippedFiles} documents skipped`);

    if (processedCount === 0) {
      console.error('❌ No documents could be processed');
      return NextResponse.json({ 
        error: 'No documents could be processed. Documents may have been generated before the serverless migration or no valid documents found.' 
      }, { status: 500 });
    }

    // Generate filename
    const timestamp = new Date().toISOString().slice(0, 16).replace(/[:-]/g, '');
    const pdfFileName = `flash_team_protection_plans_${processedCount}_customers_${timestamp}.pdf`;
    
    console.log(`✅ Combined document ready, generating PDF: ${pdfFileName} (${Math.round(combinedHtml.length/1024)}KB)`);

    // Generate PDF using puppeteer with @sparticuz/chromium for serverless
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
    
    // Configure for serverless environment
    if (process.env.VERCEL || process.env.NODE_ENV === 'production') {
      executablePath = await chromium.executablePath();
      args = chromium.args.concat(args);
    }
    
    const browser = await puppeteer.launch({
      headless: true,
      executablePath,
      args,
    });
    
    const page = await browser.newPage();
    await page.setContent(combinedHtml, { waitUntil: 'networkidle0' });
    
    const pdfBuffer = await page.pdf({
      format: 'A4',
      printBackground: true,
      preferCSSPageSize: true,
      margin: {
        top: '10mm',
        right: '10mm', 
        bottom: '10mm',
        left: '10mm'
      },
      scale: 1
    });
    
    await browser.close();

    return new NextResponse(Buffer.from(pdfBuffer), {
      status: 200,
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': `attachment; filename="${pdfFileName}"`,
        'Content-Length': pdfBuffer.length.toString(),
      },
    });

  } catch (error) {
    console.error('❌ Bulk download error:', error);
    return NextResponse.json({ 
      error: 'Failed to create document archive',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}