import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { redirect } from 'next/navigation'
import LeadWorkflow from '@/components/leads/LeadWorkflow'

export default async function LeadsWorkflowPage() {
  const session = await getServerSession(authOptions)

  // Redirect non-agents
  if (!session?.user || session.user.role !== 'AGENT') {
    redirect('/dashboard')
  }

  return <LeadWorkflow />
}