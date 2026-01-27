'use client'

import { useState } from 'react'
import { Mail, CheckCircle, AlertCircle } from 'lucide-react'

export default function EmailTestSimple() {
  const [testEmail, setTestEmail] = useState('Ken@simpleemails.co.uk')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  const testEmailConfig = async () => {
    setLoading(true)
    setResult(null)

    try {
      const response = await fetch('/api/admin/emails-simple', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: 'test_email',
          testEmail
        }),
      })

      const data = await response.json()
      setResult(data)
    } catch (error) {
      console.error('Error testing email:', error)
      setResult({
        success: false,
        error: 'Failed to test email configuration'
      })
    } finally {
      setLoading(false)
    }
  }

  const getEmailConfig = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/admin/emails-simple')
      const data = await response.json()
      console.log('Email config:', data)
    } catch (error) {
      console.error('Error getting config:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container mx-auto p-6 max-w-2xl">
      <h1 className="text-2xl font-bold mb-6">Email System Test (Simplified)</h1>
      
      <div className="space-y-6">
        {/* Email Configuration Check */}
        <div className="bg-white p-6 rounded-lg shadow border">
          <h2 className="text-lg font-semibold mb-4 flex items-center">
            <Mail className="w-5 h-5 mr-2" />
            Email Configuration
          </h2>
          
          <button
            onClick={getEmailConfig}
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Checking...' : 'Check Configuration'}
          </button>
        </div>

        {/* Test Email */}
        <div className="bg-white p-6 rounded-lg shadow border">
          <h2 className="text-lg font-semibold mb-4 flex items-center">
            <Mail className="w-5 h-5 mr-2" />
            Send Test Email
          </h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Test Email Address
              </label>
              <input
                type="email"
                value={testEmail}
                onChange={(e) => setTestEmail(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter email address to test"
              />
            </div>
            
            <button
              onClick={testEmailConfig}
              disabled={loading || !testEmail}
              className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:opacity-50"
            >
              {loading ? 'Sending...' : 'Send Test Email'}
            </button>
          </div>
        </div>

        {/* Results */}
        {result && (
          <div className={`p-4 rounded-lg ${
            result.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
          }`}>
            <div className="flex items-center">
              {result.success ? (
                <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
              ) : (
                <AlertCircle className="w-5 h-5 text-red-600 mr-2" />
              )}
              <span className={`font-medium ${
                result.success ? 'text-green-800' : 'text-red-800'
              }`}>
                {result.success ? 'Success!' : 'Error'}
              </span>
            </div>
            
            {result.messageId && (
              <p className="text-green-700 text-sm mt-2">
                Message ID: {result.messageId}
              </p>
            )}
            
            {result.error && (
              <p className="text-red-700 text-sm mt-2">
                {result.error}
              </p>
            )}
          </div>
        )}

        {/* Setup Instructions */}
        <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
          <h3 className="font-medium text-yellow-800 mb-2">Setup Required</h3>
          <p className="text-yellow-700 text-sm">
            To use email functionality, you need to set EMAIL_PASSWORD in your .env file with your Gmail app password.
            <br />
            Current configuration: Hello@theflashteam.co.uk via Gmail SMTP
          </p>
        </div>
      </div>
    </div>
  )
}