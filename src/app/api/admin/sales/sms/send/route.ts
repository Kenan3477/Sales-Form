import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '../../../../../../lib/auth'
import { sendSmsForSales } from '../../../../../../lib/sms'
import { prisma } from '../../../../../../lib/prisma'
import { withSecurity } from '../../../../../../lib/apiSecurity'
import { checkSMSRateLimit } from '../../../../../../lib/rateLimit'
import { logSecurityEvent, createSecurityContext, sanitizeInput } from '../../../../../../lib/security'

async function handleSMSSend(request: NextRequest, context: any) {
  const securityContext = createSecurityContext(request)
  const { user } = context
  
  try {
    console.log('SMS send request received')
    
    logSecurityEvent('SMS_SEND_ATTEMPT', securityContext, { 
      userId: user.id,
      userRole: user.role 
    })

    console.log('Processing SMS request for admin:', user.email)

    // Rate limit SMS sending per user
    const rateLimitResult = await checkSMSRateLimit(user.id)
    
    if (rateLimitResult.blocked) {
      logSecurityEvent('SMS_RATE_LIMIT_EXCEEDED', securityContext, { 
        userId: user.id,
        remaining: rateLimitResult.remaining 
      })
      return NextResponse.json(
        { error: 'SMS rate limit exceeded. Please try again later.' },
        { status: 429 }
      )
    }

    const body = await request.json()
    const { saleIds, confirm } = body

    console.log('SMS request body:', { saleIdsCount: saleIds?.length, confirm })

    if (!Array.isArray(saleIds) || saleIds.length === 0) {
      console.log('Invalid saleIds:', saleIds)
      logSecurityEvent('SMS_INVALID_REQUEST', securityContext, { 
        userId: user.id,
        error: 'Invalid saleIds'
      })
      return NextResponse.json(
        { error: 'Sale IDs are required' },
        { status: 400 }
      )
    }

    // Validate sale IDs (prevent injection attacks)
    const validSaleIds = saleIds.filter(id => 
      typeof id === 'string' && /^[a-zA-Z0-9\-_]+$/.test(sanitizeInput(id))
    )
    
    if (validSaleIds.length !== saleIds.length) {
      logSecurityEvent('SMS_INVALID_SALE_IDS', securityContext, { 
        userId: user.id,
        originalCount: saleIds.length,
        validCount: validSaleIds.length
      })
      return NextResponse.json(
        { error: 'Invalid sale ID format detected' },
        { status: 400 }
      )
    }

    if (!confirm) {
      console.log('Confirmation not provided')
      return NextResponse.json(
        { error: 'Confirmation required' },
        { status: 400 }
      )
    }

    // Check environment variables
    if (!process.env.VOODOO_API_KEY) {
      console.error('VOODOO_API_KEY not configured')
      return NextResponse.json(
        { error: 'SMS service not configured' },
        { status: 500 }
      )
    }

    console.log('Validating sales exist for IDs:', validSaleIds)

    // Validate sale IDs exist and get preview info
    const sales = await prisma.sale.findMany({
      where: {
        id: { in: validSaleIds }
      },
      include: {
        smsLogs: {
          orderBy: { createdAt: 'desc' },
          take: 1
        }
      }
    })

    console.log('Found sales:', sales.length, 'Expected:', validSaleIds.length)

    if (sales.length !== validSaleIds.length) {
      console.log('Sales count mismatch')
      logSecurityEvent('SMS_SALES_MISMATCH', securityContext, { 
        userId: user.id,
        expected: validSaleIds.length,
        found: sales.length
      })
      return NextResponse.json(
        { error: 'Some sales not found' },
        { status: 404 }
      )
    }

    // Send SMS messages
    console.log(`Admin ${user.email} sending SMS to ${validSaleIds.length} sales`)
    
    logSecurityEvent('SMS_SEND_INITIATED', securityContext, { 
      userId: user.id,
      saleCount: validSaleIds.length
    })
    
    try {
      const result = await sendSmsForSales(validSaleIds)

      console.log(`SMS batch complete:`, {
        total: validSaleIds.length,
        sent: result.sent,
        failed: result.failed,
        skipped: result.skipped,
        alreadySent: result.alreadySent
      })

      logSecurityEvent('SMS_SEND_COMPLETED', securityContext, { 
        userId: user.id,
        total: validSaleIds.length,
        sent: result.sent,
        failed: result.failed
      })

      return NextResponse.json({
        success: true,
        summary: {
          total: validSaleIds.length,
          sent: result.sent,
          failed: result.failed,
          skipped: result.skipped,
          alreadySent: result.alreadySent
        },
        details: result.results
      })
    } catch (smsError) {
      console.error('SMS processing error:', smsError)
      logSecurityEvent('SMS_SEND_ERROR', securityContext, { 
        userId: user.id,
        error: smsError instanceof Error ? smsError.message : 'Unknown error'
      })
      return NextResponse.json(
        { error: `SMS processing failed: ${smsError instanceof Error ? smsError.message : 'Unknown error'}` },
        { status: 500 }
      )
    }

  } catch (error) {
    console.error('SMS API endpoint error:', error)
    console.error('Error details:', {
      message: error instanceof Error ? error.message : 'Unknown error',
      stack: error instanceof Error ? error.stack : undefined,
      name: error instanceof Error ? error.name : typeof error
    })
    
    logSecurityEvent('SMS_API_ERROR', securityContext, { 
      userId: context?.user?.id,
      error: error instanceof Error ? error.message : 'Unknown error'
    })
    
    return NextResponse.json(
      { 
        error: 'Failed to send SMS messages',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    )
  }
}

// Secure SMS API endpoint with authentication and rate limiting
export const POST = withSecurity(handleSMSSend, {
  requireAuth: true,
  requireAdmin: true,
  rateLimit: {
    requests: 20,
    windowMs: 60 * 60 * 1000 // 20 SMS batches per hour
  },
  validateInput: true,
  logAccess: true
})