import nodemailer from 'nodemailer'
import { prisma } from '@/lib/prisma'
import { WebEmailService } from './webEmailService'

export interface EmailSendResult {
  success: boolean
  messageId?: string
  error?: string
}

export class SimpleEmailService {
  private static createTransporter() {
    console.log('Creating transporter with configuration:')
    console.log('HOST:', process.env.EMAIL_HOST)
    console.log('PORT:', process.env.EMAIL_PORT)
    console.log('USER:', process.env.EMAIL_USER)
    console.log('PASSWORD length:', process.env.EMAIL_PASSWORD?.length)
    
    const config = {
      host: process.env.EMAIL_HOST || 'smtp.gmail.com',
      port: parseInt(process.env.EMAIL_PORT || '587'),
      secure: false,
      auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASSWORD,
      },
      // DNS and timeout configuration for serverless environments
      connectionTimeout: 60000, // 60 seconds
      greetingTimeout: 30000, // 30 seconds  
      socketTimeout: 60000, // 60 seconds
      // Serverless optimization
      pool: false,
      maxConnections: 1,
      maxMessages: 1,
    }
    
    console.log('Final transporter config:', JSON.stringify({
      ...config,
      auth: { ...config.auth, pass: '[REDACTED]' }
    }, null, 2))
    
    return nodemailer.createTransport(config)
  }

  // Fallback transporter using direct IP addresses if DNS fails
  private static createFallbackTransporter() {
    console.log('Creating fallback transporter with alternative configuration for serverless issues...')
    
    // Try alternative configuration for Vercel/serverless environments
    const config = {
      host: process.env.EMAIL_HOST || 'smtp.gmail.com',
      port: 465, // Use secure port instead of 587
      secure: true, // Use SSL
      auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASSWORD,
      },
      // Reduced timeouts for faster failure detection
      connectionTimeout: 30000, // 30 seconds
      greetingTimeout: 15000, // 15 seconds  
      socketTimeout: 30000, // 30 seconds
      pool: false,
      maxConnections: 1,
      maxMessages: 1,
      // More permissive TLS settings for serverless
      tls: {
        rejectUnauthorized: false,
        ciphers: 'SSLv3'
      }
    }
    
    console.log('Fallback transporter config created with port 465 (SSL):', config.host)
    return nodemailer.createTransport(config)
  }

  // Secondary fallback using port 25
  private static createSecondaryFallbackTransporter() {
    console.log('Creating secondary fallback transporter with port 25...')
    
    const config = {
      host: process.env.EMAIL_HOST || 'smtp.gmail.com',
      port: 25, // Standard SMTP port
      secure: false,
      auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASSWORD,
      },
      connectionTimeout: 20000, // 20 seconds
      greetingTimeout: 10000, // 10 seconds  
      socketTimeout: 20000, // 20 seconds
      pool: false,
      maxConnections: 1,
      maxMessages: 1,
      ignoreTLS: true, // Ignore TLS for port 25
    }
    
    console.log('Secondary fallback transporter config created with port 25')
    return nodemailer.createTransport(config)
  }

  // Alternative email service for when SMTP is completely blocked
  private static async sendViaWebAPI(mailOptions: any): Promise<any> {
    console.log('🌐 SMTP blocked - switching to web-based email service (Resend)...')
    
    try {
      // Extract customer name from email content or use a default
      let customerName = 'Valued Customer'
      if (mailOptions.html) {
        const nameMatch = mailOptions.html.match(/Hello ([^,<]+)/i)
        if (nameMatch) {
          customerName = nameMatch[1].trim()
        }
      }

      // Check if this is a document email with attachments
      if (mailOptions.attachments && mailOptions.attachments.length > 0) {
        const attachment = mailOptions.attachments[0]
        const result = await WebEmailService.sendDocumentEmail(
          customerName,
          mailOptions.to,
          attachment.content,
          attachment.filename
        )
        
        if (result.success) {
          console.log('✅ Document email sent successfully via web service')
          return { messageId: result.messageId }
        } else {
          throw new Error(`Web email service failed: ${result.error}`)
        }
      } else {
        // Test email or plain email
        const result = await WebEmailService.sendEmail(
          mailOptions.to,
          mailOptions.subject,
          mailOptions.html || mailOptions.text || 'Email sent via web service'
        )
        
        if (result.success) {
          console.log('✅ Email sent successfully via web service')
          return { messageId: result.messageId }
        } else {
          throw new Error(`Web email service failed: ${result.error}`)
        }
      }
    } catch (webError: any) {
      console.error('❌ Web email service also failed:', webError.message)
      
      // Provide helpful error message
      throw new Error(`
        All email delivery methods failed:
        
        SMTP Status: Blocked in serverless environment (ports 587, 465, 25 all failed)
        Web Service Status: ${webError.message}
        
        To fix this issue:
        1. Set up Resend API key in Vercel environment variables:
           - Go to Vercel Dashboard → Project Settings → Environment Variables
           - Add: RESEND_API_KEY = your_resend_api_key
           - Get free API key at: https://resend.com
        
        2. Alternative: Use SendGrid, Mailgun, or AWS SES
        
        Email that failed to send:
        - To: ${mailOptions.to}
        - Subject: ${mailOptions.subject}
        - Has attachments: ${mailOptions.attachments?.length > 0 ? 'Yes' : 'No'}
      `)
    }
  }

  static async sendDocumentEmail(documentId: string, saleId: string): Promise<EmailSendResult> {
    try {
      console.log(`Sending individual document email - Document ID: ${documentId}, Sale ID: ${saleId}`)
      const sale = await prisma.sale.findUnique({
        where: { id: saleId },
        select: {
          customerFirstName: true,
          customerLastName: true,
          email: true,
        }
      })

      const document = await prisma.generatedDocument.findUnique({
        where: { id: documentId },
        select: {
          filename: true,
          filePath: true,
          metadata: true,
          mimeType: true,
        }
      })

      if (!sale) {
        console.error(`Sale not found for ID: ${saleId}`)
        return { success: false, error: 'Sale not found' }
      }

      if (!sale.email || sale.email.trim() === '') {
        console.error(`Customer ${sale.customerFirstName} ${sale.customerLastName} has no email address`)
        return { success: false, error: `Customer ${sale.customerFirstName} ${sale.customerLastName} has no email address` }
      }

      if (!document) {
        console.error(`Document not found for ID: ${documentId}`)
        return { success: false, error: 'Document not found' }
      }

      console.log(`Document found - Filename: ${document.filename}, MimeType: ${document.mimeType}`)
      console.log(`Metadata exists: ${!!document.metadata}`)
      
      if (document.metadata && typeof document.metadata === 'object') {
        console.log(`Metadata type check passed`)
        console.log(`Has documentContent: ${'documentContent' in document.metadata}`)
        if ('documentContent' in document.metadata) {
          const docContent = document.metadata.documentContent as string
          console.log(`DocumentContent length: ${docContent?.length || 'null/undefined'}`)
        }
      }

      if (!sale.email) {
        return { success: false, error: 'Customer email not found' }
      }

      const customerName = `${sale.customerFirstName} ${sale.customerLastName}`
      
      // Try main transporter first, fallback if DNS issues
      let transporter = this.createTransporter()
      let usesFallback = false

      // Get PDF content from metadata
      let pdfContent: Buffer | null = null
      console.log(`Starting PDF content extraction...`)
      
      if (document.metadata && typeof document.metadata === 'object' && 'documentContent' in document.metadata) {
        console.log(`PDF extraction path 1: metadata and documentContent exist`)
        const documentContent = document.metadata.documentContent as string
        if (documentContent && document.mimeType === 'application/pdf') {
          console.log(`PDF extraction path 2: content exists and mimeType is PDF`)
          // PDF content is stored as base64 in metadata
          pdfContent = Buffer.from(documentContent, 'base64')
          console.log(`PDF Buffer created successfully - Size: ${pdfContent.length} bytes`)
        } else {
          console.log(`PDF extraction failed - Content: ${!!documentContent}, MimeType: ${document.mimeType}`)
        }
      } else {
        console.log(`PDF extraction failed - Metadata structure check failed`)
      }
      
      console.log(`Final PDF content status: ${pdfContent ? 'Available' : 'Not available'}`)
      console.log(`Attachments array will have ${pdfContent ? '1' : '0'} items`)

      const mailOptions = {
        from: {
          name: 'The Flash Team',
          address: process.env.EMAIL_USER || 'Hello@theflashteam.co.uk'
        },
        to: sale.email,
        subject: `Your Sales Document - ${document.filename}`,
        html: `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #2563eb;">Hello ${customerName},</h2>
            
            <p>Thank you for choosing The Flash Team! Please find your sales document attached to this email.</p>
            
            <div style="background: #f3f4f6; padding: 20px; border-radius: 8px; margin: 20px 0;">
              <h3 style="margin: 0 0 10px 0; color: #374151;">Document Details:</h3>
              <p style="margin: 5px 0;"><strong>Document:</strong> ${document.filename}</p>
              <p style="margin: 5px 0;"><strong>Customer:</strong> ${customerName}</p>
              <p style="margin: 5px 0;"><strong>Attached:</strong> PDF document</p>
            </div>
            
            <p style="color: #6b7280; font-size: 14px; border-top: 1px solid #e5e7eb; padding-top: 20px; margin-top: 30px;">
              If you have any questions, please don't hesitate to contact us.<br>
              <strong>The Flash Team</strong><br>
              Email: Hello@theflashteam.co.uk
            </p>
          </div>
        `,
        attachments: pdfContent ? [{
          filename: document.filename,
          content: pdfContent,
          contentType: 'application/pdf'
        }] : []
      }

      console.log(`Sending email to ${sale.email} with ${mailOptions.attachments.length} attachments`)
      
      let info
      let attemptCount = 0
      let lastError: any
      
      // Try multiple transporter configurations
      while (attemptCount < 3) {
        try {
          if (attemptCount === 0) {
            console.log('Attempt 1: Using primary transporter (port 587)')
            info = await transporter.sendMail(mailOptions)
          } else if (attemptCount === 1) {
            console.log('Attempt 2: Using fallback transporter (port 465, SSL)')
            transporter = this.createFallbackTransporter()
            usesFallback = true
            info = await transporter.sendMail(mailOptions)
          } else {
            console.log('Attempt 3: Using secondary fallback transporter (port 25)')
            transporter = this.createSecondaryFallbackTransporter()
            usesFallback = true
            info = await transporter.sendMail(mailOptions)
          }
          break // Success, exit the retry loop
        } catch (error: any) {
          lastError = error
          attemptCount++
          console.log(`Attempt ${attemptCount} failed:`, error.message)
          
          if (attemptCount >= 3) {
            console.error('All SMTP transporter attempts failed')
            // Try alternative delivery method as last resort
            try {
              await this.sendViaWebAPI(mailOptions)
              throw new Error('SMTP blocked - see logs for alternative email solution options')
            } catch (webApiError: any) {
              throw webApiError
            }
          }
          
          // Wait a bit before retrying
          await new Promise(resolve => setTimeout(resolve, 2000))
        }
      }
      
      if (!info) {
        throw new Error('Failed to send email: No response received from any transporter')
      }
      
      console.log(`Email sent successfully${usesFallback ? ' (using fallback)' : ''} - MessageID: ${info.messageId}`)
      
      // Log the email send to database
      await prisma.emailLog.create({
        data: {
          saleId: saleId,
          documentId: documentId,
          recipientEmail: sale.email,
          senderEmail: process.env.EMAIL_USER || 'Hello@theflashteam.co.uk',
          subject: `Your Sales Document - ${document.filename}`,
          emailType: 'document_delivery',
          status: 'SENT',
          sentAt: new Date(),
          metadata: {
            filename: document.filename,
            customerName: customerName,
            messageId: info.messageId,
            attachmentCount: pdfContent ? 1 : 0
          }
        }
      })
      
      console.log(`Email log entry created for document ${documentId}`)
      
      return {
        success: true,
        messageId: info.messageId
      }

    } catch (error) {
      console.error('Email sending error:', error)
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      }
    }
  }

  static async testEmail(testEmail: string): Promise<EmailSendResult> {
    try {
      let transporter = this.createTransporter()
      let usesFallback = false

      const mailOptions = {
        from: {
          name: 'The Flash Team',
          address: process.env.EMAIL_USER || 'Hello@theflashteam.co.uk'
        },
        to: testEmail,
        subject: 'Email Configuration Test - The Flash Team',
        html: `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #2563eb;">Email Configuration Test</h2>
            <p>This is a test email to verify that your email configuration is working correctly.</p>
            <p><strong>Sent at:</strong> ${new Date().toISOString()}</p>
            <p>If you received this email, your email system is configured properly!</p>
          </div>
        `,
      }

      let info
      let attemptCount = 0
      let lastError: any
      
      // Try multiple transporter configurations
      while (attemptCount < 3) {
        try {
          if (attemptCount === 0) {
            console.log('Test Email Attempt 1: Using primary transporter (port 587)')
            info = await transporter.sendMail(mailOptions)
          } else if (attemptCount === 1) {
            console.log('Test Email Attempt 2: Using fallback transporter (port 465, SSL)')
            transporter = this.createFallbackTransporter()
            usesFallback = true
            info = await transporter.sendMail(mailOptions)
          } else {
            console.log('Test Email Attempt 3: Using secondary fallback transporter (port 25)')
            transporter = this.createSecondaryFallbackTransporter()
            usesFallback = true
            info = await transporter.sendMail(mailOptions)
          }
          break // Success, exit the retry loop
        } catch (error: any) {
          lastError = error
          attemptCount++
          console.log(`Test Email Attempt ${attemptCount} failed:`, error.message)
          
          if (attemptCount >= 3) {
            console.error('All test email SMTP transporter attempts failed')
            // Try alternative delivery method as last resort
            try {
              await this.sendViaWebAPI(mailOptions)
              throw new Error('SMTP blocked for test email - see logs for alternative email solution options')
            } catch (webApiError: any) {
              throw webApiError
            }
          }
          
          // Wait a bit before retrying
          await new Promise(resolve => setTimeout(resolve, 2000))
        }
      }
      
      if (!info) {
        throw new Error('Failed to send test email: No response received from any transporter')
      }
      
      console.log(`Test email sent successfully${usesFallback ? ' (using fallback IP)' : ''} - MessageID: ${info.messageId}`)
      
      return {
        success: true,
        messageId: info.messageId
      }

    } catch (error) {
      console.error('Test email error:', error)
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      }
    }
  }

  static async bulkSendDocuments(saleIds: string[]): Promise<EmailSendResult & { details?: any }> {
    try {
      console.log('Starting bulk send for sale IDs:', saleIds)
      const results = {
        totalCustomers: 0,
        successfulCustomers: 0,
        failedCustomers: 0,
        totalDocuments: 0,
        successfulDocuments: 0,
        failedDocuments: 0,
        errors: [] as string[]
      }

      for (const saleId of saleIds) {
        try {
          console.log(`Processing sale ID: ${saleId}`)
          results.totalCustomers++

          // Get sale info
          const sale = await prisma.sale.findUnique({
            where: { id: saleId },
            select: {
              customerFirstName: true,
              customerLastName: true,
              email: true,
            }
          })

          if (!sale) {
            console.log(`Sale not found for ID: ${saleId}`)
            results.failedCustomers++
            results.errors.push(`Sale ID ${saleId}: Sale not found`)
            continue
          }

          console.log(`Found sale: ${sale.customerFirstName} ${sale.customerLastName}, email: '${sale.email}'`)

          if (!sale.email || sale.email.trim() === '') {
            console.log(`No email address for ${sale.customerFirstName} ${sale.customerLastName}`)
            results.failedCustomers++
            results.errors.push(`Customer ${sale.customerFirstName} ${sale.customerLastName}: No email address`)
            continue
          }

          // Get documents for this sale
          const documents = await prisma.generatedDocument.findMany({
            where: { 
              saleId: saleId,
              isDeleted: false 
            },
            select: {
              id: true,
              filename: true,
              filePath: true,
            }
          })

          if (documents.length === 0) {
            results.failedCustomers++
            results.errors.push(`Customer ${sale.customerFirstName} ${sale.customerLastName}: No documents`)
            continue
          }

          let customerSuccess = true
          
          // Send email for each document
          for (const document of documents) {
            results.totalDocuments++
            
            const emailResult = await this.sendDocumentEmail(document.id, saleId)
            
            if (emailResult.success) {
              results.successfulDocuments++
            } else {
              results.failedDocuments++
              results.errors.push(`Document ${document.filename}: ${emailResult.error}`)
              customerSuccess = false
            }
          }

          if (customerSuccess) {
            results.successfulCustomers++
          } else {
            results.failedCustomers++
          }

          // Small delay between customers
          await new Promise(resolve => setTimeout(resolve, 500))

        } catch (error) {
          results.failedCustomers++
          results.errors.push(`Customer ${saleId}: ${error instanceof Error ? error.message : 'Unknown error'}`)
        }
      }

      const success = results.failedCustomers === 0

      return {
        success,
        details: results,
        error: success ? undefined : `${results.failedCustomers} of ${results.totalCustomers} customers failed`
      }

    } catch (error) {
      console.error('Bulk email error:', error)
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      }
    }
  }
}