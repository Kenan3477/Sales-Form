import nodemailer from 'nodemailer'
import { prisma } from '@/lib/prisma'

export interface EmailSendResult {
  success: boolean
  messageId?: string
  error?: string
}

export class SimpleEmailService {
  private static createTransporter() {
    return nodemailer.createTransport({
      host: process.env.EMAIL_HOST,
      port: parseInt(process.env.EMAIL_PORT || '587'),
      secure: false,
      auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASSWORD,
      },
    })
  }

  static async sendDocumentEmail(documentId: string, saleId: string): Promise<EmailSendResult> {
    try {
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
        }
      })

      if (!sale) {
        return { success: false, error: 'Sale not found' }
      }

      if (!document) {
        return { success: false, error: 'Document not found' }
      }

      if (!sale.email) {
        return { success: false, error: 'Customer email not found' }
      }

      const customerName = `${sale.customerFirstName} ${sale.customerLastName}`
      const transporter = this.createTransporter()

      // Create download URL - we'll need to generate this
      const downloadUrl = `${process.env.NEXTAUTH_URL || 'http://localhost:3000'}/api/paperwork/download/${documentId}`

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
            
            <p>Thank you for choosing The Flash Team! Please find your sales document attached below.</p>
            
            <div style="background: #f3f4f6; padding: 20px; border-radius: 8px; margin: 20px 0;">
              <h3 style="margin: 0 0 10px 0; color: #374151;">Document Details:</h3>
              <p style="margin: 5px 0;"><strong>Document:</strong> ${document.filename}</p>
              <p style="margin: 5px 0;"><strong>Customer:</strong> ${customerName}</p>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
              <a href="${downloadUrl}" 
                 style="display: inline-block; background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold;">
                Download Your Document
              </a>
            </div>
            
            <p style="color: #6b7280; font-size: 14px; border-top: 1px solid #e5e7eb; padding-top: 20px; margin-top: 30px;">
              If you have any questions, please don't hesitate to contact us.<br>
              <strong>The Flash Team</strong><br>
              Email: Hello@theflashteam.co.uk
            </p>
          </div>
        `,
      }

      const info = await transporter.sendMail(mailOptions)
      
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

          if (!sale || !sale.email) {
            results.failedCustomers++
            results.errors.push(`Customer ${saleId}: No email address`)
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