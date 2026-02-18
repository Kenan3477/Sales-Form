import { Resend } from 'resend'

export interface WebEmailSendResult {
  success: boolean
  messageId?: string
  error?: string
}

export class WebEmailService {
  private static resend = process.env.RESEND_API_KEY ? new Resend(process.env.RESEND_API_KEY) : null

  static async sendEmail(
    to: string,
    subject: string,
    htmlContent: string,
    attachments?: Array<{
      filename: string
      content: Buffer
      contentType: string
    }>
  ): Promise<WebEmailSendResult> {
    try {
      if (!this.resend) {
        throw new Error('Resend API key not configured. Please set RESEND_API_KEY environment variable.')
      }

      console.log('🌐 Sending email via Resend web service...')
      console.log('To:', to)
      console.log('Subject:', subject)
      console.log('Has attachments:', attachments && attachments.length > 0 ? 'Yes' : 'No')

      // Convert Buffer attachments to Resend format
      const resendAttachments = attachments?.map(att => ({
        filename: att.filename,
        content: att.content,
      })) || []

      const result = await this.resend.emails.send({
        from: 'The Flash Team <onboarding@resend.dev>', // Resend verified domain
        to: [to],
        subject: subject,
        html: htmlContent,
        attachments: resendAttachments,
      })

      console.log('✅ Email sent successfully via Resend:', result.data?.id)

      return {
        success: true,
        messageId: result.data?.id || 'resend-unknown-id'
      }

    } catch (error) {
      console.error('❌ Resend email error:', error)
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown Resend error'
      }
    }
  }

  static async sendDocumentEmail(
    customerName: string,
    email: string,
    pdfContent: Buffer,
    filename: string
  ): Promise<WebEmailSendResult> {
    const htmlContent = `
      <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px 10px 0 0;">
          <h1 style="color: white; margin: 0; text-align: center; font-size: 28px;">The Flash Team</h1>
          <p style="color: #e2e8f0; text-align: center; margin: 10px 0 0 0; font-size: 16px;">Protection Plan Documentation</p>
        </div>
        
        <div style="background: #ffffff; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
          <h2 style="color: #2d3748; margin-bottom: 20px;">Hello ${customerName},</h2>
          
          <p style="color: #4a5568; font-size: 16px; line-height: 1.6;">
            Thank you for choosing The Flash Team for your protection plan. Your documentation is attached to this email.
          </p>
          
          <div style="background: #f7fafc; padding: 20px; border-radius: 8px; border-left: 4px solid #4299e1; margin: 25px 0;">
            <p style="color: #2d3748; margin: 0; font-weight: 600;">📋 What's Included:</p>
            <ul style="color: #4a5568; margin: 10px 0 0 0; padding-left: 20px;">
              <li>Complete protection plan details</li>
              <li>Coverage information</li>
              <li>Terms and conditions</li>
              <li>Contact information</li>
            </ul>
          </div>
          
          <p style="color: #4a5568; font-size: 16px; line-height: 1.6;">
            Please keep this documentation in a safe place for your records. If you have any questions about your coverage or need assistance, don't hesitate to contact us.
          </p>
          
          <div style="text-align: center; margin: 30px 0;">
            <p style="color: #4a5568; font-size: 14px; margin: 0;">
              <strong>Need Help?</strong><br>
              📧 Email: Hello@theflashteam.co.uk<br>
              📞 Phone: Contact us through your account
            </p>
          </div>
          
          <p style="color: #6b7280; font-size: 14px; border-top: 1px solid #e5e7eb; padding-top: 20px; margin-top: 30px;">
            If you have any questions, please don't hesitate to contact us.<br>
            <strong>The Flash Team</strong><br>
            Email: Hello@theflashteam.co.uk
          </p>
        </div>
      </div>
    `

    return this.sendEmail(email, 'Your Protection Plan Documentation - The Flash Team', htmlContent, [{
      filename,
      content: pdfContent,
      contentType: 'application/pdf'
    }])
  }

  static async sendTestEmail(testEmail: string): Promise<WebEmailSendResult> {
    const htmlContent = `
      <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #2563eb;">Email Configuration Test - Web Service</h2>
        <p>This is a test email to verify that your web-based email configuration is working correctly.</p>
        <p><strong>Sent at:</strong> ${new Date().toISOString()}</p>
        <p><strong>Method:</strong> Resend Web API (SMTP fallback)</p>
        <p>✅ If you received this email, your fallback email system is configured properly!</p>
        
        <div style="background: #f0f9ff; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #0ea5e9;">
          <p style="margin: 0; color: #0c4a6e;">
            <strong>Note:</strong> This email was sent using a web-based email service because SMTP connections 
            are blocked in the serverless environment. This is the recommended approach for production deployments.
          </p>
        </div>
      </div>
    `

    return this.sendEmail(testEmail, 'Email Configuration Test - The Flash Team (Web Service)', htmlContent)
  }
}