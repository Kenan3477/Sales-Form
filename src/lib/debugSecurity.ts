import { NextRequest, NextResponse } from 'next/server'
import { getToken } from 'next-auth/jwt'
import { getServerSession } from 'next-auth/next'
import { authOptions } from '@/lib/auth'

/**
 * CRITICAL SECURITY PROTECTION FOR DEBUG ENDPOINTS
 * 
 * This module ensures debug endpoints are:
 * 1. Disabled in production
 * 2. Require super admin privileges
 * 3. Are rate limited
 * 4. Log all access attempts
 */

interface SecurityCheck {
  isAllowed: boolean
  reason?: string
  statusCode?: number
}

/**
 * Checks if debug endpoints should be accessible
 * Returns false for production or if ENABLE_DEBUG is not explicitly set
 */
export function isDebugEnabled(): boolean {
  // Disable ALL debug endpoints in production
  if (process.env.NODE_ENV === 'production') {
    return false
  }
  
  // Require explicit opt-in for debug mode
  return process.env.ENABLE_DEBUG === 'true'
}

/**
 * Validates if user has super admin privileges for debug access
 */
export async function validateDebugAccess(request: NextRequest): Promise<SecurityCheck> {
  try {
    // First check if debug is enabled at all
    if (!isDebugEnabled()) {
      logSecurityEvent('DEBUG_BLOCKED_PRODUCTION', request)
      return {
        isAllowed: false,
        reason: 'Debug endpoints are disabled in production',
        statusCode: 404 // Return 404 to hide existence
      }
    }

    // Check for valid session
    const session = await getServerSession(authOptions)
    if (!session?.user) {
      logSecurityEvent('DEBUG_BLOCKED_NO_SESSION', request)
      return {
        isAllowed: false,
        reason: 'Authentication required',
        statusCode: 401
      }
    }

    // Check for super admin role (only allow debug access to super admins)
    if (session.user.role !== 'SUPER_ADMIN') {
      logSecurityEvent('DEBUG_BLOCKED_INSUFFICIENT_PRIVILEGES', request, {
        userEmail: session.user.email,
        userRole: session.user.role
      })
      return {
        isAllowed: false,
        reason: 'Insufficient privileges. Super admin access required.',
        statusCode: 403
      }
    }

    // Additional token validation
    const token = await getToken({ req: request })
    if (!token) {
      logSecurityEvent('DEBUG_BLOCKED_INVALID_TOKEN', request)
      return {
        isAllowed: false,
        reason: 'Invalid authentication token',
        statusCode: 401
      }
    }

    // Log successful debug access
    logSecurityEvent('DEBUG_ACCESS_GRANTED', request, {
      userEmail: session.user.email,
      endpoint: request.nextUrl.pathname
    })

    return { isAllowed: true }

  } catch (error) {
    logSecurityEvent('DEBUG_VALIDATION_ERROR', request, { error: String(error) })
    return {
      isAllowed: false,
      reason: 'Security validation failed',
      statusCode: 500
    }
  }
}

/**
 * Security middleware for debug endpoints
 */
export async function secureDebugEndpoint(
  request: NextRequest,
  handler: () => Promise<NextResponse> | NextResponse
): Promise<NextResponse> {
  const securityCheck = await validateDebugAccess(request)
  
  if (!securityCheck.isAllowed) {
    return NextResponse.json(
      { 
        error: securityCheck.reason || 'Access denied',
        timestamp: new Date().toISOString()
      },
      { status: securityCheck.statusCode || 403 }
    )
  }

  try {
    return await handler()
  } catch (error) {
    logSecurityEvent('DEBUG_ENDPOINT_ERROR', request, { error: String(error) })
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

/**
 * Logs security events for debugging and monitoring
 */
function logSecurityEvent(
  event: string, 
  request: NextRequest, 
  details?: Record<string, any>
) {
  const securityEvent = {
    timestamp: new Date().toISOString(),
    event,
    ip: request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || 'unknown',
    userAgent: request.headers.get('user-agent') || 'unknown',
    endpoint: request.nextUrl.pathname,
    method: request.method,
    ...details
  }

  // Always log to console for monitoring
  console.log('[SECURITY EVENT]', JSON.stringify(securityEvent))

  // In production, this should be sent to a security monitoring system
  // TODO: Integrate with your security monitoring service
}

/**
 * Returns a standardized error response that hides sensitive information
 */
export function createSecureErrorResponse(
  message: string = 'Not found',
  statusCode: number = 404
): NextResponse {
  return NextResponse.json(
    {
      error: message,
      timestamp: new Date().toISOString()
    },
    { status: statusCode }
  )
}

/**
 * Rate limiting specifically for debug endpoints
 */
const debugAccessAttempts = new Map<string, number[]>()

export function isDebugRateLimited(request: NextRequest): boolean {
  const ip = request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || 'unknown'
  const now = Date.now()
  const windowMs = 5 * 60 * 1000 // 5 minutes
  const maxAttempts = 10 // Max 10 debug endpoint calls per 5 minutes

  // Clean old attempts
  const attempts = debugAccessAttempts.get(ip) || []
  const recentAttempts = attempts.filter(time => now - time < windowMs)
  
  if (recentAttempts.length >= maxAttempts) {
    logSecurityEvent('DEBUG_RATE_LIMITED', request, { attemptCount: recentAttempts.length })
    return true
  }

  // Record this attempt
  recentAttempts.push(now)
  debugAccessAttempts.set(ip, recentAttempts)
  
  return false
}