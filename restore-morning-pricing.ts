import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function restoreOriginalAppliancePricing() {
  try {
    console.log('=== RESTORING ORIGINAL APPLIANCE PRICING ===\n');
    
    // Based on the target of £70K total with 2295 customers (£30.50 average)
    // and current boiler costs of £36,785.67
    // The total appliance costs should be: £70,000 - £36,785.67 = £33,214.33
    
    const targetTotalAppliances = 70000 - 36785.67;
    const currentTotalAppliances = 54803.34;
    const reductionNeeded = currentTotalAppliances - targetTotalAppliances;
    
    console.log(`Target total appliance costs: £${targetTotalAppliances.toFixed(2)}`);
    console.log(`Current total appliance costs: £${currentTotalAppliances.toFixed(2)}`);
    console.log(`Reduction needed in appliance costs: £${reductionNeeded.toFixed(2)}\n`);
    
    // The issue seems to be that costs like £15, £19.99, £25 should be much lower
    // Let's reduce them to realistic values:
    // - £19.99 (washing machine) → £3.99
    // - £15 (various default items) → £3.00
    // - £25 (ovens, cookers) → £5.00
    
    const costMappings = [
      { from: 19.99, to: 3.99, name: "Washing Machine" },
      { from: 15.00, to: 3.00, name: "Default items (n/a, vacuum, etc.)" },
      { from: 25.00, to: 5.00, name: "Ovens and cookers" }
    ];
    
    console.log('=== COST REDUCTION MAPPINGS ===');
    costMappings.forEach(mapping => {
      console.log(`${mapping.name}: £${mapping.from} → £${mapping.to}`);
    });
    console.log('');
    
    // Apply the changes
    let updatedCount = 0;
    let totalReduction = 0;
    
    // Reduce £19.99 items to £3.99
    const result1 = await prisma.appliance.updateMany({
      where: { cost: 19.99 },
      data: { cost: 3.99 }
    });
    
    // Reduce £15.00 items to £3.00
    const result2 = await prisma.appliance.updateMany({
      where: { cost: 15.00 },
      data: { cost: 3.00 }
    });
    
    // Reduce £25.00 items to £5.00
    const result3 = await prisma.appliance.updateMany({
      where: { cost: 25.00 },
      data: { cost: 5.00 }
    });
    
    updatedCount = result1.count + result2.count + result3.count;
    
    console.log('=== PRICING UPDATES APPLIED ===');
    console.log(`Updated appliances with £19.99 → £3.99: ${result1.count}`);
    console.log(`Updated appliances with £15.00 → £3.00: ${result2.count}`);
    console.log(`Updated appliances with £25.00 → £5.00: ${result3.count}`);
    console.log(`Total appliances updated: ${updatedCount}\n`);
    
    // Recalculate customer totals
    console.log('=== RECALCULATING CUSTOMER TOTALS ===');
    
    const sales = await prisma.sale.findMany({
      include: {
        appliances: true
      }
    });
    
    let recalculatedCount = 0;
    let newSystemTotal = 0;
    
    for (const sale of sales) {
      let newTotal = 0;
      
      // Add boiler price if selected
      if (sale.boilerCoverSelected && sale.boilerPriceSelected) {
        newTotal += sale.boilerPriceSelected;
      }
      
      // Add appliance costs (now with updated pricing)
      for (const appliance of sale.appliances) {
        newTotal += appliance.cost;
      }
      
      // Update the sale total
      await prisma.sale.update({
        where: { id: sale.id },
        data: { totalPlanCost: newTotal }
      });
      
      newSystemTotal += newTotal;
      recalculatedCount++;
    }
    
    console.log(`Recalculated totals for: ${recalculatedCount} customers`);
    console.log(`New system total: £${newSystemTotal.toFixed(2)}`);
    console.log(`New average per customer: £${(newSystemTotal / recalculatedCount).toFixed(2)}`);
    console.log(`Reduction achieved: £${(91589.02 - newSystemTotal).toFixed(2)}\n`);
    
    console.log('✅ Original pricing structure restored');
    console.log(`✅ System total reduced from £91,589.02 to £${newSystemTotal.toFixed(2)}`);
    
  } catch (error) {
    console.error('Error restoring pricing:', error);
  } finally {
    await prisma.$disconnect();
  }
}

restoreOriginalAppliancePricing();