import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { redirect } from 'next/navigation'
import Link from 'next/link'
import LeadsOverview from '@/components/leads/LeadsOverview'

export default async function LeadsPage() {
  const session = await getServerSession(authOptions)

  if (!session?.user) {
    redirect('/auth/login')
  }

  // Both admins and agents can access this page
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Leads Management</h1>
          <p className="mt-2 text-gray-600">
            {session.user.role === 'ADMIN' 
              ? 'Manage and oversee all leads in the system'
              : 'View your assigned leads and start selling'
            }
          </p>
        </div>

        {/* Navigation */}
        <div className="mb-6">
          <nav className="flex space-x-4">
            <Link
              href="/dashboard"
              className="text-blue-600 hover:text-blue-800 underline"
            >
              ← Back to Dashboard
            </Link>
            {session.user.role === 'ADMIN' && (
              <>
                <span className="text-gray-300">|</span>
                <Link
                  href="/admin/leads/import"
                  className="text-blue-600 hover:text-blue-800 underline"
                >
                  Import Leads
                </Link>
                <span className="text-gray-300">|</span>
                <Link
                  href="/admin/sales"
                  className="text-blue-600 hover:text-blue-800 underline"
                >
                  Manage Sales
                </Link>
              </>
            )}
          </nav>
        </div>

        {/* Leads Overview Component */}
        <LeadsOverview />
      </div>
    </div>
  )
}