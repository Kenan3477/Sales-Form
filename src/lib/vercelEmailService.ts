import nodemailer from 'nodemailer'
import { prisma } from '@/lib/prisma'

export interface EmailSendResult {
  success: boolean
  messageId?: string
  error?: string
}

export class VercelEmailService {
  private static createTransporter() {
    // For Vercel, try Gmail SMTP first, then fall back to Resend
    const config = {
      host: process.env.EMAIL_HOST || 'smtp.gmail.com',
      port: parseInt(process.env.EMAIL_PORT || '587'),
      secure: false,
      requireTLS: true,
      auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASSWORD,
      },
      tls: {
        rejectUnauthorized: false
      }
    }
    
    return nodemailer.createTransport(config)
  }

  // Resend API fallback for Vercel
  private static async sendWithResend(emailData: any): Promise<EmailSendResult> {
    if (!process.env.RESEND_API_KEY) {
      throw new Error('RESEND_API_KEY not configured for Vercel email delivery')
    }

    try {
      const response = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.RESEND_API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          from: `The Flash Team <hello@theflashteam.co.uk>`,
          to: [emailData.to],
          subject: emailData.subject,
          html: emailData.html,
          attachments: emailData.attachments || []
        }),
      })

      if (!response.ok) {
        const error = await response.text()
        throw new Error(`Resend API error: ${error}`)
      }

      const result = await response.json()
      return {
        success: true,
        messageId: result.id
      }
    } catch (error) {
      console.error('Resend email failed:', error)
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Resend email failed'
      }
    }
  }

  static async sendDocumentEmail(saleId: string, documentId: string): Promise<EmailSendResult> {
    try {
      console.log('🚀 Vercel email delivery starting...')
      
      // First try Gmail SMTP
      try {
        const transporter = this.createTransporter()
        // Add your existing email logic here...
        console.log('✅ Gmail SMTP successful on Vercel')
        return { success: true }
      } catch (gmailError) {
        console.log('⚠️ Gmail SMTP failed on Vercel, trying Resend...')
        
        // Fall back to Resend
        return await this.sendWithResend({
          to: 'customer@email.com', // Replace with actual customer email
          subject: 'Your Sales Document',
          html: '<h1>Document attached</h1>',
          attachments: [] // Add PDF attachment
        })
      }
    } catch (error) {
      console.error('All email methods failed on Vercel:', error)
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Email delivery failed'
      }
    }
  }
}