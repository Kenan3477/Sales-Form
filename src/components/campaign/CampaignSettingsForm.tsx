'use client'

import { useState, useEffect } from 'react'
import { CampaignSettings, CampaignManagementService } from '@/lib/leads/campaign'
import { LeadStatus } from '@prisma/client'
import { useSession } from 'next-auth/react'

const campaignService = new CampaignManagementService()

const DIALING_STRATEGIES = [
  { value: 'ROUND_ROBIN', label: 'Round Robin', description: 'Distribute leads evenly across all agents' },
  { value: 'PRIORITY_BASED', label: 'Priority Based', description: 'Assign highest priority leads to available agents' },
  { value: 'SKILL_BASED', label: 'Skill Based', description: 'Match agent skills to lead requirements' },
  { value: 'LOAD_BALANCED', label: 'Load Balanced', description: 'Balance workload across agents optimally' }
] as const

const LEAD_STATUSES = [
  { value: 'NEW', label: 'New Leads' },
  { value: 'CALLED_NO_ANSWER', label: 'No Answer' },
  { value: 'CALLBACK', label: 'Callbacks' },
  { value: 'SALE_MADE', label: 'Sales Made' },
  { value: 'CANCELLED', label: 'Cancelled' },
  { value: 'DO_NOT_CALL', label: 'Do Not Call' }
] as const

interface CampaignSettingsFormProps {
  campaign?: CampaignSettings
  onSave: (campaign: CampaignSettings) => void
  onCancel: () => void
}

export default function CampaignSettingsForm({ campaign, onSave, onCancel }: CampaignSettingsFormProps) {
  const { data: session } = useSession()
  const [loading, setLoading] = useState(false)
  const [settings, setSettings] = useState<CampaignSettings>(() => 
    campaign || {
      name: '',
      description: '',
      isActive: false,
      dialingStrategy: 'PRIORITY_BASED',
      priorityRules: {
        callbackPriority: 10,
        newLeadPriority: 7,
        noAnswerRetryPriority: 5,
        timeSinceLastContactWeight: 0.5,
        maxContactAttempts: 5
      },
      frequencySettings: {
        minTimeBetweenCalls: 60,
        maxDailyAttempts: 3,
        retrySchedule: {
          firstRetry: 4,
          subsequentRetries: [24, 72, 168]
        },
        respectDoNotCallTimes: true,
        doNotCallHours: {
          start: '09:00',
          end: '17:00'
        }
      },
      agentAssignment: {
        useSkillMatching: false,
        maxSimultaneousLeads: 5,
        allowReassignment: true,
        reassignmentCriteria: {
          noContactAfterHours: 48,
          maxAttemptsBeforeReassign: 3
        }
      },
      leadFilters: {
        includeStatuses: ['NEW', 'CALLED_NO_ANSWER', 'CALLBACK'],
        excludeStatuses: ['SALE_MADE', 'CANCELLED', 'DO_NOT_CALL'],
        timezoneRespect: true,
        leadAgeLimit: 30
      },
      createdBy: session?.user?.id || ''
    }
  )

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!session?.user?.id) return

    setLoading(true)
    try {
      const savedSettings = await campaignService.saveCampaignSettings({
        ...settings,
        createdBy: session.user.id
      })
      onSave(savedSettings)
    } catch (error) {
      console.error('Failed to save campaign settings:', error)
      alert('Failed to save campaign settings')
    } finally {
      setLoading(false)
    }
  }

  const updateSettings = (path: string, value: any) => {
    setSettings(prev => {
      const keys = path.split('.')
      const updated = { ...prev }
      let current: any = updated

      for (let i = 0; i < keys.length - 1; i++) {
        current[keys[i]] = { ...current[keys[i]] }
        current = current[keys[i]]
      }

      current[keys[keys.length - 1]] = value
      return updated
    })
  }

  const toggleStatusInArray = (status: LeadStatus, arrayPath: 'includeStatuses' | 'excludeStatuses') => {
    const currentArray = settings.leadFilters[arrayPath]
    const isIncluded = currentArray.includes(status)
    
    if (isIncluded) {
      updateSettings(`leadFilters.${arrayPath}`, currentArray.filter(s => s !== status))
    } else {
      updateSettings(`leadFilters.${arrayPath}`, [...currentArray, status])
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">
          {campaign ? 'Edit Campaign Settings' : 'Create New Campaign'}
        </h2>
        <p className="text-gray-600">Configure how leads are assigned and dialed</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Basic Information */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h3 className="text-lg font-semibold mb-4">Basic Information</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Campaign Name *
              </label>
              <input
                type="text"
                required
                value={settings.name}
                onChange={(e) => updateSettings('name', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter campaign name"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Status
              </label>
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={settings.isActive}
                  onChange={(e) => updateSettings('isActive', e.target.checked)}
                  className="mr-2 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                Active Campaign
              </label>
            </div>
          </div>
          <div className="mt-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              value={settings.description || ''}
              onChange={(e) => updateSettings('description', e.target.value)}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Describe this campaign's purpose and strategy"
            />
          </div>
        </div>

        {/* Dialing Strategy */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h3 className="text-lg font-semibold mb-4">Dialing Strategy</h3>
          <div className="space-y-3">
            {DIALING_STRATEGIES.map((strategy) => (
              <label key={strategy.value} className="flex items-start">
                <input
                  type="radio"
                  name="dialingStrategy"
                  value={strategy.value}
                  checked={settings.dialingStrategy === strategy.value}
                  onChange={(e) => updateSettings('dialingStrategy', e.target.value)}
                  className="mt-1 mr-3 h-4 w-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                />
                <div>
                  <div className="font-medium">{strategy.label}</div>
                  <div className="text-sm text-gray-600">{strategy.description}</div>
                </div>
              </label>
            ))}
          </div>
        </div>

        {/* Priority Rules */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h3 className="text-lg font-semibold mb-4">Priority Rules</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Callback Priority (1-10)
              </label>
              <input
                type="number"
                min="1"
                max="10"
                value={settings.priorityRules.callbackPriority}
                onChange={(e) => updateSettings('priorityRules.callbackPriority', parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                New Lead Priority (1-10)
              </label>
              <input
                type="number"
                min="1"
                max="10"
                value={settings.priorityRules.newLeadPriority}
                onChange={(e) => updateSettings('priorityRules.newLeadPriority', parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                No Answer Retry Priority (1-10)
              </label>
              <input
                type="number"
                min="1"
                max="10"
                value={settings.priorityRules.noAnswerRetryPriority}
                onChange={(e) => updateSettings('priorityRules.noAnswerRetryPriority', parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Time Weight (hours multiplier)
              </label>
              <input
                type="number"
                step="0.1"
                min="0"
                value={settings.priorityRules.timeSinceLastContactWeight}
                onChange={(e) => updateSettings('priorityRules.timeSinceLastContactWeight', parseFloat(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Max Contact Attempts
              </label>
              <input
                type="number"
                min="1"
                max="20"
                value={settings.priorityRules.maxContactAttempts}
                onChange={(e) => updateSettings('priorityRules.maxContactAttempts', parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>

        {/* Frequency Settings */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h3 className="text-lg font-semibold mb-4">Frequency Controls</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Min Time Between Calls (minutes)
                </label>
                <input
                  type="number"
                  min="1"
                  value={settings.frequencySettings.minTimeBetweenCalls}
                  onChange={(e) => updateSettings('frequencySettings.minTimeBetweenCalls', parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Max Daily Attempts
                </label>
                <input
                  type="number"
                  min="1"
                  max="10"
                  value={settings.frequencySettings.maxDailyAttempts}
                  onChange={(e) => updateSettings('frequencySettings.maxDailyAttempts', parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  First Retry After (hours)
                </label>
                <input
                  type="number"
                  min="0.5"
                  step="0.5"
                  value={settings.frequencySettings.retrySchedule.firstRetry}
                  onChange={(e) => updateSettings('frequencySettings.retrySchedule.firstRetry', parseFloat(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
            <div className="space-y-4">
              <div>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={settings.frequencySettings.respectDoNotCallTimes}
                    onChange={(e) => updateSettings('frequencySettings.respectDoNotCallTimes', e.target.checked)}
                    className="mr-2 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  Respect Do Not Call Hours
                </label>
              </div>
              {settings.frequencySettings.respectDoNotCallTimes && (
                <>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Calling Start Time
                    </label>
                    <input
                      type="time"
                      value={settings.frequencySettings.doNotCallHours.start}
                      onChange={(e) => updateSettings('frequencySettings.doNotCallHours.start', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Calling End Time
                    </label>
                    <input
                      type="time"
                      value={settings.frequencySettings.doNotCallHours.end}
                      onChange={(e) => updateSettings('frequencySettings.doNotCallHours.end', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Agent Assignment */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h3 className="text-lg font-semibold mb-4">Agent Assignment</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Max Simultaneous Leads per Agent
                </label>
                <input
                  type="number"
                  min="1"
                  max="20"
                  value={settings.agentAssignment.maxSimultaneousLeads}
                  onChange={(e) => updateSettings('agentAssignment.maxSimultaneousLeads', parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={settings.agentAssignment.useSkillMatching}
                    onChange={(e) => updateSettings('agentAssignment.useSkillMatching', e.target.checked)}
                    className="mr-2 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  Use Skill-Based Matching
                </label>
              </div>
              <div>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={settings.agentAssignment.allowReassignment}
                    onChange={(e) => updateSettings('agentAssignment.allowReassignment', e.target.checked)}
                    className="mr-2 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  Allow Lead Reassignment
                </label>
              </div>
            </div>
            {settings.agentAssignment.allowReassignment && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    No Contact Reassign After (hours)
                  </label>
                  <input
                    type="number"
                    min="1"
                    value={settings.agentAssignment.reassignmentCriteria.noContactAfterHours}
                    onChange={(e) => updateSettings('agentAssignment.reassignmentCriteria.noContactAfterHours', parseInt(e.target.value))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Max Attempts Before Reassign
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="10"
                    value={settings.agentAssignment.reassignmentCriteria.maxAttemptsBeforeReassign}
                    onChange={(e) => updateSettings('agentAssignment.reassignmentCriteria.maxAttemptsBeforeReassign', parseInt(e.target.value))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Lead Filters */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h3 className="text-lg font-semibold mb-4">Lead Filters</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Include Lead Statuses</h4>
              <div className="space-y-2">
                {LEAD_STATUSES.map((status) => (
                  <label key={status.value} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={settings.leadFilters.includeStatuses.includes(status.value as LeadStatus)}
                      onChange={() => toggleStatusInArray(status.value as LeadStatus, 'includeStatuses')}
                      className="mr-2 h-4 w-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
                    />
                    <span className="text-sm">{status.label}</span>
                  </label>
                ))}
              </div>
            </div>
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Exclude Lead Statuses</h4>
              <div className="space-y-2">
                {LEAD_STATUSES.map((status) => (
                  <label key={status.value} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={settings.leadFilters.excludeStatuses.includes(status.value as LeadStatus)}
                      onChange={() => toggleStatusInArray(status.value as LeadStatus, 'excludeStatuses')}
                      className="mr-2 h-4 w-4 text-red-600 border-gray-300 rounded focus:ring-red-500"
                    />
                    <span className="text-sm">{status.label}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>
          <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Lead Age Limit (days)
              </label>
              <input
                type="number"
                min="1"
                value={settings.leadFilters.leadAgeLimit}
                onChange={(e) => updateSettings('leadFilters.leadAgeLimit', parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="flex items-center mt-6">
                <input
                  type="checkbox"
                  checked={settings.leadFilters.timezoneRespect}
                  onChange={(e) => updateSettings('leadFilters.timezoneRespect', e.target.checked)}
                  className="mr-2 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                Respect Lead Timezones
              </label>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-end space-x-4 pt-6 border-t">
          <button
            type="button"
            onClick={onCancel}
            className="px-6 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {loading ? 'Saving...' : 'Save Campaign'}
          </button>
        </div>
      </form>
    </div>
  )
}