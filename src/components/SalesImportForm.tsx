'use client'

import { useState } from 'react'

interface ImportResult {
  success: boolean
  imported: number
  total: number
  errors?: Array<{
    row?: number
    sale?: string
    error: string
  }>
  data?: any[]
}

export default function SalesImportForm() {
  const [file, setFile] = useState<File | null>(null)
  const [format, setFormat] = useState<'csv' | 'json'>('csv')
  const [isUploading, setIsUploading] = useState(false)
  const [result, setResult] = useState<ImportResult | null>(null)
  const [showSampleFormat, setShowSampleFormat] = useState(false)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile) {
      setFile(selectedFile)
      // Auto-detect format from file extension
      if (selectedFile.name.endsWith('.json')) {
        setFormat('json')
      } else if (selectedFile.name.endsWith('.csv')) {
        setFormat('csv')
      }
    }
  }

  const handleImport = async () => {
    if (!file) return

    setIsUploading(true)
    setResult(null)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('format', format)

    try {
      const response = await fetch('/api/sales/import', {
        method: 'POST',
        body: formData
      })

      const data = await response.json()
      setResult(data)
    } catch (error) {
      setResult({
        success: false,
        imported: 0,
        total: 0,
        errors: [{ error: 'Upload failed. Please try again.' }]
      })
    } finally {
      setIsUploading(false)
    }
  }

  const downloadTemplate = () => {
    window.open('/api/sales/import/template', '_blank')
  }

  const sampleCSVHeaders = `customerFirstName,customerLastName,title,phoneNumber,email,accountName,sortCode,accountNumber,directDebitDate,applianceCoverSelected,boilerCoverSelected,boilerPriceSelected,totalPlanCost,mailingStreet,mailingCity,mailingProvince,mailingPostalCode,appliance1,appliance1Cost,appliance1CoverLimit,appliance2,appliance2Cost,appliance2CoverLimit,notes`

  const sampleCSVData = `John,Doe,Mr,01234567890,john.doe@email.com,John Doe,12-34-56,12345678,2026-02-01,true,true,25.99,45.98,123 Main St,London,London,SW1A 1AA,Washing Machine,15.99,500,Dishwasher,4.00,300,Customer requested early installation`

  const sampleJSON = `[
  {
    "customerFirstName": "John",
    "customerLastName": "Doe",
    "title": "Mr",
    "phoneNumber": "01234567890",
    "email": "john.doe@email.com",
    "accountName": "John Doe",
    "sortCode": "12-34-56",
    "accountNumber": "12345678",
    "directDebitDate": "2026-02-01",
    "applianceCoverSelected": true,
    "boilerCoverSelected": true,
    "boilerPriceSelected": 25.99,
    "totalPlanCost": 45.98,
    "mailingStreet": "123 Main St",
    "mailingCity": "London",
    "mailingProvince": "London",
    "mailingPostalCode": "SW1A 1AA",
    "appliances": [
      {
        "appliance": "Washing Machine",
        "cost": 15.99,
        "coverLimit": 500
      },
      {
        "appliance": "Dishwasher",
        "cost": 4.00,
        "coverLimit": 300
      }
    ],
    "notes": "Customer requested early installation"
  }
]`

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Import Sales Data</h2>
      
      {/* File Upload Section */}
      <div className="space-y-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select File
          </label>
          <input
            type="file"
            accept=".csv,.json"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            File Format
          </label>
          <div className="flex space-x-4">
            <label className="flex items-center">
              <input
                type="radio"
                value="csv"
                checked={format === 'csv'}
                onChange={(e) => setFormat(e.target.value as 'csv' | 'json')}
                className="mr-2"
              />
              CSV
            </label>
            <label className="flex items-center">
              <input
                type="radio"
                value="json"
                checked={format === 'json'}
                onChange={(e) => setFormat(e.target.value as 'csv' | 'json')}
                className="mr-2"
              />
              JSON
            </label>
          </div>
        </div>

        {/* Sample Format Toggle */}
        <button
          type="button"
          onClick={() => setShowSampleFormat(!showSampleFormat)}
          className="text-sm text-blue-600 hover:text-blue-800 underline"
        >
          {showSampleFormat ? 'Hide' : 'Show'} Sample Format
        </button>

        {/* Sample Format Display */}
        {showSampleFormat && (
          <div className="bg-gray-50 p-4 rounded-md">
            <h3 className="font-medium text-gray-900 mb-2">
              Sample {format.toUpperCase()} Format:
            </h3>
            {format === 'csv' ? (
              <div className="space-y-2">
                <div>
                  <p className="text-xs font-medium text-gray-700 mb-1">Headers:</p>
                  <code className="block text-xs bg-white p-2 rounded border overflow-x-auto">
                    {sampleCSVHeaders}
                  </code>
                </div>
                <div>
                  <p className="text-xs font-medium text-gray-700 mb-1">Sample Data:</p>
                  <code className="block text-xs bg-white p-2 rounded border overflow-x-auto">
                    {sampleCSVData}
                  </code>
                </div>
              </div>
            ) : (
              <pre className="text-xs bg-white p-2 rounded border overflow-x-auto">
                {sampleJSON}
              </pre>
            )}
          </div>
        )}

        {/* Import Button */}
        <div className="flex space-x-3">
          <button
            onClick={downloadTemplate}
            className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700"
          >
            Download CSV Template
          </button>
          <button
            onClick={handleImport}
            disabled={!file || isUploading}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {isUploading ? 'Importing...' : 'Import Sales'}
          </button>
        </div>
      </div>

      {/* Results Section */}
      {result && (
        <div className={`p-4 rounded-md ${result.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
          <h3 className={`font-medium ${result.success ? 'text-green-800' : 'text-red-800'} mb-2`}>
            Import Results
          </h3>
          
          {result.success && (
            <div className="text-green-700">
              <p>✅ Successfully imported {result.imported} out of {result.total} sales</p>
            </div>
          )}

          {result.errors && result.errors.length > 0 && (
            <div className="mt-3">
              <p className="font-medium text-red-800 mb-2">Errors:</p>
              <ul className="text-sm text-red-700 space-y-1">
                {result.errors.map((error, index) => (
                  <li key={index}>
                    {error.row && `Row ${error.row}: `}
                    {error.sale && `Sale ${error.sale}: `}
                    {error.error}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Field Requirements */}
      <div className="mt-6 bg-blue-50 p-4 rounded-md">
        <h3 className="font-medium text-blue-900 mb-2">Required Fields:</h3>
        <ul className="text-sm text-blue-800 grid grid-cols-2 gap-1">
          <li>• customerFirstName</li>
          <li>• customerLastName</li>
          <li>• phoneNumber</li>
          <li>• email</li>
          <li>• accountName</li>
          <li>• sortCode</li>
          <li>• accountNumber</li>
          <li>• directDebitDate</li>
          <li>• totalPlanCost</li>
        </ul>
        <p className="text-xs text-blue-700 mt-2">
          Note: Appliances can be provided either as an array in JSON format or as separate fields (appliance1, appliance1Cost, etc.) in CSV format.
        </p>
      </div>
    </div>
  )
}