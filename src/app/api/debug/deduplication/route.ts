import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await request.json()
    const { customerName, excludeList } = body

    // Test the deduplication logic with a specific customer
    const testCustomer = await prisma.sale.findFirst({
      where: {
        OR: [
          {
            customerFirstName: {
              contains: customerName,
              mode: 'insensitive'
            }
          },
          {
            customerLastName: {
              contains: customerName,
              mode: 'insensitive'
            }
          }
        ]
      },
      select: {
        id: true,
        customerFirstName: true,
        customerLastName: true,
        email: true,
        phoneNumber: true,
        accountNumber: true
      }
    })

    if (!testCustomer) {
      return NextResponse.json({ 
        error: 'Customer not found',
        searchTerm: customerName
      })
    }

    // Test the deduplication logic
    const customerEmail = testCustomer.email?.toLowerCase().trim() || ''
    const customerPhone = testCustomer.phoneNumber?.replace(/[\s\-\(\)]/g, '') || ''
    const customerFullName = `${testCustomer.customerFirstName} ${testCustomer.customerLastName}`.toLowerCase().trim()
    const customerAccountNumber = testCustomer.accountNumber?.replace(/[\s\-]/g, '') || ''

    const debugInfo = {
      customer: testCustomer,
      normalizedData: {
        email: customerEmail,
        phone: customerPhone,
        fullName: customerFullName,
        accountNumber: customerAccountNumber
      },
      exclusionTests: [] as any[]
    }

    // Test against each exclusion entry
    if (excludeList && Array.isArray(excludeList)) {
      debugInfo.exclusionTests = excludeList.map((exclude: string) => {
        const excludeStr = exclude.toLowerCase().trim()
        const excludePhone = excludeStr.replace(/[\s\-\(\)]/g, '')
        const excludeAccountNumber = excludeStr.replace(/[\s\-]/g, '')
        
        const emailMatch = customerEmail !== '' && customerEmail === excludeStr
        const phoneMatch = customerPhone !== '' && customerPhone === excludePhone
        const nameMatch = customerFullName === excludeStr
        const accountMatch = customerAccountNumber !== '' && customerAccountNumber === excludeAccountNumber
        
        const reversedName = `${testCustomer.customerLastName} ${testCustomer.customerFirstName}`.toLowerCase().trim()
        const reversedNameMatch = reversedName === excludeStr

        const isExcluded = emailMatch || phoneMatch || nameMatch || accountMatch || reversedNameMatch

        return {
          originalExclude: exclude,
          normalizedExclude: excludeStr,
          tests: {
            emailMatch: { value: emailMatch, comparison: `"${customerEmail}" === "${excludeStr}"` },
            phoneMatch: { value: phoneMatch, comparison: `"${customerPhone}" === "${excludePhone}"` },
            nameMatch: { value: nameMatch, comparison: `"${customerFullName}" === "${excludeStr}"` },
            accountMatch: { value: accountMatch, comparison: `"${customerAccountNumber}" === "${excludeAccountNumber}"` },
            reversedNameMatch: { value: reversedNameMatch, comparison: `"${reversedName}" === "${excludeStr}"` }
          },
          isExcluded
        }
      })
    }

    return NextResponse.json(debugInfo)

  } catch (error) {
    console.error('Debug deduplication error:', error)
    return NextResponse.json({ 
      error: 'Internal server error',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}