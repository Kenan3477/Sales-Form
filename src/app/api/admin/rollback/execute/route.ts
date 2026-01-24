import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { performDatabaseRollback } from '@/lib/rollback'

export async function POST(request: NextRequest) {
  try {
    // Check authentication
    const session = await getServerSession(authOptions)
    if (!session || session.user.role !== 'ADMIN') {
      console.error('❌ Rollback attempt - Unauthorized access')
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    let requestBody
    try {
      requestBody = await request.json()
    } catch (parseError) {
      console.error('❌ Rollback request - Invalid JSON:', parseError)
      return NextResponse.json({ error: 'Invalid JSON in request body' }, { status: 400 })
    }

    const { backupFilename, confirmationCode } = requestBody

    console.log('🚨 EMERGENCY DATABASE ROLLBACK REQUEST')
    console.log(`👤 Requested by: ${session.user.email}`)
    console.log(`📁 Target backup: ${backupFilename}`)
    console.log(`🔐 Confirmation code provided: ${!!confirmationCode}`)
    console.log(`🔐 Confirmation code value: "${confirmationCode}"`)

    // Safety check - require specific confirmation code
    if (confirmationCode !== 'ROLLBACK_CONFIRMED_EMERGENCY') {
      console.error(`❌ Invalid confirmation code: expected "ROLLBACK_CONFIRMED_EMERGENCY", got "${confirmationCode}"`)
      return NextResponse.json(
        { 
          error: 'Invalid confirmation code. For safety, rollback requires confirmation code: ROLLBACK_CONFIRMED_EMERGENCY',
          requiresConfirmation: true
        },
        { status: 400 }
      )
    }

    if (!backupFilename) {
      console.error('❌ Rollback request - Missing backup filename')
      return NextResponse.json(
        { error: 'Backup filename is required' },
        { status: 400 }
      )
    }

    console.log('⚠️  PROCEEDING WITH DATABASE ROLLBACK - THIS IS IRREVERSIBLE')
    
    // Perform the rollback
    const result = await performDatabaseRollback(backupFilename, confirmationCode)

    if (result.success) {
      console.log('✅ DATABASE ROLLBACK COMPLETED SUCCESSFULLY')
      console.log(`📅 Rolled back to: ${result.rolledBackTo}`)
      console.log(`📊 Records restored: ${result.recordsRestored}`)
      console.log(`🔒 Data integrity verified: ${result.dataIntegrityVerified}`)
      
      return NextResponse.json({
        success: true,
        message: result.message,
        rolledBackTo: result.rolledBackTo,
        recordsRestored: result.recordsRestored,
        dataIntegrityVerified: result.dataIntegrityVerified,
        performedBy: session.user.email,
        timestamp: new Date().toISOString()
      })
    } else {
      console.error('❌ DATABASE ROLLBACK FAILED')
      console.error(`Error: ${result.error}`)
      
      return NextResponse.json(
        { 
          error: result.message,
          details: result.error
        },
        { status: 400 }
      )
    }

  } catch (error) {
    console.error('❌ Database rollback failed:', error)
    return NextResponse.json(
      { 
        error: 'Database rollback failed',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    )
  }
}