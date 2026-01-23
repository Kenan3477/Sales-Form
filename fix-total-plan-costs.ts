import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function fixTotalPlanCosts() {
  try {
    console.log('=== FIXING TOTAL PLAN COSTS ===\n');
    
    // Get all sales with their data
    const sales = await prisma.sale.findMany({
      include: {
        appliances: true
      }
    });

    console.log(`Total sales to check: ${sales.length}\n`);

    let updatedCount = 0;
    let discrepancies = [];

    for (const sale of sales) {
      // Calculate correct total
      let correctTotal = 0;
      
      // Add boiler price if selected
      if (sale.boilerCoverSelected && sale.boilerPriceSelected) {
        correctTotal += sale.boilerPriceSelected;
      }
      
      // Add appliance costs
      for (const appliance of sale.appliances) {
        correctTotal += appliance.cost;
      }
      
      // Round to 2 decimal places to avoid floating point issues
      correctTotal = Math.round(correctTotal * 100) / 100;
      const storedTotal = Math.round(sale.totalPlanCost * 100) / 100;
      
      // Check if there's a discrepancy
      if (Math.abs(correctTotal - storedTotal) > 0.01) {
        discrepancies.push({
          id: sale.id,
          name: `${sale.customerFirstName} ${sale.customerLastName}`,
          calculated: correctTotal,
          stored: storedTotal,
          difference: correctTotal - storedTotal
        });
        
        // Update the stored total to match the calculation
        await prisma.sale.update({
          where: { id: sale.id },
          data: { totalPlanCost: correctTotal }
        });
        
        updatedCount++;
      }
    }

    console.log(`=== SUMMARY ===`);
    console.log(`Total sales processed: ${sales.length}`);
    console.log(`Sales with corrected totals: ${updatedCount}`);
    console.log(`Sales left unchanged: ${sales.length - updatedCount}\n`);

    if (discrepancies.length > 0) {
      console.log(`=== DISCREPANCIES FOUND AND FIXED ===`);
      discrepancies.forEach((disc, index) => {
        console.log(`${index + 1}. ${disc.name} (${disc.id})`);
        console.log(`   Was: £${disc.stored.toFixed(2)}`);
        console.log(`   Now: £${disc.calculated.toFixed(2)}`);
        console.log(`   Diff: ${disc.difference > 0 ? '+' : ''}£${disc.difference.toFixed(2)}\n`);
      });
    } else {
      console.log('✅ All totals were already correct');
    }

    // Calculate new system total
    const updatedSales = await prisma.sale.findMany({
      select: {
        totalPlanCost: true
      }
    });

    const newSystemTotal = updatedSales.reduce((sum, sale) => sum + sale.totalPlanCost, 0);
    console.log(`=== NEW SYSTEM TOTAL ===`);
    console.log(`Total System Value: £${newSystemTotal.toFixed(2)}`);
    console.log(`Average per sale: £${(newSystemTotal / updatedSales.length).toFixed(2)}`);

  } catch (error) {
    console.error('Error fixing total plan costs:', error);
  } finally {
    await prisma.$disconnect();
  }
}

fixTotalPlanCosts();