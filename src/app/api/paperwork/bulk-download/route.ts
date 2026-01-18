import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import { withSecurity } from '@/lib/apiSecurity';
import JSZip from 'jszip';
import path from 'path';
import { readFile } from 'fs/promises';

async function handleBulkDownload(request: NextRequest, context: any) {
  try {
    const { user } = context;
    
    if (user.role !== 'admin' && user.role !== 'agent') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 403 });
    }

    const body = await request.json();
    const { documentIds, downloadAll = false, filter } = body;

    let whereClause: any = {
      isDeleted: false
    };

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

    if (documents.length === 0) {
      return NextResponse.json({ error: 'No documents found' }, { status: 404 });
    }

    // Create ZIP file
    const zip = new JSZip();
    let addedFiles = 0;

    for (const doc of documents) {
      try {
        const filePath = path.join(process.cwd(), doc.filePath);
        const fileContent = await readFile(filePath, 'utf8');
        
        // Create organized folder structure
        const customerName = `${doc.sale.customerFirstName}_${doc.sale.customerLastName}`;
        const folderName = customerName.replace(/[^a-zA-Z0-9]/g, '_');
        const fileName = doc.filename;
        
        zip.file(`${folderName}/${fileName}`, fileContent);
        addedFiles++;

        // Update download count
        await prisma.generatedDocument.update({
          where: { id: doc.id },
          data: { downloadCount: { increment: 1 } }
        });
      } catch (error) {
        console.error(`Error adding file ${doc.filename}:`, error);
        // Continue with other files
      }
    }

    if (addedFiles === 0) {
      return NextResponse.json({ error: 'No files could be added to archive' }, { status: 500 });
    }

    // Generate ZIP file
    const zipBuffer = await zip.generateAsync({ type: 'nodebuffer' });
    
    // Generate filename
    const timestamp = new Date().toISOString().slice(0, 16).replace(/[:-]/g, '');
    const zipFileName = `documents_${timestamp}.zip`;

    return new NextResponse(new Uint8Array(zipBuffer), {
      status: 200,
      headers: {
        'Content-Type': 'application/zip',
        'Content-Disposition': `attachment; filename="${zipFileName}"`,
        'Content-Length': zipBuffer.length.toString(),
      },
    });

  } catch (error) {
    console.error('Bulk download error:', error);
    return NextResponse.json({ 
      error: 'Failed to create document archive' 
    }, { status: 500 });
  }
}

export const POST = withSecurity(handleBulkDownload, {
  requireAuth: true,
  logAccess: true
});