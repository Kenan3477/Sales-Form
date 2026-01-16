import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '../../../../../lib/auth'
import { prisma } from '../../../../../lib/prisma'

export async function GET(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const searchParams = request.nextUrl.searchParams
    const dateFrom = searchParams.get('dateFrom')
    const dateTo = searchParams.get('dateTo')
    const agentFilter = searchParams.get('agent')
    const status = searchParams.get('status')

    let whereClause: any = {}

    // Date filters - default to today if no dates provided
    if (dateFrom || dateTo || (!dateFrom && !dateTo)) {
      whereClause.createdAt = {}
      
      if (dateFrom) {
        whereClause.createdAt.gte = new Date(dateFrom)
      } else {
        // Default to today
        const today = new Date()
        today.setHours(0, 0, 0, 0)
        whereClause.createdAt.gte = today
      }
      
      if (dateTo) {
        whereClause.createdAt.lte = new Date(dateTo + 'T23:59:59.999Z')
      } else if (!dateFrom) {
        // Default to end of today
        const today = new Date()
        today.setHours(23, 59, 59, 999)
        whereClause.createdAt.lte = today
      }
    }

    // Agent filter
    if (agentFilter) {
      whereClause.createdById = agentFilter
    }

    // Status filter (for completed sales, etc.)
    // Add your status logic here based on your business logic
    // For now, we'll assume all sales are valid for SMS

    const sales = await prisma.sale.findMany({
      where: whereClause,
      include: {
        createdBy: {
          select: {
            email: true,
            id: true
          }
        },
        smsLogs: {
          orderBy: { createdAt: 'desc' },
          take: 1 // Get latest SMS log for status
        }
      },
      orderBy: { createdAt: 'desc' }
    })

    // Format response with SMS status
    const salesWithSmsStatus = sales.map(sale => {
      const latestSms = sale.smsLogs[0]
      
      return {
        id: sale.id,
        createdAt: sale.createdAt,
        customerFirstName: sale.customerFirstName,
        customerLastName: sale.customerLastName,
        phoneNumber: sale.phoneNumber,
        email: sale.email,
        agentEmail: sale.createdBy.email,
        agentName: sale.agentName || sale.createdBy.email,
        totalPlanCost: sale.totalPlanCost,
        smsStatus: latestSms?.smsStatus || 'NOT_SENT',
        smsSentAt: latestSms?.smsSentAt,
        smsError: latestSms?.smsError,
        canSendSms: !latestSms || latestSms.smsStatus !== 'SENT' // Can send if never sent or failed
      }
    })

    // Get unique agents for filter dropdown
    const agents = await prisma.user.findMany({
      where: {
        role: { in: ['AGENT', 'ADMIN'] }
      },
      select: {
        id: true,
        email: true
      },
      orderBy: { email: 'asc' }
    })

    return NextResponse.json({
      sales: salesWithSmsStatus,
      agents
    })

  } catch (error) {
    console.error('Error fetching sales for SMS:', error)
    return NextResponse.json(
      { error: 'Failed to fetch sales data' },
      { status: 500 }
    )
  }
}