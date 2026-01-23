import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';

export async function GET(request: NextRequest) {
  console.log('🔄 Starting batch PDF download...');
  
  try {
    // Authentication
    const session = await getServerSession(authOptions);
    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }
    
    if (session.user.role !== 'ADMIN' && session.user.role !== 'AGENT') {
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
    return NextResponse.json({ 
      error: 'Failed to create batch PDF',
      details: error instanceof Error ? error.message : 'Unknown error'
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
          const individualPdf = await PDFDocument.load(pdfBuffer);
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
          console.error(`❌ Error merging PDF ${doc.filename}:`, pdfError);
          skippedFiles++;
        }
      } else {
        console.error(`❌ No PDF content found in metadata for ${doc.filename}`);
        skippedFiles++;
      }
    } catch (error) {
      console.error(`❌ Error processing document ${doc.filename}:`, error);
      skippedFiles++;
    }
  }

  console.log(`📊 Merged PDF batch ${batchNumber} completed: ${processedCount} documents processed, ${skippedFiles} files skipped`);

  if (processedCount === 0) {
    throw new Error('No PDF documents could be processed and merged');
  }

  // Generate the merged PDF
  const pdfBytes = await mergedPdf.save();
  return Buffer.from(pdfBytes);
}