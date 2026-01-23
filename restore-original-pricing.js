const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function restoreOriginalPricing() {
  console.log('Starting restoration of original customer pricing...');
  
  try {
    // Get all customers with their current data
    const customers = await prisma.customer.findMany({
      include: {
        appliances: true,
        boiler: true
      }
    });

    console.log(`Found ${customers.length} customers to process`);
    
    let totalBefore = 0;
    let totalAfter = 0;
    let updatedCount = 0;

    for (const customer of customers) {
      const currentTotal = parseFloat(customer.monthlyTotal || 0);
      totalBefore += currentTotal;
      
      // Calculate the CORRECT total: Boiler + Appliances only
      let correctTotal = 0;
      
      // Add boiler cost if customer has a boiler
      if (customer.boiler && customer.boiler.price) {
        correctTotal += parseFloat(customer.boiler.price);
        console.log(`Customer ${customer.firstName} ${customer.lastName}: Adding boiler £${customer.boiler.price}`);
      }
      
      // Add appliance costs
      if (customer.appliances && customer.appliances.length > 0) {
        for (const appliance of customer.appliances) {
          if (appliance.cost) {
            correctTotal += parseFloat(appliance.cost);
            console.log(`Customer ${customer.firstName} ${customer.lastName}: Adding ${appliance.type} £${appliance.cost}`);
          }
        }
      }
      
      // Round to 2 decimal places
      correctTotal = Math.round(correctTotal * 100) / 100;
      totalAfter += correctTotal;
      
      // Update if different
      if (Math.abs(currentTotal - correctTotal) > 0.01) {
        console.log(`Updating ${customer.firstName} ${customer.lastName}: £${currentTotal} → £${correctTotal}`);
        
        await prisma.customer.update({
          where: { id: customer.id },
          data: { monthlyTotal: correctTotal.toString() }
        });
        
        updatedCount++;
      } else {
        console.log(`${customer.firstName} ${customer.lastName}: Already correct at £${correctTotal}`);
      }
    }
    
    console.log('\n=== PRICING RESTORATION COMPLETE ===');
    console.log(`Total customers processed: ${customers.length}`);
    console.log(`Customers updated: ${updatedCount}`);
    console.log(`Total value before: £${totalBefore.toFixed(2)}`);
    console.log(`Total value after: £${totalAfter.toFixed(2)}`);
    console.log(`Total difference: £${(totalAfter - totalBefore).toFixed(2)}`);
    
    // Verify there are no extreme values
    const extremeCustomers = await prisma.customer.findMany({
      where: {
        monthlyTotal: {
          gt: "1000"  // Anyone over £1000/month is suspicious
        }
      },
      select: {
        firstName: true,
        lastName: true,
        monthlyTotal: true
      }
    });
    
    if (extremeCustomers.length > 0) {
      console.log('\n⚠️  WARNING: Found customers with high monthly totals:');
      extremeCustomers.forEach(c => {
        console.log(`${c.firstName} ${c.lastName}: £${c.monthlyTotal}`);
      });
    } else {
      console.log('\n✅ All customer totals are under £1000/month');
    }
    
  } catch (error) {
    console.error('Error restoring pricing:', error);
  } finally {
    await prisma.$disconnect();
  }
}

restoreOriginalPricing();