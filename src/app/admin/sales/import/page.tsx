import { getServerSession } from 'next-auth'
import { redirect } from 'next/navigation'
import { authOptions } from '@/lib/auth'
import SalesImportForm from '@/components/SalesImportForm'

export default async function SalesImportPage() {
  const session = await getServerSession(authOptions)
  
  if (!session?.user) {
    redirect('/auth/login')
  }

  if (session.user.role !== 'ADMIN') {
    redirect('/dashboard')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Import Sales Data</h1>
          <p className="mt-2 text-gray-600">
            Upload sales data via CSV or JSON files. All imported sales will be formatted according to export requirements.
          </p>
        </div>

        {/* Navigation */}
        <div className="mb-6">
          <nav className="flex space-x-4">
            <a
              href="/admin/sales"
              className="text-blue-600 hover:text-blue-800 underline"
            >
              ← Back to Sales Management
            </a>
          </nav>
        </div>

        {/* Import Form */}
        <SalesImportForm />

        {/* Information Section */}
        <div className="mt-8 bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Import Process</h2>
          
          <div className="space-y-4 text-gray-600">
            <div>
              <h3 className="font-medium text-gray-800">1. Data Validation</h3>
              <p className="text-sm">All uploaded data is validated against required fields and data types.</p>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-800">2. Automatic Processing</h3>
              <p className="text-sm">Sales are automatically processed with:</p>
              <ul className="text-sm ml-4 mt-1 space-y-1">
                <li>• Coverage type detection (appliance/boiler/both)</li>
                <li>• Appliance data parsing</li>
                <li>• Cost calculations</li>
                <li>• Direct debit date formatting</li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-800">3. Export Ready</h3>
              <p className="text-sm">
                Once imported, all sales data will be formatted according to export requirements including:
              </p>
              <ul className="text-sm ml-4 mt-1 space-y-1">
                <li>• Customer Premium calculations</li>
                <li>• Customer Package categorization (appliance/boiler/appliance + boiler)</li>
                <li>• Hardcoded values (Lead Source: FE3, Payment Method: DD, Processor: DD)</li>
                <li>• Proper appliance type and brand mapping</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}