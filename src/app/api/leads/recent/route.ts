import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'

export async function GET(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { searchParams } = new URL(request.url)
    const limit = parseInt(searchParams.get('limit') || '10')
    const isAgent = session.user.role === 'AGENT'

    // Build the where clause based on user role
    const whereClause: any = {}
    
    if (isAgent) {
      // Agents only see their assigned leads
      whereClause.assignedAgentId = session.user.id
    }
    
    // Get recent leads
    const leads = await prisma.lead.findMany({
      where: whereClause,
      include: {
        assignedAgent: {
          select: {
            email: true
          }
        },
        dispositionHistory: {
          orderBy: {
            createdAt: 'desc'
          },
          take: 1
        }
      },
      orderBy: {
        createdAt: 'desc'
      },
      take: limit
    })

    // Transform the data to match the expected format
    const transformedLeads = leads.map(lead => ({
      id: lead.id,
      customerFirstName: lead.customerFirstName,
      customerLastName: lead.customerLastName,
      phoneNumber: lead.phoneNumber,
      email: lead.email || '',
      totalPlanCost: lead.totalPlanCost || 0,
      applianceCoverSelected: lead.applianceCoverSelected || false,
      boilerCoverSelected: lead.boilerCoverSelected || false,
      timesContacted: lead.timesContacted || 0,
      status: lead.currentStatus,
      assignedAt: lead.createdAt.toISOString(),
      assignedAgent: lead.assignedAgent?.email
    }))

    return NextResponse.json({
      success: true,
      leads: transformedLeads,
      total: transformedLeads.length
    })

  } catch (error) {
    console.error('Recent leads error:', error)
    return NextResponse.json(
      { error: 'Failed to fetch recent leads' },
      { status: 500 }
    )
  }
}