import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET(request: NextRequest) {
  try {
    console.log('🚀 OPTIMIZED EXPORT - Starting export with hash map optimization...')

    // Get sales data
    const sales = await prisma.sale.findMany({
      include: {
        createdBy: {
          select: {
            email: true
          }
        },
        appliances: true
      },
      orderBy: { createdAt: 'desc' }
    })

    console.log(`🚀 OPTIMIZED EXPORT - Found ${sales.length} sales`)

    let filteredSales = sales

    // Check for duplicate file
    const { searchParams } = new URL(request.url)
    const duplicateFile = searchParams.get('duplicateFile')

    if (duplicateFile) {
      console.log('🚀 OPTIMIZED EXPORT - Processing duplicate file for deduplication...')
      
      try {
        const response = await fetch(duplicateFile)
        const csvContent = await response.text()
        const rows = csvContent.split('\n').slice(1) // Skip header
        
        console.log(`🚀 OPTIMIZED EXPORT - Processing ${rows.length} exclusion rows`)
        
        // OPTIMIZATION: Build hash maps for O(1) lookups instead of O(n) nested loops
        const exclusionMaps = {
          emails: new Set<string>(),
          phones: new Set<string>(),
          phonePartials: new Set<string>(),
          accounts: new Set<string>(),
          fullNames: new Set<string>(),
          singleNames: new Set<string>()
        }
        
        rows.forEach((row, index) => {
          const trimmed = row.trim()
          if (!trimmed) return
          
          const normalized = trimmed.toLowerCase().trim()
          
          // Email detection
          if (normalized.includes('@')) {
            exclusionMaps.emails.add(normalized)
          }
          // Phone detection
          else if (/^\+?[\d\s\-\(\)]+$/.test(normalized)) {
            const cleanPhone = normalized.replace(/[\s\-\(\)\+]/g, '')
            exclusionMaps.phones.add(cleanPhone)
            if (cleanPhone.length >= 8) {
              exclusionMaps.phonePartials.add(cleanPhone.slice(-8))
            }
          }
          // Account number detection (8-12 digits)
          else if (/^\d{8,12}$/.test(normalized.replace(/[\s\-]/g, ''))) {
            exclusionMaps.accounts.add(normalized.replace(/[\s\-]/g, ''))
          }
          // Name detection
          else {
            exclusionMaps.fullNames.add(normalized)
            
            // Handle reversed format and comma cleanup
            if (normalized.includes(' ')) {
              const parts = normalized.split(/\s+/)
              if (parts.length === 2) {
                exclusionMaps.fullNames.add(`${parts[1]} ${parts[0]}`)
              }
            }
            
            // Handle comma cleaning
            const cleanedName = normalized.replace(',', '').replace(/\s+/g, ' ').trim()
            if (cleanedName !== normalized) {
              exclusionMaps.fullNames.add(cleanedName)
            }
            
            // Single name
            if (!normalized.includes(' ')) {
              exclusionMaps.singleNames.add(normalized)
            }
          }
        })
        
        console.log(`🚀 OPTIMIZED EXPORT - Hash maps built: emails=${exclusionMaps.emails.size}, phones=${exclusionMaps.phones.size}, names=${exclusionMaps.fullNames.size}`)
        
        // OPTIMIZED filtering with O(1) lookups
        const filterStart = Date.now()
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
            console.log('🎯 MARGOT DEBUG (OPTIMIZED):', customer)
          }

          // O(1) hash map lookups
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
        
        const filterEnd = Date.now()
        console.log(`🚀 OPTIMIZED EXPORT - Filtering completed in ${filterEnd - filterStart}ms (avg ${((filterEnd - filterStart) / sales.length).toFixed(2)}ms per sale)`)
        console.log(`🚀 OPTIMIZED EXPORT - Excluded ${sales.length - filteredSales.length} duplicates, kept ${filteredSales.length}`)

      } catch (dedupError) {
        console.error('🚀 OPTIMIZED EXPORT - Deduplication error:', dedupError)
        console.log('🚀 OPTIMIZED EXPORT - Proceeding without deduplication')
      }
    }

    // Create simple CSV
    const headers = ['Customer Name', 'Email', 'Phone', 'Created Date', 'Total Cost']
    const rows = filteredSales.map(sale => [
      `${sale.customerFirstName} ${sale.customerLastName}`,
      sale.email || '',
      sale.phoneNumber,
      new Date(sale.createdAt).toLocaleDateString(),
      sale.totalPlanCost?.toString() || '0'
    ])

    const csvContent = [headers, ...rows]
      .map(row => row.map(field => `"${field}"`).join(','))
      .join('\n')

    console.log('🚀 OPTIMIZED EXPORT - CSV generated successfully')

    return new Response(csvContent, {
      headers: {
        'Content-Type': 'text/csv; charset=utf-8',
        'Content-Disposition': 'attachment; filename="optimized-export.csv"',
      },
    })

  } catch (error) {
    console.error('🚀 OPTIMIZED EXPORT - Error:', error)
    return NextResponse.json({ 
      success: false, 
      error: error instanceof Error ? error.message : 'Unknown error' 
    }, { status: 500 })
  }
}