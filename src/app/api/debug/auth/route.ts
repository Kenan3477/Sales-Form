import { NextRequest, NextResponse } from 'next/server'
import { getToken } from 'next-auth/jwt'

export async function GET(request: NextRequest) {
  try {
    const token = await getToken({ req: request })
    const headers = Object.fromEntries(request.headers.entries())
    
    // Get client info
    const ip = headers['x-forwarded-for'] || headers['x-real-ip'] || 'unknown'
    const userAgent = headers['user-agent'] || 'unknown'
    const origin = headers['origin'] || 'unknown'
    const referer = headers['referer'] || 'unknown'
    const host = headers['host'] || 'unknown'
    
    // Check cookies
    const cookies = request.cookies.getAll()
    const sessionToken = request.cookies.get('next-auth.session-token')
    const csrfToken = request.cookies.get('__Host-next-auth.csrf-token') || request.cookies.get('next-auth.csrf-token')
    
    return NextResponse.json({
      authenticated: !!token,
      user: token ? {
        id: token.sub,
        email: token.email,
        role: token.role
      } : null,
      session: {
        hasSessionToken: !!sessionToken,
        sessionTokenValue: sessionToken?.value?.substring(0, 20) + '...',
        hasCsrfToken: !!csrfToken,
        allCookies: cookies.map(c => ({ name: c.name, hasValue: !!c.value }))
      },
      request: {
        ip,
        userAgent,
        origin,
        referer,
        host,
        url: request.url,
        method: request.method
      },
      environment: {
        nodeEnv: process.env.NODE_ENV,
        nextAuthUrl: process.env.NEXTAUTH_URL,
        hasNextAuthSecret: !!process.env.NEXTAUTH_SECRET
      }
    })
  } catch (error) {
    return NextResponse.json({
      error: 'Debug failed',
      message: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}