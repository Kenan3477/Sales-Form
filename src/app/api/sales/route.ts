import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'
import { saleSchema } from '@/lib/schemas'
import { withSecurity } from '@/lib/apiSecurity'
import { logSecurityEvent, createSecurityContext, sanitizeInput } from '@/lib/security'
import { z } from 'zod'

/**
 * Enhanced duplicate checking function for sales creation
 * Prioritizes phone number and name matching, with email as additional verification
 */
async function checkForSaleDuplicate(customerData: {
  customerFirstName: string
  customerLastName: string
  email?: string
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
  const normalizedEmail = email ? sanitizeInput(email.trim().toLowerCase()) : null
  const normalizedPhone = phoneNumber.replace(/[\s\-\(\)\+]/g, '')
  
  // 1. Check for exact phone number match (highest confidence for identification)
  const phoneMatch = await prisma.sale.findFirst({
    where: {
      phoneNumber: normalizedPhone
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
    // Check if names also match for higher confidence
    const phoneFirstMatch = phoneMatch.customerFirstName.toLowerCase() === normalizedFirstName
    const phoneLastMatch = phoneMatch.customerLastName.toLowerCase() === normalizedLastName
    
    if (phoneFirstMatch && phoneLastMatch) {
      // Check if it's exactly the same sale (including account and price)
      if (accountNumber && phoneMatch.accountNumber === accountNumber && 
          totalPlanCost && Math.abs(phoneMatch.totalPlanCost - totalPlanCost) < 0.01) {
        return {
          isDuplicate: true,
          existingCustomer: phoneMatch,
          duplicateReason: 'Identical sale already exists (same customer, phone, account, and price)',
          confidence: 'HIGH'
        }
      }

      return {
        isDuplicate: true,
        existingCustomer: phoneMatch,
        duplicateReason: `Exact match found: same phone number (${phoneNumber}) and name (${customerFirstName} ${customerLastName})`,
        confidence: 'HIGH'
      }
    } else {
      return {
        isDuplicate: true,
        existingCustomer: phoneMatch,
        duplicateReason: `Phone number match found (${phoneNumber}) but different name. Existing: ${phoneMatch.customerFirstName} ${phoneMatch.customerLastName}`,
        confidence: 'MEDIUM'
      }
    }
  }

  // 2. Check for exact email match if email is provided
  if (normalizedEmail) {
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
      // Check if names also match
      const emailFirstMatch = emailMatch.customerFirstName.toLowerCase() === normalizedFirstName
      const emailLastMatch = emailMatch.customerLastName.toLowerCase() === normalizedLastName
      
      if (emailFirstMatch && emailLastMatch) {
        // Check if it's exactly the same sale
        if (accountNumber && emailMatch.accountNumber === accountNumber && 
            totalPlanCost && Math.abs(emailMatch.totalPlanCost - totalPlanCost) < 0.01) {
          return {
            isDuplicate: true,
            existingCustomer: emailMatch,
            duplicateReason: 'Identical sale already exists (same customer, email, account, and price)',
            confidence: 'HIGH'
          }
        }

        return {
          isDuplicate: true,
          existingCustomer: emailMatch,
          duplicateReason: `Exact match found: same email (${email}) and name (${customerFirstName} ${customerLastName})`,
          confidence: 'HIGH'
        }
      } else {
        return {
          isDuplicate: true,
          existingCustomer: emailMatch,
          duplicateReason: `Email match found (${email}) but different name. Existing: ${emailMatch.customerFirstName} ${emailMatch.customerLastName}`,
          confidence: 'MEDIUM'
        }
      }
    }
  }

  // 3. Check for exact name match (lower confidence without phone/email match)
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
      duplicateReason: `Name match found: ${customerFirstName} ${customerLastName}. Please verify phone number and email to confirm if this is the same customer.`,
      confidence: 'LOW'
    }
  }

  // No duplicates found
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

    // Fetch field configurations for dynamic validation
    const fieldConfigurations = await prisma.fieldConfiguration.findMany()
    const fieldConfigMap = Object.fromEntries(
      fieldConfigurations.map(config => [config.fieldName, config.isRequired])
    )
    
    // Create dynamic schema based on field configuration
    const dynamicSaleSchema = saleSchema.merge(z.object({
      email: fieldConfigMap.email 
        ? z.string()
            .refine((val) => val === '' || z.string().email().safeParse(val).success, {
              message: 'Please enter a valid email address'
            })
        : z.string()
            .refine((val) => val === '' || z.string().email().safeParse(val).success, {
              message: 'Please enter a valid email address or leave empty'
            })
            .optional()
    }))

    const validatedData = dynamicSaleSchema.parse(body)

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
        email: validatedData.email || undefined, // Handle optional email
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
        email: validatedData.email || '', // Handle optional email
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
        stack: error.stack
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
    const planType = searchParams.get('planType')
    const applianceCount = searchParams.get('applianceCount')
    const hasBoilerCover = searchParams.get('hasBoilerCover')
    const status = searchParams.get('status')
    const directDebitDateFrom = searchParams.get('directDebitDateFrom')
    const directDebitDateTo = searchParams.get('directDebitDateTo')

    let whereClause: any = {}

    // Non-admin users can only see their own sales
    if (!isAdmin) {
      whereClause.createdById = session.user.id
    } else if (agentFilter) {
      // Filter by agent email - need to find the user with that email first
      const agent = await prisma.user.findFirst({
        where: { email: agentFilter },
        select: { id: true }
      })
      
      if (agent) {
        whereClause.createdById = agent.id
      } else {
        // If agent not found, return no results
        whereClause.createdById = 'non-existent-id'
      }
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

    // Plan type filter
    if (planType) {
      if (planType === 'appliance-only') {
        whereClause.applianceCoverSelected = true
        whereClause.boilerCoverSelected = false
      } else if (planType === 'boiler-only') {
        whereClause.applianceCoverSelected = false
        whereClause.boilerCoverSelected = true
      } else if (planType === 'both') {
        whereClause.applianceCoverSelected = true
        whereClause.boilerCoverSelected = true
      }
    }

    // Boiler cover filter
    if (hasBoilerCover) {
      whereClause.boilerCoverSelected = hasBoilerCover === 'yes'
    }

    // Status filter
    if (status && status !== 'all') {
      whereClause.status = status
    }

    // Direct debit date filters
    if (directDebitDateFrom || directDebitDateTo) {
      whereClause.directDebitDate = {}
      if (directDebitDateFrom) {
        whereClause.directDebitDate.gte = new Date(directDebitDateFrom)
      }
      if (directDebitDateTo) {
        whereClause.directDebitDate.lte = new Date(directDebitDateTo + 'T23:59:59.999Z')
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
        },
        emailLogs: {
          where: {
            status: 'SENT',
            emailType: 'document_delivery'
          },
          select: {
            id: true,
            recipientEmail: true,
            sentAt: true,
            documentId: true,
            document: {
              select: {
                id: true,
                filename: true
              }
            }
          },
          orderBy: {
            sentAt: 'desc'
          }
        }
      },
      orderBy: {
        createdAt: 'desc'
      }
    })

    // Filter by appliance count if specified
    let filteredSales = sales
    if (applianceCount) {
      filteredSales = sales.filter(sale => {
        const count = sale.appliances.length
        switch (applianceCount) {
          case '1':
            return count === 1
          case '2-3':
            return count >= 2 && count <= 3
          case '4-5':
            return count >= 4 && count <= 5
          case '6+':
            return count >= 6
          default:
            return true
        }
      })
    }

    return NextResponse.json(filteredSales)
  } catch (error) {
    console.error('Error fetching sales:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}