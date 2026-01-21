import { NextRequest, NextResponse } from 'next/server'

// CORS configuration
const PRODUCTION_ORIGINS = [
  'https://sales-form-chi.vercel.app',
  // Add any additional production domains here
]

const DEVELOPMENT_ORIGINS = [
  'http://localhost:3000',
  'http://127.0.0.1:3000',
]

const getAllowedOrigins = (): string[] => {
  const isDev = process.env.NODE_ENV === 'development'
  const baseOrigins = isDev ? [...PRODUCTION_ORIGINS, ...DEVELOPMENT_ORIGINS] : PRODUCTION_ORIGINS
  
  // Add custom origins from environment variable
  const customOrigins = process.env.CORS_ALLOWED_ORIGINS?.split(',').map(o => o.trim()) || []
  
  // Add Vercel preview deployments in development/staging
  if (process.env.VERCEL_URL) {
    baseOrigins.push(`https://${process.env.VERCEL_URL}`)
  }
  
  // Add NextAuth URL if different
  if (process.env.NEXTAUTH_URL && !baseOrigins.includes(process.env.NEXTAUTH_URL)) {
    baseOrigins.push(process.env.NEXTAUTH_URL)
  }
  
  const allOrigins = baseOrigins.concat(customOrigins)
  return Array.from(new Set(allOrigins))
}

export function isAllowedOrigin(origin: string | null): boolean {
  if (!origin) return true // Same-origin requests have no origin header
  
  const allowedOrigins = getAllowedOrigins()
  
  // Exact match
  if (allowedOrigins.includes(origin)) {
    return true
  }
  
  // For development, allow localhost with any port
  if (process.env.NODE_ENV === 'development') {
    if (origin.match(/^https?:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/)) {
      return true
    }
  }
  
  return false
}

export function setCORSHeaders(request: NextRequest, response: NextResponse): void {
  const origin = request.headers.get('origin')
  
  if (isAllowedOrigin(origin)) {
    if (origin) {
      response.headers.set('Access-Control-Allow-Origin', origin)
      response.headers.set('Vary', 'Origin')
    }
  }
  
  // Set other CORS headers
  response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
  response.headers.set('Access-Control-Allow-Headers', 
    'Content-Type, Authorization, X-Requested-With, Accept, Origin, X-CSRF-Token'
  )
  response.headers.set('Access-Control-Max-Age', '86400') // 24 hours
  
  // Only allow credentials for allowed origins
  if (origin && isAllowedOrigin(origin)) {
    response.headers.set('Access-Control-Allow-Credentials', 'true')
  }
}

export function handleCORSPreflight(request: NextRequest): NextResponse | null {
  if (request.method !== 'OPTIONS') {
    return null
  }
  
  const response = new NextResponse(null, { status: 200 })
  setCORSHeaders(request, response)
  return response
}

// Wrapper for API routes that need CORS
export function withCORS(handler: (req: NextRequest) => Promise<NextResponse> | NextResponse) {
  return async (req: NextRequest): Promise<NextResponse> => {
    // Handle preflight
    const preflightResponse = handleCORSPreflight(req)
    if (preflightResponse) {
      return preflightResponse
    }
    
    // Handle actual request
    const response = await handler(req)
    setCORSHeaders(req, response)
    
    return response
  }
}