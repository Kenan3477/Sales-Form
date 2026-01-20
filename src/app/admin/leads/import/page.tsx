import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { redirect } from 'next/navigation'
import LeadImport from '@/components/leads/LeadImport'

export default async function LeadsImportPage() {
  const session = await getServerSession(authOptions)

  // Redirect non-admins
  if (!session?.user || session.user.role !== 'ADMIN') {
    redirect('/dashboard')
  }

  return <LeadImport />
}