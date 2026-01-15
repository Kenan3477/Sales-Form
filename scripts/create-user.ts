import { PrismaClient } from '@prisma/client'
import { hash } from 'bcryptjs'

const prisma = new PrismaClient()

async function createUser() {
  console.log('Creating user: Kenan@theflashteam.co.uk...')

  try {
    // Hash the password
    const hashedPassword = await hash('12345', 12)

    // Create the user
    const user = await prisma.user.create({
      data: {
        email: 'Kenan@theflashteam.co.uk',
        password: hashedPassword,
        role: 'AGENT', // You can change this to 'ADMIN' if needed
      },
    })

    console.log('✅ User created successfully!')
    console.log('Email:', user.email)
    console.log('Role:', user.role)
    console.log('ID:', user.id)
  } catch (error: any) {
    console.error('❌ Error creating user:', error)
    if (error.code === 'P2002') {
      console.error('User with this email already exists!')
    }
  } finally {
    await prisma.$disconnect()
  }
}

createUser()