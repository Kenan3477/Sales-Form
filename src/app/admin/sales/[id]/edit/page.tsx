'use client'

import { useState, useEffect } from 'react'
import { useSession } from 'next-auth/react'
import { useRouter, useParams } from 'next/navigation'
import Link from 'next/link'

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
  status: string
  applianceCoverSelected: boolean
  boilerCoverSelected: boolean
  boilerPriceSelected?: number
  totalPlanCost: number
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

interface Appliance {
  appliance: string
  otherText?: string
  coverLimit: number
  cost: number
}

export default function EditSalePage() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const params = useParams()
  const saleId = params.id as string

  const [sale, setSale] = useState<Sale | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  
  const [formData, setFormData] = useState({
    customerFirstName: '',
    customerLastName: '',
    title: '',
    phoneNumber: '',
    email: '',
    notes: '',
    mailingStreet: '',
    mailingCity: '',
    mailingProvince: '',
    mailingPostalCode: '',
    accountName: '',
    sortCode: '',
    accountNumber: '',
    directDebitDate: '',
    status: 'ACTIVE',
    applianceCoverSelected: false,
    boilerCoverSelected: false,
    boilerPriceSelected: 0,
    totalPlanCost: 0,
    appliances: [] as Appliance[]
  })

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/auth/login')
    } else if (status === 'authenticated' && session?.user?.role !== 'ADMIN') {
      router.push('/dashboard')
    }
  }, [status, session, router])

  useEffect(() => {
    if (session?.user?.role === 'ADMIN') {
      fetchSale()
    }
  }, [session, saleId])

  const fetchSale = async () => {
    try {
      const response = await fetch(`/api/sales/${saleId}`)
      if (response.ok) {
        const saleData = await response.json()
        setSale(saleData)
        
        // Populate form with existing data
        setFormData({
          customerFirstName: saleData.customerFirstName || '',
          customerLastName: saleData.customerLastName || '',
          title: saleData.title || '',
          phoneNumber: saleData.phoneNumber || '',
          email: saleData.email || '',
          notes: saleData.notes || '',
          mailingStreet: saleData.mailingStreet || '',
          mailingCity: saleData.mailingCity || '',
          mailingProvince: saleData.mailingProvince || '',
          mailingPostalCode: saleData.mailingPostalCode || '',
          accountName: saleData.accountName || '',
          sortCode: saleData.sortCode || '',
          accountNumber: saleData.accountNumber || '',
          directDebitDate: saleData.directDebitDate?.split('T')[0] || '',
          status: saleData.status || 'ACTIVE',
          applianceCoverSelected: saleData.applianceCoverSelected || false,
          boilerCoverSelected: saleData.boilerCoverSelected || false,
          boilerPriceSelected: saleData.boilerPriceSelected || 0,
          totalPlanCost: saleData.totalPlanCost || 0,
          appliances: saleData.appliances?.map((a: any) => ({
            appliance: a.appliance,
            otherText: a.otherText,
            coverLimit: a.coverLimit,
            cost: a.cost
          })) || []
        })
      } else {
        setError('Failed to load sale')
      }
    } catch (error) {
      setError('Failed to load sale')
      console.error('Error fetching sale:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSaving(true)
    setError('')

    try {
      const response = await fetch(`/api/sales/${saleId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })

      if (response.ok) {
        router.push(`/admin/sales/${saleId}`)
      } else {
        const errorData = await response.json()
        setError(errorData.error || 'Failed to update sale')
      }
    } catch (error) {
      setError('Failed to update sale')
      console.error('Error updating sale:', error)
    } finally {
      setSaving(false)
    }
  }

  const addAppliance = () => {
    setFormData({
      ...formData,
      appliances: [...formData.appliances, {
        appliance: '',
        otherText: '',
        coverLimit: 0,
        cost: 0
      }]
    })
  }

  const removeAppliance = (index: number) => {
    setFormData({
      ...formData,
      appliances: formData.appliances.filter((_, i) => i !== index)
    })
  }

  const updateAppliance = (index: number, field: string, value: any) => {
    const updatedAppliances = [...formData.appliances]
    updatedAppliances[index] = {
      ...updatedAppliances[index],
      [field]: value
    }
    setFormData({
      ...formData,
      appliances: updatedAppliances
    })
  }

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
              <span className="text-sm text-gray-700">Admin: {session.user.email}</span>
              <Link
                href={`/admin/sales/${saleId}`}
                className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Cancel
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="bg-white shadow rounded-lg p-6">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-2xl font-bold text-gray-900">
              Edit Sale - {sale?.customerFirstName} {sale?.customerLastName}
            </h1>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Customer Information */}
            <div className="border-b border-gray-200 pb-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Customer Information</h3>
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Title</label>
                  <select
                    value={formData.title}
                    onChange={(e) => setFormData({...formData, title: e.target.value})}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  >
                    <option value="">Select Title</option>
                    <option value="Mr">Mr</option>
                    <option value="Mrs">Mrs</option>
                    <option value="Miss">Miss</option>
                    <option value="Ms">Ms</option>
                    <option value="Dr">Dr</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">First Name *</label>
                  <input
                    type="text"
                    required
                    value={formData.customerFirstName}
                    onChange={(e) => setFormData({...formData, customerFirstName: e.target.value})}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Last Name *</label>
                  <input
                    type="text"
                    required
                    value={formData.customerLastName}
                    onChange={(e) => setFormData({...formData, customerLastName: e.target.value})}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 mt-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Phone Number</label>
                  <input
                    type="tel"
                    value={formData.phoneNumber}
                    onChange={(e) => setFormData({...formData, phoneNumber: e.target.value})}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Email</label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  />
                </div>
              </div>

              <div className="mt-4">
                <label className="block text-sm font-medium text-gray-700">Status</label>
                <select
                  value={formData.status}
                  onChange={(e) => setFormData({...formData, status: e.target.value})}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                >
                  <option value="ACTIVE">Active</option>
                  <option value="CANCELLED">Cancelled</option>
                  <option value="CANCELLATION_NOTICE_RECEIVED">Cancellation Notice Received</option>
                  <option value="FAILED_PAYMENT">Failed Payment</option>
                  <option value="PROCESS_DD">Process DD</option>
                </select>
              </div>
            </div>

            {/* Address Information */}
            <div className="border-b border-gray-200 pb-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Address Information</h3>
              <div className="grid grid-cols-1 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Street Address</label>
                  <input
                    type="text"
                    value={formData.mailingStreet}
                    onChange={(e) => setFormData({...formData, mailingStreet: e.target.value})}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  />
                </div>
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">City</label>
                    <input
                      type="text"
                      value={formData.mailingCity}
                      onChange={(e) => setFormData({...formData, mailingCity: e.target.value})}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Province/County</label>
                    <input
                      type="text"
                      value={formData.mailingProvince}
                      onChange={(e) => setFormData({...formData, mailingProvince: e.target.value})}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Postal Code</label>
                    <input
                      type="text"
                      value={formData.mailingPostalCode}
                      onChange={(e) => setFormData({...formData, mailingPostalCode: e.target.value})}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Payment Information */}
            <div className="border-b border-gray-200 pb-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Payment Information</h3>
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Account Name</label>
                  <input
                    type="text"
                    value={formData.accountName}
                    onChange={(e) => setFormData({...formData, accountName: e.target.value})}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Sort Code</label>
                  <input
                    type="text"
                    value={formData.sortCode}
                    onChange={(e) => setFormData({...formData, sortCode: e.target.value})}
                    onPaste={(e) => {
                      // Handle paste event to clean the pasted data
                      e.preventDefault()
                      const paste = e.clipboardData.getData('text')
                      const cleanPaste = paste.replace(/[\s\-\D]/g, '').slice(0, 6) // Remove non-digits and limit to 6 characters
                      setFormData({...formData, sortCode: cleanPaste})
                    }}
                    onInput={(e) => {
                      // Clean input as user types, but allow hyphens for user-friendly display
                      const target = e.target as HTMLInputElement
                      let cleanValue = target.value.replace(/[^\d\-]/g, '') // Allow digits and hyphens
                      // Remove spaces and limit to reasonable length
                      if (cleanValue.replace(/\-/g, '').length > 6) {
                        cleanValue = cleanValue.replace(/\-/g, '').slice(0, 6)
                      }
                      if (target.value !== cleanValue) {
                        setFormData({...formData, sortCode: cleanValue})
                      }
                    }}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Account Number</label>
                  <input
                    type="text"
                    value={formData.accountNumber}
                    onChange={(e) => setFormData({...formData, accountNumber: e.target.value})}
                    onPaste={(e) => {
                      // Handle paste event to clean the pasted data
                      e.preventDefault()
                      const paste = e.clipboardData.getData('text')
                      const cleanPaste = paste.replace(/[\s\-\D]/g, '').slice(0, 8) // Remove non-digits and limit to 8 characters
                      setFormData({...formData, accountNumber: cleanPaste})
                    }}
                    onInput={(e) => {
                      // Clean input as user types
                      const target = e.target as HTMLInputElement
                      const cleanValue = target.value.replace(/[\s\-\D]/g, '').slice(0, 8)
                      if (target.value !== cleanValue) {
                        setFormData({...formData, accountNumber: cleanValue})
                      }
                    }}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  />
                </div>
              </div>
              <div className="mt-4">
                <label className="block text-sm font-medium text-gray-700">Direct Debit Date</label>
                <input
                  type="date"
                  value={formData.directDebitDate}
                  onChange={(e) => setFormData({...formData, directDebitDate: e.target.value})}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                />
              </div>
            </div>

            {/* Coverage Selection */}
            <div className="border-b border-gray-200 pb-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Coverage Selection</h3>
              <div className="space-y-4">
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.applianceCoverSelected}
                    onChange={(e) => setFormData({...formData, applianceCoverSelected: e.target.checked})}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label className="ml-2 text-sm text-gray-700">Appliance Cover Selected</label>
                </div>
                
                <div className="flex items-center space-x-4">
                  <input
                    type="checkbox"
                    checked={formData.boilerCoverSelected}
                    onChange={(e) => setFormData({...formData, boilerCoverSelected: e.target.checked})}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label className="text-sm text-gray-700">Boiler Cover Selected</label>
                  {formData.boilerCoverSelected && (
                    <div className="flex items-center space-x-2">
                      <label className="text-sm text-gray-700">Price:</label>
                      <input
                        type="number"
                        step="0.01"
                        value={formData.boilerPriceSelected}
                        onChange={(e) => setFormData({...formData, boilerPriceSelected: parseFloat(e.target.value)})}
                        className="w-20 rounded-md border-gray-300 shadow-sm text-sm"
                      />
                    </div>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">Total Plan Cost</label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.totalPlanCost}
                    onChange={(e) => setFormData({...formData, totalPlanCost: parseFloat(e.target.value)})}
                    className="mt-1 block w-32 rounded-md border-gray-300 shadow-sm"
                  />
                </div>
              </div>
            </div>

            {/* Appliances */}
            <div className="border-b border-gray-200 pb-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-medium text-gray-900">Appliances</h3>
                <button
                  type="button"
                  onClick={addAppliance}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-md text-sm"
                >
                  Add Appliance
                </button>
              </div>
              
              {formData.appliances.map((appliance, index) => (
                <div key={index} className="border rounded-md p-4 mb-4 bg-gray-50">
                  <div className="flex justify-between items-center mb-2">
                    <h4 className="font-medium">Appliance {index + 1}</h4>
                    <button
                      type="button"
                      onClick={() => removeAppliance(index)}
                      className="text-red-600 hover:text-red-700 text-sm"
                    >
                      Remove
                    </button>
                  </div>
                  <div className="grid grid-cols-1 gap-4 sm:grid-cols-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Appliance Type</label>
                      <input
                        type="text"
                        value={appliance.appliance}
                        onChange={(e) => updateAppliance(index, 'appliance', e.target.value)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Other Text</label>
                      <input
                        type="text"
                        value={appliance.otherText || ''}
                        onChange={(e) => updateAppliance(index, 'otherText', e.target.value)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Cover Limit</label>
                      <input
                        type="number"
                        value={appliance.coverLimit}
                        onChange={(e) => updateAppliance(index, 'coverLimit', parseFloat(e.target.value))}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Cost</label>
                      <input
                        type="number"
                        step="0.01"
                        value={appliance.cost}
                        onChange={(e) => updateAppliance(index, 'cost', parseFloat(e.target.value))}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Notes */}
            <div>
              <label className="block text-sm font-medium text-gray-700">Notes</label>
              <textarea
                rows={4}
                value={formData.notes}
                onChange={(e) => setFormData({...formData, notes: e.target.value})}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              />
            </div>

            {/* Submit */}
            <div className="flex justify-end space-x-4">
              <Link
                href={`/admin/sales/${saleId}`}
                className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-md text-sm font-medium"
              >
                Cancel
              </Link>
              <button
                type="submit"
                disabled={saving}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-6 py-2 rounded-md text-sm font-medium"
              >
                {saving ? 'Saving...' : 'Save Changes'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}