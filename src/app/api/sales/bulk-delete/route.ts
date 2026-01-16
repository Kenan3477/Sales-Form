import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'

export async function DELETE(request: NextRequest) {
  try {
    // Check authentication
    const session = await getServerSession(authOptions)
    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Check if user is admin
    if (session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Admin access required' }, { status: 403 })
    }

    const { searchParams } = new URL(request.url)
    const action = searchParams.get('action') // 'all' or 'selected'
    const ids = searchParams.get('ids') // comma-separated sale IDs for selected delete

    if (action === 'all') {
      // Delete all sales and their appliances
      const deleteResult = await prisma.sale.deleteMany({})
      
      return NextResponse.json({
        success: true,
        message: `Successfully deleted ${deleteResult.count} sales`,
        deletedCount: deleteResult.count
      })
    } else if (action === 'selected' && ids) {
      // Delete selected sales
      const saleIds = ids.split(',').filter(id => id.trim())
      
      if (saleIds.length === 0) {
        return NextResponse.json({
          success: false,
          error: 'No sale IDs provided'
        }, { status: 400 })
      }

      const deleteResult = await prisma.sale.deleteMany({
        where: {
          id: {
            in: saleIds
          }
        }
      })

      return NextResponse.json({
        success: true,
        message: `Successfully deleted ${deleteResult.count} sales`,
        deletedCount: deleteResult.count
      })
    } else {
      return NextResponse.json({
        success: false,
        error: 'Invalid action. Use action=all or action=selected with ids parameter'
      }, { status: 400 })
    }

  } catch (error) {
    console.error('Bulk delete error:', error)
    return NextResponse.json(
      { 
        success: false,
        error: 'Internal server error'
      },
      { status: 500 }
    )
  }
}