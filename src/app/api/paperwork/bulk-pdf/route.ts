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

    // Get all generated documents
    const documents = await prisma.generatedDocument.findMany({
      where: {
        isDeleted: false,
      },
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

    console.log(`📋 Found ${documents.length} documents to process`);

    if (documents.length === 0) {
      return NextResponse.json({ 
        error: 'No documents available for download' 
      }, { status: 404 });
    }

    let processedCount = 0;
    let skippedFiles = 0;

    // Create combined HTML with improved PDF-ready styling
    let combinedHtml = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Documents - ${new Date().toLocaleDateString()}</title>
    <style>
        @page {
            size: A4;
            margin: 2cm;
        }
        
        * {
            box-sizing: border-box;
        }
        
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: white;
            line-height: 1.2;
            color: #333;
            font-size: 11px;
        }
        
        .customer-document {
            page-break-before: always;
            page-break-inside: avoid;
            page-break-after: always;
            width: 100%;
            padding: 0;
            margin: 0;
            min-height: 95vh;
            max-height: 95vh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        
        .customer-document:first-child {
            page-break-before: auto;
        }
        
        .document-content {
            flex: 1;
            width: 100%;
            margin: 0;
            padding: 0;
            overflow: hidden;
            font-size: 11px;
            line-height: 1.2;
            max-height: 95vh;
        }
        
        /* Ensure proper content flow and page breaks */
        .document-content h1,
        .document-content h2,
        .document-content h3 {
            page-break-after: avoid;
            page-break-inside: avoid;
            margin-top: 20px;
            margin-bottom: 15px;
        }
        
        .document-content p,
        .document-content div {
            page-break-inside: avoid;
            margin-bottom: 10px;
            orphans: 3;
            widows: 3;
        }
        
        .document-content table {
            page-break-inside: auto;
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        
        .document-content tr {
            page-break-inside: avoid;
            page-break-after: auto;
        }
        
        .document-content thead {
            display: table-header-group;
        }
        
        .document-content tbody tr {
            page-break-inside: avoid;
        }
        
        /* Reset any conflicting styles from embedded documents */
        .document-content * {
            max-width: 100% !important;
        }
        
        .document-content img {
            max-width: 100% !important;
            height: auto !important;
            page-break-inside: avoid;
        }
        
        /* Ensure content doesn't overflow */
        .document-content {
            overflow-wrap: break-word;
            word-wrap: break-word;
        }
        
        /* Print-specific optimizations */
        @media print {
            body {
                margin: 0 !important;
                padding: 0 !important;
            }
            
            .customer-document {
                width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
            }
            
            .customer-header {
                background-color: #f8f9fa !important;
                border: 2px solid #007bff !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
            
            .document-content {
                width: 100% !important;
            }
        }
        
        /* Hide any screen-only elements */
        .no-print {
            display: none !important;
        }
    </style>
</head>
<body>`;

    // Process each document
    for (const doc of documents) {
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

        // Extract and clean document content
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

        // Create customer page with proper structure for PDF
        combinedHtml += `
    <div class="customer-document">
        ${documentStyles ? `<style scoped>${documentStyles.replace(/<\/?style[^>]*>/gi, '')}</style>` : ''}
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

    // Close HTML
    combinedHtml += `
</body>
</html>`;

    if (processedCount === 0) {
      console.error('❌ No documents could be processed');
      return NextResponse.json({ 
        error: 'No documents could be processed. Documents may have been generated before the serverless migration or no valid documents found.' 
      }, { status: 500 });
    }

    console.log(`✅ Combined HTML document ready for PDF generation (${Math.round(combinedHtml.length/1024)}KB)`);
    console.log(`📄 Starting PDF generation for ${processedCount} customers...`);

    // For very large documents, we need to optimize the PDF generation
    if (combinedHtml.length > 10 * 1024 * 1024) { // > 10MB
      console.log('⚠️ Large document detected, applying optimizations...');
    }

    // Generate PDF using PDFService with optimized settings for large documents
    try {
      const pdfBuffer = await PDFService.generatePDFBuffer(combinedHtml, {
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

      // Generate filename
      const timestamp = new Date().toISOString().slice(0, 16).replace(/[:-]/g, '');
      const pdfFileName = `all_customer_documents_${processedCount}_customers_${timestamp}.pdf`;
      
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
        htmlSize: Math.round(combinedHtml.length/1024) + 'KB',
        processedCount,
        errorType: pdfError instanceof Error ? pdfError.constructor.name : typeof pdfError,
      });
      
      // If PDF generation fails due to size, offer alternative
      if (pdfError instanceof Error && (
        pdfError.message.includes('timeout') || 
        pdfError.message.includes('memory') ||
        pdfError.message.includes('Protocol error')
      )) {
        console.log('💡 Suggesting chunked download due to size limitations...');
        return NextResponse.json({
          error: 'Document set too large for single PDF generation',
          suggestion: 'Try downloading in smaller batches or use the HTML bulk download option',
          details: `Processing ${processedCount} customers (${Math.round(combinedHtml.length/1024)}KB) exceeded system limits`,
          processedCount,
          alternativeUrl: '/api/paperwork/bulk-download'
        }, { status: 413 }); // 413 Payload Too Large
      }
      
      return NextResponse.json({
        error: 'PDF generation failed',
        details: pdfError instanceof Error ? pdfError.message : String(pdfError),
        processedCount,
        htmlSize: Math.round(combinedHtml.length/1024) + 'KB'
      }, { status: 500 });
    }

  } catch (error) {
    console.error('❌ Bulk PDF download error:', error);
    return NextResponse.json({ 
      error: 'Failed to create PDF document archive',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}