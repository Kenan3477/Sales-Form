import React, { useState, useEffect } from 'react'

interface BackupFile {
  filename: string
  timestamp: string
  size: string
  records: number
  tables: Record<string, number>
  communicationSummary?: {
    totalSMS: number
    totalDocuments: number
    smsSuccessRate: number
    documentsGenerated: number
  }
  createdBy: string
  reason: string
  corrupted?: boolean
}

interface LegacyBackupFile {
  filename: string
  timestamp: string
  size: string
  records: number
  tables: Record<string, number>
}

const EnhancedBackupSystem: React.FC = () => {
  const [comprehensiveBackups, setComprehensiveBackups] = useState<BackupFile[]>([])
  const [legacyBackups, setLegacyBackups] = useState<LegacyBackupFile[]>([])
  const [loading, setLoading] = useState(false)
  const [creating, setCreating] = useState(false)
  const [backupReason, setBackupReason] = useState('')
  const [showHistory, setShowHistory] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    loadBackups()
  }, [])

  const loadBackups = async () => {
    setLoading(true)
    setError('')
    
    try {
      // Load comprehensive backups
      const comprehensiveResponse = await fetch('/api/admin/comprehensive-backup')
      if (comprehensiveResponse.ok) {
        const comprehensiveData = await comprehensiveResponse.json()
        setComprehensiveBackups(comprehensiveData.backups || [])
      }

      // Load legacy database backups
      const legacyResponse = await fetch('/api/admin/backups')
      if (legacyResponse.ok) {
        const legacyData = await legacyResponse.json()
        setLegacyBackups(legacyData.backups || [])
      }
    } catch (error) {
      console.error('Error loading backups:', error)
      setError('Failed to load backup information')
    } finally {
      setLoading(false)
    }
  }

  const createComprehensiveBackup = async () => {
    if (!backupReason.trim()) {
      setError('Please provide a reason for creating this backup')
      return
    }

    setCreating(true)
    setError('')
    setSuccess('')

    try {
      const response = await fetch('/api/admin/comprehensive-backup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          reason: backupReason.trim()
        })
      })

      const data = await response.json()

      if (response.ok) {
        setSuccess(`✅ Comprehensive backup created successfully! 
        📁 File: ${data.backupFileName}
        💾 Size: ${data.fileSize}
        📊 Records: ${data.totalRecords.toLocaleString()}
        📞 SMS: ${data.communicationSummary.totalSMS}
        📄 Documents: ${data.communicationSummary.totalDocuments}`)
        setBackupReason('')
        loadBackups() // Refresh the list
      } else {
        setError(data.error || 'Failed to create backup')
      }
    } catch (error) {
      console.error('Error creating backup:', error)
      setError('Failed to create backup - network error')
    } finally {
      setCreating(false)
    }
  }

  const formatDate = (timestamp: string) => {
    try {
      return new Date(timestamp).toLocaleString('en-GB', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch {
      return timestamp
    }
  }

  const formatNumber = (num: number) => {
    return num?.toLocaleString() || '0'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Enhanced Backup System</h2>
            <p className="mt-1 text-sm text-gray-500">
              Comprehensive data protection including SMS history, email records, and document tracking
            </p>
          </div>
          <button
            onClick={loadBackups}
            disabled={loading}
            className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
          >
            {loading ? '🔄' : '🔄'} Refresh
          </button>
        </div>
      </div>

      {/* Create New Backup */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Create Comprehensive Backup</h3>
        <div className="space-y-4">
          <div>
            <label htmlFor="reason" className="block text-sm font-medium text-gray-700">
              Backup Reason *
            </label>
            <input
              type="text"
              id="reason"
              value={backupReason}
              onChange={(e) => setBackupReason(e.target.value)}
              placeholder="e.g., Before system update, Monthly backup, etc."
              className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              disabled={creating}
            />
          </div>
          
          <div className="flex items-center space-x-4">
            <button
              onClick={createComprehensiveBackup}
              disabled={creating || !backupReason.trim()}
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {creating ? '🔄 Creating...' : '📦 Create Comprehensive Backup'}
            </button>
            <div className="text-xs text-gray-500">
              Includes: Sales, Leads, SMS History, Documents, User Data
            </div>
          </div>

          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-md">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          {success && (
            <div className="p-3 bg-green-50 border border-green-200 rounded-md">
              <pre className="text-sm text-green-800 whitespace-pre-wrap">{success}</pre>
            </div>
          )}
        </div>
      </div>

      {/* Comprehensive Backups */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-medium text-gray-900">
            Comprehensive Backups ({comprehensiveBackups.length})
          </h3>
        </div>

        {comprehensiveBackups.length === 0 ? (
          <div className="text-center py-8">
            <div className="text-gray-400 text-6xl mb-4">📦</div>
            <h4 className="text-lg font-medium text-gray-900 mb-2">No Comprehensive Backups</h4>
            <p className="text-gray-500">Create your first comprehensive backup to get started.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {comprehensiveBackups.slice(0, showHistory ? undefined : 5).map((backup, index) => (
              <div
                key={backup.filename}
                className={`border rounded-lg p-4 ${backup.corrupted ? 'border-red-200 bg-red-50' : 'border-gray-200'}`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2">
                      <h4 className="font-medium text-gray-900">{backup.filename}</h4>
                      {index === 0 && (
                        <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded">Latest</span>
                      )}
                      {backup.corrupted && (
                        <span className="px-2 py-1 bg-red-100 text-red-800 text-xs rounded">Corrupted</span>
                      )}
                    </div>
                    
                    <div className="mt-2 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <span className="text-gray-500">Date:</span><br />
                        <span className="font-medium">{formatDate(backup.timestamp)}</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Size:</span><br />
                        <span className="font-medium">{backup.size}</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Records:</span><br />
                        <span className="font-medium">{formatNumber(backup.records)}</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Created By:</span><br />
                        <span className="font-medium">{backup.createdBy}</span>
                      </div>
                    </div>

                    {backup.reason && (
                      <div className="mt-2">
                        <span className="text-gray-500 text-sm">Reason:</span>
                        <p className="text-sm text-gray-700">{backup.reason}</p>
                      </div>
                    )}

                    {backup.communicationSummary && (
                      <div className="mt-3 p-3 bg-blue-50 rounded-md">
                        <h5 className="text-sm font-medium text-blue-900 mb-2">Communication Summary</h5>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
                          <div>
                            <span className="text-blue-600">SMS Messages:</span><br />
                            <span className="font-medium">{formatNumber(backup.communicationSummary.totalSMS)}</span>
                          </div>
                          <div>
                            <span className="text-blue-600">SMS Success Rate:</span><br />
                            <span className="font-medium">{backup.communicationSummary.smsSuccessRate?.toFixed(1)}%</span>
                          </div>
                          <div>
                            <span className="text-blue-600">Documents:</span><br />
                            <span className="font-medium">{formatNumber(backup.communicationSummary.totalDocuments)}</span>
                          </div>
                          <div>
                            <span className="text-blue-600">Generated Docs:</span><br />
                            <span className="font-medium">{formatNumber(backup.communicationSummary.documentsGenerated)}</span>
                          </div>
                        </div>
                      </div>
                    )}

                    <div className="mt-3">
                      <details className="group">
                        <summary className="text-sm text-blue-600 cursor-pointer hover:text-blue-800">
                          View Table Breakdown ({Object.keys(backup.tables).length} tables)
                        </summary>
                        <div className="mt-2 grid grid-cols-2 md:grid-cols-4 gap-2 text-xs bg-gray-50 p-3 rounded">
                          {Object.entries(backup.tables).map(([table, count]) => (
                            <div key={table}>
                              <span className="text-gray-600">{table}:</span>
                              <span className="font-medium ml-1">{formatNumber(count as number)}</span>
                            </div>
                          ))}
                        </div>
                      </details>
                    </div>
                  </div>
                </div>
              </div>
            ))}

            {comprehensiveBackups.length > 5 && (
              <div className="text-center">
                <button
                  onClick={() => setShowHistory(!showHistory)}
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  {showHistory ? 'Show Less' : `Show All ${comprehensiveBackups.length} Backups`}
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Legacy Backups */}
      {legacyBackups.length > 0 && (
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            Legacy Database Backups ({legacyBackups.length})
          </h3>
          <div className="space-y-2">
            {legacyBackups.slice(0, 3).map((backup) => (
              <div key={backup.filename} className="border border-gray-200 rounded p-3">
                <div className="flex justify-between items-center">
                  <div>
                    <span className="font-medium">{backup.filename}</span>
                    <div className="text-sm text-gray-500">
                      {formatDate(backup.timestamp)} • {backup.size} • {formatNumber(backup.records)} records
                    </div>
                  </div>
                </div>
              </div>
            ))}
            {legacyBackups.length > 3 && (
              <p className="text-sm text-gray-500 text-center">
                ... and {legacyBackups.length - 3} more legacy backups
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default EnhancedBackupSystem