import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ documentId: string }> }
) {
  try {
    const { documentId } = await params;
    const url = new URL(request.url);
    const token = url.searchParams.get('token');

    // Validate token parameter
    if (!token) {
      return NextResponse.json({ error: 'Access token required' }, { status: 401 });
    }

    // Get document from database
    const document = await prisma.generatedDocument.findUnique({
      where: { id: documentId },
      include: {
        sale: {
          select: { 
            customerFirstName: true,
            customerLastName: true,
            email: true 
          },
        },
      },
    });

    if (!document) {
      return NextResponse.json({ error: 'Document not found' }, { status: 404 });
    }

    // Create a simple token based on document ID and customer email
    // This is basic security - in production you might want a more robust token system
    const expectedToken = Buffer.from(`${documentId}:${document.sale.email}`).toString('base64');
    
    if (token !== expectedToken) {
      return NextResponse.json({ error: 'Invalid access token' }, { status: 403 });
    }

    // Get document content from metadata
    let documentContent: string | undefined;
    
    if (document.metadata && typeof document.metadata === 'object' && 'documentContent' in document.metadata) {
      documentContent = document.metadata.documentContent as string;
    }
    
    if (!documentContent || typeof documentContent !== 'string') {
      return NextResponse.json(
        { error: 'Document content not found. Please contact support.' },
        { status: 404 }
      );
    }

    // Update download count
    await prisma.generatedDocument.update({
      where: { id: documentId },
      data: {
        downloadCount: { increment: 1 },
        lastDownloadAt: new Date(),
      },
    });

    // Return document content as response
    if (document.mimeType === 'application/pdf') {
      // For PDFs, the content is stored as base64, so decode it
      const pdfBuffer = Buffer.from(documentContent, 'base64');
      const responseContent = new Uint8Array(pdfBuffer);
      
      return new Response(responseContent, {
        headers: {
          'Content-Type': document.mimeType,
          'Content-Disposition': `attachment; filename="${document.filename}"`,
          'Content-Length': pdfBuffer.length.toString(),
          'Cache-Control': 'private, no-cache, no-store, must-revalidate',
          'Expires': '0',
          'Pragma': 'no-cache',
        },
      });
    } else {
      // For other formats (HTML), use as string
      return new Response(documentContent, {
        headers: {
          'Content-Type': document.mimeType,
          'Content-Disposition': `attachment; filename="${document.filename}"`,
          'Content-Length': Buffer.byteLength(documentContent, 'utf8').toString(),
          'Cache-Control': 'private, no-cache, no-store, must-revalidate',
          'Expires': '0',
          'Pragma': 'no-cache',
        },
      });
    }

  } catch (error) {
    console.error('Error downloading document:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}