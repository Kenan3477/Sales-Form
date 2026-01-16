import { prisma } from './prisma'

export interface SMSSendResult {
  saleId: string
  phoneNumber: string
  status: 'sent' | 'failed' | 'skipped'
  reason?: string
  messageId?: string
}

export interface SMSBatchResult {
  sent: number
  failed: number
  skipped: number
  alreadySent: number
  results: SMSSendResult[]
}

/**
 * Normalize UK phone number to E.164 format (+447xxxxxxxxx)
 * Returns null if invalid
 */
export function normalizeUkNumber(raw: string): string | null {
  if (!raw || typeof raw !== 'string') return null
  
  // Remove all non-digit characters
  const cleaned = raw.replace(/\D/g, '')
  
  // Handle different UK number formats
  if (cleaned.startsWith('447') && cleaned.length === 13) {
    // +447xxxxxxxxx (already normalized)
    return '+' + cleaned
  } else if (cleaned.startsWith('0044') && cleaned.length === 14) {
    // 00447xxxxxxxxx
    return '+' + cleaned.slice(2)
  } else if (cleaned.startsWith('07') && cleaned.length === 11) {
    // 07xxxxxxxxx (UK mobile)
    return '+44' + cleaned.slice(1)
  } else if (cleaned.startsWith('7') && cleaned.length === 10) {
    // 7xxxxxxxxx (missing country code and leading 0)
    return '+447' + cleaned.slice(1)
  }
  
  return null
}

/**
 * Check if normalized number is a UK mobile (not landline)
 * UK mobile numbers start with +447 followed by 9 digits
 */
export function isUkMobile(e164: string): boolean {
  if (!e164 || typeof e164 !== 'string') return false
  
  // UK mobile: +447xxxxxxxxx (13 characters total)
  // First digit after +447 should be 1,2,3,4,5,6,7,8,9 (not 0)
  const ukMobileRegex = /^\+447[1-9]\d{8}$/
  return ukMobileRegex.test(e164)
}

/**
 * Build the exact SMS message content
 */
export function buildSmsMessage(): string {
  return "Thank you for choosing Flash, If you have any questions, Queries or need to make a Repair. Please call us on 03308227695 and We'll be with you in a Flash. Our Opening hours are 9-5 Monday-Friday."
}

/**
 * Generate unique external reference for SMS
 */
export function generateSmsReference(saleId: string, messageVersion = '1'): string {
  const timestamp = Date.now()
  return `flash_${saleId}_v${messageVersion}_${timestamp}`
}

/**
 * Send SMS via VOODOO SMS API
 */
export async function sendSmsViaVoodoo({
  to,
  from = process.env.VOODOO_FROM || 'Flash',
  msg,
  external_reference
}: {
  to: string
  from?: string
  msg: string
  external_reference: string
}): Promise<{ success: boolean; messageId?: string; error?: string }> {
  const apiKey = process.env.VOODOO_API_KEY
  if (!apiKey) {
    throw new Error('VOODOO_API_KEY not configured')
  }

  try {
    const response = await fetch('https://api.voodoosms.com/sendsms', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        to,
        from,
        msg,
        external_reference
      })
    })

    const responseData = await response.json()

    if (response.ok) {
      return {
        success: true,
        messageId: responseData.id || responseData.message_id
      }
    } else {
      return {
        success: false,
        error: `HTTP ${response.status}: ${JSON.stringify(responseData)}`
      }
    }
  } catch (error) {
    return {
      success: false,
      error: `Network error: ${error instanceof Error ? error.message : 'Unknown error'}`
    }
  }
}

/**
 * Send SMS with retry logic and exponential backoff
 */
async function sendSmsWithRetry({
  to,
  msg,
  external_reference,
  maxRetries = 3
}: {
  to: string
  msg: string
  external_reference: string
  maxRetries?: number
}): Promise<{ success: boolean; messageId?: string; error?: string }> {
  let lastError = ''
  
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    const result = await sendSmsViaVoodoo({ to, msg, external_reference })
    
    if (result.success) {
      return result
    }
    
    lastError = result.error || 'Unknown error'
    
    // Don't retry on 4xx errors (client errors)
    if (lastError.includes('HTTP 4')) {
      break
    }
    
    // Exponential backoff for retries
    if (attempt < maxRetries) {
      const delay = Math.pow(2, attempt) * 1000 // 2s, 4s, 8s
      await new Promise(resolve => setTimeout(resolve, delay))
    }
  }
  
  return { success: false, error: lastError }
}

/**
 * Process SMS sending for multiple sales with batching and concurrency control
 */
export async function sendSmsForSales(saleIds: string[]): Promise<SMSBatchResult> {
  const batchSize = 20
  const maxConcurrency = 3
  const results: SMSSendResult[] = []
  let sent = 0, failed = 0, skipped = 0, alreadySent = 0

  // Get sales with their current SMS status
  const sales = await prisma.sale.findMany({
    where: {
      id: { in: saleIds }
    },
    include: {
      smsLogs: {
        orderBy: { createdAt: 'desc' },
        take: 1
      }
    }
  })

  const message = buildSmsMessage()

  // Process in batches
  for (let i = 0; i < sales.length; i += batchSize) {
    const batch = sales.slice(i, i + batchSize)
    
    // Process batch with controlled concurrency
    const batchPromises = batch.map(async (sale) => {
      const existingSms = sale.smsLogs[0]
      
      // Check if already sent
      if (existingSms?.smsStatus === 'SENT') {
        alreadySent++
        return {
          saleId: sale.id,
          phoneNumber: sale.phoneNumber,
          status: 'skipped' as const,
          reason: 'Already sent'
        }
      }

      // Normalize phone number
      const normalized = normalizeUkNumber(sale.phoneNumber)
      if (!normalized) {
        skipped++
        await createSmsLog({
          saleId: sale.id,
          phoneNumber: sale.phoneNumber,
          normalizedPhone: null,
          messageContent: message,
          status: 'SKIPPED',
          error: 'Invalid phone number format'
        })
        return {
          saleId: sale.id,
          phoneNumber: sale.phoneNumber,
          status: 'skipped' as const,
          reason: 'Invalid phone number format'
        }
      }

      // Check if it's a UK mobile number
      if (!isUkMobile(normalized)) {
        skipped++
        await createSmsLog({
          saleId: sale.id,
          phoneNumber: sale.phoneNumber,
          normalizedPhone: normalized,
          messageContent: message,
          status: 'SKIPPED',
          error: 'Not a UK mobile number'
        })
        return {
          saleId: sale.id,
          phoneNumber: sale.phoneNumber,
          status: 'skipped' as const,
          reason: 'Not a UK mobile number'
        }
      }

      // Generate external reference
      const externalRef = generateSmsReference(sale.id)

      // Create SMS log with SENDING status (prevents duplicates)
      const smsLog = await createSmsLog({
        saleId: sale.id,
        phoneNumber: sale.phoneNumber,
        normalizedPhone: normalized,
        messageContent: message,
        status: 'SENDING',
        externalReference: externalRef
      })

      // Send SMS
      const smsResult = await sendSmsWithRetry({
        to: normalized,
        msg: message,
        external_reference: externalRef
      })

      if (smsResult.success) {
        sent++
        await updateSmsLog(smsLog.id, {
          status: 'SENT',
          sentAt: new Date(),
          providerMessageId: smsResult.messageId
        })
        return {
          saleId: sale.id,
          phoneNumber: sale.phoneNumber,
          status: 'sent' as const,
          messageId: smsResult.messageId
        }
      } else {
        failed++
        await updateSmsLog(smsLog.id, {
          status: 'FAILED',
          error: smsResult.error
        })
        return {
          saleId: sale.id,
          phoneNumber: sale.phoneNumber,
          status: 'failed' as const,
          reason: smsResult.error
        }
      }
    })

    // Process batch with concurrency limit
    const batchResults = await processConcurrent(batchPromises, maxConcurrency)
    results.push(...batchResults)
  }

  return {
    sent,
    failed, 
    skipped,
    alreadySent,
    results
  }
}

/**
 * Process promises with concurrency limit
 */
async function processConcurrent<T>(promises: Promise<T>[], limit: number): Promise<T[]> {
  const results: T[] = []
  
  for (let i = 0; i < promises.length; i += limit) {
    const batch = promises.slice(i, i + limit)
    const batchResults = await Promise.all(batch)
    results.push(...batchResults)
  }
  
  return results
}

/**
 * Create SMS log entry
 */
async function createSmsLog({
  saleId,
  phoneNumber,
  normalizedPhone,
  messageContent,
  status,
  error,
  externalReference
}: {
  saleId: string
  phoneNumber: string
  normalizedPhone: string | null
  messageContent: string
  status: 'NOT_SENT' | 'SENDING' | 'SENT' | 'FAILED' | 'SKIPPED'
  error?: string
  externalReference?: string
}) {
  const ref = externalReference || generateSmsReference(saleId)
  
  return await prisma.sMSLog.create({
    data: {
      saleId,
      phoneNumber,
      normalizedPhone,
      messageContent,
      smsStatus: status,
      smsError: error,
      smsExternalReference: ref
    }
  })
}

/**
 * Update SMS log entry
 */
async function updateSmsLog(
  id: string,
  update: {
    status?: 'SENT' | 'FAILED'
    sentAt?: Date
    providerMessageId?: string
    error?: string
  }
) {
  return await prisma.sMSLog.update({
    where: { id },
    data: {
      ...(update.status && { smsStatus: update.status }),
      ...(update.sentAt && { smsSentAt: update.sentAt }),
      ...(update.providerMessageId && { smsProviderMessageId: update.providerMessageId }),
      ...(update.error && { smsError: update.error })
    }
  })
}