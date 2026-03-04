// Quick Gmail API setup for Hello@theflashteam.co.uk
// This bypasses SMTP port blocking while using your same Gmail account

import nodemailer from 'nodemailer';

export class QuickGmailService {
  // Use Gmail's OAuth2 with your existing app password as a workaround
  static async sendEmail(to: string, subject: string, html: string, attachments?: any[]) {
    try {
      // Try a direct Gmail API approach using Google's nodemailer OAuth2
      const transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
          type: 'OAuth2',
          user: process.env.EMAIL_USER,
          // We'll use service account or direct API calls
          pass: process.env.EMAIL_PASSWORD,
          clientId: process.env.GMAIL_CLIENT_ID,
          clientSecret: process.env.GMAIL_CLIENT_SECRET,
          refreshToken: process.env.GMAIL_REFRESH_TOKEN,
        },
      });

      const mailOptions = {
        from: `The Flash Team <${process.env.EMAIL_USER}>`,
        to,
        subject,
        html,
        attachments: attachments || []
      };

      const info = await transporter.sendMail(mailOptions);
      console.log('✅ Email sent via Gmail API:', info.messageId);
      
      return { success: true, messageId: info.messageId };
    } catch (error: any) {
      console.error('❌ Gmail API failed:', error.message);
      return { success: false, error: error.message };
    }
  }
}

// Alternative: Direct Gmail API without OAuth complexity
export class SimpleGmailAPI {
  static async sendEmail(to: string, subject: string, html: string, attachments?: any[]) {
    try {
      // Use Google's Gmail API directly
      const response = await fetch('https://www.googleapis.com/gmail/v1/users/me/messages/send', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.GOOGLE_ACCESS_TOKEN}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          raw: this.createEmailMessage(to, subject, html, attachments)
        })
      });

      if (response.ok) {
        const result = await response.json();
        return { success: true, messageId: result.id };
      } else {
        throw new Error(`Gmail API failed: ${response.status}`);
      }
    } catch (error: any) {
      return { success: false, error: error.message };
    }
  }

  private static createEmailMessage(to: string, subject: string, html: string, attachments?: any[]) {
    const boundary = 'boundary_' + Date.now();
    
    let email = [
      `To: ${to}`,
      `From: The Flash Team <Hello@theflashteam.co.uk>`,
      `Subject: ${subject}`,
      'MIME-Version: 1.0',
      `Content-Type: multipart/mixed; boundary="${boundary}"`,
      '',
      `--${boundary}`,
      'Content-Type: text/html; charset=utf-8',
      '',
      html,
      ''
    ];

    // Add attachments if any
    if (attachments && attachments.length > 0) {
      for (const attachment of attachments) {
        email = email.concat([
          `--${boundary}`,
          `Content-Type: ${attachment.contentType || 'application/octet-stream'}`,
          `Content-Disposition: attachment; filename="${attachment.filename}"`,
          'Content-Transfer-Encoding: base64',
          '',
          attachment.content.toString('base64'),
          ''
        ]);
      }
    }

    email.push(`--${boundary}--`);

    return Buffer.from(email.join('\r\n')).toString('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '');
  }
}