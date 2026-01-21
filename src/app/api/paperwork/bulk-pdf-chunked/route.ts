import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { checkApiRateLimit } from '@/lib/rateLimit';
import { PDFService } from '@/lib/paperwork/pdf-service';

export async function GET(request: NextRequest) {
  try {
    console.log('🚀 PDF Chunked endpoint hit:', request.url);
    
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
    console.log('🔐 Session check:', session ? `User: ${session.user?.email}` : 'No session');
    
    if (!session?.user) {
      console.log('❌ Unauthorized access attempt');
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Only admin users can bulk download all customer documents
    if (session.user.role !== 'ADMIN') {
      console.log(`❌ Access denied for role: ${session.user.role}`);
      return NextResponse.json({ error: 'Admin access required' }, { status: 403 });
    }

    // Get chunk parameters
    const url = new URL(request.url);
    const chunkParam = url.searchParams.get('chunk');
    const chunksParam = url.searchParams.get('chunks');
    const chunkSize = parseInt(url.searchParams.get('size') || '100');
    
    console.log(`📊 Request params:`, { chunk: chunkParam, chunks: chunksParam, size: chunkSize });
    if (!chunkParam || !chunksParam) {
      return NextResponse.json({ 
        error: 'Missing chunk parameters. Use /api/paperwork/bulk-pdf-info to get chunk information.' 
      }, { status: 400 });
    }

    const chunk = parseInt(chunkParam);
    const totalChunks = parseInt(chunksParam);
    
    if (chunk < 1 || chunk > totalChunks) {
      return NextResponse.json({ 
        error: `Invalid chunk number. Must be between 1 and ${totalChunks}` 
      }, { status: 400 });
    }

    const { prisma } = await import('@/lib/prisma');
    console.log(`📋 Starting chunked PDF download - chunk ${chunk}/${totalChunks} for admin: ${session.user.email}`);

    // Calculate offset and limit for this chunk
    const offset = (chunk - 1) * chunkSize;
    const limit = chunkSize;

    console.log(`📊 Database query params: offset=${offset}, limit=${limit}`);

    // Get documents for this chunk
    let documents;
    try {
      documents = await prisma.generatedDocument.findMany({
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
        skip: offset,
        take: limit,
      });
      console.log(`📋 Found ${documents.length} documents in chunk ${chunk}`);
    } catch (dbError) {
      console.error('❌ Database query failed:', dbError);
      return NextResponse.json({ 
        error: 'Database query failed',
        details: dbError instanceof Error ? dbError.message : String(dbError)
      }, { status: 500 });
    }

    if (documents.length === 0) {
      return NextResponse.json({ 
        error: 'No documents found in this chunk' 
      }, { status: 404 });
    }

    // Generate HTML for this chunk (using the same logic as bulk-pdf)
    let combinedHtml = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Documents - Chunk ${chunk}/${totalChunks}</title>
    <style>
        @page {
            size: A4;
            margin: 1cm;
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
        
        .chunk-info {
            background-color: #e9ecef;
            padding: 10px;
            border: 1px solid #dee2e6;
            text-align: center;
            font-weight: bold;
            color: #495057;
            margin-bottom: 20px;
            page-break-after: avoid;
            font-size: 12px;
        }
        
        /* Aggressive content compression for single-page fit */
        .document-content * {
            margin-top: 0 !important;
            margin-bottom: 6px !important;
            padding-top: 0 !important;
            padding-bottom: 2px !important;
            line-height: 1.1 !important;
            max-width: 100% !important;
        }
        
        .document-content h1 { 
            font-size: 14px !important; 
            margin: 8px 0 6px 0 !important;
            font-weight: bold !important;
            page-break-after: avoid !important;
        }
        .document-content h2 { 
            font-size: 12px !important; 
            margin: 6px 0 4px 0 !important;
            font-weight: bold !important;
            page-break-after: avoid !important;
        }
        .document-content h3 { 
            font-size: 11px !important; 
            margin: 4px 0 3px 0 !important;
            font-weight: bold !important;
            page-break-after: avoid !important;
        }
        .document-content p { 
            font-size: 10px !important; 
            margin: 0 0 4px 0 !important;
            line-height: 1.1 !important;
        }
        .document-content div {
            font-size: 10px !important;
            margin: 0 0 3px 0 !important;
            line-height: 1.1 !important;
        }
        
        /* Compact table styling */
        .document-content table { 
            width: 100% !important; 
            margin-bottom: 8px !important; 
            border-collapse: collapse !important;
            font-size: 9px !important;
            border-spacing: 0 !important;
        }
        .document-content td, .document-content th { 
            padding: 3px 4px !important; 
            border: 1px solid #ddd !important; 
            font-size: 9px !important;
            line-height: 1.1 !important;
            vertical-align: top !important;
        }
        .document-content th {
            background-color: #f5f5f5 !important;
            font-weight: bold !important;
        }
        
        /* Handle long text and prevent overflow */
        .document-content {
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
            hyphens: auto !important;
        }
        
        /* Remove excessive spacing from lists */
        .document-content ul, .document-content ol {
            margin: 0 0 6px 0 !important;
            padding-left: 20px !important;
        }
        .document-content li {
            margin: 0 0 2px 0 !important;
            font-size: 10px !important;
            line-height: 1.1 !important;
        }
        
        /* Ensure images don't break layout */
        .document-content img {
            max-width: 100% !important;
            height: auto !important;
            max-height: 150px !important;
            display: block !important;
            margin: 4px 0 !important;
        }
        
        /* Hide any print-breaking elements */
        .document-content .page-break,
        .document-content .break,
        .document-content br + br,
        .document-content hr {
            display: none !important;
        }
        
        /* Force all content to stay within page */
        .document-content {
            max-height: calc(95vh - 120px);
            overflow: hidden;
        }
        
        /* Print-specific optimizations */
        @media print {
            body {
                margin: 0 !important;
                padding: 0 !important;
                font-size: 11px !important;
            }
            
            .customer-document {
                width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
                min-height: 95vh !important;
                max-height: 95vh !important;
                page-break-inside: avoid !important;
            }
            
            .customer-header {
                background-color: #f8f9fa !important;
                border: 2px solid #007bff !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
            
            .document-content {
                width: 100% !important;
                max-height: calc(95vh - 100px) !important;
            }
            
            /* Ensure fonts render correctly */
            * {
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
        }
        
        .no-print {
            display: none !important;
        }
    </style>
</head>
<body>
    <div class="chunk-info">
        Customer Documents - Chunk ${chunk} of ${totalChunks}<br>
        Generated on ${new Date().toLocaleDateString()} at ${new Date().toLocaleTimeString()}
    </div>`;

    let processedCount = 0;
    let skippedFiles = 0;

    // Process each document in this chunk
    for (const doc of documents) {
      try {
        // Get document content from metadata
        let fileContent: string | undefined;
        
        if (doc.metadata && typeof doc.metadata === 'object' && 'documentContent' in doc.metadata) {
          fileContent = doc.metadata.documentContent as string;
        }
        
        if (!fileContent || typeof fileContent !== 'string') {
          console.error(`❌ Document content not found for ${doc.filename}`);
          skippedFiles++;
          continue;
        }

        console.log(`🔍 Processing document: ${doc.filename}, Content length: ${fileContent.length}`);

        // Extract and clean document content
        let documentHtml = fileContent;
        let documentStyles = '';
        let documentBody = '';
        
        // Extract styles from the head section
        const styleMatch = documentHtml.match(/<style[^>]*>([\s\S]*?)<\/style>/gi);
        if (styleMatch) {
          documentStyles = styleMatch.join('\n');
          console.log(`📝 Found ${styleMatch.length} style blocks`);
        }
        
        // Extract content from body
        const bodyMatch = documentHtml.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
        if (bodyMatch) {
          documentBody = bodyMatch[1].trim();
          console.log(`📄 Extracted body content: ${documentBody.length} chars`);
        } else {
          documentBody = documentHtml
            .replace(/<!DOCTYPE[^>]*>/gi, '')
            .replace(/<html[^>]*>/gi, '')
            .replace(/<\/html>/gi, '')
            .replace(/<head[^>]*>[\s\S]*?<\/head>/gi, '')
            .trim();
          console.log(`📄 Fallback content extraction: ${documentBody.length} chars`);
        }

        // Create customer page
        combinedHtml += `
    <div class="customer-document">
        ${documentStyles ? `<style scoped>${documentStyles.replace(/<\/?style[^>]*>/gi, '')}</style>` : ''}
        <div class="document-content">
            ${documentBody || '<p>No document content available</p>'}
        </div>
    </div>
`;

        processedCount++;
        console.log(`✅ Added customer ${processedCount}: ${doc.sale.customerFirstName} ${doc.sale.customerLastName}`);
      } catch (error) {
        console.error(`❌ Error processing file ${doc.filename}:`, error);
        skippedFiles++;
      }
    }

    // Close HTML
    combinedHtml += `
</body>
</html>`;

    if (processedCount === 0) {
      return NextResponse.json({ 
        error: 'No documents could be processed in this chunk' 
      }, { status: 500 });
    }

    console.log(`✅ Chunk ${chunk} HTML ready for PDF generation (${Math.round(combinedHtml.length/1024)}KB)`);

    // Generate PDF
    try {
      console.log(`🔧 Generating PDF for chunk ${chunk}...`);
      
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
        timeout: 120000, // 2 minutes for chunk
      });

      console.log(`✅ Chunk ${chunk} PDF generated! Size: ${Math.round(pdfBuffer.length/1024)}KB`);

      const timestamp = new Date().toISOString().slice(0, 16).replace(/[:-]/g, '');
      const pdfFileName = `customer_documents_chunk_${chunk}_of_${totalChunks}_${timestamp}.pdf`;
      
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
      console.error(`❌ Chunk ${chunk} PDF generation failed:`, pdfError);
      return NextResponse.json({
        error: `PDF generation failed for chunk ${chunk}`,
        details: pdfError instanceof Error ? pdfError.message : String(pdfError),
        chunk,
        totalChunks,
        processedCount,
      }, { status: 500 });
    }

  } catch (error) {
    console.error('❌ Chunked PDF download error:', error);
    return NextResponse.json({ 
      error: 'Failed to create chunked PDF',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}