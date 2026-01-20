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

  const downloadTemplate = (format: 'simple' | 'comprehensive' = 'simple') => {
    let template = ''
    let filename = ''

    if (format === 'simple') {
      template = `customer_first_name,customer_last_name,email,phone_number,title,mailing_street,mailing_city,mailing_province,mailing_postal_code,appliance_type,appliance_brand,appliance_price,boiler_cover,boiler_price,notes,assigned_agent_email
John,Doe,john.doe@example.com,07700123456,Mr,123 High St,London,London,SW1A 1AA,Washing Machine,Bosch,25.99,true,15.00,Customer interested in full coverage,agent@company.com
Jane,Smith,jane.smith@example.com,07700654321,Mrs,456 Oak Ave,Manchester,Greater Manchester,M1 1AA,Dishwasher,Siemens,22.50,false,,Existing customer referral,
`
      filename = 'lead_import_template_simple.csv'
    } else {
      template = `First Name,Last Name,Phone,Email Address,Appliance 1 Type,Appliance 1 Brand,Appliance 1 Age,Appliance 1 Value,Appliance 2 Type,Appliance 2 Brand,Appliance 2 Age,Appliance 2 Value,Boiler Cover Selected,Customer Premium,Boiler Price,Mailing Street,Mailing City,Mailing Province,Mailing Postal Code,Assigned Agent Email,Notes,Total Cost
John,Smith,555-0123,john.smith@email.com,Refrigerator,Samsung,3,150,Dishwasher,LG,2,100,Yes,25.99,75.50,123 Main St,Toronto,Ontario,M1A 1A1,agent@salesportal.com,Customer interested in comprehensive coverage,251.49
Jane,Doe,555-0456,jane.doe@email.com,Washer,Whirlpool,5,120,,,,,No,15.99,,456 Oak Ave,Vancouver,BC,V6B 1B1,,Basic appliance coverage only,135.99
`
      filename = 'lead_import_template_comprehensive.csv'
    }
    
    const blob = new Blob([template], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
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
          <p>• <strong>Two formats supported:</strong> Simple format or Comprehensive format (matches sales export)</p>
          <p>• Required fields: First Name/customer_first_name, Last Name/customer_last_name, Email/email, Phone/phone_number</p>
          <p>• Optional: Assigned Agent Email (if not provided, leads assigned via round-robin)</p>
          <p>• Supports up to 10 appliances per lead (Appliance 1-10 Type/Brand/Age/Value)</p>
          <p>• Boiler cover: Use "Yes"/"No" or "true"/"false" for Boiler Cover Selected</p>
        </div>
        
        <div className="mt-6 flex gap-4">
          <button
            onClick={() => downloadTemplate('simple')}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          >
            📥 Download Simple Template
          </button>
          <button
            onClick={() => downloadTemplate('comprehensive')}
            className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700"
          >
            📥 Download Comprehensive Template
          </button>
        </div>
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
        <h2 className="text-lg font-medium text-gray-900 mb-4">Supported CSV Formats</h2>
        
        <div className="grid md:grid-cols-2 gap-6">
          {/* Simple Format */}
          <div className="bg-white p-4 rounded border">
            <h3 className="font-medium text-gray-800 mb-3">Simple Format</h3>
            <div className="text-sm text-gray-600 mb-3">Traditional lead import format</div>
            <div className="space-y-2 text-sm">
              <div>
                <strong className="text-gray-800">Required:</strong>
                <ul className="ml-4 space-y-1 text-gray-600">
                  <li>• customer_first_name</li>
                  <li>• customer_last_name</li>
                  <li>• email</li>
                  <li>• phone_number</li>
                </ul>
              </div>
              <div>
                <strong className="text-gray-800">Optional:</strong>
                <ul className="ml-4 space-y-1 text-gray-600">
                  <li>• title, mailing_*, notes</li>
                  <li>• appliance_type, appliance_brand</li>
                  <li>• boiler_cover, boiler_price</li>
                  <li>• assigned_agent_email</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Comprehensive Format */}
          <div className="bg-white p-4 rounded border">
            <h3 className="font-medium text-gray-800 mb-3">Comprehensive Format</h3>
            <div className="text-sm text-gray-600 mb-3">Matches sales export format</div>
            <div className="space-y-2 text-sm">
              <div>
                <strong className="text-gray-800">Required:</strong>
                <ul className="ml-4 space-y-1 text-gray-600">
                  <li>• First Name, Last Name</li>
                  <li>• Phone, Email Address</li>
                </ul>
              </div>
              <div>
                <strong className="text-gray-800">Optional:</strong>
                <ul className="ml-4 space-y-1 text-gray-600">
                  <li>• Appliance 1-10 Type/Brand/Age/Value</li>
                  <li>• Boiler Cover Selected (Yes/No)</li>
                  <li>• Customer Premium, Boiler Price</li>
                  <li>• Total Cost, Mailing Address</li>
                  <li>• Assigned Agent Email, Notes</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded text-sm">
          <strong className="text-yellow-800">💡 Tip:</strong> 
          <span className="text-yellow-700 ml-1">
            You can export sales data and re-import as leads for follow-up campaigns. 
            The comprehensive format accepts the exact same field names as the sales export.
          </span>
        </div>
      </div>
    </div>
  )
}