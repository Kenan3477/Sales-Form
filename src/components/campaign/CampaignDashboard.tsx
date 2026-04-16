'use client'

import { useState, useEffect } from 'react'
import { CampaignSettings, CampaignManagementService, QueueOptimizationResult } from '@/lib/leads/campaign'
import CampaignSettingsForm from '@/components/campaign/CampaignSettingsForm'
import { useSession } from 'next-auth/react'

const campaignService = new CampaignManagementService()

interface CampaignDashboardProps {
  campaigns: CampaignSettings[]
  activeCampaign: CampaignSettings | null
}

export default function CampaignDashboard({ campaigns: initialCampaigns, activeCampaign }: CampaignDashboardProps) {
  const { data: session } = useSession()
  const [campaigns, setCampaigns] = useState(initialCampaigns)
  const [selectedCampaign, setSelectedCampaign] = useState<CampaignSettings | null>(activeCampaign)
  const [showForm, setShowForm] = useState(false)
  const [editingCampaign, setEditingCampaign] = useState<CampaignSettings | null>(null)
  const [optimization, setOptimization] = useState<QueueOptimizationResult | null>(null)
  const [loading, setLoading] = useState({ optimization: false, apply: false })

  const handleCreateCampaign = () => {
    setEditingCampaign(null)
    setShowForm(true)
  }

  const handleEditCampaign = (campaign: CampaignSettings) => {
    setEditingCampaign(campaign)
    setShowForm(true)
  }

  const handleSaveCampaign = (campaign: CampaignSettings) => {
    if (editingCampaign) {
      // Update existing
      setCampaigns(prev => prev.map(c => c.id === campaign.id ? campaign : c))
    } else {
      // Add new
      setCampaigns(prev => [campaign, ...prev])
    }
    
    // If this campaign is set as active, update selected campaign
    if (campaign.isActive) {
      setSelectedCampaign(campaign)
      // Deactivate other campaigns
      setCampaigns(prev => prev.map(c => 
        c.id !== campaign.id ? { ...c, isActive: false } : c
      ))
    }
    
    setShowForm(false)
  }

  const handleActivateCampaign = async (campaign: CampaignSettings) => {
    try {
      const updatedCampaign = await campaignService.saveCampaignSettings({
        ...campaign,
        isActive: true
      })
      
      setCampaigns(prev => prev.map(c => ({
        ...c,
        isActive: c.id === campaign.id
      })))
      setSelectedCampaign(updatedCampaign)
    } catch (error) {
      console.error('Failed to activate campaign:', error)
      alert('Failed to activate campaign')
    }
  }

  const handleOptimizeQueue = async () => {
    if (!selectedCampaign) return

    setLoading(prev => ({ ...prev, optimization: true }))
    try {
      const result = await campaignService.optimizeQueue(selectedCampaign.id)
      setOptimization(result)
    } catch (error) {
      console.error('Failed to optimize queue:', error)
      alert('Failed to optimize queue')
    } finally {
      setLoading(prev => ({ ...prev, optimization: false }))
    }
  }

  const handleApplyOptimization = async () => {
    if (!selectedCampaign) return

    setLoading(prev => ({ ...prev, apply: true }))
    try {
      const result = await campaignService.applyQueueOptimization(selectedCampaign.id)
      alert(`Applied optimization to ${result.applied} leads. ${result.errors.length} errors.`)
      if (result.errors.length > 0) {
        console.error('Optimization errors:', result.errors)
      }
    } catch (error) {
      console.error('Failed to apply optimization:', error)
      alert('Failed to apply optimization')
    } finally {
      setLoading(prev => ({ ...prev, apply: false }))
    }
  }

  if (showForm) {
    return (
      <CampaignSettingsForm
        campaign={editingCampaign || undefined}
        onSave={handleSaveCampaign}
        onCancel={() => setShowForm(false)}
      />
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Campaign Management</h1>
          <p className="text-gray-600">Configure lead dialing strategies and queue optimization</p>
        </div>
        <button
          onClick={handleCreateCampaign}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-medium"
        >
          Create Campaign
        </button>
      </div>

      {/* Active Campaign Status */}
      {selectedCampaign && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-6">
          <div className="flex items-start justify-between">
            <div>
              <h2 className="text-xl font-semibold text-green-800">Active Campaign</h2>
              <p className="text-green-700 font-medium">{selectedCampaign.name}</p>
              {selectedCampaign.description && (
                <p className="text-green-600 text-sm mt-1">{selectedCampaign.description}</p>
              )}
              <div className="mt-2 text-sm text-green-600">
                <span className="inline-block mr-4">
                  Strategy: <strong>{selectedCampaign.dialingStrategy.replace('_', ' ')}</strong>
                </span>
                <span className="inline-block mr-4">
                  Max Leads/Agent: <strong>{selectedCampaign.agentAssignment.maxSimultaneousLeads}</strong>
                </span>
                <span className="inline-block">
                  Max Attempts: <strong>{selectedCampaign.priorityRules.maxContactAttempts}</strong>
                </span>
              </div>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => handleEditCampaign(selectedCampaign)}
                className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm"
              >
                Edit
              </button>
              <button
                onClick={handleOptimizeQueue}
                disabled={loading.optimization}
                className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm disabled:opacity-50"
              >
                {loading.optimization ? 'Optimizing...' : 'Optimize Queue'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Queue Optimization Results */}
      {optimization && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <div className="flex justify-between items-start mb-4">
            <h3 className="text-lg font-semibold text-blue-800">Queue Optimization Results</h3>
            <button
              onClick={handleApplyOptimization}
              disabled={loading.apply}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded disabled:opacity-50"
            >
              {loading.apply ? 'Applying...' : 'Apply Optimization'}
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
            <div className="bg-white p-3 rounded border">
              <div className="text-2xl font-bold text-blue-600">{optimization.metrics.totalLeadsQueued}</div>
              <div className="text-sm text-gray-600">Total Leads Queued</div>
            </div>
            <div className="bg-white p-3 rounded border">
              <div className="text-2xl font-bold text-blue-600">{optimization.metrics.averagePriority.toFixed(1)}</div>
              <div className="text-sm text-gray-600">Average Priority</div>
            </div>
            <div className="bg-white p-3 rounded border">
              <div className="text-2xl font-bold text-blue-600">{Object.keys(optimization.metrics.agentDistribution).length}</div>
              <div className="text-sm text-gray-600">Agents Assigned</div>
            </div>
            <div className="bg-white p-3 rounded border">
              <div className="text-2xl font-bold text-blue-600">
                {optimization.metrics.estimatedCompletionTime.toLocaleTimeString()}
              </div>
              <div className="text-sm text-gray-600">Est. Completion</div>
            </div>
          </div>

          {/* Agent Distribution */}
          <div className="bg-white rounded border p-4">
            <h4 className="font-medium mb-3">Agent Distribution</h4>
            <div className="space-y-2">
              {Object.entries(optimization.metrics.agentDistribution).map(([agentId, count]) => (
                <div key={agentId} className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Agent {agentId.slice(-8)}</span>
                  <div className="flex items-center">
                    <div className="bg-blue-200 h-4 rounded-full mr-2" style={{ width: `${(count / Math.max(...Object.values(optimization.metrics.agentDistribution))) * 100}px` }}></div>
                    <span className="text-sm font-medium">{count} leads</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Campaign List */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">All Campaigns</h2>
        </div>
        <div className="divide-y divide-gray-200">
          {campaigns.map((campaign) => (
            <div key={campaign.id} className="px-6 py-4 flex justify-between items-center hover:bg-gray-50">
              <div className="flex-1">
                <div className="flex items-center">
                  <h3 className="font-medium text-gray-900">{campaign.name}</h3>
                  {campaign.isActive && (
                    <span className="ml-2 inline-flex px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
                      Active
                    </span>
                  )}
                </div>
                {campaign.description && (
                  <p className="text-sm text-gray-600 mt-1">{campaign.description}</p>
                )}
                <div className="mt-2 text-xs text-gray-500">
                  Strategy: {campaign.dialingStrategy.replace('_', ' ')} • 
                  Max Attempts: {campaign.priorityRules.maxContactAttempts} • 
                  Updated: {campaign.updatedAt ? new Date(campaign.updatedAt).toLocaleDateString() : 'Never'}
                </div>
              </div>
              <div className="flex items-center space-x-2">
                {!campaign.isActive && (
                  <button
                    onClick={() => handleActivateCampaign(campaign)}
                    className="text-green-600 hover:text-green-800 text-sm font-medium"
                  >
                    Activate
                  </button>
                )}
                <button
                  onClick={() => handleEditCampaign(campaign)}
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  Edit
                </button>
              </div>
            </div>
          ))}
          {campaigns.length === 0 && (
            <div className="px-6 py-8 text-center">
              <p className="text-gray-500">No campaigns configured yet.</p>
              <button
                onClick={handleCreateCampaign}
                className="mt-2 text-blue-600 hover:text-blue-800 font-medium"
              >
                Create your first campaign
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}