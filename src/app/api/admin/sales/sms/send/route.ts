import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '../../../../../../lib/auth'
import { sendSmsForSales } from '../../../../../../lib/sms'
import { prisma } from '../../../../../../lib/prisma'

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await request.json()
    const { saleIds, confirm } = body

    if (!Array.isArray(saleIds) || saleIds.length === 0) {
      return NextResponse.json(
        { error: 'Sale IDs are required' },
        { status: 400 }
      )
    }

    if (!confirm) {
      return NextResponse.json(
        { error: 'Confirmation required' },
        { status: 400 }
      )
    }

    // Validate sale IDs exist and get preview info
    const sales = await prisma.sale.findMany({
      where: {
        id: { in: saleIds }
      },
      include: {
        smsLogs: {
          orderBy: { createdAt: 'desc' },
          take: 1
        }
      }
    })

    if (sales.length !== saleIds.length) {
      return NextResponse.json(
        { error: 'Some sales not found' },
        { status: 404 }
      )
    }

    // Send SMS messages
    console.log(`Admin ${session.user.email} sending SMS to ${saleIds.length} sales`)
    
    const result = await sendSmsForSales(saleIds)

    console.log(`SMS batch complete:`, {
      total: saleIds.length,
      sent: result.sent,
      failed: result.failed,
      skipped: result.skipped,
      alreadySent: result.alreadySent
    })

    return NextResponse.json({
      success: true,
      summary: {
        total: saleIds.length,
        sent: result.sent,
        failed: result.failed,
        skipped: result.skipped,
        alreadySent: result.alreadySent
      },
      details: result.results
    })

  } catch (error) {
    console.error('Error sending SMS batch:', error)
    return NextResponse.json(
      { error: 'Failed to send SMS messages' },
      { status: 500 }
    )
  }
}