import NextAuth from 'next-auth'
import { authOptions } from '@/lib/auth'
import { NextRequest, NextResponse } from 'next/server'
import { checkLoginRateLimit } from '@/lib/rateLimit'
import { getClientIP, logSecurityEvent, createSecurityContext } from '@/lib/security'

async function secureHandler(req: NextRequest, res: NextResponse) {
  const securityContext = createSecurityContext(req)
  
  // Rate limit login attempts
  if (req.method === 'POST' && req.url.includes('/signin')) {
    const rateLimitResult = await checkLoginRateLimit(securityContext.ip)
    
    if (rateLimitResult.blocked) {
      logSecurityEvent('LOGIN_RATE_LIMIT_EXCEEDED', securityContext)
      return NextResponse.json(
        { error: 'Too many login attempts. Please try again later.' },
        { status: 429 }
      )
    }
  }
  
  return NextAuth(authOptions)(req, res)
}

const handler = NextAuth(authOptions)

export { handler as GET, handler as POST }