import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'
import Papa from 'papaparse'

interface ImportSaleData {
  // Customer information
  customerFirstName: string
  customerLastName: string
  title?: string
  phoneNumber: string
  email: string
  notes?: string

  // Address information
  mailingStreet?: string
  mailingCity?: string
  mailingProvince?: string
  mailingPostalCode?: string

  // Direct debit information
  accountName: string
  sortCode: string
  accountNumber: string
  directDebitDate: string // Will be converted to Date

  // Coverage selection
  applianceCoverSelected: boolean
  boilerCoverSelected: boolean
  boilerPriceSelected?: number

  // Total cost
  totalPlanCost: number

  // Appliances (can be JSON string or separate fields)
  appliances?: Array<{
    appliance: string
    otherText?: string
    coverLimit: number
    cost: number
  }>

  // Alternative appliance fields (for CSV compatibility)
  appliance1?: string
  appliance1Cost?: number
  appliance1CoverLimit?: number
  appliance2?: string
  appliance2Cost?: number
  appliance2CoverLimit?: number
  appliance3?: string
  appliance3Cost?: number
  appliance3CoverLimit?: number
  appliance4?: string
  appliance4Cost?: number
  appliance4CoverLimit?: number
  appliance5?: string
  appliance5Cost?: number
  appliance5CoverLimit?: number
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
    const format = formData.get('format') as string // 'csv' or 'json'

    if (!file) {
      return NextResponse.json({ error: 'No file uploaded' }, { status: 400 })
    }

    const fileContent = await file.text()
    let salesData: ImportSaleData[] = []

    // Parse based on format
    if (format === 'csv') {
      const parseResult = Papa.parse(fileContent, {
        header: true,
        skipEmptyLines: true,
        transformHeader: (header) => header.trim()
      })

      if (parseResult.errors.length > 0) {
        return NextResponse.json({ 
          error: 'CSV parsing error', 
          details: parseResult.errors 
        }, { status: 400 })
      }

      salesData = parseResult.data as ImportSaleData[]
    } else if (format === 'json') {
      try {
        const jsonData = JSON.parse(fileContent)
        salesData = Array.isArray(jsonData) ? jsonData : [jsonData]
      } catch (error) {
        return NextResponse.json({ 
          error: 'Invalid JSON format' 
        }, { status: 400 })
      }
    } else {
      return NextResponse.json({ 
        error: 'Unsupported format. Use csv or json' 
      }, { status: 400 })
    }

    // Process and validate each sale
    const processedSales = []
    const errors = []

    for (let i = 0; i < salesData.length; i++) {
      const saleData = salesData[i]
      
      try {
        // Validate required fields
        const requiredFields = [
          'customerFirstName', 'customerLastName', 'phoneNumber', 'email',
          'accountName', 'sortCode', 'accountNumber', 'directDebitDate', 'totalPlanCost'
        ]
        
        const missingFields = requiredFields.filter(field => !saleData[field as keyof ImportSaleData])
        if (missingFields.length > 0) {
          errors.push({
            row: i + 1,
            error: `Missing required fields: ${missingFields.join(', ')}`
          })
          continue
        }

        // Process appliances
        const appliances = []
        
        if (saleData.appliances && Array.isArray(saleData.appliances)) {
          // Use appliances array if provided
          appliances.push(...saleData.appliances)
        } else {
          // Check individual appliance fields (for CSV compatibility)
          for (let j = 1; j <= 5; j++) {
            const applianceField = saleData[`appliance${j}` as keyof ImportSaleData] as string
            const costField = saleData[`appliance${j}Cost` as keyof ImportSaleData] as number
            const coverLimitField = saleData[`appliance${j}CoverLimit` as keyof ImportSaleData] as number
            
            if (applianceField && costField && coverLimitField) {
              appliances.push({
                appliance: applianceField,
                otherText: null,
                coverLimit: Number(coverLimitField),
                cost: Number(costField)
              })
            }
          }
        }

        // Create sale object
        const processedSale = {
          customerFirstName: saleData.customerFirstName,
          customerLastName: saleData.customerLastName,
          title: saleData.title || null,
          phoneNumber: saleData.phoneNumber,
          email: saleData.email,
          notes: saleData.notes || null,
          mailingStreet: saleData.mailingStreet || null,
          mailingCity: saleData.mailingCity || null,
          mailingProvince: saleData.mailingProvince || null,
          mailingPostalCode: saleData.mailingPostalCode || null,
          accountName: saleData.accountName,
          sortCode: saleData.sortCode,
          accountNumber: saleData.accountNumber,
          directDebitDate: new Date(saleData.directDebitDate),
          applianceCoverSelected: Boolean(saleData.applianceCoverSelected) || appliances.length > 0,
          boilerCoverSelected: Boolean(saleData.boilerCoverSelected) || Boolean(saleData.boilerPriceSelected),
          boilerPriceSelected: saleData.boilerPriceSelected ? Number(saleData.boilerPriceSelected) : null,
          totalPlanCost: Number(saleData.totalPlanCost),
          createdById: session.user.id,
          appliances: appliances
        }

        processedSales.push(processedSale)
      } catch (error) {
        errors.push({
          row: i + 1,
          error: `Processing error: ${error instanceof Error ? error.message : 'Unknown error'}`
        })
      }
    }

    if (errors.length > 0 && processedSales.length === 0) {
      return NextResponse.json({ 
        error: 'No valid sales data found', 
        errors 
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
      total: salesData.length,
      errors: errors.length > 0 ? errors : undefined,
      data: results
    })

  } catch (error) {
    console.error('Import error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}