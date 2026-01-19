import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET(request: NextRequest) {
  try {
    // Get first 5 sales with their email data
    const sales = await prisma.sale.findMany({
      take: 5,
      orderBy: { createdAt: 'desc' },
      select: {
        id: true,
        customerFirstName: true,
        customerLastName: true,
        email: true,
        createdAt: true,
        createdBy: {
          select: {
            email: true
          }
        }
      }
    })

    const emailAnalysis = sales.map(sale => ({
      saleId: sale.id,
      customerName: `${sale.customerFirstName} ${sale.customerLastName}`,
      email: sale.email,
      emailType: typeof sale.email,
      emailLength: sale.email ? sale.email.length : 0,
      isPlaceholder: sale.email?.includes('placeholder') || sale.email?.includes('example') || sale.email?.includes('test') || sale.email?.includes('sample'),
      rawEmailValue: JSON.stringify(sale.email),
      createdAt: sale.createdAt,
      agentEmail: sale.createdBy?.email
    }))

    return NextResponse.json({
      success: true,
      totalSales: sales.length,
      emailAnalysis,
      summary: {
        hasPlaceholders: emailAnalysis.some(s => s.isPlaceholder),
        emptyEmails: emailAnalysis.filter(s => !s.email).length,
        placeholderCount: emailAnalysis.filter(s => s.isPlaceholder).length
      }
    })

  } catch (error) {
    console.error('Debug check emails error:', error)
    return NextResponse.json({ 
      success: false, 
      error: error instanceof Error ? error.message : 'Unknown error' 
    }, { status: 500 })
  }
}