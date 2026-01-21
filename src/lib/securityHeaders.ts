import { NextRequest, NextResponse } from 'next/server'

// Security headers to prevent information disclosure
export const SECURITY_HEADERS = {
  // Prevent information disclosure through server headers
  'X-Powered-By': '', // Remove default Next.js header
  'Server': 'nginx', // Generic server name
  
  // Security headers
  'X-Content-Type-Options': 'nosniff',
  'X-Frame-Options': 'DENY',
  'X-XSS-Protection': '1; mode=block',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
  
  // HSTS (only in production with HTTPS)
  ...(process.env.NODE_ENV === 'production' ? {
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload'
  } : {}),
}

// Remove sensitive headers that could leak information
export const REMOVE_HEADERS = [
  'x-powered-by',
  'x-vercel-id', 
  'x-vercel-cache',
  'x-matched-path',
  'server'
]

// Sanitize error messages to prevent information disclosure
export function sanitizeErrorMessage(error: any): string {
  // In production, return generic error messages
  if (process.env.NODE_ENV === 'production') {
    if (error?.code === 'ECONNREFUSED' || error?.code === 'ENOTFOUND') {
      return 'Service temporarily unavailable'
    }
    if (error?.name === 'DatabaseError' || error?.name === 'PrismaClientKnownRequestError') {
      return 'Database operation failed'
    }
    if (error?.name === 'ValidationError') {
      return 'Invalid input provided'
    }
    if (error?.status === 401) {
      return 'Authentication required'
    }
    if (error?.status === 403) {
      return 'Access denied'
    }
    if (error?.status === 404) {
      return 'Resource not found'
    }
    if (error?.status === 429) {
      return 'Too many requests'
    }
    
    // Generic fallback
    return 'An error occurred while processing your request'
  } else {
    // In development, show detailed errors for debugging
    return error?.message || 'Unknown error occurred'
  }
}

// Add security headers to response
export function addSecurityHeaders(response: NextResponse): NextResponse {
  // Add security headers
  Object.entries(SECURITY_HEADERS).forEach(([key, value]) => {
    if (value) {
      response.headers.set(key, value)
    }
  })
  
  // Remove sensitive headers
  REMOVE_HEADERS.forEach(header => {
    response.headers.delete(header)
  })
  
  return response
}

// Create secure error response
export function createErrorResponse(
  message: string, 
  status: number = 500,
  details?: any
): NextResponse {
  const sanitizedMessage = sanitizeErrorMessage({ message, status, ...details })
  
  const response = NextResponse.json(
    { 
      error: sanitizedMessage,
      timestamp: new Date().toISOString(),
      // Only include request ID in development
      ...(process.env.NODE_ENV === 'development' && details?.requestId ? {
        requestId: details.requestId
      } : {})
    },
    { status }
  )
  
  return addSecurityHeaders(response)
}

// Wrapper for API routes to add security headers
export function withSecurityHeaders<T extends any[]>(
  handler: (...args: T) => Promise<NextResponse> | NextResponse
) {
  return async (...args: T): Promise<NextResponse> => {
    try {
      const response = await handler(...args)
      return addSecurityHeaders(response)
    } catch (error) {
      console.error('API Error:', error)
      return createErrorResponse('Internal server error', 500, { error })
    }
  }
}

// Check if request contains sensitive information patterns
export function containsSensitiveInfo(data: any): boolean {
  const sensitivePatterns = [
    /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/, // Email
    /\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b/, // Credit card
    /\b\d{3}[\s-]?\d{2}[\s-]?\d{4}\b/, // SSN
    /\b(?:password|pass|pwd|token|key|secret|api[_-]?key)\b/i, // Sensitive fields
    /\b(?:mongodb|postgres|mysql|redis):\/\/[^\s]+/i, // Database URLs
    /\b[A-Za-z0-9]{20,}\b/, // Long tokens/keys
  ]
  
  const dataString = JSON.stringify(data).toLowerCase()
  return sensitivePatterns.some(pattern => pattern.test(dataString))
}

// Log security events
export function logSecurityEvent(
  event: string, 
  request: NextRequest, 
  details?: any
): void {
  const ip = request.headers.get('x-forwarded-for') || 
           request.headers.get('x-real-ip') || 
           'unknown'
  
  const userAgent = request.headers.get('user-agent') || 'unknown'
  
  console.warn(`[SECURITY] ${event}`, {
    ip,
    userAgent,
    url: request.url,
    timestamp: new Date().toISOString(),
    ...details
  })
}