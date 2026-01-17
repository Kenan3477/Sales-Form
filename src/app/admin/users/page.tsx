'use client'

import { useState, useEffect } from 'react'
import { useSession } from 'next-auth/react'
import { redirect } from 'next/navigation'
import AdminNav from '@/components/AdminNav'

interface User {
  id: string
  email: string
  role: 'ADMIN' | 'AGENT'
  createdAt: string
  salesCount?: number
}

interface CreateUserForm {
  email: string
  password: string
  confirmPassword: string
  role: 'ADMIN' | 'AGENT'
}

interface UpdateUserForm {
  email: string
  password: string
  confirmPassword: string
  role: 'ADMIN' | 'AGENT'
}

export default function UsersManagement() {
  const { data: session, status } = useSession()
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [editingUser, setEditingUser] = useState<User | null>(null)
  const [deletingUser, setDeletingUser] = useState<User | null>(null)
  
  const [createForm, setCreateForm] = useState<CreateUserForm>({
    email: '',
    password: '',
    confirmPassword: '',
    role: 'AGENT'
  })

  const [updateForm, setUpdateForm] = useState<UpdateUserForm>({
    email: '',
    password: '',
    confirmPassword: '',
    role: 'AGENT'
  })

  // Redirect if not admin
  if (status === 'loading') {
    return <div className="flex justify-center items-center h-64">Loading...</div>
  }

  if (!session || session.user.role !== 'ADMIN') {
    redirect('/dashboard')
  }

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    try {
      const response = await fetch('/api/users')
      const data = await response.json()
      
      if (response.ok) {
        setUsers(data.users)
      } else {
        setError(data.error || 'Failed to fetch users')
      }
    } catch (err) {
      setError('Network error occurred')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    if (createForm.password !== createForm.confirmPassword) {
      setError('Passwords do not match')
      return
    }

    try {
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(createForm)
      })

      const data = await response.json()

      if (response.ok) {
        setSuccess('User created successfully')
        setCreateForm({
          email: '',
          password: '',
          confirmPassword: '',
          role: 'AGENT'
        })
        setShowCreateForm(false)
        fetchUsers()
      } else {
        setError(data.error || 'Failed to create user')
      }
    } catch (err) {
      setError('Network error occurred')
    }
  }

  const handleUpdateUser = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!editingUser) return

    setError('')
    setSuccess('')

    if (updateForm.password && updateForm.password !== updateForm.confirmPassword) {
      setError('Passwords do not match')
      return
    }

    try {
      const updateData: any = {
        email: updateForm.email,
        role: updateForm.role
      }

      if (updateForm.password) {
        updateData.password = updateForm.password
        updateData.confirmPassword = updateForm.confirmPassword
      }

      const response = await fetch(`/api/users/${editingUser.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updateData)
      })

      const data = await response.json()

      if (response.ok) {
        setSuccess('User updated successfully')
        setEditingUser(null)
        setUpdateForm({
          email: '',
          password: '',
          confirmPassword: '',
          role: 'AGENT'
        })
        fetchUsers()
      } else {
        setError(data.error || 'Failed to update user')
      }
    } catch (err) {
      setError('Network error occurred')
    }
  }

  const handleDeleteUser = async () => {
    if (!deletingUser) return

    setError('')
    setSuccess('')

    try {
      const response = await fetch(`/api/users/${deletingUser.id}`, {
        method: 'DELETE'
      })

      const data = await response.json()

      if (response.ok) {
        setSuccess('User deleted successfully')
        setDeletingUser(null)
        fetchUsers()
      } else {
        setError(data.error || 'Failed to delete user')
      }
    } catch (err) {
      setError('Network error occurred')
    }
  }

  const startEdit = (user: User) => {
    setEditingUser(user)
    setUpdateForm({
      email: user.email,
      password: '',
      confirmPassword: '',
      role: user.role
    })
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <AdminNav />
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="flex justify-center items-center h-64">
            <div className="text-lg">Loading users...</div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <AdminNav />

      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-2xl font-bold">User Management</h1>
            <button
              onClick={() => setShowCreateForm(true)}
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md"
            >
              Add New User
            </button>
          </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {success && (
        <div className="bg-green-50 border border-green-200 text-green-600 px-4 py-3 rounded mb-4">
          {success}
        </div>
      )}

      {/* Create User Modal */}
      {showCreateForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
          <div className="bg-white p-6 rounded-lg w-96">
            <h2 className="text-lg font-semibold mb-4">Create New User</h2>
            <form onSubmit={handleCreateUser}>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2">Email</label>
                <input
                  type="email"
                  value={createForm.email}
                  onChange={(e) => setCreateForm({ ...createForm, email: e.target.value })}
                  className="w-full px-3 py-2 border rounded-md"
                  required
                />
              </div>
              
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2">Password</label>
                <input
                  type="password"
                  value={createForm.password}
                  onChange={(e) => setCreateForm({ ...createForm, password: e.target.value })}
                  className="w-full px-3 py-2 border rounded-md"
                  required
                  minLength={8}
                />
              </div>
              
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2">Confirm Password</label>
                <input
                  type="password"
                  value={createForm.confirmPassword}
                  onChange={(e) => setCreateForm({ ...createForm, confirmPassword: e.target.value })}
                  className="w-full px-3 py-2 border rounded-md"
                  required
                />
              </div>
              
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2">Role</label>
                <select
                  value={createForm.role}
                  onChange={(e) => setCreateForm({ ...createForm, role: e.target.value as 'ADMIN' | 'AGENT' })}
                  className="w-full px-3 py-2 border rounded-md"
                  required
                >
                  <option value="AGENT">Agent</option>
                  <option value="ADMIN">Admin</option>
                </select>
              </div>
              
              <div className="flex justify-end space-x-2">
                <button
                  type="button"
                  onClick={() => {
                    setShowCreateForm(false)
                    setCreateForm({
                      email: '',
                      password: '',
                      confirmPassword: '',
                      role: 'AGENT'
                    })
                  }}
                  className="px-4 py-2 text-gray-600 border rounded-md hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
                >
                  Create User
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Update User Modal */}
      {editingUser && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
          <div className="bg-white p-6 rounded-lg w-96">
            <h2 className="text-lg font-semibold mb-4">Update User</h2>
            <form onSubmit={handleUpdateUser}>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2">Email</label>
                <input
                  type="email"
                  value={updateForm.email}
                  onChange={(e) => setUpdateForm({ ...updateForm, email: e.target.value })}
                  className="w-full px-3 py-2 border rounded-md"
                  required
                />
              </div>
              
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2">New Password (leave blank to keep current)</label>
                <input
                  type="password"
                  value={updateForm.password}
                  onChange={(e) => setUpdateForm({ ...updateForm, password: e.target.value })}
                  className="w-full px-3 py-2 border rounded-md"
                  minLength={8}
                />
              </div>
              
              {updateForm.password && (
                <div className="mb-4">
                  <label className="block text-sm font-medium mb-2">Confirm New Password</label>
                  <input
                    type="password"
                    value={updateForm.confirmPassword}
                    onChange={(e) => setUpdateForm({ ...updateForm, confirmPassword: e.target.value })}
                    className="w-full px-3 py-2 border rounded-md"
                    required
                  />
                </div>
              )}
              
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2">Role</label>
                <select
                  value={updateForm.role}
                  onChange={(e) => setUpdateForm({ ...updateForm, role: e.target.value as 'ADMIN' | 'AGENT' })}
                  className="w-full px-3 py-2 border rounded-md"
                  required
                  disabled={editingUser.id === session?.user?.id} // Prevent changing own role
                >
                  <option value="AGENT">Agent</option>
                  <option value="ADMIN">Admin</option>
                </select>
                {editingUser.id === session?.user?.id && (
                  <p className="text-sm text-gray-500 mt-1">You cannot change your own role</p>
                )}
              </div>
              
              <div className="flex justify-end space-x-2">
                <button
                  type="button"
                  onClick={() => {
                    setEditingUser(null)
                    setUpdateForm({
                      email: '',
                      password: '',
                      confirmPassword: '',
                      role: 'AGENT'
                    })
                  }}
                  className="px-4 py-2 text-gray-600 border rounded-md hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
                >
                  Update User
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {deletingUser && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
          <div className="bg-white p-6 rounded-lg w-96">
            <h2 className="text-lg font-semibold mb-4">Confirm Delete</h2>
            <p className="mb-4">
              Are you sure you want to delete user <strong>{deletingUser.email}</strong>?
              {deletingUser.salesCount && deletingUser.salesCount > 0 && (
                <span className="text-red-600">
                  <br />This user has {deletingUser.salesCount} sales records.
                </span>
              )}
            </p>
            <div className="flex justify-end space-x-2">
              <button
                onClick={() => setDeletingUser(null)}
                className="px-4 py-2 text-gray-600 border rounded-md hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteUser}
                className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Users Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Email
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Role
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Sales Count
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Created At
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {users.map((user) => (
              <tr key={user.id}>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900">{user.email}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    user.role === 'ADMIN' 
                      ? 'bg-purple-100 text-purple-800' 
                      : 'bg-green-100 text-green-800'
                  }`}>
                    {user.role}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {user.salesCount || 0}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {new Date(user.createdAt).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button
                    onClick={() => startEdit(user)}
                    className="text-blue-600 hover:text-blue-900 mr-3"
                  >
                    Edit
                  </button>
                  {user.id !== session?.user?.id && (
                    <button
                      onClick={() => setDeletingUser(user)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {users.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No users found.
        </div>
      )}
        </div>
      </div>
    </div>
  )
}