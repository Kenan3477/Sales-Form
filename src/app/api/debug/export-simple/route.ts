import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'

export async function POST(request: NextRequest) {
  try {
    console.log('Export POST endpoint called')
    
    const session = await getServerSession(authOptions)
    
    if (!session || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await request.json()
    console.log('Received body:', Object.keys(body))
    
    return NextResponse.json({ 
      success: true, 
      message: 'Export endpoint is working',
      receivedData: {
        hasFilters: !!body.filters,
        hasSelectedIds: !!(body.selectedIds && body.selectedIds.length > 0),
        hasExcludeCustomers: !!(body.excludeCustomers && body.excludeCustomers.length > 0)
      }
    })
    
  } catch (error) {
    console.error('Export POST error:', error)
    return NextResponse.json({ 
      error: 'Internal server error',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}

export async function GET() {
  return NextResponse.json({ 
    message: 'Export GET endpoint is working' 
  })
}