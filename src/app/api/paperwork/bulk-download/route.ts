import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';

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

    // Create combined HTML file with proper print layout
    console.log('📄 Creating combined HTML document...');
    let skippedFiles = 0;
    let combinedHtml = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Documents - ${new Date().toLocaleDateString()}</title>
    <style>
        @page {
            size: A4;
            margin: 0;
        }
        
        * {
            box-sizing: border-box;
        }
        
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: white;
        }
        
        .customer-page {
            page-break-after: always;
            page-break-inside: avoid;
            width: 100vw;
            min-height: 100vh;
            padding: 1cm;
            display: flex;
            flex-direction: column;
        }
        
        .customer-page:last-child {
            page-break-after: auto;
        }
        
        .customer-header {
            background-color: #f8f9fa;
            padding: 10px;
            border: 1px solid #dee2e6;
            margin-bottom: 15px;
            border-radius: 4px;
            text-align: center;
            flex-shrink: 0;
        }
        
        .customer-name {
            font-size: 16px;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        
        .customer-info {
            font-size: 12px;
            color: #666;
        }
        
        .document-content {
            flex: 1;
            width: 100%;
            overflow: hidden;
        }
        
        /* Reset any conflicting styles from embedded documents */
        .document-content * {
            max-width: 100% !important;
        }
        
        .document-content img {
            max-width: 100% !important;
            height: auto !important;
        }
        
        /* Print-specific styles */
        @media print {
            body {
                margin: 0 !important;
                padding: 0 !important;
            }
            
            .customer-page {
                width: 100% !important;
                height: 100vh !important;
                margin: 0 !important;
                padding: 1cm !important;
            }
            
            .customer-header {
                background-color: #f8f9fa !important;
                border: 1px solid #dee2e6 !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
        }
        
        /* Hide screen-only elements */
        @media print {
            .no-print {
                display: none !important;
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

        // The document content is a complete HTML document - we need to extract the styled content properly
        let documentHtml = fileContent;
        let documentStyles = '';
        let documentBody = '';
        
        // Extract styles from the head section
        const styleMatch = documentHtml.match(/<style[^>]*>([\s\S]*?)<\/style>/gi);
        if (styleMatch) {
          documentStyles = styleMatch.join('\n');
        }
        
        // Extract content from body, but if no body tags exist, use everything after head
        const bodyMatch = documentHtml.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
        if (bodyMatch) {
          documentBody = bodyMatch[1].trim();
        } else {
          // Fallback: remove head and html wrapper tags but keep all content
          documentBody = documentHtml
            .replace(/<!DOCTYPE[^>]*>/gi, '')
            .replace(/<html[^>]*>/gi, '')
            .replace(/<\/html>/gi, '')
            .replace(/<head[^>]*>[\s\S]*?<\/head>/gi, '')
            .trim();
        }

        // Create customer page with proper structure for printing
        combinedHtml += `
    <div class="customer-page">
        ${documentStyles ? `<style scoped>${documentStyles.replace(/<\/?style[^>]*>/gi, '')}</style>` : ''}
        <div class="customer-header">
            <div class="customer-name">${doc.sale.customerFirstName} ${doc.sale.customerLastName}</div>
            <div class="customer-info">
                Email: ${doc.sale.email} | 
                Document: ${doc.template.name || 'Welcome Letter'} | 
                Generated: ${new Date(doc.generatedAt).toLocaleDateString()}
            </div>
        </div>
        <div class="document-content">
            ${documentBody}
        </div>
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
    const htmlFileName = `all_customer_documents_${processedCount}_customers_${timestamp}.html`;
    
    console.log(`✅ Combined HTML document ready: ${htmlFileName} (${Math.round(combinedHtml.length/1024)}KB)`);

    return new NextResponse(combinedHtml, {
      status: 200,
      headers: {
        'Content-Type': 'text/html',
        'Content-Disposition': `attachment; filename="${htmlFileName}"`,
        'Content-Length': Buffer.byteLength(combinedHtml, 'utf8').toString(),
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