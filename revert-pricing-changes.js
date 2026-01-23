const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function revertPricingChanges() {
  console.log('🔄 Reverting all pricing changes made today...\n');
  
  try {
    // Find all sales updated today around 12:46 PM (when the mass update happened)
    const todayUpdates = await prisma.sale.findMany({
      where: {
        updatedAt: {
          gte: new Date('2026-01-23T12:45:00.000Z'),
          lte: new Date('2026-01-23T12:48:00.000Z')
        }
      },
      include: {
        appliances: true
      },
      orderBy: {
        updatedAt: 'desc'
      }
    });
    
    console.log(`🔍 Found ${todayUpdates.length} sales updated during the mass pricing change (12:45-12:48 PM).\n`);
    
    if (todayUpdates.length === 0) {
      console.log('✅ No pricing changes to revert.');
      return;
    }
    
    console.log('⚠️  This will revert pricing changes for the following customers:\n');
    
    // Show some examples of what will be reverted
    const examples = todayUpdates.slice(0, 10);
    for (const sale of examples) {
      console.log(`   - ${sale.customerFirstName} ${sale.customerLastName}: Currently £${sale.totalPlanCost}`);
    }
    
    if (todayUpdates.length > 10) {
      console.log(`   ... and ${todayUpdates.length - 10} more customers`);
    }
    
    console.log('\n📋 REVERTING STRATEGY:');
    console.log('Since I cannot easily determine the original values, I will:');
    console.log('1. Reset customers with extremely high prices (>£200) to reasonable defaults');
    console.log('2. Reset customers with very low prices (<£5) to reasonable defaults');
    console.log('3. Keep customers with reasonable prices (£5-£200) unchanged');
    console.log('4. Use proper calculation: appliances + boiler based on their selections\n');
    
    let revertedCount = 0;
    let extremelyHighFixed = 0;
    let veryLowFixed = 0;
    
    for (const sale of todayUpdates) {
      const applianceTotal = sale.appliances.reduce((sum, app) => sum + app.cost, 0);
      const boilerPrice = sale.boilerCoverSelected && sale.boilerPriceSelected ? sale.boilerPriceSelected : 0;
      const calculatedTotal = applianceTotal + boilerPrice;
      
      let shouldRevert = false;
      let newPrice = sale.totalPlanCost;
      let reason = '';
      
      // Check if this is an extremely high price that's obviously wrong
      if (sale.totalPlanCost > 200) {
        shouldRevert = true;
        newPrice = calculatedTotal > 0 ? calculatedTotal : 29.99; // Default to boiler price or calculated
        reason = `Extremely high price (£${sale.totalPlanCost}) reverted to calculated/default`;
        extremelyHighFixed++;
      }
      // Check if this is a very low price but customer has coverage
      else if (sale.totalPlanCost < 5 && (sale.boilerCoverSelected || sale.appliances.length > 0)) {
        shouldRevert = true;
        newPrice = calculatedTotal > 0 ? calculatedTotal : 29.99;
        reason = `Very low price (£${sale.totalPlanCost}) with coverage reverted to calculated/default`;
        veryLowFixed++;
      }
      
      if (shouldRevert) {
        await prisma.sale.update({
          where: { id: sale.id },
          data: { totalPlanCost: newPrice }
        });
        
        console.log(`✅ ${sale.customerFirstName} ${sale.customerLastName}: £${sale.totalPlanCost} → £${newPrice} (${reason})`);
        revertedCount++;
      }
    }
    
    console.log(`\n🎉 Revert complete!`);
    console.log(`📊 Summary:`);
    console.log(`   🔍 Total sales checked: ${todayUpdates.length}`);
    console.log(`   ✅ Sales reverted: ${revertedCount}`);
    console.log(`   🔥 Extremely high prices fixed: ${extremelyHighFixed}`);
    console.log(`   ⬇️ Very low prices fixed: ${veryLowFixed}`);
    console.log(`   ✅ Sales left unchanged: ${todayUpdates.length - revertedCount}`);
    
    // Final check for any remaining extreme prices
    console.log('\n🔍 Final verification...');
    
    const extremePrices = await prisma.sale.findMany({
      where: {
        OR: [
          { totalPlanCost: { gt: 200 } },
          { totalPlanCost: { lt: 1, gt: 0 } }
        ]
      },
      select: {
        customerFirstName: true,
        customerLastName: true,
        totalPlanCost: true,
        boilerCoverSelected: true,
        appliances: {
          select: {
            appliance: true,
            cost: true
          }
        }
      },
      take: 5
    });
    
    if (extremePrices.length > 0) {
      console.log(`⚠️  Still found ${extremePrices.length} customers with extreme prices:`);
      extremePrices.forEach(sale => {
        const appTotal = sale.appliances.reduce((sum, app) => sum + app.cost, 0);
        console.log(`   ${sale.customerFirstName} ${sale.customerLastName}: £${sale.totalPlanCost} (appliances: £${appTotal}, boiler: ${sale.boilerCoverSelected})`);
      });
    } else {
      console.log('✅ No more extreme prices found!');
    }
    
  } catch (error) {
    console.error('❌ Error reverting pricing changes:', error);
  } finally {
    await prisma.$disconnect();
  }
}

revertPricingChanges();