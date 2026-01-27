'use client'

import { useState } from 'react'
import { useSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'

interface EmailResult {
  success: boolean
  message?: string
  error?: string
  messageId?: string
  logId?: string
}

export default function EmailTestPage() {
  const { data: session, status } = useSession()
  const router = useRouter()

  const [testEmail, setTestEmail] = useState('Ken@simpleemails.co.uk')
  const [isTestingSending, setIsTestingSending] = useState(false)
  const [emailResult, setEmailResult] = useState<EmailResult | null>(null)

  const [manualEmail, setManualEmail] = useState({
    to: '',
    subject: '',
    content: ''
  })
  const [isSendingManual, setIsSendingManual] = useState(false)
  const [manualResult, setManualResult] = useState<EmailResult | null>(null)

  // Authentication check
  if (status === 'loading') {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>
  }

  if (!session || session.user.role !== 'ADMIN') {
    router.push('/auth/login')
    return null
  }

  const handleTestEmail = async () => {
    setIsTestingSending(true)
    setEmailResult(null)

    try {
      const response = await fetch('/api/admin/emails', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'test',
          testEmail
        })
      })

      const result = await response.json()
      setEmailResult(result)

    } catch (error) {
      setEmailResult({
        success: false,
        error: 'Network error occurred'
      })
    } finally {
      setIsTestingSending(false)
    }
  }

  const handleSendManual = async () => {
    if (!manualEmail.to || !manualEmail.subject || !manualEmail.content) {
      setManualResult({
        success: false,
        error: 'All fields are required'
      })
      return
    }

    setIsSendingManual(true)
    setManualResult(null)

    try {
      const response = await fetch('/api/admin/emails', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'send_manual',
          to: manualEmail.to,
          subject: manualEmail.subject,
          htmlContent: `
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
              <div style="background: #1f2937; color: white; padding: 20px; text-align: center;">
                <h1>🏠 The Flash Team</h1>
                <p>Your Home Protection Specialists</p>
              </div>
              <div style="padding: 30px 20px; background: #f9f9f9;">
                ${manualEmail.content.replace(/\n/g, '<br>')}
              </div>
              <div style="padding: 20px; text-align: center; background: #f1f1f1; font-size: 12px;">
                <p>© 2026 The Flash Team. All rights reserved.</p>
                <p>📧 Hello@theflashteam.co.uk</p>
              </div>
            </div>
          `,
          textContent: manualEmail.content
        })
      })

      const result = await response.json()
      setManualResult(result)

      if (result.success) {
        setManualEmail({ to: '', subject: '', content: '' })
      }

    } catch (error) {
      setManualResult({
        success: false,
        error: 'Network error occurred'
      })
    } finally {
      setIsSendingManual(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <button
                onClick={() => router.back()}
                className="inline-flex items-center px-3 py-2 text-sm leading-4 font-medium rounded-md text-gray-500 hover:text-gray-700 focus:outline-none transition ease-in-out duration-150"
              >
                ← Back
              </button>
              <div className="ml-6">
                <h1 className="text-xl font-semibold text-gray-900">📧 Email System Test</h1>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto py-8 px-4 space-y-8">
        
        {/* Email Configuration Test */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">🧪 Test Email Configuration</h2>
          <p className="text-sm text-gray-600 mb-4">
            Test if emails can be sent from Hello@theflashteam.co.uk
          </p>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Test Email Address</label>
              <input
                type="email"
                value={testEmail}
                onChange={(e) => setTestEmail(e.target.value)}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="Ken@simpleemails.co.uk"
              />
            </div>
            
            <button
              onClick={handleTestEmail}
              disabled={isTestingSending || !testEmail}
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isTestingSending ? '🔄 Sending...' : '📧 Send Test Email'}
            </button>

            {emailResult && (
              <div className={`p-4 rounded-md ${emailResult.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
                {emailResult.success ? (
                  <div className="text-green-800">
                    <h4 className="font-medium">✅ Test Email Sent Successfully!</h4>
                    <p className="text-sm mt-1">{emailResult.message}</p>
                    {emailResult.messageId && (
                      <p className="text-xs mt-1">Message ID: {emailResult.messageId}</p>
                    )}
                  </div>
                ) : (
                  <div className="text-red-800">
                    <h4 className="font-medium">❌ Test Email Failed</h4>
                    <p className="text-sm mt-1">{emailResult.error}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Manual Email Sending */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">✍️ Send Manual Email</h2>
          <p className="text-sm text-gray-600 mb-4">
            Send a custom email from your business account
          </p>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Recipient Email</label>
              <input
                type="email"
                value={manualEmail.to}
                onChange={(e) => setManualEmail({...manualEmail, to: e.target.value})}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="customer@example.com"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700">Subject</label>
              <input
                type="text"
                value={manualEmail.subject}
                onChange={(e) => setManualEmail({...manualEmail, subject: e.target.value})}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="Your Documents from The Flash Team"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700">Message Content</label>
              <textarea
                value={manualEmail.content}
                onChange={(e) => setManualEmail({...manualEmail, content: e.target.value})}
                rows={6}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="Dear Customer,

Thank you for choosing The Flash Team...

Best regards,
The Flash Team"
              />
            </div>
            
            <button
              onClick={handleSendManual}
              disabled={isSendingManual || !manualEmail.to || !manualEmail.subject || !manualEmail.content}
              className="inline-flex items-center px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSendingManual ? '🔄 Sending...' : '📤 Send Email'}
            </button>

            {manualResult && (
              <div className={`p-4 rounded-md ${manualResult.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
                {manualResult.success ? (
                  <div className="text-green-800">
                    <h4 className="font-medium">✅ Email Sent Successfully!</h4>
                    <p className="text-sm mt-1">{manualResult.message}</p>
                    {manualResult.messageId && (
                      <p className="text-xs mt-1">Message ID: {manualResult.messageId}</p>
                    )}
                  </div>
                ) : (
                  <div className="text-red-800">
                    <h4 className="font-medium">❌ Email Send Failed</h4>
                    <p className="text-sm mt-1">{manualResult.error}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Setup Instructions */}
        <div className="bg-blue-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-3">⚙️ Email Setup Instructions</h3>
          <div className="text-blue-800 text-sm space-y-2">
            <p><strong>Step 1:</strong> Add these environment variables to your .env file:</p>
            <div className="bg-blue-100 p-3 rounded font-mono text-xs">
              EMAIL_HOST=smtp.gmail.com<br/>
              EMAIL_PORT=587<br/>
              EMAIL_USER=Hello@theflashteam.co.uk<br/>
              EMAIL_PASSWORD=your_app_specific_password
            </div>
            <p><strong>Step 2:</strong> For Gmail, create an App Password at: <a href="https://myaccount.google.com/apppasswords" target="_blank" className="underline">myaccount.google.com/apppasswords</a></p>
            <p><strong>Step 3:</strong> Test the configuration using the test form above</p>
            <p><strong>Step 4:</strong> Once working, emails will be sent automatically when documents are generated</p>
          </div>
        </div>

      </div>
    </div>
  )
}