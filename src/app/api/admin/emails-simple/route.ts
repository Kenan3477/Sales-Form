import { NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { SimpleEmailService } from '@/lib/emailServiceSimple'

export async function POST(request: Request) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session?.user?.role || !['ADMIN', 'AGENT'].includes(session.user.role)) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await request.json()
    const { action, documentId, saleId, testEmail, saleIds } = body

    switch (action) {
      case 'test_email':
        if (!testEmail) {
          return NextResponse.json({ error: 'Test email address is required' }, { status: 400 })
        }
        
        const testResult = await SimpleEmailService.testEmail(testEmail)
        return NextResponse.json(testResult)

      case 'send_document':
        if (!documentId || !saleId) {
          return NextResponse.json({ error: 'Document ID and Sale ID are required' }, { status: 400 })
        }
        
        const sendResult = await SimpleEmailService.sendDocumentEmail(documentId, saleId)
        return NextResponse.json(sendResult)

      case 'bulk_send':
        if (!saleIds || !Array.isArray(saleIds)) {
          return NextResponse.json({ error: 'Sale IDs array is required' }, { status: 400 })
        }
        
        const bulkResult = await SimpleEmailService.bulkSendDocuments(saleIds)
        return NextResponse.json(bulkResult)

      default:
        return NextResponse.json({ error: 'Invalid action' }, { status: 400 })
    }
  } catch (error) {
    console.error('Email API error:', error)
    return NextResponse.json({ 
      success: false, 
      error: 'Internal server error' 
    }, { status: 500 })
  }
}

export async function GET() {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session?.user?.role || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Admin access required' }, { status: 401 })
    }

    // Return email configuration status
    const emailConfig = {
      host: process.env.EMAIL_HOST,
      port: process.env.EMAIL_PORT,
      user: process.env.EMAIL_USER,
      configured: !!(process.env.EMAIL_HOST && process.env.EMAIL_USER && process.env.EMAIL_PASSWORD)
    }

    return NextResponse.json({ success: true, config: emailConfig })
  } catch (error) {
    console.error('Email config error:', error)
    return NextResponse.json({ 
      success: false, 
      error: 'Internal server error' 
    }, { status: 500 })
  }
}