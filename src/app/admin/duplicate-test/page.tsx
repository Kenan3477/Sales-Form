'use client'

import { useState } from 'react'

interface MatchResult {
  id: string
  customerFirstName: string
  customerLastName: string
  email: string | null
  phoneNumber: string
  totalPlanCost: number
  createdAt: string
  createdBy?: {
    email: string
  }
}

interface TestResults {
  success?: boolean
  error?: string
  testData?: {
    customerFirstName: string
    customerLastName: string
    phoneNumber: string
    normalizedPhone: string
    email: string
  }
  matches?: {
    phoneMatches: MatchResult[]
    emailMatches: MatchResult[]
    nameMatches: MatchResult[]
  }
  summary?: {
    phoneMatchCount: number
    emailMatchCount: number
    nameMatchCount: number
    wouldBlock: boolean
  }
}

export default function DuplicateTestPage() {
  const [testData, setTestData] = useState({
    customerFirstName: '',
    customerLastName: '',
    phoneNumber: '',
    email: ''
  })
  const [results, setResults] = useState<TestResults | null>(null)
  const [loading, setLoading] = useState(false)

  const handleTest = async () => {
    setLoading(true)
    setResults(null)
    
    try {
      const response = await fetch('/api/admin/test-duplicate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(testData)
      })
      
      const data = await response.json()
      setResults(data)
    } catch (error) {
      console.error('Test failed:', error)
      setResults({ error: 'Test failed' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">🔍 Duplicate Detection Test</h1>
      
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4">Test Customer Data</h2>
        
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium mb-1">First Name</label>
            <input
              type="text"
              className="w-full border rounded px-3 py-2"
              value={testData.customerFirstName}
              onChange={(e) => setTestData({...testData, customerFirstName: e.target.value})}
              placeholder="John"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Last Name</label>
            <input
              type="text"
              className="w-full border rounded px-3 py-2"
              value={testData.customerLastName}
              onChange={(e) => setTestData({...testData, customerLastName: e.target.value})}
              placeholder="Smith"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Phone Number</label>
            <input
              type="text"
              className="w-full border rounded px-3 py-2"
              value={testData.phoneNumber}
              onChange={(e) => setTestData({...testData, phoneNumber: e.target.value})}
              placeholder="01234567890"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <input
              type="email"
              className="w-full border rounded px-3 py-2"
              value={testData.email}
              onChange={(e) => setTestData({...testData, email: e.target.value})}
              placeholder="john.smith@email.com"
            />
          </div>
        </div>
        
        <button
          onClick={handleTest}
          disabled={loading || !testData.customerFirstName || !testData.customerLastName || !testData.phoneNumber}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-4 py-2 rounded"
        >
          {loading ? 'Testing...' : 'Test Duplicate Detection'}
        </button>
      </div>
      
      {results && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">🎯 Test Results</h2>
          
          {results.error ? (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              Error: {results.error}
            </div>
          ) : results.summary ? (
            <div className="space-y-4">
              {/* Summary */}
              <div className={`border-l-4 p-4 ${results.summary.wouldBlock ? 'border-red-500 bg-red-50' : 'border-green-500 bg-green-50'}`}>
                <h3 className="font-semibold">
                  {results.summary.wouldBlock ? '🚫 DUPLICATE DETECTED - Sale would be blocked' : '✅ NO DUPLICATES - Sale would be allowed'}
                </h3>
                <p className="text-sm mt-1">
                  Phone matches: {results.summary.phoneMatchCount} | 
                  Email matches: {results.summary.emailMatchCount} | 
                  Name matches: {results.summary.nameMatchCount}
                </p>
              </div>
              
              {/* Phone Matches */}
              {results.matches?.phoneMatches && results.matches.phoneMatches.length > 0 && (
                <div>
                  <h3 className="font-semibold text-red-600">📞 Phone Number Matches ({results.matches.phoneMatches.length})</h3>
                  <div className="mt-2 space-y-2">
                    {results.matches.phoneMatches.map((match, index) => (
                      <div key={index} className="bg-red-50 border border-red-200 rounded p-3">
                        <p><strong>Customer:</strong> {match.customerFirstName} {match.customerLastName}</p>
                        <p><strong>Email:</strong> {match.email}</p>
                        <p><strong>Phone:</strong> {match.phoneNumber}</p>
                        <p><strong>Total Cost:</strong> £{match.totalPlanCost}</p>
                        <p><strong>Created:</strong> {new Date(match.createdAt).toLocaleDateString()}</p>
                        <p><strong>Created By:</strong> {match.createdBy?.email}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {/* Email Matches */}
              {results.matches?.emailMatches && results.matches.emailMatches.length > 0 && (
                <div>
                  <h3 className="font-semibold text-orange-600">📧 Email Matches ({results.matches.emailMatches.length})</h3>
                  <div className="mt-2 space-y-2">
                    {results.matches.emailMatches.map((match, index) => (
                      <div key={index} className="bg-orange-50 border border-orange-200 rounded p-3">
                        <p><strong>Customer:</strong> {match.customerFirstName} {match.customerLastName}</p>
                        <p><strong>Email:</strong> {match.email}</p>
                        <p><strong>Phone:</strong> {match.phoneNumber}</p>
                        <p><strong>Total Cost:</strong> £{match.totalPlanCost}</p>
                        <p><strong>Created:</strong> {new Date(match.createdAt).toLocaleDateString()}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {/* Name Matches */}
              {results.matches?.nameMatches && results.matches.nameMatches.length > 0 && (
                <div>
                  <h3 className="font-semibold text-blue-600">👤 Name Matches ({results.matches.nameMatches.length})</h3>
                  <div className="mt-2 space-y-2">
                    {results.matches.nameMatches.map((match, index) => (
                      <div key={index} className="bg-blue-50 border border-blue-200 rounded p-3">
                        <p><strong>Customer:</strong> {match.customerFirstName} {match.customerLastName}</p>
                        <p><strong>Email:</strong> {match.email}</p>
                        <p><strong>Phone:</strong> {match.phoneNumber}</p>
                        <p><strong>Total Cost:</strong> £{match.totalPlanCost}</p>
                        <p><strong>Created:</strong> {new Date(match.createdAt).toLocaleDateString()}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : null}
        </div>
      )}
    </div>
  )
}