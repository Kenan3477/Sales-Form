import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function restoreOriginalPricing() {
  console.log('Starting restoration of original customer pricing...');
  
  try {
    // Get all sales with their current data
    const sales = await prisma.sale.findMany({
      include: {
        appliances: true,
        // Note: boiler info is stored directly on the sale record
      }
    });

    console.log(`Found ${sales.length} sales to process`);
    
    let totalBefore = 0;
    let totalAfter = 0;
    let updatedCount = 0;

    for (const sale of sales) {
      const currentTotal = parseFloat(sale.totalPlanCost?.toString() || '0');
      totalBefore += currentTotal;
      
      // Calculate the CORRECT total: Boiler + Appliances only
      let correctTotal = 0;
      
      // Add boiler cost if sale has boiler cover selected
      if (sale.boilerCoverSelected && sale.boilerPriceSelected) {
        correctTotal += parseFloat(sale.boilerPriceSelected.toString());
        console.log(`Sale ${sale.customerFirstName} ${sale.customerLastName}: Adding boiler £${sale.boilerPriceSelected}`);
      }
      
      // Add appliance costs
      if (sale.appliances && sale.appliances.length > 0) {
        for (const appliance of sale.appliances) {
          if (appliance.cost) {
            correctTotal += appliance.cost;
            console.log(`Sale ${sale.customerFirstName} ${sale.customerLastName}: Adding ${appliance.appliance} £${appliance.cost}`);
          }
        }
      }
      
      // Round to 2 decimal places
      correctTotal = Math.round(correctTotal * 100) / 100;
      totalAfter += correctTotal;
      
      // Update if different
      if (Math.abs(currentTotal - correctTotal) > 0.01) {
        console.log(`Updating ${sale.customerFirstName} ${sale.customerLastName}: £${currentTotal} → £${correctTotal}`);
        
        await prisma.sale.update({
          where: { id: sale.id },
          data: { totalPlanCost: correctTotal }
        });
        
        updatedCount++;
      } else {
        console.log(`${sale.customerFirstName} ${sale.customerLastName}: Already correct at £${correctTotal}`);
      }
    }
    
    console.log('\n=== PRICING RESTORATION COMPLETE ===');
    console.log(`Total sales processed: ${sales.length}`);
    console.log(`Customers updated: ${updatedCount}`);
    console.log(`Total value before: £${totalBefore.toFixed(2)}`);
    console.log(`Total value after: £${totalAfter.toFixed(2)}`);
    console.log(`Total difference: £${(totalAfter - totalBefore).toFixed(2)}`);
    
    // Verify there are no extreme values
    const extremeSales = await prisma.sale.findMany({
      where: {
        totalPlanCost: {
          gt: 1000  // Anyone over £1000/month is suspicious
        }
      },
      select: {
        customerFirstName: true,
        customerLastName: true,
        totalPlanCost: true
      }
    });
    
    if (extremeSales.length > 0) {
      console.log('\n⚠️  WARNING: Found sales with high monthly totals:');
      extremeSales.forEach((c: any) => {
        console.log(`${c.customerFirstName} ${c.customerLastName}: £${c.totalPlanCost}`);
      });
    } else {
      console.log('\n✅ All sale totals are under £1000/month');
    }
    
  } catch (error) {
    console.error('Error restoring pricing:', error);
  } finally {
    await prisma.$disconnect();
  }
}

restoreOriginalPricing();