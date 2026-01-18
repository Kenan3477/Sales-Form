import { NextRequest, NextResponse } from 'next/server'
import { getToken } from 'next-auth/jwt'
import { checkApiRateLimit } from '@/lib/rateLimit'
import { 
  getClientIP, 
  validateRequestSize, 
  validateOrigin, 
  addSecurityHeaders, 
  logSecurityEvent,
  createSecurityContext,
  isBot,
  detectSQLInjection,
  detectXSS
} from '@/lib/security'

export async function middleware(req: NextRequest) {
  const response = NextResponse.next()
  
  // Add security headers to all responses
  addSecurityHeaders(response)
  
  const securityContext = createSecurityContext(req)
  
  // Validate request size
  if (!validateRequestSize(req)) {
    logSecurityEvent('REQUEST_TOO_LARGE', securityContext)
    return new NextResponse('Request too large', { status: 413 })
  }
  
  // Validate origin for non-GET requests (more permissive in production)
  if (req.method !== 'GET' && !validateOrigin(req)) {
    // In production, log the issue but don't block - temporarily for debugging
    if (process.env.NODE_ENV === 'production') {
      logSecurityEvent('INVALID_ORIGIN_WARNING', securityContext, { 
        origin: req.headers.get('origin'),
        host: req.headers.get('host'),
        referer: req.headers.get('referer')
      })
      // Don't block in production for now - just log
    } else {
      logSecurityEvent('INVALID_ORIGIN', securityContext, { origin: req.headers.get('origin') })
      return new NextResponse('Invalid origin', { status: 403 })
    }
  }
  
  // Check for bot traffic on sensitive endpoints (allow bots from localhost in development)
  if (isBot(securityContext.userAgent) && req.nextUrl.pathname.startsWith('/api/')) {
    const isLocalhost = securityContext.ip === '::1' || securityContext.ip === '127.0.0.1' || securityContext.ip === 'unknown'
    if (process.env.NODE_ENV === 'development' && isLocalhost) {
      // Allow bots from localhost in development
      console.log('Allowing bot from localhost in development mode')
    } else {
      logSecurityEvent('BOT_API_ACCESS', securityContext)
      return new NextResponse('Bot access denied', { status: 403 })
    }
  }
  
  // Rate limiting for API endpoints
  if (req.nextUrl.pathname.startsWith('/api/')) {
    const rateLimitResult = await checkApiRateLimit(securityContext.ip)
    
    if (rateLimitResult.blocked) {
      logSecurityEvent('API_RATE_LIMIT_EXCEEDED', securityContext)
      return new NextResponse(
        JSON.stringify({ error: 'Rate limit exceeded', retryAfter: rateLimitResult.reset }),
        { 
          status: 429,
          headers: {
            'Content-Type': 'application/json',
            'Retry-After': Math.ceil((rateLimitResult.reset - Date.now()) / 1000).toString()
          }
        }
      )
    }
    
    // Add rate limit headers
    response.headers.set('X-RateLimit-Remaining', rateLimitResult.remaining.toString())
    response.headers.set('X-RateLimit-Reset', new Date(rateLimitResult.reset).toISOString())
  }
  
  // Check for potential attacks in query parameters
  const url = new URL(req.url)
  const params = Array.from(url.searchParams.entries())
  
  for (const [key, value] of params) {
    if (detectSQLInjection(value) || detectXSS(value)) {
      logSecurityEvent('POTENTIAL_ATTACK_DETECTED', securityContext, { 
        type: 'query_param', 
        key, 
        value: value.substring(0, 100) 
      })
      return new NextResponse('Malicious request detected', { status: 400 })
    }
  }
  
  // Authentication and authorization
  const token = await getToken({ req })
  
  // Allow access to public pages
  if (req.nextUrl.pathname === '/' || req.nextUrl.pathname.startsWith('/auth/')) {
    return response
  }
  
  // Require authentication for all other pages
  if (!token) {
    const loginUrl = new URL('/auth/login', req.url)
    return NextResponse.redirect(loginUrl)
  }

  // Admin-only routes
  if (req.nextUrl.pathname.startsWith('/admin/')) {
    if (token.role !== 'ADMIN') {
      return new NextResponse('Admin access required', { status: 403 })
    }
  }

  return response
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api/auth (NextAuth API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public files (public folder)
     */
    '/((?!api/auth|_next/static|_next/image|favicon.ico|.*\\.).*)',
  ],
}