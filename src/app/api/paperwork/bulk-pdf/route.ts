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

        console.log(`🔍 SINGLE DOCUMENT MODE: ${doc.filename}, using original HTML directly`);
        console.log(`🔄 Starting PDF generation for ${Math.round(fileContent.length/1024)}KB HTML content`);

        // For single documents, use professional A4 single-page layout
        const singleDocumentCSS = `
          <style>
            /* Reset and base styles */
            * {
              margin: 0;
              padding: 0;
              box-sizing: border-box;
              -webkit-print-color-adjust: exact !important;
              print-color-adjust: exact !important;
            }
            
            /* A4 page constraints */
            @page {
              size: A4 !important;
              margin: 0 !important;
              orphans: 1;
              widows: 1;
            }
            
            /* A4 sheet container */
            html, body {
              width: 210mm !important;
              height: 297mm !important;
              margin: 0 !important;
              padding: 0 !important;
              font-family: Arial, Helvetica, sans-serif !important;
              font-size: 12pt !important;
              line-height: 1.3 !important;
              background: white !important;
              overflow: hidden !important;
            }
            
            /* Main content container */
            body {
              display: flex !important;
              flex-direction: column !important;
              padding: 12mm !important;
              width: 210mm !important;
              height: 297mm !important;
              transform-origin: top left !important;
            }
            
            /* Auto-fit scaling calculation */
            .document-content {
              width: 186mm !important; /* 210mm - 24mm padding */
              max-height: 273mm !important; /* 297mm - 24mm padding */
              overflow: hidden !important;
              flex: 1 !important;
              display: flex !important;
              flex-direction: column !important;
            }
            
            /* Absolute page break prevention */
            * {
              page-break-inside: avoid !important;
              break-inside: avoid !important;
              page-break-before: avoid !important;
              page-break-after: avoid !important;
              break-before: avoid !important;
              break-after: avoid !important;
            }
            
            /* Typography scaling */
            h1 {
              font-size: 16pt !important;
              line-height: 1.2 !important;
              margin: 0 0 6pt 0 !important;
              font-weight: bold !important;
            }
            
            h2 {
              font-size: 14pt !important;
              line-height: 1.2 !important;
              margin: 0 0 4pt 0 !important;
              font-weight: bold !important;
              padding: 4pt !important;
            }
            
            h3, h4 {
              font-size: 12pt !important;
              line-height: 1.2 !important;
              margin: 0 0 3pt 0 !important;
              font-weight: bold !important;
            }
            
            p {
              font-size: 10pt !important;
              line-height: 1.2 !important;
              margin: 0 0 3pt 0 !important;
            }
            
            /* Table optimization */
            table {
              width: 100% !important;
              border-collapse: collapse !important;
              margin: 2pt 0 !important;
              font-size: 9pt !important;
            }
            
            td, th {
              padding: 2pt !important;
              vertical-align: top !important;
              border: inherit !important;
              font-size: 9pt !important;
            }
            
            /* List optimization */
            ul, ol {
              margin: 0 0 3pt 12pt !important;
              padding: 0 !important;
            }
            
            li {
              font-size: 9pt !important;
              line-height: 1.2 !important;
              margin: 0 0 1pt 0 !important;
            }
            
            /* Section styling preservation */
            .header, .section, div[style*="background"] {
              background-color: inherit !important;
              color: inherit !important;
              margin: 2pt 0 !important;
              padding: 3pt !important;
              border-radius: inherit !important;
            }
            
            /* Image and logo handling */
            img {
              max-width: 100% !important;
              height: auto !important;
              display: inline-block !important;
              image-rendering: -webkit-optimize-contrast !important;
              image-rendering: crisp-edges !important;
            }
            
            /* Footer positioning */
            .footer, .guarantee {
              margin-top: auto !important;
              font-size: 8pt !important;
              padding: 2pt !important;
            }
            
            /* Responsive scaling for content overflow */
            @media print {
              .auto-scale {
                transform-origin: top left !important;
              }
            }
          </style>
          
          <script>
            // Auto-fit scaling function
            function fitToPage() {
              const content = document.querySelector('.document-content') || document.body;
              const maxHeight = 273; // mm (297 - 24mm padding)
              
              // Reset any previous scaling
              content.style.transform = '';
              
              // Measure actual content height
              const rect = content.getBoundingClientRect();
              const heightMM = (rect.height * 25.4) / 96; // Convert px to mm (assuming 96 DPI)
              
              if (heightMM > maxHeight) {
                const scale = maxHeight / heightMM;
                content.style.transform = 'scale(' + scale + ')';
                console.log('Auto-scaled content by factor:', scale.toFixed(3));
              }
            }
            
            // Apply scaling when DOM is ready
            if (document.readyState === 'loading') {
              document.addEventListener('DOMContentLoaded', fitToPage);
            } else {
              fitToPage();
            }
            
            // Apply before print (browser print)
            window.addEventListener('beforeprint', fitToPage);
          </script>
        `;

        // Wrap content in A4 container and inject CSS/JS
        let htmlWithWrapper = fileContent;
        
        // Add CSS and JS to head
        if (htmlWithWrapper.includes('</head>')) {
          htmlWithWrapper = htmlWithWrapper.replace('</head>', `${singleDocumentCSS}</head>`);
        } else {
          htmlWithWrapper = `${singleDocumentCSS}${htmlWithWrapper}`;
        }
        
        // Wrap body content in document-content container if not already wrapped
        if (!htmlWithWrapper.includes('document-content')) {
          htmlWithWrapper = htmlWithWrapper.replace(
            /<body[^>]*>/i,
            '$&<div class="document-content">'
          ).replace('</body>', '</div></body>');
        }

        console.log(`🎨 Added professional A4 single-page layout with auto-fit scaling`);

        // Update download count
        await prisma.generatedDocument.update({
          where: { id: doc.id },
          data: { 
            downloadCount: { increment: 1 },
            lastDownloadAt: new Date()
          }
        });

        // Generate PDF with optimal A4 single-page settings
        const pdfBuffer = await PDFService.generatePDFBuffer(htmlWithWrapper, {
          format: 'A4',
          margin: {
            top: '0',
            right: '0',
            bottom: '0',
            left: '0',
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