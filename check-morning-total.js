const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function checkMorningTotal() {
  try {
    console.log('Checking system total from this morning...\n');
    
    // Get all customers with their data
    const customers = await prisma.customer.findMany({
      include: {
        boilerCover: true,
        customerAppliances: {
          include: {
            appliance: true
          }
        }
      }
    });

    console.log(`Total customers: ${customers.length}\n`);

    let totalSystemValue = 0;
    let customerDetails = [];

    for (const customer of customers) {
      let customerTotal = 0;
      
      // Add boiler price if selected
      if (customer.boilerCover) {
        customerTotal += customer.boilerCover.price;
      }
      
      // Add appliance costs
      for (const custAppliance of customer.customerAppliances) {
        customerTotal += custAppliance.appliance.cost;
      }
      
      totalSystemValue += customerTotal;
      
      customerDetails.push({
        name: `${customer.firstName} ${customer.lastName}`,
        total: customerTotal,
        boilerPrice: customer.boilerCover ? customer.boilerCover.price : 0,
        applianceCount: customer.customerAppliances.length,
        applianceCosts: customer.customerAppliances.map(ca => ({
          name: ca.appliance.name,
          cost: ca.appliance.cost
        }))
      });
    }

    console.log('=== SYSTEM TOTAL FROM THIS MORNING ===');
    console.log(`Total System Value: £${totalSystemValue.toFixed(2)}`);
    console.log(`Average per customer: £${(totalSystemValue / customers.length).toFixed(2)}\n`);

    // Show customers sorted by total descending
    customerDetails.sort((a, b) => b.total - a.total);
    
    console.log('=== TOP 10 CUSTOMERS BY VALUE ===');
    customerDetails.slice(0, 10).forEach((customer, index) => {
      console.log(`${index + 1}. ${customer.name}: £${customer.total.toFixed(2)}`);
      console.log(`   Boiler: £${customer.boilerPrice.toFixed(2)}`);
      console.log(`   Appliances (${customer.applianceCount}): ${customer.applianceCosts.map(a => `${a.name} £${a.cost}`).join(', ')}`);
      console.log('');
    });

    // Show distribution
    const ranges = [
      { min: 0, max: 50, count: 0 },
      { min: 50, max: 100, count: 0 },
      { min: 100, max: 200, count: 0 },
      { min: 200, max: 500, count: 0 },
      { min: 500, max: 1000, count: 0 },
      { min: 1000, max: 999999, count: 0 }
    ];

    customerDetails.forEach(customer => {
      for (const range of ranges) {
        if (customer.total >= range.min && customer.total < range.max) {
          range.count++;
          break;
        }
      }
    });

    console.log('=== CUSTOMER VALUE DISTRIBUTION ===');
    ranges.forEach(range => {
      const label = range.max === 999999 ? `£${range.min}+` : `£${range.min}-£${range.max}`;
      console.log(`${label}: ${range.count} customers`);
    });

  } catch (error) {
    console.error('Error checking morning total:', error);
  } finally {
    await prisma.$disconnect();
  }
}

checkMorningTotal();