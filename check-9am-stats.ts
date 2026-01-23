import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function getMorningStats() {
  try {
    console.log('=== SYSTEM STATS AT 9AM THIS MORNING ===\n');
    
    // Get all sales with their data (as it was at 9am)
    const sales = await prisma.sale.findMany({
      include: {
        appliances: true
      }
    });

    console.log(`Total customers: ${sales.length}\n`);

    let totalSystemValue = 0;
    let totalApplianceCosts = 0;
    let totalBoilerCosts = 0;
    let customersWithBoilers = 0;
    let applianceCount = 0;
    let customerDetails: any[] = [];

    for (const sale of sales) {
      let customerTotal = 0;
      
      // Add boiler price if selected
      if (sale.boilerCoverSelected && sale.boilerPriceSelected) {
        customerTotal += sale.boilerPriceSelected;
        totalBoilerCosts += sale.boilerPriceSelected;
        customersWithBoilers++;
      }
      
      // Add appliance costs
      for (const appliance of sale.appliances) {
        customerTotal += appliance.cost;
        totalApplianceCosts += appliance.cost;
        applianceCount++;
      }
      
      totalSystemValue += customerTotal;
      
      customerDetails.push({
        name: `${sale.customerFirstName} ${sale.customerLastName}`,
        total: customerTotal,
        boilerPrice: sale.boilerPriceSelected || 0,
        applianceCount: sale.appliances.length,
        totalPlanCost: sale.totalPlanCost
      });
    }

    console.log('=== 9AM SYSTEM TOTALS ===');
    console.log(`Total System Value (calculated): £${totalSystemValue.toFixed(2)}`);
    console.log(`Average per customer: £${(totalSystemValue / sales.length).toFixed(2)}`);
    console.log('');
    
    console.log('=== BREAKDOWN ===');
    console.log(`Total appliance costs: £${totalApplianceCosts.toFixed(2)}`);
    console.log(`Total boiler costs: £${totalBoilerCosts.toFixed(2)}`);
    console.log(`Average appliance cost: £${(totalApplianceCosts / applianceCount).toFixed(2)}`);
    console.log(`Average boiler cost: £${customersWithBoilers > 0 ? (totalBoilerCosts / customersWithBoilers).toFixed(2) : '0.00'}`);
    console.log(`Customers with boilers: ${customersWithBoilers} out of ${sales.length}`);
    console.log('');

    // Check stored totals vs calculated
    const storedSystemTotal = sales.reduce((sum, sale) => sum + sale.totalPlanCost, 0);
    console.log('=== STORED VS CALCULATED ===');
    console.log(`Stored system total: £${storedSystemTotal.toFixed(2)}`);
    console.log(`Calculated system total: £${totalSystemValue.toFixed(2)}`);
    console.log(`Difference: £${Math.abs(storedSystemTotal - totalSystemValue).toFixed(2)}`);
    console.log('');

    // Show top customers by value
    customerDetails.sort((a, b) => b.total - a.total);
    console.log('=== TOP 10 CUSTOMERS BY VALUE (9AM) ===');
    customerDetails.slice(0, 10).forEach((customer, index) => {
      console.log(`${index + 1}. ${customer.name}: £${customer.total.toFixed(2)} (stored: £${customer.totalPlanCost})`);
    });
    console.log('');

    // Distribution analysis
    const ranges = [
      { min: 0, max: 25, count: 0 },
      { min: 25, max: 50, count: 0 },
      { min: 50, max: 75, count: 0 },
      { min: 75, max: 100, count: 0 },
      { min: 100, max: 150, count: 0 },
      { min: 150, max: 200, count: 0 },
      { min: 200, max: 999999, count: 0 }
    ];

    customerDetails.forEach(customer => {
      for (const range of ranges) {
        if (customer.total >= range.min && customer.total < range.max) {
          range.count++;
          break;
        }
      }
    });

    console.log('=== CUSTOMER VALUE DISTRIBUTION (9AM) ===');
    ranges.forEach(range => {
      const label = range.max === 999999 ? `£${range.min}+` : `£${range.min}-£${range.max}`;
      const percentage = ((range.count / sales.length) * 100).toFixed(1);
      console.log(`${label}: ${range.count} customers (${percentage}%)`);
    });

  } catch (error) {
    console.error('Error getting morning stats:', error);
  } finally {
    await prisma.$disconnect();
  }
}

getMorningStats();