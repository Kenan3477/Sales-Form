import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function recalculateAndUpdateTotals() {
  try {
    console.log('=== RECALCULATING AND UPDATING STORED TOTALS ===\n');
    
    // Get all sales with their data
    const sales = await prisma.sale.findMany({
      include: {
        appliances: true
      }
    });

    console.log(`Processing ${sales.length} customers...\n`);

    let updatedCount = 0;
    let discrepancies = [];
    let totalSystemBefore = 0;
    let totalSystemAfter = 0;

    // First pass - identify discrepancies and calculate totals
    for (const sale of sales) {
      totalSystemBefore += sale.totalPlanCost;
      
      // Calculate correct total based on current appliance and boiler data
      let correctTotal = 0;
      
      // Add boiler price if selected (don't change this)
      if (sale.boilerCoverSelected && sale.boilerPriceSelected) {
        correctTotal += sale.boilerPriceSelected;
      }
      
      // Add appliance costs (don't change these)
      for (const appliance of sale.appliances) {
        correctTotal += appliance.cost;
      }
      
      // Round to 2 decimal places to avoid floating point issues
      correctTotal = Math.round(correctTotal * 100) / 100;
      const storedTotal = Math.round(sale.totalPlanCost * 100) / 100;
      
      // Check if there's a discrepancy (more than 1 penny difference)
      if (Math.abs(correctTotal - storedTotal) > 0.01) {
        discrepancies.push({
          id: sale.id,
          name: `${sale.customerFirstName} ${sale.customerLastName}`,
          calculated: correctTotal,
          stored: storedTotal,
          difference: correctTotal - storedTotal
        });
      }
      
      totalSystemAfter += correctTotal;
    }

    console.log('=== SUMMARY OF CHANGES ===');
    console.log(`Total customers processed: ${sales.length}`);
    console.log(`Customers with discrepancies: ${discrepancies.length}`);
    console.log(`System total before: £${totalSystemBefore.toFixed(2)}`);
    console.log(`System total after: £${totalSystemAfter.toFixed(2)}`);
    console.log(`Total reduction: £${(totalSystemBefore - totalSystemAfter).toFixed(2)}\n`);

    if (discrepancies.length > 0) {
      console.log('=== TOP 20 DISCREPANCIES TO BE FIXED ===');
      discrepancies
        .sort((a, b) => Math.abs(b.difference) - Math.abs(a.difference))
        .slice(0, 20)
        .forEach((disc, index) => {
          console.log(`${index + 1}. ${disc.name}`);
          console.log(`   Stored: £${disc.stored.toFixed(2)} → Correct: £${disc.calculated.toFixed(2)}`);
          console.log(`   Difference: ${disc.difference > 0 ? '+' : ''}£${disc.difference.toFixed(2)}\n`);
        });

      // Second pass - apply the corrections
      console.log('=== APPLYING CORRECTIONS ===');
      for (const discrepancy of discrepancies) {
        await prisma.sale.update({
          where: { id: discrepancy.id },
          data: { totalPlanCost: discrepancy.calculated }
        });
        updatedCount++;
        
        if (updatedCount % 50 === 0) {
          console.log(`Updated ${updatedCount}/${discrepancies.length} customers...`);
        }
      }
      
      console.log(`\n✅ Successfully updated ${updatedCount} customer totals`);
    } else {
      console.log('✅ No discrepancies found - all totals were already correct');
    }

    // Verify the final state
    const finalSales = await prisma.sale.findMany({
      select: {
        totalPlanCost: true
      }
    });

    const finalSystemTotal = finalSales.reduce((sum, sale) => sum + sale.totalPlanCost, 0);
    console.log(`\n=== FINAL VERIFICATION ===`);
    console.log(`Final system total: £${finalSystemTotal.toFixed(2)}`);
    console.log(`Average per customer: £${(finalSystemTotal / finalSales.length).toFixed(2)}`);
    
    console.log('\n✅ Recalculation complete - stored totals now match calculated totals');
    console.log('✅ No changes made to appliance costs or boiler prices');
    console.log('✅ Only totalPlanCost field updated to reflect correct calculations');

  } catch (error) {
    console.error('Error recalculating totals:', error);
  } finally {
    await prisma.$disconnect();
  }
}

recalculateAndUpdateTotals();