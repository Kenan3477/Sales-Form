import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { redirect } from 'next/navigation'
import AdminNav from '@/components/AdminNav'
import CampaignDashboard from '@/components/campaign/CampaignDashboard'
import { CampaignManagementService } from '@/lib/leads/campaign'

const campaignService = new CampaignManagementService()

export default async function CampaignManagementPage() {
  const session = await getServerSession(authOptions)

  if (!session?.user || session.user.role !== 'ADMIN') {
    redirect('/dashboard')
  }

  // Fetch campaigns data
  const campaigns = await campaignService.listCampaigns()
  const activeCampaign = campaigns.find(c => c.isActive) || null

  return (
    <div className="min-h-screen bg-gray-100">
      <AdminNav />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <CampaignDashboard 
          campaigns={campaigns}
          activeCampaign={activeCampaign}
        />
      </div>
    </div>
  )
}