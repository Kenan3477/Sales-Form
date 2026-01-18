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
  try {
    const session = await getServerSession(authOptions)
    
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { id } = await params
    const saleId = id
    const body = await request.json()

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
          accountName: body.accountName,
          sortCode: body.sortCode,
          accountNumber: body.accountNumber,
          directDebitDate: new Date(body.directDebitDate),
          applianceCoverSelected: body.applianceCoverSelected,
          boilerCoverSelected: body.boilerCoverSelected,
          boilerPriceSelected: body.boilerPriceSelected || null,
          totalPlanCost: body.totalPlanCost,
          appliances: {
            create: body.appliances || []
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
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
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