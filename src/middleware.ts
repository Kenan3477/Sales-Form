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
  
  // Validate origin for non-GET requests (more permissive for different browsers)
  if (req.method !== 'GET' && !validateOrigin(req)) {
    // Log but don't block in most cases - different browsers/networks need flexibility
    const origin = req.headers.get('origin')
    const host = req.headers.get('host')
    const referer = req.headers.get('referer')
    
    // Only block if it looks clearly malicious
    const isMalicious = origin && (
      !origin.includes(host || '') && 
      !origin.includes('localhost') &&
      !origin.includes('127.0.0.1') &&
      origin.includes('evil') // Basic heuristic
    )
    
    if (isMalicious) {
      logSecurityEvent('BLOCKED_MALICIOUS_ORIGIN', securityContext, { origin, host, referer })
      return new NextResponse('Invalid origin', { status: 403 })
    } else {
      // Just log for monitoring
      logSecurityEvent('ORIGIN_WARNING', securityContext, { origin, host, referer })
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
  
  // Authentication and authorization - v3 with proper cookie handling
  const token = await getToken({ 
    req,
    secret: process.env.NEXTAUTH_SECRET,
    cookieName: process.env.NODE_ENV === 'production' ? '__Secure-next-auth.session-token' : 'next-auth.session-token'
  })
  
  // Debug logging for dashboard access - v3
  if (req.nextUrl.pathname.startsWith('/dashboard')) {
    console.log('🎯 Dashboard access attempt:', {
      path: req.nextUrl.pathname,
      hasToken: !!token,
      tokenDetails: token ? {
        sub: token.sub,
        email: token.email,
        role: token.role,
        exp: token.exp,
        iat: token.iat
      } : null,
      userAgent: req.headers.get('user-agent')?.substring(0, 50),
      cookies: req.cookies.getAll().map(c => ({ name: c.name, hasValue: !!c.value })),
      environment: {
        hasSecret: !!process.env.NEXTAUTH_SECRET,
        hasUrl: !!process.env.NEXTAUTH_URL,
        nodeEnv: process.env.NODE_ENV
      }
    })
  }
  
  // Allow access to public pages and debug endpoints
  if (req.nextUrl.pathname === '/' || 
      req.nextUrl.pathname.startsWith('/auth/') ||
      req.nextUrl.pathname.startsWith('/api/auth/') ||
      req.nextUrl.pathname.startsWith('/api/debug/') ||
      req.nextUrl.pathname.startsWith('/api/health/') ||
      req.nextUrl.pathname.startsWith('/api/clear-all-rate-limits/') ||
      req.nextUrl.pathname.startsWith('/api/seed-production/')) {
    return response
  }
  
  // Require authentication for all other pages
  if (!token) {
    console.log('❌ No token found, redirecting to login:', {
      path: req.nextUrl.pathname,
      cookies: req.cookies.getAll().map(c => ({ name: c.name, hasValue: !!c.value }))
    })
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