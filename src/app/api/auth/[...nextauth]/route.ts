import NextAuth from 'next-auth'
import { authOptions } from '@/lib/auth'
import { NextRequest, NextResponse } from 'next/server'
import { checkLoginRateLimit } from '@/lib/rateLimit'
import { logSecurityEvent } from '@/lib/securityHeaders'
import { sanitizeErrorMessage } from '@/lib/securityHeaders'

async function secureHandler(req: NextRequest, res: NextResponse) {
  const ip = req.headers.get('x-forwarded-for') || 
           req.headers.get('x-real-ip') || 
           'unknown'
  
  // Rate limit login attempts
  if (req.method === 'POST' && req.url.includes('/signin')) {
    const rateLimitResult = await checkLoginRateLimit(ip)
    
    if (rateLimitResult.blocked) {
      logSecurityEvent('LOGIN_RATE_LIMIT_EXCEEDED', req)
      return NextResponse.json(
        { error: 'Too many login attempts. Please try again later.' },
        { 
          status: 429,
          headers: {
            'Retry-After': Math.ceil((rateLimitResult.reset - Date.now()) / 1000).toString()
          }
        }
      )
    }
  }
  
  try {
    return NextAuth(authOptions)(req, res)
  } catch (error) {
    console.error('NextAuth error:', error)
    const sanitizedMessage = sanitizeErrorMessage(error)
    return NextResponse.json(
      { error: sanitizedMessage },
      { status: 500 }
    )
  }
}

const handler = NextAuth(authOptions)

export { handler as GET, handler as POST }