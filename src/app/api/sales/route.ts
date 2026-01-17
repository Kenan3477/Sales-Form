import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'
import { saleSchema } from '@/lib/schemas'
import { withSecurity } from '@/lib/apiSecurity'
import { logSecurityEvent, createSecurityContext, sanitizeInput } from '@/lib/security'

/**
 * Enhanced duplicate checking function for sales creation
 */
async function checkForSaleDuplicate(customerData: {
  customerFirstName: string
  customerLastName: string
  email: string
  phoneNumber: string
  accountNumber?: string
  totalPlanCost?: number
}): Promise<{
  isDuplicate: boolean
  existingCustomer?: any
  duplicateReason?: string
  confidence?: 'HIGH' | 'MEDIUM' | 'LOW'
}> {
  const { customerFirstName, customerLastName, email, phoneNumber, accountNumber, totalPlanCost } = customerData

  // Normalize inputs for comparison
  const normalizedFirstName = sanitizeInput(customerFirstName.trim().toLowerCase())
  const normalizedLastName = sanitizeInput(customerLastName.trim().toLowerCase())
  const normalizedEmail = sanitizeInput(email.trim().toLowerCase())
  const normalizedPhone = phoneNumber.replace(/[\s\-\(\)\+]/g, '')
  
  // Check for exact email match (highest confidence)
  const emailMatch = await prisma.sale.findFirst({
    where: {
      email: {
        equals: normalizedEmail,
        mode: 'insensitive'
      }
    },
    select: {
      id: true,
      customerFirstName: true,
      customerLastName: true,
      email: true,
      phoneNumber: true,
      totalPlanCost: true,
      accountNumber: true,
      createdAt: true,
      createdBy: {
        select: {
          email: true
        }
      }
    }
  })

  if (emailMatch) {
    // Check if it's exactly the same sale (including account and price)
    if (accountNumber && emailMatch.accountNumber === accountNumber && 
        totalPlanCost && Math.abs(emailMatch.totalPlanCost - totalPlanCost) < 0.01) {
      return {
        isDuplicate: true,
        existingCustomer: emailMatch,
        duplicateReason: 'Identical sale already exists (same customer, account, and price)',
        confidence: 'HIGH'
      }
    }

    return {
      isDuplicate: true,
      existingCustomer: emailMatch,
      duplicateReason: 'Email address already exists in the system',
      confidence: 'HIGH'
    }
  }

  // Check for phone number match (high confidence)
  const phoneQueries = [
    { phoneNumber: normalizedPhone },
    { phoneNumber: phoneNumber },
    // For UK numbers, check last 10 digits
    ...(normalizedPhone.length >= 10 ? [{ 
      phoneNumber: { 
        endsWith: normalizedPhone.slice(-10) 
      } 
    }] : [])
  ]

  const phoneMatch = await prisma.sale.findFirst({
    where: {
      OR: phoneQueries
    },
    select: {
      id: true,
      customerFirstName: true,
      customerLastName: true,
      email: true,
      phoneNumber: true,
      totalPlanCost: true,
      accountNumber: true,
      createdAt: true,
      createdBy: {
        select: {
          email: true
        }
      }
    }
  })

  if (phoneMatch) {
    return {
      isDuplicate: true,
      existingCustomer: phoneMatch,
      duplicateReason: 'Phone number already exists in the system',
      confidence: 'HIGH'
    }
  }

  // Check for full name match (medium confidence)
  const nameMatch = await prisma.sale.findFirst({
    where: {
      AND: [
        {
          customerFirstName: {
            equals: normalizedFirstName,
            mode: 'insensitive'
          }
        },
        {
          customerLastName: {
            equals: normalizedLastName,
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
      totalPlanCost: true,
      accountNumber: true,
      createdAt: true,
      createdBy: {
        select: {
          email: true
        }
      }
    }
  })

  if (nameMatch) {
    return {
      isDuplicate: true,
      existingCustomer: nameMatch,
      duplicateReason: 'Customer with same name already exists',
      confidence: 'MEDIUM'
    }
  }

  return {
    isDuplicate: false
  }
}

export async function POST(request: NextRequest) {
  const securityContext = createSecurityContext(request)
  let session: any = null
  
  try {
    // Add early database connectivity check
    console.log('Starting sale creation process...')
    
    session = await getServerSession(authOptions)
    console.log('Session obtained:', !!session)
    
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Test database connectivity early
    try {
      await prisma.$queryRaw`SELECT 1`
      console.log('Database connection test successful')
    } catch (dbError) {
      console.error('Database connection failed:', dbError)
      return NextResponse.json({ error: 'Database connection failed' }, { status: 500 })
    }

    const body = await request.json()
    console.log('Request body parsed successfully')
    
    logSecurityEvent('SALE_CREATION_ATTEMPT', securityContext, {
      userId: session.user.id,
      customerName: `${body.customerFirstName} ${body.customerLastName}`,
      hasIgnoreDuplicateFlag: !!body.ignoreDuplicateWarning
    })

    const validatedData = saleSchema.parse(body)

    // Calculate total cost
    let totalCost = 0
    
    if (validatedData.applianceCoverSelected) {
      totalCost += validatedData.appliances.reduce((sum: number, appliance: any) => sum + Number(appliance.cost), 0)
    }
    
    if (validatedData.boilerCoverSelected && validatedData.boilerPriceSelected) {
      totalCost += Number(validatedData.boilerPriceSelected)
    }

    // Enhanced duplicate checking unless explicitly overridden
    if (!body.ignoreDuplicateWarning) {
      const duplicateCheck = await checkForSaleDuplicate({
        customerFirstName: validatedData.customerFirstName,
        customerLastName: validatedData.customerLastName,
        email: validatedData.email,
        phoneNumber: validatedData.phoneNumber,
        accountNumber: validatedData.accountNumber,
        totalPlanCost: totalCost
      })

      if (duplicateCheck.isDuplicate) {
        logSecurityEvent('SALE_DUPLICATE_BLOCKED', securityContext, {
          userId: session.user.id,
          duplicateReason: duplicateCheck.duplicateReason,
          confidence: duplicateCheck.confidence,
          existingCustomerId: duplicateCheck.existingCustomer?.id
        })

        const errorMessage = duplicateCheck.confidence === 'HIGH' 
          ? `Duplicate customer detected: ${duplicateCheck.duplicateReason}`
          : `Potential duplicate: ${duplicateCheck.duplicateReason}`

        return NextResponse.json({ 
          error: errorMessage,
          isDuplicate: true,
          duplicateDetails: duplicateCheck.existingCustomer,
          confidence: duplicateCheck.confidence
        }, { status: 409 })
      }
    } else {
      logSecurityEvent('SALE_DUPLICATE_OVERRIDE', securityContext, {
        userId: session.user.id,
        customerName: `${validatedData.customerFirstName} ${validatedData.customerLastName}`
      })
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

    logSecurityEvent('SALE_CREATION_SUCCESS', securityContext, {
      userId: session.user.id,
      saleId: sale.id,
      totalCost,
      customerName: `${validatedData.customerFirstName} ${validatedData.customerLastName}`
    })

    return NextResponse.json(sale)
  } catch (error) {
    logSecurityEvent('SALE_CREATION_ERROR', securityContext, {
      error: error instanceof Error ? error.message : 'Unknown error',
      errorStack: error instanceof Error ? error.stack : undefined,
      userId: session?.user?.id
    })
    console.error('Error creating sale:', error)
    
    // More detailed error logging for production debugging
    if (error instanceof Error) {
      console.error('Error details:', {
        name: error.name,
        message: error.message,
        stack: error.stack,
        cause: error.cause
      })
    }
    
    return NextResponse.json({ 
      error: 'Internal server error',
      details: process.env.NODE_ENV === 'production' ? undefined : (error instanceof Error ? error.message : 'Unknown error')
    }, { status: 500 })
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