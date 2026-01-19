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
    // Generate CSV rows - Fixed to match exactly 173 headers
    const rows = sales.map((sale: any) => {
      const createdAt = new Date(sale.createdAt)
      
      // Calculate internal pricing
      const singleAppPrice = sale.appliances.reduce((sum: number, app: any) => sum + Number(app.cost), 0)
      const boilerPrice = sale.boilerCoverSelected && sale.boilerPriceSelected ? Number(sale.boilerPriceSelected) : 0
      
      // Customer Package logic
      let customerPackage = ''
      if (sale.applianceCoverSelected && sale.boilerCoverSelected) {
        customerPackage = 'Both Appliance & Boiler Cover'
      } else if (sale.applianceCoverSelected) {
        customerPackage = 'Appliance Cover Only'
      } else if (sale.boilerCoverSelected) {
        customerPackage = 'Boiler Cover Only'
      } else {
        customerPackage = 'No Cover Selected'
      }
      
      // Get appliances data (up to 10)
      const appliances = Array(10).fill(null).map((_, i) => {
        const app = sale.appliances[i]
        return app ? {
          type: app.appliance,
          brand: '', // Not captured in our system
          age: '', // Not captured in our system
          value: `£${app.coverLimit.toFixed(2)}`
        } : { type: '', brand: '', age: '', value: '' }
      })
      
      // Build row with exactly 173 fields to match headers
      return [
        '', // 1. Record Id
        '', // 2. Customers Owner.id
        'Kenan', // 3. Customers Owner
        'FE3', // 4. Lead Source
        sale.customerFirstName, // 5. First Name
        sale.customerLastName, // 6. Last Name
        `${sale.customerFirstName} ${sale.customerLastName}`, // 7. Customers Name
        // 8. Email - Filter out placeholder/fake emails
        (sale.email && !sale.email.includes('placeholder') && !sale.email.includes('example') && !sale.email.includes('test') && !sale.email.includes('imported') && !sale.email.includes('demo') && !sale.email.includes('fake') && !sale.email.includes('temp')) ? sale.email : '',
        sale.title || '', // 9. Title
        sale.phoneNumber, // 10. Phone
        '', // 11. Mobile
        '', // 12. Date of Birth
        '', // 13. Modified By.id
        '', // 14. Modified By
        '', // 15. Modified Time
        '', // 16. Salutation
        '', // 17. Last Activity Time
        sale.mailingStreet || '', // 18. Mailing Street
        sale.mailingCity || 'London', // 19. Mailing City
        sale.mailingProvince || '', // 20. Mailing Province
        sale.mailingPostalCode || '', // 21. Mailing Postal Code
        '', // 22. Description
        '', // 23. Tag
        '', // 24. Unsubscribed Mode
        '', // 25. Unsubscribed Time
        '', // 26. Change Log Time
        '', // 27. Locked
        '', // 28. Last Enriched Time
        '', // 29. Enrich Status
        'DD', // 30. Payment Method
        'Process DD', // 31. Status
        createdAt.toLocaleDateString('en-GB'), // 32. Created Date
        sale.sortCode || '', // 33. SortCode
        sale.accountNumber || '', // 34. Acc Number
        '', // 35. CVC
        '', // 36. EXP Date
        '', // 37. Card Number
        '', // 38. LeadIdCPY
        sale.phoneNumber, // 39. Plain Phone
        `£${(singleAppPrice + boilerPrice).toFixed(2)}`, // 40. Customer Premium
        '', // 41. Package Excess
        '', // 42. Last Service Date
        '', // 43. Boiler Make
        '', // 44. Pre Existing Issue
        '', // 45. Boiler Age
        '', // 46. Cancellation Notes
        '', // 47. Renewal Date
        '', // 48. Cancellation Fee
        '', // 49. Date of renewal notification
        sale.agentName || sale.createdBy?.email || '', // 50. Lead Sales Agent
        createdAt.toLocaleDateString('en-GB'), // 51. Date of Sale
        sale.mailingStreet || '', // 52. First Line Add
        customerPackage, // 53. Customer Package
        '', // 54. Cancellation status
        '', // 55. Type of renewal notification
        sale.directDebitDate ? new Date(sale.directDebitDate).toLocaleDateString('en-GB') : '', // 56. First DD Date
        `£${(singleAppPrice + boilerPrice).toFixed(2)}`, // 57. DD Amount
        '', // 58. Residential Status
        `TFT${String(Math.floor(Math.random() * 10000)).padStart(4, '0')}`, // 59. Plan Reference Number
        'Flash Team', // 60. Brand
        '', // 61. Processor
        appliances[1].age, // 62. Appliance 2 Age
        appliances[0].brand, // 63. Appliance 1 Brand
        appliances[4].type, // 64. Appliance 5 Type
        appliances[3].type, // 65. Appliance 4 Type
        appliances[2].type, // 66. Appliance 3 Type
        appliances[0].age, // 67. Appliance 1 Age
        appliances[4].brand, // 68. Appliance 5 Brand
        appliances[3].brand, // 69. Appliance 4 Brand
        appliances[2].brand, // 70. Appliance 3 Brand
        appliances[4].age, // 71. Appliance 5 Age
        appliances[3].age, // 72. Appliance 4 Age
        appliances[1].type, // 73. Appliance 2 Type
        appliances[0].type, // 74. Appliance 1 Type
        appliances[1].brand, // 75. Appliance 2 Brand
        appliances[2].age, // 76. Appliance 3 Age
        '', // 77. TV Value
        '', // 78. TV Brand
        '', // 79. TV Size
        '', // 80. TV Age
        'Flash Team', // 81. Sales Office Name
        '', // 82. Affiliate Reference
        '', // 83. Free Offer Period_Months
        '', // 84. Cancellation Agent
        '', // 85. Remaining Payments Due
        '', // 86. Cancellation Reason
        '', // 87. Welcome Letter Sent Date
        '', // 88. Date of CNR
        '', // 89. Contact Attempts
        '', // 90. Last Contact Date
        '', // 91. Resend Welcome Pack
        '', // 92. Resend Method
        '', // 93. Cancelled Date
        '', // 94. Call Notes
        customerPackage, // 95. Product sold
        '', // 96. Customer Upgraded
        sale.directDebitDate ? new Date(sale.directDebitDate).getDate() : '', // 97. Preferred Payment Date
        sale.accountNumber ? sale.accountNumber.slice(-2) : '', // 98. Last 2 Acc Number (Post Docs)
        '', // 99. DD Originator Reference
        '', // 100. Authorised Persons on Account
        '', // 101. Customer Preferences
        '', // 102. Details of Vulnerabilities (if any)
        '', // 103. POA
        appliances[5].age, // 104. Appliance 6 Age
        appliances[5].type, // 105. Appliance 6 Type
        appliances[5].brand, // 106. Appliance 6 Brand
        appliances[6].brand, // 107. Appliance 7 Brand
        appliances[6].type, // 108. Appliance 7 Type
        appliances[6].age, // 109. Appliance 7 Age
        appliances[7].type, // 110. Appliance 8 Type
        appliances[7].brand, // 111. Appliance 8 Brand
        appliances[7].age, // 112. Appliance 8 Age
        '', // 113. Reduced price exp date
        '', // 114. Reduced Price
        '', // 115. TV Model Number
        '', // 116. Contacted for TV Information
        '', // 117. Boiler 2 Age
        '', // 118. Boiler 2 Make
        '', // 119. TV 2 Value
        '', // 120. TV 2 -Age
        '', // 121. TV 2 Model Number
        '', // 122. TV 2 Brand
        '', // 123. TV 2 - Size
        `£${boilerPrice.toFixed(2)}`, // 124. Boiler Package Price (Internal)
        `£${singleAppPrice.toFixed(2)}`, // 125. Single App Price (Internal)
        `£${(singleAppPrice + boilerPrice).toFixed(2)}`, // 126. App Bundle Price (Internal)
        '', // 127. Landlord Boiler Package Price (Internal)
        appliances[8].type, // 128. Appliance 9 Type
        appliances[8].brand, // 129. Appliance 9 Brand
        appliances[8].age, // 130. Appliance 9 Age
        '', // 131. Multi Package Discount
        '', // 132. TV Monthly Premium
        '', // 133. Boiler 3-Months Free
        appliances[4].value, // 134. Appliance 5 Value
        appliances[5].value, // 135. Appliance 6 Value
        appliances[3].value, // 136. Appliance 4 Value
        appliances[1].value, // 137. Appliance 2 Value
        appliances[2].value, // 138. Appliance 3 Value
        appliances[0].value, // 139. Appliance 1 Value
        appliances[8].value, // 140. Appliance 9 Value
        appliances[6].value, // 141. Appliance 7 Value
        appliances[7].value, // 142. Appliance 8 Value
        '', // 143. GC Mandate ID
        '', // 144. Reinstated Date
        '', // 145. Payment Status
        '', // 146. Date of last payment status
        appliances[9].type, // 147. Appliance 10 Type
        appliances[9].brand, // 148. Appliance 10 Brand
        appliances[9].age, // 149. Appliance 10 Age
        appliances[9].value, // 150. Appliance 10 Value
        createdAt.toLocaleDateString('en-GB'), // 151. Plan Start Date
        '', // 152. Months Free Provided
        'Yes', // 153. Sale Approved
        '', // 154. GC Bank Account ID
        '', // 155. GC Customer ID
        '', // 156. Connected To.module
        '', // 157. Connected To.id
        '', // 158. GC Subscription Status
        '', // 159. GC Subscription ID
        '', // 160. GC API Status
        '', // 161. GC Mandate Status
        '', // 162. GC Payment Status Update
        '', // 163. GC Payment ID
        '', // 164. GC Last Event ID
        '', // 165. GC Last Webhook ID
        '', // 166. GC Last Cause
        '', // 167. GC Last Description
        '', // 168. GC Last Received At Date
        '', // 169. GC Last Resource Type
        '', // 170. GS Manual Update All Status
        '', // 171. GC Payment ID Scheduled To Refund
        '', // 172. GC Last Payment Refunded
        '' // 173. Cancellation Fee Taken
      ]
    })
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
        sale.id || '', // Record Id
        'Kenan', // Customers Owner
        sale.createdBy?.id || '', // Customers Owner.id
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
        sale.accountNumber || '', // Account Number
        sale.accountName || '', // Account Name
        sale.directDebitDate ? new Date(sale.directDebitDate).toLocaleDateString('en-GB') : '', // DD Date
        sale.createdBy?.email || '', // Lead Sales Agent
        createdAt.toLocaleDateString('en-GB'), // Date of Sale
        sale.mailingStreet || '', // First Line Add
        customerPackage, // Customer Package
        packageCost.toString(), // Customer Package Cost
        sale.applianceCoverSelected ? 'Yes' : 'No', // Appliance Cover Selected
        sale.boilerCoverSelected ? 'Yes' : 'No', // Boiler Cover Selected
        sale.totalPlanCost?.toString() || '0', // Total Cost
        '', // Boiler Make - not available in current schema
        '', // Boiler Age - not available in current schema
        '', // Brand Value
        '', // Call Outcome
        '', // Comments
        '', // Renewal Date
        '', // Quoted Cost
        '', // Monthly Cost
        '', // Commission Cost
        '', // Plan Reference Number
        '', // Brand
        '', // Processor
        '', // Appliance 2 Age - not available in current schema
        sale.appliances && sale.appliances[0] ? sale.appliances[0].appliance : '', // Appliance 1 Brand
        sale.appliances && sale.appliances[4] ? sale.appliances[4].appliance : '', // Appliance 5 Type
        sale.appliances && sale.appliances[3] ? sale.appliances[3].appliance : '', // Appliance 4 Type
        sale.appliances && sale.appliances[2] ? sale.appliances[2].appliance : '', // Appliance 3 Type
        '', // Appliance 1 Age - not available in current schema
        sale.appliances && sale.appliances[4] ? sale.appliances[4].appliance : '', // Appliance 5 Brand
        sale.appliances && sale.appliances[3] ? sale.appliances[3].appliance : '', // Appliance 4 Brand
        sale.appliances && sale.appliances[2] ? sale.appliances[2].appliance : '', // Appliance 3 Brand
        '', // Appliance 5 Age - not available in current schema
        '', // Appliance 4 Age - not available in current schema
        sale.appliances && sale.appliances[1] ? sale.appliances[1].appliance : '', // Appliance 2 Type
        sale.appliances && sale.appliances[0] ? sale.appliances[0].appliance : '', // Appliance 1 Type
        sale.appliances && sale.appliances[1] ? sale.appliances[1].appliance : '', // Appliance 2 Brand
        '', // Appliance 3 Age - not available in current schema
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