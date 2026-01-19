import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET(request: NextRequest) {
  try {
    console.log('🧪 RAW EXPORT - Starting simple export without any deduplication...')
    
    // Get sales without any processing, just first 5
    const sales = await prisma.sale.findMany({
      take: 5,
      orderBy: { createdAt: 'desc' },
      include: {
        createdBy: {
          select: {
            email: true
          }
        },
        appliances: true
      }
    })

    console.log(`🧪 RAW EXPORT - Found ${sales.length} sales`)

    // Create simple CSV with just basic info
    const headers = ['Customer Name', 'Email From DB', 'Phone', 'Created Date', 'Raw Email Debug']
    
    const rows = sales.map(sale => {
      const emailDebug = {
        value: sale.email,
        type: typeof sale.email,
        isPlaceholder: sale.email?.includes('placeholder') || sale.email?.includes('example') || sale.email?.includes('test'),
        length: sale.email ? sale.email.length : 0
      }

      console.log(`🧪 RAW EXPORT - Sale ${sale.id}:`, {
        name: `${sale.customerFirstName} ${sale.customerLastName}`,
        email: sale.email,
        emailDebug
      })

      return [
        `${sale.customerFirstName} ${sale.customerLastName}`,
        sale.email || '[NO EMAIL]',
        sale.phoneNumber,
        new Date(sale.createdAt).toLocaleDateString(),
        JSON.stringify(emailDebug)
      ]
    })

    const csvContent = [headers, ...rows]
      .map(row => row.map(field => `"${field}"`).join(','))
      .join('\n')

    console.log('🧪 RAW EXPORT - CSV generated successfully')

    return new Response(csvContent, {
      headers: {
        'Content-Type': 'text/csv; charset=utf-8',
        'Content-Disposition': 'attachment; filename="raw-debug-export.csv"',
      },
    })

  } catch (error) {
    console.error('🧪 RAW EXPORT - Error:', error)
    return NextResponse.json({ 
      success: false, 
      error: error instanceof Error ? error.message : 'Unknown error' 
    }, { status: 500 })
  }
}