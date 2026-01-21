import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { checkApiRateLimit } from '@/lib/rateLimit';
import { prisma } from '@/lib/prisma';
import fs from 'fs/promises';
import path from 'path';

export async function DELETE(
  request: NextRequest,
  { params }: { params: { documentId: string } }
) {
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
      return NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      );
    }

    const { documentId } = params;

    // Find the document first
    const document = await prisma.generatedDocument.findUnique({
      where: { id: documentId },
      include: { sale: true }
    });

    if (!document) {
      return NextResponse.json(
        { error: 'Document not found' },
        { status: 404 }
      );
    }

    // Check authorization - only admin or the agent who created the sale can delete
    const isAdmin = session.user.role === 'admin';
    const isOwner = session.user.id === document.sale.createdById;

    if (!isAdmin && !isOwner) {
      return NextResponse.json(
        { error: 'Insufficient permissions to delete this document' },
        { status: 403 }
      );
    }

    // Delete the physical file if it exists
    if (document.filePath) {
      try {
        const fullPath = path.join(process.cwd(), document.filePath);
        await fs.unlink(fullPath);
      } catch (fileError) {
        console.warn('File not found or could not be deleted:', document.filePath);
        // Continue with database deletion even if file deletion fails
      }
    }

    // Delete from database
    await prisma.generatedDocument.delete({
      where: { id: documentId }
    });

    return NextResponse.json({
      success: true,
      message: 'Document deleted successfully'
    });

  } catch (error) {
    console.error('Error deleting document:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}