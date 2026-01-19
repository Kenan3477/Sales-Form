import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET(request: NextRequest) {
  try {
    console.log('🔍 MARGOT DEBUG - Searching for Margot Maitland in sales database...')

    // Search for Margot Maitland in the database
    const margotSales = await prisma.sale.findMany({
      where: {
        OR: [
          {
            customerFirstName: {
              contains: 'Margot',
              mode: 'insensitive'
            }
          },
          {
            customerFirstName: {
              contains: 'margot',
              mode: 'insensitive'
            }
          },
          {
            customerLastName: {
              contains: 'Maitland', 
              mode: 'insensitive'
            }
          },
          {
            customerLastName: {
              contains: 'maitland',
              mode: 'insensitive'
            }
          }
        ]
      },
      select: {
        id: true,
        customerFirstName: true,
        customerLastName: true,
        email: true,
        phoneNumber: true,
        accountNumber: true,
        createdAt: true,
        createdBy: {
          select: {
            email: true
          }
        }
      }
    })

    console.log(`🔍 MARGOT DEBUG - Found ${margotSales.length} Margot/Maitland sales`)

    const analysis = margotSales.map(sale => {
      const fullName = `${sale.customerFirstName} ${sale.customerLastName}`.toLowerCase().trim()
      return {
        saleId: sale.id,
        customerName: `${sale.customerFirstName} ${sale.customerLastName}`,
        email: sale.email,
        phoneNumber: sale.phoneNumber,
        accountNumber: sale.accountNumber,
        normalizedName: fullName,
        containsMargot: fullName.includes('margot'),
        containsMaitland: fullName.includes('maitland'),
        isBothMargotAndMaitland: fullName.includes('margot') && fullName.includes('maitland'),
        createdAt: sale.createdAt,
        agentEmail: sale.createdBy?.email
      }
    })

    return NextResponse.json({
      success: true,
      totalMargotSales: margotSales.length,
      margotAnalysis: analysis,
      searchTermsUsed: ['Margot', 'margot', 'Maitland', 'maitland'],
      summary: {
        exactMargotMaitland: analysis.filter(s => s.isBothMargotAndMaitland).length,
        onlyMargot: analysis.filter(s => s.containsMargot && !s.containsMaitland).length,
        onlyMaitland: analysis.filter(s => !s.containsMargot && s.containsMaitland).length
      }
    })

  } catch (error) {
    console.error('🔍 MARGOT DEBUG - Error:', error)
    return NextResponse.json({ 
      success: false, 
      error: error instanceof Error ? error.message : 'Unknown error' 
    }, { status: 500 })
  }
}