import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { checkApiRateLimit } from '@/lib/rateLimit';

export async function GET(request: NextRequest) {
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

    // Only admin users can access this
    if (session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Admin access required' }, { status: 403 });
    }

    const { prisma } = await import('@/lib/prisma');

    // Count total documents
    const totalDocuments = await prisma.generatedDocument.count({
      where: {
        isDeleted: false,
      },
    });

    // Get size estimation
    const sampleDoc = await prisma.generatedDocument.findFirst({
      where: {
        isDeleted: false,
      },
      include: {
        template: true,
        sale: true,
      },
    });

    let estimatedSizePerDoc = 20000; // Default 20KB per document
    if (sampleDoc && sampleDoc.metadata && typeof sampleDoc.metadata === 'object' && 'documentContent' in sampleDoc.metadata) {
      const sampleContent = sampleDoc.metadata.documentContent as string;
      if (typeof sampleContent === 'string') {
        estimatedSizePerDoc = sampleContent.length;
      }
    }

    const estimatedTotalSize = totalDocuments * estimatedSizePerDoc;
    const recommendedChunkSize = estimatedTotalSize > 50 * 1024 * 1024 ? 25 : 50; // Smaller chunks for Vercel limits
    const totalChunks = Math.ceil(totalDocuments / recommendedChunkSize);

    // Determine if chunking is recommended
    const shouldChunk = totalDocuments > 100 || estimatedTotalSize > 20 * 1024 * 1024;

    return NextResponse.json({
      totalDocuments,
      estimatedSizePerDocument: Math.round(estimatedSizePerDoc / 1024) + 'KB',
      estimatedTotalSize: Math.round(estimatedTotalSize / (1024 * 1024)) + 'MB',
      shouldUseChunking: shouldChunk,
      recommendedChunkSize,
      totalChunks: shouldChunk ? totalChunks : 1,
      reasoning: shouldChunk 
        ? `Large document set (${totalDocuments} docs, ~${Math.round(estimatedTotalSize / (1024 * 1024))}MB) - chunking recommended for better performance`
        : `Small document set (${totalDocuments} docs) - single PDF should work fine`,
      chunkUrls: shouldChunk ? Array.from({ length: totalChunks }, (_, i) => 
        `/api/paperwork/bulk-pdf-chunked?chunk=${i + 1}&chunks=${totalChunks}&size=${recommendedChunkSize}`
      ) : [],
      singlePdfUrl: '/api/paperwork/bulk-pdf',
    });

  } catch (error) {
    console.error('❌ Bulk PDF info error:', error);
    return NextResponse.json({ 
      error: 'Failed to get bulk PDF information',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}