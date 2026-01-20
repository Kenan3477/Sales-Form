import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth/next'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'
import { isAdminRole } from '@/lib/apiSecurity'
import { sendSmsViaVoodoo, analyzePhoneNumber } from '@/lib/sms'

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    if (!session || !isAdminRole(session.user.role)) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { saleIds, confirm } = await request.json()

    if (!saleIds || !Array.isArray(saleIds) || saleIds.length === 0) {
      return NextResponse.json({ error: 'No sales selected' }, { status: 400 })
    }

    if (!confirm) {
      return NextResponse.json({ error: 'Confirmation required' }, { status: 400 })
    }

    // Fetch the selected sales
    const sales = await prisma.sale.findMany({
      where: {
        id: {
          in: saleIds
        }
      },
      include: {
        smsLogs: {
          orderBy: {
            createdAt: 'desc'
          },
          take: 1
        }
      }
    })

    const results: Array<{
      saleId: string
      customerName: string
      phoneNumber: string
      status: 'sent' | 'failed' | 'skipped'
      reason?: string
      messageId?: string
      error?: string
    }> = []

    let sentCount = 0
    let failedCount = 0
    let skippedCount = 0

    for (const sale of sales) {
      const customerName = `${sale.customerFirstName} ${sale.customerLastName}`
      const phoneAnalysis = analyzePhoneNumber(sale.phoneNumber)

      // Check if SMS can be sent
      if (!sale.phoneNumber || sale.phoneNumber.trim() === '') {
        results.push({
          saleId: sale.id,
          customerName,
          phoneNumber: sale.phoneNumber || 'N/A',
          status: 'skipped',
          reason: 'No phone number'
        })
        skippedCount++
        continue
      }

      if (!phoneAnalysis.canSendSMS || phoneAnalysis.type !== 'mobile') {
        results.push({
          saleId: sale.id,
          customerName,
          phoneNumber: sale.phoneNumber,
          status: 'skipped',
          reason: `Invalid number type: ${phoneAnalysis.type}`
        })
        skippedCount++
        continue
      }

      // Check if already sent
      const latestSms = sale.smsLogs[0]
      if (latestSms && latestSms.smsStatus === 'SENT') {
        results.push({
          saleId: sale.id,
          customerName,
          phoneNumber: sale.phoneNumber,
          status: 'skipped',
          reason: 'Already sent'
        })
        skippedCount++
        continue
      }

      // Prepare SMS message
      const message = `Hi ${sale.customerFirstName}, welcome to Flash Team! Your Protection Plan is now active. For support call 0330 822 7695. Reply STOP to opt out.`

      // Attempt to send SMS
      try {
        const smsResult = await sendSmsViaVoodoo({
          to: sale.phoneNumber,
          msg: message,
          external_reference: `sale-${sale.id}`
        })
        
        if (smsResult.success) {
          // Log successful SMS
          await prisma.sMSLog.create({
            data: {
              saleId: sale.id,
              phoneNumber: sale.phoneNumber,
              normalizedPhone: phoneAnalysis?.normalized || null,
              messageContent: message,
              smsStatus: 'SENT',
              smsSentAt: new Date(),
              smsProviderMessageId: smsResult.messageId || null,
              smsExternalReference: `sale-${sale.id}-${Date.now()}`
            }
          })

          results.push({
            saleId: sale.id,
            customerName,
            phoneNumber: sale.phoneNumber,
            status: 'sent',
            messageId: smsResult.messageId
          })
          sentCount++
        } else {
          // Log failed SMS
          await prisma.sMSLog.create({
            data: {
              saleId: sale.id,
              phoneNumber: sale.phoneNumber,
              normalizedPhone: phoneAnalysis?.normalized || null,
              messageContent: message,
              smsStatus: 'FAILED',
              smsError: smsResult.error || 'Unknown error',
              smsProviderMessageId: null,
              smsExternalReference: `sale-${sale.id}-${Date.now()}-failed`
            }
          })

          results.push({
            saleId: sale.id,
            customerName,
            phoneNumber: sale.phoneNumber,
            status: 'failed',
            error: smsResult.error
          })
          failedCount++
        }
      } catch (error) {
        console.error(`Error sending SMS to ${sale.phoneNumber}:`, error)
        
        // Log failed SMS
        await prisma.sMSLog.create({
          data: {
            saleId: sale.id,
            phoneNumber: sale.phoneNumber,
            normalizedPhone: phoneAnalysis?.normalized || null,
            messageContent: message,
            smsStatus: 'FAILED',
            smsError: error instanceof Error ? error.message : 'Unknown error',
            smsProviderMessageId: null,
            smsExternalReference: `sale-${sale.id}-${Date.now()}-error`
          }
        })

        results.push({
          saleId: sale.id,
          customerName,
          phoneNumber: sale.phoneNumber,
          status: 'failed',
          error: error instanceof Error ? error.message : 'Unknown error'
        })
        failedCount++
      }
    }

    const summary = {
      total: saleIds.length,
      sent: sentCount,
      failed: failedCount,
      skipped: skippedCount
    }

    return NextResponse.json({
      success: true,
      summary,
      details: results
    })

  } catch (error) {
    console.error('Error in SMS send endpoint:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}