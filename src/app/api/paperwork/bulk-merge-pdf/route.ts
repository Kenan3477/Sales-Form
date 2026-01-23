import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';

export async function OPTIONS(request: NextRequest) {
  return new NextResponse(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}

export async function POST(request: NextRequest) {
  console.log('🔄 Starting bulk PDF merge request...');
  
  try {
    // Authentication
    console.log('🔐 Checking authentication...');
    const session = await getServerSession(authOptions);
    if (!session?.user) {
      console.log('❌ No session found');
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    console.log('📥 Bulk PDF merge request started:', { 
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
    const { documentIds, downloadAll = false, filter, batchSize = 300 } = body;
    
    console.log('📥 Bulk PDF merge parameters:', { 
      documentIds: documentIds?.length, 
      downloadAll, 
      filter, 
      batchSize 
    });

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

    console.log('📥 Found documents for bulk merge:', documents.length);

    if (documents.length === 0) {
      console.log('❌ No documents found for bulk merge');
      return NextResponse.json({ error: 'No documents found' }, { status: 404 });
    }

    // Calculate batches
    const totalBatches = Math.ceil(documents.length / batchSize);
    console.log(`📊 Will create ${totalBatches} PDF batch(es) with max ${batchSize} documents each`);

    // If only one batch needed, create single PDF
    if (totalBatches === 1) {
      const mergedPdf = await createMergedPDF(documents, 1, 1);
      
      const timestamp = new Date().toISOString().slice(0, 10);
      const fileName = `PAPERWORK_ALL_${documents.length}_documents_${timestamp}.pdf`;
      
      console.log(`✅ Single merged PDF created: ${fileName}`);
      
      return new NextResponse(Buffer.from(mergedPdf), {
        status: 200,
        headers: {
          'Content-Type': 'application/pdf',
          'Content-Disposition': `attachment; filename="${fileName}"`,
          'Content-Length': mergedPdf.length.toString(),
        },
      });
    }

    // Multiple batches - return info about batches for frontend to download individually
    const batchInfo = [];
    for (let i = 0; i < totalBatches; i++) {
      const start = i * batchSize;
      const end = Math.min(start + batchSize, documents.length);
      const batchDocs = documents.slice(start, end);
      
      batchInfo.push({
        batch: i + 1,
        totalBatches,
        documentCount: batchDocs.length,
        startIndex: start,
        endIndex: end - 1
      });
    }

    return NextResponse.json({
      totalDocuments: documents.length,
      batchSize,
      totalBatches,
      batches: batchInfo,
      message: `${documents.length} documents will be split into ${totalBatches} PDF files. Use the batch download endpoint to get each batch.`
    });

  } catch (error) {
    console.error('❌ Bulk PDF merge error:', error);
    return NextResponse.json({ 
      error: 'Failed to merge PDFs',
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
          
          console.log(`✅ Added ${pages.length} page(s) from ${doc.filename} to merged PDF`);
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