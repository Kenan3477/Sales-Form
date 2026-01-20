import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { leadWorkflowService } from '@/lib/leads/workflow'

interface RouteParams {
  params: {
    id: string
  }
}

export async function GET(request: NextRequest, { params }: RouteParams) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { id: leadId } = params

    // Only agents can checkout leads, and only their assigned ones
    if (session.user.role !== 'AGENT') {
      return NextResponse.json({ error: 'Only agents can checkout leads' }, { status: 403 })
    }

    const lead = await leadWorkflowService.getLeadWithCheckout(leadId, session.user.id)

    if (!lead) {
      return NextResponse.json({ error: 'Lead not found' }, { status: 404 })
    }

    // Verify lead is assigned to this agent
    if (lead.assignedAgentId !== session.user.id) {
      return NextResponse.json({ error: 'Lead not assigned to this agent' }, { status: 403 })
    }

    return NextResponse.json({ lead })

  } catch (error) {
    console.error('Checkout lead error:', error)
    
    if (error instanceof Error && error.message.includes('being worked on')) {
      return NextResponse.json({ error: error.message }, { status: 409 })
    }
    
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

export async function DELETE(request: NextRequest, { params }: RouteParams) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user || session.user.role !== 'AGENT') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { id: leadId } = params

    const released = await leadWorkflowService.releaseLead(leadId, session.user.id)

    if (!released) {
      return NextResponse.json({ error: 'Unable to release lead' }, { status: 400 })
    }

    return NextResponse.json({ success: true })

  } catch (error) {
    console.error('Release lead error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}