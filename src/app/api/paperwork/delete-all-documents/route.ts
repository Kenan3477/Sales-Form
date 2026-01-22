import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth/next';
import { authOptions } from '@/lib/auth';

export async function DELETE(request: NextRequest) {
  console.log('🗑️ Delete all documents request started');
  
  try {
    // Authentication
    const session = await getServerSession(authOptions);
    if (!session?.user) {
      console.log('❌ No session or user found');
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Only allow admins to delete all documents
    if (session.user.role !== 'ADMIN') {
      console.log('❌ User is not admin:', session.user.role);
      return NextResponse.json({ error: 'Admin access required' }, { status: 403 });
    }

    console.log('✅ Admin authenticated:', session.user.email);

    const { prisma } = await import('@/lib/prisma');

    // Get count of documents before deletion
    const documentCount = await prisma.generatedDocument.count();
    console.log(`📊 Found ${documentCount} documents to delete`);

    // Delete all generated documents
    const deleteResult = await prisma.generatedDocument.deleteMany({});
    console.log(`🗑️ Deleted ${deleteResult.count} documents`);

    // Reset documentsGenerated flag on all sales
    const salesUpdateResult = await prisma.sale.updateMany({
      data: {
        documentsGenerated: false,
        documentsGeneratedAt: null,
        documentsGeneratedBy: null
      }
    });
    console.log(`🔄 Reset document flags on ${salesUpdateResult.count} sales`);

    return NextResponse.json({
      success: true,
      message: 'All generated documents deleted successfully',
      documentsDeleted: deleteResult.count,
      salesReset: salesUpdateResult.count
    });

  } catch (error) {
    console.error('❌ Error deleting all documents:', error);
    return NextResponse.json(
      { error: 'Failed to delete documents' },
      { status: 500 }
    );
  }
}