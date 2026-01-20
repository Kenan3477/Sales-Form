import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import JSZip from 'jszip';

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
        }
      });
    }

    console.log('📥 Found documents for bulk download:', documents.length);

    if (documents.length === 0) {
      console.log('❌ No documents found for bulk download');
      return NextResponse.json({ error: 'No documents found' }, { status: 404 });
    }

    // Create ZIP file
    const zip = new JSZip();
    let addedFiles = 0;
    let skippedFiles = 0;

    for (const doc of documents) {
      try {
        // Get document content from metadata (stored there since we can't use filesystem on serverless platforms)
        let fileContent: string | undefined;
        
        if (doc.metadata && typeof doc.metadata === 'object' && 'documentContent' in doc.metadata) {
          fileContent = doc.metadata.documentContent as string;
        }
        
        if (!fileContent || typeof fileContent !== 'string') {
          console.error(`❌ Document content not found for ${doc.filename}. Document may have been generated before serverless migration.`);
          skippedFiles++;
          continue; // Skip this document but continue with others
        }
        
        // Create organized folder structure
        const customerName = `${doc.sale.customerFirstName}_${doc.sale.customerLastName}`;
        const folderName = customerName.replace(/[^a-zA-Z0-9]/g, '_');
        const fileName = doc.filename;
        
        zip.file(`${folderName}/${fileName}`, fileContent);
        addedFiles++;

        // Update download count
        await prisma.generatedDocument.update({
          where: { id: doc.id },
          data: { 
            downloadCount: { increment: 1 },
            lastDownloadAt: new Date()
          }
        });
        
        console.log(`✅ Added file to archive: ${folderName}/${fileName}`);
      } catch (error) {
        console.error(`❌ Error processing file ${doc.filename}:`, error);
        skippedFiles++;
        // Continue with other files
      }
    }

    console.log(`📥 Bulk download processing complete: ${addedFiles} added, ${skippedFiles} skipped`);

    if (addedFiles === 0) {
      console.error('❌ No files could be added to archive');
      return NextResponse.json({ 
        error: 'No files could be added to archive. Documents may have been generated before the serverless migration.' 
      }, { status: 500 });
    }

    // Generate ZIP file
    console.log('📦 Generating ZIP archive...');
    const zipBuffer = await zip.generateAsync({ type: 'nodebuffer' });
    
    // Generate filename
    const timestamp = new Date().toISOString().slice(0, 16).replace(/[:-]/g, '');
    const zipFileName = `documents_${timestamp}.zip`;
    
    console.log(`✅ ZIP archive created: ${zipFileName} (${zipBuffer.length} bytes)`);

    return new NextResponse(new Uint8Array(zipBuffer), {
      status: 200,
      headers: {
        'Content-Type': 'application/zip',
        'Content-Disposition': `attachment; filename="${zipFileName}"`,
        'Content-Length': zipBuffer.length.toString(),
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