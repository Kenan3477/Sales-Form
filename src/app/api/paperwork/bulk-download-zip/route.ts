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
  console.log('🔄 Starting bulk ZIP download request...');
  
  try {
    // Authentication
    console.log('🔐 Checking authentication...');
    const session = await getServerSession(authOptions);
    if (!session?.user) {
      console.log('❌ No session found');
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    console.log('📥 Bulk ZIP download request started:', { 
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
    
    console.log('📥 Bulk ZIP download parameters:', { documentIds: documentIds?.length, downloadAll, filter });

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

    // Create ZIP file with all PDF documents
    console.log('📦 Creating ZIP archive with PDF documents...');
    
    // Dynamic import of JSZip for better compatibility
    const JSZip = (await import('jszip')).default;
    const zip = new JSZip();
    let processedCount = 0;
    let skippedFiles = 0;

    for (const doc of documents) {
      try {
        console.log(`📄 Processing document: ${doc.filename} for ${doc.sale.customerFirstName} ${doc.sale.customerLastName}`);
        
        // Get the PDF content from metadata
        if (doc.metadata && typeof doc.metadata === 'object' && 'documentContent' in doc.metadata) {
          const pdfContent = doc.metadata.documentContent as string;
          
          // Create a safe filename for the PDF
          const safeCustomerName = `${doc.sale.customerFirstName}_${doc.sale.customerLastName}`.replace(/[^a-zA-Z0-9_-]/g, '_');
          const pdfFileName = `${safeCustomerName}_${doc.template.templateType}_${new Date(doc.generatedAt).toISOString().slice(0, 10)}.pdf`;
          
          // Add PDF to ZIP (convert base64 to binary if needed)
          let pdfBuffer: Buffer;
          try {
            // Try to decode as base64 first
            pdfBuffer = Buffer.from(pdfContent, 'base64');
            
            // Verify it's a valid PDF by checking the header
            if (!pdfBuffer.toString('ascii', 0, 4).includes('PDF')) {
              // If not base64 PDF, try as direct binary string
              pdfBuffer = Buffer.from(pdfContent, 'binary');
            }
          } catch (error) {
            console.error(`❌ Error processing PDF content for ${doc.filename}:`, error);
            pdfBuffer = Buffer.from(pdfContent, 'utf8');
          }
          
          zip.file(pdfFileName, pdfBuffer);
          console.log(`✅ Added ${pdfFileName} to ZIP (${Math.round(pdfBuffer.length/1024)}KB)`);
          
          // Update download count
          await prisma.generatedDocument.update({
            where: { id: doc.id },
            data: { 
              downloadCount: { increment: 1 },
              lastDownloadAt: new Date()
            }
          });
          
          processedCount++;
        } else {
          console.error(`❌ No PDF content found in metadata for ${doc.filename}`);
          skippedFiles++;
        }
      } catch (error) {
        console.error(`❌ Error processing document ${doc.filename}:`, error);
        skippedFiles++;
      }
    }

    if (processedCount === 0) {
      console.error('❌ No PDF documents could be processed');
      return NextResponse.json({ 
        error: 'No PDF documents could be processed. Please ensure documents have been generated properly.' 
      }, { status: 500 });
    }

    console.log(`📦 ZIP archive ready: ${processedCount} PDFs processed, ${skippedFiles} files skipped`);

    // Generate the ZIP file
    const zipBuffer = await zip.generateAsync({ type: 'nodebuffer' });
    
    // Generate filename with current date
    const timestamp = new Date().toISOString().slice(0, 10);
    const zipFileName = `PAPERWORK_${timestamp}.zip`;
    
    console.log(`✅ ZIP file generated: ${zipFileName} (${Math.round(zipBuffer.length/1024)}KB)`);

    // Return the ZIP file
    return new NextResponse(Buffer.from(zipBuffer), {
      status: 200,
      headers: {
        'Content-Type': 'application/zip',
        'Content-Disposition': `attachment; filename="${zipFileName}"`,
        'Content-Length': zipBuffer.length.toString(),
      },
    });

  } catch (error) {
    console.error('❌ Bulk ZIP download error:', error);
    return NextResponse.json({ 
      error: 'Failed to create ZIP archive',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}