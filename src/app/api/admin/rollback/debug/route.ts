import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'

export async function POST(request: NextRequest) {
  try {
    console.log('🔍 DEBUG: Rollback test endpoint called')
    
    // Check authentication
    const session = await getServerSession(authOptions)
    if (!session || session.user.role !== 'ADMIN') {
      console.log('❌ DEBUG: No session or not admin')
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    console.log('✅ DEBUG: Admin authenticated:', session.user.email)

    let body
    try {
      body = await request.json()
      console.log('✅ DEBUG: Request body parsed:', body)
    } catch (error) {
      console.error('❌ DEBUG: Failed to parse JSON:', error)
      return NextResponse.json({ error: 'Invalid JSON' }, { status: 400 })
    }

    const { backupFilename, confirmationCode } = body

    console.log('🔍 DEBUG: Extracted values:')
    console.log('  - backupFilename:', backupFilename)
    console.log('  - confirmationCode:', confirmationCode)

    // Check confirmation code
    if (confirmationCode !== 'ROLLBACK_CONFIRMED_EMERGENCY') {
      console.log('❌ DEBUG: Invalid confirmation code')
      return NextResponse.json({
        error: 'Invalid confirmation code',
        expected: 'ROLLBACK_CONFIRMED_EMERGENCY',
        received: confirmationCode
      }, { status: 400 })
    }

    console.log('✅ DEBUG: Confirmation code is correct')

    // Check if backup filename is provided
    if (!backupFilename) {
      console.log('❌ DEBUG: No backup filename provided')
      return NextResponse.json({ error: 'No backup filename provided' }, { status: 400 })
    }

    console.log('✅ DEBUG: All validations passed - this should work')

    return NextResponse.json({
      success: true,
      message: 'Debug test passed - rollback parameters are valid',
      receivedData: {
        backupFilename,
        confirmationCode,
        user: session.user.email
      }
    })

  } catch (error) {
    console.error('❌ DEBUG: Unexpected error:', error)
    return NextResponse.json({
      error: 'Debug test failed',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}