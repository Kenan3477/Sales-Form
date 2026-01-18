'use client'

import { useState, useEffect } from 'react'
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
  applianceCoverSelected: boolean
  boilerCoverSelected: boolean
  boilerPriceSelected: number | null
  totalPlanCost: number
  appliances: {
    id: string
    appliance: string
    otherText: string | null
    coverLimit: number
    cost: number
  }[]
}

export default function MySalesPage() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const [sales, setSales] = useState<Sale[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/auth/login')
    }
  }, [status, router])

  useEffect(() => {
    if (session) {
      fetchSales()
    }
  }, [session])

  const fetchSales = async () => {
    try {
      const response = await fetch('/api/sales')
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
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-900">My Sales</h1>
            <p className="mt-2 text-sm text-gray-600">
              View and edit your submitted sales. Click "View/Edit" to view details and make changes.
            </p>
            <p className="mt-2 text-sm text-gray-600">
              View all your submitted sales and their details.
            </p>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
              {error}
            </div>
          )}

          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            {sales.length === 0 ? (
              <div className="text-center py-12">
                <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M34 40h10v-4a6 6 0 00-10.712-3.714M34 40H14m20 0v-4a9.971 9.971 0 00-.712-3.714M14 40H4v-4a6 6 0 0110.712-3.714M14 40v-4a9.971 9.971 0 01.712-3.714M18 20a6 6 0 1112 0c0 1.657-.672 3.157-1.757 4.243M18 20v10h12V20M18 20a6 6 0 016-6 6 6 0 016 6M6 16a6 6 0 1112 0v4"/>
                </svg>
                <h3 className="mt-2 text-sm font-medium text-gray-900">No sales yet</h3>
                <p className="mt-1 text-sm text-gray-500">Get started by creating your first sale.</p>
                <div className="mt-6">
                  <Link
                    href="/sales/new"
                    className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
                  >
                    Create New Sale
                  </Link>
                </div>
              </div>
            ) : (
              <ul className="divide-y divide-gray-200">
                {sales.map((sale) => (
                  <li key={sale.id} className="px-6 py-4">
                    <div className="flex items-center justify-between">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between">
                          <p className="text-sm font-medium text-gray-900 truncate">
                            {sale.customerFirstName} {sale.customerLastName}
                          </p>
                          <div className="flex flex-shrink-0 space-x-2">
                            {sale.applianceCoverSelected && (
                              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                Appliance Cover
                              </span>
                            )}
                            {sale.boilerCoverSelected && (
                              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                Boiler Cover
                              </span>
                            )}
                          </div>
                        </div>
                        <div className="mt-2 flex justify-between">
                          <div className="sm:flex">
                            <p className="flex items-center text-sm text-gray-500">
                              <svg className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                                <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
                              </svg>
                              {sale.email}
                            </p>
                            <p className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0 sm:ml-6">
                              <svg className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd"/>
                              </svg>
                              {new Date(sale.createdAt).toLocaleDateString()}
                            </p>
                          </div>
                          <div className="flex flex-col items-end">
                            <p className="text-lg font-semibold text-gray-900">
                              {formatCurrency(sale.totalPlanCost)}
                            </p>
                            <p className="text-xs text-gray-500">monthly</p>
                          </div>
                        </div>
                        
                        {/* Appliances Summary */}
                        {sale.appliances.length > 0 && (
                          <div className="mt-3">
                            <p className="text-sm text-gray-600">
                              <strong>Appliances:</strong>{' '}
                              {sale.appliances.map(app => 
                                app.appliance === 'Other' ? app.otherText : app.appliance
                              ).join(', ')}
                            </p>
                          </div>
                        )}

                        {/* Boiler Summary */}
                        {sale.boilerCoverSelected && sale.boilerPriceSelected && (
                          <div className="mt-2">
                            <p className="text-sm text-gray-600">
                              <strong>Boiler Cover:</strong> {formatCurrency(sale.boilerPriceSelected)}/month
                            </p>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Sale ID and Actions */}
                    <div className="mt-3 flex justify-between items-center">
                      <p className="text-xs text-gray-400">
                        Sale ID: {sale.id}
                      </p>
                      <div className="flex items-center space-x-3">
                        <p className="text-xs text-gray-400">
                          Phone: {sale.phoneNumber}
                        </p>
                        <Link
                          href={`/sales/${sale.id}`}
                          className="inline-flex items-center px-2.5 py-1.5 border border-blue-300 shadow-sm text-xs leading-4 font-medium rounded text-blue-700 bg-blue-50 hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                        >
                          ✏️ View/Edit
                        </Link>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* Actions */}
          <div className="mt-6 flex justify-end space-x-3">
            <Link
              href="/sales/new"
              className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-md text-sm font-medium"
            >
              Create New Sale
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}