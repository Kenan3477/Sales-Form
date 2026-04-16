import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { CampaignManagementService } from '@/lib/leads/campaign'

const campaignService = new CampaignManagementService()

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { campaignId, agentIds } = await request.json()

    const optimization = await campaignService.optimizeQueue(campaignId, agentIds)
    return NextResponse.json(optimization)
  } catch (error) {
    console.error('Queue optimization error:', error)
    return NextResponse.json({ error: 'Failed to optimize queue' }, { status: 500 })
  }
}