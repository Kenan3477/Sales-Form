'use client'

import { useState, useEffect, useCallback } from 'react'
import { useSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { formatCurrency } from '@/lib/schemas'

interface Sale {
  id: string
  createdAt: string
  customerFirstName: string
  customerLastName: string
  title: string | null
  phoneNumber: string
  email: string
  notes: string | null
  mailingStreet: string | null
  mailingCity: string | null
  mailingProvince: string | null
  mailingPostalCode: string | null
  accountName: string
  sortCode: string
  accountNumber: string
  directDebitDate: string
  status: string
  applianceCoverSelected: boolean
  boilerCoverSelected: boolean
  boilerPriceSelected: number | null
  totalPlanCost: number
  createdBy: {
    id: string
    email: string
  }
  appliances: {
    id: string
    appliance: string
    otherText: string | null
    coverLimit: number
    cost: number
  }[]
}

export default function AdminSalesPage() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const [sales, setSales] = useState<Sale[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [selectedSales, setSelectedSales] = useState<string[]>([])
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)
  const [deleteAction, setDeleteAction] = useState<'all' | 'selected' | null>(null)
  const [availableAgents, setAvailableAgents] = useState<string[]>([])
  const [filters, setFilters] = useState({
    dateFrom: '',
    dateTo: '',
    agent: '',
    search: '',
    planType: '', // appliance-only, boiler-only, both
    applianceCount: '', // 1, 2-3, 4-5, 6+
    hasBoilerCover: '', // yes, no
    status: '', // ACTIVE, CANCELLED, etc.
    directDebitDateFrom: '',
    directDebitDateTo: ''
  })
  const [duplicateCheckFile, setDuplicateCheckFile] = useState<File | null>(null)
  const [showDuplicateCheck, setShowDuplicateCheck] = useState(false)
  const [duplicateExclusions, setDuplicateExclusions] = useState<string[]>([])
  const [duplicateCustomerCount, setDuplicateCustomerCount] = useState(0)
  const [duplicateCheckUploadError, setDuplicateCheckUploadError] = useState('')

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/auth/login')
    } else if (status === 'authenticated' && session?.user?.role !== 'ADMIN') {
      router.push('/dashboard')
    }
  }, [status, session, router])

  const fetchSales = useCallback(async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (filters.dateFrom) params.append('dateFrom', filters.dateFrom)
      if (filters.dateTo) params.append('dateTo', filters.dateTo)
      if (filters.agent) params.append('agent', filters.agent)
      if (filters.planType) params.append('planType', filters.planType)
      if (filters.applianceCount) params.append('applianceCount', filters.applianceCount)
      if (filters.hasBoilerCover) params.append('hasBoilerCover', filters.hasBoilerCover)
      if (filters.status) params.append('status', filters.status)
      if (filters.directDebitDateFrom) params.append('directDebitDateFrom', filters.directDebitDateFrom)
      if (filters.directDebitDateTo) params.append('directDebitDateTo', filters.directDebitDateTo)

      const response = await fetch(`/api/sales?${params}`)
      if (response.ok) {
        const data = await response.json()
        setSales(data)
      } else {
        setError('Failed to load sales')
      }
    } catch (error) {
      setError('Failed to load sales')
      console.error('Error fetching sales:', error)
    }
    setLoading(false)
  }, [filters])

  useEffect(() => {
    if (session?.user?.role === 'ADMIN') {
      fetchSales()
    }
  }, [session, fetchSales])

  // Separate function to fetch all agents for the dropdown
  const fetchAllAgents = async () => {
    try {
      const response = await fetch('/api/sales')
      if (response.ok) {
        const allSales = await response.json()
        const uniqueAgents = Array.from(new Set(allSales.map((sale: Sale) => sale.createdBy.email))) as string[]
        setAvailableAgents(uniqueAgents.sort()) // Sort alphabetically
      }
    } catch (error) {
      console.error('Error fetching agents:', error)
    }
  }

  // Load agents separately on component mount
  useEffect(() => {
    if (session?.user?.role === 'ADMIN') {
      fetchAllAgents()
    }
  }, [session])

  const handleDuplicateCheckFile = async (file: File | null) => {
    setDuplicateCheckFile(file)
    setDuplicateCheckUploadError('')
    setDuplicateExclusions([])
    setDuplicateCustomerCount(0)

    if (!file) {
      return
    }

    try {
      const text = await file.text()
      const lines = text.split('\n').filter(line => line.trim() !== '')
      
      // Parse CSV properly - each row represents one customer
      const customers = new Set<string>()
      let isFirstLine = true
      let customerCount = 0
      let processedRows = 0
      let skippedRows = 0
      
      lines.forEach((line, index) => {
        const trimmed = line.trim()
        if (!trimmed) return
        
        // Skip header row if it looks like headers
        if (isFirstLine) {
          const lowerLine = trimmed.toLowerCase()
          if (lowerLine.includes('name') || lowerLine.includes('email') || lowerLine.includes('phone') || lowerLine.includes('number') || lowerLine.includes('customer')) {
            isFirstLine = false
            return // Skip this header line
          }
          isFirstLine = false
        }
        
        // Parse CSV row
        const columns = trimmed.split(',').map(col => col.trim().replace(/"/g, ''))
        
        // Validate that this row contains meaningful customer data
        // Look for name (multiple words) and postcode patterns
        let hasName = false
        let hasPostcode = false
        let validColumns: string[] = []
        
        columns.forEach(col => {
          if (col && col.length > 1) {
            const cleaned = col.trim()
            validColumns.push(cleaned)
            
            // Very flexible name validation - anything with letters that's not clearly non-name data
            if (/[a-zA-Z]/.test(cleaned) && 
                !cleaned.includes('@') && 
                !/^[\d\s\-\+\(\)]+$/.test(cleaned) && // Not just numbers/phone chars
                cleaned.length > 1 &&
                !/(ltd|limited|company|corp|inc|plc)$/i.test(cleaned)) { // Not company names
              hasName = true
            }
            
            // Much more flexible postcode validation - any alphanumeric that could be a postcode
            if (/^[A-Z0-9]{2,8}\s*[A-Z0-9]{0,3}$/i.test(cleaned.replace(/\s+/g, ' ')) ||
                /^[A-Z][0-9][A-Z0-9]?\s*[0-9][A-Z]{2}$/i.test(cleaned) ||
                /^[A-Z]{1,2}[0-9]{1,2}[A-Z]?\s*[0-9][A-Z]{2}$/i.test(cleaned)) {
              hasPostcode = true
            }
          }
        })
        
        // More flexible validation - accept rows with good data even if not perfect
        // Accept if we have either a very clear name OR postcode, plus some other data
        const hasGoodData = (hasName || hasPostcode) && validColumns.length >= 2
        
        // Fallback: if we have enough columns with data, probably a customer row
        const hasSufficientData = validColumns.length >= 3 && 
          validColumns.some(col => col.length > 2) // At least one substantial field
        
        if (!hasGoodData && !hasSufficientData) {
          skippedRows++
          console.log('Skipping row:', { 
            row: trimmed.substring(0, 100), 
            hasName, 
            hasPostcode, 
            hasGoodData,
            hasSufficientData,
            validColumnsCount: validColumns.length,
            validColumns: validColumns.slice(0, 4) // Show first 4 columns
          })
          return // Skip this row
        }
        
        processedRows++
        
        // Extract the most reliable customer identifiers from this row
        const customerIdentifiers: string[] = []
        let customerName = ''
        let customerEmail = ''
        let customerPhone = ''
        let customerAccountNumber = ''
        
        validColumns.forEach(col => {
          const cleaned = col.trim()
          
          // Email detection
          if (cleaned.includes('@') && cleaned.includes('.')) {
            customerEmail = cleaned.toLowerCase()
            customerIdentifiers.push(customerEmail)
          }
          
          // Phone number detection - must be 10+ digits
          else if (/^[\d\s\-\+\(\)]{10,}$/.test(cleaned)) {
            const phoneDigits = cleaned.replace(/[^\d]/g, '')
            if (phoneDigits.length >= 10) {
              customerPhone = phoneDigits
              customerIdentifiers.push(customerPhone)
            }
          }
          
          // Account number detection - 8 digits typical for UK bank accounts
          else if (/^\d{8}$/.test(cleaned.replace(/[\s\-]/g, ''))) {
            customerAccountNumber = cleaned.replace(/[\s\-]/g, '')
            customerIdentifiers.push(customerAccountNumber)
          }
          
          // Name detection - must have 2+ words and be primarily letters
          else if (/^[a-zA-Z\s\-\'\.]+$/.test(cleaned) && 
                   cleaned.includes(' ') && 
                   cleaned.split(' ').length >= 2 &&
                   cleaned.length > 3) {
            // This could be a customer name
            const nameParts = cleaned.split(' ').filter(part => part.length > 1)
            if (nameParts.length >= 2) {
              const formattedName = nameParts.join(' ').toLowerCase()
              if (!customerName) { // Take the first valid name found
                customerName = formattedName
                customerIdentifiers.push(formattedName)
                // Also add reversed format (Last, First)
                if (nameParts.length === 2) {
                  customerIdentifiers.push(`${nameParts[1]} ${nameParts[0]}`.toLowerCase())
                }
              }
            }
          }
        })
        
        // Only add customers that have at least one reliable identifier
        if (customerIdentifiers.length > 0) {
          customerIdentifiers.forEach(identifier => {
            customers.add(identifier)
          })
          customerCount++
          
          console.log(`Customer ${customerCount}:`, {
            name: customerName || 'none',
            email: customerEmail || 'none', 
            phone: customerPhone || 'none',
            accountNumber: customerAccountNumber || 'none',
            identifiers: customerIdentifiers.length
          })
        }
      })

      console.log('CSV Processing Summary:', {
        totalLines: lines.length,
        processedRows,
        skippedRows,
        uniqueIdentifiers: customers.size,
        totalCustomers: customerCount,
        sampleIdentifiers: Array.from(customers).slice(0, 10) // Show first 10 for debugging
      })

      setDuplicateExclusions(Array.from(customers))
      setDuplicateCustomerCount(customerCount)
      
      if (customers.size === 0) {
        setDuplicateCheckUploadError('No valid customer identifiers found in file. Please check the file format.')
        return
      }
      
      console.log(`Successfully loaded ${customerCount} customers with ${customers.size} unique identifiers from duplicate reference file`)
      
    } catch (error) {
      console.error('Error processing duplicate check file:', error)
      setDuplicateCheckUploadError('Failed to process file. Please ensure it\'s a valid CSV or text file.')
    }
  }

  const exportToCSV = async () => {
    try {
      const params = new URLSearchParams()
      
      if (filters.dateFrom) {
        params.append('dateFrom', filters.dateFrom)
      }
      if (filters.dateTo) {
        params.append('dateTo', filters.dateTo)
      }
      if (filters.agent) {
        params.append('agent', filters.agent)
      }
      if (filters.status) {
        params.append('status', filters.status)
      }
      if (filters.directDebitDateFrom) {
        params.append('directDebitDateFrom', filters.directDebitDateFrom)
      }
      if (filters.directDebitDateTo) {
        params.append('directDebitDateTo', filters.directDebitDateTo)
      }
      if (filters.planType) {
        params.append('planType', filters.planType)
      }
      if (filters.applianceCount) {
        params.append('applianceCount', filters.applianceCount)
      }
      if (filters.hasBoilerCover) {
        params.append('hasBoilerCover', filters.hasBoilerCover)
      }

      // If duplicate exclusions exist, send them as a POST request
      let response
      if (duplicateExclusions.length > 0) {
        response = await fetch('/api/sales/export', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            filters: {
              dateFrom: filters.dateFrom,
              dateTo: filters.dateTo,
              agent: filters.agent,
              status: filters.status,
              directDebitDateFrom: filters.directDebitDateFrom,
              directDebitDateTo: filters.directDebitDateTo,
              planType: filters.planType,
              applianceCount: filters.applianceCount,
              hasBoilerCover: filters.hasBoilerCover
            },
            excludeCustomers: duplicateExclusions
          })
        })
      } else {
        response = await fetch(`/api/sales/export?${params.toString()}`)
      }
      
      if (!response.ok) {
        throw new Error('Export failed')
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      const filename = duplicateExclusions.length > 0 
        ? `sales_export_deduplicated_${new Date().toISOString().split('T')[0]}.csv`
        : `sales_export_${new Date().toISOString().split('T')[0]}.csv`
      a.download = filename
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Error exporting CSV:', error)
      alert('Failed to export CSV. Please try again.')
    }
  }

  const exportSelectedToCSV = async () => {
    if (selectedSales.length === 0) {
      alert('Please select sales to export.')
      return
    }

    try {
      // If duplicate exclusions exist, send them as a POST request
      let response
      if (duplicateExclusions.length > 0) {
        response = await fetch('/api/sales/export', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            filters: {
              dateFrom: filters.dateFrom,
              dateTo: filters.dateTo,
              agent: filters.agent
            },
            selectedIds: selectedSales,
            excludeCustomers: duplicateExclusions
          })
        })
      } else {
        const params = new URLSearchParams()
        
        // Add selected sale IDs
        selectedSales.forEach(id => params.append('ids', id))
        
        // Add other filters if needed
        if (filters.dateFrom) {
          params.append('dateFrom', filters.dateFrom)
        }
        if (filters.dateTo) {
          params.append('dateTo', filters.dateTo)
        }
        if (filters.agent) {
          params.append('agent', filters.agent)
        }

        response = await fetch(`/api/sales/export?${params.toString()}`)
      }
      
      if (!response.ok) {
        throw new Error('Export failed')
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      const filename = duplicateExclusions.length > 0
        ? `selected_sales_export_deduplicated_${new Date().toISOString().split('T')[0]}.csv`
        : `selected_sales_export_${new Date().toISOString().split('T')[0]}.csv`
      a.download = filename
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Error exporting selected CSV:', error)
      alert('Failed to export selected CSV. Please try again.')
    }
  }

  const handleSelectAll = (checked: boolean) => {
    if (checked) {
      setSelectedSales(filteredSales.map(sale => sale.id))
    } else {
      setSelectedSales([])
    }
  }

  const handleSelectSale = (saleId: string, checked: boolean) => {
    if (checked) {
      setSelectedSales(prev => [...prev, saleId])
    } else {
      setSelectedSales(prev => prev.filter(id => id !== saleId))
    }
  }

  const handleDeleteAll = () => {
    setDeleteAction('all')
    setShowDeleteConfirm(true)
  }

  const handleDeleteSelected = () => {
    if (selectedSales.length === 0) {
      alert('Please select sales to delete')
      return
    }
    setDeleteAction('selected')
    setShowDeleteConfirm(true)
  }

  const confirmDelete = async () => {
    try {
      const params = new URLSearchParams()
      params.append('action', deleteAction!)
      
      if (deleteAction === 'selected') {
        params.append('ids', selectedSales.join(','))
      }

      const response = await fetch(`/api/sales/bulk-delete?${params.toString()}`, {
        method: 'DELETE'
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Delete failed')
      }

      alert(data.message)
      setSelectedSales([])
      setShowDeleteConfirm(false)
      setDeleteAction(null)
      
      // Refresh the sales list
      fetchSales()
    } catch (error) {
      console.error('Error deleting sales:', error)
      alert('Failed to delete sales. Please try again.')
    }
  }

  const cancelDelete = () => {
    setShowDeleteConfirm(false)
    setDeleteAction(null)
  }

  const deleteSale = async (saleId: string) => {
    const sale = sales.find(s => s.id === saleId)
    const customerName = sale ? `${sale.customerFirstName} ${sale.customerLastName}` : 'this customer'
    
    if (!confirm(`Are you sure you want to delete the sale for ${customerName}? This action cannot be undone.`)) {
      return
    }

    try {
      const response = await fetch(`/api/sales/${saleId}`, {
        method: 'DELETE',
      })

      if (response.ok) {
        // Remove the sale from the local state
        setSales(sales.filter(sale => sale.id !== saleId))
        alert('Sale deleted successfully.')
      } else {
        throw new Error('Failed to delete sale')
      }
    } catch (error) {
      console.error('Error deleting sale:', error)
      alert('Failed to delete sale. Please try again.')
    }
  }

  const filteredSales = sales.filter(sale => {
    if (filters.search) {
      const searchLower = filters.search.toLowerCase()
      return (
        sale.customerFirstName.toLowerCase().includes(searchLower) ||
        sale.customerLastName.toLowerCase().includes(searchLower) ||
        sale.email.toLowerCase().includes(searchLower) ||
        sale.createdBy.email.toLowerCase().includes(searchLower)
      )
    }
    return true
  })

  if (status === 'loading' || loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    )
  }

  if (!session || session.user.role !== 'ADMIN') {
    return null
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link href="/dashboard" className="text-xl font-semibold text-gray-900 hover:text-primary-600">
                Sales Form Portal
              </Link>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">
                {session.user.email} ({session.user.role})
              </span>
              <Link
                href="/dashboard"
                className="bg-gray-600 hover:bg-gray-700 text-white px-3 py-2 rounded-md text-sm font-medium"
              >
                Dashboard
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="mb-6 flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">All Sales</h1>
              <p className="mt-2 text-sm text-gray-600">
                Manage all sales submissions from agents.
              </p>
            </div>

            {/* Duplicate Check Section */}
            <div className="mb-4">
              <button
                onClick={() => setShowDuplicateCheck(!showDuplicateCheck)}
                className="bg-purple-600 hover:bg-purple-700 text-white px-3 py-2 rounded-md text-sm font-medium"
              >
                {showDuplicateCheck ? 'Hide' : 'Show'} Duplicate Check
              </button>
            </div>
          </div>

          {/* Duplicate Check Upload Panel */}
          {showDuplicateCheck && (
            <div className="mb-6 bg-purple-50 border border-purple-200 rounded-lg p-4">
              <h3 className="text-lg font-medium text-purple-900 mb-3">Duplicate Check</h3>
              <p className="text-sm text-purple-700 mb-4">
                Upload a CSV file containing existing CRM customers to exclude them from exports. 
                Each row must contain both a customer name AND postcode to be counted as a valid customer.
              </p>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-purple-700 mb-2">
                    Upload CRM Customer File
                  </label>
                  <input
                    type="file"
                    accept=".csv,.txt"
                    onChange={(e) => handleDuplicateCheckFile(e.target.files?.[0] || null)}
                    className="block w-full text-sm text-purple-700 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-purple-100 file:text-purple-700 hover:file:bg-purple-200"
                  />
                  <p className="mt-1 text-xs text-purple-600">
                    CSV format. Each valid row must have: Customer Name (e.g., "John Smith") AND Postcode (e.g., "SW1A 1AA")
                  </p>
                </div>

                {duplicateCheckUploadError && (
                  <div className="text-red-600 text-sm">
                    {duplicateCheckUploadError}
                  </div>
                )}

                {duplicateCheckFile && (
                  <div className="bg-white border border-purple-300 rounded-md p-3">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-purple-900">{duplicateCheckFile.name}</p>
                        <p className="text-xs text-purple-600">
                          {duplicateCustomerCount} customers loaded ({duplicateExclusions.length} identifiers)
                        </p>
                      </div>
                      <button
                        onClick={() => handleDuplicateCheckFile(null)}
                        className="text-purple-400 hover:text-purple-600"
                      >
                        ×
                      </button>
                    </div>
                  </div>
                )}

                {duplicateExclusions.length > 0 && (
                  <div className="text-sm text-green-600">
                    ✅ Ready to export with duplicate exclusion ({duplicateCustomerCount} customers, {duplicateExclusions.length} identifiers)
                  </div>
                )}
              </div>
            </div>
          )}

          <div className="mb-6 flex justify-between items-start">
            <div className="flex space-x-3">
              <Link
                href="/admin/sales/sms"
                className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Send SMS
              </Link>
              <Link
                href="/admin/sales/import"
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Import Sales
              </Link>
              <button
                onClick={exportToCSV}
                disabled={sales.length === 0}
                className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm font-medium disabled:opacity-50"
              >
                Export All CSV
              </button>
              <button
                onClick={exportSelectedToCSV}
                disabled={selectedSales.length === 0}
                className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium disabled:opacity-50"
              >
                Export Selected ({selectedSales.length})
              </button>
              <button
                onClick={handleDeleteSelected}
                disabled={selectedSales.length === 0}
                className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-md text-sm font-medium disabled:opacity-50"
              >
                Delete Selected ({selectedSales.length})
              </button>
              <button
                onClick={handleDeleteAll}
                disabled={sales.length === 0}
                className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium disabled:opacity-50"
              >
                Delete All
              </button>
            </div>
          </div>

          {/* Filters */}
          <div className="bg-white p-4 rounded-lg shadow mb-6">
            <h3 className="text-sm font-medium text-gray-900 mb-3">Filters</h3>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-4 lg:grid-cols-9">
              <div>
                <label htmlFor="search" className="block text-xs font-medium text-gray-700">
                  Search
                </label>
                <input
                  type="text"
                  id="search"
                  value={filters.search}
                  onChange={(e) => setFilters({...filters, search: e.target.value})}
                  placeholder="Customer name, email..."
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm text-sm"
                />
              </div>
              <div>
                <label htmlFor="agent" className="block text-xs font-medium text-gray-700">
                  Agent
                </label>
                <select
                  id="agent"
                  value={filters.agent}
                  onChange={(e) => setFilters({...filters, agent: e.target.value})}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm text-sm"
                >
                  <option value="">All Agents</option>
                  {availableAgents.map((agentEmail) => (
                    <option key={agentEmail} value={agentEmail}>
                      {agentEmail}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label htmlFor="dateFrom" className="block text-xs font-medium text-gray-700">
                  Date From
                </label>
                <input
                  type="date"
                  id="dateFrom"
                  value={filters.dateFrom}
                  onChange={(e) => setFilters({...filters, dateFrom: e.target.value})}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm text-sm"
                />
              </div>
              <div>
                <label htmlFor="dateTo" className="block text-xs font-medium text-gray-700">
                  Date To
                </label>
                <input
                  type="date"
                  id="dateTo"
                  value={filters.dateTo}
                  onChange={(e) => setFilters({...filters, dateTo: e.target.value})}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm text-sm"
                />
              </div>
              <div>
                <label htmlFor="status" className="block text-xs font-medium text-gray-700">
                  Status
                </label>
                <select
                  id="status"
                  value={filters.status}
                  onChange={(e) => setFilters({...filters, status: e.target.value})}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm text-sm"
                >
                  <option value="">All Status</option>
                  <option value="ACTIVE">Active</option>
                  <option value="CANCELLED">Cancelled</option>
                  <option value="CANCELLATION_NOTICE_RECEIVED">Cancellation Notice Received</option>
                  <option value="FAILED_PAYMENT">Failed Payment</option>
                  <option value="PROCESS_DD">Process DD</option>
                </select>
              </div>
              <div>
                <label htmlFor="directDebitDateFrom" className="block text-xs font-medium text-gray-700">
                  DD From
                </label>
                <input
                  type="date"
                  id="directDebitDateFrom"
                  value={filters.directDebitDateFrom}
                  onChange={(e) => setFilters({...filters, directDebitDateFrom: e.target.value})}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm text-sm"
                />
              </div>
              <div>
                <label htmlFor="directDebitDateTo" className="block text-xs font-medium text-gray-700">
                  DD To
                </label>
                <input
                  type="date"
                  id="directDebitDateTo"
                  value={filters.directDebitDateTo}
                  onChange={(e) => setFilters({...filters, directDebitDateTo: e.target.value})}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm text-sm"
                />
              </div>
              <div>
                <label htmlFor="planType" className="block text-xs font-medium text-gray-700">
                  Plan Type
                </label>
                <select
                  id="planType"
                  value={filters.planType}
                  onChange={(e) => setFilters({...filters, planType: e.target.value})}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm text-sm"
                >
                  <option value="">All Plans</option>
                  <option value="appliance-only">Appliance Only</option>
                  <option value="boiler-only">Boiler Only</option>
                  <option value="both">Both</option>
                </select>
              </div>
              <div>
                <label htmlFor="applianceCount" className="block text-xs font-medium text-gray-700">
                  Appliances
                </label>
                <select
                  id="applianceCount"
                  value={filters.applianceCount}
                  onChange={(e) => setFilters({...filters, applianceCount: e.target.value})}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm text-sm"
                >
                  <option value="">Any Amount</option>
                  <option value="1">1 Appliance</option>
                  <option value="2-3">2-3 Appliances</option>
                  <option value="4-5">4-5 Appliances</option>
                  <option value="6+">6+ Appliances</option>
                </select>
              </div>
              <div>
                <label htmlFor="hasBoilerCover" className="block text-xs font-medium text-gray-700">
                  Boiler Cover
                </label>
                <select
                  id="hasBoilerCover"
                  value={filters.hasBoilerCover}
                  onChange={(e) => setFilters({...filters, hasBoilerCover: e.target.value})}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm text-sm"
                >
                  <option value="">Any</option>
                  <option value="yes">Has Boiler Cover</option>
                  <option value="no">No Boiler Cover</option>
                </select>
              </div>
            </div>
            <div className="mt-4 flex justify-end">
              <button
                onClick={fetchSales}
                className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Apply Filters
              </button>
            </div>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
              {error}
            </div>
          )}

          {/* Sales Stats */}
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-3 mb-6">
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm font-medium">📊</span>
                    </div>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        Total Sales
                      </dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {filteredSales.length}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm font-medium">£</span>
                    </div>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        Total Value
                      </dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {formatCurrency(filteredSales.reduce((sum, sale) => sum + sale.totalPlanCost, 0))}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm font-medium">⚡</span>
                    </div>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        Avg. Sale Value
                      </dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {filteredSales.length > 0 
                          ? formatCurrency(filteredSales.reduce((sum, sale) => sum + sale.totalPlanCost, 0) / filteredSales.length)
                          : '£0.00'
                        }
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            {filteredSales.length === 0 ? (
              <div className="text-center py-12">
                <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M34 40h10v-4a6 6 0 00-10.712-3.714M34 40H14m20 0v-4a9.971 9.971 0 00-.712-3.714M14 40H4v-4a6 6 0 0110.712-3.714M14 40v-4a9.971 9.971 0 01.712-3.714M18 20a6 6 0 1112 0c0 1.657-.672 3.157-1.757 4.243M18 20v10h12V20M18 20a6 6 0 016-6 6 6 0 016 6M6 16a6 6 0 1112 0v4"/>
                </svg>
                <h3 className="mt-2 text-sm font-medium text-gray-900">No sales found</h3>
                <p className="mt-1 text-sm text-gray-500">
                  {filters.search || filters.dateFrom || filters.dateTo 
                    ? 'Try adjusting your filters.' 
                    : 'Sales will appear here once agents start submitting them.'
                  }
                </p>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left">
                        <input
                          type="checkbox"
                          checked={filteredSales.length > 0 && selectedSales.length === filteredSales.length}
                          onChange={(e) => handleSelectAll(e.target.checked)}
                          className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        />
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Customer
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Status
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Agent
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Coverage
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Total
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Date
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Actions
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {filteredSales.map((sale) => (
                      <tr key={sale.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <input
                            type="checkbox"
                            checked={selectedSales.includes(sale.id)}
                            onChange={(e) => handleSelectSale(sale.id, e.target.checked)}
                            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                          />
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex flex-col">
                            <div className="text-sm font-medium text-gray-900">
                              {sale.customerFirstName} {sale.customerLastName}
                            </div>
                            <div className="text-sm text-gray-500">{sale.email}</div>
                            <div className="text-sm text-gray-500">{sale.phoneNumber}</div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                            sale.status === 'ACTIVE' ? 'bg-green-100 text-green-800' :
                            sale.status === 'CANCELLED' ? 'bg-red-100 text-red-800' :
                            sale.status === 'CANCELLATION_NOTICE_RECEIVED' ? 'bg-yellow-100 text-yellow-800' :
                            sale.status === 'FAILED_PAYMENT' ? 'bg-orange-100 text-orange-800' :
                            sale.status === 'PROCESS_DD' ? 'bg-blue-100 text-blue-800' :
                            'bg-gray-100 text-gray-800'
                          }`}>
                            {sale.status === 'CANCELLATION_NOTICE_RECEIVED' ? 'CNR' : 
                             sale.status === 'FAILED_PAYMENT' ? 'Failed Payment' :
                             sale.status === 'PROCESS_DD' ? 'Process DD' :
                             sale.status?.charAt(0) + sale.status?.slice(1).toLowerCase()}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900">{sale.createdBy.email}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex flex-col space-y-1">
                            {sale.applianceCoverSelected && (
                              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                {sale.appliances.length} Appliance{sale.appliances.length !== 1 ? 's' : ''}
                              </span>
                            )}
                            {sale.boilerCoverSelected && (
                              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                Boiler {sale.boilerPriceSelected ? formatCurrency(sale.boilerPriceSelected) : ''}
                              </span>
                            )}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900">
                            {formatCurrency(sale.totalPlanCost)}
                          </div>
                          <div className="text-sm text-gray-500">monthly</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {new Date(sale.createdAt).toLocaleDateString()}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          <div className="flex space-x-2">
                            <Link
                              href={`/admin/sales/${sale.id}`}
                              className="inline-flex items-center px-3 py-2 border border-blue-300 shadow-sm text-sm leading-4 font-medium rounded-md text-blue-700 bg-blue-50 hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                            >
                              👁️ View
                            </Link>
                            <button
                              onClick={() => deleteSale(sale.id)}
                              className="inline-flex items-center px-3 py-2 border border-red-300 shadow-sm text-sm leading-4 font-medium rounded-md text-red-700 bg-red-50 hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                            >
                              🗑️ Delete
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Delete Confirmation Dialog */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3 text-center">
              <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
                <svg
                  className="h-6 w-6 text-red-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth="1.5"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"
                  />
                </svg>
              </div>
              <h3 className="text-lg leading-6 font-medium text-gray-900 mt-4">
                Confirm Delete
              </h3>
              <div className="mt-2 px-7 py-3">
                <p className="text-sm text-gray-500">
                  {deleteAction === 'all' 
                    ? `Are you sure you want to delete ALL ${sales.length} sales? This action cannot be undone.`
                    : `Are you sure you want to delete ${selectedSales.length} selected sales? This action cannot be undone.`
                  }
                </p>
              </div>
              <div className="items-center px-4 py-3">
                <div className="flex space-x-3 justify-center">
                  <button
                    onClick={cancelDelete}
                    className="px-4 py-2 bg-gray-500 text-white text-base font-medium rounded-md shadow-sm hover:bg-gray-600 focus:outline-none"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={confirmDelete}
                    className="px-4 py-2 bg-red-600 text-white text-base font-medium rounded-md shadow-sm hover:bg-red-700 focus:outline-none"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}