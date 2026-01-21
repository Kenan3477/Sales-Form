import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { redirect } from 'next/navigation'
import LeadWorkflow from '@/components/leads/LeadWorkflow'

export default async function LeadsWorkflowPage() {
  const session = await getServerSession(authOptions)

  // Require authentication
  if (!session?.user) {
    redirect('/auth/login')
  }

  // Allow both agents and admins to access workflow
  if (session.user.role !== 'AGENT' && session.user.role !== 'ADMIN') {
    redirect('/dashboard')
  }

  return <LeadWorkflow />
}