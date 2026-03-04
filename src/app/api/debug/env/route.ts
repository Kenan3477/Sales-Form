import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    console.log('🔍 Vercel Environment Debug')
    
    const envDebug = {
      NODE_ENV: process.env.NODE_ENV,
      NEXTAUTH_URL: process.env.NEXTAUTH_URL,
      NEXTAUTH_SECRET: process.env.NEXTAUTH_SECRET ? '✅ Set' : '❌ Missing',
      DATABASE_URL: process.env.DATABASE_URL ? '✅ Set' : '❌ Missing',
      EMAIL_USER: process.env.EMAIL_USER,
      EMAIL_PASSWORD: process.env.EMAIL_PASSWORD ? `✅ Set (${process.env.EMAIL_PASSWORD.length} chars)` : '❌ Missing',
      EMAIL_HOST: process.env.EMAIL_HOST,
      EMAIL_PORT: process.env.EMAIL_PORT,
      RESEND_API_KEY: process.env.RESEND_API_KEY ? '✅ Set' : '❌ Missing',
      timestamp: new Date().toISOString(),
      vercelRegion: process.env.VERCEL_REGION || 'unknown',
      vercelUrl: process.env.VERCEL_URL || 'unknown'
    }

    // Test database connection
    let dbStatus = 'unknown'
    try {
      const { prisma } = await import('@/lib/prisma')
      await prisma.$queryRaw`SELECT 1`
      dbStatus = '✅ Connected'
    } catch (dbError) {
      dbStatus = `❌ Failed: ${dbError instanceof Error ? dbError.message : 'Unknown error'}`
    }

    return NextResponse.json({
      status: 'debug',
      environment: envDebug,
      database: dbStatus,
      message: 'Environment debug completed'
    })

  } catch (error) {
    console.error('Debug API error:', error)
    return NextResponse.json({
      error: 'Debug failed',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}