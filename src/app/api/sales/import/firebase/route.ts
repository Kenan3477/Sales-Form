import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'

interface FirebaseAppliance {
  age: string
  make: string
  model: string
  monthlyCost: number
  type: string
}

interface FirebaseSale {
  agentEmail: string
  agentId: string
  appliances: FirebaseAppliance[]
  contact: {
    address: string
    email: string
    name: string
    phone: string
    postcode: string
  }
  createdAt: string
  notes?: string
  payment: {
    accountNumber: string
    ddDate: string
    sortCode: string
  }
  plan: {
    number: string
    totalCost: number
    type: string
  }
  submittedAt: string
  timestamp: number
  updatedAt: string
  version: number
}

interface FirebaseData {
  exportDate: string
  projectId: string
  databaseUrl: string
  data: {
    sales: { [key: string]: FirebaseSale }
    [key: string]: any
  }
}

export async function POST(request: NextRequest) {
  try {
    // Check authentication
    const session = await getServerSession(authOptions)
    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Check if user is admin
    if (session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Admin access required' }, { status: 403 })
    }

    const formData = await request.formData()
    const file = formData.get('file') as File

    if (!file) {
      return NextResponse.json({ error: 'No file uploaded' }, { status: 400 })
    }

    const fileContent = await file.text()
    let firebaseData: FirebaseData

    try {
      firebaseData = JSON.parse(fileContent)
    } catch (error) {
      return NextResponse.json({ 
        success: false,
        error: 'Invalid JSON format',
        imported: 0,
        total: 0
      }, { status: 400 })
    }

    // Validate Firebase export structure
    if (!firebaseData.data?.sales) {
      return NextResponse.json({ 
        success: false,
        error: 'Invalid Firebase export format. Expected data.sales structure.',
        imported: 0,
        total: 0
      }, { status: 400 })
    }

    const salesEntries = Object.entries(firebaseData.data.sales)
    const processedSales = []
    const errors = []

    console.log(`Processing ${salesEntries.length} Firebase sales`)

    for (let i = 0; i < salesEntries.length; i++) {
      const [firebaseId, saleData] = salesEntries[i]
      
      try {
        // Validate required Firebase fields
        if (!saleData.contact?.name || !saleData.contact?.phone || !saleData.payment?.accountNumber) {
          errors.push({
            row: i + 1,
            firebaseId,
            error: 'Missing required fields: contact.name, contact.phone, or payment.accountNumber'
          })
          continue
        }

        // Split name into first and last name
        const nameParts = saleData.contact.name.trim().split(' ')
        const firstName = nameParts[0] || ''
        const lastName = nameParts.slice(1).join(' ') || 'Unknown'

        // Transform appliances
        const appliances = saleData.appliances?.map(app => ({
          appliance: app.type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
          otherText: app.make !== 'n/a' && app.make !== 'n./a' ? app.make : null,
          coverLimit: 500, // Default cover limit
          cost: app.monthlyCost || 0
        })) || []

        // Calculate coverage types
        const hasAppliances = appliances.length > 0
        const hasBoiler = saleData.plan?.type?.toLowerCase().includes('boiler')
        const boilerCost = hasBoiler ? (saleData.plan.totalCost - appliances.reduce((sum, a) => sum + a.cost, 0)) : 0

        // Parse DD date
        let directDebitDate: Date
        try {
          // Firebase ddDate format: "22 January/1/2026"
          const ddDateStr = saleData.payment.ddDate
          let dateStr = ddDateStr
          
          // Try to clean up the date format
          if (ddDateStr.includes('/')) {
            const parts = ddDateStr.split('/')
            if (parts.length >= 3) {
              dateStr = `${parts[0]} ${parts[2]}` // "22 January 2026"
            }
          }
          
          directDebitDate = new Date(dateStr)
          if (isNaN(directDebitDate.getTime())) {
            // Fallback: use current date + 30 days
            directDebitDate = new Date()
            directDebitDate.setDate(directDebitDate.getDate() + 30)
          }
        } catch (error) {
          directDebitDate = new Date()
          directDebitDate.setDate(directDebitDate.getDate() + 30)
        }

        // Create sale object
        const processedSale = {
          customerFirstName: firstName,
          customerLastName: lastName,
          title: null,
          phoneNumber: saleData.contact.phone,
          email: saleData.contact.email || `${firstName.toLowerCase()}.${lastName.toLowerCase()}@imported.com`,
          notes: saleData.notes || `Imported from Firebase: ${firebaseId}`,
          mailingStreet: saleData.contact.address || null,
          mailingCity: null,
          mailingProvince: null,
          mailingPostalCode: saleData.contact.postcode || null,
          accountName: saleData.contact.name,
          sortCode: saleData.payment.sortCode,
          accountNumber: saleData.payment.accountNumber,
          directDebitDate: directDebitDate,
          applianceCoverSelected: hasAppliances,
          boilerCoverSelected: hasBoiler,
          boilerPriceSelected: hasBoiler ? boilerCost : null,
          totalPlanCost: saleData.plan?.totalCost || 0,
          createdById: session.user.id,
          // Preserve original sale dates from Firebase
          createdAt: new Date(saleData.createdAt || saleData.submittedAt),
          updatedAt: new Date(saleData.updatedAt || saleData.createdAt || saleData.submittedAt),
          appliances: appliances
        }

        processedSales.push(processedSale)
      } catch (error) {
        errors.push({
          row: i + 1,
          firebaseId,
          error: `Processing error: ${error instanceof Error ? error.message : 'Unknown error'}`
        })
      }
    }

    console.log(`Processed ${processedSales.length} sales, ${errors.length} errors`)

    if (errors.length > 0 && processedSales.length === 0) {
      return NextResponse.json({ 
        success: false,
        error: 'No valid sales data found in Firebase export', 
        errors,
        imported: 0,
        total: salesEntries.length
      }, { status: 400 })
    }

    // Save to database
    const results = []
    
    for (const saleData of processedSales) {
      try {
        const sale = await prisma.sale.create({
          data: {
            ...saleData,
            appliances: {
              create: saleData.appliances
            }
          },
          include: {
            appliances: true,
            createdBy: true
          }
        })
        results.push(sale)
      } catch (error) {
        errors.push({
          sale: `${saleData.customerFirstName} ${saleData.customerLastName}`,
          error: `Database error: ${error instanceof Error ? error.message : 'Unknown error'}`
        })
      }
    }

    return NextResponse.json({
      success: true,
      imported: results.length,
      total: salesEntries.length,
      errors: errors.length > 0 ? errors : undefined,
      data: results
    })

  } catch (error) {
    console.error('Firebase import error:', error)
    return NextResponse.json(
      { 
        success: false,
        error: 'Internal server error',
        imported: 0,
        total: 0
      },
      { status: 500 }
    )
  }
}