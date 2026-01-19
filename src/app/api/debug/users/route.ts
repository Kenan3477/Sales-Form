import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET(request: NextRequest) {
  try {
    // Get all users from the database
    const users = await prisma.user.findMany({
      select: {
        id: true,
        email: true,
        role: true,
        createdAt: true
      }
    })

    return NextResponse.json({
      totalUsers: users.length,
      users: users.map(user => ({
        id: user.id,
        email: user.email,
        role: user.role,
        createdAt: user.createdAt
      }))
    })
  } catch (error) {
    return NextResponse.json({ 
      error: 'Failed to fetch users',
      message: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}