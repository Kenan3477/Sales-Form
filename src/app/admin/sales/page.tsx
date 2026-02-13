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
  emailLogs?: {
    id: string
    recipientEmail: string
    sentAt: string
    documentId: string | null
    document: {
      id: string
      filename: string
    } | null
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
  
  // Database Restore states
  const [showRestoreModal, setShowRestoreModal] = useState(false)
  const [availableBackups, setAvailableBackups] = useState<any[]>([])
  const [selectedBackup, setSelectedBackup] = useState('')
  const [restoreConfirmation, setRestoreConfirmation] = useState('')
  const [restoreLoading, setRestoreLoading] = useState(false)
  const [restoreError, setRestoreError] = useState('')

  // Database Rollback states  
  const [showRollbackModal, setShowRollbackModal] = useState(false)
  const [availableRollbackPoints, setAvailableRollbackPoints] = useState<any[]>([])
  const [selectedRollbackPoint, setSelectedRollbackPoint] = useState('')
  const [rollbackConfirmation, setRollbackConfirmation] = useState('')
  const [rollbackLoading, setRollbackLoading] = useState(false)
  const [rollbackError, setRollbackError] = useState('')

  // Backup creation states
  const [backupLoading, setBackupLoading] = useState(false)
  const [backupSuccess, setBackupSuccess] = useState('')
  const [backupError, setBackupError] = useState('')

  // Bulk email states
  const [emailLoading, setEmailLoading] = useState(false)
  const [emailSuccess, setEmailSuccess] = useState('')
  const [emailError, setEmailError] = useState('')
  const [emailProgress, setEmailProgress] = useState({ sent: 0, total: 0, errors: 0 })
  const [showEmailConfirm, setShowEmailConfirm] = useState(false)

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
  }, [
    filters.dateFrom,
    filters.dateTo,
    filters.agent,
    filters.planType,
    filters.applianceCount,
    filters.hasBoilerCover,
    filters.status,
    filters.directDebitDateFrom,
    filters.directDebitDateTo
    // Note: search is excluded because it's client-side filtering only
  ])

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
      // Always use POST for selected exports to avoid URL length limits
      const response = await fetch('/api/sales/export', {
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

  const handleSelectCustomersWithEmail = () => {
    const salesWithEmail = filteredSales.filter(sale => sale.email).map(sale => sale.id)
    setSelectedSales(salesWithEmail)
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

  // Bulk email functions
  const handleBulkEmail = () => {
    const salesWithEmail = selectedSales
      .map(saleId => sales.find(sale => sale.id === saleId))
      .filter(sale => sale && sale.email)

    if (salesWithEmail.length === 0) {
      setEmailError('No selected customers have email addresses')
      setTimeout(() => setEmailError(''), 3000)
      return
    }

    setShowEmailConfirm(true)
  }

  const confirmBulkEmail = async () => {
    setEmailLoading(true)
    setEmailError('')
    setEmailSuccess('')
    setEmailProgress({ sent: 0, total: 0, errors: 0 })
    setShowEmailConfirm(false)

    try {
      // Get sales with email addresses
      const salesWithEmail = selectedSales
        .map(saleId => sales.find(sale => sale.id === saleId))
        .filter(sale => sale && sale.email)
        .map(sale => sale!.id)

      if (salesWithEmail.length === 0) {
        setEmailError('No selected customers have email addresses')
        return
      }

      setEmailProgress({ sent: 0, total: salesWithEmail.length, errors: 0 })

      // Use the bulk send API
      const response = await fetch('/api/admin/emails-simple', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: 'bulk_send',
          saleIds: salesWithEmail
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to send bulk emails')
      }

      const data = await response.json()
      
      if (data.success) {
        const details = data.details
        setEmailSuccess(`Successfully sent documents to ${details.successfulCustomers} customer(s). ${details.successfulDocuments} documents sent.`)
        setEmailProgress({ 
          sent: details.successfulCustomers, 
          total: details.totalCustomers, 
          errors: details.failedCustomers 
        })
      } else {
        const details = data.details
        if (details) {
          setEmailSuccess(`Sent to ${details.successfulCustomers} of ${details.totalCustomers} customers. ${details.failedDocuments} documents failed.`)
          setEmailProgress({ 
            sent: details.successfulCustomers, 
            total: details.totalCustomers, 
            errors: details.failedCustomers 
          })
        } else {
          throw new Error(data.error || 'Bulk email failed')
        }
      }

    } catch (error) {
      console.error('Bulk email error:', error)
      setEmailError(error instanceof Error ? error.message : 'Failed to send bulk emails. Please try again.')
    } finally {
      setEmailLoading(false)
      // Refresh sales data to update email status
      await fetchSales()
      // Clear progress after 5 seconds
      setTimeout(() => {
        setEmailProgress({ sent: 0, total: 0, errors: 0 })
        setEmailSuccess('')
        setEmailError('')
      }, 5000)
    }
  }

  const cancelBulkEmail = () => {
    setShowEmailConfirm(false)
  }

  // Backup creation function - Updated to use comprehensive backup
  const handleCreateBackup = async () => {
    setBackupLoading(true)
    setBackupError('')
    setBackupSuccess('')
    
    try {
      const response = await fetch('/api/admin/comprehensive-backup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          reason: 'Manual backup from admin sales page'
        })
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Failed to create backup')
      }

      setBackupSuccess(`✅ Comprehensive backup created successfully!
📁 File: ${data.backupFileName}
💾 Size: ${data.fileSize}
📊 Records: ${data.totalRecords.toLocaleString()}`)
      
      // Clear success message after 10 seconds
      setTimeout(() => setBackupSuccess(''), 10000)
      
    } catch (error) {
      console.error('Error creating backup:', error)
      setBackupError(error instanceof Error ? error.message : 'Failed to create backup')
    } finally {
      setBackupLoading(false)
    }
  }

  // Database Restore Functions
  const fetchAvailableBackups = async () => {
    try {
      const response = await fetch('/api/admin/backups')
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch backups')
      }

      setAvailableBackups(data.backups || [])
    } catch (error) {
      console.error('Error fetching backups:', error)
      setRestoreError('Failed to fetch available backups')
    }
  }

  const handleShowRestore = () => {
    setShowRestoreModal(true)
    setRestoreError('')
    setSelectedBackup('')
    setRestoreConfirmation('')
    fetchAvailableBackups()
  }

  const handleRestoreDatabase = async () => {
    if (!selectedBackup) {
      setRestoreError('Please select a backup file')
      return
    }

    if (restoreConfirmation !== 'RESTORE_CONFIRMED_EMERGENCY') {
      setRestoreError('Please enter the correct confirmation code: RESTORE_CONFIRMED_EMERGENCY')
      return
    }

    setRestoreLoading(true)
    setRestoreError('')

    try {
      const response = await fetch('/api/admin/restore', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          backupFilename: selectedBackup,
          confirmationCode: restoreConfirmation
        })
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Restore failed')
      }

      alert(`✅ Database restored successfully!\n\nRestored from: ${data.backupDate}\nRecords restored: ${data.totalRecordsRestored}\n\nThe page will now refresh to show the restored data.`)
      
      // Close modal and refresh page
      setShowRestoreModal(false)
      window.location.reload()

    } catch (error) {
      console.error('Error restoring database:', error)
      setRestoreError(error instanceof Error ? error.message : 'Failed to restore database')
    } finally {
      setRestoreLoading(false)
    }
  }

  const closeRestoreModal = () => {
    setShowRestoreModal(false)
    setRestoreError('')
    setSelectedBackup('')
    setRestoreConfirmation('')
  }

  // 🔄 ROLLBACK FUNCTIONALITY
  const fetchAvailableRollbackPoints = async () => {
    try {
      const response = await fetch('/api/admin/rollback/list')
      if (response.ok) {
        const data = await response.json()
        setAvailableRollbackPoints(data.rollbackPoints || [])
      } else {
        setRollbackError('Failed to load rollback points')
      }
    } catch (error) {
      setRollbackError('Failed to load rollback points')
      console.error('Error fetching rollback points:', error)
    }
  }

  const openRollbackModal = () => {
    setShowRollbackModal(true)
    setRollbackError('')
    setSelectedRollbackPoint('')
    setRollbackConfirmation('')
    fetchAvailableRollbackPoints()
  }

  const handleDatabaseRollback = async () => {
    if (!selectedRollbackPoint) {
      setRollbackError('Please select a rollback point')
      return
    }

    if (rollbackConfirmation !== 'ROLLBACK_CONFIRMED_EMERGENCY') {
      setRollbackError('Please enter the correct confirmation code: ROLLBACK_CONFIRMED_EMERGENCY')
      return
    }

    // Extra confirmation for rollback (more dangerous than restore)
    if (!confirm(`🚨 EMERGENCY DATABASE ROLLBACK\n\nThis will PERMANENTLY replace ALL current data with data from the selected backup point.\n\nSelected rollback point: ${selectedRollbackPoint}\n\nTHIS ACTION IS IRREVERSIBLE!\n\nAre you absolutely sure you want to proceed?`)) {
      return
    }

    setRollbackLoading(true)
    setRollbackError('')

    try {
      const response = await fetch('/api/admin/rollback/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          backupFilename: selectedRollbackPoint,
          confirmationCode: rollbackConfirmation
        })
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Rollback failed')
      }

      alert(`✅ Database rollback completed successfully!\n\nRolled back to: ${data.rolledBackTo}\nRecords restored: ${data.recordsRestored}\nData integrity verified: ${data.dataIntegrityVerified ? 'YES' : 'NO'}\n\nThe page will now refresh to show the rolled back data.`)
      
      // Close modal and refresh page
      setShowRollbackModal(false)
      window.location.reload()

    } catch (error) {
      console.error('Error performing rollback:', error)
      setRollbackError(error instanceof Error ? error.message : 'Failed to perform rollback')
    } finally {
      setRollbackLoading(false)
    }
  }

  const closeRollbackModal = () => {
    setShowRollbackModal(false)
    setRollbackError('')
    setSelectedRollbackPoint('')
    setRollbackConfirmation('')
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
              <button
                onClick={handleSelectCustomersWithEmail}
                className="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-md text-sm font-medium flex items-center space-x-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <span>Select Email Customers ({filteredSales.filter(sale => sale.email).length})</span>
              </button>
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
                onClick={handleBulkEmail}
                disabled={selectedSales.length === 0 || emailLoading}
                className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-md text-sm font-medium disabled:opacity-50 flex items-center space-x-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <span>
                  {emailLoading ? 'Emailing...' : `Email Documents (${selectedSales.filter(saleId => sales.find(sale => sale.id === saleId)?.email).length})`}
                </span>
              </button>
              <button
                onClick={handleCreateBackup}
                disabled={backupLoading}
                className="bg-cyan-600 hover:bg-cyan-700 text-white px-4 py-2 rounded-md text-sm font-medium disabled:opacity-50 flex items-center space-x-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <span>{backupLoading ? 'Creating...' : 'Create Backup'}</span>
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
              <button
                onClick={handleShowRestore}
                className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium flex items-center space-x-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                <span>Database Restore</span>
              </button>
              <button
                onClick={openRollbackModal}
                className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-md text-sm font-medium flex items-center space-x-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>Emergency Rollback</span>
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

          {backupSuccess && (
            <div className="bg-green-50 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
              {backupSuccess}
            </div>
          )}

          {backupError && (
            <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
              {backupError}
            </div>
          )}

          {/* Sales Stats */}
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-5 mb-6">
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

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm font-medium">🏠</span>
                    </div>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        Appliances Sold
                      </dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {filteredSales.reduce((sum, sale) => sum + sale.appliances.length, 0)}
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
                    <div className="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm font-medium">🔥</span>
                    </div>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        Boilers Sold
                      </dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {filteredSales.filter(sale => sale.boilerCoverSelected).length}
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
                        Email Status
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
                          {sale.emailLogs && sale.emailLogs.length > 0 ? (
                            <div className="flex items-center space-x-2">
                              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                ✅ Sent
                              </span>
                              <span className="text-xs text-gray-400">
                                {sale.emailLogs.length} email{sale.emailLogs.length !== 1 ? 's' : ''}
                              </span>
                            </div>
                          ) : (
                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
                              ❌ Not sent
                            </span>
                          )}
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

      {/* Email Confirmation Dialog */}
      {showEmailConfirm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3 text-center">
              <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-purple-100">
                <svg
                  className="h-6 w-6 text-purple-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth="1.5"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                  />
                </svg>
              </div>
              <h3 className="text-lg leading-6 font-medium text-gray-900 mt-4">
                Send Documents via Email
              </h3>
              <div className="mt-2 px-7 py-3">
                <p className="text-sm text-gray-500">
                  Send documents to {selectedSales.filter(saleId => sales.find(sale => sale.id === saleId)?.email).length} customer(s) who have email addresses?
                  <br /><br />
                  <span className="font-medium">This will:</span>
                  <br />• Find all documents for selected customers
                  <br />• Send professional emails with download links
                  <br />• Email from Hello@theflashteam.co.uk
                </p>
              </div>
              <div className="items-center px-4 py-3">
                <div className="flex space-x-3 justify-center">
                  <button
                    onClick={cancelBulkEmail}
                    className="px-4 py-2 bg-gray-500 text-white text-base font-medium rounded-md shadow-sm hover:bg-gray-600 focus:outline-none"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={confirmBulkEmail}
                    className="px-4 py-2 bg-purple-600 text-white text-base font-medium rounded-md shadow-sm hover:bg-purple-700 focus:outline-none"
                  >
                    Send Emails
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Email Progress Display */}
      {emailLoading && (
        <div className="fixed bottom-4 right-4 bg-white border border-gray-300 rounded-lg shadow-lg p-4 z-50 min-w-[300px]">
          <div className="flex items-center space-x-3">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-purple-600"></div>
            <div>
              <p className="text-sm font-medium text-gray-900">Sending emails...</p>
              <p className="text-xs text-gray-600">
                {emailProgress.sent} of {emailProgress.total} sent
                {emailProgress.errors > 0 && ` (${emailProgress.errors} errors)`}
              </p>
            </div>
          </div>
          {emailProgress.total > 0 && (
            <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-purple-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${(emailProgress.sent / emailProgress.total) * 100}%` }}
              ></div>
            </div>
          )}
        </div>
      )}

      {/* Email Success/Error Messages */}
      {emailSuccess && (
        <div className="fixed bottom-4 right-4 bg-green-50 border border-green-200 rounded-lg shadow-lg p-4 z-50 min-w-[300px]">
          <div className="flex items-center space-x-3">
            <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            <p className="text-sm font-medium text-green-900">{emailSuccess}</p>
          </div>
        </div>
      )}

      {emailError && (
        <div className="fixed bottom-4 right-4 bg-red-50 border border-red-200 rounded-lg shadow-lg p-4 z-50 min-w-[300px]">
          <div className="flex items-center space-x-3">
            <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="text-sm font-medium text-red-900">{emailError}</p>
          </div>
        </div>
      )}

      {/* Database Restore Modal */}
      {showRestoreModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-10 mx-auto p-5 border w-full max-w-2xl shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg leading-6 font-medium text-gray-900 flex items-center space-x-2">
                  <svg className="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  <span>Database Restore</span>
                </h3>
                <button
                  onClick={closeRestoreModal}
                  className="text-gray-400 hover:text-gray-600 text-xl font-bold"
                >
                  ×
                </button>
              </div>

              <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4 mb-4">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-yellow-800">
                      ⚠️ CRITICAL WARNING
                    </h3>
                    <div className="mt-2 text-sm text-yellow-700">
                      <p>This will <strong>REPLACE ALL CURRENT DATA</strong> with the selected backup.</p>
                      <p className="mt-1">All current sales, customers, and system data will be permanently lost.</p>
                      <p className="mt-1 font-semibold">This action cannot be undone!</p>
                    </div>
                  </div>
                </div>
              </div>

              {availableBackups.length === 0 ? (
                <div className="text-center py-6">
                  <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2M4 13h2m8-5v2m0 6V9.5a2.5 2.5 0 00-5 0V16" />
                  </svg>
                  <h3 className="mt-2 text-sm font-medium text-gray-900">No backups available</h3>
                  <p className="mt-1 text-sm text-gray-500">
                    No backup files found. The backup system may not be configured or no backups have been created yet.
                  </p>
                </div>
              ) : (
                <>
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Select Backup to Restore:
                    </label>
                    <select
                      value={selectedBackup}
                      onChange={(e) => setSelectedBackup(e.target.value)}
                      className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    >
                      <option value="">Choose a backup...</option>
                      {availableBackups.map((backup, index) => (
                        <option key={backup.filename} value={backup.filename}>
                          {new Date(backup.timestamp).toLocaleString()} - {backup.records} records ({backup.size})
                          {index === 0 ? ' [Most Recent]' : ''}
                        </option>
                      ))}
                    </select>
                  </div>

                  {selectedBackup && (
                    <div className="mb-4 bg-gray-50 p-3 rounded-md">
                      <h4 className="text-sm font-medium text-gray-900 mb-2">Backup Details:</h4>
                      {(() => {
                        const backup = availableBackups.find(b => b.filename === selectedBackup)
                        if (!backup) return null
                        return (
                          <div className="text-sm text-gray-600 space-y-1">
                            <p><strong>Date:</strong> {new Date(backup.timestamp).toLocaleString()}</p>
                            <p><strong>Total Records:</strong> {backup.records.toLocaleString()}</p>
                            <p><strong>File Size:</strong> {backup.size}</p>
                            <div className="mt-2">
                              <strong>Tables:</strong>
                              <div className="grid grid-cols-2 gap-x-4 mt-1 text-xs">
                                {Object.entries(backup.tables).map(([table, count]) => (
                                  <div key={table}>• {table}: {count as number}</div>
                                ))}
                              </div>
                            </div>
                          </div>
                        )
                      })()}
                    </div>
                  )}

                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Type confirmation code to proceed:
                    </label>
                    <input
                      type="text"
                      value={restoreConfirmation}
                      onChange={(e) => setRestoreConfirmation(e.target.value)}
                      placeholder="RESTORE_CONFIRMED_EMERGENCY"
                      className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    />
                    <p className="mt-1 text-xs text-gray-500">
                      Must type: <code className="bg-gray-100 px-1 py-0.5 rounded">RESTORE_CONFIRMED_EMERGENCY</code>
                    </p>
                  </div>

                  {restoreError && (
                    <div className="mb-4 bg-red-50 border border-red-200 rounded-md p-3">
                      <div className="flex">
                        <div className="flex-shrink-0">
                          <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                          </svg>
                        </div>
                        <div className="ml-3">
                          <p className="text-sm text-red-800">{restoreError}</p>
                        </div>
                      </div>
                    </div>
                  )}
                </>
              )}

              <div className="flex justify-end space-x-3 pt-4 border-t">
                <button
                  onClick={closeRestoreModal}
                  disabled={restoreLoading}
                  className="px-4 py-2 bg-gray-500 text-white text-base font-medium rounded-md shadow-sm hover:bg-gray-600 focus:outline-none disabled:opacity-50"
                >
                  Cancel
                </button>
                <button
                  onClick={handleRestoreDatabase}
                  disabled={!selectedBackup || restoreConfirmation !== 'RESTORE_CONFIRMED_EMERGENCY' || restoreLoading || availableBackups.length === 0}
                  className="px-4 py-2 bg-indigo-600 text-white text-base font-medium rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none disabled:opacity-50 flex items-center space-x-2"
                >
                  {restoreLoading ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                      <span>Restoring...</span>
                    </>
                  ) : (
                    <>
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                      <span>Restore Database</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Emergency Database Rollback Modal */}
      {showRollbackModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-11/12 max-w-2xl shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center">
                  <div className="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-orange-100">
                    <svg className="h-6 w-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <h3 className="ml-4 text-lg leading-6 font-medium text-gray-900">🚨 Emergency Database Rollback</h3>
                </div>
                <button onClick={closeRollbackModal} className="text-gray-400 hover:text-gray-600">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div className="bg-orange-50 border-l-4 border-orange-400 p-4 mb-4">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16c-.77.833.192 2.5 1.732 2.5z" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-orange-800">⚠️ CRITICAL WARNING</h3>
                    <div className="mt-2 text-sm text-orange-700">
                      <p><strong>Emergency Rollback will:</strong></p>
                      <ul className="list-disc ml-5 mt-1">
                        <li>PERMANENTLY replace ALL current database data</li>
                        <li>Create an emergency backup of current state first</li>
                        <li>Restore data to the selected rollback point</li>
                        <li>Verify data integrity throughout the process</li>
                        <li><strong>THIS ACTION IS IRREVERSIBLE!</strong></li>
                      </ul>
                      <p className="mt-2"><strong>Use only in emergency situations when current data is corrupted!</strong></p>
                    </div>
                  </div>
                </div>
              </div>

              {rollbackError && (
                <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-4">
                  <div className="text-sm text-red-600">{rollbackError}</div>
                </div>
              )}

              <div className="mt-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Select Rollback Point:
                </label>
                <select
                  value={selectedRollbackPoint}
                  onChange={(e) => setSelectedRollbackPoint(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                  disabled={rollbackLoading}
                >
                  <option value="">Choose a rollback point...</option>
                  {availableRollbackPoints.map((point) => (
                    <option key={point.filename} value={point.filename}>
                      {point.displayName} {point.dataIntegrityVerified ? '✅' : '⚠️ INTEGRITY ISSUES'}
                    </option>
                  ))}
                </select>
                <p className="text-xs text-gray-500 mt-1">
                  Only verified rollback points are recommended. Points with integrity issues may contain corrupted data.
                </p>
              </div>

              <div className="mt-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Confirmation Code:
                  <span className="text-red-500 ml-1">ROLLBACK_CONFIRMED_EMERGENCY</span>
                </label>
                <input
                  type="text"
                  value={rollbackConfirmation}
                  onChange={(e) => setRollbackConfirmation(e.target.value)}
                  placeholder="Enter: ROLLBACK_CONFIRMED_EMERGENCY"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                  disabled={rollbackLoading}
                />
                <p className="text-xs text-gray-500 mt-1">
                  Type the exact confirmation code to proceed with rollback.
                </p>
              </div>

              <div className="flex justify-end space-x-3 mt-6 pt-4 border-t">
                <button
                  onClick={closeRollbackModal}
                  disabled={rollbackLoading}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md disabled:opacity-50"
                >
                  Cancel
                </button>
                <button
                  onClick={handleDatabaseRollback}
                  disabled={rollbackLoading || !selectedRollbackPoint || rollbackConfirmation !== 'ROLLBACK_CONFIRMED_EMERGENCY'}
                  className="px-6 py-2 bg-orange-600 hover:bg-orange-700 text-white text-sm font-medium rounded-md disabled:opacity-50 flex items-center space-x-2"
                >
                  {rollbackLoading ? (
                    <>
                      <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></div>
                      <span>Rolling Back Database...</span>
                    </>
                  ) : (
                    <>
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span>Emergency Rollback</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}