import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { checkApiRateLimit } from '@/lib/rateLimit';
import { PDFService } from '@/lib/paperwork/pdf-service';

export async function GET(request: NextRequest) {
  return handleBulkPDFDownload(request);
}

export async function POST(request: NextRequest) {
  return handleBulkPDFDownload(request);
}

async function handleBulkPDFDownload(request: NextRequest) {
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

    // Authentication
    const session = await getServerSession(authOptions);
    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Only admin users can bulk download all customer documents
    if (session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Admin access required' }, { status: 403 });
    }

    const { prisma } = await import('@/lib/prisma');
    console.log(`📋 Starting PDF bulk download for admin: ${session.user.email}`);

    // Handle POST request with specific document IDs
    let documentIds: string[] = [];
    if (request.method === 'POST') {
      try {
        const body = await request.json();
        documentIds = body.documentIds || [];
        console.log(`📋 POST request: filtering by ${documentIds.length} specific document IDs`);
      } catch (error) {
        console.error('Failed to parse POST body:', error);
        return NextResponse.json({ error: 'Invalid request body' }, { status: 400 });
      }
    }

    // Build where clause based on whether we're filtering specific documents
    const whereClause: any = {
      isDeleted: false,
    };

    if (documentIds.length > 0) {
      whereClause.id = {
        in: documentIds
      };
    }

    // Get documents based on filter
    const documents = await prisma.generatedDocument.findMany({
      where: whereClause,
      include: {
        template: true,
        sale: true,
      },
      orderBy: [
        { sale: { customerLastName: 'asc' } },
        { sale: { customerFirstName: 'asc' } },
        { generatedAt: 'desc' },
      ],
    });

    const documentType = documentIds.length > 0 ? 'selected' : 'all';
    console.log(`📋 Found ${documents.length} ${documentType} documents to process`);

    if (documents.length === 0) {
      return NextResponse.json({ 
        error: documentIds.length > 0 ? 'No matching documents found' : 'No documents available for download' 
      }, { status: 404 });
    }

    let processedCount = 0;
    let skippedFiles = 0;

    // For single document, use original HTML directly without any modification
    if (documents.length === 1) {
      const doc = documents[0];
      
      try {
        let fileContent: string | undefined;
        
        if (doc.metadata && typeof doc.metadata === 'object' && 'documentContent' in doc.metadata) {
          fileContent = doc.metadata.documentContent as string;
        }
        
        if (!fileContent || typeof fileContent !== 'string') {
          console.error(`❌ Document content not found for ${doc.filename}`);
          return NextResponse.json({ error: 'Document content not found' }, { status: 500 });
        }

        console.log(`🔍 Single document: ${doc.filename}, using original HTML directly`);

        // Update download count
        await prisma.generatedDocument.update({
          where: { id: doc.id },
          data: { 
            downloadCount: { increment: 1 },
            lastDownloadAt: new Date()
          }
        });

        // Generate PDF directly from original HTML
        const pdfBuffer = await PDFService.generatePDFBuffer(fileContent, {
          format: 'A4',
          margin: {
            top: '1.5cm',
            right: '1.5cm',
            bottom: '1.5cm',
            left: '1.5cm',
          },
          displayHeaderFooter: false,
          printBackground: true,
          timeout: 300000,
        });

        console.log(`✅ Single PDF generated successfully! Size: ${Math.round(pdfBuffer.length/1024)}KB`);

        // Generate filename
        const timestamp = new Date().toISOString().slice(0, 16).replace(/[:-]/g, '');
        const pdfFileName = `${doc.sale.customerFirstName}_${doc.sale.customerLastName}_${timestamp}.pdf`;
        
        return new Response(new Uint8Array(pdfBuffer), {
          status: 200,
          headers: {
            'Content-Type': 'application/pdf',
            'Content-Disposition': `attachment; filename="${pdfFileName}"`,
            'Content-Length': pdfBuffer.length.toString(),
            'Cache-Control': 'no-cache',
          },
        });
      } catch (error) {
        console.error('❌ Single PDF generation failed:', error);
        return NextResponse.json({
          error: 'PDF generation failed',
          message: error instanceof Error ? error.message : 'Unknown error'
        }, { status: 500 });
      }
    }

    // For multiple documents, continue with existing logic
    let allDocumentStyles = '';
    let allDocumentContent = '';

    // Start building the master HTML document for multiple documents
    let combinedHTML = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Documents - ${new Date().toLocaleDateString()}</title>
    <style>
        @page {
            size: A4;
            margin: 1.5cm;
        }
        
        body {
            margin: 0;
            padding: 0;
            background: white;
        }
        
        .customer-document {
            page-break-after: always;
            width: 100%;
            background: white;
            box-sizing: border-box;
        }
        
        .customer-document:last-child {
            page-break-after: auto;
        }
        
        .customer-document .document-container {
            max-width: none !important;
            margin: 0 auto !important;
            background: white !important;
            box-shadow: none !important;
            border-radius: 0 !important;
            overflow: visible !important;
            page-break-inside: avoid !important;
        }
    </style>
    <!-- All document styles will be inserted here -->
</head>
<body>`;

    // Process each document and collect content with page breaks
    for (const doc of documents) {
      try {
        // Get complete document content from metadata
        let fileContent: string | undefined;
        
        if (doc.metadata && typeof doc.metadata === 'object' && 'documentContent' in doc.metadata) {
          fileContent = doc.metadata.documentContent as string;
        }
        
        if (!fileContent || typeof fileContent !== 'string') {
          console.error(`❌ Document content not found for ${doc.filename}. Document may have been generated before serverless migration.`);
          skippedFiles++;
          continue;
        }

        console.log(`🔍 Processing document: ${doc.filename}, Content length: ${fileContent.length}`);

        // Extract the document body content and styles separately
        let documentStyles = '';
        let documentBodyContent = '';
        
        // Extract styles from the original document
        const styleMatches = fileContent.match(/<style[^>]*>([\s\S]*?)<\/style>/gi) || [];
        if (styleMatches.length > 0) {
          documentStyles = styleMatches
            .map(styleBlock => styleBlock.replace(/<\/?style[^>]*>/gi, ''))
            .join('\n');
          
          // Add to collected styles if not already present
          if (documentStyles && !allDocumentStyles.includes(documentStyles)) {
            allDocumentStyles += '\n' + documentStyles;
          }
        }
        
        // Extract body content
        const bodyMatch = fileContent.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
        if (bodyMatch) {
          documentBodyContent = bodyMatch[1];
        } else {
          // Fallback: take everything after head
          documentBodyContent = fileContent
            .replace(/<!DOCTYPE[^>]*>/gi, '')
            .replace(/<html[^>]*>/gi, '')
            .replace(/<\/html>/gi, '')
            .replace(/<head[^>]*>[\s\S]*?<\/head>/gi, '')
            .replace(/<body[^>]*>/gi, '')
            .replace(/<\/body>/gi, '')
            .trim();
        }

        // Add this customer's content with proper page break wrapper
        allDocumentContent += `
    <div class="customer-document">
        ${documentBodyContent}
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
      }
    }

    // Complete the HTML document
    combinedHTML = combinedHTML.replace(
      '<!-- All document styles will be inserted here -->',
      `<style>${allDocumentStyles}</style>`
    );
    
    combinedHTML += allDocumentContent + `
</body>
</html>`;

    if (processedCount === 0) {
      console.error('❌ No documents could be processed');
      return NextResponse.json({ 
        error: 'No documents could be processed. Documents may have been generated before the serverless migration or no valid documents found.' 
      }, { status: 500 });
    }

    console.log(`📊 Processing complete: ${processedCount} documents, ${skippedFiles} skipped`);
    console.log(`📋 Starting PDF generation for combined content...`);

    console.log(`📄 Total combined HTML size: ${Math.round(combinedHTML.length/1024)}KB`);

    // Generate PDF using PDFService with optimized settings
    try {
      const pdfBuffer = await PDFService.generatePDFBuffer(combinedHTML, {
        format: 'A4',
        margin: {
          top: '1.5cm',
          right: '1.5cm',
          bottom: '1.5cm',
          left: '1.5cm',
        },
        displayHeaderFooter: false,
        printBackground: true,
        timeout: 300000, // 5 minutes for very large documents
      });

      console.log(`✅ PDF generated successfully! Size: ${Math.round(pdfBuffer.length/1024)}KB`);

      // Generate filename based on document type
      const timestamp = new Date().toISOString().slice(0, 16).replace(/[:-]/g, '');
      const filePrefix = documentIds.length > 0 ? 'selected_documents' : 'all_customer_documents';
      const countSuffix = documentIds.length > 0 ? `${documentIds.length}_documents` : `${processedCount}_customers`;
      const pdfFileName = `${filePrefix}_${countSuffix}_${timestamp}.pdf`;
      
      return new Response(new Uint8Array(pdfBuffer), {
        status: 200,
        headers: {
          'Content-Type': 'application/pdf',
          'Content-Disposition': `attachment; filename="${pdfFileName}"`,
          'Content-Length': pdfBuffer.length.toString(),
          'Cache-Control': 'no-cache',
        },
      });
    } catch (pdfError) {
      console.error('❌ PDF generation failed:', pdfError);
      console.error('Error details:', {
        message: pdfError instanceof Error ? pdfError.message : String(pdfError),
        stack: pdfError instanceof Error ? pdfError.stack?.split('\n').slice(0, 5).join('\n') : undefined,
        htmlSize: Math.round(combinedHTML.length/1024) + 'KB',
        processedCount,
        errorType: pdfError instanceof Error ? pdfError.constructor.name : typeof pdfError,
      });

      // Return more helpful error message
      return NextResponse.json({
        error: 'PDF generation failed',
        message: pdfError instanceof Error ? pdfError.message : 'Unknown error occurred during PDF generation',
        suggestion: 'The document set may be too large. Try downloading fewer documents or use the chunked download option.',
        htmlSizeKB: Math.round(combinedHTML.length/1024),
        documentCount: processedCount,
      }, { status: 500 });
    }

  } catch (error) {
    console.error('❌ Bulk PDF download error:', error);
    return NextResponse.json({
      error: 'Internal server error',
      message: error instanceof Error ? error.message : 'An unexpected error occurred'
    }, { status: 500 });
  }
}