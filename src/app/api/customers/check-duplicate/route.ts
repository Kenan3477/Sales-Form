import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'
import { withSecurity } from '@/lib/apiSecurity'
import { logSecurityEvent, createSecurityContext, sanitizeInput } from '@/lib/security'
import * as z from 'zod'

const customerLookupSchema = z.object({
  customerFirstName: z.string().min(1, 'First name is required'),
  customerLastName: z.string().min(1, 'Last name is required'),
  email: z.string().email('Valid email is required'),
  phoneNumber: z.string().min(1, 'Phone number is required')
})

interface DuplicateCheckResult {
  isDuplicate: boolean
  existingCustomer?: {
    id: string
    customerFirstName: string
    customerLastName: string
    email: string
    phoneNumber: string
    totalPlanCost: number
    createdAt: Date
    createdBy: {
      email: string
    }
  }
  duplicateReason?: string
  confidence?: 'HIGH' | 'MEDIUM' | 'LOW'
}

/**
 * Advanced customer duplicate detection with confidence scoring
 */
async function checkForDuplicate(customerData: {
  customerFirstName: string
  customerLastName: string
  email: string
  phoneNumber: string
}): Promise<DuplicateCheckResult> {
  const { customerFirstName, customerLastName, email, phoneNumber } = customerData

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
      createdAt: true,
      createdBy: {
        select: {
          email: true
        }
      }
    }
  })

  if (emailMatch) {
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
      createdAt: true,
      createdBy: {
        select: {
          email: true
        }
      }
    }
  })

  if (nameMatch) {
    // Check if emails have similar usernames or domains
    const currentEmailUser = normalizedEmail.split('@')[0]
    const currentEmailDomain = normalizedEmail.split('@')[1]
    const existingEmailUser = nameMatch.email.toLowerCase().split('@')[0]
    const existingEmailDomain = nameMatch.email.toLowerCase().split('@')[1]
    
    // High confidence if same domain and similar username
    if (currentEmailDomain === existingEmailDomain && 
        (currentEmailUser.includes(existingEmailUser) || existingEmailUser.includes(currentEmailUser))) {
      return {
        isDuplicate: true,
        existingCustomer: nameMatch,
        duplicateReason: 'Same name with similar email address',
        confidence: 'HIGH'
      }
    }

    // Medium confidence for same name with different email
    return {
      isDuplicate: true,
      existingCustomer: nameMatch,
      duplicateReason: 'Customer with same name already exists',
      confidence: 'MEDIUM'
    }
  }

  // Check for similar names (low confidence)
  const similarNameMatch = await prisma.sale.findFirst({
    where: {
      OR: [
        {
          AND: [
            { customerFirstName: { contains: normalizedFirstName, mode: 'insensitive' } },
            { customerLastName: { equals: normalizedLastName, mode: 'insensitive' } }
          ]
        },
        {
          AND: [
            { customerFirstName: { equals: normalizedFirstName, mode: 'insensitive' } },
            { customerLastName: { contains: normalizedLastName, mode: 'insensitive' } }
          ]
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
      createdAt: true,
      createdBy: {
        select: {
          email: true
        }
      }
    }
  })

  if (similarNameMatch) {
    return {
      isDuplicate: true,
      existingCustomer: similarNameMatch,
      duplicateReason: 'Similar customer name found',
      confidence: 'LOW'
    }
  }

  return {
    isDuplicate: false
  }
}

// POST - Check for customer duplicates
async function handleCustomerLookup(request: NextRequest, context: any) {
  const securityContext = createSecurityContext(request)
  const { user } = context

  try {
    const body = await request.json()
    
    logSecurityEvent('CUSTOMER_DUPLICATE_CHECK', securityContext, {
      userId: user.id,
      customerData: {
        firstName: body.customerFirstName,
        lastName: body.customerLastName,
        email: body.email?.substring(0, 5) + '***' // Partial email for privacy
      }
    })

    // Validate input
    const validation = customerLookupSchema.safeParse(body)
    if (!validation.success) {
      return NextResponse.json({
        error: 'Validation failed',
        details: validation.error.format()
      }, { status: 400 })
    }

    const duplicateCheck = await checkForDuplicate(validation.data)

    if (duplicateCheck.isDuplicate && duplicateCheck.existingCustomer) {
      logSecurityEvent('CUSTOMER_DUPLICATE_FOUND', securityContext, {
        userId: user.id,
        duplicateReason: duplicateCheck.duplicateReason,
        confidence: duplicateCheck.confidence,
        existingCustomerId: duplicateCheck.existingCustomer.id
      })

      return NextResponse.json({
        isDuplicate: true,
        customer: duplicateCheck.existingCustomer,
        reason: duplicateCheck.duplicateReason,
        confidence: duplicateCheck.confidence,
        message: getDuplicateMessage(duplicateCheck.duplicateReason, duplicateCheck.confidence)
      })
    }

    return NextResponse.json({
      isDuplicate: false,
      message: 'No duplicate customer found'
    })

  } catch (error) {
    logSecurityEvent('CUSTOMER_DUPLICATE_CHECK_ERROR', securityContext, {
      error: error instanceof Error ? error.message : 'Unknown error',
      userId: user.id
    })
    
    console.error('Customer duplicate check error:', error)
    return NextResponse.json(
      { error: 'Failed to check for duplicates' },
      { status: 500 }
    )
  }
}

function getDuplicateMessage(reason?: string, confidence?: string): string {
  const confidenceText = confidence === 'HIGH' ? 'Strong match' : 
                        confidence === 'MEDIUM' ? 'Possible match' : 
                        'Potential match'
  
  switch (reason) {
    case 'Email address already exists in the system':
      return `${confidenceText}: This email address is already registered`
    case 'Phone number already exists in the system':
      return `${confidenceText}: This phone number is already registered`
    case 'Same name with similar email address':
      return `${confidenceText}: Customer with same name and similar email found`
    case 'Customer with same name already exists':
      return `${confidenceText}: Customer with same name found`
    case 'Similar customer name found':
      return `${confidenceText}: Similar customer name found`
    default:
      return `${confidenceText}: Potential duplicate customer found`
  }
}

export const POST = withSecurity(handleCustomerLookup, {
  requireAuth: true,
  rateLimit: {
    requests: 100,
    windowMs: 60 * 60 * 1000
  },
  validateInput: true,
  logAccess: true
})