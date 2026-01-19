import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    console.log('🧪 DEDUP TEST - Testing deduplication logic...')

    // Test data
    const testSales = [
      {
        id: 'test1',
        customerFirstName: 'Margot',
        customerLastName: 'Maitland', 
        email: 'margot@test.com',
        phoneNumber: '07123456789',
        accountNumber: '12345678'
      },
      {
        id: 'test2',
        customerFirstName: 'John',
        customerLastName: 'Smith',
        email: 'john@test.com', 
        phoneNumber: '07987654321',
        accountNumber: '87654321'
      }
    ]

    const testExclusions = body.exclusions || [
      'Margot Maitland',
      'margot maitland', 
      'MARGOT MAITLAND',
      'Maitland, Margot',
      'margot@test.com',
      '07123456789'
    ]

    console.log('🧪 Test sales:', testSales)
    console.log('🧪 Test exclusions:', testExclusions)

    // Apply the deduplication logic
    const normalizedExclusions = testExclusions.map((exclude: string, index: number) => {
      const normalized = exclude?.toLowerCase().replace(/\s+/g, ' ').trim() || ''
      return {
        original: exclude || '',
        normalized,
        phone: normalized.replace(/[\s\-\(\)\+]/g, ''),
        account: normalized.replace(/[\s\-]/g, ''),
        isEmail: normalized.includes('@'),
        isPhone: /\d{6,}/.test(normalized),
        isAccount: /^\d{8,}$/.test(normalized.replace(/[\s\-]/g, ''))
      }
    })

    console.log('🧪 Normalized exclusions:', normalizedExclusions)

    const filteredSales = testSales.filter((sale) => {
      const customer = {
        email: sale.email?.toLowerCase().trim() || '',
        phone: sale.phoneNumber?.replace(/[\s\-\(\)\+]/g, '') || '',
        fullName: `${sale.customerFirstName?.trim() || ''} ${sale.customerLastName?.trim() || ''}`.toLowerCase().replace(/\s+/g, ' ').trim(),
        firstName: sale.customerFirstName?.toLowerCase().trim() || '',
        lastName: sale.customerLastName?.toLowerCase().trim() || '',
        reversedName: `${sale.customerLastName?.trim() || ''} ${sale.customerFirstName?.trim() || ''}`.toLowerCase().replace(/\s+/g, ' ').trim(),
        account: sale.accountNumber?.replace(/[\s\-]/g, '') || ''
      }

      console.log('🧪 Processing customer:', customer)

      const isExcluded = normalizedExclusions.some((exclusion: any) => {
        const matches = []

        // 1. Email exact match
        if (customer.email && exclusion.isEmail && exclusion.normalized && customer.email === exclusion.normalized) {
          matches.push('email-exact')
        }

        // 2. Phone exact match  
        if (customer.phone && exclusion.isPhone && exclusion.phone && customer.phone === exclusion.phone) {
          matches.push('phone-exact')
        }

        // 3. Account number match
        if (customer.account && exclusion.isAccount && exclusion.account && customer.account === exclusion.account) {
          matches.push('account-exact')
        }

        // 4. Full name match
        if (customer.fullName && exclusion.normalized && customer.fullName === exclusion.normalized) {
          matches.push('name-full-exact')
        }

        // 5. Reversed name match
        if (customer.reversedName && exclusion.normalized && customer.reversedName === exclusion.normalized) {
          matches.push('name-reversed-exact')
        }

        // 6. First or last name only
        if (exclusion.normalized && !exclusion.normalized.includes(' ') && !exclusion.isEmail && !exclusion.isPhone && !exclusion.isAccount) {
          if (customer.firstName === exclusion.normalized || customer.lastName === exclusion.normalized) {
            matches.push('name-single')
          }
        }

        if (matches.length > 0) {
          console.log(`🧪 MATCH FOUND: ${customer.fullName} matched "${exclusion.original}" via: ${matches.join(', ')}`)
        }

        return matches.length > 0
      })

      console.log(`🧪 Customer ${customer.fullName}: isExcluded = ${isExcluded}`)
      return !isExcluded
    })

    return NextResponse.json({
      success: true,
      originalSales: testSales,
      exclusions: testExclusions,
      normalizedExclusions,
      filteredSales,
      excluded: testSales.filter(s => !filteredSales.find(f => f.id === s.id)),
      margotExcluded: !filteredSales.find(s => s.customerFirstName === 'Margot'),
      summary: {
        originalCount: testSales.length,
        filteredCount: filteredSales.length,
        excludedCount: testSales.length - filteredSales.length
      }
    })

  } catch (error) {
    console.error('🧪 DEDUP TEST - Error:', error)
    return NextResponse.json({ 
      success: false, 
      error: error instanceof Error ? error.message : 'Unknown error' 
    }, { status: 500 })
  }
}