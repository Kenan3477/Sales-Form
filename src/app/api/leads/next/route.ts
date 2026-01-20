import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { leadWorkflowService } from '@/lib/leads/workflow'

export async function GET(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Only agents can get their next lead
    if (session.user.role !== 'AGENT') {
      return NextResponse.json({ error: 'Only agents can access lead workflow' }, { status: 403 })
    }

    const url = new URL(request.url)
    const includeCallbacks = url.searchParams.get('includeCallbacks') !== 'false'
    const prioritizeCallbacks = url.searchParams.get('prioritizeCallbacks') !== 'false'

    const result = await leadWorkflowService.getNextLead({
      agentId: session.user.id,
      includeCallbacks,
      prioritizeCallbacks
    })

    return NextResponse.json(result)

  } catch (error) {
    console.error('Get next lead error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}