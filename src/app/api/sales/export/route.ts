import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '../../../../lib/auth'
import { prisma } from '../../../../lib/prisma'

export async function GET(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const searchParams = request.nextUrl.searchParams
    const dateFrom = searchParams.get('dateFrom')
    const dateTo = searchParams.get('dateTo')
    const agentFilter = searchParams.get('agent')
    const ids = searchParams.getAll('ids') // Get array of selected IDs

    let whereClause: any = {}

    // If specific IDs are provided, use those instead of other filters
    if (ids && ids.length > 0) {
      whereClause.id = {
        in: ids
      }
    } else {
      // Admin filters (only apply when not selecting specific IDs)
      if (agentFilter) {
        whereClause.createdById = agentFilter
      }

      // Date filters (only apply when not selecting specific IDs)
      if (dateFrom || dateTo) {
        whereClause.createdAt = {}
        if (dateFrom) {
          whereClause.createdAt.gte = new Date(dateFrom)
        }
        if (dateTo) {
          whereClause.createdAt.lte = new Date(dateTo + 'T23:59:59.999Z')
        }
      }
    }

    const sales = await prisma.sale.findMany({
      where: whereClause,
      include: {
        appliances: true,
        createdBy: {
          select: {
            id: true,
            email: true,
          }
        }
      },
      orderBy: {
        createdAt: 'desc'
      }
    })

    // Generate CSV headers - Complete CRM format
    const headers = [
      'Record Id',
      'Customers Owner.id',
      'Customers Owner',
      'Lead Source',
      'First Name',
      'Last Name',
      'Customers Name',
      'Email',
      'Title',
      'Phone',
      'Mobile',
      'Date of Birth',
      'Modified By.id',
      'Modified By',
      'Modified Time',
      'Salutation',
      'Last Activity Time',
      'Mailing Street',
      'Mailing City',
      'Mailing Province',
      'Mailing Postal Code',
      'Description',
      'Tag',
      'Unsubscribed Mode',
      'Unsubscribed Time',
      'Change Log Time',
      'Locked',
      'Last Enriched Time',
      'Enrich Status',
      'Payment Method',
      'Status',
      'Created Date',
      'SortCode',
      'Acc Number',
      'CVC',
      'EXP Date',
      'Card Number',
      'LeadIdCPY',
      'Plain Phone',
      'Customer Premium',
      'Package Excess',
      'Last Service Date',
      'Boiler Make',
      'Pre Existing Issue',
      'Boiler Age',
      'Cancellation Notes',
      'Renewal Date',
      'Cancellation Fee',
      'Date of renewal notification',
      'Lead Sales Agent',
      'Date of Sale',
      'First Line Add',
      'Customer Package',
      'Cancellation status',
      'Type of renewal notification',
      'First DD Date',
      'DD Amount',
      'Residential Status',
      'Plan Reference Number',
      'Brand',
      'Processor',
      'Appliance 2 Age',
      'Appliance 1 Brand',
      'Appliance 5 Type',
      'Appliance 4 Type',
      'Appliance 3 Type',
      'Appliance 1 Age',
      'Appliance 5 Brand',
      'Appliance 4 Brand',
      'Appliance 3 Brand',
      'Appliance 5 Age',
      'Appliance 4 Age',
      'Appliance 2 Type',
      'Appliance 1 Type',
      'Appliance 2 Brand',
      'Appliance 3 Age',
      'TV Value',
      'TV Brand',
      'TV Size',
      'TV Age',
      'Sales Office Name',
      'Affiliate Reference',
      'Free Offer Period_Months',
      'Cancellation Agent',
      'Remaining Payments Due',
      'Cancellation Reason',
      'Welcome Letter Sent Date',
      'Date of CNR',
      'Contact Attempts',
      'Last Contact Date',
      'Resend Welcome Pack',
      'Resend Method',
      'Cancelled Date',
      'Call Notes',
      'Product sold',
      'Customer Upgraded',
      'Preferred Payment Date',
      'Last 2 Acc Number (Post Docs)',
      'DD Originator Reference',
      'Authorised Persons on Account',
      'Customer Preferences',
      'Details of Vulnerabilities (if any)',
      'POA',
      'Appliance 6 Age',
      'Appliance 6 Type',
      'Appliance 6 Brand',
      'Appliance 7 Brand',
      'Appliance 7 Type',
      'Appliance 7 Age',
      'Appliance 8 Type',
      'Appliance 8 Brand',
      'Appliance 8 Age',
      'Reduced price exp date',
      'Reduced Price',
      'TV Model Number',
      'Contacted for TV Information',
      'Boiler 2 Age',
      'Boiler 2 Make',
      'TV 2 Value',
      'TV 2 -Age',
      'TV 2 Model Number',
      'TV 2 Brand',
      'TV 2 - Size',
      'Boiler Package Price (Internal)',
      'Single App Price (Internal)',
      'App Bundle Price (Internal)',
      'Landlord Boiler Package Price (Internal)',
      'Appliance 9 Type',
      'Appliance 9 Brand',
      'Appliance 9 Age',
      'Multi Package Discount',
      'TV Monthly Premium',
      'Boiler 3-Months Free',
      'Appliance 5 Value',
      'Appliance 6 Value',
      'Appliance 4 Value',
      'Appliance 2 Value',
      'Appliance 3 Value',
      'Appliance 1 Value',
      'Appliance 9 Value',
      'Appliance 7 Value',
      'Appliance 8 Value',
      'GC Mandate ID',
      'Reinstated Date',
      'Payment Status',
      'Date of last payment status',
      'Appliance 10 Type',
      'Appliance 10 Brand',
      'Appliance 10 Age',
      'Appliance 10 Value',
      'Plan Start Date',
      'Months Free Provided',
      'Sale Approved',
      'GC Bank Account ID',
      'GC Customer ID',
      'Connected To.module',
      'Connected To.id',
      'GC Subscription Status',
      'GC Subscription ID',
      'GC API Status',
      'GC Mandate Status',
      'GC Payment Status Update',
      'GC Payment ID',
      'GC Last Event ID',
      'GC Last Webhook ID',
      'GC Last Cause',
      'GC Last Description',
      'GC Last Received At Date',
      'GC Last Resource Type',
      'GS Manual Update All Status',
      'GC Payment ID Scheduled To Refund',
      'GC Last Payment Refunded',
      'Cancellation Fee Taken'
    ]

    // Generate CSV rows
    const rows = sales.map((sale: any) => {
      const createdAt = new Date(sale.createdAt)
      const directDebitDate = new Date(sale.directDebitDate)
      
      // Calculate internal pricing
      const singleAppPrice = sale.appliances.reduce((sum: number, app: any) => sum + Number(app.cost), 0)
      const boilerPrice = sale.boilerCoverSelected && sale.boilerPriceSelected ? Number(sale.boilerPriceSelected) : 0
      
      const row = [
        '', // Record Id - blank as requested
        '', // Customers Owner.id - blank
        'Kenan', // Customers Owner - hardcoded
        'FE3', // Lead Source - hardcoded
        sale.customerFirstName, // First Name
        sale.customerLastName, // Last Name
        `${sale.customerFirstName} ${sale.customerLastName}`, // Customers Name (First - Last)
        sale.email, // Email
        sale.title ? sale.title : '', // Title - ensure it's not null
        sale.phoneNumber, // Phone
        '', // Mobile - blank
        '', // Date of Birth - blank
        '', // Modified By.id - blank
        '', // Modified By - blank
        '', // Modified Time - blank
        '', // Salutation - blank
        '', // Last Activity Time - blank
        sale.mailingStreet ? sale.mailingStreet : '', // Mailing Street - ensure it's not null
        sale.mailingCity ? sale.mailingCity : 'London', // Mailing City - default to London if missing
        sale.mailingProvince ? sale.mailingProvince : '', // Mailing Province - ensure it's not null
        sale.mailingPostalCode ? sale.mailingPostalCode : '', // Mailing Postal Code - ensure it's not null
        '', // Description - blank
        '', // Tag - blank
        '', // Unsubscribed Mode - blank
        '', // Unsubscribed Time - blank
        '', // Change Log Time - blank
        '', // Locked - blank
        '', // Last Enriched Time - blank
        '', // Enrich Status - blank
        'DD', // Payment Method - hardcoded to DD
        'Process DD', // Status - hardcoded
        createdAt.toLocaleDateString('en-GB'), // Created Date
        sale.sortCode, // SortCode
        sale.accountNumber, // Acc Number
        '', // CVC - blank
        '', // EXP Date - blank
        '', // Card Number - blank
        '', // LeadIdCPY - blank
        sale.phoneNumber, // Plain Phone (same as Phone)
        `£${(singleAppPrice + boilerPrice).toFixed(2)}`, // Customer Premium - calculated total
        '', // Package Excess - blank
        '', // Last Service Date - blank
        '', // Boiler Make - blank
        '', // Pre Existing Issue - blank
        '', // Boiler Age - blank
        '', // Cancellation Notes - blank
        '', // Renewal Date - blank
        '', // Cancellation Fee - blank
        '', // Date of renewal notification - blank
        sale.agentName || sale.createdBy.email, // Lead Sales Agent - prefer agentName, fall back to email
        createdAt.toLocaleDateString('en-GB'), // Date of Sale
        sale.mailingStreet || '', // First Line Add
        // Customer Package - determine based on what coverage is selected
        sale.boilerCoverSelected && sale.applianceCoverSelected ? 'appliance + boiler' : 
        sale.boilerCoverSelected ? 'boiler' : 
        sale.applianceCoverSelected ? 'appliance' : '', // Customer Package
        '', // Cancellation status - blank
        '', // Type of renewal notification - blank
        directDebitDate.toLocaleDateString('en-GB'), // First DD Date
        `£${sale.totalPlanCost.toFixed(2)}`, // DD Amount
        '', // Residential Status - blank
        '', // Plan Reference Number - blank
        '', // Brand - blank
        'DD', // Processor - hardcoded to DD
        '', // Appliance 2 Age - blank
        '', // Appliance 1 Brand - blank (we only have appliance type, not brand)
        sale.appliances[4]?.appliance || '', // Appliance 5 Type - using appliance name as type
        sale.appliances[3]?.appliance || '', // Appliance 4 Type - using appliance name as type
        sale.appliances[2]?.appliance || '', // Appliance 3 Type - using appliance name as type
        '', // Appliance 1 Age - blank
        '', // Appliance 5 Brand - blank (we only have appliance type, not brand)
        '', // Appliance 4 Brand - blank (we only have appliance type, not brand)
        '', // Appliance 3 Brand - blank (we only have appliance type, not brand)
        '', // Appliance 5 Age - blank
        '', // Appliance 4 Age - blank
        sale.appliances[1]?.appliance || '', // Appliance 2 Type - using appliance name as type
        sale.appliances[0]?.appliance || '', // Appliance 1 Type - using appliance name as type
        '', // Appliance 2 Brand - blank (we only have appliance type, not brand)
        '', // Appliance 3 Age - blank
        '', // TV Value - blank
        '', // TV Brand - blank
        '', // TV Size - blank
        '', // TV Age - blank
        '', // Sales Office Name - blank
        '', // Affiliate Reference - blank
        '', // Free Offer Period_Months - blank
        '', // Cancellation Agent - blank
        '', // Remaining Payments Due - blank
        '', // Cancellation Reason - blank
        '', // Welcome Letter Sent Date - blank
        '', // Date of CNR - blank
        '', // Contact Attempts - blank
        '', // Last Contact Date - blank
        '', // Resend Welcome Pack - blank
        '', // Resend Method - blank
        '', // Cancelled Date - blank
        '', // Call Notes - blank
        '', // Product sold - blank
        '', // Customer Upgraded - blank
        '', // Preferred Payment Date - blank
        '', // Last 2 Acc Number (Post Docs) - blank
        '', // DD Originator Reference - blank
        '', // Authorised Persons on Account - blank
        '', // Customer Preferences - blank
        '', // Details of Vulnerabilities (if any) - blank
        '', // POA - blank
        '', // Appliance 6 Age - blank
        '', // Appliance 6 Type - blank
        '', // Appliance 6 Brand - blank
        '', // Appliance 7 Brand - blank
        '', // Appliance 7 Type - blank
        '', // Appliance 7 Age - blank
        '', // Appliance 8 Type - blank
        '', // Appliance 8 Brand - blank
        '', // Appliance 8 Age - blank
        '', // Reduced price exp date - blank
        '', // Reduced Price - blank
        '', // TV Model Number - blank
        '', // Contacted for TV Information - blank
        '', // Boiler 2 Age - blank
        '', // Boiler 2 Make - blank
        '', // TV 2 Value - blank
        '', // TV 2 -Age - blank
        '', // TV 2 Model Number - blank
        '', // TV 2 Brand - blank
        '', // TV 2 - Size - blank
        boilerPrice > 0 ? `£${boilerPrice.toFixed(2)}` : '', // Boiler Package Price (Internal)
        singleAppPrice > 0 ? `£${singleAppPrice.toFixed(2)}` : '', // Single App Price (Internal)
        '', // App Bundle Price (Internal) - blank
        '', // Landlord Boiler Package Price (Internal) - blank
        '', // Appliance 9 Type - blank
        '', // Appliance 9 Brand - blank
        '', // Appliance 9 Age - blank
        '', // Multi Package Discount - blank
        '', // TV Monthly Premium - blank
        '', // Boiler 3-Months Free - blank
        '', // Appliance 5 Value - blank
        '', // Appliance 6 Value - blank
        '', // Appliance 4 Value - blank
        '', // Appliance 2 Value - blank
        '', // Appliance 3 Value - blank
        '', // Appliance 1 Value - blank
        '', // Appliance 9 Value - blank
        '', // Appliance 7 Value - blank
        '', // Appliance 8 Value - blank
        '', // GC Mandate ID - blank
        '', // Reinstated Date - blank
        '', // Payment Status - blank
        '', // Date of last payment status - blank
        '', // Appliance 10 Type - blank
        '', // Appliance 10 Brand - blank
        '', // Appliance 10 Age - blank
        '', // Appliance 10 Value - blank
        '', // Plan Start Date - blank
        '', // Months Free Provided - blank
        '', // Sale Approved - blank
        '', // GC Bank Account ID - blank
        '', // GC Customer ID - blank
        '', // Connected To.module - blank
        '', // Connected To.id - blank
        '', // GC Subscription Status - blank
        '', // GC Subscription ID - blank
        '', // GC API Status - blank
        '', // GC Mandate Status - blank
        '', // GC Payment Status Update - blank
        '', // GC Payment ID - blank
        '', // GC Last Event ID - blank
        '', // GC Last Webhook ID - blank
        '', // GC Last Cause - blank
        '', // GC Last Description - blank
        '', // GC Last Received At Date - blank
        '', // GC Last Resource Type - blank
        '', // GS Manual Update All Status - blank
        '', // GC Payment ID Scheduled To Refund - blank
        '', // GC Last Payment Refunded - blank
        '' // Cancellation Fee Taken - blank
      ]

      // Update appliance data in the correct positions if we have appliances
      if (sale.appliances && sale.appliances.length > 0) {
        // Map to correct CRM positions
        sale.appliances.forEach((app: any, index: number) => {
          if (index === 0) { // Appliance 1
            row[73] = app.appliance // Appliance 1 Type
            // row[62] = '' // Appliance 1 Brand - leave blank
            row[66] = '' // Appliance 1 Age
            row[138] = `£${app.coverLimit.toFixed(2)}` // Appliance 1 Value (from cover limit)
          } else if (index === 1) { // Appliance 2
            row[72] = app.appliance // Appliance 2 Type
            // row[74] = '' // Appliance 2 Brand - leave blank
            row[61] = '' // Appliance 2 Age
            row[136] = `£${app.coverLimit.toFixed(2)}` // Appliance 2 Value
          } else if (index === 2) { // Appliance 3
            row[65] = app.appliance // Appliance 3 Type
            // row[69] = '' // Appliance 3 Brand - leave blank
            row[75] = '' // Appliance 3 Age
            row[137] = `£${app.coverLimit.toFixed(2)}` // Appliance 3 Value
          } else if (index === 3) { // Appliance 4
            row[64] = app.appliance // Appliance 4 Type
            // row[68] = '' // Appliance 4 Brand - leave blank
            row[71] = '' // Appliance 4 Age
            row[135] = `£${app.coverLimit.toFixed(2)}` // Appliance 4 Value
          } else if (index === 4) { // Appliance 5
            row[63] = app.appliance // Appliance 5 Type
            // row[67] = '' // Appliance 5 Brand - leave blank
            row[70] = '' // Appliance 5 Age
            row[133] = `£${app.coverLimit.toFixed(2)}` // Appliance 5 Value
          }
        })
      }

      return row
    })

    // Create CSV content
    const csvRows = [headers, ...rows].map((row: any[]) => 
      row.map((cell: any) => {
        const cellStr = String(cell || '')
        // Escape quotes and wrap in quotes if necessary
        if (cellStr.includes(',') || cellStr.includes('"') || cellStr.includes('\n') || cellStr.includes('\r')) {
          return `"${cellStr.replace(/"/g, '""')}"`
        }
        return cellStr
      }).join(',')
    ).join('\n')

    // Add BOM for Excel compatibility
    const BOM = '\uFEFF'
    const csvContent = BOM + csvRows

    return new Response(csvContent, {
      headers: {
        'Content-Type': 'text/csv; charset=utf-8',
        'Content-Disposition': `attachment; filename="sales_export_${new Date().toISOString().split('T')[0]}.csv"`,
      },
    })
  } catch (error) {
    console.error('Error exporting CSV:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await request.json()
    const { filters, selectedIds, excludeCustomers } = body

    let whereClause: any = {}

    // If specific IDs are provided (selected export), use those
    if (selectedIds && selectedIds.length > 0) {
      whereClause.id = {
        in: selectedIds
      }
    } else {
      // Apply filters for all export
      if (filters?.agent) {
        whereClause.createdById = filters.agent
      }

      // Date filters
      if (filters?.dateFrom || filters?.dateTo) {
        whereClause.createdAt = {}
        if (filters.dateFrom) {
          whereClause.createdAt.gte = new Date(filters.dateFrom)
        }
        if (filters.dateTo) {
          whereClause.createdAt.lte = new Date(filters.dateTo + 'T23:59:59.999Z')
        }
      }
    }

    const sales = await prisma.sale.findMany({
      where: whereClause,
      include: {
        appliances: true,
        createdBy: {
          select: {
            id: true,
            email: true,
          },
        },
      },
      orderBy: {
        createdAt: 'desc',
      },
    })

    // Filter out duplicates if exclusion list provided
    let filteredSales = sales
    if (excludeCustomers && excludeCustomers.length > 0) {
      console.log(`Filtering ${sales.length} sales against ${excludeCustomers.length} exclusion entries`)
      
      filteredSales = sales.filter(sale => {
        // Normalize customer data for comparison
        const customerEmail = sale.email?.toLowerCase().trim() || ''
        const customerPhone = sale.phoneNumber?.replace(/[\s\-\(\)]/g, '') || '' // Remove formatting
        const customerFullName = `${sale.customerFirstName} ${sale.customerLastName}`.toLowerCase().trim()
        const customerAccountNumber = sale.accountNumber?.replace(/[\s\-]/g, '') || ''
        
        // Check if any identifier exactly matches the exclusion list
        const isExcluded = excludeCustomers.some((exclude: string) => {
          const excludeStr = exclude.toLowerCase().trim()
          
          // Parse the exclusion entry to extract identifiers
          // Could be: email, phone, name, or account number
          const excludePhone = excludeStr.replace(/[\s\-\(\)]/g, '')
          const excludeAccountNumber = excludeStr.replace(/[\s\-]/g, '')
          
          // Exact matches only (no partial matching)
          const emailMatch = customerEmail !== '' && customerEmail === excludeStr
          const phoneMatch = customerPhone !== '' && customerPhone === excludePhone
          const nameMatch = customerFullName === excludeStr
          const accountMatch = customerAccountNumber !== '' && customerAccountNumber === excludeAccountNumber
          
          // Also check reversed name format (Last, First)
          const reversedName = `${sale.customerLastName} ${sale.customerFirstName}`.toLowerCase().trim()
          const reversedNameMatch = reversedName === excludeStr
          
          return emailMatch || phoneMatch || nameMatch || accountMatch || reversedNameMatch
        })
        
        if (isExcluded) {
          console.log(`Excluding customer: ${customerFullName} (${customerEmail}) - matched exclusion list`)
        }

        return !isExcluded
      })
      
      console.log(`Filtered result: ${filteredSales.length} sales remaining after exclusion (${sales.length - filteredSales.length} excluded)`)
    }

    // Generate CSV with same format as GET handler
    const csvHeader = [
      'Customers Owner',
      'Lead Source',
      'First Name',
      'Last Name',
      'Customers Name',
      'Email',
      'Title',
      'Phone',
      'Mobile',
      'Date of Birth',
      'Modified By.id',
      'Modified By',
      'Modified Time',
      'Salutation',
      'Last Activity Time',
      'Mailing Street',
      'Mailing City',
      'Mailing Province/State',
      'Mailing Postal Code',
      'Description',
      'Tag',
      'Unsubscribed Mode',
      'Unsubscribed Time',
      'Change Log Time',
      'Locked',
      'Last Enriched Time',
      'Enrich Status',
      'Payment Method',
      'Status',
      'Created Date',
      'SortCode',
      'Account Number',
      'Account Name',
      'DD Date',
      'Lead Sales Agent',
      'Date of Sale',
      'First Line Add',
      'Customer Package',
      'Customer Package Cost',
      'Appliance Cover Selected',
      'Boiler Cover Selected',
      'Total Cost'
    ]

    const csvRows = filteredSales.map(sale => {
      const createdAt = new Date(sale.createdAt)
      
      // Customer Package logic (same as GET handler)
      let customerPackage = ''
      let packageCost = 0
      
      if (sale.applianceCoverSelected && sale.boilerCoverSelected) {
        customerPackage = 'Both Appliance & Boiler Cover'
        packageCost = sale.totalPlanCost
      } else if (sale.applianceCoverSelected) {
        customerPackage = 'Appliance Cover Only'
        packageCost = sale.appliances.reduce((sum, appliance) => sum + appliance.cost, 0)
      } else if (sale.boilerCoverSelected) {
        customerPackage = 'Boiler Cover Only'
        packageCost = sale.boilerPriceSelected || 0
      } else {
        customerPackage = 'No Cover Selected'
        packageCost = 0
      }

      return [
        'Kenan', // Customers Owner - hardcoded
        'FE3', // Lead Source - hardcoded
        sale.customerFirstName, // First Name
        sale.customerLastName, // Last Name
        `${sale.customerFirstName} ${sale.customerLastName}`, // Customers Name
        sale.email, // Email
        sale.title ? sale.title : '', // Title
        sale.phoneNumber, // Phone
        '', // Mobile - blank
        '', // Date of Birth - blank
        '', // Modified By.id - blank
        '', // Modified By - blank
        '', // Modified Time - blank
        '', // Salutation - blank
        '', // Last Activity Time - blank
        sale.mailingStreet ? sale.mailingStreet : '', // Mailing Street
        sale.mailingCity ? sale.mailingCity : 'London', // Mailing City - default to London
        sale.mailingProvince ? sale.mailingProvince : '', // Mailing Province
        sale.mailingPostalCode ? sale.mailingPostalCode : '', // Mailing Postal Code
        '', // Description - blank
        '', // Tag - blank
        '', // Unsubscribed Mode - blank
        '', // Unsubscribed Time - blank
        '', // Change Log Time - blank
        '', // Locked - blank
        '', // Last Enriched Time - blank
        '', // Enrich Status - blank
        'DD', // Payment Method - hardcoded
        'Process DD', // Status - hardcoded
        createdAt.toLocaleDateString('en-GB'), // Created Date
        sale.sortCode, // SortCode
        sale.accountNumber, // Account Number
        sale.accountName, // Account Name
        new Date(sale.directDebitDate).toLocaleDateString('en-GB'), // DD Date
        sale.createdBy.email, // Lead Sales Agent
        createdAt.toLocaleDateString('en-GB'), // Date of Sale
        sale.mailingStreet || '', // First Line Add
        customerPackage, // Customer Package
        packageCost.toString(), // Customer Package Cost
        sale.applianceCoverSelected ? 'Yes' : 'No', // Appliance Cover Selected
        sale.boilerCoverSelected ? 'Yes' : 'No', // Boiler Cover Selected
        sale.totalPlanCost.toString() // Total Cost
      ]
    })

    // Create CSV content
    const csvContent = [csvHeader, ...csvRows]
      .map(row => row.map(cell => `"${cell}"`).join(','))
      .join('\n')

    const excludedCount = sales.length - filteredSales.length
    const filename = selectedIds && selectedIds.length > 0
      ? `selected_sales_export_deduplicated_${new Date().toISOString().split('T')[0]}.csv`
      : `sales_export_deduplicated_${new Date().toISOString().split('T')[0]}.csv`

    return new NextResponse(csvContent, {
      headers: {
        'Content-Type': 'text/csv; charset=utf-8',
        'Content-Disposition': `attachment; filename="${filename}"`,
        'X-Excluded-Count': excludedCount.toString(),
      },
    })
  } catch (error) {
    console.error('Error exporting CSV with duplicate check:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}