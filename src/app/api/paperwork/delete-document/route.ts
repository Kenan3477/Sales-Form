import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import fs from 'fs/promises';
import path from 'path';

export async function DELETE(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    
    if (!session || session.user.role !== 'admin') {
      return NextResponse.json(
        { error: 'Unauthorized - Admin access required' },
        { status: 401 }
      );
    }

    const { documentId } = await request.json();

    if (!documentId) {
      return NextResponse.json(
        { error: 'Document ID is required' },
        { status: 400 }
      );
    }

    // Find the document first to get file path
    const document = await prisma.generatedDocument.findUnique({
      where: { id: documentId }
    });

    if (!document) {
      return NextResponse.json(
        { error: 'Document not found' },
        { status: 404 }
      );
    }

    // Delete the physical file if it exists
    if (document.filePath) {
      try {
        const fullPath = path.join(process.cwd(), document.filePath);
        await fs.unlink(fullPath);
      } catch (fileError) {
        console.warn('Failed to delete physical file:', fileError);
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