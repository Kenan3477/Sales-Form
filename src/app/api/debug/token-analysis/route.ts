import { NextRequest, NextResponse } from 'next/server'
import { getToken } from 'next-auth/jwt'

export async function GET(request: NextRequest) {
  try {
    // Get all cookies
    const cookies = request.cookies.getAll()
    const sessionToken = request.cookies.get('next-auth.session-token')
    
    // Try different ways to get token
    const token1 = await getToken({ req: request })
    const token2 = await getToken({ req: request, secret: process.env.NEXTAUTH_SECRET })
    const token3 = await getToken({ 
      req: request, 
      secret: process.env.NEXTAUTH_SECRET,
      cookieName: 'next-auth.session-token'
    })
    
    // Try different cookie names
    const token4 = await getToken({ 
      req: request, 
      secret: process.env.NEXTAUTH_SECRET,
      cookieName: '__Secure-next-auth.session-token'
    })
    
    return NextResponse.json({
      cookies: {
        total: cookies.length,
        all: cookies.map(c => ({ name: c.name, hasValue: !!c.value, valueLength: c.value?.length })),
        sessionToken: {
          exists: !!sessionToken,
          name: sessionToken?.name,
          valueLength: sessionToken?.value?.length,
          valuePreview: sessionToken?.value?.substring(0, 50) + '...'
        }
      },
      tokenAttempts: {
        method1_default: { hasToken: !!token1, email: token1?.email },
        method2_withSecret: { hasToken: !!token2, email: token2?.email },
        method3_cookieName: { hasToken: !!token3, email: token3?.email },
        method4_secureCookie: { hasToken: !!token4, email: token4?.email }
      },
      environment: {
        hasSecret: !!process.env.NEXTAUTH_SECRET,
        secretLength: process.env.NEXTAUTH_SECRET?.length,
        hasUrl: !!process.env.NEXTAUTH_URL,
        nodeEnv: process.env.NODE_ENV,
        nextAuthUrl: process.env.NEXTAUTH_URL
      }
    })
    
  } catch (error) {
    return NextResponse.json({
      error: 'Token analysis failed',
      message: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}