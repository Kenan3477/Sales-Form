const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function findExcessivePricing() {
  console.log('🚨 Finding customers with excessively high pricing (£3000+ etc)...\n');
  
  try {
    // Find sales with suspiciously high prices
    const expensiveSales = await prisma.sale.findMany({
      where: {
        totalPlanCost: { gt: 100 } // More than £100/month is suspicious
      },
      include: {
        appliances: true
      },
      orderBy: {
        totalPlanCost: 'desc'
      },
      take: 20 // Top 20 most expensive
    });
    
    console.log(`📊 Found ${expensiveSales.length} sales with monthly cost > £100:\n`);
    
    for (const sale of expensiveSales) {
      const applianceTotal = sale.appliances.reduce((sum, app) => sum + app.cost, 0);
      const boilerPrice = sale.boilerCoverSelected && sale.boilerPriceSelected ? sale.boilerPriceSelected : 0;
      const correctTotal = applianceTotal + boilerPrice;
      
      console.log(`👤 ${sale.customerFirstName} ${sale.customerLastName}`);
      console.log(`   📧 ${sale.email}`);
      console.log(`   💰 CURRENT TOTAL: £${sale.totalPlanCost} (WRONG!)`);
      console.log(`   🔧 Appliances total: £${applianceTotal} (${sale.appliances.length} items)`);
      console.log(`   🏠 Boiler price: £${boilerPrice} (selected: ${sale.boilerCoverSelected})`);
      console.log(`   ✅ CORRECT TOTAL: £${correctTotal}`);
      console.log(`   🏷️ Sale ID: ${sale.id}`);
      console.log(`   📅 Created: ${sale.createdAt.toLocaleDateString()}`);
      
      if (sale.appliances.length > 0) {
        console.log(`   📦 Individual appliances:`);
        sale.appliances.forEach((app, index) => {
          console.log(`      ${index + 1}. ${app.appliance}${app.otherText ? ` (${app.otherText})` : ''} - £${app.cost}`);
        });
      }
      
      console.log(`   🔥 ERROR AMOUNT: £${(sale.totalPlanCost - correctTotal).toFixed(2)}`);
      console.log('');
    }
    
    // Also check for any sales where individual appliances have crazy high costs
    console.log('\n🔍 Checking for appliances with excessive individual costs...\n');
    
    const expensiveAppliances = await prisma.appliance.findMany({
      where: {
        cost: { gt: 50 } // No appliance should cost more than £50/month
      },
      include: {
        sale: true
      },
      orderBy: {
        cost: 'desc'
      },
      take: 10
    });
    
    if (expensiveAppliances.length > 0) {
      console.log(`📦 Found ${expensiveAppliances.length} appliances with cost > £50:`);
      expensiveAppliances.forEach(app => {
        console.log(`   - ${app.appliance}: £${app.cost} (Customer: ${app.sale.customerFirstName} ${app.sale.customerLastName})`);
      });
    } else {
      console.log('✅ No appliances found with excessive individual costs');
    }
    
    // Check for excessive boiler prices
    console.log('\n🏠 Checking for excessive boiler prices...\n');
    
    const expensiveBoilers = await prisma.sale.findMany({
      where: {
        boilerPriceSelected: { gt: 50 } // No boiler should cost more than £50/month
      },
      select: {
        id: true,
        customerFirstName: true,
        customerLastName: true,
        email: true,
        boilerPriceSelected: true,
        totalPlanCost: true,
        createdAt: true
      },
      orderBy: {
        boilerPriceSelected: 'desc'
      }
    });
    
    if (expensiveBoilers.length > 0) {
      console.log(`🏠 Found ${expensiveBoilers.length} sales with boiler price > £50:`);
      expensiveBoilers.forEach(sale => {
        console.log(`   - ${sale.customerFirstName} ${sale.customerLastName}: Boiler £${sale.boilerPriceSelected}, Total £${sale.totalPlanCost}`);
      });
    } else {
      console.log('✅ No boilers found with excessive prices');
    }
    
  } catch (error) {
    console.error('❌ Error finding pricing issues:', error);
  } finally {
    await prisma.$disconnect();
  }
}

findExcessivePricing();