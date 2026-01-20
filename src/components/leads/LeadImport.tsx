'use client'

import { useState, useRef } from 'react'
import { useSession } from 'next-auth/react'

interface ImportResult {
  success: boolean
  batchId: string
  totalRows: number
  successfulRows: number
  failedRows: number
  errors: Array<{
    row: number
    data: any
    reason: string
  }>
}

export default function LeadImport() {
  const { data: session } = useSession()
  const [importing, setImporting] = useState(false)
  const [result, setResult] = useState<ImportResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    if (!file.name.endsWith('.csv')) {
      setError('Please select a CSV file')
      return
    }

    setImporting(true)
    setError(null)
    setResult(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('/api/leads/import', {
        method: 'POST',
        body: formData
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Import failed')
      }

      setResult(data)
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Import failed')
    } finally {
      setImporting(false)
    }
  }

  const downloadTemplate = () => {
    const template = `customer_first_name,customer_last_name,email,phone_number,title,mailing_street,mailing_city,mailing_province,mailing_postal_code,appliance_type,appliance_brand,appliance_price,boiler_cover,boiler_price,notes,assigned_agent_email
John,Doe,john.doe@example.com,07700123456,Mr,123 High St,London,London,SW1A 1AA,Washing Machine,Bosch,25.99,true,15.00,Customer interested in full coverage,agent@company.com
Jane,Smith,jane.smith@example.com,07700654321,Mrs,456 Oak Ave,Manchester,Greater Manchester,M1 1AA,Dishwasher,Siemens,22.50,false,,Existing customer referral,
`
    
    const blob = new Blob([template], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'lead_import_template.csv'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  }

  if (session?.user?.role !== 'ADMIN') {
    return <div className="p-6 text-center text-red-600">Access denied. Admin only.</div>
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Import Leads</h1>
        <p className="text-gray-600">Upload a CSV file to import new leads into the system</p>
      </div>

      {/* Import Instructions */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
        <h2 className="text-lg font-medium text-blue-900 mb-4">Import Instructions</h2>
        <div className="text-blue-800 space-y-2">
          <p>• CSV files must include headers with customer and plan information</p>
          <p>• Maximum 5,000 rows per import</p>
          <p>• Required fields: customer_first_name, customer_last_name, email, phone_number</p>
          <p>• Optional: assigned_agent_email (if not provided, leads will be assigned via round-robin)</p>
          <p>• Appliance info can be individual fields or JSON array in 'appliances' column</p>
        </div>
        
        <button
          onClick={downloadTemplate}
          className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
        >
          📥 Download Template
        </button>
      </div>

      {/* File Upload */}
      <div className="bg-white border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mb-8">
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          onChange={handleFileUpload}
          disabled={importing}
          className="hidden"
        />
        
        <div className="space-y-4">
          <div className="text-4xl">📊</div>
          <div>
            <h3 className="text-lg font-medium text-gray-900">Choose CSV file</h3>
            <p className="text-gray-500">Click to upload or drag and drop</p>
          </div>
          
          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={importing}
            className="bg-green-600 text-white px-6 py-3 rounded-md font-medium hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {importing ? 'Importing...' : 'Select File'}
          </button>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="text-red-800 font-medium">Import Error</div>
          <div className="text-red-700 mt-1">{error}</div>
        </div>
      )}

      {/* Import Results */}
      {result && (
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Import Results</h2>
          
          <div className="grid md:grid-cols-4 gap-4 mb-6">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{result.totalRows}</div>
              <div className="text-sm text-blue-800">Total Rows</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-600">{result.successfulRows}</div>
              <div className="text-sm text-green-800">Successful</div>
            </div>
            <div className="bg-red-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-red-600">{result.failedRows}</div>
              <div className="text-sm text-red-800">Failed</div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">
                {Math.round((result.successfulRows / result.totalRows) * 100)}%
              </div>
              <div className="text-sm text-purple-800">Success Rate</div>
            </div>
          </div>

          <div className="text-sm text-gray-600 mb-4">
            Batch ID: <code className="bg-gray-100 px-2 py-1 rounded">{result.batchId}</code>
          </div>

          {/* Error Details */}
          {result.errors.length > 0 && (
            <div className="mt-6">
              <h3 className="text-lg font-medium text-gray-900 mb-3">Import Errors</h3>
              <div className="bg-red-50 rounded-lg max-h-64 overflow-y-auto">
                {result.errors.slice(0, 10).map((error, index) => (
                  <div key={index} className="p-3 border-b border-red-200 last:border-b-0">
                    <div className="text-red-800 font-medium">Row {error.row}</div>
                    <div className="text-red-700 text-sm">{error.reason}</div>
                    <div className="text-red-600 text-xs mt-1">
                      Data: {JSON.stringify(error.data).substring(0, 100)}...
                    </div>
                  </div>
                ))}
                {result.errors.length > 10 && (
                  <div className="p-3 text-red-600 text-center">
                    ... and {result.errors.length - 10} more errors
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Success Message */}
          {result.successfulRows > 0 && (
            <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="text-green-800 font-medium">
                ✅ Successfully imported {result.successfulRows} leads!
              </div>
              <div className="text-green-700 text-sm mt-1">
                Leads have been assigned to agents and are ready for calling.
              </div>
            </div>
          )}
        </div>
      )}

      {/* Sample Data Format */}
      <div className="mt-8 bg-gray-50 border border-gray-200 rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Supported CSV Columns</h2>
        <div className="grid md:grid-cols-2 gap-4 text-sm">
          <div>
            <h3 className="font-medium text-gray-800 mb-2">Required Fields:</h3>
            <ul className="space-y-1 text-gray-600">
              <li>• customer_first_name</li>
              <li>• customer_last_name</li>
              <li>• email</li>
              <li>• phone_number</li>
            </ul>
          </div>
          <div>
            <h3 className="font-medium text-gray-800 mb-2">Optional Fields:</h3>
            <ul className="space-y-1 text-gray-600">
              <li>• title</li>
              <li>• mailing_street, mailing_city, mailing_province, mailing_postal_code</li>
              <li>• appliance_type, appliance_brand, appliance_price</li>
              <li>• boiler_cover (true/false), boiler_price</li>
              <li>• notes</li>
              <li>• assigned_agent_email</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}