import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { hash } from 'bcryptjs'

export async function POST(request: NextRequest) {
  try {
    const { email, password, role } = await request.json()
    
    if (!email || !password || !role) {
      return NextResponse.json({ error: 'Email, password, and role required' }, { status: 400 })
    }

    // Check if user already exists
    const existingUser = await prisma.user.findUnique({
      where: { email }
    })

    if (existingUser) {
      return NextResponse.json({ error: 'User already exists' }, { status: 400 })
    }

    // Hash password
    const hashedPassword = await hash(password, 12)

    // Create user
    const user = await prisma.user.create({
      data: {
        email,
        password: hashedPassword,
        role: role.toUpperCase()
      }
    })

    return NextResponse.json({ 
      success: true, 
      message: `User ${email} created successfully`,
      user: { id: user.id, email: user.email, role: user.role }
    })
  } catch (error) {
    return NextResponse.json({ 
      error: 'Failed to create user',
      message: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}