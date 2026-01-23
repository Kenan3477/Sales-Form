import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';

export async function OPTIONS() {
  return new NextResponse(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}

export async function GET(request: NextRequest) {
  console.log('🔄 Starting batch PDF download...');
  
  try {
    // Authentication
    const session = await getServerSession(authOptions);
    console.log('🔐 Session check:', { hasSession: !!session, userId: session?.user?.id, role: session?.user?.role });
    
    if (!session?.user) {
      console.log('❌ No session or user found');
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }
    
    if (session.user.role !== 'ADMIN' && session.user.role !== 'AGENT') {
      console.log('❌ Insufficient permissions:', session.user.role);
      return NextResponse.json({ error: 'Unauthorized' }, { status: 403 });
    }

    const url = new URL(request.url);
    const batch = parseInt(url.searchParams.get('batch') || '1');
    const totalBatches = parseInt(url.searchParams.get('totalBatches') || '1');
    const batchSize = parseInt(url.searchParams.get('batchSize') || '300');
    const downloadAll = url.searchParams.get('downloadAll') === 'true';
    const filter = url.searchParams.get('filter');
    const documentIds = url.searchParams.get('documentIds')?.split(',') || [];

    console.log('📥 Batch download parameters:', { batch, totalBatches, batchSize, downloadAll, filter });

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
    console.log('📥 Fetching documents with params:', { downloadAll, documentIds: documentIds.length, filter, whereClause });
    
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

    console.log(`📊 Found ${documents.length} total documents`);

    // Get the specific batch
    const startIndex = (batch - 1) * batchSize;
    const endIndex = startIndex + batchSize;
    const batchDocuments = documents.slice(startIndex, endIndex);

    console.log(`📊 Processing batch ${batch}/${totalBatches}: ${batchDocuments.length} documents`);

    if (batchDocuments.length === 0) {
      return NextResponse.json({ error: 'No documents found for this batch' }, { status: 404 });
    }

    const mergedPdf = await createMergedPDF(batchDocuments, batch, totalBatches);
    
    const timestamp = new Date().toISOString().slice(0, 10);
    const fileName = totalBatches > 1 
      ? `PAPERWORK_BATCH_${batch}_of_${totalBatches}_${batchDocuments.length}_docs_${timestamp}.pdf`
      : `PAPERWORK_ALL_${batchDocuments.length}_documents_${timestamp}.pdf`;
    
    console.log(`✅ Batch ${batch} PDF created: ${fileName}`);
    
    return new NextResponse(Buffer.from(mergedPdf), {
      status: 200,
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': `attachment; filename="${fileName}"`,
        'Content-Length': mergedPdf.length.toString(),
      },
    });

  } catch (error) {
    console.error('❌ Batch PDF download error:', error);
    console.error('❌ Error stack:', error instanceof Error ? error.stack : 'No stack trace');
    
    // Return more detailed error information
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    const errorDetails = error instanceof Error ? {
      message: error.message,
      stack: error.stack?.split('\n').slice(0, 5).join('\n') // First 5 lines of stack
    } : { message: 'Unknown error type' };
    
    return NextResponse.json({ 
      error: 'Failed to create batch PDF',
      details: errorMessage,
      debug: errorDetails
    }, { status: 500 });
  }
}

async function createMergedPDF(documents: any[], batchNumber: number, totalBatches: number): Promise<Buffer> {
  // Dynamic import of PDF-lib
  const PDFLib = await import('pdf-lib');
  const { PDFDocument } = PDFLib;

  const mergedPdf = await PDFDocument.create();
  let processedCount = 0;
  let skippedFiles = 0;

  console.log(`📄 Creating merged PDF batch ${batchNumber}/${totalBatches} with ${documents.length} documents...`);

  for (const doc of documents) {
    try {
      console.log(`📄 Processing document: ${doc.filename} for ${doc.sale.customerFirstName} ${doc.sale.customerLastName}`);
      
      // Get the PDF content from metadata
      if (doc.metadata && typeof doc.metadata === 'object' && 'documentContent' in doc.metadata) {
        const pdfContent = doc.metadata.documentContent as string;
        
        // Convert base64 to buffer
        let pdfBuffer: Buffer;
        try {
          pdfBuffer = Buffer.from(pdfContent, 'base64');
          
          // Verify it's a valid PDF by checking the header
          if (!pdfBuffer.toString('ascii', 0, 4).includes('PDF')) {
            pdfBuffer = Buffer.from(pdfContent, 'binary');
          }
        } catch (error) {
          console.error(`❌ Error processing PDF content for ${doc.filename}:`, error);
          skippedFiles++;
          continue;
        }
        
        try {
          // Load the individual PDF
          console.log(`🔍 Loading PDF ${doc.filename} (${pdfBuffer.length} bytes)`);
          const individualPdf = await PDFDocument.load(pdfBuffer);
          const pageCount = individualPdf.getPageCount();
          console.log(`📖 PDF ${doc.filename} has ${pageCount} pages`);
          
          const pages = await mergedPdf.copyPages(individualPdf, individualPdf.getPageIndices());
          
          // Add pages to merged PDF
          pages.forEach((page) => mergedPdf.addPage(page));
          
          console.log(`✅ Added ${pages.length} page(s) from ${doc.filename} to batch ${batchNumber}`);
          processedCount++;
          
          // Update download count
          await prisma.generatedDocument.update({
            where: { id: doc.id },
            data: { 
              downloadCount: { increment: 1 },
              lastDownloadAt: new Date()
            }
          });
          
        } catch (pdfError) {
          console.error(`❌ Error loading/merging PDF ${doc.filename}:`, {
            filename: doc.filename,
            docId: doc.id,
            customerName: `${doc.sale.customerFirstName} ${doc.sale.customerLastName}`,
            bufferSize: pdfBuffer?.length || 'unknown',
            error: pdfError instanceof Error ? pdfError.message : pdfError,
            stack: pdfError instanceof Error ? pdfError.stack?.split('\n').slice(0, 3) : []
          });
          skippedFiles++;
        }
      } else {
        console.error(`❌ No PDF content found in metadata for ${doc.filename}`);
        skippedFiles++;
      }
    } catch (error) {
      console.error(`❌ Error processing document ${doc.filename}:`, {
        filename: doc.filename,
        docId: doc.id,
        error: error instanceof Error ? error.message : error,
        stack: error instanceof Error ? error.stack?.split('\n').slice(0, 3) : []
      });
      skippedFiles++;
    }
  }

  console.log(`📊 Merged PDF batch ${batchNumber} completed: ${processedCount} documents processed, ${skippedFiles} files skipped`);

  if (processedCount === 0) {
    console.error(`❌ No documents could be processed in batch ${batchNumber}`);
    throw new Error(`No PDF documents could be processed and merged in batch ${batchNumber}. All ${documents.length} documents were skipped due to errors.`);
  }

  // Generate the merged PDF
  console.log(`📝 Generating final merged PDF for batch ${batchNumber}...`);
  const pdfBytes = await mergedPdf.save();
  console.log(`✅ Batch ${batchNumber} PDF generated successfully: ${pdfBytes.length} bytes`);
  
  return Buffer.from(pdfBytes);
}