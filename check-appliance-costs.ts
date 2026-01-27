import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function checkApplianceCosts() {
  try {
    // Get the most recent sales with their appliances
    const recentSales = await prisma.sale.findMany({
      include: {
        appliances: true
      },
      orderBy: { createdAt: 'desc' },
      take: 5
    })

    console.log('\n🧮 Checking appliance cost calculations:')
    console.log('==========================================')

    for (const sale of recentSales) {
      console.log(`\n📊 Sale: ${sale.customerFirstName} ${sale.customerLastName}`)
      console.log(`   Date: ${sale.createdAt.toISOString()}`)
      console.log(`   Total Cost: £${sale.totalPlanCost}`)
      console.log(`   Appliances: ${sale.appliances.length}`)
      
      if (sale.appliances.length > 0) {
        const totalApplianceCost = sale.appliances.reduce((sum, app) => sum + app.cost, 0)
        const expectedPerAppCost = totalApplianceCost / sale.appliances.length
        const actualCosts = sale.appliances.map(app => app.cost)
        const allSame = actualCosts.every(cost => Math.abs(cost - actualCosts[0]) < 0.01)
        
        console.log(`   Total Appliance Cost: £${totalApplianceCost.toFixed(2)}`)
        console.log(`   Expected Per-App: £${expectedPerAppCost.toFixed(2)}`)
        console.log(`   All costs same? ${allSame ? '✅ Yes' : '❌ No'}`)
        
        sale.appliances.forEach((appliance, index) => {
          console.log(`     ${index + 1}. ${appliance.appliance}: £${appliance.cost}/month (Cover: £${appliance.coverLimit})`)
        })
      }
    }

  } catch (error) {
    console.error('Error checking appliance costs:', error)
  } finally {
    await prisma.$disconnect()
  }
}

checkApplianceCosts()