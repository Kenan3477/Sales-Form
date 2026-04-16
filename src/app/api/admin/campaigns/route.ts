import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { CampaignManagementService } from '@/lib/leads/campaign'

const campaignService = new CampaignManagementService()

export async function GET(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { searchParams } = new URL(request.url)
    const campaignId = searchParams.get('campaignId')

    if (campaignId) {
      const campaign = await campaignService.getCampaignSettings(campaignId)
      return NextResponse.json(campaign)
    } else {
      const campaigns = await campaignService.listCampaigns()
      return NextResponse.json(campaigns)
    }
  } catch (error) {
    console.error('Campaign GET error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const campaignSettings = await request.json()
    campaignSettings.createdBy = session.user.id

    const savedCampaign = await campaignService.saveCampaignSettings(campaignSettings)
    return NextResponse.json(savedCampaign)
  } catch (error) {
    console.error('Campaign POST error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

export async function PUT(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const campaignSettings = await request.json()
    const savedCampaign = await campaignService.saveCampaignSettings(campaignSettings)
    return NextResponse.json(savedCampaign)
  } catch (error) {
    console.error('Campaign PUT error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}