import { google } from 'googleapis'
import { OAuth2Client } from 'google-auth-library'

export interface GmailSendResult {
  success: boolean
  messageId?: string
  error?: string
}

export class GmailAPIService {
  private static oAuth2Client: OAuth2Client

  private static async getOAuth2Client() {
    if (!this.oAuth2Client) {
      this.oAuth2Client = new google.auth.OAuth2(
        process.env.GMAIL_CLIENT_ID,
        process.env.GMAIL_CLIENT_SECRET,
        process.env.GMAIL_REDIRECT_URI || 'urn:ietf:wg:oauth:2.0:oob'
      )

      // Set the refresh token
      this.oAuth2Client.setCredentials({
        refresh_token: process.env.GMAIL_REFRESH_TOKEN
      })
    }

    return this.oAuth2Client
  }

  private static async createRawMessage(options: {
    to: string
    from: string
    subject: string
    text?: string
    html?: string
    attachments?: Array<{
      filename: string
      content: Buffer | string
      contentType?: string
    }>
  }) {
    const { to, from, subject, text, html, attachments } = options

    const boundary = `boundary_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    
    let message = [
      `To: ${to}`,
      `From: ${from}`,
      `Subject: ${subject}`,
      `MIME-Version: 1.0`,
      `Content-Type: multipart/mixed; boundary="${boundary}"`,
      '',
      `--${boundary}`,
      `Content-Type: multipart/alternative; boundary="alt_${boundary}"`,
      '',
      `--alt_${boundary}`,
      `Content-Type: text/plain; charset="UTF-8"`,
      '',
      text || (html ? html.replace(/<[^>]*>/g, '') : ''),
      ''
    ]

    if (html) {
      message = message.concat([
        `--alt_${boundary}`,
        `Content-Type: text/html; charset="UTF-8"`,
        '',
        html,
        '',
        `--alt_${boundary}--`,
        ''
      ])
    } else {
      message.push(`--alt_${boundary}--`, '')
    }

    // Add attachments if any
    if (attachments && attachments.length > 0) {
      for (const attachment of attachments) {
        const contentType = attachment.contentType || 'application/octet-stream'
        const content = Buffer.isBuffer(attachment.content) 
          ? attachment.content.toString('base64')
          : Buffer.from(attachment.content).toString('base64')

        message = message.concat([
          `--${boundary}`,
          `Content-Type: ${contentType}`,
          `Content-Disposition: attachment; filename="${attachment.filename}"`,
          `Content-Transfer-Encoding: base64`,
          '',
          content,
          ''
        ])
      }
    }

    message.push(`--${boundary}--`)

    return Buffer.from(message.join('\r\n')).toString('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '')
  }

  static async sendEmail(options: {
    to: string
    subject: string
    text?: string
    html?: string
    attachments?: Array<{
      filename: string
      content: Buffer | string
      contentType?: string
    }>
  }): Promise<GmailSendResult> {
    try {
      console.log('📧 Sending email via Gmail API to:', options.to)

      const auth = await this.getOAuth2Client()
      const gmail = google.gmail({ version: 'v1', auth })

      const raw = await this.createRawMessage({
        ...options,
        from: `The Flash Team <${process.env.EMAIL_USER || 'Hello@theflashteam.co.uk'}>`
      })

      const result = await gmail.users.messages.send({
        userId: 'me',
        requestBody: {
          raw
        }
      })

      console.log('✅ Email sent successfully via Gmail API:', result.data.id)
      
      return {
        success: true,
        messageId: result.data.id || undefined
      }
    } catch (error: any) {
      console.error('❌ Gmail API send failed:', error.message)
      
      // Check for specific OAuth errors
      if (error.message.includes('invalid_grant') || error.message.includes('Token has been expired')) {
        return {
          success: false,
          error: 'Gmail authorization expired. Please re-authenticate your Google account.'
        }
      }
      
      if (error.message.includes('insufficient authentication scopes')) {
        return {
          success: false,
          error: 'Gmail API requires additional permissions. Please re-authorize with Gmail scope.'
        }
      }

      return {
        success: false,
        error: `Gmail API error: ${error.message}`
      }
    }
  }

  static async sendDocumentEmail(
    customerName: string,
    recipientEmail: string,
    pdfContent: Buffer,
    filename: string
  ): Promise<GmailSendResult> {
    const subject = `Your Sales Document - ${filename.replace('.pdf', '')}`
    
    const htmlContent = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
          .header { background: #2563eb; color: white; padding: 20px; text-align: center; }
          .content { padding: 30px; max-width: 600px; margin: 0 auto; }
          .footer { background: #f8f9fa; padding: 20px; text-align: center; color: #666; }
          .button { 
            background: #2563eb; 
            color: white; 
            padding: 12px 30px; 
            text-decoration: none; 
            border-radius: 5px; 
            display: inline-block; 
            margin: 20px 0; 
          }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>The Flash Team</h1>
          <p>Your Trusted Home Services Partner</p>
        </div>
        
        <div class="content">
          <h2>Hello ${customerName},</h2>
          
          <p>Thank you for choosing The Flash Team for your home protection needs!</p>
          
          <p>Please find attached your personalized sales document. This contains all the important details about your coverage and our services.</p>
          
          <p><strong>Document:</strong> ${filename}</p>
          
          <p>If you have any questions about your coverage or need assistance, please don't hesitate to contact us:</p>
          
          <ul>
            <li><strong>Email:</strong> Hello@theflashteam.co.uk</li>
            <li><strong>Phone:</strong> [Your Phone Number]</li>
          </ul>
          
          <p>We appreciate your trust in The Flash Team and look forward to serving you.</p>
          
          <p>Best regards,<br>
          <strong>The Flash Team</strong><br>
          Your Home Protection Specialists</p>
        </div>
        
        <div class="footer">
          <p>&copy; ${new Date().getFullYear()} The Flash Team. All rights reserved.</p>
          <p>This email was sent from Hello@theflashteam.co.uk</p>
        </div>
      </body>
      </html>
    `

    return this.sendEmail({
      to: recipientEmail,
      subject,
      html: htmlContent,
      attachments: [{
        filename,
        content: pdfContent,
        contentType: 'application/pdf'
      }]
    })
  }
}