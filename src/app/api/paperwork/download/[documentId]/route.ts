import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { checkApiRateLimit } from '@/lib/rateLimit';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ documentId: string }> }
) {
  try {
    const { documentId } = await params;

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

    // Get document from database
    const { prisma } = await import('@/lib/prisma');
    const document = await prisma.generatedDocument.findUnique({
      where: { id: documentId },
      include: {
        sale: {
          select: { createdById: true },
        },
      },
    });

    if (!document) {
      return NextResponse.json({ error: 'Document not found' }, { status: 404 });
    }

    // Check if user has access to this document (agents can only access their own sales)
    if (session.user.role === 'AGENT' && document.sale.createdById !== session.user.id) {
      return NextResponse.json({ error: 'Access denied' }, { status: 403 });
    }

    // Get document content from metadata (stored there since we can't use filesystem on Vercel)
    let documentContent: string | undefined;
    
    if (document.metadata && typeof document.metadata === 'object' && 'documentContent' in document.metadata) {
      documentContent = document.metadata.documentContent as string;
    }
    
    if (!documentContent || typeof documentContent !== 'string') {
      return NextResponse.json(
        { error: 'Document content not found. Document may have been generated before the serverless migration.' },
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

    // Determine if it should be inline or attachment based on query param
    const url = new URL(request.url);
    const disposition = url.searchParams.get('inline') === 'true' ? 'inline' : 'attachment';

    // Return document content as response
    if (document.mimeType === 'application/pdf') {
      // For PDFs, the content is stored as base64, so decode it
      const pdfBuffer = Buffer.from(documentContent, 'base64');
      const responseContent = new Uint8Array(pdfBuffer);
      
      return new Response(responseContent, {
        headers: {
          'Content-Type': document.mimeType,
          'Content-Disposition': `${disposition}; filename="${document.filename}"`,
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
          'Content-Disposition': `${disposition}; filename="${document.filename}"`,
          'Content-Length': Buffer.byteLength(documentContent, 'utf8').toString(),
          'Cache-Control': 'private, no-cache, no-store, must-revalidate',
          'Expires': '0',
          'Pragma': 'no-cache',
        },
      });
    }

  } catch (error) {
    console.error('Document download error:', error);

    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}