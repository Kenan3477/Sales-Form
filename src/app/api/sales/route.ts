import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'
import { saleSchema } from '@/lib/schemas'

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await request.json()
    const validatedData = saleSchema.parse(body)

    // Calculate total cost
    let totalCost = 0
    
    if (validatedData.applianceCoverSelected) {
      totalCost += validatedData.appliances.reduce((sum: number, appliance: any) => sum + Number(appliance.cost), 0)
    }
    
    if (validatedData.boilerCoverSelected && validatedData.boilerPriceSelected) {
      totalCost += Number(validatedData.boilerPriceSelected)
    }

    // Check for duplicate sale
    const duplicateSale = await prisma.sale.findFirst({
      where: {
        AND: [
          { customerFirstName: validatedData.customerFirstName },
          { customerLastName: validatedData.customerLastName },
          { email: validatedData.email },
          { phoneNumber: validatedData.phoneNumber },
          { accountNumber: validatedData.accountNumber },
          { totalPlanCost: totalCost }
        ]
      }
    })

    if (duplicateSale) {
      return NextResponse.json({ error: 'Already A Sale - A sale with the same customer details, account number, phone number, and price already exists.' }, { status: 400 })
    }

    // Create sale with appliances
    const sale = await prisma.sale.create({
      data: {
        customerFirstName: validatedData.customerFirstName,
        customerLastName: validatedData.customerLastName,
        title: validatedData.title,
        phoneNumber: validatedData.phoneNumber,
        email: validatedData.email,
        notes: validatedData.notes,
        mailingStreet: validatedData.mailingStreet,
        mailingCity: validatedData.mailingCity,
        mailingProvince: validatedData.mailingProvince,
        mailingPostalCode: validatedData.mailingPostalCode,
        accountName: validatedData.accountName,
        sortCode: validatedData.sortCode,
        accountNumber: validatedData.accountNumber,
        directDebitDate: new Date(validatedData.directDebitDate),
        applianceCoverSelected: validatedData.applianceCoverSelected,
        boilerCoverSelected: validatedData.boilerCoverSelected,
        boilerPriceSelected: validatedData.boilerPriceSelected,
        totalPlanCost: totalCost,
        agentName: (validatedData as any).agentName,
        createdById: (validatedData as any).agentId || session.user.id,
        appliances: {
          create: validatedData.appliances.map((appliance: any) => ({
            appliance: appliance.appliance,
            otherText: appliance.otherText,
            coverLimit: appliance.coverLimit,
            cost: appliance.cost,
          }))
        }
      },
      include: {
        appliances: true,
        createdBy: {
          select: {
            email: true,
          }
        }
      }
    })

    return NextResponse.json(sale)
  } catch (error) {
    console.error('Error creating sale:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

export async function GET(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const isAdmin = session.user.role === 'ADMIN'
    const searchParams = request.nextUrl.searchParams
    const agentFilter = searchParams.get('agent')
    const dateFrom = searchParams.get('dateFrom')
    const dateTo = searchParams.get('dateTo')

    let whereClause: any = {}

    // Non-admin users can only see their own sales
    if (!isAdmin) {
      whereClause.createdById = session.user.id
    } else if (agentFilter) {
      whereClause.createdById = agentFilter
    }

    // Date filters
    if (dateFrom || dateTo) {
      whereClause.createdAt = {}
      if (dateFrom) {
        whereClause.createdAt.gte = new Date(dateFrom)
      }
      if (dateTo) {
        whereClause.createdAt.lte = new Date(dateTo + 'T23:59:59.999Z')
      }
    }

    const sales = await prisma.sale.findMany({
      where: whereClause,
      include: {
        appliances: true,
        createdBy: {
          select: {
            id: true,
            email: true,
          }
        }
      },
      orderBy: {
        createdAt: 'desc'
      }
    })

    return NextResponse.json(sales)
  } catch (error) {
    console.error('Error fetching sales:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}