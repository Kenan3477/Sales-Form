import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'
import { hash } from 'bcryptjs'
import { withSecurity } from '@/lib/apiSecurity'
import { logSecurityEvent, createSecurityContext, sanitizeInput } from '@/lib/security'
import * as z from 'zod'

const userUpdateSchema = z.object({
  email: z.string().email('Valid email is required').optional(),
  password: z.string().min(8, 'Password must be at least 8 characters').optional(),
  role: z.enum(['ADMIN', 'AGENT'], {
    errorMap: () => ({ message: 'Role must be ADMIN or AGENT' })
  }).optional(),
  confirmPassword: z.string().optional()
}).refine((data) => {
  if (data.password && !data.confirmPassword) return false
  if (data.password && data.password !== data.confirmPassword) return false
  return true
}, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
})

// GET - Get single user details
async function handleGetUser(request: NextRequest, context: any, { params }: { params: { id: string } }) {
  const securityContext = createSecurityContext(request)
  const { user } = context
  const { id } = params

  try {
    logSecurityEvent('USER_GET_DETAILS', securityContext, {
      userId: user.id,
      targetUserId: id
    })

    const targetUser = await prisma.user.findUnique({
      where: { id },
      select: {
        id: true,
        email: true,
        role: true,
        createdAt: true,
        updatedAt: true,
        _count: {
          select: {
            sales: true
          }
        }
      }
    })

    if (!targetUser) {
      return NextResponse.json({
        error: 'User not found'
      }, { status: 404 })
    }

    return NextResponse.json({
      success: true,
      user: {
        ...targetUser,
        salesCount: targetUser._count.sales
      }
    })

  } catch (error) {
    logSecurityEvent('USER_GET_ERROR', securityContext, {
      error: error instanceof Error ? error.message : 'Unknown error',
      userId: user.id,
      targetUserId: id
    })
    
    console.error('User get error:', error)
    return NextResponse.json(
      { error: 'Failed to fetch user' },
      { status: 500 }
    )
  }
}

// PUT - Update user
async function handleUpdateUser(request: NextRequest, context: any, { params }: { params: { id: string } }) {
  const securityContext = createSecurityContext(request)
  const { user } = context
  const { id } = params

  try {
    const body = await request.json()
    
    logSecurityEvent('USER_UPDATE_ATTEMPT', securityContext, {
      userId: user.id,
      targetUserId: id,
      updateFields: Object.keys(body)
    })

    // Prevent users from updating themselves to avoid lockout
    if (user.id === id && body.role && body.role !== user.role) {
      logSecurityEvent('USER_SELF_ROLE_CHANGE_BLOCKED', securityContext, {
        userId: user.id,
        attemptedRole: body.role
      })
      return NextResponse.json({
        error: 'Cannot change your own role'
      }, { status: 403 })
    }

    // Validate input
    const validation = userUpdateSchema.safeParse(body)
    if (!validation.success) {
      return NextResponse.json({
        error: 'Validation failed',
        details: validation.error.format()
      }, { status: 400 })
    }

    const updateData: any = {}
    const { email, password, role } = validation.data

    if (email) {
      const sanitizedEmail = sanitizeInput(email).toLowerCase()
      
      // Check if email is already taken by another user
      const existingUser = await prisma.user.findFirst({
        where: {
          email: sanitizedEmail,
          NOT: { id }
        }
      })

      if (existingUser) {
        return NextResponse.json({
          error: 'Email already taken by another user'
        }, { status: 409 })
      }

      updateData.email = sanitizedEmail
    }

    if (password) {
      updateData.password = await hash(password, 12)
    }

    if (role) {
      updateData.role = role
    }

    const updatedUser = await prisma.user.update({
      where: { id },
      data: updateData,
      select: {
        id: true,
        email: true,
        role: true,
        updatedAt: true
      }
    })

    logSecurityEvent('USER_UPDATE_SUCCESS', securityContext, {
      userId: user.id,
      targetUserId: id,
      updatedFields: Object.keys(updateData)
    })

    return NextResponse.json({
      success: true,
      user: updatedUser
    })

  } catch (error) {
    logSecurityEvent('USER_UPDATE_ERROR', securityContext, {
      error: error instanceof Error ? error.message : 'Unknown error',
      userId: user.id,
      targetUserId: id
    })
    
    console.error('User update error:', error)
    return NextResponse.json(
      { error: 'Failed to update user' },
      { status: 500 }
    )
  }
}

// DELETE - Delete user
async function handleDeleteUser(request: NextRequest, context: any, { params }: { params: { id: string } }) {
  const securityContext = createSecurityContext(request)
  const { user } = context
  const { id } = params

  try {
    logSecurityEvent('USER_DELETE_ATTEMPT', securityContext, {
      userId: user.id,
      targetUserId: id
    })

    // Prevent users from deleting themselves
    if (user.id === id) {
      logSecurityEvent('USER_SELF_DELETE_BLOCKED', securityContext, {
        userId: user.id
      })
      return NextResponse.json({
        error: 'Cannot delete your own account'
      }, { status: 403 })
    }

    // Check if user exists and get their sales count
    const targetUser = await prisma.user.findUnique({
      where: { id },
      include: {
        _count: {
          select: {
            sales: true
          }
        }
      }
    })

    if (!targetUser) {
      return NextResponse.json({
        error: 'User not found'
      }, { status: 404 })
    }

    // Check if user has sales (optional: you might want to prevent deletion if they have sales)
    if (targetUser._count.sales > 0) {
      logSecurityEvent('USER_DELETE_WITH_SALES_BLOCKED', securityContext, {
        userId: user.id,
        targetUserId: id,
        salesCount: targetUser._count.sales
      })
      return NextResponse.json({
        error: `Cannot delete user with ${targetUser._count.sales} sales records. Transfer or delete sales first.`
      }, { status: 409 })
    }

    // Delete the user
    await prisma.user.delete({
      where: { id }
    })

    logSecurityEvent('USER_DELETE_SUCCESS', securityContext, {
      userId: user.id,
      deletedUserId: id,
      deletedUserEmail: targetUser.email
    })

    return NextResponse.json({
      success: true,
      message: 'User deleted successfully'
    })

  } catch (error) {
    logSecurityEvent('USER_DELETE_ERROR', securityContext, {
      error: error instanceof Error ? error.message : 'Unknown error',
      userId: user.id,
      targetUserId: id
    })
    
    console.error('User delete error:', error)
    return NextResponse.json(
      { error: 'Failed to delete user' },
      { status: 500 }
    )
  }
}

export const GET = withSecurity(handleGetUser, {
  requireAuth: true,
  requireAdmin: true,
  rateLimit: {
    requests: 100,
    windowMs: 60 * 60 * 1000
  },
  logAccess: true
})

export const PUT = withSecurity(handleUpdateUser, {
  requireAuth: true,
  requireAdmin: true,
  rateLimit: {
    requests: 20,
    windowMs: 60 * 60 * 1000
  },
  validateInput: true,
  logAccess: true
})

export const DELETE = withSecurity(handleDeleteUser, {
  requireAuth: true,
  requireAdmin: true,
  rateLimit: {
    requests: 10,
    windowMs: 60 * 60 * 1000
  },
  logAccess: true
})