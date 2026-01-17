'use client'

import Link from 'next/link'
import { useSession } from 'next-auth/react'
import { usePathname } from 'next/navigation'

export default function AdminNav() {
  const { data: session } = useSession()
  const pathname = usePathname()

  const isActive = (path: string) => pathname === path

  return (
    <nav className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/dashboard" className="text-xl font-semibold text-gray-900 hover:text-primary-600">
              Sales Form Portal
            </Link>
            
            {/* Admin Navigation Links */}
            <div className="ml-10 flex items-baseline space-x-4">
              <Link
                href="/admin/sales"
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  isActive('/admin/sales') || pathname?.startsWith('/admin/sales/')
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
                }`}
              >
                Sales Management
              </Link>
              <Link
                href="/admin/users"
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  isActive('/admin/users')
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
                }`}
              >
                User Management
              </Link>
              <Link
                href="/admin/settings"
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  isActive('/admin/settings')
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
                }`}
              >
                Settings
              </Link>
              <Link
                href="/admin/paperwork"
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  isActive('/admin/paperwork') || pathname?.startsWith('/admin/paperwork/')
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
                }`}
              >
                Templates
              </Link>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-700">
              {session?.user?.email} ({session?.user?.role})
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
  )
}

// Named export for compatibility
export { AdminNav }