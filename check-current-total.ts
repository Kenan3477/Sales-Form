import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function getCurrentTotal() {
  try {
    console.log('=== CURRENT SYSTEM ANALYSIS ===\n');
    
    // Get all sales (customers) with their data
    const sales = await prisma.sale.findMany({
      include: {
        appliances: true
      }
    });

    console.log(`Total sales: ${sales.length}\n`);

    let totalSystemValue = 0;
    let customerDetails: any[] = [];

    for (const sale of sales) {
      let customerTotal = 0;
      
      // Add boiler price if selected
      if (sale.boilerCoverSelected && sale.boilerPriceSelected) {
        customerTotal += sale.boilerPriceSelected;
      }
      
      // Add appliance costs
      for (const appliance of sale.appliances) {
        customerTotal += appliance.cost;
      }
      
      totalSystemValue += customerTotal;
      
      customerDetails.push({
        id: sale.id,
        name: `${sale.customerFirstName} ${sale.customerLastName}`,
        total: customerTotal,
        boilerPrice: sale.boilerPriceSelected || 0,
        applianceCount: sale.appliances.length,
        applianceCosts: sale.appliances.map((a: any) => ({
          name: a.appliance,
          cost: a.cost
        })),
        totalPlanCost: sale.totalPlanCost
      });
    }

    console.log('=== CURRENT SYSTEM TOTAL ===');
    console.log(`Total System Value: £${totalSystemValue.toFixed(2)}`);
    console.log(`Average per sale: £${(totalSystemValue / sales.length).toFixed(2)}\n`);

    // Show customers sorted by total descending
    customerDetails.sort((a, b) => b.total - a.total);
    
    console.log('=== TOP 10 CUSTOMERS BY VALUE ===');
    customerDetails.slice(0, 10).forEach((customer, index) => {
      console.log(`${index + 1}. ${customer.name}: £${customer.total.toFixed(2)} (Plan Cost: £${customer.totalPlanCost})`);
      console.log(`   Boiler: £${customer.boilerPrice.toFixed(2)}`);
      console.log(`   Appliances (${customer.applianceCount}): ${customer.applianceCosts.map((a: any) => `${a.name} £${a.cost}`).join(', ')}`);
      console.log('');
    });

    // Check for discrepancies between calculated and stored totals
    console.log('\n=== CHECKING FOR DISCREPANCIES ===');
    let discrepancies = 0;
    customerDetails.forEach(customer => {
      if (Math.abs(customer.total - customer.totalPlanCost) > 0.01) {
        discrepancies++;
        console.log(`⚠️  ${customer.name}: Calculated £${customer.total.toFixed(2)} vs Stored £${customer.totalPlanCost}`);
      }
    });
    
    if (discrepancies === 0) {
      console.log('✅ All calculated totals match stored totals');
    } else {
      console.log(`❌ Found ${discrepancies} discrepancies between calculated and stored totals`);
    }

    // Get unique appliance names and costs
    const applianceMap = new Map();
    customerDetails.forEach(customer => {
      customer.applianceCosts.forEach((appliance: any) => {
        if (!applianceMap.has(appliance.name)) {
          applianceMap.set(appliance.name, new Set());
        }
        applianceMap.get(appliance.name).add(appliance.cost);
      });
    });

    console.log('\n=== APPLIANCE COSTS IN USE ===');
    Array.from(applianceMap.entries()).forEach(([name, costs]) => {
      const costsArray = Array.from(costs) as number[];
      costsArray.sort((a, b) => a - b);
      const suspicious = costsArray.some(cost => cost > 50);
      const flag = suspicious ? ' ⚠️  SUSPICIOUS' : '';
      console.log(`${name}: £${costsArray.join(', £')}${flag}`);
    });

    // Check unique boiler prices
    const boilerPrices = new Set();
    customerDetails.forEach(customer => {
      if (customer.boilerPrice > 0) {
        boilerPrices.add(customer.boilerPrice);
      }
    });

    console.log('\n=== BOILER PRICES IN USE ===');
    Array.from(boilerPrices).sort((a: any, b: any) => a - b).forEach(price => {
      console.log(`Boiler: £${price}`);
    });

    return totalSystemValue;

  } catch (error) {
    console.error('Error checking total:', error);
  } finally {
    await prisma.$disconnect();
  }
}

getCurrentTotal();