import { PrismaClient } from '@prisma/client'
import { hash } from 'bcryptjs'

const prisma = new PrismaClient()

async function main() {
  console.log('🌱 Seeding database...')

  // Create admin user
  const adminPassword = await hash('admin123', 12)
  const admin = await prisma.user.upsert({
    where: { email: 'admin@salesportal.com' },
    update: {},
    create: {
      email: 'admin@salesportal.com',
      password: adminPassword,
      role: 'ADMIN',
    },
  })

  // Create agent user
  const agentPassword = await hash('agent123', 12)
  const agent = await prisma.user.upsert({
    where: { email: 'agent@salesportal.com' },
    update: {},
    create: {
      email: 'agent@salesportal.com',
      password: agentPassword,
      role: 'AGENT',
    },
  })

  // Create default field configurations
  const defaultFields = [
    { fieldName: 'customerFirstName', isRequired: true },
    { fieldName: 'customerLastName', isRequired: true },
    { fieldName: 'title', isRequired: false },
    { fieldName: 'phoneNumber', isRequired: true },
    { fieldName: 'email', isRequired: true },
    { fieldName: 'notes', isRequired: false },
    { fieldName: 'mailingStreet', isRequired: false },
    { fieldName: 'mailingCity', isRequired: false },
    { fieldName: 'mailingProvince', isRequired: false },
    { fieldName: 'mailingPostalCode', isRequired: false },
    { fieldName: 'accountName', isRequired: true },
    { fieldName: 'sortCode', isRequired: true },
    { fieldName: 'accountNumber', isRequired: true },
    { fieldName: 'directDebitDate', isRequired: true },
    { fieldName: 'applianceCover', isRequired: false },
    { fieldName: 'boilerCover', isRequired: false },
    { fieldName: 'applianceRows', isRequired: false },
    { fieldName: 'boilerOption', isRequired: false },
  ]

  for (const field of defaultFields) {
    await prisma.fieldConfiguration.upsert({
      where: { fieldName: field.fieldName },
      update: {},
      create: field,
    })
  }

  console.log('✅ Seeding completed!')
  console.log('Admin user: admin@salesportal.com / admin123')
  console.log('Agent user: agent@salesportal.com / agent123')
}

main()
  .catch((e) => {
    console.error(e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })