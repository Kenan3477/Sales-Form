import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { listAvailableRollbackPoints } from '@/lib/rollback'

export async function GET(request: NextRequest) {
  try {
    // Check authentication
    const session = await getServerSession(authOptions)
    if (!session || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    console.log('🔄 Admin requesting rollback points list')
    console.log(`👤 Requested by: ${session.user.email}`)

    const rollbackPoints = await listAvailableRollbackPoints()

    return NextResponse.json({
      success: true,
      rollbackPoints: rollbackPoints.map((point: any) => ({
        filename: point.filename,
        timestamp: point.timestamp,
        size: point.size,
        recordCount: point.recordCount,
        dataIntegrityVerified: point.dataIntegrityVerified,
        displayName: `${new Date(point.timestamp).toLocaleString()} (${point.recordCount} records, ${point.size})`
      }))
    })

  } catch (error) {
    console.error('❌ Failed to list rollback points:', error)
    return NextResponse.json(
      { 
        error: 'Failed to list rollback points',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    )
  }
}