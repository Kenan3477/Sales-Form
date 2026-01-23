import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '../../../../lib/auth'
import { prisma } from '../../../../lib/prisma'

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Allow both admins and agents to view sales (agents can view their own sales)
    const { id } = await params
    const saleId = id

    let whereClause: any = { id: saleId }

    // If the user is not an admin, they can only view their own sales
    if (session.user.role !== 'ADMIN') {
      whereClause.createdById = session.user.id
    }

    const sale = await prisma.sale.findFirst({
      where: whereClause,
      include: {
        appliances: true,
        createdBy: {
          select: {
            id: true,
            email: true,
          }
        }
      }
    })

    if (!sale) {
      return NextResponse.json({ error: 'Sale not found' }, { status: 404 })
    }

    return NextResponse.json(sale)
  } catch (error) {
    console.error('Error fetching sale:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  let id: string | undefined
  let body: any

  try {
    const session = await getServerSession(authOptions)
    
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const parsedParams = await params
    id = parsedParams.id
    const saleId = id
    body = await request.json()

    console.log('📝 Received sale update request:', {
      saleId,
      hasCustomerFirstName: !!body.customerFirstName,
      hasCustomerLastName: !!body.customerLastName,
      hasEmail: !!body.email,
      hasPhoneNumber: !!body.phoneNumber,
      hasTotalPlanCost: body.totalPlanCost !== undefined,
      hasApplianceCoverSelected: body.applianceCoverSelected !== undefined,
      hasBoilerCoverSelected: body.boilerCoverSelected !== undefined,
      appliancesCount: body.appliances?.length || 0
    })

    // Check if the sale exists and if the user has permission to edit it
    const existingSale = await prisma.sale.findUnique({
      where: { id: saleId },
      include: { appliances: true }
    })

    if (!existingSale) {
      return NextResponse.json({ error: 'Sale not found' }, { status: 404 })
    }

    // Check permissions: Admin can edit any sale, Agent can only edit their own sales
    if (session.user.role !== 'ADMIN' && existingSale.createdById !== session.user.id) {
      return NextResponse.json({ error: 'Forbidden: You can only edit your own sales' }, { status: 403 })
    }

    // Validate required fields based on field configuration (outside transaction)
    console.log('🔍 Validating sale update fields:', {
      customerFirstName: body.customerFirstName,
      customerLastName: body.customerLastName,
      email: body.email,
      phoneNumber: body.phoneNumber,
      accountName: body.accountName,
      sortCode: body.sortCode,
      accountNumber: body.accountNumber
    })

    // Get field configurations to check what's actually required
    const fieldConfigs = await prisma.fieldConfiguration.findMany()
    const isFieldRequired = (fieldName: string): boolean => {
      const config = fieldConfigs.find(c => c.fieldName === fieldName)
      return config?.isRequired || false
    }

    // Validate dynamic required fields
    const missingFields: string[] = []
    
    if (isFieldRequired('customerFirstName') && !body.customerFirstName) {
      missingFields.push('firstName')
    }
    if (isFieldRequired('customerLastName') && !body.customerLastName) {
      missingFields.push('lastName')
    }
    if (isFieldRequired('email') && !body.email) {
      missingFields.push('email')
    }
    if (isFieldRequired('phoneNumber') && !body.phoneNumber) {
      missingFields.push('phoneNumber')
    }
    if (isFieldRequired('accountName') && !body.accountName && !existingSale.accountName) {
      missingFields.push('accountName')
    }
    if (isFieldRequired('sortCode') && !body.sortCode && !existingSale.sortCode) {
      missingFields.push('sortCode')
    }
    if (isFieldRequired('accountNumber') && !body.accountNumber && !existingSale.accountNumber) {
      missingFields.push('accountNumber')
    }

    if (missingFields.length > 0) {
      return NextResponse.json({ 
        error: `Missing required fields: ${missingFields.join(', ')}. Please fill in all required fields.` 
      }, { status: 400 })
    }

    // Additional validation for data integrity
    if (body.totalPlanCost === undefined || body.totalPlanCost === null) {
      return NextResponse.json({ 
        error: 'Total plan cost is required' 
      }, { status: 400 })
    }

    if (body.applianceCoverSelected === undefined || body.boilerCoverSelected === undefined) {
      return NextResponse.json({ 
        error: 'Appliance and boiler cover selections are required' 
      }, { status: 400 })
    }

    // Validate appliances array if present
    if (body.appliances && !Array.isArray(body.appliances)) {
      return NextResponse.json({ 
        error: 'Appliances must be an array' 
      }, { status: 400 })
    }

    // Validate each appliance in the array
    if (body.appliances) {
      for (let i = 0; i < body.appliances.length; i++) {
        const appliance = body.appliances[i]
        if (!appliance.appliance || appliance.coverLimit === undefined || appliance.cost === undefined) {
          return NextResponse.json({ 
            error: `Appliance ${i + 1} is missing required fields (appliance, coverLimit, cost)` 
          }, { status: 400 })
        }
      }
    }

    // Update the sale and appliances in a transaction
    const updatedSale = await prisma.$transaction(async (prisma) => {
      // Delete existing appliances
      await prisma.appliance.deleteMany({
        where: { saleId }
      })

      // Update the sale with new data
      return await prisma.sale.update({
        where: { id: saleId },
        data: {
          customerFirstName: body.customerFirstName,
          customerLastName: body.customerLastName,
          title: body.title || null,
          phoneNumber: body.phoneNumber,
          email: body.email,
          notes: body.notes || null,
          mailingStreet: body.mailingStreet || null,
          mailingCity: body.mailingCity || null,
          mailingProvince: body.mailingProvince || null,
          mailingPostalCode: body.mailingPostalCode || null,
          accountName: body.accountName || existingSale.accountName,
          sortCode: body.sortCode || existingSale.sortCode,
          accountNumber: body.accountNumber || existingSale.accountNumber,
          directDebitDate: body.directDebitDate ? new Date(body.directDebitDate) : existingSale.directDebitDate,
          applianceCoverSelected: body.applianceCoverSelected,
          boilerCoverSelected: body.boilerCoverSelected,
          boilerPriceSelected: body.boilerPriceSelected || null,
          totalPlanCost: body.totalPlanCost,
          appliances: {
            create: (body.appliances || []).map((appliance: any) => ({
              appliance: appliance.appliance,
              otherText: appliance.otherText || null,
              coverLimit: appliance.coverLimit,
              cost: appliance.cost
            }))
          }
        },
        include: {
          appliances: true,
          createdBy: {
            select: {
              id: true,
              email: true,
            }
          }
        }
      })
    })

    return NextResponse.json(updatedSale)
  } catch (error) {
    console.error('Error updating sale:', error)
    console.error('Sale ID:', id)
    console.error('Request body:', JSON.stringify(body, null, 2))
    
    // Return more specific error messages
    if (error instanceof Error) {
      return NextResponse.json(
        { error: error.message },
        { status: 500 }
      )
    }
    
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { id } = await params
    const saleId = id

    // Check if the sale exists
    const existingSale = await prisma.sale.findUnique({
      where: { id: saleId }
    })

    if (!existingSale) {
      return NextResponse.json({ error: 'Sale not found' }, { status: 404 })
    }

    // Delete the sale (appliances will be deleted automatically due to cascade)
    await prisma.sale.delete({
      where: { id: saleId }
    })

    return NextResponse.json({ message: 'Sale deleted successfully' })
  } catch (error) {
    console.error('Error deleting sale:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}