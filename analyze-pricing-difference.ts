import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function restoreOriginalPricing() {
  try {
    console.log('=== RESTORING ORIGINAL PRICING STRUCTURE ===\n');
    
    // The issue is that the pricing logic should be: Boiler + Appliances ONLY
    // But we need to check if the current appliance costs are inflated
    
    // First, let's see what a typical "morning" pricing structure should look like
    // Based on your request, the total should be around £70K for 2295 customers
    // That's about £30.50 per customer on average
    
    const targetSystemTotal = 70000;
    const customerCount = 2295;
    const targetAveragePerCustomer = targetSystemTotal / customerCount;
    
    console.log(`Target system total: £${targetSystemTotal.toLocaleString()}`);
    console.log(`Current customer count: ${customerCount}`);
    console.log(`Target average per customer: £${targetAveragePerCustomer.toFixed(2)}\n`);
    
    // Get current state
    const sales = await prisma.sale.findMany({
      include: {
        appliances: true
      }
    });
    
    let currentTotal = 0;
    sales.forEach(sale => {
      currentTotal += sale.totalPlanCost;
    });
    
    console.log(`Current system total: £${currentTotal.toFixed(2)}`);
    console.log(`Current average per customer: £${(currentTotal / sales.length).toFixed(2)}`);
    console.log(`Difference from target: £${(currentTotal - targetSystemTotal).toFixed(2)}\n`);
    
    // The problem seems to be that appliances costs might be too high
    // Let's check what the average appliance cost per customer is
    
    let totalApplianceCosts = 0;
    let totalBoilerCosts = 0;
    let applianceCount = 0;
    let customersWithBoilers = 0;
    
    sales.forEach(sale => {
      sale.appliances.forEach(appliance => {
        totalApplianceCosts += appliance.cost;
        applianceCount++;
      });
      
      if (sale.boilerCoverSelected && sale.boilerPriceSelected) {
        totalBoilerCosts += sale.boilerPriceSelected;
        customersWithBoilers++;
      }
    });
    
    console.log('=== CURRENT PRICING BREAKDOWN ===');
    console.log(`Total appliance costs: £${totalApplianceCosts.toFixed(2)}`);
    console.log(`Total boiler costs: £${totalBoilerCosts.toFixed(2)}`);
    console.log(`Average appliance cost: £${(totalApplianceCosts / applianceCount).toFixed(2)}`);
    console.log(`Average boiler cost: £${(totalBoilerCosts / customersWithBoilers).toFixed(2)}`);
    console.log(`Customers with boilers: ${customersWithBoilers} out of ${sales.length}\n`);
    
    // If we want to get to £70K total, we need to reduce pricing
    const reductionNeeded = currentTotal - targetSystemTotal;
    const reductionPercentage = reductionNeeded / currentTotal;
    
    console.log(`Reduction needed: £${reductionNeeded.toFixed(2)}`);
    console.log(`Reduction percentage: ${(reductionPercentage * 100).toFixed(1)}%\n`);
    
    // Let me check if there's a pattern in the original pricing that we should restore
    console.log('=== CHECKING FOR PATTERNS ===');
    
    // Check for appliances that might have been incorrectly priced
    const applianceCostGroups = new Map();
    sales.forEach(sale => {
      sale.appliances.forEach(appliance => {
        const key = appliance.appliance;
        if (!applianceCostGroups.has(key)) {
          applianceCostGroups.set(key, []);
        }
        applianceCostGroups.get(key).push(appliance.cost);
      });
    });
    
    // Show appliances with suspicious high costs
    console.log('Appliances with potentially inflated costs:');
    Array.from(applianceCostGroups.entries()).forEach(([name, costs]) => {
      const uniqueCosts = [...new Set(costs)].sort((a, b) => a - b);
      const maxCost = Math.max(...costs);
      const avgCost = costs.reduce((sum, cost) => sum + cost, 0) / costs.length;
      
      if (maxCost > 15 || avgCost > 10) {
        console.log(`${name}: avg £${avgCost.toFixed(2)}, max £${maxCost.toFixed(2)}, costs: [£${uniqueCosts.slice(0, 5).join(', £')}${uniqueCosts.length > 5 ? '...' : ''}]`);
      }
    });

  } catch (error) {
    console.error('Error analyzing pricing:', error);
  } finally {
    await prisma.$disconnect();
  }
}

restoreOriginalPricing();