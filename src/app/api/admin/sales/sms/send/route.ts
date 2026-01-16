import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '../../../../../../lib/auth'
import { sendSmsForSales } from '../../../../../../lib/sms'
import { prisma } from '../../../../../../lib/prisma'

export async function POST(request: NextRequest) {
  try {
    console.log('SMS send request received')
    
    const session = await getServerSession(authOptions)
    
    if (!session || session.user.role !== 'ADMIN') {
      console.log('Unauthorized access attempt:', session?.user)
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    console.log('Processing SMS request for admin:', session.user.email)

    const body = await request.json()
    const { saleIds, confirm } = body

    console.log('SMS request body:', { saleIdsCount: saleIds?.length, confirm })

    if (!Array.isArray(saleIds) || saleIds.length === 0) {
      console.log('Invalid saleIds:', saleIds)
      return NextResponse.json(
        { error: 'Sale IDs are required' },
        { status: 400 }
      )
    }

    if (!confirm) {
      console.log('Confirmation not provided')
      return NextResponse.json(
        { error: 'Confirmation required' },
        { status: 400 }
      )
    }

    // Check environment variables
    if (!process.env.VOODOO_API_KEY) {
      console.error('VOODOO_API_KEY not configured')
      return NextResponse.json(
        { error: 'SMS service not configured' },
        { status: 500 }
      )
    }

    console.log('Validating sales exist for IDs:', saleIds)

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

    console.log('Found sales:', sales.length, 'Expected:', saleIds.length)

    if (sales.length !== saleIds.length) {
      console.log('Sales count mismatch')
      return NextResponse.json(
        { error: 'Some sales not found' },
        { status: 404 }
      )
    }

    // Send SMS messages
    console.log(`Admin ${session.user.email} sending SMS to ${saleIds.length} sales`)
    
    try {
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
    } catch (smsError) {
      console.error('SMS processing error:', smsError)
      return NextResponse.json(
        { error: `SMS processing failed: ${smsError instanceof Error ? smsError.message : 'Unknown error'}` },
        { status: 500 }
      )
    }

  } catch (error) {
    console.error('SMS API endpoint error:', error)
    console.error('Error details:', {
      message: error instanceof Error ? error.message : 'Unknown error',
      stack: error instanceof Error ? error.stack : undefined,
      name: error instanceof Error ? error.name : typeof error
    })
    return NextResponse.json(
      { 
        error: 'Failed to send SMS messages',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    )
  }
}