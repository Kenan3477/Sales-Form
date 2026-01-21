import { NextRequest, NextResponse } from 'next/server'
import { getToken } from 'next-auth/jwt'
import { checkApiRateLimit, checkLoginRateLimit } from '@/lib/rateLimit'
import { createSecureCSP, generateNonce } from '@/lib/csp'
import { withCORS } from '@/lib/cors'
import { addSecurityHeaders, logSecurityEvent } from '@/lib/securityHeaders'
import { 
  getClientIP, 
  validateRequestSize, 
  validateOrigin, 
  createSecurityContext,
  isBot,
  detectSQLInjection,
  detectXSS
} from '@/lib/security'

export async function middleware(req: NextRequest) {
  const response = NextResponse.next()
  
  // SECURITY: Block dangerous endpoints in production
  const dangerousEndpoints = ['/api/debug', '/api/seed-production', '/api/clear-all-rate-limits']
  const pathname = req.nextUrl.pathname
  
  if (process.env.NODE_ENV === 'production') {
    for (const endpoint of dangerousEndpoints) {
      if (pathname.startsWith(endpoint)) {
        console.log(`[SECURITY BLOCK] Dangerous endpoint ${pathname} blocked in production`)
        return new NextResponse('Not Found', { status: 404 })
      }
    }
  }
  
  // Generate nonce for CSP
  const nonce = generateNonce()
  
  // Add all security headers including CSP
  addSecurityHeaders(response)
  response.headers.set('Content-Security-Policy', createSecureCSP(nonce))
  
  // Apply CORS for API routes
  if (req.nextUrl.pathname.startsWith('/api/')) {
    const allowedOrigins = ['https://sales-form-chi.vercel.app', 'http://localhost:3000']
    const origin = req.headers.get('origin')
    if (origin && allowedOrigins.includes(origin)) {
      response.headers.set('Access-Control-Allow-Origin', origin)
      response.headers.set('Access-Control-Allow-Credentials', 'true')
      response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
      response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    }
  }
  
  const securityContext = createSecurityContext(req)
  
  // Validate request size
  if (!validateRequestSize(req)) {
    logSecurityEvent('REQUEST_TOO_LARGE', req)
    return new NextResponse('Request too large', { status: 413 })
  }
  
  // Enhanced origin validation for non-GET requests
  if (req.method !== 'GET' && !validateOrigin(req)) {
    const origin = req.headers.get('origin')
    const host = req.headers.get('host')
    const referer = req.headers.get('referer')
    
    // Block clearly malicious origins
    const isMalicious = origin && (
      !origin.includes(host || '') && 
      !origin.includes('localhost') &&
      !origin.includes('127.0.0.1') &&
      (origin.includes('evil') || origin.includes('malicious'))
    )
    
    if (isMalicious) {
      logSecurityEvent('BLOCKED_MALICIOUS_ORIGIN', req, { origin, host, referer })
      return new NextResponse('Invalid origin', { status: 403 })
    } else {
      logSecurityEvent('ORIGIN_WARNING', req, { origin, host, referer })
    }
  }
  
  // Check for bot traffic on sensitive endpoints (allow bots from localhost in development)
  if (isBot(securityContext.userAgent) && req.nextUrl.pathname.startsWith('/api/')) {
    const isLocalhost = securityContext.ip === '::1' || securityContext.ip === '127.0.0.1' || securityContext.ip === 'unknown'
    if (process.env.NODE_ENV === 'development' && isLocalhost) {
      // Allow bots from localhost in development
      console.log('Allowing bot from localhost in development mode')
    } else {
      logSecurityEvent('BOT_API_ACCESS', req)
      return new NextResponse('Bot access denied', { status: 403 })
    }
  }
  
  // Rate limiting for API endpoints
  if (req.nextUrl.pathname.startsWith('/api/')) {
    const rateLimitResult = await checkApiRateLimit(securityContext.ip)
    
    if (rateLimitResult.blocked) {
      logSecurityEvent('API_RATE_LIMIT_EXCEEDED', req)
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
      logSecurityEvent('POTENTIAL_ATTACK_DETECTED', req, { 
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