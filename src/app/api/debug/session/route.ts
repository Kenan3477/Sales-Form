import { NextRequest, NextResponse } from 'next/server'
import { getToken } from 'next-auth/jwt'
import { getServerSession } from 'next-auth/next'
import { authOptions } from '@/lib/auth'

export async function GET(request: NextRequest) {
  try {
    // Check JWT token
    const token = await getToken({ req: request })
    
    // Check server session
    const session = await getServerSession(authOptions)
    
    // Get cookies
    const cookies = request.cookies.getAll()
    const sessionTokenCookie = request.cookies.get('next-auth.session-token')
    const csrfTokenCookie = request.cookies.get('__Host-next-auth.csrf-token') || request.cookies.get('next-auth.csrf-token')
    
    // Get headers
    const headers = Object.fromEntries(request.headers.entries())
    
    return NextResponse.json({
      middleware_check: {
        hasToken: !!token,
        token: token ? {
          sub: token.sub,
          email: token.email,
          role: token.role,
          exp: token.exp,
          iat: token.iat
        } : null
      },
      server_session: {
        hasSession: !!session,
        session: session ? {
          user: session.user,
          expires: session.expires
        } : null
      },
      cookies: {
        total: cookies.length,
        sessionToken: {
          exists: !!sessionTokenCookie,
          name: sessionTokenCookie?.name,
          hasValue: !!sessionTokenCookie?.value,
          valueLength: sessionTokenCookie?.value?.length
        },
        csrfToken: {
          exists: !!csrfTokenCookie,
          name: csrfTokenCookie?.name
        },
        allCookieNames: cookies.map(c => c.name)
      },
      request_info: {
        url: request.url,
        method: request.method,
        userAgent: headers['user-agent'],
        origin: headers['origin'],
        referer: headers['referer']
      },
      environment: {
        nodeEnv: process.env.NODE_ENV,
        nextAuthUrl: process.env.NEXTAUTH_URL,
        hasNextAuthSecret: !!process.env.NEXTAUTH_SECRET,
        nextAuthSecretLength: process.env.NEXTAUTH_SECRET?.length
      }
    })
  } catch (error) {
    return NextResponse.json({
      error: 'Session check failed',
      message: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}