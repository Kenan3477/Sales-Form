'use client'

import { useState, useEffect } from 'react'
import { useSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

interface FieldConfiguration {
  id: string
  fieldName: string
  isRequired: boolean
}

const FIELD_LABELS = {
  customerFirstName: 'Customer First Name',
  customerLastName: 'Customer Last Name',
  phoneNumber: 'Phone Number',
  email: 'Email',
  accountName: 'Account Name',
  sortCode: 'Sort Code',
  accountNumber: 'Account Number',
  directDebitDate: 'Direct Debit Date',
  applianceCover: 'Appliance Cover Checkbox',
  boilerCover: 'Boiler Cover Checkbox',
  applianceRows: 'Appliance Rows (when appliance cover selected)',
  boilerOption: 'Boiler Option (when boiler cover selected)',
}

export default function AdminSettingsPage() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const [fieldConfigurations, setFieldConfigurations] = useState<FieldConfiguration[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/auth/login')
    } else if (status === 'authenticated' && session?.user?.role !== 'ADMIN') {
      router.push('/dashboard')
    }
  }, [status, session, router])

  useEffect(() => {
    if (session?.user?.role === 'ADMIN') {
      fetchFieldConfigurations()
    }
  }, [session])

  const fetchFieldConfigurations = async () => {
    try {
      const response = await fetch('/api/field-configurations')
      if (response.ok) {
        const data = await response.json()
        setFieldConfigurations(data)
      } else {
        setError('Failed to load field configurations')
      }
    } catch (error) {
      setError('Failed to load field configurations')
      console.error('Error fetching field configurations:', error)
    }
    setLoading(false)
  }

  const handleToggle = (fieldName: string) => {
    setFieldConfigurations(prev =>
      prev.map(config =>
        config.fieldName === fieldName
          ? { ...config, isRequired: !config.isRequired }
          : config
      )
    )
  }

  const handleSave = async () => {
    setSaving(true)
    setError('')
    setSuccess('')

    try {
      const response = await fetch('/api/field-configurations', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          configurations: fieldConfigurations
        }),
      })

      if (response.ok) {
        setSuccess('Field configurations saved successfully!')
        setTimeout(() => setSuccess(''), 3000)
      } else {
        setError('Failed to save field configurations')
      }
    } catch (error) {
      setError('Failed to save field configurations')
      console.error('Error saving field configurations:', error)
    }
    setSaving(false)
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

      <div className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-900">Field Configuration</h1>
            <p className="mt-2 text-sm text-gray-600">
              Configure which fields are mandatory or optional in the sales form.
            </p>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
              {error}
            </div>
          )}

          {success && (
            <div className="bg-green-50 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
              {success}
            </div>
          )}

          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <div className="space-y-4">
                {fieldConfigurations.map((config) => (
                  <div key={config.fieldName} className="flex items-center justify-between py-3 border-b border-gray-200 last:border-b-0">
                    <div className="flex-1">
                      <h3 className="text-sm font-medium text-gray-900">
                        {FIELD_LABELS[config.fieldName as keyof typeof FIELD_LABELS] || config.fieldName}
                      </h3>
                      <p className="text-sm text-gray-500">
                        Field name: <code className="text-xs bg-gray-100 px-1 py-0.5 rounded">{config.fieldName}</code>
                      </p>
                    </div>
                    <div className="flex items-center">
                      <span className={`mr-3 text-sm ${config.isRequired ? 'text-red-600' : 'text-gray-500'}`}>
                        {config.isRequired ? 'Required' : 'Optional'}
                      </span>
                      <button
                        type="button"
                        className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 ${
                          config.isRequired ? 'bg-primary-600' : 'bg-gray-200'
                        }`}
                        onClick={() => handleToggle(config.fieldName)}
                      >
                        <span className="sr-only">Toggle {config.fieldName}</span>
                        <span
                          className={`pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition duration-200 ease-in-out ${
                            config.isRequired ? 'translate-x-5' : 'translate-x-0'
                          }`}
                        />
                      </button>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-8 flex justify-end space-x-3">
                <Link
                  href="/dashboard"
                  className="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50"
                >
                  Cancel
                </Link>
                <button
                  type="button"
                  onClick={handleSave}
                  disabled={saving}
                  className="bg-primary-600 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-50"
                >
                  {saving ? 'Saving...' : 'Save Configuration'}
                </button>
              </div>
            </div>
          </div>

          <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="text-sm font-medium text-blue-800">About Field Configuration</h3>
            <div className="mt-2 text-sm text-blue-700">
              <ul className="list-disc list-inside space-y-1">
                <li><strong>Required fields</strong> must be filled by agents before they can submit a sale</li>
                <li><strong>Optional fields</strong> can be left empty by agents</li>
                <li><strong>Conditional fields</strong> (like appliance rows) are only validated when their parent section is selected</li>
                <li>Changes take effect immediately for new sales</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}