const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function fixExcessiveApplianceCosts() {
  console.log('🛠️  Fixing excessive appliance costs (£500 → realistic monthly costs)...\n');
  
  try {
    // Find all appliances with cost > £50 (unrealistic for monthly)
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
    
    console.log(`📦 Found ${expensiveAppliances.length} appliances with excessive costs:\n`);
    
    // Create a mapping of realistic monthly costs based on appliance type
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
      'Toaster': 4,
      'SKY EQUIPMENT': 15,
      'n/a': 10 // Default for unspecified items
    };
    
    const fixedAppliances = [];
    let totalSavings = 0;
    
    for (const appliance of expensiveAppliances) {
      const currentCost = appliance.cost;
      
      // Try to find a realistic cost for this appliance type
      let newCost = realisticCosts[appliance.appliance];
      
      if (!newCost) {
        // If not in our mapping, use a sensible default based on the appliance name
        if (appliance.appliance.toLowerCase().includes('wash')) {
          newCost = 19.99;
        } else if (appliance.appliance.toLowerCase().includes('fridge') || appliance.appliance.toLowerCase().includes('freezer')) {
          newCost = 10;
        } else if (appliance.appliance.toLowerCase().includes('cooker') || appliance.appliance.toLowerCase().includes('oven')) {
          newCost = 25;
        } else if (appliance.appliance.toLowerCase().includes('tv') || appliance.appliance.toLowerCase().includes('television')) {
          newCost = 15;
        } else {
          newCost = 15; // Generic appliance default
        }
      }
      
      const savings = currentCost - newCost;
      totalSavings += savings;
      
      console.log(`📦 ${appliance.appliance} (${appliance.sale.customerFirstName} ${appliance.sale.customerLastName})`);
      console.log(`   💰 Current: £${currentCost} → New: £${newCost}`);
      console.log(`   💸 Savings: £${savings.toFixed(2)}`);
      
      fixedAppliances.push({
        id: appliance.id,
        saleId: appliance.saleId,
        appliance: appliance.appliance,
        oldCost: currentCost,
        newCost: newCost,
        customer: `${appliance.sale.customerFirstName} ${appliance.sale.customerLastName}`,
        email: appliance.sale.email
      });
    }
    
    console.log(`\n📋 Summary:`);
    console.log(`   🛠️  Appliances to fix: ${fixedAppliances.length}`);
    console.log(`   💸 Total monthly savings: £${totalSavings.toFixed(2)}`);
    console.log(`   📊 Average savings per appliance: £${(totalSavings / fixedAppliances.length).toFixed(2)}`);
    
    console.log('\n⚡ Applying appliance cost fixes...\n');
    
    // Apply appliance fixes
    for (const fix of fixedAppliances) {
      await prisma.appliance.update({
        where: { id: fix.id },
        data: { cost: fix.newCost }
      });
      console.log(`✅ Fixed ${fix.appliance} for ${fix.customer}: £${fix.oldCost} → £${fix.newCost}`);
    }
    
    console.log('\n🔄 Now recalculating total costs for affected sales...\n');
    
    // Get unique sales that were affected
    const affectedSaleIds = [...new Set(fixedAppliances.map(fix => fix.saleId))];
    
    for (const saleId of affectedSaleIds) {
      // Recalculate the total cost for this sale
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
        
        console.log(`💰 Recalculated total for ${sale.customerFirstName} ${sale.customerLastName}: £${oldTotalCost} → £${newTotalCost}`);
      }
    }
    
    console.log(`\n🎉 Successfully fixed ${fixedAppliances.length} appliances and recalculated ${affectedSaleIds.length} sales!`);
    console.log(`💸 Total monthly cost savings across all customers: £${totalSavings.toFixed(2)}`);
    
    // Final verification
    console.log('\n🔍 Final verification - checking for remaining excessive costs...');
    
    const stillExpensive = await prisma.sale.findMany({
      where: {
        totalPlanCost: { gt: 200 }
      },
      include: {
        appliances: true
      }
    });
    
    if (stillExpensive.length === 0) {
      console.log('✅ No more sales with excessive costs (>£200/month)!');
    } else {
      console.log(`⚠️  ${stillExpensive.length} sales still have costs >£200/month:`);
      stillExpensive.forEach(sale => {
        const appTotal = sale.appliances.reduce((sum, app) => sum + app.cost, 0);
        console.log(`   ${sale.customerFirstName} ${sale.customerLastName}: £${sale.totalPlanCost} (${sale.appliances.length} appliances: £${appTotal})`);
      });
    }
    
  } catch (error) {
    console.error('❌ Error fixing appliance costs:', error);
  } finally {
    await prisma.$disconnect();
  }
}

fixExcessiveApplianceCosts();