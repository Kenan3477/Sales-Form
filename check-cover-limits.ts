import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function checkCoverLimits() {
  try {
    // Get the latest 10 sales with their appliances
    const sales = await prisma.sale.findMany({
      include: {
        appliances: true
      },
      orderBy: { createdAt: 'desc' },
      take: 10
    })

    console.log('\n🔍 Checking recent sales for coverLimit issues:')
    console.log('================================================')

    for (const sale of sales) {
      console.log(`\n📊 Sale: ${sale.customerFirstName} ${sale.customerLastName}`)
      console.log(`   Date: ${sale.createdAt.toISOString()}`)
      console.log(`   Appliances: ${sale.appliances.length}`)
      
      for (const appliance of sale.appliances) {
        const coverLimitStatus = isNaN(appliance.coverLimit) ? '❌ NaN' : 
                                appliance.coverLimit === 0 ? '⚠️ Zero' : '✅ Valid'
        const costStatus = isNaN(appliance.cost) ? '❌ NaN' : 
                          appliance.cost === 0 ? '⚠️ Zero' : '✅ Valid'
        
        console.log(`     - ${appliance.appliance}: Cover Limit: £${appliance.coverLimit} ${coverLimitStatus}, Cost: £${appliance.cost} ${costStatus}`)
      }
    }

    // Check for any appliances with invalid values
    const invalidAppliances = await prisma.appliance.findMany({
      where: {
        OR: [
          { coverLimit: 0 },
          { cost: 0 }
        ]
      },
      include: {
        sale: {
          select: {
            customerFirstName: true,
            customerLastName: true,
            createdAt: true
          }
        }
      },
      orderBy: {
        sale: {
          createdAt: 'desc'
        }
      },
      take: 20
    })

    console.log(`\n⚠️ Found ${invalidAppliances.length} appliances with zero values:`)
    if (invalidAppliances.length > 0) {
      for (const appliance of invalidAppliances) {
        console.log(`   - ${appliance.sale.customerFirstName} ${appliance.sale.customerLastName}: ${appliance.appliance} (Cover: £${appliance.coverLimit}, Cost: £${appliance.cost})`)
      }
    }

  } catch (error) {
    console.error('Error checking coverLimits:', error)
  } finally {
    await prisma.$disconnect()
  }
}

checkCoverLimits()