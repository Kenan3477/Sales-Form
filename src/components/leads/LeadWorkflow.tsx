'use client'

import { useState, useEffect } from 'react'
import { useSession } from 'next-auth/react'

interface Lead {
  id: string
  customerFirstName: string
  customerLastName: string
  phoneNumber: string
  email: string
  totalPlanCost: number
  applianceCoverSelected: boolean
  boilerCoverSelected: boolean
  boilerPriceSelected?: number
  appliances: Array<{
    applianceType: string
    brand?: string
    model?: string
    price: number
  }>
  timesContacted: number
  dispositionHistory: Array<{
    status: string
    notes?: string
    createdAt: string
  }>
}

interface LeadStats {
  totalAssigned: number
  newLeads: number
  callbacksDue: number
  callbacksScheduled: number
  noAnswers: number
  totalContacted: number
}

export default function LeadWorkflow() {
  const { data: session } = useSession()
  const [currentLead, setCurrentLead] = useState<Lead | null>(null)
  const [stats, setStats] = useState<LeadStats | null>(null)
  const [loading, setLoading] = useState(false)
  const [disposing, setDisposing] = useState(false)
  const [disposition, setDisposition] = useState('')
  const [notes, setNotes] = useState('')
  const [callbackDate, setCallbackDate] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  // Load stats on mount
  useEffect(() => {
    if (session?.user?.role === 'AGENT' || session?.user?.role === 'ADMIN') {
      loadStats()
    }
  }, [session])

  const loadStats = async () => {
    try {
      const response = await fetch('/api/leads/stats')
      if (response.ok) {
        const data = await response.json()
        setStats(data)
      }
    } catch (error) {
      console.error('Failed to load stats:', error)
    }
  }

  const startSelling = async () => {
    setLoading(true)
    setError(null)
    setSuccess(null)

    try {
      const response = await fetch('/api/leads/next')
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Failed to get next lead')
      }

      if (data.lead) {
        setCurrentLead(data.lead)
        setSuccess('Lead loaded successfully!')
      } else {
        setError('No leads available at this time.')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to load lead')
    } finally {
      setLoading(false)
    }
  }

  const skipLead = async () => {
    if (!currentLead) return

    try {
      const response = await fetch('/api/leads/skip', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ leadId: currentLead.id })
      })

      if (response.ok) {
        setSuccess('Lead skipped')
        setCurrentLead(null)
        setDisposition('')
        setNotes('')
        setCallbackDate('')
        loadStats()
      } else {
        const data = await response.json()
        setError(data.error || 'Failed to skip lead')
      }
    } catch (error) {
      setError('Failed to skip lead')
    }
  }

  const saveAndNext = async () => {
    if (!currentLead || !disposition) {
      setError('Please select a disposition')
      return
    }

    setDisposing(true)
    setError(null)

    try {
      const payload: any = {
        leadId: currentLead.id,
        status: disposition,
        notes: notes.trim() || undefined
      }

      if (disposition === 'CALLBACK' && callbackDate) {
        payload.callbackAt = new Date(callbackDate).toISOString()
      }

      const response = await fetch('/api/leads/disposition', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Failed to save disposition')
      }

      if (disposition === 'SALE_MADE' && data.sale) {
        setSuccess(`🎉 Sale created! Sale ID: ${data.sale.id}`)
      } else {
        setSuccess('Disposition saved successfully!')
      }

      // Reset form and get next lead
      setCurrentLead(null)
      setDisposition('')
      setNotes('')
      setCallbackDate('')
      loadStats()
      
      // Auto-load next lead after short delay
      setTimeout(() => {
        startSelling()
      }, 1000)

    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to save disposition')
    } finally {
      setDisposing(false)
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    setSuccess('Copied to clipboard!')
  }

  if (session?.user?.role !== 'AGENT' && session?.user?.role !== 'ADMIN') {
    return <div className="p-6 text-center text-red-600">Access denied. Agents and Admins only.</div>
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Lead Workflow</h1>

      {/* Stats Dashboard */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-6 gap-4 mb-8">
          <div className="bg-blue-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-blue-600">{stats.totalAssigned}</div>
            <div className="text-sm text-blue-800">Total Assigned</div>
          </div>
          <div className="bg-green-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-green-600">{stats.newLeads}</div>
            <div className="text-sm text-green-800">New Leads</div>
          </div>
          <div className="bg-orange-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-orange-600">{stats.callbacksDue}</div>
            <div className="text-sm text-orange-800">Callbacks Due</div>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-purple-600">{stats.callbacksScheduled}</div>
            <div className="text-sm text-purple-800">Future Callbacks</div>
          </div>
          <div className="bg-yellow-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-yellow-600">{stats.noAnswers}</div>
            <div className="text-sm text-yellow-800">No Answers</div>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-gray-600">{stats.totalContacted}</div>
            <div className="text-sm text-gray-800">Total Contacted</div>
          </div>
        </div>
      )}

      {/* Error/Success Messages */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="text-red-800">{error}</div>
        </div>
      )}
      
      {success && (
        <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
          <div className="text-green-800">{success}</div>
        </div>
      )}

      {/* Start Selling Button */}
      {!currentLead && (
        <div className="text-center mb-8">
          <button
            onClick={startSelling}
            disabled={loading}
            className="bg-blue-600 text-white px-8 py-4 rounded-lg text-xl font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? 'Loading Lead...' : '🎯 Start Selling'}
          </button>
        </div>
      )}

      {/* Lead Card */}
      {currentLead && (
        <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
          <div className="grid md:grid-cols-2 gap-6">
            {/* Customer Info */}
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-4">
                {currentLead.customerFirstName} {currentLead.customerLastName}
              </h2>
              
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Phone:</span>
                  <div className="flex items-center space-x-2">
                    <a 
                      href={`tel:${currentLead.phoneNumber}`}
                      className="text-blue-600 hover:underline font-medium"
                    >
                      {currentLead.phoneNumber}
                    </a>
                    <button
                      onClick={() => copyToClipboard(currentLead.phoneNumber)}
                      className="text-gray-400 hover:text-gray-600"
                      title="Copy phone"
                    >
                      📋
                    </button>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Email:</span>
                  <div className="flex items-center space-x-2">
                    <a 
                      href={`mailto:${currentLead.email}`}
                      className="text-blue-600 hover:underline"
                    >
                      {currentLead.email}
                    </a>
                    <button
                      onClick={() => copyToClipboard(currentLead.email)}
                      className="text-gray-400 hover:text-gray-600"
                      title="Copy email"
                    >
                      📋
                    </button>
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Times Contacted:</span>
                  <span className="font-medium">{currentLead.timesContacted}</span>
                </div>
              </div>
            </div>

            {/* Plan Info */}
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Plan Details</h3>
              
              <div className="space-y-3">
                {/* Appliances */}
                {currentLead.applianceCoverSelected && (
                  <div>
                    <span className="text-gray-600">Appliances:</span>
                    <div className="mt-1">
                      {currentLead.appliances.map((app, index) => (
                        <div key={index} className="flex justify-between text-sm">
                          <span>{app.applianceType} {app.brand && `(${app.brand})`}</span>
                          <span className="font-medium">£{app.price}/month</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Boiler */}
                {currentLead.boilerCoverSelected && (
                  <div className="flex justify-between">
                    <span className="text-gray-600">Boiler Cover:</span>
                    <span className="font-medium">£{currentLead.boilerPriceSelected}/month</span>
                  </div>
                )}

                {/* Total */}
                <div className="flex justify-between text-lg font-bold text-green-600 pt-2 border-t">
                  <span>Total Plan Cost:</span>
                  <span>£{currentLead.totalPlanCost}/month</span>
                </div>
              </div>
            </div>
          </div>

          {/* Disposition History */}
          {currentLead.dispositionHistory.length > 0 && (
            <div className="mt-6 pt-6 border-t">
              <h4 className="text-md font-medium text-gray-900 mb-2">Recent Activity</h4>
              <div className="space-y-2">
                {currentLead.dispositionHistory.slice(0, 3).map((history, index) => (
                  <div key={index} className="text-sm text-gray-600">
                    <span className="font-medium">{history.status}</span>
                    {history.notes && ` - ${history.notes}`}
                    <span className="text-gray-400 ml-2">
                      {new Date(history.createdAt).toLocaleDateString()}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Disposition Form */}
      {currentLead && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Call Disposition</h3>
          
          <div className="space-y-4">
            {/* Disposition Dropdown */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Disposition *
              </label>
              <select
                value={disposition}
                onChange={(e) => setDisposition(e.target.value)}
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              >
                <option value="">Select disposition...</option>
                <option value="CALLED_NO_ANSWER">Called - No Answer</option>
                <option value="CALLBACK">Schedule Callback</option>
                <option value="SALE_MADE">Sale Made! 🎉</option>
                <option value="CANCELLED">Customer Not Interested</option>
                <option value="DO_NOT_CALL">Do Not Call</option>
              </select>
            </div>

            {/* Callback Date */}
            {disposition === 'CALLBACK' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Callback Date *
                </label>
                <input
                  type="datetime-local"
                  value={callbackDate}
                  onChange={(e) => setCallbackDate(e.target.value)}
                  min={new Date().toISOString().slice(0, 16)}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
            )}

            {/* Notes */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Notes
              </label>
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                rows={3}
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Optional notes about the call..."
              />
            </div>

            {/* Action Buttons */}
            <div className="flex space-x-4">
              <button
                onClick={saveAndNext}
                disabled={!disposition || disposing}
                className="flex-1 bg-green-600 text-white px-6 py-3 rounded-md font-medium hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                {disposing ? 'Saving...' : '✅ Save & Next'}
              </button>
              
              <button
                onClick={skipLead}
                className="bg-gray-600 text-white px-6 py-3 rounded-md font-medium hover:bg-gray-700"
              >
                ⏭️ Skip
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}