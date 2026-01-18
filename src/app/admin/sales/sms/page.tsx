'use client'

import { useState, useEffect } from 'react'
import { useSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { buildSmsMessage } from '@/lib/sms'

interface Sale {
  id: string
  createdAt: string
  customerFirstName: string
  customerLastName: string
  phoneNumber: string
  email: string
  agentEmail: string
  agentName: string
  totalPlanCost: number
  smsStatus: 'NOT_SENT' | 'SENDING' | 'SENT' | 'FAILED' | 'SKIPPED'
  smsSentAt?: string
  smsError?: string
  canSendSms: boolean
}

interface Agent {
  id: string
  email: string
}

interface SMSSummary {
  total: number
  sent: number
  failed: number
  skipped: number
  alreadySent: number
}

interface SMSResult {
  saleId: string
  phoneNumber: string
  status: 'sent' | 'failed' | 'skipped'
  reason?: string
  messageId?: string
}

export default function AdminSMSPage() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const [sales, setSales] = useState<Sale[]>([])
  const [agents, setAgents] = useState<Agent[]>([])
  const [selectedSaleIds, setSelectedSaleIds] = useState<string[]>([])
  const [showConfirmModal, setShowConfirmModal] = useState(false)
  const [sendResults, setSendResults] = useState<{ summary: SMSSummary; details: SMSResult[] } | null>(null)
  const [error, setError] = useState('')

  // Filters
  const [dateFrom, setDateFrom] = useState('')
  const [dateTo, setDateTo] = useState('')
  const [agentFilter, setAgentFilter] = useState('')
  const [smsStatusFilter, setSmsStatusFilter] = useState('')

  useEffect(() => {
    if (status === 'loading') return
    
    if (!session || session.user.role !== 'ADMIN') {
      router.push('/auth/login')
      return
    }

    // Set default dates to today
    const today = new Date()
    const todayStr = today.toISOString().split('T')[0]
    if (!dateFrom) setDateFrom(todayStr)
    if (!dateTo) setDateTo(todayStr)
    
    fetchSales()
  }, [session, status, router])

  useEffect(() => {
    if (dateFrom || dateTo || agentFilter || smsStatusFilter) {
      fetchSales()
    }
  }, [dateFrom, dateTo, agentFilter, smsStatusFilter])

  const fetchSales = async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams()
      if (dateFrom) params.append('dateFrom', dateFrom)
      if (dateTo) params.append('dateTo', dateTo)
      if (agentFilter) params.append('agent', agentFilter)
      if (smsStatusFilter) params.append('smsStatus', smsStatusFilter)

      const response = await fetch(`/api/admin/sales/sms?${params}`)
      if (!response.ok) throw new Error('Failed to fetch sales')

      const data = await response.json()
      setSales(data.sales)
      setAgents(data.agents)
    } catch (error) {
      console.error('Error fetching sales:', error)
      setError('Failed to load sales data')
    } finally {
      setLoading(false)
    }
  }

  const handleSelectAll = () => {
    const eligibleSales = sales.filter(sale => sale.canSendSms)
    if (selectedSaleIds.length === eligibleSales.length) {
      setSelectedSaleIds([])
    } else {
      setSelectedSaleIds(eligibleSales.map(sale => sale.id))
    }
  }

  const handleSelectSale = (saleId: string) => {
    if (selectedSaleIds.includes(saleId)) {
      setSelectedSaleIds(selectedSaleIds.filter(id => id !== saleId))
    } else {
      setSelectedSaleIds([...selectedSaleIds, saleId])
    }
  }

  const getSelectionSummary = () => {
    const selectedSales = sales.filter(sale => selectedSaleIds.includes(sale.id))
    const willSend = selectedSales.filter(sale => sale.smsStatus !== 'SENT').length
    const alreadySent = selectedSales.filter(sale => sale.smsStatus === 'SENT').length
    const nonMobile = selectedSales.length - willSend - alreadySent
    
    return { willSend, alreadySent, nonMobile, total: selectedSales.length }
  }

  const handleSendSMS = async () => {
    if (selectedSaleIds.length === 0) return

    setShowConfirmModal(false)
    setSending(true)
    setError('')
    setSendResults(null)

    try {
      const response = await fetch('/api/admin/sales/sms/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          saleIds: selectedSaleIds,
          confirm: true
        })
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Failed to send SMS')
      }

      setSendResults({
        summary: data.summary,
        details: data.details
      })

      // Refresh sales list to update statuses
      await fetchSales()
      
      // Clear selection
      setSelectedSaleIds([])

    } catch (error) {
      console.error('Error sending SMS:', error)
      setError(error instanceof Error ? error.message : 'Failed to send SMS')
    } finally {
      setSending(false)
    }
  }

  const getSmsStatusBadge = (status: string) => {
    const badges = {
      NOT_SENT: 'bg-gray-100 text-gray-800',
      SENDING: 'bg-yellow-100 text-yellow-800',
      SENT: 'bg-green-100 text-green-800',
      FAILED: 'bg-red-100 text-red-800',
      SKIPPED: 'bg-orange-100 text-orange-800'
    }
    
    return badges[status as keyof typeof badges] || badges.NOT_SENT
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-GB', {
      style: 'currency',
      currency: 'GBP'
    }).format(amount)
  }

  if (status === 'loading' || loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
            <div className="space-y-4">
              {[1,2,3].map(i => (
                <div key={i} className="h-16 bg-gray-200 rounded"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  const eligibleSales = sales.filter(sale => sale.canSendSms)
  const summary = getSelectionSummary()

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Send SMS</h1>
              <p className="text-gray-600 mt-1">Send SMS messages to customers manually</p>
            </div>
            <Link
              href="/admin/sales"
              className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-md transition-colors"
            >
              Back to Sales
            </Link>
          </div>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
            <div className="text-red-800">{error}</div>
          </div>
        )}

        {/* Filters */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Filters</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Date From
              </label>
              <input
                type="date"
                value={dateFrom}
                onChange={(e) => setDateFrom(e.target.value)}
                className="w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Date To
              </label>
              <input
                type="date"
                value={dateTo}
                onChange={(e) => setDateTo(e.target.value)}
                className="w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Agent
              </label>
              <select
                value={agentFilter}
                onChange={(e) => setAgentFilter(e.target.value)}
                className="w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              >
                <option value="">All Agents</option>
                {agents.map(agent => (
                  <option key={agent.id} value={agent.id}>{agent.email}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                SMS Status
              </label>
              <select
                value={smsStatusFilter}
                onChange={(e) => setSmsStatusFilter(e.target.value)}
                className="w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              >
                <option value="">All Status</option>
                <option value="NOT_SENT">Not Sent</option>
                <option value="SENT">Sent</option>
                <option value="FAILED">Failed</option>
                <option value="SKIPPED">Skipped</option>
                <option value="SENDING">Sending</option>
              </select>
            </div>
          </div>
        </div>

        {/* Selection Controls */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={handleSelectAll}
                className="text-primary-600 hover:text-primary-700 font-medium"
              >
                {selectedSaleIds.length === eligibleSales.length ? 'Deselect All' : 'Select All Eligible'}
              </button>
              <span className="text-gray-600">
                {selectedSaleIds.length} of {sales.length} selected
              </span>
            </div>
            
            {selectedSaleIds.length > 0 && (
              <button
                onClick={() => setShowConfirmModal(true)}
                disabled={sending}
                className="bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 text-white px-6 py-2 rounded-md transition-colors flex items-center"
              >
                {sending && (
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                )}
                Send SMS to Selected ({selectedSaleIds.length})
              </button>
            )}
          </div>

          {selectedSaleIds.length > 0 && (
            <div className="mt-4 text-sm text-gray-600">
              Will send: {summary.willSend} | Already sent: {summary.alreadySent} | Selected: {summary.total}
            </div>
          )}
        </div>

        {/* Results */}
        {sendResults && (
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">SMS Send Results</h2>
            
            <div className="grid grid-cols-4 gap-4 mb-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">{sendResults.summary.sent}</div>
                <div className="text-sm text-gray-600">Sent</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-red-600">{sendResults.summary.failed}</div>
                <div className="text-sm text-gray-600">Failed</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-orange-600">{sendResults.summary.skipped}</div>
                <div className="text-sm text-gray-600">Skipped</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-600">{sendResults.summary.alreadySent}</div>
                <div className="text-sm text-gray-600">Already Sent</div>
              </div>
            </div>

            {sendResults.details.filter(r => r.status === 'failed' || r.status === 'skipped').length > 0 && (
              <div className="mt-4">
                <h3 className="font-medium text-gray-900 mb-2">Issues:</h3>
                <div className="space-y-1 text-sm">
                  {sendResults.details.filter(r => r.status === 'failed' || r.status === 'skipped').map((result, index) => (
                    <div key={index} className="flex justify-between">
                      <span>{result.phoneNumber}</span>
                      <span className="text-red-600">{result.reason}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Sales Table */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">
              Sales ({sales.length} total, {eligibleSales.length} eligible)
            </h2>
          </div>
          
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    <input
                      type="checkbox"
                      checked={selectedSaleIds.length === eligibleSales.length && eligibleSales.length > 0}
                      onChange={handleSelectAll}
                      className="rounded border-gray-300"
                    />
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Customer</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Phone</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Agent</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sale Date</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">SMS Status</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {sales.map((sale) => (
                  <tr key={sale.id} className={`${selectedSaleIds.includes(sale.id) ? 'bg-blue-50' : ''}`}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <input
                        type="checkbox"
                        checked={selectedSaleIds.includes(sale.id)}
                        onChange={() => handleSelectSale(sale.id)}
                        disabled={!sale.canSendSms}
                        className="rounded border-gray-300"
                      />
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">
                        {sale.customerFirstName} {sale.customerLastName}
                      </div>
                      <div className="text-sm text-gray-500">{sale.email}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {sale.phoneNumber}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {sale.agentName}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {new Date(sale.createdAt).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {formatCurrency(sale.totalPlanCost)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getSmsStatusBadge(sale.smsStatus)}`}>
                        {sale.smsStatus.replace('_', ' ')}
                      </span>
                      {sale.smsSentAt && (
                        <div className="text-xs text-gray-500 mt-1">
                          {new Date(sale.smsSentAt).toLocaleString()}
                        </div>
                      )}
                      {sale.smsError && (
                        <div className="text-xs text-red-500 mt-1" title={sale.smsError}>
                          Error
                        </div>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Confirmation Modal */}
        {showConfirmModal && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
              <div className="mt-3">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Confirm SMS Send</h3>
                <div className="space-y-2 text-sm text-gray-600 mb-6">
                  <p>You are about to send SMS to <strong>{summary.willSend}</strong> recipients.</p>
                  <p>Message: <em>"{buildSmsMessage()}"</em></p>
                  <div className="bg-gray-50 p-3 rounded">
                    <p>Will send: <span className="font-medium">{summary.willSend}</span></p>
                    <p>Already sent: <span className="font-medium">{summary.alreadySent}</span></p>
                    <p>Selected total: <span className="font-medium">{summary.total}</span></p>
                  </div>
                </div>
                <div className="flex space-x-3">
                  <button
                    onClick={() => setShowConfirmModal(false)}
                    className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 py-2 px-4 rounded-md transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleSendSMS}
                    className="flex-1 bg-primary-600 hover:bg-primary-700 text-white py-2 px-4 rounded-md transition-colors"
                  >
                    Send SMS
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}