import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth/next'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'
import { analyzePhoneNumber } from '@/lib/sms'

export async function GET(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    if (!session || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { searchParams } = new URL(request.url)
    const dateFrom = searchParams.get('dateFrom')
    const dateTo = searchParams.get('dateTo')
    const agent = searchParams.get('agent')

    const whereClause: any = {}

    if (dateFrom || dateTo) {
      whereClause.createdAt = {}
      if (dateFrom) {
        whereClause.createdAt.gte = new Date(`${dateFrom}T00:00:00.000Z`)
      }
      if (dateTo) {
        whereClause.createdAt.lte = new Date(`${dateTo}T23:59:59.999Z`)
      }
    }

    if (agent) {
      whereClause.agentName = agent
    }

    const sales = await prisma.sale.findMany({
      where: whereClause,
      include: {
        smsLogs: true,
        createdBy: true,
      },
      orderBy: {
        createdAt: 'desc',
      },
    })

    // Get all unique agents for filter dropdown
    const agents = await prisma.sale.findMany({
      select: {
        agentName: true,
      },
      distinct: ['agentName'],
      where: {
        agentName: {
          not: null
        }
      },
      orderBy: {
        agentName: 'asc',
      },
    })

    // Process sales with comprehensive phone analysis
    const processedSales = sales.map(sale => {
      const phoneAnalysis = analyzePhoneNumber(sale.phoneNumber)
      const latestSms = sale.smsLogs[sale.smsLogs.length - 1]

      let smsStatus = 'NOT_SENT'
      let smsSentAt = null
      let smsError = null

      if (latestSms) {
        smsStatus = latestSms.smsStatus
        smsSentAt = latestSms.smsSentAt
        smsError = latestSms.smsError
      }

      return {
        id: sale.id,
        createdAt: sale.createdAt.toISOString(),
        customerFirstName: sale.customerFirstName,
        customerLastName: sale.customerLastName,
        phoneNumber: sale.phoneNumber,
        email: sale.email,
        agentEmail: sale.createdBy?.email || 'Unknown',
        agentName: sale.agentName,
        totalPlanCost: sale.totalPlanCost,
        smsStatus,
        smsSentAt,
        smsError,
        canSendSms: phoneAnalysis.canSendSMS && phoneAnalysis.type === 'mobile',
        phoneAnalysis: phoneAnalysis
      }
    })

    // Generate comprehensive phone number statistics
    const phoneStats = {
      total: processedSales.length,
      withPhoneNumbers: processedSales.filter(s => s.phoneNumber && s.phoneNumber.trim() !== '').length,
      validNumbers: processedSales.filter(s => s.phoneAnalysis.type !== 'invalid').length,
      mobileNumbers: processedSales.filter(s => s.phoneAnalysis.type === 'mobile').length,
      landlineNumbers: processedSales.filter(s => s.phoneAnalysis.type === 'landline').length,
      specialNumbers: processedSales.filter(s => s.phoneAnalysis.type === 'special').length,
      invalidNumbers: processedSales.filter(s => s.phoneAnalysis.type === 'invalid').length,
      smsCapable: processedSales.filter(s => s.canSendSms).length,
      nonSmsCapable: processedSales.filter(s => !s.canSendSms).length,
    }

    return NextResponse.json({
      sales: processedSales,
      agents: agents.map(a => ({
        id: a.agentName || 'Unknown',
        email: a.agentName || 'Unknown',
      })),
      phoneStats,
      smsCapableCustomers: processedSales.filter(sale => sale.canSendSms),
      summary: {
        totalCustomers: phoneStats.total,
        phoneNumberBreakdown: {
          mobile: phoneStats.mobileNumbers,
          landline: phoneStats.landlineNumbers,
          special: phoneStats.specialNumbers,
          invalid: phoneStats.invalidNumbers
        },
        smsCapability: {
          canSendSms: phoneStats.smsCapable,
          cannotSendSms: phoneStats.nonSmsCapable,
          percentage: phoneStats.total > 0 ? Math.round((phoneStats.smsCapable / phoneStats.total) * 100) : 0
        }
      }
    })
  } catch (error) {
    console.error('Error fetching sales for SMS:', error)
    return NextResponse.json(
      { error: 'Failed to fetch sales data' },
      { status: 500 }
    )
  }
}
