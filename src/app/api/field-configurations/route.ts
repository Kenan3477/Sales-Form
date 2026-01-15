import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'

export async function GET() {
  try {
    const fieldConfigurations = await prisma.fieldConfiguration.findMany({
      orderBy: {
        fieldName: 'asc'
      }
    })

    return NextResponse.json(fieldConfigurations)
  } catch (error) {
    console.error('Error fetching field configurations:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

export async function PUT(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await request.json()
    const { configurations } = body

    // Update all configurations
    for (const config of configurations) {
      await prisma.fieldConfiguration.upsert({
        where: { fieldName: config.fieldName },
        update: { isRequired: config.isRequired },
        create: { 
          fieldName: config.fieldName,
          isRequired: config.isRequired 
        }
      })
    }

    const updatedConfigurations = await prisma.fieldConfiguration.findMany({
      orderBy: {
        fieldName: 'asc'
      }
    })

    return NextResponse.json(updatedConfigurations)
  } catch (error) {
    console.error('Error updating field configurations:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}