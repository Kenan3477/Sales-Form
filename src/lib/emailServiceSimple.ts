import nodemailer from 'nodemailer'
import { prisma } from '@/lib/prisma'

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
      host: process.env.EMAIL_HOST,
      port: parseInt(process.env.EMAIL_PORT || '587'),
      secure: false,
      auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASSWORD,
      },
    }
    
    console.log('Final transporter config:', JSON.stringify({
      ...config,
      auth: { ...config.auth, pass: '[REDACTED]' }
    }, null, 2))
    
    return nodemailer.createTransport(config)
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
      const transporter = this.createTransporter()

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
      
      const info = await transporter.sendMail(mailOptions)
      
      console.log(`Email sent successfully - MessageID: ${info.messageId}`)
      
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
      const transporter = this.createTransporter()

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

      const info = await transporter.sendMail(mailOptions)
      
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