import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'
import { hash } from 'bcryptjs'
import { withSecurity } from '@/lib/apiSecurity'
import { logSecurityEvent, createSecurityContext, sanitizeInput, isValidEmail } from '@/lib/security'
import * as z from 'zod'

// Validation schema for user creation/update
const userCreateSchema = z.object({
  email: z.string().email('Valid email is required'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  role: z.enum(['ADMIN', 'AGENT']),
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
})

const userUpdateSchema = z.object({
  email: z.string().email('Valid email is required').optional(),
  password: z.string().min(8, 'Password must be at least 8 characters').optional(),
  role: z.enum(['ADMIN', 'AGENT']).optional(),
  confirmPassword: z.string().optional()
}).refine((data) => {
  if (data.password && !data.confirmPassword) return false
  if (data.password && data.password !== data.confirmPassword) return false
  return true
}, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
})

// GET - List all users (admin only)
async function handleGetUsers(request: NextRequest, context: any) {
  const securityContext = createSecurityContext(request)
  const { user } = context

  try {
    logSecurityEvent('USER_LIST_ACCESS', securityContext, { 
      userId: user.id,
      userRole: user.role 
    })

    const users = await prisma.user.findMany({
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
      },
      orderBy: {
        createdAt: 'desc'
      }
    })

    return NextResponse.json({
      success: true,
      users: users.map(user => ({
        ...user,
        salesCount: user._count.sales
      }))
    })

  } catch (error) {
    logSecurityEvent('USER_LIST_ERROR', securityContext, {
      error: error instanceof Error ? error.message : 'Unknown error',
      userId: user.id
    })
    
    console.error('User list error:', error)
    return NextResponse.json(
      { error: 'Failed to fetch users' },
      { status: 500 }
    )
  }
}

// POST - Create new user (admin only)
async function handleCreateUser(request: NextRequest, context: any) {
  const securityContext = createSecurityContext(request)
  const { user } = context

  try {
    const body = await request.json()
    
    logSecurityEvent('USER_CREATE_ATTEMPT', securityContext, { 
      userId: user.id,
      userRole: user.role,
      newUserEmail: body.email 
    })

    // Validate input
    const validation = userCreateSchema.safeParse(body)
    if (!validation.success) {
      return NextResponse.json({
        error: 'Validation failed',
        details: validation.error.format()
      }, { status: 400 })
    }

    const { email, password, role } = validation.data

    // Additional role validation
    if (!['ADMIN', 'AGENT'].includes(role)) {
      return NextResponse.json({
        error: 'Role must be ADMIN or AGENT'
      }, { status: 400 })
    }

    // Sanitize email
    const sanitizedEmail = sanitizeInput(email).toLowerCase()

    // Check if user already exists
    const existingUser = await prisma.user.findUnique({
      where: { email: sanitizedEmail }
    })

    if (existingUser) {
      logSecurityEvent('USER_CREATE_DUPLICATE', securityContext, {
        userId: user.id,
        attemptedEmail: sanitizedEmail
      })
      return NextResponse.json({
        error: 'User with this email already exists'
      }, { status: 409 })
    }

    // Hash password
    const hashedPassword = await hash(password, 12)

    // Create user
    const newUser = await prisma.user.create({
      data: {
        email: sanitizedEmail,
        password: hashedPassword,
        role: role
      },
      select: {
        id: true,
        email: true,
        role: true,
        createdAt: true
      }
    })

    logSecurityEvent('USER_CREATE_SUCCESS', securityContext, {
      userId: user.id,
      newUserId: newUser.id,
      newUserEmail: newUser.email,
      newUserRole: newUser.role
    })

    return NextResponse.json({
      success: true,
      user: newUser
    }, { status: 201 })

  } catch (error) {
    logSecurityEvent('USER_CREATE_ERROR', securityContext, {
      error: error instanceof Error ? error.message : 'Unknown error',
      userId: user.id
    })
    
    console.error('User creation error:', error)
    return NextResponse.json(
      { error: 'Failed to create user' },
      { status: 500 }
    )
  }
}

export const GET = withSecurity(handleGetUsers, {
  requireAuth: true,
  requireAdmin: true,
  rateLimit: {
    requests: 50,
    windowMs: 60 * 60 * 1000 // 50 requests per hour
  },
  validateInput: true,
  logAccess: true
})

export const POST = withSecurity(handleCreateUser, {
  requireAuth: true,
  requireAdmin: true,
  rateLimit: {
    requests: 10,
    windowMs: 60 * 60 * 1000 // 10 user creations per hour
  },
  validateInput: true,
  logAccess: true
})