import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '../../../lib/auth'
import { prisma } from '../../../lib/prisma'

export async function GET(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Get first 5 sales to check their data
    const sales = await prisma.sale.findMany({
      take: 5,
      orderBy: {
        createdAt: 'desc'
      },
      select: {
        id: true,
        customerFirstName: true,
        customerLastName: true,
        title: true,
        email: true,
        mailingStreet: true,
        mailingCity: true,
        mailingProvince: true,
        mailingPostalCode: true,
        createdAt: true
      }
    })

    return NextResponse.json(sales)
  } catch (error) {
    console.error('Error checking sales data:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}