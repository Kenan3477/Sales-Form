import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { PaperworkService } from '@/lib/paperwork';
import { checkApiRateLimit } from '@/lib/rateLimit';
import * as fs from 'fs/promises';
import * as path from 'path';

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

    // Initialize paperwork service
    const paperworkService = new PaperworkService();

    // Get document info and check permissions
    const documentInfo = await paperworkService.getDocumentForDownload(documentId);
    if (!documentInfo) {
      return NextResponse.json({ error: 'Document not found' }, { status: 404 });
    }

    // Check if user has access to this document (agents can only access their own sales)
    if (session.user.role === 'AGENT') {
      const { prisma } = await import('@/lib/prisma');
      const document = await prisma.generatedDocument.findUnique({
        where: { id: documentId },
        include: {
          sale: {
            select: { createdById: true },
          },
        },
      });

      if (!document || document.sale.createdById !== session.user.id) {
        return NextResponse.json({ error: 'Access denied' }, { status: 403 });
      }
    }

    // Check if file exists
    try {
      await fs.access(documentInfo.filePath);
    } catch (error) {
      console.error('File not found:', documentInfo.filePath);
      return NextResponse.json(
        { error: 'Document file not found on disk' },
        { status: 404 }
      );
    }

    // Read file and return as download
    const fileBuffer = await fs.readFile(documentInfo.filePath);
    
    // Determine if it should be inline or attachment based on query param
    const url = new URL(request.url);
    const disposition = url.searchParams.get('inline') === 'true' ? 'inline' : 'attachment';

    return new Response(new Uint8Array(fileBuffer), {
      headers: {
        'Content-Type': documentInfo.mimeType,
        'Content-Disposition': `${disposition}; filename="${documentInfo.filename}"`,
        'Content-Length': fileBuffer.length.toString(),
        'Cache-Control': 'private, no-cache, no-store, must-revalidate',
        'Expires': '0',
        'Pragma': 'no-cache',
      },
    });

  } catch (error) {
    console.error('Document download error:', error);

    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}