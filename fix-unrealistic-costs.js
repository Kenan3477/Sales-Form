const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function fixUnrealisticApplianceCosts() {
  console.log('🛠️  Fixing unrealistic appliance costs (£500 → realistic monthly costs)...\n');
  
  try {
    // Find all appliances with unrealistic costs (over £50/month)
    const expensiveAppliances = await prisma.appliance.findMany({
      where: {
        cost: { gt: 50 }
      },
      include: {
        sale: true
      },
      orderBy: {
        cost: 'desc'
      }
    });
    
    console.log(`📦 Found ${expensiveAppliances.length} appliances with unrealistic costs (>£50/month):\n`);
    
    if (expensiveAppliances.length === 0) {
      console.log('✅ No unrealistic appliance costs found!');
      return;
    }
    
    // Show examples
    const examples = expensiveAppliances.slice(0, 10);
    for (const app of examples) {
      console.log(`   - ${app.appliance}: £${app.cost}/month (${app.sale.customerFirstName} ${app.sale.customerLastName})`);
    }
    if (expensiveAppliances.length > 10) {
      console.log(`   ... and ${expensiveAppliances.length - 10} more`);
    }
    
    // Realistic monthly costs for common appliances
    const realisticCosts = {
      'Washing Machine': 19.99,
      'Fridge / Freezer': 10,
      'Fridge/Freezer': 10,
      'Fridge Freezer': 10,
      'Tumble Dryer': 15,
      'Dishwasher': 15,
      'Built in Oven': 25,
      'Freestanding cooker': 25,
      'Electric cooker': 25,
      'Gas cooker': 25,
      'Oven': 25,
      'Hob': 15,
      'Microwave': 15,
      'Vacuum Cleaner': 15,
      'TV': 15,
      'Television': 15,
      'Freezer': 10,
      'Freezer - Undercounter': 10,
      'Coffee Machine': 15,
      'Kettle': 4,
      'Toaster': 4
    };
    
    console.log('\n⚡ Applying realistic pricing...\n');
    
    let fixedCount = 0;
    let totalSavings = 0;
    
    for (const appliance of expensiveAppliances) {
      const currentCost = appliance.cost;
      
      // Determine realistic cost
      let newCost = realisticCosts[appliance.appliance];
      
      if (!newCost) {
        // Default based on appliance type
        if (appliance.appliance.toLowerCase().includes('wash')) {
          newCost = 19.99;
        } else if (appliance.appliance.toLowerCase().includes('fridge') || 
                   appliance.appliance.toLowerCase().includes('freezer')) {
          newCost = 10;
        } else if (appliance.appliance.toLowerCase().includes('cooker') || 
                   appliance.appliance.toLowerCase().includes('oven')) {
          newCost = 25;
        } else if (appliance.appliance.toLowerCase().includes('tv') || 
                   appliance.appliance.toLowerCase().includes('television')) {
          newCost = 15;
        } else {
          newCost = 15; // Generic default
        }
      }
      
      const savings = currentCost - newCost;
      totalSavings += savings;
      
      // Update the appliance cost
      await prisma.appliance.update({
        where: { id: appliance.id },
        data: { cost: newCost }
      });
      
      console.log(`✅ ${appliance.appliance} (${appliance.sale.customerFirstName} ${appliance.sale.customerLastName}): £${currentCost} → £${newCost}`);
      fixedCount++;
    }
    
    console.log(`\n🎉 Fixed ${fixedCount} appliances!`);
    console.log(`💸 Total monthly cost reduction: £${totalSavings.toFixed(2)}`);
    
    // Now recalculate totals for affected sales
    console.log('\n🔄 Recalculating total costs for affected customers...\n');
    
    const affectedSaleIds = [...new Set(expensiveAppliances.map(app => app.saleId))];
    let recalculatedCount = 0;
    
    for (const saleId of affectedSaleIds) {
      const sale = await prisma.sale.findUnique({
        where: { id: saleId },
        include: { appliances: true }
      });
      
      if (sale) {
        const newApplianceTotal = sale.appliances.reduce((sum, app) => sum + app.cost, 0);
        const boilerPrice = sale.boilerCoverSelected && sale.boilerPriceSelected ? sale.boilerPriceSelected : 0;
        const newTotalCost = newApplianceTotal + boilerPrice;
        
        const oldTotalCost = sale.totalPlanCost;
        
        await prisma.sale.update({
          where: { id: saleId },
          data: { totalPlanCost: newTotalCost }
        });
        
        console.log(`💰 ${sale.customerFirstName} ${sale.customerLastName}: £${oldTotalCost} → £${newTotalCost}`);
        recalculatedCount++;
      }
    }
    
    console.log(`\n📊 Summary:`);
    console.log(`   🔧 Appliances fixed: ${fixedCount}`);
    console.log(`   💰 Customers recalculated: ${recalculatedCount}`);
    console.log(`   💸 Monthly savings: £${totalSavings.toFixed(2)}`);
    console.log(`   📈 Average savings per customer: £${(totalSavings / recalculatedCount).toFixed(2)}`);
    
    // Final verification
    console.log('\n🔍 Final check for extreme prices...');
    
    const stillHighPrices = await prisma.sale.findMany({
      where: {
        totalPlanCost: { gt: 200 }
      },
      select: {
        customerFirstName: true,
        customerLastName: true,
        totalPlanCost: true
      },
      take: 5
    });
    
    if (stillHighPrices.length === 0) {
      console.log('✅ No more customers with pricing above £200/month!');
    } else {
      console.log(`⚠️  ${stillHighPrices.length} customers still have high prices (may need manual review)`);
      stillHighPrices.forEach(sale => {
        console.log(`   ${sale.customerFirstName} ${sale.customerLastName}: £${sale.totalPlanCost}`);
      });
    }
    
  } catch (error) {
    console.error('❌ Error fixing appliance costs:', error);
  } finally {
    await prisma.$disconnect();
  }
}

fixUnrealisticApplianceCosts();