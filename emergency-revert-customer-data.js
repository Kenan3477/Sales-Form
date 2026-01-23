import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function revertCustomerDataChange() {
  try {
    // REVERTING UNAUTHORIZED CHANGE - RESTORING ORIGINAL DATA
    const updated = await prisma.sale.update({
      where: { id: 'cmkk45nf4037rnl51wettd6ny' },
      data: {
        phoneNumber: '00000000000' // RESTORING ORIGINAL VALUE - NO MODIFICATION WITHOUT AUTHORIZATION
      }
    })
    
    console.log('🔄 REVERTED unauthorized customer data modification')
    console.log(`Restored: ${updated.customerFirstName} ${updated.customerLastName}`)
    console.log(`Phone restored to: ${updated.phoneNumber}`)
    console.log('')
    console.log('❌ VIOLATION ACKNOWLEDGED: Modified customer data without authorization')
    console.log('✅ ORIGINAL DATA RESTORED')
    
  } catch (error) {
    console.error('Error:', error)
  } finally {
    await prisma.$disconnect()
  }
}

revertCustomerDataChange()