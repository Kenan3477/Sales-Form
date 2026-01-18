'use client'

import { useState, useEffect } from 'react'
import { useSession } from 'next-auth/react'
import { useRouter, useParams } from 'next/navigation'
import Link from 'next/link'
import { formatCurrency } from '@/lib/schemas'

interface Sale {
  id: string
  customerFirstName: string
  customerLastName: string
  title?: string
  phoneNumber: string
  email: string
  notes?: string
  mailingStreet?: string
  mailingCity?: string
  mailingProvince?: string
  mailingPostalCode?: string
  accountName: string
  sortCode: string
  accountNumber: string
  directDebitDate: string
  applianceCoverSelected: boolean
  boilerCoverSelected: boolean
  boilerPriceSelected?: number
  totalPlanCost: number
  createdAt: string
  appliances: Array<{
    id: string
    appliance: string
    otherText?: string
    coverLimit: number
    cost: number
  }>
  createdBy: {
    id: string
    email: string
  }
}

export default function AgentSaleDetailPage() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const params = useParams()
  const saleId = params.id as string
  const [sale, setSale] = useState<Sale | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [isEditing, setIsEditing] = useState(false)
  const [updating, setUpdating] = useState(false)
  const [editForm, setEditForm] = useState<Partial<Sale>>({})
  const [successMessage, setSuccessMessage] = useState('')

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/auth/login')
    }
  }, [status, router])

  useEffect(() => {
    if (session && saleId) {
      fetchSale()
    }
  }, [session, saleId])

  const fetchSale = async () => {
    try {
      const response = await fetch(`/api/sales/${saleId}`)
      if (response.ok) {
        const data = await response.json()
        setSale(data)
        setEditForm(data) // Initialize edit form with current data
      } else if (response.status === 404) {
        setError('Sale not found or you do not have permission to view it')
      } else {
        setError('Failed to load sale details')
      }
    } catch (error) {
      setError('Failed to load sale details')
      console.error('Error fetching sale:', error)
    }
    setLoading(false)
  }

  const handleEdit = () => {
    setIsEditing(true)
    setError('')
    setSuccessMessage('')
  }

  const handleCancelEdit = () => {
    setIsEditing(false)
    setEditForm(sale || {}) // Reset form to original data
    setError('')
    setSuccessMessage('')
  }

  const handleSave = async () => {
    if (!sale) return
    
    setUpdating(true)
    setError('')
    setSuccessMessage('')

    try {
      const response = await fetch(`/api/sales/${saleId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(editForm)
      })

      if (response.ok) {
        const updatedSale = await response.json()
        setSale(updatedSale)
        setEditForm(updatedSale)
        setIsEditing(false)
        setSuccessMessage('Sale updated successfully!')
        // Clear success message after 3 seconds
        setTimeout(() => setSuccessMessage(''), 3000)
      } else {
        const errorData = await response.json()
        setError(errorData.error || 'Failed to update sale')
      }
    } catch (error) {
      setError('Failed to update sale')
      console.error('Error updating sale:', error)
    }
    setUpdating(false)
  }

  const handleInputChange = (field: string, value: any) => {
    setEditForm(prev => ({
      ...prev,
      [field]: value
    }))
  }

  if (status === 'loading' || loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    )
  }

  if (!session) {
    return null
  }

  if (error) {
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
                  href="/sales/my-sales"
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium"
                >
                  Back to My Sales
                </Link>
              </div>
            </div>
          </div>
        </nav>

        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">Sale Not Found</h1>
            <p className="text-gray-600 mb-4">{error}</p>
            <Link
              href="/sales/my-sales"
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium"
            >
              Back to My Sales
            </Link>
          </div>
        </div>
      </div>
    )
  }

  if (!sale) {
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
                href="/sales/my-sales"
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Back to My Sales
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="lg:grid lg:grid-cols-12 lg:gap-x-5">
          <div className="space-y-6 sm:px-6 lg:px-0 lg:col-span-12">
            {/* Header */}
            <div className="bg-white shadow sm:rounded-lg">
              <div className="px-4 py-5 sm:px-6">
                {/* Success/Error Messages */}
                {successMessage && (
                  <div className="mb-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded">
                    {successMessage}
                  </div>
                )}
                {error && !isEditing && (
                  <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
                    {error}
                  </div>
                )}
                
                <div className="flex justify-between items-start">
                  <div>
                    <h1 className="text-2xl font-bold text-gray-900">
                      Sale Details {isEditing && <span className="text-orange-600">(Editing)</span>}
                    </h1>
                    <p className="mt-1 text-sm text-gray-600">
                      Sale ID: {sale.id}
                    </p>
                    <p className="text-sm text-gray-600">
                      Submitted: {new Date(sale.createdAt).toLocaleString()}
                    </p>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="text-right">
                      <p className="text-2xl font-bold text-green-600">
                        {formatCurrency(isEditing ? (editForm.totalPlanCost || 0) : sale.totalPlanCost)}
                      </p>
                      <p className="text-sm text-gray-500">monthly</p>
                    </div>
                    
                    {/* Edit Controls */}
                    {!isEditing ? (
                      <button
                        onClick={handleEdit}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium flex items-center space-x-2"
                      >
                        <span>✏️</span>
                        <span>Edit Sale</span>
                      </button>
                    ) : (
                      <div className="flex space-x-2">
                        <button
                          onClick={handleSave}
                          disabled={updating}
                          className={`px-4 py-2 rounded-md text-sm font-medium flex items-center space-x-2 ${
                            updating 
                              ? 'bg-gray-300 cursor-not-allowed' 
                              : 'bg-green-600 hover:bg-green-700 text-white'
                          }`}
                        >
                          <span>💾</span>
                          <span>{updating ? 'Saving...' : 'Save'}</span>
                        </button>
                        <button
                          onClick={handleCancelEdit}
                          disabled={updating}
                          className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-md text-sm font-medium flex items-center space-x-2"
                        >
                          <span>❌</span>
                          <span>Cancel</span>
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Customer Information */}
            <div className="bg-white shadow sm:rounded-lg">
              <div className="px-4 py-5 sm:px-6">
                <h2 className="text-lg leading-6 font-medium text-gray-900">Customer Information</h2>
              </div>
              <div className="border-t border-gray-200">
                <dl className="sm:divide-y sm:divide-gray-200">
                  <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt className="text-sm font-medium text-gray-500">First Name</dt>
                    <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                      {isEditing ? (
                        <input
                          type="text"
                          value={editForm.customerFirstName || ''}
                          onChange={(e) => handleInputChange('customerFirstName', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      ) : (
                        <span>{sale.customerFirstName}</span>
                      )}
                    </dd>
                  </div>
                  <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt className="text-sm font-medium text-gray-500">Last Name</dt>
                    <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                      {isEditing ? (
                        <input
                          type="text"
                          value={editForm.customerLastName || ''}
                          onChange={(e) => handleInputChange('customerLastName', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      ) : (
                        <span>{sale.customerLastName}</span>
                      )}
                    </dd>
                  </div>
                  <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt className="text-sm font-medium text-gray-500">Email</dt>
                    <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                      {isEditing ? (
                        <input
                          type="email"
                          value={editForm.email || ''}
                          onChange={(e) => handleInputChange('email', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      ) : (
                        <span>{sale.email}</span>
                      )}
                    </dd>
                  </div>
                  <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt className="text-sm font-medium text-gray-500">Phone Number</dt>
                    <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                      {isEditing ? (
                        <input
                          type="tel"
                          value={editForm.phoneNumber || ''}
                          onChange={(e) => handleInputChange('phoneNumber', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      ) : (
                        <span>{sale.phoneNumber}</span>
                      )}
                    </dd>
                  </div>
                  <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt className="text-sm font-medium text-gray-500">Notes</dt>
                    <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                      {isEditing ? (
                        <textarea
                          value={editForm.notes || ''}
                          onChange={(e) => handleInputChange('notes', e.target.value)}
                          rows={3}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                          placeholder="Add notes..."
                        />
                      ) : (
                        <span>{sale.notes || 'No notes'}</span>
                      )}
                    </dd>
                  </div>
                </dl>
              </div>
            </div>

            {/* Payment Information */}
            <div className="bg-white shadow sm:rounded-lg">
              <div className="px-4 py-5 sm:px-6">
                <h2 className="text-lg leading-6 font-medium text-gray-900">Payment Information</h2>
              </div>
              <div className="border-t border-gray-200">
                <dl className="sm:divide-y sm:divide-gray-200">
                  <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt className="text-sm font-medium text-gray-500">Account Name</dt>
                    <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{sale.accountName}</dd>
                  </div>
                  <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt className="text-sm font-medium text-gray-500">Sort Code</dt>
                    <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{sale.sortCode}</dd>
                  </div>
                  <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt className="text-sm font-medium text-gray-500">Account Number</dt>
                    <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{sale.accountNumber}</dd>
                  </div>
                  <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt className="text-sm font-medium text-gray-500">Direct Debit Date</dt>
                    <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                      {new Date(sale.directDebitDate).toLocaleDateString()}
                    </dd>
                  </div>
                  <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt className="text-sm font-medium text-gray-500">Total Monthly Cost</dt>
                    <dd className="mt-1 text-sm font-semibold text-gray-900 sm:mt-0 sm:col-span-2">
                      {formatCurrency(sale.totalPlanCost)}
                    </dd>
                  </div>
                </dl>
              </div>
            </div>

            {/* Coverage Information */}
            <div className="bg-white shadow sm:rounded-lg">
              <div className="px-4 py-5 sm:px-6">
                <h2 className="text-lg leading-6 font-medium text-gray-900">Coverage Information</h2>
              </div>
              <div className="border-t border-gray-200">
                <dl className="sm:divide-y sm:divide-gray-200">
                  <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt className="text-sm font-medium text-gray-500">Appliance Cover</dt>
                    <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                      {sale.applianceCoverSelected ? (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          ✓ Selected
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                          Not Selected
                        </span>
                      )}
                    </dd>
                  </div>
                  {sale.applianceCoverSelected && sale.appliances.length > 0 && (
                    <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                      <dt className="text-sm font-medium text-gray-500">Appliances</dt>
                      <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                        <div className="space-y-3">
                          {sale.appliances.map((appliance, index) => (
                            <div key={appliance.id} className="border rounded-lg p-3 bg-gray-50">
                              <div className="flex justify-between items-start">
                                <div>
                                  <h4 className="font-medium text-gray-900">
                                    {appliance.appliance}
                                    {appliance.appliance === 'Other' && appliance.otherText && (
                                      <span className="text-gray-600 ml-2">({appliance.otherText})</span>
                                    )}
                                  </h4>
                                  <p className="text-sm text-gray-600">
                                    Cover Limit: {formatCurrency(appliance.coverLimit)}
                                  </p>
                                </div>
                                <div className="text-right">
                                  <p className="font-medium text-gray-900">{formatCurrency(appliance.cost)}/month</p>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </dd>
                    </div>
                  )}
                  <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt className="text-sm font-medium text-gray-500">Boiler Cover</dt>
                    <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                      {sale.boilerCoverSelected ? (
                        <div className="space-y-1">
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            ✓ Selected
                          </span>
                          {sale.boilerPriceSelected && (
                            <div className="text-sm font-medium">
                              {formatCurrency(sale.boilerPriceSelected)}/month
                            </div>
                          )}
                        </div>
                      ) : (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                          Not Selected
                        </span>
                      )}
                    </dd>
                  </div>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}