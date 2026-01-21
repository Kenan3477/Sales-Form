import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { leadDispositionService } from '@/lib/leads/disposition'

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user || (session.user.role !== 'AGENT' && session.user.role !== 'ADMIN')) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await request.json()
    const { leadId } = body

    if (!leadId) {
      return NextResponse.json({ 
        error: 'leadId is required' 
      }, { status: 400 })
    }

    const skipped = await leadDispositionService.skipLead(leadId, session.user.id)

    if (!skipped) {
      return NextResponse.json({ 
        error: 'Unable to skip lead. Lead may not be checked out by this agent.' 
      }, { status: 400 })
    }

    return NextResponse.json({ success: true })

  } catch (error) {
    console.error('Skip lead error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}