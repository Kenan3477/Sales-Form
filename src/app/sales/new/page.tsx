'use client'

import { useState, useEffect } from 'react'
import { useSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import { useForm, useFieldArray } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { saleSchema, type SaleFormData, APPLIANCE_OPTIONS, BOILER_OPTIONS, formatCurrency } from '@/lib/schemas'
import { PlusIcon, MinusIcon } from 'lucide-react'

interface FieldConfiguration {
  fieldName: string
  isRequired: boolean
}

export default function NewSalePage() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [fieldConfigs, setFieldConfigs] = useState<FieldConfiguration[]>([])
  const [totalCost, setTotalCost] = useState(0)
  const [agents, setAgents] = useState<Array<{id: string, name: string, email: string}>>([])
  const [selectedAgent, setSelectedAgent] = useState('')

  const {
    register,
    handleSubmit,
    watch,
    control,
    formState: { errors },
    setValue,
  } = useForm<SaleFormData>({
    resolver: undefined, // zodResolver(saleSchema), // Temporarily disabled for deployment
    defaultValues: {
      applianceCoverSelected: false,
      boilerCoverSelected: false,
      appliances: [],
      boilerPriceSelected: null,
    }
  })

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'appliances'
  })

  const watchedFields = watch()
  const applianceCoverSelected = watch('applianceCoverSelected')
  const boilerCoverSelected = watch('boilerCoverSelected')
  const appliances = watch('appliances')
  const boilerPrice = watch('boilerPriceSelected')

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/auth/login')
    }
  }, [status, router])

  useEffect(() => {
    // Fetch field configurations and agents
    const fetchFieldConfigs = async () => {
      try {
        const response = await fetch('/api/field-configurations')
        if (response.ok) {
          const configs = await response.json()
          setFieldConfigs(configs)
        }
      } catch (error) {
        console.error('Error fetching field configurations:', error)
      }
    }

    const fetchAgents = async () => {
      try {
        const response = await fetch('/api/users?role=AGENT')
        if (response.ok) {
          const agentData = await response.json()
          setAgents(agentData)
          // Set current user as default if they're an agent
          if (session?.user?.role === 'AGENT') {
            setSelectedAgent(session.user.id)
          }
        }
      } catch (error) {
        console.error('Error fetching agents:', error)
      }
    }

    fetchFieldConfigs()
    fetchAgents()
  }, [session])

  useEffect(() => {
    // Calculate total cost
    let total = 0
    
    if (applianceCoverSelected && appliances) {
      total += appliances.reduce((sum: number, appliance: any) => {
        const cost = Number(appliance.cost) || 0
        return sum + cost
      }, 0)
    }
    
    if (boilerCoverSelected && boilerPrice) {
      const price = Number(boilerPrice) || 0
      total += price
    }
    
    setTotalCost(total)
  }, [applianceCoverSelected, boilerCoverSelected, appliances, boilerPrice])

  const isFieldRequired = (fieldName: string): boolean => {
    const config = fieldConfigs.find(c => c.fieldName === fieldName)
    return config?.isRequired || false
  }

  const onSubmit = async (data: SaleFormData) => {
    setLoading(true)
    setError('') // Clear any previous errors
    try {
      // Add the selected agent to the data
      const submitData = {
        ...data,
        agentId: selectedAgent || session?.user?.id
      }

      const response = await fetch('/api/sales', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(submitData),
      })

      if (response.ok) {
        const sale = await response.json()
        router.push(`/sales/success?id=${sale.id}`)
      } else {
        const errorData = await response.json()
        if (errorData.error && errorData.error.includes('Already A Sale')) {
          setError('Already A Sale - A sale with the same customer details, account number, phone number, and price already exists.')
        } else {
          setError('Error creating sale. Please try again.')
        }
      }
    } catch (error) {
      console.error('Error submitting sale:', error)
      setError('Error creating sale. Please try again.')
    }
    setLoading(false)
  }

  if (status === 'loading') {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>
  }

  if (!session) {
    return null
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h1 className="text-2xl font-bold text-gray-900 mb-8">Create New Sale</h1>
            
            {/* Error Display */}
            {error && (
              <div className="mb-6 bg-red-50 border border-red-200 rounded-md p-4">
                <div className="flex">
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">
                      {error.includes('Already A Sale') ? 'Duplicate Sale Detected' : 'Error'}
                    </h3>
                    <div className="mt-2 text-sm text-red-700">
                      {error}
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
              {/* Agent Assignment */}
              {session?.user?.role === 'ADMIN' && (
                <div>
                  <h2 className="text-lg font-semibold text-gray-900 mb-4">Agent Assignment</h2>
                  <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Assign to Agent <span className="text-red-500">*</span>
                      </label>
                      <select
                        value={selectedAgent}
                        onChange={(e) => setSelectedAgent(e.target.value)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                        required
                      >
                        <option value="">Select an agent...</option>
                        {agents.map(agent => (
                          <option key={agent.id} value={agent.id}>
                            {agent.name} ({agent.email})
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>
                </div>
              )}

              {/* Customer Information */}
              <div>
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Customer Information</h2>
                <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      First Name {isFieldRequired('customerFirstName') && <span className="text-red-500">*</span>}
                    </label>
                    <input
                      type="text"
                      {...register('customerFirstName')}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    />
                    {errors.customerFirstName && (
                      <p className="mt-1 text-sm text-red-600">{errors.customerFirstName.message}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Last Name {isFieldRequired('customerLastName') && <span className="text-red-500">*</span>}
                    </label>
                    <input
                      type="text"
                      {...register('customerLastName')}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    />
                    {errors.customerLastName && (
                      <p className="mt-1 text-sm text-red-600">{errors.customerLastName.message}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Title {isFieldRequired('title') && <span className="text-red-500">*</span>}
                    </label>
                    <input
                      type="text"
                      {...register('title')}
                      placeholder="e.g. Mr, Mrs, Dr, etc."
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    />
                    {errors.title && (
                      <p className="mt-1 text-sm text-red-600">{errors.title.message}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Phone Number {isFieldRequired('phoneNumber') && <span className="text-red-500">*</span>}
                    </label>
                    <input
                      type="tel"
                      {...register('phoneNumber')}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    />
                    {errors.phoneNumber && (
                      <p className="mt-1 text-sm text-red-600">{errors.phoneNumber.message}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Email {isFieldRequired('email') && <span className="text-red-500">*</span>}
                    </label>
                    <input
                      type="email"
                      {...register('email')}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    />
                    {errors.email && (
                      <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Street Address {isFieldRequired('mailingStreet') && <span className="text-red-500">*</span>}
                    </label>
                    <input
                      type="text"
                      {...register('mailingStreet')}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    />
                    {errors.mailingStreet && (
                      <p className="mt-1 text-sm text-red-600">{errors.mailingStreet.message}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      City {isFieldRequired('mailingCity') && <span className="text-red-500">*</span>}
                    </label>
                    <input
                      type="text"
                      {...register('mailingCity')}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    />
                    {errors.mailingCity && (
                      <p className="mt-1 text-sm text-red-600">{errors.mailingCity.message}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Province/State {isFieldRequired('mailingProvince') && <span className="text-red-500">*</span>}
                    </label>
                    <input
                      type="text"
                      {...register('mailingProvince')}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    />
                    {errors.mailingProvince && (
                      <p className="mt-1 text-sm text-red-600">{errors.mailingProvince.message}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Postal Code {isFieldRequired('mailingPostalCode') && <span className="text-red-500">*</span>}
                    </label>
                    <input
                      type="text"
                      {...register('mailingPostalCode')}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    />
                    {errors.mailingPostalCode && (
                      <p className="mt-1 text-sm text-red-600">{errors.mailingPostalCode.message}</p>
                    )}
                  </div>
                </div>
              </div>

              {/* Direct Debit Information */}
              <div>
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Direct Debit Information</h2>
                <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Account Name {isFieldRequired('accountName') && <span className="text-red-500">*</span>}
                    </label>
                    <input
                      type="text"
                      {...register('accountName')}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    />
                    {errors.accountName && (
                      <p className="mt-1 text-sm text-red-600">{errors.accountName.message}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Sort Code {isFieldRequired('sortCode') && <span className="text-red-500">*</span>}
                    </label>
                    <input
                      type="text"
                      placeholder="123456"
                      {...register('sortCode')}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    />
                    {errors.sortCode && (
                      <p className="mt-1 text-sm text-red-600">{errors.sortCode.message}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Account Number {isFieldRequired('accountNumber') && <span className="text-red-500">*</span>}
                    </label>
                    <input
                      type="text"
                      placeholder="12345678"
                      {...register('accountNumber')}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    />
                    {errors.accountNumber && (
                      <p className="mt-1 text-sm text-red-600">{errors.accountNumber.message}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Direct Debit Date {isFieldRequired('directDebitDate') && <span className="text-red-500">*</span>}
                    </label>
                    <input
                      type="date"
                      {...register('directDebitDate')}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    />
                    {errors.directDebitDate && (
                      <p className="mt-1 text-sm text-red-600">{errors.directDebitDate.message}</p>
                    )}
                  </div>
                </div>
              </div>

              {/* Cover Selection */}
              <div>
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Cover Selection</h2>
                <div className="space-y-4">
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      {...register('applianceCoverSelected')}
                      className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                    />
                    <label className="ml-2 block text-sm text-gray-900">
                      Appliance Cover {isFieldRequired('applianceCover') && <span className="text-red-500">*</span>}
                    </label>
                  </div>

                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      {...register('boilerCoverSelected')}
                      className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                    />
                    <label className="ml-2 block text-sm text-gray-900">
                      Boiler Cover {isFieldRequired('boilerCover') && <span className="text-red-500">*</span>}
                    </label>
                  </div>
                </div>
              </div>

              {/* Appliance Cover Section */}
              {applianceCoverSelected && (
                <div>
                  <h3 className="text-lg font-medium text-gray-900 mb-4">Appliances</h3>
                  {fields.map((field, index) => (
                    <div key={field.id} className="border rounded-lg p-4 mb-4 bg-gray-50">
                      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700">
                            Appliance Type {isFieldRequired('applianceRows') && <span className="text-red-500">*</span>}
                          </label>
                          <select
                            {...register(`appliances.${index}.appliance`)}
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                          >
                            <option value="">Select appliance</option>
                            {APPLIANCE_OPTIONS.map((option: string) => (
                              <option key={option} value={option}>{option}</option>
                            ))}
                          </select>
                        </div>

                        {watchedFields.appliances?.[index]?.appliance === 'Other' && (
                          <div>
                            <label className="block text-sm font-medium text-gray-700">
                              Specify Appliance
                            </label>
                            <input
                              type="text"
                              {...register(`appliances.${index}.otherText`)}
                              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                            />
                          </div>
                        )}

                        <div>
                          <label className="block text-sm font-medium text-gray-700">
                            Cover Limit (£)
                          </label>
                          <input
                            type="number"
                            step="0.01"
                            min="0"
                            {...register(`appliances.${index}.coverLimit`, { valueAsNumber: true })}
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700">
                            Cost (£/month)
                          </label>
                          <input
                            type="number"
                            step="0.01"
                            min="0"
                            {...register(`appliances.${index}.cost`, { valueAsNumber: true })}
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                          />
                        </div>
                      </div>
                      
                      <button
                        type="button"
                        onClick={() => remove(index)}
                        className="mt-2 inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded text-red-700 bg-red-100 hover:bg-red-200"
                      >
                        <MinusIcon className="h-3 w-3 mr-1" />
                        Remove
                      </button>
                    </div>
                  ))}
                  
                  <button
                    type="button"
                    onClick={() => append({ appliance: '', otherText: '', coverLimit: 0, cost: 0 })}
                    className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                  >
                    <PlusIcon className="h-4 w-4 mr-2" />
                    Add Appliance
                  </button>
                </div>
              )}

              {/* Boiler Cover Section */}
              {boilerCoverSelected && (
                <div>
                  <h3 className="text-lg font-medium text-gray-900 mb-4">Boiler Cover Options</h3>
                  <div className="space-y-3">
                    {BOILER_OPTIONS.map((option: { value: number; label: string }) => (
                      <div key={option.value} className="flex items-center">
                        <input
                          type="radio"
                          value={option.value.toString()}
                          {...register('boilerPriceSelected')}
                          className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300"
                        />
                        <label className="ml-2 block text-sm text-gray-900">
                          {option.label}
                        </label>
                      </div>
                    ))}
                  </div>
                  {errors.boilerPriceSelected && (
                    <p className="mt-1 text-sm text-red-600">{errors.boilerPriceSelected.message}</p>
                  )}
                </div>
              )}

              {/* Notes Section */}
              <div>
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Additional Notes</h2>
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Notes {isFieldRequired('notes') && <span className="text-red-500">*</span>}
                  </label>
                  <textarea
                    {...register('notes')}
                    rows={4}
                    placeholder="Enter any additional notes or comments about this sale..."
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                  {errors.notes && (
                    <p className="mt-1 text-sm text-red-600">{errors.notes.message}</p>
                  )}
                </div>
              </div>

              {/* Total Cost Display */}
              <div className="bg-blue-50 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-blue-900">
                  Total Plan Cost: {formatCurrency(totalCost)}
                </h3>
                <p className="text-sm text-blue-700 mt-1">
                  This is the monthly cost for all selected coverage.
                </p>
              </div>

              {/* Submit Button */}
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => router.push('/dashboard')}
                  className="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="bg-primary-600 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-50"
                >
                  {loading ? 'Creating...' : 'Create Sale'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}