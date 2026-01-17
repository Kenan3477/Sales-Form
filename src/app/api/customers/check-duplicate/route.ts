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
  email: z.string().email('Valid email is required').optional().or(z.literal('')),
  phoneNumber: z.string().min(1, 'Phone number is required')
})

interface DuplicateCheckResult {
  isDuplicate: boolean
  existingCustomer?: {
    id: string
    customerFirstName: string
    customerLastName: string
    email: string | null
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
 * Prioritizes phone number and name matching, with email as additional verification
 */
async function checkForDuplicate(customerData: {
  customerFirstName: string
  customerLastName: string
  email?: string
  phoneNumber: string
}): Promise<DuplicateCheckResult> {
  const { customerFirstName, customerLastName, email, phoneNumber } = customerData

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

/**
 * Main handler for customer duplicate checking
 */
async function handleCustomerLookup(request: NextRequest): Promise<NextResponse> {
  const securityContext = createSecurityContext(request)

  try {
    const session = await getServerSession(authOptions)
    
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await request.json()
    
    // Validate the input data
    const validatedData = customerLookupSchema.parse(body)
    
    logSecurityEvent('DUPLICATE_CHECK_ATTEMPT', securityContext, {
      userId: session.user.id,
      customerName: `${validatedData.customerFirstName} ${validatedData.customerLastName}`,
      hasEmail: !!validatedData.email
    })

    // Perform duplicate check
    const duplicateResult = await checkForDuplicate({
      customerFirstName: validatedData.customerFirstName,
      customerLastName: validatedData.customerLastName,
      email: validatedData.email,
      phoneNumber: validatedData.phoneNumber
    })

    if (duplicateResult.isDuplicate) {
      logSecurityEvent('DUPLICATE_CUSTOMER_DETECTED', securityContext, {
        userId: session.user.id,
        duplicateConfidence: duplicateResult.confidence,
        duplicateReason: duplicateResult.duplicateReason,
        existingCustomerId: duplicateResult.existingCustomer?.id
      })
    }

    return NextResponse.json({
      isDuplicate: duplicateResult.isDuplicate,
      customer: duplicateResult.existingCustomer,
      reason: duplicateResult.duplicateReason,
      confidence: duplicateResult.confidence,
      message: duplicateResult.isDuplicate 
        ? formatDuplicateMessage(duplicateResult.duplicateReason || '', duplicateResult.confidence || 'LOW')
        : 'No duplicates found'
    })
  } catch (error) {
    logSecurityEvent('DUPLICATE_CHECK_ERROR', securityContext, {
      error: error instanceof Error ? error.message : 'Unknown error'
    })

    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      )
    }

    console.error('Error checking for duplicates:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

function formatDuplicateMessage(reason: string, confidence: 'HIGH' | 'MEDIUM' | 'LOW'): string {
  const confidenceText = confidence === 'HIGH' 
    ? 'High confidence'
    : confidence === 'MEDIUM' 
    ? 'Medium confidence'
    : 'Low confidence'

  // Return a user-friendly message based on the reason
  if (reason.includes('same phone number') && reason.includes('same') && reason.includes('name')) {
    return `${confidenceText}: This customer already exists with matching phone and name`
  }
  if (reason.includes('Phone number match') && reason.includes('different name')) {
    return `${confidenceText}: This phone number is registered to a different customer`
  }
  if (reason.includes('same email') && reason.includes('same') && reason.includes('name')) {
    return `${confidenceText}: This customer already exists with matching email and name`
  }
  if (reason.includes('Email match') && reason.includes('different name')) {
    return `${confidenceText}: This email is registered to a different customer`
  }
  if (reason.includes('Name match found')) {
    return `${confidenceText}: Customer with same name found - please verify contact details`
  }
  
  return `${confidenceText}: Potential duplicate customer found`
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