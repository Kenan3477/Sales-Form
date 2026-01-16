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
            name: true,
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