
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function findProblematicCustomers() {
  try {
    const sales = await prisma.sale.findMany()
    
    console.log('Looking for customers with problematic data...')
    
    for (const sale of sales) {
      // Check for fake phone numbers
      if (sale.phoneNumber && (
        sale.phoneNumber === '0000000000' ||
        sale.phoneNumber === '00000000000' ||
        sale.phoneNumber === '1111111111' ||
        sale.phoneNumber === '12345678901' ||
        /^(.)+$/.test(sale.phoneNumber) // All same digit
      )) {
        console.log(`FOUND: Customer ${sale.customerFirstName} ${sale.customerLastName}`)
        console.log(`  ID: ${sale.id}`)
        console.log(`  Email: ${sale.email}`)
        console.log(`  Phone: ${sale.phoneNumber}`)
        console.log(`  Created: ${sale.createdAt}`)
        console.log('---')
      }
    }
  } catch (error) {
    console.error('Error:', error)
  } finally {
    await prisma.$disconnect()
  }
}

findProblematicCustomers()
