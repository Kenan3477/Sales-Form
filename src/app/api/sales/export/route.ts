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
        // Filter out placeholder/fake emails
        (sale.email && !sale.email.includes('placeholder') && !sale.email.includes('example') && !sale.email.includes('test') && !sale.email.includes('imported') && !sale.email.includes('demo') && !sale.email.includes('fake') && !sale.email.includes('temp')) ? sale.email : '', // Email
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
        `£${sale.totalPlanCost.toFixed(2)}`, // Customer Premium - total plan cost
        '', // Package Excess - blank
        '', // Last Service Date - blank
        '', // Boiler Make - blank
        '', // Pre Existing Issue - blank
        '', // Boiler Age - blank
        '', // Cancellation Notes - blank
        '', // Renewal Date - blank
        '', // Cancellation Fee - blank
        '', // Date of renewal notification - blank
        sale.agentName || sale.createdBy?.email || '', // Lead Sales Agent - prefer agentName, fall back to email
        createdAt.toLocaleDateString('en-GB'), // Date of Sale
        sale.mailingStreet || '', // First Line Add
        // Customer Package - determine based on what coverage is selected
        (() => {
          if (sale.applianceCoverSelected && sale.boilerCoverSelected) return 'Appliances + Boiler'
          if (sale.boilerCoverSelected) return 'Boiler'
          if (sale.applianceCoverSelected) return 'Appliances'
          return 'No Cover Selected'
        })(), // Customer Package
        '', // Cancellation status - blank
        '', // Type of renewal notification - blank
        sale.directDebitDate ? new Date(sale.directDebitDate).toLocaleDateString('en-GB') : '', // First DD Date
        `£${sale.totalPlanCost.toFixed(2)}`, // DD Amount - total plan cost
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
        sale.boilerCoverSelected && sale.boilerPriceSelected ? `£${Number(sale.boilerPriceSelected).toFixed(2)}` : '', // Boiler Package Price (Internal)
        sale.applianceCoverSelected ? `£${singleAppPrice.toFixed(2)}` : '', // Single App Price (Internal)
        '', // App Bundle Price (Internal) - blank as we don't collect this info
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

    // OPTIMIZED: Filter out duplicates with hash maps for O(1) lookups instead of O(n*m) nested loops
    let filteredSales = sales
    if (excludeCustomers && excludeCustomers.length > 0) {
      console.log(`🚀 OPTIMIZED DEDUPLICATION - Starting with ${excludeCustomers.length} exclusions...`)
      
      try {
        // Build hash maps for instant lookups - O(n) instead of O(n*m)
        const exclusionMaps = {
          emails: new Set<string>(),
          phones: new Set<string>(),
          phonePartials: new Set<string>(),
          accounts: new Set<string>(),
          fullNames: new Set<string>(),
          singleNames: new Set<string>()
        }
        
        // Build hash maps from exclusions - O(n) operation
        excludeCustomers.forEach((exclude: string) => {
          const trimmed = exclude?.trim() || ''
          if (!trimmed) return
          
          const normalized = trimmed.toLowerCase().trim()
          
          // Email detection
          if (normalized.includes('@')) {
            exclusionMaps.emails.add(normalized)
          }
          // Phone detection (6+ digits)
          else if (/\d{6,}/.test(normalized)) {
            const cleanPhone = normalized.replace(/[\s\-\(\)\+]/g, '')
            exclusionMaps.phones.add(cleanPhone)
            if (cleanPhone.length >= 8) {
              exclusionMaps.phonePartials.add(cleanPhone.slice(-8))
            }
          }
          // Account number detection (8+ digits)
          else if (/^\d{8,}$/.test(normalized.replace(/[\s\-]/g, ''))) {
            exclusionMaps.accounts.add(normalized.replace(/[\s\-]/g, ''))
          }
          // Name detection
          else {
            exclusionMaps.fullNames.add(normalized)
            
            // Handle comma format: "Last, First" -> "first last"  
            if (normalized.includes(',')) {
              const commaClean = normalized.replace(',', '').replace(/\s+/g, ' ').trim()
              exclusionMaps.fullNames.add(commaClean)
              
              // Also try reversed: "Last, First" -> "last first"
              const parts = normalized.split(',').map(p => p.trim())
              if (parts.length === 2) {
                exclusionMaps.fullNames.add(`${parts[1]} ${parts[0]}`)
              }
            }
            
            // Handle reversed format: "First Last" -> "last first"
            if (normalized.includes(' ')) {
              const parts = normalized.split(/\s+/)
              if (parts.length === 2) {
                exclusionMaps.fullNames.add(`${parts[1]} ${parts[0]}`)
              }
            }
            
            // Single name handling
            if (!normalized.includes(' ') && !normalized.includes(',')) {
              exclusionMaps.singleNames.add(normalized)
            }
          }
        })
        
        console.log(`🚀 OPTIMIZED DEDUPLICATION - Hash maps built: emails=${exclusionMaps.emails.size}, phones=${exclusionMaps.phones.size}, names=${exclusionMaps.fullNames.size}`)
        
        // Check for Margot specifically in exclusions
        const margotFound = Array.from(exclusionMaps.fullNames).filter(name => 
          name.includes('margot') || name.includes('maitland')
        )
        if (margotFound.length > 0) {
          console.log('🎯 MARGOT FOUND in exclusions:', margotFound)
        } else {
          console.log('❌ MARGOT NOT FOUND in exclusions')
          console.log('Sample exclusion names:', Array.from(exclusionMaps.fullNames).slice(0, 10))
        }
        
        // Apply deduplication with O(1) hash map lookups - O(m) instead of O(n*m)
        const dedupStart = Date.now()
        filteredSales = sales.filter((sale, index) => {
          const customer = {
            email: sale.email?.toLowerCase().trim() || '',
            phone: sale.phoneNumber?.replace(/[\s\-\(\)\+]/g, '') || '',
            fullName: `${sale.customerFirstName?.trim() || ''} ${sale.customerLastName?.trim() || ''}`.toLowerCase().replace(/\s+/g, ' ').trim(),
            firstName: sale.customerFirstName?.toLowerCase().trim() || '',
            lastName: sale.customerLastName?.toLowerCase().trim() || '',
            reversedName: `${sale.customerLastName?.trim() || ''} ${sale.customerFirstName?.trim() || ''}`.toLowerCase().replace(/\s+/g, ' ').trim(),
            account: sale.accountNumber?.replace(/[\s\-]/g, '') || ''
          }

          // Debug Margot specifically
          const isMargot = customer.fullName.includes('margot') && customer.fullName.includes('maitland')
          if (isMargot) {
            console.log('🎯 MARGOT DEBUG (OPTIMIZED):', {
              customerData: customer,
              salesId: sale.id
            })
          }

          // O(1) hash map lookups instead of nested loops
          const matches: string[] = []
          
          if (customer.email && exclusionMaps.emails.has(customer.email)) {
            matches.push('email-exact')
          }
          if (customer.phone && exclusionMaps.phones.has(customer.phone)) {
            matches.push('phone-exact')
          }
          if (customer.phone && customer.phone.length >= 8 && exclusionMaps.phonePartials.has(customer.phone.slice(-8))) {
            matches.push('phone-partial-8')
          }
          if (customer.account && exclusionMaps.accounts.has(customer.account)) {
            matches.push('account-exact')
          }
          if (customer.fullName && exclusionMaps.fullNames.has(customer.fullName)) {
            matches.push('name-full-exact')
          }
          if (customer.reversedName && exclusionMaps.fullNames.has(customer.reversedName)) {
            matches.push('name-reversed-exact')
          }
          if (customer.firstName && exclusionMaps.singleNames.has(customer.firstName)) {
            matches.push('name-first-only')
          }
          if (customer.lastName && exclusionMaps.singleNames.has(customer.lastName)) {
            matches.push('name-last-only')
          }

          const isExcluded = matches.length > 0

          if (isMargot) {
            console.log('🎯 MARGOT RESULT (OPTIMIZED): isExcluded =', isExcluded, ', matches:', matches)
          }

          if (isExcluded) {
            console.log(`🚀 EXCLUDING: ${customer.fullName} via: ${matches.join(', ')}`)
          }

          return !isExcluded
        })
        
        const dedupEnd = Date.now()
        console.log(`🚀 OPTIMIZED DEDUPLICATION - Completed in ${dedupEnd - dedupStart}ms (avg ${((dedupEnd - dedupStart) / sales.length).toFixed(2)}ms per sale)`)
        console.log(`🚀 OPTIMIZED DEDUPLICATION - Excluded ${sales.length - filteredSales.length} duplicates, kept ${filteredSales.length}`)
        
      } catch (deduplicationError) {
        console.error('🚨 Critical error during optimized deduplication:', deduplicationError)
        // Fall back to original sales list if deduplication fails
        filteredSales = sales
        console.log('🚨 Falling back to unfiltered sales due to deduplication error')
      }
    }

    // Generate CSV with complete header format matching CRM requirements
    const csvHeader = [
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

    console.log('📧 EMAIL DEBUG - Starting CSV generation. Checking first 3 sales emails...')
    
    // Debug first 3 sales to check email values
    const firstThreeSales = filteredSales.slice(0, 3)
    firstThreeSales.forEach((sale, index) => {
      console.log(`📧 EMAIL DEBUG - Sale ${index + 1}:`, {
        saleId: sale.id,
        customerName: `${sale.customerFirstName} ${sale.customerLastName}`,
        emailFromDB: sale.email,
        emailType: typeof sale.email,
        emailIsPlaceholder: sale.email?.includes('placeholder') || sale.email?.includes('example') || sale.email?.includes('test'),
        rawEmailJSON: JSON.stringify(sale.email),
        createdAt: sale.createdAt
      })
    })

    const csvRows = filteredSales.map(sale => {
      const createdAt = new Date(sale.createdAt)
      
      // Customer Package logic (same as GET handler)
      let customerPackage = ''
      let packageCost = 0
      
      if (sale.applianceCoverSelected && sale.boilerCoverSelected) {
        customerPackage = 'Appliances + Boiler'
        packageCost = sale.totalPlanCost
      } else if (sale.applianceCoverSelected) {
        customerPackage = 'Appliances'
        packageCost = sale.appliances.reduce((sum, appliance) => sum + appliance.cost, 0)
      } else if (sale.boilerCoverSelected) {
        customerPackage = 'Boiler'
        packageCost = sale.boilerPriceSelected || 0
      } else {
        customerPackage = 'No Cover Selected'
        packageCost = 0
      }

      // Debug email field specifically for the first few sales
      const debugThisSale = filteredSales.indexOf(sale) < 3
      if (debugThisSale) {
        console.log(`📧 EMAIL DEBUG - Building CSV row for sale ${sale.id}:`, {
          customerName: `${sale.customerFirstName} ${sale.customerLastName}`,
          emailValue: sale.email,
          emailWillBeInCSV: sale.email || '[EMPTY]'
        })
      }

      return [
        '', // 1. Record Id
        '', // 2. Customers Owner.id
        'Kenan', // 3. Customers Owner
        'FE3', // Lead Source
        sale.customerFirstName, // First Name
        sale.customerLastName, // Last Name
        `${sale.customerFirstName} ${sale.customerLastName}`, // Customers Name
        // Filter out placeholder/fake emails
        (sale.email && !sale.email.includes('placeholder') && !sale.email.includes('example') && !sale.email.includes('test') && !sale.email.includes('imported') && !sale.email.includes('demo') && !sale.email.includes('fake') && !sale.email.includes('temp')) ? sale.email : '', // Email
        sale.title || '', // Title
        sale.phoneNumber, // Phone
        '', // Mobile
        '', // Date of Birth
        '', // Modified By.id
        '', // Modified By
        '', // Modified Time
        '', // Salutation
        '', // Last Activity Time
        sale.mailingStreet || '', // Mailing Street
        sale.mailingCity || 'London', // Mailing City
        sale.mailingProvince || '', // Mailing Province
        sale.mailingPostalCode || '', // Mailing Postal Code
        '', // Description
        '', // Tag
        '', // Unsubscribed Mode
        '', // Unsubscribed Time
        '', // Change Log Time
        '', // Locked
        '', // Last Enriched Time
        '', // Enrich Status
        'DD', // Payment Method
        'Process DD', // Status
        createdAt.toLocaleDateString('en-GB'), // Created Date
        sale.sortCode || '', // SortCode
        sale.accountNumber || '', // Acc Number
        '', // CVC
        '', // EXP Date
        '', // Card Number
        '', // LeadIdCPY
        sale.phoneNumber, // Plain Phone
        `£${sale.totalPlanCost.toFixed(2)}`, // Customer Premium - total plan cost
        '', // Package Excess
        '', // Last Service Date
        '', // Boiler Make
        '', // Pre Existing Issue
        '', // Boiler Age
        '', // Cancellation Notes
        '', // Renewal Date
        '', // Cancellation Fee
        '', // Date of renewal notification
        sale.agentName || sale.createdBy?.email || '', // Lead Sales Agent
        createdAt.toLocaleDateString('en-GB'), // Date of Sale
        sale.mailingStreet || '', // First Line Add
        customerPackage, // Customer Package
        '', // Cancellation status
        '', // Type of renewal notification
        sale.directDebitDate ? new Date(sale.directDebitDate).toLocaleDateString('en-GB') : '', // First DD Date
        `£${sale.totalPlanCost.toFixed(2)}`, // DD Amount - total plan cost
        '', // Residential Status
        `TFT${String(Math.floor(Math.random() * 10000)).padStart(4, '0')}`, // Plan Reference Number
        'Flash Team', // Brand
        '', // Processor
        '', // Appliance 2 Age
        '', // Appliance 1 Brand
        sale.appliances[4]?.appliance || '', // Appliance 5 Type
        sale.appliances[3]?.appliance || '', // Appliance 4 Type
        sale.appliances[2]?.appliance || '', // Appliance 3 Type
        '', // Appliance 1 Age
        '', // Appliance 5 Brand
        '', // Appliance 4 Brand
        '', // Appliance 3 Brand
        '', // Appliance 5 Age
        '', // Appliance 4 Age
        sale.appliances[1]?.appliance || '', // Appliance 2 Type
        sale.appliances[0]?.appliance || '', // Appliance 1 Type
        '', // Appliance 2 Brand
        '', // Appliance 3 Age
        '', // TV Value - not available in current schema
        '', // TV Brand - not available in current schema
        '', // TV Size - not available in current schema
        '', // TV Age - not available in current schema
        '', // Sales Office Name
        '', // Affiliate Reference
        '', // Free Offer Period_Months
        '', // Cancellation Agent
        '', // Remaining Payments Due
        '', // Cancellation Reason
        '', // Welcome Letter Sent Date
        '', // Date of CNR
        '', // Contact Attempts
        '', // Last Contact Date
        '', // Resend Welcome Pack
        '', // Resend Method
        '', // Cancelled Date
        '', // Call Notes
        customerPackage, // Product sold
        '', // Customer Upgraded
        sale.directDebitDate ? new Date(sale.directDebitDate).toLocaleDateString('en-GB') : '', // Preferred Payment Date
        sale.accountNumber ? sale.accountNumber.slice(-2) : '', // Last 2 Acc Number (Post Docs)
        '', // DD Originator Reference
        '', // Authorised Persons on Account
        '', // Customer Preferences
        '', // Details of Vulnerabilities (if any)
        '', // POA
        '', // Appliance 6 Age - not available in current schema
        sale.appliances && sale.appliances[5] ? sale.appliances[5].appliance : '', // Appliance 6 Type
        sale.appliances && sale.appliances[5] ? sale.appliances[5].appliance : '', // Appliance 6 Brand
        sale.appliances && sale.appliances[6] ? sale.appliances[6].appliance : '', // Appliance 7 Brand
        sale.appliances && sale.appliances[6] ? sale.appliances[6].appliance : '', // Appliance 7 Type
        '', // Appliance 7 Age - not available in current schema
        sale.appliances && sale.appliances[7] ? sale.appliances[7].appliance : '', // Appliance 8 Type
        sale.appliances && sale.appliances[7] ? sale.appliances[7].appliance : '', // Appliance 8 Brand
        '', // Appliance 8 Age - not available in current schema
        '', // Reduced price exp date
        '', // Reduced Price
        '', // TV Model Number - not available in current schema
        '', // Contacted for TV Information
        '', // Boiler 2 Age
        '', // Boiler 2 Make
        '', // TV 2 Value
        '', // TV 2 -Age
        '', // TV 2 Model Number
        '', // TV 2 Brand
        '', // TV 2 - Size
        '', // Boiler Package Price (Internal)
        '', // Single App Price (Internal)
        '', // App Bundle Price (Internal)
        '', // Landlord Boiler Package Price (Internal)
        sale.appliances && sale.appliances[8] ? sale.appliances[8].appliance : '', // Appliance 9 Type
        sale.appliances && sale.appliances[8] ? sale.appliances[8].appliance : '', // Appliance 9 Brand
        '', // Appliance 9 Age - not available in current schema
        '', // Multi Package Discount
        '', // TV Monthly Premium
        '', // Boiler 3-Months Free
        sale.appliances && sale.appliances[4] ? (sale.appliances[4].cost?.toString() || '') : '', // Appliance 5 Value
        sale.appliances && sale.appliances[5] ? (sale.appliances[5].cost?.toString() || '') : '', // Appliance 6 Value
        sale.appliances && sale.appliances[3] ? (sale.appliances[3].cost?.toString() || '') : '', // Appliance 4 Value
        sale.appliances && sale.appliances[1] ? (sale.appliances[1].cost?.toString() || '') : '', // Appliance 2 Value
        sale.appliances && sale.appliances[2] ? (sale.appliances[2].cost?.toString() || '') : '', // Appliance 3 Value
        sale.appliances && sale.appliances[0] ? (sale.appliances[0].cost?.toString() || '') : '', // Appliance 1 Value
        sale.appliances && sale.appliances[8] ? (sale.appliances[8].cost?.toString() || '') : '', // Appliance 9 Value
        sale.appliances && sale.appliances[6] ? (sale.appliances[6].cost?.toString() || '') : '', // Appliance 7 Value
        sale.appliances && sale.appliances[7] ? (sale.appliances[7].cost?.toString() || '') : '', // Appliance 8 Value
        '', // GC Mandate ID
        '', // Reinstated Date
        '', // Payment Status
        '', // Date of last payment status
        sale.appliances && sale.appliances[9] ? sale.appliances[9].appliance : '', // Appliance 10 Type
        sale.appliances && sale.appliances[9] ? sale.appliances[9].appliance : '', // Appliance 10 Brand
        '', // Appliance 10 Age - not available in current schema
        sale.appliances && sale.appliances[9] ? (sale.appliances[9].cost?.toString() || '') : '', // Appliance 10 Value
        createdAt.toLocaleDateString('en-GB'), // Plan Start Date
        '', // Months Free Provided
        '', // Sale Approved
        '', // GC Bank Account ID
        '', // GC Customer ID
        '', // Connected To.module
        '', // Connected To.id
        '', // GC Subscription Status
        '', // GC Subscription ID
        '', // GS Refund Date
        '', // GS Refund Amount
        '', // GC Payment Method ID  
        '', // GC Last Resource Type
        '', // GS Manual Update All Status
        '', // GC Payment ID Scheduled To Refund
        '', // GC Last Payment Refunded
        '' // Cancellation Fee Taken
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