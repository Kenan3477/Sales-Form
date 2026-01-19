import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '../../../../lib/auth'
import { prisma } from '../../../../lib/prisma'

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await request.json()
    const { filters, selectedIds, excludeCustomers } = body

    console.log('🚀 FIXED EXPORT - Starting with optimized deduplication...')

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

    console.log(`🚀 FIXED EXPORT - Found ${sales.length} sales`)

    // OPTIMIZED: Filter out duplicates with hash maps for O(1) lookups
    let filteredSales = sales
    if (excludeCustomers && excludeCustomers.length > 0) {
      console.log(`🚀 FIXED EXPORT - Starting OPTIMIZED deduplication with ${excludeCustomers.length} exclusions...`)
      
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
      
      console.log(`🚀 FIXED EXPORT - Hash maps built: emails=${exclusionMaps.emails.size}, phones=${exclusionMaps.phones.size}, names=${exclusionMaps.fullNames.size}`)
      
      // Check for Margot specifically in exclusions
      const margotFound = Array.from(exclusionMaps.fullNames).filter(name => 
        name.includes('margot') || name.includes('maitland')
      )
      if (margotFound.length > 0) {
        console.log('🎯 MARGOT FOUND in exclusions:', margotFound)
      } else {
        console.log('❌ MARGOT NOT FOUND in exclusions - this might be the issue!')
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
      console.log(`🚀 FIXED EXPORT - Deduplication completed in ${dedupEnd - dedupStart}ms (avg ${((dedupEnd - dedupStart) / sales.length).toFixed(2)}ms per sale)`)
      console.log(`🚀 FIXED EXPORT - Excluded ${sales.length - filteredSales.length} duplicates, kept ${filteredSales.length}`)
    }

    // Generate comprehensive CSV with all 160+ fields
    const csvHeader = [
      'Record Id','Customers Owner.id','Customers Owner','Lead Source','First Name','Last Name','Customers Name',
      'Email','Title','Phone','Mobile','Date of Birth','Modified By.id','Modified By','Modified Time','Salutation',
      'Last Activity Time','Mailing Street','Mailing City','Mailing Province','Mailing Postal Code','Description',
      'Tag','Unsubscribed Mode','Unsubscribed Time','Change Log Time','Locked','Last Enriched Time','Enrich Status',
      'Payment Method','Status','Created Date','SortCode','Acc Number','CVC','EXP Date','Card Number','LeadIdCPY',
      'Plain Phone','Customer Premium','Package Excess','Last Service Date','Boiler Make','Pre Existing Issue',
      'Boiler Age','Cancellation Notes','Renewal Date','Cancellation Fee','Date of renewal notification',
      'Lead Sales Agent','Date of Sale','First Line Add','Customer Package','Cancellation status',
      'Type of renewal notification','First DD Date','DD Amount','Residential Status','Plan Reference Number',
      'Brand','Processor','Appliance 2 Age','Appliance 1 Brand','Appliance 5 Type','Appliance 4 Type',
      'Appliance 3 Type','Appliance 1 Age','Appliance 5 Brand','Appliance 4 Brand','Appliance 3 Brand',
      'Appliance 5 Age','Appliance 4 Age','Appliance 2 Type','Appliance 1 Type','Appliance 2 Brand',
      'Appliance 3 Age','TV Value','TV Brand','TV Size','TV Age','Sales Office Name','Affiliate Reference',
      'Free Offer Period_Months','Cancellation Agent','Remaining Payments Due','Cancellation Reason',
      'Welcome Letter Sent Date','Date of CNR','Contact Attempts','Last Contact Date','Resend Welcome Pack',
      'Resend Method','Cancelled Date','Call Notes','Product sold','Customer Upgraded','Preferred Payment Date',
      'Last 2 Acc Number (Post Docs)','DD Originator Reference','Authorised Persons on Account',
      'Customer Preferences','Details of Vulnerabilities (if any)','POA','Appliance 6 Age','Appliance 6 Type',
      'Appliance 6 Brand','Appliance 7 Brand','Appliance 7 Type','Appliance 7 Age','Appliance 8 Type',
      'Appliance 8 Brand','Appliance 8 Age','Reduced price exp date','Reduced Price','TV Model Number',
      'Contacted for TV Information','Boiler 2 Age','Boiler 2 Make','TV 2 Value','TV 2 -Age',
      'TV 2 Model Number','TV 2 Brand','TV 2 - Size','Boiler Package Price (Internal)',
      'Single App Price (Internal)','App Bundle Price (Internal)','Landlord Boiler Package Price (Internal)',
      'Appliance 9 Type','Appliance 9 Brand','Appliance 9 Age','Multi Package Discount','TV Monthly Premium',
      'Boiler 3-Months Free','Appliance 5 Value','Appliance 6 Value','Appliance 4 Value','Appliance 2 Value',
      'Appliance 3 Value','Appliance 1 Value','Appliance 9 Value','Appliance 7 Value','Appliance 8 Value',
      'GC Mandate ID','Reinstated Date','Payment Status','Date of last payment status','Appliance 10 Type',
      'Appliance 10 Brand','Appliance 10 Age','Appliance 10 Value','Plan Start Date','Months Free Provided',
      'Sale Approved','GC Bank Account ID','GC Customer ID','Connected To.module','Connected To.id',
      'GC Subscription Status','GC Subscription ID','GC API Status','GC Mandate Status',
      'GC Payment Status Update','GC Payment ID','GC Last Event ID','GC Last Webhook ID','GC Last Cause',
      'GC Last Description','GC Last Received At Date','GC Last Resource Type','GS Manual Update All Status',
      'GC Payment ID Scheduled To Refund','GC Last Payment Refunded','Cancellation Fee Taken'
    ].join(',')

    const csvRows = filteredSales.map(sale => {
      const createdAt = new Date(sale.createdAt)
      const directDebitDate = new Date(sale.directDebitDate)
      const singleAppPrice = sale.appliances.reduce((sum, app) => sum + app.cost, 0)
      const boilerPrice = sale.boilerCoverSelected && sale.boilerPriceSelected ? sale.boilerPriceSelected : 0
      
      // Determine customer package
      let customerPackage = ''
      if (sale.applianceCoverSelected && sale.boilerCoverSelected) {
        customerPackage = 'Both Appliance & Boiler Cover'
      } else if (sale.applianceCoverSelected) {
        customerPackage = 'Appliance Cover Only'
      } else if (sale.boilerCoverSelected) {
        customerPackage = 'Boiler Cover Only'
      }

      return [
        sale.id || '', // Record Id
        'Kenan', // Customers Owner
        sale.createdBy?.id || '', // Customers Owner.id
        'FE3', // Lead Source
        sale.customerFirstName, // First Name
        sale.customerLastName, // Last Name
        `${sale.customerFirstName} ${sale.customerLastName}`, // Customers Name
        sale.email, // Email
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
        sale.accountNumber || '', // Account Number
        '', // CVC
        '', // EXP Date
        '', // Card Number
        '', // LeadIdCPY
        sale.phoneNumber, // Plain Phone
        `£${(singleAppPrice + boilerPrice).toFixed(2)}`, // Customer Premium
        '', // Package Excess
        '', // Last Service Date
        '', // Boiler Make
        '', // Pre Existing Issue
        '', // Boiler Age
        '', // Cancellation Notes
        '', // Renewal Date
        '', // Cancellation Fee
        '', // Date of renewal notification
        sale.createdBy?.email || '', // Lead Sales Agent
        createdAt.toLocaleDateString('en-GB'), // Date of Sale
        sale.mailingStreet || '', // First Line Add
        customerPackage, // Customer Package
        '', // Cancellation status
        '', // Type of renewal notification
        directDebitDate.toLocaleDateString('en-GB'), // First DD Date
        `£${sale.totalPlanCost.toFixed(2)}`, // DD Amount
        '', // Residential Status
        '', // Plan Reference Number
        '', // Brand
        'DD', // Processor
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
        '', // TV Value through Cancellation Fee Taken (all empty for now)
        ...Array(95).fill('')
      ].map(field => `"${field}"`).join(',')
    })

    const csvContent = [csvHeader, ...csvRows].join('\n')

    console.log('🚀 FIXED EXPORT - CSV generated successfully')

    return new Response(csvContent, {
      headers: {
        'Content-Type': 'text/csv; charset=utf-8',
        'Content-Disposition': 'attachment; filename="sales-export-fixed.csv"',
      },
    })

  } catch (error) {
    console.error('🚀 FIXED EXPORT - Error:', error)
    return NextResponse.json({ 
      success: false, 
      error: error instanceof Error ? error.message : 'Unknown error' 
    }, { status: 500 })
  }
}