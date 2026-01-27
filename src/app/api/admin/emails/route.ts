import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { emailService } from '@/lib/emailService'

export async function POST(request: NextRequest) {
  try {
    // Check authentication
    const session = await getServerSession(authOptions)
    if (!session || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await request.json()
    const { action, ...data } = body

    switch (action) {
      case 'test':
        return handleTestEmail(data)
      
      case 'send_document':
        return handleSendDocument(data)
      
      case 'send_manual':
        return handleSendManual(data)
      
      case 'bulk_send':
        return handleBulkSend(data)
      
      default:
        return NextResponse.json({ error: 'Invalid action' }, { status: 400 })
    }

  } catch (error) {
    console.error('❌ Email API error:', error)
    return NextResponse.json({
      error: 'Email operation failed',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}

async function handleTestEmail(data: { testEmail?: string }) {
  const testEmail = data.testEmail || 'Ken@simpleemails.co.uk'
  
  console.log('🧪 Testing email configuration with:', testEmail)
  
  const result = await emailService.testEmailConfiguration(testEmail)
  
  if (result.success) {
    return NextResponse.json({
      success: true,
      message: `Test email sent successfully to ${testEmail}`,
      messageId: result.messageId,
      logId: result.logId
    })
  } else {
    return NextResponse.json({
      success: false,
      error: result.error
    }, { status: 500 })
  }
}

async function handleSendDocument(data: {
  saleId: string
  documentId: string
  customerEmail?: string
  customerName?: string
}) {
  const { saleId, documentId, customerEmail, customerName } = data
  
  if (!saleId || !documentId) {
    return NextResponse.json({ error: 'Sale ID and Document ID are required' }, { status: 400 })
  }

  // Get customer details if not provided
  const { prisma } = await import('@/lib/prisma')
  
  const sale = await prisma.sale.findUnique({
    where: { id: saleId },
    select: {
      customerFirstName: true,
      customerLastName: true,
      email: true
    }
  })

  if (!sale) {
    return NextResponse.json({ error: 'Sale not found' }, { status: 404 })
  }

  const finalEmail = customerEmail || sale.email
  const finalName = customerName || `${sale.customerFirstName} ${sale.customerLastName}`

  if (!finalEmail) {
    return NextResponse.json({ error: 'Customer email not available' }, { status: 400 })
  }

  console.log('📧 Sending document email to:', finalEmail)

  const result = await emailService.sendDocumentEmail(saleId, documentId, finalEmail, finalName)

  if (result.success) {
    return NextResponse.json({
      success: true,
      message: `Document sent successfully to ${finalEmail}`,
      messageId: result.messageId,
      logId: result.logId
    })
  } else {
    return NextResponse.json({
      success: false,
      error: result.error
    }, { status: 500 })
  }
}

async function handleSendManual(data: {
  to: string
  subject: string
  htmlContent: string
  textContent?: string
  saleId?: string
}) {
  const { to, subject, htmlContent, textContent, saleId } = data
  
  if (!to || !subject || !htmlContent) {
    return NextResponse.json({ error: 'Email recipient, subject, and content are required' }, { status: 400 })
  }

  console.log('📧 Sending manual email to:', to)

  const result = await emailService.sendEmail({
    to,
    subject,
    htmlContent,
    textContent,
    saleId,
    emailType: 'manual'
  })

  if (result.success) {
    return NextResponse.json({
      success: true,
      message: `Email sent successfully to ${to}`,
      messageId: result.messageId,
      logId: result.logId
    })
  } else {
    return NextResponse.json({
      success: false,
      error: result.error
    }, { status: 500 })
  }
}

async function handleBulkSend(data: {
  customerIds: string[]
  subject: string
  htmlContent: string
  textContent?: string
  includeDocuments?: boolean
}) {
  const { customerIds, subject, htmlContent, textContent, includeDocuments } = data
  
  if (!customerIds?.length || !subject || !htmlContent) {
    return NextResponse.json({ error: 'Customer IDs, subject, and content are required' }, { status: 400 })
  }

  console.log('📧 Sending bulk emails to:', customerIds.length, 'customers')

  const { prisma } = await import('@/lib/prisma')
  
  // Get customer details
  const sales = await prisma.sale.findMany({
    where: { id: { in: customerIds } },
    select: {
      id: true,
      customerFirstName: true,
      customerLastName: true,
      email: true,
      generatedDocuments: includeDocuments ? {
        where: { isDeleted: false },
        take: 1 // Just get the latest document
      } : false
    }
  })

  const results = {
    successful: 0,
    failed: 0,
    errors: [] as string[]
  }

  // Send emails to each customer
  for (const sale of sales) {
    if (!sale.email) {
      results.failed++
      results.errors.push(`No email for ${sale.customerFirstName} ${sale.customerLastName}`)
      continue
    }

    try {
      const customerName = `${sale.customerFirstName} ${sale.customerLastName}`
      
      const result = await emailService.sendEmail({
        to: sale.email,
        subject,
        htmlContent: htmlContent.replace(/\[Customer Name\]/g, customerName),
        textContent: textContent?.replace(/\[Customer Name\]/g, customerName),
        saleId: sale.id,
        emailType: 'bulk'
      })

      if (result.success) {
        results.successful++
      } else {
        results.failed++
        results.errors.push(`Failed to send to ${sale.email}: ${result.error}`)
      }

    } catch (error) {
      results.failed++
      results.errors.push(`Error sending to ${sale.email}: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  return NextResponse.json({
    success: true,
    message: `Bulk email completed. ${results.successful} sent, ${results.failed} failed.`,
    results
  })
}

export async function GET(request: NextRequest) {
  try {
    // Check authentication
    const session = await getServerSession(authOptions)
    if (!session || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { searchParams } = new URL(request.url)
    const action = searchParams.get('action')

    if (action === 'logs') {
      return handleGetEmailLogs(searchParams)
    } else if (action === 'templates') {
      return handleGetEmailTemplates()
    }

    return NextResponse.json({ error: 'Invalid action' }, { status: 400 })

  } catch (error) {
    console.error('❌ Email API GET error:', error)
    return NextResponse.json({
      error: 'Failed to fetch email data',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}

async function handleGetEmailLogs(searchParams: URLSearchParams) {
  const { prisma } = await import('@/lib/prisma')
  
  const page = parseInt(searchParams.get('page') || '1')
  const limit = parseInt(searchParams.get('limit') || '50')
  const skip = (page - 1) * limit

  const saleId = searchParams.get('saleId')
  const status = searchParams.get('status')

  const where: any = {}
  if (saleId) where.saleId = saleId
  if (status) where.status = status

  const [logs, total] = await Promise.all([
    prisma.emailLog.findMany({
      where,
      include: {
        sale: {
          select: {
            customerFirstName: true,
            customerLastName: true,
            email: true
          }
        },
        document: {
          select: {
            filename: true,
            template: {
              select: {
                name: true
              }
            }
          }
        }
      },
      orderBy: { createdAt: 'desc' },
      skip,
      take: limit
    }),
    prisma.emailLog.count({ where })
  ])

  return NextResponse.json({
    success: true,
    logs,
    pagination: {
      page,
      limit,
      total,
      pages: Math.ceil(total / limit)
    }
  })
}

async function handleGetEmailTemplates() {
  const { prisma } = await import('@/lib/prisma')
  
  const templates = await prisma.emailTemplate.findMany({
    where: { isActive: true },
    orderBy: { name: 'asc' }
  })

  return NextResponse.json({
    success: true,
    templates
  })
}