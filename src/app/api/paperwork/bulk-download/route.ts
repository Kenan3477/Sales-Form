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

    // Create combined HTML file instead of ZIP
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
            margin: 1cm;
        }
        
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }
        
        .page-break {
            page-break-before: always;
        }
        
        .customer-document {
            width: 100%;
            min-height: 90vh;
            position: relative;
            padding-bottom: 2cm;
        }
        
        .customer-header {
            background-color: #f8f9fa;
            padding: 15px;
            border: 2px solid #dee2e6;
            margin-bottom: 30px;
            border-radius: 8px;
            text-align: center;
        }
        
        .customer-name {
            font-size: 20px;
            font-weight: bold;
            color: #333;
            margin-bottom: 8px;
        }
        
        .customer-info {
            font-size: 14px;
            color: #666;
        }
        
        .document-content {
            /* Preserve the original document styling */
            width: 100%;
            overflow: visible;
        }
        
        /* Ensure embedded styles in documents work properly */
        .document-content table {
            border-collapse: collapse;
            width: 100%;
        }
        
        .document-content th,
        .document-content td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        
        .document-content th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        
        /* Print styles */
        @media print {
            .customer-header {
                background-color: #f8f9fa !important;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
                border: 2px solid #dee2e6 !important;
            }
            
            .customer-document {
                min-height: 90vh;
                padding-bottom: 2cm;
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

        // Add page break for all documents except the first one
        const pageBreakClass = processedCount > 0 ? 'customer-document page-break' : 'customer-document';
        
        // Create customer section with embedded styles for this document
        combinedHtml += `
    <div class="${pageBreakClass}">
        ${documentStyles ? `<style>${documentStyles.replace(/<\/?style[^>]*>/gi, '')}</style>` : ''}
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