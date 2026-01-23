import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function fixProblematicCustomer() {
  try {
    // Find the customer with fake phone number
    const customer = await prisma.sale.findUnique({
      where: { id: 'cmkk45nf4037rnl51wettd6ny' }
    })
    
    if (!customer) {
      console.log('Customer not found')
      return
    }
    
    console.log('Current customer data:')
    console.log(`Name: ${customer.customerFirstName} ${customer.customerLastName}`)
    console.log(`Email: ${customer.email}`)
    console.log(`Phone: ${customer.phoneNumber}`)
    
    // This customer appears to be legitimate (real name and email) but phone number is corrupted
    // Since we can't guess the real phone number, we'll mark it as missing rather than fake
    // A missing phone number is better than fake data
    
    const updated = await prisma.sale.update({
      where: { id: 'cmkk45nf4037rnl51wettd6ny' },
      data: {
        phoneNumber: 'MISSING' // Mark as missing data - NOT fake, just incomplete
      }
    })
    
    console.log('✅ Updated customer data:')
    console.log(`Name: ${updated.customerFirstName} ${updated.customerLastName}`)
    console.log(`Email: ${updated.email}`)
    console.log(`Phone: ${updated.phoneNumber || 'NULL (removed fake number)'}`)
    console.log('')
    console.log('🔒 Customer data integrity restored - fake phone number removed')
    
  } catch (error) {
    console.error('Error:', error)
  } finally {
    await prisma.$disconnect()
  }
}

fixProblematicCustomer()