import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import JSZip from 'jszip';

export async function POST(request: NextRequest) {
  console.log('🔄 Starting bulk download request...');
  
  try {
    // Authentication
    console.log('🔐 Checking authentication...');
    const session = await getServerSession(authOptions);
    if (!session?.user) {
      console.log('❌ No session found');
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

    console.log('📄 Parsing request body...');
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
    console.log('🔍 Fetching documents from database...');
    
    try {
      if (downloadAll) {
        console.log('📦 Fetching all documents with where clause:', JSON.stringify(whereClause, null, 2));
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
        console.log('📦 Fetching specific documents with IDs:', documentIds);
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
      
      console.log('✅ Database query successful, found documents:', documents.length);
    } catch (dbError) {
      console.error('❌ Database query failed:', dbError);
      return NextResponse.json({ 
        error: 'Database query failed', 
        details: dbError instanceof Error ? dbError.message : 'Unknown database error'
      }, { status: 500 });
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
        console.log(`🔄 Processing document for ${doc.sale.customerFirstName} ${doc.sale.customerLastName}`);
        
        // Get the sale data for this document
        const sale = await prisma.sale.findUnique({
          where: { id: doc.saleId }
        });
        
        if (!sale) {
          console.error(`❌ Sale not found for document ${doc.filename} (sale ID: ${doc.saleId})`);
          skippedFiles++;
          continue;
        }

        // Generate fresh HTML content for this customer using the enhanced template service
        const { EnhancedTemplateService } = await import('@/lib/paperwork/enhanced-template-service');
        const templateService = new EnhancedTemplateService();
        
        // Prepare the data for template generation
        const templateData = {
          customerName: `${sale.customerFirstName} ${sale.customerLastName}`,
          email: sale.email,
          phone: sale.phoneNumber || 'N/A',
          address: `${sale.mailingStreet || ''}${sale.mailingCity ? `, ${sale.mailingCity}` : ''}${sale.mailingProvince ? `, ${sale.mailingProvince}` : ''}${sale.mailingPostalCode ? ` ${sale.mailingPostalCode}` : ''}`.trim() || 'N/A',
          monthlyCost: sale.totalPlanCost?.toString() || '0',
          totalCost: sale.totalPlanCost?.toString() || '0',
          policyNumber: `TFT${String(Math.floor(Math.random() * 10000)).padStart(4, '0')}`, 
          coverageStartDate: sale.createdAt ? new Date(sale.createdAt).toLocaleDateString() : new Date().toLocaleDateString(),
          currentDate: new Date().toLocaleDateString(),
          applianceCover: sale.applianceCoverSelected ? 'Yes' : 'No',
          boilerCover: sale.boilerCoverSelected ? 'Yes' : 'No'
        };
        
        // Generate the document content using enhanced template service
        const documentHtml = await templateService.generateDocument('welcome-letter', templateData);
        console.log(`✅ Generated fresh content for ${sale.customerFirstName} ${sale.customerLastName}`);

        // Extract body content from the generated HTML (remove html wrapper but keep styles)
        let bodyContent = documentHtml;
        
        // Remove DOCTYPE and outer HTML wrapper, but keep everything else including styles
        bodyContent = bodyContent
          .replace(/<!DOCTYPE[^>]*>/gi, '')
          .replace(/<html[^>]*>/gi, '')
          .replace(/<\/html>/gi, '')
          .trim();
        
        // Extract the head content (including styles) and body content separately
        const headMatch = bodyContent.match(/<head[^>]*>([\s\S]*?)<\/head>/i);
        const bodyMatch = bodyContent.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
        
        let headContent = headMatch ? headMatch[1] : '';
        let finalBodyContent = bodyMatch ? bodyMatch[1] : bodyContent;
        
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

        // Create a single page for this customer
        combinedHtml += `
    <div class="customer-page">
        ${documentStyles ? `<style>${documentStyles}</style>` : ''}
        ${finalBodyContent}
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
        console.error(`❌ Error processing document ${doc.filename}:`, error);
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
    
    console.log(`✅ Combined document ready: ${pdfFileName} (${Math.round(combinedHtml.length/1024)}KB)`);

    // Return HTML for client-side PDF generation
    return new NextResponse(combinedHtml, {
      status: 200,
      headers: {
        'Content-Type': 'text/html',
        'Content-Disposition': `inline; filename="${pdfFileName.replace('.pdf', '.html')}"`,
        'X-PDF-Filename': pdfFileName,
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