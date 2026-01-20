import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';

export async function POST(request: NextRequest) {
  try {
    // Authentication - only ADMIN can run this
    const session = await getServerSession(authOptions);
    if (!session?.user || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    console.log('🔧 Starting boiler price data fix via API...');

    // Check for inconsistent sales
    const inconsistentSales = await prisma.sale.count({
      where: { 
        boilerCoverSelected: true,
        OR: [
          { boilerPriceSelected: 0 },
          { boilerPriceSelected: null }
        ]
      }
    });

    console.log(`Found ${inconsistentSales} sales with boilerCoverSelected=true but boilerPriceSelected=0/null`);

    if (inconsistentSales === 0) {
      return NextResponse.json({ 
        success: true,
        message: 'No inconsistent boiler pricing data found!',
        updated: 0
      });
    }

    // Use £29.99 as default (most common price)
    const defaultBoilerPrice = 29.99;
    let totalUpdated = 0;

    // Update in safe batches
    const batchSize = 50;
    while (true) {
      const salesToUpdate = await prisma.sale.findMany({
        where: { 
          boilerCoverSelected: true,
          OR: [
            { boilerPriceSelected: 0 },
            { boilerPriceSelected: null }
          ]
        },
        take: batchSize,
        select: { id: true }
      });

      if (salesToUpdate.length === 0) {
        break;
      }

      const saleIds = salesToUpdate.map(sale => sale.id);
      const updateResult = await prisma.sale.updateMany({
        where: { id: { in: saleIds } },
        data: { boilerPriceSelected: defaultBoilerPrice }
      });

      totalUpdated += updateResult.count;
      console.log(`Updated batch: ${updateResult.count} sales (Total: ${totalUpdated})`);

      // Small delay for safety
      await new Promise(resolve => setTimeout(resolve, 50));
    }

    // Verify the fix
    const remainingInconsistent = await prisma.sale.count({
      where: { 
        boilerCoverSelected: true,
        OR: [
          { boilerPriceSelected: 0 },
          { boilerPriceSelected: null }
        ]
      }
    });

    console.log(`✅ Boiler price fix completed: ${totalUpdated} sales updated`);

    return NextResponse.json({ 
      success: true,
      message: `Fixed boiler pricing inconsistencies`,
      updated: totalUpdated,
      defaultPrice: defaultBoilerPrice,
      beforeCount: inconsistentSales,
      afterCount: remainingInconsistent,
      fixedCount: inconsistentSales - remainingInconsistent
    });

  } catch (error) {
    console.error('❌ Error in boiler price fix API:', error);
    return NextResponse.json({ 
      success: false,
      error: 'Failed to fix boiler pricing data',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}