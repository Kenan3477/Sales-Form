import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';

export async function POST(request: NextRequest) {
  try {
    // Authentication - only allow admin users
    const session = await getServerSession(authOptions);
    if (!session?.user || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    console.log('🔧 Starting document generation status fix...');
    
    // Get unique sale IDs that have documents but are not marked as documentsGenerated
    const saleIdsWithDocs = await prisma.generatedDocument.findMany({
      where: {
        isDeleted: false
      },
      select: {
        saleId: true
      },
      distinct: ['saleId']
    });
    
    const saleIds = saleIdsWithDocs.map(doc => doc.saleId);
    console.log(`📋 Found ${saleIds.length} unique sales with documents`);
    
    if (saleIds.length === 0) {
      return NextResponse.json({ 
        success: true, 
        message: 'No sales to update',
        updated: 0,
        verified: { salesWithDocs: 0, totalDocs: 0 }
      });
    }
    
    // Update all sales that have documents but are not marked as documentsGenerated
    const result = await prisma.sale.updateMany({
      where: {
        id: { in: saleIds },
        documentsGenerated: false
      },
      data: {
        documentsGenerated: true,
        documentsGeneratedAt: new Date(),
        documentsGeneratedBy: null // Historical documents don't have this info
      }
    });
    
    console.log(`✅ Updated ${result.count} sales to documentsGenerated: true`);
    
    // Verify the fix
    const finalCount = await prisma.sale.count({
      where: { documentsGenerated: true }
    });
    const totalDocs = await prisma.generatedDocument.count({
      where: { isDeleted: false }
    });
    
    console.log(`📊 Verification: ${finalCount} sales marked, ${totalDocs} total documents`);
    
    return NextResponse.json({
      success: true,
      message: `Successfully fixed document generation status`,
      updated: result.count,
      verified: {
        salesWithDocs: finalCount,
        totalDocs: totalDocs
      }
    });
    
  } catch (error) {
    console.error('❌ Error fixing document generation status:', error);
    return NextResponse.json({ 
      success: false,
      error: 'Failed to fix document generation status',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}