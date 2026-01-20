import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { leadDispositionService } from '@/lib/leads/disposition'
import { LeadStatus } from '@prisma/client'

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user || session.user.role !== 'AGENT') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await request.json()
    const { leadId, status, notes, callbackAt } = body

    // Validate required fields
    if (!leadId || !status) {
      return NextResponse.json({ 
        error: 'leadId and status are required' 
      }, { status: 400 })
    }

    // Validate status
    const validStatuses: LeadStatus[] = [
      'CALLED_NO_ANSWER', 
      'CALLBACK', 
      'SALE_MADE', 
      'CANCELLED', 
      'DO_NOT_CALL'
    ]
    
    if (!validStatuses.includes(status)) {
      return NextResponse.json({ 
        error: `Invalid status. Must be one of: ${validStatuses.join(', ')}` 
      }, { status: 400 })
    }

    // Validate callback date if required
    let parsedCallbackAt: Date | undefined
    if (status === 'CALLBACK') {
      if (!callbackAt) {
        return NextResponse.json({ 
          error: 'callbackAt is required for CALLBACK status' 
        }, { status: 400 })
      }
      
      parsedCallbackAt = new Date(callbackAt)
      if (isNaN(parsedCallbackAt.getTime())) {
        return NextResponse.json({ 
          error: 'Invalid callbackAt date format' 
        }, { status: 400 })
      }
      
      if (parsedCallbackAt <= new Date()) {
        return NextResponse.json({ 
          error: 'Callback date must be in the future' 
        }, { status: 400 })
      }
    }

    // Process disposition
    const result = await leadDispositionService.disposeLead({
      leadId,
      agentId: session.user.id,
      status,
      notes,
      callbackAt: parsedCallbackAt
    })

    if (!result.success) {
      return NextResponse.json({ error: result.error }, { status: 400 })
    }

    return NextResponse.json({
      success: true,
      lead: result.lead,
      sale: result.sale // Only present for SALE_MADE disposition
    })

  } catch (error) {
    console.error('Disposition error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}