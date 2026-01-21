'use client'

import { useState, useEffect } from 'react'
import { useSession } from 'next-auth/react'
import Link from 'next/link'

interface LeadStats {
  totalAssigned: number
  newLeads: number
  callbacksDue: number
  callbacksScheduled: number
  noAnswers: number
  totalContacted: number
}

interface Lead {
  id: string
  customerFirstName: string
  customerLastName: string
  phoneNumber: string
  email: string
  totalPlanCost: number
  applianceCoverSelected: boolean
  boilerCoverSelected: boolean
  timesContacted: number
  status: string
  assignedAt: string
}

export default function LeadsOverview() {
  const { data: session } = useSession()
  const [stats, setStats] = useState<LeadStats | null>(null)
  const [recentLeads, setRecentLeads] = useState<Lead[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (session?.user) {
      loadLeadsData()
    }
  }, [session])

  const loadLeadsData = async () => {
    try {
      setLoading(true)
      
      // Load stats for agents
      if (session?.user.role === 'AGENT') {
        const statsResponse = await fetch('/api/leads/stats')
        if (statsResponse.ok) {
          const statsData = await statsResponse.json()
          setStats(statsData)
        }
      }

      // Load recent leads (this endpoint needs to be created)
      const leadsResponse = await fetch('/api/leads/recent')
      if (leadsResponse.ok) {
        const leadsData = await leadsResponse.json()
        setRecentLeads(leadsData.leads || [])
      }

    } catch (error) {
      console.error('Failed to load leads data:', error)
      setError('Failed to load leads data')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-lg text-gray-600">Loading leads data...</div>
      </div>
    )
  }

  const isAgent = session?.user.role === 'AGENT'
  const isAdmin = session?.user.role === 'ADMIN'

  return (
    <div className="space-y-8">
      {/* Agent Stats Dashboard */}
      {isAgent && stats && (
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-6">Your Lead Statistics</h2>
          
          <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg text-center">
              <div className="text-2xl font-bold text-blue-600">{stats.totalAssigned}</div>
              <div className="text-sm text-blue-800">Total Assigned</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg text-center">
              <div className="text-2xl font-bold text-green-600">{stats.newLeads}</div>
              <div className="text-sm text-green-800">New Leads</div>
            </div>
            <div className="bg-orange-50 p-4 rounded-lg text-center">
              <div className="text-2xl font-bold text-orange-600">{stats.callbacksDue}</div>
              <div className="text-sm text-orange-800">Callbacks Due</div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg text-center">
              <div className="text-2xl font-bold text-purple-600">{stats.callbacksScheduled}</div>
              <div className="text-sm text-purple-800">Future Callbacks</div>
            </div>
            <div className="bg-yellow-50 p-4 rounded-lg text-center">
              <div className="text-2xl font-bold text-yellow-600">{stats.noAnswers}</div>
              <div className="text-sm text-yellow-800">No Answers</div>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg text-center">
              <div className="text-2xl font-bold text-gray-600">{stats.totalContacted}</div>
              <div className="text-sm text-gray-800">Total Contacted</div>
            </div>
          </div>
        </div>
      )}

      {/* No Leads Assigned Message */}
      {isAgent && stats && stats.totalAssigned === 0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
          <div className="text-yellow-800">
            <h3 className="text-lg font-medium mb-2">No Leads Assigned</h3>
            <p className="text-sm">
              You don't have any leads assigned to you at the moment. 
              Please contact your administrator to get leads assigned to your account.
            </p>
          </div>
        </div>
      )}

      {/* Start Working Button for Agents with Leads */}
      {isAgent && stats && stats.totalAssigned > 0 && (
        <div className="bg-white shadow rounded-lg p-6">
          <div className="text-center">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Ready to Start Selling?</h3>
            <p className="text-gray-600 mb-6">
              You have {stats.totalAssigned} leads available. 
              {stats.callbacksDue > 0 && (
                <span className="text-orange-600 font-medium"> {stats.callbacksDue} callbacks are due now!</span>
              )}
            </p>
            <Link
              href="/leads/workflow"
              className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-medium hover:bg-blue-700 transition-colors"
            >
              🎯 Start Selling ({stats.totalAssigned} leads)
            </Link>
          </div>
        </div>
      )}

      {/* Admin Overview */}
      {isAdmin && (
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-6">Admin Overview</h2>
          
          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center p-4 border border-gray-200 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{recentLeads.length}</div>
              <div className="text-sm text-gray-600">Recent Leads</div>
            </div>
            
            <div className="text-center p-4 border border-gray-200 rounded-lg">
              <Link 
                href="/admin/leads/import"
                className="block bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
              >
                📥 Import Leads
              </Link>
            </div>
            
            <div className="text-center p-4 border border-gray-200 rounded-lg">
              <Link 
                href="/admin/sales"
                className="block bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
              >
                📊 Manage Sales
              </Link>
            </div>
          </div>
        </div>
      )}

      {/* Recent Leads Table */}
      {recentLeads.length > 0 && (
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">
              {isAgent ? 'Your Recent Leads' : 'Recent Leads in System'}
            </h3>
          </div>
          
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Customer
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Contact
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Plan Value
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Assigned
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {recentLeads.map((lead) => (
                  <tr key={lead.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">
                        {lead.customerFirstName} {lead.customerLastName}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{lead.phoneNumber}</div>
                      <div className="text-sm text-gray-500">{lead.email}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">
                        £{lead.totalPlanCost}/month
                      </div>
                      <div className="text-xs text-gray-500">
                        {lead.applianceCoverSelected && 'Appliances'} 
                        {lead.applianceCoverSelected && lead.boilerCoverSelected && ' + '}
                        {lead.boilerCoverSelected && 'Boiler'}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        lead.status === 'NEW' ? 'bg-green-100 text-green-800' :
                        lead.status === 'CONTACTED' ? 'bg-blue-100 text-blue-800' :
                        lead.status === 'CALLBACK' ? 'bg-orange-100 text-orange-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {lead.status}
                      </span>
                      {lead.timesContacted > 0 && (
                        <div className="text-xs text-gray-500 mt-1">
                          Contacted {lead.timesContacted}x
                        </div>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(lead.assignedAt).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="text-red-800">
            <h3 className="text-sm font-medium">Error Loading Leads</h3>
            <p className="text-sm mt-1">{error}</p>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && recentLeads.length === 0 && (!stats || stats.totalAssigned === 0) && (
        <div className="text-center py-12">
          <div className="text-gray-500">
            <h3 className="text-lg font-medium mb-2">No Leads Found</h3>
            <p className="text-sm">
              {isAgent 
                ? 'You don\'t have any leads assigned to you yet.'
                : 'There are no leads in the system yet.'
              }
            </p>
            {isAdmin && (
              <div className="mt-4">
                <Link
                  href="/admin/leads/import"
                  className="inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                >
                  Import Leads
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}