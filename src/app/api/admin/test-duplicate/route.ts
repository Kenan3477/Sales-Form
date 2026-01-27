import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await request.json()
    const { customerFirstName, customerLastName, phoneNumber, email } = body

    console.log('🔍 Testing duplicate check for:', {
      customerFirstName,
      customerLastName, 
      phoneNumber,
      email
    })

    // Normalize phone number like the actual duplicate check does
    const normalizedPhone = phoneNumber.replace(/[\s\-\(\)\+]/g, '')
    
    console.log('📞 Normalized phone:', normalizedPhone)

    // Check for phone number matches
    const phoneMatches = await prisma.sale.findMany({
      where: {
        phoneNumber: normalizedPhone
      },
      select: {
        id: true,
        customerFirstName: true,
        customerLastName: true,
        email: true,
        phoneNumber: true,
        totalPlanCost: true,
        createdAt: true,
        createdBy: {
          select: {
            email: true
          }
        }
      }
    })

    console.log('📊 Phone matches found:', phoneMatches.length)

    // Check for email matches if email provided
    let emailMatches: any[] = []
    if (email) {
      const normalizedEmail = email.trim().toLowerCase()
      emailMatches = await prisma.sale.findMany({
        where: {
          email: {
            equals: normalizedEmail,
            mode: 'insensitive'
          }
        },
        select: {
          id: true,
          customerFirstName: true,
          customerLastName: true,
          email: true,
          phoneNumber: true,
          totalPlanCost: true,
          createdAt: true
        }
      })
      console.log('📧 Email matches found:', emailMatches.length)
    }

    // Check for name matches
    const nameMatches = await prisma.sale.findMany({
      where: {
        AND: [
          {
            customerFirstName: {
              equals: customerFirstName.trim(),
              mode: 'insensitive'
            }
          },
          {
            customerLastName: {
              equals: customerLastName.trim(),
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
        totalPlanCost: true,
        createdAt: true
      }
    })

    console.log('👤 Name matches found:', nameMatches.length)

    return NextResponse.json({
      success: true,
      testData: {
        customerFirstName,
        customerLastName,
        phoneNumber,
        normalizedPhone,
        email
      },
      matches: {
        phoneMatches,
        emailMatches,
        nameMatches
      },
      summary: {
        phoneMatchCount: phoneMatches.length,
        emailMatchCount: emailMatches.length,
        nameMatchCount: nameMatches.length,
        wouldBlock: phoneMatches.length > 0 || emailMatches.length > 0
      }
    })

  } catch (error) {
    console.error('🚨 Duplicate test error:', error)
    return NextResponse.json({
      error: 'Test failed',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}