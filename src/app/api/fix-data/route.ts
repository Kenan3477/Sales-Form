import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '../../../lib/auth'
import { prisma } from '../../../lib/prisma'

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Update all sales records that have null/empty title or mailingCity
    const updateResult = await prisma.sale.updateMany({
      where: {
        OR: [
          { title: null },
          { title: '' },
          { mailingCity: null },
          { mailingCity: '' }
        ]
      },
      data: {
        title: 'Mr',  // Default title for records that don't have one
        mailingCity: 'London'  // Default city for records that don't have one
      }
    })

    // Get count of sales to see how many we updated
    const totalSales = await prisma.sale.count()

    return NextResponse.json({ 
      message: 'Sales records updated successfully',
      updatedRecords: updateResult.count,
      totalSales: totalSales
    })
  } catch (error) {
    console.error('Error updating sales data:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}